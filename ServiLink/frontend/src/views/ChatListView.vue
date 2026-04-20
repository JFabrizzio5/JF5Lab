<template>
  <div class="chat-list-page">
    <div class="page-header">
      <h1>💬 Conversaciones</h1>
    </div>

    <div v-if="loading" class="loading">Cargando chats...</div>

    <div v-else-if="rooms.length === 0" class="empty">
      <div class="empty-icon">💬</div>
      <p>No tienes conversaciones aún.</p>
      <p v-if="auth.isClient" class="hint">Ve al <router-link to="/marketplace">Marketplace</router-link> y contacta a un profesional.</p>
    </div>

    <div v-else class="rooms-list">
      <div
        v-for="room in rooms"
        :key="room.room_id"
        class="room-card"
        @click="$router.push(`/chat/${room.room_id}`)"
      >
        <img
          :src="room.other_user.avatar_url || `https://api.dicebear.com/7.x/initials/svg?seed=${room.other_user.name}`"
          class="room-avatar"
        />
        <div class="room-info">
          <div class="room-name">{{ room.other_user.name }}</div>
          <div class="room-role">{{ room.other_user.role === 'freelancer' ? 'Profesional' : 'Cliente' }}</div>
          <div class="room-last">{{ room.last_message || 'Sin mensajes aún' }}</div>
        </div>
        <div class="room-time">{{ formatDate(room.last_at) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { chatApi } from '../api/index.js'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const rooms = ref([])
const loading = ref(true)

async function load() {
  try {
    const res = await chatApi.listRooms()
    rooms.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  const d = new Date(iso)
  const now = new Date()
  const diff = (now - d) / 1000
  if (diff < 60) return 'ahora'
  if (diff < 3600) return `${Math.floor(diff/60)}m`
  if (diff < 86400) return `${Math.floor(diff/3600)}h`
  return d.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' })
}

onMounted(load)
</script>

<style scoped>
.chat-list-page { padding: 24px; max-width: 720px; margin: 0 auto; }

.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 22px; font-weight: 700; }

.loading { text-align: center; color: var(--text2); padding: 40px; }

.empty { text-align: center; padding: 60px 20px; color: var(--text2); }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty p { font-size: 14px; margin: 4px 0; }
.hint a { color: var(--accent); text-decoration: none; }

.rooms-list { display: flex; flex-direction: column; gap: 8px; }

.room-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.1s;
}
.room-card:hover { border-color: var(--accent); transform: translateX(2px); }

.room-avatar { width: 46px; height: 46px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }

.room-info { flex: 1; min-width: 0; }
.room-name { font-weight: 600; font-size: 14px; }
.room-role { font-size: 11px; color: var(--accent); margin-bottom: 4px; }
.room-last { font-size: 13px; color: var(--text2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.room-time { font-size: 11px; color: var(--text2); flex-shrink: 0; }
</style>
