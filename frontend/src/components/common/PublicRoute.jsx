import { Navigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import Loader from './Loader'

export default function PublicRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <Loader />
  if (user) return <Navigate to="/dashboard" replace />
  return children
}
