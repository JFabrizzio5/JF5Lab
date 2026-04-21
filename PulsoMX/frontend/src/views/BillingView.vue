<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { billingApi, mPlansApi, membersApi } from '../api/endpoints'

const payments = ref([]); const mplans = ref([]); const members = ref([])
const selectedPlan = ref(null); const selectedMember = ref(null); const provider = ref('stripe')
const checkoutUrl = ref(null); const loading = ref(false)

async function load() {
  const [p, m, me] = await Promise.all([billingApi.payments(), mPlansApi.list(), membersApi.list()])
  payments.value = p.data; mplans.value = m.data; members.value = me.data
}
async function charge() {
  if (!selectedPlan.value || !selectedMember.value) return
  loading.value = true
  try {
    const { data } = await billingApi.checkout({
      membership_plan_id: selectedPlan.value, member_id: selectedMember.value, provider: provider.value,
    })
    checkoutUrl.value = data.checkout_url
    window.open(data.checkout_url, '_blank')
  } finally { loading.value = false }
}

function peso(n){ return new Intl.NumberFormat('es-MX',{style:'currency',currency:'MXN'}).format(Number(n)) }

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="head"><h1>Cobros</h1><p class="muted">Stripe + Conekta. OXXO, tarjeta, SPEI.</p></div>

    <div class="grid-2" style="align-items:start;">
      <div class="card">
        <h3 style="margin-top:0;">Cobrar a un miembro</h3>
        <div class="grid-2">
          <div><label>Miembro</label>
            <select v-model="selectedMember">
              <option :value="null">—</option>
              <option v-for="m in members" :key="m.id" :value="m.id">{{ m.first_name }} {{ m.last_name }} ({{ m.code }})</option>
            </select>
          </div>
          <div><label>Plan / Paquete</label>
            <select v-model="selectedPlan">
              <option :value="null">—</option>
              <option v-for="p in mplans" :key="p.id" :value="p.id">{{ p.name }} — {{ peso(p.price_mxn) }}</option>
            </select>
          </div>
        </div>
        <label style="margin-top:14px;">Pasarela</label>
        <div class="radio-row">
          <label class="radio" :class="{sel:provider==='stripe'}">
            <input type="radio" value="stripe" v-model="provider" /> <b>Stripe</b> <span class="muted" style="font-size:12px;">Tarjeta, OXXO</span>
          </label>
          <label class="radio" :class="{sel:provider==='conekta'}">
            <input type="radio" value="conekta" v-model="provider" /> <b>Conekta</b> <span class="muted" style="font-size:12px;">MX, SPEI, OXXO</span>
          </label>
        </div>
        <button class="btn btn-gradient" style="width:100%; margin-top:16px; justify-content:center;" :disabled="!selectedMember || !selectedPlan || loading" @click="charge">
          <i class="mdi mdi-credit-card-outline"></i>
          {{ loading ? 'Abriendo checkout…' : 'Cobrar ahora' }}
        </button>
        <p v-if="checkoutUrl" class="muted" style="font-size:12px; margin-top:8px;">
          <i class="mdi mdi-information"></i> Se abrió en otra pestaña. <a :href="checkoutUrl" target="_blank">Ir</a>
        </p>
      </div>

      <div class="card">
        <h3 style="margin-top:0;">Planes disponibles</h3>
        <div v-for="p in mplans" :key="p.id" class="plan-row">
          <div style="flex:1;">
            <div style="font-weight:700;">{{ p.name }}</div>
            <div class="muted" style="font-size:12px;">{{ p.billing_interval }}{{ p.visits_included ? ` · ${p.visits_included} visitas` : '' }}</div>
          </div>
          <div style="font-weight:800; font-size:16px;">{{ peso(p.price_mxn) }}</div>
        </div>
        <div v-if="!mplans.length" class="muted">Sin planes.</div>
      </div>
    </div>

    <h3 style="margin:28px 0 12px;">Historial de pagos</h3>
    <div class="card" style="padding:0; overflow:auto;">
      <table class="table">
        <thead><tr><th>Fecha</th><th>Descripción</th><th>Pasarela</th><th>Monto</th><th>Estado</th></tr></thead>
        <tbody>
          <tr v-for="p in payments" :key="p.id">
            <td class="muted">{{ new Date(p.created_at).toLocaleString('es-MX') }}</td>
            <td>{{ p.description }}</td>
            <td><span class="badge">{{ p.provider }}</span></td>
            <td class="mono"><b>{{ peso(p.amount_mxn) }}</b></td>
            <td>
              <span class="badge" :class="{ success: p.status==='succeeded', warn: p.status==='pending', danger: p.status==='failed' }">{{ p.status }}</span>
            </td>
          </tr>
          <tr v-if="!payments.length"><td colspan="5" class="muted" style="text-align:center; padding:30px;">Sin cobros aún.</td></tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<style scoped>
.head h1 { font-size:30px; letter-spacing:-0.03em; font-weight:800; margin:0; }
.head { margin-bottom:24px; }
.radio-row { display:flex; gap:10px; }
.radio { flex:1; border:1.5px solid var(--border-strong); border-radius:10px; padding:12px; cursor:pointer; display:flex; align-items:center; gap:6px; font-size:14px; transition:all .15s; }
.radio.sel { border-color:var(--violet); background:var(--violet-soft); }
.radio input { width:auto; }
.plan-row { display:flex; align-items:center; padding:10px 0; border-bottom:1px dashed var(--border); }
.plan-row:last-child { border:none; }
</style>
