<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useSession } from '../stores/session'

const router = useRouter()
const route = useRoute()
const session = useSession()

const nav = [
  { to: '/app/dashboard', icon: 'mdi-view-dashboard-outline', label: 'Dashboard' },
  { to: '/app/notes',     icon: 'mdi-receipt-text-outline',   label: 'Notas' },
  { to: '/app/customers', icon: 'mdi-account-multiple-outline', label: 'Clientes' },
  { to: '/app/products',  icon: 'mdi-tag-outline',            label: 'Productos' },
  { to: '/app/billing',   icon: 'mdi-credit-card-outline',    label: 'Pagos' },
  { to: '/app/cfdi',      icon: 'mdi-file-document-outline',  label: 'CFDI' },
]

function logout() {
  session.clear()
  router.push('/')
}
</script>

<template>
  <div class="app-layout">
    <aside class="app-side">
      <router-link to="/" class="app-brand">
        <div class="app-brand-mark"><i class="mdi mdi-receipt-text-check"></i></div>
        <div>Nota<span class="gradient-text">MX</span></div>
      </router-link>
      <div class="tenant-pill" v-if="session.tenantName">
        <div class="tp-dot" :style="{ background: session.brandColor }"></div>
        <div>
          <div class="tp-name">{{ session.tenantName }}</div>
          <div class="tp-muted">{{ session.industry }}</div>
        </div>
      </div>
      <nav class="app-nav">
        <router-link v-for="n in nav" :key="n.to" :to="n.to"
                     class="app-nav-item"
                     :class="{ active: route.path.startsWith(n.to) }">
          <i :class="['mdi', n.icon]"></i>
          <span>{{ n.label }}</span>
        </router-link>
      </nav>
      <div class="app-side-foot">
        <button class="btn btn-sm btn-ghost" @click="logout" style="width:100%;justify-content:center;">
          <i class="mdi mdi-logout"></i> Salir del demo
        </button>
      </div>
    </aside>
    <main class="app-main">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.tenant-pill {
  display: flex; align-items: center; gap: 10px; padding: 10px 12px;
  background: var(--bg-subtle); border-radius: 10px; margin-bottom: 14px;
}
.tp-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.tp-name { font-weight: 700; font-size: 13px; line-height: 1.2; }
.tp-muted { font-size: 11px; color: var(--text-muted); text-transform: capitalize; }
.app-side-foot { margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--border); }

@media (max-width: 820px) {
  .tenant-pill { display: none; }
  .app-side-foot { display: none; }
}
</style>
