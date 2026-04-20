import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isOrganizer = computed(() => user.value?.role === 'organizer' || user.value?.role === 'superadmin')
  const isAdmin = computed(() => user.value?.role === 'superadmin')

  function setAuth(data) {
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function login(email, password) {
    const form = new FormData()
    form.append('username', email)
    form.append('password', password)
    const { data } = await api.post('/auth/login', form)
    setAuth(data)
    return data.user
  }

  async function register(email, name, password, role = 'attendee') {
    const { data } = await api.post('/auth/register', { email, name, password, role })
    setAuth(data)
    return data.user
  }

  return { token, user, isLoggedIn, isOrganizer, isAdmin, login, register, logout, setAuth }
})
