<template>
  <div class="rag-page">
    <div class="page-header">
      <h1>🤖 Asistente IA</h1>
      <p>Tu asesor de negocios con inteligencia artificial — analiza tus datos en tiempo real</p>
    </div>

    <div class="page-body rag-layout">
      <!-- Chat -->
      <div class="chat-panel card">
        <div class="chat-messages" ref="messagesEl">
          <div class="chat-welcome" v-if="messages.length === 0">
            <div class="welcome-icon">🤖</div>
            <h3>¡Hola! Soy tu asesor de negocios</h3>
            <p>Pregúntame sobre tus ventas, inventario, clientes o pídeme recomendaciones estratégicas. Analizo los datos reales de tu negocio.</p>
          </div>

          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message"
            :class="msg.role"
          >
            <div class="msg-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
            <div class="msg-bubble">
              <div class="msg-text" v-html="formatMsg(msg.content)"></div>
              <div class="msg-time">{{ msg.time }}</div>
            </div>
          </div>

          <div v-if="thinking" class="message assistant">
            <div class="msg-avatar">🤖</div>
            <div class="msg-bubble">
              <div class="thinking-dots">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input-area">
          <div class="suggestions">
            <button
              v-for="s in suggestions"
              :key="s"
              class="suggestion-chip"
              @click="sendSuggestion(s)"
            >{{ s }}</button>
          </div>
          <div class="input-row">
            <textarea
              v-model="inputText"
              placeholder="Escribe tu pregunta..."
              rows="1"
              @keydown.enter.exact.prevent="sendMessage"
              @input="autoResize"
              ref="inputEl"
            />
            <button class="send-btn btn btn-primary" :disabled="!inputText.trim() || thinking" @click="sendMessage">
              ➤
            </button>
          </div>
          <p class="input-hint">Presiona Enter para enviar · Shift+Enter para nueva línea</p>
        </div>
      </div>

      <!-- Info panel -->
      <div class="info-panel">
        <div class="card info-card">
          <h4>💡 ¿Qué puedo preguntarle?</h4>
          <ul class="tip-list">
            <li>¿Qué productos debo reabastecer urgentemente?</li>
            <li>¿Cuál es mi producto más rentable?</li>
            <li>¿Cómo puedo aumentar mis ventas este mes?</li>
            <li>¿Qué método de pago prefieren mis clientes?</li>
            <li>Dame un análisis de mi negocio</li>
            <li>¿Cómo mejorar mi gestión de inventario?</li>
          </ul>
        </div>
        <div class="card info-card">
          <h4>⚙️ Estado del asistente</h4>
          <div class="status-item">
            <span class="status-dot" :class="apiConnected ? 'green' : 'yellow'"></span>
            <span>{{ apiConnected ? 'Conectado con Claude AI' : 'Modo sin API key' }}</span>
          </div>
          <p class="status-note">
            {{ apiConnected
              ? 'El asistente analiza tus datos reales del negocio.'
              : 'Configura ANTHROPIC_API_KEY en el backend para habilitar el asistente completo.' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import api from '../api/index.js'

const auth = useAuthStore()
const messages = ref([])
const inputText = ref('')
const thinking = ref(false)
const messagesEl = ref(null)
const inputEl = ref(null)
const apiConnected = ref(false)

const suggestions = [
  '¿Qué productos tienen stock bajo?',
  '¿Cuáles son mis productos más vendidos?',
  'Dame un resumen de mis ventas recientes',
  '¿Cómo puedo mejorar mi rentabilidad?',
  'Recomendaciones para aumentar ventas',
]

function formatMsg(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

function now() {
  return new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

function autoResize(e) {
  const el = e.target
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 120) + 'px'
}

async function sendSuggestion(text) {
  inputText.value = text
  await sendMessage()
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || thinking.value) return

  messages.value.push({ role: 'user', content: text, time: now() })
  inputText.value = ''
  if (inputEl.value) inputEl.value.style.height = 'auto'
  thinking.value = true
  await scrollToBottom()

  try {
    const user = auth.user
    const res = await api.post('/rag/ask', {
      query: text,
      user_profile: {
        business_name: user?.business_name || '',
        top_products: [],
        low_stock_count: 0,
      },
    })
    messages.value.push({ role: 'assistant', content: res.data.response, time: now() })
    // If response doesn't say "no disponible" → API is connected
    if (!res.data.response.includes('no disponible')) apiConnected.value = true
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: 'Lo siento, ocurrió un error al procesar tu consulta. Por favor intenta de nuevo.',
      time: now(),
    })
  } finally {
    thinking.value = false
    await scrollToBottom()
  }
}

onMounted(async () => {
  // Probe to see if API key is set
  try {
    const res = await api.post('/rag/ask', { query: 'hola', user_profile: { business_name: '', top_products: [], low_stock_count: 0 } })
    apiConnected.value = !res.data.response.includes('no disponible')
  } catch {}
})
</script>

<style scoped>
.rag-page { height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
.page-header { flex-shrink: 0; }

.rag-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
  overflow: hidden;
  padding-top: 0;
}

.chat-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-welcome {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
}
.welcome-icon { font-size: 48px; margin-bottom: 12px; }
.chat-welcome h3 { font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.chat-welcome p { font-size: 14px; line-height: 1.6; max-width: 400px; margin: 0 auto; }

.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message.user { flex-direction: row-reverse; }

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.msg-bubble {
  max-width: 70%;
  background: var(--bg3);
  border-radius: 12px;
  padding: 12px 16px;
  border: 1px solid var(--border);
}

.message.user .msg-bubble {
  background: rgba(249,115,22,0.12);
  border-color: rgba(249,115,22,0.3);
}

.msg-text { font-size: 14px; line-height: 1.6; }
.msg-time { font-size: 11px; color: var(--text-muted); margin-top: 6px; }

.thinking-dots {
  display: flex;
  gap: 5px;
  padding: 4px 0;
}
.thinking-dots span {
  width: 8px; height: 8px;
  background: var(--text-muted);
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

.chat-input-area {
  border-top: 1px solid var(--border);
  padding: 12px 16px;
  flex-shrink: 0;
}

.suggestions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.suggestion-chip {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text-muted);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.suggestion-chip:hover { border-color: var(--primary); color: var(--primary); }

.input-row {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-row textarea {
  flex: 1;
  resize: none;
  padding: 10px 14px;
  font-size: 14px;
  line-height: 1.5;
  max-height: 120px;
  overflow-y: auto;
}

.send-btn {
  padding: 10px 18px;
  font-size: 16px;
  flex-shrink: 0;
}

.input-hint { font-size: 11px; color: var(--text-muted); margin-top: 6px; }

/* Info panel */
.info-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.info-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 12px; }
.tip-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.tip-list li {
  font-size: 12px;
  color: var(--text-muted);
  padding: 6px 10px;
  background: var(--bg3);
  border-radius: 6px;
  border-left: 2px solid var(--primary);
  line-height: 1.4;
}

.status-item { display: flex; align-items: center; gap: 8px; font-size: 13px; margin-bottom: 8px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.green { background: var(--success); box-shadow: 0 0 6px var(--success); }
.status-dot.yellow { background: var(--warning); box-shadow: 0 0 6px var(--warning); }
.status-note { font-size: 12px; color: var(--text-muted); line-height: 1.4; }
</style>
