<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>{{ conv.id ? 'Configuración de Convención' : 'Nueva Convención' }}</h1>
        <div style="display:flex;gap:10px">
          <router-link v-if="conv.slug" :to="`/c/${conv.slug}`" target="_blank" class="btn btn-ghost btn-sm">Ver pública →</router-link>
          <button @click="save" class="btn btn-primary" :disabled="saving">{{ saving ? 'Guardando...' : 'Guardar' }}</button>
        </div>
      </div>

      <div v-if="msg" class="success-msg">{{ msg }}</div>

      <div class="settings-grid">
        <!-- Basic Info -->
        <div class="settings-section">
          <h2>Información básica</h2>
          <div class="form-group"><label>Nombre *</label><input v-model="form.name" placeholder="MexiCon 2025" /></div>
          <div class="form-group"><label>Slug (URL) *</label><input v-model="form.slug" placeholder="mexican-2025" /></div>
          <div class="form-group"><label>Edición</label><input v-model="form.edition" placeholder="2025 Edition" /></div>
          <div class="form-group"><label>Tagline</label><input v-model="form.tagline" placeholder="La convención de..." /></div>
          <div class="form-group"><label>Descripción</label><textarea v-model="form.description" rows="4" placeholder="Descripción completa..."></textarea></div>
          <div class="form-group"><label>Sitio web</label><input v-model="form.website" placeholder="https://..." /></div>
          <div class="form-group"><label>Reglas / Código de conducta</label><textarea v-model="form.rules_text" rows="3"></textarea></div>
        </div>

        <!-- Visual -->
        <div class="settings-section">
          <h2>Identidad Visual</h2>
          <div class="form-group"><label>Logo URL</label><input v-model="form.logo_url" placeholder="https://..." /></div>
          <div class="form-group"><label>Cover URL</label><input v-model="form.cover_url" placeholder="https://..." /></div>
          <div class="form-group"><label>Banner URL (hero wide)</label><input v-model="form.banner_url" placeholder="https://..." /></div>
          <div class="colors-row">
            <div class="form-group">
              <label>Color Principal</label>
              <div class="color-input-row">
                <input type="color" v-model="form.theme_color" class="color-picker" />
                <input v-model="form.theme_color" placeholder="#7c3aed" />
              </div>
            </div>
            <div class="form-group">
              <label>Color Acento</label>
              <div class="color-input-row">
                <input type="color" v-model="form.accent_color" class="color-picker" />
                <input v-model="form.accent_color" placeholder="#f59e0b" />
              </div>
            </div>
            <div class="form-group">
              <label>Color Fondo</label>
              <div class="color-input-row">
                <input type="color" v-model="form.bg_color" class="color-picker" />
                <input v-model="form.bg_color" placeholder="#0a0a0f" />
              </div>
            </div>
          </div>
          <div class="form-group">
            <label>Estilo de fuente</label>
            <select v-model="form.font_style">
              <option value="modern">Moderno</option>
              <option value="retro">Retro</option>
              <option value="elegant">Elegante</option>
              <option value="gaming">Gaming</option>
            </select>
          </div>
        </div>

        <!-- Location & Dates -->
        <div class="settings-section">
          <h2>Fecha & Lugar</h2>
          <div class="form-group"><label>Nombre del venue</label><input v-model="form.venue_name" /></div>
          <div class="form-group"><label>Dirección</label><input v-model="form.address" /></div>
          <div class="form-group"><label>Ciudad</label><input v-model="form.city" /></div>
          <div class="form-row">
            <div class="form-group"><label>Latitud</label><input v-model.number="form.lat" type="number" step="any" /></div>
            <div class="form-group"><label>Longitud</label><input v-model.number="form.lng" type="number" step="any" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Fecha inicio</label><input v-model="form.start_date" type="datetime-local" /></div>
            <div class="form-group"><label>Fecha fin</label><input v-model="form.end_date" type="datetime-local" /></div>
          </div>
          <div class="form-group"><label>Máximo de asistentes</label><input v-model.number="form.max_attendees" type="number" /></div>
          <div class="form-group"><label>Status</label>
            <select v-model="form.status">
              <option value="draft">Borrador</option>
              <option value="published">Publicado</option>
              <option value="live">En vivo</option>
              <option value="finished">Finalizado</option>
            </select>
          </div>
        </div>

        <!-- Social -->
        <div class="settings-section">
          <h2>Redes Sociales</h2>
          <div class="form-group"><label>Twitter/X</label><input v-model="social.twitter" placeholder="@handle" /></div>
          <div class="form-group"><label>Instagram</label><input v-model="social.instagram" placeholder="@handle" /></div>
          <div class="form-group"><label>Facebook</label><input v-model="social.facebook" placeholder="Página de Facebook" /></div>
          <div class="form-group"><label>TikTok</label><input v-model="social.tiktok" placeholder="@handle" /></div>
        </div>

        <!-- Stripe -->
        <div class="settings-section stripe-section">
          <h2>💳 Pagos & Comisiones (Stripe Connect)</h2>
          <div class="form-group">
            <label>Fee de plataforma (%)</label>
            <input v-model.number="form.platform_fee_percent" type="number" min="0" max="30" step="0.5" />
          </div>

          <div v-if="conv.stripe_onboarding_complete" class="stripe-ok">
            <div class="stripe-badge">✅ Stripe Conectado</div>
            <p class="stripe-id">ID: {{ conv.stripe_account_id }}</p>
            <p>Los pagos van directo a tu cuenta. La plataforma retiene <strong>{{ form.platform_fee_percent }}%</strong></p>
          </div>

          <div v-else class="stripe-pending">
            <div class="fee-visual">
              <div class="fee-bar">
                <div class="fee-yours" :style="`width:${100 - form.platform_fee_percent}%`">
                  {{ 100 - form.platform_fee_percent }}% tuyo
                </div>
                <div class="fee-platform" :style="`width:${form.platform_fee_percent}%`">
                  {{ form.platform_fee_percent }}% plataforma
                </div>
              </div>
            </div>
            <p class="fee-example">
              Ejemplo: venta de $1,000 → tú recibes <strong>${{ (1000 * (100 - form.platform_fee_percent) / 100).toFixed(0) }}</strong>,
              plataforma retiene <strong>${{ (1000 * form.platform_fee_percent / 100).toFixed(0) }}</strong>
            </p>
            <button @click="connectStripe" class="btn-stripe-connect" :disabled="!conv.id">
              <span>⚡</span> Conectar con Stripe →
            </button>
            <div v-if="!conv.id" class="stripe-note">Guarda la convención primero para habilitar Stripe</div>
            <div v-if="stripeMsg" class="stripe-msg" :class="stripeMsg === 'connected' ? 'ok' : 'err'">
              {{ stripeMsg === 'connected' ? '✅ Stripe conectado exitosamente' : '❌ Error al conectar Stripe. Verifica tu configuración.' }}
            </div>
          </div>
        </div>
      </div>

      <div style="margin-top:24px;display:flex;justify-content:flex-end">
        <button @click="save" class="btn btn-primary" :disabled="saving">{{ saving ? 'Guardando...' : 'Guardar Configuración' }}</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const route = useRoute()
const conv = ref({})
const saving = ref(false)
const msg = ref('')
const stripeMsg = ref(route.query.stripe || '')

const form = ref({
  name: '', slug: '', edition: '', tagline: '', description: '',
  logo_url: '', cover_url: '', banner_url: '',
  theme_color: '#7c3aed', accent_color: '#f59e0b', bg_color: '#0a0a0f',
  font_style: 'modern', venue_name: '', address: '', city: '',
  lat: null, lng: null, start_date: '', end_date: '',
  status: 'draft', max_attendees: null, website: '',
  rules_text: '', platform_fee_percent: 5.0,
})

const social = ref({ twitter: '', instagram: '', facebook: '', tiktok: '' })

function loadConv(c) {
  conv.value = c
  Object.assign(form.value, {
    name: c.name || '',
    slug: c.slug || '',
    edition: c.edition || '',
    tagline: c.tagline || '',
    description: c.description || '',
    logo_url: c.logo_url || '',
    cover_url: c.cover_url || '',
    banner_url: c.banner_url || '',
    theme_color: c.theme_color || '#7c3aed',
    accent_color: c.accent_color || '#f59e0b',
    bg_color: c.bg_color || '#0a0a0f',
    font_style: c.font_style || 'modern',
    venue_name: c.venue_name || '',
    address: c.address || '',
    city: c.city || '',
    lat: c.lat || null,
    lng: c.lng || null,
    start_date: c.start_date ? c.start_date.slice(0, 16) : '',
    end_date: c.end_date ? c.end_date.slice(0, 16) : '',
    status: c.status || 'draft',
    max_attendees: c.max_attendees || null,
    website: c.website || '',
    rules_text: c.rules_text || '',
    platform_fee_percent: c.platform_fee_percent || 5.0,
  })
  if (c.social_json) {
    try { Object.assign(social.value, JSON.parse(c.social_json)) } catch {}
  }
}

async function save() {
  saving.value = true
  msg.value = ''
  try {
    const payload = {
      ...form.value,
      social_json: JSON.stringify(social.value),
    }
    let result
    if (conv.value.id) {
      result = await api.put(`/conventions/${conv.value.id}`, payload)
    } else {
      result = await api.post('/conventions/', payload)
    }
    loadConv(result.data)
    msg.value = '✅ Guardado exitosamente'
    setTimeout(() => msg.value = '', 3000)
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al guardar')
  } finally {
    saving.value = false
  }
}

async function connectStripe() {
  try {
    const { data } = await api.post(`/payments/stripe-connect/${conv.value.id}`)
    window.location.href = data.url
  } catch (e) {
    alert(e.response?.data?.detail || 'Stripe no configurado en el servidor. Agrega STRIPE_CLIENT_ID y STRIPE_SECRET_KEY.')
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get('/conventions/my')
    loadConv(data)
  } catch {}
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.settings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.settings-section { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px; display: flex; flex-direction: column; gap: 14px; }
.settings-section h2 { font-size: 16px; font-weight: 700; border-bottom: 1px solid var(--border); padding-bottom: 12px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.colors-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.color-input-row { display: flex; gap: 8px; align-items: center; }
.color-picker { width: 40px !important; height: 40px; padding: 2px; border-radius: 6px; cursor: pointer; flex-shrink: 0; }

.success-msg { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #10b981; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; }

/* Stripe */
.stripe-section { grid-column: 1 / -1; }
.stripe-ok { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); border-radius: 10px; padding: 16px; }
.stripe-badge { font-size: 16px; font-weight: 700; color: #10b981; margin-bottom: 8px; }
.stripe-id { font-family: monospace; font-size: 12px; color: var(--text2); margin-bottom: 6px; }

.fee-visual { margin-bottom: 12px; }
.fee-bar { display: flex; height: 36px; border-radius: 8px; overflow: hidden; }
.fee-yours { background: var(--primary); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: white; transition: width 0.3s; }
.fee-platform { background: var(--text2); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: white; transition: width 0.3s; }

.fee-example { font-size: 13px; color: var(--text2); margin-bottom: 16px; }

.btn-stripe-connect {
  background: #635bff;
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: opacity 0.2s;
}
.btn-stripe-connect:hover { opacity: 0.85; }
.btn-stripe-connect:disabled { opacity: 0.5; cursor: not-allowed; }

.stripe-note { font-size: 12px; color: var(--text2); margin-top: 8px; }
.stripe-msg { margin-top: 12px; padding: 10px 14px; border-radius: 8px; font-size: 14px; font-weight: 600; }
.stripe-msg.ok { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #10b981; }
.stripe-msg.err { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #ef4444; }
</style>
