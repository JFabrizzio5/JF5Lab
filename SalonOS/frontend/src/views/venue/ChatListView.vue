<template>
  <div>
    <div class="page-header">
      <h1>Chats</h1>
      <p>Conversaciones con clientes</p>
    </div>

    <div class="page-body">
      <div v-if="loading" style="color:var(--text2)">Cargando conversaciones...</div>

      <div v-else-if="!rooms.length" class="card" style="text-align:center;color:var(--text2);padding:3rem">
        <div style="font-size:3rem;margin-bottom:1rem">💬</div>
        <p>No hay conversaciones aún. Los clientes pueden iniciar un chat desde tu landing pública.</p>
      </div>

      <div v-else class="rooms-list">
        <router-link
          v-for="room in rooms"
          :key="room.id"
          :to="`/chat/${room.id}`"
          class="room-card card"
        >
          <div class="room-avatar">
            {{ room.client_name?.charAt(0)?.toUpperCase() || '?' }}
          </div>
          <div class="room-info">
            <div class="room-name">{{ room.client_name }}</div>
            <div class="room-email">{{ room.client_email }}</div>
            <div class="room-last-msg">{{ room.last_message || 'Sin mensajes' }}</div>
          </div>
          <div class="room-time">{{ formatDate(room.last_message_at || room.created_at) }}</div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const rooms = ref([])
const loading = ref(true)

function formatDate(dt) {
  if (!dt) return ''
  const d = new Date(dt)
  const now = new Date()
  if (d.toDateString() === now.toDateString()) {
    return d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
  }
  return d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short' })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/chat/rooms')
    rooms.value = data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.rooms-list { display: flex; flex-direction: column; gap: 0.5rem; }

.room-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  text-decoration: none;
  color: var(--text);
  transition: all 0.2s;
}

.room-card:hover {
  border-color: var(--primary);
  background: rgba(124,58,237,0.05);
}

.room-avatar {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.room-info { flex: 1; min-width: 0; }

.room-name { font-size: 0.95rem; font-weight: 600; }

.room-email { font-size: 0.78rem; color: var(--text2); }

.room-last-msg {
  font-size: 0.82rem;
  color: var(--text2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 0.2rem;
}

.room-time {
  font-size: 0.75rem;
  color: var(--text2);
  flex-shrink: 0;
}
</style>
