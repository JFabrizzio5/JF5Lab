<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import jsQR from 'jsqr'
import { checkinApi } from '../api/endpoints'

const video = ref(null); const canvas = ref(null); const fileInput = ref(null)
const stream = ref(null); const lastCode = ref(null); const result = ref(null); const error = ref(null)
const manualCode = ref(''); const scanning = ref(false)
const secure = typeof window !== 'undefined' && (window.isSecureContext || location.hostname === 'localhost')
const mediaOk = typeof navigator !== 'undefined' && navigator.mediaDevices?.getUserMedia
const canUseCamera = computed(() => secure && mediaOk)
let rafId = null

async function startCamera() {
  error.value = null
  if (!canUseCamera.value) { error.value = secure ? 'Navegador sin cámara. Sube imagen o escribe el código.' : 'Cámara requiere HTTPS. Sube imagen o escribe el código.'; return }
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    video.value.srcObject = stream.value; await video.value.play(); scanning.value = true; tick()
  } catch (e) { error.value = 'Cámara: ' + e.message }
}
function stopCamera() { if (rafId) cancelAnimationFrame(rafId); if (stream.value) stream.value.getTracks().forEach(t=>t.stop()); stream.value=null; scanning.value=false }
function tick() {
  if (!video.value || video.value.readyState !== 4) { rafId = requestAnimationFrame(tick); return }
  const c = canvas.value; c.width = video.value.videoWidth; c.height = video.value.videoHeight
  const ctx = c.getContext('2d'); ctx.drawImage(video.value, 0, 0, c.width, c.height)
  const img = ctx.getImageData(0, 0, c.width, c.height)
  const code = jsQR(img.data, img.width, img.height)
  if (code && code.data && code.data !== lastCode.value) handle(code.data)
  rafId = requestAnimationFrame(tick)
}
async function onFile(e) {
  const f = e.target.files?.[0]; if (!f) return
  const img = new Image()
  img.onload = () => {
    const c = canvas.value || document.createElement('canvas')
    c.width = img.width; c.height = img.height
    const ctx = c.getContext('2d'); ctx.drawImage(img, 0, 0)
    const data = ctx.getImageData(0, 0, c.width, c.height)
    const code = jsQR(data.data, data.width, data.height)
    if (code?.data) handle(code.data); else error.value = 'QR no legible.'
  }
  img.src = URL.createObjectURL(f)
}
async function handleManual() { if (manualCode.value.trim()) { await handle(manualCode.value.trim()); manualCode.value = '' } }
async function handle(code) {
  lastCode.value = code
  try { const { data } = await checkinApi.punch({ code, method: 'QR' }); result.value = { ok: true, data } }
  catch (e) { result.value = { ok: false, msg: e?.response?.data?.detail || e.message } }
}

onMounted(() => { if (canUseCamera.value) startCamera() })
onBeforeUnmount(stopCamera)
</script>

<template>
  <AppLayout>
    <div class="head"><h1>Check-in QR</h1><p class="muted">Escanea el QR del miembro o escribe su código.</p></div>
    <div class="grid-2">
      <div class="card">
        <div v-if="canUseCamera" class="cam">
          <video ref="video" playsinline muted></video>
          <canvas ref="canvas" style="display:none;"></canvas>
          <div class="overlay"></div>
        </div>
        <div v-else class="cam placeholder">
          <canvas ref="canvas" style="display:none;"></canvas>
          <i class="mdi mdi-camera-off" style="font-size:48px; opacity:.3;"></i>
          <div class="muted" style="max-width:280px; text-align:center; margin-top:10px;">Cámara no disponible. Usa upload o código manual.</div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">
          <button v-if="canUseCamera && !scanning" class="btn btn-primary" @click="startCamera"><i class="mdi mdi-camera"></i> Cámara</button>
          <button v-else-if="canUseCamera" class="btn" @click="stopCamera"><i class="mdi mdi-camera-off"></i> Pausar</button>
          <button class="btn" @click="fileInput.click()"><i class="mdi mdi-image"></i> Subir QR</button>
          <input type="file" accept="image/*" ref="fileInput" @change="onFile" style="display:none;" />
        </div>
        <div style="margin-top:14px;">
          <label>Código manual</label>
          <div style="display:flex; gap:8px;">
            <input v-model="manualCode" placeholder="PM-1024" @keyup.enter="handleManual" />
            <button class="btn btn-primary" :disabled="!manualCode" @click="handleManual"><i class="mdi mdi-send"></i></button>
          </div>
        </div>
        <p v-if="error" class="badge danger" style="margin-top:10px;">{{ error }}</p>
      </div>

      <div class="card">
        <h3 style="margin-top:0;">Último check-in</h3>
        <div v-if="!result" class="muted" style="text-align:center; padding:40px;">
          <i class="mdi mdi-qrcode-scan" style="font-size:48px; opacity:.2;"></i>
          <div style="margin-top:10px;">Escanea, sube imagen o escribe el código…</div>
        </div>
        <div v-else-if="result.ok">
          <div class="success-banner">
            <i class="mdi mdi-check-circle"></i>
            <div>
              <div style="font-weight:700;">Check-in registrado</div>
              <div class="muted" style="font-size:12px;">{{ new Date(result.data.at).toLocaleString('es-MX') }}</div>
            </div>
          </div>
          <div class="muted" style="font-size:13px; margin-top:12px;">ID: <span class="mono">{{ result.data.id }}</span></div>
          <div class="muted" style="font-size:13px;">Método: {{ result.data.method }}</div>
        </div>
        <div v-else>
          <div class="err-banner"><i class="mdi mdi-alert-circle"></i> {{ result.msg }}</div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.head h1 { font-size:30px; letter-spacing:-0.03em; font-weight:800; margin:0; }
.head { margin-bottom:24px; }
.cam { position:relative; aspect-ratio:4/3; background:#000; border-radius:14px; overflow:hidden; }
.cam.placeholder { background:var(--bg-subtle); border:2px dashed var(--border); display:grid; place-items:center; }
.cam video { width:100%; height:100%; object-fit:cover; }
.overlay { position:absolute; inset:20%; border:2px dashed rgba(255,255,255,.7); border-radius:12px; pointer-events:none; }
.success-banner { display:flex; gap:14px; align-items:center; padding:16px; background:var(--emerald-soft); border-radius:12px; color:#047857; }
.success-banner .mdi { font-size:36px; }
.err-banner { display:flex; gap:10px; align-items:center; padding:14px; background:#fee2e2; color:#b91c1c; border-radius:12px; font-size:14px; font-weight:500; }
</style>
