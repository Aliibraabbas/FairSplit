import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import groupService from '../../services/groupService'
import Loader from '../../components/common/Loader'

export default function GroupListPage() {
  const [groups, setGroups] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    groupService.getGroups()
      .then((data) => setGroups(data.results ?? data))
      .catch(() => setError('Impossible de charger les groupes'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Loader />

  return (
    <div className="page-container">
      <div className="section-header">
        <h1>Mes groupes</h1>
        <Link to="/groups/new" className="btn-primary">+ Nouveau groupe</Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      {groups.length === 0 ? (
        <div className="empty-state">
          <p>Vous n'avez encore aucun groupe.</p>
          <Link to="/groups/new" className="btn-primary">Créer votre premier groupe</Link>
        </div>
      ) : (
        <div className="groups-grid">
          {groups.map((group) => (
            <Link to={`/groups/${group.id}`} key={group.id} className="group-card">
              <h3>{group.name}</h3>
              {group.description && <p className="card-description">{group.description}</p>}
              <div className="card-meta">
                <span>👥 {group.member_count} membre{group.member_count > 1 ? 's' : ''}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
