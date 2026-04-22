<script setup>
import { ref, onMounted, watch } from 'vue'
import QRCode from 'qrcode'
import AppLayout from '../components/AppLayout.vue'
import { itemsApi, labelsApi } from '../api/endpoints'

const items = ref([])
const selected = ref(new Set())
const created = ref([])
const kind = ref('QR')
const busy = ref(false)
const q = ref('')
const nfcWriteBusy = ref(null)
const writeMsg = ref(null)

async function load() {
  const { data } = await itemsApi.list({ q: q.value || undefined })
  items.value = data
}

function toggle(id) {
  const s = new Set(selected.value)
  if (s.has(id)) s.delete(id); else s.add(id)
  selected.value = s
}

async function generate() {
  busy.value = true
  writeMsg.value = null
  try {
    for (const id of selected.value) {
      const { data } = await labelsApi.create({ kind: kind.value, item_id: id })
      const item = items.value.find(i => i.id === id)
      const payload = `stocklink://${data.kind.toLowerCase()}/${data.code}`
      const qrDataUrl = await QRCode.toDataURL(payload, { margin: 1, width: 240, color: { dark: '#0f172a', light: '#ffffff' } })
      created.value.push({ ...data, itemName: item?.name, itemSku: item?.sku, payload, qrDataUrl })
    }
    selected.value = new Set()
  } finally { busy.value = false }
}

async function exportPDF() {
  const ids = created.value.map(l => l.id)
  if (!ids.length) return
  const { data } = await labelsApi.pdf(ids)
  const url = URL.createObjectURL(data)
  const a = document.createElement('a')
  a.href = url; a.download = `etiquetas-${new Date().toISOString().slice(0,10)}.pdf`
  document.body.appendChild(a); a.click(); a.remove()
  URL.revokeObjectURL(url)
}

async function writeNFC(label) {
  if (!('NDEFReader' in window)) {
    writeMsg.value = 'Web NFC no disponible. Usa Chrome Android sobre HTTPS.'
    return
  }
  nfcWriteBusy.value = label.id
  writeMsg.value = 'Acerca el tag NFC al celular…'
  try {
    const ndef = new NDEFReader()
    await ndef.write({ records: [
      { recordType: 'text', data: label.payload },
      { recordType: 'url',  data: `https://stocklink.mx/s/${label.code}` },
    ]})
    writeMsg.value = `Tag escrito correctamente con ${label.code}`
  } catch (e) {
    writeMsg.value = 'Error: ' + (e.message || e.name)
  } finally { nfcWriteBusy.value = null }
}

function copyPayload(p) {
  navigator.clipboard?.writeText(p)
  writeMsg.value = 'Payload copiado al portapapeles'
  setTimeout(() => { writeMsg.value = null }, 2500)
}

onMounted(load)
watch(q, () => load())
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1>Etiquetas</h1>
        <p class="muted">Genera QR, Code128 o NFC. Imprime en PDF A4 (21 por hoja).</p>
      </div>
      <div class="actions">
        <select v-model="kind" style="width:auto;">
          <option value="QR">QR</option>
          <option value="BARCODE">Code128</option>
          <option value="NFC">NFC</option>
        </select>
        <button class="btn btn-primary btn-sm" :disabled="!selected.size || busy" @click="generate">
          <i class="mdi mdi-qrcode-plus"></i> Generar ({{ selected.size }})
        </button>
      </div>
    </div>

    <div v-if="writeMsg" class="card flash">{{ writeMsg }}</div>

    <div class="grid-2">
      <div class="card" style="padding:0; overflow:auto; max-height:70vh;">
        <div style="padding:14px 20px 8px; position:sticky; top:0; background:var(--surface); border-bottom:1px solid var(--border);">
          <input v-model="q" placeholder="Buscar artículo…" />
        </div>
        <table class="table">
          <thead><tr><th style="width:40px;"></th><th>SKU</th><th>Nombre</th><th>Unidad</th></tr></thead>
          <tbody>
            <tr v-for="i in items" :key="i.id" @click="toggle(i.id)" style="cursor:pointer;">
              <td><input type="checkbox" :checked="selected.has(i.id)" @click.stop="toggle(i.id)" style="width:auto;" /></td>
              <td class="mono">{{ i.sku }}</td>
              <td>{{ i.name }}</td>
              <td>{{ i.unit }}</td>
            </tr>
            <tr v-if="!items.length"><td colspan="4" class="muted" style="text-align:center; padding:30px;">Sin artículos.</td></tr>
          </tbody>
        </table>
      </div>

      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <h3 style="margin:0;">Etiquetas creadas ({{ created.length }})</h3>
          <button class="btn btn-sm" :disabled="!created.length" @click="exportPDF">
            <i class="mdi mdi-file-pdf-box"></i> PDF A4
          </button>
        </div>

        <div v-if="!created.length" class="muted empty">
          <i class="mdi mdi-qrcode" style="font-size:48px; opacity:.2;"></i>
          <div style="margin-top:8px;">Selecciona artículos y presiona Generar.</div>
        </div>

        <div v-else class="labels-grid">
          <div v-for="l in created" :key="l.id" class="lbl" :class="{ nfc: l.kind === 'NFC' }">
            <img v-if="l.kind !== 'NFC'" :src="l.qrDataUrl" alt="label" />
            <div v-else class="nfc-icon"><i class="mdi mdi-nfc-variant"></i></div>

            <div class="lbl-name">{{ l.itemName || 'Etiqueta' }}</div>
            <div class="mono lbl-code">{{ l.code }}</div>
            <div class="badge" :class="l.kind === 'NFC' ? 'accent' : ''">{{ l.kind }}</div>

            <div class="lbl-actions">
              <button class="btn btn-sm" @click="copyPayload(l.payload)" title="Copiar deep-link">
                <i class="mdi mdi-content-copy"></i>
              </button>
              <button v-if="l.kind === 'NFC'" class="btn btn-primary btn-sm" @click="writeNFC(l)" :disabled="nfcWriteBusy === l.id">
                <i class="mdi mdi-nfc-tap"></i>
                {{ nfcWriteBusy === l.id ? 'Escribiendo…' : 'Escribir tag' }}
              </button>
            </div>

            <details class="lbl-details">
              <summary>Ver link</summary>
              <code class="mono">{{ l.payload }}</code>
            </details>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.actions { display: flex; gap: 8px; align-items: center; }
.flash { background: linear-gradient(135deg, rgba(99,102,241,.12), rgba(168,85,247,.12)); border-color: var(--accent); margin-bottom: 16px; padding: 12px 16px; font-size: 14px; }
.empty { text-align: center; padding: 40px 20px; }
.labels-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 16px; }
.lbl { text-align: center; border: 1px solid var(--border); border-radius: 12px; padding: 14px 12px; background: var(--bg); display: flex; flex-direction: column; gap: 6px; align-items: center; }
.lbl.nfc { background: linear-gradient(135deg, rgba(99,102,241,.08), rgba(168,85,247,.08)); }
.lbl img { width: 100%; max-width: 140px; aspect-ratio: 1; object-fit: contain; background: white; border-radius: 8px; padding: 8px; }
.nfc-icon { width: 140px; height: 140px; border-radius: 8px; background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: white; display: grid; place-items: center; font-size: 64px; }
.lbl-name { font-weight: 600; font-size: 13px; line-height: 1.3; min-height: 34px; }
.lbl-code { font-size: 11px; color: var(--text-muted); word-break: break-all; }
.lbl-actions { display: flex; gap: 6px; justify-content: center; margin-top: 4px; }
.lbl-details { font-size: 11px; margin-top: 4px; width: 100%; }
.lbl-details summary { cursor: pointer; color: var(--text-muted); }
.lbl-details code { display: block; margin-top: 6px; word-break: break-all; background: var(--surface-2); padding: 6px; border-radius: 6px; font-size: 10px; }
</style>
