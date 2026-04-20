<template>
  <div>
    <div class="page-header">
      <div class="header-row">
        <div>
          <h1>Inventario</h1>
          <p>Gestión de productos y niveles de stock</p>
        </div>
        <button class="btn btn-primary" @click="showAdd = true">+ Nuevo producto</button>
      </div>
    </div>

    <div class="page-body">
      <!-- Alerts -->
      <div v-if="lowStockProducts.length > 0" class="alert-banner">
        <span>⚠️</span>
        <span><strong>{{ lowStockProducts.length }} producto(s)</strong> con stock bajo el mínimo</span>
      </div>

      <div class="card">
        <div class="table-toolbar">
          <input v-model="search" placeholder="🔍 Buscar..." style="max-width: 280px" />
          <select v-model="filterCat" style="max-width: 180px">
            <option value="">Todas las categorías</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
          <select v-model="filterStock" style="max-width: 160px">
            <option value="">Todo el stock</option>
            <option value="low">Stock bajo</option>
            <option value="ok">Stock OK</option>
            <option value="zero">Sin stock</option>
          </select>
        </div>

        <div v-if="loading" class="empty-state">Cargando...</div>
        <table v-else>
          <thead>
            <tr>
              <th>Producto</th>
              <th>SKU</th>
              <th>Categoría</th>
              <th>Precio</th>
              <th>Costo</th>
              <th>Stock</th>
              <th>Mínimo</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in filteredProducts" :key="p.id">
              <td><span class="product-name-cell">{{ p.name }}</span></td>
              <td><code class="sku">{{ p.sku }}</code></td>
              <td>
                <span v-if="p.category_name" class="badge" :style="{ background: p.category_color + '22', color: p.category_color }">
                  {{ p.category_name }}
                </span>
              </td>
              <td>${{ p.price.toFixed(2) }}</td>
              <td>${{ p.cost.toFixed(2) }}</td>
              <td>
                <span class="stock-num" :class="{ danger: p.low_stock, zero: p.stock === 0 }">{{ p.stock }}</span>
              </td>
              <td>{{ p.min_stock }}</td>
              <td>
                <span class="badge" :class="p.stock === 0 ? 'badge-danger' : p.low_stock ? 'badge-warning' : 'badge-success'">
                  {{ p.stock === 0 ? 'Sin stock' : p.low_stock ? 'Bajo' : 'OK' }}
                </span>
              </td>
              <td>
                <div class="action-btns">
                  <button class="btn btn-ghost btn-xs" @click="openAdjust(p)">📦 Ajustar</button>
                  <button class="btn btn-ghost btn-xs" @click="openEdit(p)">✏️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Adjust Stock Modal -->
    <div v-if="adjustProduct" class="modal-overlay" @click.self="adjustProduct = null">
      <div class="modal">
        <h3>Ajustar Stock — {{ adjustProduct.name }}</h3>
        <p class="modal-sub">Stock actual: <strong>{{ adjustProduct.stock }}</strong> unidades</p>
        <div class="form-group">
          <label>Cambio de cantidad (+ para agregar, - para quitar)</label>
          <input v-model.number="adjustQty" type="number" placeholder="ej. 10 o -5" />
        </div>
        <div class="form-group">
          <label>Motivo</label>
          <select v-model="adjustReason">
            <option value="adjustment">Ajuste</option>
            <option value="purchase">Compra</option>
            <option value="return">Devolución</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="adjustProduct = null">Cancelar</button>
          <button class="btn btn-primary" @click="submitAdjust">Guardar</button>
        </div>
      </div>
    </div>

    <!-- Add Product Modal -->
    <div v-if="showAdd" class="modal-overlay" @click.self="showAdd = false">
      <div class="modal modal-lg">
        <h3>Nuevo Producto</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>Nombre</label>
            <input v-model="newProd.name" />
          </div>
          <div class="form-group">
            <label>SKU</label>
            <input v-model="newProd.sku" />
          </div>
          <div class="form-group">
            <label>Categoría</label>
            <select v-model="newProd.category_id">
              <option :value="null">Sin categoría</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Precio venta</label>
            <input v-model.number="newProd.price" type="number" />
          </div>
          <div class="form-group">
            <label>Costo</label>
            <input v-model.number="newProd.cost" type="number" />
          </div>
          <div class="form-group">
            <label>Stock inicial</label>
            <input v-model.number="newProd.stock" type="number" />
          </div>
          <div class="form-group">
            <label>Stock mínimo</label>
            <input v-model.number="newProd.min_stock" type="number" />
          </div>
          <div class="form-group" style="grid-column: span 2">
            <label>Descripción</label>
            <textarea v-model="newProd.description" rows="2" />
          </div>
        </div>
        <p v-if="addError" class="error-msg">{{ addError }}</p>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="showAdd = false">Cancelar</button>
          <button class="btn btn-primary" @click="submitAdd">Crear producto</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index.js'

const products = ref([])
const categories = ref([])
const loading = ref(false)
const search = ref('')
const filterCat = ref('')
const filterStock = ref('')
const adjustProduct = ref(null)
const adjustQty = ref(0)
const adjustReason = ref('adjustment')
const showAdd = ref(false)
const addError = ref('')
const newProd = ref({ name: '', sku: '', category_id: null, price: 0, cost: 0, stock: 0, min_stock: 5, description: '' })

const lowStockProducts = computed(() => products.value.filter(p => p.low_stock))

const filteredProducts = computed(() => {
  let list = products.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(p => p.name.toLowerCase().includes(q) || p.sku.toLowerCase().includes(q))
  }
  if (filterCat.value) list = list.filter(p => p.category_id == filterCat.value)
  if (filterStock.value === 'low') list = list.filter(p => p.low_stock && p.stock > 0)
  else if (filterStock.value === 'ok') list = list.filter(p => !p.low_stock)
  else if (filterStock.value === 'zero') list = list.filter(p => p.stock === 0)
  return list
})

function openAdjust(p) {
  adjustProduct.value = p
  adjustQty.value = 0
  adjustReason.value = 'adjustment'
}

function openEdit(p) {
  // Simple: re-open adjust for now; in production would open edit form
  openAdjust(p)
}

async function submitAdjust() {
  if (!adjustQty.value) return
  await api.post(`/products/${adjustProduct.value.id}/adjust-stock`, {
    change_qty: adjustQty.value,
    reason: adjustReason.value,
  })
  adjustProduct.value = null
  await loadProducts()
}

async function submitAdd() {
  addError.value = ''
  try {
    await api.post('/products/', newProd.value)
    showAdd.value = false
    newProd.value = { name: '', sku: '', category_id: null, price: 0, cost: 0, stock: 0, min_stock: 5, description: '' }
    await loadProducts()
  } catch (e) {
    addError.value = e.response?.data?.detail || 'Error al crear producto'
  }
}

async function loadProducts() {
  loading.value = true
  try {
    const [pRes, catRes] = await Promise.all([
      api.get('/products/all'),
      api.get('/products/categories/list'),
    ])
    products.value = pRes.data
    categories.value = catRes.data
  } finally {
    loading.value = false
  }
}

onMounted(loadProducts)
</script>

<style scoped>
.header-row { display: flex; align-items: flex-start; justify-content: space-between; }
.table-toolbar { display: flex; gap: 12px; margin-bottom: 16px; }
.alert-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(245,158,11,0.1);
  border: 1px solid rgba(245,158,11,0.3);
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 16px;
  font-size: 14px;
  color: var(--warning);
}
.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }
.product-name-cell { font-weight: 600; }
.sku { background: var(--bg3); padding: 2px 7px; border-radius: 4px; font-size: 12px; }
.stock-num { font-weight: 700; font-size: 15px; color: var(--success); }
.stock-num.danger { color: var(--warning); }
.stock-num.zero { color: var(--danger); }
.action-btns { display: flex; gap: 6px; }
.btn-xs { padding: 4px 10px; font-size: 12px; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.7);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 14px; padding: 28px; width: 400px;
}
.modal-lg { width: 600px; }
.modal h3 { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
.modal-sub { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 5px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }
.error-msg { color: var(--danger); font-size: 13px; margin-bottom: 10px; }
</style>
