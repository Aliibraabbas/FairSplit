import api from '../api/axiosConfig'

const authService = {
  register: async (userData) => {
    const response = await api.post('/auth/register/', userData)
    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
    }
    return response.data
  },

  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials)
    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
    }
    return response.data
  },

  logout: async () => {
    try {
      await api.post('/auth/logout/')
    } finally {
      localStorage.removeItem('token')
    }
  },

  getCurrentUser: () => api.get('/auth/user/'),

  isAuthenticated: () => !!localStorage.getItem('token'),
}

export default authService
