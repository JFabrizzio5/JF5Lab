<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <h1 class="page-title">Configuración</h1>
      <p class="page-subtitle">Personaliza tu landing y configura pagos</p>

      <div v-if="loadingProfile" class="loading">Cargando perfil...</div>

      <template v-else>
        <!-- Tabs -->
        <div class="tabs">
          <button v-for="tab in tabs" :key="tab.key" class="tab-btn" :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
            {{ tab.icon }} {{ tab.label }}
          </button>
        </div>

        <!-- Tab: Identidad -->
        <div v-if="activeTab === 'identity'" class="tab-content card">
          <h3 class="section-label">Identidad de tu negocio</h3>
          <div class="form-grid">
            <div class="form-group">
              <label class="label">Nombre del negocio *</label>
              <input v-model="form.business_name" type="text" class="input" placeholder="Aqua Adventures" />
            </div>
            <div class="form-group">
              <label class="label">Slug (URL) *</label>
              <div class="slug-wrapper">
                <span class="slug-prefix">rentame.mx/r/</span>
                <input v-model="form.slug" type="text" class="input slug-in" placeholder="mi-negocio" />
              </div>
              <p class="field-hint">Tu landing estará en: <a :href="`/r/${form.slug}`" target="_blank" style="color: var(--primary)">{{ form.slug ? `/r/${form.slug}` : '...' }}</a></p>
            </div>
          </div>
          <div class="form-group">
            <label class="label">Tagline</label>
            <input v-model="form.tagline" type="text" class="input" placeholder="Tu slogan o frase de valor" />
          </div>
          <div class="form-group">
            <label class="label">Descripción</label>
            <textarea v-model="form.description" class="input" rows="4" placeholder="Cuéntale a tus clientes quién eres y qué ofreces..."></textarea>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label class="label">URL del logo</label>
              <input v-model="form.logo_url" type="url" class="input" placeholder="https://..." />
              <div v-if="form.logo_url" class="preview-img">
                <img :src="form.logo_url" alt="Logo preview" />
              </div>
            </div>
            <div class="form-group">
              <label class="label">URL de portada (cover)</label>
              <input v-model="form.cover_url" type="url" class="input" placeholder="https://..." />
              <div v-if="form.cover_url" class="preview-cover">
                <img :src="form.cover_url" alt="Cover preview" />
              </div>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label class="label">Color principal</label>
              <div class="color-row">
                <input type="color" v-model="form.theme_color" class="color-picker" />
                <input v-model="form.theme_color" type="text" class="input color-text" placeholder="#6366f1" />
              </div>
              <div class="color-preview" :style="{ background: form.theme_color }">
                <span style="color: white; font-size: 12px; font-weight: 600;">Tu color principal</span>
              </div>
            </div>
            <div class="form-group">
              <label class="label">Color de acento</label>
              <div class="color-row">
                <input type="color" v-model="form.accent_color" class="color-picker" />
                <input v-model="form.accent_color" type="text" class="input color-text" placeholder="#f59e0b" />
              </div>
              <div class="color-preview" :style="{ background: form.accent_color }">
                <span style="color: #07070d; font-size: 12px; font-weight: 600;">Tu color de acento</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Contacto -->
        <div v-if="activeTab === 'contact'" class="tab-content card">
          <h3 class="section-label">Información de contacto y redes sociales</h3>
          <div class="form-grid">
            <div class="form-group">
              <label class="label">Teléfono</label>
              <input v-model="form.phone" type="tel" class="input" placeholder="+52 55 1234 5678" />
            </div>
            <div class="form-group">
              <label class="label">Correo electrónico</label>
              <input v-model="form.email" type="email" class="input" placeholder="info@tunegocio.mx" />
            </div>
          </div>
          <div class="form-group">
            <label class="label">WhatsApp (formato: 52XXXXXXXXXX)</label>
            <input v-model="form.whatsapp" type="text" class="input" placeholder="527441234567" />
            <p class="field-hint">Sin +, sin espacios ni guiones. Ej: 527441234567</p>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label class="label">Facebook URL</label>
              <input v-model="form.facebook_url" type="url" class="input" placeholder="https://facebook.com/tunegocio" />
            </div>
            <div class="form-group">
              <label class="label">Instagram URL</label>
              <input v-model="form.instagram_url" type="url" class="input" placeholder="https://instagram.com/tunegocio" />
            </div>
            <div class="form-group">
              <label class="label">TikTok URL</label>
              <input v-model="form.tiktok_url" type="url" class="input" placeholder="https://tiktok.com/@tunegocio" />
            </div>
            <div class="form-group">
              <label class="label">Sitio web</label>
              <input v-model="form.website_url" type="url" class="input" placeholder="https://tunegocio.mx" />
            </div>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label class="label">Dirección</label>
              <input v-model="form.address" type="text" class="input" placeholder="Marina Local 12" />
            </div>
            <div class="form-group">
              <label class="label">Ciudad</label>
              <input v-model="form.city" type="text" class="input" placeholder="Acapulco" />
            </div>
          </div>
        </div>

        <!-- Tab: Políticas -->
        <div v-if="activeTab === 'policies'" class="tab-content card">
          <h3 class="section-label">Políticas de renta</h3>
          <div class="form-group">
            <label class="label">Política de cancelación</label>
            <textarea v-model="form.cancellation_policy" class="input" rows="6" placeholder="Ej: Cancelaciones con más de 48 horas: reembolso total..."></textarea>
          </div>
          <div class="form-group">
            <label class="label">Porcentaje de depósito requerido: <strong>{{ form.deposit_percent }}%</strong></label>
            <input type="range" v-model.number="form.deposit_percent" min="0" max="100" step="5" class="range-input" />
            <div class="deposit-preview">
              <p>En una renta de <strong>$1,000</strong>: depósito requerido = <strong style="color: var(--warning)">${{ (10 * form.deposit_percent).toFixed(0) }}</strong></p>
            </div>
          </div>
        </div>

        <!-- Tab: Stripe -->
        <div v-if="activeTab === 'stripe'" class="tab-content card">
          <h3 class="section-label">💳 Stripe Connect — Recibe pagos directamente</h3>

          <div class="stripe-panel">
            <div class="fee-breakdown">
              <h4 style="margin-bottom: 12px;">Distribución de pagos</h4>
              <div class="fee-bar">
                <div class="fee-yours" :style="`width:${100 - (vendor?.platform_fee_percent || 5)}%`">
                  {{ (100 - (vendor?.platform_fee_percent || 5)).toFixed(0) }}% tuyo
                </div>
                <div class="fee-platform" :style="`width:${vendor?.platform_fee_percent || 5}%`">
                  {{ (vendor?.platform_fee_percent || 5) }}%
                </div>
              </div>
              <p class="fee-example">
                En una renta de $1,000: tú recibes
                <strong style="color: var(--success)">${{ (1000 * (100 - (vendor?.platform_fee_percent || 5)) / 100).toFixed(0) }}</strong>,
                plataforma retiene
                <strong style="color: var(--text2)">${{ (1000 * (vendor?.platform_fee_percent || 5) / 100).toFixed(0) }}</strong>
              </p>
            </div>

            <div class="stripe-status">
              <div v-if="vendor?.stripe_onboarding_complete" class="stripe-connected">
                <div class="connected-badge">✅ Cuenta Stripe conectada</div>
                <div class="connected-id">ID: {{ vendor.stripe_account_id }}</div>
                <p style="font-size: 13px; color: var(--text2); margin-top: 8px;">
                  Tu cuenta está conectada. Los pagos de tus clientes irán directamente a tu cuenta Stripe.
                </p>
              </div>
              <div v-else class="stripe-not-connected">
                <p style="color: var(--text2); font-size: 14px; margin-bottom: 16px;">
                  Conecta tu cuenta Stripe para recibir pagos directamente. El proceso toma menos de 5 minutos.
                </p>
                <button class="btn-stripe" @click="connectStripe" :disabled="stripeLoading">
                  {{ stripeLoading ? 'Conectando...' : '⚡ Conectar con Stripe →' }}
                </button>
                <div v-if="stripeError" class="error-msg" style="margin-top: 12px;">{{ stripeError }}</div>
                <div v-if="stripeSuccess" class="success-msg" style="margin-top: 12px;">{{ stripeSuccess }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Save button -->
        <div v-if="activeTab !== 'stripe'" class="save-section">
          <div v-if="saveError" class="error-msg">{{ saveError }}</div>
          <div v-if="saveSuccess" class="success-msg">{{ saveSuccess }}</div>
          <button class="btn btn-primary" @click="saveProfile" :disabled="saving">
            {{ saving ? 'Guardando...' : 'Guardar cambios' }}
          </button>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from '../../components/AppSidebar.vue'
import { vendorAPI, paymentsAPI } from '../../api/index.js'

const route = useRoute()
const loadingProfile = ref(true)
const vendor = ref(null)
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref('')
const activeTab = ref('identity')
const stripeLoading = ref(false)
const stripeError = ref('')
const stripeSuccess = ref('')

const tabs = [
  { key: 'identity', icon: '🎨', label: 'Identidad' },
  { key: 'contact', icon: '📞', label: 'Contacto y redes' },
  { key: 'policies', icon: '📋', label: 'Políticas' },
  { key: 'stripe', icon: '💳', label: 'Pagos Stripe' },
]

const form = ref({
  business_name: '',
  slug: '',
  tagline: '',
  description: '',
  logo_url: '',
  cover_url: '',
  theme_color: '#6366f1',
  accent_color: '#f59e0b',
  phone: '',
  email: '',
  whatsapp: '',
  facebook_url: '',
  instagram_url: '',
  tiktok_url: '',
  website_url: '',
  address: '',
  city: '',
  cancellation_policy: '',
  deposit_percent: 30,
})

onMounted(async () => {
  try {
    const res = await vendorAPI.getProfile()
    vendor.value = res.data
    Object.keys(form.value).forEach(k => {
      if (res.data[k] !== undefined && res.data[k] !== null) {
        form.value[k] = res.data[k]
      }
    })
    // Handle Stripe callback params
    const stripeParam = route.query.stripe
    if (stripeParam === 'connected') {
      stripeSuccess.value = '✅ Cuenta Stripe conectada exitosamente'
      activeTab.value = 'stripe'
      // Reload vendor to get updated stripe status
      const updated = await vendorAPI.getProfile()
      vendor.value = updated.data
    } else if (stripeParam === 'error') {
      stripeError.value = 'Error al conectar con Stripe. Intenta de nuevo.'
      activeTab.value = 'stripe'
    }
  } catch {}
  loadingProfile.value = false
})

async function saveProfile() {
  saving.value = true
  saveError.value = ''
  saveSuccess.value = ''
  try {
    const res = await vendorAPI.updateProfile(form.value)
    vendor.value = res.data
    saveSuccess.value = 'Cambios guardados exitosamente'
    setTimeout(() => saveSuccess.value = '', 3000)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Error al guardar'
  } finally {
    saving.value = false
  }
}

async function connectStripe() {
  stripeLoading.value = true
  stripeError.value = ''
  try {
    const res = await paymentsAPI.connectStripe()
    window.location.href = res.data.url
  } catch (e) {
    stripeError.value = e.response?.data?.detail || 'Error al conectar Stripe. Verifica que STRIPE_CLIENT_ID esté configurado en el servidor.'
  } finally {
    stripeLoading.value = false
  }
}
</script>

<style scoped>
.loading { text-align: center; padding: 60px; color: var(--text2); }
.tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.tab-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text2);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-btn:hover { color: var(--text); border-color: var(--border2); }
.tab-btn.active { background: var(--primary); border-color: var(--primary); color: white; }

.tab-content { margin-bottom: 20px; }
.section-label { font-size: 16px; font-weight: 700; margin-bottom: 20px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field-hint { font-size: 12px; color: var(--text2); margin-top: 4px; }

.slug-wrapper {
  display: flex;
  align-items: center;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.slug-prefix {
  padding: 10px 12px;
  font-size: 13px;
  color: var(--text2);
  background: var(--surface);
  border-right: 1px solid var(--border);
  white-space: nowrap;
}
.slug-in { border: none; border-radius: 0; background: transparent; }
.slug-in:focus { border-color: transparent; }

.preview-img img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 8px;
}
.preview-cover img {
  width: 100%;
  max-height: 120px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 8px;
}
.color-row { display: flex; gap: 8px; align-items: center; }
.color-picker { width: 40px; height: 40px; border: none; background: none; cursor: pointer; border-radius: 6px; }
.color-text { flex: 1; }
.color-preview {
  margin-top: 8px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.range-input {
  width: 100%;
  accent-color: var(--primary);
  height: 6px;
  margin: 12px 0;
}
.deposit-preview {
  background: var(--bg3);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
}

/* Stripe panel */
.stripe-panel { display: flex; flex-direction: column; gap: 24px; }
.fee-breakdown {}
.fee-bar {
  display: flex;
  height: 32px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
}
.fee-yours {
  background: var(--success);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
  min-width: 40px;
}
.fee-platform {
  background: var(--bg3);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: var(--text2);
  min-width: 30px;
}
.fee-example { font-size: 14px; color: var(--text2); }

.stripe-connected {}
.connected-badge { font-size: 16px; font-weight: 700; color: var(--success); margin-bottom: 6px; }
.connected-id { font-size: 12px; color: var(--text2); font-family: monospace; }

.btn-stripe {
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  background: #635bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-stripe:hover:not(:disabled) { background: #5148e8; transform: translateY(-1px); }
.btn-stripe:disabled { opacity: 0.5; cursor: not-allowed; }

.save-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}
.error-msg {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #f87171;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
}
.success-msg {
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.3);
  color: #34d399;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
}

@media (max-width: 768px) {
  .form-grid { grid-template-columns: 1fr; }
}
</style>
