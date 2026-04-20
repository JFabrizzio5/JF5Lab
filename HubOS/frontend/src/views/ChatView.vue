<template>
  <div class="chat-shell">
    <!-- Sessions bar -->
    <aside class="sessions-bar">
      <div class="sb-head">
        <h3>Mis sesiones</h3>
        <button @click="createSession" class="btn btn-primary btn-sm" :disabled="creatingSession" :title="creatingSession ? 'Creando…' : 'Nueva sesión'">
          <i v-show="!creatingSession" data-lucide="plus" style="width:14px;height:14px"></i>
          <span v-show="creatingSession" class="mini-spinner"></span>
        </button>
      </div>
      <div class="sessions">
        <div v-if="!sessions.length" class="empty">
          Aún no has conectado un WhatsApp. Crea una sesión nueva.
        </div>
        <div v-for="s in sessions" :key="s.id" class="session" :class="{ active: activeSession?.id === s.id }" @click="selectSession(s)">
          <div class="dot" :class="`dot-${s.status}`"></div>
          <div class="info">
            <div class="name">{{ s.display_name || s.instance_name }}</div>
            <div class="phone">{{ s.phone_number || s.status }}</div>
          </div>
          <button v-if="s.status === 'connected'" @click.stop="syncChats(s)" class="mini" :disabled="syncingId === s.id" :title="syncingId === s.id ? 'Sincronizando…' : 'Importar chats de WhatsApp'">
            <i data-lucide="refresh-cw" style="width:14px;height:14px"></i>
          </button>
          <button @click.stop="showQr(s)" class="mini" title="QR / reconectar">
            <i data-lucide="qr-code" style="width:14px;height:14px"></i>
          </button>
          <button @click.stop="removeSession(s)" class="mini danger" title="Eliminar sesión (los chats se conservan)">
            <i data-lucide="x" style="width:14px;height:14px"></i>
          </button>
        </div>
      </div>
    </aside>

    <!-- Conversations list -->
    <aside class="conv-list">
      <div class="sb-head">
        <h3>Conversaciones</h3>
        <button @click="openNewConv" class="btn btn-primary btn-sm" :disabled="!activeSession || activeSession.status !== 'connected'" title="Nueva conversación">
          <i data-lucide="plus" style="width:14px;height:14px"></i>
        </button>
      </div>
      <div v-if="!conversations.length" class="empty">
        Sin conversaciones. Envía un mensaje desde WhatsApp a tu número para iniciar.
      </div>
      <div v-for="c in conversations" :key="c.id" class="conv" :class="{ active: activeConv?.id === c.id }" @click="selectConv(c)">
        <div class="avatar">{{ (c.contact_name || '?')[0].toUpperCase() }}</div>
        <div class="info">
          <div class="row1">
            <span class="name">{{ c.contact_name || c.contact_phone }}</span>
            <span class="time">{{ relTime(c.last_message_at) }}</span>
          </div>
          <div class="row2">
            <span class="last">{{ c.last_message || '—' }}</span>
            <span v-if="c.unread" class="unread">{{ c.unread }}</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Messages panel -->
    <section class="messages-panel">
      <div v-if="!activeConv" class="placeholder">
        <i data-lucide="message-circle" style="width:48px;height:48px;color:var(--text3)"></i>
        <p>Selecciona una conversación.</p>
      </div>
      <template v-else>
        <div class="msg-head">
          <div class="avatar">{{ (activeConv.contact_name || '?')[0].toUpperCase() }}</div>
          <div style="flex:1;min-width:0">
            <div class="name">{{ activeConv.contact_name || activeConv.contact_phone }}</div>
            <div class="phone">{{ activeConv.contact_phone }}</div>
          </div>
          <!-- Always-available rename/link button. WhatsApp LIDs hide the real
               phone number, so every chat can optionally be annotated with the
               true contact. Shown as a neutral edit icon, not a warning. -->
          <button @click="openLinkContact" class="mini" title="Renombrar / vincular número real">
            <i data-lucide="pencil" style="width:14px;height:14px"></i>
          </button>
          <!-- Loud banner: only when a send has failed with LID privacy. -->
          <button v-if="needsLinkPrompt" @click="openLinkContact" class="lid-warn" title="Agregar número real para poder responder">
            <i data-lucide="shield-alert" style="width:14px;height:14px"></i>
            Vincular número real
          </button>
          <button v-if="duplicates.length" @click="openMerge" class="dup-warn" :title="`${duplicates.length} conversación(es) duplicada(s) detectada(s)`">
            <i data-lucide="git-merge" style="width:14px;height:14px"></i>
            Fusionar ({{ duplicates.length }})
          </button>
        </div>

        <div ref="msgsRef" class="msgs">
          <div v-for="m in messages" :key="m.id" class="msg" :class="m.from_me ? 'out' : 'in'">
            <div class="bubble" :class="{ 'bubble-media': m.media_type }">
              <div v-if="isGroup && !m.from_me && m.author_name" class="author" :style="{ color: authorColor(m.author_name) }">
                {{ m.author_name }}
              </div>
              <img
                v-if="m.media_type === 'image' || m.media_type === 'sticker'"
                :src="mediaUrl(m.id)"
                class="media-img"
                loading="lazy"
                @click="openMedia(m)"
              />
              <video
                v-else-if="m.media_type === 'video'"
                :src="mediaUrl(m.id)"
                class="media-video"
                controls
                preload="metadata"
              />
              <audio
                v-else-if="m.media_type === 'audio'"
                :src="mediaUrl(m.id)"
                class="media-audio"
                controls
                preload="none"
              />
              <a
                v-else-if="m.media_type === 'document'"
                :href="mediaUrl(m.id)"
                target="_blank"
                rel="noopener"
                class="media-doc"
              >
                <i data-lucide="file" style="width:18px;height:18px"></i>
                {{ m.body || 'Documento' }}
              </a>
              <!-- Visible body: for media bubbles only show the caption if it's
                   user-written (skip the auto-placeholders we generated for
                   empty bodies like "[Imagen]"). -->
              <div v-if="bodyToShow(m)" class="body">{{ bodyToShow(m) }}</div>
              <div class="ts">{{ fmtTime(m.timestamp) }}</div>
            </div>
          </div>
          <div v-if="peerTyping" class="msg in">
            <div class="bubble typing-bubble">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>
        <div class="composer">
          <input
            v-model="draft"
            @keydown.enter.prevent="send"
            @input="broadcastTyping"
            placeholder="Escribe un mensaje…"
          />
          <button @click="showTemplates = true" class="btn btn-ghost" title="Insertar plantilla">
            <i data-lucide="layout-template" style="width:16px;height:16px"></i>
          </button>
          <button @click="send" class="btn btn-primary" :disabled="!draft">
            <i data-lucide="send" style="width:16px;height:16px"></i>
          </button>
        </div>
      </template>
    </section>

    <Modal v-model="showQrModal" title="Conectar WhatsApp">
      <div v-if="qrLoading" class="qr-loading">
        <div class="spinner"></div>
        <p class="loading-text">Generando QR…</p>
        <p class="loading-sub">Esto toma unos segundos.</p>
      </div>
      <div v-else-if="qrData?.qr_code && !qrData.qr_code.startsWith('error')" class="qr-wrap">
        <img v-if="qrData.qr_code.startsWith('data:')" :src="qrData.qr_code" />
        <img v-else :src="'data:image/png;base64,' + qrData.qr_code" />
        <p class="hint">Escanea con tu WhatsApp (Configuración → Dispositivos vinculados).</p>
        <p class="status">Estado: <strong>{{ qrData.status }}</strong></p>
        <button @click="refreshQr" class="btn btn-ghost btn-sm" :disabled="qrRefreshing">
          <i data-lucide="refresh-ccw" style="width:14px;height:14px"></i>
          {{ qrRefreshing ? 'Actualizando…' : 'Actualizar' }}
        </button>
      </div>
      <div v-else class="qr-error">
        <i data-lucide="alert-triangle" style="width:32px;height:32px;color:var(--warning)"></i>
        <p>No se pudo generar el QR.</p>
        <p class="err-detail">{{ qrData?.qr_code || qrData?.error || 'Error desconocido' }}</p>
        <button @click="refreshQr" class="btn btn-ghost btn-sm">Reintentar</button>
      </div>
    </Modal>

    <Modal v-model="showNewConv" title="Nueva conversación">
      <div v-if="!activeSession || activeSession.status !== 'connected'" class="warn">
        Conecta una sesión de WhatsApp antes de iniciar conversaciones.
      </div>
      <template v-else>
        <label>Buscar contacto</label>
        <input v-model="contactQuery" @input="searchContacts" placeholder="Nombre, empresa, email, teléfono…" style="margin-bottom:0.6rem" />

        <div v-if="contactResults.length" class="contact-list">
          <div v-for="c in contactResults" :key="c.id"
            class="contact-row"
            :class="{ active: pickedContact?.id === c.id }"
            @click="pickContact(c)">
            <div class="avatar">{{ (c.name || '?')[0].toUpperCase() }}</div>
            <div class="info">
              <div class="name">{{ c.name }}</div>
              <div class="sub">{{ c.phone || 'sin teléfono' }} · {{ c.company || c.email || '' }}</div>
            </div>
          </div>
        </div>
        <div v-else-if="contactQuery" class="empty">Sin resultados.</div>

        <div class="divider">o teléfono manual</div>
        <FormField v-model="manualPhone" label="Número (con código de país, sin +)" placeholder="5215512345678" />
        <FormField v-model="newConvText" label="Mensaje" type="textarea" :rows="4" placeholder="Hola, te escribo de..." required />

        <p v-if="newConvError" class="error-msg">{{ newConvError }}</p>
      </template>

      <template #footer>
        <button @click="showNewConv = false" class="btn btn-ghost">Cancelar</button>
        <button @click="startConversation" class="btn btn-primary" :disabled="newConvSending || !canStartConv">
          <i data-lucide="send" style="width:14px;height:14px"></i>
          {{ newConvSending ? 'Enviando…' : 'Iniciar' }}
        </button>
      </template>
    </Modal>

    <Modal v-model="showMerge" title="Fusionar conversaciones duplicadas">
      <p class="hint-text">
        Selecciona la conversación con la que quieres fusionar. Todos los mensajes de la
        conversación actual se moverán a la seleccionada y esta se eliminará.
      </p>
      <div class="dup-list">
        <div v-for="d in duplicates" :key="d.id" class="dup-row" @click="mergeInto(d)">
          <div class="avatar">{{ (d.contact_name || '?')[0].toUpperCase() }}</div>
          <div class="info">
            <div class="name">{{ d.contact_name }}</div>
            <div class="sub">{{ d.contact_phone }} · {{ d.remote_jid?.includes('@lid') ? 'LID' : 'PN' }}</div>
          </div>
          <i data-lucide="chevron-right" style="width:16px;height:16px;color:var(--text3)"></i>
        </div>
      </div>
      <template #footer>
        <button @click="showMerge = false" class="btn btn-ghost">Cancelar</button>
      </template>
    </Modal>

    <Modal v-model="showLinkContact" title="Vincular contacto al chat">
      <p class="hint-text">
        Este chat usa privacidad LID de WhatsApp. Agrega el número telefónico real para poder responder.
      </p>
      <FormField v-model="linkPhone" label="Número (con código de país, sin +)" placeholder="5215512345678" required />
      <FormField v-model="linkName" label="Nombre (opcional)" placeholder="Cómo quieres llamarlo" />
      <p v-if="linkError" class="error-msg">{{ linkError }}</p>
      <template #footer>
        <button @click="showLinkContact = false" class="btn btn-ghost" :disabled="linkSaving">Cancelar</button>
        <button type="button" @click="saveLinkContact" class="btn btn-primary" :disabled="linkSaving">
          {{ linkSaving ? 'Guardando…' : 'Vincular y continuar' }}
        </button>
      </template>
    </Modal>

    <Modal v-model="showTemplates" title="Insertar plantilla de soporte">
      <div class="tpl-list">
        <div v-for="t in supportTemplates" :key="t.id" class="tpl-item" @click="pickTemplate(t)">
          <div class="tpl-name">{{ t.name }}</div>
          <div class="tpl-desc">{{ t.description }}</div>
        </div>
        <div v-if="!supportTemplates.length" class="empty">Crea plantillas en la sección de Plantillas.</div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api/index.js'
import Modal from '../components/Modal.vue'
import FormField from '../components/FormField.vue'

const route = useRoute()
const router = useRouter()

const sessions = ref([])
const conversations = ref([])
const messages = ref([])
const supportTemplates = ref([])
const activeSession = ref(null)
const activeConv = ref(null)
const draft = ref('')
const showQrModal = ref(false)
const qrData = ref(null)
const qrLoading = ref(false)
const qrRefreshing = ref(false)
const creatingSession = ref(false)
const syncingId = ref(null)
const showTemplates = ref(false)
const msgsRef = ref(null)
let ws = null

// New-conversation state
const showNewConv = ref(false)
const contactQuery = ref('')
const contactResults = ref([])
const pickedContact = ref(null)
const manualPhone = ref('')
const newConvText = ref('')
const newConvSending = ref(false)
const newConvError = ref('')
let searchTimer = null

const canStartConv = computed(() =>
  !!newConvText.value && (!!pickedContact.value || !!manualPhone.value)
)
// Tracks conversation IDs whose last outbound send failed with a LID-privacy
// rejection. We only show the "link real number" button for those — a blanket
// warning on every @lid chat was noise under Evolution v1.8 (almost all chats
// are @lid by default there).
const lidFailedIds = ref(new Set())
const needsLinkPrompt = computed(() => {
  const c = activeConv.value
  return !!c && lidFailedIds.value.has(c.id) && !c.contact_id
})
const isGroup = computed(() => !!activeConv.value?.remote_jid?.endsWith('@g.us'))

// Deterministic per-author color (hash → HSL) so each participant's name
// stays the same color through the thread, like WhatsApp Web.
function authorColor(name) {
  if (!name) return 'var(--text2)'
  let h = 0
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffff
  return `hsl(${h % 360}, 70%, 65%)`
}

// Auth token piggy-backed on media URLs so <img>/<audio>/<video> tags load
// directly without a custom fetcher. Mirrors the ws?token= pattern.
const authToken = computed(() => sessionStorage.getItem('hubos_token') || localStorage.getItem('hubos_token') || '')
function mediaUrl(msgId) {
  return `/api/chat/messages/${msgId}/media?token=${encodeURIComponent(authToken.value)}`
}
function openMedia(m) {
  window.open(mediaUrl(m.id), '_blank', 'noopener')
}
// Auto-placeholders we inject for empty media bodies — hide them in the UI
// (the actual media tag already conveys what the message is).
const MEDIA_PLACEHOLDERS = new Set([
  '[Imagen]', '[Video]', '[Audio]', '[Nota de voz]', '[Sticker]',
  '[Documento]', '[Contacto]', '[Contactos]', '[Ubicación]',
])
function bodyToShow(m) {
  if (!m.body) return ''
  if (m.media_type && MEDIA_PLACEHOLDERS.has(m.body.trim())) return ''
  return m.body
}

// Typing indicator — peer side, keyed by conv id. Cleared on timeout so the
// bubble disappears if the final "paused" event never arrives.
const peerTypingByConv = ref({})
const peerTyping = computed(() => {
  const c = activeConv.value
  return !!c && peerTypingByConv.value[c.id]
})
let peerTypingTimer = null
function setPeerTyping(convId, active) {
  if (active) {
    peerTypingByConv.value = { ...peerTypingByConv.value, [convId]: true }
    clearTimeout(peerTypingTimer)
    // WhatsApp re-fires `composing` every few seconds; give it 8s to decay.
    peerTypingTimer = setTimeout(() => setPeerTyping(convId, false), 8000)
  } else {
    const copy = { ...peerTypingByConv.value }
    delete copy[convId]
    peerTypingByConv.value = copy
  }
}

// Outbound typing throttle — hit the backend at most every 2s while we're
// actively typing. Keeps the other end's "escribiendo…" indicator alive.
let lastPresenceSent = 0
function broadcastTyping() {
  const now = Date.now()
  if (!activeConv.value || now - lastPresenceSent < 2000) return
  lastPresenceSent = now
  api.post('/chat/presence', {
    conversation_id: activeConv.value.id,
    presence: 'composing',
  }).catch(() => {})
}

const duplicates = ref([])
const showMerge = ref(false)

async function loadDuplicates() {
  if (!activeConv.value) { duplicates.value = []; return }
  try {
    const { data } = await api.get(`/chat/conversations/${activeConv.value.id}/duplicates`)
    duplicates.value = data
  } catch { duplicates.value = [] }
}

function openMerge() {
  showMerge.value = true
}

async function mergeInto(target) {
  if (!confirm(`Fusionar mensajes actuales hacia ${target.contact_name}?`)) return
  try {
    await api.post(`/chat/conversations/${activeConv.value.id}/merge-into/${target.id}`)
    showMerge.value = false
    await selectSession(activeSession.value)
    const fresh = conversations.value.find(c => c.id === target.id)
    if (fresh) await selectConv(fresh)
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al fusionar')
  }
}

const showLinkContact = ref(false)
const linkPhone = ref('')
const linkName = ref('')
const linkError = ref('')
const linkSaving = ref(false)

function openLinkContact() {
  linkPhone.value = ''
  linkName.value = activeConv.value?.contact_name || ''
  linkError.value = ''
  showLinkContact.value = true
}

async function saveLinkContact() {
  console.log('[linkContact] submit', { phone: linkPhone.value, name: linkName.value, convId: activeConv.value?.id })
  linkError.value = ''
  if (!activeConv.value) { linkError.value = 'No hay conversación activa'; return }
  const clean = (linkPhone.value || '').replace(/\D+/g, '')
  if (!clean) { linkError.value = 'Captura un número con código de país (ej: 5215512345678)'; return }
  linkSaving.value = true
  try {
    const { data } = await api.post(`/chat/conversations/${activeConv.value.id}/link-contact`, {
      phone: clean,
      name: linkName.value,
    })
    const fresh = data.conversation
    const idx = conversations.value.findIndex(c => c.id === fresh.id)
    if (idx >= 0) conversations.value[idx] = fresh
    activeConv.value = fresh
    lidFailedIds.value.delete(fresh.id)
    showLinkContact.value = false
    // If a pending message was kept, auto-retry send now.
    if (draft.value) send()
  } catch (e) {
    console.error('[linkContact] error', e)
    linkError.value = e.response?.data?.detail || e.message || 'Error al vincular'
  } finally {
    linkSaving.value = false
  }
}

// Refresh icons whenever modals open (they mount new DOM subtrees).
watch([showQrModal, showNewConv, showTemplates], () => refreshIcons())

async function loadSessions() {
  const { data } = await api.get('/chat/sessions')
  sessions.value = data
  // Re-bind activeSession to the fresh reference (status may have updated server-side).
  if (activeSession.value) {
    const fresh = data.find(s => s.id === activeSession.value.id)
    if (fresh) activeSession.value = fresh
    else activeSession.value = data[0] || null
  } else if (data.length) {
    selectSession(data[0])
  }
  refreshIcons()
}

// Auto-poll session status every 10s so "Conectado" updates even if
// webhook CONNECTION_UPDATE didn't arrive in time.
let sessionPoll = null
function startSessionPoll() {
  if (sessionPoll) return
  sessionPoll = setInterval(() => {
    if (!document.hidden) loadSessions()
  }, 10000)
}

async function selectSession(s) {
  activeSession.value = s
  // Filter conversations to only those belonging to this session.
  const { data } = await api.get('/chat/conversations', { params: { session_id: s.id } })
  conversations.value = data
  // If a different session is selected, deselect the open conv (stale session)
  if (activeConv.value && activeConv.value.session_id !== s.id) {
    activeConv.value = null
    messages.value = []
  }
  // Auto-import chats if this is a connected session with no conversations yet.
  // Baileys populates its store for tens of seconds after pairing, so firing a
  // sync on entry catches chats that weren't ready during the last wave.
  if (s.status === 'connected' && !data.length && syncingId.value !== s.id) {
    backgroundSync(s)
  }
}

async function backgroundSync(s) {
  if (syncingId.value) return
  syncingId.value = s.id
  try {
    await api.post(`/chat/sessions/${s.id}/sync-chats`)
    const { data } = await api.get('/chat/conversations', { params: { session_id: s.id } })
    conversations.value = data
  } catch {} finally {
    syncingId.value = null
  }
}

async function openChatForContact(contactId) {
  // Called when arriving at /chat?contact=ID from Contacts view.
  // If a conv for this contact already exists, open it. Else open new-conv modal prefilled.
  const { data: contactData } = await api.get('/contacts/', { params: { limit: 500 } })
  const c = contactData.find(x => x.id === Number(contactId))
  if (!c) return
  // Look for existing conv by phone.
  const clean = (c.phone || '').replace(/\D+/g, '')
  const match = conversations.value.find(cv => (cv.contact_phone || '') === clean)
  if (match) {
    await selectConv(match)
    return
  }
  // No existing conv — open the new-conv modal with this contact preselected.
  openNewConv()
  pickedContact.value = c
  newConvText.value = ''
}

async function selectConv(c) {
  activeConv.value = c
  const { data } = await api.get(`/chat/conversations/${c.id}/messages`)
  messages.value = data
  c.unread = 0
  await nextTick()
  scrollBottom()
  loadDuplicates()
  refreshIcons()
}

async function send() {
  if (!draft.value || !activeConv.value) return
  const text = draft.value
  draft.value = ''
  try {
    const { data } = await api.post('/chat/send', { conversation_id: activeConv.value.id, text })
    messages.value.push(data)
    activeConv.value.last_message = text
    await nextTick()
    scrollBottom()
  } catch (e) {
    const detail = e.response?.data?.detail || 'Error al enviar'
    // LID-privacy failures are the one case where we need the user to link a
    // real number before we can send. Mark this conv so the "vincular" button
    // surfaces, then auto-open the modal.
    if (/LID|privacidad/i.test(detail)) {
      lidFailedIds.value.add(activeConv.value.id)
      draft.value = text
      openLinkContact()
      return
    }
    alert(detail)
    draft.value = text
  }
}

async function createSession() {
  if (creatingSession.value) return   // guard double-click
  creatingSession.value = true
  qrData.value = null
  qrLoading.value = true
  showQrModal.value = true
  try {
    const { data } = await api.post('/chat/sessions', { display_name: '' })
    await loadSessions()
    qrData.value = { qr_code: data.qr_code, status: data.status }
  } catch (e) {
    qrData.value = { qr_code: '', error: e.response?.data?.detail || 'Error al crear sesión' }
  } finally {
    qrLoading.value = false
    creatingSession.value = false
  }
}

async function showQr(s) {
  activeSession.value = s   // track which session's QR we're showing (for refreshQr)
  qrData.value = null
  qrLoading.value = true
  showQrModal.value = true
  try {
    const { data } = await api.get(`/chat/sessions/${s.id}/qr`)
    qrData.value = data
  } catch (e) {
    if (e.response?.status === 404) {
      // Session got wiped (backend boot wipe or logout). Refresh list.
      showQrModal.value = false
      await loadSessions()
      alert('Esa sesión ya no existe (fue limpiada). Crea una nueva desde "+" .')
    } else {
      qrData.value = { qr_code: '', error: e.response?.data?.detail || 'Error' }
    }
  } finally {
    qrLoading.value = false
  }
}
async function refreshQr() {
  if (!activeSession.value || qrRefreshing.value) return
  qrRefreshing.value = true
  try {
    const { data } = await api.get(`/chat/sessions/${activeSession.value.id}/qr`)
    qrData.value = data
  } catch (e) {
    if (e.response?.status === 404) {
      showQrModal.value = false
      await loadSessions()
      alert('Sesión no encontrada. Lista actualizada.')
    } else {
      qrData.value = { qr_code: '', error: e.response?.data?.detail || 'Error al actualizar' }
    }
  } finally {
    qrRefreshing.value = false
  }
}

async function syncChats(s) {
  if (syncingId.value) return
  syncingId.value = s.id
  try {
    const { data } = await api.post(`/chat/sessions/${s.id}/sync-chats`)
    await selectSession(s)  // reload conversations
    alert(`Importado: ${data.imported} chats nuevos, ${data.updated} actualizados, ${data.contacts_imported} contactos CRM.`)
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al sincronizar')
  } finally {
    syncingId.value = null
  }
}

async function removeSession(s) {
  if (!confirm('¿Eliminar sesión?')) return
  await api.delete(`/chat/sessions/${s.id}`)
  await loadSessions()
}

async function loadSupportTemplates() {
  const { data } = await api.get('/templates/', { params: { category: 'support' } })
  supportTemplates.value = data
}

function openNewConv() {
  pickedContact.value = null
  manualPhone.value = ''
  newConvText.value = ''
  newConvError.value = ''
  contactQuery.value = ''
  contactResults.value = []
  showNewConv.value = true
  loadInitialContacts()
}

async function loadInitialContacts() {
  const { data } = await api.get('/contacts/', { params: { limit: 20 } })
  contactResults.value = data
}

function searchContacts() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    if (!contactQuery.value) { loadInitialContacts(); return }
    const { data } = await api.get('/contacts/', { params: { q: contactQuery.value, limit: 20 } })
    contactResults.value = data
  }, 200)
}

function pickContact(c) {
  pickedContact.value = c
  manualPhone.value = ''
}

async function startConversation() {
  if (!canStartConv.value || !activeSession.value) return
  newConvError.value = ''
  newConvSending.value = true
  try {
    const body = {
      session_id: activeSession.value.id,
      text: newConvText.value,
    }
    if (pickedContact.value) body.contact_id = pickedContact.value.id
    else {
      body.phone = manualPhone.value
      body.contact_name = ''
    }
    const { data } = await api.post('/chat/conversations/start', body)
    showNewConv.value = false
    // Refresh conversations + open the new one
    await selectSession(activeSession.value)
    const conv = conversations.value.find(c => c.id === data.conversation.id) || data.conversation
    await selectConv(conv)
  } catch (e) {
    newConvError.value = e.response?.data?.detail || 'Error al iniciar conversación'
  } finally {
    newConvSending.value = false
  }
}

function pickTemplate(t) {
  const text = (t.blocks || []).filter(b => b.type === 'text' || b.type === 'heading').map(b => b.content).join('\n\n')
  draft.value = text
  showTemplates.value = false
}

function fmtTime(iso) { return iso ? new Date(iso).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }) : '' }
function relTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const now = new Date()
  const diff = (now - d) / 1000
  if (diff < 60) return 'ahora'
  if (diff < 3600) return `${Math.floor(diff/60)}m`
  if (diff < 86400) return `${Math.floor(diff/3600)}h`
  return d.toLocaleDateString('es-MX')
}
function scrollBottom() {
  if (msgsRef.value) msgsRef.value.scrollTop = msgsRef.value.scrollHeight
}

function connectWs() {
  // Auth token lives in sessionStorage (see api/index.js, router/index.js,
  // stores/auth.js). This was reading from localStorage and silently
  // returning, so the WebSocket never opened — which is why inbound messages
  // never pushed live and the app felt like it required a page refresh.
  const token = sessionStorage.getItem('hubos_token') || localStorage.getItem('hubos_token')
  if (!token) return
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  ws = new WebSocket(`${proto}://${location.host}/api/chat/ws?token=${token}`)
  ws.onmessage = (ev) => {
    try {
      const m = JSON.parse(ev.data)
      if (m.type === 'message' && activeConv.value?.id === m.conversation_id) {
        messages.value.push(m.message)
        nextTick(scrollBottom)
      }
      // bump conversations list
      if (m.type === 'message') {
        const conv = conversations.value.find(c => c.id === m.conversation_id)
        if (conv) {
          conv.last_message = m.message.body
          conv.last_message_at = m.message.timestamp
          if (activeConv.value?.id !== conv.id && !m.message.from_me) conv.unread = (conv.unread || 0) + 1
        }
        // Arrival of an actual message supersedes the typing indicator.
        setPeerTyping(m.conversation_id, false)
      }
      if (m.type === 'presence') {
        setPeerTyping(m.conversation_id, m.state === 'composing' || m.state === 'recording')
      }
    } catch {}
  }
  ws.onclose = () => { setTimeout(connectWs, 3000) }
}

function refreshIcons() {
  // Defer to next tick so Vue finishes DOM work before lucide mutates it.
  nextTick(() => { if (window.lucide) window.lucide.createIcons() })
}

onMounted(async () => {
  await loadSessions()
  await loadSupportTemplates()
  connectWs()
  startSessionPoll()
  // Deep-link: /chat?contact=ID
  if (route.query.contact) {
    await openChatForContact(route.query.contact)
    // Clear query so refresh doesn't retrigger
    router.replace({ path: '/chat' })
  }
  refreshIcons()
})

// React to inter-route nav like clicking Chat from another page with query param
watch(() => route.query.contact, async (id) => {
  if (id) {
    await openChatForContact(id)
    router.replace({ path: '/chat' })
  }
})
onUnmounted(() => {
  if (ws) ws.close()
  if (sessionPoll) clearInterval(sessionPoll)
})
</script>

<style scoped>
.chat-shell {
  display: grid;
  grid-template-columns: 240px 320px 1fr;
  height: 100vh;
  background: var(--bg);
}
@media (max-width: 960px) {
  .chat-shell { grid-template-columns: 1fr; }
  .sessions-bar, .conv-list { display: none; }
}

.sessions-bar, .conv-list {
  border-right: 1px solid var(--border);
  background: var(--bg2);
  overflow-y: auto;
}
.sb-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}
.sb-head h3 { font-size: 0.85rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text2); }

.sessions, .conv-list { padding: 0.5rem 0; }
.session, .conv {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.7rem 0.9rem;
  cursor: pointer;
  border-left: 2px solid transparent;
}
.session:hover, .conv:hover { background: rgba(255,255,255,0.02); }
.session.active, .conv.active { background: rgba(99,102,241,0.08); border-left-color: var(--primary); }
.dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-connected { background: var(--success); }
.dot-disconnected { background: var(--text3); }
.dot-connecting, .dot-error { background: var(--warning); }

.info { flex: 1; min-width: 0; }
.name { font-size: 0.85rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.phone { font-size: 0.7rem; color: var(--text3); }
.mini {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.mini:hover { color: var(--text); border-color: var(--primary); }
.mini.danger:hover { color: var(--danger); border-color: var(--danger); }

.avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  flex-shrink: 0;
}

.conv .row1 { display: flex; justify-content: space-between; align-items: center; }
.conv .time { font-size: 0.7rem; color: var(--text3); }
.conv .row2 { display: flex; justify-content: space-between; align-items: center; margin-top: 0.15rem; }
.conv .last { font-size: 0.75rem; color: var(--text2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }
.unread { background: var(--primary); color: white; font-size: 0.7rem; font-weight: 700; padding: 1px 7px; border-radius: 10px; }

.messages-panel {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg);
}
.placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  color: var(--text3);
}

.msg-head {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg2);
}
.msg-head .name { font-size: 0.95rem; font-weight: 600; }
.msg-head .phone { font-size: 0.75rem; color: var(--text3); }
.lid-warn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.7rem;
  background: rgba(245,158,11,0.15);
  color: var(--warning);
  border: 1px solid rgba(245,158,11,0.3);
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.15s;
}
.lid-warn:hover { background: rgba(245,158,11,0.25); border-color: rgba(245,158,11,0.5); }
.dup-warn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.7rem;
  background: rgba(99,102,241,0.15);
  color: #a5b4fc;
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.15s;
  margin-left: 0.4rem;
}
.dup-warn:hover { background: rgba(99,102,241,0.25); }
.dup-list { display: flex; flex-direction: column; gap: 0.4rem; }
.dup-row { display: flex; align-items: center; gap: 0.7rem; padding: 0.7rem 0.9rem; background: var(--bg3); border: 1px solid var(--border); border-radius: 10px; cursor: pointer; transition: all 0.15s; }
.dup-row:hover { border-color: var(--primary); background: rgba(99,102,241,0.08); }
.dup-row .avatar { width: 34px; height: 34px; }
.dup-row .info { flex: 1; min-width: 0; }
.dup-row .name { font-size: 0.88rem; font-weight: 600; }
.dup-row .sub { font-size: 0.72rem; color: var(--text3); }
.hint-text { color: var(--text2); font-size: 0.82rem; line-height: 1.5; margin-bottom: 0.9rem; }

.msgs {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: radial-gradient(circle at 50% 20%, rgba(99,102,241,0.03), transparent 60%), var(--bg);
}
.msg { display: flex; }
.msg.out { justify-content: flex-end; }
.bubble {
  max-width: 68%;
  padding: 0.55rem 0.85rem;
  border-radius: 14px;
  background: var(--bg3);
  border: 1px solid var(--border);
  font-size: 0.88rem;
  line-height: 1.45;
  white-space: pre-wrap;
  word-wrap: break-word;
}
.msg.out .bubble {
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  border-color: transparent;
}
.ts { font-size: 0.65rem; opacity: 0.6; text-align: right; margin-top: 0.25rem; }
.author { font-size: 0.72rem; font-weight: 700; margin-bottom: 0.15rem; letter-spacing: 0.02em; }

.bubble-media { padding: 0.3rem 0.3rem 0.35rem; }
.bubble-media .author { padding: 0.1rem 0.4rem 0; }
.bubble-media .body { padding: 0.1rem 0.5rem 0; }
.bubble-media .ts { padding: 0 0.5rem; }
.media-img {
  display: block;
  max-width: 100%;
  max-height: 340px;
  border-radius: 10px;
  cursor: zoom-in;
  object-fit: cover;
}
.media-video { display: block; max-width: 100%; max-height: 340px; border-radius: 10px; }
.media-audio { display: block; width: 260px; max-width: 100%; }
.media-doc {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255,255,255,0.06);
  border-radius: 8px;
  color: inherit;
  text-decoration: none;
  font-size: 0.85rem;
  word-break: break-all;
}
.media-doc:hover { background: rgba(255,255,255,0.12); }
.body { white-space: pre-wrap; }

/* Typing indicator — three dots staggering in a WhatsApp-style wave. */
.typing-bubble {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0.55rem 0.8rem;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 14px;
}
.typing-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--text2);
  opacity: 0.4;
  animation: typing-bounce 1.2s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.3s; }
@keyframes typing-bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-4px); opacity: 1; }
}

.composer {
  display: flex;
  gap: 0.5rem;
  padding: 0.9rem 1.25rem;
  border-top: 1px solid var(--border);
  background: var(--bg2);
}
.composer input { flex: 1; }

.qr-wrap { text-align: center; }
.qr-wrap img { max-width: 280px; margin: 0 auto; background: white; padding: 12px; border-radius: 12px; }
.qr-wrap .hint { font-size: 0.82rem; color: var(--text2); margin-top: 0.8rem; }
.qr-wrap .status { font-size: 0.82rem; margin: 0.4rem 0; }

.qr-loading, .qr-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
  padding: 2.5rem 1rem;
  text-align: center;
}
.loading-text { font-size: 0.95rem; font-weight: 600; color: var(--text); }
.loading-sub { font-size: 0.8rem; color: var(--text3); }
.err-detail { font-size: 0.75rem; color: var(--text3); word-break: break-all; max-width: 300px; }

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
.mini-spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.tpl-list { display: flex; flex-direction: column; gap: 0.5rem; }
.tpl-item { background: var(--bg3); border: 1px solid var(--border); border-radius: 9px; padding: 0.8rem; cursor: pointer; transition: all 0.15s; }
.tpl-item:hover { border-color: var(--primary); }
.tpl-name { font-weight: 600; font-size: 0.9rem; }
.tpl-desc { font-size: 0.75rem; color: var(--text2); margin-top: 0.2rem; }

.empty { color: var(--text3); text-align: center; padding: 1.5rem; font-size: 0.82rem; }

/* new conversation modal */
.warn { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); color: #f59e0b; padding: 0.7rem 0.9rem; border-radius: 8px; font-size: 0.82rem; }
.contact-list { max-height: 220px; overflow-y: auto; border: 1px solid var(--border); border-radius: 10px; margin-bottom: 0.8rem; }
.contact-row { display: flex; align-items: center; gap: 0.6rem; padding: 0.55rem 0.7rem; cursor: pointer; border-bottom: 1px solid var(--border); transition: background 0.15s; }
.contact-row:last-child { border-bottom: none; }
.contact-row:hover { background: rgba(255,255,255,0.03); }
.contact-row.active { background: rgba(99,102,241,0.15); }
.contact-row .avatar { width: 32px; height: 32px; font-size: 0.8rem; }
.contact-row .info { flex: 1; min-width: 0; }
.contact-row .name { font-size: 0.85rem; font-weight: 600; }
.contact-row .sub { font-size: 0.72rem; color: var(--text3); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.divider { text-align: center; color: var(--text3); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; margin: 0.9rem 0 0.6rem; }
.error-msg { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #ef4444; padding: 0.55rem 0.8rem; border-radius: 8px; font-size: 0.8rem; margin-top: 0.6rem; }
</style>
