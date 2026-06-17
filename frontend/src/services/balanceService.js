import api from '../api/axiosConfig'

const balanceService = {
  getBalances: (groupId) => api.get(`/groups/${groupId}/balances/`).then((r) => r.data),
  getSettlements: (groupId) => api.get(`/groups/${groupId}/balances/settlements/`).then((r) => r.data),
  recordReimbursement: (groupId, data) =>
    api.post(`/groups/${groupId}/balances/reimburse/`, data).then((r) => r.data),
}

export default balanceService
