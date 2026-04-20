<template>
  <div class="chat-page">
    <div class="chat-header">
      <button class="back-btn" @click="$router.back()">← Volver</button>
      <div v-if="otherUser" class="chat-peer">
        <img :src="otherUser.avatar_url || `https://api.dicebear.com/7.x/initials/svg?seed=${otherUser.name}`" class="peer-avatar" />
        <div>
          <div class="peer-name">{{ otherUser.name }}</div>
          <div class="peer-role">{{ otherUser.role === 'freelancer' ? 'Profesional' : 'Cliente' }}</div>
        </div>
      </div>
      <div class="conn-badge" :class="wsStatus">{{ wsLabel }}</div>
    </div>

    <div class="messages-area" ref="messagesEl">
      <div v-if="loading" class="loading-msgs">Cargando mensajes...</div>

      <template v-else>
        <div v-for="msg in messages" :key="msg.id" class="msg-row" :class="{ mine: msg.is_mine }">
          <img v-if="!msg.is_mine" :src="msg.sender_avatar || `https://api.dicebear.com/7.x/initials/svg?seed=${msg.sender_name}`" class="msg-avatar" />
          <div class="msg-bubble">
            <div v-if="!msg.is_mine" class="msg-sender">{{ msg.sender_name }}</div>
            <div class="msg-content">{{ msg.content }}</div>
            <div class="msg-time">{{ formatTime(msg.created_at) }}</div>
          </div>
        </div>

        <div v-if="typing" class="typing-indicator">
          <span>{{ typing }} está escribiendo</span>
          <span class="dots"><span>.</span><span>.</span><span>.</span></span>
        </div>
      </template>
    </div>

    <div class="chat-input-area">
      <textarea
        v-model="inputText"
        placeholder="Escribe un mensaje..."
        rows="1"
        @keydown.enter.exact.prevent="sendMessage"
        @input="onInput"
        class="msg-input"
      />
      <button @click="sendMessage" :disabled="!inputText.trim() || wsStatus !== 'connected'" class="send-btn">
        ➤
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import { chatApi, createChatWS } from '../api/index.js'
import { useAuthStore } from '../stores/auth.js'

const route = useRoute()
const auth = useAuthStore()
const roomId = Number(route.params.room_id)

const messages = ref([])
const loading = ref(true)
const inputText = ref('')
const messagesEl = ref(null)
const wsStatus = ref('connecting')
const typing = ref('')
const otherUser = ref(null)

let ws = null
let typingTimer = null

const wsLabel = computed(() => ({
  connecting: '⟳ Conectando',
  connected: '● Conectado',
  disconnected: '○ Desconectado',
}[wsStatus.value]))

async function loadHistory() {
  try {
    const res = await chatApi.getMessages(roomId)
    messages.value = res.data
    await nextTick()
    scrollBottom()

    // Derive other user from messages
    const other = res.data.find(m => !m.is_mine)
    if (other) {
      otherUser.value = { name: other.sender_name, avatar_url: other.sender_avatar, role: 'freelancer' }
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// Load room list to get other user info
async function loadRoomInfo() {
  try {
    const rooms = await chatApi.listRooms()
    const room = rooms.data.find(r => r.room_id === roomId)
    if (room) otherUser.value = room.other_user
  } catch {}
}

function connectWS() {
  ws = createChatWS(roomId)

  ws.onopen = () => { wsStatus.value = 'connected' }

  ws.onmessage = async (ev) => {
    const data = JSON.parse(ev.data)
    if (data.type === 'message') {
      messages.value.push({
        id: data.id,
        content: data.content,
        sender_id: data.sender_id,
        sender_name: data.sender_name,
        sender_avatar: data.sender_avatar,
        created_at: data.created_at,
        is_mine: data.sender_id === auth.user?.id,
      })
      typing.value = ''
      await nextTick()
      scrollBottom()
    } else if (data.type === 'typing') {
      if (data.user_id !== auth.user?.id) {
        typing.value = data.user_name
        clearTimeout(typingTimer)
        typingTimer = setTimeout(() => { typing.value = '' }, 3000)
      }
    }
  }

  ws.onclose = () => {
    wsStatus.value = 'disconnected'
    setTimeout(connectWS, 3000)
  }

  ws.onerror = () => { wsStatus.value = 'disconnected' }
}

function sendMessage() {
  const content = inputText.value.trim()
  if (!content || wsStatus.value !== 'connected') return
  ws.send(JSON.stringify({ type: 'message', content }))
  inputText.value = ''
}

let lastTypingSent = 0
function onInput() {
  const now = Date.now()
  if (now - lastTypingSent > 2000 && ws?.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'typing' }))
    lastTypingSent = now
  }
}

function scrollBottom() {
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

function formatTime(iso) {
  const d = new Date(iso)
  return d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  await Promise.all([loadHistory(), loadRoomInfo()])
  connectWS()
})

onUnmounted(() => {
  clearTimeout(typingTimer)
  if (ws) ws.close()
})
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg);
  color: var(--text);
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  flex-shrink: 0;
}

.back-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 12px;
  color: var(--text2);
  cursor: pointer;
  font-size: 13px;
}
.back-btn:hover { border-color: var(--accent); color: var(--accent); }

.chat-peer { display: flex; align-items: center; gap: 10px; flex: 1; }
.peer-avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
.peer-name { font-weight: 600; font-size: 14px; }
.peer-role { font-size: 11px; color: var(--text2); }

.conn-badge { font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 600; }
.conn-badge.connected { background: #16a34a22; color: #4ade80; }
.conn-badge.connecting { background: #ca8a0422; color: #fbbf24; }
.conn-badge.disconnected { background: #dc262622; color: #f87171; }

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.loading-msgs { text-align: center; color: var(--text2); padding: 40px; }

.msg-row {
  display: flex;
  gap: 10px;
  max-width: 70%;
}
.msg-row.mine {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; flex-shrink: 0; margin-top: 2px; }

.msg-bubble {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 14px;
  max-width: 100%;
}
.msg-row.mine .msg-bubble {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.msg-sender { font-size: 11px; font-weight: 600; color: var(--text2); margin-bottom: 4px; }
.msg-row.mine .msg-sender { display: none; }
.msg-content { font-size: 14px; line-height: 1.5; word-break: break-word; }
.msg-time { font-size: 10px; color: rgba(255,255,255,0.6); margin-top: 4px; text-align: right; }
.msg-row:not(.mine) .msg-time { color: var(--text2); }

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text2);
  padding: 4px 8px;
}
.dots span {
  animation: blink 1.2s infinite;
  font-size: 16px;
}
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80%,100% { opacity: 0 } 40% { opacity: 1 } }

.chat-input-area {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid var(--border);
  background: var(--surface);
  flex-shrink: 0;
}

.msg-input {
  flex: 1;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
  resize: none;
  font-family: inherit;
  line-height: 1.5;
  max-height: 120px;
  overflow-y: auto;
}
.msg-input:focus { outline: none; border-color: var(--accent); }

.send-btn {
  background: var(--accent);
  border: none;
  border-radius: 12px;
  padding: 10px 18px;
  color: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: opacity 0.2s;
  flex-shrink: 0;
}
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.send-btn:not(:disabled):hover { opacity: 0.85; }
</style>
