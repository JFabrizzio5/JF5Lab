<script setup>
import { useRouter } from 'vue-router'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()

const nav = [
  { to: '/app/dashboard',  label: 'Dashboard',   icon: 'mdi-view-dashboard' },
  { to: '/app/items',      label: 'Catálogo',    icon: 'mdi-package-variant' },
  { to: '/app/movements',  label: 'Movimientos', icon: 'mdi-swap-horizontal' },
  { to: '/app/labels',     label: 'Etiquetas',   icon: 'mdi-qrcode' },
  { to: '/app/scanner',    label: 'Escáner',     icon: 'mdi-barcode-scan' },
  { to: '/app/attendance', label: 'Asistencias', icon: 'mdi-account-clock' },
  { to: '/app/reports',    label: 'Reportes',    icon: 'mdi-chart-box' },
]

function logout() {
  session.clear()
  router.push('/')
}
</script>

<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="logo-mark">SL</div>
        <div>
          <div class="brand-title">StockLink</div>
          <div class="brand-tenant muted">{{ session.tenantName || 'Sin tenant' }}</div>
        </div>
      </div>
      <nav>
        <router-link v-for="i in nav" :key="i.to" :to="i.to" class="nav-item">
          <i :class="['mdi', i.icon]"></i> {{ i.label }}
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button @click="logout" class="btn-ghost btn btn-sm" style="width:100%; justify-content:flex-start;">
          <i class="mdi mdi-logout"></i> Cerrar tenant
        </button>
      </div>
    </aside>
    <main class="content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.shell { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
.sidebar { background: var(--surface); border-right: 1px solid var(--border); padding: 20px 16px; display: flex; flex-direction: column; position: sticky; top: 0; height: 100vh; }
.brand { display: flex; align-items: center; gap: 12px; padding: 8px 8px 20px; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.logo-mark { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: white; font-weight: 800; display: grid; place-items: center; }
.brand-title { font-weight: 700; }
.brand-tenant { font-size: 11px; margin-top: 2px; max-width: 170px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 8px; color: var(--text-muted); font-size: 14px; text-decoration: none; transition: all .15s; }
.nav-item:hover { background: var(--surface-2); color: var(--text); }
.nav-item.router-link-active { background: rgba(99,102,241,.12); color: var(--accent); font-weight: 500; }
.nav-item .mdi { font-size: 18px; }
.sidebar-footer { border-top: 1px solid var(--border); padding-top: 12px; margin-top: 12px; }
.content { padding: 28px 32px; overflow-x: hidden; }

@media (max-width: 820px) {
  .shell { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; flex-direction: row; align-items: center; gap: 16px; padding: 12px 16px; overflow-x: auto; }
  .brand { padding: 0; border: none; margin: 0; }
  nav { flex-direction: row; flex: 1; overflow-x: auto; }
  .nav-item { white-space: nowrap; }
  .sidebar-footer { border: none; padding: 0; margin: 0; }
}
</style>
