<script setup>
import { onMounted, ref, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { apiPayments } from '../api/endpoints'

const items = ref([])
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  items.value = await apiPayments()
  loading.value = false
})

function fmtMoney(n) { return '$' + Number(n||0).toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
function fmtDate(d) { return d ? new Date(d).toLocaleString('es-MX') : '—' }

const totalOk = computed(() => items.value.filter(p => p.status === 'succeeded').reduce((s, p) => s + Number(p.amount_mxn || 0), 0))
const totalPending = computed(() => items.value.filter(p => p.status === 'pending').reduce((s, p) => s + Number(p.amount_mxn || 0), 0))
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1 class="page-title">Pagos</h1>
        <p class="page-subtitle">Depósitos cobrados con Stripe / Conekta.</p>
      </div>
    </div>

    <div class="grid-3">
      <div class="kpi" style="--kpi-accent: var(--success);">
        <div class="kpi-label">Cobrado</div>
        <div class="kpi-value">{{ fmtMoney(totalOk) }}</div>
        <div class="kpi-sub">{{ items.filter(p => p.status === 'succeeded').length }} pagos OK</div>
      </div>
      <div class="kpi" style="--kpi-accent: var(--gold);">
        <div class="kpi-label">Pendiente</div>
        <div class="kpi-value">{{ fmtMoney(totalPending) }}</div>
        <div class="kpi-sub">{{ items.filter(p => p.status === 'pending').length }} por completar</div>
      </div>
      <div class="kpi" style="--kpi-accent: var(--navy);">
        <div class="kpi-label">Integraciones</div>
        <div class="kpi-value" style="font-size:22px;">Stripe · Conekta</div>
        <div class="kpi-sub">Modo demo activo (sin API keys)</div>
      </div>
    </div>

    <div style="margin-top:28px;">
      <div v-if="loading" class="muted">Cargando...</div>
      <table v-else class="table">
        <thead><tr><th>Fecha</th><th>Descripción</th><th>Proveedor</th><th>Monto</th><th>Estado</th><th>Pagado</th></tr></thead>
        <tbody>
          <tr v-for="p in items" :key="p.id">
            <td class="muted">{{ fmtDate(p.created_at) }}</td>
            <td style="color:var(--navy);font-weight:500;">{{ p.description }}</td>
            <td>{{ p.provider }}</td>
            <td><strong>{{ fmtMoney(p.amount_mxn) }}</strong></td>
            <td>
              <span :class="['chip', p.status === 'succeeded' ? 'chip-success' : (p.status === 'failed' ? 'chip-danger' : 'chip-gold')]">
                {{ p.status }}
              </span>
            </td>
            <td class="muted">{{ fmtDate(p.paid_at) }}</td>
          </tr>
          <tr v-if="!items.length"><td colspan="6" class="muted" style="text-align:center;padding:40px 0;">Sin pagos registrados.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="card" style="margin-top:28px;">
      <div class="serif" style="font-size:20px;color:var(--navy);margin-bottom:12px;font-weight:600;">Conectar Stripe o Conekta</div>
      <p class="muted" style="font-size:14px;">
        Para cobros reales agrega tus API keys al archivo <code>.env.docker</code>:
      </p>
      <pre style="background:var(--cream-2);padding:14px;border-radius:10px;font-size:12px;overflow-x:auto;margin:0;">STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
CONEKTA_PRIVATE_KEY=key_...</pre>
      <p class="muted" style="font-size:13px;margin-top:12px;">
        Sin estas keys, AgendaPro usa un checkout demo que simula el pago sin cobrar nada.
      </p>
    </div>
  </AppLayout>
</template>
