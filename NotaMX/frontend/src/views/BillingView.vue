<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { billingApi, exportsApi } from '../api/endpoints'

const items = ref([]); const loading = ref(false); const error = ref(null)
const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits: 2 }).format(n || 0)

async function load() {
  loading.value = true
  try { const { data } = await billingApi.payments(); items.value = data }
  catch (e) { error.value = e.message } finally { loading.value = false }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="app-top">
      <div>
        <h1 class="page-title">Pagos</h1>
        <p class="page-sub">Historial de cobros por Stripe, Conekta y pagos manuales.</p>
      </div>
      <button class="btn btn-sm" @click="exportsApi.payments()"><i class="mdi mdi-file-excel-outline"></i> Exportar</button>
    </div>
    <div class="providers">
      <div class="prov-card">
        <div class="prov-logo"><b>Stripe</b></div>
        <p class="muted">Conecta <code>STRIPE_SECRET_KEY</code> en .env.docker para cobros reales.</p>
        <div class="badge teal">Demo checkout activo</div>
      </div>
      <div class="prov-card">
        <div class="prov-logo"><b style="color:#00b884;">Conekta</b></div>
        <p class="muted">Conecta <code>CONEKTA_PRIVATE_KEY</code> para OXXO/SPEI reales.</p>
        <div class="badge teal">Demo checkout activo</div>
      </div>
    </div>
    <div class="card" style="padding: 0;">
      <table class="table">
        <thead><tr><th>Creado</th><th>Monto</th><th>Proveedor</th><th>Método</th><th>Estado</th><th>Pagado</th></tr></thead>
        <tbody>
          <tr v-if="loading"><td colspan="6" class="muted" style="padding: 30px; text-align:center;">Cargando…</td></tr>
          <tr v-else-if="!items.length"><td colspan="6" class="muted" style="padding: 30px; text-align:center;">Sin pagos aún.</td></tr>
          <tr v-for="p in items" :key="p.id">
            <td class="muted">{{ new Date(p.created_at).toLocaleString('es-MX') }}</td>
            <td style="font-weight: 700;">{{ peso(p.amount_mxn) }}</td>
            <td class="muted">{{ p.provider || '-' }}</td>
            <td class="muted">{{ p.method || '-' }}</td>
            <td><span :class="['badge', p.status === 'succeeded' ? 'success' : p.status === 'pending' ? 'warn' : 'danger']">{{ p.status }}</span></td>
            <td class="muted">{{ p.paid_at ? new Date(p.paid_at).toLocaleString('es-MX') : '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<style scoped>
.providers { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 20px; }
.prov-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 18px; }
.prov-logo { font-size: 18px; margin-bottom: 6px; }
.prov-card p { font-size: 13px; margin: 0 0 10px; }
code { background: var(--bg-subtle); padding: 2px 6px; border-radius: 4px; font-size: 12px; }
</style>
