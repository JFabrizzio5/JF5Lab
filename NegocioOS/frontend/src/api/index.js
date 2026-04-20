import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Request interceptor — attach Bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('negocio_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — 401 → soft redirect (skip auth endpoints + if already on login → avoids reload loop)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || ''
    const isAuthCall = url.includes('/auth/login') || url.includes('/auth/register')
    const alreadyOnLogin = window.location.pathname === '/login'
    if (error.response?.status === 401 && !isAuthCall && !alreadyOnLogin) {
      localStorage.removeItem('negocio_token')
      localStorage.removeItem('negocio_user')
      window.history.pushState({}, '', '/login')
      window.dispatchEvent(new PopStateEvent('popstate'))
    }
    return Promise.reject(error)
  }
)

export default api
