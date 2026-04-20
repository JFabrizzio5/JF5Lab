<template>
  <div class="checkout-page">
    <div class="checkout-header">
      <router-link :to="`/c/${route.params.slug}`" class="back-link">← Volver a {{ conv?.name }}</router-link>
    </div>
    <div class="checkout-container" v-if="conv">
      <div class="checkout-card">
        <h1>Comprar Boletos</h1>
        <h2>{{ conv.name }}</h2>

        <div v-if="step === 1">
          <div v-for="tt in conv.ticket_types" :key="tt.id" class="tt-row">
            <div>
              <div class="tt-name">{{ tt.name }}</div>
              <div class="tt-price">${{ tt.price.toFixed(0) }} MXN</div>
              <div class="tt-avail">{{ (tt.quantity_total || 9999) - tt.quantity_sold }} disponibles</div>
            </div>
            <div class="qty-ctrl">
              <button @click="dec(tt.id)" class="qty-btn">−</button>
              <span>{{ quantities[tt.id] || 0 }}</span>
              <button @click="inc(tt.id, tt)" class="qty-btn">+</button>
            </div>
          </div>
          <div class="total-row">Total: <strong>${{ total.toFixed(0) }} MXN</strong></div>
          <button @click="step = 2" :disabled="total === 0" class="btn btn-primary" style="width:100%;margin-top:16px">
            Continuar →
          </button>
        </div>

        <div v-if="step === 2">
          <div class="form-group"><label>Nombre</label><input v-model="buyer.name" required /></div>
          <div class="form-group" style="margin-top:12px"><label>Email</label><input v-model="buyer.email" type="email" required /></div>
          <div class="form-group" style="margin-top:12px"><label>Teléfono</label><input v-model="buyer.phone" /></div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="step = 1" class="btn btn-ghost" style="flex:1">Atrás</button>
            <button @click="purchase" :disabled="loading || !buyer.name || !buyer.email" class="btn btn-primary" style="flex:1">
              {{ loading ? 'Procesando...' : 'Confirmar' }}
            </button>
          </div>
        </div>

        <div v-if="step === 3" class="success">
          <div style="font-size:48px">✅</div>
          <h3>¡Listo!</h3>
          <p>Total pagado: <strong>${{ result?.total?.toFixed(0) }} MXN</strong></p>
          <p v-if="result?.note" style="font-size:13px;color:var(--text2)">{{ result.note }}</p>
          <router-link :to="`/c/${route.params.slug}`" class="btn btn-primary" style="margin-top:16px;display:block;text-align:center">
            Volver a la convención
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/index.js'

const route = useRoute()
const conv = ref(null)
const step = ref(1)
const quantities = ref({})
const buyer = ref({ name: '', email: '', phone: '' })
const loading = ref(false)
const result = ref(null)

const total = computed(() => {
  let t = 0
  for (const tt of (conv.value?.ticket_types || [])) {
    t += (quantities.value[tt.id] || 0) * tt.price
  }
  return t
})

function inc(id, tt) {
  const avail = (tt.quantity_total || 9999) - tt.quantity_sold
  const cur = quantities.value[id] || 0
  if (cur < avail && cur < 10) quantities.value = { ...quantities.value, [id]: cur + 1 }
}

function dec(id) {
  const cur = quantities.value[id] || 0
  if (cur > 0) quantities.value = { ...quantities.value, [id]: cur - 1 }
}

async function purchase() {
  loading.value = true
  try {
    const items = Object.entries(quantities.value)
      .filter(([, q]) => q > 0)
      .map(([id, qty]) => ({ ticket_type_id: parseInt(id), quantity: qty }))
    const { data } = await api.post('/payments/purchase', {
      convention_id: conv.value.id,
      buyer_name: buyer.value.name,
      buyer_email: buyer.value.email,
      buyer_phone: buyer.value.phone,
      items,
    })
    result.value = data
    if (!data.stripe_client_secret) {
      await api.post(`/payments/confirm/${data.payment_id}`)
    }
    step.value = 3
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al procesar')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const { data } = await api.get(`/public/convention/${route.params.slug}`)
  conv.value = data
})
</script>

<style scoped>
.checkout-page { min-height: 100vh; background: var(--bg); padding: 40px 20px; }
.checkout-header { max-width: 600px; margin: 0 auto 24px; }
.back-link { color: var(--text2); font-size: 14px; }
.back-link:hover { color: var(--text); }
.checkout-container { max-width: 600px; margin: 0 auto; }
.checkout-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 36px; }
h1 { font-size: 22px; font-weight: 800; margin-bottom: 4px; }
h2 { font-size: 16px; color: var(--text2); font-weight: 400; margin-bottom: 24px; }
.tt-row { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid var(--border); }
.tt-name { font-weight: 700; }
.tt-price { font-size: 13px; color: var(--accent); font-weight: 600; }
.tt-avail { font-size: 11px; color: var(--text2); }
.qty-ctrl { display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 16px; }
.qty-btn { width: 32px; height: 32px; background: var(--bg3); border: 1px solid var(--border); color: var(--text); border-radius: 8px; font-size: 18px; cursor: pointer; }
.total-row { text-align: right; padding: 16px 0; font-size: 18px; }
.success { text-align: center; padding: 20px 0; }
.success h3 { font-size: 24px; font-weight: 800; margin: 12px 0 8px; }
.success p { color: var(--text2); margin-bottom: 4px; }
</style>
