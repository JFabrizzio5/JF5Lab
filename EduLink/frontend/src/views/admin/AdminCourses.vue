<template>
  <div>
    <div class="page-header">
      <h1>Gestión de Cursos</h1>
      <p>Revisa y modera todos los cursos de la plataforma</p>
    </div>

    <div class="page-content">
      <div class="toolbar">
        <input v-model="search" type="text" placeholder="🔍 Buscar cursos..." class="search-input" />
        <select v-model="filterCat" class="filter-select">
          <option value="">Todas las categorías</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Cargando cursos...</div>
      <div v-else class="table-wrapper card" style="padding:0;overflow:hidden">
        <table>
          <thead>
            <tr>
              <th>Curso</th>
              <th>Categoría</th>
              <th>Precio</th>
              <th>Restricción</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in filteredCourses" :key="c.id">
              <td style="font-weight:600;max-width:220px">{{ c.title }}</td>
              <td><span class="badge badge-school">{{ c.category }}</span></td>
              <td>
                <span v-if="c.price === 0" class="badge badge-free">Gratis</span>
                <span v-else class="badge badge-price">${{ c.price }} MXN</span>
              </td>
              <td>
                <span v-if="c.school_restricted" class="restricted-badge">🔒 Escuela</span>
                <span v-else class="public-badge">🌐 Público</span>
              </td>
              <td>
                <span :class="['pub-badge', c.is_published ? 'published' : 'hidden']">
                  {{ c.is_published ? '● Publicado' : '● Oculto' }}
                </span>
              </td>
              <td>
                <button @click="toggleCourse(c)" class="btn btn-ghost btn-sm">
                  {{ c.is_published ? 'Ocultar' : 'Publicar' }}
                </button>
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
import api from '../../api/index.js'

const courses = ref([])
const loading = ref(true)
const search = ref('')
const filterCat = ref('')

const categories = ['Matemáticas', 'Física', 'Química', 'Programación', 'Historia', 'Inglés', 'Biología', 'Economía']

const filteredCourses = computed(() => {
  return courses.value.filter(c => {
    const q = search.value.toLowerCase()
    const matchSearch = !q || c.title.toLowerCase().includes(q)
    const matchCat = !filterCat.value || c.category === filterCat.value
    return matchSearch && matchCat
  })
})

async function fetchCourses() {
  loading.value = true
  try {
    const res = await api.get('/admin/courses')
    courses.value = res.data
  } finally {
    loading.value = false
  }
}

async function toggleCourse(course) {
  const res = await api.put(`/admin/courses/${course.id}/toggle`)
  course.is_published = res.data.is_published
}

onMounted(fetchCourses)
</script>

<style scoped>
.toolbar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.search-input {
  flex: 1;
  min-width: 200px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
}
.search-input:focus { outline: none; border-color: var(--primary); }
.filter-select {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
}
.filter-select:focus { outline: none; border-color: var(--primary); }

.restricted-badge { font-size: 12px; color: var(--primary); }
.public-badge { font-size: 12px; color: var(--text2); }

.pub-badge { font-size: 12px; font-weight: 600; }
.pub-badge.published { color: var(--accent); }
.pub-badge.hidden { color: #f87171; }
</style>
