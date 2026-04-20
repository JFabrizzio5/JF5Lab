import { defineStore } from 'pinia'
import { auth as authApi } from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  getters: {
    isAuthenticated: (s) => !!s.token
  },
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const { data } = await authApi.login({ email, password })
        this.token = data.access_token
        this.user = data.user
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
      } catch (e) {
        this.error = e.response?.data?.detail || 'Error al iniciar sesión'
        throw e
      } finally {
        this.loading = false
      }
    },
    async register(email, password, name, phone) {
      this.loading = true
      this.error = null
      try {
        const { data } = await authApi.register({ email, password, name, phone })
        this.token = data.access_token
        this.user = data.user
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
      } catch (e) {
        this.error = e.response?.data?.detail || 'Error al registrarse'
        throw e
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
