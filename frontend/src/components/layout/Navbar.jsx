import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <Link to={user ? '/dashboard' : '/'} className="navbar-brand">
        💸 FairSplit
      </Link>
      <div className="navbar-links">
        {user ? (
          <>
            <Link to="/groups">Groupes</Link>
            <span className="navbar-user">👤 {user.username}</span>
            <button className="btn-logout" onClick={handleLogout}>Déconnexion</button>
          </>
        ) : (
          <>
            <Link to="/login">Connexion</Link>
            <Link to="/register" className="btn-primary">S'inscrire</Link>
          </>
        )}
      </div>
    </nav>
  )
}
