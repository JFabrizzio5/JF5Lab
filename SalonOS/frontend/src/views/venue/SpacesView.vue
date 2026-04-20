<template>
  <div>
    <div class="page-header" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem">
      <div>
        <h1>Espacios</h1>
        <p>Administra los salones y áreas de tu venue</p>
      </div>
      <button @click="openCreate" class="btn btn-primary">+ Nuevo espacio</button>
    </div>

    <div class="page-body">
      <div v-if="loading" style="color:var(--text2);padding:2rem">Cargando espacios...</div>

      <div v-else class="spaces-grid">
        <div v-if="!spaces.length" style="color:var(--text2)">No hay espacios creados</div>

        <div v-for="s in spaces" :key="s.id" class="space-card card">
          <img v-if="firstImage(s)" :src="firstImage(s)" :alt="s.name" class="space-img" />
          <div v-else class="space-img-placeholder">🏠</div>

          <div class="space-body">
            <div class="space-header">
              <h3>{{ s.name }}</h3>
              <span :class="s.is_active ? 'badge-active' : 'badge-inactive'">
                {{ s.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
            <p class="space-desc">{{ s.description || 'Sin descripción' }}</p>
            <div class="space-stats">
              <span>👥 {{ s.capacity }} personas</span>
              <span>💰 ${{ s.price_event?.toLocaleString() }}/evento</span>
              <span v-if="s.price_per_hour > 0">⏰ ${{ s.price_per_hour?.toLocaleString() }}/hr</span>
            </div>
            <div v-if="amenities(s).length" class="space-amenities">
              <span v-for="a in amenities(s).slice(0,3)" :key="a" class="chip-sm">{{ a }}</span>
              <span v-if="amenities(s).length > 3" class="chip-sm">+{{ amenities(s).length - 3 }}</span>
            </div>
            <div class="space-actions">
              <button @click="editSpace(s)" class="btn btn-ghost btn-sm">Editar</button>
              <button @click="deleteSpace(s)" class="btn btn-danger btn-sm">Eliminar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal" style="max-width:580px">
        <h2>{{ editing ? 'Editar espacio' : 'Nuevo espacio' }}</h2>

        <div class="form-group">
          <label>Nombre *</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="form-group">
          <label>Descripción</label>
          <textarea v-model="form.description" rows="3"></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Capacidad (personas)</label>
            <input v-model.number="form.capacity" type="number" min="1" />
          </div>
          <div class="form-group">
            <label>Precio por evento ($)</label>
            <input v-model.number="form.price_event" type="number" min="0" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Precio por hora ($)</label>
            <input v-model.number="form.price_per_hour" type="number" min="0" />
          </div>
          <div class="form-group">
            <label>Sucursal</label>
            <select v-model="form.branch_id">
              <option value="">Sin sucursal</option>
              <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Imágenes (URLs separadas por coma)</label>
          <input v-model="imagesInput" type="text" placeholder="https://... , https://..." />
        </div>
        <div class="form-group">
          <label>Amenidades (separadas por coma)</label>
          <input v-model="amenitiesInput" type="text" placeholder="Pista, Escenario, Sonido..." />
        </div>
        <div class="form-group">
          <label>URL del plano</label>
          <input v-model="form.floor_plan_url" type="url" />
        </div>
        <div class="form-group" style="display:flex;align-items:center;gap:.75rem">
          <input v-model="form.is_active" type="checkbox" id="is_active" style="width:auto" />
          <label for="is_active" style="margin:0">Espacio activo</label>
        </div>

        <div class="modal-footer">
          <button @click="showModal = false" class="btn btn-ghost">Cancelar</button>
          <button @click="saveSpace" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : (editing ? 'Actualizar' : 'Crear espacio') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const spaces = ref([])
const branches = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)

const form = ref({
  name: '', description: '', capacity: 100, price_per_hour: 0, price_event: 0,
  images_json: null, amenities_json: null, floor_plan_url: '', branch_id: '', is_active: true
})
const imagesInput = ref('')
const amenitiesInput = ref('')

function firstImage(s) {
  try { return JSON.parse(s.images_json || '[]')[0] || null } catch { return null }
}

function amenities(s) {
  try { return JSON.parse(s.amenities_json || '[]') } catch { return [] }
}

async function loadSpaces() {
  loading.value = true
  try {
    const [spacesRes, branchesRes] = await Promise.all([
      api.get('/spaces/'),
      api.get('/venues/me/branches'),
    ])
    spaces.value = spacesRes.data
    branches.value = branchesRes.data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = { name: '', description: '', capacity: 100, price_per_hour: 0, price_event: 0, images_json: null, amenities_json: null, floor_plan_url: '', branch_id: '', is_active: true }
  imagesInput.value = ''
  amenitiesInput.value = ''
  showModal.value = true
}

function editSpace(s) {
  editing.value = s.id
  form.value = { ...s, branch_id: s.branch_id || '' }
  try { imagesInput.value = JSON.parse(s.images_json || '[]').join(', ') } catch { imagesInput.value = '' }
  try { amenitiesInput.value = JSON.parse(s.amenities_json || '[]').join(', ') } catch { amenitiesInput.value = '' }
  showModal.value = true
}

async function saveSpace() {
  saving.value = true
  try {
    const payload = { ...form.value }
    payload.images_json = imagesInput.value ? JSON.stringify(imagesInput.value.split(',').map(s => s.trim()).filter(Boolean)) : null
    payload.amenities_json = amenitiesInput.value ? JSON.stringify(amenitiesInput.value.split(',').map(s => s.trim()).filter(Boolean)) : null
    if (!payload.branch_id) payload.branch_id = null

    if (editing.value) {
      await api.put(`/spaces/${editing.value}`, payload)
    } else {
      await api.post('/spaces/', payload)
    }
    showModal.value = false
    await loadSpaces()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al guardar espacio')
  } finally {
    saving.value = false
  }
}

async function deleteSpace(s) {
  if (!confirm(`¿Eliminar "${s.name}"?`)) return
  try {
    await api.delete(`/spaces/${s.id}`)
    await loadSpaces()
  } catch (e) {
    alert('Error al eliminar')
  }
}

onMounted(loadSpaces)
</script>

<style scoped>
.spaces-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.space-card { padding: 0; overflow: hidden; }

.space-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.space-img-placeholder {
  height: 100px;
  background: var(--bg2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.space-body { padding: 1.25rem; }

.space-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.space-header h3 { font-size: 1rem; font-weight: 700; }

.badge-active { background: rgba(16,185,129,0.2); color: #34d399; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.75rem; }
.badge-inactive { background: rgba(239,68,68,0.2); color: #f87171; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.75rem; }

.space-desc {
  font-size: 0.82rem;
  color: var(--text2);
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.space-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.82rem;
  color: var(--accent);
  font-weight: 600;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.space-amenities {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.chip-sm {
  background: rgba(255,255,255,0.05);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  color: var(--text2);
}

.space-actions { display: flex; gap: 0.5rem; }

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
</style>
