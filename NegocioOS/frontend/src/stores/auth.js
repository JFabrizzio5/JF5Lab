import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('negocio_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('negocio_user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isOwner = computed(() => user.value?.role === 'owner' || user.value?.role === 'admin')

  async function login(email, password) {
    const res = await api.post('/auth/login', { email, password })
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem('negocio_token', token.value)
    localStorage.setItem('negocio_user', JSON.stringify(user.value))
    return res.data
  }

  async function register(data) {
    const res = await api.post('/auth/register', data)
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem('negocio_token', token.value)
    localStorage.setItem('negocio_user', JSON.stringify(user.value))
    return res.data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('negocio_token')
    localStorage.removeItem('negocio_user')
  }

  return { token, user, isAuthenticated, isAdmin, isOwner, login, register, logout }
})
