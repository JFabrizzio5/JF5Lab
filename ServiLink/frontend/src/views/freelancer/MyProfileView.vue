<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Mi perfil profesional</h1>
        <p class="page-subtitle">Configura cómo te ven los clientes</p>
      </div>

      <div v-if="loading" class="loading-state">Cargando...</div>
      <div v-else style="display:flex;flex-direction:column;gap:20px;">

        <!-- Public page banner -->
        <div class="public-banner">
          <div class="public-banner-left">
            <div class="pub-icon">🌐</div>
            <div>
              <div class="pub-title">Tu página pública</div>
              <div class="pub-url">{{ publicUrl }}</div>
              <div class="pub-hint">Comparte este link con tus clientes para que puedan verte y contactarte</div>
            </div>
          </div>
          <div class="pub-actions">
            <button @click="copyLink" class="btn btn-secondary btn-sm">
              {{ copied ? '✓ Copiado' : '📋 Copiar link' }}
            </button>
            <a :href="publicUrl" target="_blank" class="btn btn-accent btn-sm">👁 Ver mi página</a>
          </div>
        </div>

        <div class="card">
          <h2 style="margin-bottom:16px;font-size:16px;">Información del servicio</h2>
          <div class="grid-2">
            <div class="field">
              <label class="label">Tarifa por hora (MXN)</label>
              <input v-model.number="form.hourly_rate" type="number" class="input" min="0" />
            </div>
            <div class="field">
              <label class="label">Años de experiencia</label>
              <input v-model.number="form.experience_years" type="number" class="input" min="0" />
            </div>
          </div>
          <div class="field">
            <label class="label">Biografía / Descripción</label>
            <textarea v-model="form.bio" class="input" rows="4" placeholder="Cuéntale a los clientes sobre ti y tus servicios..."></textarea>
          </div>
        </div>

        <div class="card">
          <h2 style="margin-bottom:16px;font-size:16px;">Ubicación</h2>
          <div class="field">
            <label class="label">Dirección</label>
            <input v-model="form.address" class="input" placeholder="Colonia, Ciudad" />
          </div>
          <div class="grid-2">
            <div class="field">
              <label class="label">Latitud</label>
              <input v-model.number="form.lat" type="number" step="0.0001" class="input" placeholder="19.4326" />
            </div>
            <div class="field">
              <label class="label">Longitud</label>
              <input v-model.number="form.lng" type="number" step="0.0001" class="input" placeholder="-99.1332" />
            </div>
          </div>
          <button @click="getLocation" class="btn btn-secondary btn-sm">📍 Usar mi ubicación actual</button>
        </div>

        <div class="card">
          <h2 style="margin-bottom:16px;font-size:16px;">Categorías de servicio</h2>
          <div class="cats-grid">
            <label v-for="c in categories" :key="c.id" class="cat-option">
              <input type="checkbox" :value="c.id" v-model="form.category_ids" />
              <span>{{ c.icon }} {{ c.name }}</span>
            </label>
          </div>
        </div>

        <div class="card" style="display:flex;align-items:center;justify-content:space-between;">
          <div>
            <div style="font-size:15px;font-weight:600;">Disponibilidad</div>
            <div style="color:var(--text2);font-size:13px;">Aparece como disponible en el mapa</div>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="form.is_available" />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <!-- Page customization -->
        <div class="card">
          <h2 style="margin-bottom:4px;font-size:16px;">🎨 Personalizar mi página pública</h2>
          <p style="font-size:13px;color:var(--text2);margin-bottom:16px;">Así se verá tu landing page cuando compartas tu link con clientes</p>

          <div class="grid-2">
            <div class="field">
              <label class="label">Tagline / Eslogan</label>
              <input v-model="form.tagline" class="input" placeholder='Ej: "El mejor plomero de la CDMX"' />
            </div>
            <div class="field">
              <label class="label">Color principal de tu página</label>
              <div style="display:flex;align-items:center;gap:10px;">
                <input type="color" v-model="form.theme_color" style="width:48px;height:38px;border-radius:8px;border:1px solid var(--border);cursor:pointer;padding:2px;" />
                <span style="font-size:13px;color:var(--text2);">{{ form.theme_color }}</span>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">URL de imagen de portada (banner)</label>
            <input v-model="form.cover_url" class="input" placeholder="https://images.unsplash.com/..." />
            <div v-if="form.cover_url" style="margin-top:8px;border-radius:8px;overflow:hidden;height:120px;">
              <img :src="form.cover_url" style="width:100%;height:100%;object-fit:cover;" @error="form.cover_url = ''" />
            </div>
          </div>
        </div>

        <!-- Services builder -->
        <div class="card">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div>
              <h2 style="font-size:16px;margin-bottom:4px;">📦 Mis servicios</h2>
              <p style="font-size:13px;color:var(--text2);">Define los servicios que ofreces con precio y descripción propios</p>
            </div>
            <button @click="addService" class="btn btn-secondary btn-sm">+ Agregar servicio</button>
          </div>

          <div v-if="services.length === 0" class="empty-services">
            Sin servicios personalizados — se mostrarán tus categorías por defecto
          </div>

          <div v-for="(svc, i) in services" :key="i" class="service-row">
            <div class="service-row-fields">
              <input v-model="svc.title" class="input" placeholder="Nombre del servicio" style="flex:2;" />
              <input v-model.number="svc.price" type="number" class="input" placeholder="Precio MXN" style="flex:1;" />
            </div>
            <textarea v-model="svc.description" class="input" rows="2" placeholder="Descripción breve..." style="margin-top:8px;"></textarea>
            <button @click="removeService(i)" class="btn-remove-svc">✕ Eliminar</button>
          </div>
        </div>

        <div v-if="successMsg" class="alert-success">{{ successMsg }}</div>
        <div v-if="errorMsg" class="alert-error">{{ errorMsg }}</div>

        <button @click="saveProfile" class="btn btn-primary btn-lg" style="align-self:flex-start;" :disabled="saving">
          {{ saving ? 'Guardando...' : 'Guardar cambios' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { profApi, categoryApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'

const auth = useAuthStore()
const publicUrl = computed(() => `${window.location.origin}/pro/${auth.user?.id}`)
const copied = ref(false)

function copyLink() {
  navigator.clipboard.writeText(publicUrl.value)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

const loading = ref(true)
const saving = ref(false)
const successMsg = ref('')
const errorMsg = ref('')
const categories = ref([])
const services = ref([])
const form = ref({
  bio: '', hourly_rate: 0, experience_years: 0,
  lat: null, lng: null, address: '', is_available: true, category_ids: [],
  cover_url: '', tagline: '', theme_color: '#6366f1',
})

onMounted(async () => {
  const [catRes, profRes] = await Promise.allSettled([categoryApi.list(), profApi.myProfile()])
  if (catRes.status === 'fulfilled') categories.value = catRes.value.data
  if (profRes.status === 'fulfilled') {
    const p = profRes.value.data
    form.value = {
      bio: p.bio || '',
      hourly_rate: p.hourly_rate,
      experience_years: p.experience_years,
      lat: p.lat, lng: p.lng, address: p.address || '',
      is_available: p.is_available,
      category_ids: categories.value.filter(c => p.categories.includes(c.name)).map(c => c.id),
      cover_url: p.cover_url || '',
      tagline: p.tagline || '',
      theme_color: p.theme_color || '#6366f1',
    }
    try { services.value = p.services_json ? JSON.parse(p.services_json) : [] } catch { services.value = [] }
  }
  loading.value = false
})

function getLocation() {
  navigator.geolocation?.getCurrentPosition(
    (pos) => { form.value.lat = pos.coords.latitude; form.value.lng = pos.coords.longitude },
    () => alert('No se pudo obtener ubicación')
  )
}

function addService() {
  services.value.push({ title: '', description: '', price: null })
}

function removeService(i) {
  services.value.splice(i, 1)
}

async function saveProfile() {
  saving.value = true
  successMsg.value = ''
  errorMsg.value = ''
  try {
    const payload = {
      ...form.value,
      services_json: JSON.stringify(services.value.filter(s => s.title.trim())),
    }
    await profApi.updateProfile(payload)
    successMsg.value = '¡Perfil actualizado correctamente!'
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Error al guardar'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.field { margin-bottom: 14px; }
.loading-state { padding: 32px; text-align: center; color: var(--text2); }

.public-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(16,185,129,0.08));
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 14px;
  flex-wrap: wrap;
}
.public-banner-left { display: flex; align-items: flex-start; gap: 16px; flex: 1; min-width: 0; }
.pub-icon { font-size: 28px; flex-shrink: 0; }
.pub-title { font-weight: 700; font-size: 15px; margin-bottom: 4px; }
.pub-url { font-size: 13px; color: var(--accent); font-family: monospace; margin-bottom: 4px; word-break: break-all; }
.pub-hint { font-size: 12px; color: var(--text2); }
.pub-actions { display: flex; gap: 8px; flex-wrap: wrap; flex-shrink: 0; }
.cats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }
.cat-option { display: flex; align-items: center; gap: 8px; padding: 10px 12px; background: var(--bg3); border: 1px solid var(--border); border-radius: 8px; cursor: pointer; font-size: 13px; transition: border-color 0.2s; }
.cat-option:hover { border-color: var(--primary); }
.cat-option input:checked + span { color: var(--primary); }
.toggle { position: relative; display: inline-block; width: 48px; height: 26px; }
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-slider { position: absolute; inset: 0; background: var(--border); border-radius: 26px; transition: 0.3s; cursor: pointer; }
.toggle-slider::before { content: ''; position: absolute; width: 20px; height: 20px; left: 3px; top: 3px; background: white; border-radius: 50%; transition: 0.3s; }
input:checked + .toggle-slider { background: var(--accent); }
input:checked + .toggle-slider::before { transform: translateX(22px); }
.alert-success { background: rgba(16,185,129,0.1); border: 1px solid var(--accent); border-radius: 8px; padding: 10px 14px; color: var(--accent); font-size: 14px; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 10px 14px; color: var(--danger); font-size: 14px; }

.empty-services { color: var(--text2); font-size: 13px; text-align: center; padding: 20px; border: 1px dashed var(--border); border-radius: 8px; }
.service-row { background: var(--bg3); border: 1px solid var(--border); border-radius: 10px; padding: 14px; margin-bottom: 10px; }
.service-row-fields { display: flex; gap: 10px; }
.btn-remove-svc { margin-top: 8px; background: transparent; border: none; color: var(--danger); font-size: 12px; cursor: pointer; padding: 4px 0; }
</style>
