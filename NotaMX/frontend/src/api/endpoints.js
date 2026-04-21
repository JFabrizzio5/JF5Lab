import api, { downloadBlob } from './client'
import { useSession } from '../stores/session'

export const plansApi     = { list: () => api.get('/plans') }
export const tenantsApi   = { create: (d) => api.post('/tenants', d) }
export const customersApi = {
  list: (q) => api.get('/customers', { params: { q } }),
  create: (d) => api.post('/customers', d),
  get: (id) => api.get(`/customers/${id}`),
}
export const productsApi  = {
  list: (q) => api.get('/products', { params: { q } }),
  create: (d) => api.post('/products', d),
}
export const notesApi     = {
  list: (status) => api.get('/notes', { params: { status } }),
  create: (d) => api.post('/notes', d),
  get: (id) => api.get(`/notes/${id}`),
  send: (id, d) => api.post(`/notes/${id}/send`, d),
  checkout: (id, d) => api.post(`/notes/${id}/checkout`, d),
  issueCfdi: (id, d) => api.post(`/notes/${id}/cfdi`, d),
  qrUrl: (id, size = 320) => `/notas/v1/notes/${id}/qr?size=${size}&tenant=${useSession().tenantId || ''}`,
}
export const publicNotesApi = {
  get: (token) => api.get(`/public/note/${token}`),
  checkout: (nid, d) => api.post(`/notes/${nid}/checkout`, d),
}
export const billingApi   = { payments: () => api.get('/payments') }
export const cfdiApi      = { list: () => api.get('/cfdi') }
export const dashboardApi = { get: () => api.get('/dashboard') }
export const demoApi      = { seed: (industry) => api.post(`/demo/seed?industry=${industry}`) }
export const exportsApi   = {
  notes:    () => downloadBlob('/exports/notes.xlsx',    `notas-${new Date().toISOString().slice(0,10)}.xlsx`),
  payments: () => downloadBlob('/exports/payments.xlsx', `pagos-${new Date().toISOString().slice(0,10)}.xlsx`),
}
