<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Asistentes</h1>
        <div style="display:flex;gap:10px;align-items:center">
          <input v-model="search" placeholder="Buscar por nombre o email..." class="search-input" style="width:280px" />
          <select v-model="filterStatus" class="filter-select">
            <option value="">Todos los estados</option>
            <option value="paid">Pagado</option>
            <option value="pending">Pendiente</option>
            <option value="checked_in">Check-in</option>
            <option value="cancelled">Cancelado</option>
          </select>
        </div>
      </div>

      <div class="stats-bar">
        <div class="stat-pill">Total: <strong>{{ tickets.length }}</strong></div>
        <div class="stat-pill paid">Pagados: <strong>{{ countByStatus('paid') + countByStatus('checked_in') }}</strong></div>
        <div class="stat-pill checkin">Check-in: <strong>{{ countByStatus('checked_in') }}</strong></div>
        <div class="stat-pill pending">Pendientes: <strong>{{ countByStatus('pending') }}</strong></div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Tipo</th>
            <th>QR Code</th>
            <th>Estado</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in filteredTickets" :key="t.id">
            <td>{{ t.attendee_name }}</td>
            <td>{{ t.attendee_email }}</td>
            <td>{{ t.attendee_phone || '—' }}</td>
            <td>
              <span class="badge" :style="`background:${t.ticket_type?.color}22;color:${t.ticket_type?.color}`">
                {{ t.ticket_type?.name }}
              </span>
            </td>
            <td><code class="qr-code">{{ t.qr_code }}</code></td>
            <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
            <td>{{ fmtDate(t.created_at) }}</td>
            <td>
              <button @click="toggleCheckin(t)" class="btn btn-sm" :class="t.status === 'checked_in' ? 'btn-ghost' : 'btn-primary'">
                {{ t.status === 'checked_in' ? '↩ Deshacer' : '✓ Check-in' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!filteredTickets.length" class="empty-state">Sin asistentes que coincidan con el filtro</div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const tickets = ref([])
const search = ref('')
const filterStatus = ref('')

function statusBadge(s) {
  if (s === 'paid') return 'badge-success'
  if (s === 'checked_in') return 'badge-info'
  if (s === 'pending') return 'badge-warning'
  return 'badge-danger'
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
}

function countByStatus(s) {
  return tickets.value.filter(t => t.status === s).length
}

const filteredTickets = computed(() => {
  return tickets.value.filter(t => {
    const q = search.value.toLowerCase()
    const matchSearch = !q ||
      t.attendee_name?.toLowerCase().includes(q) ||
      t.attendee_email?.toLowerCase().includes(q)
    const matchStatus = !filterStatus.value || t.status === filterStatus.value
    return matchSearch && matchStatus
  })
})

async function toggleCheckin(t) {
  const { data } = await api.patch(`/tickets/${t.id}/checkin`)
  const idx = tickets.value.findIndex(x => x.id === data.id)
  if (idx >= 0) tickets.value[idx] = data
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  tickets.value = await api.get(`/tickets/convention/${conv.value.id}`).then(r => r.data)
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.search-input, .filter-select { background: var(--bg3); border: 1px solid var(--border); color: var(--text); border-radius: 8px; padding: 8px 12px; font-size: 14px; }
.filter-select { width: 180px; }
.stats-bar { display: flex; gap: 12px; margin-bottom: 20px; }
.stat-pill { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 8px 14px; font-size: 13px; }
.stat-pill.paid { border-color: rgba(16,185,129,0.3); }
.stat-pill.checkin { border-color: rgba(59,130,246,0.3); }
.stat-pill.pending { border-color: rgba(245,158,11,0.3); }
code.qr-code { font-family: monospace; font-size: 11px; background: var(--bg3); padding: 2px 6px; border-radius: 4px; }
.empty-state { padding: 20px; text-align: center; color: var(--text2); }
</style>
