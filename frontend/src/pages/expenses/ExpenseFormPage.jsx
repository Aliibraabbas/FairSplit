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

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.participants.length === 0 && form.guest_participants.length === 0) {
      setError('Sélectionnez au moins un participant')
      return
    }
    setSaving(true)
    setError('')
    try {
      if (isEdit) {
        await expenseService.updateExpense(groupId, expenseId, form)
      } else {
        await expenseService.createExpense(groupId, form)
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
            <label>Montant (€) *</label>
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
              Part par personne : {(parseFloat(form.amount) / totalParticipants).toFixed(2)} €
            </p>
          )}
        </div>

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
