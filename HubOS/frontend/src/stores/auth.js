import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/index.js'

// sessionStorage: persists across page reloads WITHIN a tab,
// auto-wipes when the tab closes. Perfect for public-server safety
// + good UX (reload doesn't kill WhatsApp session).
const store = sessionStorage

export const useAuthStore = defineStore('auth', () => {
  const token = ref(store.getItem('hubos_token') || null)
  const user = ref(JSON.parse(store.getItem('hubos_user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const workspaceId = computed(() => user.value?.workspace_id)

  function _persist(t, u) {
    token.value = t
    user.value = u
    if (t) store.setItem('hubos_token', t); else store.removeItem('hubos_token')
    if (u) store.setItem('hubos_user', JSON.stringify(u)); else store.removeItem('hubos_user')
  }

  async function login(email, password) {
    const { data } = await api.post('/auth/login', { email, password })
    _persist(data.access_token, data.user)
    return data
  }

  async function register(payload) {
    const { data } = await api.post('/auth/register', payload)
    _persist(data.access_token, data.user)
    return data
  }

  async function logout({ serverWipe = true } = {}) {
    if (serverWipe && token.value) {
      try { await api.post('/auth/logout') } catch {}
    }
    _persist(null, null)
  }

  return { token, user, isAuthenticated, workspaceId, login, register, logout }
})
