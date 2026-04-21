<script setup>
import { ref } from 'vue'
import api from '../api/client'

const drag = ref(false)
const files = ref([])
const uploading = ref(false)
const results = ref([])
const err = ref('')

function onDrop(e) {
  e.preventDefault()
  drag.value = false
  files.value = Array.from(e.dataTransfer.files)
}
function onPick(e) { files.value = Array.from(e.target.files) }

async function uploadAll() {
  uploading.value = true
  err.value = ''
  results.value = []
  for (const f of files.value) {
    const fd = new FormData()
    fd.append('file', f)
    try {
      const { data } = await api.post('/invoices/import', fd, { headers: {'Content-Type': 'multipart/form-data'} })
      results.value.push({ file: f.name, ok: true, ...data })
    } catch(e) {
      results.value.push({ file: f.name, ok: false, error: e.response?.data?.detail || e.message })
    }
  }
  uploading.value = false
  files.value = []
}
</script>

<template>
  <div>
    <h1>Upload CFDI / CSV</h1>
    <div class="muted" style="font-size:13px; margin-bottom: 18px">
      Arrastra archivos XML (CFDI 3.3 / 4.0) o CSV con columnas <span class="mono">rfc,name,email,phone,cfdi_uuid,folio,total,due_at</span>.
    </div>

    <div class="drop-zone" :class="{drag}" @drop="onDrop" @dragover.prevent="drag=true" @dragleave="drag=false" @click="$refs.fi.click()">
      <i class="mdi mdi-cloud-upload-outline" style="font-size:42px; color:var(--cash)"></i>
      <h3 style="margin: 8px 0 4px">Suelta archivos aquí</h3>
      <div class="muted" style="font-size:13px">.xml (1 factura CFDI) o .csv (batch)</div>
      <input ref="fi" type="file" accept=".xml,.csv" multiple @change="onPick" style="display:none">
    </div>

    <div v-if="files.length" class="card" style="margin-top: 14px">
      <div style="margin-bottom:8px"><strong>{{ files.length }}</strong> archivos listos para subir:</div>
      <ul style="list-style:none; padding:0; margin:0; font-size:13px">
        <li v-for="f in files" :key="f.name"><i class="mdi mdi-file-outline"></i> {{ f.name }} <span class="muted">({{ (f.size/1024).toFixed(1) }} KB)</span></li>
      </ul>
      <div style="margin-top:12px; display:flex; justify-content:flex-end">
        <button class="btn btn-primary" :disabled="uploading" @click="uploadAll">
          <i class="mdi mdi-upload"></i> {{ uploading ? 'Subiendo…' : 'Confirmar upload' }}
        </button>
      </div>
    </div>

    <div v-if="results.length" class="card" style="margin-top: 14px">
      <h3 style="margin-bottom: 10px">Resultados</h3>
      <div v-for="(r, i) in results" :key="i" style="padding: 8px 0; border-bottom: 1px solid var(--border)">
        <div style="display:flex; justify-content:space-between">
          <span><i class="mdi" :class="r.ok ? 'mdi-check-circle' : 'mdi-alert-circle-outline'" :style="{color: r.ok ? 'var(--cash)' : 'var(--danger)'}"></i> {{ r.file }}</span>
          <span class="muted" v-if="r.ok">{{ r.created || 0 }} creadas</span>
        </div>
        <div v-if="!r.ok" class="muted" style="font-size:12px; color:var(--danger)">{{ r.error }}</div>
        <div v-else-if="r.uuid" class="mono muted" style="font-size:11px">UUID: {{ r.uuid }}</div>
      </div>
    </div>
  </div>
</template>
