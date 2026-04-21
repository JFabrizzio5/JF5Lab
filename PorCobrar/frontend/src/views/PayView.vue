<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const token = route.params.token
const info = ref(null)
const err = ref('')
const loading = ref(true)
const processing = ref(false)

// Pay page es SIEMPRE tema claro (deudor externo, sin login)
document.documentElement.setAttribute('data-theme', 'light')

function fmt(n) { return '$' + Number(n || 0).toLocaleString('es-MX', { maximumFractionDigits: 2 }) }

async function load() {
  try {
    const { data } = await axios.get(`/cobrar/v1/public/pay/${token}`)
    info.value = data
  } catch(e) {
    err.value = e.response?.data?.detail || 'Link no válido o expirado'
  }
  loading.value = false
}
onMounted(load)

async function pay(provider) {
  processing.value = true
  try {
    const { data } = await axios.post(`/cobrar/v1/public/pay/${token}/checkout?provider=${provider}`)
    window.location.href = data.url
  } catch(e) {
    err.value = e.response?.data?.detail || e.message
  }
  processing.value = false
}
</script>

<template>
  <div style="min-height:100vh; background: #fafaf9; color: #0a0a0b; padding: 40px 20px">
    <div style="max-width: 560px; margin: 0 auto;">
      <div v-if="loading" style="text-align:center; padding: 80px 0">Cargando…</div>
      <div v-else-if="err" class="card" style="text-align:center; padding: 40px; border: 1px solid #fee2e2; background: white">
        <i class="mdi mdi-alert-circle-outline" style="font-size: 48px; color: #ef4444"></i>
        <h2 style="margin: 14px 0 8px">No pudimos cargar este link</h2>
        <div class="muted">{{ err }}</div>
      </div>
      <template v-else-if="info">
        <div style="text-align:center; margin-bottom: 28px">
          <div style="display:inline-flex; align-items:center; gap:8px; font-weight:700; font-size: 19px; color:#0a0a0b">
            <i class="mdi mdi-cash-fast" :style="{color: info.tenant.brand_color}" style="font-size:24px"></i>
            PorCobrar
          </div>
        </div>

        <div class="card" style="background:white; border: 1px solid #e4e4e7; box-shadow: 0 10px 40px rgba(0,0,0,.08); padding: 28px">
          <div style="font-size: 12px; color:#71717a; text-transform:uppercase; letter-spacing:.06em">
            {{ info.tenant.razon_social || info.tenant.name }}
          </div>
          <div style="font-size: 12px; color:#71717a; margin-top:4px">RFC {{ info.tenant.rfc }}</div>
          <h1 style="margin: 22px 0 6px; font-size: 24px">Pago de factura</h1>
          <div style="color:#52525b; font-size:13px">Factura <span class="mono">{{ info.invoice.serie }}{{ info.invoice.folio }}</span> · Emitida {{ info.invoice.issued_at?.slice(0,10) }} · Vence {{ info.invoice.due_at?.slice(0,10) }}</div>

          <div style="background: #fafaf9; border-radius: 10px; padding: 22px; margin: 20px 0; border: 1px solid #e4e4e7">
            <div style="font-size:12px; color:#71717a">Total a pagar</div>
            <div style="font-family: var(--mono); font-size: 42px; font-weight: 700; color:#0a0a0b; margin: 4px 0">
              {{ fmt(info.invoice.balance) }} <span style="font-size:14px; color:#71717a">{{ info.invoice.currency }}</span>
            </div>
            <div style="font-size:12px; color:#71717a">
              Facturado a: <strong style="color:#0a0a0b">{{ info.debtor.name }}</strong>
            </div>
          </div>

          <div v-if="info.invoice.status === 'paid'" class="badge" style="background:#d1fae5; color:#047857; padding: 8px 14px; font-size: 13px">
            <i class="mdi mdi-check-decagram"></i> Factura pagada
          </div>
          <template v-else>
            <button class="btn btn-primary btn-lg" style="width:100%; background: #10b981; color:white; font-weight:700; padding: 14px; border-radius:10px; border:none; margin-bottom: 10px; cursor:pointer; font-size:15px"
                    :disabled="processing" @click="pay('stripe')">
              <i class="mdi mdi-credit-card-outline"></i> Pagar con tarjeta (Stripe)
            </button>
            <button class="btn btn-lg" style="width:100%; background: white; border:1px solid #d4d4d8; color:#0a0a0b; font-weight:600; padding: 14px; border-radius:10px; font-size:15px; cursor:pointer"
                    :disabled="processing" @click="pay('conekta')">
              <i class="mdi mdi-bank-outline"></i> Pagar con SPEI / OXXO (Conekta)
            </button>
          </template>

          <div style="font-size:11px; color:#a1a1aa; text-align:center; margin-top: 18px; line-height: 1.5">
            Pago seguro procesado por Stripe / Conekta.<br/>
            Powered by PorCobrar · <span class="mono" style="font-size:10px">UUID: {{ info.invoice.cfdi_uuid }}</span>
          </div>
        </div>

        <div style="text-align:center; margin-top: 18px; font-size:12px; color:#a1a1aa">
          ¿Dudas? Contacta a <a :href="'mailto:' + (info.tenant.contact_email || 'cobranza@porcobrar.mx')">cobranza@{{ info.tenant.name?.split(' ')[0]?.toLowerCase() || 'porcobrar' }}.mx</a>
        </div>
      </template>
    </div>
  </div>
</template>
