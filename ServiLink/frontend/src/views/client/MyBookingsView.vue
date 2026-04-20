<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Mis reservas</h1>
        <p class="page-subtitle">Historial y estado de tus servicios contratados</p>
      </div>

      <div v-if="loading" class="loading-state">Cargando...</div>

      <div v-else-if="bookings.length === 0" class="empty-state card">
        <p>No tienes reservas aún. <router-link to="/home">Busca un profesional</router-link></p>
      </div>

      <div v-else class="bookings-list">
        <div v-for="b in bookings" :key="b.id" class="booking-card card">
          <div class="booking-header">
            <div class="booking-info">
              <div class="booking-title">{{ b.category?.icon }} {{ b.category?.name }}</div>
              <div class="booking-prof">con <strong>{{ b.professional?.name }}</strong></div>
              <div class="booking-date">{{ formatDate(b.created_at) }}</div>
            </div>
            <div class="booking-right">
              <span :class="`status-${b.status} badge`" style="font-size:13px;">{{ statusLabel(b.status) }}</span>
              <div class="booking-price">${{ b.price }}/hr</div>
            </div>
          </div>

          <p v-if="b.description" class="booking-desc">{{ b.description }}</p>
          <p v-if="b.client_address" class="booking-addr">📍 {{ b.client_address }}</p>

          <div class="booking-actions">
            <button v-if="b.status === 'pending'" @click="cancelBooking(b.id)" class="btn btn-danger btn-sm">Cancelar</button>
            <button v-if="b.status === 'completed' && !b.has_review" @click="openReviewModal(b)" class="btn btn-accent btn-sm">⭐ Dejar reseña</button>
            <span v-if="b.status === 'completed' && b.has_review" class="badge badge-accent">Reseña enviada</span>
          </div>

          <!-- Simulated tracking for in_progress -->
          <div v-if="b.status === 'in_progress'" class="tracking-bar">
            <div class="tracking-dot"></div>
            <span>El profesional está en camino — ubicación simulada</span>
            <span class="tracking-time">~15 min</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <div v-if="reviewModal" class="modal-overlay" @click.self="reviewModal = null">
      <div class="modal-sm">
        <h2 style="margin-bottom:16px;">Califica el servicio</h2>
        <p style="color:var(--text2);font-size:14px;margin-bottom:16px;">con {{ reviewModal.professional?.name }}</p>
        <div class="star-rating">
          <span v-for="n in 5" :key="n" @click="reviewForm.rating = n" class="star" :class="{ active: n <= reviewForm.rating }">★</span>
        </div>
        <textarea v-model="reviewForm.comment" class="input" rows="3" placeholder="Cuenta tu experiencia..." style="margin-top:12px;"></textarea>
        <div v-if="reviewError" class="alert-error" style="margin-top:8px;">{{ reviewError }}</div>
        <div style="display:flex;gap:8px;margin-top:16px;">
          <button @click="reviewModal = null" class="btn btn-secondary" style="flex:1;justify-content:center;">Cancelar</button>
          <button @click="submitReview" class="btn btn-primary" style="flex:1;justify-content:center;" :disabled="reviewLoading">
            {{ reviewLoading ? 'Enviando...' : 'Enviar reseña' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { bookingApi, reviewApi } from '../../api/index.js'

const bookings = ref([])
const loading = ref(true)
const reviewModal = ref(null)
const reviewForm = ref({ rating: 5, comment: '' })
const reviewLoading = ref(false)
const reviewError = ref('')

onMounted(async () => {
  const { data } = await bookingApi.list()
  bookings.value = data
  loading.value = false
})

function statusLabel(s) {
  return { pending: '⏳ Pendiente', accepted: '✅ Aceptada', in_progress: '🚀 En progreso', completed: '✓ Completada', cancelled: '✗ Cancelada' }[s] || s
}

function formatDate(dt) {
  return dt ? new Date(dt).toLocaleDateString('es-MX', { day: 'numeric', month: 'short', year: 'numeric' }) : ''
}

async function cancelBooking(id) {
  await bookingApi.updateStatus(id, 'cancelled')
  const { data } = await bookingApi.list()
  bookings.value = data
}

function openReviewModal(b) {
  reviewModal.value = b
  reviewForm.value = { rating: 5, comment: '' }
  reviewError.value = ''
}

async function submitReview() {
  reviewLoading.value = true
  reviewError.value = ''
  try {
    await reviewApi.create({ booking_id: reviewModal.value.id, ...reviewForm.value })
    reviewModal.value = null
    const { data } = await bookingApi.list()
    bookings.value = data
  } catch (e) {
    reviewError.value = e.response?.data?.detail || 'Error al enviar reseña'
  } finally {
    reviewLoading.value = false
  }
}
</script>

<style scoped>
.bookings-list { display: flex; flex-direction: column; gap: 16px; }
.booking-card { display: flex; flex-direction: column; gap: 12px; }
.booking-header { display: flex; justify-content: space-between; align-items: flex-start; }
.booking-title { font-size: 16px; font-weight: 600; }
.booking-prof { font-size: 14px; color: var(--text2); margin: 4px 0; }
.booking-date { font-size: 12px; color: var(--text2); }
.booking-right { text-align: right; display: flex; flex-direction: column; gap: 8px; align-items: flex-end; }
.booking-price { font-size: 16px; font-weight: 700; color: var(--accent); }
.booking-desc { font-size: 14px; color: var(--text2); }
.booking-addr { font-size: 13px; color: var(--text2); }
.booking-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.loading-state { padding: 32px; text-align: center; color: var(--text2); }
.empty-state { padding: 40px; text-align: center; color: var(--text2); }
.empty-state a { color: var(--primary); }
.tracking-bar { background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.3); border-radius: 8px; padding: 10px 14px; display: flex; align-items: center; gap: 10px; font-size: 13px; color: #06b6d4; }
.tracking-dot { width: 8px; height: 8px; background: #06b6d4; border-radius: 50%; animation: pulse 1.5s infinite; flex-shrink: 0; }
.tracking-time { margin-left: auto; font-weight: 600; }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.3; } }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-sm { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 32px; width: 100%; max-width: 400px; }
.star-rating { display: flex; gap: 8px; }
.star { font-size: 32px; color: var(--border); cursor: pointer; transition: color 0.15s; }
.star.active { color: #f59e0b; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 10px; font-size: 14px; color: var(--danger); }
</style>
