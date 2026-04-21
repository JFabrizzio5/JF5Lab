<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const note = ref(null); const loading = ref(true); const error = ref(null)
const paying = ref(null)

const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits: 2 }).format(n || 0)

async function load() {
  loading.value = true
  try {
    const { data } = await axios.get(`/notas/v1/public/note/${route.params.token}`)
    note.value = data
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Nota no encontrada'
  } finally { loading.value = false }
}

async function pay(provider) {
  paying.value = provider
  try {
    const { data } = await axios.post(`/notas/v1/notes/${note.value.id}/checkout`, { provider })
    window.location.href = data.checkout_url
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { paying.value = null }
}

onMounted(load)
</script>

<template>
  <div class="public-page" :style="note ? { '--brand': note.tenant_brand_color } : {}">
    <div v-if="loading" class="center muted">Cargando nota…</div>
    <div v-else-if="error" class="center" style="color:var(--danger);">{{ error }}</div>
    <div v-else-if="note" class="sheet">
      <header class="sheet-head">
        <div class="brand-line">
          <div class="bmark" :style="{ background: note.tenant_brand_color }"><i class="mdi mdi-receipt-text-check"></i></div>
          <div>
            <div class="tn">{{ note.tenant_name }}</div>
            <div class="muted rfc">{{ note.tenant_rfc || '' }}</div>
          </div>
        </div>
        <div class="folio-box">
          <div class="muted label">Folio</div>
          <div class="mono folio">{{ note.number }}</div>
          <span :class="['badge', note.status]">{{ note.status }}</span>
        </div>
      </header>

      <div class="client-row">
        <div>
          <div class="muted label">Cliente</div>
          <div class="client-name">{{ note.customer_name || '-' }}</div>
        </div>
        <div v-if="note.valid_until">
          <div class="muted label">Vigencia</div>
          <div>{{ new Date(note.valid_until).toLocaleDateString('es-MX') }}</div>
        </div>
      </div>

      <table class="items-table">
        <thead><tr><th>Descripción</th><th class="r">Cant.</th><th class="r">P. unit</th><th class="r">Total</th></tr></thead>
        <tbody>
          <tr v-for="it in note.items" :key="it.id">
            <td>{{ it.description }}</td>
            <td class="r">{{ it.qty }}</td>
            <td class="r">{{ peso(it.unit_price) }}</td>
            <td class="r" style="font-weight:700;">{{ peso(it.total) }}</td>
          </tr>
        </tbody>
      </table>

      <div class="totals-box">
        <div><span class="muted">Subtotal</span> <b>{{ peso(note.subtotal) }}</b></div>
        <div><span class="muted">IVA</span> <b>{{ peso(note.tax_total) }}</b></div>
        <div v-if="Number(note.discount) > 0"><span class="muted">Descuento</span> <b>-{{ peso(note.discount) }}</b></div>
        <div class="total-big"><span class="muted">Total</span> <b>{{ peso(note.total) }}</b></div>
      </div>

      <div v-if="note.notes" class="note-text">"{{ note.notes }}"</div>

      <div v-if="note.status === 'paid'" class="paid-banner">
        <i class="mdi mdi-check-circle"></i>
        <div>
          <b>Nota pagada</b>
          <div class="muted" style="font-size: 13px;">Pagada el {{ new Date(note.paid_at).toLocaleDateString('es-MX') }}. El CFDI se emitirá y te llegará al correo.</div>
        </div>
      </div>

      <div v-else class="pay-box">
        <div class="pay-title">Pagar esta nota</div>
        <div class="pay-buttons">
          <button class="btn btn-stripe" :disabled="paying" @click="pay('stripe')">
            <i class="mdi mdi-credit-card-outline"></i>
            <span>{{ paying === 'stripe' ? 'Abriendo…' : 'Tarjeta con Stripe' }}</span>
          </button>
          <button class="btn btn-conekta" :disabled="paying" @click="pay('conekta')">
            <span class="cokdot"></span>
            <span>{{ paying === 'conekta' ? 'Abriendo…' : 'OXXO / SPEI con Conekta' }}</span>
          </button>
        </div>
        <div class="muted small">Pago seguro. No guardamos datos de tu tarjeta.</div>
      </div>

      <footer class="foot">
        <span class="muted">Generado con</span> <b class="gradient-text">NotaMX</b>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.public-page { min-height: 100vh; background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 100%); padding: 40px 16px; --brand: #10b981; }
[data-theme="dark"] .public-page { background: linear-gradient(135deg, #05100c 0%, #06140f 100%); }
.center { text-align: center; padding: 80px 0; }
.sheet { max-width: 680px; margin: 0 auto; background: var(--surface); border: 1px solid var(--border); border-radius: 22px; padding: 36px; box-shadow: 0 20px 60px rgba(16,185,129,.15); }
.sheet-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; padding-bottom: 22px; border-bottom: 1px solid var(--border); }
.brand-line { display: flex; align-items: center; gap: 12px; }
.bmark { width: 44px; height: 44px; border-radius: 12px; color: white; display: grid; place-items: center; font-size: 22px; }
.tn { font-weight: 800; font-size: 20px; letter-spacing: -0.02em; }
.rfc { font-family: ui-monospace, Menlo, monospace; font-size: 12px; margin-top: 2px; }
.folio-box { text-align: right; }
.label { font-size: 10px; text-transform: uppercase; letter-spacing: .08em; font-weight: 700; color: var(--text-muted); }
.folio { font-size: 20px; font-weight: 800; margin: 4px 0 6px; }

.client-row { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 24px; flex-wrap: wrap; }
.client-name { font-size: 17px; font-weight: 700; letter-spacing: -0.01em; margin-top: 4px; }

.items-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 14px; }
.items-table th { text-align: left; padding: 10px 0; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); font-weight: 700; border-bottom: 1px solid var(--border); }
.items-table th.r, .items-table td.r { text-align: right; }
.items-table td { padding: 12px 0; border-bottom: 1px solid var(--border); }

.totals-box { background: var(--bg-subtle); padding: 16px 22px; border-radius: 14px; margin-bottom: 20px; }
.totals-box > div { display: flex; justify-content: space-between; padding: 4px 0; font-size: 14px; }
.total-big { margin-top: 8px; padding-top: 10px; border-top: 1px solid var(--border); font-size: 20px; }
.total-big b { font-size: 26px; font-weight: 800; letter-spacing: -0.02em; color: var(--brand); }

.note-text { font-style: italic; color: var(--text-muted); font-size: 14px; margin-bottom: 24px; }

.paid-banner { display: flex; align-items: center; gap: 14px; background: var(--emerald-soft); color: var(--emerald-dark); padding: 18px 22px; border-radius: 14px; margin-bottom: 20px; }
.paid-banner .mdi { font-size: 32px; }

.pay-box { background: linear-gradient(135deg, var(--brand) 0%, #14b8a6 100%); color: white; padding: 24px; border-radius: 18px; margin-bottom: 20px; }
.pay-title { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; font-weight: 700; opacity: .9; margin-bottom: 12px; }
.pay-buttons { display: flex; flex-direction: column; gap: 10px; margin-bottom: 12px; }
.pay-buttons .btn { justify-content: center; padding: 14px; font-weight: 700; font-size: 15px; }
.btn-stripe { background: #635bff; color: white; border: none; }
.btn-conekta { background: white; color: #00b884; border: none; }
.cokdot { width: 12px; height: 12px; border-radius: 50%; background: #00b884; display: inline-block; margin-right: 6px; }
.pay-box .small { color: rgba(255,255,255,.85); font-size: 12px; text-align: center; }

.foot { margin-top: 26px; text-align: center; font-size: 13px; padding-top: 16px; border-top: 1px solid var(--border); }
.gradient-text { background: linear-gradient(135deg, #059669, #14b8a6); -webkit-background-clip: text; background-clip: text; color: transparent; font-weight: 700; }

@media (max-width: 500px) {
  .sheet { padding: 22px 18px; border-radius: 14px; }
  .sheet-head { flex-direction: column; gap: 14px; }
  .folio-box { text-align: left; }
}
</style>
