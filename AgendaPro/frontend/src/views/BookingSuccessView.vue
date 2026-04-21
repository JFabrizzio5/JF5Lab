<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({ canceled: { type: Boolean, default: false } })
const route = useRoute()
const ref_ = computed(() => route.query.ref || '')
</script>

<template>
  <div class="success-shell">
    <div class="success-card">
      <div class="success-icon" v-if="!canceled">
        <i class="mdi mdi-check-circle-outline"></i>
      </div>
      <div class="success-icon" style="background:var(--danger);" v-else>
        <i class="mdi mdi-close-circle-outline"></i>
      </div>
      <h1 class="serif">
        <span v-if="!canceled">¡Cita <em>confirmada!</em></span>
        <span v-else>Pago <em>cancelado.</em></span>
      </h1>
      <p class="muted">
        <span v-if="!canceled">Tu reserva está lista. Te enviaremos un WhatsApp con el recordatorio 24h antes.</span>
        <span v-else>No te preocupes, tu horario sigue reservado por unos minutos. Vuelve a intentar cuando quieras.</span>
      </p>
      <div class="ref" v-if="ref_">Ref: <code>{{ ref_ }}</code></div>
      <router-link to="/" class="btn btn-primary" style="margin-top:24px;">
        <i class="mdi mdi-home-outline"></i> Volver a AgendaPro
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.success-shell {
  min-height: 100vh; display: grid; place-items: center;
  padding: 40px 20px; background: var(--cream);
}
.success-card {
  max-width: 480px; width: 100%;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 48px 40px;
  box-shadow: var(--shadow-lg); text-align: center;
}
.success-icon {
  width: 72px; height: 72px; border-radius: 50%;
  background: var(--success); color: var(--cream);
  display: grid; place-items: center;
  font-size: 44px; margin: 0 auto 24px;
}
h1 { font-size: 34px; letter-spacing: -0.02em; margin: 0 0 12px; color: var(--navy); font-weight: 500; }
h1 em { color: var(--gold); font-style: italic; font-weight: 600; }
.ref { font-size: 12px; color: var(--muted); margin-top: 10px; }
.ref code { background: var(--cream-2); padding: 2px 8px; border-radius: 6px; }
</style>
