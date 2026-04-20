import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export const auth = {
  register: (data) => api.post('/auth/v1/register', data),
  login: (data) => api.post('/auth/v1/login/json', data),
  me: () => api.get('/auth/v1/me')
}

export const properties = {
  list: () => api.get('/properties/v1/'),
  get: (id) => api.get(`/properties/v1/${id}`),
  create: (data) => api.post('/properties/v1/', data),
  update: (id, data) => api.put(`/properties/v1/${id}`, data),
  delete: (id) => api.delete(`/properties/v1/${id}`)
}

export const tenants = {
  list: () => api.get('/tenants/v1/'),
  get: (id) => api.get(`/tenants/v1/${id}`),
  create: (data) => api.post('/tenants/v1/', data),
  update: (id, data) => api.put(`/tenants/v1/${id}`, data),
  delete: (id) => api.delete(`/tenants/v1/${id}`)
}

export const contracts = {
  list: () => api.get('/contracts/v1/'),
  get: (id) => api.get(`/contracts/v1/${id}`),
  create: (data) => api.post('/contracts/v1/', data),
  update: (id, data) => api.put(`/contracts/v1/${id}`, data)
}

export const payments = {
  list: (status) => api.get('/payments/v1/', { params: status ? { status } : {} }),
  overdue: () => api.get('/payments/v1/overdue'),
  get: (id) => api.get(`/payments/v1/${id}`),
  create: (data) => api.post('/payments/v1/', data),
  update: (id, data) => api.put(`/payments/v1/${id}`, data),
  markPaid: (id, data) => api.post(`/payments/v1/${id}/mark-paid`, data)
}

export const reports = {
  dashboard: () => api.get('/reports/v1/dashboard'),
  monthly: (year, month) => api.get('/reports/v1/monthly', { params: { year, month } })
}

export default api
