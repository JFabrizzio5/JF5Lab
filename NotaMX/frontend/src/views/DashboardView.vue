<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { dashboardApi, exportsApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const session = useSession()
const router = useRouter()
const kpis = ref(null); const loading = ref(false); const error = ref(null)

async function load() {
  if (!session.tenantId) { router.push('/'); return }
  loading.value = true
  try {
    const { data } = await dashboardApi.get()
    kpis.value = data
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { loading.value = false }
}

const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits:0 }).format(n || 0)

const maxSeries = computed(() => {
  if (!kpis.value?.monthly_series?.length) return 1
  return Math.max(...kpis.value.monthly_series.map(x => x.revenue)) || 1
})

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="app-top">
      <div>
        <h1 class="page-title">Hola, {{ session.tenantName || 'tenant' }}</h1>
        <p class="page-sub">Resumen de cobros, notas enviadas y CFDI.</p>
      </div>
      <div class="top-actions">
        <button class="btn btn-sm" @click="exportsApi.notes()"><i class="mdi mdi-file-excel-outline"></i> Notas .xlsx</button>
        <button class="btn btn-sm" @click="exportsApi.payments()"><i class="mdi mdi-file-excel-outline"></i> Pagos .xlsx</button>
        <router-link to="/app/notes" class="btn btn-primary btn-sm"><i class="mdi mdi-plus"></i> Nueva nota</router-link>
      </div>
    </div>

    <div v-if="loading" class="muted">Cargando…</div>
    <div v-else-if="error" class="muted" style="color:var(--danger);">{{ error }}</div>
    <template v-else-if="kpis">
      <div class="grid-4">
        <div class="card kpi">
          <div class="kpi-label">Notas este mes</div>
          <div class="kpi-val">{{ kpis.notes_mtd }}</div>
          <div class="muted tiny">{{ kpis.notes_paid_mtd }} cobradas · {{ kpis.notes_pending }} pendientes</div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">Ingresos MTD</div>
          <div class="kpi-val gradient-text">{{ peso(kpis.revenue_mtd_mxn) }}</div>
          <div class="muted tiny">Promedio por nota: {{ peso(kpis.avg_note_mxn) }}</div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">Conversión</div>
          <div class="kpi-val">{{ (kpis.conversion_rate*100).toFixed(0) }}%</div>
          <div class="muted tiny">Notas cobradas / enviadas</div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">CFDI emitidos</div>
          <div class="kpi-val">{{ kpis.cfdi_issued_mtd }}</div>
          <div class="muted tiny">Este mes</div>
        </div>
      </div>

      <div class="grid-2" style="margin-top: 18px;">
        <div class="card">
          <h3 class="card-title">Ingresos (últimos 6 meses)</h3>
          <div class="bars">
            <div v-for="m in kpis.monthly_series" :key="m.month" class="bar-wrap">
              <div class="bar-val">{{ peso(m.revenue) }}</div>
              <div class="bar" :style="{ height: `${(m.revenue / maxSeries) * 100}%` }"></div>
              <div class="bar-label">{{ m.month.slice(5) }}/{{ m.month.slice(2,4) }}</div>
            </div>
          </div>
        </div>
        <div class="card">
          <h3 class="card-title">Top clientes</h3>
          <table class="table" style="margin-top: 8px;">
            <thead><tr><th>Cliente</th><th style="text-align:right;">Total cobrado</th></tr></thead>
            <tbody>
              <tr v-for="c in kpis.top_customers" :key="c.name">
                <td>{{ c.name }}</td>
                <td style="text-align:right; font-weight: 700;">{{ peso(c.total_mxn) }}</td>
              </tr>
              <tr v-if="!kpis.top_customers.length"><td colspan="2" class="muted" style="text-align:center;">Aún sin pagos cobrados.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card" style="margin-top: 18px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <h3 class="card-title" style="margin:0;">Notas recientes</h3>
          <router-link to="/app/notes">Ver todas <i class="mdi mdi-arrow-right"></i></router-link>
        </div>
        <table class="table" style="margin-top: 10px;">
          <thead><tr>
            <th>Folio</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Creada</th><th></th>
          </tr></thead>
          <tbody>
            <tr v-for="n in kpis.recent_notes" :key="n.id">
              <td class="mono">{{ n.number }}</td>
              <td>{{ n.customer }}</td>
              <td style="font-weight:700;">{{ peso(n.total) }}</td>
              <td><span :class="['badge', n.status]">{{ n.status }}</span></td>
              <td class="muted">{{ new Date(n.created_at).toLocaleDateString('es-MX') }}</td>
              <td><router-link :to="`/app/notes/${n.id}`">Abrir</router-link></td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </AppLayout>
</template>

<style scoped>
.top-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.kpi-label { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: .08em; }
.kpi-val { font-size: 28px; font-weight: 800; letter-spacing: -0.025em; margin: 6px 0; }
.tiny { font-size: 12px; }
.card-title { font-size: 14px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); margin: 0 0 10px; font-weight: 700; }
.bars { display: flex; gap: 10px; align-items: flex-end; height: 180px; padding-top: 20px; border-bottom: 1px solid var(--border); }
.bar-wrap { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.bar { width: 100%; background: var(--brand-grad); border-radius: 6px 6px 0 0; min-height: 4px; transition: height .3s; }
.bar-val { font-size: 10px; color: var(--text-muted); font-weight: 600; }
.bar-label { font-size: 11px; color: var(--text-muted); padding-top: 4px; }
</style>
