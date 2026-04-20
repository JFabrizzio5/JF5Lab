<template>
  <div>
    <div class="page-header">
      <h1>Gestión de Venues</h1>
      <p>Administra todos los salones registrados en la plataforma</p>
    </div>

    <div class="page-body">
      <div v-if="loading" style="color:var(--text2)">Cargando venues...</div>

      <div class="venues-grid" v-else>
        <div v-if="!venues.length" style="color:var(--text2)">No hay venues registrados</div>

        <div v-for="v in venues" :key="v.id" class="venue-card card">
          <div class="venue-cover" :style="v.cover_url ? `background-image:url(${v.cover_url})` : ''">
            <div class="venue-cover-overlay"></div>
            <img v-if="v.logo_url" :src="v.logo_url" :alt="v.name" class="venue-logo" />
          </div>
          <div class="venue-body">
            <div class="venue-top">
              <div>
                <h3>{{ v.name }}</h3>
                <a :href="`/v/${v.slug}`" target="_blank" class="venue-slug">/v/{{ v.slug }}</a>
              </div>
              <span :class="v.is_active ? 'badge-active' : 'badge-inactive'">
                {{ v.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </div>

            <p class="venue-desc">{{ v.tagline || 'Sin descripción' }}</p>

            <div class="venue-meta">
              <span v-if="v.city">📍 {{ v.city }}</span>
              <span v-if="v.stripe_onboarding_complete">💳 Stripe OK</span>
              <span>💰 Fee: {{ v.platform_fee_percent }}%</span>
            </div>

            <div class="venue-actions">
              <a :href="`/v/${v.slug}`" target="_blank" class="btn btn-ghost btn-sm">🌐 Ver landing</a>
              <button @click="toggleVenue(v)" class="btn btn-sm" :class="v.is_active ? 'btn-danger' : 'btn-primary'">
                {{ v.is_active ? 'Desactivar' : 'Activar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/index.js'

const venues = ref([])
const loading = ref(true)

async function loadVenues() {
  loading.value = true
  try {
    const { data } = await api.get('/venues/all')
    venues.value = data
  } finally {
    loading.value = false
  }
}

async function toggleVenue(v) {
  try {
    const { data } = await api.put(`/venues/${v.id}/toggle`)
    const idx = venues.value.findIndex(x => x.id === v.id)
    if (idx >= 0) venues.value[idx] = data
  } catch {
    alert('Error al cambiar estado del venue')
  }
}

onMounted(loadVenues)
</script>

<style scoped>
.venues-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.venue-card { padding: 0; overflow: hidden; }

.venue-cover {
  height: 140px;
  background: var(--bg2);
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}

.venue-cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
}

.venue-logo {
  position: relative;
  z-index: 1;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid rgba(255,255,255,0.2);
}

.venue-body { padding: 1.25rem; }

.venue-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.venue-top h3 { font-size: 1rem; font-weight: 700; }

.venue-slug {
  font-size: 0.75rem;
  color: var(--primary);
  text-decoration: none;
}

.badge-active { background: rgba(16,185,129,.2); color: #34d399; padding: .2rem .6rem; border-radius: 12px; font-size: .75rem; font-weight: 600; }
.badge-inactive { background: rgba(239,68,68,.2); color: #f87171; padding: .2rem .6rem; border-radius: 12px; font-size: .75rem; font-weight: 600; }

.venue-desc {
  font-size: 0.82rem;
  color: var(--text2);
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.venue-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: var(--text2);
  margin-bottom: 1rem;
}

.venue-actions { display: flex; gap: 0.5rem; }
</style>
