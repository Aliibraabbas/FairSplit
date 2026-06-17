import axiosInstance from '../api/axiosConfig'

export const expenseService = {
  getExpenses: async (groupId) => {
    const response = await axiosInstance.get(`/groups/${groupId}/expenses/`)
    return response.data
  },

  getExpense: async (id) => {
    const response = await axiosInstance.get(`/expenses/${id}/`)
    return response.data
  },

  createExpense: async (groupId, expenseData) => {
    const response = await axiosInstance.post(`/groups/${groupId}/expenses/`, expenseData)
    return response.data
  },

  updateExpense: async (id, expenseData) => {
    const response = await axiosInstance.put(`/expenses/${id}/`, expenseData)
    return response.data
  },

  deleteExpense: async (id) => {
    const response = await axiosInstance.delete(`/expenses/${id}/`)
    return response.data
  },
}
