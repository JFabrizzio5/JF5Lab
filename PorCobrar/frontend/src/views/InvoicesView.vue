<script setup>
import { ref, onMounted, computed } from 'vue'
import api, { downloadBlob } from '../api/client'

const invoices = ref([])
const debtors = ref({})
const flows = ref([])
const filter = ref('all')
const loading = ref(true)
const selected = ref(new Set())
const msg = ref('')

function fmt(n) { return '$' + Number(n || 0).toLocaleString('es-MX', { maximumFractionDigits: 0 }) }

async function load() {
  loading.value = true
  try {
    const [i, d, f] = await Promise.all([
      api.get('/invoices'), api.get('/debtors'), api.get('/dunning-flows')
    ])
    invoices.value = i.data
    debtors.value = Object.fromEntries(d.data.map(x => [x.id, x]))
    flows.value = f.data
  } catch(e) { msg.value = e.message }
  loading.value = false
}
onMounted(load)

const filtered = computed(() => {
  if (filter.value === 'all') return invoices.value
  if (filter.value === 'overdue') return invoices.value.filter(i => i.status === 'overdue')
  if (filter.value === 'pending') return invoices.value.filter(i => ['pending','partial'].includes(i.status))
  if (filter.value === 'paid')    return invoices.value.filter(i => i.status === 'paid')
  return invoices.value
})

function statusBadge(s) {
  return s === 'paid' ? 'cash'
    : s === 'overdue' ? 'danger'
    : s === 'partial' ? 'warn' : 'info'
}
function debtorName(id) { return debtors.value[id]?.name || '—' }

function toggleSel(id) {
  if (selected.value.has(id)) selected.value.delete(id)
  else selected.value.add(id)
  selected.value = new Set(selected.value)
}

async function assignFlow() {
  const f = flows.value[0]?.id
  if (!f) { msg.value = 'No hay flows disponibles.'; return }
  let ok = 0
  for (const id of selected.value) {
    try { await api.post(`/invoices/${id}/assign-flow`, { flow_id: f }); ok++ } catch {}
  }
  msg.value = `Flow "${flows.value[0].name}" asignado a ${ok} facturas.`
  selected.value = new Set()
}

async function generateLinks() {
  let ok = 0
  const links = []
  for (const id of selected.value) {
    try {
      const { data } = await api.post(`/invoices/${id}/payment-link`)
      links.push(data.link); ok++
    } catch {}
  }
  msg.value = `Generados ${ok} payment links.` + (links.length ? ' Ejemplo: ' + links[0] : '')
  selected.value = new Set()
}

async function sendReminder() {
  let ok = 0
  for (const id of selected.value) {
    try {
      await api.post(`/invoices/${id}/assign-flow`, { flow_id: flows.value[0].id })
      ok++
    } catch {}
  }
  msg.value = `${ok} recordatorios encolados.`
  selected.value = new Set()
}

async function onePayLink(invId) {
  try {
    const { data } = await api.post(`/invoices/${invId}/payment-link`)
    msg.value = 'Link: ' + data.link
    navigator.clipboard?.writeText(data.link)
  } catch(e) { msg.value = e.message }
}

async function exportXlsx() { await downloadBlob('/exports/invoices.xlsx', 'porcobrar-invoices.xlsx') }
</script>

<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 14px">
      <div>
        <h1>Facturas</h1>
        <div class="muted" style="font-size:13px">Cartera completa · {{ filtered.length }} resultados</div>
      </div>
      <div style="display:flex; gap:8px">
        <button class="btn btn-sm" @click="exportXlsx"><i class="mdi mdi-file-excel-outline"></i> Exportar .xlsx</button>
        <button class="btn btn-sm" @click="load"><i class="mdi mdi-refresh"></i> Refrescar</button>
      </div>
    </div>

    <div class="card-inset" style="display:flex; gap:6px; margin-bottom: 14px">
      <button class="btn btn-sm" :class="{'btn-primary': filter==='all'}" @click="filter='all'">Todas ({{invoices.length}})</button>
      <button class="btn btn-sm" :class="{'btn-primary': filter==='overdue'}" @click="filter='overdue'">Vencidas</button>
      <button class="btn btn-sm" :class="{'btn-primary': filter==='pending'}" @click="filter='pending'">Pendientes</button>
      <button class="btn btn-sm" :class="{'btn-primary': filter==='paid'}" @click="filter='paid'">Pagadas</button>
    </div>

    <div class="card-inset" v-if="selected.size" style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px; border-color: var(--cash)">
      <div><strong>{{ selected.size }}</strong> seleccionadas</div>
      <div style="display:flex; gap:8px">
        <button class="btn btn-sm" @click="assignFlow"><i class="mdi mdi-transit-connection-variant"></i> Asignar flow</button>
        <button class="btn btn-sm" @click="sendReminder"><i class="mdi mdi-email-fast-outline"></i> Mandar recordatorio</button>
        <button class="btn btn-sm btn-primary" @click="generateLinks"><i class="mdi mdi-link-variant"></i> Generar links</button>
      </div>
    </div>

    <div class="card" style="padding:0; overflow-x:auto">
      <table class="table">
        <thead>
          <tr>
            <th style="width:30px"></th>
            <th>Folio</th>
            <th>Deudor</th>
            <th>Emitida</th>
            <th>Vence</th>
            <th>Status</th>
            <th class="num">Total</th>
            <th class="num">Saldo</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inv in filtered" :key="inv.id">
            <td><input type="checkbox" :checked="selected.has(inv.id)" @change="toggleSel(inv.id)" style="width:auto"></td>
            <td><span class="mono">{{ inv.serie }}{{ inv.folio }}</span></td>
            <td>{{ debtorName(inv.debtor_id) }}</td>
            <td class="muted">{{ inv.issued_at ? inv.issued_at.slice(0,10) : '—' }}</td>
            <td class="muted">{{ inv.due_at ? inv.due_at.slice(0,10) : '—' }}</td>
            <td><span class="badge" :class="statusBadge(inv.status)">{{ inv.status }}</span></td>
            <td class="num">{{ fmt(inv.total) }}</td>
            <td class="num">{{ fmt(Number(inv.total) - Number(inv.paid_amount)) }}</td>
            <td>
              <button class="btn btn-sm" @click="onePayLink(inv.id)"><i class="mdi mdi-link-variant"></i> Link</button>
            </td>
          </tr>
          <tr v-if="!loading && !filtered.length"><td colspan="9" class="muted" style="text-align:center; padding: 22px">Sin facturas.</td></tr>
        </tbody>
      </table>
    </div>

    <div v-if="msg" class="card" style="margin-top: 14px; border-color: var(--cash)">
      <i class="mdi mdi-information-outline"></i> {{ msg }}
    </div>
  </div>
</template>
