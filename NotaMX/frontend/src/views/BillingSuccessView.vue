<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const canceled = computed(() => route.meta?.canceled || route.query.canceled)
</script>

<template>
  <div class="bs-page">
    <div class="bs-card">
      <div v-if="canceled" class="ico" style="background: #fee2e2; color: #b91c1c;"><i class="mdi mdi-close-circle-outline"></i></div>
      <div v-else class="ico" style="background: var(--emerald-soft); color: var(--emerald-dark);"><i class="mdi mdi-check-circle-outline"></i></div>
      <h1>{{ canceled ? 'Pago cancelado' : '¡Pago recibido!' }}</h1>
      <p class="muted">{{ canceled ? 'Puedes intentar de nuevo cuando quieras.' : 'Te llegará el comprobante y el CFDI a tu correo.' }}</p>
      <router-link to="/app/dashboard" class="btn btn-primary">Volver al dashboard</router-link>
    </div>
  </div>
</template>

<style scoped>
.bs-page { min-height: 100vh; display: grid; place-items: center; background: var(--bg); padding: 40px 20px; }
.bs-card { background: var(--surface); border-radius: 22px; padding: 60px 40px; text-align: center; max-width: 420px; width: 100%; box-shadow: var(--shadow-lg); border: 1px solid var(--border); }
.ico { width: 72px; height: 72px; border-radius: 50%; display: grid; place-items: center; font-size: 44px; margin: 0 auto 20px; }
h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.02em; margin: 0 0 10px; }
p { margin: 0 0 24px; font-size: 15px; }
</style>
