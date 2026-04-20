<template>
  <div>
    <div class="page-header" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
      <div>
        <h1>Eventos</h1>
        <p>Gestión de reservaciones y cotizaciones</p>
      </div>
      <button @click="openCreate" class="btn btn-primary">+ Nueva cotización</button>
    </div>

    <div class="page-body">
      <!-- Filters -->
      <div class="filters-bar">
        <button v-for="s in statusOptions" :key="s.value"
          :class="['filter-btn', statusFilter === s.value && 'active']"
          @click="setFilter(s.value)">
          {{ s.label }}
        </button>
      </div>

      <div class="card" style="padding:0">
        <table>
          <thead>
            <tr>
              <th>Evento</th>
              <th>Cliente</th>
              <th>Espacio</th>
              <th>Fecha</th>
              <th>Invitados</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading"><td colspan="8" style="text-align:center;color:var(--text2);padding:2rem">Cargando...</td></tr>
            <tr v-else-if="!events.length"><td colspan="8" style="text-align:center;color:var(--text2);padding:2rem">No hay eventos</td></tr>
            <tr v-for="ev in events" :key="ev.id">
              <td>
                <div class="ev-title">{{ ev.title }}</div>
                <div class="ev-type">{{ ev.event_type }}</div>
              </td>
              <td>{{ ev.client_name }}</td>
              <td>{{ ev.space_name || '—' }}</td>
              <td>{{ formatDate(ev.start_datetime) }}</td>
              <td>{{ ev.guests_count }}</td>
              <td>${{ ev.total_price?.toLocaleString() }}</td>
              <td><span :class="`badge badge-${ev.status}`">{{ statusLabel(ev.status) }}</span></td>
              <td>
                <div style="display:flex;gap:.5rem">
                  <select @change="e => updateStatus(ev, e.target.value)" :value="ev.status" class="status-select">
                    <option v-for="s in statusOptions.slice(1)" :key="s.value" :value="s.value">{{ s.label }}</option>
                  </select>
                  <button @click="editEvent(ev)" class="btn btn-ghost btn-sm">✏️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal" style="max-width:600px">
        <h2>{{ editing ? 'Editar evento' : 'Nueva cotización' }}</h2>

        <div class="form-row">
          <div class="form-group">
            <label>Cliente *</label>
            <select v-model="form.client_id" required>
              <option value="">Selecciona un cliente</option>
              <option v-for="c in clients" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Espacio</label>
            <select v-model="form.space_id">
              <option value="">Sin espacio específico</option>
              <option v-for="s in spaces" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Título del evento *</label>
          <input v-model="form.title" type="text" placeholder="Boda María & Juan" required />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Tipo de evento</label>
            <select v-model="form.event_type">
              <option value="boda">Boda</option>
              <option value="xv">XV Años</option>
              <option value="corporativo">Corporativo</option>
              <option value="graduacion">Graduación</option>
              <option value="otro">Otro</option>
            </select>
          </div>
          <div class="form-group">
            <label>Estado</label>
            <select v-model="form.status">
              <option v-for="s in statusOptions.slice(1)" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Inicio *</label>
            <input v-model="form.start_datetime" type="datetime-local" required />
          </div>
          <div class="form-group">
            <label>Fin *</label>
            <input v-model="form.end_datetime" type="datetime-local" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Invitados</label>
            <input v-model.number="form.guests_count" type="number" min="0" />
          </div>
          <div class="form-group">
            <label>Precio total ($)</label>
            <input v-model.number="form.total_price" type="number" min="0" />
          </div>
        </div>

        <div class="form-group">
          <label>Depósito ($)</label>
          <input v-model.number="form.deposit_amount" type="number" min="0" />
        </div>

        <div class="form-group">
          <label>Notas</label>
          <textarea v-model="form.notes" rows="3"></textarea>
        </div>

        <div class="modal-footer">
          <button @click="showModal = false" class="btn btn-ghost">Cancelar</button>
          <button @click="saveEvent" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : (editing ? 'Actualizar' : 'Crear cotización') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const events = ref([])
const clients = ref([])
const spaces = ref([])
const loading = ref(true)
const statusFilter = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)

const statusOptions = [
  { value: '', label: 'Todos' },
  { value: 'inquiry', label: 'Consulta' },
  { value: 'quote_sent', label: 'Cotización enviada' },
  { value: 'confirmed', label: 'Confirmado' },
  { value: 'deposit_paid', label: 'Depósito pagado' },
  { value: 'completed', label: 'Completado' },
  { value: 'cancelled', label: 'Cancelado' },
]

function statusLabel(s) {
  return statusOptions.find(x => x.value === s)?.label || s
}

const form = ref({
  client_id: '', space_id: '', title: '', event_type: 'boda',
  start_datetime: '', end_datetime: '', guests_count: 0,
  status: 'inquiry', total_price: 0, deposit_amount: 0, notes: ''
})

function formatDate(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function loadEvents() {
  loading.value = true
  try {
    const params = {}
    if (statusFilter.value) params.status = statusFilter.value
    const { data } = await api.get('/events/', { params })
    events.value = data
  } finally {
    loading.value = false
  }
}

async function setFilter(v) {
  statusFilter.value = v
  await loadEvents()
}

async function updateStatus(ev, status) {
  try {
    await api.put(`/events/${ev.id}`, { status })
    ev.status = status
  } catch (e) {
    alert('Error al actualizar estado')
  }
}

function openCreate() {
  editing.value = null
  form.value = {
    client_id: '', space_id: '', title: '', event_type: 'boda',
    start_datetime: '', end_datetime: '', guests_count: 0,
    status: 'inquiry', total_price: 0, deposit_amount: 0, notes: ''
  }
  showModal.value = true
}

function editEvent(ev) {
  editing.value = ev.id
  const toLocal = dt => dt ? dt.slice(0,16) : ''
  form.value = {
    client_id: ev.client_id,
    space_id: ev.space_id || '',
    title: ev.title,
    event_type: ev.event_type,
    start_datetime: toLocal(ev.start_datetime),
    end_datetime: toLocal(ev.end_datetime),
    guests_count: ev.guests_count,
    status: ev.status,
    total_price: ev.total_price,
    deposit_amount: ev.deposit_amount,
    notes: ev.notes || '',
  }
  showModal.value = true
}

async function saveEvent() {
  saving.value = true
  try {
    const payload = { ...form.value }
    if (!payload.space_id) payload.space_id = null
    if (!payload.client_id) { alert('Selecciona un cliente'); return }
    payload.client_id = parseInt(payload.client_id)
    if (editing.value) {
      await api.put(`/events/${editing.value}`, payload)
    } else {
      await api.post('/events/', payload)
    }
    showModal.value = false
    await loadEvents()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al guardar evento')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    loadEvents(),
    api.get('/clients/').then(r => clients.value = r.data),
    api.get('/spaces/').then(r => spaces.value = r.data),
  ])
})
</script>

<style scoped>
.filters-bar {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.filter-btn {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text2);
  padding: 0.4rem 0.9rem;
  border-radius: 20px;
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn.active, .filter-btn:hover {
  background: rgba(124,58,237,0.15);
  border-color: var(--primary);
  color: var(--primary);
}

.ev-title { font-size: 0.875rem; font-weight: 600; }
.ev-type { font-size: 0.75rem; color: var(--text2); text-transform: capitalize; }

.status-select {
  padding: 0.3rem 0.5rem;
  font-size: 0.78rem;
  border-radius: 6px;
  width: auto;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
</style>
