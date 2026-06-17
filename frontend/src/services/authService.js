import axiosInstance from '../api/axiosConfig'

export const authService = {
  login: async (credentials) => {
    const response = await axiosInstance.post('/auth/login/', credentials)
    return response.data
  },

  register: async (userData) => {
    const response = await axiosInstance.post('/auth/register/', userData)
    return response.data
  },

  logout: async () => {
    const response = await axiosInstance.post('/auth/logout/')
    return response.data
  },

  getCurrentUser: async () => {
    const response = await axiosInstance.get('/auth/me/')
    return response.data
  },
}
