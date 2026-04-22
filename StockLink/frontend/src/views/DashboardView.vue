<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { reportsApi, exportsApi } from '../api/endpoints'

const kpis = ref(null)
const viability = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const [d, v] = await Promise.all([reportsApi.dashboard(), reportsApi.viability()])
    kpis.value = d.data
    viability.value = v.data
  } finally { loading.value = false }
}

onMounted(load)

function verdictClass(v) {
  return { 'Excelente': 'success', 'Bueno': 'accent', 'Atención': 'warn', 'Crítico': 'danger' }[v] || ''
}
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1>Dashboard</h1>
        <p class="muted">Panorama general de tu inventario y operación.</p>
      </div>
      <div class="actions">
        <button class="btn btn-sm" @click="exportsApi.inventory()"><i class="mdi mdi-file-excel"></i> Excel inventario</button>
        <button class="btn btn-sm" @click="exportsApi.movements()"><i class="mdi mdi-file-excel"></i> Excel movimientos</button>
      </div>
    </div>

    <div v-if="loading" class="muted"><i class="mdi mdi-loading mdi-spin"></i> Cargando…</div>

    <div v-else-if="kpis">
      <div class="grid-4">
        <div class="card kpi">
          <div class="kpi-label">Artículos</div>
          <div class="kpi-value">{{ kpis.total_items.toLocaleString('es-MX') }}</div>
          <div class="kpi-sub muted"><i class="mdi mdi-package-variant"></i> SKUs activos</div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">Almacenes</div>
          <div class="kpi-value">{{ kpis.total_warehouses }}</div>
          <div class="kpi-sub muted">{{ kpis.total_locations }} ubicaciones</div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">Movimientos</div>
          <div class="kpi-value">{{ kpis.total_movements.toLocaleString('es-MX') }}</div>
          <div class="kpi-sub muted">Histórico total</div>
        </div>
        <div class="card kpi" :class="{ alert: kpis.items_under_min > 0 }">
          <div class="kpi-label">Bajo mínimo</div>
          <div class="kpi-value">{{ kpis.items_under_min }}</div>
          <div class="kpi-sub muted">Requieren reabasto</div>
        </div>
      </div>

      <div class="grid-2" style="margin-top:20px;">
        <div class="card">
          <h3 style="margin:0 0 14px;">Viabilidad del inventario</h3>
          <div v-if="viability" class="via">
            <div class="via-score">
              <div class="score-num">{{ viability.health_score }}</div>
              <div class="muted">/ 100</div>
              <span class="badge" :class="verdictClass(viability.verdict)">{{ viability.verdict }}</span>
            </div>
            <div class="via-stats">
              <div><span class="muted">Valor inventario:</span> <b>${{ Number(viability.stock_value_mxn).toLocaleString('es-MX', {maximumFractionDigits:2}) }} MXN</b></div>
              <div><span class="muted">Movs. últimos 30d:</span> <b>{{ viability.movements_last_30d }}</b></div>
              <div><span class="muted">Bajo mínimo:</span> <b>{{ viability.items_under_min }}</b></div>
              <div><span class="muted">Sobre máximo:</span> <b>{{ viability.items_above_max }}</b></div>
            </div>
            <ul class="recs">
              <li v-for="r in viability.recommendations" :key="r"><i class="mdi mdi-lightbulb-on"></i> {{ r }}</li>
              <li v-if="!viability.recommendations.length" class="muted"><i class="mdi mdi-check-circle"></i> Sin recomendaciones, todo en orden.</li>
            </ul>
          </div>
        </div>

        <div class="card">
          <h3 style="margin:0 0 14px;">Movimientos recientes</h3>
          <table class="table">
            <thead><tr><th>Tipo</th><th>Artículo</th><th>Qty</th><th>Cuándo</th></tr></thead>
            <tbody>
              <tr v-for="m in kpis.recent_movements" :key="m.id">
                <td><span class="badge accent">{{ m.kind }}</span></td>
                <td>{{ m.item }}</td>
                <td class="mono">{{ m.qty }}</td>
                <td class="muted">{{ m.at }}</td>
              </tr>
              <tr v-if="!kpis.recent_movements.length"><td colspan="4" class="muted">Sin movimientos aún.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.page-head p { margin: 4px 0 0; }
.actions { display: flex; gap: 8px; }
.kpi-label { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); font-weight: 600; }
.kpi-value { font-size: 32px; font-weight: 800; margin: 6px 0; letter-spacing: -0.02em; }
.kpi-sub { font-size: 13px; }
.kpi.alert .kpi-value { color: var(--warn); }
.via-score { display: flex; align-items: baseline; gap: 8px; margin-bottom: 16px; }
.score-num { font-size: 44px; font-weight: 800; color: var(--accent); letter-spacing: -0.02em; }
.via-stats div { padding: 6px 0; border-bottom: 1px dashed var(--border); font-size: 14px; }
.via-stats div:last-child { border: none; }
.recs { list-style: none; padding: 0; margin: 14px 0 0; font-size: 13px; }
.recs li { padding: 6px 0; display: flex; align-items: flex-start; gap: 8px; }
.recs .mdi { color: var(--accent); margin-top: 2px; }
</style>
