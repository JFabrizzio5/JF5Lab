<template>
  <div class="venue-public" :style="cssVars">
    <div v-if="loading" class="loading-screen">
      <div class="spinner"></div>
      <p>Cargando...</p>
    </div>

    <div v-else-if="error" class="error-screen">
      <h2>Venue no encontrado</h2>
      <p>El salón que buscas no existe o no está disponible.</p>
      <router-link to="/" class="btn btn-primary">Ir al inicio</router-link>
    </div>

    <template v-else>
      <!-- Nav -->
      <nav class="venue-nav">
        <div class="venue-nav-brand">
          <img v-if="venue.logo_url" :src="venue.logo_url" :alt="venue.name" class="venue-logo" />
          <span class="venue-nav-name">{{ venue.name }}</span>
        </div>
        <div class="venue-nav-actions">
          <a v-if="venue.whatsapp_number"
            :href="`https://wa.me/${venue.whatsapp_number}?text=${encodeURIComponent(venue.whatsapp_message || '')}`"
            target="_blank"
            class="btn-wa-nav">
            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            WhatsApp
          </a>
          <a href="#contacto" class="btn-cta">Cotizar mi evento</a>
        </div>
      </nav>

      <!-- Hero -->
      <section class="venue-hero" :style="{ backgroundImage: `url(${venue.cover_url})` }">
        <div class="hero-overlay"></div>
        <div class="hero-content">
          <h1>{{ venue.name }}</h1>
          <p class="hero-tagline">{{ venue.tagline }}</p>
          <a href="#contacto" class="hero-cta">Cotizar mi evento →</a>
        </div>
      </section>

      <!-- Description + Amenities -->
      <section class="venue-about">
        <div class="container">
          <div class="about-grid">
            <div class="about-text">
              <h2>Sobre nosotros</h2>
              <p>{{ venue.description }}</p>
            </div>
            <div class="about-amenities">
              <h3>Amenidades</h3>
              <div class="amenities-chips">
                <span v-for="a in amenities" :key="a" class="chip">✓ {{ a }}</span>
              </div>
              <div class="venue-contact-info">
                <div v-if="venue.phone" class="contact-item">📞 {{ venue.phone }}</div>
                <div v-if="venue.email" class="contact-item">✉️ {{ venue.email }}</div>
                <div v-if="venue.address" class="contact-item">📍 {{ venue.address }}, {{ venue.city }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Map -->
      <section v-if="venue.branches?.length" class="venue-map-section">
        <div class="container">
          <h2 class="section-title">Nuestras sucursales</h2>
          <div class="map-layout">
            <div id="venue-map" class="leaflet-map"></div>
            <div class="branches-list">
              <div v-for="b in venue.branches" :key="b.id" class="branch-card">
                <h4>{{ b.name }}</h4>
                <p v-if="b.address">📍 {{ b.address }}</p>
                <p v-if="b.phone">📞 {{ b.phone }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Spaces -->
      <section v-if="venue.spaces?.length" class="venue-spaces">
        <div class="container">
          <h2 class="section-title">Nuestros espacios</h2>
          <div class="spaces-grid">
            <div v-for="space in venue.spaces" :key="space.id" class="space-card">
              <img v-if="spaceImage(space)" :src="spaceImage(space)" :alt="space.name" class="space-img" />
              <div class="space-content">
                <h3>{{ space.name }}</h3>
                <p class="space-desc">{{ space.description }}</p>
                <div class="space-meta">
                  <span>👥 {{ space.capacity }} personas</span>
                  <span v-if="space.price_event > 0">💰 ${{ space.price_event.toLocaleString() }}/evento</span>
                </div>
                <div v-if="spaceAmenities(space).length" class="space-amenities">
                  <span v-for="a in spaceAmenities(space)" :key="a" class="chip-sm">{{ a }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Gallery -->
      <section v-if="gallery.length" class="venue-gallery">
        <div class="container">
          <h2 class="section-title">Galería</h2>
          <div class="gallery-grid">
            <img v-for="(img, i) in gallery" :key="i" :src="img" :alt="`Foto ${i+1}`" class="gallery-img" />
          </div>
        </div>
      </section>

      <!-- Contact Form -->
      <section id="contacto" class="venue-contact">
        <div class="container">
          <h2 class="section-title">Cotiza tu evento</h2>
          <p class="section-sub">Cuéntanos sobre tu evento y te contactaremos en menos de 24 horas</p>

          <div v-if="inquirySuccess" class="inquiry-success">
            <div class="success-icon">✅</div>
            <h3>¡Solicitud enviada!</h3>
            <p>Gracias {{ inquiryForm.name }}, te contactaremos pronto.</p>
          </div>

          <form v-else @submit.prevent="submitInquiry" class="inquiry-form">
            <div class="form-row">
              <div class="form-group">
                <label>Tu nombre *</label>
                <input v-model="inquiryForm.name" type="text" required placeholder="María García" />
              </div>
              <div class="form-group">
                <label>Email *</label>
                <input v-model="inquiryForm.email" type="email" required placeholder="maria@gmail.com" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Teléfono</label>
                <input v-model="inquiryForm.phone" type="tel" placeholder="+52 55 1234 5678" />
              </div>
              <div class="form-group">
                <label>Tipo de evento *</label>
                <select v-model="inquiryForm.event_type">
                  <option value="boda">Boda</option>
                  <option value="xv">XV Años</option>
                  <option value="corporativo">Corporativo</option>
                  <option value="graduacion">Graduación</option>
                  <option value="otro">Otro</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Fecha del evento *</label>
                <input v-model="inquiryForm.start_date" type="date" required />
              </div>
              <div class="form-group">
                <label>Número de invitados</label>
                <input v-model.number="inquiryForm.guests_count" type="number" min="1" placeholder="150" />
              </div>
            </div>
            <div class="form-group">
              <label>Mensaje / Detalles adicionales</label>
              <textarea v-model="inquiryForm.notes" rows="4" placeholder="Cuéntanos más sobre tu evento..."></textarea>
            </div>
            <p v-if="inquiryError" class="error-msg">{{ inquiryError }}</p>
            <button type="submit" class="btn-submit" :disabled="inquiryLoading">
              {{ inquiryLoading ? 'Enviando...' : 'Enviar solicitud' }}
            </button>
          </form>
        </div>
      </section>

      <!-- WhatsApp widget -->
      <WhatsAppWidget :number="venue.whatsapp_number" :message="venue.whatsapp_message" />

      <!-- Footer -->
      <footer class="venue-footer">
        <p>© {{ new Date().getFullYear() }} {{ venue.name }} — Powered by <strong>SalonOS</strong></p>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/index.js'
import WhatsAppWidget from '../../components/WhatsAppWidget.vue'

const route = useRoute()
const venue = ref(null)
const loading = ref(true)
const error = ref(false)
let map = null

const inquiryForm = ref({
  name: '', email: '', phone: '',
  event_type: 'boda', start_date: '', guests_count: 100, notes: ''
})
const inquiryLoading = ref(false)
const inquirySuccess = ref(false)
const inquiryError = ref('')

const cssVars = computed(() => ({
  '--venue-accent': venue.value?.theme_color || '#7c3aed',
  '--venue-accent2': venue.value?.accent_color || '#f59e0b',
}))

const gallery = computed(() => {
  try { return JSON.parse(venue.value?.gallery_json || '[]') } catch { return [] }
})

const amenities = computed(() => {
  try { return JSON.parse(venue.value?.amenities_json || '[]') } catch { return [] }
})

function spaceImage(space) {
  try {
    const imgs = JSON.parse(space.images_json || '[]')
    return imgs[0] || null
  } catch { return null }
}

function spaceAmenities(space) {
  try { return JSON.parse(space.amenities_json || '[]') } catch { return [] }
}

async function loadVenue() {
  try {
    const { data } = await api.get(`/public/venue/${route.params.slug}`)
    venue.value = data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function initMap() {
  if (!venue.value || typeof window === 'undefined') return
  import('leaflet').then((L) => {
    if (map) { map.remove(); map = null }
    const center = [venue.value.lat || 19.4326, venue.value.lng || -99.1332]
    map = L.map('venue-map').setView(center, 12)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    const branches = venue.value.branches || []
    branches.forEach(b => {
      if (b.lat && b.lng) {
        L.marker([b.lat, b.lng])
          .addTo(map)
          .bindPopup(`<strong>${b.name}</strong><br>${b.address || ''}`)
      }
    })

    if (venue.value.lat && venue.value.lng && !branches.length) {
      L.marker([venue.value.lat, venue.value.lng])
        .addTo(map)
        .bindPopup(`<strong>${venue.value.name}</strong>`)
    }
  })
}

async function submitInquiry() {
  inquiryError.value = ''
  inquiryLoading.value = true
  try {
    await api.post(`/public/venue/${route.params.slug}/inquiry`, {
      ...inquiryForm.value,
      start_datetime: inquiryForm.value.start_date + 'T12:00:00',
    })
    inquirySuccess.value = true
  } catch (e) {
    inquiryError.value = e.response?.data?.detail || 'Error al enviar solicitud'
  } finally {
    inquiryLoading.value = false
  }
}

onMounted(async () => {
  await loadVenue()
  if (venue.value?.branches?.length || venue.value?.lat) {
    setTimeout(initMap, 100)
  }
})
</script>

<style scoped>
.venue-public {
  --venue-accent: #7c3aed;
  --venue-accent2: #f59e0b;
  background: #0a0a0f;
  color: #e2e8f0;
  min-height: 100vh;
}

.loading-screen, .error-screen {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.spinner {
  width: 40px; height: 40px;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: var(--venue-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Nav */
.venue-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(10,10,15,0.95);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.venue-nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.venue-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.venue-nav-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}

.venue-nav-actions { display: flex; gap: 0.75rem; align-items: center; }

.btn-wa-nav {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: #25d366;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-wa-nav:hover { background: #22c55e; }

.btn-cta {
  background: var(--venue-accent);
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-cta:hover { opacity: 0.9; }

/* Hero */
.venue-hero {
  height: 80vh;
  min-height: 500px;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(10,10,15,0.9) 0%, rgba(10,10,15,0.5) 50%, rgba(10,10,15,0.3) 100%);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  padding: 2rem;
}

.hero-content h1 {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 900;
  margin-bottom: 1rem;
  text-shadow: 0 2px 20px rgba(0,0,0,0.5);
}

.hero-tagline {
  font-size: 1.2rem;
  color: rgba(255,255,255,0.85);
  margin-bottom: 2rem;
}

.hero-cta {
  display: inline-block;
  background: var(--venue-accent);
  color: white;
  padding: 0.9rem 2.5rem;
  border-radius: 50px;
  font-size: 1.05rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

.hero-cta:hover { transform: translateY(-2px); opacity: 0.9; }

/* About */
.venue-about {
  padding: 5rem 0;
  background: #111118;
}

.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
}

.about-text h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--venue-accent);
}

.about-text p {
  color: #94a3b8;
  line-height: 1.8;
}

.about-amenities h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.amenities-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.chip {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 0.35rem 0.8rem;
  border-radius: 20px;
  font-size: 0.82rem;
  color: #94a3b8;
}

.venue-contact-info { margin-top: 1.5rem; }

.contact-item {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

/* Sections */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--venue-accent);
}

.section-sub {
  color: #64748b;
  margin-bottom: 2rem;
}

/* Map */
.venue-map-section {
  padding: 5rem 0;
}

.map-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  height: 400px;
}

.leaflet-map {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
}

.branches-list {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.branch-card {
  background: #1a1a2e;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 1.25rem;
}

.branch-card h4 {
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.branch-card p {
  font-size: 0.82rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

/* Spaces */
.venue-spaces {
  padding: 5rem 0;
  background: #111118;
}

.spaces-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.space-card {
  background: #1a1a2e;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;
}

.space-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.space-content { padding: 1.5rem; }

.space-content h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.space-desc {
  font-size: 0.88rem;
  color: #64748b;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.space-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--venue-accent2);
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.space-amenities { display: flex; flex-wrap: wrap; gap: 0.4rem; }

.chip-sm {
  background: rgba(255,255,255,0.05);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  color: #64748b;
}

/* Gallery */
.venue-gallery { padding: 5rem 0; }

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.gallery-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.2s;
}

.gallery-img:hover { transform: scale(1.02); }

/* Contact */
.venue-contact {
  padding: 5rem 0;
  background: #111118;
}

.inquiry-form {
  background: #1a1a2e;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 2.5rem;
  max-width: 700px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.error-msg {
  color: #ef4444;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.btn-submit {
  background: var(--venue-accent);
  color: white;
  border: none;
  padding: 0.85rem 2rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}

.btn-submit:hover { opacity: 0.9; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.inquiry-success {
  text-align: center;
  padding: 3rem;
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 20px;
  max-width: 400px;
}

.success-icon { font-size: 3rem; margin-bottom: 1rem; }
.inquiry-success h3 { font-size: 1.25rem; margin-bottom: 0.5rem; }
.inquiry-success p { color: #64748b; }

/* Footer */
.venue-footer {
  padding: 2rem;
  text-align: center;
  border-top: 1px solid rgba(255,255,255,0.06);
  color: #64748b;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .about-grid { grid-template-columns: 1fr; gap: 2rem; }
  .map-layout { grid-template-columns: 1fr; height: auto; }
  .leaflet-map { height: 300px; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
