<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute(); const router = useRouter()
const ref_ = ref(route.query.ref || '')
const canceled = route.path.includes('cancel')
</script>

<template>
  <div class="wrap">
    <div class="card">
      <div class="ic" :class="{ cancel: canceled }">
        <i class="mdi" :class="canceled ? 'mdi-close-circle-outline' : 'mdi-check-decagram'"></i>
      </div>
      <h1>{{ canceled ? 'Pago cancelado' : '¡Pago exitoso!' }}</h1>
      <p class="muted">{{ canceled ? 'No se hizo ningún cargo. Puedes intentar de nuevo cuando quieras.' : 'Tu suscripción quedó activa. Ya puedes entrar a tu dashboard.' }}</p>
      <div class="muted mono" style="margin:12px 0 24px;" v-if="ref_">ref: {{ ref_ }}</div>
      <div style="display:flex; gap:8px; justify-content:center;">
        <router-link to="/app/dashboard" class="btn btn-gradient"><i class="mdi mdi-view-dashboard"></i> Ir al dashboard</router-link>
        <router-link to="/" class="btn">Regresar</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrap { min-height: 100vh; display: grid; place-items: center; padding: 40px 20px; }
.card { max-width: 480px; text-align: center; padding: 48px 32px; }
.ic { width: 80px; height: 80px; margin: 0 auto 20px; border-radius: 50%; background: var(--emerald-soft); color: var(--emerald); display: grid; place-items: center; font-size: 44px; }
.ic.cancel { background: #fee2e2; color: #b91c1c; }
h1 { font-size: 30px; letter-spacing: -0.03em; font-weight: 800; margin: 0 0 10px; }
</style>
