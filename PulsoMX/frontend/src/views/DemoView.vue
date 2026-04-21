<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { demoApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const creating = ref(null)
const error = ref(null)

const options = [
  { id:'gym', name:'Gimnasio', icon:'mdi-dumbbell', tint:'#7c3aed' },
  { id:'yoga', name:'Yoga', icon:'mdi-meditation', tint:'#10b981' },
  { id:'coworking', name:'Coworking', icon:'mdi-monitor-dashboard', tint:'#0ea5e9' },
  { id:'dojo', name:'Dojo / MMA', icon:'mdi-karate', tint:'#ec4899' },
]

async function seed(industry) {
  creating.value = industry; error.value = null
  try {
    const { data } = await demoApi.seed(industry)
    session.set({ tenant_id: data.tenant_id, name: data.name, industry, brand_color: data.brand_color })
    router.push('/app/dashboard')
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { creating.value = null }
}
</script>

<template>
  <div class="wrap">
    <div class="container">
      <router-link to="/" class="back"><i class="mdi mdi-arrow-left"></i> Regresar</router-link>
      <h1>Elige tu giro</h1>
      <p class="muted">Te creamos un demo con miembros, clases, pagos e instructores reales.</p>
      <div class="grid-4" style="margin-top:28px;">
        <button v-for="o in options" :key="o.id" class="opt" :style="`--c:${o.tint}`" :class="{busy:creating===o.id}" @click="seed(o.id)">
          <i :class="['mdi', o.icon]"></i>
          <div class="opt-name">{{ o.name }}</div>
          <div class="opt-sub muted"><span v-if="creating===o.id"><i class="mdi mdi-loading mdi-spin"></i> Creando…</span><span v-else>Crear demo</span></div>
        </button>
      </div>
      <p v-if="error" style="color:var(--danger); margin-top:20px;">{{ error }}</p>
    </div>
  </div>
</template>

<style scoped>
.wrap { padding: 40px 24px 80px; }
.back { display: inline-flex; align-items: center; gap: 4px; margin-bottom: 20px; font-size: 14px; color: var(--text-muted); }
h1 { font-size: 42px; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 8px; }
.opt { text-align: center; padding: 32px 20px; background: var(--surface); border: 1.5px solid var(--border); border-radius: 18px; cursor: pointer; font-family: inherit; color: inherit; transition: all .2s; }
.opt:hover { transform: translateY(-4px); border-color: var(--c); box-shadow: 0 16px 32px color-mix(in srgb, var(--c) 25%, transparent); }
.opt.busy { opacity:.6; pointer-events:none; }
.opt .mdi { font-size: 40px; color: var(--c); display: block; margin-bottom: 14px; }
.opt-name { font-weight: 800; font-size: 18px; letter-spacing: -0.01em; }
.opt-sub { font-size: 13px; margin-top: 6px; }
</style>
