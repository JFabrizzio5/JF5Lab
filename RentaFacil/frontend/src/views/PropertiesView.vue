<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Propiedades</h1>
      <button class="btn btn-primary" @click="openModal()">+ Nueva propiedad</button>
    </div>

    <div class="card">
      <div v-if="loading" class="empty">Cargando...</div>
      <div v-else-if="!items.length" class="empty">Sin propiedades. ¡Agrega la primera!</div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Dirección</th>
              <th>Tipo</th>
              <th>Renta mensual</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in items" :key="p.id">
              <td><strong>{{ p.name }}</strong></td>
              <td>{{ p.address }}<span v-if="p.city">, {{ p.city }}</span></td>
              <td>{{ typeLabel(p.property_type) }}</td>
              <td>${{ fmt(p.monthly_rent) }}</td>
              <td><span class="badge" :class="statusClass(p.status)">{{ statusLabel(p.status) }}</span></td>
              <td>
                <div class="actions">
                  <button class="btn btn-secondary" @click="openModal(p)">Editar</button>
                  <button class="btn btn-danger" @click="remove(p.id)">Eliminar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="modal" class="modal-overlay" @click.self="modal = false">
      <div class="modal">
        <div class="modal-title">{{ editing ? 'Editar propiedad' : 'Nueva propiedad' }}</div>
        <form @submit.prevent="save">
          <div class="form-grid">
            <div class="form-group" style="grid-column: 1 / -1">
              <label>Nombre</label>
              <input v-model="form.name" required />
            </div>
            <div class="form-group" style="grid-column: 1 / -1">
              <label>Dirección</label>
              <input v-model="form.address" required />
            </div>
            <div class="form-group">
              <label>Ciudad</label>
              <input v-model="form.city" />
            </div>
            <div class="form-group">
              <label>Estado / Provincia</label>
              <input v-model="form.state" />
            </div>
            <div class="form-group">
              <label>Tipo</label>
              <select v-model="form.property_type">
                <option value="apartment">Apartamento</option>
                <option value="house">Casa</option>
                <option value="commercial">Local comercial</option>
                <option value="office">Oficina</option>
                <option value="warehouse">Bodega</option>
              </select>
            </div>
            <div class="form-group">
              <label>Renta mensual ($)</label>
              <input v-model="form.monthly_rent" type="number" step="0.01" required />
            </div>
            <div class="form-group">
              <label>Estado</label>
              <select v-model="form.status">
                <option value="vacant">Vacante</option>
                <option value="occupied">Ocupada</option>
                <option value="maintenance">Mantenimiento</option>
              </select>
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
import { properties as api } from '../api/client'

const items = ref([])
const loading = ref(true)
const modal = ref(false)
const editing = ref(null)
const form = reactive({ name: '', address: '', city: '', state: '', property_type: 'apartment', monthly_rent: '', status: 'vacant', notes: '' })

const typeLabel = t => ({ apartment: 'Apartamento', house: 'Casa', commercial: 'Local', office: 'Oficina', warehouse: 'Bodega' }[t] || t)
const statusLabel = s => ({ vacant: 'Vacante', occupied: 'Ocupada', maintenance: 'Mantenimiento' }[s] || s)
const statusClass = s => ({ vacant: 'badge-blue', occupied: 'badge-green', maintenance: 'badge-yellow' }[s] || 'badge-gray')
const fmt = n => Number(n).toLocaleString('es-MX', { minimumFractionDigits: 2 })

async function load() {
  const { data } = await api.list()
  items.value = data
}

function openModal(p = null) {
  editing.value = p?.id || null
  Object.assign(form, p ? { ...p } : { name: '', address: '', city: '', state: '', property_type: 'apartment', monthly_rent: '', status: 'vacant', notes: '' })
  modal.value = true
}

async function save() {
  if (editing.value) {
    await api.update(editing.value, form)
  } else {
    await api.create(form)
  }
  modal.value = false
  await load()
}

async function remove(id) {
  if (!confirm('¿Eliminar esta propiedad?')) return
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
