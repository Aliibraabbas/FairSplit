import api from '../api/axiosConfig'

const expenseService = {
  getExpenses: (groupId) => api.get(`/groups/${groupId}/expenses/`).then((r) => r.data),
  getExpense: (groupId, id) => api.get(`/groups/${groupId}/expenses/${id}/`).then((r) => r.data),
  createExpense: (groupId, data) => api.post(`/groups/${groupId}/expenses/`, data).then((r) => r.data),
  updateExpense: (groupId, id, data) =>
    api.put(`/groups/${groupId}/expenses/${id}/`, data).then((r) => r.data),
  deleteExpense: (groupId, id) => api.delete(`/groups/${groupId}/expenses/${id}/`),
}

export default expenseService
