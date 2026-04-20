<template>
  <div class="pro-public">
    <!-- Nav minimal -->
    <nav class="pub-nav">
      <router-link to="/" class="pub-logo">⚡ ServiLink</router-link>
      <div class="pub-nav-right">
        <router-link v-if="!isLoggedIn" to="/login" class="pub-btn-ghost">Iniciar sesión</router-link>
        <router-link v-if="!isLoggedIn" to="/register" class="pub-btn-cta">Registrarse</router-link>
        <router-link v-if="isLoggedIn && isClient" to="/marketplace" class="pub-btn-ghost">← Volver al marketplace</router-link>
      </div>
    </nav>

    <!-- Loading -->
    <div v-if="loading" class="pub-loading">
      <div class="loading-spinner"></div>
      <p>Cargando perfil...</p>
    </div>

    <!-- Not found -->
    <div v-else-if="!prof" class="pub-notfound">
      <div class="notfound-icon">😕</div>
      <h1>Profesional no encontrado</h1>
      <p>Este perfil no existe o fue desactivado.</p>
      <router-link to="/marketplace" class="pub-btn-cta">Ver marketplace →</router-link>
    </div>

    <!-- Profile -->
    <div v-else class="pub-profile" :style="`--pro-accent: ${prof.theme_color || '#6366f1'}`">

      <!-- Hero -->
      <div class="pub-hero" :style="prof.cover_url ? `background-image: url('${prof.cover_url}'); background-size: cover; background-position: center;` : ''">
        <div class="pub-hero-bg" :style="prof.cover_url ? 'background: linear-gradient(to bottom, rgba(10,10,15,0.5) 0%, rgba(10,10,15,0.85) 100%)' : ''"></div>
        <div class="pub-hero-content">
          <div class="pub-avatar-wrap">
            <img :src="prof.avatar_url" class="pub-avatar" :alt="prof.name" />
            <div class="pub-avail-dot" :class="prof.is_available ? 'online' : 'offline'"></div>
          </div>
          <div class="pub-hero-info">
            <div class="pub-hero-top">
              <h1 class="pub-name">{{ prof.name }}</h1>
              <p v-if="prof.tagline" class="pub-tagline">{{ prof.tagline }}</p>
              <span :class="['pub-status', prof.is_available ? 'avail' : 'busy']">
                {{ prof.is_available ? '● Disponible ahora' : '○ No disponible' }}
              </span>
              <span v-if="prof.subscription_plan !== 'free'" :class="`plan-badge plan-${prof.subscription_plan}`">
                {{ { basic: '🔵 Básico', pro: '🟢 Pro', premium: '⭐ Premium' }[prof.subscription_plan] }}
              </span>
            </div>
            <div class="pub-rating">
              <span class="stars">{{ '★'.repeat(Math.round(prof.rating_avg)) }}{{ '☆'.repeat(5 - Math.round(prof.rating_avg)) }}</span>
              <span class="rating-num">{{ prof.rating_avg }}</span>
              <span class="rating-cnt">{{ prof.total_reviews }} reseñas</span>
              <span class="sep">·</span>
              <span class="jobs-cnt">{{ prof.total_jobs }} servicios completados</span>
            </div>
            <div class="pub-cats">
              <span v-for="cat in prof.categories" :key="cat" class="pub-cat-tag">{{ cat }}</span>
              <span class="pub-cat-tag exp">{{ prof.experience_years }} años exp.</span>
            </div>
            <div class="pub-price">${{ prof.hourly_rate }}<span>/hora</span></div>
          </div>

          <!-- CTA -->
          <div class="pub-cta-box">
            <div class="pub-cta-price">${{ prof.hourly_rate }}/hr</div>
            <button @click="startChat" class="pub-chat-btn" :disabled="!prof.is_available && false">
              💬 Chatear y reservar
            </button>
            <button @click="copyLink" class="pub-share-btn">
              {{ copied ? '✓ Link copiado' : '🔗 Compartir perfil' }}
            </button>
            <div v-if="prof.address" class="pub-location">📍 {{ prof.address }}</div>
          </div>
        </div>
      </div>

      <!-- Body -->
      <div class="pub-body">
        <div class="pub-main">

          <!-- Bio -->
          <section class="pub-section">
            <h2>Sobre mí</h2>
            <p class="pub-bio">{{ prof.bio || 'Este profesional aún no ha agregado una descripción.' }}</p>
          </section>

          <!-- Services: custom JSON or fallback to categories -->
          <section class="pub-section">
            <h2>Servicios que ofrezco</h2>
            <div v-if="customServices.length" class="pub-services-grid custom">
              <div v-for="(svc, i) in customServices" :key="i" class="pub-service-card custom-card">
                <div class="pub-service-name">{{ svc.title }}</div>
                <div class="pub-service-desc">{{ svc.description }}</div>
                <div class="pub-service-price" v-if="svc.price">${{ svc.price }}</div>
              </div>
            </div>
            <div v-else class="pub-services-grid">
              <div v-for="cat in prof.categories" :key="cat" class="pub-service-card">
                <div class="pub-service-icon">{{ catIcon(cat) }}</div>
                <div class="pub-service-name">{{ cat }}</div>
                <div class="pub-service-price">${{ prof.hourly_rate }}/hr</div>
              </div>
            </div>
          </section>

          <!-- Stats -->
          <section class="pub-section">
            <h2>Estadísticas</h2>
            <div class="pub-stats-row">
              <div class="pub-stat">
                <div class="pub-stat-val" style="color:#f59e0b;">★ {{ prof.rating_avg }}</div>
                <div class="pub-stat-lbl">Rating promedio</div>
              </div>
              <div class="pub-stat">
                <div class="pub-stat-val" style="color:#6366f1;">{{ prof.total_reviews }}</div>
                <div class="pub-stat-lbl">Reseñas</div>
              </div>
              <div class="pub-stat">
                <div class="pub-stat-val" style="color:#10b981;">{{ prof.total_jobs }}</div>
                <div class="pub-stat-lbl">Trabajos</div>
              </div>
              <div class="pub-stat">
                <div class="pub-stat-val">{{ prof.experience_years }}</div>
                <div class="pub-stat-lbl">Años exp.</div>
              </div>
            </div>
          </section>

          <!-- Reviews -->
          <section class="pub-section">
            <h2>Reseñas de clientes</h2>
            <div v-if="prof.reviews.length === 0" class="pub-empty">Sin reseñas aún.</div>
            <div v-for="r in prof.reviews" :key="r.id" class="pub-review">
              <div class="pub-review-top">
                <img :src="r.client_avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${r.client_name}`" class="pub-review-avatar" />
                <div>
                  <div class="pub-review-name">{{ r.client_name }}</div>
                  <div class="pub-review-date">{{ formatDate(r.created_at) }}</div>
                </div>
                <div class="pub-review-stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</div>
              </div>
              <p class="pub-review-text">{{ r.comment }}</p>
            </div>
          </section>
        </div>

        <!-- Sidebar sticky CTA -->
        <aside class="pub-sidebar">
          <div class="pub-sidebar-card">
            <img :src="prof.avatar_url" class="pub-sidebar-avatar" />
            <div class="pub-sidebar-name">{{ prof.name }}</div>
            <div class="pub-sidebar-rating">★ {{ prof.rating_avg }} · {{ prof.total_reviews }} reseñas</div>
            <div class="pub-sidebar-price">${{ prof.hourly_rate }}<span>/hr</span></div>
            <button @click="startChat" class="pub-chat-btn-full">
              💬 Chatear y reservar
            </button>
            <button @click="copyLink" class="pub-share-btn-sm">
              {{ copied ? '✓ Copiado' : '🔗 Compartir' }}
            </button>
            <div class="pub-sidebar-avail" :class="prof.is_available ? 'avail' : 'busy'">
              {{ prof.is_available ? '● Disponible ahora' : '○ No disponible' }}
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- Auth Modal (if not logged in) -->
    <div v-if="showAuthModal" class="auth-modal-overlay" @click.self="showAuthModal = false">
      <div class="auth-modal">
        <h2>Inicia sesión para chatear</h2>
        <p>Crea una cuenta gratis o inicia sesión para contactar a <strong>{{ prof?.name }}</strong>.</p>
        <div class="auth-modal-btns">
          <router-link :to="`/login?next=/pro/${userId}`" class="pub-chat-btn-full" style="display:block;text-align:center;">Iniciar sesión</router-link>
          <router-link :to="`/register?next=/pro/${userId}`" class="pub-share-btn" style="display:block;text-align:center;margin-top:8px;">Crear cuenta</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { publicApi, chatApi } from '../api/index.js'

const route = useRoute()
const router = useRouter()
const userId = computed(() => Number(route.params.id))
const prof = ref(null)
const loading = ref(true)
const copied = ref(false)
const showAuthModal = ref(false)

const customServices = computed(() => {
  if (!prof.value?.services_json) return []
  try { return JSON.parse(prof.value.services_json) } catch { return [] }
})

const isLoggedIn = computed(() => !!localStorage.getItem('servilink_token'))
const currentUser = computed(() => JSON.parse(localStorage.getItem('servilink_user') || 'null'))
const isClient = computed(() => currentUser.value?.role === 'client')

const catIcons = {
  'Plomería': '🔧', 'Electricidad': '⚡', 'Limpieza': '🧹', 'Jardinería': '🌿',
  'Pintura': '🎨', 'Carpintería': '🪚', 'Cerrajería': '🔑', 'Mudanzas': '📦',
  'Aire Acondicionado': '❄️', 'Tecnología': '💻',
}
function catIcon(name) { return catIcons[name] || '🔧' }
function formatDate(dt) {
  return new Date(dt).toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' })
}

onMounted(async () => {
  try {
    const { data } = await publicApi.getProfile(userId.value)
    prof.value = data
  } catch {
    prof.value = null
  } finally {
    loading.value = false
  }
})

async function startChat() {
  if (!isLoggedIn.value) {
    showAuthModal.value = true
    return
  }
  if (!isClient.value) {
    alert('Solo los clientes pueden iniciar chats con profesionales.')
    return
  }
  try {
    const { data } = await chatApi.getOrCreateRoom(userId.value)
    router.push(`/chat/${data.room_id}`)
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al iniciar chat')
  }
}

function copyLink() {
  navigator.clipboard.writeText(window.location.href)
  copied.value = true
  setTimeout(() => copied.value = false, 2000)
}
</script>

<style scoped>
.pro-public { min-height: 100vh; background: #0a0a0f; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; }

/* Nav */
.pub-nav { display: flex; align-items: center; justify-content: space-between; padding: 16px 32px; border-bottom: 1px solid rgba(255,255,255,0.06); background: rgba(10,10,15,0.8); backdrop-filter: blur(16px); position: sticky; top: 0; z-index: 50; }
.pub-logo { font-size: 20px; font-weight: 900; color: #6366f1; text-decoration: none; }
.pub-nav-right { display: flex; gap: 12px; align-items: center; }
.pub-btn-ghost { color: #64748b; text-decoration: none; font-size: 14px; padding: 8px 16px; font-weight: 500; transition: color 0.2s; }
.pub-btn-ghost:hover { color: #e2e8f0; }
.pub-btn-cta { background: #6366f1; color: white; text-decoration: none; font-size: 14px; font-weight: 700; padding: 9px 20px; border-radius: 8px; transition: all 0.2s; }
.pub-btn-cta:hover { background: #4f46e5; }

/* Loading / notfound */
.pub-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 16px; color: #64748b; }
.loading-spinner { width: 40px; height: 40px; border: 3px solid rgba(99,102,241,0.2); border-top-color: #6366f1; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.pub-notfound { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 16px; text-align: center; }
.notfound-icon { font-size: 64px; }
.pub-notfound h1 { font-size: 28px; font-weight: 700; }
.pub-notfound p { color: #64748b; }

/* Hero */
.pub-hero { position: relative; padding: 60px 32px 40px; overflow: hidden; }
.pub-hero-bg { position: absolute; inset: 0; background: linear-gradient(135deg, rgba(99,102,241,0.06) 0%, rgba(16,185,129,0.03) 100%); border-bottom: 1px solid rgba(255,255,255,0.04); }
.pub-hero-content { position: relative; max-width: 1200px; margin: 0 auto; display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap; }
.pub-avatar-wrap { position: relative; flex-shrink: 0; }
.pub-avatar { width: 120px; height: 120px; border-radius: 50%; border: 4px solid rgba(99,102,241,0.3); }
.pub-avail-dot { position: absolute; bottom: 6px; right: 6px; width: 18px; height: 18px; border-radius: 50%; border: 3px solid #0a0a0f; }
.pub-avail-dot.online { background: #10b981; }
.pub-avail-dot.offline { background: #ef4444; }
.pub-hero-info { flex: 1; min-width: 280px; }
.pub-hero-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 10px; }
.pub-name { font-size: 32px; font-weight: 800; letter-spacing: -0.02em; }
.pub-status { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 999px; }
.pub-status.avail { background: rgba(16,185,129,0.15); color: #10b981; }
.pub-status.busy { background: rgba(239,68,68,0.15); color: #ef4444; }
.plan-badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.plan-badge.plan-pro { background: rgba(16,185,129,0.15); color: #10b981; }
.plan-badge.plan-premium { background: rgba(245,158,11,0.15); color: #f59e0b; }
.plan-badge.plan-basic { background: rgba(99,102,241,0.15); color: #6366f1; }
.pub-rating { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 14px; }
.stars { color: #f59e0b; }
.rating-num { font-weight: 700; }
.rating-cnt, .jobs-cnt { color: #64748b; }
.sep { color: #374151; }
.pub-cats { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.pub-cat-tag { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 4px 12px; font-size: 13px; color: #94a3b8; }
.pub-cat-tag.exp { color: #6366f1; border-color: rgba(99,102,241,0.3); }
.pub-price { font-size: 28px; font-weight: 800; color: #10b981; }
.pub-price span { font-size: 16px; font-weight: 400; color: #64748b; }

/* CTA box */
.pub-cta-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 10px; min-width: 240px; }
.pub-cta-price { font-size: 22px; font-weight: 800; color: #10b981; text-align: center; }
.pub-chat-btn { padding: 14px; background: var(--pro-accent, #6366f1); color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.pub-chat-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(99,102,241,0.4); }
.pub-share-btn { padding: 10px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #94a3b8; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.pub-share-btn:hover { border-color: rgba(99,102,241,0.3); color: #e2e8f0; }
.pub-location { font-size: 12px; color: #64748b; text-align: center; }

/* Body */
.pub-body { max-width: 1200px; margin: 0 auto; padding: 40px 32px; display: grid; grid-template-columns: 1fr 300px; gap: 40px; align-items: start; }
.pub-main { display: flex; flex-direction: column; gap: 40px; }
.pub-section h2 { font-size: 20px; font-weight: 700; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 12px; }
.pub-tagline { font-size: 16px; color: #94a3b8; margin-top: 4px; font-style: italic; }
.pub-bio { font-size: 15px; color: #94a3b8; line-height: 1.7; }
.pub-services-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
.pub-services-grid.custom { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
.pub-service-desc { font-size: 12px; color: #64748b; margin: 6px 0; line-height: 1.5; }
.pub-service-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 16px; text-align: center; transition: border-color 0.2s; }
.pub-service-card:hover { border-color: rgba(99,102,241,0.25); }
.pub-service-icon { font-size: 28px; margin-bottom: 8px; }
.pub-service-name { font-size: 13px; font-weight: 600; margin-bottom: 6px; }
.pub-service-price { font-size: 12px; color: #10b981; font-weight: 600; }
.pub-stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.pub-stat { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; text-align: center; }
.pub-stat-val { font-size: 28px; font-weight: 800; margin-bottom: 6px; }
.pub-stat-lbl { font-size: 12px; color: #64748b; }
.pub-review { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.pub-review-top { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.pub-review-avatar { width: 36px; height: 36px; border-radius: 50%; }
.pub-review-name { font-size: 14px; font-weight: 600; }
.pub-review-date { font-size: 12px; color: #64748b; }
.pub-review-stars { margin-left: auto; color: #f59e0b; font-size: 14px; }
.pub-review-text { font-size: 14px; color: #94a3b8; line-height: 1.6; }
.pub-empty { color: #64748b; font-size: 14px; }

/* Sidebar */
.pub-sidebar { position: sticky; top: 80px; }
.pub-sidebar-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 12px; align-items: center; }
.pub-sidebar-avatar { width: 72px; height: 72px; border-radius: 50%; }
.pub-sidebar-name { font-size: 18px; font-weight: 700; }
.pub-sidebar-rating { font-size: 13px; color: #f59e0b; }
.pub-sidebar-price { font-size: 28px; font-weight: 800; color: #10b981; }
.pub-sidebar-price span { font-size: 14px; font-weight: 400; color: #64748b; }
.pub-chat-btn-full { width: 100%; padding: 14px; background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border: none; border-radius: 10px; font-size: 14px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.pub-chat-btn-full:hover { box-shadow: 0 6px 20px rgba(99,102,241,0.4); }
.pub-share-btn-sm { width: 100%; padding: 10px; background: transparent; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #64748b; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.pub-share-btn-sm:hover { border-color: rgba(99,102,241,0.3); color: #e2e8f0; }
.pub-sidebar-avail { font-size: 12px; font-weight: 600; }
.pub-sidebar-avail.avail { color: #10b981; }
.pub-sidebar-avail.busy { color: #ef4444; }

/* Auth modal */
.auth-modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 200; }
.auth-modal { background: #111118; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px; max-width: 400px; width: 100%; text-align: center; }
.auth-modal h2 { font-size: 22px; font-weight: 700; margin-bottom: 10px; }
.auth-modal p { color: #64748b; font-size: 14px; margin-bottom: 24px; line-height: 1.6; }
</style>
