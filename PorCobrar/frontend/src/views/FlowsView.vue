<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const flows = ref([])
const templates = ref([])
const loading = ref(true)
const err = ref('')
const newFlow = ref({ name: '', description: '', steps: [{ day: 0, channel: 'email', template_id: '' }] })
const newTemplate = ref({ name: '', channel: 'email', subject: '', body: '' })

async function load() {
  loading.value = true
  try {
    const [f, t] = await Promise.all([api.get('/dunning-flows'), api.get('/dunning-templates')])
    flows.value = f.data
    templates.value = t.data
  } catch(e) { err.value = e.message }
  loading.value = false
}
onMounted(load)

async function createFlow() {
  try {
    await api.post('/dunning-flows', newFlow.value)
    newFlow.value = { name: '', description: '', steps: [{ day: 0, channel: 'email', template_id: '' }] }
    await load()
  } catch(e) { err.value = e.message }
}

async function createTemplate() {
  try {
    await api.post('/dunning-templates', newTemplate.value)
    newTemplate.value = { name: '', channel: 'email', subject: '', body: '' }
    await load()
  } catch(e) { err.value = e.message }
}

function addStep() {
  newFlow.value.steps.push({ day: 0, channel: 'email', template_id: '' })
}
function rmStep(i) {
  newFlow.value.steps.splice(i, 1)
}

function chColor(c) {
  if (c === 'whatsapp') return 'var(--cash)'
  if (c === 'sms') return 'var(--warn)'
  return 'var(--info)'
}
</script>

<template>
  <div>
    <h1>Dunning flows</h1>
    <div class="muted" style="font-size:13px; margin-bottom: 22px">Programa recordatorios escalados por email, WhatsApp y SMS.</div>

    <div class="grid-2">
      <div>
        <h3 style="margin-bottom: 12px">Flows activos</h3>
        <div class="card" v-for="f in flows" :key="f.id" style="margin-bottom: 12px">
          <div style="display:flex; justify-content:space-between">
            <div>
              <div style="font-weight:700">{{ f.name }}</div>
              <div class="muted" style="font-size:12px">{{ f.description }}</div>
            </div>
            <span class="badge cash" v-if="f.active">Activo</span>
          </div>
          <div style="display:flex; gap:8px; align-items:center; margin-top: 12px; flex-wrap:wrap">
            <template v-for="(s, i) in f.steps" :key="i">
              <div class="card-inset" style="padding:8px 12px; min-width: 110px">
                <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase">Paso {{ i + 1 }}</div>
                <div style="font-family:var(--mono); font-weight:700; font-size:16px" :style="{color: chColor(s.channel)}">+{{ s.day }}d</div>
                <div><span class="chip-channel" :class="s.channel">{{ s.channel }}</span></div>
              </div>
              <i class="mdi mdi-arrow-right muted" v-if="i < f.steps.length - 1"></i>
            </template>
          </div>
        </div>
        <div v-if="!flows.length" class="card muted">Sin flows.</div>
      </div>

      <div>
        <h3 style="margin-bottom: 12px">Nuevo flow</h3>
        <div class="card">
          <label>Nombre</label>
          <input v-model="newFlow.name" placeholder="Ej: Agresivo 5 toques">
          <div style="height:10px"></div>
          <label>Descripción</label>
          <input v-model="newFlow.description">
          <div style="height:14px"></div>
          <label>Pasos</label>
          <div v-for="(s, i) in newFlow.steps" :key="i" style="display:grid; grid-template-columns: 80px 130px 1fr 36px; gap:6px; margin-bottom: 6px">
            <input type="number" v-model.number="s.day" placeholder="día">
            <select v-model="s.channel">
              <option value="email">email</option>
              <option value="whatsapp">whatsapp</option>
              <option value="sms">sms</option>
            </select>
            <select v-model="s.template_id">
              <option value="">(plantilla)</option>
              <option v-for="t in templates.filter(t => t.channel === s.channel)" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
            <button class="btn btn-sm btn-ghost" @click="rmStep(i)"><i class="mdi mdi-close"></i></button>
          </div>
          <button class="btn btn-sm" @click="addStep"><i class="mdi mdi-plus"></i> Paso</button>
          <div style="margin-top: 14px; display:flex; justify-content:flex-end">
            <button class="btn btn-primary" @click="createFlow"><i class="mdi mdi-content-save-outline"></i> Guardar flow</button>
          </div>
        </div>

        <h3 style="margin: 22px 0 12px">Nueva plantilla</h3>
        <div class="card">
          <div class="grid-2">
            <div><label>Nombre</label><input v-model="newTemplate.name"></div>
            <div><label>Canal</label>
              <select v-model="newTemplate.channel"><option>email</option><option>whatsapp</option><option>sms</option></select>
            </div>
          </div>
          <div style="margin-top: 8px"><label>Asunto (email)</label><input v-model="newTemplate.subject"></div>
          <div style="margin-top: 8px"><label>Cuerpo (usa &#123;&#123;debtor.name&#125;&#125;, &#123;&#123;invoice.total&#125;&#125;, &#123;&#123;invoice.pay_link&#125;&#125;)</label>
            <textarea v-model="newTemplate.body" rows="5"></textarea>
          </div>
          <div style="margin-top: 12px; display:flex; justify-content:flex-end">
            <button class="btn" @click="createTemplate"><i class="mdi mdi-content-save-outline"></i> Guardar plantilla</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="err" class="card" style="margin-top: 14px; border-color:var(--danger)">{{ err }}</div>
  </div>
</template>
