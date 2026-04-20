<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <h1 class="page-title">Reservas</h1>
      <p class="page-subtitle">Gestiona todas las solicitudes de renta</p>

      <!-- Kanban -->
      <div class="kanban">
        <div v-for="col in columns" :key="col.key" class="kanban-col">
          <div class="col-header" :style="{ borderTop: `3px solid ${col.color}` }">
            <span class="col-title">{{ col.label }}</span>
            <span class="col-count" :style="{ background: col.color + '20', color: col.color }">
              {{ getBookings(col.key).length }}
            </span>
          </div>
          <div class="col-cards">
            <div v-if="getBookings(col.key).length === 0" class="col-empty">
              Sin reservas
            </div>
            <div
              v-for="b in getBookings(col.key)"
              :key="b.id"
              class="booking-card"
              @click="openDetail(b)"
            >
              <div class="bc-item">{{ b.item_name }}</div>
              <div class="bc-customer">👤 {{ b.customer_name }}</div>
              <div class="bc-dates">
                {{ fmtDate(b.start_datetime) }} — {{ fmtDate(b.end_datetime) }}
              </div>
              <div class="bc-footer">
                <span class="bc-total">${{ fmt(b.total) }}</span>
                <span v-if="b.deposit_amount > 0" class="bc-deposit">Dep: ${{ fmt(b.deposit_amount) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Booking detail modal -->
      <div v-if="selectedBooking" class="modal-overlay" @click.self="selectedBooking = null">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">Reserva #{{ selectedBooking.id }}</h2>
            <button class="modal-close" @click="selectedBooking = null">×</button>
          </div>

          <div class="booking-detail">
            <div class="detail-section">
              <h4>Artículo</h4>
              <p><strong>{{ selectedBooking.item_name }}</strong></p>
              <p class="detail-sub">{{ selectedBooking.item_category }}</p>
            </div>

            <div class="detail-grid">
              <div class="detail-section">
                <h4>Cliente</h4>
                <p>{{ selectedBooking.customer_name }}</p>
                <p class="detail-sub">{{ selectedBooking.customer_email }}</p>
                <p v-if="selectedBooking.customer_phone" class="detail-sub">{{ selectedBooking.customer_phone }}</p>
              </div>
              <div class="detail-section">
                <h4>Fechas</h4>
                <p>{{ fmtDate(selectedBooking.start_datetime) }}</p>
                <p class="detail-sub">→ {{ fmtDate(selectedBooking.end_datetime) }}</p>
                <p class="detail-sub">{{ unitLabel(selectedBooking.rental_unit) }} · x{{ selectedBooking.quantity }}</p>
              </div>
            </div>

            <div class="detail-pricing">
              <div class="dp-row">
                <span>Precio unitario</span>
                <span>${{ fmt(selectedBooking.unit_price) }}</span>
              </div>
              <div class="dp-row">
                <span>Subtotal</span>
                <span>${{ fmt(selectedBooking.subtotal) }}</span>
              </div>
              <div v-if="selectedBooking.deposit_amount > 0" class="dp-row">
                <span>Depósito</span>
                <span style="color: var(--warning)">${{ fmt(selectedBooking.deposit_amount) }}</span>
              </div>
              <div class="dp-row total">
                <span><strong>Total</strong></span>
                <span><strong>${{ fmt(selectedBooking.total) }}</strong></span>
              </div>
            </div>

            <div v-if="selectedBooking.notes" class="detail-section">
              <h4>Notas del cliente</h4>
              <p class="detail-sub">{{ selectedBooking.notes }}</p>
            </div>

            <!-- Status change -->
            <div class="detail-section">
              <h4>Estado</h4>
              <div class="status-btns">
                <button
                  v-for="col in columns"
                  :key="col.key"
                  class="status-btn"
                  :class="{ active: selectedBooking.status === col.key }"
                  :style="selectedBooking.status === col.key ? { background: col.color, borderColor: col.color, color: 'white' } : { borderColor: col.color + '50', color: col.color }"
                  @click="changeStatus(col.key)"
                >
                  {{ col.label }}
                </button>
              </div>
            </div>

            <!-- Internal notes -->
            <div class="detail-section">
              <h4>Notas internas</h4>
              <textarea v-model="internalNotes" class="input" rows="3" placeholder="Notas que solo tú puedes ver..."></textarea>
              <button class="btn btn-secondary btn-sm" style="margin-top: 8px;" @click="saveNotes">Guardar notas</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { bookingsAPI } from '../../api/index.js'

const bookings = ref([])
const selectedBooking = ref(null)
const internalNotes = ref('')

const columns = [
  { key: 'inquiry', label: 'Consulta', color: '#f59e0b' },
  { key: 'quote_sent', label: 'Cotización', color: '#6366f1' },
  { key: 'confirmed', label: 'Confirmado', color: '#10b981' },
  { key: 'deposit_paid', label: 'Dep. pagado', color: '#06b6d4' },
  { key: 'active', label: 'Activo', color: '#8b5cf6' },
  { key: 'completed', label: 'Completado', color: '#64748b' },
  { key: 'cancelled', label: 'Cancelado', color: '#ef4444' },
]

function getBookings(status) {
  return bookings.value.filter(b => b.status === status)
}

function fmt(n) { return Number(n || 0).toLocaleString('es-MX') }
function fmtDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' })
}
function unitLabel(u) {
  return { hour: 'Por hora', day: 'Por día', weekend: 'Fin de semana', week: 'Por semana' }[u] || u
}

function openDetail(b) {
  selectedBooking.value = b
  internalNotes.value = b.internal_notes || ''
}

async function changeStatus(status) {
  if (!selectedBooking.value) return
  try {
    const res = await bookingsAPI.updateStatus(selectedBooking.value.id, status)
    const idx = bookings.value.findIndex(b => b.id === selectedBooking.value.id)
    if (idx !== -1) bookings.value[idx] = res.data
    selectedBooking.value = res.data
  } catch (e) {
    alert('Error al actualizar estado')
  }
}

async function saveNotes() {
  if (!selectedBooking.value) return
  try {
    await bookingsAPI.updateNotes(selectedBooking.value.id, internalNotes.value)
    const idx = bookings.value.findIndex(b => b.id === selectedBooking.value.id)
    if (idx !== -1) bookings.value[idx].internal_notes = internalNotes.value
    alert('Notas guardadas')
  } catch {
    alert('Error al guardar notas')
  }
}

onMounted(async () => {
  const res = await bookingsAPI.list()
  bookings.value = res.data
})
</script>

<style scoped>
.kanban {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 16px;
}

.kanban-col {
  min-width: 220px;
  flex-shrink: 0;
}

.col-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--bg2);
  border-radius: 10px 10px 0 0;
  border: 1px solid var(--border);
  border-bottom: none;
}
.col-title { font-size: 13px; font-weight: 700; }
.col-count {
  padding: 2px 8px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
}

.col-cards {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 10px 10px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 200px;
  max-height: calc(100vh - 260px);
  overflow-y: auto;
}

.col-empty {
  text-align: center;
  padding: 20px;
  color: var(--text2);
  font-size: 12px;
}

.booking-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.booking-card:hover { border-color: var(--border2); transform: translateY(-1px); }
.bc-item { font-size: 13px; font-weight: 700; margin-bottom: 4px; }
.bc-customer { font-size: 12px; color: var(--text2); margin-bottom: 3px; }
.bc-dates { font-size: 11px; color: var(--text2); margin-bottom: 8px; }
.bc-footer { display: flex; justify-content: space-between; align-items: center; }
.bc-total { font-size: 13px; font-weight: 700; color: var(--success); }
.bc-deposit { font-size: 11px; color: var(--warning); }

/* Detail modal */
.booking-detail { display: flex; flex-direction: column; gap: 16px; }
.detail-section h4 { font-size: 12px; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
.detail-section p { font-size: 14px; }
.detail-sub { color: var(--text2); font-size: 13px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.detail-pricing {
  background: var(--bg3);
  border-radius: 8px;
  padding: 12px;
}
.dp-row { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: var(--text2); }
.dp-row.total { border-top: 1px solid var(--border); padding-top: 10px; margin-top: 4px; font-size: 15px; color: var(--text); }

.status-btns { display: flex; flex-wrap: wrap; gap: 6px; }
.status-btn {
  padding: 5px 10px;
  border-radius: 6px;
  border: 1px solid;
  background: transparent;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
</style>
