<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiSeed } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const loading = ref(false)
const error = ref('')

const options = [
  { id: 'barber',  icon: 'content-cut',     title: 'Barbería El Corte', sub: '3 barberos · 6 servicios · 20 citas demo' },
  { id: 'dentist', icon: 'tooth-outline',   title: 'Clínica Dental Sonrisa', sub: '2 dentistas · 4 servicios · depósito obligatorio' },
  { id: 'vet',     icon: 'paw-outline',     title: 'Vet Amigo', sub: '2 MVZ · 4 servicios · consulta $400' },
  { id: 'coach',   icon: 'bullseye-arrow',  title: 'Coach Flow', sub: '1 coach · sesión intro gratis · paquetes' },
]

async function pick(industry) {
  loading.value = true; error.value = ''
  try {
    const r = await apiSeed(industry)
    if (r.error) throw new Error(r.error)
    session.set({
      tenant_id: r.tenant_id, name: r.name,
      industry: r.industry, brand_color: r.brand_color,
      slug: r.slug,
    })
    router.push('/app/dashboard')
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || 'Error al crear demo'
  } finally { loading.value = false }
}
</script>

<template>
  <div class="demo-shell">
    <div class="demo-card">
      <router-link to="/" class="back">
        <i class="mdi mdi-arrow-left"></i> Inicio
      </router-link>
      <h1 class="serif">Elige tu <em>demo.</em></h1>
      <p class="muted">Creamos un negocio con servicios, staff, horarios y 20 citas reales de los próximos 7 días.</p>

      <div class="options">
        <button v-for="o in options" :key="o.id"
                :disabled="loading" @click="pick(o.id)"
                class="opt-card">
          <div class="opt-icon"><i :class="'mdi mdi-' + o.icon"></i></div>
          <div class="opt-body">
            <div class="opt-title">{{ o.title }}</div>
            <div class="opt-sub">{{ o.sub }}</div>
          </div>
          <i class="mdi mdi-arrow-right opt-arrow"></i>
        </button>
      </div>

      <div v-if="loading" class="state">
        <i class="mdi mdi-loading mdi-spin"></i> Preparando tu demo...
      </div>
      <div v-if="error" class="err">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.demo-shell {
  min-height: 100vh; display: grid; place-items: center;
  padding: 40px 20px; background: var(--cream);
}
.demo-card {
  max-width: 560px; width: 100%;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 44px 40px;
  box-shadow: var(--shadow-lg);
}
.back {
  color: var(--muted); font-size: 13px;
  display: inline-flex; align-items: center; gap: 4px; margin-bottom: 24px;
}
.back:hover { color: var(--navy); }
h1 {
  font-size: 36px; letter-spacing: -0.02em; margin: 0 0 10px;
  color: var(--navy); font-weight: 500;
}
h1 em { color: var(--gold); font-style: italic; font-weight: 600; }

.options { display: flex; flex-direction: column; gap: 10px; margin-top: 32px; }
.opt-card {
  display: flex; align-items: center; gap: 18px;
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: var(--radius); padding: 18px 20px;
  cursor: pointer; transition: all .18s; text-align: left;
  font-family: inherit; width: 100%;
}
.opt-card:hover { border-color: var(--navy); transform: translateY(-2px); box-shadow: var(--shadow-md); }
.opt-card:disabled { opacity: 0.5; cursor: wait; }

.opt-icon {
  width: 44px; height: 44px; border-radius: 10px;
  background: var(--navy); color: var(--cream);
  display: grid; place-items: center; font-size: 22px; flex-shrink: 0;
}
.opt-body { flex: 1; min-width: 0; }
.opt-title { font-family: var(--serif); font-size: 18px; color: var(--navy); margin-bottom: 2px; font-weight: 600; }
.opt-sub { font-size: 12px; color: var(--muted); }
.opt-arrow { font-size: 20px; color: var(--gold); }

.state {
  text-align: center; color: var(--muted); margin-top: 24px;
  font-size: 14px;
}
.mdi-spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.err { margin-top: 20px; color: var(--danger); font-size: 13px; text-align: center; }
</style>
