import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import groupService from '../../services/groupService'
import expenseService from '../../services/expenseService'
import Loader from '../../components/common/Loader'

const CATEGORIES = [
  { value: 'food', label: 'Nourriture' },
  { value: 'transport', label: 'Transport' },
  { value: 'accommodation', label: 'Hébergement' },
  { value: 'entertainment', label: 'Divertissement' },
  { value: 'shopping', label: 'Shopping' },
  { value: 'other', label: 'Autre' },
]

const today = new Date().toISOString().split('T')[0]

export default function ExpenseFormPage() {
  const { groupId, expenseId } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const isEdit = !!expenseId

  const [group, setGroup] = useState(null)
  const [form, setForm] = useState({
    title: '',
    amount: '',
    paid_by: '',
    participants: [],
    guest_participants: [],
    date: today,
    category: 'other',
    description: '',
    split_type: 'equal',
    custom_shares: [],
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      const g = await groupService.getGroup(groupId)
      setGroup(g)
      if (isEdit) {
        const e = await expenseService.getExpense(groupId, expenseId)
        setForm({
          title: e.title,
          amount: e.amount,
          paid_by: e.paid_by,
          participants: e.participants,
          guest_participants: e.guest_participants || [],
          date: e.date,
          category: e.category,
          description: e.description || '',
          split_type: e.split_type || 'equal',
          custom_shares: e.custom_shares_detail || [],
        })
      } else {
        setForm((f) => ({
          ...f,
          paid_by: user.id,
          participants: g.members.map((m) => m.id),
          guest_participants: g.guest_members?.map((gm) => gm.id) || [],
        }))
      }
      setLoading(false)
    }
    load().catch(() => { setError('Erreur de chargement'); setLoading(false) })
  }, [groupId, expenseId])

  const toggleParticipant = (userId) => {
    setForm((f) => ({
      ...f,
      participants: f.participants.includes(userId)
        ? f.participants.filter((id) => id !== userId)
        : [...f.participants, userId],
    }))
  }

  const toggleGuestParticipant = (guestId) => {
    setForm((f) => ({
      ...f,
      guest_participants: f.guest_participants.includes(guestId)
        ? f.guest_participants.filter((id) => id !== guestId)
        : [...f.guest_participants, guestId],
    }))
  }

  const totalParticipants = form.participants.length + form.guest_participants.length

  // Initialiser les custom_shares quand on passe en mode custom
  const initializeCustomShares = () => {
    const shares = []
    form.participants.forEach(userId => {
      shares.push({ user_id: userId, guest_id: null, amount: '' })
    })
    form.guest_participants.forEach(guestId => {
      shares.push({ user_id: null, guest_id: guestId, amount: '' })
    })
    setForm({ ...form, custom_shares: shares })
  }

  const handleSplitTypeChange = (e) => {
    const newType = e.target.value
    setForm({ ...form, split_type: newType })
    if (newType === 'custom' && form.custom_shares.length === 0) {
      initializeCustomShares()
    }
  }

  const updateCustomShare = (index, amount) => {
    const newShares = [...form.custom_shares]
    newShares[index].amount = amount
    setForm({ ...form, custom_shares: newShares })
  }

  const getParticipantName = (share) => {
    if (share.user_id) {
      const member = group?.members.find(m => m.id === share.user_id)
      return member?.username || `User ${share.user_id}`
    }
    if (share.guest_id) {
      const guest = group?.guest_members?.find(g => g.id === share.guest_id)
      return guest?.name || `Guest ${share.guest_id}`
    }
    return 'Inconnu'
  }

  const calculateCustomSharesTotal = () => {
    return form.custom_shares.reduce((sum, share) => {
      const amount = parseFloat(share.amount) || 0
      return sum + amount
    }, 0)
  }

  const customSharesTotal = calculateCustomSharesTotal()
  const expenseAmount = parseFloat(form.amount) || 0
  const remainingAmount = expenseAmount - customSharesTotal
  const isCustomSharesValid = Math.abs(remainingAmount) < 0.01

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (form.split_type === 'equal') {
      if (form.participants.length === 0 && form.guest_participants.length === 0) {
        setError('Sélectionnez au moins un participant')
        return
      }
    } else {
      // Mode custom
      if (form.custom_shares.length === 0) {
        setError('Ajoutez au moins un participant avec un montant')
        return
      }
      if (!isCustomSharesValid) {
        setError(`Le total des parts (${customSharesTotal.toFixed(2)}${group.currency_symbol}) doit être égal au montant total (${expenseAmount.toFixed(2)}${group.currency_symbol})`)
        return
      }
    }
    
    setSaving(true)
    setError('')
    try {
      const payload = { ...form }
      if (form.split_type === 'custom') {
        // Envoyer seulement les custom_shares, pas participants
        delete payload.participants
        delete payload.guest_participants
      } else {
        // Mode equal, supprimer custom_shares
        delete payload.custom_shares
      }
      
      if (isEdit) {
        await expenseService.updateExpense(groupId, expenseId, payload)
      } else {
        await expenseService.createExpense(groupId, payload)
      }
      navigate(`/groups/${groupId}`)
    } catch (err) {
      const data = err.response?.data
      setError(data ? Object.values(data).flat().join(' ') : 'Erreur lors de l\'enregistrement')
    } finally {
      setSaving(false)
    }
  }

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  if (loading) return <Loader />

  return (
    <div className="page-container page-narrow">
      <div className="section-header">
        <h1>{isEdit ? 'Modifier la dépense' : 'Nouvelle dépense'}</h1>
        <Link to={`/groups/${groupId}`} className="btn-secondary">Annuler</Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="card">
        <div className="form-group">
          <label>Titre *</label>
          <input type="text" value={form.title} onChange={set('title')} placeholder="Ex: Restaurant" required />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Montant ({group.currency_symbol}) *</label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={form.amount}
              onChange={set('amount')}
              placeholder="0.00"
              required
            />
          </div>
          <div className="form-group">
            <label>Date *</label>
            <input type="date" value={form.date} onChange={set('date')} required />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Payé par *</label>
            <select value={form.paid_by} onChange={set('paid_by')} required>
              {group?.members.map((m) => (
                <option key={m.id} value={m.id}>{m.username}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Catégorie</label>
            <select value={form.category} onChange={set('category')}>
              {CATEGORIES.map((c) => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Type de répartition *</label>
          <select value={form.split_type} onChange={handleSplitTypeChange}>
            <option value="equal">Répartition égale</option>
            <option value="custom">Répartition personnalisée</option>
          </select>
        </div>

        {form.split_type === 'equal' ? (
          <div className="form-group">
            <label>Participants *</label>
            <div className="checkbox-group">
              {group?.members.map((m) => (
                <label key={`u-${m.id}`} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={form.participants.includes(m.id)}
                    onChange={() => toggleParticipant(m.id)}
                  />
                  {m.username}
                </label>
              ))}
              {group?.guest_members?.map((gm) => (
                <label key={`g-${gm.id}`} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={form.guest_participants.includes(gm.id)}
                    onChange={() => toggleGuestParticipant(gm.id)}
                  />
                  {gm.name} <span style={{ fontSize: '0.75rem', color: '#92400e', marginLeft: '4px' }}>invité</span>
                </label>
              ))}
            </div>
            {totalParticipants > 0 && form.amount && (
              <p className="share-hint">
                Part par personne : {(parseFloat(form.amount) / totalParticipants).toFixed(2)} {group.currency_symbol}
              </p>
            )}
          </div>
        ) : (
          <div className="form-group">
            <label>Parts personnalisées *</label>
            {form.custom_shares.length === 0 ? (
              <p className="hint-text">Sélectionnez d'abord les participants en mode égal, puis passez en mode personnalisé.</p>
            ) : (
              <div className="custom-shares-list">
                {form.custom_shares.map((share, index) => (
                  <div key={index} className="custom-share-item">
                    <span className="participant-name">{getParticipantName(share)}</span>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      value={share.amount}
                      onChange={(e) => updateCustomShare(index, e.target.value)}
                      placeholder="0.00"
                      required
                    />
                    <span>{group.currency_symbol}</span>
                  </div>
                ))}
                <div className="custom-shares-summary">
                  <div className="summary-row">
                    <span>Total des parts :</span>
                    <strong>{customSharesTotal.toFixed(2)} {group.currency_symbol}</strong>
                  </div>
                  <div className="summary-row">
                    <span>Montant de la dépense :</span>
                    <strong>{expenseAmount.toFixed(2)} {group.currency_symbol}</strong>
                  </div>
                  <div className={`summary-row ${isCustomSharesValid ? 'valid' : 'invalid'}`}>
                    <span>Restant à répartir :</span>
                    <strong>{remainingAmount.toFixed(2)} {group.currency_symbol}</strong>
                  </div>
                  {!isCustomSharesValid && expenseAmount > 0 && (
                    <p className="error-text">⚠️ Le total des parts doit être égal au montant de la dépense</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="form-group">
          <label>Description</label>
          <textarea value={form.description} onChange={set('description')} rows={2} placeholder="Optionnel..." />
        </div>

        <button type="submit" className="btn-primary btn-full" disabled={saving}>
          {saving ? 'Enregistrement...' : (isEdit ? 'Modifier' : 'Ajouter la dépense')}
        </button>
      </form>
    </div>
  )
}
