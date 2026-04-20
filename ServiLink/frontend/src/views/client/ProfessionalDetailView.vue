<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div v-if="loading" class="loading-state">Cargando...</div>
      <div v-else-if="!prof" class="loading-state">Profesional no encontrado</div>
      <div v-else>
        <div class="prof-header card" style="margin-bottom:20px;display:flex;gap:20px;align-items:flex-start;">
          <img :src="prof.avatar_url" class="avatar" style="width:80px;height:80px;" />
          <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
              <h1 style="font-size:22px;font-weight:700;">{{ prof.name }}</h1>
              <span :class="prof.is_available ? 'badge-accent' : 'badge-danger'" class="badge">
                {{ prof.is_available ? '✓ Disponible' : '✗ Ocupado' }}
              </span>
            </div>
            <div class="stars" style="margin:6px 0;">★ {{ prof.rating_avg }} · {{ prof.total_reviews }} reseñas · {{ prof.total_jobs }} trabajos</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">
              <span v-for="cat in prof.categories" :key="cat" class="tag">{{ cat }}</span>
              <span class="tag">{{ prof.experience_years }} años</span>
              <span class="tag" style="color:var(--accent);">${{ prof.hourly_rate }}/hr</span>
            </div>
          </div>
        </div>
        <div class="grid-2">
          <div>
            <div class="card" style="margin-bottom:16px;">
              <h2 style="margin-bottom:10px;font-size:16px;">Sobre mí</h2>
              <p style="color:var(--text2);font-size:14px;line-height:1.6;">{{ prof.bio || 'Sin descripción' }}</p>
            </div>
            <div class="card">
              <h2 style="margin-bottom:12px;font-size:16px;">Reseñas ({{ reviews.length }})</h2>
              <div v-for="r in reviews" :key="r.id" class="review-item">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                  <span style="font-weight:600;font-size:13px;">{{ r.client_name }}</span>
                  <span class="stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
                </div>
                <p style="font-size:13px;color:var(--text2);">{{ r.comment }}</p>
              </div>
              <p v-if="reviews.length === 0" style="color:var(--text2);font-size:13px;">Sin reseñas aún</p>
            </div>
          </div>
          <div class="card booking-panel">
            <h2 style="margin-bottom:16px;font-size:16px;">Contratar servicio</h2>
            <div class="field">
              <label class="label">Categoría</label>
              <select v-model="form.category_id" class="input">
                <option v-for="c in matchedCategories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
              </select>
            </div>
            <div class="field">
              <label class="label">Descripción</label>
              <textarea v-model="form.description" class="input" rows="4" placeholder="Describe qué necesitas..."></textarea>
            </div>
            <div class="field">
              <label class="label">Tu dirección</label>
              <input v-model="form.client_address" class="input" placeholder="Calle, colonia" />
            </div>
            <div v-if="success" class="alert-success">¡Reserva creada con éxito!</div>
            <div v-if="error" class="alert-error">{{ error }}</div>
            <button @click="book" class="btn btn-primary" style="width:100%;justify-content:center;" :disabled="loading2">
              {{ loading2 ? 'Enviando...' : `Contratar · $${prof.hourly_rate}/hr` }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from '../../components/AppSidebar.vue'
import { profApi, reviewApi, bookingApi, categoryApi } from '../../api/index.js'

const route = useRoute()
const prof = ref(null)
const reviews = ref([])
const categories = ref([])
const loading = ref(true)
const loading2 = ref(false)
const success = ref(false)
const error = ref('')
const form = ref({ category_id: null, description: '', client_address: '' })

const matchedCategories = computed(() =>
  categories.value.filter(c => prof.value?.categories?.includes(c.name))
)

onMounted(async () => {
  const id = route.params.id
  const [profRes, catsRes] = await Promise.all([profApi.get(id), categoryApi.list()])
  prof.value = profRes.data
  categories.value = catsRes.data
  const revRes = await reviewApi.forProfessional(prof.value.user_id)
  reviews.value = revRes.data
  if (matchedCategories.value.length) form.value.category_id = matchedCategories.value[0].id
  loading.value = false
})

async function book() {
  if (!form.value.category_id) { error.value = 'Selecciona una categoría'; return }
  loading2.value = true
  error.value = ''
  try {
    await bookingApi.create({ professional_id: prof.value.user_id, ...form.value })
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear reserva'
  } finally {
    loading2.value = false
  }
}
</script>

<style scoped>
.loading-state { padding: 40px; text-align: center; color: var(--text2); }
.field { margin-bottom: 14px; }
.review-item { background: var(--bg3); border-radius: 8px; padding: 12px; margin-bottom: 8px; }
.alert-success { background: rgba(16,185,129,0.1); border: 1px solid var(--accent); border-radius: 8px; padding: 10px; color: var(--accent); font-size: 14px; margin-bottom: 10px; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 10px; color: var(--danger); font-size: 14px; margin-bottom: 10px; }
</style>
