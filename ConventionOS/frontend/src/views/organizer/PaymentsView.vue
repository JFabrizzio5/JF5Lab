<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Pagos & Ingresos</h1>
      </div>

      <!-- Stripe status -->
      <div class="stripe-card" :class="stats.convention?.stripe_onboarding_complete ? 'connected' : 'pending'">
        <div v-if="stats.convention?.stripe_onboarding_complete" class="stripe-status">
          <span class="stripe-icon">✅</span>
          <div>
            <div class="stripe-title">Stripe Conectado</div>
            <div class="stripe-sub">Los pagos fluyen directo a tu cuenta Stripe</div>
          </div>
        </div>
        <div v-else class="stripe-status">
          <span class="stripe-icon">⚠️</span>
          <div>
            <div class="stripe-title">Stripe no conectado</div>
            <div class="stripe-sub">Configura Stripe Connect para recibir pagos automáticamente</div>
          </div>
          <router-link to="/organizer/settings" class="btn btn-primary btn-sm">Conectar Stripe →</router-link>
        </div>
      </div>

      <!-- Revenue stats -->
      <div class="stats-grid" style="margin-top:24px">
        <div class="stat-card">
          <div class="stat-label">Ingresos Totales</div>
          <div class="stat-value" style="color:var(--success)">${{ (stats.total_revenue || 0).toFixed(2) }}</div>
          <div class="stat-sub">MXN</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Fee de Plataforma</div>
          <div class="stat-value" style="color:var(--danger)">${{ (stats.platform_fees || 0).toFixed(2) }}</div>
          <div class="stat-sub">MXN</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Neto para Ti</div>
          <div class="stat-value" style="color:var(--primary)">${{ (stats.net_to_organizer || 0).toFixed(2) }}</div>
          <div class="stat-sub">MXN</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Boletos Vendidos</div>
          <div class="stat-value">{{ stats.tickets_sold || 0 }}</div>
        </div>
      </div>

      <!-- Revenue bar -->
      <div class="revenue-bar-card card" style="margin-top:16px" v-if="stats.total_revenue > 0">
        <div class="revenue-bar">
          <div class="rev-net" :style="`width:${netPct}%`">
            <span>${{ (stats.net_to_organizer || 0).toFixed(0) }} tuyos</span>
          </div>
          <div class="rev-fee" :style="`width:${feePct}%`">
            <span v-if="feePct > 10">${{ (stats.platform_fees || 0).toFixed(0) }} fee</span>
          </div>
        </div>
      </div>

      <!-- Payments table -->
      <div class="payments-section">
        <h2>Historial de Pagos</h2>
        <table>
          <thead>
            <tr><th>ID</th><th>Comprador</th><th>Email</th><th>Total</th><th>Fee</th><th>Neto</th><th>Estado</th><th>Fecha</th></tr>
          </thead>
          <tbody>
            <tr v-for="p in payments" :key="p.id">
              <td>#{{ p.id }}</td>
              <td>{{ p.buyer_name }}</td>
              <td>{{ p.buyer_email }}</td>
              <td>${{ p.amount.toFixed(0) }}</td>
              <td style="color:var(--danger)">-${{ p.platform_fee.toFixed(0) }}</td>
              <td style="color:var(--success)">${{ p.organizer_amount.toFixed(0) }}</td>
              <td><span class="badge" :class="payBadge(p.status)">{{ p.status }}</span></td>
              <td>{{ fmtDate(p.created_at) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="!payments.length" class="empty-state">Sin pagos registrados aún</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const stats = ref({})
const payments = ref([])

const netPct = computed(() => {
  const t = stats.value.total_revenue || 0
  if (!t) return 95
  return Math.round((stats.value.net_to_organizer / t) * 100)
})

const feePct = computed(() => 100 - netPct.value)

function payBadge(s) {
  if (s === 'succeeded') return 'badge-success'
  if (s === 'pending') return 'badge-warning'
  return 'badge-danger'
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
}

onMounted(async () => {
  const [statsRes, paymentsRes] = await Promise.all([
    api.get('/payments/stats'),
    api.get('/payments/history'),
  ])
  stats.value = statsRes.data
  payments.value = paymentsRes.data
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }

.stripe-card { border-radius: 12px; padding: 18px 20px; border: 1px solid; }
.stripe-card.connected { background: rgba(16,185,129,0.08); border-color: rgba(16,185,129,0.25); }
.stripe-card.pending { background: rgba(245,158,11,0.08); border-color: rgba(245,158,11,0.25); }
.stripe-status { display: flex; align-items: center; gap: 14px; }
.stripe-icon { font-size: 24px; }
.stripe-title { font-weight: 700; font-size: 15px; }
.stripe-sub { font-size: 13px; color: var(--text2); }

.stat-sub { font-size: 12px; color: var(--text2); margin-top: 2px; }

.revenue-bar { height: 40px; border-radius: 10px; overflow: hidden; display: flex; }
.rev-net { background: var(--primary); display: flex; align-items: center; padding: 0 12px; font-size: 12px; font-weight: 700; color: white; transition: width 0.5s; }
.rev-fee { background: var(--text2); display: flex; align-items: center; padding: 0 8px; font-size: 12px; color: white; transition: width 0.5s; }

.payments-section { margin-top: 28px; }
.payments-section h2 { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
.empty-state { padding: 20px; text-align: center; color: var(--text2); }
</style>
