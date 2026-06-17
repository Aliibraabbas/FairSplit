import { Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from '../layouts/MainLayout'
import ProtectedRoute from '../components/common/ProtectedRoute'
import PublicRoute from '../components/common/PublicRoute'
import LoginPage from '../pages/LoginPage'
import RegisterPage from '../pages/RegisterPage'
import DashboardPage from '../pages/DashboardPage'
import GroupListPage from '../pages/groups/GroupListPage'
import GroupCreatePage from '../pages/groups/GroupCreatePage'
import GroupDetailPage from '../pages/groups/GroupDetailPage'
import ExpenseFormPage from '../pages/expenses/ExpenseFormPage'
import BalancesPage from '../pages/balances/BalancesPage'

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/groups" element={<ProtectedRoute><GroupListPage /></ProtectedRoute>} />
        <Route path="/groups/new" element={<ProtectedRoute><GroupCreatePage /></ProtectedRoute>} />
        <Route path="/groups/:id" element={<ProtectedRoute><GroupDetailPage /></ProtectedRoute>} />
        <Route path="/groups/:groupId/expenses/new" element={<ProtectedRoute><ExpenseFormPage /></ProtectedRoute>} />
        <Route path="/groups/:groupId/expenses/:expenseId/edit" element={<ProtectedRoute><ExpenseFormPage /></ProtectedRoute>} />
        <Route path="/groups/:id/balances" element={<ProtectedRoute><BalancesPage /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
