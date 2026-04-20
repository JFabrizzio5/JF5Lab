<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Dashboard</h1>
        <div style="display:flex;gap:10px;align-items:center">
          <span class="badge" :class="statusBadge(conv?.status)">{{ conv?.status || 'draft' }}</span>
          <button v-if="conv?.status === 'draft'" @click="publish" class="btn btn-primary btn-sm">Publicar Convención</button>
          <router-link v-if="conv" :to="`/c/${conv.slug}`" target="_blank" class="btn btn-ghost btn-sm">Ver pública →</router-link>
        </div>
      </div>

      <div v-if="!conv" class="no-conv">
        <div class="no-conv-icon">🎪</div>
        <h2>Aún no tienes convención</h2>
        <p>Crea tu primera convención para empezar a organizarla</p>
        <router-link to="/organizer/settings" class="btn btn-primary">Crear Convención</router-link>
      </div>

      <template v-else>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Boletos vendidos</div>
            <div class="stat-value" style="color:var(--primary)">{{ stats.tickets_sold || 0 }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Ingresos totales</div>
            <div class="stat-value" style="color:var(--success)">${{ (stats.total_revenue || 0).toFixed(0) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Check-ins</div>
            <div class="stat-value" style="color:var(--accent)">{{ stats.checked_in || 0 }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Días para el evento</div>
            <div class="stat-value" style="color:var(--text)">{{ daysUntil }}</div>
          </div>
        </div>

        <div class="quick-links">
          <h2>Accesos rápidos</h2>
          <div class="links-grid">
            <router-link to="/organizer/stages" class="quick-link">
              <div class="ql-icon">🎭</div><div class="ql-label">Escenarios</div>
            </router-link>
            <router-link to="/organizer/speakers" class="quick-link">
              <div class="ql-icon">🎤</div><div class="ql-label">Ponentes</div>
            </router-link>
            <router-link to="/organizer/stands" class="quick-link">
              <div class="ql-icon">🏪</div><div class="ql-label">Stands</div>
            </router-link>
            <router-link to="/organizer/tickets" class="quick-link">
              <div class="ql-icon">🎫</div><div class="ql-label">Boletos</div>
            </router-link>
            <router-link to="/organizer/tournaments" class="quick-link">
              <div class="ql-icon">🏆</div><div class="ql-label">Torneos</div>
            </router-link>
            <router-link to="/organizer/payments" class="quick-link">
              <div class="ql-icon">💳</div><div class="ql-label">Pagos</div>
            </router-link>
            <router-link to="/organizer/attendees" class="quick-link">
              <div class="ql-icon">👥</div><div class="ql-label">Asistentes</div>
            </router-link>
            <router-link to="/organizer/settings" class="quick-link">
              <div class="ql-icon">⚙️</div><div class="ql-label">Configuración</div>
            </router-link>
          </div>
        </div>

        <div class="conv-summary card">
          <div class="summary-row">
            <img v-if="conv.logo_url" :src="conv.logo_url" class="summary-logo" />
            <div>
              <h3>{{ conv.name }}</h3>
              <p>{{ conv.tagline }}</p>
              <p style="color:var(--text2);font-size:13px">📍 {{ conv.venue_name }} · {{ conv.city }}</p>
              <p style="color:var(--accent);font-size:13px;margin-top:4px" v-if="conv.start_date">
                📅 {{ formatDate(conv.start_date) }}
              </p>
            </div>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const stats = ref({})

const daysUntil = computed(() => {
  if (!conv.value?.start_date) return '—'
  const diff = new Date(conv.value.start_date) - new Date()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
  if (days < 0) return 'Finalizado'
  if (days === 0) return '¡Hoy!'
  return days
})

function statusBadge(s) {
  if (s === 'published') return 'badge-success'
  if (s === 'live') return 'badge-info'
  if (s === 'finished') return 'badge-warning'
  return 'badge-primary'
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' })
}

async function publish() {
  try {
    await api.patch(`/conventions/${conv.value.id}/status`, { status: 'published' })
    conv.value.status = 'published'
  } catch (e) {
    alert('Error al publicar')
  }
}

onMounted(async () => {
  try {
    conv.value = await api.get('/conventions/my').then(r => r.data)
    stats.value = await api.get('/payments/stats').then(r => r.data)
  } catch {}
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }

.no-conv { text-align: center; padding: 80px 20px; }
.no-conv-icon { font-size: 64px; margin-bottom: 16px; }
.no-conv h2 { font-size: 24px; font-weight: 800; margin-bottom: 8px; }
.no-conv p { color: var(--text2); margin-bottom: 24px; }

.quick-links { margin: 32px 0; }
.quick-links h2 { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
.links-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.quick-link {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.quick-link:hover { border-color: var(--primary); transform: translateY(-2px); }
.ql-icon { font-size: 28px; }
.ql-label { font-size: 13px; font-weight: 600; }

.conv-summary { margin-top: 24px; }
.summary-row { display: flex; align-items: center; gap: 16px; }
.summary-logo { width: 60px; height: 60px; border-radius: 10px; object-fit: contain; flex-shrink: 0; }
.conv-summary h3 { font-size: 20px; font-weight: 800; margin-bottom: 4px; }
.conv-summary p { font-size: 14px; color: var(--text2); }
</style>
