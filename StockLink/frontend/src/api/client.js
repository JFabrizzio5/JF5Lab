import axios from 'axios'
import { useSession } from '../stores/session'

const api = axios.create({
  baseURL: '/inventory/v1',
  timeout: 20000,
})

api.interceptors.request.use(cfg => {
  try {
    const session = useSession()
    if (session.tenantId) cfg.headers['X-Tenant-Id'] = session.tenantId
  } catch {}
  return cfg
})

export default api
