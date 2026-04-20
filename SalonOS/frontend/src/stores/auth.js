import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('salonos_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('salonos_user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const role = computed(() => user.value?.role || null)

  async function login(email, password) {
    const { data } = await api.post('/auth/login', { email, password })
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('salonos_token', data.access_token)
    localStorage.setItem('salonos_user', JSON.stringify(data.user))
    return data.user
  }

  async function register(payload) {
    const { data } = await api.post('/auth/register', payload)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('salonos_token', data.access_token)
    localStorage.setItem('salonos_user', JSON.stringify(data.user))
    return data.user
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('salonos_token')
    localStorage.removeItem('salonos_user')
  }

  return { token, user, isAuthenticated, role, login, register, logout }
})
