<template>
  <div class="chat-page">
    <div class="chat-header">
      <router-link to="/chats" class="back-btn">← Volver</router-link>
      <div class="chat-client-info">
        <div class="chat-avatar">{{ clientName?.charAt(0)?.toUpperCase() || '?' }}</div>
        <div>
          <div class="chat-client-name">{{ clientName || 'Cliente' }}</div>
          <div class="chat-status">{{ wsConnected ? '🟢 En línea' : '🔴 Desconectado' }}</div>
        </div>
      </div>
    </div>

    <div class="chat-messages" ref="messagesEl">
      <div v-if="loading" style="text-align:center;color:var(--text2);padding:2rem">Cargando mensajes...</div>
      <div v-else-if="!messages.length" style="text-align:center;color:var(--text2);padding:2rem">
        No hay mensajes aún. Inicia la conversación.
      </div>
      <div
        v-for="m in messages"
        :key="m.id"
        :class="['msg-bubble', m.sender_type === 'staff' ? 'msg-staff' : 'msg-client']"
      >
        <div class="msg-sender">{{ m.sender_name }}</div>
        <div class="msg-content">{{ m.content }}</div>
        <div class="msg-time">{{ formatTime(m.created_at) }}</div>
      </div>
    </div>

    <div class="chat-input-bar">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Escribe un mensaje..."
        @keydown.enter="sendMessage"
      />
      <button @click="sendMessage" class="btn btn-primary" :disabled="!newMessage.trim()">Enviar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/index.js'

const route = useRoute()
const roomId = route.params.room_id
const messages = ref([])
const loading = ref(true)
const newMessage = ref('')
const messagesEl = ref(null)
const clientName = ref('')
const wsConnected = ref(false)

let ws = null

function formatTime(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

async function loadMessages() {
  loading.value = true
  try {
    const { data } = await api.get(`/chat/rooms/${roomId}/messages`)
    messages.value = data
    if (data.length > 0) {
      const clientMsg = data.find(m => m.sender_type === 'client')
      if (clientMsg) clientName.value = clientMsg.sender_name
    }
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

function connectWS() {
  const token = localStorage.getItem('salonos_token')
  if (!token) return

  const wsProto = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${wsProto}//${window.location.host}/api/chat/ws/${roomId}?token=${token}`

  ws = new WebSocket(wsUrl)

  ws.onopen = () => { wsConnected.value = true }
  ws.onclose = () => { wsConnected.value = false }

  ws.onmessage = async (e) => {
    const msg = JSON.parse(e.data)
    messages.value.push(msg)
    await scrollToBottom()
  }
}

function sendMessage() {
  const content = newMessage.value.trim()
  if (!content || !ws || ws.readyState !== WebSocket.OPEN) return
  ws.send(JSON.stringify({ content }))
  newMessage.value = ''
}

onMounted(async () => {
  // Load rooms to get client name
  try {
    const { data } = await api.get('/chat/rooms')
    const room = data.find(r => String(r.id) === String(roomId))
    if (room) clientName.value = room.client_name
  } catch {}

  await loadMessages()
  connectWS()
})

onUnmounted(() => {
  if (ws) ws.close()
})
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg2);
}

.back-btn {
  color: var(--text2);
  text-decoration: none;
  font-size: 0.9rem;
  white-space: nowrap;
}

.back-btn:hover { color: var(--text); }

.chat-client-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.chat-avatar {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 700;
  color: white;
}

.chat-client-name { font-size: 0.95rem; font-weight: 600; }
.chat-status { font-size: 0.75rem; color: var(--text2); }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.msg-bubble {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
}

.msg-staff {
  align-self: flex-end;
  background: rgba(124,58,237,0.2);
  border: 1px solid rgba(124,58,237,0.3);
}

.msg-client {
  align-self: flex-start;
  background: var(--surface);
  border: 1px solid var(--border);
}

.msg-sender {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text2);
  margin-bottom: 0.25rem;
}

.msg-content {
  font-size: 0.9rem;
  color: var(--text);
  line-height: 1.5;
}

.msg-time {
  font-size: 0.7rem;
  color: var(--text2);
  margin-top: 0.25rem;
  text-align: right;
}

.chat-input-bar {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border);
  background: var(--bg2);
}

.chat-input-bar input {
  flex: 1;
}
</style>
