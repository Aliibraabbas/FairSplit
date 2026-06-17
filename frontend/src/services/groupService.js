import axiosInstance from '../api/axiosConfig'

export const groupService = {
  getGroups: async () => {
    const response = await axiosInstance.get('/groups/')
    return response.data
  },

  getGroup: async (id) => {
    const response = await axiosInstance.get(`/groups/${id}/`)
    return response.data
  },

  createGroup: async (groupData) => {
    const response = await axiosInstance.post('/groups/', groupData)
    return response.data
  },

  updateGroup: async (id, groupData) => {
    const response = await axiosInstance.put(`/groups/${id}/`, groupData)
    return response.data
  },

  deleteGroup: async (id) => {
    const response = await axiosInstance.delete(`/groups/${id}/`)
    return response.data
  },
}
