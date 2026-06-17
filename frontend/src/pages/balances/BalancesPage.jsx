import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import groupService from '../../services/groupService'
import balanceService from '../../services/balanceService'
import Loader from '../../components/common/Loader'

export default function BalancesPage() {
  const { id } = useParams()
  const [group, setGroup] = useState(null)
  const [balances, setBalances] = useState([])
  const [settlements, setSettlements] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [guestBalances, setGuestBalances] = useState([])

  useEffect(() => {
    Promise.all([
      groupService.getGroup(id),
      balanceService.getBalances(id),
      balanceService.getSettlements(id),
    ])
      .then(([g, b, s]) => {
        setGroup(g)
        setBalances(b.members || [])
        setGuestBalances(b.guests || [])
        setSettlements(s)
      })
      .catch(() => setError('Impossible de charger les soldes'))
      .finally(() => setLoading(false))
  }, [id])

  const handleSettle = async (s) => {
    try {
      await balanceService.recordReimbursement(id, {
        from_type: s.from.type,
        from_id: s.from.id,
        to_id: s.to.id,
        amount: s.amount,
      })
      const [b, newSettlements] = await Promise.all([
        balanceService.getBalances(id),
        balanceService.getSettlements(id),
      ])
      setBalances(b.members || [])
      setGuestBalances(b.guests || [])
      setSettlements(newSettlements)
    } catch {
      alert('Erreur lors de l\'enregistrement du remboursement')
    }
  }

  if (loading) return <Loader />
  if (error) return <div className="page-container"><div className="error-message">{error}</div></div>

  return (
    <div className="page-container">
      <div className="section-header">
        <h1>Soldes — {group.name}</h1>
        <Link to={`/groups/${id}`} className="btn-secondary">← Retour</Link>
      </div>

      <section className="balances-section">
        <h2>Solde de chaque membre</h2>
        {balances.length === 0 ? (
          <p className="empty-text">Aucune dépense enregistrée.</p>
        ) : (
          <div className="balance-list">
            {balances.map((b) => (
              <div key={b.user.id} className={`balance-item ${parseFloat(b.balance) >= 0 ? 'positive' : 'negative'}`}>
                <span className="balance-user">{b.user.username}</span>
                <span className="balance-amount">
                  {parseFloat(b.balance) >= 0 ? '+' : ''}{parseFloat(b.balance).toFixed(2)} {group.currency_symbol}
                </span>
              </div>
            ))}
            {guestBalances.map((b) => (
              <div key={`g-${b.guest.id}`} className="balance-item negative">
                <span className="balance-user">
                  {b.guest.name}
                  <span className="badge badge-guest" style={{ marginLeft: '0.5rem' }}>Invité</span>
                </span>
                <span className="balance-amount">{parseFloat(b.balance).toFixed(2)} {group.currency_symbol}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="settlements-section">
        <h2>Remboursements suggérés</h2>
        {settlements.length === 0 ? (
          <p className="empty-text">Tout est équilibré 🎉</p>
        ) : (
          <div className="settlement-list">
            {settlements.map((s, i) => (
              <div key={i} className="settlement-item">
                <div className="settlement-info">
                  <span className="settlement-from">
                    {s.from.name}
                    {s.from.type === 'guest' && <span className="badge badge-guest" style={{ marginLeft: '0.4rem' }}>Invité</span>}
                  </span>
                  <span className="settlement-arrow">doit</span>
                  <span className="settlement-amount">{parseFloat(s.amount).toFixed(2)} {group.currency_symbol}</span>
                  <span className="settlement-arrow">à</span>
                  <span className="settlement-to">{s.to.name}</span>
                </div>
                <button
                  className="btn-sm btn-success"
                  onClick={() => handleSettle(s)}
                >
                  Réglé ✓
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
