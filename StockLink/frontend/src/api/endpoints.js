import api from './client'
import { useSession } from '../stores/session'

export const plansApi = {
  list: () => api.get('/plans'),
}

export const tenantsApi = {
  create: (data) => api.post('/tenants', data),
}

export const itemsApi = {
  list: (params = {}) => api.get('/items', { params }),
  create: (data) => api.post('/items', data),
  get: (id) => api.get(`/items/${id}`),
  stock: (id) => api.get(`/items/${id}/stock`),
}

export const warehousesApi = {
  list: () => api.get('/warehouses'),
  create: (data) => api.post('/warehouses', data),
}

export const locationsApi = {
  list: (warehouse_id) => api.get('/locations', { params: { warehouse_id } }),
  create: (data) => api.post('/locations', data),
}

export const movementsApi = {
  list: (params = {}) => api.get('/movements', { params }),
  create: (data) => api.post('/movements', data),
}

export const labelsApi = {
  create: (data) => api.post('/labels', data),
  imageUrl: (id, size = 320) => {
    const tid = useSession().tenantId
    return `/inventory/v1/labels/${id}/image?size=${size}&tenant=${tid || ''}`
  },
  pdf: (ids) => api.post('/labels/pdf', ids, { responseType: 'blob' }),
}

export const scanApi = {
  resolve: (code) => api.get(`/scan/${encodeURIComponent(code)}`),
}

export const employeesApi = {
  list: () => api.get('/employees'),
  create: (data) => api.post('/employees', data),
}

export const attendanceApi = {
  punch: (data) => api.post('/attendance/punch', data),
  list: (params = {}) => api.get('/attendance', { params }),
}

export const eventsApi = {
  webhook: (data) => api.post('/events/webhook', data),
}

export const reportsApi = {
  dashboard: () => api.get('/reports/dashboard'),
  viability: () => api.get('/reports/viability'),
}

export const demoApi = {
  seed: (industry) => api.post(`/demo/seed?industry=${industry}`),
}

// Downloads: use blob via axios so custom header travels
export async function downloadExcel(kind, filename) {
  const { data } = await api.get(`/exports/${kind}.xlsx`, { responseType: 'blob' })
  const url = URL.createObjectURL(data)
  const a = document.createElement('a')
  a.href = url; a.download = filename
  document.body.appendChild(a); a.click(); a.remove()
  URL.revokeObjectURL(url)
}

export const exportsApi = {
  inventory: () => downloadExcel('inventory', `inventario-${new Date().toISOString().slice(0,10)}.xlsx`),
  movements: () => downloadExcel('movements', `movimientos-${new Date().toISOString().slice(0,10)}.xlsx`),
  attendance: () => downloadExcel('attendance', `asistencias-${new Date().toISOString().slice(0,10)}.xlsx`),
}
