<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Suscripción</h1>
        <p class="page-subtitle">Elige el plan que mejor se adapta a tu negocio</p>
      </div>

      <div v-if="currentSub" class="current-plan card" style="margin-bottom:24px;">
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <div>
            <div class="stat-label">Plan actual</div>
            <div style="font-size:22px;font-weight:700;margin-top:4px;">{{ currentSub.plan_details?.name || currentSub.plan }}</div>
            <div v-if="currentSub.expires_at" style="color:var(--text2);font-size:13px;margin-top:4px;">Expira: {{ formatDate(currentSub.expires_at) }}</div>
          </div>
          <span :class="planBadgeClass(currentSub.plan)" class="badge" style="font-size:15px;padding:8px 16px;">
            ${{ currentSub.price_monthly }}/mes
          </span>
        </div>
      </div>

      <div class="plans-grid">
        <div v-for="plan in plans" :key="plan.plan" class="plan-card" :class="{ current: currentSub?.plan === plan.plan, recommended: plan.plan === 'pro' }">
          <div v-if="plan.plan === 'pro'" class="plan-badge">⭐ Recomendado</div>
          <div class="plan-name">{{ plan.name }}</div>
          <div class="plan-price">${{ plan.price }}<span>/mes</span></div>
          <ul class="plan-features">
            <li>{{ plan.max_services === -1 ? 'Servicios ilimitados' : `Hasta ${plan.max_services} servicios` }}</li>
            <li v-if="plan.badge">✓ Badge verificado</li>
            <li v-if="plan.featured">✓ Aparece primero en búsquedas</li>
            <li v-if="plan.plan === 'premium'">✓ Soporte prioritario</li>
            <li v-if="plan.plan === 'premium'">✓ Estadísticas avanzadas</li>
          </ul>
          <button
            @click="subscribe(plan.plan)"
            :class="['btn', currentSub?.plan === plan.plan ? 'btn-secondary' : 'btn-primary']"
            style="width:100%;justify-content:center;margin-top:auto;"
            :disabled="subscribing === plan.plan || currentSub?.plan === plan.plan"
          >
            {{ currentSub?.plan === plan.plan ? '✓ Plan actual' : subscribing === plan.plan ? 'Procesando...' : `Activar ${plan.name}` }}
          </button>
        </div>
      </div>

      <div v-if="successMsg" class="alert-success" style="margin-top:20px;">{{ successMsg }}</div>
      <p style="color:var(--text2);font-size:12px;margin-top:20px;">* Demo — sin cobro real. En producción se integraría con Stripe.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { subApi } from '../../api/index.js'

const plans = ref([])
const currentSub = ref(null)
const subscribing = ref(null)
const successMsg = ref('')

onMounted(async () => {
  const [plansRes, subRes] = await Promise.all([subApi.plans(), subApi.me()])
  plans.value = plansRes.data
  currentSub.value = subRes.data
})

function planBadgeClass(plan) {
  return { free: 'badge-primary', basic: 'badge-primary', pro: 'badge-accent', premium: 'badge-warning' }[plan] || 'badge-primary'
}

function formatDate(dt) {
  return new Date(dt).toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' })
}

async function subscribe(plan) {
  subscribing.value = plan
  successMsg.value = ''
  try {
    const { data } = await subApi.subscribe(plan)
    successMsg.value = data.message
    const subRes = await subApi.me()
    currentSub.value = subRes.data
  } finally {
    subscribing.value = null
  }
}
</script>

<style scoped>
.plans-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.plan-card { background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; display: flex; flex-direction: column; gap: 16px; position: relative; transition: border-color 0.2s; }
.plan-card:hover { border-color: var(--primary); }
.plan-card.current { border-color: var(--accent); }
.plan-card.recommended { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary); }
.plan-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--primary); color: white; padding: 3px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; white-space: nowrap; }
.plan-name { font-size: 18px; font-weight: 700; margin-top: 8px; }
.plan-price { font-size: 36px; font-weight: 800; color: var(--primary); }
.plan-price span { font-size: 16px; font-weight: 400; color: var(--text2); }
.plan-features { list-style: none; display: flex; flex-direction: column; gap: 8px; flex: 1; }
.plan-features li { font-size: 13px; color: var(--text2); }
.plan-features li:first-child { color: var(--text); font-weight: 500; }
.alert-success { background: rgba(16,185,129,0.1); border: 1px solid var(--accent); border-radius: 8px; padding: 12px 16px; color: var(--accent); }
</style>
