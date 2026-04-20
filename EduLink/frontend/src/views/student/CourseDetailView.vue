<template>
  <div v-if="loading" class="loading">Cargando curso...</div>
  <div v-else-if="course">
    <!-- Header -->
    <div class="course-header">
      <button @click="router.back()" class="back-btn">← Volver</button>
      <div class="header-content">
        <div class="header-info">
          <span class="badge badge-school">{{ course.category }}</span>
          <h1>{{ course.title }}</h1>
          <p class="desc">{{ course.description }}</p>
          <div class="header-meta">
            <div class="tutor-row">
              <img :src="course.tutor?.avatar_url || defaultAvatar" class="tutor-img" />
              <div>
                <div class="tutor-name">{{ course.tutor?.name }}</div>
                <div class="tutor-school">{{ course.tutor?.school }}</div>
              </div>
            </div>
            <div class="rating-row" v-if="course.avg_rating">
              <span class="stars">{{ '★'.repeat(Math.round(course.avg_rating)) }}</span>
              <span class="rating-text">{{ course.avg_rating }} ({{ course.review_count }} reseñas)</span>
            </div>
          </div>
          <div class="enroll-area">
            <span v-if="course.price === 0" class="price-badge free">Gratis</span>
            <span v-else class="price-badge paid">${{ course.price }} MXN</span>
            <button v-if="!enrolled" @click="enroll" class="btn btn-primary" :disabled="enrolling">
              {{ enrolling ? 'Inscribiendo...' : 'Inscribirme' }}
            </button>
            <span v-else class="enrolled-badge">✅ Inscrito — {{ enrollProgress }}% completado</span>
          </div>
          <div v-if="enrollError" class="alert alert-error">{{ enrollError }}</div>
        </div>
        <div class="header-thumb">
          <img :src="course.thumbnail_url || defaultThumb" :alt="course.title" />
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="page-content">
      <!-- Video player -->
      <div v-if="activeLesson" class="video-section">
        <div class="video-container">
          <iframe
            :src="activeLesson.video_url"
            allowfullscreen
            frameborder="0"
          ></iframe>
        </div>
        <div class="video-info">
          <h2>{{ activeLesson.title }}</h2>
          <p>{{ activeLesson.description }}</p>
          <span class="duration">⏱ {{ activeLesson.duration_mins }} min</span>
        </div>
      </div>

      <div class="content-grid">
        <!-- Lessons list -->
        <div>
          <h2 class="section-title">Lecciones ({{ lessons.length }})</h2>
          <div class="lessons-list">
            <div
              v-for="lesson in lessons"
              :key="lesson.id"
              @click="activeLesson = lesson"
              :class="['lesson-item', activeLesson?.id === lesson.id ? 'active' : '']"
            >
              <div class="lesson-num">{{ lesson.order }}</div>
              <div class="lesson-body">
                <div class="lesson-title">{{ lesson.title }}</div>
                <div class="lesson-meta">⏱ {{ lesson.duration_mins }} min</div>
              </div>
              <div class="lesson-play">▶</div>
            </div>
          </div>
        </div>

        <!-- Reviews -->
        <div>
          <h2 class="section-title">Reseñas</h2>
          <div v-if="enrolled" class="review-form card">
            <h3>Deja tu reseña</h3>
            <div class="star-select">
              <button
                v-for="n in 5" :key="n"
                @click="reviewForm.rating = n"
                :class="['star-btn', n <= reviewForm.rating ? 'on' : '']"
              >★</button>
            </div>
            <div class="form-group" style="margin-top:10px">
              <textarea v-model="reviewForm.comment" rows="3" placeholder="Tu opinión sobre el curso..."></textarea>
            </div>
            <button @click="submitReview" class="btn btn-accent btn-sm" :disabled="reviewForm.rating === 0">
              Enviar reseña
            </button>
            <span v-if="reviewMsg" class="review-msg">{{ reviewMsg }}</span>
          </div>

          <div v-if="reviews.length === 0" class="empty-state" style="padding:30px 0">
            <p>Sin reseñas aún. ¡Sé el primero!</p>
          </div>
          <div v-else class="reviews-list">
            <div v-for="r in reviews" :key="r.id" class="review-item card">
              <div class="review-header">
                <span class="reviewer-name">{{ r.reviewer_name }}</span>
                <span class="stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
              </div>
              <p class="review-comment">{{ r.comment }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api/index.js'

const route = useRoute()
const router = useRouter()
const course = ref(null)
const lessons = ref([])
const reviews = ref([])
const activeLesson = ref(null)
const loading = ref(true)
const enrolled = ref(false)
const enrollProgress = ref(0)
const enrolling = ref(false)
const enrollError = ref('')
const reviewMsg = ref('')
const defaultThumb = 'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=400&h=225&fit=crop'
const defaultAvatar = 'https://ui-avatars.com/api/?name=T&background=334155&color=fff'

const reviewForm = reactive({ rating: 0, comment: '' })

const courseId = route.params.id

async function fetchAll() {
  loading.value = true
  try {
    const [cRes, lRes, rRes, eRes] = await Promise.all([
      api.get(`/courses/${courseId}`),
      api.get(`/lessons/course/${courseId}`),
      api.get(`/reviews/course/${courseId}`),
      api.get(`/enrollments/check/${courseId}`).catch(() => ({ data: { enrolled: false, progress: 0 } }))
    ])
    course.value = cRes.data
    lessons.value = lRes.data
    reviews.value = rRes.data
    enrolled.value = eRes.data.enrolled
    enrollProgress.value = eRes.data.progress
    if (lessons.value.length > 0) activeLesson.value = lessons.value[0]
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function enroll() {
  enrolling.value = true
  enrollError.value = ''
  try {
    await api.post(`/enrollments/${courseId}`)
    enrolled.value = true
    enrollProgress.value = 0
  } catch (e) {
    enrollError.value = e.response?.data?.detail || 'Error al inscribirse'
  } finally {
    enrolling.value = false
  }
}

async function submitReview() {
  if (reviewForm.rating === 0) return
  try {
    const res = await api.post('/reviews/', {
      course_id: parseInt(courseId),
      rating: reviewForm.rating,
      comment: reviewForm.comment
    })
    reviews.value.unshift(res.data)
    reviewMsg.value = '¡Reseña enviada!'
    reviewForm.rating = 0
    reviewForm.comment = ''
    setTimeout(() => reviewMsg.value = '', 3000)
  } catch (e) {
    reviewMsg.value = e.response?.data?.detail || 'Error al enviar reseña'
  }
}

onMounted(fetchAll)
</script>

<style scoped>
.course-header {
  background: linear-gradient(135deg, var(--bg2), var(--bg));
  border-bottom: 1px solid var(--border);
  padding: 24px 32px;
}
.back-btn {
  background: none;
  border: none;
  color: var(--text2);
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 20px;
  display: block;
}
.back-btn:hover { color: var(--text); }

.header-content { display: grid; grid-template-columns: 1fr 320px; gap: 32px; align-items: start; }
.header-info h1 { font-size: 26px; font-weight: 800; margin: 10px 0; }
.desc { color: var(--text2); font-size: 14px; line-height: 1.6; margin-bottom: 16px; }

.header-meta { display: flex; gap: 20px; align-items: center; margin-bottom: 20px; flex-wrap: wrap; }
.tutor-row { display: flex; align-items: center; gap: 10px; }
.tutor-img { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
.tutor-name { font-weight: 600; font-size: 14px; }
.tutor-school { font-size: 12px; color: var(--text2); }
.rating-row { display: flex; align-items: center; gap: 8px; }
.stars { color: var(--primary); }
.rating-text { font-size: 13px; color: var(--text2); }

.enroll-area { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.price-badge { font-size: 20px; font-weight: 800; }
.price-badge.free { color: var(--accent); }
.price-badge.paid { color: var(--primary); }
.enrolled-badge { font-size: 14px; color: var(--accent); font-weight: 600; }

.header-thumb { border-radius: 12px; overflow: hidden; aspect-ratio: 16/9; }
.header-thumb img { width: 100%; height: 100%; object-fit: cover; }

.video-section { margin-bottom: 32px; }
.video-container {
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 16/9;
  max-width: 800px;
}
.video-container iframe { width: 100%; height: 100%; }
.video-info { padding: 12px 0; }
.video-info h2 { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
.video-info p { color: var(--text2); font-size: 13px; }
.duration { font-size: 12px; color: var(--text2); }

.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.section-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; }

.lessons-list { display: flex; flex-direction: column; gap: 8px; }
.lesson-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}
.lesson-item:hover { border-color: var(--primary); }
.lesson-item.active { border-color: var(--primary); background: rgba(245,158,11,0.08); }
.lesson-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--bg3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
.lesson-body { flex: 1; }
.lesson-title { font-size: 13px; font-weight: 600; }
.lesson-meta { font-size: 11px; color: var(--text2); margin-top: 2px; }
.lesson-play { color: var(--primary); font-size: 14px; }

.review-form h3 { font-size: 15px; font-weight: 700; margin-bottom: 10px; }
.star-select { display: flex; gap: 4px; }
.star-btn {
  font-size: 24px;
  background: none;
  border: none;
  color: var(--bg3);
  cursor: pointer;
  transition: all 0.1s;
  padding: 0;
}
.star-btn.on { color: var(--primary); }
.star-btn:hover { transform: scale(1.2); }
.review-msg { font-size: 13px; color: var(--accent); margin-left: 10px; }

.reviews-list { display: flex; flex-direction: column; gap: 12px; margin-top: 12px; }
.review-item { padding: 14px; }
.review-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.reviewer-name { font-weight: 600; font-size: 13px; }
.review-comment { font-size: 13px; color: var(--text2); line-height: 1.5; }

@media (max-width: 900px) {
  .header-content { grid-template-columns: 1fr; }
  .header-thumb { display: none; }
  .content-grid { grid-template-columns: 1fr; }
}
</style>
