import api from './client'

export const apiPlans       = () => api.get('/plans').then(r => r.data)
export const apiCreateTenant = (p) => api.post('/tenants', p).then(r => r.data)

export const apiStaff       = () => api.get('/staff').then(r => r.data)
export const apiCreateStaff = (p) => api.post('/staff', p).then(r => r.data)

export const apiServices       = () => api.get('/services').then(r => r.data)
export const apiCreateService  = (p) => api.post('/services', p).then(r => r.data)
export const apiUpdateService  = (id, p) => api.patch(`/services/${id}`, p).then(r => r.data)

export const apiCustomers      = () => api.get('/customers').then(r => r.data)
export const apiCreateCustomer = (p) => api.post('/customers', p).then(r => r.data)

export const apiAppointments      = (params = {}) => api.get('/appointments', { params }).then(r => r.data)
export const apiCreateAppointment = (p) => api.post('/appointments', p).then(r => r.data)
export const apiConfirmAppt       = (id) => api.post(`/appointments/${id}/confirm`).then(r => r.data)
export const apiCancelAppt        = (id, reason = '') => api.post(`/appointments/${id}/cancel`, null, { params: { reason } }).then(r => r.data)
export const apiCompleteAppt      = (id) => api.post(`/appointments/${id}/complete`).then(r => r.data)
export const apiRemindAppt        = (id, hours = 24) => api.post(`/appointments/${id}/remind`, null, { params: { hours_before: hours } }).then(r => r.data)
export const apiCheckoutAppt      = (id, provider = 'stripe') => api.post(`/appointments/${id}/checkout`, null, { params: { provider } }).then(r => r.data)

export const apiRules      = () => api.get('/availability-rules').then(r => r.data)
export const apiCreateRule = (p) => api.post('/availability-rules', p).then(r => r.data)

export const apiExceptions      = () => api.get('/availability-exceptions').then(r => r.data)
export const apiCreateException = (p) => api.post('/availability-exceptions', p).then(r => r.data)

export const apiAvailability = (p) => api.get('/availability', { params: p }).then(r => r.data)

export const apiDashboard = () => api.get('/dashboard').then(r => r.data)

export const apiPayments = () => api.get('/payments').then(r => r.data)

export const apiSeed = (industry) => api.post(`/demo/seed?industry=${industry}`).then(r => r.data)

// PÚBLICO (por slug)
export const pubTenant = (slug) => api.get(`/public/tenant/${slug}`).then(r => r.data)
export const pubAvailability = (slug, params) => api.get(`/public/availability/${slug}`, { params }).then(r => r.data)
export const pubBook = (slug, payload) => api.post(`/public/book/${slug}`, payload).then(r => r.data)
