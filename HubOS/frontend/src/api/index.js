import axios from 'axios'

const api = axios.create({ baseURL: '/api', timeout: 30000 })

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('hubos_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (error) => {
    const url = error.config?.url || ''
    const isAuthCall = url.includes('/auth/login') || url.includes('/auth/register')
    const alreadyOnLogin = window.location.pathname === '/login'
    if (error.response?.status === 401 && !isAuthCall && !alreadyOnLogin) {
      sessionStorage.removeItem('hubos_token')
      sessionStorage.removeItem('hubos_user')
      window.history.pushState({}, '', '/login')
      window.dispatchEvent(new PopStateEvent('popstate'))
    }
    return Promise.reject(error)
  }
)

export default api
