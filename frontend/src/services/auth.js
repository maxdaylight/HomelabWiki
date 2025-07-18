import api from './api'

export const authService = {
  async login(credentials) {
    const response = await api.post('/api/auth/login', credentials)
    return response.data
  },
  
  async logout() {
    const response = await api.post('/api/auth/logout')
    return response.data
  },
  
  async checkAuth() {
    const response = await api.get('/api/auth/check')
    return response.data
  },
  
  async getCurrentUser() {
    const response = await api.get('/api/auth/me')
    return response.data
  },
  
  async testLdapConnection() {
    const response = await api.post('/api/auth/test-ldap')
    return response.data
  }
}

export default authService
