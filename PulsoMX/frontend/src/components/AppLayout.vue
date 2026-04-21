<script setup>
import { useRouter } from 'vue-router'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const nav = [
  { to: '/app/dashboard', label: 'Dashboard',   icon: 'mdi-view-dashboard' },
  { to: '/app/members',   label: 'Miembros',    icon: 'mdi-account-multiple' },
  { to: '/app/classes',   label: 'Clases',      icon: 'mdi-calendar-clock' },
  { to: '/app/checkin',   label: 'Check-in QR', icon: 'mdi-qrcode-scan' },
  { to: '/app/billing',   label: 'Cobros',      icon: 'mdi-credit-card-outline' },
]

function logout() { session.clear(); router.push('/') }
</script>

<template>
  <div class="shell">
    <aside class="sb">
      <div class="sb-brand">
        <div class="sb-mark"><i class="mdi mdi-pulse"></i></div>
        <div>
          <div class="sb-title">PulsoMX</div>
          <div class="sb-tenant">{{ session.tenantName || 'Sin tenant' }}</div>
        </div>
      </div>
      <nav>
        <router-link v-for="i in nav" :key="i.to" :to="i.to" class="sb-item">
          <i :class="['mdi', i.icon]"></i> {{ i.label }}
        </router-link>
      </nav>
      <div class="sb-foot">
        <button @click="logout" class="btn btn-ghost btn-sm" style="width:100%; justify-content:flex-start;">
          <i class="mdi mdi-logout"></i> Cerrar tenant
        </button>
      </div>
    </aside>
    <main class="content"><slot /></main>
  </div>
</template>

<style scoped>
.shell { display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }
.sb { background: var(--surface); border-right: 1px solid var(--border); padding: 20px 14px; display: flex; flex-direction: column; position: sticky; top: 0; height: 100vh; }
.sb-brand { display: flex; align-items: center; gap: 10px; padding: 4px 6px 18px; border-bottom: 1px solid var(--border); margin-bottom: 14px; }
.sb-mark { width: 34px; height: 34px; border-radius: 10px; background: var(--brand-grad); color: white; display: grid; place-items: center; font-size: 18px; }
.sb-title { font-weight: 800; letter-spacing: -0.01em; }
.sb-tenant { font-size: 11px; color: var(--text-muted); max-width: 160px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
nav { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.sb-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; color: var(--text-muted); font-size: 14px; text-decoration: none; transition: all .15s; font-weight: 500; }
.sb-item:hover { background: var(--surface-2); color: var(--text); }
.sb-item.router-link-active { background: var(--violet-soft); color: var(--violet); }
.sb-item .mdi { font-size: 17px; }
.sb-foot { border-top: 1px solid var(--border); padding-top: 10px; }
.content { padding: 26px 32px; overflow-x: hidden; }
@media (max-width: 820px) {
  .shell { grid-template-columns: 1fr; }
  .sb { position: static; height: auto; flex-direction: row; align-items: center; gap: 14px; padding: 10px 14px; overflow-x: auto; }
  .sb-brand { padding: 0; border: none; margin: 0; }
  nav { flex-direction: row; }
  .sb-item { white-space: nowrap; }
  .sb-foot { border: none; padding: 0; }
}
</style>
