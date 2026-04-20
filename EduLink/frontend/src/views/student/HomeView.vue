<template>
  <div>
    <div class="page-header">
      <h1>Explorar Cursos</h1>
      <p>Encuentra el curso perfecto para tu carrera universitaria</p>
    </div>

    <div class="page-content">
      <!-- Filters -->
      <div class="filters">
        <input v-model="search" @input="fetchCourses" type="text" placeholder="🔍 Buscar cursos..." class="search-input" />
        <div class="cat-tabs">
          <button
            v-for="cat in ['Todos', ...categories]"
            :key="cat"
            @click="selectCategory(cat)"
            :class="['cat-btn', selectedCategory === cat ? 'active' : '']"
          >{{ cat }}</button>
        </div>
      </div>

      <div v-if="loading" class="loading">Cargando cursos...</div>

      <div v-else-if="courses.length === 0" class="empty-state">
        <h3>No se encontraron cursos</h3>
        <p>Intenta con otra categoría o término de búsqueda</p>
      </div>

      <div v-else class="grid-3">
        <div v-for="course in courses" :key="course.id" class="course-card" @click="router.push(`/courses/${course.id}`)">
          <div class="course-thumb">
            <img :src="course.thumbnail_url || defaultThumb" :alt="course.title" />
            <span v-if="course.school_restricted" class="thumb-badge restricted">🔒 {{ tutorSchool(course) }}</span>
            <span class="thumb-badge cat-badge">{{ course.category }}</span>
          </div>
          <div class="course-body">
            <h3 class="course-title">{{ course.title }}</h3>
            <div class="course-tutor">
              <img :src="course.tutor?.avatar_url || defaultAvatar" class="tutor-avatar" />
              {{ course.tutor?.name || 'Tutor' }}
              <span class="badge badge-school" style="margin-left:auto">{{ course.tutor?.school }}</span>
            </div>
            <div class="course-meta">
              <div class="stars" v-if="course.avg_rating">
                {{ '★'.repeat(Math.round(course.avg_rating)) }}{{ '☆'.repeat(5 - Math.round(course.avg_rating)) }}
                <span class="rating-num">{{ course.avg_rating }}</span>
                <span class="review-count">({{ course.review_count }})</span>
              </div>
              <div v-else class="no-reviews">Sin reseñas aún</div>
              <div class="lesson-count">📹 {{ course.lesson_count }} lecciones</div>
            </div>
            <div class="course-footer">
              <span v-if="course.price === 0" class="badge badge-free">Gratis</span>
              <span v-else class="badge badge-price">${{ course.price }} MXN</span>
              <button class="btn btn-primary btn-sm" @click.stop="router.push(`/courses/${course.id}`)">Ver Curso</button>
            </div>
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
const courses = ref([])
const loading = ref(false)
const search = ref('')
const selectedCategory = ref('Todos')
const defaultThumb = 'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=400&h=225&fit=crop'
const defaultAvatar = 'https://ui-avatars.com/api/?name=T&background=334155&color=fff'

const categories = ['Matemáticas', 'Física', 'Química', 'Programación', 'Historia', 'Inglés', 'Biología', 'Economía']

function tutorSchool(course) {
  return course.tutor?.school || ''
}

async function fetchCourses() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (selectedCategory.value !== 'Todos') params.category = selectedCategory.value
    const res = await api.get('/courses/', { params })
    courses.value = res.data
  } catch (e) {
    courses.value = []
  } finally {
    loading.value = false
  }
}

function selectCategory(cat) {
  selectedCategory.value = cat
  fetchCourses()
}

onMounted(fetchCourses)
</script>

<style scoped>
.filters { margin-bottom: 24px; }
.search-input {
  width: 100%;
  max-width: 400px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 16px;
  color: var(--text);
  font-size: 14px;
  margin-bottom: 16px;
}
.search-input:focus { outline: none; border-color: var(--primary); }
.search-input::placeholder { color: var(--text2); }

.cat-tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.cat-btn {
  padding: 7px 16px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg2);
  color: var(--text2);
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}
.cat-btn:hover, .cat-btn.active {
  background: var(--primary);
  color: #0f172a;
  border-color: var(--primary);
  font-weight: 600;
}

.course-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}
.course-card:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }

.course-thumb { position: relative; aspect-ratio: 16/9; overflow: hidden; }
.course-thumb img { width: 100%; height: 100%; object-fit: cover; }
.thumb-badge {
  position: absolute;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
}
.restricted { top: 8px; left: 8px; background: rgba(15,23,42,0.85); color: var(--primary); }
.cat-badge { bottom: 8px; right: 8px; background: rgba(15,23,42,0.85); color: var(--text); }

.course-body { padding: 16px; }
.course-title { font-size: 15px; font-weight: 700; margin-bottom: 10px; line-height: 1.3; }

.course-tutor {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text2);
  margin-bottom: 10px;
}
.tutor-avatar { width: 24px; height: 24px; border-radius: 50%; object-fit: cover; }

.course-meta { margin-bottom: 12px; font-size: 12px; }
.stars { color: var(--primary); }
.rating-num { font-weight: 700; color: var(--text); margin-left: 4px; }
.review-count { color: var(--text2); }
.no-reviews { color: var(--text2); }
.lesson-count { color: var(--text2); margin-top: 4px; }

.course-footer { display: flex; align-items: center; justify-content: space-between; }
</style>
