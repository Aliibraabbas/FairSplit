import { useEffect, useState, useRef } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import groupService from '../../services/groupService'
import expenseService from '../../services/expenseService'
import Loader from '../../components/common/Loader'

export default function GroupDetailPage() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [group, setGroup] = useState(null)
  const [expenses, setExpenses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [addMemberUsername, setAddMemberUsername] = useState('')
  const [memberError, setMemberError] = useState('')
  const [activeTab, setActiveTab] = useState('expenses')
  const [suggestions, setSuggestions] = useState([])
  const searchTimeout = useRef(null)
  const [showInviteModal, setShowInviteModal] = useState(false)
  const [invitationLink, setInvitationLink] = useState('')
  const [copied, setCopied] = useState(false)
  const [exportingCsv, setExportingCsv] = useState(false)
  const [exportingExcel, setExportingExcel] = useState(false)

  const handleMemberInputChange = (e) => {
    const val = e.target.value
    setAddMemberUsername(val)
    setMemberError('')
    clearTimeout(searchTimeout.current)
    if (val.trim().length === 0) {
      setSuggestions([])
      return
    }
    searchTimeout.current = setTimeout(async () => {
      try {
        const results = await groupService.searchUsers(val.trim())
        const existingIds = new Set(group?.members?.map((m) => m.id) || [])
        const filtered = results.filter((u) => !existingIds.has(u.id))
        setSuggestions(filtered)
      } catch {
        setSuggestions([])
      }
    }, 250)
  }

  const handleSelectSuggestion = async (username) => {
    setMemberError('')
    setSuggestions([])
    setAddMemberUsername('')
    try {
      await groupService.addMember(id, username)
      const g = await groupService.getGroup(id)
      setGroup(g)
    } catch (err) {
      setMemberError(err.response?.data?.error || 'Erreur lors de l\'ajout')
    }
  }

  const loadData = async () => {
    try {
      const [g, e] = await Promise.all([
        groupService.getGroup(id),
        expenseService.getExpenses(id),
      ])
      setGroup(g)
      setExpenses(e.results || e)
    } catch {
      setError('Impossible de charger le groupe')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadData() }, [id])

  const handleAddMember = async (e) => {
    e.preventDefault()
    setMemberError('')
    setSuggestions([])
    try {
      await groupService.addMember(id, addMemberUsername)
      setAddMemberUsername('')
      const g = await groupService.getGroup(id)
      setGroup(g)
    } catch (err) {
      setMemberError(err.response?.data?.error || 'Erreur lors de l\'ajout')
    }
  }

  const handleRemoveGuest = async (guestId) => {
    if (!confirm('Retirer cet invité du groupe ?')) return
    try {
      await groupService.removeGuest(id, guestId)
      const g = await groupService.getGroup(id)
      setGroup(g)
    } catch (err) {
      alert(err.response?.data?.error || 'Erreur')
    }
  }

  const handleRemoveMember = async (userId) => {
    if (!confirm('Retirer ce membre du groupe ?')) return
    try {
      await groupService.removeMember(id, userId)
      const g = await groupService.getGroup(id)
      setGroup(g)
    } catch (err) {
      alert(err.response?.data?.error || 'Erreur')
    }
  }

  const handleDeleteExpense = async (expenseId) => {
    if (!confirm('Supprimer cette dépense ?')) return
    try {
      await expenseService.deleteExpense(id, expenseId)
      setExpenses(expenses.filter((e) => e.id !== expenseId))
    } catch {
      alert('Erreur lors de la suppression')
    }
  }

  const handleDeleteGroup = async () => {
    if (!confirm('Supprimer définitivement ce groupe et toutes ses dépenses ?')) return
    try {
      await groupService.deleteGroup(id)
      navigate('/groups')
    } catch (err) {
      alert(err.response?.data?.error || 'Erreur lors de la suppression')
    }
  }

  const handleExportCsv = async () => {
    setExportingCsv(true)
    try {
      await groupService.exportCsv(id)
    } catch (err) {
      alert('Erreur lors de l\'export CSV')
    } finally {
      setExportingCsv(false)
    }
  }

  const handleExportExcel = async () => {
    setExportingExcel(true)
    try {
      await groupService.exportExcel(id)
    } catch (err) {
      alert('Erreur lors de l\'export Excel')
    } finally {
      setExportingExcel(false)
    }
  }

  const handleCreateInvitation = async () => {
    try {
      const invitation = await groupService.createInvitation(id, { days_valid: 7, max_uses: 0 })
      const link = `${window.location.origin}/invite/${invitation.token}`
      setInvitationLink(link)
      setShowInviteModal(true)
    } catch (err) {
      alert('Erreur lors de la création de l\'invitation')
    }
  }

  const handleCopyLink = () => {
    navigator.clipboard.writeText(invitationLink)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const totalExpenses = expenses.reduce((sum, e) => sum + parseFloat(e.amount), 0)
  const isCreator = group?.created_by?.id === user?.id

  if (loading) return <Loader />
  if (error) return <div className="page-container"><div className="error-message">{error}</div></div>

  return (
    <div className="page-container">
      <div className="section-header">
        <div>
          <h1>{group.name}</h1>
          {group.description && <p className="subtitle">{group.description}</p>}
        </div>
        <div className="header-actions">
          <button onClick={handleExportCsv} className="btn-secondary" disabled={exportingCsv}>
            {exportingCsv ? 'Export CSV...' : 'Export CSV'}
          </button>
          <button onClick={handleExportExcel} className="btn-secondary" disabled={exportingExcel}>
            {exportingExcel ? 'Export Excel...' : 'Export Excel'}
          </button>
          <Link to={`/groups/${id}/balances`} className="btn-secondary">Soldes</Link>
          <Link to={`/groups/${id}/expenses/new`} className="btn-primary">+ Dépense</Link>
        </div>
      </div>

      <div className="tabs">
        <button
          className={activeTab === 'expenses' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('expenses')}
        >
          Dépenses ({expenses.length})
        </button>
        <button
          className={activeTab === 'members' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('members')}
        >
          Membres ({group.members.length})
        </button>
      </div>

      {activeTab === 'expenses' && (
        <div>
          {expenses.length === 0 ? (
            <div className="empty-state">
              <p>Aucune dépense pour l'instant.</p>
              <Link to={`/groups/${id}/expenses/new`} className="btn-primary">
                Ajouter la première dépense
              </Link>
            </div>
          ) : (
            <>
              <div className="total-bar">
                Total du groupe : <strong>{totalExpenses.toFixed(2)} {group.currency_symbol}</strong>
              </div>
              <div className="expense-list">
                {expenses.map((expense) => (
                  <div key={expense.id} className="expense-item">
                    <div className="expense-main">
                      <div>
                        <span className="expense-title">{expense.title}</span>
                        <span className="expense-category">{expense.category_display}</span>
                      </div>
                      <span className="expense-amount">{parseFloat(expense.amount).toFixed(2)} {expense.currency_symbol}</span>
                    </div>
                    <div className="expense-meta">
                      <span>Payé par <strong>{expense.paid_by_detail?.username}</strong></span>
                      <span>{expense.date}</span>
                    </div>
                    <div className="expense-participants">
                      Participants : {[
                        ...(expense.participants_detail?.map((p) => p.username) || []),
                        ...(expense.guest_participants_detail?.map((g) => g.name) || []),
                      ].join(', ')}
                    </div>
                    <div className="expense-actions">
                      <Link to={`/groups/${id}/expenses/${expense.id}/edit`} className="btn-sm">
                        Modifier
                      </Link>
                      <button className="btn-sm btn-danger" onClick={() => handleDeleteExpense(expense.id)}>
                        Supprimer
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {activeTab === 'members' && (
        <div>
          <ul className="member-list">
            {group.members.map((member) => (
              <li key={`u-${member.id}`} className="member-item">
                <span>
                  <strong>{member.username}</strong>
                  {member.id === group.created_by.id && <span className="badge">Créateur</span>}
                </span>
                {isCreator && member.id !== user.id && (
                  <button className="btn-sm btn-danger" onClick={() => handleRemoveMember(member.id)}>
                    Retirer
                  </button>
                )}
              </li>
            ))}
            {group.guest_members?.map((guest) => (
              <li key={`g-${guest.id}`} className="member-item">
                <span>
                  <strong>{guest.name}</strong>
                  <span className="badge badge-guest">Invité</span>
                </span>
                {isCreator && (
                  <button className="btn-sm btn-danger" onClick={() => handleRemoveGuest(guest.id)}>
                    Retirer
                  </button>
                )}
              </li>
            ))}
          </ul>

          <div className="add-member-section">
            <button onClick={handleCreateInvitation} className="btn-secondary btn-full" style={{ marginBottom: '1rem' }}>
              Créer un lien d'invitation
            </button>
          </div>

          <form onSubmit={handleAddMember} className="add-member-form">
            <h3>Ajouter un membre</h3>
            {memberError && <div className="error-message">{memberError}</div>}
            <div className="form-inline">
              <input
                type="text"
                value={addMemberUsername}
                onChange={handleMemberInputChange}
                placeholder="Rechercher ou saisir un nom"
                required
                autoComplete="off"
              />
              <button type="submit" className="btn-primary">Ajouter</button>
            </div>
            {suggestions.length > 0 && (
              <ul className="suggestion-list">
                {suggestions.map((u) => (
                  <li key={u.id} className="suggestion-item">
                    <span>{u.username}</span>
                    <button
                      type="button"
                      className="btn-sm btn-primary-outline"
                      onClick={() => handleSelectSuggestion(u.username)}
                    >
                      Ajouter
                    </button>
                  </li>
                ))}
              </ul>
            )}
            {addMemberUsername.trim() && !suggestions.find((s) => s.username === addMemberUsername.trim()) && (
              <p className="hint-text">
                "{addMemberUsername.trim()}" n'est pas inscrit — sera ajouté comme invité.
              </p>
            )}
          </form>

          {isCreator && (
            <div className="danger-zone">
              <h3>Zone dangereuse</h3>
              <button className="btn-danger" onClick={handleDeleteGroup}>
                Supprimer ce groupe
              </button>
            </div>
          )}
        </div>
      )}

      {showInviteModal && (
        <div className="modal-overlay" onClick={() => setShowInviteModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Lien d'invitation</h2>
              <button className="modal-close" onClick={() => setShowInviteModal(false)}>×</button>
            </div>
            <p>Partagez ce lien pour inviter des personnes à rejoindre le groupe :</p>
            <div className="invitation-link-box">{invitationLink}</div>
            <button 
              className={`btn-copy ${copied ? 'copied' : ''}`}
              onClick={handleCopyLink}
            >
              {copied ? 'Copié !' : 'Copier le lien'}
            </button>
            <p className="hint-text" style={{ marginTop: '1rem' }}>
              Ce lien est valide pendant 7 jours et peut être utilisé un nombre illimité de fois.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
