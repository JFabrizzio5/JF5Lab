<template>
  <div>
    <div class="page-header">
      <h1>Dashboard</h1>
      <p>Resumen de tu salón de eventos</p>
    </div>

    <div class="page-body">
      <div v-if="loading" class="loading-msg">Cargando estadísticas...</div>

      <template v-else>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-label">Total Clientes</div>
            <div class="stat-value">{{ stats.total_clients }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📅</div>
            <div class="stat-label">Eventos (próx. 30 días)</div>
            <div class="stat-value">{{ stats.upcoming_events }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-label">Ingresos este mes</div>
            <div class="stat-value">${{ stats.revenue_month?.toLocaleString() || '0' }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📋</div>
            <div class="stat-label">Cotizaciones activas</div>
            <div class="stat-value">{{ (stats.by_status?.inquiry || 0) + (stats.by_status?.quote_sent || 0) }}</div>
          </div>
        </div>

        <!-- Status breakdown -->
        <div class="dashboard-grid">
          <div class="card">
            <h3 class="card-title">Eventos por estado</h3>
            <div class="status-bars">
              <div v-for="s in statusList" :key="s.key" class="status-bar-row">
                <div class="status-bar-label">
                  <span :class="`badge badge-${s.key}`">{{ s.label }}</span>
                </div>
                <div class="status-bar-track">
                  <div class="status-bar-fill" :style="{ width: barWidth(s.key) + '%', background: s.color }"></div>
                </div>
                <div class="status-bar-count">{{ stats.by_status?.[s.key] || 0 }}</div>
              </div>
            </div>
          </div>

          <div class="card">
            <h3 class="card-title">Actividad reciente</h3>
            <div v-if="!stats.recent_activity?.length" class="empty-msg">No hay actividad reciente</div>
            <div v-else class="activity-list">
              <div v-for="ev in stats.recent_activity" :key="ev.id" class="activity-item">
                <div class="activity-dot" :style="{ background: statusColor(ev.status) }"></div>
                <div class="activity-content">
                  <div class="activity-title">{{ ev.title }}</div>
                  <div class="activity-meta">
                    {{ ev.client_name }} · {{ formatDate(ev.start_datetime) }}
                  </div>
                </div>
                <span :class="`badge badge-${ev.status}`">{{ ev.status }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick links -->
        <div class="quick-links">
          <router-link to="/events" class="quick-link">
            <span>📅</span>
            <div>
              <div class="ql-title">Ver todos los eventos</div>
              <div class="ql-sub">Gestionar reservaciones</div>
            </div>
          </router-link>
          <router-link to="/clients" class="quick-link">
            <span>👥</span>
            <div>
              <div class="ql-title">CRM de clientes</div>
              <div class="ql-sub">Prospectos y seguimiento</div>
            </div>
          </router-link>
          <router-link to="/calendar" class="quick-link">
            <span>🗓️</span>
            <div>
              <div class="ql-title">Calendario</div>
              <div class="ql-sub">Vista mensual</div>
            </div>
          </router-link>
          <router-link to="/settings" class="quick-link">
            <span>⚙️</span>
            <div>
              <div class="ql-title">Ajustes del venue</div>
              <div class="ql-sub">Perfil y pagos</div>
            </div>
          </router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const stats = ref({})
const loading = ref(true)

const statusList = [
  { key: 'inquiry', label: 'Consulta', color: '#64748b' },
  { key: 'quote_sent', label: 'Cotización', color: '#3b82f6' },
  { key: 'confirmed', label: 'Confirmado', color: '#10b981' },
  { key: 'deposit_paid', label: 'Depósito', color: '#7c3aed' },
  { key: 'completed', label: 'Completado', color: '#f59e0b' },
  { key: 'cancelled', label: 'Cancelado', color: '#ef4444' },
]

function statusColor(s) {
  return statusList.find(x => x.key === s)?.color || '#64748b'
}

function barWidth(key) {
  const total = Object.values(stats.value?.by_status || {}).reduce((a, b) => a + b, 0)
  if (!total) return 0
  return Math.round(((stats.value.by_status?.[key] || 0) / total) * 100)
}

function formatDate(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/events/stats')
    stats.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.loading-msg { color: var(--text2); padding: 2rem; }

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  color: var(--text);
}

.status-bars { display: flex; flex-direction: column; gap: 0.75rem; }

.status-bar-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-bar-label { width: 100px; }

.status-bar-track {
  flex: 1;
  height: 6px;
  background: rgba(255,255,255,0.06);
  border-radius: 3px;
  overflow: hidden;
}

.status-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.status-bar-count {
  width: 24px;
  text-align: right;
  font-size: 0.85rem;
  color: var(--text2);
}

.empty-msg { color: var(--text2); font-size: 0.9rem; padding: 1rem 0; }

.activity-list { display: flex; flex-direction: column; gap: 0.75rem; }

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.activity-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.activity-content { flex: 1; min-width: 0; }

.activity-title {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.activity-meta {
  font-size: 0.78rem;
  color: var(--text2);
}

.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.quick-link {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  color: var(--text);
  font-size: 1.75rem;
  transition: all 0.2s;
}

.quick-link:hover {
  border-color: var(--primary);
  background: rgba(124,58,237,0.05);
}

.ql-title { font-size: 0.9rem; font-weight: 600; }
.ql-sub { font-size: 0.78rem; color: var(--text2); }

@media (max-width: 768px) {
  .dashboard-grid { grid-template-columns: 1fr; }
}
</style>
