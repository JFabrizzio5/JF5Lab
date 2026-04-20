<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Inquilinos</h1>
      <button class="btn btn-primary" @click="openModal()">+ Nuevo inquilino</button>
    </div>

    <div class="card">
      <div v-if="loading" class="empty">Cargando...</div>
      <div v-else-if="!items.length" class="empty">Sin inquilinos registrados.</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>RFC</th>
              <th>Contratos</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in items" :key="t.id">
              <td><strong>{{ t.name }}</strong></td>
              <td>{{ t.email || '—' }}</td>
              <td>{{ t.phone || '—' }}</td>
              <td>{{ t.rfc || '—' }}</td>
              <td>{{ t.contracts?.length || 0 }}</td>
              <td>
                <div class="actions">
                  <button class="btn btn-secondary" @click="openModal(t)">Editar</button>
                  <button class="btn btn-danger" @click="remove(t.id)">Eliminar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="modal" class="modal-overlay" @click.self="modal = false">
      <div class="modal">
        <div class="modal-title">{{ editing ? 'Editar inquilino' : 'Nuevo inquilino' }}</div>
        <form @submit.prevent="save">
          <div class="form-grid">
            <div class="form-group" style="grid-column: 1 / -1">
              <label>Nombre completo *</label>
              <input v-model="form.name" required />
            </div>
            <div class="form-group">
              <label>Correo electrónico</label>
              <input v-model="form.email" type="email" />
            </div>
            <div class="form-group">
              <label>Teléfono</label>
              <input v-model="form.phone" type="tel" />
            </div>
            <div class="form-group">
              <label>RFC</label>
              <input v-model="form.rfc" />
            </div>
            <div class="form-group" style="grid-column: 1 / -1">
              <label>Dirección</label>
              <input v-model="form.address" />
            </div>
            <div class="form-group" style="grid-column: 1 / -1">
              <label>Notas</label>
              <textarea v-model="form.notes" rows="2"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="modal = false">Cancelar</button>
            <button type="submit" class="btn btn-primary">{{ editing ? 'Guardar' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { tenants as api } from '../api/client'

const items = ref([])
const loading = ref(true)
const modal = ref(false)
const editing = ref(null)
const blank = () => ({ name: '', email: '', phone: '', rfc: '', address: '', notes: '' })
const form = reactive(blank())

async function load() {
  const { data } = await api.list()
  items.value = data
}

function openModal(t = null) {
  editing.value = t?.id || null
  Object.assign(form, t ? { name: t.name, email: t.email || '', phone: t.phone || '', rfc: t.rfc || '', address: t.address || '', notes: t.notes || '' } : blank())
  modal.value = true
}

async function save() {
  const payload = Object.fromEntries(Object.entries(form).filter(([, v]) => v !== ''))
  if (editing.value) {
    await api.update(editing.value, payload)
  } else {
    await api.create(payload)
  }
  modal.value = false
  await load()
}

async function remove(id) {
  if (!confirm('¿Eliminar este inquilino?')) return
  await api.delete(id)
  await load()
}

onMounted(async () => {
  try { await load() } finally { loading.value = false }
})
</script>

<style scoped>
.actions { display: flex; gap: 8px; }
</style>
