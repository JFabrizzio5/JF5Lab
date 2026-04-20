import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('servilink_user') || 'null'))
  const token = ref(localStorage.getItem('servilink_token') || null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'superadmin')
  const isFreelancer = computed(() => user.value?.role === 'freelancer')
  const isClient = computed(() => user.value?.role === 'client')

  async function login(email, password) {
    const { data } = await authApi.login(email, password)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('servilink_token', data.access_token)
    localStorage.setItem('servilink_user', JSON.stringify(data.user))
    return data.user
  }

  async function register(formData) {
    const { data } = await authApi.register(formData)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('servilink_token', data.access_token)
    localStorage.setItem('servilink_user', JSON.stringify(data.user))
    return data.user
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('servilink_token')
    localStorage.removeItem('servilink_user')
  }

  return { user, token, isLoggedIn, isAdmin, isFreelancer, isClient, login, register, logout }
})
