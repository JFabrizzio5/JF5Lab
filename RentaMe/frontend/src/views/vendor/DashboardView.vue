<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <div class="page-header">
        <div>
          <h1 class="page-title">Dashboard</h1>
          <p class="page-subtitle">Bienvenido, {{ authStore.user?.name }} 👋</p>
        </div>
        <div class="header-actions">
          <a v-if="vendor?.slug" :href="`/r/${vendor.slug}`" target="_blank" class="btn btn-secondary btn-sm">
            🌐 Ver mi landing ↗
          </a>
        </div>
      </div>

      <!-- Stats -->
      <div class="stats-grid" v-if="stats">
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-value">{{ stats.total_items }}</div>
          <div class="stat-label">Artículos activos</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📅</div>
          <div class="stat-value">{{ stats.total_bookings }}</div>
          <div class="stat-label">Total reservas</div>
        </div>
        <div class="stat-card highlight">
          <div class="stat-icon">⏳</div>
          <div class="stat-value" style="color: var(--warning)">{{ stats.pending_bookings }}</div>
          <div class="stat-label">Pendientes de respuesta</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-value" style="color: var(--success)">${{ fmt(stats.revenue_this_month) }}</div>
          <div class="stat-label">Ingresos este mes</div>
        </div>
      </div>

      <!-- Quick links -->
      <div class="quick-links card" style="margin-bottom: 24px;">
        <h3 style="margin-bottom: 14px; font-size: 15px; font-weight: 700;">Acciones rápidas</h3>
        <div class="ql-grid">
          <router-link to="/vendor/items" class="ql-btn">
            <span class="ql-icon">📦</span>
            <span>Agregar artículo</span>
          </router-link>
          <router-link to="/vendor/bookings" class="ql-btn">
            <span class="ql-icon">📅</span>
            <span>Ver reservas</span>
          </router-link>
          <router-link to="/vendor/availability" class="ql-btn">
            <span class="ql-icon">🗓️</span>
            <span>Disponibilidad</span>
          </router-link>
          <router-link to="/vendor/settings" class="ql-btn">
            <span class="ql-icon">⚙️</span>
            <span>Configuración</span>
          </router-link>
        </div>
      </div>

      <!-- Recent bookings -->
      <div class="card">
        <div class="card-header">
          <h3>Reservas recientes</h3>
          <router-link to="/vendor/bookings" class="btn btn-secondary btn-sm">Ver todas</router-link>
        </div>
        <div v-if="recentBookings.length === 0" class="empty-state">
          <p>No hay reservas aún. Comparte tu landing y empieza a recibir solicitudes.</p>
          <a v-if="vendor?.slug" :href="`/r/${vendor.slug}`" target="_blank" class="btn btn-primary" style="margin-top: 12px;">
            Ver mi landing ↗
          </a>
        </div>
        <div v-else class="bookings-table">
          <table>
            <thead>
              <tr>
                <th>Artículo</th>
                <th>Cliente</th>
                <th>Fechas</th>
                <th>Total</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in recentBookings" :key="b.id">
                <td>{{ b.item_name }}</td>
                <td>{{ b.customer_name }}</td>
                <td>{{ fmtDate(b.start_datetime) }}</td>
                <td>${{ fmt(b.total) }}</td>
                <td><span :class="`badge badge-${statusColor(b.status)}`">{{ statusLabel(b.status) }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { useAuthStore } from '../../stores/auth.js'
import { vendorAPI, bookingsAPI } from '../../api/index.js'

const authStore = useAuthStore()
const stats = ref(null)
const vendor = ref(null)
const recentBookings = ref([])

function fmt(n) {
  return Number(n || 0).toLocaleString('es-MX')
}

function fmtDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}

const STATUS_LABELS = {
  inquiry: 'Consulta',
  quote_sent: 'Cotización',
  confirmed: 'Confirmado',
  deposit_paid: 'Depósito pagado',
  active: 'Activo',
  completed: 'Completado',
  cancelled: 'Cancelado',
}

const STATUS_COLORS = {
  inquiry: 'warning',
  quote_sent: 'primary',
  confirmed: 'success',
  deposit_paid: 'success',
  active: 'primary',
  completed: 'gray',
  cancelled: 'danger',
}

function statusLabel(s) { return STATUS_LABELS[s] || s }
function statusColor(s) { return STATUS_COLORS[s] || 'gray' }

onMounted(async () => {
  try {
    const [statsRes, vendorRes, bookingsRes] = await Promise.all([
      vendorAPI.getStats(),
      vendorAPI.getProfile(),
      bookingsAPI.list(),
    ])
    stats.value = statsRes.data
    vendor.value = vendorRes.data
    recentBookings.value = bookingsRes.data.slice(0, 10)
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
  gap: 16px;
}
.header-actions { display: flex; gap: 10px; flex-wrap: wrap; }
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
.stat-card.highlight { border-color: rgba(245,158,11,0.3); }
.stat-icon { font-size: 28px; margin-bottom: 8px; }
.stat-value { font-size: 28px; font-weight: 800; margin-bottom: 4px; }
.stat-label { font-size: 13px; color: var(--text2); }

.ql-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.ql-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 10px;
  text-decoration: none;
  color: var(--text3);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
  text-align: center;
}
.ql-btn:hover { border-color: var(--primary); color: var(--text); }
.ql-icon { font-size: 22px; }

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.card-header h3 { font-size: 16px; font-weight: 700; }

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text2);
}

.bookings-table { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th {
  font-size: 12px;
  font-weight: 600;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
td {
  padding: 12px;
  font-size: 14px;
  border-bottom: 1px solid var(--border);
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .ql-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
