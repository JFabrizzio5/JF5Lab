<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { notesApi } from '../api/endpoints'

const route = useRoute(); const router = useRouter()
const note = ref(null); const loading = ref(false); const error = ref(null)
const publicUrl = ref(null); const waStatus = ref(null); const sending = ref(false)
const issuingCfdi = ref(false); const cfdiResult = ref(null)
const copied = ref(false)

const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits:2 }).format(n || 0)

async function load() {
  loading.value = true
  try {
    const { data } = await notesApi.get(route.params.id)
    note.value = data
    publicUrl.value = `${window.location.origin}/n/${data.public_token}`
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { loading.value = false }
}

async function sendWhatsapp() {
  sending.value = true
  try {
    const { data } = await notesApi.send(note.value.id, { channel: 'whatsapp' })
    publicUrl.value = data.public_url
    waStatus.value = data.whatsapp_sent ? 'Enviado a WhatsApp' : `Link listo · ${data.whatsapp_status}`
    await load()
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { sending.value = false }
}

async function copyLink() {
  await navigator.clipboard.writeText(publicUrl.value)
  copied.value = true
  setTimeout(() => copied.value = false, 1500)
}

async function issueCfdi() {
  issuingCfdi.value = true
  try {
    const { data } = await notesApi.issueCfdi(note.value.id, { metodo_pago: 'PUE', forma_pago: '03', serie: 'A' })
    cfdiResult.value = data
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { issuingCfdi.value = false }
}

async function checkout(provider) {
  try {
    const { data } = await notesApi.checkout(note.value.id, { provider })
    window.open(data.checkout_url, '_blank')
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div v-if="loading" class="muted">Cargando…</div>
    <div v-else-if="error" class="muted" style="color:var(--danger);">{{ error }}</div>
    <div v-else-if="note">
      <router-link to="/app/notes" class="back muted"><i class="mdi mdi-arrow-left"></i> Volver a notas</router-link>
      <div class="app-top">
        <div>
          <h1 class="page-title">Nota <span class="mono">{{ note.number }}</span></h1>
          <p class="page-sub">
            <span :class="['badge', note.status]">{{ note.status }}</span>
            <span class="muted" style="margin-left: 10px;">{{ new Date(note.created_at).toLocaleDateString('es-MX') }}</span>
          </p>
        </div>
        <div class="top-actions">
          <button class="btn btn-whatsapp" :disabled="sending" @click="sendWhatsapp"><i class="mdi mdi-whatsapp"></i> {{ sending ? 'Enviando…' : 'Enviar por WhatsApp' }}</button>
          <button class="btn" @click="copyLink"><i class="mdi mdi-content-copy"></i> {{ copied ? '¡Copiado!' : 'Copiar link' }}</button>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <h3 class="card-title">Conceptos</h3>
          <table class="table" style="margin-top: 8px;">
            <thead><tr><th>Descripción</th><th>Cant</th><th>P. unit</th><th style="text-align:right;">Total</th></tr></thead>
            <tbody>
              <tr v-for="it in note.items" :key="it.id">
                <td>{{ it.description }}</td>
                <td>{{ it.qty }}</td>
                <td>{{ peso(it.unit_price) }}</td>
                <td style="text-align:right; font-weight:700;">{{ peso(it.total) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="totals">
            <div><span class="muted">Subtotal</span> <b>{{ peso(note.subtotal) }}</b></div>
            <div><span class="muted">IVA</span> <b>{{ peso(note.tax_total) }}</b></div>
            <div v-if="Number(note.discount) > 0"><span class="muted">Descuento</span> <b>-{{ peso(note.discount) }}</b></div>
            <div class="tot-big"><span class="muted">Total</span> <b class="gradient-text">{{ peso(note.total) }}</b></div>
          </div>
          <div v-if="note.notes" class="muted" style="margin-top: 16px; font-style: italic;">"{{ note.notes }}"</div>
        </div>

        <div>
          <div class="card">
            <h3 class="card-title">Cliente</h3>
            <div v-if="note.customer">
              <div style="font-weight:700;font-size:15px;">{{ note.customer.name }}</div>
              <div class="muted" style="font-size:13px;">{{ note.customer.email }}</div>
              <div class="muted" style="font-size:13px;">{{ note.customer.phone }}</div>
              <div v-if="note.customer.rfc" class="muted mono" style="font-size:12px; margin-top: 8px;">RFC: {{ note.customer.rfc }}</div>
            </div>
            <div v-else class="muted">Sin cliente asignado</div>
          </div>

          <div class="card" style="margin-top: 16px;">
            <h3 class="card-title">Link público</h3>
            <div class="link-box">
              <input :value="publicUrl" readonly @focus="($event.target).select()" />
            </div>
            <div v-if="waStatus" class="muted" style="margin-top: 8px; font-size: 12px;">{{ waStatus }}</div>
            <img v-if="note.id" :src="`/notas/v1/notes/${note.id}/qr?size=200`" alt="QR" class="qr" />
          </div>

          <div class="card" style="margin-top: 16px;">
            <h3 class="card-title">Pagar esta nota</h3>
            <div style="display:flex;flex-direction:column;gap:8px;">
              <button class="btn btn-stripe" @click="checkout('stripe')"><i class="mdi mdi-credit-card-outline"></i> Checkout Stripe</button>
              <button class="btn btn-conekta" @click="checkout('conekta')"><span class="cokdot"></span> Checkout Conekta (OXXO/SPEI)</button>
            </div>
          </div>

          <div class="card" style="margin-top: 16px;">
            <h3 class="card-title">CFDI 4.0</h3>
            <div v-if="cfdiResult" class="cfdi-res">
              <div><span :class="['badge', cfdiResult.status === 'issued' ? 'success' : 'warn']">{{ cfdiResult.status }}</span></div>
              <div class="muted" style="font-size:13px; margin-top: 6px;">Folio: {{ cfdiResult.serie }}-{{ cfdiResult.folio }}</div>
              <div class="muted" style="font-size:12px;">Uso: {{ cfdiResult.uso_cfdi }} · Método: {{ cfdiResult.metodo_pago }}</div>
              <div class="muted" style="font-size:12px; margin-top: 8px;">Timbrado real vía PAC pendiente de integración.</div>
            </div>
            <button v-else class="btn" :disabled="note.status !== 'paid' || issuingCfdi" @click="issueCfdi">
              <i class="mdi mdi-file-certificate-outline"></i> {{ issuingCfdi ? 'Timbrando…' : 'Emitir CFDI' }}
            </button>
            <div v-if="note.status !== 'paid'" class="muted" style="font-size: 12px; margin-top: 8px;">
              La nota debe estar pagada antes de emitir el CFDI.
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.back { display: inline-flex; align-items: center; gap: 4px; font-size: 14px; margin-bottom: 10px; }
.top-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.card-title { font-size: 13px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); margin: 0 0 10px; font-weight: 700; }
.totals { background: var(--bg-subtle); padding: 14px 18px; border-radius: 12px; margin-top: 16px; }
.totals > div { display: flex; justify-content: space-between; padding: 3px 0; font-size: 14px; }
.tot-big { font-size: 20px; margin-top: 6px; padding-top: 8px; border-top: 1px solid var(--border); }
.tot-big b { font-size: 24px; font-weight: 800; letter-spacing: -0.02em; }
.link-box input { font-size: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.qr { display: block; margin: 14px auto 0; width: 180px; border: 1px solid var(--border); border-radius: 10px; background: white; padding: 6px; }
.cokdot { width: 10px; height: 10px; border-radius: 50%; background: #00b884; display: inline-block; margin-right: 4px; }
.cfdi-res { }
</style>
