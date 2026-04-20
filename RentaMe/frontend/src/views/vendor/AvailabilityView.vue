<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <h1 class="page-title">Disponibilidad</h1>
      <p class="page-subtitle">Gestiona fechas bloqueadas y disponibilidad de tus artículos</p>

      <div class="avail-layout">
        <!-- Calendar -->
        <div class="calendar-section card">
          <div class="cal-nav">
            <button class="btn btn-secondary btn-sm" @click="prevMonth">←</button>
            <h3 class="cal-month">{{ monthLabel }}</h3>
            <button class="btn btn-secondary btn-sm" @click="nextMonth">→</button>
          </div>

          <div class="cal-grid">
            <div class="cal-header" v-for="d in ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb']" :key="d">{{ d }}</div>
            <div
              v-for="(day, idx) in calendarDays"
              :key="idx"
              class="cal-day"
              :class="dayClass(day)"
              @click="day.date && selectDay(day)"
            >
              <span v-if="day.date">{{ day.date.getDate() }}</span>
            </div>
          </div>

          <div class="cal-legend">
            <div class="legend-item"><span class="dot dot-available"></span> Disponible</div>
            <div class="legend-item"><span class="dot dot-booked"></span> Reservado</div>
            <div class="legend-item"><span class="dot dot-blocked"></span> Bloqueado</div>
          </div>
        </div>

        <!-- Right panel -->
        <div class="right-panel">
          <!-- Block editor -->
          <div class="card block-editor">
            <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 700;">
              {{ selectedDay ? `Bloquear: ${fmtDate(selectedDay)}` : 'Crear bloqueo' }}
            </h3>

            <div class="form-group">
              <label class="label">Artículo</label>
              <select v-model="blockForm.item_id" class="input">
                <option value="">Todos los artículos</option>
                <option v-for="item in items" :key="item.id" :value="item.id">{{ item.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="label">Tipo</label>
              <select v-model="blockForm.reason" class="input">
                <option value="blocked">🚫 Bloqueado</option>
                <option value="maintenance">🔧 Mantenimiento</option>
                <option value="personal">👤 Personal</option>
              </select>
            </div>
            <div class="form-group">
              <label class="label">Inicio</label>
              <input v-model="blockForm.start" type="datetime-local" class="input" />
            </div>
            <div class="form-group">
              <label class="label">Fin</label>
              <input v-model="blockForm.end" type="datetime-local" class="input" />
            </div>
            <div class="form-group">
              <label class="label">Nota (opcional)</label>
              <input v-model="blockForm.note" type="text" class="input" placeholder="Ej: Reparación motor" />
            </div>
            <div v-if="blockError" class="error-msg">{{ blockError }}</div>
            <button class="btn btn-primary" style="width: 100%; justify-content: center;" @click="createBlock" :disabled="blockLoading">
              {{ blockLoading ? 'Creando...' : '+ Crear bloqueo' }}
            </button>
          </div>

          <!-- Existing blocks -->
          <div class="card blocks-list">
            <h3 style="margin-bottom: 14px; font-size: 15px; font-weight: 700;">Bloqueos activos</h3>
            <div v-if="blocks.length === 0" class="empty-blocks">
              <p>Sin bloqueos. El calendario está disponible.</p>
            </div>
            <div v-else class="block-items">
              <div v-for="b in blocks" :key="b.id" class="block-item">
                <div class="block-info">
                  <div class="block-reason">{{ reasonIcon(b.reason) }} {{ b.reason }}</div>
                  <div class="block-dates">{{ fmtDate(b.start_datetime) }} → {{ fmtDate(b.end_datetime) }}</div>
                  <div v-if="b.note" class="block-note">{{ b.note }}</div>
                  <div v-if="b.item_id" class="block-item-name">{{ itemName(b.item_id) }}</div>
                </div>
                <button class="remove-block-btn" @click="removeBlock(b.id)" title="Eliminar bloqueo">×</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { availabilityAPI, itemsAPI } from '../../api/index.js'

const now = new Date()
const currentYear = ref(now.getFullYear())
const currentMonth = ref(now.getMonth())
const blocks = ref([])
const items = ref([])
const selectedDay = ref(null)
const blockLoading = ref(false)
const blockError = ref('')

const blockForm = ref({
  item_id: '',
  reason: 'blocked',
  start: '',
  end: '',
  note: '',
})

const MONTH_NAMES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const monthLabel = computed(() => `${MONTH_NAMES[currentMonth.value]} ${currentYear.value}`)

function prevMonth() {
  if (currentMonth.value === 0) { currentMonth.value = 11; currentYear.value-- }
  else currentMonth.value--
}
function nextMonth() {
  if (currentMonth.value === 11) { currentMonth.value = 0; currentYear.value++ }
  else currentMonth.value++
}

const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const days = []
  for (let i = 0; i < firstDay; i++) days.push({ date: null })
  for (let d = 1; d <= daysInMonth; d++) days.push({ date: new Date(year, month, d) })
  return days
})

function isBlocked(date) {
  if (!date) return false
  return blocks.value.some(b => {
    const start = new Date(b.start_datetime)
    const end = new Date(b.end_datetime)
    return date >= start && date <= end
  })
}

function dayClass(day) {
  if (!day.date) return 'cal-day-empty'
  const classes = []
  const date = day.date
  const today = new Date()
  if (date.toDateString() === today.toDateString()) classes.push('cal-day-today')
  if (isBlocked(date)) classes.push('cal-day-blocked')
  if (selectedDay.value && date.toDateString() === selectedDay.value.toDateString()) classes.push('cal-day-selected')
  return classes.join(' ')
}

function selectDay(day) {
  selectedDay.value = day.date
  const d = day.date
  const start = new Date(d)
  start.setHours(8, 0, 0, 0)
  const end = new Date(d)
  end.setHours(20, 0, 0, 0)
  blockForm.value.start = start.toISOString().slice(0, 16)
  blockForm.value.end = end.toISOString().slice(0, 16)
}

function fmtDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}

function reasonIcon(r) {
  return { blocked: '🚫', maintenance: '🔧', personal: '👤' }[r] || '🚫'
}

function itemName(id) {
  return items.value.find(i => i.id === id)?.name || `Item #${id}`
}

async function createBlock() {
  blockError.value = ''
  if (!blockForm.value.start || !blockForm.value.end) {
    blockError.value = 'Por favor indica las fechas de inicio y fin'
    return
  }
  blockLoading.value = true
  try {
    await availabilityAPI.create({
      item_id: blockForm.value.item_id || null,
      start_datetime: new Date(blockForm.value.start).toISOString(),
      end_datetime: new Date(blockForm.value.end).toISOString(),
      reason: blockForm.value.reason,
      note: blockForm.value.note || null,
    })
    blockForm.value = { item_id: '', reason: 'blocked', start: '', end: '', note: '' }
    selectedDay.value = null
    await loadBlocks()
  } catch (e) {
    blockError.value = e.response?.data?.detail || 'Error al crear bloqueo'
  } finally {
    blockLoading.value = false
  }
}

async function removeBlock(id) {
  if (!confirm('¿Eliminar este bloqueo?')) return
  try {
    await availabilityAPI.delete(id)
    await loadBlocks()
  } catch {}
}

async function loadBlocks() {
  const res = await availabilityAPI.list()
  blocks.value = res.data
}

onMounted(async () => {
  const [b, i] = await Promise.all([availabilityAPI.list(), itemsAPI.list()])
  blocks.value = b.data
  items.value = i.data.filter(i => i.is_active)
})
</script>

<style scoped>
.avail-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 20px;
  align-items: start;
}

.cal-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.cal-month { font-size: 16px; font-weight: 700; }

.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}
.cal-header {
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  color: var(--text2);
  padding: 6px 0;
  text-transform: uppercase;
}
.cal-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
  color: var(--text3);
  background: var(--bg3);
}
.cal-day:hover:not(.cal-day-empty) { background: var(--surface); color: var(--text); }
.cal-day-empty { background: transparent; cursor: default; }
.cal-day-today { font-weight: 700; color: var(--primary); border: 1px solid var(--primary); }
.cal-day-blocked { background: rgba(239,68,68,0.15); color: #f87171; }
.cal-day-selected { background: var(--primary); color: white; }

.cal-legend {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text2); }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot-available { background: var(--success); }
.dot-booked { background: var(--warning); }
.dot-blocked { background: var(--danger); }

.right-panel { display: flex; flex-direction: column; gap: 16px; }
.block-editor { display: flex; flex-direction: column; gap: 12px; }
.error-msg {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #f87171;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
}

.empty-blocks { text-align: center; padding: 20px; color: var(--text2); font-size: 13px; }
.block-items { display: flex; flex-direction: column; gap: 8px; }
.block-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  background: var(--bg3);
  border-radius: 8px;
  padding: 10px 12px;
  gap: 8px;
}
.block-reason { font-size: 13px; font-weight: 600; text-transform: capitalize; }
.block-dates { font-size: 12px; color: var(--text2); margin-top: 2px; }
.block-note { font-size: 12px; color: var(--text2); font-style: italic; }
.block-item-name { font-size: 11px; color: var(--primary); margin-top: 2px; }
.remove-block-btn {
  background: none;
  border: none;
  color: var(--text2);
  font-size: 18px;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  flex-shrink: 0;
  transition: all 0.2s;
}
.remove-block-btn:hover { color: var(--danger); background: rgba(239,68,68,0.1); }

@media (max-width: 900px) {
  .avail-layout { grid-template-columns: 1fr; }
}
</style>
