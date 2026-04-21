import axios from 'axios'
import { useSession } from '../stores/session'

const api = axios.create({ baseURL: '/notas/v1', timeout: 20000 })

api.interceptors.request.use(cfg => {
  try {
    const s = useSession()
    if (s.tenantId) cfg.headers['X-Tenant-Id'] = s.tenantId
  } catch {}
  return cfg
})

export default api

export async function downloadBlob(url, filename) {
  const { data } = await api.get(url, { responseType: 'blob' })
  const link = URL.createObjectURL(data)
  const a = document.createElement('a')
  a.href = link; a.download = filename
  document.body.appendChild(a); a.click(); a.remove()
  URL.revokeObjectURL(link)
}
