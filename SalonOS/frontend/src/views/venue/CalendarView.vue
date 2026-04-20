<template>
  <div>
    <div class="page-header">
      <h1>Calendario</h1>
      <p>Vista mensual de eventos</p>
    </div>

    <div class="page-body">
      <div class="calendar-nav">
        <button @click="prevMonth" class="btn btn-ghost btn-sm">← Anterior</button>
        <h2 class="cal-title">{{ monthName }} {{ year }}</h2>
        <button @click="nextMonth" class="btn btn-ghost btn-sm">Siguiente →</button>
      </div>

      <div class="calendar-grid">
        <div class="cal-header" v-for="d in dayNames" :key="d">{{ d }}</div>
        <div
          v-for="(cell, i) in calendarCells"
          :key="i"
          :class="['cal-cell', !cell.day && 'empty', cell.isToday && 'today', cell.events?.length && 'has-events']"
          @click="cell.day && selectDay(cell)"
        >
          <div v-if="cell.day" class="cal-day-num">{{ cell.day }}</div>
          <div v-if="cell.events?.length" class="cal-events">
            <div v-for="ev in cell.events.slice(0, 2)" :key="ev.id" :class="`cal-event ev-${ev.status}`">
              {{ ev.title }}
            </div>
            <div v-if="cell.events.length > 2" class="cal-event-more">+{{ cell.events.length - 2 }} más</div>
          </div>
        </div>
      </div>

      <!-- Day detail modal -->
      <div v-if="selectedDay" class="modal-overlay" @click.self="selectedDay = null">
        <div class="modal" style="max-width:480px">
          <h2>Eventos — {{ selectedDay.day }} de {{ monthName }}</h2>
          <div v-if="!selectedDay.events?.length" style="color:var(--text2);padding:1rem 0">Sin eventos este día</div>
          <div v-for="ev in selectedDay.events" :key="ev.id" class="day-event-card">
            <div class="day-event-header">
              <strong>{{ ev.title }}</strong>
              <span :class="`badge badge-${ev.status}`">{{ ev.status }}</span>
            </div>
            <div class="day-event-meta">
              👤 {{ ev.client_name || 'Cliente' }} ·
              👥 {{ ev.guests_count }} personas ·
              💰 ${{ ev.total_price?.toLocaleString() }}
            </div>
            <div class="day-event-time">
              🕐 {{ formatTime(ev.start_datetime) }} — {{ formatTime(ev.end_datetime) }}
            </div>
          </div>
          <button @click="selectedDay = null" class="btn btn-ghost" style="margin-top:1rem">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../../api/index.js'

const now = new Date()
const month = ref(now.getMonth() + 1)
const year = ref(now.getFullYear())
const events = ref([])
const loading = ref(false)
const selectedDay = ref(null)

const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
const monthNames = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

const monthName = computed(() => monthNames[month.value - 1])

const calendarCells = computed(() => {
  const firstDay = new Date(year.value, month.value - 1, 1).getDay()
  const daysInMonth = new Date(year.value, month.value, 0).getDate()
  const today = new Date()
  const cells = []

  for (let i = 0; i < firstDay; i++) cells.push({ day: null })

  for (let d = 1; d <= daysInMonth; d++) {
    const dayEvents = events.value.filter(ev => {
      const evDate = new Date(ev.start_datetime)
      return evDate.getDate() === d &&
        evDate.getMonth() + 1 === month.value &&
        evDate.getFullYear() === year.value
    })
    const isToday = d === today.getDate() && month.value === today.getMonth() + 1 && year.value === today.getFullYear()
    cells.push({ day: d, events: dayEvents, isToday })
  }

  return cells
})

function formatTime(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

function prevMonth() {
  if (month.value === 1) { month.value = 12; year.value-- }
  else month.value--
}

function nextMonth() {
  if (month.value === 12) { month.value = 1; year.value++ }
  else month.value++
}

function selectDay(cell) {
  if (cell.events?.length) selectedDay.value = cell
}

async function loadEvents() {
  loading.value = true
  try {
    const { data } = await api.get('/events/calendar', { params: { year: year.value, month: month.value } })
    events.value = data
  } finally {
    loading.value = false
  }
}

watch([month, year], loadEvents)
onMounted(loadEvents)
</script>

<style scoped>
.calendar-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.cal-title {
  font-size: 1.25rem;
  font-weight: 700;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.cal-header {
  background: var(--surface);
  padding: 0.75rem;
  text-align: center;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text2);
  text-transform: uppercase;
}

.cal-cell {
  background: var(--bg2);
  min-height: 100px;
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.15s;
}

.cal-cell.empty {
  background: var(--bg);
  cursor: default;
}

.cal-cell:hover:not(.empty) {
  background: var(--surface);
}

.cal-cell.today {
  background: rgba(124,58,237,0.08);
  border: 1px solid rgba(124,58,237,0.3);
}

.cal-day-num {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.35rem;
}

.cal-cell.today .cal-day-num {
  color: var(--primary);
}

.cal-events { display: flex; flex-direction: column; gap: 2px; }

.cal-event {
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 3px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ev-inquiry { background: rgba(100,116,139,0.3); color: #94a3b8; }
.ev-quote_sent { background: rgba(59,130,246,0.3); color: #60a5fa; }
.ev-confirmed { background: rgba(16,185,129,0.3); color: #34d399; }
.ev-deposit_paid { background: rgba(124,58,237,0.3); color: #a78bfa; }
.ev-completed { background: rgba(245,158,11,0.3); color: #fbbf24; }
.ev-cancelled { background: rgba(239,68,68,0.3); color: #f87171; }

.cal-event-more {
  font-size: 0.68rem;
  color: var(--text2);
  padding: 0.1rem 0.4rem;
}

.day-event-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 0.75rem;
}

.day-event-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.day-event-meta, .day-event-time {
  font-size: 0.82rem;
  color: var(--text2);
}
</style>
