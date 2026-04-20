<template>
  <div>
    <div class="page-header">
      <h1>Mis Cursos</h1>
      <p>Continúa aprendiendo desde donde lo dejaste</p>
    </div>
    <div class="page-content">
      <div v-if="loading" class="loading">Cargando tus cursos...</div>
      <div v-else-if="enrollments.length === 0" class="empty-state">
        <h3>Aún no estás inscrito en ningún curso</h3>
        <p style="margin-bottom:20px">Explora el catálogo y encuentra el curso perfecto</p>
        <RouterLink to="/courses" class="btn btn-primary">Explorar Cursos</RouterLink>
      </div>
      <div v-else class="grid-3">
        <div v-for="e in enrollments" :key="e.id" class="enroll-card" @click="router.push(`/courses/${e.course_id}`)">
          <div class="enroll-thumb">
            <img :src="e.thumbnail_url || defaultThumb" :alt="e.title" />
          </div>
          <div class="enroll-body">
            <span class="badge badge-school" style="margin-bottom:8px">{{ e.category }}</span>
            <h3>{{ e.title }}</h3>
            <p class="tutor-text">👨‍🏫 {{ e.tutor_name }}</p>
            <div class="progress-section">
              <div class="prog-header">
                <span>Progreso</span>
                <span class="prog-pct">{{ e.progress }}%</span>
              </div>
              <div class="prog-bar">
                <div class="prog-fill" :style="{ width: e.progress + '%' }"></div>
              </div>
            </div>
            <div class="enrolled-date">Inscrito: {{ formatDate(e.enrolled_at) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api/index.js'

const router = useRouter()
const enrollments = ref([])
const loading = ref(true)
const defaultThumb = 'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=400&h=225&fit=crop'

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' })
}

async function fetchEnrollments() {
  try {
    const res = await api.get('/enrollments/my')
    enrollments.value = res.data
  } catch (e) {
    enrollments.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchEnrollments)
</script>

<style scoped>
.enroll-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}
.enroll-card:hover { border-color: var(--primary); transform: translateY(-2px); }
.enroll-thumb { aspect-ratio: 16/9; overflow: hidden; }
.enroll-thumb img { width: 100%; height: 100%; object-fit: cover; }
.enroll-body { padding: 16px; }
.enroll-body h3 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
.tutor-text { font-size: 13px; color: var(--text2); margin-bottom: 14px; }

.progress-section { margin-bottom: 10px; }
.prog-header { display: flex; justify-content: space-between; font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.prog-pct { font-weight: 700; color: var(--primary); }
.prog-bar { height: 6px; background: var(--bg3); border-radius: 3px; }
.prog-fill { height: 100%; background: var(--primary); border-radius: 3px; transition: width 0.3s; }

.enrolled-date { font-size: 11px; color: var(--text2); }
</style>
