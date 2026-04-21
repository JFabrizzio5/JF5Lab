<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSession } from '../stores/session'

const route = useRoute()
const router = useRouter()
const session = useSession()

const nav = [
  { group: 'Operación', items: [
    { to: '/app/dashboard', icon: 'view-dashboard-outline', label: 'Dashboard' },
    { to: '/app/calendar',  icon: 'calendar-month-outline', label: 'Calendario' },
    { to: '/app/customers', icon: 'account-group-outline',  label: 'Clientes' },
  ]},
  { group: 'Catálogo', items: [
    { to: '/app/services',  icon: 'briefcase-outline',      label: 'Servicios' },
    { to: '/app/staff',     icon: 'account-tie-outline',    label: 'Staff' },
  ]},
  { group: 'Finanzas', items: [
    { to: '/app/billing',   icon: 'credit-card-outline',    label: 'Pagos' },
  ]},
]

const isActive = (to) => route.path.startsWith(to)

function logout() {
  session.clear()
  router.push('/')
}

const publicUrl = computed(() => session.slug ? `/${session.slug}` : null)
</script>

<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="brand">Agenda<strong>Pro</strong></div>
      <div class="tenant-info" v-if="session.tenantName">
        {{ session.tenantName }}<br>
        <span style="font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:rgba(253,251,245,0.5);">{{ session.industry }}</span>
      </div>

      <div class="nav-group" v-for="group in nav" :key="group.group">
        <div class="nav-title">{{ group.group }}</div>
        <router-link v-for="item in group.items" :key="item.to"
                     :to="item.to" :class="['nav-link', { active: isActive(item.to) }]">
          <i :class="'mdi mdi-' + item.icon"></i>{{ item.label }}
        </router-link>
      </div>

      <div class="nav-group" v-if="publicUrl">
        <div class="nav-title">Mi página</div>
        <a :href="publicUrl" target="_blank" class="nav-link">
          <i class="mdi mdi-open-in-new"></i>Ver página pública
        </a>
      </div>

      <div style="margin-top:auto;padding-top:18px;">
        <button @click="logout" class="nav-link" style="background:transparent;border:none;width:100%;text-align:left;color:rgba(253,251,245,0.55);">
          <i class="mdi mdi-logout-variant"></i>Cerrar sesión
        </button>
      </div>
    </aside>

    <main class="main">
      <slot />
    </main>
  </div>
</template>
