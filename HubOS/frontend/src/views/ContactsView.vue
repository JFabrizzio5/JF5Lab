<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Contactos</h1>
        <p>Tu base de clientes y prospectos.</p>
      </div>
      <button @click="openNew" class="btn btn-primary">
        <i data-lucide="plus" style="width:16px;height:16px"></i> Nuevo contacto
      </button>
    </div>

    <div class="page-body">
      <div class="search-row">
        <input v-model="q" @input="search" placeholder="Buscar por nombre, email, teléfono, empresa…" />
        <select v-model="sessionFilter" @change="load()" class="session-filter">
          <option value="">Todas las sesiones</option>
          <option v-for="s in sessions" :key="s.id" :value="s.id">
            {{ s.display_name || s.instance_name }}
          </option>
        </select>
      </div>

      <DataTable
        :columns="[
          { key: 'name', label: 'Nombre' },
          { key: 'company', label: 'Empresa' },
          { key: 'email', label: 'Email' },
          { key: 'phone', label: 'Teléfono' },
          { key: 'source', label: 'Origen' },
        ]"
        :rows="contacts"
      >
        <template #cell-source="{ value }">
          <span class="badge badge-primary">{{ value }}</span>
        </template>
        <template #actions="{ row }">
          <button @click="chat(row)" class="btn btn-sm" :disabled="!row.phone" style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3)" :title="row.phone ? 'Enviar WhatsApp' : 'Sin teléfono'">
            <i data-lucide="message-circle" style="width:14px;height:14px"></i>
          </button>
          <button @click="edit(row)" class="btn btn-ghost btn-sm">Editar</button>
          <button @click="remove(row)" class="btn btn-sm" style="background:transparent;color:var(--danger);border:1px solid rgba(239,68,68,0.3)">
            <i data-lucide="trash-2" style="width:14px;height:14px"></i>
          </button>
        </template>
      </DataTable>
    </div>

    <Modal v-model="showModal" :title="form.id ? 'Editar contacto' : 'Nuevo contacto'">
      <FormField v-model="form.name" label="Nombre" required />
      <FormField v-model="form.email" label="Email" type="email" />
      <FormField v-model="form.phone" label="Teléfono (WhatsApp)" placeholder="5215512345678" />
      <FormField v-model="form.company" label="Empresa" />
      <FormField v-model="form.notes" label="Notas" type="textarea" />
      <FormField v-model="form.source" label="Origen" type="select" :options="['manual','whatsapp','web','referral']" />
      <template #footer>
        <button @click="showModal = false" class="btn btn-ghost">Cancelar</button>
        <button @click="save" class="btn btn-primary">Guardar</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/index.js'
import DataTable from '../components/DataTable.vue'
import Modal from '../components/Modal.vue'
import FormField from '../components/FormField.vue'

const router = useRouter()
function chat(c) {
  if (!c.phone) return
  router.push({ path: '/chat', query: { contact: c.id } })
}

const contacts = ref([])
const sessions = ref([])
const sessionFilter = ref('')
const q = ref('')
const showModal = ref(false)
const form = ref(emptyForm())

function emptyForm() { return { id: null, name: '', email: '', phone: '', company: '', notes: '', source: 'manual' } }

async function load() {
  const params = {}
  if (q.value) params.q = q.value
  if (sessionFilter.value) params.session_id = sessionFilter.value
  const { data } = await api.get('/contacts/', { params })
  contacts.value = data
}
async function loadSessions() {
  try {
    const { data } = await api.get('/chat/sessions')
    sessions.value = data
  } catch { sessions.value = [] }
}
let t
function search() { clearTimeout(t); t = setTimeout(load, 250) }

function openNew() { form.value = emptyForm(); showModal.value = true }
function edit(c) { form.value = { ...c }; showModal.value = true }
async function save() {
  const payload = { ...form.value }; delete payload.id
  if (form.value.id) await api.put(`/contacts/${form.value.id}`, payload)
  else await api.post('/contacts/', payload)
  showModal.value = false
  await load()
}
async function remove(c) {
  if (!confirm(`¿Eliminar ${c.name}?`)) return
  await api.delete(`/contacts/${c.id}`)
  await load()
}

onMounted(() => { load(); loadSessions(); if (window.lucide) window.lucide.createIcons() })
</script>

<style scoped>
.search-row { margin-bottom: 1rem; display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap; }
.search-row input { max-width: 420px; flex: 1 1 280px; }
.session-filter { max-width: 240px; flex: 0 1 220px; }
</style>
