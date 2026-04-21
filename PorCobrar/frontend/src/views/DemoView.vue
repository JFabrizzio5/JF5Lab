<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const industry = ref('servicios')
const loading = ref(false)
const err = ref('')

async function seed() {
  loading.value = true
  err.value = ''
  try {
    const { data } = await api.post(`/demo/seed?industry=${industry.value}`)
    session.setTenant(data.tenant_id, data.tenant_slug || 'Demo tenant', data.industry)
    router.push('/app/dashboard')
  } catch(e) {
    err.value = e.response?.data?.detail || e.message
  }
  loading.value = false
}

const industries = [
  { id: 'servicios',   name: 'Servicios',     icon: 'mdi-briefcase-variant-outline', desc: '15 clientes, facturas $35K-$180K. Crédito 30d.' },
  { id: 'manufactura', name: 'Manufactura',   icon: 'mdi-factory',                    desc: 'Clientes industriales, facturas $50K-$2M. Crédito 60d.' },
  { id: 'comercio',    name: 'Comercio',      icon: 'mdi-store-outline',              desc: 'Distribuidora, 20 clientes, tickets $5K-$50K.' },
  { id: 'legal',       name: 'Despacho legal',icon: 'mdi-scale-balance',              desc: 'Honorarios mensuales + proyectos $20K-$500K.' },
]
</script>

<template>
  <div class="hero-grad" style="min-height:100vh;">
    <header class="container" style="padding: 22px 22px; display:flex; justify-content:space-between;">
      <router-link to="/" style="display:flex; align-items:center; gap:8px; color:var(--text); font-weight:700;">
        <i class="mdi mdi-cash-fast" style="color:var(--cash); font-size:22px"></i> PorCobrar
      </router-link>
      <router-link to="/" class="btn btn-ghost btn-sm"><i class="mdi mdi-arrow-left"></i> Inicio</router-link>
    </header>

    <div class="container" style="max-width:760px; padding: 40px 22px;">
      <div class="badge cash" style="margin-bottom: 12px"><i class="mdi mdi-play-circle"></i> DEMO</div>
      <h1>Genera un tenant con datos reales</h1>
      <p class="muted">Elige una vertical y creamos deudores, facturas y un dunning flow estándar de 3 toques.</p>

      <div class="grid-2" style="margin-top: 26px">
        <div class="card" v-for="i in industries" :key="i.id"
             :style="{ borderColor: industry === i.id ? 'var(--cash)' : '' }"
             @click="industry = i.id" style="cursor:pointer">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom: 8px">
            <i class="mdi" :class="i.icon" style="font-size: 24px; color: var(--cash)"></i>
            <h3>{{ i.name }}</h3>
            <i class="mdi mdi-check-circle" v-if="industry === i.id" style="color:var(--cash); margin-left:auto"></i>
          </div>
          <p class="muted" style="font-size: 13px; margin: 0">{{ i.desc }}</p>
        </div>
      </div>

      <div style="margin-top: 26px; display:flex; gap: 10px; align-items:center">
        <button class="btn btn-primary btn-lg" :disabled="loading" @click="seed">
          <i class="mdi mdi-rocket-launch-outline"></i> {{ loading ? 'Generando...' : 'Crear demo ' + industry }}
        </button>
        <span class="muted" style="font-size:12px">Esto crea un tenant aislado con RLS. Puedes borrarlo luego.</span>
      </div>

      <div v-if="err" class="card" style="margin-top: 20px; border-color: var(--danger);">
        <div style="color:var(--danger)"><i class="mdi mdi-alert-circle-outline"></i> {{ err }}</div>
      </div>
    </div>
  </div>
</template>
