import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import groupService from '../services/groupService'
import Loader from '../components/common/Loader'

export default function InvitePage() {
  const { token } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [invitation, setInvitation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [joining, setJoining] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const data = await groupService.getInvitationInfo(token)
        setInvitation(data)
      } catch (err) {
        setError('Invitation introuvable ou invalide')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [token])

  const handleJoin = async () => {
    setJoining(true)
    setError('')
    try {
      const result = await groupService.joinInvitation(token)
      navigate(`/groups/${result.group.id}`)
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la tentative de rejoindre le groupe')
    } finally {
      setJoining(false)
    }
  }

  if (loading) return <Loader />

  if (error) {
    return (
      <div className="invite-page">
        <div className="invite-card">
          <h1>Invitation invalide</h1>
          <p className="error-text">{error}</p>
          <div className="invite-actions">
            <Link to="/dashboard" className="btn-primary btn-full">
              Retour au tableau de bord
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="invite-page">
      <div className="invite-card">
        <h1>Invitation à rejoindre un groupe</h1>
        <div className="group-name">{invitation.group_name}</div>
        {invitation.group_description && (
          <p style={{ color: '#6b7280', marginTop: '0.5rem' }}>{invitation.group_description}</p>
        )}

        {invitation.is_valid ? (
          <div className="invite-status valid">
            Cette invitation est valide
          </div>
        ) : (
          <div className="invite-status invalid">
            Cette invitation a expiré
          </div>
        )}

        {invitation.max_uses && (
          <p className="hint-text">
            Utilisations : {invitation.uses_count} / {invitation.max_uses}
          </p>
        )}

        <div className="invite-actions">
          {!user ? (
            <>
              <p style={{ marginBottom: '1rem', color: '#6b7280' }}>
                Vous devez être connecté pour rejoindre ce groupe
              </p>
              <Link to="/login" className="btn-primary btn-full">
                Se connecter
              </Link>
              <Link to="/register" className="btn-secondary btn-full">
                Créer un compte
              </Link>
            </>
          ) : invitation.is_valid ? (
            <>
              <button 
                onClick={handleJoin} 
                className="btn-primary btn-full"
                disabled={joining}
              >
                {joining ? 'Rejoindre...' : 'Rejoindre le groupe'}
              </button>
              <Link to="/dashboard" className="btn-secondary btn-full">
                Annuler
              </Link>
            </>
          ) : (
            <Link to="/dashboard" className="btn-primary btn-full">
              Retour au tableau de bord
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}
