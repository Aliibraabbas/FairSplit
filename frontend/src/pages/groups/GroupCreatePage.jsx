import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import groupService from '../../services/groupService'

const CURRENCIES = [
  { value: 'EUR', label: 'Euro (€)' },
  { value: 'USD', label: 'Dollar américain ($)' },
  { value: 'GBP', label: 'Livre sterling (£)' },
  { value: 'LBP', label: 'Livre libanaise' },
]

export default function GroupCreatePage() {
  const [form, setForm] = useState({ name: '', description: '', currency: 'EUR' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const group = await groupService.createGroup(form)
      navigate(`/groups/${group.id}`)
    } catch (err) {
      setError(err.response?.data?.name?.[0] || 'Erreur lors de la création')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container page-narrow">
      <div className="section-header">
        <h1>Nouveau groupe</h1>
        <Link to="/groups" className="btn-secondary">Annuler</Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="card">
        <div className="form-group">
          <label>Nom du groupe *</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="Ex: Vacances Ibiza 2025"
            required
          />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            placeholder="Description optionnelle..."
            rows={3}
          />
        </div>
        <div className="form-group">
          <label>Devise *</label>
          <select
            value={form.currency}
            onChange={(e) => setForm({ ...form, currency: e.target.value })}
            required
          >
            {CURRENCIES.map((currency) => (
              <option key={currency.value} value={currency.value}>
                {currency.label}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn-primary btn-full" disabled={loading}>
          {loading ? 'Création...' : 'Créer le groupe'}
        </button>
      </form>
    </div>
  )
}
