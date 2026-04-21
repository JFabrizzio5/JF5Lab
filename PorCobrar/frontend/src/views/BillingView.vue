<script setup>
import { ref, onMounted } from 'vue'
import api, { downloadBlob } from '../api/client'

const runs = ref([])
const dashboard = ref(null)

function fmt(n) { return '$' + Number(n || 0).toLocaleString('es-MX', { maximumFractionDigits: 0 }) }

onMounted(async () => {
  try {
    const [u, d] = await Promise.all([api.get('/dunning/upcoming?days=14'), api.get('/dashboard')])
    runs.value = u.data
    dashboard.value = d.data
  } catch(e) {}
})

async function execute(id) {
  try { await api.post(`/dunning/${id}/execute`); runs.value = runs.value.filter(r => r.id !== id) } catch(e) {}
}
</script>

<template>
  <div>
    <h1>Billing & cobranza</h1>
    <div class="muted" style="font-size:13px; margin-bottom:18px">Pagos recibidos y próximos envíos programados.</div>

    <div class="grid-3" v-if="dashboard">
      <div class="card"><div class="kpi-label">Cobrado MTD</div><div class="kpi-number" style="color:var(--cash)">{{ fmt(dashboard.paid_mtd) }}</div></div>
      <div class="card"><div class="kpi-label">Por cobrar</div><div class="kpi-number" style="color:var(--warn)">{{ fmt(dashboard.total_owed) }}</div></div>
      <div class="card"><div class="kpi-label">DSO</div><div class="kpi-number">{{ dashboard.dso_days }} días</div></div>
    </div>

    <div class="card" style="margin-top: 18px; padding:0">
      <div style="padding:14px 18px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border)">
        <h3>Próximos envíos (14 días)</h3>
        <button class="btn btn-sm" @click="downloadBlob('/exports/cartera-antiguedad.xlsx','cartera.xlsx')"><i class="mdi mdi-file-excel-outline"></i> Cartera XLSX</button>
      </div>
      <table class="table">
        <thead>
          <tr><th>Fecha</th><th>Canal</th><th>Paso</th><th>Factura</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="r in runs" :key="r.id">
            <td class="muted">{{ r.scheduled_at.slice(0,16).replace('T',' ') }}</td>
            <td><span class="chip-channel" :class="r.channel">{{ r.channel }}</span></td>
            <td>{{ r.step_index + 1 }}</td>
            <td class="mono" style="font-size:11px">{{ r.invoice_id.slice(0,8) }}…</td>
            <td><button class="btn btn-sm btn-primary" @click="execute(r.id)"><i class="mdi mdi-send"></i> Ejecutar ahora</button></td>
          </tr>
          <tr v-if="!runs.length"><td colspan="5" class="muted" style="text-align:center; padding: 22px">Sin envíos programados. Asigna un flow a una factura.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
