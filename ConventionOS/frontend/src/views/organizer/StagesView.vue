<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Escenarios & Agenda</h1>
        <button @click="openStageModal(null)" class="btn btn-primary">+ Nuevo Escenario</button>
      </div>

      <div class="stages-list">
        <div v-for="stage in stages" :key="stage.id" class="stage-panel">
          <div class="stage-header">
            <div class="stage-dot" :style="`background:${stage.color}`"></div>
            <div class="stage-info">
              <div class="stage-name">{{ stage.name }}</div>
              <div class="stage-sub">{{ stage.location_in_venue }} · Capacidad: {{ stage.capacity || '—' }}</div>
            </div>
            <div class="stage-actions">
              <a v-if="stage.stream_url" :href="stage.stream_url" target="_blank" class="btn btn-ghost btn-sm">📺 Stream</a>
              <button @click="openStageModal(stage)" class="btn btn-ghost btn-sm">Editar</button>
              <button @click="deleteStage(stage)" class="btn btn-danger btn-sm">Eliminar</button>
              <button @click="addSessionFor(stage)" class="btn btn-primary btn-sm">+ Sesión</button>
            </div>
          </div>

          <!-- Sessions table -->
          <div class="sessions-table" v-if="sessionsByStage[stage.id]?.length">
            <table>
              <thead>
                <tr><th>Hora inicio</th><th>Hora fin</th><th>Tipo</th><th>Sesión</th><th>Ponente</th><th>Acciones</th></tr>
              </thead>
              <tbody>
                <tr v-for="s in sessionsByStage[stage.id]" :key="s.id">
                  <td>{{ fmtDT(s.start_time) }}</td>
                  <td>{{ fmtDT(s.end_time) }}</td>
                  <td><span class="badge" :class="sessionBadge(s.session_type)">{{ s.session_type }}</span></td>
                  <td>{{ s.title }}</td>
                  <td>{{ s.speaker?.name || '—' }}</td>
                  <td>
                    <button @click="editSession(s)" class="btn btn-ghost btn-sm">Editar</button>
                    <button @click="deleteSession(s)" class="btn btn-danger btn-sm">✕</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="no-sessions">No hay sesiones en este escenario</div>
        </div>

        <div v-if="!stages.length" class="empty-state card">Sin escenarios aún. Crea el primero.</div>
      </div>

      <!-- Stage Modal -->
      <div class="modal-overlay" v-if="showStageModal" @click.self="showStageModal = false">
        <div class="modal">
          <h2>{{ editingStage?.id ? 'Editar Escenario' : 'Nuevo Escenario' }}</h2>
          <div class="form-group"><label>Nombre *</label><input v-model="stageForm.name" /></div>
          <div class="form-group"><label>Descripción</label><textarea v-model="stageForm.description" rows="2"></textarea></div>
          <div class="form-group"><label>Capacidad</label><input v-model.number="stageForm.capacity" type="number" /></div>
          <div class="form-group"><label>Ubicación en el venue</label><input v-model="stageForm.location_in_venue" placeholder="Hall B, Nivel 2" /></div>
          <div class="form-group"><label>URL de Stream (YouTube/Twitch)</label><input v-model="stageForm.stream_url" /></div>
          <div class="form-group"><label>Color del escenario</label>
            <div style="display:flex;gap:10px;align-items:center">
              <input type="color" v-model="stageForm.color" style="width:50px;height:40px;padding:2px;border-radius:6px;cursor:pointer" />
              <input v-model="stageForm.color" placeholder="#6366f1" />
            </div>
          </div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="showStageModal = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
            <button @click="saveStage" :disabled="!stageForm.name" class="btn btn-primary" style="flex:1">Guardar</button>
          </div>
        </div>
      </div>

      <!-- Session Modal -->
      <div class="modal-overlay" v-if="showSessionModal" @click.self="showSessionModal = false">
        <div class="modal">
          <h2>{{ editingSession?.id ? 'Editar Sesión' : 'Nueva Sesión' }}</h2>
          <div class="form-group"><label>Título *</label><input v-model="sessionForm.title" /></div>
          <div class="form-group"><label>Descripción</label><textarea v-model="sessionForm.description" rows="2"></textarea></div>
          <div class="form-group"><label>Tipo</label>
            <select v-model="sessionForm.session_type">
              <option value="talk">Ponencia</option>
              <option value="panel">Panel</option>
              <option value="workshop">Taller</option>
              <option value="performance">Actuación</option>
              <option value="ceremony">Ceremonia</option>
            </select>
          </div>
          <div class="form-group"><label>Escenario</label>
            <select v-model="sessionForm.stage_id">
              <option v-for="s in stages" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div class="form-group"><label>Ponente (opcional)</label>
            <select v-model="sessionForm.speaker_id">
              <option :value="null">Sin ponente</option>
              <option v-for="sp in speakers" :key="sp.id" :value="sp.id">{{ sp.name }}</option>
            </select>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Inicio *</label><input v-model="sessionForm.start_time" type="datetime-local" /></div>
            <div class="form-group"><label>Fin *</label><input v-model="sessionForm.end_time" type="datetime-local" /></div>
          </div>
          <div class="form-group"><label>Tags (JSON)</label><input v-model="sessionForm.tags_json" placeholder='["gaming","esports"]' /></div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="showSessionModal = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
            <button @click="saveSession" :disabled="!sessionForm.title || !sessionForm.start_time" class="btn btn-primary" style="flex:1">Guardar</button>
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
const stages = ref([])
const sessions = ref([])
const speakers = ref([])

const showStageModal = ref(false)
const showSessionModal = ref(false)
const editingStage = ref(null)
const editingSession = ref(null)

const stageForm = ref({ name: '', description: '', capacity: null, color: '#6366f1', location_in_venue: '', stream_url: '' })
const sessionForm = ref({ title: '', description: '', session_type: 'talk', stage_id: null, speaker_id: null, start_time: '', end_time: '', tags_json: '' })

const sessionsByStage = computed(() => {
  const map = {}
  for (const s of sessions.value) {
    if (!map[s.stage_id]) map[s.stage_id] = []
    map[s.stage_id].push(s)
  }
  return map
})

function sessionBadge(t) {
  if (t === 'workshop') return 'badge-success'
  if (t === 'panel') return 'badge-info'
  if (t === 'performance') return 'badge-warning'
  if (t === 'ceremony') return 'badge-danger'
  return 'badge-primary'
}

function fmtDT(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-MX', { month: 'short', day: 'numeric' }) + ' ' +
    d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

function openStageModal(stage) {
  editingStage.value = stage
  if (stage) {
    Object.assign(stageForm.value, { ...stage })
  } else {
    stageForm.value = { name: '', description: '', capacity: null, color: '#6366f1', location_in_venue: '', stream_url: '' }
  }
  showStageModal.value = true
}

function addSessionFor(stage) {
  editingSession.value = null
  sessionForm.value = { title: '', description: '', session_type: 'talk', stage_id: stage.id, speaker_id: null, start_time: '', end_time: '', tags_json: '' }
  showSessionModal.value = true
}

function editSession(s) {
  editingSession.value = s
  sessionForm.value = {
    title: s.title,
    description: s.description || '',
    session_type: s.session_type,
    stage_id: s.stage_id,
    speaker_id: s.speaker_id || null,
    start_time: s.start_time ? s.start_time.slice(0, 16) : '',
    end_time: s.end_time ? s.end_time.slice(0, 16) : '',
    tags_json: s.tags_json || '',
  }
  showSessionModal.value = true
}

async function saveStage() {
  const payload = { ...stageForm.value, convention_id: conv.value.id }
  if (editingStage.value?.id) {
    const { data } = await api.put(`/stages/${editingStage.value.id}`, payload)
    const idx = stages.value.findIndex(s => s.id === data.id)
    if (idx >= 0) stages.value[idx] = data
  } else {
    const { data } = await api.post('/stages/', payload)
    stages.value.push(data)
  }
  showStageModal.value = false
}

async function deleteStage(stage) {
  if (!confirm('¿Eliminar escenario?')) return
  await api.delete(`/stages/${stage.id}`)
  stages.value = stages.value.filter(s => s.id !== stage.id)
}

async function saveSession() {
  const payload = { ...sessionForm.value, convention_id: conv.value.id }
  if (editingSession.value?.id) {
    const { data } = await api.put(`/stages/sessions/${editingSession.value.id}`, payload)
    const idx = sessions.value.findIndex(s => s.id === data.id)
    if (idx >= 0) sessions.value[idx] = data
  } else {
    const { data } = await api.post('/stages/sessions', payload)
    sessions.value.push(data)
  }
  showSessionModal.value = false
}

async function deleteSession(s) {
  if (!confirm('¿Eliminar sesión?')) return
  await api.delete(`/stages/sessions/${s.id}`)
  sessions.value = sessions.value.filter(x => x.id !== s.id)
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  const [stagesRes, sessionsRes, speakersRes] = await Promise.all([
    api.get(`/stages/convention/${conv.value.id}`),
    api.get(`/stages/convention/${conv.value.id}/sessions`),
    api.get(`/speakers/convention/${conv.value.id}`),
  ])
  stages.value = stagesRes.data
  sessions.value = sessionsRes.data
  speakers.value = speakersRes.data
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.stages-list { display: flex; flex-direction: column; gap: 20px; }
.stage-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.stage-header { display: flex; align-items: center; gap: 14px; padding: 16px 20px; border-bottom: 1px solid var(--border); }
.stage-dot { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; }
.stage-info { flex: 1; }
.stage-name { font-weight: 700; font-size: 16px; }
.stage-sub { font-size: 12px; color: var(--text2); }
.stage-actions { display: flex; gap: 8px; }
.sessions-table { padding: 12px; }
.no-sessions { padding: 20px; font-size: 13px; color: var(--text2); text-align: center; }
.empty-state { padding: 40px; text-align: center; color: var(--text2); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.modal .form-group { margin-top: 12px; }
.modal .form-group:first-child { margin-top: 0; }
</style>
