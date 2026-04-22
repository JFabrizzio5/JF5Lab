import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSession = defineStore('session', () => {
  const tenantId = ref(null)
  const tenantName = ref(null)
  const industry = ref(null)

  function set(t) {
    tenantId.value = t.tenant_id || t.id
    tenantName.value = t.name
    industry.value = t.industry
    localStorage.setItem('stocklink_session', JSON.stringify({
      tenant_id: tenantId.value, name: tenantName.value, industry: industry.value,
    }))
  }

  function restore() {
    try {
      const raw = localStorage.getItem('stocklink_session')
      if (raw) {
        const d = JSON.parse(raw)
        tenantId.value = d.tenant_id
        tenantName.value = d.name
        industry.value = d.industry
      }
    } catch {}
  }

  function clear() {
    tenantId.value = null; tenantName.value = null; industry.value = null
    localStorage.removeItem('stocklink_session')
  }

  const active = computed(() => !!tenantId.value)

  return { tenantId, tenantName, industry, active, set, restore, clear }
})
