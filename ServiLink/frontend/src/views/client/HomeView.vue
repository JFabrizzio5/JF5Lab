<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content" style="padding:0;display:flex;flex-direction:column;">

      <!-- Filters bar -->
      <div class="filters-bar">
        <div class="filters-left">
          <select v-model="filters.category_id" class="input" style="width:180px;" @change="loadProfessionals">
            <option value="">Todas las categorías</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
          </select>
          <label style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text2);cursor:pointer;">
            <input type="checkbox" v-model="filters.available_only" @change="loadProfessionals" />
            Solo disponibles
          </label>
        </div>
        <div class="filters-right">
          <span class="result-count">{{ professionals.length }} profesionales</span>
          <button class="btn btn-secondary btn-sm" @click="useMyLocation">📍 Mi ubicación</button>
        </div>
      </div>

      <div class="map-content">
        <!-- Map -->
        <div class="map-container">
          <div id="servilink-map" style="width:100%;height:100%;"></div>
        </div>

        <!-- Sidebar list -->
        <div class="prof-list">
          <div v-if="loading" class="loading-state">Cargando...</div>
          <div v-else-if="professionals.length === 0" class="empty-state">No hay profesionales en esta área</div>
          <div
            v-for="p in professionals"
            :key="p.id"
            class="prof-card"
            :class="{ active: selectedProfId === p.id }"
            @click="selectProfessional(p)"
          >
            <img :src="p.avatar_url" class="avatar" :alt="p.name" />
            <div class="prof-info">
              <div class="prof-name">{{ p.name }}</div>
              <div class="prof-cats">{{ p.categories.join(' · ') }}</div>
              <div class="prof-meta">
                <span class="stars">★ {{ p.rating_avg }}</span>
                <span style="color:var(--text2);font-size:12px;">({{ p.total_reviews }})</span>
                <span class="prof-rate">${{ p.hourly_rate }}/hr</span>
              </div>
              <div v-if="p.distance_km !== null" class="prof-distance">📍 {{ p.distance_km }} km</div>
              <span :class="p.is_available ? 'badge badge-accent' : 'badge badge-danger'" style="margin-top:6px;">
                {{ p.is_available ? '✓ Disponible' : '✗ Ocupado' }}
              </span>
              <a :href="`/pro/${p.user_id}`" target="_blank" @click.stop style="display:inline-block;margin-top:6px;font-size:11px;color:var(--text2);text-decoration:none;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text2)'">🌐 Ver página</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="selectedProf" class="modal-overlay" @click.self="selectedProf = null">
      <div class="modal">
        <div class="modal-header">
          <img :src="selectedProf.avatar_url" class="avatar avatar-lg" />
          <div>
            <h2>{{ selectedProf.name }}</h2>
            <div class="stars">★ {{ selectedProf.rating_avg }} · {{ selectedProf.total_reviews }} reseñas · {{ selectedProf.total_jobs }} trabajos</div>
          </div>
          <button @click="selectedProf = null" class="close-btn">✕</button>
        </div>

        <div class="modal-body">
          <p style="color:var(--text2);font-size:14px;margin-bottom:12px;">{{ selectedProf.bio }}</p>
          <div class="modal-tags">
            <span v-for="cat in selectedProf.categories" :key="cat" class="tag">{{ cat }}</span>
            <span class="tag">{{ selectedProf.experience_years }} años exp.</span>
            <span class="tag">${{ selectedProf.hourly_rate }}/hr</span>
          </div>

          <div class="reviews-section">
            <h3>Reseñas recientes</h3>
            <div v-if="loadingReviews" class="loading-state" style="padding:10px;">Cargando...</div>
            <div v-for="r in reviews" :key="r.id" class="review-item">
              <div class="review-header">
                <span class="review-name">{{ r.client_name }}</span>
                <span class="stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
              </div>
              <p class="review-comment">{{ r.comment }}</p>
            </div>
            <p v-if="reviews.length === 0 && !loadingReviews" style="color:var(--text2);font-size:13px;">Sin reseñas aún</p>
          </div>

          <div class="booking-form">
            <h3>Contratar servicio</h3>
            <div class="field">
              <label class="label">Categoría del servicio</label>
              <select v-model="bookingForm.category_id" class="input">
                <option v-for="c in categories.filter(c => selectedProf.categories.includes(c.name))" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
              </select>
            </div>
            <div class="field">
              <label class="label">Descripción del trabajo</label>
              <textarea v-model="bookingForm.description" class="input" rows="3" placeholder="Describe qué necesitas..."></textarea>
            </div>
            <div class="field">
              <label class="label">Tu dirección</label>
              <input v-model="bookingForm.client_address" class="input" placeholder="Calle, colonia, CDMX" />
            </div>
            <div v-if="bookingSuccess" class="alert-success">¡Reserva creada! El profesional recibirá tu solicitud.</div>
            <div v-if="bookingError" class="alert-error">{{ bookingError }}</div>
            <button @click="createBooking" class="btn btn-primary" style="width:100%;justify-content:center;" :disabled="bookingLoading">
              {{ bookingLoading ? 'Enviando...' : `Contratar — $${selectedProf.hourly_rate}/hr` }}
            </button>
            <a :href="`/pro/${selectedProf.user_id}`" target="_blank" style="display:block;text-align:center;padding:10px;border:1px solid var(--border);border-radius:8px;color:var(--text2);font-size:13px;text-decoration:none;transition:all 0.2s;margin-top:4px;" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='var(--border)';this.style.color='var(--text2)'">🌐 Ver página pública completa</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { profApi, categoryApi, reviewApi, bookingApi } from '../../api/index.js'

const professionals = ref([])
const categories = ref([])
const loading = ref(false)
const selectedProf = ref(null)
const selectedProfId = ref(null)
const reviews = ref([])
const loadingReviews = ref(false)
const filters = ref({ category_id: '', available_only: false })
const userLocation = ref({ lat: 19.4326, lng: -99.1332 })

const bookingForm = ref({ category_id: null, description: '', client_address: '' })
const bookingLoading = ref(false)
const bookingSuccess = ref(false)
const bookingError = ref('')

let map = null
let markers = []

onMounted(async () => {
  const [catRes] = await Promise.all([categoryApi.list()])
  categories.value = catRes.data
  await loadProfessionals()
  initMap()
})

onUnmounted(() => { if (map) map.remove() })

async function loadProfessionals() {
  loading.value = true
  try {
    const params = {
      lat: userLocation.value.lat,
      lng: userLocation.value.lng,
      radius_km: 100,
      available_only: filters.value.available_only || undefined,
    }
    if (filters.value.category_id) params.category_id = filters.value.category_id
    const { data } = await profApi.list(params)
    professionals.value = data
    updateMarkers()
  } finally {
    loading.value = false
  }
}

function initMap() {
  if (typeof window === 'undefined') return
  import('leaflet').then((L) => {
    if (map) return
    map = L.default.map('servilink-map').setView([userLocation.value.lat, userLocation.value.lng], 12)
    L.default.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    // User marker
    L.default.circleMarker([userLocation.value.lat, userLocation.value.lng], {
      radius: 10, fillColor: '#6366f1', color: '#fff', weight: 2, fillOpacity: 1
    }).addTo(map).bindPopup('📍 Tu ubicación')

    updateMarkers()
  })
}

function updateMarkers() {
  if (!map) return
  import('leaflet').then((L) => {
    markers.forEach(m => m.remove())
    markers = []
    professionals.value.forEach(p => {
      if (!p.lat || !p.lng) return
      const icon = L.default.divIcon({
        html: `<div style="background:${p.is_available ? '#10b981' : '#ef4444'};width:36px;height:36px;border-radius:50%;border:3px solid white;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 2px 8px rgba(0,0,0,0.3);">🔧</div>`,
        className: '',
        iconSize: [36, 36],
        iconAnchor: [18, 18],
      })
      const marker = L.default.marker([p.lat, p.lng], { icon })
        .addTo(map)
        .bindPopup(`<b>${p.name}</b><br>★ ${p.rating_avg} · $${p.hourly_rate}/hr<br><button onclick="window.__selectProf(${p.id})" style="margin-top:6px;padding:4px 10px;background:#6366f1;color:white;border:none;border-radius:4px;cursor:pointer;">Ver perfil</button>`)
      marker.on('click', () => selectProfessional(p))
      markers.push(marker)
    })
    window.__selectProf = (id) => {
      const p = professionals.value.find(x => x.id === id)
      if (p) selectProfessional(p)
    }
  })
}

async function selectProfessional(p) {
  selectedProfId.value = p.id
  selectedProf.value = p
  bookingSuccess.value = false
  bookingError.value = ''
  bookingForm.value.category_id = null
  loadingReviews.value = true
  try {
    const { data } = await reviewApi.forProfessional(p.user_id)
    reviews.value = data
  } finally {
    loadingReviews.value = false
  }
  if (map) map.setView([p.lat || userLocation.value.lat, p.lng || userLocation.value.lng], 14)
}

async function createBooking() {
  if (!bookingForm.value.category_id) {
    bookingError.value = 'Selecciona una categoría'
    return
  }
  bookingLoading.value = true
  bookingError.value = ''
  try {
    await bookingApi.create({
      professional_id: selectedProf.value.user_id,
      category_id: bookingForm.value.category_id,
      description: bookingForm.value.description,
      client_address: bookingForm.value.client_address,
      client_lat: userLocation.value.lat,
      client_lng: userLocation.value.lng,
    })
    bookingSuccess.value = true
  } catch (e) {
    bookingError.value = e.response?.data?.detail || 'Error al crear reserva'
  } finally {
    bookingLoading.value = false
  }
}

function useMyLocation() {
  navigator.geolocation?.getCurrentPosition(
    (pos) => {
      userLocation.value = { lat: pos.coords.latitude, lng: pos.coords.longitude }
      if (map) map.setView([pos.coords.latitude, pos.coords.longitude], 13)
      loadProfessionals()
    },
    () => alert('No se pudo obtener tu ubicación')
  )
}
</script>

<style scoped>
.filters-bar { display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; background: var(--bg2); border-bottom: 1px solid var(--border); }
.filters-left { display: flex; align-items: center; gap: 12px; }
.filters-right { display: flex; align-items: center; gap: 12px; }
.result-count { font-size: 13px; color: var(--text2); }
.map-content { display: flex; flex: 1; overflow: hidden; }
.map-container { flex: 1; min-height: 500px; }
.prof-list { width: 320px; overflow-y: auto; background: var(--bg2); border-left: 1px solid var(--border); }
.prof-card { display: flex; gap: 12px; padding: 16px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.15s; }
.prof-card:hover, .prof-card.active { background: rgba(99,102,241,0.08); }
.prof-info { flex: 1; }
.prof-name { font-weight: 600; font-size: 14px; }
.prof-cats { font-size: 12px; color: var(--text2); margin: 3px 0; }
.prof-meta { display: flex; align-items: center; gap: 6px; }
.prof-rate { margin-left: auto; font-size: 13px; font-weight: 600; color: var(--accent); }
.prof-distance { font-size: 12px; color: var(--text2); margin-top: 4px; }
.loading-state, .empty-state { padding: 32px; text-align: center; color: var(--text2); font-size: 14px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.modal { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; width: 100%; max-width: 560px; max-height: 85vh; overflow-y: auto; }
.modal-header { display: flex; align-items: center; gap: 16px; padding: 24px; border-bottom: 1px solid var(--border); position: relative; }
.modal-body { padding: 24px; display: flex; flex-direction: column; gap: 20px; }
.modal-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.close-btn { position: absolute; right: 16px; top: 16px; background: none; border: none; color: var(--text2); font-size: 18px; cursor: pointer; }
.reviews-section h3, .booking-form h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
.review-item { background: var(--bg3); border-radius: 8px; padding: 12px; margin-bottom: 8px; }
.review-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.review-name { font-size: 13px; font-weight: 600; }
.review-comment { font-size: 13px; color: var(--text2); }
.field { margin-bottom: 14px; }
.alert-success { background: rgba(16,185,129,0.1); border: 1px solid var(--accent); border-radius: 8px; padding: 10px 14px; font-size: 14px; color: var(--accent); }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 10px 14px; font-size: 14px; color: var(--danger); }
</style>
