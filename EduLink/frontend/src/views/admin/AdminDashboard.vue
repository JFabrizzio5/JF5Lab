<template>
  <div>
    <div class="page-header">
      <h1>Panel de Administración</h1>
      <p>Gestiona usuarios, cursos y métricas de EduLink</p>
    </div>

    <div class="page-content">
      <div v-if="loading" class="loading">Cargando estadísticas...</div>
      <div v-else>
        <div class="stats-grid" style="margin-bottom:36px">
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_users }}</div>
            <div class="stat-label">Usuarios totales</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_students }}</div>
            <div class="stat-label">Estudiantes</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_tutors }}</div>
            <div class="stat-label">Tutores</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_courses }}</div>
            <div class="stat-label">Cursos totales</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.published_courses }}</div>
            <div class="stat-label">Cursos publicados</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_enrollments }}</div>
            <div class="stat-label">Inscripciones</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_bookings }}</div>
            <div class="stat-label">Reservas de tutoría</div>
          </div>
        </div>

        <div class="admin-nav-cards">
          <RouterLink to="/admin/users" class="admin-nav-card">
            <div class="anc-icon">👥</div>
            <div class="anc-title">Gestionar Usuarios</div>
            <div class="anc-desc">Activar, desactivar o cambiar roles de usuarios</div>
          </RouterLink>
          <RouterLink to="/admin/courses" class="admin-nav-card">
            <div class="anc-icon">🎬</div>
            <div class="anc-title">Gestionar Cursos</div>
            <div class="anc-desc">Ver, publicar u ocultar cursos de la plataforma</div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const stats = ref({})
const loading = ref(true)

async function fetchStats() {
  try {
    const res = await api.get('/admin/stats')
    stats.value = res.data
  } catch (e) {
    stats.value = {}
  } finally {
    loading.value = false
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 16px; }

.admin-nav-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.admin-nav-card {
  display: block;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
  text-decoration: none;
  transition: all 0.2s;
}
.admin-nav-card:hover { border-color: var(--primary); transform: translateY(-2px); text-decoration: none; }
.anc-icon { font-size: 36px; margin-bottom: 12px; }
.anc-title { font-size: 16px; font-weight: 700; color: var(--text); margin-bottom: 6px; }
.anc-desc { font-size: 13px; color: var(--text2); line-height: 1.5; }
</style>
