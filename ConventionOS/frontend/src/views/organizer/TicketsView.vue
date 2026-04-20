<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Boletos</h1>
        <button @click="openModal(null)" class="btn btn-primary">+ Tipo de Boleto</button>
      </div>

      <!-- Ticket types -->
      <div class="types-grid">
        <div v-for="tt in ticketTypes" :key="tt.id" class="type-card" :style="`--tc: ${tt.color}`">
          <div class="type-bar" :style="`background: ${tt.color}`"></div>
          <div class="type-body">
            <div class="type-name">{{ tt.name }}</div>
            <div class="type-price">${{ tt.price.toFixed(0) }} MXN</div>
            <div class="type-sold">{{ tt.quantity_sold }} / {{ tt.quantity_total || '∞' }} vendidos</div>
            <div class="qty-bar" v-if="tt.quantity_total">
              <div class="qty-fill" :style="`width:${Math.min(100, tt.quantity_sold / tt.quantity_total * 100)}%;background:${tt.color}`"></div>
            </div>
            <div class="type-benefits" v-if="tt.benefits_json">
              <span v-for="b in parseBenefits(tt.benefits_json)" :key="b" class="benefit-tag">✓ {{ b }}</span>
            </div>
            <div class="type-actions">
              <button @click="openModal(tt)" class="btn btn-ghost btn-sm">Editar</button>
              <button @click="deleteType(tt)" class="btn btn-danger btn-sm">Eliminar</button>
            </div>
          </div>
        </div>
        <div v-if="!ticketTypes.length" class="empty-card">Sin tipos de boletos. Agrega el primero.</div>
      </div>

      <!-- Purchased tickets -->
      <div class="tickets-section">
        <div class="section-header">
          <h2>Boletos Comprados</h2>
          <input v-model="search" placeholder="Buscar por nombre o email..." class="search-input" style="max-width:280px" />
        </div>
        <table>
          <thead>
            <tr><th>ID</th><th>Asistente</th><th>Email</th><th>Tipo</th><th>QR Code</th><th>Estado</th><th>Fecha</th></tr>
          </thead>
          <tbody>
            <tr v-for="t in filteredTickets" :key="t.id">
              <td>#{{ t.id }}</td>
              <td>{{ t.attendee_name }}</td>
              <td>{{ t.attendee_email }}</td>
              <td><span class="badge" :style="`background:${t.ticket_type?.color}22;color:${t.ticket_type?.color}`">{{ t.ticket_type?.name }}</span></td>
              <td><code class="qr-code">{{ t.qr_code }}</code></td>
              <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
              <td>{{ fmtDate(t.created_at) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="!filteredTickets.length" class="empty-state">Sin boletos comprados aún</div>
      </div>

      <!-- Modal -->
      <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
        <div class="modal">
          <h2>{{ editing?.id ? 'Editar Tipo de Boleto' : 'Nuevo Tipo de Boleto' }}</h2>
          <div class="form-group"><label>Nombre *</label><input v-model="form.name" placeholder="General, VIP, Exhibidor..." /></div>
          <div class="form-group"><label>Descripción</label><textarea v-model="form.description" rows="2"></textarea></div>
          <div class="form-group"><label>Precio (MXN)</label><input v-model.number="form.price" type="number" min="0" /></div>
          <div class="form-group"><label>Cantidad total (dejar vacío = sin límite)</label><input v-model.number="form.quantity_total" type="number" min="0" /></div>
          <div class="form-group">
            <label>Color</label>
            <div style="display:flex;gap:10px;align-items:center">
              <input type="color" v-model="form.color" style="width:50px;height:40px;border-radius:6px;cursor:pointer;padding:2px" />
              <input v-model="form.color" />
            </div>
          </div>
          <div class="form-group">
            <label>Beneficios</label>
            <div v-for="(b, i) in benefits" :key="i" class="benefit-row">
              <input v-model="benefits[i]" placeholder="Beneficio..." />
              <button @click="benefits.splice(i, 1)" class="btn btn-danger btn-sm">✕</button>
            </div>
            <button @click="benefits.push('')" class="btn btn-ghost btn-sm" style="margin-top:8px">+ Agregar beneficio</button>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Venta inicia</label><input v-model="form.sale_start" type="datetime-local" /></div>
            <div class="form-group"><label>Venta termina</label><input v-model="form.sale_end" type="datetime-local" /></div>
          </div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="showModal = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
            <button @click="save" :disabled="!form.name" class="btn btn-primary" style="flex:1">Guardar</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const ticketTypes = ref([])
const tickets = ref([])
const showModal = ref(false)
const editing = ref(null)
const search = ref('')
const benefits = ref([])
const form = ref({ name: '', description: '', price: 0, quantity_total: null, color: '#6366f1', sale_start: '', sale_end: '' })

function parseBenefits(json) {
  try { return JSON.parse(json) } catch { return [] }
}

function statusBadge(s) {
  if (s === 'paid' || s === 'checked_in') return 'badge-success'
  if (s === 'pending') return 'badge-warning'
  if (s === 'cancelled' || s === 'refunded') return 'badge-danger'
  return 'badge-primary'
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
}

const filteredTickets = computed(() => {
  if (!search.value) return tickets.value
  const q = search.value.toLowerCase()
  return tickets.value.filter(t =>
    t.attendee_name?.toLowerCase().includes(q) ||
    t.attendee_email?.toLowerCase().includes(q)
  )
})

function openModal(tt) {
  editing.value = tt
  if (tt) {
    Object.assign(form.value, { ...tt, sale_start: tt.sale_start ? tt.sale_start.slice(0, 16) : '', sale_end: tt.sale_end ? tt.sale_end.slice(0, 16) : '' })
    benefits.value = parseBenefits(tt.benefits_json)
  } else {
    form.value = { name: '', description: '', price: 0, quantity_total: null, color: '#6366f1', sale_start: '', sale_end: '' }
    benefits.value = []
  }
  showModal.value = true
}

async function save() {
  const payload = {
    ...form.value,
    convention_id: conv.value.id,
    benefits_json: JSON.stringify(benefits.value.filter(b => b.trim())),
  }
  if (editing.value?.id) {
    const { data } = await api.put(`/tickets/types/${editing.value.id}`, payload)
    const idx = ticketTypes.value.findIndex(t => t.id === data.id)
    if (idx >= 0) ticketTypes.value[idx] = data
  } else {
    const { data } = await api.post('/tickets/types', payload)
    ticketTypes.value.push(data)
  }
  showModal.value = false
}

async function deleteType(tt) {
  if (!confirm('¿Eliminar tipo de boleto?')) return
  await api.delete(`/tickets/types/${tt.id}`)
  ticketTypes.value = ticketTypes.value.filter(t => t.id !== tt.id)
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  const [typesRes, ticketsRes] = await Promise.all([
    api.get(`/tickets/types/convention/${conv.value.id}`),
    api.get(`/tickets/convention/${conv.value.id}`),
  ])
  ticketTypes.value = typesRes.data
  tickets.value = ticketsRes.data
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.types-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; margin-bottom: 32px; }
.type-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.type-bar { height: 4px; }
.type-body { padding: 16px; }
.type-name { font-weight: 800; font-size: 16px; }
.type-price { font-size: 24px; font-weight: 900; color: var(--tc); margin: 4px 0; }
.type-sold { font-size: 12px; color: var(--text2); margin-bottom: 8px; }
.qty-bar { height: 4px; background: var(--border); border-radius: 2px; margin-bottom: 8px; }
.qty-fill { height: 100%; border-radius: 2px; }
.type-benefits { display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px; }
.benefit-tag { font-size: 11px; color: var(--text2); }
.type-actions { display: flex; gap: 8px; }
.empty-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 40px; text-align: center; color: var(--text2); grid-column: 1/-1; }
.tickets-section { margin-top: 8px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.section-header h2 { font-size: 18px; font-weight: 700; }
.search-input {}
code.qr-code { font-family: monospace; font-size: 12px; background: var(--bg3); padding: 2px 6px; border-radius: 4px; }
.empty-state { padding: 20px; text-align: center; color: var(--text2); }
.benefit-row { display: flex; gap: 8px; margin-bottom: 8px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.modal .form-group { margin-top: 12px; }
</style>
