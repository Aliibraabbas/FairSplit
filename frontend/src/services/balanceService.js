import axiosInstance from '../api/axiosConfig'

export const balanceService = {
  getBalances: async (groupId) => {
    const response = await axiosInstance.get(`/groups/${groupId}/balances/`)
    return response.data
  },

  getSettlements: async (groupId) => {
    const response = await axiosInstance.get(`/groups/${groupId}/settlements/`)
    return response.data
  },
}
