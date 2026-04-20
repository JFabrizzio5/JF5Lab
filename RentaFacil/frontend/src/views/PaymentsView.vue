<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Pagos</h1>
      <div class="header-actions">
        <select v-model="statusFilter" @change="load" class="filter-select">
          <option value="">Todos</option>
          <option value="pending">Pendientes</option>
          <option value="paid">Pagados</option>
          <option value="overdue">Vencidos</option>
        </select>
        <button class="btn btn-primary" @click="openModal()">+ Registrar pago</button>
      </div>
    </div>

    <div v-if="overdueCount > 0" class="alert-banner">
      ⚠️ Tienes <strong>{{ overdueCount }}</strong> pago(s) vencido(s).
    </div>

    <div class="card">
      <div v-if="loading" class="empty">Cargando...</div>
      <div v-else-if="!items.length" class="empty">Sin pagos para mostrar.</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Contrato ID</th>
              <th>Monto</th>
              <th>Vencimiento</th>
              <th>Pagado el</th>
              <th>Método</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in items" :key="p.id" :class="{ 'row-overdue': isOverdue(p) }">
              <td>#{{ p.contract_id }}</td>
              <td><strong>${{ fmt(p.amount) }}</strong></td>
              <td>{{ p.due_date }}</td>
              <td>{{ p.paid_date || '—' }}</td>
              <td>{{ p.payment_method || '—' }}</td>
              <td><span class="badge" :class="paymentClass(p)">{{ paymentLabel(p) }}</span></td>
              <td>
                <div class="actions">
                  <button v-if="p.status !== 'paid'" class="btn btn-success" @click="markPaid(p)">Cobrado</button>
                  <button class="btn btn-secondary" @click="openEdit(p)">Editar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="modal" class="modal-overlay" @click.self="modal = false">
      <div class="modal">
        <div class="modal-title">{{ editing ? 'Editar pago' : 'Registrar pago' }}</div>
        <form @submit.prevent="save">
          <div class="form-grid">
            <div class="form-group" style="grid-column: 1 / -1" v-if="!editing">
              <label>Contrato *</label>
              <select v-model="form.contract_id" required>
                <option value="">Seleccionar...</option>
                <option v-for="c in contractList" :key="c.id" :value="c.id">
                  #{{ c.id }} — {{ c.tenant?.name }} / {{ c.property?.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Monto ($) *</label>
              <input v-model="form.amount" type="number" step="0.01" required />
            </div>
            <div class="form-group">
              <label>Fecha de vencimiento *</label>
              <input v-model="form.due_date" type="date" required />
            </div>
            <div class="form-group">
              <label>Estado</label>
              <select v-model="form.status">
                <option value="pending">Pendiente</option>
                <option value="paid">Pagado</option>
              </select>
            </div>
            <div class="form-group">
              <label>Método de pago</label>
              <select v-model="form.payment_method">
                <option value="">—</option>
                <option value="transfer">Transferencia</option>
                <option value="cash">Efectivo</option>
                <option value="card">Tarjeta</option>
                <option value="check">Cheque</option>
              </select>
            </div>
            <div class="form-group">
              <label>Fecha de pago</label>
              <input v-model="form.paid_date" type="date" />
            </div>
            <div class="form-group">
              <label>Referencia</label>
              <input v-model="form.reference" />
            </div>
            <div class="form-group" style="grid-column: 1 / -1">
              <label>Notas</label>
              <textarea v-model="form.notes" rows="2"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="modal = false">Cancelar</button>
            <button type="submit" class="btn btn-primary">{{ editing ? 'Guardar' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { payments as api, contracts } from '../api/client'

const items = ref([])
const contractList = ref([])
const loading = ref(true)
const modal = ref(false)
const editing = ref(null)
const statusFilter = ref('')
const overdueCount = ref(0)
const blank = () => ({ contract_id: '', amount: '', due_date: '', paid_date: '', status: 'pending', payment_method: '', reference: '', notes: '' })
const form = reactive(blank())

const fmt = n => Number(n || 0).toLocaleString('es-MX', { minimumFractionDigits: 2 })
const isOverdue = p => p.status === 'pending' && new Date(p.due_date) < new Date()
const paymentLabel = p => {
  if (p.status === 'paid') return 'Pagado'
  if (isOverdue(p)) return 'Vencido'
  return 'Pendiente'
}
const paymentClass = p => {
  if (p.status === 'paid') return 'badge-green'
  if (isOverdue(p)) return 'badge-red'
  return 'badge-yellow'
}

async function load() {
  const status = statusFilter.value === 'overdue' ? null : statusFilter.value || null
  const [p, ov] = await Promise.all([api.list(status), api.overdue()])
  items.value = statusFilter.value === 'overdue' ? ov.data : p.data
  overdueCount.value = ov.data.length
}

async function loadContracts() {
  const { data } = await contracts.list()
  contractList.value = data
}

function openModal() {
  editing.value = null
  Object.assign(form, blank())
  modal.value = true
}

function openEdit(p) {
  editing.value = p.id
  Object.assign(form, {
    contract_id: p.contract_id,
    amount: p.amount,
    due_date: p.due_date,
    paid_date: p.paid_date || '',
    status: p.status,
    payment_method: p.payment_method || '',
    reference: p.reference || '',
    notes: p.notes || ''
  })
  modal.value = true
}

async function save() {
  const payload = { ...form, amount: parseFloat(form.amount) }
  if (!payload.paid_date) delete payload.paid_date
  if (!payload.payment_method) delete payload.payment_method
  if (!payload.reference) delete payload.reference
  if (editing.value) {
    await api.update(editing.value, payload)
  } else {
    await api.create(payload)
  }
  modal.value = false
  await load()
}

async function markPaid(p) {
  const today = new Date().toISOString().slice(0, 10)
  await api.markPaid(p.id, { paid_date: today, status: 'paid' })
  await load()
}

onMounted(async () => {
  try { await Promise.all([load(), loadContracts()]) } finally { loading.value = false }
})
</script>

<style scoped>
.header-actions { display: flex; gap: 12px; align-items: center; }
.filter-select { padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 0.9rem; }
.actions { display: flex; gap: 8px; }
.alert-banner { background: #fef3c7; border: 1px solid #f59e0b; color: #92400e; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 0.9rem; }
.row-overdue td { background: #fff7ed; }
</style>
