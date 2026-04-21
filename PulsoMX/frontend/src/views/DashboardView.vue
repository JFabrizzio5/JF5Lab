<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { dashboardApi, exportsApi } from '../api/endpoints'

const k = ref(null); const loading = ref(true)

async function load() {
  loading.value = true
  try { const { data } = await dashboardApi.get(); k.value = data } finally { loading.value = false }
}
onMounted(load)

function peso(n) { return new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits:0 }).format(Number(n)) }
function timeOnly(s) { return new Date(s).toLocaleString('es-MX', { weekday:'short', hour:'2-digit', minute:'2-digit' }) }
</script>

<template>
  <AppLayout>
    <div class="head">
      <div><h1>Dashboard</h1><p class="muted">Panorama de hoy.</p></div>
      <div class="acts">
        <button class="btn btn-sm" @click="exportsApi.members()"><i class="mdi mdi-file-excel"></i> Miembros</button>
        <button class="btn btn-sm" @click="exportsApi.checkins()"><i class="mdi mdi-file-excel"></i> Check-ins</button>
      </div>
    </div>

    <div v-if="loading" class="muted"><i class="mdi mdi-loading mdi-spin"></i> Cargando…</div>

    <div v-else-if="k">
      <div class="grid-4">
        <div class="card kpi"><div class="kl">Miembros</div><div class="kv">{{ k.total_members }}</div><div class="muted" style="font-size:12px;">{{ k.active_memberships }} activos</div></div>
        <div class="card kpi"><div class="kl">Check-ins hoy</div><div class="kv gradient-text">{{ k.check_ins_today }}</div><div class="muted" style="font-size:12px;">Reservas: {{ k.bookings_today }}</div></div>
        <div class="card kpi"><div class="kl">Ingreso MTD</div><div class="kv">{{ peso(k.revenue_mtd_mxn) }}</div><div class="muted" style="font-size:12px;">+{{ k.new_members_last_7d }} nuevos (7d)</div></div>
        <div class="card kpi"><div class="kl">Churn 30d</div><div class="kv" :style="k.churn_last_30d > 0 ? 'color:var(--danger)':''">{{ k.churn_last_30d }}</div><div class="muted" style="font-size:12px;">Cancelaciones</div></div>
      </div>

      <div class="grid-2" style="margin-top:18px;">
        <div class="card">
          <h3 style="margin:0 0 14px;">Próximas clases</h3>
          <div v-for="c in k.upcoming_classes" :key="c.id" class="up-row">
            <div class="up-time">{{ timeOnly(c.starts_at) }}</div>
            <div style="flex:1;">
              <div style="font-weight:600;">{{ c.name }}</div>
              <div class="muted" style="font-size:12px;">{{ c.booked }}/{{ c.capacity }}</div>
            </div>
            <div class="up-bar"><div class="up-fill" :style="`width:${Math.round((c.booked/c.capacity)*100)}%`"></div></div>
          </div>
          <div v-if="!k.upcoming_classes.length" class="muted">Sin clases agendadas.</div>
        </div>

        <div class="card">
          <h3 style="margin:0 0 14px;">Check-ins recientes</h3>
          <table class="table">
            <thead><tr><th>Miembro</th><th>Hora</th><th>Método</th></tr></thead>
            <tbody>
              <tr v-for="r in k.recent_check_ins" :key="r.id">
                <td>{{ r.member }}</td>
                <td class="muted">{{ new Date(r.at).toLocaleString('es-MX') }}</td>
                <td><span class="badge violet">{{ r.method }}</span></td>
              </tr>
              <tr v-if="!k.recent_check_ins.length"><td colspan="3" class="muted">Sin check-ins aún.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.head { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:24px; }
.head h1 { margin:0; font-size:30px; letter-spacing:-0.03em; font-weight:800; }
.acts { display:flex; gap:8px; }
.kl { font-size:11px; text-transform:uppercase; letter-spacing:.1em; color:var(--text-muted); font-weight:700; }
.kv { font-size:32px; font-weight:800; letter-spacing:-0.03em; margin:6px 0 2px; }
.up-row { display:flex; align-items:center; gap:12px; padding:10px 0; border-bottom:1px dashed var(--border); position:relative; }
.up-row:last-child { border:none; }
.up-time { font-weight:700; font-size:13px; color:var(--violet); min-width:60px; }
.up-bar { width:70px; height:4px; background:var(--bg-subtle); border-radius:2px; overflow:hidden; flex-shrink:0; }
.up-fill { height:100%; background:var(--brand-grad); }
</style>
