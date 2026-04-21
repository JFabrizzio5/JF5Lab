<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api/client'
import { useSession } from '../stores/session'
import { RouterLink } from 'vue-router'

const session = useSession()
const data = ref(null)
const loading = ref(true)
const err = ref('')

function fmt(n) { return '$' + Number(n || 0).toLocaleString('es-MX', { maximumFractionDigits: 0 }) }

onMounted(async () => {
  if (!session.tenantId) { err.value = 'No hay tenant activo. Usa /demo para crear uno.'; loading.value = false; return }
  try {
    const res = await api.get('/dashboard')
    data.value = res.data
  } catch(e) {
    err.value = e.response?.data?.detail || e.message
  }
  loading.value = false
})

const ageBars = computed(() => {
  if (!data.value) return []
  const total = Object.values(data.value.aging).reduce((a,b) => a + b.amount, 0) || 1
  return [
    { label: '0-30', key: '0-30', color: 'var(--cash)' },
    { label: '31-60', key: '31-60', color: 'var(--info)' },
    { label: '61-90', key: '61-90', color: 'var(--warn)' },
    { label: '+90', key: '+90', color: 'var(--danger)' },
  ].map(b => ({
    ...b,
    pct: Math.round((data.value.aging[b.key].amount / total) * 1000) / 10,
    amt: data.value.aging[b.key].amount,
    count: data.value.aging[b.key].count,
  }))
})

function scoreClass(s) {
  if (s >= 70) return 's-hi'
  if (s >= 40) return 's-md'
  return 's-lo'
}
</script>

<template>
  <div v-if="loading" class="muted">Cargando…</div>
  <div v-else-if="err" class="card" style="border-color:var(--danger)">
    <i class="mdi mdi-alert-circle-outline" style="color:var(--danger)"></i> {{ err }}
  </div>
  <div v-else-if="data">
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 18px">
      <div>
        <h1>Dashboard</h1>
        <div class="muted" style="font-size:13px">Snapshot en vivo · {{ new Date(data.as_of).toLocaleString('es-MX') }}</div>
      </div>
      <div style="display:flex; gap:8px">
        <RouterLink to="/app/upload" class="btn btn-sm"><i class="mdi mdi-cloud-upload-outline"></i> Upload</RouterLink>
        <RouterLink to="/app/invoices" class="btn btn-primary btn-sm"><i class="mdi mdi-receipt-text-outline"></i> Ver facturas</RouterLink>
      </div>
    </div>

    <div class="grid-4" style="margin-bottom: 18px">
      <div class="card">
        <div class="kpi-label">Total por cobrar</div>
        <div class="kpi-number" style="color: var(--warn)">{{ fmt(data.total_owed) }}</div>
        <div class="muted" style="font-size:12px">Saldo pendiente</div>
      </div>
      <div class="card">
        <div class="kpi-label">Cobrado (mes)</div>
        <div class="kpi-number" style="color: var(--cash)">{{ fmt(data.paid_mtd) }}</div>
        <div class="muted" style="font-size:12px">MTD</div>
      </div>
      <div class="card">
        <div class="kpi-label">DSO</div>
        <div class="kpi-number">{{ data.dso_days }}</div>
        <div class="muted" style="font-size:12px">días promedio de cobro</div>
      </div>
      <div class="card">
        <div class="kpi-label">Recuperación</div>
        <div class="kpi-number">{{ data.recovery_rate_pct }}%</div>
        <div class="muted" style="font-size:12px">este mes</div>
      </div>
    </div>

    <div class="grid-2" style="margin-bottom: 18px">
      <div class="card">
        <div style="display:flex; justify-content:space-between; margin-bottom: 14px">
          <h3>Cartera por edad</h3>
          <span class="muted" style="font-size:12px">Saldo pendiente por antigüedad</span>
        </div>
        <div class="age-bar" style="margin-bottom: 14px">
          <span v-for="b in ageBars" :key="b.key"
                :style="{ width: b.pct + '%', background: b.color }"></span>
        </div>
        <div class="grid-4">
          <div v-for="b in ageBars" :key="b.key" class="card-inset">
            <div style="display:flex; align-items:center; gap:6px">
              <span style="width:8px; height:8px; border-radius:999px" :style="{background:b.color}"></span>
              <span style="font-size:12px; font-weight:600">{{ b.label }}d</span>
            </div>
            <div style="font-family:var(--mono); font-size:15px; font-weight:700; margin-top: 4px">{{ fmt(b.amt) }}</div>
            <div class="muted" style="font-size:11px">{{ b.count }} facturas · {{ b.pct }}%</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div style="display:flex; justify-content:space-between; margin-bottom: 14px">
          <h3>Top 5 deudores</h3>
          <RouterLink to="/app/debtors" style="font-size:12px">Ver todos →</RouterLink>
        </div>
        <table class="table">
          <thead>
            <tr><th>Nombre</th><th>Score</th><th class="num">Adeudo</th></tr>
          </thead>
          <tbody>
            <tr v-for="d in data.top_debtors" :key="d.id">
              <td>{{ d.name }}</td>
              <td><span class="score-pill" :class="scoreClass(d.payment_score)">{{ d.payment_score }}</span></td>
              <td class="num">{{ fmt(d.total_owed) }}</td>
            </tr>
            <tr v-if="!data.top_debtors.length"><td colspan="3" class="muted" style="text-align:center">Sin deudores.</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
