<script setup>
import { useSession } from '../stores/session'
import { RouterLink, useRouter } from 'vue-router'
const s = useSession()
const router = useRouter()

function exitTenant() {
  s.clearTenant()
  router.push('/')
}
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <i class="mdi mdi-cash-fast"></i>
        PorCobrar
      </div>
      <div class="nav-sep">Workspace</div>
      <RouterLink to="/app/dashboard" class="nav-link"><i class="mdi mdi-view-dashboard-outline"></i> Dashboard</RouterLink>
      <RouterLink to="/app/invoices"  class="nav-link"><i class="mdi mdi-receipt-text-outline"></i> Facturas</RouterLink>
      <RouterLink to="/app/debtors"   class="nav-link"><i class="mdi mdi-account-group-outline"></i> Deudores</RouterLink>
      <RouterLink to="/app/flows"     class="nav-link"><i class="mdi mdi-transit-connection-variant"></i> Flows</RouterLink>
      <RouterLink to="/app/upload"    class="nav-link"><i class="mdi mdi-cloud-upload-outline"></i> Upload CFDI</RouterLink>
      <RouterLink to="/app/billing"   class="nav-link"><i class="mdi mdi-credit-card-check-outline"></i> Billing</RouterLink>

      <div class="nav-sep">Cuenta</div>
      <a class="nav-link" @click="exitTenant" style="cursor:pointer"><i class="mdi mdi-logout-variant"></i> Salir demo</a>
      <a class="nav-link" href="/docs" target="_blank"><i class="mdi mdi-file-document-outline"></i> API docs</a>
    </aside>
    <main class="main">
      <div class="banner-tenant" v-if="s.tenantId">
        <div>
          <span class="pulse-dot"></span>
          <strong style="margin-left:8px">{{ s.tenantName || 'Tenant activo' }}</strong>
          <span class="muted" style="margin-left:8px"> · {{ s.industry }}</span>
        </div>
        <div class="tid">tenant_id: {{ s.tenantId }}</div>
      </div>
      <slot />
    </main>
  </div>
</template>
