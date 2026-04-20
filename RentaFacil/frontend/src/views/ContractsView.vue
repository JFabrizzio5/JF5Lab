<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Contratos</h1>
      <button class="btn btn-primary" @click="openModal()">+ Nuevo contrato</button>
    </div>

    <div class="card">
      <div v-if="loading" class="empty">Cargando...</div>
      <div v-else-if="!items.length" class="empty">Sin contratos registrados.</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Propiedad</th>
              <th>Inquilino</th>
              <th>Inicio</th>
              <th>Fin</th>
              <th>Renta</th>
              <th>Depósito</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in items" :key="c.id">
              <td>{{ c.property?.name || '—' }}</td>
              <td>{{ c.tenant?.name || '—' }}</td>
              <td>{{ c.start_date }}</td>
              <td>{{ c.end_date }}</td>
              <td>${{ fmt(c.rent_amount) }}</td>
              <td>${{ fmt(c.deposit_amount) }}</td>
              <td><span class="badge" :class="statusClass(c.status)">{{ statusLabel(c.status) }}</span></td>
              <td>
                <button class="btn btn-secondary" @click="openEdit(c)">Editar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="modal" class="modal-overlay" @click.self="modal = false">
      <div class="modal">
        <div class="modal-title">{{ editing ? 'Editar contrato' : 'Nuevo contrato' }}</div>
        <form @submit.prevent="save">
          <div class="form-grid">
            <div class="form-group">
              <label>Propiedad *</label>
              <select v-model="form.property_id" required :disabled="!!editing">
                <option value="">Seleccionar...</option>
                <option v-for="p in propList" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Inquilino *</label>
              <select v-model="form.tenant_id" required :disabled="!!editing">
                <option value="">Seleccionar...</option>
                <option v-for="t in tenantList" :key="t.id" :value="t.id">{{ t.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Fecha inicio *</label>
              <input v-model="form.start_date" type="date" required />
            </div>
            <div class="form-group">
              <label>Fecha fin *</label>
              <input v-model="form.end_date" type="date" required />
            </div>
            <div class="form-group">
              <label>Renta mensual ($) *</label>
              <input v-model="form.rent_amount" type="number" step="0.01" required />
            </div>
            <div class="form-group">
              <label>Depósito ($)</label>
              <input v-model="form.deposit_amount" type="number" step="0.01" />
            </div>
            <div class="form-group">
              <label>Estado</label>
              <select v-model="form.status">
                <option value="active">Activo</option>
                <option value="expired">Vencido</option>
                <option value="cancelled">Cancelado</option>
              </select>
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
import { ref, reactive, onMounted } from 'vue'
import { contracts as api, properties, tenants } from '../api/client'

const items = ref([])
const propList = ref([])
const tenantList = ref([])
const loading = ref(true)
const modal = ref(false)
const editing = ref(null)
const blank = () => ({ property_id: '', tenant_id: '', start_date: '', end_date: '', rent_amount: '', deposit_amount: '0', status: 'active', notes: '' })
const form = reactive(blank())

const fmt = n => Number(n || 0).toLocaleString('es-MX', { minimumFractionDigits: 2 })
const statusLabel = s => ({ active: 'Activo', expired: 'Vencido', cancelled: 'Cancelado' }[s] || s)
const statusClass = s => ({ active: 'badge-green', expired: 'badge-gray', cancelled: 'badge-red' }[s] || 'badge-gray')

async function load() {
  const [c, p, t] = await Promise.all([api.list(), properties.list(), tenants.list()])
  items.value = c.data
  propList.value = p.data
  tenantList.value = t.data
}

function openModal() {
  editing.value = null
  Object.assign(form, blank())
  modal.value = true
}

function openEdit(c) {
  editing.value = c.id
  Object.assign(form, {
    property_id: c.property_id,
    tenant_id: c.tenant_id,
    start_date: c.start_date,
    end_date: c.end_date,
    rent_amount: c.rent_amount,
    deposit_amount: c.deposit_amount,
    status: c.status,
    notes: c.notes || ''
  })
  modal.value = true
}

async function save() {
  const payload = { ...form, rent_amount: parseFloat(form.rent_amount), deposit_amount: parseFloat(form.deposit_amount) }
  if (editing.value) {
    await api.update(editing.value, { start_date: payload.start_date, end_date: payload.end_date, rent_amount: payload.rent_amount, deposit_amount: payload.deposit_amount, status: payload.status, notes: payload.notes })
  } else {
    await api.create(payload)
  }
  modal.value = false
  await load()
}

onMounted(async () => {
  try { await load() } finally { loading.value = false }
})
</script>
