<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content" style="padding:0;display:flex;flex-direction:column;min-height:100vh;">

      <!-- Header bar -->
      <div class="mkt-header">
        <div class="mkt-header-left">
          <h1 class="mkt-title">Marketplace de Servicios</h1>
          <p class="mkt-sub">{{ filtered.length }} profesionales disponibles</p>
        </div>
        <div class="view-toggle">
          <button @click="view = 'grid'" :class="['toggle-btn', view === 'grid' && 'active']">⊞ Grid</button>
          <button @click="view = 'map'" :class="['toggle-btn', view === 'map' && 'active']">🗺️ Mapa</button>
        </div>
      </div>

      <div class="mkt-body">
        <!-- Filters sidebar -->
        <aside class="filters-panel">
          <div class="filter-group">
            <div class="filter-label">🔍 Buscar</div>
            <input v-model="search" class="input" placeholder="Nombre o descripción..." @input="applyFilters" />
          </div>

          <div class="filter-group">
            <div class="filter-label">🏷️ Categoría</div>
            <div class="cat-filters">
              <button
                v-for="c in [{id:'', name:'Todas', icon:'✨'}, ...categories]"
                :key="c.id"
                @click="selectedCat = c.id; applyFilters()"
                :class="['cat-btn', selectedCat === c.id && 'active']"
              >
                {{ c.icon }} {{ c.name }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <div class="filter-label">⭐ Rating mínimo</div>
            <div class="rating-btns">
              <button v-for="r in [0,3,4,4.5]" :key="r" @click="minRating = r; applyFilters()" :class="['rating-btn', minRating === r && 'active']">
                {{ r === 0 ? 'Todos' : `★ ${r}+` }}
              </button>
            </div>
          </div>

          <div class="filter-group">
            <div class="filter-label">💰 Precio máximo /hr</div>
            <input v-model.number="maxPrice" type="range" min="0" max="2000" step="50" class="range-input" @input="applyFilters" />
            <div class="range-labels">
              <span>$0</span>
              <span class="range-val">${{ maxPrice === 2000 ? 'Sin límite' : maxPrice }}</span>
            </div>
          </div>

          <div class="filter-group">
            <label class="toggle-label">
              <input type="checkbox" v-model="availableOnly" @change="applyFilters" />
              <span class="toggle-check"></span>
              Solo disponibles ahora
            </label>
          </div>

          <div class="filter-group">
            <div class="filter-label">📍 Radio de búsqueda</div>
            <div class="rating-btns">
              <button v-for="r in [5,10,25,50]" :key="r" @click="radius = r; applyFilters()" :class="['rating-btn', radius === r && 'active']">
                {{ r }}km
              </button>
            </div>
          </div>

          <button @click="clearFilters" class="btn-clear">✕ Limpiar filtros</button>
        </aside>

        <!-- Content -->
        <div class="mkt-content">

          <!-- Grid view -->
          <div v-if="view === 'grid'" class="prof-grid">
            <div v-if="loading" v-for="n in 6" :key="n" class="prof-card skeleton">
              <div class="sk-avatar"></div>
              <div class="sk-line long"></div>
              <div class="sk-line short"></div>
              <div class="sk-line mid"></div>
            </div>

            <div v-else-if="filtered.length === 0" class="empty-grid">
              <div class="empty-icon">🔍</div>
              <h3>Sin resultados</h3>
              <p>Prueba cambiando los filtros</p>
              <button @click="clearFilters" class="btn btn-secondary btn-sm" style="margin-top:12px;">Limpiar filtros</button>
            </div>

            <div
              v-else
              v-for="p in filtered"
              :key="p.id"
              class="prof-card"
              @click="openProfessional(p)"
            >
              <div class="prof-card-top">
                <img :src="p.avatar_url" class="prof-avatar" :alt="p.name" />
                <div class="prof-status-badge" :class="p.is_available ? 'available' : 'busy'">
                  {{ p.is_available ? '● Disponible' : '○ Ocupado' }}
                </div>
              </div>

              <div class="prof-card-body">
                <h3 class="prof-name">{{ p.name }}</h3>

                <div class="prof-rating">
                  <span class="stars">{{ '★'.repeat(Math.round(p.rating_avg)) }}{{ '☆'.repeat(5 - Math.round(p.rating_avg)) }}</span>
                  <span class="rating-val">{{ p.rating_avg }}</span>
                  <span class="rating-count">({{ p.total_reviews }})</span>
                </div>

                <div class="prof-cats">
                  <span v-for="cat in p.categories.slice(0, 2)" :key="cat" class="cat-tag">{{ cat }}</span>
                  <span v-if="p.categories.length > 2" class="cat-tag more">+{{ p.categories.length - 2 }}</span>
                </div>

                <p class="prof-bio">{{ p.bio?.slice(0, 80) || 'Profesional verificado' }}{{ p.bio?.length > 80 ? '...' : '' }}</p>

                <div class="prof-footer">
                  <div class="prof-price">${{ p.hourly_rate }}<span>/hr</span></div>
                  <div class="prof-meta-right">
                    <span v-if="p.distance_km !== null" class="prof-dist">📍 {{ p.distance_km }}km</span>
                    <span class="prof-jobs">{{ p.total_jobs }} trabajos</span>
                  </div>
                </div>

                <div class="prof-plan-badge" v-if="p.subscription_plan !== 'free'">
                  <span :class="`plan-${p.subscription_plan}`">{{ planIcon(p.subscription_plan) }} {{ p.subscription_plan }}</span>
                </div>
              </div>

              <div class="prof-card-actions">
                <button class="prof-hire-btn" @click.stop="openProfessional(p)">Contratar →</button>
                <a :href="`/pro/${p.user_id}`" target="_blank" class="prof-page-btn" @click.stop>🌐 Ver página</a>
              </div>
            </div>
          </div>

          <!-- Map view -->
          <div v-else class="map-view">
            <div id="marketplace-map" style="width:100%;height:100%;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Professional Modal -->
    <div v-if="selectedProf" class="modal-overlay" @click.self="selectedProf = null">
      <div class="prof-modal">
        <button @click="selectedProf = null" class="modal-close">✕</button>

        <div class="modal-hero">
          <img :src="selectedProf.avatar_url" class="modal-avatar" />
          <div class="modal-hero-info">
            <div class="modal-header-top">
              <h2>{{ selectedProf.name }}</h2>
              <span :class="['avail-badge', selectedProf.is_available ? 'available' : 'busy']">
                {{ selectedProf.is_available ? '● Disponible' : '○ Ocupado' }}
              </span>
            </div>
            <div class="modal-rating">
              <span class="stars">★ {{ selectedProf.rating_avg }}</span>
              <span style="color:var(--text2);font-size:13px;">{{ selectedProf.total_reviews }} reseñas · {{ selectedProf.total_jobs }} servicios</span>
            </div>
            <div class="modal-cats">
              <span v-for="cat in selectedProf.categories" :key="cat" class="cat-tag">{{ cat }}</span>
              <span class="cat-tag exp">{{ selectedProf.experience_years }} años exp.</span>
            </div>
            <div class="modal-price">${{ selectedProf.hourly_rate }}<span>/hr</span></div>
          </div>
        </div>

        <div class="modal-body-cols">
          <div class="modal-col-left">
            <div class="modal-section">
              <h3>Sobre el profesional</h3>
              <p>{{ selectedProf.bio || 'Sin descripción disponible.' }}</p>
            </div>
            <div class="modal-section">
              <h3>Ubicación</h3>
              <p>{{ selectedProf.address || 'CDMX' }}</p>
              <p v-if="selectedProf.distance_km !== null" style="color:var(--accent);font-size:13px;margin-top:4px;">📍 A {{ selectedProf.distance_km }} km de ti</p>
            </div>
            <div class="modal-section">
              <h3>Reseñas ({{ reviews.length }})</h3>
              <div v-if="loadingReviews" style="color:var(--text2);font-size:13px;">Cargando...</div>
              <div v-for="r in reviews.slice(0, 3)" :key="r.id" class="review-card">
                <div class="review-top">
                  <span class="review-author">{{ r.client_name }}</span>
                  <span class="stars" style="font-size:12px;">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
                </div>
                <p class="review-text">{{ r.comment }}</p>
              </div>
              <p v-if="reviews.length === 0 && !loadingReviews" style="color:var(--text2);font-size:13px;">Sin reseñas aún</p>
            </div>
          </div>

          <div class="modal-col-right">
            <div class="booking-form-card">
              <h3>Solicitar servicio</h3>
              <div class="field">
                <label class="label">Categoría</label>
                <select v-model="bookForm.category_id" class="input">
                  <option v-for="c in matchedCats" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
                </select>
              </div>
              <div class="field">
                <label class="label">¿Qué necesitas?</label>
                <textarea v-model="bookForm.description" class="input" rows="3" placeholder="Describe el trabajo..."></textarea>
              </div>
              <div class="field">
                <label class="label">Tu dirección</label>
                <input v-model="bookForm.client_address" class="input" placeholder="Calle, colonia, ciudad" />
              </div>
              <div v-if="bookSuccess" class="alert-success">✅ ¡Solicitud enviada! El profesional te responderá pronto.</div>
              <div v-if="bookError" class="alert-error">{{ bookError }}</div>
              <button @click="submitBooking" class="btn-book" :disabled="bookLoading">
                {{ bookLoading ? 'Enviando...' : `Contratar · $${selectedProf.hourly_rate}/hr` }}
              </button>
              <a :href="`/pro/${selectedProf.user_id}`" target="_blank" class="btn-view-page">🌐 Ver página pública completa</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { profApi, categoryApi, reviewApi, bookingApi } from '../../api/index.js'

const professionals = ref([])
const categories = ref([])
const filtered = ref([])
const loading = ref(true)
const view = ref('grid')

// Filters
const search = ref('')
const selectedCat = ref('')
const minRating = ref(0)
const maxPrice = ref(2000)
const availableOnly = ref(false)
const radius = ref(50)
const userLocation = ref({ lat: 19.4326, lng: -99.1332 })

// Modal
const selectedProf = ref(null)
const reviews = ref([])
const loadingReviews = ref(false)
const bookForm = ref({ category_id: null, description: '', client_address: '' })
const bookLoading = ref(false)
const bookSuccess = ref(false)
const bookError = ref('')

// Map
let map = null
let markers = []

const matchedCats = computed(() => {
  if (!selectedProf.value) return []
  return categories.value.filter(c => selectedProf.value.categories.includes(c.name))
})

onMounted(async () => {
  navigator.geolocation?.getCurrentPosition(
    (pos) => { userLocation.value = { lat: pos.coords.latitude, lng: pos.coords.longitude }; loadProfessionals() },
    () => loadProfessionals()
  )
  const { data } = await categoryApi.list()
  categories.value = data
})

onUnmounted(() => { if (map) map.remove() })

async function loadProfessionals() {
  loading.value = true
  try {
    const { data } = await profApi.list({
      lat: userLocation.value.lat,
      lng: userLocation.value.lng,
      radius_km: 200,
    })
    professionals.value = data
    applyFilters()
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  let result = [...professionals.value]

  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    result = result.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.bio?.toLowerCase().includes(q) ||
      p.categories.some(c => c.toLowerCase().includes(q))
    )
  }

  if (selectedCat.value) {
    const catName = categories.value.find(c => c.id == selectedCat.value)?.name
    if (catName) result = result.filter(p => p.categories.includes(catName))
  }

  if (minRating.value > 0) {
    result = result.filter(p => p.rating_avg >= minRating.value)
  }

  if (maxPrice.value < 2000) {
    result = result.filter(p => p.hourly_rate <= maxPrice.value)
  }

  if (availableOnly.value) {
    result = result.filter(p => p.is_available)
  }

  if (radius.value < 50 && userLocation.value) {
    result = result.filter(p => p.distance_km === null || p.distance_km <= radius.value)
  }

  filtered.value = result
  if (view.value === 'map') updateMapMarkers()
}

function clearFilters() {
  search.value = ''
  selectedCat.value = ''
  minRating.value = 0
  maxPrice.value = 2000
  availableOnly.value = false
  radius.value = 50
  applyFilters()
}

function planIcon(plan) {
  return { basic: '🔵', pro: '🟢', premium: '⭐' }[plan] || ''
}

async function openProfessional(p) {
  selectedProf.value = p
  bookSuccess.value = false
  bookError.value = ''
  bookForm.value = { category_id: null, description: '', client_address: '' }
  loadingReviews.value = true
  reviews.value = []
  try {
    const { data } = await reviewApi.forProfessional(p.user_id)
    reviews.value = data
  } finally {
    loadingReviews.value = false
  }
  // Pre-select category
  const mc = categories.value.filter(c => p.categories.includes(c.name))
  if (mc.length) bookForm.value.category_id = mc[0].id
}

async function submitBooking() {
  if (!bookForm.value.category_id) { bookError.value = 'Selecciona una categoría'; return }
  bookLoading.value = true
  bookError.value = ''
  try {
    await bookingApi.create({
      professional_id: selectedProf.value.user_id,
      category_id: bookForm.value.category_id,
      description: bookForm.value.description,
      client_address: bookForm.value.client_address,
      client_lat: userLocation.value.lat,
      client_lng: userLocation.value.lng,
    })
    bookSuccess.value = true
  } catch (e) {
    bookError.value = e.response?.data?.detail || 'Error al crear solicitud'
  } finally {
    bookLoading.value = false
  }
}

// Map
watch(view, (v) => { if (v === 'map') setTimeout(initMap, 100) })

function initMap() {
  if (map) { updateMapMarkers(); return }
  import('leaflet').then((L) => {
    map = L.default.map('marketplace-map').setView([userLocation.value.lat, userLocation.value.lng], 12)
    L.default.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map)
    L.default.circleMarker([userLocation.value.lat, userLocation.value.lng], { radius: 10, fillColor: '#6366f1', color: '#fff', weight: 2, fillOpacity: 1 }).addTo(map).bindPopup('📍 Tu ubicación')
    updateMapMarkers()
  })
}

function updateMapMarkers() {
  if (!map) return
  import('leaflet').then((L) => {
    markers.forEach(m => m.remove())
    markers = []
    filtered.value.forEach(p => {
      if (!p.lat || !p.lng) return
      const icon = L.default.divIcon({
        html: `<div style="background:${p.is_available ? '#10b981' : '#ef4444'};width:38px;height:38px;border-radius:50%;border:3px solid white;display:flex;align-items:center;justify-content:center;font-size:17px;box-shadow:0 2px 10px rgba(0,0,0,0.4);">🔧</div>`,
        className: '', iconSize: [38, 38], iconAnchor: [19, 19],
      })
      const m = L.default.marker([p.lat, p.lng], { icon }).addTo(map)
      m.on('click', () => openProfessional(p))
      m.bindPopup(`<b>${p.name}</b><br>★ ${p.rating_avg} · $${p.hourly_rate}/hr`)
      markers.push(m)
    })
  })
}
</script>

<style scoped>
.mkt-header { display: flex; align-items: center; justify-content: space-between; padding: 20px 28px; background: var(--bg2); border-bottom: 1px solid var(--border); }
.mkt-title { font-size: 20px; font-weight: 700; }
.mkt-sub { font-size: 13px; color: var(--text2); margin-top: 3px; }
.view-toggle { display: flex; background: var(--bg3); border-radius: 8px; padding: 3px; gap: 2px; }
.toggle-btn { padding: 7px 14px; border-radius: 6px; border: none; background: transparent; color: var(--text2); font-size: 13px; cursor: pointer; transition: all 0.2s; }
.toggle-btn.active { background: var(--bg2); color: var(--text); border: 1px solid var(--border); }

.mkt-body { display: flex; flex: 1; overflow: hidden; min-height: 0; }

/* Filters */
.filters-panel { width: 240px; background: var(--bg2); border-right: 1px solid var(--border); padding: 20px 16px; overflow-y: auto; flex-shrink: 0; display: flex; flex-direction: column; gap: 20px; }
.filter-group { display: flex; flex-direction: column; gap: 8px; }
.filter-label { font-size: 11px; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 0.06em; }
.cat-filters { display: flex; flex-direction: column; gap: 4px; }
.cat-btn { padding: 7px 10px; border-radius: 6px; border: 1px solid transparent; background: transparent; color: var(--text2); font-size: 13px; cursor: pointer; text-align: left; transition: all 0.15s; }
.cat-btn:hover { background: var(--bg3); color: var(--text); }
.cat-btn.active { background: rgba(99,102,241,0.12); color: var(--primary); border-color: rgba(99,102,241,0.25); }
.rating-btns { display: flex; flex-wrap: wrap; gap: 6px; }
.rating-btn { padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border); background: transparent; color: var(--text2); font-size: 12px; cursor: pointer; transition: all 0.15s; }
.rating-btn.active { border-color: var(--primary); color: var(--primary); background: rgba(99,102,241,0.1); }
.range-input { width: 100%; accent-color: var(--primary); }
.range-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--text2); }
.range-val { color: var(--primary); font-weight: 600; }
.toggle-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; color: var(--text2); }
.toggle-label input { display: none; }
.toggle-check { width: 18px; height: 18px; border: 1px solid var(--border); border-radius: 4px; background: var(--bg3); position: relative; flex-shrink: 0; transition: all 0.2s; }
input:checked ~ .toggle-check, .toggle-label input:checked + .toggle-check { background: var(--primary); border-color: var(--primary); }
.toggle-label input:checked + .toggle-check::after { content: '✓'; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 11px; color: white; }
.btn-clear { padding: 8px; border-radius: 6px; border: 1px dashed var(--border); background: transparent; color: var(--text2); font-size: 13px; cursor: pointer; transition: all 0.2s; }
.btn-clear:hover { border-color: var(--danger); color: var(--danger); }

/* Content */
.mkt-content { flex: 1; overflow-y: auto; padding: 24px; }
.map-view { flex: 1; }

/* Grid */
.prof-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.prof-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; cursor: pointer; transition: all 0.2s; display: flex; flex-direction: column; }
.prof-card:hover { border-color: var(--primary); transform: translateY(-3px); box-shadow: 0 8px 32px rgba(99,102,241,0.15); }
.prof-card-top { position: relative; background: linear-gradient(135deg, var(--bg3), var(--bg2)); padding: 20px; display: flex; justify-content: center; }
.prof-avatar { width: 72px; height: 72px; border-radius: 50%; border: 3px solid var(--border); }
.prof-status-badge { position: absolute; top: 10px; right: 10px; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 999px; }
.prof-status-badge.available { background: rgba(16,185,129,0.15); color: #10b981; }
.prof-status-badge.busy { background: rgba(239,68,68,0.15); color: #ef4444; }
.prof-card-body { padding: 16px; flex: 1; display: flex; flex-direction: column; gap: 8px; }
.prof-name { font-size: 16px; font-weight: 700; }
.prof-rating { display: flex; align-items: center; gap: 6px; }
.stars { color: #f59e0b; font-size: 13px; }
.rating-val { font-size: 13px; font-weight: 600; }
.rating-count { font-size: 12px; color: var(--text2); }
.prof-cats { display: flex; flex-wrap: wrap; gap: 4px; }
.cat-tag { background: var(--bg3); border: 1px solid var(--border); border-radius: 6px; padding: 2px 8px; font-size: 11px; color: var(--text2); }
.cat-tag.exp { color: var(--primary); border-color: rgba(99,102,241,0.3); }
.cat-tag.more { color: var(--text2); }
.prof-bio { font-size: 12px; color: var(--text2); line-height: 1.5; flex: 1; }
.prof-footer { display: flex; align-items: center; justify-content: space-between; margin-top: auto; }
.prof-price { font-size: 18px; font-weight: 800; color: var(--accent); }
.prof-price span { font-size: 12px; font-weight: 400; color: var(--text2); }
.prof-meta-right { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }
.prof-dist, .prof-jobs { font-size: 11px; color: var(--text2); }
.prof-plan-badge { font-size: 11px; font-weight: 600; }
.plan-basic { color: #6366f1; }
.plan-pro { color: #10b981; }
.plan-premium { color: #f59e0b; }
.prof-card-actions { display: flex; border-top: 1px solid var(--border); }
.prof-hire-btn { flex: 1; padding: 12px; background: rgba(99,102,241,0.08); border: none; border-right: 1px solid var(--border); color: var(--primary); font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.prof-hire-btn:hover { background: rgba(99,102,241,0.16); }
.prof-page-btn { flex: 0 0 auto; padding: 12px; background: transparent; border: none; color: var(--text2); font-size: 12px; cursor: pointer; text-decoration: none; transition: color 0.2s; white-space: nowrap; }
.prof-page-btn:hover { color: var(--accent); }
.btn-view-page { display: block; text-align: center; padding: 10px; border: 1px solid var(--border); border-radius: 8px; color: var(--text2); font-size: 13px; text-decoration: none; transition: all 0.2s; }
.btn-view-page:hover { border-color: var(--accent); color: var(--accent); }

/* Skeleton */
.skeleton { pointer-events: none; animation: shimmer 1.5s infinite; }
.sk-avatar { width: 72px; height: 72px; border-radius: 50%; background: var(--bg3); margin: 20px auto; }
.sk-line { height: 10px; background: var(--bg3); border-radius: 4px; margin: 8px 16px; }
.sk-line.long { width: 70%; }
.sk-line.mid { width: 50%; }
.sk-line.short { width: 35%; }
@keyframes shimmer { 0%,100%{opacity:1;} 50%{opacity:0.5;} }

/* Empty */
.empty-grid { grid-column: 1/-1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; color: var(--text2); }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-grid h3 { font-size: 18px; color: var(--text); }
.empty-grid p { font-size: 14px; margin-top: 6px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.prof-modal { background: var(--bg2); border: 1px solid var(--border); border-radius: 20px; width: 100%; max-width: 800px; max-height: 90vh; overflow-y: auto; position: relative; }
.modal-close { position: sticky; top: 16px; left: calc(100% - 40px); display: block; background: var(--bg3); border: 1px solid var(--border); border-radius: 50%; width: 32px; height: 32px; cursor: pointer; color: var(--text2); font-size: 14px; z-index: 10; margin: 16px 16px 0 auto; }
.modal-hero { display: flex; gap: 20px; align-items: flex-start; padding: 0 24px 24px; border-bottom: 1px solid var(--border); }
.modal-avatar { width: 80px; height: 80px; border-radius: 50%; border: 3px solid var(--border); flex-shrink: 0; }
.modal-hero-info { flex: 1; }
.modal-header-top { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; flex-wrap: wrap; }
.modal-header-top h2 { font-size: 22px; font-weight: 700; }
.avail-badge { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 999px; }
.avail-badge.available { background: rgba(16,185,129,0.15); color: #10b981; }
.avail-badge.busy { background: rgba(239,68,68,0.15); color: #ef4444; }
.modal-rating { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; font-size: 14px; }
.modal-cats { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.modal-price { font-size: 24px; font-weight: 800; color: var(--accent); }
.modal-price span { font-size: 14px; font-weight: 400; color: var(--text2); }
.modal-body-cols { display: grid; grid-template-columns: 1fr 340px; gap: 0; }
.modal-col-left { padding: 24px; border-right: 1px solid var(--border); display: flex; flex-direction: column; gap: 24px; }
.modal-col-right { padding: 24px; }
.modal-section h3 { font-size: 15px; font-weight: 700; margin-bottom: 10px; }
.modal-section p { font-size: 14px; color: var(--text2); line-height: 1.6; }
.review-card { background: var(--bg3); border-radius: 8px; padding: 12px; margin-bottom: 8px; }
.review-top { display: flex; justify-content: space-between; margin-bottom: 6px; }
.review-author { font-size: 13px; font-weight: 600; }
.review-text { font-size: 13px; color: var(--text2); }
.booking-form-card { background: var(--bg3); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 14px; border: 1px solid var(--border); }
.booking-form-card h3 { font-size: 16px; font-weight: 700; }
.field { display: flex; flex-direction: column; gap: 6px; }
.btn-book { padding: 14px; background: var(--primary); color: white; border: none; border-radius: 10px; font-size: 14px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.btn-book:hover:not(:disabled) { background: var(--primary-hover); transform: translateY(-1px); }
.btn-book:disabled { opacity: 0.6; cursor: not-allowed; }
.alert-success { background: rgba(16,185,129,0.1); border: 1px solid #10b981; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #10b981; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid #ef4444; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #ef4444; }
</style>
