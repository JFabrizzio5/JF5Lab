<template>
  <div>
    <div class="page-header">
      <h1>Admin Dashboard</h1>
      <p>Panel de control global de SalonOS</p>
    </div>

    <div class="page-body">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🏢</div>
          <div class="stat-label">Venues activos</div>
          <div class="stat-value">{{ venues.filter(v => v.is_active).length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💳</div>
          <div class="stat-label">Venues con Stripe</div>
          <div class="stat-value">{{ venues.filter(v => v.stripe_onboarding_complete).length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-label">Total venues</div>
          <div class="stat-value">{{ venues.length }}</div>
        </div>
      </div>

      <div class="card">
        <h3 style="font-size:1rem;font-weight:700;margin-bottom:1rem">Todos los venues</h3>
        <div v-if="loading" style="color:var(--text2)">Cargando...</div>
        <table v-else>
          <thead>
            <tr>
              <th>Venue</th>
              <th>Slug</th>
              <th>Ciudad</th>
              <th>Stripe</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!venues.length">
              <td colspan="6" style="text-align:center;color:var(--text2);padding:2rem">No hay venues</td>
            </tr>
            <tr v-for="v in venues" :key="v.id">
              <td>
                <div style="font-weight:600">{{ v.name }}</div>
                <div style="font-size:.75rem;color:var(--text2)">{{ v.email || '' }}</div>
              </td>
              <td>
                <a :href="`/v/${v.slug}`" target="_blank" style="color:var(--primary);text-decoration:none">/v/{{ v.slug }}</a>
              </td>
              <td>{{ v.city || '—' }}</td>
              <td>
                <span v-if="v.stripe_onboarding_complete" class="badge" style="background:rgba(16,185,129,.2);color:#34d399">✅ Conectado</span>
                <span v-else class="badge" style="background:rgba(100,116,139,.2);color:#94a3b8">—</span>
              </td>
              <td>
                <span :class="v.is_active ? 'badge-active' : 'badge-inactive'">{{ v.is_active ? 'Activo' : 'Inactivo' }}</span>
              </td>
              <td>
                <button @click="toggleVenue(v)" class="btn btn-ghost btn-sm">
                  {{ v.is_active ? 'Desactivar' : 'Activar' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const venues = ref([])
const loading = ref(true)

async function loadVenues() {
  loading.value = true
  try {
    const { data } = await api.get('/venues/all')
    venues.value = data
  } finally {
    loading.value = false
  }
}

async function toggleVenue(v) {
  try {
    const { data } = await api.put(`/venues/${v.id}/toggle`)
    const idx = venues.value.findIndex(x => x.id === v.id)
    if (idx >= 0) venues.value[idx] = data
  } catch (e) {
    alert('Error al cambiar estado')
  }
}

onMounted(loadVenues)
</script>

<style scoped>
.badge-active { background: rgba(16,185,129,.2); color: #34d399; padding: .2rem .6rem; border-radius: 12px; font-size: .75rem; font-weight: 600; }
.badge-inactive { background: rgba(239,68,68,.2); color: #f87171; padding: .2rem .6rem; border-radius: 12px; font-size: .75rem; font-weight: 600; }
</style>
