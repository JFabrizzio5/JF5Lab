<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <div class="month-selector">
        <select v-model="selectedMonth" @change="loadMonthly">
          <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="empty">Cargando...</div>
    <template v-else>
      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-label">Total Propiedades</div>
          <div class="stat-value">{{ stats.total_properties }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Ocupadas</div>
          <div class="stat-value green">{{ stats.occupied }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Vacantes</div>
          <div class="stat-value">{{ stats.vacant }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Ocupación</div>
          <div class="stat-value">{{ stats.occupancy_rate }}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Pagos Vencidos</div>
          <div class="stat-value" :class="stats.overdue_payments > 0 ? 'red' : ''">{{ stats.overdue_payments }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Contratos Activos</div>
          <div class="stat-value">{{ stats.active_contracts }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Resumen del mes</div>
        <div class="monthly-grid">
          <div class="monthly-item green">
            <div class="monthly-label">Cobrado</div>
            <div class="monthly-amount">${{ fmt(monthly.paid_amount) }}</div>
            <div class="monthly-count">{{ monthly.paid_count }} pagos</div>
          </div>
          <div class="monthly-item yellow">
            <div class="monthly-label">Pendiente</div>
            <div class="monthly-amount">${{ fmt(monthly.pending_amount) }}</div>
            <div class="monthly-count">{{ monthly.pending_count }} pagos</div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { reports } from '../api/client'

const loading = ref(true)
const stats = ref({})
const monthly = ref({})
const now = new Date()
const selectedMonth = ref(`${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`)

const months = Array.from({ length: 12 }, (_, i) => {
  const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
  return {
    value: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`,
    label: d.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' })
  }
})

function fmt(n) {
  return Number(n || 0).toLocaleString('es-MX', { minimumFractionDigits: 2 })
}

async function loadMonthly() {
  const [y, m] = selectedMonth.value.split('-')
  const { data } = await reports.monthly(parseInt(y), parseInt(m))
  monthly.value = data
}

onMounted(async () => {
  try {
    const [s, mo] = await Promise.all([reports.dashboard(), loadMonthly()])
    stats.value = s.data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.month-selector select { padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 0.9rem; }
.card-title { font-size: 1rem; font-weight: 600; margin-bottom: 16px; }
.monthly-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.monthly-item { padding: 20px; border-radius: 10px; }
.monthly-item.green { background: #f0fdf4; }
.monthly-item.yellow { background: #fffbeb; }
.monthly-label { font-size: 0.8rem; font-weight: 600; color: #64748b; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.04em; }
.monthly-amount { font-size: 1.6rem; font-weight: 700; }
.monthly-item.green .monthly-amount { color: #10b981; }
.monthly-item.yellow .monthly-amount { color: #f59e0b; }
.monthly-count { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
</style>
