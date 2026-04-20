import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('servilink_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('servilink_token')
      localStorage.removeItem('servilink_user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
}

export const profApi = {
  list: (params) => api.get('/professionals/', { params }),
  get: (id) => api.get(`/professionals/${id}`),
  updateProfile: (data) => api.put('/professionals/me/profile', data),
  myProfile: () => api.get('/professionals/me/profile'),
}

export const bookingApi = {
  create: (data) => api.post('/bookings/', data),
  list: () => api.get('/bookings/'),
  updateStatus: (id, status) => api.patch(`/bookings/${id}/status`, null, { params: { status } }),
}

export const reviewApi = {
  create: (data) => api.post('/reviews/', data),
  forProfessional: (userId) => api.get(`/reviews/professional/${userId}`),
}

export const categoryApi = {
  list: () => api.get('/categories/'),
  create: (data) => api.post('/categories/', data),
  update: (id, data) => api.put(`/categories/${id}`, data),
  delete: (id) => api.delete(`/categories/${id}`),
}

export const subApi = {
  plans: () => api.get('/subscriptions/plans'),
  me: () => api.get('/subscriptions/me'),
  subscribe: (plan) => api.post('/subscriptions/subscribe', { plan }),
  all: () => api.get('/subscriptions/all'),
}

export const adminApi = {
  stats: () => api.get('/admin/stats'),
  users: () => api.get('/admin/users'),
  toggleUser: (id) => api.patch(`/admin/users/${id}/toggle`),
  bookings: () => api.get('/admin/bookings'),
}

export const chatApi = {
  getOrCreateRoom: (professionalUserId) => api.get(`/chat/room/${professionalUserId}`),
  listRooms: () => api.get('/chat/rooms'),
  getMessages: (roomId) => api.get(`/chat/rooms/${roomId}/messages`),
}

export const publicApi = {
  getProfile: (userId) => api.get(`/public/pro/${userId}`),
}

// WebSocket factory
export function createChatWS(roomId) {
  const token = localStorage.getItem('servilink_token')
  const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
  const host = window.location.host
  return new WebSocket(`${proto}://${host}/api/chat/ws/${roomId}?token=${token}`)
}

export default api
