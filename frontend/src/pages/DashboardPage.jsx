import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import groupService from '../services/groupService'
import Loader from '../components/common/Loader'

export default function DashboardPage() {
  const { user } = useAuth()
  const [groups, setGroups] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    groupService.getGroups().then((data) => setGroups(data.results ?? data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <Loader />

  return (
    <div className="page-container">
      <h1>Bonjour, {user.username} 👋</h1>
      <p className="subtitle">Bienvenue sur FairSplit</p>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-number">{groups.length}</span>
          <span className="stat-label">Groupe{groups.length > 1 ? 's' : ''}</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">
            {groups.reduce((sum, g) => sum + g.member_count, 0)}
          </span>
          <span className="stat-label">Membres au total</span>
        </div>
      </div>

      <div className="section-header">
        <h2>Mes groupes récents</h2>
        <Link to="/groups" className="btn-primary">Voir tous</Link>
      </div>

      {groups.length === 0 ? (
        <div className="empty-state">
          <p>Vous n'avez pas encore de groupe.</p>
          <Link to="/groups/new" className="btn-primary">Créer un groupe</Link>
        </div>
      ) : (
        <div className="groups-grid">
          {groups.slice(0, 3).map((group) => (
            <Link to={`/groups/${group.id}`} key={group.id} className="group-card">
              <h3>{group.name}</h3>
              <p>{group.member_count} membre{group.member_count > 1 ? 's' : ''}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
