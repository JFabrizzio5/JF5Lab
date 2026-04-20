<template>
  <div>
    <div class="page-header">
      <h1>Dashboard del Tutor</h1>
      <p>Bienvenido, {{ user?.name }}</p>
    </div>

    <div class="page-content">
      <!-- Stats -->
      <div class="stats-row" style="margin-bottom:32px">
        <div class="stat-card">
          <div class="stat-number">{{ stats.courses }}</div>
          <div class="stat-label">Cursos publicados</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.students }}</div>
          <div class="stat-label">Estudiantes</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.bookings }}</div>
          <div class="stat-label">Sesiones</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.slots }}</div>
          <div class="stat-label">Horarios activos</div>
        </div>
      </div>

      <!-- My courses preview -->
      <div style="margin-bottom:32px">
        <div class="section-header">
          <h2>Mis Cursos</h2>
          <RouterLink to="/tutor/courses" class="btn btn-ghost btn-sm">Ver todos →</RouterLink>
        </div>
        <div v-if="courses.length === 0" class="empty-state" style="padding:30px 0">
          <p>No tienes cursos aún</p>
          <RouterLink to="/tutor/courses" class="btn btn-primary" style="margin-top:12px">Crear primer curso</RouterLink>
        </div>
        <div v-else class="grid-3">
          <div v-for="c in courses.slice(0,3)" :key="c.id" class="mini-course-card">
            <div class="mini-thumb">
              <img :src="c.thumbnail_url || defaultThumb" :alt="c.title" />
            </div>
            <div class="mini-body">
              <div class="mini-title">{{ c.title }}</div>
              <div class="mini-meta">{{ c.category }} · {{ c.lesson_count }} lecciones</div>
              <div class="mini-price">{{ c.price === 0 ? 'Gratis' : '$' + c.price + ' MXN' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming bookings -->
      <div>
        <div class="section-header">
          <h2>Próximas Sesiones</h2>
          <RouterLink to="/tutor/schedule" class="btn btn-ghost btn-sm">Gestionar →</RouterLink>
        </div>
        <div v-if="bookings.length === 0" class="empty-state" style="padding:30px 0">
          <p>No tienes sesiones pendientes</p>
        </div>
        <div v-else class="booking-grid">
          <div v-for="b in bookings.slice(0,4)" :key="b.id" class="booking-card">
            <div class="bk-header">
              <span class="bk-date">📅 {{ b.date }}</span>
              <span :class="['status-badge', `status-${b.status}`]">{{ statusLabel(b.status) }}</span>
            </div>
            <div class="bk-student">👩‍🎓 {{ b.student_name }}</div>
            <div class="bk-time">🕐 {{ b.slot_start }} - {{ b.slot_end }}</div>
            <div v-if="b.subject" class="bk-subject">📚 {{ b.subject }}</div>
            <div v-if="b.status === 'pending'" class="bk-actions">
              <button @click="updateStatus(b.id, 'confirmed')" class="btn btn-accent btn-sm">Confirmar</button>
              <button @click="updateStatus(b.id, 'cancelled')" class="btn btn-danger btn-sm">Cancelar</button>
            </div>
            <div v-if="b.status === 'confirmed'" class="bk-actions">
              <button @click="updateStatus(b.id, 'completed')" class="btn btn-ghost btn-sm">Marcar completada</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth.js'
import api from '../../api/index.js'

const auth = useAuthStore()
const user = computed(() => auth.user)
const courses = ref([])
const bookings = ref([])
const defaultThumb = 'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=400&h=225&fit=crop'

const stats = ref({ courses: 0, students: 0, bookings: 0, slots: 0 })

function statusLabel(s) {
  const map = { pending: 'Pendiente', confirmed: 'Confirmada', cancelled: 'Cancelada', completed: 'Completada' }
  return map[s] || s
}

async function fetchData() {
  const [cRes, bRes, sRes] = await Promise.all([
    api.get('/courses/my'),
    api.get('/schedule/bookings/my'),
    api.get('/schedule/slots/my')
  ])
  courses.value = cRes.data
  bookings.value = bRes.data
  const activeSlots = sRes.data.filter(s => s.is_available)
  stats.value = {
    courses: cRes.data.length,
    students: 0,
    bookings: bRes.data.length,
    slots: activeSlots.length
  }
}

async function updateStatus(bookingId, status) {
  await api.put(`/schedule/bookings/${bookingId}/status`, { status })
  await fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.section-header h2 { font-size: 18px; font-weight: 700; }

.mini-course-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}
.mini-thumb { aspect-ratio: 16/9; overflow: hidden; }
.mini-thumb img { width: 100%; height: 100%; object-fit: cover; }
.mini-body { padding: 12px; }
.mini-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.mini-meta { font-size: 12px; color: var(--text2); margin-bottom: 4px; }
.mini-price { font-size: 13px; font-weight: 700; color: var(--primary); }

.booking-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }
.booking-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.bk-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.bk-date { font-size: 13px; font-weight: 600; }
.bk-student, .bk-time, .bk-subject { font-size: 13px; color: var(--text2); margin-bottom: 4px; }
.bk-actions { display: flex; gap: 8px; margin-top: 10px; }

.status-badge { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 12px; }
.status-pending { background: rgba(245,158,11,0.2); color: var(--primary); }
.status-confirmed { background: rgba(16,185,129,0.2); color: var(--accent); }
.status-cancelled { background: rgba(239,68,68,0.2); color: #f87171; }
.status-completed { background: rgba(99,102,241,0.2); color: #818cf8; }

@media (max-width: 900px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
}
</style>
