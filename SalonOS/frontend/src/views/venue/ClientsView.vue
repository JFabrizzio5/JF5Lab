<template>
  <div>
    <div class="page-header" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
      <div>
        <h1>Clientes</h1>
        <p>CRM de clientes y prospectos</p>
      </div>
      <button @click="showCreate = true" class="btn btn-primary">+ Nuevo cliente</button>
    </div>

    <div class="page-body">
      <!-- Search bar -->
      <div class="search-bar">
        <input v-model="search" type="text" placeholder="Buscar por nombre, email o teléfono..." @input="loadClients" />
        <select v-model="sourceFilter" @change="loadClients" style="max-width:160px">
          <option value="">Todas las fuentes</option>
          <option value="web">Web</option>
          <option value="whatsapp">WhatsApp</option>
          <option value="referral">Referido</option>
          <option value="direct">Directo</option>
        </select>
      </div>

      <div class="card" style="padding:0">
        <table>
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Teléfono</th>
              <th>Fuente</th>
              <th>Eventos</th>
              <th>Registro</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading"><td colspan="6" style="text-align:center;color:var(--text2);padding:2rem">Cargando...</td></tr>
            <tr v-else-if="!clients.length"><td colspan="6" style="text-align:center;color:var(--text2);padding:2rem">No se encontraron clientes</td></tr>
            <tr v-for="c in clients" :key="c.id" @click="selectClient(c)" style="cursor:pointer">
              <td>
                <div class="client-name">{{ c.name }}</div>
                <div class="client-email">{{ c.email }}</div>
              </td>
              <td>{{ c.phone || '—' }}</td>
              <td><span :class="`badge badge-${c.source}`">{{ c.source }}</span></td>
              <td>{{ c.event_count || 0 }}</td>
              <td>{{ formatDate(c.created_at) }}</td>
              <td>
                <button @click.stop="selectClient(c)" class="btn btn-ghost btn-sm">Ver</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Client detail sidebar -->
    <div v-if="selected" class="client-sidebar" @click.self="selected = null">
      <div class="sidebar-panel">
        <div class="sidebar-header">
          <h2>{{ selected.name }}</h2>
          <button @click="selected = null" class="close-btn">✕</button>
        </div>

        <div class="client-detail">
          <div class="detail-row"><span>Email</span><span>{{ selected.email || '—' }}</span></div>
          <div class="detail-row"><span>Teléfono</span><span>{{ selected.phone || '—' }}</span></div>
          <div class="detail-row"><span>Fuente</span><span :class="`badge badge-${selected.source}`">{{ selected.source }}</span></div>
          <div class="detail-row"><span>Registro</span><span>{{ formatDate(selected.created_at) }}</span></div>
        </div>

        <div class="form-group">
          <label>Notas internas</label>
          <textarea v-model="editNotes" rows="3" placeholder="Agregar notas..."></textarea>
          <button @click="saveNotes" class="btn btn-primary btn-sm" style="margin-top:.5rem">Guardar notas</button>
        </div>

        <h3 style="margin:1.5rem 0 0.75rem;font-size:0.95rem">Eventos</h3>
        <div v-if="!selectedDetail?.bookings?.length" class="empty-msg">Sin eventos</div>
        <div v-for="b in selectedDetail?.bookings" :key="b.id" class="booking-chip">
          <div class="booking-chip-title">{{ b.title }}</div>
          <div class="booking-chip-meta">{{ formatDate(b.start_datetime) }} · {{ b.guests_count }} personas</div>
          <span :class="`badge badge-${b.status}`">{{ b.status }}</span>
        </div>

        <div style="margin-top:1.5rem;display:flex;gap:.75rem;flex-wrap:wrap">
          <router-link :to="`/chats`" class="btn btn-ghost btn-sm">💬 Chat</router-link>
          <router-link to="/events" class="btn btn-primary btn-sm">+ Crear evento</router-link>
        </div>
      </div>
    </div>

    <!-- Create client modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal">
        <h2>Nuevo cliente</h2>
        <div class="form-group">
          <label>Nombre *</label>
          <input v-model="newClient.name" type="text" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="newClient.email" type="email" />
        </div>
        <div class="form-group">
          <label>Teléfono</label>
          <input v-model="newClient.phone" type="tel" />
        </div>
        <div class="form-group">
          <label>Fuente</label>
          <select v-model="newClient.source">
            <option value="web">Web</option>
            <option value="whatsapp">WhatsApp</option>
            <option value="referral">Referido</option>
            <option value="direct">Directo</option>
          </select>
        </div>
        <div class="form-group">
          <label>Notas</label>
          <textarea v-model="newClient.notes" rows="3"></textarea>
        </div>
        <div class="modal-footer">
          <button @click="showCreate = false" class="btn btn-ghost">Cancelar</button>
          <button @click="createClient" class="btn btn-primary" :disabled="creating">
            {{ creating ? 'Guardando...' : 'Crear cliente' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const clients = ref([])
const loading = ref(true)
const search = ref('')
const sourceFilter = ref('')
const selected = ref(null)
const selectedDetail = ref(null)
const editNotes = ref('')
const showCreate = ref(false)
const creating = ref(false)

const newClient = ref({ name: '', email: '', phone: '', source: 'web', notes: '' })

function formatDate(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function loadClients() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (sourceFilter.value) params.source = sourceFilter.value
    const { data } = await api.get('/clients/', { params })
    clients.value = data
  } finally {
    loading.value = false
  }
}

async function selectClient(c) {
  selected.value = c
  editNotes.value = c.notes || ''
  try {
    const { data } = await api.get(`/clients/${c.id}`)
    selectedDetail.value = data
  } catch {}
}

async function saveNotes() {
  if (!selected.value) return
  try {
    await api.put(`/clients/${selected.value.id}`, { notes: editNotes.value })
    selected.value.notes = editNotes.value
  } catch {}
}

async function createClient() {
  if (!newClient.value.name) return
  creating.value = true
  try {
    await api.post('/clients/', newClient.value)
    showCreate.value = false
    newClient.value = { name: '', email: '', phone: '', source: 'web', notes: '' }
    await loadClients()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al crear cliente')
  } finally {
    creating.value = false
  }
}

onMounted(loadClients)
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.client-name { font-size: 0.9rem; font-weight: 600; }
.client-email { font-size: 0.78rem; color: var(--text2); }

.client-sidebar {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 200;
  display: flex;
  justify-content: flex-end;
}

.sidebar-panel {
  width: 400px;
  background: var(--surface);
  border-left: 1px solid var(--border);
  height: 100%;
  overflow-y: auto;
  padding: 1.5rem;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.sidebar-header h2 { font-size: 1.2rem; font-weight: 700; }

.close-btn {
  background: none;
  border: none;
  color: var(--text2);
  font-size: 1.2rem;
  cursor: pointer;
}

.client-detail {
  background: var(--bg2);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.875rem;
}

.detail-row:last-child { border-bottom: none; }
.detail-row > span:first-child { color: var(--text2); }

.booking-chip {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.booking-chip-title { font-size: 0.875rem; font-weight: 600; margin-bottom: 0.25rem; }
.booking-chip-meta { font-size: 0.78rem; color: var(--text2); margin-bottom: 0.5rem; }

.empty-msg { color: var(--text2); font-size: 0.875rem; padding: 0.5rem 0; }
</style>
