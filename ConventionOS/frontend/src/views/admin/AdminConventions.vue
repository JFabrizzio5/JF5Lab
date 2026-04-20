<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Gestión de Convenciones</h1>
      </div>

      <div class="filters" style="margin-bottom:20px;display:flex;gap:12px">
        <input v-model="search" placeholder="Buscar..." style="max-width:280px" />
        <select v-model="filterStatus">
          <option value="">Todos</option>
          <option value="draft">Borrador</option>
          <option value="published">Publicado</option>
          <option value="live">En vivo</option>
          <option value="finished">Finalizado</option>
        </select>
      </div>

      <table>
        <thead>
          <tr><th>ID</th><th>Nombre</th><th>Slug</th><th>Ciudad</th><th>Inicio</th><th>Estado</th><th>Stripe</th><th>Acciones</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td>#{{ c.id }}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <img v-if="c.logo_url" :src="c.logo_url" style="width:24px;height:24px;border-radius:4px;object-fit:contain;background:white" />
                {{ c.name }}
              </div>
            </td>
            <td><code>{{ c.slug }}</code></td>
            <td>{{ c.city || '—' }}</td>
            <td>{{ c.start_date ? fmtDate(c.start_date) : '—' }}</td>
            <td>
              <select :value="c.status" @change="changeStatus(c, $event.target.value)" class="status-select">
                <option value="draft">Borrador</option>
                <option value="published">Publicado</option>
                <option value="live">En vivo</option>
                <option value="finished">Finalizado</option>
              </select>
            </td>
            <td>
              <span v-if="c.stripe_onboarding_complete" class="badge badge-success">Conectado</span>
              <span v-else class="badge badge-warning">Pendiente</span>
            </td>
            <td>
              <router-link :to="`/c/${c.slug}`" target="_blank" class="btn btn-ghost btn-sm">Ver →</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conventions = ref([])
const search = ref('')
const filterStatus = ref('')

const filtered = computed(() => {
  return conventions.value.filter(c => {
    const q = search.value.toLowerCase()
    const matchSearch = !q || c.name?.toLowerCase().includes(q) || c.slug?.includes(q)
    const matchStatus = !filterStatus.value || c.status === filterStatus.value
    return matchSearch && matchStatus
  })
})

function fmtDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function changeStatus(c, status) {
  await api.patch(`/conventions/${c.id}/status`, { status })
  c.status = status
}

onMounted(async () => {
  conventions.value = await api.get('/conventions/').then(r => r.data)
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
code { font-family: monospace; background: var(--bg3); padding: 2px 6px; border-radius: 4px; font-size: 11px; }
.status-select { background: var(--bg3); border: 1px solid var(--border); color: var(--text); border-radius: 6px; padding: 4px 8px; font-size: 12px; cursor: pointer; }
select { background: var(--bg3); border: 1px solid var(--border); color: var(--text); border-radius: 8px; padding: 8px 12px; font-size: 14px; }
</style>
