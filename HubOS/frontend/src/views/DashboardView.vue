<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Dashboard</h1>
        <p>Panorama general del workspace.</p>
      </div>
      <router-link to="/chat" class="btn btn-primary">
        <i data-lucide="message-circle" style="width:16px;height:16px"></i>
        Abrir chats
      </router-link>
    </div>
    <div class="page-body">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Contactos</div>
          <div class="stat-value">{{ stats.contacts }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Deals abiertos</div>
          <div class="stat-value">{{ stats.deals_open }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Pipeline valor</div>
          <div class="stat-value">${{ formatMoney(stats.pipeline_value) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Sesiones WhatsApp</div>
          <div class="stat-value">{{ stats.sessions }}</div>
        </div>
      </div>

      <div class="two-col">
        <div class="card">
          <div class="card-head">
            <h3>Últimos contactos</h3>
            <router-link to="/contacts" class="link">Ver todos →</router-link>
          </div>
          <div v-if="!contacts.length" class="empty">Sin contactos aún.</div>
          <ul v-else class="list">
            <li v-for="c in contacts.slice(0,5)" :key="c.id">
              <div class="avatar">{{ (c.name || '?')[0].toUpperCase() }}</div>
              <div class="meta">
                <div class="name">{{ c.name }}</div>
                <div class="sub">{{ c.company || c.email || c.phone }}</div>
              </div>
              <span class="badge badge-primary">{{ c.source }}</span>
            </li>
          </ul>
        </div>

        <div class="card">
          <div class="card-head">
            <h3>Deals recientes</h3>
            <router-link to="/deals" class="link">Ver kanban →</router-link>
          </div>
          <div v-if="!deals.length" class="empty">Sin deals aún.</div>
          <ul v-else class="list">
            <li v-for="d in deals.slice(0,5)" :key="d.id">
              <div class="icon-wrap"><i data-lucide="briefcase" style="width:14px;height:14px"></i></div>
              <div class="meta">
                <div class="name">{{ d.title }}</div>
                <div class="sub">${{ formatMoney(d.value) }} · {{ d.contact?.name || '—' }}</div>
              </div>
              <span class="badge" :class="badgeForStage(d.stage)">{{ d.stage }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api/index.js'

const contacts = ref([])
const deals = ref([])
const sessions = ref([])

const stats = computed(() => ({
  contacts: contacts.value.length,
  deals_open: deals.value.filter(d => d.status === 'open').length,
  pipeline_value: deals.value.filter(d => d.status === 'open').reduce((a, b) => a + (b.value || 0), 0),
  sessions: sessions.value.length,
}))

function formatMoney(n) { return (n || 0).toLocaleString('es-MX', { maximumFractionDigits: 0 }) }
function badgeForStage(s) {
  const map = { 'Ganado': 'badge-success', 'Perdido': 'badge-danger', 'Propuesta': 'badge-accent', 'Negociación': 'badge-warning' }
  return map[s] || 'badge-primary'
}

async function load() {
  try {
    const [c, d, s] = await Promise.all([
      api.get('/contacts/'),
      api.get('/deals/'),
      api.get('/chat/sessions'),
    ])
    contacts.value = c.data
    deals.value = d.data
    sessions.value = s.data
  } catch (e) { console.error(e) }
}
onMounted(() => { load(); if (window.lucide) window.lucide.createIcons() })
</script>

<style scoped>
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
@media (max-width: 860px) { .two-col { grid-template-columns: 1fr; } }
.card-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.card-head h3 { font-size: 1rem; font-weight: 700; }
.link { font-size: 0.8rem; color: var(--primary); }
.empty { color: var(--text3); text-align: center; padding: 1.5rem; font-size: 0.88rem; }
.list { list-style: none; display: flex; flex-direction: column; gap: 0.6rem; }
.list li {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.6rem;
  border-radius: 9px;
  background: rgba(255,255,255,0.02);
}
.avatar, .icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  color: white;
  flex-shrink: 0;
}
.meta { flex: 1; min-width: 0; }
.name { font-size: 0.87rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sub { font-size: 0.72rem; color: var(--text3); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>
