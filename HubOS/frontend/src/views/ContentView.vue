<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Contenido</h1>
        <p>Páginas y posts de tu CMS, editados en bloques.</p>
      </div>
      <button @click="openNew" class="btn btn-primary">
        <i data-lucide="plus" style="width:16px;height:16px"></i> Nuevo contenido
      </button>
    </div>

    <div class="page-body">
      <div class="tabs">
        <button v-for="k in kinds" :key="k.value" @click="kind = k.value; load()" class="tab" :class="{ active: kind === k.value }">
          {{ k.label }}
        </button>
      </div>

      <div class="grid">
        <div v-for="c in items" :key="c.id" class="item" @click="edit(c)">
          <div class="item-head">
            <span class="badge" :class="c.status === 'published' ? 'badge-success' : 'badge-warning'">{{ c.status }}</span>
            <span class="kind">{{ c.kind }}</span>
          </div>
          <h3>{{ c.title }}</h3>
          <div class="slug">/{{ c.slug }}</div>
          <div class="updated">Actualizado: {{ fmt(c.updated_at) }}</div>
        </div>
        <div v-if="!items.length" class="empty">No hay contenido todavía.</div>
      </div>
    </div>

    <Modal v-model="showModal" :title="form.id ? 'Editar' : 'Nuevo contenido'">
      <FormField v-model="form.title" label="Título" required />
      <FormField v-model="form.slug" label="Slug (URL)" placeholder="auto-generado si se deja vacío" />
      <FormField v-model="form.kind" label="Tipo" type="select" :options="[{value:'page',label:'Página'},{value:'post',label:'Post'},{value:'snippet',label:'Snippet'}]" />
      <FormField v-model="form.status" label="Estado" type="select" :options="[{value:'draft',label:'Borrador'},{value:'published',label:'Publicado'}]" />
      <FormField v-model="form.cover_url" label="Imagen de portada (URL)" />
      <label style="margin-top:0.5rem">Bloques</label>
      <BlockEditor v-model="form.blocks" />
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
import BlockEditor from '../components/BlockEditor.vue'

const items = ref([])
const kind = ref('')
const kinds = [{ value: '', label: 'Todos' }, { value: 'page', label: 'Páginas' }, { value: 'post', label: 'Posts' }, { value: 'snippet', label: 'Snippets' }]
const showModal = ref(false)
const form = ref(emptyForm())

function emptyForm() { return { id: null, title: '', slug: '', kind: 'page', status: 'draft', cover_url: '', blocks: [], body: '' } }
function fmt(iso) { return iso ? new Date(iso).toLocaleDateString('es-MX') : '—' }

async function load() {
  const { data } = await api.get('/content/', { params: kind.value ? { kind: kind.value } : {} })
  items.value = data
}

function openNew() { form.value = emptyForm(); showModal.value = true }
function edit(c) { form.value = { ...c, blocks: [...(c.blocks || [])] }; showModal.value = true }
async function save() {
  const payload = { ...form.value }; delete payload.id
  if (form.value.id) await api.put(`/content/${form.value.id}`, payload)
  else await api.post('/content/', payload)
  showModal.value = false
  await load()
}
async function remove() {
  if (!confirm('¿Eliminar?')) return
  await api.delete(`/content/${form.value.id}`)
  showModal.value = false
  await load()
}

onMounted(() => { load(); if (window.lucide) window.lucide.createIcons() })
</script>

<style scoped>
.tabs { display: flex; gap: 0.4rem; margin-bottom: 1.2rem; }
.tab { background: transparent; border: 1px solid var(--border); color: var(--text2); padding: 0.4rem 0.85rem; border-radius: 8px; font-size: 0.82rem; font-weight: 500; }
.tab.active { background: rgba(99,102,241,0.18); border-color: rgba(99,102,241,0.4); color: #a5b4fc; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; }
.item { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; cursor: pointer; transition: all 0.15s; }
.item:hover { border-color: var(--primary); transform: translateY(-2px); }
.item-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.kind { font-size: 0.7rem; color: var(--text3); text-transform: uppercase; letter-spacing: 0.05em; }
.item h3 { font-size: 1rem; font-weight: 700; margin-bottom: 0.3rem; }
.slug { font-size: 0.8rem; color: var(--text2); font-family: ui-monospace, monospace; }
.updated { font-size: 0.72rem; color: var(--text3); margin-top: 0.6rem; }
.empty { grid-column: 1 / -1; text-align: center; color: var(--text3); padding: 2.5rem; }
</style>
