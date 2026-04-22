<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { itemsApi, exportsApi, locationsApi } from '../api/endpoints'

const items = ref([])
const locations = ref([])
const q = ref('')
const loading = ref(false)
const showNew = ref(false)
const emptyForm = () => ({
  sku: '', name: '', unit: 'pieza', barcode: '',
  min_stock: 0, max_stock: 0, cost: 0, price: 0,
  initial_qty: 0, initial_location_id: '',
})
const form = ref(emptyForm())
const saveError = ref(null)

async function load() {
  loading.value = true
  try {
    const [i, l] = await Promise.all([
      itemsApi.list({ q: q.value || undefined }),
      locationsApi.list(),
    ])
    items.value = i.data
    locations.value = l.data
  } finally { loading.value = false }
}

async function create() {
  saveError.value = null
  try {
    const body = { ...form.value }
    if (!body.initial_location_id) body.initial_location_id = null
    if (!body.initial_qty) body.initial_qty = 0
    await itemsApi.create(body)
    form.value = emptyForm()
    showNew.value = false
    load()
  } catch (e) {
    saveError.value = e?.response?.data?.detail || e.message || 'Error al guardar'
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1>Catálogo</h1>
        <p class="muted">Todos los artículos de tu tenant.</p>
      </div>
      <div class="actions">
        <button class="btn btn-sm" @click="exportsApi.inventory()"><i class="mdi mdi-file-excel"></i> Exportar Excel</button>
        <button class="btn btn-primary btn-sm" @click="showNew = !showNew"><i class="mdi mdi-plus"></i> Nuevo artículo</button>
      </div>
    </div>

    <div class="card" v-if="showNew" style="margin-bottom:20px;">
      <h3 style="margin:0 0 16px;">Nuevo artículo</h3>
      <div class="grid-3">
        <div><label>SKU *</label><input v-model="form.sku" placeholder="SKU-001" /></div>
        <div><label>Nombre *</label><input v-model="form.name" placeholder="Nombre visible" /></div>
        <div><label>Unidad</label>
          <select v-model="form.unit">
            <option>pieza</option><option>kg</option><option>l</option><option>caja</option>
            <option>m</option><option>m2</option><option>m3</option><option>par</option><option>bulto</option>
          </select>
        </div>
        <div><label>Código de barras</label><input v-model="form.barcode" placeholder="7501... (opcional)" /></div>
        <div><label>Mínimo</label><input type="number" step="0.001" v-model.number="form.min_stock" /></div>
        <div><label>Máximo</label><input type="number" step="0.001" v-model.number="form.max_stock" /></div>
        <div><label>Costo (MXN)</label><input type="number" step="0.01" v-model.number="form.cost" /></div>
        <div><label>Precio (MXN)</label><input type="number" step="0.01" v-model.number="form.price" /></div>
        <div></div>
      </div>
      <div class="initial-stock">
        <h4 style="margin:0 0 10px;"><i class="mdi mdi-package-down"></i> Stock inicial (opcional)</h4>
        <div class="grid-2">
          <div><label>Cantidad inicial</label><input type="number" step="0.001" v-model.number="form.initial_qty" placeholder="0" /></div>
          <div><label>Ubicación</label>
            <select v-model="form.initial_location_id">
              <option value="">— (sin stock inicial)</option>
              <option v-for="l in locations" :key="l.id" :value="l.id">{{ l.path || l.name }}</option>
            </select>
          </div>
        </div>
        <p class="muted" style="font-size:12px; margin:8px 0 0;">
          Si indicas cantidad + ubicación, se registrará un movimiento IN al crear el artículo.
        </p>
      </div>
      <div v-if="saveError" class="badge danger" style="margin-top:10px;">{{ saveError }}</div>
      <div style="margin-top:16px; display:flex; gap:8px;">
        <button class="btn btn-primary" :disabled="!form.sku || !form.name" @click="create">
          <i class="mdi mdi-content-save"></i> Guardar
        </button>
        <button class="btn" @click="showNew=false">Cancelar</button>
      </div>
    </div>

    <div style="margin-bottom:14px; display:flex; gap:12px; align-items:center;">
      <input v-model="q" placeholder="Buscar por nombre, SKU o código…" @input="load" style="max-width:420px;" />
      <span class="muted" style="font-size:13px;">{{ items.length }} resultados</span>
    </div>

    <div class="card" style="padding:0; overflow:auto;">
      <table class="table">
        <thead>
          <tr>
            <th>SKU</th><th>Nombre</th><th>Unidad</th><th>Barcode</th>
            <th>Mín</th><th>Máx</th><th>Costo</th><th>Precio</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in items" :key="i.id">
            <td class="mono">{{ i.sku }}</td>
            <td>{{ i.name }}</td>
            <td>{{ i.unit }}</td>
            <td class="mono muted">{{ i.barcode || '—' }}</td>
            <td>{{ i.min_stock }}</td>
            <td>{{ i.max_stock }}</td>
            <td>${{ Number(i.cost).toLocaleString('es-MX') }}</td>
            <td>${{ Number(i.price).toLocaleString('es-MX') }}</td>
          </tr>
          <tr v-if="!items.length && !loading"><td colspan="8" class="muted" style="text-align:center; padding:40px;">Sin artículos. Crea el primero.</td></tr>
          <tr v-if="loading"><td colspan="8" class="muted" style="text-align:center;"><i class="mdi mdi-loading mdi-spin"></i> Cargando…</td></tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.actions { display: flex; gap: 8px; }
.initial-stock { margin-top: 20px; padding-top: 20px; border-top: 1px dashed var(--border); }
.initial-stock h4 { font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: .06em; display: flex; align-items: center; gap: 6px; }
</style>
