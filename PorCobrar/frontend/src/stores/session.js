import { defineStore } from 'pinia'

export const useSession = defineStore('session', {
  state: () => ({
    tenantId: localStorage.getItem('pc_tenant_id') || '',
    tenantName: localStorage.getItem('pc_tenant_name') || '',
    industry: localStorage.getItem('pc_industry') || '',
    theme: localStorage.getItem('pc_theme') || 'dark',
  }),
  actions: {
    setTenant(id, name, industry) {
      this.tenantId = id
      this.tenantName = name || ''
      this.industry = industry || ''
      localStorage.setItem('pc_tenant_id', id)
      localStorage.setItem('pc_tenant_name', name || '')
      localStorage.setItem('pc_industry', industry || '')
    },
    clearTenant() {
      this.tenantId = ''; this.tenantName=''; this.industry=''
      localStorage.removeItem('pc_tenant_id')
      localStorage.removeItem('pc_tenant_name')
      localStorage.removeItem('pc_industry')
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('pc_theme', this.theme)
      document.documentElement.setAttribute('data-theme', this.theme)
    },
  },
})
