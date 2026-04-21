<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { cfdiApi } from '../api/endpoints'

const items = ref([]); const loading = ref(false); const error = ref(null)
const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits: 2 }).format(n || 0)

async function load() {
  loading.value = true
  try { const { data } = await cfdiApi.list(); items.value = data }
  catch (e) { error.value = e.message } finally { loading.value = false }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="app-top">
      <div>
        <h1 class="page-title">CFDI 4.0</h1>
        <p class="page-sub">Facturas SAT generadas desde tus notas pagadas.</p>
      </div>
    </div>
    <div class="note-box">
      <i class="mdi mdi-information-outline" style="color: var(--emerald-dark); font-size: 18px;"></i>
      <div>
        <b>Timbrado real pendiente.</b>
        <span class="muted"> En este MVP el endpoint guarda los datos y status. Para producción conecta un PAC (Facturama, Finkok, SW) con tus certificados CSD.</span>
      </div>
    </div>
    <div class="card" style="padding: 0;">
      <table class="table">
        <thead><tr><th>Serie-Folio</th><th>UUID SAT</th><th>Total</th><th>Uso</th><th>Método</th><th>Estado</th><th>Emitido</th></tr></thead>
        <tbody>
          <tr v-if="loading"><td colspan="7" class="muted" style="padding: 30px; text-align:center;">Cargando…</td></tr>
          <tr v-else-if="!items.length"><td colspan="7" class="muted" style="padding: 30px; text-align:center;">Aún no se ha emitido ningún CFDI.</td></tr>
          <tr v-for="c in items" :key="c.id">
            <td class="mono">{{ c.serie }}-{{ c.folio }}</td>
            <td class="mono" style="font-size: 11px;">{{ c.uuid_sat || '-' }}</td>
            <td style="font-weight: 700;">{{ peso(c.total) }}</td>
            <td class="muted">{{ c.uso_cfdi }}</td>
            <td class="muted">{{ c.metodo_pago }}</td>
            <td><span :class="['badge', c.status === 'issued' ? 'success' : c.status === 'pending' ? 'warn' : c.status === 'canceled' ? 'danger' : 'draft']">{{ c.status }}</span></td>
            <td class="muted">{{ c.issued_at ? new Date(c.issued_at).toLocaleDateString('es-MX') : '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<style scoped>
.note-box { background: var(--emerald-soft); padding: 12px 16px; border-radius: 12px; display: flex; gap: 10px; align-items: flex-start; margin-bottom: 16px; font-size: 13.5px; }
</style>
