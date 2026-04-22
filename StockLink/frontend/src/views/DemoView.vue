<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { demoApi, tenantsApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const creating = ref(null)
const error = ref(null)
const custom = ref({ name: '', industry: 'store', rfc: '', contact_email: '' })
const showCustom = ref(false)

const options = [
  { id: 'store', name: 'Tiendita', icon: 'mdi-store' },
  { id: 'restaurant', name: 'Restaurante', icon: 'mdi-silverware-fork-knife' },
  { id: 'shipping', name: 'Paquetería', icon: 'mdi-truck-fast' },
  { id: 'construction', name: 'Constructora', icon: 'mdi-hammer-wrench' },
]

async function seed(industry) {
  creating.value = industry
  error.value = null
  try {
    const { data } = await demoApi.seed(industry)
    session.set({ tenant_id: data.tenant_id, name: data.name, industry })
    router.push('/app/dashboard')
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { creating.value = null }
}

async function createCustom() {
  creating.value = 'custom'
  error.value = null
  try {
    const { data } = await tenantsApi.create(custom.value)
    session.set(data)
    router.push('/app/dashboard')
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { creating.value = null }
}
</script>

<template>
  <div class="container" style="padding: 40px 24px 80px;">
    <router-link to="/" class="btn-ghost btn btn-sm" style="margin-bottom:20px;"><i class="mdi mdi-arrow-left"></i> Regresar</router-link>

    <h1 style="font-size:32px; letter-spacing:-0.02em; margin:0 0 8px;">Empieza con un demo</h1>
    <p class="muted" style="margin:0 0 28px;">Creamos un tenant con datos reales de tu giro. Puedes borrarlo cuando quieras.</p>

    <div class="grid-4">
      <div v-for="o in options" :key="o.id" class="card industry-card" @click="seed(o.id)" :class="{ busy: creating === o.id }">
        <i :class="['mdi', o.icon]" style="font-size:32px; color:var(--accent);"></i>
        <div style="font-weight:600; margin-top:10px;">{{ o.name }}</div>
        <div class="muted" style="font-size:13px; margin-top:4px;">
          <span v-if="creating === o.id"><i class="mdi mdi-loading mdi-spin"></i> Creando…</span>
          <span v-else>Clic para crear</span>
        </div>
      </div>
    </div>

    <div style="margin-top:40px;">
      <button class="btn-ghost btn" @click="showCustom = !showCustom">
        <i class="mdi" :class="showCustom ? 'mdi-chevron-down' : 'mdi-chevron-right'"></i>
        {{ showCustom ? 'Ocultar' : 'O crear uno propio' }}
      </button>
      <div v-if="showCustom" class="card" style="margin-top:16px; max-width:560px;">
        <label>Nombre del negocio</label>
        <input v-model="custom.name" placeholder="Mi Empresa SA" />
        <div class="grid-2" style="margin-top:14px;">
          <div>
            <label>Giro</label>
            <select v-model="custom.industry">
              <option v-for="o in options" :key="o.id" :value="o.id">{{ o.name }}</option>
              <option value="warehouse">Almacén general</option>
              <option value="pharmacy">Farmacia</option>
              <option value="workshop">Taller</option>
              <option value="clinic">Clínica</option>
              <option value="other">Otro</option>
            </select>
          </div>
          <div>
            <label>RFC (opcional)</label>
            <input v-model="custom.rfc" placeholder="XAXX010101000" maxlength="13" />
          </div>
        </div>
        <label style="margin-top:14px;">Email de contacto</label>
        <input v-model="custom.contact_email" type="email" placeholder="contacto@miempresa.mx" />
        <button class="btn btn-primary" style="margin-top:18px; width:100%; justify-content:center;"
                :disabled="!custom.name || creating === 'custom'" @click="createCustom">
          <i class="mdi mdi-rocket-launch"></i> Crear tenant
        </button>
      </div>
    </div>

    <p v-if="error" class="muted" style="color:var(--danger); margin-top:20px;">{{ error }}</p>
  </div>
</template>

<style scoped>
.industry-card { cursor: pointer; text-align: center; transition: all .2s; }
.industry-card:hover { transform: translateY(-2px); border-color: var(--accent); }
.industry-card.busy { opacity: .6; pointer-events: none; }
</style>
