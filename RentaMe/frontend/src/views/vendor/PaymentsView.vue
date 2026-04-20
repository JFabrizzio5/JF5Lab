<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <h1 class="page-title">Pagos</h1>
      <p class="page-subtitle">Historial de pagos procesados</p>

      <div v-if="!vendor?.stripe_onboarding_complete" class="stripe-alert card">
        <div class="alert-icon">⚠️</div>
        <div>
          <h3>Stripe no conectado</h3>
          <p>Para recibir pagos en línea, primero conecta tu cuenta de Stripe en Configuración.</p>
          <router-link to="/vendor/settings" class="btn btn-primary" style="margin-top: 12px;">
            Ir a Configuración →
          </router-link>
        </div>
      </div>

      <div class="stats-row" v-if="payments.length > 0">
        <div class="stat-mini">
          <div class="sm-val">${{ fmt(totalRevenue) }}</div>
          <div class="sm-label">Total recibido (succeeded)</div>
        </div>
        <div class="stat-mini">
          <div class="sm-val">${{ fmt(totalFees) }}</div>
          <div class="sm-label">Comisiones plataforma</div>
        </div>
        <div class="stat-mini">
          <div class="sm-val">{{ payments.length }}</div>
          <div class="sm-label">Total transacciones</div>
        </div>
      </div>

      <div class="card">
        <div v-if="loading" class="loading">Cargando pagos...</div>
        <div v-else-if="payments.length === 0" class="empty-state">
          <p>Sin historial de pagos todavía.</p>
        </div>
        <div v-else class="payments-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Reserva</th>
                <th>Tipo</th>
                <th>Monto</th>
                <th>Comisión</th>
                <th>Recibido</th>
                <th>Estado</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in payments" :key="p.id">
                <td class="id-cell">#{{ p.id }}</td>
                <td>#{{ p.booking_id }}</td>
                <td>{{ typeLabel(p.payment_type) }}</td>
                <td>${{ fmt(p.amount) }}</td>
                <td class="fee-cell">${{ fmt(p.platform_fee) }}</td>
                <td class="recv-cell">${{ fmt(p.vendor_amount) }}</td>
                <td><span :class="`badge badge-${statusColor(p.status)}`">{{ p.status }}</span></td>
                <td>{{ fmtDate(p.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { paymentsAPI, vendorAPI } from '../../api/index.js'

const payments = ref([])
const vendor = ref(null)
const loading = ref(true)

const totalRevenue = computed(() =>
  payments.value.filter(p => p.status === 'succeeded').reduce((s, p) => s + p.vendor_amount, 0)
)
const totalFees = computed(() =>
  payments.value.filter(p => p.status === 'succeeded').reduce((s, p) => s + p.platform_fee, 0)
)

function fmt(n) { return Number(n || 0).toLocaleString('es-MX') }
function fmtDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}
function typeLabel(t) {
  return { deposit: 'Depósito', full: 'Completo', balance: 'Saldo' }[t] || t
}
function statusColor(s) {
  return { succeeded: 'success', pending: 'warning', failed: 'danger', refunded: 'gray' }[s] || 'gray'
}

onMounted(async () => {
  try {
    const [pRes, vRes] = await Promise.all([paymentsAPI.history(), vendorAPI.getProfile()])
    payments.value = pRes.data
    vendor.value = vRes.data
  } catch {}
  loading.value = false
})
</script>

<style scoped>
.stripe-alert {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 24px;
  border-color: rgba(245,158,11,0.3);
  background: rgba(245,158,11,0.05);
}
.alert-icon { font-size: 28px; flex-shrink: 0; }
.stripe-alert h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.stripe-alert p { font-size: 14px; color: var(--text2); }

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}
.stat-mini {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px;
  text-align: center;
}
.sm-val { font-size: 22px; font-weight: 800; color: var(--success); }
.sm-label { font-size: 12px; color: var(--text2); margin-top: 4px; }

.loading, .empty-state { text-align: center; padding: 40px; color: var(--text2); }
.payments-table { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th {
  font-size: 11px;
  font-weight: 700;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
td { padding: 12px; font-size: 13px; border-bottom: 1px solid var(--border); }
tr:last-child td { border-bottom: none; }
.id-cell { color: var(--text2); }
.fee-cell { color: var(--text2); }
.recv-cell { color: var(--success); font-weight: 600; }
</style>
