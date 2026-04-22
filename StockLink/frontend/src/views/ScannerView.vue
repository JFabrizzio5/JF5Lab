<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import jsQR from 'jsqr'
import { scanApi, attendanceApi } from '../api/endpoints'

const video = ref(null)
const canvas = ref(null)
const fileInput = ref(null)
const stream = ref(null)
const lastCode = ref(null)
const result = ref(null)
const error = ref(null)
const info = ref(null)
const mode = ref('inventory') // inventory | attendance
const scanning = ref(false)
const manualCode = ref('')

const secure = typeof window !== 'undefined' && (window.isSecureContext || location.hostname === 'localhost')
const mediaAvail = typeof navigator !== 'undefined' && navigator.mediaDevices && navigator.mediaDevices.getUserMedia
const canUseCamera = computed(() => secure && mediaAvail)

const nfcSupported = typeof window !== 'undefined' && 'NDEFReader' in window
const nfcActive = ref(false)

let rafId = null

async function startCamera() {
  error.value = null
  if (!canUseCamera.value) {
    error.value = secure
      ? 'Tu navegador no expone la cámara. Usa subir imagen o escribe el código.'
      : 'La cámara requiere HTTPS (o localhost). Aquí estás en HTTP. Usa subir imagen o escribe el código.'
    return
  }
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    video.value.srcObject = stream.value
    await video.value.play()
    scanning.value = true
    tick()
  } catch (e) {
    error.value = 'Cámara: ' + (e.message || e.name)
  }
}

function stopCamera() {
  if (rafId) cancelAnimationFrame(rafId)
  if (stream.value) stream.value.getTracks().forEach(t => t.stop())
  stream.value = null; scanning.value = false
}

function tick() {
  if (!video.value || video.value.readyState !== 4) { rafId = requestAnimationFrame(tick); return }
  const c = canvas.value
  c.width = video.value.videoWidth; c.height = video.value.videoHeight
  const ctx = c.getContext('2d')
  ctx.drawImage(video.value, 0, 0, c.width, c.height)
  const img = ctx.getImageData(0, 0, c.width, c.height)
  const code = jsQR(img.data, img.width, img.height)
  if (code && code.data && code.data !== lastCode.value) {
    handleCode(code.data)
  }
  rafId = requestAnimationFrame(tick)
}

async function onFileUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  error.value = null
  const img = new Image()
  img.onload = () => {
    const c = canvas.value || document.createElement('canvas')
    c.width = img.width; c.height = img.height
    const ctx = c.getContext('2d')
    ctx.drawImage(img, 0, 0)
    const data = ctx.getImageData(0, 0, c.width, c.height)
    const code = jsQR(data.data, data.width, data.height)
    if (code && code.data) handleCode(code.data)
    else error.value = 'No se encontró QR legible en la imagen.'
  }
  img.onerror = () => { error.value = 'No se pudo leer la imagen.' }
  img.src = URL.createObjectURL(file)
}

async function handleManual() {
  if (!manualCode.value.trim()) return
  await handleCode(manualCode.value.trim())
  manualCode.value = ''
}

async function handleCode(code) {
  lastCode.value = code
  info.value = null
  try {
    if (mode.value === 'attendance') {
      const { data } = await attendanceApi.punch({ code, kind: 'IN', method: 'QR' })
      result.value = { type: 'attendance', data }
    } else {
      const { data } = await scanApi.resolve(code)
      result.value = { type: 'scan', data }
    }
  } catch (e) {
    result.value = { type: 'error', message: e?.response?.data?.detail || e.message }
  }
}

async function startNFC() {
  if (!nfcSupported) return
  try {
    const ndef = new NDEFReader()
    await ndef.scan()
    nfcActive.value = true
    ndef.onreading = (ev) => {
      const uid = ev.serialNumber?.toUpperCase() || ''
      if (uid) handleCode(uid)
      for (const rec of ev.message.records) {
        if (rec.recordType === 'text') {
          const dec = new TextDecoder(rec.encoding || 'utf-8')
          handleCode(dec.decode(rec.data))
        }
      }
    }
  } catch (e) { error.value = 'NFC: ' + e.message }
}

onMounted(() => { if (canUseCamera.value) startCamera() })
onBeforeUnmount(stopCamera)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1>Escáner</h1>
        <p class="muted">Cámara, imagen, código manual o NFC. Funciona en cualquier condición.</p>
      </div>
      <div class="actions">
        <button class="btn btn-sm" :class="{ 'btn-primary': mode==='inventory' }" @click="mode='inventory'"><i class="mdi mdi-package-variant"></i> Inventario</button>
        <button class="btn btn-sm" :class="{ 'btn-primary': mode==='attendance' }" @click="mode='attendance'"><i class="mdi mdi-account-clock"></i> Asistencia</button>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div v-if="canUseCamera" class="scan-frame">
          <video ref="video" playsinline muted></video>
          <canvas ref="canvas" style="display:none;"></canvas>
          <div class="overlay"></div>
        </div>
        <div v-else class="scan-frame placeholder">
          <canvas ref="canvas" style="display:none;"></canvas>
          <div class="placeholder-inner">
            <i class="mdi mdi-camera-off" style="font-size:48px; opacity:.3;"></i>
            <div class="muted" style="margin-top:10px; font-size:14px; max-width:260px; text-align:center;">
              Cámara no disponible. Sube una imagen del QR/código o escribe el código manualmente.
            </div>
          </div>
        </div>

        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:14px;">
          <button v-if="canUseCamera && !scanning" class="btn btn-primary" @click="startCamera"><i class="mdi mdi-camera"></i> Abrir cámara</button>
          <button v-else-if="canUseCamera" class="btn" @click="stopCamera"><i class="mdi mdi-camera-off"></i> Pausar</button>
          <button class="btn" @click="fileInput.click()"><i class="mdi mdi-image"></i> Subir imagen QR</button>
          <input type="file" accept="image/*" ref="fileInput" @change="onFileUpload" style="display:none;" />
          <button v-if="nfcSupported && !nfcActive" class="btn" @click="startNFC"><i class="mdi mdi-nfc-tap"></i> Activar NFC</button>
          <span v-if="nfcActive" class="badge success"><i class="mdi mdi-nfc"></i> NFC activo</span>
        </div>

        <div style="margin-top:16px; padding-top:14px; border-top:1px dashed var(--border);">
          <label>Código manual</label>
          <div style="display:flex; gap:8px;">
            <input v-model="manualCode" placeholder="SKU-123, 7501055363057, EMP-001…" @keyup.enter="handleManual" />
            <button class="btn btn-primary" @click="handleManual" :disabled="!manualCode"><i class="mdi mdi-send"></i></button>
          </div>
        </div>

        <p v-if="error" class="badge danger" style="margin-top:10px;">{{ error }}</p>
        <p v-if="!secure" class="muted" style="margin-top:10px; font-size:12px;">
          <i class="mdi mdi-information"></i> Tip: cámara/NFC requieren HTTPS. Puedes poner un reverse proxy (Caddy/Nginx) con SSL para habilitarlos.
        </p>
      </div>

      <div class="card">
        <h3 style="margin-top:0;">Último escaneo</h3>
        <div v-if="!result" class="muted empty-state">
          <i class="mdi mdi-qrcode-scan" style="font-size:48px; opacity:.2;"></i>
          <div style="margin-top:10px;">Escanea, sube una imagen o escribe el código…</div>
        </div>
        <div v-else-if="result.type === 'scan'">
          <div style="display:flex; gap:8px; align-items:center;">
            <span class="badge accent">{{ result.data.kind }}</span>
            <span class="badge">{{ result.data.resolved_type }}</span>
          </div>
          <div class="mono" style="margin:10px 0 14px; word-break:break-all; padding:10px; background:var(--surface-2); border-radius:8px; font-size:13px;">{{ result.data.code }}</div>
          <div v-if="result.data.resolved_type === 'item' && result.data.resolved">
            <h4 style="margin:0;">{{ result.data.resolved.name }}</h4>
            <div class="muted mono">{{ result.data.resolved.sku }} · {{ result.data.resolved.unit }}</div>
            <h5 style="margin:16px 0 6px;">Stock actual</h5>
            <table class="table" style="font-size:13px;">
              <thead><tr><th>Ubicación</th><th>Qty</th><th>Reservado</th></tr></thead>
              <tbody>
                <tr v-for="s in result.data.stock" :key="s.location_id">
                  <td class="mono">{{ s.location_id.slice(0,8) }}…</td>
                  <td><b>{{ s.qty }}</b></td>
                  <td>{{ s.reserved }}</td>
                </tr>
                <tr v-if="!result.data.stock.length"><td colspan="3" class="muted">Sin stock registrado.</td></tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="result.data.resolved_type === 'location' && result.data.resolved">
            <h4 style="margin:0;">{{ result.data.resolved.name }}</h4>
            <div class="muted mono">{{ result.data.resolved.path }}</div>
          </div>
          <div v-else-if="result.data.resolved_type === 'employee' && result.data.resolved">
            <h4 style="margin:0;">{{ result.data.resolved.name }}</h4>
            <div class="muted mono">{{ result.data.resolved.code }}</div>
          </div>
          <div v-else class="muted">Código no encontrado en este tenant.</div>
        </div>
        <div v-else-if="result.type === 'attendance'">
          <span class="badge success"><i class="mdi mdi-check"></i> Checada registrada</span>
          <div class="muted" style="margin-top:10px;">ID: <span class="mono">{{ result.data.id }}</span></div>
          <div class="muted">Hora: {{ result.data.at }}</div>
        </div>
        <div v-else-if="result.type === 'error'">
          <span class="badge danger">Error</span>
          <div class="muted" style="margin-top:8px;">{{ result.message }}</div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.actions { display: flex; gap: 8px; }
.scan-frame { position: relative; aspect-ratio: 4/3; background: #000; border-radius: 12px; overflow: hidden; }
.scan-frame video { width: 100%; height: 100%; object-fit: cover; }
.scan-frame.placeholder { background: var(--surface-2); border: 2px dashed var(--border); display: grid; place-items: center; }
.placeholder-inner { text-align: center; padding: 20px; }
.overlay { position: absolute; inset: 20%; border: 2px dashed rgba(255,255,255,.6); border-radius: 10px; pointer-events: none; }
.empty-state { text-align: center; padding: 40px 20px; }
</style>
