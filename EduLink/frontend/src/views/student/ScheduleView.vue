<template>
  <div>
    <div class="page-header">
      <h1>Reservar Tutoría</h1>
      <p>Agenda una sesión personalizada con tus tutores</p>
    </div>

    <div class="page-content">
      <div class="sched-grid">
        <!-- Tutor list -->
        <div>
          <h2 class="section-title">Tutores disponibles</h2>
          <div class="tutor-list">
            <div
              v-for="tutor in tutors"
              :key="tutor.id"
              @click="selectTutor(tutor)"
              :class="['tutor-card', selectedTutor?.id === tutor.id ? 'active' : '']"
            >
              <img :src="tutor.avatar_url || defaultAvatar" class="tutor-big-img" />
              <div class="tutor-info">
                <div class="tutor-name">{{ tutor.name }}</div>
                <div class="tutor-school">
                  <span class="badge badge-school">{{ tutor.school }}</span>
                </div>
                <div class="slot-count">📅 {{ tutor.slot_count }} horarios disponibles</div>
              </div>
            </div>
          </div>

          <!-- My bookings -->
          <h2 class="section-title" style="margin-top:32px">Mis Reservas</h2>
          <div v-if="myBookings.length === 0" class="empty-state" style="padding:20px 0">
            <p>No tienes reservas activas</p>
          </div>
          <div v-else class="bookings-list">
            <div v-for="b in myBookings" :key="b.id" class="booking-card">
              <div class="booking-header">
                <span class="booking-date">📅 {{ b.date }}</span>
                <span :class="['status-badge', `status-${b.status}`]">{{ statusLabel(b.status) }}</span>
              </div>
              <div class="booking-detail">👨‍🏫 {{ b.tutor_name }}</div>
              <div class="booking-detail">🕐 {{ b.slot_start }} - {{ b.slot_end }}</div>
              <div v-if="b.subject" class="booking-detail">📝 {{ b.subject }}</div>
              <button
                v-if="b.status === 'pending'"
                @click="cancelBooking(b.id)"
                class="btn btn-danger btn-sm"
                style="margin-top:8px"
              >Cancelar</button>
            </div>
          </div>
        </div>

        <!-- Slot selector -->
        <div v-if="selectedTutor">
          <h2 class="section-title">Horarios de {{ selectedTutor.name }}</h2>
          <div v-if="loadingSlots" class="loading">Cargando horarios...</div>
          <div v-else-if="slots.length === 0" class="empty-state" style="padding:20px 0">
            <p>No hay horarios disponibles</p>
          </div>
          <div v-else>
            <div class="day-groups">
              <div v-for="(daySlots, dayName) in groupedSlots" :key="dayName" class="day-group">
                <h3 class="day-label">{{ dayName }}</h3>
                <div class="slots-row">
                  <div
                    v-for="slot in daySlots"
                    :key="slot.id"
                    @click="selectSlot(slot)"
                    :class="['slot-chip', selectedSlot?.id === slot.id ? 'active' : '', !slot.is_available ? 'unavail' : '']"
                  >
                    {{ slot.start_time }}–{{ slot.end_time }}
                    <div class="slot-price">${{ slot.price_per_hour }}/hr</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Booking form -->
            <div v-if="selectedSlot" class="booking-form card" style="margin-top:20px">
              <h3>Reservar: {{ selectedSlot.day_name }} {{ selectedSlot.start_time }}–{{ selectedSlot.end_time }}</h3>
              <div class="form-group" style="margin-top:14px">
                <label>Fecha (debe ser {{ selectedSlot.day_name }})</label>
                <input v-model="bookingForm.date" type="date" />
              </div>
              <div class="form-group">
                <label>Materia/Tema</label>
                <input v-model="bookingForm.subject" type="text" placeholder="Ej: Cálculo - Integrales" />
              </div>
              <div class="form-group">
                <label>Notas adicionales</label>
                <textarea v-model="bookingForm.notes" rows="2" placeholder="¿En qué necesitas ayuda?"></textarea>
              </div>
              <div v-if="bookingError" class="alert alert-error">{{ bookingError }}</div>
              <div v-if="bookingSuccess" class="alert alert-success">{{ bookingSuccess }}</div>
              <button @click="createBooking" class="btn btn-primary" :disabled="bookingLoading">
                {{ bookingLoading ? 'Reservando...' : 'Confirmar Reserva' }}
              </button>
            </div>
          </div>
        </div>

        <div v-else class="no-tutor-placeholder">
          <div class="placeholder-content">
            <span class="placeholder-icon">👈</span>
            <p>Selecciona un tutor para ver sus horarios disponibles</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import api from '../../api/index.js'

const tutors = ref([])
const selectedTutor = ref(null)
const slots = ref([])
const selectedSlot = ref(null)
const loadingSlots = ref(false)
const myBookings = ref([])
const bookingLoading = ref(false)
const bookingError = ref('')
const bookingSuccess = ref('')
const defaultAvatar = 'https://ui-avatars.com/api/?name=T&background=334155&color=fff'

const bookingForm = reactive({ date: '', subject: '', notes: '' })

const DAY_NAMES = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

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

async function fetchTutors() {
  const res = await api.get('/schedule/tutors')
  tutors.value = res.data
}

async function fetchMyBookings() {
  try {
    const res = await api.get('/schedule/bookings/my')
    myBookings.value = res.data
  } catch (e) {}
}

async function selectTutor(tutor) {
  selectedTutor.value = tutor
  selectedSlot.value = null
  loadingSlots.value = true
  try {
    const res = await api.get(`/schedule/slots/tutor/${tutor.id}`)
    slots.value = res.data
  } finally {
    loadingSlots.value = false
  }
}

function selectSlot(slot) {
  if (!slot.is_available) return
  selectedSlot.value = slot
  bookingError.value = ''
  bookingSuccess.value = ''
}

async function createBooking() {
  if (!bookingForm.date) { bookingError.value = 'Selecciona una fecha'; return }
  bookingLoading.value = true
  bookingError.value = ''
  bookingSuccess.value = ''
  try {
    await api.post('/schedule/bookings', {
      tutor_id: selectedTutor.value.id,
      slot_id: selectedSlot.value.id,
      date: bookingForm.date,
      subject: bookingForm.subject,
      notes: bookingForm.notes
    })
    bookingSuccess.value = '¡Reserva creada exitosamente!'
    bookingForm.date = ''
    bookingForm.subject = ''
    bookingForm.notes = ''
    selectedSlot.value = null
    await fetchMyBookings()
  } catch (e) {
    bookingError.value = e.response?.data?.detail || 'Error al crear reserva'
  } finally {
    bookingLoading.value = false
  }
}

async function cancelBooking(bookingId) {
  try {
    await api.put(`/schedule/bookings/${bookingId}/status`, { status: 'cancelled' })
    await fetchMyBookings()
  } catch (e) {}
}

onMounted(async () => {
  await Promise.all([fetchTutors(), fetchMyBookings()])
})
</script>

<style scoped>
.sched-grid { display: grid; grid-template-columns: 320px 1fr; gap: 32px; }

.section-title { font-size: 16px; font-weight: 700; margin-bottom: 14px; }

.tutor-list { display: flex; flex-direction: column; gap: 10px; }
.tutor-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.tutor-card:hover { border-color: var(--primary); }
.tutor-card.active { border-color: var(--primary); background: rgba(245,158,11,0.08); }
.tutor-big-img { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; }
.tutor-name { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.tutor-school { margin-bottom: 4px; }
.slot-count { font-size: 12px; color: var(--text2); }

.bookings-list { display: flex; flex-direction: column; gap: 10px; }
.booking-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px;
}
.booking-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.booking-date { font-size: 13px; font-weight: 600; }
.booking-detail { font-size: 12px; color: var(--text2); margin-bottom: 4px; }

.status-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 12px;
}
.status-pending { background: rgba(245,158,11,0.2); color: var(--primary); }
.status-confirmed { background: rgba(16,185,129,0.2); color: var(--accent); }
.status-cancelled { background: rgba(239,68,68,0.2); color: #f87171; }
.status-completed { background: rgba(99,102,241,0.2); color: #818cf8; }

.day-groups { display: flex; flex-direction: column; gap: 16px; }
.day-label { font-size: 14px; font-weight: 700; color: var(--text2); margin-bottom: 8px; }
.slots-row { display: flex; flex-wrap: wrap; gap: 8px; }
.slot-chip {
  padding: 8px 14px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  text-align: center;
  transition: all 0.2s;
}
.slot-chip:hover { border-color: var(--primary); }
.slot-chip.active { border-color: var(--primary); background: rgba(245,158,11,0.1); color: var(--primary); }
.slot-chip.unavail { opacity: 0.4; cursor: not-allowed; }
.slot-price { font-size: 11px; color: var(--text2); font-weight: 400; }

.booking-form h3 { font-size: 15px; font-weight: 700; margin-bottom: 4px; }

.no-tutor-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: var(--bg2);
  border: 2px dashed var(--border);
  border-radius: 16px;
}
.placeholder-content { text-align: center; color: var(--text2); }
.placeholder-icon { font-size: 48px; display: block; margin-bottom: 12px; }

@media (max-width: 900px) {
  .sched-grid { grid-template-columns: 1fr; }
}
</style>
