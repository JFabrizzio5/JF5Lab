<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <h1 class="page-title">Admin Dashboard</h1>
      <p class="page-subtitle">Panel de administración de RentaMe</p>

      <div class="stats-grid" v-if="stats">
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-value">{{ stats.total_users }}</div>
          <div class="stat-label">Usuarios totales</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏪</div>
          <div class="stat-value">{{ stats.active_vendors }}</div>
          <div class="stat-label">Vendedores activos</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-value">{{ stats.total_items }}</div>
          <div class="stat-label">Artículos en catálogo</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📅</div>
          <div class="stat-value">{{ stats.total_bookings }}</div>
          <div class="stat-label">Reservas totales</div>
        </div>
      </div>

      <div class="card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
          <h3 style="font-size: 16px; font-weight: 700;">Acciones rápidas</h3>
        </div>
        <div class="quick-grid">
          <router-link to="/admin/vendors" class="quick-btn">
            <span>🏪</span>
            <span>Gestionar vendedores</span>
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { adminAPI } from '../../api/index.js'

const stats = ref(null)

onMounted(async () => {
  try {
    const res = await adminAPI.stats()
    stats.value = res.data
  } catch {}
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  text-align: center;
}
.stat-icon { font-size: 28px; margin-bottom: 8px; }
.stat-value { font-size: 28px; font-weight: 800; margin-bottom: 4px; }
.stat-label { font-size: 13px; color: var(--text2); }
.quick-grid { display: flex; gap: 12px; }
.quick-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 10px;
  text-decoration: none;
  color: var(--text3);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}
.quick-btn:hover { border-color: var(--primary); color: var(--text); }
@media (max-width: 768px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
