<template>
  <div>
    <div class="page-header">
      <h1>Ajustes del Venue</h1>
      <p>Configura tu perfil, apariencia y pagos</p>
    </div>

    <div class="page-body">
      <div v-if="loading" style="color:var(--text2)">Cargando...</div>

      <template v-else>
        <!-- Success/error -->
        <div v-if="saveSuccess" class="alert-success">✅ Cambios guardados correctamente</div>
        <div v-if="saveError" class="alert-error">{{ saveError }}</div>

        <div class="settings-grid">
          <!-- Profile -->
          <div class="card">
            <h3 class="section-title">Información básica</h3>
            <div class="form-group">
              <label>Nombre del venue *</label>
              <input v-model="form.name" type="text" />
            </div>
            <div class="form-group">
              <label>Tagline</label>
              <input v-model="form.tagline" type="text" placeholder="El lugar para tus momentos especiales" />
            </div>
            <div class="form-group">
              <label>Descripción</label>
              <textarea v-model="form.description" rows="4"></textarea>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Teléfono</label>
                <input v-model="form.phone" type="tel" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="form.email" type="email" />
              </div>
            </div>
            <div class="form-group">
              <label>Dirección</label>
              <input v-model="form.address" type="text" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Ciudad</label>
                <input v-model="form.city" type="text" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Latitud</label>
                <input v-model.number="form.lat" type="number" step="any" />
              </div>
              <div class="form-group">
                <label>Longitud</label>
                <input v-model.number="form.lng" type="number" step="any" />
              </div>
            </div>
          </div>

          <!-- Branding -->
          <div class="card">
            <h3 class="section-title">Identidad visual</h3>
            <div class="form-group">
              <label>URL del logo</label>
              <input v-model="form.logo_url" type="url" />
              <img v-if="form.logo_url" :src="form.logo_url" class="preview-img" alt="Logo preview" />
            </div>
            <div class="form-group">
              <label>URL de la imagen de portada</label>
              <input v-model="form.cover_url" type="url" />
              <img v-if="form.cover_url" :src="form.cover_url" class="preview-cover" alt="Cover preview" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Color principal</label>
                <div style="display:flex;gap:.5rem;align-items:center">
                  <input v-model="form.theme_color" type="color" style="width:50px;height:38px;padding:2px" />
                  <input v-model="form.theme_color" type="text" style="flex:1" />
                </div>
              </div>
              <div class="form-group">
                <label>Color de acento</label>
                <div style="display:flex;gap:.5rem;align-items:center">
                  <input v-model="form.accent_color" type="color" style="width:50px;height:38px;padding:2px" />
                  <input v-model="form.accent_color" type="text" style="flex:1" />
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Galería (URLs separadas por coma)</label>
              <textarea v-model="galleryInput" rows="3" placeholder="https://..., https://..."></textarea>
            </div>
            <div class="form-group">
              <label>Amenidades (separadas por coma)</label>
              <input v-model="amenitiesInput" type="text" placeholder="Estacionamiento, WiFi, Sonido..." />
            </div>
          </div>

          <!-- WhatsApp -->
          <div class="card">
            <h3 class="section-title">WhatsApp</h3>
            <div class="form-group">
              <label>Número de WhatsApp (con código de país, sin +)</label>
              <input v-model="form.whatsapp_number" type="text" placeholder="525512345678" />
            </div>
            <div class="form-group">
              <label>Mensaje predeterminado</label>
              <textarea v-model="form.whatsapp_message" rows="3"></textarea>
            </div>
            <div v-if="form.whatsapp_number" class="wa-preview">
              <span>Vista previa:</span>
              <a :href="`https://wa.me/${form.whatsapp_number}?text=${encodeURIComponent(form.whatsapp_message || '')}`"
                 target="_blank" class="btn-wa">
                💬 Abrir WhatsApp
              </a>
            </div>
          </div>

          <!-- Stripe -->
          <div class="card stripe-section">
            <h3 class="section-title">💳 Pagos con Stripe</h3>
            <div v-if="venue?.stripe_onboarding_complete" class="stripe-connected">
              <div class="stripe-connected-icon">✅</div>
              <div>
                <p class="stripe-connected-title">Cuenta Stripe conectada</p>
                <p class="stripe-account-id">{{ venue.stripe_account_id }}</p>
                <p class="stripe-fee-note">
                  Recibirás pagos directamente. La plataforma retiene
                  <strong>{{ venue.platform_fee_percent }}%</strong> de cada transacción.
                </p>
              </div>
            </div>
            <div v-else class="stripe-disconnected">
              <p>Conecta tu cuenta Stripe para recibir pagos de tus clientes directamente.</p>
              <p style="margin:.75rem 0">
                La plataforma retiene <strong>{{ venue?.platform_fee_percent }}%</strong> de cada transacción.
              </p>
              <button @click="connectStripe" class="btn-stripe" :disabled="connectingStripe">
                <img src="https://b.stripecdn.com/manage-statics-srv/assets/images/brand/stripe-wordmark--blurple.svg"
                  height="20" alt="Stripe" />
                {{ connectingStripe ? 'Redirigiendo...' : 'Conectar con Stripe' }}
              </button>
            </div>
          </div>

          <!-- Public URL -->
          <div class="card">
            <h3 class="section-title">URL pública</h3>
            <div class="public-url-box">
              <span class="url-prefix">{{ origin }}/v/</span>
              <span class="url-slug">{{ venue?.slug }}</span>
            </div>
            <a :href="`/v/${venue?.slug}`" target="_blank" class="btn btn-ghost btn-sm" style="margin-top:.75rem">
              🌐 Ver landing pública
            </a>
          </div>
        </div>

        <div style="margin-top:1.5rem">
          <button @click="saveSettings" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : 'Guardar cambios' }}
          </button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/index.js'

const loading = ref(true)
const saving = ref(false)
const connectingStripe = ref(false)
const saveSuccess = ref(false)
const saveError = ref('')
const venue = ref(null)
const galleryInput = ref('')
const amenitiesInput = ref('')
const origin = window.location.origin

const form = ref({
  name: '', tagline: '', description: '', logo_url: '', cover_url: '',
  theme_color: '#7c3aed', accent_color: '#f59e0b',
  phone: '', email: '', whatsapp_number: '', whatsapp_message: '',
  address: '', city: '', lat: null, lng: null,
  gallery_json: null, amenities_json: null,
})

const route = useRoute()

onMounted(async () => {
  try {
    const { data } = await api.get('/venues/me')
    venue.value = data
    Object.keys(form.value).forEach(k => {
      if (data[k] !== undefined) form.value[k] = data[k]
    })
    try { galleryInput.value = JSON.parse(data.gallery_json || '[]').join(', ') } catch { galleryInput.value = '' }
    try { amenitiesInput.value = JSON.parse(data.amenities_json || '[]').join(', ') } catch { amenitiesInput.value = '' }

    if (route.query.stripe === 'connected') {
      saveSuccess.value = true
      setTimeout(() => saveSuccess.value = false, 4000)
    }
  } catch (e) {
    saveError.value = 'No se pudo cargar la configuración del venue'
  } finally {
    loading.value = false
  }
})

async function saveSettings() {
  saving.value = true
  saveSuccess.value = false
  saveError.value = ''
  try {
    const payload = { ...form.value }
    payload.gallery_json = galleryInput.value
      ? JSON.stringify(galleryInput.value.split(',').map(s => s.trim()).filter(Boolean))
      : null
    payload.amenities_json = amenitiesInput.value
      ? JSON.stringify(amenitiesInput.value.split(',').map(s => s.trim()).filter(Boolean))
      : null

    const { data } = await api.put('/venues/me', payload)
    venue.value = data
    saveSuccess.value = true
    setTimeout(() => saveSuccess.value = false, 3000)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Error al guardar'
  } finally {
    saving.value = false
  }
}

async function connectStripe() {
  connectingStripe.value = true
  try {
    const { data } = await api.post('/payments/stripe-connect')
    window.location.href = data.url
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Error al conectar con Stripe'
    connectingStripe.value = false
  }
}
</script>

<style scoped>
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.preview-img {
  margin-top: 0.75rem;
  height: 64px;
  border-radius: 8px;
  object-fit: contain;
  background: var(--bg);
}

.preview-cover {
  margin-top: 0.75rem;
  width: 100%;
  height: 120px;
  border-radius: 8px;
  object-fit: cover;
}

.wa-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: var(--text2);
}

.btn-wa {
  background: #25d366;
  color: white;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
}

.stripe-section .section-title { border-bottom: none; }

.stripe-connected {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 10px;
  padding: 1.25rem;
}

.stripe-connected-icon { font-size: 1.5rem; }

.stripe-connected-title { font-weight: 700; margin-bottom: 0.25rem; }
.stripe-account-id { font-size: 0.78rem; color: var(--text2); font-family: monospace; }
.stripe-fee-note { font-size: 0.85rem; color: var(--text2); margin-top: 0.5rem; }

.stripe-disconnected {
  background: rgba(255,255,255,0.02);
  border: 1px dashed var(--border);
  border-radius: 10px;
  padding: 1.5rem;
  font-size: 0.9rem;
  color: var(--text2);
}

.btn-stripe {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: #635bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.75rem;
}

.btn-stripe:hover { background: #5147e7; }
.btn-stripe:disabled { opacity: 0.6; cursor: not-allowed; }

.public-url-box {
  display: flex;
  align-items: center;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-family: monospace;
  font-size: 0.9rem;
}

.url-prefix { color: var(--text2); }
.url-slug { color: var(--primary); font-weight: 700; }

.alert-success {
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.3);
  color: #34d399;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.alert-error {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #f87171;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

@media (max-width: 900px) {
  .settings-grid { grid-template-columns: 1fr; }
}
</style>
