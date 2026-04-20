import client from './client'

export const auth = {
  login: (email, password) => client.post('/auth/login', { email, password }),
}

export const editors = {
  list: () => client.get('/editors/'),
  me: () => client.get('/editors/me'),
  get: (id) => client.get(`/editors/${id}`),
  create: (data) => client.post('/editors/', data),
  update: (id, data) => client.patch(`/editors/${id}`, data),
  delete: (id) => client.delete(`/editors/${id}`),
}

export const reviews = {
  list: (params) => client.get('/reviews/', { params }),
  get: (id) => client.get(`/reviews/${id}`),
  stats: () => client.get('/reviews/stats'),
  create: (data) => client.post('/reviews/', data),
  update: (id, data) => client.patch(`/reviews/${id}`, data),
  changeStatus: (id, status, note) => client.post(`/reviews/${id}/status`, { status, note }),
  addComment: (id, comment) => client.post(`/reviews/${id}/comments`, { comment }),
  history: (id) => client.get(`/reviews/${id}/history`),
  delete: (id) => client.delete(`/reviews/${id}`),
}

export const billing = {
  plans: () => client.get('/billing/plans'),
  mySubscription: () => client.get('/billing/subscription/me'),
  checkout: (data) => client.post('/billing/checkout', data),
  cancel: () => client.post('/billing/subscription/cancel'),
}
