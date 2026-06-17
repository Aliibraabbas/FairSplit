import api from '../api/axiosConfig'

const groupService = {
  getGroups: () => api.get('/groups/').then((r) => r.data),
  getGroup: (id) => api.get(`/groups/${id}/`).then((r) => r.data),
  createGroup: (data) => api.post('/groups/', data).then((r) => r.data),
  updateGroup: (id, data) => api.put(`/groups/${id}/`, data).then((r) => r.data),
  deleteGroup: (id) => api.delete(`/groups/${id}/`),
  addMember: (groupId, username) =>
    api.post(`/groups/${groupId}/members/add/`, { username }).then((r) => r.data),
  removeMember: (groupId, userId) =>
    api.post(`/groups/${groupId}/members/remove/`, { user_id: userId }),
  removeGuest: (groupId, guestId) =>
    api.post(`/groups/${groupId}/guests/remove/`, { guest_id: guestId }),
  searchUsers: (q) =>
    api.get('/accounts/search/', { params: { q } }).then((r) => r.data),
  
  // Export CSV
  exportCsv: (groupId) => {
    return api.get(`/groups/${groupId}/export/csv/`, { responseType: 'blob' })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `fairsplit_group_${groupId}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      })
  },
  
  // Export Excel
  exportExcel: (groupId) => {
    return api.get(`/groups/${groupId}/export/xlsx/`, { responseType: 'blob' })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `fairsplit_group_${groupId}.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      })
  },
  
  // Invitations
  createInvitation: (groupId, data = {}) =>
    api.post(`/groups/${groupId}/invitations/create/`, data).then((r) => r.data),
  getInvitations: (groupId) =>
    api.get(`/groups/${groupId}/invitations/`).then((r) => r.data),
  getInvitationInfo: (token) =>
    api.get(`/groups/invitations/${token}/`).then((r) => r.data),
  joinInvitation: (token) =>
    api.post(`/groups/invitations/${token}/join/`).then((r) => r.data),
}

export default groupService
