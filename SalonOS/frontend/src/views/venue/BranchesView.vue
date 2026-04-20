<template>
  <div>
    <div class="page-header" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
      <div>
        <h1>Sucursales</h1>
        <p>Gestiona las ubicaciones de tu venue</p>
      </div>
      <button @click="openCreate" class="btn btn-primary">+ Nueva sucursal</button>
    </div>

    <div class="page-body">
      <div id="branches-map" class="branches-map"></div>

      <div class="branches-list" style="margin-top:1.5rem">
        <div v-if="loading" style="color:var(--text2)">Cargando...</div>
        <div v-else-if="!branches.length" style="color:var(--text2)">No hay sucursales creadas</div>

        <div v-for="b in branches" :key="b.id" class="branch-card card">
          <div class="branch-info">
            <div class="branch-name">{{ b.name }}</div>
            <div v-if="b.address" class="branch-meta">📍 {{ b.address }}</div>
            <div v-if="b.phone" class="branch-meta">📞 {{ b.phone }}</div>
            <div v-if="b.lat && b.lng" class="branch-meta">🌐 {{ b.lat.toFixed(4) }}, {{ b.lng.toFixed(4) }}</div>
          </div>
          <div class="branch-actions">
            <span :class="b.is_active ? 'badge-active' : 'badge-inactive'">
              {{ b.is_active ? 'Activa' : 'Inactiva' }}
            </span>
            <button @click="editBranch(b)" class="btn btn-ghost btn-sm">Editar</button>
            <button @click="deleteBranch(b)" class="btn btn-danger btn-sm">Eliminar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h2>{{ editing ? 'Editar sucursal' : 'Nueva sucursal' }}</h2>

        <div class="form-group">
          <label>Nombre *</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="form-group">
          <label>Dirección</label>
          <input v-model="form.address" type="text" />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Latitud</label>
            <input v-model.number="form.lat" type="number" step="any" placeholder="19.4326" />
          </div>
          <div class="form-group">
            <label>Longitud</label>
            <input v-model.number="form.lng" type="number" step="any" placeholder="-99.1332" />
          </div>
        </div>
        <div class="form-group">
          <label>Teléfono</label>
          <input v-model="form.phone" type="tel" />
        </div>
        <div class="form-group" style="display:flex;align-items:center;gap:.75rem">
          <input v-model="form.is_active" type="checkbox" id="branch_active" style="width:auto" />
          <label for="branch_active" style="margin:0">Sucursal activa</label>
        </div>

        <div class="modal-footer">
          <button @click="showModal = false" class="btn btn-ghost">Cancelar</button>
          <button @click="saveBranch" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : (editing ? 'Actualizar' : 'Crear') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const branches = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
let map = null

const form = ref({ name: '', address: '', lat: null, lng: null, phone: '', is_active: true })

async function loadBranches() {
  loading.value = true
  try {
    const { data } = await api.get('/venues/me/branches')
    branches.value = data
    updateMap()
  } finally {
    loading.value = false
  }
}

function updateMap() {
  import('leaflet').then(L => {
    if (map) { map.remove(); map = null }
    const el = document.getElementById('branches-map')
    if (!el) return
    const center = branches.value.length
      ? [branches.value[0].lat || 19.4326, branches.value[0].lng || -99.1332]
      : [19.4326, -99.1332]
    map = L.map('branches-map').setView(center, 12)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map)
    branches.value.forEach(b => {
      if (b.lat && b.lng) {
        L.marker([b.lat, b.lng]).addTo(map).bindPopup(`<strong>${b.name}</strong><br>${b.address || ''}`)
      }
    })
  })
}

function openCreate() {
  editing.value = null
  form.value = { name: '', address: '', lat: null, lng: null, phone: '', is_active: true }
  showModal.value = true
}

function editBranch(b) {
  editing.value = b.id
  form.value = { ...b }
  showModal.value = true
}

async function saveBranch() {
  if (!form.value.name) return
  saving.value = true
  try {
    if (editing.value) {
      await api.put(`/venues/me/branches/${editing.value}`, form.value)
    } else {
      await api.post('/venues/me/branches', form.value)
    }
    showModal.value = false
    await loadBranches()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al guardar')
  } finally {
    saving.value = false
  }
}

async function deleteBranch(b) {
  if (!confirm(`¿Eliminar "${b.name}"?`)) return
  try {
    await api.delete(`/venues/me/branches/${b.id}`)
    await loadBranches()
  } catch (e) {
    alert('Error al eliminar sucursal')
  }
}

onMounted(loadBranches)
</script>

<style scoped>
.branches-map {
  height: 320px;
  border-radius: 12px;
  border: 1px solid var(--border);
  overflow: hidden;
}

.branch-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.branch-name { font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem; }
.branch-meta { font-size: 0.82rem; color: var(--text2); }

.branch-actions { display: flex; align-items: center; gap: 0.5rem; }

.badge-active { background: rgba(16,185,129,0.2); color: #34d399; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.badge-inactive { background: rgba(239,68,68,0.2); color: #f87171; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
</style>
