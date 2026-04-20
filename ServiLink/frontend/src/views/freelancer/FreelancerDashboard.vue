<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Mi Dashboard</h1>
        <p class="page-subtitle">Gestiona tus solicitudes de servicio</p>
      </div>

      <!-- Quick actions -->
      <div class="quick-actions">
        <a :href="`/pro/${auth.user?.id}`" target="_blank" class="qa-card qa-page">
          <div class="qa-icon">🌐</div>
          <div>
            <div class="qa-title">Ver mi página pública</div>
            <div class="qa-sub">Link que compartes con clientes</div>
          </div>
        </a>
        <router-link to="/my-profile" class="qa-card qa-profile">
          <div class="qa-icon">✏️</div>
          <div>
            <div class="qa-title">Editar perfil</div>
            <div class="qa-sub">Bio, tarifa, categorías, ubicación</div>
          </div>
        </router-link>
        <router-link to="/chats" class="qa-card qa-chat">
          <div class="qa-icon">💬</div>
          <div>
            <div class="qa-title">Mis chats</div>
            <div class="qa-sub">Mensajes de clientes</div>
          </div>
        </router-link>
        <router-link to="/subscriptions" class="qa-card qa-sub">
          <div class="qa-icon">⭐</div>
          <div>
            <div class="qa-title">Suscripción</div>
            <div class="qa-sub">{{ profile?.subscription_plan || 'free' }}</div>
          </div>
        </router-link>
      </div>

      <!-- Stats -->
      <div class="grid-4" style="margin-bottom:28px;">
        <div class="stat-card">
          <div class="stat-value" style="color:var(--warning);">{{ stats.pending }}</div>
          <div class="stat-label">Pendientes</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--primary);">{{ stats.accepted }}</div>
          <div class="stat-label">Aceptadas</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:var(--accent);">{{ stats.completed }}</div>
          <div class="stat-label">Completadas</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color:#f59e0b;">★ {{ profile?.rating_avg || '—' }}</div>
          <div class="stat-label">Rating promedio</div>
        </div>
      </div>

      <!-- Bookings -->
      <div class="card">
        <h2 style="margin-bottom:16px;font-size:18px;">Solicitudes de servicio</h2>
        <div v-if="loading" class="loading-state">Cargando...</div>
        <div v-else-if="bookings.length === 0" class="empty-state">No tienes solicitudes aún</div>
        <table v-else class="table">
          <thead>
            <tr>
              <th>Cliente</th><th>Servicio</th><th>Descripción</th><th>Precio</th><th>Estado</th><th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id">
              <td>
                <div style="display:flex;align-items:center;gap:8px;">
                  <img :src="b.client?.avatar_url" class="avatar" style="width:28px;height:28px;" />
                  {{ b.client?.name }}
                </div>
              </td>
              <td>{{ b.category?.icon }} {{ b.category?.name }}</td>
              <td style="max-width:200px;color:var(--text2);font-size:13px;">{{ b.description || '—' }}</td>
              <td>${{ b.price }}/hr</td>
              <td><span :class="`status-${b.status}`">{{ statusLabel(b.status) }}</span></td>
              <td>
                <div style="display:flex;gap:6px;">
                  <button v-if="b.status === 'pending'" @click="updateStatus(b.id, 'accepted')" class="btn btn-accent btn-sm">Aceptar</button>
                  <button v-if="b.status === 'pending'" @click="updateStatus(b.id, 'cancelled')" class="btn btn-danger btn-sm">Rechazar</button>
                  <button v-if="b.status === 'accepted'" @click="updateStatus(b.id, 'in_progress')" class="btn btn-primary btn-sm">Iniciar</button>
                  <button v-if="b.status === 'in_progress'" @click="updateStatus(b.id, 'completed')" class="btn btn-accent btn-sm">Completar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { bookingApi, profApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'

const auth = useAuthStore()

const bookings = ref([])
const profile = ref(null)
const loading = ref(true)

const stats = computed(() => ({
  pending: bookings.value.filter(b => b.status === 'pending').length,
  accepted: bookings.value.filter(b => b.status === 'accepted').length,
  completed: bookings.value.filter(b => b.status === 'completed').length,
}))

onMounted(async () => {
  const [bookRes] = await Promise.allSettled([
    bookingApi.list(),
    profApi.myProfile().then(r => profile.value = r.data).catch(() => {}),
  ])
  if (bookRes.status === 'fulfilled') bookings.value = bookRes.value.data
  loading.value = false
})

function statusLabel(s) {
  return { pending: '⏳ Pendiente', accepted: '✅ Aceptada', in_progress: '🚀 En progreso', completed: '✓ Completada', cancelled: '✗ Cancelada' }[s] || s
}

async function updateStatus(id, status) {
  await bookingApi.updateStatus(id, status)
  const { data } = await bookingApi.list()
  bookings.value = data
}
</script>

<style scoped>
.loading-state, .empty-state { padding: 32px; text-align: center; color: var(--text2); }

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}
.qa-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: var(--surface);
  cursor: pointer;
  text-decoration: none;
  color: var(--text);
  transition: border-color 0.2s, transform 0.1s;
}
.qa-card:hover { transform: translateY(-2px); }
.qa-page:hover { border-color: #6366f1; }
.qa-profile:hover { border-color: var(--primary); }
.qa-chat:hover { border-color: var(--accent); }
.qa-sub:hover { border-color: #f59e0b; }
.qa-icon { font-size: 24px; flex-shrink: 0; }
.qa-title { font-weight: 600; font-size: 13px; }
.qa-sub { font-size: 11px; color: var(--text2); margin-top: 2px; }
</style>
