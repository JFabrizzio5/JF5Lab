<template>
  <div class="pos-layout">
    <!-- LEFT: Product grid -->
    <div class="pos-products">
      <div class="pos-toolbar">
        <input v-model="search" placeholder="🔍 Buscar producto..." class="search-input" />
        <div class="category-filters">
          <button
            class="cat-btn"
            :class="{ active: selectedCat === null }"
            @click="selectedCat = null"
          >Todos</button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="cat-btn"
            :class="{ active: selectedCat === cat.id }"
            :style="selectedCat === cat.id ? { background: cat.color + '22', borderColor: cat.color, color: cat.color } : {}"
            @click="selectedCat = cat.id"
          >{{ cat.name }}</button>
        </div>
      </div>

      <div v-if="loading" class="pos-empty">Cargando productos...</div>
      <div v-else-if="filteredProducts.length === 0" class="pos-empty">No se encontraron productos</div>
      <div v-else class="product-grid">
        <div
          v-for="p in filteredProducts"
          :key="p.id"
          class="product-card"
          :class="{ 'out-of-stock': p.stock === 0 }"
          @click="addToCart(p)"
        >
          <div class="product-img">{{ p.name[0] }}</div>
          <div class="product-info">
            <div class="product-name">{{ p.name }}</div>
            <div class="product-sku">{{ p.sku }}</div>
            <div class="product-bottom">
              <span class="product-price">${{ p.price.toFixed(2) }}</span>
              <span class="product-stock" :class="{ low: p.low_stock }">
                {{ p.stock }} uds
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT: Cart -->
    <div class="pos-cart">
      <div class="cart-header">
        <h2>Carrito</h2>
        <button v-if="cart.length > 0" class="btn btn-ghost btn-sm" @click="clearCart">🗑 Limpiar</button>
      </div>

      <!-- Customer selector -->
      <div class="cart-section">
        <label class="section-label">Cliente (opcional)</label>
        <select v-model="selectedCustomerId">
          <option :value="null">— Sin cliente —</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <!-- Cart items -->
      <div class="cart-items">
        <div v-if="cart.length === 0" class="cart-empty">
          <div style="font-size: 40px; margin-bottom: 8px">🛒</div>
          <p>Agrega productos al carrito</p>
        </div>
        <div v-else>
          <div v-for="(item, idx) in cart" :key="item.product_id" class="cart-item">
            <div class="cart-item-name">{{ item.name }}</div>
            <div class="cart-item-controls">
              <button class="qty-btn" @click="decreaseQty(idx)">−</button>
              <span class="qty-val">{{ item.quantity }}</span>
              <button class="qty-btn" @click="increaseQty(idx, item)">+</button>
            </div>
            <div class="cart-item-sub">${{ (item.unit_price * item.quantity).toFixed(2) }}</div>
            <button class="remove-btn" @click="removeItem(idx)">✕</button>
          </div>
        </div>
      </div>

      <!-- Totals -->
      <div class="cart-totals">
        <div class="total-row">
          <span>Subtotal</span>
          <span>${{ subtotal.toFixed(2) }}</span>
        </div>
        <div class="total-row">
          <span>IVA (16%)</span>
          <span>${{ tax.toFixed(2) }}</span>
        </div>
        <div class="total-row total-final">
          <span>Total</span>
          <span>${{ total.toFixed(2) }}</span>
        </div>
      </div>

      <!-- Payment method -->
      <div class="cart-section">
        <label class="section-label">Método de pago</label>
        <div class="payment-methods">
          <button
            v-for="m in paymentMethods"
            :key="m.value"
            class="pay-btn"
            :class="{ active: paymentMethod === m.value }"
            @click="paymentMethod = m.value"
          >{{ m.icon }} {{ m.label }}</button>
        </div>
      </div>

      <button
        class="btn btn-primary cobrar-btn"
        :disabled="cart.length === 0 || completing"
        @click="completeSale"
      >
        {{ completing ? 'Procesando...' : `💰 Cobrar $${total.toFixed(2)}` }}
      </button>

      <!-- Success ticket -->
      <div v-if="lastSale" class="ticket">
        <div class="ticket-header">✅ Venta #{{ lastSale.id }} completada</div>
        <div class="ticket-row" v-for="item in lastSale.items" :key="item.id">
          <span>{{ item.product_name }} x{{ item.quantity }}</span>
          <span>${{ item.subtotal.toFixed(2) }}</span>
        </div>
        <div class="ticket-total">Total: ${{ lastSale.total.toFixed(2) }}</div>
        <button class="btn btn-ghost btn-sm mt-8" @click="lastSale = null">Cerrar</button>
      </div>

      <p v-if="saleError" class="error-msg">{{ saleError }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index.js'

const search = ref('')
const selectedCat = ref(null)
const products = ref([])
const categories = ref([])
const customers = ref([])
const cart = ref([])
const selectedCustomerId = ref(null)
const paymentMethod = ref('cash')
const loading = ref(false)
const completing = ref(false)
const lastSale = ref(null)
const saleError = ref('')

const paymentMethods = [
  { value: 'cash', label: 'Efectivo', icon: '💵' },
  { value: 'card', label: 'Tarjeta', icon: '💳' },
  { value: 'transfer', label: 'Transferencia', icon: '📲' },
]

const filteredProducts = computed(() => {
  let list = products.value.filter(p => p.is_active)
  if (selectedCat.value !== null) list = list.filter(p => p.category_id === selectedCat.value)
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(p => p.name.toLowerCase().includes(q) || p.sku.toLowerCase().includes(q))
  }
  return list
})

const subtotal = computed(() => cart.value.reduce((s, i) => s + i.unit_price * i.quantity, 0))
const tax = computed(() => subtotal.value * 0.16)
const total = computed(() => subtotal.value + tax.value)

function addToCart(product) {
  if (product.stock === 0) return
  const existing = cart.value.find(i => i.product_id === product.id)
  if (existing) {
    if (existing.quantity < product.stock) existing.quantity++
  } else {
    cart.value.push({ product_id: product.id, name: product.name, unit_price: product.price, quantity: 1, stock: product.stock })
  }
}

function increaseQty(idx, item) {
  if (cart.value[idx].quantity < item.stock) cart.value[idx].quantity++
}

function decreaseQty(idx) {
  if (cart.value[idx].quantity <= 1) removeItem(idx)
  else cart.value[idx].quantity--
}

function removeItem(idx) { cart.value.splice(idx, 1) }
function clearCart() { cart.value = []; lastSale.value = null; saleError.value = '' }

async function completeSale() {
  saleError.value = ''
  completing.value = true
  try {
    const payload = {
      customer_id: selectedCustomerId.value,
      payment_method: paymentMethod.value,
      items: cart.value.map(i => ({
        product_id: i.product_id,
        quantity: i.quantity,
        unit_price: i.unit_price,
      })),
    }
    const res = await api.post('/sales/', payload)
    lastSale.value = res.data
    cart.value = []
    selectedCustomerId.value = null
    paymentMethod.value = 'cash'
    await loadProducts()
  } catch (e) {
    saleError.value = e.response?.data?.detail || 'Error al procesar la venta'
  } finally {
    completing.value = false
  }
}

async function loadProducts() {
  loading.value = true
  try {
    const [pRes, cRes, catRes] = await Promise.all([
      api.get('/products/'),
      api.get('/customers/'),
      api.get('/products/categories/list'),
    ])
    products.value = pRes.data
    customers.value = cRes.data
    categories.value = catRes.data
  } finally {
    loading.value = false
  }
}

onMounted(loadProducts)
</script>

<style scoped>
.pos-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.pos-products {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-right: 1px solid var(--border);
}

.pos-toolbar {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg2);
}

.search-input {
  margin-bottom: 12px;
}

.category-filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.cat-btn {
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--border);
  background: var(--bg3);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
}

.cat-btn.active {
  background: rgba(249,115,22,0.12);
  border-color: var(--primary);
  color: var(--primary);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  padding: 16px 20px;
  overflow-y: auto;
  flex: 1;
}

.product-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s;
  overflow: hidden;
}

.product-card:hover { border-color: var(--primary); transform: translateY(-2px); }
.product-card.out-of-stock { opacity: 0.4; cursor: not-allowed; }

.product-img {
  background: linear-gradient(135deg, rgba(249,115,22,0.15), rgba(99,102,241,0.15));
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  color: var(--primary);
}

.product-info { padding: 10px; }
.product-name { font-size: 13px; font-weight: 600; margin-bottom: 2px; line-height: 1.3; }
.product-sku { font-size: 10px; color: var(--text-muted); margin-bottom: 8px; }
.product-bottom { display: flex; justify-content: space-between; align-items: center; }
.product-price { font-size: 14px; font-weight: 700; color: var(--primary); }
.product-stock { font-size: 11px; color: var(--success); }
.product-stock.low { color: var(--danger); }

.pos-empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

/* Cart */
.pos-cart {
  width: 340px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: var(--bg2);
}

.cart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.cart-header h2 { font-size: 18px; font-weight: 700; }

.cart-section {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

.section-label { display: block; font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px; }

.cart-items {
  flex: 1;
  overflow-y: auto;
  min-height: 120px;
  padding: 8px 0;
}

.cart-empty {
  text-align: center;
  padding: 32px 20px;
  color: var(--text-muted);
  font-size: 13px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-bottom: 1px solid var(--border);
}

.cart-item-name { flex: 1; font-size: 13px; font-weight: 500; min-width: 0; }
.cart-item-controls { display: flex; align-items: center; gap: 6px; }
.qty-btn { width: 24px; height: 24px; border-radius: 4px; background: var(--bg3); color: var(--text); font-size: 14px; cursor: pointer; border: 1px solid var(--border); }
.qty-val { font-size: 13px; font-weight: 700; min-width: 20px; text-align: center; }
.cart-item-sub { font-size: 13px; font-weight: 600; color: var(--primary); min-width: 60px; text-align: right; }
.remove-btn { background: none; color: var(--text-muted); font-size: 12px; cursor: pointer; }
.remove-btn:hover { color: var(--danger); }

.cart-totals { padding: 12px 16px; border-top: 1px solid var(--border); }
.total-row { display: flex; justify-content: space-between; font-size: 13px; color: var(--text-muted); margin-bottom: 4px; }
.total-final { font-size: 18px; font-weight: 700; color: var(--text); margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border); }

.payment-methods { display: flex; gap: 8px; }
.pay-btn {
  flex: 1;
  padding: 8px 4px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--border);
  background: var(--bg3);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
}
.pay-btn.active { background: rgba(249,115,22,0.12); border-color: var(--primary); color: var(--primary); }

.cobrar-btn {
  margin: 12px 16px;
  width: calc(100% - 32px);
  justify-content: center;
  padding: 14px;
  font-size: 16px;
}

.cobrar-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.ticket {
  margin: 0 16px 16px;
  background: var(--bg3);
  border: 1px solid var(--success);
  border-radius: 10px;
  padding: 14px;
  font-size: 13px;
}

.ticket-header { color: var(--success); font-weight: 700; margin-bottom: 8px; }
.ticket-row { display: flex; justify-content: space-between; margin-bottom: 4px; color: var(--text-muted); }
.ticket-total { font-weight: 700; border-top: 1px solid var(--border); margin-top: 8px; padding-top: 8px; }

.btn-sm { padding: 6px 12px; font-size: 12px; }
.mt-8 { margin-top: 8px; }
.error-msg { color: var(--danger); font-size: 13px; padding: 0 16px 12px; }
</style>
