<template>
  <div v-if="loadError" class="conv-error">
    <div class="err-card">
      <div class="err-icon">⚠️</div>
      <h2>Convención no encontrada</h2>
      <p>{{ loadError }}</p>
      <router-link to="/" class="btn btn-primary">← Volver al inicio</router-link>
    </div>
  </div>
  <div v-else-if="!conv.id" class="conv-loading">
    <div class="spinner"></div>
    <p>Cargando convención…</p>
  </div>
  <div v-else class="conv-page" :style="cssVars">
    <!-- NAV -->
    <nav class="conv-nav">
      <div class="nav-left">
        <img v-if="conv.logo_url" :src="conv.logo_url" class="nav-logo" />
        <div>
          <div class="nav-name">{{ conv.name }}</div>
          <div class="nav-edition" v-if="conv.edition">{{ conv.edition }}</div>
        </div>
      </div>
      <div class="nav-right">
        <div class="days-counter" v-if="daysUntil !== null">
          <span v-if="daysUntil > 0"><strong>{{ daysUntil }}</strong> días</span>
          <span v-else-if="daysUntil === 0" style="color:var(--conv-accent)">¡HOY!</span>
          <span v-else style="color:var(--text2)">Finalizado</span>
        </div>
        <button @click="openCheckout" class="btn-buy">🎫 Comprar Boletos</button>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero" :style="heroStyle">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-edition" v-if="conv.edition">{{ conv.edition }}</div>
        <h1 class="hero-title">{{ conv.name }}</h1>
        <p class="hero-tagline" v-if="conv.tagline">{{ conv.tagline }}</p>
        <div class="hero-meta">
          <span v-if="conv.start_date">📅 {{ formatDateRange(conv.start_date, conv.end_date) }}</span>
          <span v-if="conv.venue_name">📍 {{ conv.venue_name }}, {{ conv.city }}</span>
        </div>
        <div class="countdown" v-if="countdown">
          <div class="cd-item"><div class="cd-num">{{ countdown.days }}</div><div class="cd-label">Días</div></div>
          <div class="cd-sep">:</div>
          <div class="cd-item"><div class="cd-num">{{ countdown.hours }}</div><div class="cd-label">Horas</div></div>
          <div class="cd-sep">:</div>
          <div class="cd-item"><div class="cd-num">{{ countdown.minutes }}</div><div class="cd-label">Min</div></div>
          <div class="cd-sep">:</div>
          <div class="cd-item"><div class="cd-num">{{ countdown.seconds }}</div><div class="cd-label">Seg</div></div>
        </div>
        <button @click="openCheckout" class="btn-hero-cta">🎫 Comprar Boletos</button>
      </div>
    </section>

    <!-- STAGES -->
    <section class="section" v-if="conv.stages?.length">
      <div class="container">
        <h2 class="section-title">Escenarios</h2>
        <div class="stages-grid">
          <div
            v-for="stage in conv.stages"
            :key="stage.id"
            class="stage-card"
            :class="{ active: activeStage?.id === stage.id }"
            @click="activeStage = stage"
            :style="`--sc: ${stage.color}`"
          >
            <div class="stage-dot" :style="`background:${stage.color}`"></div>
            <div class="stage-info">
              <div class="stage-name">{{ stage.name }}</div>
              <div class="stage-loc" v-if="stage.location_in_venue">{{ stage.location_in_venue }}</div>
              <a v-if="stage.stream_url" :href="stage.stream_url" target="_blank" class="stream-link" @click.stop>
                📺 Ver en vivo
              </a>
            </div>
            <div class="stage-count">{{ stage.sessions?.length || 0 }} sesiones</div>
          </div>
        </div>

        <!-- Schedule Grid -->
        <div class="schedule" v-if="activeStage">
          <h3 class="schedule-title">📅 Agenda — {{ activeStage.name }}</h3>
          <div v-for="(daySessions, day) in groupedSessions" :key="day" class="schedule-day">
            <div class="day-header">{{ day }}</div>
            <div class="sessions-list">
              <div v-for="s in daySessions" :key="s.id" class="session-row">
                <div class="session-time">
                  {{ fmtTime(s.start_time) }}<br><span style="color:var(--text2);font-size:11px">{{ fmtTime(s.end_time) }}</span>
                </div>
                <div class="session-type-badge" :class="s.session_type">{{ s.session_type }}</div>
                <div class="session-detail">
                  <div class="session-title">{{ s.title }}</div>
                  <div class="session-desc" v-if="s.description">{{ s.description }}</div>
                  <div class="session-speaker" v-if="s.speaker">
                    <img :src="s.speaker.photo_url" v-if="s.speaker.photo_url" class="sp-photo" />
                    <span>{{ s.speaker.name }}<span v-if="s.speaker.title">, {{ s.speaker.title }}</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="!activeStage.sessions?.length" class="empty-state">No hay sesiones programadas aún</div>
        </div>
      </div>
    </section>

    <!-- SPEAKERS -->
    <section class="section section-dark" v-if="conv.speakers?.length">
      <div class="container">
        <h2 class="section-title">Ponentes</h2>
        <div class="speakers-grid">
          <div v-for="sp in conv.speakers" :key="sp.id" class="speaker-card">
            <div class="speaker-keynote" v-if="sp.is_keynote">KEYNOTE</div>
            <img :src="sp.photo_url || `https://api.dicebear.com/7.x/personas/svg?seed=${sp.name}`" class="speaker-photo" />
            <div class="speaker-name">{{ sp.name }}</div>
            <div class="speaker-title" v-if="sp.title">{{ sp.title }}</div>
            <div class="speaker-company" v-if="sp.company">{{ sp.company }}</div>
            <a v-if="sp.twitter" :href="`https://twitter.com/${sp.twitter.replace('@','')}`" target="_blank" class="speaker-twitter">{{ sp.twitter }}</a>
          </div>
        </div>
      </div>
    </section>

    <!-- FLOOR PLAN (Stands) -->
    <section class="section" v-if="conv.stands?.length">
      <div class="container">
        <h2 class="section-title">Plano de Exhibición</h2>
        <div class="floor-plan-legend">
          <span class="legend-item available">Disponible</span>
          <span class="legend-item reserved">Reservado</span>
          <span class="legend-item sold">Ocupado</span>
        </div>
        <div class="floor-plan">
          <div
            v-for="stand in conv.stands"
            :key="stand.id"
            class="stand-box"
            :class="stand.status"
            :style="`left:${stand.x_pos}%;top:${stand.y_pos}%;width:${stand.width}%;height:${stand.height}%;`"
            @click="selectedStand = stand"
          >
            <div class="stand-num">{{ stand.number }}</div>
            <div class="stand-sname" v-if="stand.name">{{ stand.name }}</div>
          </div>
        </div>
        <div class="stand-detail" v-if="selectedStand">
          <div class="stand-detail-header">
            <h4>Stand {{ selectedStand.number }}</h4>
            <button @click="selectedStand = null" class="close-btn">✕</button>
          </div>
          <p v-if="selectedStand.name"><strong>Exhibidor:</strong> {{ selectedStand.name }}</p>
          <p><strong>Categoría:</strong> {{ selectedStand.category }}</p>
          <p><strong>Tamaño:</strong> {{ selectedStand.size }}</p>
          <p><strong>Estado:</strong> <span :class="`badge badge-${standBadge(selectedStand.status)}`">{{ selectedStand.status }}</span></p>
          <p v-if="selectedStand.description">{{ selectedStand.description }}</p>
          <p v-if="selectedStand.status === 'available' && selectedStand.price > 0">
            <strong>Precio:</strong> ${{ selectedStand.price.toFixed(0) }} MXN
          </p>
        </div>
      </div>
    </section>

    <!-- SPONSORS -->
    <section class="section section-dark" v-if="conv.sponsors?.length">
      <div class="container">
        <h2 class="section-title">Patrocinadores</h2>
        <template v-for="tier in sponsorTiers" :key="tier.key">
          <div v-if="getSponsorsByTier(tier.key).length" class="sponsor-tier">
            <div class="tier-label" :class="`tier-${tier.key}`">{{ tier.label }}</div>
            <div class="tier-logos" :class="`tier-size-${tier.size}`">
              <a
                v-for="sp in getSponsorsByTier(tier.key)"
                :key="sp.id"
                :href="sp.website || '#'"
                target="_blank"
                class="sponsor-logo-wrap"
              >
                <img :src="sp.logo_url || `https://api.dicebear.com/7.x/initials/svg?seed=${sp.name}`" :alt="sp.name" class="sponsor-logo" />
                <span class="sponsor-name">{{ sp.name }}</span>
              </a>
            </div>
          </div>
        </template>
      </div>
    </section>

    <!-- TICKETS -->
    <section class="section" id="tickets" v-if="conv.ticket_types?.length">
      <div class="container">
        <h2 class="section-title">Boletos</h2>
        <div class="tickets-grid">
          <div v-for="tt in conv.ticket_types" :key="tt.id" class="ticket-card" :style="`--tc: ${tt.color}`">
            <div class="ticket-color-bar" :style="`background: ${tt.color}`"></div>
            <div class="ticket-body">
              <div class="ticket-name">{{ tt.name }}</div>
              <div class="ticket-price">${{ tt.price.toFixed(0) }} <span>MXN</span></div>
              <div class="ticket-desc" v-if="tt.description">{{ tt.description }}</div>
              <ul class="ticket-benefits" v-if="tt.benefits_json">
                <li v-for="b in parseBenefits(tt.benefits_json)" :key="b">✓ {{ b }}</li>
              </ul>
              <div class="ticket-qty" v-if="tt.quantity_total">
                <div class="qty-bar">
                  <div class="qty-fill" :style="`width:${Math.min(100, tt.quantity_sold / tt.quantity_total * 100)}%; background:${tt.color}`"></div>
                </div>
                <span class="qty-label">{{ tt.quantity_total - tt.quantity_sold }} restantes de {{ tt.quantity_total }}</span>
              </div>
              <button @click="openCheckoutWithType(tt)" class="btn-ticket">Comprar →</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TOURNAMENTS -->
    <section class="section section-dark" v-if="conv.tournaments?.length">
      <div class="container">
        <h2 class="section-title">Torneos</h2>
        <div class="tournaments-grid">
          <div v-for="t in conv.tournaments" :key="t.id" class="tournament-card">
            <div class="tournament-game">{{ t.game }}</div>
            <div class="tournament-name">{{ t.name }}</div>
            <div class="tournament-meta">
              <span>🏆 ${{ t.prize_pool.toFixed(0) }} MXN</span>
              <span>👥 {{ t.participants_count }}/{{ t.max_participants }}</span>
              <span>🎮 {{ formatFormat(t.format) }}</span>
              <span v-if="t.entry_fee > 0">💰 ${{ t.entry_fee.toFixed(0) }} inscripción</span>
              <span v-else>Gratis</span>
            </div>
            <div class="tournament-prize" v-if="t.prize_description">{{ t.prize_description }}</div>
            <div class="tournament-status" :class="t.status">{{ t.status }}</div>
            <button v-if="t.status === 'open'" @click="openTournamentReg(t)" class="btn btn-primary btn-sm">Inscribirse</button>
          </div>
        </div>
      </div>
    </section>

    <!-- LOCATION -->
    <section class="section" v-if="conv.lat && conv.lng">
      <div class="container">
        <h2 class="section-title">Ubicación</h2>
        <div class="location-card">
          <div id="map" class="map-container"></div>
          <div class="location-info">
            <h3>{{ conv.venue_name }}</h3>
            <p>{{ conv.address }}</p>
            <p>{{ conv.city }}</p>
            <a :href="`https://maps.google.com/?q=${conv.lat},${conv.lng}`" target="_blank" class="btn btn-ghost btn-sm">
              Abrir en Google Maps →
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- CHECKOUT MODAL -->
    <div class="modal-overlay" v-if="showCheckout" @click.self="showCheckout = false">
      <div class="modal checkout-modal">
        <div class="modal-header">
          <h2>🎫 Comprar Boletos</h2>
          <button @click="showCheckout = false" class="close-btn">✕</button>
        </div>

        <!-- Step 1: Select quantities -->
        <div v-if="checkoutStep === 1">
          <div v-for="tt in conv.ticket_types" :key="tt.id" class="checkout-tt-row">
            <div class="tt-info">
              <div class="tt-name">{{ tt.name }}</div>
              <div class="tt-price">${{ tt.price.toFixed(0) }} MXN</div>
            </div>
            <div class="qty-controls">
              <button @click="decrementQty(tt.id)" class="qty-btn">−</button>
              <span class="qty-val">{{ quantities[tt.id] || 0 }}</span>
              <button @click="incrementQty(tt.id, tt)" class="qty-btn">+</button>
            </div>
          </div>
          <div class="checkout-total">
            Total: <strong>${{ checkoutTotal.toFixed(0) }} MXN</strong>
          </div>
          <div style="display:flex;gap:10px;margin-top:16px">
            <button @click="showCheckout = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
            <button @click="checkoutStep = 2" :disabled="checkoutTotal === 0" class="btn btn-primary" style="flex:1">
              Continuar →
            </button>
          </div>
        </div>

        <!-- Step 2: Buyer info -->
        <div v-if="checkoutStep === 2">
          <div class="form-group"><label>Nombre completo</label><input v-model="buyer.name" placeholder="Tu nombre" required /></div>
          <div class="form-group" style="margin-top:12px"><label>Email</label><input v-model="buyer.email" type="email" placeholder="tu@email.com" required /></div>
          <div class="form-group" style="margin-top:12px"><label>Teléfono</label><input v-model="buyer.phone" placeholder="+52 55 ..." /></div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="checkoutStep = 1" class="btn btn-ghost" style="flex:1">← Atrás</button>
            <button @click="processPurchase" :disabled="!buyer.name || !buyer.email || purchasing" class="btn btn-primary" style="flex:1">
              {{ purchasing ? 'Procesando...' : 'Confirmar Compra' }}
            </button>
          </div>
        </div>

        <!-- Step 3: Confirmation -->
        <div v-if="checkoutStep === 3" class="checkout-success">
          <div class="success-icon">✅</div>
          <h3>¡Compra registrada!</h3>
          <div v-if="purchaseResult?.note" class="manual-note">
            <strong>Pago Manual:</strong> {{ purchaseResult.note }}
          </div>
          <p>Total: <strong>${{ purchaseResult?.total?.toFixed(0) }} MXN</strong></p>
          <div v-if="purchaseTickets.length" class="qr-list">
            <div v-for="t in purchaseTickets" :key="t.id" class="qr-item">
              <div class="qr-code">{{ t.qr_code }}</div>
              <div class="qr-label">{{ t.attendee_name }} — {{ t.ticket_type?.name }}</div>
            </div>
          </div>
          <button @click="resetCheckout" class="btn btn-primary" style="margin-top:16px;width:100%">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- TOURNAMENT REGISTRATION MODAL -->
    <div class="modal-overlay" v-if="showTournamentReg" @click.self="showTournamentReg = false">
      <div class="modal">
        <h2>Inscripción: {{ selectedTournament?.name }}</h2>
        <div class="form-group" style="margin-top:16px"><label>Nombre del jugador</label><input v-model="tournamentReg.player_name" placeholder="Nombre completo" /></div>
        <div class="form-group" style="margin-top:12px"><label>Email</label><input v-model="tournamentReg.player_email" type="email" placeholder="tu@email.com" /></div>
        <div class="form-group" style="margin-top:12px"><label>Gamer Tag (opcional)</label><input v-model="tournamentReg.player_tag" placeholder="@GamerTag" /></div>
        <div v-if="tournamentRegError" class="error-msg" style="margin-top:10px">{{ tournamentRegError }}</div>
        <div style="display:flex;gap:10px;margin-top:20px">
          <button @click="showTournamentReg = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
          <button @click="submitTournamentReg" :disabled="regLoading" class="btn btn-primary" style="flex:1">
            {{ regLoading ? 'Registrando...' : 'Inscribirme' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/index.js'

const route = useRoute()
const conv = ref({})
const loadError = ref('')
const activeStage = ref(null)
const selectedStand = ref(null)
const countdown = ref(null)
let countdownInterval = null
let mapInstance = null

// Checkout state
const showCheckout = ref(false)
const checkoutStep = ref(1)
const quantities = ref({})
const buyer = ref({ name: '', email: '', phone: '' })
const purchasing = ref(false)
const purchaseResult = ref(null)
const purchaseTickets = ref([])

// Tournament reg
const showTournamentReg = ref(false)
const selectedTournament = ref(null)
const tournamentReg = ref({ player_name: '', player_email: '', player_tag: '' })
const tournamentRegError = ref('')
const regLoading = ref(false)

const cssVars = computed(() => ({
  '--conv-primary': conv.value.theme_color || '#7c3aed',
  '--conv-accent': conv.value.accent_color || '#f59e0b',
  '--conv-bg': conv.value.bg_color || '#0a0a0f',
}))

const heroStyle = computed(() => {
  if (conv.value.banner_url || conv.value.cover_url) {
    return `background-image: url(${conv.value.banner_url || conv.value.cover_url})`
  }
  return `background: linear-gradient(135deg, ${conv.value.bg_color || '#0a0a0f'}, ${conv.value.theme_color || '#7c3aed'}22)`
})

const daysUntil = computed(() => {
  if (!conv.value.start_date) return null
  const diff = new Date(conv.value.start_date) - new Date()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
})

const groupedSessions = computed(() => {
  if (!activeStage.value?.sessions) return {}
  const groups = {}
  for (const s of activeStage.value.sessions) {
    const day = new Date(s.start_time).toLocaleDateString('es-MX', { weekday: 'long', day: 'numeric', month: 'long' })
    if (!groups[day]) groups[day] = []
    groups[day].push(s)
  }
  return groups
})

const checkoutTotal = computed(() => {
  let total = 0
  for (const tt of (conv.value.ticket_types || [])) {
    total += (quantities.value[tt.id] || 0) * tt.price
  }
  return total
})

const sponsorTiers = [
  { key: 'title', label: 'Patrocinador Título', size: 'xl' },
  { key: 'diamond', label: 'Diamante', size: 'lg' },
  { key: 'platinum', label: 'Platino', size: 'lg' },
  { key: 'gold', label: 'Oro', size: 'md' },
  { key: 'silver', label: 'Plata', size: 'sm' },
  { key: 'bronze', label: 'Bronce', size: 'sm' },
  { key: 'media', label: 'Media Partner', size: 'sm' },
]

function getSponsorsByTier(tier) {
  return (conv.value.sponsors || []).filter(s => s.tier === tier)
}

function parseBenefits(json) {
  try { return JSON.parse(json) } catch { return [] }
}

function formatDateRange(start, end) {
  const s = new Date(start)
  const e = end ? new Date(end) : null
  const opts = { day: 'numeric', month: 'long', year: 'numeric' }
  if (!e || s.toDateString() === e.toDateString()) return s.toLocaleDateString('es-MX', opts)
  return `${s.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' })} — ${e.toLocaleDateString('es-MX', opts)}`
}

function fmtTime(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
}

function formatFormat(f) {
  const map = { single_elim: 'Eliminación Simple', double_elim: 'Doble Eliminación', round_robin: 'Round Robin', swiss: 'Sistema Suizo' }
  return map[f] || f
}

function standBadge(status) {
  if (status === 'available') return 'success'
  if (status === 'reserved') return 'warning'
  return 'danger'
}

function startCountdown() {
  if (!conv.value.start_date) return
  const update = () => {
    const diff = new Date(conv.value.start_date) - new Date()
    if (diff <= 0) { countdown.value = null; return }
    const d = Math.floor(diff / (1000 * 60 * 60 * 24))
    const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    const s = Math.floor((diff % (1000 * 60)) / 1000)
    countdown.value = {
      days: String(d).padStart(2, '0'),
      hours: String(h).padStart(2, '0'),
      minutes: String(m).padStart(2, '0'),
      seconds: String(s).padStart(2, '0'),
    }
  }
  update()
  countdownInterval = setInterval(update, 1000)
}

function initMap() {
  if (!conv.value.lat || !conv.value.lng) return
  import('leaflet').then(L => {
    if (mapInstance) mapInstance.remove()
    mapInstance = L.map('map').setView([conv.value.lat, conv.value.lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(mapInstance)
    L.marker([conv.value.lat, conv.value.lng])
      .addTo(mapInstance)
      .bindPopup(`<strong>${conv.value.venue_name}</strong><br>${conv.value.address}`)
      .openPopup()
  })
}

function openCheckout() {
  showCheckout.value = true
  checkoutStep.value = 1
}

function openCheckoutWithType(tt) {
  quantities.value = {}
  quantities.value[tt.id] = 1
  showCheckout.value = true
  checkoutStep.value = 1
}

function incrementQty(id, tt) {
  const available = (tt.quantity_total || 9999) - tt.quantity_sold
  const current = quantities.value[id] || 0
  if (current < available && current < 10) {
    quantities.value = { ...quantities.value, [id]: current + 1 }
  }
}

function decrementQty(id) {
  const current = quantities.value[id] || 0
  if (current > 0) quantities.value = { ...quantities.value, [id]: current - 1 }
}

async function processPurchase() {
  if (!buyer.value.name || !buyer.value.email) return
  purchasing.value = true
  try {
    const items = []
    for (const [ttId, qty] of Object.entries(quantities.value)) {
      if (qty > 0) items.push({ ticket_type_id: parseInt(ttId), quantity: qty })
    }
    const { data } = await api.post('/payments/purchase', {
      convention_id: conv.value.id,
      buyer_name: buyer.value.name,
      buyer_email: buyer.value.email,
      buyer_phone: buyer.value.phone,
      items,
    })
    purchaseResult.value = data
    // If manual payment, confirm right away to get tickets
    if (!data.stripe_client_secret) {
      await api.post(`/payments/confirm/${data.payment_id}`)
      // Reload conv to refresh quantities
      const { data: updated } = await api.get(`/public/convention/${route.params.slug}`)
      conv.value = updated
    }
    checkoutStep.value = 3
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al procesar la compra')
  } finally {
    purchasing.value = false
  }
}

function resetCheckout() {
  showCheckout.value = false
  checkoutStep.value = 1
  quantities.value = {}
  buyer.value = { name: '', email: '', phone: '' }
  purchaseResult.value = null
  purchaseTickets.value = []
}

function openTournamentReg(t) {
  selectedTournament.value = t
  showTournamentReg.value = true
  tournamentReg.value = { player_name: '', player_email: '', player_tag: '' }
  tournamentRegError.value = ''
}

async function submitTournamentReg() {
  regLoading.value = true
  tournamentRegError.value = ''
  try {
    await api.post('/tournaments/register', {
      tournament_id: selectedTournament.value.id,
      ...tournamentReg.value
    })
    showTournamentReg.value = false
    alert('¡Inscripción exitosa! Te esperamos en el torneo.')
    // Refresh conv
    const { data } = await api.get(`/public/convention/${route.params.slug}`)
    conv.value = data
  } catch (e) {
    tournamentRegError.value = e.response?.data?.detail || 'Error al inscribirse'
  } finally {
    regLoading.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get(`/public/convention/${route.params.slug}`)
    conv.value = data
    if (data.stages?.length) activeStage.value = data.stages[0]
    startCountdown()
    setTimeout(initMap, 300)
  } catch (e) {
    loadError.value = e.response?.status === 404
      ? `No existe convención con slug "${route.params.slug}".`
      : (e.response?.data?.detail || 'Error al cargar la convención.')
    console.error('Convention load failed', e)
  }
})

onUnmounted(() => {
  if (countdownInterval) clearInterval(countdownInterval)
  if (mapInstance) mapInstance.remove()
})
</script>

<style scoped>
.conv-page {
  background: var(--conv-bg, #0a0a0f);
  color: var(--text);
  min-height: 100vh;
}

/* NAV */
.conv-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 40px;
  background: rgba(7,7,13,0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}
.nav-left { display: flex; align-items: center; gap: 14px; }
.nav-logo { width: 36px; height: 36px; border-radius: 8px; }
.nav-name { font-weight: 800; font-size: 16px; }
.nav-edition { font-size: 11px; color: var(--conv-accent); }
.nav-right { display: flex; align-items: center; gap: 16px; }
.days-counter { font-size: 14px; color: var(--text2); }
.btn-buy {
  background: var(--conv-primary, #7c3aed);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.2s;
}
.btn-buy:hover { opacity: 0.85; }

/* HERO */
.hero {
  min-height: 92vh;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.7) 60%, rgba(7,7,13,1) 100%);
}
.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 40px 20px;
  max-width: 800px;
}
.hero-edition {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 16px;
  color: var(--conv-accent);
}
.hero-title {
  font-size: 70px;
  font-weight: 900;
  line-height: 1.0;
  margin-bottom: 16px;
  letter-spacing: -2px;
  text-shadow: 0 4px 30px rgba(0,0,0,0.5);
}
.hero-tagline {
  font-size: 20px;
  color: rgba(255,255,255,0.8);
  margin-bottom: 20px;
  font-weight: 300;
}
.hero-meta {
  display: flex;
  gap: 24px;
  justify-content: center;
  font-size: 15px;
  color: rgba(255,255,255,0.7);
  margin-bottom: 32px;
}
.countdown {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 32px;
}
.cd-item { text-align: center; }
.cd-num {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 36px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  min-width: 70px;
}
.cd-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); margin-top: 6px; }
.cd-sep { font-size: 32px; font-weight: 900; color: var(--conv-accent); align-self: flex-start; padding-top: 10px; }
.btn-hero-cta {
  background: var(--conv-primary, #7c3aed);
  color: white;
  border: none;
  padding: 16px 40px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.btn-hero-cta:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(0,0,0,0.5); }

/* SECTIONS */
.section { padding: 80px 0; }
.section-dark { background: var(--bg2); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 40px; }
.section-title { font-size: 32px; font-weight: 900; margin-bottom: 36px; }

/* STAGES */
.stages-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 32px; }
.stage-card {
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 14px;
}
.stage-card.active { border-color: var(--sc); background: rgba(255,255,255,0.05); }
.stage-card:hover { border-color: var(--sc); }
.stage-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.stage-info { flex: 1; min-width: 0; }
.stage-name { font-weight: 700; font-size: 15px; }
.stage-loc { font-size: 12px; color: var(--text2); margin-top: 2px; }
.stream-link { font-size: 12px; color: var(--conv-primary, #7c3aed); font-weight: 600; display: inline-block; margin-top: 4px; }
.stage-count { font-size: 12px; color: var(--text2); white-space: nowrap; }

.schedule { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px; }
.schedule-title { font-size: 18px; font-weight: 700; margin-bottom: 20px; }
.schedule-day { margin-bottom: 24px; }
.day-header { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--conv-accent); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.sessions-list { display: flex; flex-direction: column; gap: 10px; }
.session-row { display: grid; grid-template-columns: 80px 90px 1fr; gap: 14px; align-items: start; padding: 12px; background: rgba(255,255,255,0.02); border-radius: 8px; }
.session-time { font-size: 13px; font-weight: 600; font-family: monospace; }
.session-type-badge {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 4px;
  background: rgba(124,58,237,0.2);
  color: #a78bfa;
  width: fit-content;
  align-self: start;
  margin-top: 2px;
}
.session-type-badge.workshop { background: rgba(16,185,129,0.2); color: #10b981; }
.session-type-badge.panel { background: rgba(59,130,246,0.2); color: #3b82f6; }
.session-type-badge.performance { background: rgba(245,158,11,0.2); color: #f59e0b; }
.session-type-badge.ceremony { background: rgba(239,68,68,0.2); color: #ef4444; }

.session-title { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.session-desc { font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.session-speaker { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text2); }
.sp-photo { width: 24px; height: 24px; border-radius: 50%; object-fit: cover; }

.empty-state { text-align: center; color: var(--text2); padding: 32px; }

/* SPEAKERS */
.speakers-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; }
.speaker-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  text-align: center;
  position: relative;
  transition: border-color 0.2s;
}
.speaker-card:hover { border-color: var(--conv-primary, #7c3aed); }
.speaker-keynote {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--conv-accent, #f59e0b);
  color: #000;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 1px;
  padding: 2px 8px;
  border-radius: 4px;
}
.speaker-photo { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin: 0 auto 12px; display: block; border: 2px solid var(--border); }
.speaker-name { font-weight: 700; font-size: 15px; margin-bottom: 4px; }
.speaker-title { font-size: 12px; color: var(--conv-accent, #f59e0b); margin-bottom: 2px; }
.speaker-company { font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.speaker-twitter { font-size: 11px; color: var(--conv-primary, #7c3aed); }

/* FLOOR PLAN */
.floor-plan-legend { display: flex; gap: 16px; margin-bottom: 16px; }
.legend-item { font-size: 12px; padding: 4px 12px; border-radius: 4px; font-weight: 600; }
.legend-item.available { background: rgba(16,185,129,0.15); color: #10b981; }
.legend-item.reserved { background: rgba(245,158,11,0.15); color: #f59e0b; }
.legend-item.sold { background: rgba(239,68,68,0.15); color: #ef4444; }

.floor-plan {
  position: relative;
  width: 100%;
  height: 400px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 40px 40px;
}

.stand-box {
  position: absolute;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid;
  transition: all 0.15s;
  font-size: 10px;
}
.stand-box.available { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.5); }
.stand-box.available:hover { background: rgba(16,185,129,0.25); }
.stand-box.reserved { background: rgba(245,158,11,0.15); border-color: rgba(245,158,11,0.5); }
.stand-box.sold { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.4); }
.stand-box.complimentary { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.5); }

.stand-num { font-weight: 800; font-size: 11px; }
.stand-sname { font-size: 9px; text-align: center; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 90%; color: var(--text2); }

.stand-detail {
  margin-top: 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
}
.stand-detail-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.stand-detail-header h4 { font-size: 16px; font-weight: 700; }
.close-btn { background: transparent; border: 1px solid var(--border); color: var(--text2); width: 28px; height: 28px; border-radius: 6px; cursor: pointer; }
.stand-detail p { font-size: 14px; margin-bottom: 6px; color: var(--text2); }

/* SPONSORS */
.sponsor-tier { margin-bottom: 32px; }
.tier-label { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }
.tier-title { color: #ffd700; }
.tier-diamond { color: #b9f2ff; }
.tier-platinum { color: #e5e7eb; }
.tier-gold { color: #f59e0b; }
.tier-silver { color: #94a3b8; }
.tier-bronze { color: #d97706; }
.tier-media { color: var(--text2); }

.tier-logos { display: flex; flex-wrap: wrap; gap: 20px; align-items: center; }
.tier-size-xl .sponsor-logo-wrap { flex-direction: column; }
.tier-size-xl .sponsor-logo { width: 140px; height: 140px; }
.tier-size-lg .sponsor-logo { width: 100px; height: 100px; }
.tier-size-md .sponsor-logo { width: 80px; height: 80px; }
.tier-size-sm .sponsor-logo { width: 60px; height: 60px; }

.sponsor-logo-wrap { display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit; }
.sponsor-logo { border-radius: 8px; object-fit: contain; background: white; padding: 4px; }
.sponsor-name { font-size: 12px; font-weight: 600; }

/* TICKETS */
.tickets-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
.ticket-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; transition: border-color 0.2s; }
.ticket-card:hover { border-color: var(--tc); }
.ticket-color-bar { height: 4px; }
.ticket-body { padding: 20px; }
.ticket-name { font-size: 18px; font-weight: 800; margin-bottom: 6px; }
.ticket-price { font-size: 32px; font-weight: 900; color: var(--tc); }
.ticket-price span { font-size: 16px; font-weight: 400; color: var(--text2); }
.ticket-desc { font-size: 13px; color: var(--text2); margin: 10px 0; }
.ticket-benefits { list-style: none; margin: 12px 0; font-size: 13px; line-height: 1.8; }
.ticket-benefits li { color: var(--text2); }
.qty-bar { height: 4px; background: var(--border); border-radius: 2px; margin-bottom: 4px; }
.qty-fill { height: 100%; border-radius: 2px; transition: width 0.3s; }
.qty-label { font-size: 11px; color: var(--text2); }
.btn-ticket {
  margin-top: 16px;
  width: 100%;
  padding: 12px;
  background: var(--tc, var(--primary));
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-ticket:hover { opacity: 0.85; }

/* TOURNAMENTS */
.tournaments-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.tournament-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 20px; }
.tournament-game { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--conv-accent, #f59e0b); margin-bottom: 6px; }
.tournament-name { font-size: 18px; font-weight: 800; margin-bottom: 12px; }
.tournament-meta { display: flex; flex-wrap: wrap; gap: 8px; font-size: 12px; color: var(--text2); margin-bottom: 10px; }
.tournament-meta span { background: var(--bg3); padding: 3px 8px; border-radius: 4px; }
.tournament-prize { font-size: 12px; color: var(--text2); margin-bottom: 12px; }
.tournament-status { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; }
.tournament-status.open { background: rgba(16,185,129,0.15); color: #10b981; }
.tournament-status.closed { background: rgba(239,68,68,0.15); color: #ef4444; }
.tournament-status.in_progress { background: rgba(245,158,11,0.15); color: #f59e0b; }
.tournament-status.finished { background: rgba(100,116,139,0.15); color: #64748b; }

/* LOCATION */
.location-card { display: grid; grid-template-columns: 1fr 300px; gap: 24px; align-items: start; }
.map-container { height: 320px; border-radius: 12px; border: 1px solid var(--border); overflow: hidden; }
.location-info { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; }
.location-info h3 { font-size: 20px; font-weight: 800; margin-bottom: 8px; }
.location-info p { font-size: 14px; color: var(--text2); margin-bottom: 6px; }
.location-info a { margin-top: 12px; }

/* CHECKOUT MODAL */
.checkout-modal { max-width: 500px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }

.checkout-tt-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
}
.tt-info {}
.tt-name { font-weight: 700; font-size: 15px; }
.tt-price { font-size: 13px; color: var(--text2); }
.qty-controls { display: flex; align-items: center; gap: 12px; }
.qty-btn { width: 32px; height: 32px; background: var(--bg3); border: 1px solid var(--border); color: var(--text); border-radius: 8px; font-size: 18px; cursor: pointer; transition: all 0.15s; }
.qty-btn:hover { border-color: var(--primary); }
.qty-val { font-size: 16px; font-weight: 700; min-width: 20px; text-align: center; }
.checkout-total { text-align: right; font-size: 18px; padding: 16px 0; }

.checkout-success { text-align: center; }
.success-icon { font-size: 48px; margin-bottom: 12px; }
.checkout-success h3 { font-size: 22px; font-weight: 800; margin-bottom: 8px; }
.checkout-success p { color: var(--text2); margin-bottom: 8px; }
.manual-note { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); border-radius: 8px; padding: 12px; font-size: 13px; margin-bottom: 12px; }

.qr-list { display: flex; flex-direction: column; gap: 10px; margin-top: 16px; }
.qr-item { background: var(--bg3); border-radius: 8px; padding: 14px; }
.qr-code { font-family: monospace; font-size: 20px; font-weight: 800; letter-spacing: 4px; color: var(--conv-primary, #7c3aed); margin-bottom: 4px; }
.qr-label { font-size: 12px; color: var(--text2); }

.error-msg { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #ef4444; padding: 10px 14px; border-radius: 8px; font-size: 13px; }

/* LOADING + ERROR STATES */
.conv-loading, .conv-error {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  color: var(--text);
  padding: 24px;
}
.conv-loading { flex-direction: column; gap: 16px; }
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.err-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  max-width: 420px;
}
.err-icon { font-size: 48px; margin-bottom: 12px; }
.err-card h2 { font-size: 22px; font-weight: 800; margin-bottom: 8px; }
.err-card p { color: var(--text2); margin-bottom: 20px; font-size: 14px; }
</style>
