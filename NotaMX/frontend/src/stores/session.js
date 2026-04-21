import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSession = defineStore('session', () => {
  const tenantId = ref(null)
  const tenantName = ref(null)
  const industry = ref(null)
  const brandColor = ref('#10b981')

  function set(t) {
    tenantId.value = t.tenant_id || t.id
    tenantName.value = t.name
    industry.value = t.industry
    brandColor.value = t.brand_color || '#10b981'
    localStorage.setItem('notamx_session', JSON.stringify({
      tenant_id: tenantId.value, name: tenantName.value,
      industry: industry.value, brand_color: brandColor.value,
    }))
  }
  function restore() {
    try {
      const raw = localStorage.getItem('notamx_session')
      if (raw) {
        const d = JSON.parse(raw)
        tenantId.value = d.tenant_id; tenantName.value = d.name
        industry.value = d.industry; brandColor.value = d.brand_color
      }
    } catch {}
  }
  function clear() {
    tenantId.value = null; tenantName.value = null; industry.value = null
    localStorage.removeItem('notamx_session')
  }
  const active = computed(() => !!tenantId.value)
  return { tenantId, tenantName, industry, brandColor, active, set, restore, clear }
})
