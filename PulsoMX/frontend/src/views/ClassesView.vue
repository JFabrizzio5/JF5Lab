<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { sessionsApi, templatesApi, instructorsApi } from '../api/endpoints'

const sessions = ref([]); const tpls = ref([]); const instrs = ref([])

async function load() {
  const [s, t, i] = await Promise.all([sessionsApi.list(), templatesApi.list(), instructorsApi.list()])
  sessions.value = s.data; tpls.value = t.data; instrs.value = i.data
}
onMounted(load)

function timefmt(s) { return new Date(s).toLocaleString('es-MX', { weekday:'short', day:'numeric', month:'short', hour:'2-digit', minute:'2-digit' }) }
function tplName(id) { return tpls.value.find(t => t.id === id)?.name || '—' }
function tplColor(id) { return tpls.value.find(t => t.id === id)?.color || '#7c3aed' }
function instrName(id) { return instrs.value.find(i => i.id === id)?.name || '—' }
</script>

<template>
  <AppLayout>
    <div class="head">
      <div><h1>Clases</h1><p class="muted">{{ sessions.length }} sesiones programadas</p></div>
    </div>

    <div class="grid-3">
      <div v-for="s in sessions" :key="s.id" class="sess" :style="`--c:${tplColor(s.template_id)}`">
        <div class="sess-time">{{ timefmt(s.starts_at) }}</div>
        <div class="sess-name">{{ s.name || tplName(s.template_id) }}</div>
        <div class="muted" style="font-size:13px; margin-top:4px;">{{ instrName(s.instructor_id) }}</div>
        <div class="sess-cap">
          <div class="cap-bar"><div class="cap-f" :style="`width:${Math.round((s.booked_count/s.capacity)*100)}%`"></div></div>
          <span>{{ s.booked_count }}/{{ s.capacity }}</span>
        </div>
      </div>
      <div v-if="!sessions.length" class="card muted" style="grid-column:1/-1; text-align:center; padding:40px;">Sin clases programadas.</div>
    </div>
  </AppLayout>
</template>

<style scoped>
.head { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:24px; }
.head h1 { margin:0; font-size:30px; letter-spacing:-0.03em; font-weight:800; }
.sess { background:var(--surface); border:1px solid var(--border); border-left:4px solid var(--c); border-radius:14px; padding:18px; transition:transform .15s; }
.sess:hover { transform: translateY(-2px); }
.sess-time { font-size:11px; text-transform:uppercase; letter-spacing:.1em; color:var(--c); font-weight:700; }
.sess-name { font-weight:700; font-size:17px; letter-spacing:-0.01em; margin-top:6px; }
.sess-cap { margin-top:12px; display:flex; align-items:center; gap:8px; font-size:12px; color:var(--text-muted); }
.cap-bar { flex:1; height:5px; background:var(--bg-subtle); border-radius:3px; overflow:hidden; }
.cap-f { height:100%; background:var(--c); border-radius:3px; }
</style>
