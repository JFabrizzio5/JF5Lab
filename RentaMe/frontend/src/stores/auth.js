import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('rentame_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('rentame_user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const role = computed(() => user.value?.role || null)
  const isVendor = computed(() => role.value === 'vendor')
  const isAdmin = computed(() => role.value === 'superadmin')

  function setAuth(data) {
    token.value = data.access_token
    user.value = {
      id: data.user_id,
      name: data.name,
      role: data.role,
    }
    localStorage.setItem('rentame_token', data.access_token)
    localStorage.setItem('rentame_user', JSON.stringify(user.value))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('rentame_token')
    localStorage.removeItem('rentame_user')
  }

  async function login(email, password) {
    const res = await authAPI.login({ email, password })
    setAuth(res.data)
    return res.data
  }

  async function register(data) {
    const res = await authAPI.register(data)
    setAuth(res.data)
    return res.data
  }

  const roleHome = {
    superadmin: '/admin',
    vendor: '/vendor/dashboard',
    customer: '/',
  }

  function getHome() {
    return roleHome[role.value] || '/'
  }

  return { token, user, isLoggedIn, role, isVendor, isAdmin, login, register, logout, getHome }
})
