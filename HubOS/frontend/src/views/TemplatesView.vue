<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Armador de Plantillas</h1>
        <p>Soporte, presentaciones y documentación técnica. Reutilizable y con variables.</p>
      </div>
      <button @click="openNew" class="btn btn-primary">
        <i data-lucide="plus" style="width:16px;height:16px"></i> Nueva plantilla
      </button>
    </div>

    <div class="page-body">
      <div class="tabs">
        <button v-for="c in categories" :key="c.value" @click="category = c.value; load()" class="tab" :class="{ active: category === c.value }">
          <i :data-lucide="c.icon" style="width:14px;height:14px"></i>
          {{ c.label }}
        </button>
      </div>

      <div class="grid">
        <div v-for="t in items" :key="t.id" class="item">
          <div class="item-head">
            <span class="badge badge-primary">{{ t.category }}</span>
            <div class="actions">
              <button @click="preview(t)" class="mini" title="Preview">
                <i data-lucide="eye" style="width:14px;height:14px"></i>
              </button>
              <button @click="edit(t)" class="mini" title="Editar">
                <i data-lucide="pencil" style="width:14px;height:14px"></i>
              </button>
              <button @click="remove(t)" class="mini danger" title="Eliminar">
                <i data-lucide="trash-2" style="width:14px;height:14px"></i>
              </button>
            </div>
          </div>
          <h3>{{ t.name }}</h3>
          <p class="desc">{{ t.description || 'Sin descripción' }}</p>
          <div class="meta">
            <span>{{ t.blocks.length }} bloques</span>
            <span>{{ t.variables.length }} variables</span>
          </div>
        </div>
        <div v-if="!items.length" class="empty">Ninguna plantilla en esta categoría.</div>
      </div>
    </div>

    <!-- Edit / create modal -->
    <Modal v-model="showModal" :title="form.id ? 'Editar plantilla' : 'Nueva plantilla'">
      <FormField v-model="form.name" label="Nombre" required />
      <FormField v-model="form.category" label="Categoría" type="select" :options="[
        {value:'support',label:'Soporte'},
        {value:'presentation',label:'Presentación'},
        {value:'tech_doc',label:'Documentación técnica'},
        {value:'general',label:'General'}
      ]" />
      <FormField v-model="form.description" label="Descripción" type="textarea" :rows="2" />

      <label style="margin-top:0.5rem">Variables</label>
      <div class="vars">
        <div v-for="(v, i) in form.variables" :key="i" class="var-row">
          <input v-model="v.key" placeholder="key" />
          <input v-model="v.label" placeholder="Etiqueta" />
          <input v-model="v.default" placeholder="Default" />
          <button @click="form.variables.splice(i, 1)" class="mini danger">
            <i data-lucide="x" style="width:14px;height:14px"></i>
          </button>
        </div>
        <button @click="form.variables.push({ key: '', label: '', default: '' })" class="btn btn-ghost btn-sm">
          <i data-lucide="plus" style="width:14px;height:14px"></i> Agregar variable
        </button>
      </div>

      <label style="margin-top:1rem">Bloques</label>
      <BlockEditor v-model="form.blocks" />

      <template #footer>
        <button @click="showModal = false" class="btn btn-ghost">Cancelar</button>
        <button @click="save" class="btn btn-primary">Guardar</button>
      </template>
    </Modal>

    <!-- Preview / render modal -->
    <Modal v-model="showPreview" title="Preview con variables">
      <div v-if="previewing">
        <div class="preview-vars" v-if="previewing.variables?.length">
          <div v-for="v in previewing.variables" :key="v.key" class="preview-var">
            <label>{{ v.label || v.key }}</label>
            <input v-model="varValues[v.key]" :placeholder="v.default" />
          </div>
          <button @click="render" class="btn btn-primary btn-sm" style="margin-top:0.5rem">
            <i data-lucide="wand-2" style="width:14px;height:14px"></i> Renderizar
          </button>
        </div>
        <div class="preview-output" v-if="rendered">
          <div v-for="(b, i) in rendered.blocks" :key="i" class="rb" :class="`rb-${b.type}`">
            <h3 v-if="b.type === 'heading'">{{ b.content }}</h3>
            <pre v-else-if="b.type === 'code'"><code>{{ b.content }}</code></pre>
            <img v-else-if="b.type === 'image' && b.content" :src="b.content" />
            <hr v-else-if="b.type === 'divider'" />
            <div v-else-if="b.type === 'callout'" class="callout">{{ b.content }}</div>
            <p v-else>{{ b.content }}</p>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'
import Modal from '../components/Modal.vue'
import FormField from '../components/FormField.vue'
import BlockEditor from '../components/BlockEditor.vue'

const categories = [
  { value: '', label: 'Todas', icon: 'layers' },
  { value: 'support', label: 'Soporte', icon: 'life-buoy' },
  { value: 'presentation', label: 'Presentación', icon: 'monitor' },
  { value: 'tech_doc', label: 'Docs técnicas', icon: 'book' },
  { value: 'general', label: 'General', icon: 'file-text' },
]
const items = ref([])
const category = ref('')
const showModal = ref(false)
const showPreview = ref(false)
const previewing = ref(null)
const varValues = ref({})
const rendered = ref(null)
const form = ref(emptyForm())

function emptyForm() { return { id: null, name: '', category: 'general', description: '', blocks: [], variables: [] } }

async function load() {
  const { data } = await api.get('/templates/', { params: category.value ? { category: category.value } : {} })
  items.value = data
}

function openNew() { form.value = emptyForm(); showModal.value = true }
function edit(t) {
  form.value = { ...t, blocks: [...(t.blocks || [])], variables: [...(t.variables || [])] }
  showModal.value = true
}
async function save() {
  const payload = { ...form.value }; delete payload.id
  if (form.value.id) await api.put(`/templates/${form.value.id}`, payload)
  else await api.post('/templates/', payload)
  showModal.value = false
  await load()
}
async function remove(t) {
  if (!confirm(`¿Eliminar "${t.name}"?`)) return
  await api.delete(`/templates/${t.id}`)
  await load()
}

function preview(t) {
  previewing.value = t
  varValues.value = {}
  for (const v of (t.variables || [])) varValues.value[v.key] = v.default || ''
  rendered.value = null
  showPreview.value = true
  render()
}
async function render() {
  const { data } = await api.post(`/templates/${previewing.value.id}/render`, { values: varValues.value })
  rendered.value = data
}

onMounted(() => { load(); if (window.lucide) window.lucide.createIcons() })
</script>

<style scoped>
.tabs { display: flex; gap: 0.4rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
.tab { display: inline-flex; align-items: center; gap: 0.4rem; background: transparent; border: 1px solid var(--border); color: var(--text2); padding: 0.4rem 0.85rem; border-radius: 8px; font-size: 0.82rem; font-weight: 500; }
.tab.active { background: rgba(99,102,241,0.18); border-color: rgba(99,102,241,0.4); color: #a5b4fc; }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.item { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.1rem; transition: all 0.15s; }
.item:hover { border-color: var(--primary); }
.item-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.actions { display: flex; gap: 0.3rem; }
.mini { background: transparent; border: 1px solid var(--border); color: var(--text2); width: 28px; height: 28px; border-radius: 7px; display: inline-flex; align-items: center; justify-content: center; }
.mini:hover { border-color: var(--primary); color: var(--text); }
.mini.danger:hover { border-color: var(--danger); color: var(--danger); }
.item h3 { font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }
.desc { font-size: 0.83rem; color: var(--text2); line-height: 1.4; min-height: 2.2em; }
.meta { display: flex; gap: 1rem; font-size: 0.72rem; color: var(--text3); margin-top: 0.7rem; padding-top: 0.7rem; border-top: 1px solid var(--border); }
.empty { grid-column: 1 / -1; text-align: center; color: var(--text3); padding: 2.5rem; }

.vars { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
.var-row { display: grid; grid-template-columns: 1fr 1fr 1fr 32px; gap: 0.4rem; }

.preview-vars { margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }
.preview-var { margin-bottom: 0.5rem; }
.preview-var label { font-size: 0.75rem; color: var(--text2); }
.preview-output { background: var(--bg3); border-radius: 10px; padding: 1.2rem; }
.rb { margin-bottom: 0.8rem; }
.rb h3 { font-size: 1.1rem; font-weight: 700; }
.rb pre { background: #0b0b14; padding: 0.8rem; border-radius: 7px; font-size: 0.8rem; overflow-x: auto; }
.rb img { max-width: 100%; border-radius: 8px; }
.rb .callout { background: rgba(6,182,212,0.1); border-left: 3px solid var(--accent); padding: 0.7rem 1rem; border-radius: 6px; color: var(--text2); }
.rb hr { border: 0; border-top: 1px solid var(--border); }
</style>
