<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Plano de Stands</h1>
        <button @click="addNew" class="btn btn-primary">+ Agregar Stand</button>
      </div>

      <div class="stands-workspace">
        <!-- Floor Plan -->
        <div class="floor-plan-panel">
          <div class="floor-header">Plano Interactivo</div>
          <div class="floor-legend">
            <span class="leg available">Disponible</span>
            <span class="leg reserved">Reservado</span>
            <span class="leg sold">Vendido</span>
          </div>
          <div class="floor-plan">
            <div
              v-for="stand in stands"
              :key="stand.id"
              class="stand-box"
              :class="[stand.status, { selected: selectedStand?.id === stand.id }]"
              :style="`left:${stand.x_pos || 5}%;top:${stand.y_pos || 5}%;width:${stand.width || 8}%;height:${stand.height || 8}%;`"
              @click="selectStand(stand)"
            >
              <div class="sb-num">{{ stand.number }}</div>
              <div class="sb-name" v-if="stand.name">{{ stand.name.slice(0, 12) }}</div>
            </div>
          </div>
        </div>

        <!-- Detail Form -->
        <div class="stand-detail-panel" v-if="selectedStand || isNew">
          <div class="detail-header">
            <h3>{{ isNew ? 'Nuevo Stand' : `Stand ${selectedStand?.number}` }}</h3>
            <button @click="cancelEdit" class="btn btn-ghost btn-sm">✕ Cancelar</button>
          </div>
          <div class="detail-form">
            <div class="form-group"><label>Número *</label><input v-model="form.number" placeholder="A-01" /></div>
            <div class="form-group"><label>Nombre del exhibidor</label><input v-model="form.name" /></div>
            <div class="form-group"><label>Categoría</label>
              <select v-model="form.category">
                <option value="general">General</option>
                <option value="gaming">Gaming</option>
                <option value="merch">Merchandise</option>
                <option value="food">Alimentos</option>
                <option value="sponsor">Patrocinador</option>
              </select>
            </div>
            <div class="form-group"><label>Tamaño</label>
              <select v-model="form.size">
                <option value="small">Pequeño</option>
                <option value="standard">Estándar</option>
                <option value="large">Grande</option>
                <option value="premium">Premium</option>
              </select>
            </div>
            <div class="form-group"><label>Precio (MXN)</label><input v-model.number="form.price" type="number" /></div>
            <div class="form-group"><label>Estado</label>
              <select v-model="form.status">
                <option value="available">Disponible</option>
                <option value="reserved">Reservado</option>
                <option value="sold">Vendido</option>
                <option value="complimentary">Cortesía</option>
              </select>
            </div>
            <div class="pos-row">
              <div class="form-group"><label>X (%)</label><input v-model.number="form.x_pos" type="number" min="0" max="90" /></div>
              <div class="form-group"><label>Y (%)</label><input v-model.number="form.y_pos" type="number" min="0" max="90" /></div>
              <div class="form-group"><label>Ancho (%)</label><input v-model.number="form.width" type="number" min="3" max="30" /></div>
              <div class="form-group"><label>Alto (%)</label><input v-model.number="form.height" type="number" min="3" max="30" /></div>
            </div>
            <div class="form-group"><label>Contacto (nombre)</label><input v-model="form.contact_name" /></div>
            <div class="form-group"><label>Contacto (email)</label><input v-model="form.contact_email" type="email" /></div>
            <div class="form-group"><label>Contacto (teléfono)</label><input v-model="form.contact_phone" /></div>
            <div class="form-group"><label>Descripción</label><textarea v-model="form.description" rows="2"></textarea></div>
            <div style="display:flex;gap:10px;margin-top:16px">
              <button v-if="!isNew" @click="deleteStand" class="btn btn-danger btn-sm">Eliminar</button>
              <button @click="saveStand" class="btn btn-primary" style="flex:1">Guardar</button>
            </div>
          </div>
        </div>

        <div class="stand-detail-panel hint" v-else>
          <div class="hint-icon">👆</div>
          <p>Haz clic en un stand para editarlo</p>
        </div>
      </div>

      <!-- Stands table -->
      <div class="stands-table-section">
        <h2>Todos los Stands</h2>
        <table>
          <thead><tr><th>Núm.</th><th>Nombre</th><th>Categoría</th><th>Tamaño</th><th>Precio</th><th>Estado</th><th>Contacto</th></tr></thead>
          <tbody>
            <tr v-for="s in stands" :key="s.id" @click="selectStand(s)" :class="{ 'row-selected': selectedStand?.id === s.id }">
              <td>{{ s.number }}</td>
              <td>{{ s.name || '—' }}</td>
              <td>{{ s.category }}</td>
              <td>{{ s.size }}</td>
              <td>${{ s.price.toFixed(0) }}</td>
              <td><span class="badge" :class="statusBadge(s.status)">{{ s.status }}</span></td>
              <td>{{ s.contact_name || s.contact_email || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const stands = ref([])
const selectedStand = ref(null)
const isNew = ref(false)
const form = ref({})

function defaultForm() {
  return { number: '', name: '', category: 'general', size: 'standard', price: 0, status: 'available', x_pos: 5, y_pos: 5, width: 8, height: 8, contact_name: '', contact_email: '', contact_phone: '', description: '' }
}

function statusBadge(s) {
  if (s === 'available') return 'badge-success'
  if (s === 'reserved') return 'badge-warning'
  if (s === 'sold') return 'badge-danger'
  return 'badge-primary'
}

function selectStand(s) {
  selectedStand.value = s
  isNew.value = false
  form.value = { ...s }
}

function addNew() {
  selectedStand.value = null
  isNew.value = true
  form.value = defaultForm()
}

function cancelEdit() {
  selectedStand.value = null
  isNew.value = false
}

async function saveStand() {
  const payload = { ...form.value, convention_id: conv.value.id }
  if (isNew.value) {
    const { data } = await api.post('/stands/', payload)
    stands.value.push(data)
    selectedStand.value = data
    isNew.value = false
  } else {
    const { data } = await api.put(`/stands/${selectedStand.value.id}`, payload)
    const idx = stands.value.findIndex(s => s.id === data.id)
    if (idx >= 0) stands.value[idx] = data
    selectedStand.value = data
  }
}

async function deleteStand() {
  if (!confirm('¿Eliminar stand?')) return
  await api.delete(`/stands/${selectedStand.value.id}`)
  stands.value = stands.value.filter(s => s.id !== selectedStand.value.id)
  cancelEdit()
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  stands.value = await api.get(`/stands/convention/${conv.value.id}`).then(r => r.data)
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }

.stands-workspace { display: grid; grid-template-columns: 1fr 320px; gap: 20px; margin-bottom: 32px; }

.floor-plan-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.floor-header { padding: 14px 20px; font-weight: 700; border-bottom: 1px solid var(--border); }
.floor-legend { display: flex; gap: 12px; padding: 10px 20px; }
.leg { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 4px; }
.leg.available { background: rgba(16,185,129,0.15); color: #10b981; }
.leg.reserved { background: rgba(245,158,11,0.15); color: #f59e0b; }
.leg.sold { background: rgba(239,68,68,0.15); color: #ef4444; }

.floor-plan {
  position: relative;
  height: 400px;
  background: var(--bg3);
  background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 40px 40px;
}

.stand-box {
  position: absolute;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid;
  transition: all 0.15s;
  overflow: hidden;
}
.stand-box.available { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.4); }
.stand-box.reserved { background: rgba(245,158,11,0.15); border-color: rgba(245,158,11,0.4); }
.stand-box.sold { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.4); }
.stand-box.complimentary { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.4); }
.stand-box.selected { border-width: 3px; border-color: white !important; }
.stand-box:hover { filter: brightness(1.3); }

.sb-num { font-size: 10px; font-weight: 800; }
.sb-name { font-size: 8px; color: var(--text2); text-align: center; }

.stand-detail-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 20px; overflow-y: auto; max-height: 520px; }
.stand-detail-panel.hint { display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--text2); }
.hint-icon { font-size: 36px; margin-bottom: 12px; }
.detail-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.detail-header h3 { font-size: 16px; font-weight: 700; }
.detail-form { display: flex; flex-direction: column; gap: 12px; }
.pos-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }

.stands-table-section { margin-top: 8px; }
.stands-table-section h2 { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
.row-selected td { background: rgba(124,58,237,0.08); }
tr { cursor: pointer; }
</style>
