<script setup>
import { onMounted, ref, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import {
  apiAppointments, apiStaff, apiServices,
  apiCancelAppt, apiConfirmAppt, apiCompleteAppt, apiRemindAppt
} from '../api/endpoints'

const month = ref(new Date())
const appts = ref([])
const staff = ref([])
const services = ref([])
const loading = ref(true)
const sel = ref(null)

function fmtTime(d) { return new Date(d).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false }) }
function fmtMoney(n) { return '$' + Number(n||0).toLocaleString('es-MX') }

const daysGrid = computed(() => {
  const y = month.value.getFullYear(), m = month.value.getMonth()
  const first = new Date(y, m, 1)
  const offset = (first.getDay() + 6) % 7 // lunes=0
  const daysInMonth = new Date(y, m+1, 0).getDate()
  const cells = []
  for (let i = 0; i < offset; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) {
    const day = new Date(y, m, d)
    const key = day.toISOString().split('T')[0]
    const items = appts.value.filter(a => a.starts_at.startsWith(key))
    cells.push({ date: day, key, items })
  }
  while (cells.length % 7 !== 0) cells.push(null)
  return cells
})

const staffMap = computed(() => Object.fromEntries(staff.value.map(s => [s.id, s])))
const svcMap = computed(() => Object.fromEntries(services.value.map(s => [s.id, s])))

async function load() {
  loading.value = true
  const y = month.value.getFullYear(), m = month.value.getMonth()
  const from = new Date(y, m, 1).toISOString()
  const to = new Date(y, m+1, 0, 23, 59, 59).toISOString()
  const [a, s, sv] = await Promise.all([
    apiAppointments({ date_from: from, date_to: to }),
    apiStaff(),
    apiServices(),
  ])
  appts.value = a; staff.value = s; services.value = sv
  loading.value = false
}
onMounted(load)

function prevMonth() { month.value = new Date(month.value.getFullYear(), month.value.getMonth() - 1, 1); load() }
function nextMonth() { month.value = new Date(month.value.getFullYear(), month.value.getMonth() + 1, 1); load() }

function pickDay(c) { sel.value = c }

async function doAction(a, fn) {
  if (!confirm('¿Confirmas la acción?')) return
  await fn(a.id)
  await load()
  sel.value = null
}
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1 class="page-title">Calendario</h1>
        <p class="page-subtitle">Vista mensual. Click en un día para abrir las citas.</p>
      </div>
      <div class="row">
        <button class="btn btn-ghost btn-sm" @click="prevMonth"><i class="mdi mdi-chevron-left"></i></button>
        <div class="serif" style="font-size:22px;color:var(--navy);min-width:200px;text-align:center;font-weight:600;">
          {{ month.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' }) }}
        </div>
        <button class="btn btn-ghost btn-sm" @click="nextMonth"><i class="mdi mdi-chevron-right"></i></button>
      </div>
    </div>

    <div v-if="loading" class="muted">Cargando...</div>
    <div v-else class="card" style="padding: 0;">
      <div class="month">
        <div class="wd" v-for="wd in ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']" :key="wd">{{ wd }}</div>
        <div v-for="(c, i) in daysGrid" :key="i"
             :class="['day', { empty: !c, today: c && c.date.toDateString() === new Date().toDateString() }]"
             @click="c && pickDay(c)">
          <template v-if="c">
            <div class="day-n">{{ c.date.getDate() }}</div>
            <div class="day-appts">
              <div v-for="a in c.items.slice(0,3)" :key="a.id"
                   class="mini-appt"
                   :style="{ '--staff-color': staffMap[a.staff_id]?.color || '#0c1933' }"
                   :class="{ pending: a.status === 'pending_payment' }">
                {{ fmtTime(a.starts_at) }} · {{ staffMap[a.staff_id]?.name?.split(' ')[0] || '—' }}
              </div>
              <div v-if="c.items.length > 3" class="more">+{{ c.items.length - 3 }} más</div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- Drawer -->
    <div v-if="sel" class="drawer-bg" @click.self="sel = null">
      <div class="drawer">
        <div class="drawer-head">
          <div>
            <div class="serif" style="font-size:24px;font-weight:600;color:var(--navy);">
              {{ sel.date.toLocaleDateString('es-MX', { weekday:'long', day:'numeric', month:'long' }) }}
            </div>
            <div class="muted" style="font-size:13px;">{{ sel.items.length }} citas</div>
          </div>
          <button class="btn btn-ghost btn-sm" @click="sel = null"><i class="mdi mdi-close"></i></button>
        </div>
        <div class="drawer-body">
          <div v-if="!sel.items.length" class="muted" style="text-align:center;padding:40px 0;">Sin citas este día.</div>
          <div v-for="a in sel.items" :key="a.id" class="drawer-item"
               :style="{ borderLeftColor: staffMap[a.staff_id]?.color || '#0c1933' }">
            <div style="display:flex;justify-content:space-between;align-items:start;gap:12px;">
              <div>
                <div class="drawer-time">{{ fmtTime(a.starts_at) }} – {{ fmtTime(a.ends_at) }}</div>
                <div class="drawer-svc">{{ svcMap[a.service_id]?.name || 'Servicio' }}</div>
                <div class="muted" style="font-size:12px;">{{ staffMap[a.staff_id]?.name || '—' }} · {{ fmtMoney(a.total) }}</div>
              </div>
              <span :class="['chip', a.status === 'confirmed' ? 'chip-success' : (a.status === 'completed' ? 'chip-navy' : (a.status === 'canceled' ? 'chip-danger' : 'chip-gold'))]">
                {{ a.status }}
              </span>
            </div>
            <div class="drawer-actions" v-if="a.status !== 'completed' && a.status !== 'canceled'">
              <button class="btn btn-sm" @click="doAction(a, apiConfirmAppt)" v-if="a.status === 'pending_payment'">
                <i class="mdi mdi-check"></i> Confirmar
              </button>
              <button class="btn btn-sm" @click="doAction(a, apiCompleteAppt)">
                <i class="mdi mdi-check-all"></i> Completar
              </button>
              <button class="btn btn-sm" @click="doAction(a, (id) => apiRemindAppt(id, 24))">
                <i class="mdi mdi-whatsapp"></i> Recordatorio
              </button>
              <button class="btn btn-sm btn-danger" @click="doAction(a, (id) => apiCancelAppt(id, 'Cancelada desde admin'))">
                <i class="mdi mdi-close"></i> Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.month {
  display: grid; grid-template-columns: repeat(7, 1fr);
}
.wd {
  padding: 12px; background: var(--cream-2); text-align: center;
  font-size: 11px; color: var(--muted); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
  border-right: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
}
.wd:last-child { border-right: none; }
.day {
  min-height: 112px; padding: 6px 8px;
  border-right: 1px solid var(--line-soft); border-bottom: 1px solid var(--line-soft);
  cursor: pointer; transition: background .15s;
}
.day:hover { background: var(--cream); }
.day.today { background: rgba(182,137,43,.08); }
.day.empty { background: var(--cream-2); cursor: default; }
.day-n { font-family: var(--serif); font-size: 18px; color: var(--navy); margin-bottom: 4px; font-weight: 600; }
.day-appts { display: flex; flex-direction: column; gap: 3px; }
.mini-appt {
  background: var(--cream); border-left: 3px solid var(--staff-color, var(--navy));
  padding: 3px 5px; border-radius: 3px; font-size: 10px; color: var(--navy);
  font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.mini-appt.pending { background: rgba(182,137,43,.12); }
.more { font-size: 10px; color: var(--muted); }

.drawer-bg {
  position: fixed; inset: 0; background: rgba(12,25,51,0.5);
  display: flex; justify-content: flex-end; z-index: 80;
}
.drawer {
  width: 480px; max-width: 100%; background: var(--surface);
  height: 100vh; overflow-y: auto; box-shadow: var(--shadow-lg);
}
.drawer-head {
  padding: 24px 28px; border-bottom: 1px solid var(--line-soft);
  display: flex; justify-content: space-between; align-items: start; gap: 12px;
}
.drawer-body { padding: 18px 24px; }
.drawer-item {
  padding: 16px; border-left: 4px solid var(--navy);
  background: var(--cream); border-radius: var(--radius-sm);
  margin-bottom: 12px;
}
.drawer-time { font-family: var(--serif); font-size: 18px; color: var(--navy); font-weight: 600; }
.drawer-svc { font-size: 14px; color: var(--ink-2); font-weight: 600; }
.drawer-actions {
  display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px;
  padding-top: 12px; border-top: 1px solid var(--line-soft);
}
</style>
