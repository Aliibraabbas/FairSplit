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
}

export default groupService
