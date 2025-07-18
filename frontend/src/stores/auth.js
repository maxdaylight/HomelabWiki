import api from '@/services/api'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)
  
  const login = async (credentials) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/login', credentials)
      user.value = response.data.user
      return { success: true, message: response.data.message }
    } catch (err) {
      error.value = err.response?.data?.error || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }
  
  const logout = async () => {
    isLoading.value = true
    
    try {
      await api.post('/auth/logout')
      user.value = null
      return { success: true }
    } catch (err) {
      // Even if logout fails, clear local user
      user.value = null
      return { success: false, error: err.response?.data?.error || 'Logout failed' }
    } finally {
      isLoading.value = false
    }
  }
  
  const checkAuth = async () => {
    isLoading.value = true
    
    try {
      const response = await api.get('/auth/check')
      if (response.data.authenticated) {
        user.value = response.data.user
      } else {
        user.value = null
      }
      return response.data.authenticated
    } catch (err) {
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  const getCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me')
      user.value = response.data.user
      return user.value
    } catch (err) {
      user.value = null
      throw err
    }
  }
  
  const hasPermission = (permission) => {
    if (!user.value) return false
    
    const permissions = user.value.permissions || {}
    
    switch (permission) {
      case 'read':
        return true // All authenticated users can read
      case 'create':
        return permissions.can_create || false
      case 'edit':
        return permissions.can_edit || false
      case 'delete':
        return permissions.can_delete || isAdmin.value
      case 'upload':
        return permissions.can_upload || false
      case 'admin':
        return isAdmin.value
      default:
        return false
    }
  }
  
  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    checkAuth,
    getCurrentUser,
    hasPermission
  }
})
