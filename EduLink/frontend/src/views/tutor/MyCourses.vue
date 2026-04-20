<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Mis Cursos</h1>
        <p>Crea y gestiona tu contenido educativo</p>
      </div>
      <button @click="showCreateModal = true" class="btn btn-primary">+ Nuevo Curso</button>
    </div>

    <div class="page-content">
      <div v-if="loading" class="loading">Cargando cursos...</div>
      <div v-else-if="courses.length === 0" class="empty-state">
        <h3>No tienes cursos aún</h3>
        <p style="margin-bottom:16px">Crea tu primer curso y comparte tu conocimiento</p>
        <button @click="showCreateModal = true" class="btn btn-primary">Crear Primer Curso</button>
      </div>
      <div v-else class="courses-list">
        <div v-for="course in courses" :key="course.id" class="course-row">
          <div class="course-thumb-sm">
            <img :src="course.thumbnail_url || defaultThumb" :alt="course.title" />
          </div>
          <div class="course-info">
            <h3>{{ course.title }}</h3>
            <div class="course-tags">
              <span class="badge badge-school">{{ course.category }}</span>
              <span class="badge" :class="course.price === 0 ? 'badge-free' : 'badge-price'">
                {{ course.price === 0 ? 'Gratis' : '$' + course.price + ' MXN' }}
              </span>
              <span v-if="course.school_restricted" class="badge" style="background:rgba(99,102,241,0.2);color:#818cf8;border:1px solid rgba(99,102,241,0.4)">🔒 Restringido</span>
              <span class="badge" :class="course.is_published ? 'badge-free' : ''" style="background:rgba(100,100,100,0.2);color:#888" v-if="!course.is_published">Oculto</span>
            </div>
            <div class="course-stats">
              <span>📹 {{ course.lesson_count }} lecciones</span>
              <span v-if="course.avg_rating">⭐ {{ course.avg_rating }}</span>
            </div>
          </div>
          <div class="course-actions">
            <button @click="openLessons(course)" class="btn btn-ghost btn-sm">📹 Lecciones</button>
            <button @click="openEdit(course)" class="btn btn-ghost btn-sm">✏️ Editar</button>
            <button @click="deleteCourse(course.id)" class="btn btn-danger btn-sm">🗑️</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || editingCourse" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ editingCourse ? 'Editar Curso' : 'Nuevo Curso' }}</h2>
        <div class="form-group">
          <label>Título *</label>
          <input v-model="courseForm.title" type="text" placeholder="Nombre del curso" />
        </div>
        <div class="form-group">
          <label>Descripción</label>
          <textarea v-model="courseForm.description" rows="3" placeholder="Describe el contenido del curso..."></textarea>
        </div>
        <div class="form-group">
          <label>Categoría *</label>
          <select v-model="courseForm.category">
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>URL de miniatura</label>
          <input v-model="courseForm.thumbnail_url" type="text" placeholder="https://..." />
        </div>
        <div class="form-group">
          <label>Precio (0 = Gratis)</label>
          <input v-model.number="courseForm.price" type="number" min="0" step="10" />
        </div>
        <div class="form-group" style="display:flex;align-items:center;gap:10px">
          <input v-model="courseForm.school_restricted" type="checkbox" id="restricted" />
          <label for="restricted" style="margin-bottom:0">Solo para mi universidad</label>
        </div>
        <div v-if="formError" class="alert alert-error">{{ formError }}</div>
        <div style="display:flex;gap:10px;margin-top:8px">
          <button @click="saveCourse" class="btn btn-primary" :disabled="formLoading">
            {{ formLoading ? 'Guardando...' : (editingCourse ? 'Actualizar' : 'Crear Curso') }}
          </button>
          <button @click="closeModal" class="btn btn-ghost">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Lessons Modal -->
    <div v-if="managingCourse" class="modal-overlay" @click.self="managingCourse = null">
      <div class="modal" style="max-width:600px">
        <h2>Lecciones: {{ managingCourse.title }}</h2>
        <div class="lessons-manager">
          <div v-for="l in managingLessons" :key="l.id" class="lesson-row">
            <span class="lesson-ord">{{ l.order }}</span>
            <div class="lesson-txt">
              <div class="lesson-title-sm">{{ l.title }}</div>
              <div class="lesson-url">{{ l.video_url }}</div>
            </div>
            <button @click="deleteLesson(l.id)" class="btn btn-danger btn-sm">🗑️</button>
          </div>
        </div>

        <h3 style="margin-top:20px;margin-bottom:14px;font-size:15px">Agregar Lección</h3>
        <div class="form-group">
          <label>Título</label>
          <input v-model="lessonForm.title" type="text" placeholder="Título de la lección" />
        </div>
        <div class="form-group">
          <label>URL de video (YouTube embed)</label>
          <input v-model="lessonForm.video_url" type="text" placeholder="https://www.youtube.com/embed/ID" />
        </div>
        <div class="form-group">
          <label>Descripción</label>
          <input v-model="lessonForm.description" type="text" placeholder="Breve descripción" />
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div class="form-group">
            <label>Orden</label>
            <input v-model.number="lessonForm.order" type="number" min="1" />
          </div>
          <div class="form-group">
            <label>Duración (min)</label>
            <input v-model.number="lessonForm.duration_mins" type="number" min="0" />
          </div>
        </div>
        <div style="display:flex;gap:10px">
          <button @click="addLesson" class="btn btn-primary" :disabled="lessonLoading">
            {{ lessonLoading ? 'Agregando...' : 'Agregar Lección' }}
          </button>
          <button @click="managingCourse = null" class="btn btn-ghost">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../../api/index.js'

const courses = ref([])
const loading = ref(true)
const showCreateModal = ref(false)
const editingCourse = ref(null)
const managingCourse = ref(null)
const managingLessons = ref([])
const formLoading = ref(false)
const lessonLoading = ref(false)
const formError = ref('')
const defaultThumb = 'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=400&h=225&fit=crop'

const categories = ['Matemáticas', 'Física', 'Química', 'Programación', 'Historia', 'Inglés', 'Biología', 'Economía', 'Arte', 'Música']

const courseForm = reactive({
  title: '', description: '', category: 'Matemáticas',
  thumbnail_url: '', price: 0, school_restricted: false
})

const lessonForm = reactive({
  title: '', video_url: '', description: '', order: 1, duration_mins: 0
})

async function fetchCourses() {
  loading.value = true
  try {
    const res = await api.get('/courses/my')
    courses.value = res.data
  } finally {
    loading.value = false
  }
}

function openEdit(course) {
  editingCourse.value = course
  courseForm.title = course.title
  courseForm.description = course.description || ''
  courseForm.category = course.category
  courseForm.thumbnail_url = course.thumbnail_url || ''
  courseForm.price = course.price
  courseForm.school_restricted = course.school_restricted
}

function closeModal() {
  showCreateModal.value = false
  editingCourse.value = null
  Object.assign(courseForm, { title: '', description: '', category: 'Matemáticas', thumbnail_url: '', price: 0, school_restricted: false })
  formError.value = ''
}

async function saveCourse() {
  if (!courseForm.title) { formError.value = 'El título es obligatorio'; return }
  formLoading.value = true
  formError.value = ''
  try {
    if (editingCourse.value) {
      await api.put(`/courses/${editingCourse.value.id}`, courseForm)
    } else {
      await api.post('/courses/', courseForm)
    }
    closeModal()
    await fetchCourses()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Error al guardar'
  } finally {
    formLoading.value = false
  }
}

async function deleteCourse(id) {
  if (!confirm('¿Eliminar este curso?')) return
  await api.delete(`/courses/${id}`)
  await fetchCourses()
}

async function openLessons(course) {
  managingCourse.value = course
  const res = await api.get(`/lessons/course/${course.id}`)
  managingLessons.value = res.data
  lessonForm.order = res.data.length + 1
}

async function addLesson() {
  if (!lessonForm.title) return
  lessonLoading.value = true
  try {
    await api.post(`/lessons/course/${managingCourse.value.id}`, lessonForm)
    const res = await api.get(`/lessons/course/${managingCourse.value.id}`)
    managingLessons.value = res.data
    lessonForm.title = ''
    lessonForm.video_url = ''
    lessonForm.description = ''
    lessonForm.order = managingLessons.value.length + 1
    lessonForm.duration_mins = 0
    await fetchCourses()
  } finally {
    lessonLoading.value = false
  }
}

async function deleteLesson(id) {
  await api.delete(`/lessons/${id}`)
  managingLessons.value = managingLessons.value.filter(l => l.id !== id)
}

onMounted(fetchCourses)
</script>

<style scoped>
.courses-list { display: flex; flex-direction: column; gap: 12px; }
.course-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px;
}
.course-thumb-sm { width: 80px; height: 50px; border-radius: 8px; overflow: hidden; flex-shrink: 0; }
.course-thumb-sm img { width: 100%; height: 100%; object-fit: cover; }
.course-info { flex: 1; }
.course-info h3 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
.course-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 6px; }
.course-stats { font-size: 12px; color: var(--text2); display: flex; gap: 12px; }
.course-actions { display: flex; gap: 8px; flex-shrink: 0; }

.lessons-manager { display: flex; flex-direction: column; gap: 8px; max-height: 200px; overflow-y: auto; }
.lesson-row { display: flex; align-items: center; gap: 10px; background: var(--bg3); border-radius: 8px; padding: 10px; }
.lesson-ord { font-size: 14px; font-weight: 700; color: var(--primary); width: 24px; text-align: center; }
.lesson-txt { flex: 1; }
.lesson-title-sm { font-size: 13px; font-weight: 600; }
.lesson-url { font-size: 11px; color: var(--text2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
