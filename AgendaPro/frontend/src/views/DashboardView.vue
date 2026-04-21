<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { apiDashboard, apiAppointments, apiStaff } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const kpis = ref(null)
const loading = ref(true)
const weekAppts = ref([])
const staffMap = ref({})

function fmtMoney(n) {
  return '$' + Number(n || 0).toLocaleString('es-MX', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}
function fmtDay(d) {
  return new Date(d).toLocaleString('es-MX', { weekday: 'short', day: 'numeric', month: 'short' })
}
function fmtTime(d) {
  return new Date(d).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false })
}

onMounted(async () => {
  if (!session.active) { router.push('/demo'); return }
  try {
    const [k, staff] = await Promise.all([apiDashboard(), apiStaff()])
    kpis.value = k
    staffMap.value = Object.fromEntries(staff.map(s => [s.id, s]))
    const now = new Date(); now.setHours(0,0,0,0)
    const end = new Date(now); end.setDate(end.getDate() + 7)
    weekAppts.value = await apiAppointments({
      date_from: now.toISOString(), date_to: end.toISOString(),
    })
  } finally { loading.value = false }
})

// Agrupar citas por día
const days = computed(() => {
  const now = new Date(); now.setHours(0,0,0,0)
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(now); d.setDate(d.getDate() + i)
    const key = d.toISOString().split('T')[0]
    const items = weekAppts.value.filter(a => a.starts_at.startsWith(key))
      .sort((a,b) => a.starts_at.localeCompare(b.starts_at))
    return { date: d, key, items }
  })
})
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Cómo va tu semana en un vistazo.</p>
      </div>
      <div v-if="session.slug">
        <a :href="'/' + session.slug" target="_blank" class="btn btn-primary">
          <i class="mdi mdi-open-in-new"></i> Ver mi página pública
        </a>
      </div>
    </div>

    <div v-if="loading" class="muted">Cargando...</div>
    <div v-else-if="kpis">
      <div class="grid-4">
        <div class="kpi" style="--kpi-accent: var(--navy);">
          <div class="kpi-label">Citas hoy</div>
          <div class="kpi-value">{{ kpis.appts_today }}</div>
          <div class="kpi-sub">Confirmadas + pendientes</div>
        </div>
        <div class="kpi" style="--kpi-accent: var(--gold);">
          <div class="kpi-label">Esta semana</div>
          <div class="kpi-value">{{ kpis.appts_week }}</div>
          <div class="kpi-sub">Próximos 7 días</div>
        </div>
        <div class="kpi" style="--kpi-accent: var(--success);">
          <div class="kpi-label">Ingresos mes</div>
          <div class="kpi-value">{{ fmtMoney(kpis.revenue_mtd_mxn) }}</div>
          <div class="kpi-sub">Pagos confirmados MTD</div>
        </div>
        <div class="kpi" style="--kpi-accent: var(--danger);">
          <div class="kpi-label">No-show rate</div>
          <div class="kpi-value">{{ kpis.no_show_rate }}%</div>
          <div class="kpi-sub">{{ kpis.confirmed_rate }}% confirmadas</div>
        </div>
      </div>

      <!-- Semana tipo Cal.com -->
      <div class="card" style="margin-top: 28px; padding: 0;">
        <div style="padding: 18px 22px; border-bottom: 1px solid var(--line-soft); display: flex; justify-content: space-between; align-items: center;">
          <div class="serif" style="font-size: 22px; color: var(--navy); font-weight: 600;">Semana</div>
          <router-link to="/app/calendar" class="btn btn-ghost btn-sm">
            <i class="mdi mdi-calendar-month-outline"></i> Ver calendario completo
          </router-link>
        </div>
        <div class="week-grid">
          <div v-for="d in days" :key="d.key" class="day-col">
            <div class="day-head">
              <div class="day-wd">{{ d.date.toLocaleDateString('es-MX', { weekday: 'short' }) }}</div>
              <div class="day-num">{{ d.date.getDate() }}</div>
            </div>
            <div class="day-body">
              <div v-if="!d.items.length" class="muted" style="font-size:11px;text-align:center;padding:20px 0;">Sin citas</div>
              <div v-for="a in d.items" :key="a.id"
                   class="appt"
                   :style="{ '--staff-color': staffMap[a.staff_id]?.color || '#0c1933' }"
                   :class="{ pending: a.status === 'pending_payment' }">
                <div class="appt-time">{{ fmtTime(a.starts_at) }}</div>
                <div class="appt-staff">{{ staffMap[a.staff_id]?.name || '—' }}</div>
                <div v-if="a.status === 'pending_payment'" class="appt-flag">por pagar</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid-2" style="margin-top: 28px;">
        <div class="card">
          <div class="serif" style="font-size: 20px; color: var(--navy); margin-bottom: 16px; font-weight: 600;">Top staff</div>
          <div v-if="!kpis.top_staff.length" class="muted">Sin datos todavía.</div>
          <div v-for="(s, i) in kpis.top_staff" :key="s.name" class="rank-row">
            <div class="rank">{{ i+1 }}</div>
            <div class="rank-name">{{ s.name }}</div>
            <div class="rank-val">{{ s.count }} citas</div>
          </div>
        </div>
        <div class="card">
          <div class="serif" style="font-size: 20px; color: var(--navy); margin-bottom: 16px; font-weight: 600;">Top servicios</div>
          <div v-if="!kpis.top_services.length" class="muted">Sin datos todavía.</div>
          <div v-for="(s, i) in kpis.top_services" :key="s.name" class="rank-row">
            <div class="rank">{{ i+1 }}</div>
            <div class="rank-name">{{ s.name }}</div>
            <div class="rank-val">{{ s.count }} citas</div>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 28px;">
        <div class="serif" style="font-size: 20px; color: var(--navy); margin-bottom: 16px; font-weight: 600;">Próximas citas</div>
        <table class="table" v-if="kpis.upcoming.length">
          <thead><tr><th>Hora</th><th>Cliente</th><th>Servicio</th><th>Staff</th><th>Estado</th></tr></thead>
          <tbody>
            <tr v-for="a in kpis.upcoming" :key="a.id">
              <td><strong>{{ fmtDay(a.starts_at) }}</strong> · {{ fmtTime(a.starts_at) }}</td>
              <td>{{ a.customer }}</td>
              <td>{{ a.service }}</td>
              <td>{{ a.staff }}</td>
              <td>
                <span :class="['chip', a.status === 'confirmed' ? 'chip-success' : 'chip-gold']">
                  {{ a.status === 'confirmed' ? 'Confirmada' : 'Por pagar' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="muted">No hay citas próximas.</div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.week-grid {
  display: grid; grid-template-columns: repeat(7, 1fr);
  min-height: 420px;
}
.day-col { border-right: 1px solid var(--line-soft); }
.day-col:last-child { border-right: none; }
.day-head {
  padding: 10px 12px; text-align: center;
  border-bottom: 1px solid var(--line-soft); background: var(--cream-2);
}
.day-wd { font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 700; }
.day-num { font-family: var(--serif); font-size: 22px; color: var(--navy); font-weight: 600; }
.day-body { padding: 8px; display: flex; flex-direction: column; gap: 6px; }
.appt {
  background: var(--cream); border-left: 3px solid var(--staff-color, var(--navy));
  padding: 6px 8px; border-radius: 6px; font-size: 11px;
  cursor: pointer;
}
.appt.pending { background: rgba(182,137,43,.1); }
.appt-time { font-weight: 700; color: var(--navy); font-size: 12px; }
.appt-staff { color: var(--ink-2); font-size: 11px; }
.appt-flag { color: var(--gold); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }

.rank-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid var(--line-soft);
}
.rank-row:last-child { border-bottom: none; }
.rank {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--navy); color: var(--cream);
  display: grid; place-items: center;
  font-size: 12px; font-weight: 700;
}
.rank-name { flex: 1; color: var(--text); font-weight: 500; font-size: 14px; }
.rank-val { color: var(--muted); font-size: 13px; font-weight: 600; }

@media (max-width: 900px) {
  .week-grid { grid-template-columns: repeat(7, minmax(100px, 1fr)); overflow-x: auto; }
}
</style>
