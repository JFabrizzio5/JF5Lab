<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { demoApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const seeding = ref(null); const error = ref(null)

const industries = [
  { id:'freelance',   name:'Freelancer diseño web', icon:'mdi-palette-outline',       c:'emerald', desc:'8 clientes, 10 productos, 15 notas mixtas (draft/sent/paid).' },
  { id:'consultorio', name:'Consultorio dental',    icon:'mdi-stethoscope',           c:'teal',    desc:'Paquetes limpieza, extracción, ortodoncia. 6 pacientes.' },
  { id:'abogados',    name:'Despacho legal',        icon:'mdi-gavel',                 c:'violet',  desc:'Honorarios fijos, juicios, consultas. Clientes corporativos.' },
  { id:'agencia',     name:'Agencia marketing',     icon:'mdi-rocket-launch-outline', c:'coral',   desc:'Retainers mensuales, campañas, producción de video.' },
]

async function tryDemo(id) {
  seeding.value = id; error.value = null
  try {
    const { data } = await demoApi.seed(id)
    if (data.error) throw new Error(data.error)
    session.set({ tenant_id: data.tenant_id, name: data.name, industry: id, brand_color: data.brand_color })
    router.push('/app/dashboard')
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { seeding.value = null }
}
</script>

<template>
  <div class="demo-page">
    <div class="demo-inner">
      <router-link to="/" class="back-link"><i class="mdi mdi-arrow-left"></i> Volver</router-link>
      <h1 class="title">Elige un <span class="gradient-text">demo</span></h1>
      <p class="muted sub">Creamos en segundos un tenant con clientes, productos y notas en estados mixtos.</p>
      <div class="grid">
        <button v-for="i in industries" :key="i.id" class="card-btn" :class="[`c-${i.c}`, { busy: seeding === i.id }]" @click="tryDemo(i.id)">
          <div class="ico"><i :class="['mdi', i.icon]"></i></div>
          <div class="name">{{ i.name }}</div>
          <div class="desc">{{ i.desc }}</div>
          <div class="cta">
            <span v-if="seeding === i.id"><i class="mdi mdi-loading mdi-spin"></i> Creando…</span>
            <span v-else>Probar <i class="mdi mdi-arrow-right"></i></span>
          </div>
        </button>
      </div>
      <p v-if="error" class="err">{{ error }}</p>
    </div>
  </div>
</template>

<style scoped>
.demo-page { min-height: 100vh; padding: 60px 24px; background: var(--bg); }
.demo-inner { max-width: 920px; margin: 0 auto; }
.back-link { color: var(--text-muted); font-size: 14px; display: inline-flex; align-items: center; gap: 4px; }
.title { font-size: clamp(32px, 5vw, 52px); font-weight: 800; letter-spacing: -0.035em; margin: 16px 0 10px; }
.sub { font-size: 17px; max-width: 560px; margin: 0 0 40px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.card-btn { text-align: left; background: var(--surface); border: 1px solid var(--border); border-radius: 18px; padding: 24px; cursor: pointer; font-family: inherit; color: inherit; transition: all .25s; }
.card-btn:hover { transform: translateY(-6px); border-color: var(--c); box-shadow: 0 20px 40px color-mix(in srgb, var(--c) 30%, transparent); }
.card-btn.busy { opacity: .6; pointer-events: none; }
.ico { width: 48px; height: 48px; border-radius: 12px; background: var(--c-soft); color: var(--c); display: grid; place-items: center; font-size: 24px; margin-bottom: 14px; }
.name { font-weight: 800; font-size: 18px; margin-bottom: 6px; }
.desc { font-size: 13.5px; color: var(--text-muted); line-height: 1.55; margin-bottom: 14px; }
.cta { font-size: 13px; color: var(--c); font-weight: 700; display: inline-flex; align-items: center; gap: 4px; }
.card-btn.c-emerald { --c: #10b981; --c-soft: var(--emerald-soft); }
.card-btn.c-teal    { --c: #14b8a6; --c-soft: var(--teal-soft); }
.card-btn.c-violet  { --c: #7c3aed; --c-soft: var(--violet-soft); }
.card-btn.c-coral   { --c: #fb7185; --c-soft: var(--coral-soft); }
.err { color: var(--danger); margin-top: 20px; }
</style>
