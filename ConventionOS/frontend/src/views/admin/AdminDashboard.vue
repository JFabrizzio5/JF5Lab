<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Admin Dashboard</h1>
        <span class="badge badge-danger">SUPERADMIN</span>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Convenciones</div>
          <div class="stat-value">{{ conventions.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Publicadas</div>
          <div class="stat-value" style="color:var(--success)">{{ published }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">En borrador</div>
          <div class="stat-value" style="color:var(--text2)">{{ draft }}</div>
        </div>
      </div>

      <div class="conv-list">
        <h2>Todas las Convenciones</h2>
        <table>
          <thead>
            <tr><th>Nombre</th><th>Slug</th><th>Organizador</th><th>Estado</th><th>Creada</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            <tr v-for="c in conventions" :key="c.id">
              <td>{{ c.name }}</td>
              <td><code>{{ c.slug }}</code></td>
              <td>{{ c.organizer_id }}</td>
              <td><span class="badge" :class="statusBadge(c.status)">{{ c.status }}</span></td>
              <td>{{ fmtDate(c.created_at) }}</td>
              <td>
                <router-link :to="`/c/${c.slug}`" target="_blank" class="btn btn-ghost btn-sm">Ver</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conventions = ref([])
const published = computed(() => conventions.value.filter(c => c.status === 'published' || c.status === 'live').length)
const draft = computed(() => conventions.value.filter(c => c.status === 'draft').length)

function statusBadge(s) {
  if (s === 'published') return 'badge-success'
  if (s === 'live') return 'badge-info'
  if (s === 'draft') return 'badge-primary'
  return 'badge-warning'
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('es-MX') : '—'
}

onMounted(async () => {
  conventions.value = await api.get('/conventions/').then(r => r.data)
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.conv-list { margin-top: 24px; }
.conv-list h2 { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
code { font-family: monospace; background: var(--bg3); padding: 2px 6px; border-radius: 4px; font-size: 12px; }
</style>
