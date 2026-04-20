<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Todas las reservas</h1>
        <p class="page-subtitle">{{ bookings.length }} reservas en el sistema</p>
      </div>
      <div class="card">
        <div v-if="loading" class="loading-state">Cargando...</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Cliente</th><th>Profesional</th><th>Categoría</th><th>Estado</th><th>Precio</th><th>Fecha</th></tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id">
              <td style="color:var(--text2);">{{ b.id }}</td>
              <td>{{ b.client }}</td>
              <td>{{ b.professional }}</td>
              <td>{{ b.category }}</td>
              <td><span :class="`status-${b.status}`">{{ statusLabel(b.status) }}</span></td>
              <td>${{ b.price }}/hr</td>
              <td style="color:var(--text2);font-size:13px;">{{ formatDate(b.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { adminApi } from '../../api/index.js'

const bookings = ref([])
const loading = ref(true)

onMounted(async () => {
  const { data } = await adminApi.bookings()
  bookings.value = data
  loading.value = false
})

function statusLabel(s) {
  return { pending: '⏳ Pendiente', accepted: '✅ Aceptada', in_progress: '🚀 En progreso', completed: '✓ Completada', cancelled: '✗ Cancelada' }[s] || s
}
function formatDate(dt) { return dt ? new Date(dt).toLocaleDateString('es-MX') : '—' }
</script>

<style scoped>
.loading-state { padding: 32px; text-align: center; color: var(--text2); }
</style>
