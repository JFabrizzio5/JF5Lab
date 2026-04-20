<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Deals</h1>
        <p>Pipeline con drag & drop entre etapas.</p>
      </div>
      <button @click="openNew" class="btn btn-primary">
        <i data-lucide="plus" style="width:16px;height:16px"></i> Nuevo deal
      </button>
    </div>

    <div class="page-body">
      <div v-if="!pipeline" class="card empty-state">Sin pipelines configurados.</div>
      <div v-else class="kanban">
        <div
          v-for="stage in pipeline.stages"
          :key="stage"
          class="col"
          @dragover.prevent
          @drop="onDrop(stage)"
        >
          <div class="col-head">
            <span>{{ stage }}</span>
            <span class="count">{{ byStage(stage).length }}</span>
          </div>
          <div class="cards">
            <div
              v-for="d in byStage(stage)"
              :key="d.id"
              class="deal-card"
              draggable="true"
              @dragstart="drag = d"
              @click="edit(d)"
            >
              <div class="deal-title">{{ d.title }}</div>
              <div class="deal-amount">${{ formatMoney(d.value) }} <span class="cur">{{ d.currency }}</span></div>
              <div v-if="d.contact" class="deal-contact">
                <i data-lucide="user" style="width:12px;height:12px"></i>
                {{ d.contact.name }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal v-model="showModal" :title="form.id ? 'Editar deal' : 'Nuevo deal'">
      <FormField v-model="form.title" label="Título" required />
      <FormField v-model.number="form.value" label="Valor" type="number" />
      <FormField v-model="form.currency" label="Moneda" type="select" :options="['MXN','USD','EUR']" />
      <FormField v-model="form.stage" label="Etapa" type="select" :options="pipeline?.stages || []" />
      <FormField v-model="form.status" label="Estado" type="select" :options="['open','won','lost']" />
      <FormField v-model="form.contact_id" label="Contacto ID (opcional)" type="number" />
      <template #footer>
        <button @click="showModal = false" class="btn btn-ghost">Cancelar</button>
        <button v-if="form.id" @click="remove" class="btn btn-danger">Eliminar</button>
        <button @click="save" class="btn btn-primary">Guardar</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'
import Modal from '../components/Modal.vue'
import FormField from '../components/FormField.vue'

const deals = ref([])
const pipeline = ref(null)
const drag = ref(null)
const showModal = ref(false)
const form = ref(emptyForm())

function emptyForm() { return { id: null, title: '', value: 0, currency: 'MXN', stage: 'Nuevo', status: 'open', contact_id: null, pipeline_id: null } }
function byStage(s) { return deals.value.filter(d => d.stage === s) }
function formatMoney(n) { return (n || 0).toLocaleString('es-MX', { maximumFractionDigits: 0 }) }

async function load() {
  const [p, d] = await Promise.all([api.get('/deals/pipelines'), api.get('/deals/')])
  pipeline.value = p.data[0] || null
  deals.value = d.data
}

async function onDrop(stage) {
  if (!drag.value || drag.value.stage === stage) return
  const d = drag.value
  drag.value = null
  d.stage = stage
  await api.patch(`/deals/${d.id}/stage`, { stage })
}

function openNew() {
  form.value = emptyForm()
  form.value.pipeline_id = pipeline.value?.id
  form.value.stage = pipeline.value?.stages[0] || 'Nuevo'
  showModal.value = true
}
function edit(d) { form.value = { ...d, pipeline_id: pipeline.value?.id }; showModal.value = true }

async function save() {
  const payload = { ...form.value }; delete payload.id
  if (form.value.id) await api.put(`/deals/${form.value.id}`, payload)
  else await api.post('/deals/', payload)
  showModal.value = false
  await load()
}
async function remove() {
  if (!confirm('¿Eliminar deal?')) return
  await api.delete(`/deals/${form.value.id}`)
  showModal.value = false
  await load()
}

onMounted(() => { load(); if (window.lucide) window.lucide.createIcons() })
</script>

<style scoped>
.kanban {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(260px, 1fr);
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}
.col { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px; padding: 0.8rem; min-height: 400px; }
.col-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; font-size: 0.85rem; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 0.05em; }
.count { background: var(--bg3); padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; color: var(--text); font-weight: 600; }
.cards { display: flex; flex-direction: column; gap: 0.5rem; }
.deal-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.7rem 0.85rem;
  cursor: grab;
  transition: border-color 0.15s, transform 0.15s;
}
.deal-card:hover { border-color: var(--primary); transform: translateY(-1px); }
.deal-card:active { cursor: grabbing; }
.deal-title { font-size: 0.85rem; font-weight: 600; margin-bottom: 0.3rem; }
.deal-amount { font-size: 0.9rem; font-weight: 700; color: var(--success); }
.cur { font-size: 0.7rem; color: var(--text3); }
.deal-contact { display: flex; align-items: center; gap: 0.3rem; font-size: 0.72rem; color: var(--text3); margin-top: 0.35rem; }
.empty-state { text-align: center; color: var(--text3); padding: 2.5rem; }
</style>
