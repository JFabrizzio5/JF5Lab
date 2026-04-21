<script setup>
import { ref, onMounted } from 'vue'
import api, { downloadBlob } from '../api/client'

const list = ref([])
const q = ref('')
const loading = ref(true)
const msg = ref('')

function fmt(n) { return '$' + Number(n || 0).toLocaleString('es-MX', { maximumFractionDigits: 0 }) }
function scoreClass(s) { if (s >= 70) return 's-hi'; if (s >= 40) return 's-md'; return 's-lo' }

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/debtors' + (q.value ? '?q='+encodeURIComponent(q.value) : ''))
    list.value = data
  } catch(e) { msg.value = e.message }
  loading.value = false
}
onMounted(load)

async function recalc(id) {
  try {
    const { data } = await api.post(`/debtors/${id}/recalculate-score`)
    msg.value = `Score actualizado: ${data.score}`
    await load()
  } catch(e) { msg.value = e.message }
}

async function exportXlsx() { await downloadBlob('/exports/debtors.xlsx', 'porcobrar-debtors.xlsx') }
</script>

<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 14px">
      <div>
        <h1>Deudores</h1>
        <div class="muted" style="font-size:13px">{{ list.length }} clientes · score IA de pago</div>
      </div>
      <div style="display:flex; gap:8px">
        <input v-model="q" @keyup.enter="load" placeholder="Buscar deudor..." style="width:240px">
        <button class="btn btn-sm" @click="load"><i class="mdi mdi-magnify"></i> Buscar</button>
        <button class="btn btn-sm" @click="exportXlsx"><i class="mdi mdi-file-excel-outline"></i> Exportar</button>
      </div>
    </div>

    <div class="card" style="padding:0; overflow-x:auto">
      <table class="table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>RFC</th>
            <th>Contacto</th>
            <th>Score</th>
            <th class="num">Adeudo total</th>
            <th class="num">Dias prom. atraso</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in list" :key="d.id">
            <td>{{ d.name }}</td>
            <td><span class="mono">{{ d.rfc }}</span></td>
            <td style="font-size:12px">
              <div v-if="d.email">{{ d.email }}</div>
              <div class="muted" v-if="d.phone">{{ d.phone }}</div>
            </td>
            <td><span class="score-pill" :class="scoreClass(d.payment_score)">{{ d.payment_score }}</span></td>
            <td class="num">{{ fmt(d.total_owed) }}</td>
            <td class="num">{{ d.overdue_days_avg }}d</td>
            <td><button class="btn btn-sm" @click="recalc(d.id)"><i class="mdi mdi-brain"></i> Recalcular</button></td>
          </tr>
          <tr v-if="!list.length"><td colspan="7" class="muted" style="text-align:center; padding:22px">Sin deudores.</td></tr>
        </tbody>
      </table>
    </div>

    <div v-if="msg" class="card" style="margin-top: 14px; border-color:var(--cash)">
      <i class="mdi mdi-information-outline"></i> {{ msg }}
    </div>
  </div>
</template>
