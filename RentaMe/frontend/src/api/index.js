import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('rentame_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('rentame_token')
      localStorage.removeItem('rentame_user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

// Auth
export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
}

// Vendor
export const vendorAPI = {
  getProfile: () => api.get('/vendors/me'),
  updateProfile: (data) => api.put('/vendors/me', data),
  getStats: () => api.get('/vendors/me/stats'),
}

// Items
export const itemsAPI = {
  list: () => api.get('/items/'),
  create: (data) => api.post('/items/', data),
  update: (id, data) => api.put(`/items/${id}`, data),
  delete: (id) => api.delete(`/items/${id}`),
}

// Availability
export const availabilityAPI = {
  list: () => api.get('/availability/'),
  create: (data) => api.post('/availability/', data),
  delete: (id) => api.delete(`/availability/${id}`),
}

// Bookings
export const bookingsAPI = {
  list: (status) => api.get('/bookings/', { params: status ? { status } : {} }),
  updateStatus: (id, status) => api.put(`/bookings/${id}/status`, { status }),
  updateNotes: (id, internal_notes) => api.put(`/bookings/${id}/notes`, { internal_notes }),
}

// Payments
export const paymentsAPI = {
  history: () => api.get('/payments/history'),
  connectStripe: () => api.post('/payments/stripe-connect'),
  createIntent: (data) => api.post('/payments/create-intent', data),
}

// Public
export const publicAPI = {
  getVendor: (slug) => api.get(`/public/vendor/${slug}`),
  createInquiry: (slug, data) => api.post(`/public/vendor/${slug}/inquiry`, data),
  getAvailability: (slug, params) => api.get(`/public/vendor/${slug}/availability`, { params }),
}

// Admin
export const adminAPI = {
  stats: () => api.get('/admin/stats'),
  vendors: () => api.get('/admin/vendors'),
  toggleVendor: (id) => api.put(`/admin/vendors/${id}/toggle`),
  setFee: (id, fee) => api.put(`/admin/vendors/${id}/fee`, null, { params: { fee } }),
}
