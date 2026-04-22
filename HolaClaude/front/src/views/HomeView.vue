<template>
  <WavesCanvas />

  <div class="layout">
    <header class="top">
      <div class="brand">
        <i class="mdi mdi-wave"></i>
        <span>HolaClaude</span>
      </div>
      <div class="meta mono">
        <span class="badge" :class="{ ok: status.enrolled, warn: !status.enrolled }">
          {{ status.enrolled ? 'owner enrolado' : 'sin enrolar' }}
        </span>
        <span v-if="status.disabled" class="badge danger">deshabilitado</span>
        <span v-if="session.token" class="badge ok">sesión activa</span>
      </div>
    </header>

    <main class="main">
      <section class="card stage">
        <CameraPanel ref="cam" :paused-gestures="gesturesPaused" @gesture="onGesture" @blink="onBlink" />
        <div class="stage-text">
          <h1 class="mono">{{ headline }}</h1>
          <p class="muted">{{ subline }}</p>
          <div class="row wrap" style="margin-top: 14px;">
            <button v-if="!status.enrolled" @click="doEnroll" :disabled="busy">
              <i class="mdi mdi-account-plus"></i> Enrolar mi rostro
            </button>
            <button v-else-if="!session.token" @click="doVerify" :disabled="busy || status.disabled">
              <i class="mdi mdi-fingerprint"></i> Verificar rostro
            </button>
            <button v-if="verifying" @click="cancelVerify" class="ghost">
              <i class="mdi mdi-close"></i> Cancelar
            </button>
            <button @click="gesturesPaused = !gesturesPaused" class="ghost">
              <i :class="gesturesPaused ? 'mdi mdi-play' : 'mdi mdi-pause'"></i>
              {{ gesturesPaused ? 'Reanudar gestos' : 'Pausar gestos' }}
            </button>
            <button @click="testSpeak" class="ghost">
              <i class="mdi mdi-volume-high"></i> Probar voz
            </button>
            <button v-if="status.enrolled" @click="showPinDialog = true" class="ghost">
              <i class="mdi mdi-lock"></i> PIN
            </button>
          </div>
          <p v-if="msg" class="muted" style="margin-top: 8px;">{{ msg }}</p>
        </div>
      </section>

      <section class="card chat" v-if="session.token">
        <div class="chat-head">
          <i class="mdi mdi-robot-outline"></i>
          <span>Canal Claude CLI</span>
          <span class="spacer"></span>
          <button class="ghost small" @click="toggleVoice">
            <i :class="voice.listening ? 'mdi mdi-microphone-off' : 'mdi mdi-microphone'"></i>
            {{ voice.listening ? 'apagar mic' : 'prender mic' }}
          </button>
        </div>
        <VoiceWave :active="voice.listening" :transcript="voiceTranscript" :interim="voiceInterim" />
        <div class="chat-body" ref="chatBody">
          <div v-for="(m, i) in session.messages" :key="i" class="msg" :class="m.role">
            <strong>{{ m.role === 'me' ? 'tu' : 'claude' }}:</strong>
            <pre>{{ m.text }}</pre>
          </div>
          <div v-if="thinking" class="msg claude"><em class="muted">pensando…</em></div>
        </div>
        <form class="chat-form" @submit.prevent="sendText">
          <input v-model="draft" placeholder="habla o escribe. di 'hola claude' para activar voz." :disabled="thinking" />
          <button type="submit" :disabled="!draft.trim() || thinking">
            <i class="mdi mdi-send"></i>
          </button>
        </form>
      </section>

      <section class="card gestures" v-if="gestures.length">
        <h3><i class="mdi mdi-hand-wave"></i> Gestos activos</h3>
        <ul class="g-list">
          <li v-for="g in gestures" :key="g.gesture" class="mono">
            <span class="tag">{{ g.gesture }}</span> → {{ g.action }}<span v-if="g.label"> ({{ g.label }})</span>
          </li>
        </ul>
        <p class="muted">editar: <code>artifacts/gestures.json</code></p>
      </section>
    </main>
  </div>

  <PinDialog v-if="showPinDialog" @close="showPinDialog = false" @disable="onDisable" @reset="onReset" />
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue';
import WavesCanvas from '../components/WavesCanvas.vue';
import CameraPanel from '../components/CameraPanel.vue';
import PinDialog from '../components/PinDialog.vue';
import VoiceWave from '../components/VoiceWave.vue';
import { useSession } from '../stores/session';
import * as api from '../api/holaclaude.js';

const session = useSession();
const cam = ref(null);
const chatBody = ref(null);
const status = ref({ enrolled: false, disabled: false, locked_out: false });
const busy = ref(false);
const msg = ref('');
const showPinDialog = ref(false);
const draft = ref('');
const thinking = ref(false);
const headline = ref('HolaClaude');
const subline = ref('waves + cámara + voz. primer rostro queda dueño.');
const gestures = ref([]);
const gesturesPaused = ref(false);
const verifying = ref(false);
let ws = null;
let wakeDetected = false;
let verifyCancelled = false;
let ttsVoice = null;

const voice = ref({ listening: false, rec: null });
const voiceTranscript = ref('');
const voiceInterim = ref('');

function pickVoice() {
  if (!('speechSynthesis' in window)) return null;
  const voices = speechSynthesis.getVoices();
  return voices.find(v => /es-MX/i.test(v.lang))
      || voices.find(v => /es-US|es-419/i.test(v.lang))
      || voices.find(v => /^es/i.test(v.lang))
      || voices[0] || null;
}

if ('speechSynthesis' in window) {
  speechSynthesis.onvoiceschanged = () => { ttsVoice = pickVoice(); };
}

async function refreshStatus() {
  try { status.value = await api.getStatus(); } catch {}
}

async function refreshGestures() {
  try { gestures.value = await api.fetchGestures(); } catch { gestures.value = []; }
}

async function doEnroll() {
  busy.value = true;
  try {
    const d = cam.value?.captureDescriptor();
    if (!d) { msg.value = 'no se detectó rostro, acércate a la cámara'; speak('no detecté tu rostro, acércate'); return; }
    const r = await api.enrollFace(d);
    if (r.ok) {
      msg.value = 'enrolado correctamente — ya eres dueño';
      speak('listo, estás enrolado. ahora verifica parpadeando una vez.');
    } else {
      msg.value = 'error enrolando';
    }
    await refreshStatus();
  } catch (e) {
    msg.value = (e.response?.data?.detail) || e.message;
    speak('no pude enrolarte');
  }
  finally { busy.value = false; }
}

function cancelVerify() {
  verifyCancelled = true;
  verifying.value = false;
  busy.value = false;
  msg.value = 'verificación cancelada';
}

async function doVerify() {
  busy.value = true;
  verifying.value = true;
  verifyCancelled = false;
  try {
    msg.value = 'buscando tu rostro...';
    let d = cam.value?.captureDescriptor();
    const t0 = Date.now();
    while (!d && Date.now() - t0 < 5000) {
      if (verifyCancelled) throw new Error('cancelado');
      await new Promise(r => setTimeout(r, 200));
      d = cam.value?.captureDescriptor();
    }
    if (!d) throw new Error('no detecté rostro, acércate a la cámara');
    const r = await api.verifyFace(d, 0);
    if (r.ok) {
      session.setToken(r.token);
      msg.value = 'verificado';
      speak('verificado, canal Claude listo');
      openWs();
    }
  } catch (e) {
    msg.value = (e.response?.data?.detail) || e.message;
    speak('no pude verificarte');
  }
  finally {
    busy.value = false;
    verifying.value = false;
  }
}

function testSpeak() {
  if (!ttsVoice) ttsVoice = pickVoice();
  speak('hola, soy Claude. te escucho y te respondo con voz.');
}

async function onDisable(pin) {
  try {
    await api.disableWithPin(pin);
    session.clearToken();
    await refreshStatus();
    msg.value = 'sesión deshabilitada';
    showPinDialog.value = false;
  } catch (e) { msg.value = e.response?.data?.detail || e.message; }
}

async function onReset(pin) {
  try {
    const d = cam.value?.captureDescriptor();
    if (!d) throw new Error('sin rostro para reenrolar');
    await api.resetWithPin(pin, d);
    await refreshStatus();
    msg.value = 'reenrolado con PIN';
    showPinDialog.value = false;
  } catch (e) { msg.value = e.response?.data?.detail || e.message; }
}

function openWs() {
  if (ws) ws.close();
  ws = api.openAgentWs(session.token, (m) => {
    if (m.type === 'thinking') thinking.value = true;
    else if (m.type === 'reply') {
      thinking.value = false;
      const text = m.stdout || m.error || '(sin respuesta)';
      session.addMessage({ role: 'claude', text });
      speak(text.slice(0, 220));
      scrollChat();
    } else if (m.type === 'ready') {
      session.addMessage({ role: 'claude', text: 'canal listo. di "hola claude" seguido de tu mensaje.' });
    }
  });
}

function sendText() {
  const t = draft.value.trim();
  if (!t || !ws) return;
  session.addMessage({ role: 'me', text: t });
  ws.send(JSON.stringify({ type: 'text', text: t }));
  draft.value = '';
  scrollChat();
}

function scrollChat() {
  nextTick(() => { if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight; });
}

function speak(text) {
  if (!('speechSynthesis' in window) || !text) return;
  try { speechSynthesis.cancel(); } catch {}
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'es-MX';
  u.rate = 1.03;
  u.pitch = 1.0;
  if (!ttsVoice) ttsVoice = pickVoice();
  if (ttsVoice) u.voice = ttsVoice;
  speechSynthesis.speak(u);
}

function toggleVoice() { voice.value.listening ? stopVoice() : startVoice(); }

function startVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { msg.value = 'tu browser no soporta Web Speech API — usa Chrome o Edge'; speak('tu navegador no soporta reconocimiento de voz'); return; }
  const rec = new SR();
  rec.lang = 'es-MX';
  rec.continuous = true;
  rec.interimResults = true;
  rec.onresult = (e) => {
    let interim = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const res = e.results[i];
      const t = res[0].transcript.trim();
      if (res.isFinal) {
        voiceTranscript.value = t;
        voiceInterim.value = '';
        const tl = t.toLowerCase();
        if (!wakeDetected && /hola\s+claude/.test(tl)) {
          wakeDetected = true;
          const cmd = tl.replace(/.*hola\s+claude[\s,.:]*/i, '').trim();
          if (cmd) {
            draft.value = cmd; sendText(); wakeDetected = false;
          } else {
            speak('te escucho');
          }
        } else if (wakeDetected) {
          draft.value = t; sendText(); wakeDetected = false;
        }
      } else {
        interim += t + ' ';
      }
    }
    voiceInterim.value = interim.trim();
  };
  rec.onerror = (e) => {
    msg.value = 'error mic: ' + (e.error || 'desconocido');
    voice.value.listening = false;
  };
  rec.onend = () => { if (voice.value.listening) { try { rec.start(); } catch {} } };
  try { rec.start(); } catch (e) { msg.value = 'no pude iniciar mic: ' + e.message; return; }
  voice.value.rec = rec;
  voice.value.listening = true;
  speak('micrófono encendido, di hola claude seguido de tu mensaje');
}

function stopVoice() {
  voice.value.listening = false;
  try { voice.value.rec?.stop(); } catch {}
  voiceInterim.value = '';
}

function onGesture(g) {
  const item = gestures.value.find(x => x.gesture === g);
  if (!item) return;
  session.addMessage({ role: 'me', text: `[gesto: ${g}]` });
  if (item.action === 'redirect' && item.url) {
    setTimeout(() => { window.open(item.url, '_blank'); }, 300);
  } else if (item.action === 'greet') {
    const text = item.say || 'hola';
    session.addMessage({ role: 'claude', text });
    speak(text);
  } else if (item.action === 'confirm') {
    if (draft.value.trim()) sendText();
  } else if (item.action === 'cancel') {
    draft.value = '';
  }
}

function onBlink(n) {
  if (verifying.value) {
    const beep = new Audio('data:audio/wav;base64,UklGRkQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YSAAAAB/f39/f39/f39/f39/f39/f39/f39/f39/f39/f39/f39/');
    beep.volume = 0.2;
    beep.play().catch(() => {});
  }
}

onMounted(async () => {
  await refreshStatus();
  await refreshGestures();
});
</script>

<style scoped>
.layout { position: relative; z-index: 1; height: 100%; display: flex; flex-direction: column; padding: 18px 22px; gap: 18px; max-width: 1200px; margin: 0 auto; }
.top { display: flex; align-items: center; justify-content: space-between; }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 18px; }
.brand i { color: var(--accent); font-size: 22px; }
.meta { display: flex; gap: 8px; }
.badge { padding: 4px 10px; border-radius: 999px; font-size: 11px; background: var(--surface-2); border: 1px solid var(--border); }
.badge.ok { color: var(--ok); border-color: rgba(61,220,151,0.3); }
.badge.warn { color: #f0b860; }
.badge.danger { color: var(--danger); border-color: rgba(255,107,107,0.3); }
.main { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; overflow: auto; }
.stage { grid-column: span 2; display: flex; gap: 20px; align-items: center; }
.stage-text h1 { font-size: 22px; margin-bottom: 6px; }
.chat { display: flex; flex-direction: column; height: 420px; }
.chat-head { display: flex; gap: 8px; align-items: center; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.chat-head .spacer { flex: 1; }
.chat-body { flex: 1; overflow-y: auto; padding: 12px 0; display: flex; flex-direction: column; gap: 10px; }
.msg pre { white-space: pre-wrap; word-break: break-word; font-family: inherit; font-size: 14px; }
.msg.me { align-self: flex-end; background: var(--accent); color: #fff; padding: 8px 12px; border-radius: 12px; max-width: 80%; }
.msg.claude { align-self: flex-start; background: var(--surface-2); padding: 8px 12px; border-radius: 12px; max-width: 85%; }
.chat-form { display: flex; gap: 8px; padding-top: 10px; border-top: 1px solid var(--border); }
.chat-form input { flex: 1; }
.gestures h3 { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.g-list { list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 13px; }
.tag { background: var(--surface-2); padding: 2px 8px; border-radius: 6px; border: 1px solid var(--border); margin-right: 6px; }
.ghost { background: transparent; border-color: var(--border); }
.ghost.small { padding: 6px 10px; }
.wrap { flex-wrap: wrap; }
@media (max-width: 900px) { .main { grid-template-columns: 1fr; } .stage { grid-column: span 1; flex-direction: column; } }
</style>
