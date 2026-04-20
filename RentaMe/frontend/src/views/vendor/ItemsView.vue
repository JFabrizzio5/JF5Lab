<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <div class="page-header">
        <div>
          <h1 class="page-title">Artículos</h1>
          <p class="page-subtitle">Gestiona tu catálogo de artículos en renta</p>
        </div>
        <button class="btn btn-primary" @click="openCreate">+ Agregar artículo</button>
      </div>

      <div v-if="loading" class="loading">Cargando artículos...</div>

      <div v-else-if="items.length === 0" class="empty-state card">
        <div class="empty-icon">📦</div>
        <h3>Sin artículos aún</h3>
        <p>Agrega tu primer artículo para empezar a recibir solicitudes de renta.</p>
        <button class="btn btn-primary" @click="openCreate" style="margin-top: 16px;">+ Agregar artículo</button>
      </div>

      <div v-else class="items-grid">
        <div v-for="item in items" :key="item.id" class="item-card" :class="{ inactive: !item.is_active }">
          <div class="item-img">
            <img v-if="item.images?.[0]" :src="item.images[0]" :alt="item.name" />
            <div v-else class="item-no-img">{{ catIcon(item.category) }}</div>
            <span v-if="item.is_featured" class="featured-tag">⭐ Destacado</span>
            <span v-if="!item.is_active" class="inactive-tag">Inactivo</span>
          </div>
          <div class="item-body">
            <div class="item-cat">{{ catLabel(item.category) }}</div>
            <h3 class="item-name">{{ item.name }}</h3>
            <div class="item-prices">
              <span v-if="item.price_per_hour" class="price-chip">${{ fmt(item.price_per_hour) }}/hr</span>
              <span v-if="item.price_per_day" class="price-chip primary">${{ fmt(item.price_per_day) }}/día</span>
              <span v-if="item.price_per_weekend" class="price-chip">${{ fmt(item.price_per_weekend) }}/fds</span>
              <span v-if="item.price_per_week" class="price-chip">${{ fmt(item.price_per_week) }}/sem</span>
            </div>
            <div class="item-meta">
              <span>Cantidad: {{ item.quantity }}</span>
            </div>
          </div>
          <div class="item-actions">
            <button class="btn btn-secondary btn-sm" @click="openEdit(item)">Editar</button>
            <button class="btn btn-danger btn-sm" @click="deleteItem(item)">Eliminar</button>
          </div>
        </div>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal modal-lg">
          <div class="modal-header">
            <h2 class="modal-title">{{ editingItem ? 'Editar artículo' : 'Nuevo artículo' }}</h2>
            <button class="modal-close" @click="closeModal">×</button>
          </div>

          <form @submit.prevent="saveItem" class="item-form">
            <div class="form-grid">
              <div class="form-group">
                <label class="label">Nombre del artículo *</label>
                <input v-model="form.name" type="text" class="input" placeholder="Ej: Lancha 20ft" required />
              </div>
              <div class="form-group">
                <label class="label">Categoría</label>
                <select v-model="form.category" class="input">
                  <option v-for="cat in CATEGORIES" :key="cat.key" :value="cat.key">{{ cat.icon }} {{ cat.label }}</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="label">Descripción</label>
              <textarea v-model="form.description" class="input" rows="3" placeholder="Describe el artículo, sus características principales..."></textarea>
            </div>

            <!-- Images -->
            <div class="form-group">
              <label class="label">Imágenes (URLs, máx 6)</label>
              <div class="images-grid">
                <div v-for="(url, idx) in imageUrls" :key="idx" class="image-input-row">
                  <input v-model="imageUrls[idx]" type="url" class="input" :placeholder="`URL imagen ${idx + 1}`" />
                  <div v-if="imageUrls[idx]" class="img-preview">
                    <img :src="imageUrls[idx]" :alt="`img${idx}`" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Pricing -->
            <div class="form-group">
              <label class="label">Precios</label>
              <div class="pricing-grid">
                <div class="price-option">
                  <label class="price-check">
                    <input type="checkbox" v-model="priceEnabled.hour" />
                    <span>Por hora</span>
                  </label>
                  <input v-if="priceEnabled.hour" v-model.number="form.price_per_hour" type="number" class="input" placeholder="$0.00" min="0" step="0.01" />
                </div>
                <div class="price-option">
                  <label class="price-check">
                    <input type="checkbox" v-model="priceEnabled.day" />
                    <span>Por día</span>
                  </label>
                  <input v-if="priceEnabled.day" v-model.number="form.price_per_day" type="number" class="input" placeholder="$0.00" min="0" step="0.01" />
                </div>
                <div class="price-option">
                  <label class="price-check">
                    <input type="checkbox" v-model="priceEnabled.weekend" />
                    <span>Fin de semana</span>
                  </label>
                  <input v-if="priceEnabled.weekend" v-model.number="form.price_per_weekend" type="number" class="input" placeholder="$0.00" min="0" step="0.01" />
                </div>
                <div class="price-option">
                  <label class="price-check">
                    <input type="checkbox" v-model="priceEnabled.week" />
                    <span>Por semana</span>
                  </label>
                  <input v-if="priceEnabled.week" v-model.number="form.price_per_week" type="number" class="input" placeholder="$0.00" min="0" step="0.01" />
                </div>
              </div>
            </div>

            <div class="form-grid-3">
              <div class="form-group">
                <label class="label">Cantidad disponible</label>
                <input v-model.number="form.quantity" type="number" class="input" min="1" />
              </div>
              <div class="form-group">
                <label class="label">Horas mínimas</label>
                <input v-model.number="form.min_rental_hours" type="number" class="input" min="1" />
              </div>
              <div class="form-group">
                <label class="label">Días de anticipación</label>
                <input v-model.number="form.advance_booking_days" type="number" class="input" min="0" />
              </div>
            </div>

            <div class="form-group">
              <label class="label">Depósito fijo (sobrescribe % del vendedor)</label>
              <input v-model.number="form.deposit_amount" type="number" class="input" min="0" step="0.01" placeholder="0.00" />
            </div>

            <!-- Specifications -->
            <div class="form-group">
              <label class="label">Especificaciones (clave: valor)</label>
              <div v-for="(spec, idx) in specs" :key="idx" class="spec-row-input">
                <input v-model="spec.key" type="text" class="input" placeholder="Clave (ej: Capacidad)" />
                <input v-model="spec.value" type="text" class="input" placeholder="Valor (ej: 6 personas)" />
                <button type="button" class="remove-btn" @click="specs.splice(idx, 1)">×</button>
              </div>
              <button type="button" class="btn btn-secondary btn-sm" @click="specs.push({ key: '', value: '' })">+ Agregar</button>
            </div>

            <!-- Included -->
            <div class="form-grid">
              <div class="form-group">
                <label class="label">Incluye</label>
                <div v-for="(item, idx) in includedList" :key="idx" class="list-input-row">
                  <input v-model="includedList[idx]" type="text" class="input" placeholder="Ej: Chaleco salvavidas" />
                  <button type="button" class="remove-btn" @click="includedList.splice(idx, 1)">×</button>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" @click="includedList.push('')">+ Agregar</button>
              </div>
              <div class="form-group">
                <label class="label">No incluye</label>
                <div v-for="(item, idx) in notIncludedList" :key="idx" class="list-input-row">
                  <input v-model="notIncludedList[idx]" type="text" class="input" placeholder="Ej: Combustible" />
                  <button type="button" class="remove-btn" @click="notIncludedList.splice(idx, 1)">×</button>
                </div>
                <button type="button" class="btn btn-secondary btn-sm" @click="notIncludedList.push('')">+ Agregar</button>
              </div>
            </div>

            <div class="form-group">
              <label class="label">Requisitos</label>
              <textarea v-model="form.requirements" class="input" rows="2" placeholder="Ej: Se requiere licencia náutica..."></textarea>
            </div>

            <div class="form-options">
              <label class="toggle-label">
                <input type="checkbox" v-model="form.is_featured" />
                <span>⭐ Artículo destacado</span>
              </label>
            </div>

            <div v-if="saveError" class="error-msg">{{ saveError }}</div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Guardando...' : (editingItem ? 'Guardar cambios' : 'Crear artículo') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { itemsAPI } from '../../api/index.js'

const CATEGORIES = [
  { key: 'boats', icon: '⛵', label: 'Barcos' },
  { key: 'vehicles', icon: '🚗', label: 'Vehículos' },
  { key: 'furniture', icon: '🪑', label: 'Muebles' },
  { key: 'party', icon: '🎉', label: 'Fiestas' },
  { key: 'sports', icon: '⚽', label: 'Deportes' },
  { key: 'housing', icon: '🏠', label: 'Inmuebles' },
  { key: 'equipment', icon: '🔧', label: 'Equipo' },
  { key: 'other', icon: '📦', label: 'Otro' },
]

const items = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingItem = ref(null)
const saving = ref(false)
const saveError = ref('')

const form = ref({})
const priceEnabled = ref({})
const imageUrls = ref(['', '', '', '', '', ''])
const specs = ref([])
const includedList = ref([])
const notIncludedList = ref([])

function fmt(n) { return Number(n || 0).toLocaleString('es-MX') }
function catLabel(cat) { return CATEGORIES.find(c => c.key === cat)?.label || cat }
function catIcon(cat) { return CATEGORIES.find(c => c.key === cat)?.icon || '📦' }

function resetForm() {
  form.value = {
    name: '',
    description: '',
    category: 'general',
    price_per_hour: null,
    price_per_day: null,
    price_per_weekend: null,
    price_per_week: null,
    quantity: 1,
    min_rental_hours: 1,
    advance_booking_days: 0,
    deposit_amount: 0,
    is_featured: false,
    requirements: '',
  }
  priceEnabled.value = { hour: false, day: true, weekend: false, week: false }
  imageUrls.value = ['', '', '', '', '', '']
  specs.value = []
  includedList.value = []
  notIncludedList.value = []
}

function openCreate() {
  editingItem.value = null
  resetForm()
  showModal.value = true
  saveError.value = ''
}

function openEdit(item) {
  editingItem.value = item
  form.value = {
    name: item.name,
    description: item.description || '',
    category: item.category,
    price_per_hour: item.price_per_hour,
    price_per_day: item.price_per_day,
    price_per_weekend: item.price_per_weekend,
    price_per_week: item.price_per_week,
    quantity: item.quantity,
    min_rental_hours: item.min_rental_hours,
    advance_booking_days: item.advance_booking_days,
    deposit_amount: item.deposit_amount,
    is_featured: item.is_featured,
    requirements: item.requirements || '',
    is_active: item.is_active,
  }
  priceEnabled.value = {
    hour: !!item.price_per_hour,
    day: !!item.price_per_day,
    weekend: !!item.price_per_weekend,
    week: !!item.price_per_week,
  }
  const imgs = item.images || []
  imageUrls.value = [...imgs, ...Array(6 - imgs.length).fill('')].slice(0, 6)
  const specObj = item.specifications || {}
  specs.value = Object.entries(specObj).map(([key, value]) => ({ key, value }))
  includedList.value = [...(item.included || [])]
  notIncludedList.value = [...(item.not_included || [])]
  showModal.value = true
  saveError.value = ''
}

function closeModal() {
  showModal.value = false
  editingItem.value = null
}

async function saveItem() {
  saving.value = true
  saveError.value = ''
  try {
    const images = imageUrls.value.filter(Boolean)
    const specsObj = {}
    specs.value.filter(s => s.key).forEach(s => { specsObj[s.key] = s.value })

    const payload = {
      ...form.value,
      price_per_hour: priceEnabled.value.hour ? form.value.price_per_hour : null,
      price_per_day: priceEnabled.value.day ? form.value.price_per_day : null,
      price_per_weekend: priceEnabled.value.weekend ? form.value.price_per_weekend : null,
      price_per_week: priceEnabled.value.week ? form.value.price_per_week : null,
      images_json: JSON.stringify(images),
      specifications_json: JSON.stringify(specsObj),
      included_json: JSON.stringify(includedList.value.filter(Boolean)),
      not_included_json: JSON.stringify(notIncludedList.value.filter(Boolean)),
    }

    if (editingItem.value) {
      await itemsAPI.update(editingItem.value.id, payload)
    } else {
      await itemsAPI.create(payload)
    }
    await loadItems()
    closeModal()
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Error al guardar'
  } finally {
    saving.value = false
  }
}

async function deleteItem(item) {
  if (!confirm(`¿Eliminar "${item.name}"? El artículo quedará inactivo.`)) return
  try {
    await itemsAPI.delete(item.id)
    await loadItems()
  } catch (e) {
    alert('Error al eliminar')
  }
}

async function loadItems() {
  try {
    const res = await itemsAPI.list()
    items.value = res.data
  } catch {}
  loading.value = false
}

onMounted(loadItems)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}
.loading { text-align: center; padding: 60px; color: var(--text2); }
.empty-state {
  text-align: center;
  padding: 60px;
}
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty-state h3 { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.empty-state p { color: var(--text2); }

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.item-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  transition: border-color 0.2s;
}
.item-card:hover { border-color: var(--border2); }
.item-card.inactive { opacity: 0.6; }

.item-img {
  position: relative;
  height: 180px;
  overflow: hidden;
}
.item-img img { width: 100%; height: 100%; object-fit: cover; }
.item-no-img {
  width: 100%;
  height: 100%;
  background: var(--bg3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
}
.featured-tag {
  position: absolute;
  top: 8px;
  left: 8px;
  background: var(--accent);
  color: #07070d;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
}
.inactive-tag {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(100,116,139,0.8);
  color: white;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.item-body { padding: 14px; }
.item-cat { font-size: 11px; color: var(--text2); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
.item-name { font-size: 16px; font-weight: 700; margin-bottom: 10px; }
.item-prices { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.price-chip {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 3px 10px;
  font-size: 12px;
  color: var(--text3);
}
.price-chip.primary { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.3); color: #818cf8; }
.item-meta { font-size: 12px; color: var(--text2); }
.item-actions {
  padding: 12px 14px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 8px;
}

/* Form */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
.item-form { display: flex; flex-direction: column; gap: 16px; }

.images-grid { display: flex; flex-direction: column; gap: 8px; }
.image-input-row { display: flex; align-items: center; gap: 8px; }
.img-preview { width: 48px; height: 48px; flex-shrink: 0; }
.img-preview img { width: 100%; height: 100%; object-fit: cover; border-radius: 6px; }

.pricing-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.price-option { display: flex; flex-direction: column; gap: 6px; }
.price-check {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text3);
}
.price-check input[type="checkbox"] { width: 14px; height: 14px; }

.spec-row-input { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.list-input-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.remove-btn {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text2);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  transition: all 0.2s;
}
.remove-btn:hover { color: var(--danger); border-color: var(--danger); }

.form-options {
  display: flex;
  gap: 20px;
}
.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text3);
}

.error-msg {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #f87171;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}

@media (max-width: 768px) {
  .form-grid, .form-grid-3, .pricing-grid { grid-template-columns: 1fr; }
}
</style>
