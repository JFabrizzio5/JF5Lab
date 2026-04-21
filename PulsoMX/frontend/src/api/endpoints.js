import api, { downloadBlob } from './client'
import { useSession } from '../stores/session'

export const plansApi       = { list: () => api.get('/plans') }
export const tenantsApi     = { create: (d) => api.post('/tenants', d) }
export const venuesApi      = { list: () => api.get('/venues'), create: (d) => api.post('/venues', d) }
export const membersApi     = {
  list: (q) => api.get('/members', { params: { q } }),
  create: (d) => api.post('/members', d),
  qrUrl: (id, size = 300) => `/membership/v1/members/${id}/qr?size=${size}&tenant=${useSession().tenantId || ''}`,
}
export const mPlansApi      = { list: () => api.get('/membership-plans'), create: (d) => api.post('/membership-plans', d) }
export const membershipsApi = { create: (d) => api.post('/memberships', d) }
export const instructorsApi = { list: () => api.get('/instructors'), create: (d) => api.post('/instructors', d) }
export const templatesApi   = { list: () => api.get('/class-templates'), create: (d) => api.post('/class-templates', d) }
export const sessionsApi    = { list: (params) => api.get('/sessions', { params }), create: (d) => api.post('/sessions', d) }
export const bookingsApi    = { create: (d) => api.post('/bookings', d) }
export const checkinApi     = { punch: (d) => api.post('/check-ins', d), list: (params) => api.get('/check-ins', { params }) }
export const billingApi     = {
  checkout: (d) => api.post('/billing/checkout', d),
  payments: () => api.get('/payments'),
}
export const dashboardApi   = { get: () => api.get('/dashboard') }
export const demoApi        = { seed: (industry) => api.post(`/demo/seed?industry=${industry}`) }
export const exportsApi     = {
  members:  () => downloadBlob('/exports/members.xlsx',  `miembros-${new Date().toISOString().slice(0,10)}.xlsx`),
  checkins: () => downloadBlob('/exports/checkins.xlsx', `checkins-${new Date().toISOString().slice(0,10)}.xlsx`),
}
