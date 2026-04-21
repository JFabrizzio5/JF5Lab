<script setup>
import { ref, onMounted, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { notesApi, customersApi, productsApi } from '../api/endpoints'
import { useRouter } from 'vue-router'

const router = useRouter()
const notes = ref([]); const loading = ref(false); const error = ref(null)
const filter = ref('all')
const showForm = ref(false)
const customers = ref([]); const products = ref([])

const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits:2 }).format(n || 0)

async function load() {
  loading.value = true
  try {
    const status = filter.value === 'all' ? null : filter.value
    const { data } = await notesApi.list(status)
    notes.value = data
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { loading.value = false }
}

async function openForm() {
  showForm.value = true
  try {
    const [c, p] = await Promise.all([customersApi.list(), productsApi.list()])
    customers.value = c.data; products.value = p.data
    form.value.customer_id = customers.value[0]?.id || ''
  } catch (e) { error.value = e.message }
}

const form = ref({
  customer_id: '',
  items: [{ description: '', qty: 1, unit_price: 0, tax_rate: 0.16, product_id: null }],
  notes: 'Gracias por tu preferencia.',
  valid_until: new Date(Date.now() + 15*86400000).toISOString().slice(0,10),
})

function addItem() {
  form.value.items.push({ description: '', qty: 1, unit_price: 0, tax_rate: 0.16, product_id: null })
}
function delItem(i) { form.value.items.splice(i, 1) }
function setProduct(i, pid) {
  const p = products.value.find(x => x.id === pid)
  if (p) {
    form.value.items[i].product_id = p.id
    form.value.items[i].description = p.name
    form.value.items[i].unit_price = Number(p.price_mxn)
    form.value.items[i].tax_rate = Number(p.tax_rate)
  }
}
const totals = computed(() => {
  let sub = 0, tax = 0
  for (const it of form.value.items) {
    const s = (it.qty || 0) * (it.unit_price || 0)
    sub += s; tax += s * (it.tax_rate || 0)
  }
  return { subtotal: sub, tax, total: sub + tax }
})

const saving = ref(false)
async function submit() {
  saving.value = true
  try {
    const payload = {
      customer_id: form.value.customer_id,
      items: form.value.items.map(i => ({
        product_id: i.product_id || null,
        description: i.description,
        qty: Number(i.qty), unit_price: Number(i.unit_price), tax_rate: Number(i.tax_rate),
      })),
      notes: form.value.notes,
      valid_until: form.value.valid_until || null,
    }
    const { data } = await notesApi.create(payload)
    showForm.value = false
    router.push(`/app/notes/${data.id}`)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { saving.value = false }
}

const filters = [
  { id: 'all',    label: 'Todas' },
  { id: 'draft',  label: 'Borradores' },
  { id: 'sent',   label: 'Enviadas' },
  { id: 'paid',   label: 'Cobradas' },
  { id: 'canceled', label: 'Canceladas' },
]

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="app-top">
      <div>
        <h1 class="page-title">Notas</h1>
        <p class="page-sub">Cotizaciones y recibos. Envía por WhatsApp y cobra con Stripe/Conekta.</p>
      </div>
      <button class="btn btn-primary" @click="openForm"><i class="mdi mdi-plus"></i> Nueva nota</button>
    </div>

    <div class="filters">
      <button v-for="f in filters" :key="f.id" class="chip" :class="{ active: filter === f.id }" @click="filter = f.id; load()">
        {{ f.label }}
      </button>
    </div>

    <div class="card" style="padding: 0;">
      <table class="table">
        <thead><tr>
          <th>Folio</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Canal</th><th>Creada</th><th></th>
        </tr></thead>
        <tbody>
          <tr v-if="loading"><td colspan="7" class="muted" style="padding: 30px; text-align:center;">Cargando…</td></tr>
          <tr v-else-if="!notes.length"><td colspan="7" class="muted" style="padding: 30px; text-align:center;">Sin notas aún. Crea la primera.</td></tr>
          <tr v-for="n in notes" :key="n.id">
            <td class="mono">{{ n.number }}</td>
            <td class="muted">-</td>
            <td style="font-weight:700;">{{ peso(n.total) }}</td>
            <td><span :class="['badge', n.status]">{{ n.status }}</span></td>
            <td class="muted">{{ n.channel }}</td>
            <td class="muted">{{ new Date(n.created_at).toLocaleDateString('es-MX') }}</td>
            <td><router-link :to="`/app/notes/${n.id}`">Abrir</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- FORM MODAL -->
    <div v-if="showForm" class="modal-back" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-head">
          <h2>Nueva nota</h2>
          <button class="btn btn-ghost btn-sm" @click="showForm = false"><i class="mdi mdi-close"></i></button>
        </div>
        <div class="modal-body">
          <div class="grid-2">
            <div>
              <label>Cliente</label>
              <select v-model="form.customer_id">
                <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div>
              <label>Válida hasta</label>
              <input type="date" v-model="form.valid_until" />
            </div>
          </div>
          <div class="items-wrap">
            <div class="items-head">
              <div style="flex:3;">Descripción</div>
              <div style="width:70px;">Cant</div>
              <div style="width:110px;">Precio unit</div>
              <div style="width:70px;">IVA</div>
              <div style="width:110px; text-align:right;">Total</div>
              <div style="width:30px;"></div>
            </div>
            <div v-for="(it, i) in form.items" :key="i" class="item-row">
              <select @change="e => setProduct(i, e.target.value)" style="flex:0.9; min-width: 110px;">
                <option value="">Producto...</option>
                <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
              <input v-model="it.description" placeholder="Descripción" style="flex:2;" />
              <input v-model.number="it.qty" type="number" step="0.01" style="width:70px;" />
              <input v-model.number="it.unit_price" type="number" step="0.01" style="width:110px;" />
              <input v-model.number="it.tax_rate" type="number" step="0.01" style="width:70px;" />
              <div style="width:110px; text-align:right; font-weight:700; padding: 9px 0;">{{ peso(it.qty * it.unit_price * (1 + it.tax_rate)) }}</div>
              <button class="btn btn-sm btn-ghost" @click="delItem(i)" style="width:30px; padding: 6px 8px;"><i class="mdi mdi-close"></i></button>
            </div>
            <button class="btn btn-sm" @click="addItem"><i class="mdi mdi-plus"></i> Agregar línea</button>
          </div>
          <div class="totals">
            <div><span class="muted">Subtotal</span> <b>{{ peso(totals.subtotal) }}</b></div>
            <div><span class="muted">IVA</span> <b>{{ peso(totals.tax) }}</b></div>
            <div class="total-big"><span class="muted">Total</span> <b class="gradient-text">{{ peso(totals.total) }}</b></div>
          </div>
          <label>Nota al cliente</label>
          <textarea v-model="form.notes" rows="2"></textarea>
        </div>
        <div class="modal-foot">
          <button class="btn btn-ghost" @click="showForm = false">Cancelar</button>
          <button class="btn btn-primary" :disabled="saving || !form.customer_id || !form.items.length" @click="submit">
            <i class="mdi mdi-content-save-outline"></i> {{ saving ? 'Guardando…' : 'Crear nota' }}
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.filters { display: flex; gap: 6px; margin-bottom: 14px; flex-wrap: wrap; }
.chip { padding: 6px 14px; border: 1px solid var(--border-strong); background: var(--surface); border-radius: 999px; cursor: pointer; font-size: 13px; color: var(--text-muted); font-weight: 600; }
.chip.active { background: var(--emerald-soft); color: var(--emerald-dark); border-color: transparent; }

.modal-back { position: fixed; inset: 0; background: rgba(0,0,0,.5); display: grid; place-items: center; z-index: 100; padding: 20px; }
.modal { background: var(--surface); border-radius: 18px; width: 100%; max-width: 780px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: var(--shadow-lg); }
.modal-head, .modal-foot { padding: 18px 22px; display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.modal-head { border-bottom: 1px solid var(--border); }
.modal-head h2 { margin: 0; font-size: 20px; font-weight: 800; }
.modal-body { padding: 18px 22px; overflow-y: auto; }
.modal-foot { border-top: 1px solid var(--border); justify-content: flex-end; }
.items-wrap { margin: 16px 0; }
.items-head { display: flex; gap: 8px; padding: 0 4px; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); font-weight: 600; margin-bottom: 6px; }
.item-row { display: flex; gap: 8px; margin-bottom: 6px; align-items: center; flex-wrap: wrap; }
.totals { background: var(--bg-subtle); padding: 14px 18px; border-radius: 12px; margin: 14px 0; }
.totals > div { display: flex; justify-content: space-between; padding: 3px 0; font-size: 14px; }
.total-big { font-size: 20px; margin-top: 6px; padding-top: 8px; border-top: 1px solid var(--border); }
.total-big b { font-size: 24px; font-weight: 800; letter-spacing: -0.02em; }
</style>
