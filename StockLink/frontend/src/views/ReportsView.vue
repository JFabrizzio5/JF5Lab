<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { reportsApi, exportsApi } from '../api/endpoints'

const report = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try { const { data } = await reportsApi.viability(); report.value = data } finally { loading.value = false }
}
onMounted(load)

function verdictClass(v) {
  return { 'Excelente':'success','Bueno':'accent','Atención':'warn','Crítico':'danger' }[v] || ''
}
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div><h1>Reporte de viabilidad</h1><p class="muted">Análisis automático con recomendaciones.</p></div>
      <div class="actions">
        <button class="btn btn-sm" @click="exportsApi.inventory()"><i class="mdi mdi-file-excel"></i> Inventario</button>
        <button class="btn btn-sm" @click="exportsApi.movements()"><i class="mdi mdi-file-excel"></i> Movimientos</button>
        <button class="btn btn-sm" @click="exportsApi.attendance()"><i class="mdi mdi-file-excel"></i> Asistencias</button>
      </div>
    </div>

    <div v-if="loading" class="muted"><i class="mdi mdi-loading mdi-spin"></i> Calculando…</div>
    <div v-else-if="report">
      <div class="card" style="text-align:center; padding:40px;">
        <div class="muted" style="text-transform:uppercase; font-size:12px; letter-spacing:.1em;">Score de salud</div>
        <div style="font-size:72px; font-weight:800; letter-spacing:-0.02em; color:var(--accent);">{{ report.health_score }}</div>
        <span class="badge" :class="verdictClass(report.verdict)" style="font-size:14px; padding:6px 16px;">{{ report.verdict }}</span>
      </div>

      <div class="grid-4" style="margin-top:20px;">
        <div class="card kpi"><div class="muted small">Artículos</div><div class="kval">{{ report.total_items }}</div></div>
        <div class="card kpi"><div class="muted small">Almacenes</div><div class="kval">{{ report.total_warehouses }}</div></div>
        <div class="card kpi"><div class="muted small">Movs. 30d</div><div class="kval">{{ report.movements_last_30d }}</div></div>
        <div class="card kpi"><div class="muted small">Valor inventario</div><div class="kval">${{ Number(report.stock_value_mxn).toLocaleString('es-MX', {maximumFractionDigits:0}) }}</div></div>
      </div>

      <div class="grid-2" style="margin-top:20px;">
        <div class="card">
          <h3 style="margin-top:0;">Top consumos últimos 30 días</h3>
          <table class="table">
            <thead><tr><th>Artículo</th><th>Qty</th></tr></thead>
            <tbody>
              <tr v-for="t in report.top_consumers_last_30d" :key="t.name"><td>{{ t.name }}</td><td class="mono">{{ t.qty }}</td></tr>
              <tr v-if="!report.top_consumers_last_30d.length"><td colspan="2" class="muted">Sin datos.</td></tr>
            </tbody>
          </table>
        </div>
        <div class="card">
          <h3 style="margin-top:0;">Recomendaciones</h3>
          <ul style="list-style:none; padding:0; margin:0;">
            <li v-for="r in report.recommendations" :key="r" style="padding:8px 0; border-bottom:1px dashed var(--border);">
              <i class="mdi mdi-lightbulb-on" style="color:var(--accent);"></i> {{ r }}
            </li>
            <li v-if="!report.recommendations.length" class="muted"><i class="mdi mdi-check-circle" style="color:var(--success);"></i> Todo en orden.</li>
          </ul>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
.kval { font-size: 26px; font-weight: 800; margin-top: 4px; }
.small { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; font-weight: 600; }
</style>
