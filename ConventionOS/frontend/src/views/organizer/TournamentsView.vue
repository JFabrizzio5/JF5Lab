<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Torneos</h1>
        <button @click="openModal(null)" class="btn btn-primary">+ Nuevo Torneo</button>
      </div>

      <div class="tournaments-grid">
        <div v-for="t in tournaments" :key="t.id" class="tournament-card">
          <div class="tc-header">
            <div>
              <div class="tc-game">{{ t.game }}</div>
              <div class="tc-name">{{ t.name }}</div>
            </div>
            <span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span>
          </div>
          <div class="tc-meta">
            <span>🎮 {{ formatFormat(t.format) }}</span>
            <span>👥 {{ t.participants_count }}/{{ t.max_participants }}</span>
            <span v-if="t.prize_pool > 0">🏆 ${{ t.prize_pool.toFixed(0) }}</span>
            <span v-if="t.entry_fee > 0">💰 ${{ t.entry_fee.toFixed(0) }} entrada</span>
          </div>
          <div class="tc-actions">
            <button @click="viewRegistrations(t)" class="btn btn-ghost btn-sm">👥 Registros</button>
            <button @click="openModal(t)" class="btn btn-ghost btn-sm">Editar</button>
            <button @click="deleteItem(t)" class="btn btn-danger btn-sm">Eliminar</button>
          </div>

          <!-- Registrations table (expanded) -->
          <div class="registrations" v-if="expandedTournament?.id === t.id">
            <div class="reg-header">Jugadores Registrados</div>
            <table v-if="registrations.length">
              <thead><tr><th>Nombre</th><th>Tag</th><th>Email</th><th>Estado</th><th>Fecha</th></tr></thead>
              <tbody>
                <tr v-for="r in registrations" :key="r.id">
                  <td>{{ r.player_name }}</td>
                  <td>{{ r.player_tag || '—' }}</td>
                  <td>{{ r.player_email }}</td>
                  <td>
                    <select :value="r.status" @change="updateRegStatus(r, $event.target.value)" class="status-select">
                      <option value="registered">Registrado</option>
                      <option value="checked_in">Check-in</option>
                      <option value="eliminated">Eliminado</option>
                      <option value="winner">Ganador</option>
                    </select>
                  </td>
                  <td>{{ fmtDate(r.created_at) }}</td>
                </tr>
              </tbody>
            </table>
            <div v-else class="empty-reg">Sin registros aún</div>
          </div>
        </div>
        <div v-if="!tournaments.length" class="empty-card">Sin torneos. Crea el primero.</div>
      </div>

      <!-- Modal -->
      <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
        <div class="modal">
          <h2>{{ editing?.id ? 'Editar Torneo' : 'Nuevo Torneo' }}</h2>
          <div class="form-group"><label>Nombre *</label><input v-model="form.name" /></div>
          <div class="form-group"><label>Juego</label><input v-model="form.game" placeholder="Street Fighter 6, Pokémon TCG..." /></div>
          <div class="form-group"><label>Formato</label>
            <select v-model="form.format">
              <option value="single_elim">Eliminación Simple</option>
              <option value="double_elim">Doble Eliminación</option>
              <option value="round_robin">Round Robin</option>
              <option value="swiss">Sistema Suizo</option>
            </select>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Máx. participantes</label><input v-model.number="form.max_participants" type="number" min="2" /></div>
            <div class="form-group"><label>Inscripción (MXN)</label><input v-model.number="form.entry_fee" type="number" min="0" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Premio total (MXN)</label><input v-model.number="form.prize_pool" type="number" min="0" /></div>
            <div class="form-group"><label>Escenario</label>
              <select v-model="form.stage_id">
                <option :value="null">Sin escenario</option>
                <option v-for="s in stages" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>
          </div>
          <div class="form-group"><label>Descripción del premio</label><textarea v-model="form.prize_description" rows="2"></textarea></div>
          <div class="form-group"><label>Inicio</label><input v-model="form.start_time" type="datetime-local" /></div>
          <div class="form-group"><label>URL de reglas</label><input v-model="form.rules_url" placeholder="https://..." /></div>
          <div class="form-group"><label>Estado</label>
            <select v-model="form.status">
              <option value="open">Abierto</option>
              <option value="closed">Cerrado</option>
              <option value="in_progress">En progreso</option>
              <option value="finished">Finalizado</option>
            </select>
          </div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="showModal = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
            <button @click="save" :disabled="!form.name" class="btn btn-primary" style="flex:1">Guardar</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const tournaments = ref([])
const stages = ref([])
const showModal = ref(false)
const editing = ref(null)
const expandedTournament = ref(null)
const registrations = ref([])
const form = ref({ name: '', game: '', format: 'single_elim', max_participants: 32, entry_fee: 0, prize_pool: 0, prize_description: '', start_time: '', rules_url: '', status: 'open', stage_id: null })

function statusBadge(s) {
  if (s === 'open') return 'badge-success'
  if (s === 'in_progress') return 'badge-warning'
  if (s === 'finished') return 'badge-info'
  return 'badge-danger'
}

function formatFormat(f) {
  const map = { single_elim: 'Elim. Simple', double_elim: 'Doble Elim.', round_robin: 'Round Robin', swiss: 'Swiss' }
  return map[f] || f
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }) : '—'
}

function openModal(t) {
  editing.value = t
  if (t) {
    Object.assign(form.value, { ...t, start_time: t.start_time ? t.start_time.slice(0, 16) : '' })
  } else {
    form.value = { name: '', game: '', format: 'single_elim', max_participants: 32, entry_fee: 0, prize_pool: 0, prize_description: '', start_time: '', rules_url: '', status: 'open', stage_id: null }
  }
  showModal.value = true
}

async function viewRegistrations(t) {
  if (expandedTournament.value?.id === t.id) {
    expandedTournament.value = null
    registrations.value = []
    return
  }
  expandedTournament.value = t
  const { data } = await api.get(`/tournaments/${t.id}/registrations`)
  registrations.value = data
}

async function updateRegStatus(r, status) {
  await api.patch(`/tournaments/registrations/${r.id}/status`, { status })
  r.status = status
}

async function save() {
  const payload = { ...form.value, convention_id: conv.value.id }
  if (editing.value?.id) {
    const { data } = await api.put(`/tournaments/${editing.value.id}`, payload)
    const idx = tournaments.value.findIndex(t => t.id === data.id)
    if (idx >= 0) tournaments.value[idx] = data
  } else {
    const { data } = await api.post('/tournaments/', payload)
    tournaments.value.push(data)
  }
  showModal.value = false
}

async function deleteItem(t) {
  if (!confirm('¿Eliminar torneo?')) return
  await api.delete(`/tournaments/${t.id}`)
  tournaments.value = tournaments.value.filter(x => x.id !== t.id)
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  const [tRes, sRes] = await Promise.all([
    api.get(`/tournaments/convention/${conv.value.id}`),
    api.get(`/stages/convention/${conv.value.id}`),
  ])
  tournaments.value = tRes.data
  stages.value = sRes.data
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.tournaments-grid { display: flex; flex-direction: column; gap: 16px; }
.tournament-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 20px; }
.tc-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.tc-game { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--accent); font-weight: 700; }
.tc-name { font-size: 18px; font-weight: 800; }
.tc-meta { display: flex; flex-wrap: wrap; gap: 10px; font-size: 13px; color: var(--text2); margin-bottom: 14px; }
.tc-meta span { background: var(--bg3); padding: 4px 10px; border-radius: 6px; }
.tc-actions { display: flex; gap: 8px; }
.registrations { margin-top: 16px; border-top: 1px solid var(--border); padding-top: 16px; }
.reg-header { font-size: 13px; font-weight: 700; margin-bottom: 10px; }
.empty-reg { font-size: 13px; color: var(--text2); }
.status-select { background: var(--bg3); border: 1px solid var(--border); color: var(--text); border-radius: 4px; padding: 4px 8px; font-size: 12px; }
.empty-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 40px; text-align: center; color: var(--text2); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.modal .form-group { margin-top: 12px; }
</style>
