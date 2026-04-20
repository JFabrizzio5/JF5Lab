<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Mi Horario</h1>
        <p>Gestiona tus horarios de tutoría disponibles</p>
      </div>
      <button @click="showAddSlot = true" class="btn btn-primary">+ Agregar Horario</button>
    </div>

    <div class="page-content">
      <div class="sched-layout">
        <!-- Slots -->
        <div>
          <h2 class="section-title">Mis Horarios</h2>
          <div v-if="loadingSlots" class="loading">Cargando...</div>
          <div v-else-if="slots.length === 0" class="empty-state" style="padding:30px 0">
            <p>No tienes horarios configurados</p>
          </div>
          <div v-else class="day-groups">
            <div v-for="(daySlots, dayName) in groupedSlots" :key="dayName" class="day-section">
              <h3 class="day-name">{{ dayName }}</h3>
              <div class="slot-cards">
                <div v-for="slot in daySlots" :key="slot.id" class="slot-card" :class="{ unavail: !slot.is_available }">
                  <div class="slot-time">🕐 {{ slot.start_time }} – {{ slot.end_time }}</div>
                  <div class="slot-price">${{ slot.price_per_hour }}/hora</div>
                  <div class="slot-tags">
                    <span :class="['avail-badge', slot.is_available ? 'avail' : 'not-avail']">
                      {{ slot.is_available ? 'Disponible' : 'No disponible' }}
                    </span>
                    <span v-if="slot.school_restricted" class="school-badge">🔒 Mi escuela</span>
                  </div>
                  <div class="slot-actions">
                    <button @click="toggleSlot(slot)" class="btn btn-ghost btn-sm">
                      {{ slot.is_available ? 'Desactivar' : 'Activar' }}
                    </button>
                    <button @click="deleteSlot(slot.id)" class="btn btn-danger btn-sm">🗑️</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bookings -->
        <div>
          <h2 class="section-title">Solicitudes de Sesión</h2>
          <div v-if="bookings.length === 0" class="empty-state" style="padding:30px 0">
            <p>No tienes solicitudes de sesión</p>
          </div>
          <div v-else class="bookings-list">
            <div v-for="b in bookings" :key="b.id" class="booking-card">
              <div class="bk-top">
                <span class="bk-date">📅 {{ b.date }} · {{ b.slot_start }}-{{ b.slot_end }}</span>
                <span :class="['status-badge', `status-${b.status}`]">{{ statusLabel(b.status) }}</span>
              </div>
              <div class="bk-student">👩‍🎓 {{ b.student_name }}</div>
              <div v-if="b.subject" class="bk-subject">📝 {{ b.subject }}</div>
              <div v-if="b.notes" class="bk-notes">{{ b.notes }}</div>
              <div v-if="b.status === 'pending'" class="bk-actions">
                <button @click="setStatus(b.id, 'confirmed')" class="btn btn-accent btn-sm">✅ Confirmar</button>
                <button @click="setStatus(b.id, 'cancelled')" class="btn btn-danger btn-sm">❌ Cancelar</button>
              </div>
              <div v-else-if="b.status === 'confirmed'" class="bk-actions">
                <button @click="setStatus(b.id, 'completed')" class="btn btn-ghost btn-sm">✔ Completada</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Slot Modal -->
    <div v-if="showAddSlot" class="modal-overlay" @click.self="showAddSlot = false">
      <div class="modal">
        <h2>Agregar Horario</h2>
        <div class="form-group">
          <label>Día de la semana</label>
          <select v-model="slotForm.day_of_week">
            <option v-for="(name, idx) in DAY_NAMES" :key="idx" :value="idx">{{ name }}</option>
          </select>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div class="form-group">
            <label>Hora inicio</label>
            <input v-model="slotForm.start_time" type="time" />
          </div>
          <div class="form-group">
            <label>Hora fin</label>
            <input v-model="slotForm.end_time" type="time" />
          </div>
        </div>
        <div class="form-group">
          <label>Precio por hora (MXN)</label>
          <input v-model.number="slotForm.price_per_hour" type="number" min="0" step="50" />
        </div>
        <div class="form-group" style="display:flex;align-items:center;gap:10px">
          <input v-model="slotForm.school_restricted" type="checkbox" id="sr" />
          <label for="sr" style="margin-bottom:0">Solo para mi universidad</label>
        </div>
        <div v-if="slotError" class="alert alert-error">{{ slotError }}</div>
        <div style="display:flex;gap:10px">
          <button @click="addSlot" class="btn btn-primary" :disabled="slotLoading">
            {{ slotLoading ? 'Guardando...' : 'Agregar' }}
          </button>
          <button @click="showAddSlot = false" class="btn btn-ghost">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import api from '../../api/index.js'

const slots = ref([])
const bookings = ref([])
const loadingSlots = ref(false)
const showAddSlot = ref(false)
const slotLoading = ref(false)
const slotError = ref('')

const DAY_NAMES = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

const slotForm = reactive({
  day_of_week: 0, start_time: '09:00', end_time: '10:00',
  price_per_hour: 200, school_restricted: false
})

const groupedSlots = computed(() => {
  const groups = {}
  slots.value.forEach(s => {
    const day = s.day_name || DAY_NAMES[s.day_of_week]
    if (!groups[day]) groups[day] = []
    groups[day].push(s)
  })
  return groups
})

function statusLabel(s) {
  const map = { pending: 'Pendiente', confirmed: 'Confirmada', cancelled: 'Cancelada', completed: 'Completada' }
  return map[s] || s
}

async function fetchAll() {
  loadingSlots.value = true
  try {
    const [sRes, bRes] = await Promise.all([
      api.get('/schedule/slots/my'),
      api.get('/schedule/bookings/my')
    ])
    slots.value = sRes.data
    bookings.value = bRes.data
  } finally {
    loadingSlots.value = false
  }
}

async function addSlot() {
  slotLoading.value = true
  slotError.value = ''
  try {
    await api.post('/schedule/slots', slotForm)
    showAddSlot.value = false
    await fetchAll()
  } catch (e) {
    slotError.value = e.response?.data?.detail || 'Error al agregar horario'
  } finally {
    slotLoading.value = false
  }
}

async function toggleSlot(slot) {
  await api.put(`/schedule/slots/${slot.id}`, { is_available: !slot.is_available })
  await fetchAll()
}

async function deleteSlot(id) {
  if (!confirm('¿Eliminar este horario?')) return
  await api.delete(`/schedule/slots/${id}`)
  await fetchAll()
}

async function setStatus(bookingId, status) {
  await api.put(`/schedule/bookings/${bookingId}/status`, { status })
  await fetchAll()
}

onMounted(fetchAll)
</script>

<style scoped>
.sched-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.section-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; }

.day-groups { display: flex; flex-direction: column; gap: 20px; }
.day-section {}
.day-name { font-size: 14px; font-weight: 700; color: var(--primary); margin-bottom: 10px; }
.slot-cards { display: flex; flex-direction: column; gap: 8px; }
.slot-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px;
  transition: border-color 0.2s;
}
.slot-card:not(.unavail):hover { border-color: var(--primary); }
.slot-card.unavail { opacity: 0.6; }
.slot-time { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
.slot-price { font-size: 12px; color: var(--text2); margin-bottom: 8px; }
.slot-tags { display: flex; gap: 6px; margin-bottom: 10px; }
.avail-badge { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 10px; }
.avail { background: rgba(16,185,129,0.2); color: var(--accent); }
.not-avail { background: rgba(100,100,100,0.2); color: #888; }
.school-badge { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 10px; background: rgba(245,158,11,0.2); color: var(--primary); }
.slot-actions { display: flex; gap: 8px; }

.bookings-list { display: flex; flex-direction: column; gap: 10px; }
.booking-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 10px; padding: 14px; }
.bk-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.bk-date { font-size: 13px; font-weight: 600; }
.bk-student { font-size: 13px; color: var(--text2); margin-bottom: 4px; }
.bk-subject { font-size: 13px; color: var(--text2); margin-bottom: 4px; }
.bk-notes { font-size: 12px; color: var(--text2); font-style: italic; margin-bottom: 8px; }
.bk-actions { display: flex; gap: 8px; margin-top: 10px; }

.status-badge { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 12px; }
.status-pending { background: rgba(245,158,11,0.2); color: var(--primary); }
.status-confirmed { background: rgba(16,185,129,0.2); color: var(--accent); }
.status-cancelled { background: rgba(239,68,68,0.2); color: #f87171; }
.status-completed { background: rgba(99,102,241,0.2); color: #818cf8; }

@media (max-width: 900px) {
  .sched-layout { grid-template-columns: 1fr; }
}
</style>
