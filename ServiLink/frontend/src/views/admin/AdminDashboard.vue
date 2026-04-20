<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Dashboard Admin</h1>
        <p class="page-subtitle">Visión general de ServiLink</p>
      </div>

      <div class="grid-4" style="margin-bottom:28px;">
        <div class="stat-card">
          <div class="stat-value" style="color:var(--primary);">{{ stats.total_users }}</div>
          <div class="stat-label">Usuarios totales</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent);">{{ stats.total_freelancers }}</div>
          <div class="stat-label">Freelancers</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--warning);">{{ stats.total_bookings }}</div>
          <div class="stat-label">Reservas totales</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent);">${{ stats.monthly_revenue?.toLocaleString() }}</div>
          <div class="stat-label">Ingresos mensual (demo)</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="stat-card">
          <div class="stat-label">Clientes</div>
          <div class="stat-value" style="color:var(--primary);font-size:24px;">{{ stats.total_clients }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Reservas completadas</div>
          <div class="stat-value" style="color:var(--accent);font-size:24px;">{{ stats.completed_bookings }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Reseñas</div>
          <div class="stat-value" style="color:#f59e0b;font-size:24px;">{{ stats.total_reviews }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Categorías activas</div>
          <div class="stat-value" style="font-size:24px;">{{ stats.total_categories }}</div>
        </div>
      </div>

      <div class="quick-links" style="margin-top:24px;">
        <router-link to="/admin/users" class="btn btn-secondary">👥 Gestionar usuarios</router-link>
        <router-link to="/admin/categories" class="btn btn-secondary">🏷️ Gestionar categorías</router-link>
        <router-link to="/admin/bookings" class="btn btn-secondary">📋 Ver todas las reservas</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { adminApi } from '../../api/index.js'

const stats = ref({})
onMounted(async () => {
  const { data } = await adminApi.stats()
  stats.value = data
})
</script>

<style scoped>
.quick-links { display: flex; gap: 12px; flex-wrap: wrap; }
</style>
