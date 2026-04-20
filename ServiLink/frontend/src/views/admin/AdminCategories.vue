<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header" style="display:flex;align-items:center;justify-content:space-between;">
        <div>
          <h1 class="page-title">Categorías</h1>
          <p class="page-subtitle">{{ categories.length }} categorías activas</p>
        </div>
        <button @click="openCreate" class="btn btn-primary">+ Nueva categoría</button>
      </div>

      <div class="cats-grid">
        <div v-for="c in categories" :key="c.id" class="cat-card card">
          <div class="cat-icon">{{ c.icon }}</div>
          <div class="cat-name">{{ c.name }}</div>
          <div class="cat-desc">{{ c.description }}</div>
          <div style="display:flex;gap:6px;margin-top:12px;">
            <button @click="openEdit(c)" class="btn btn-secondary btn-sm" style="flex:1;justify-content:center;">Editar</button>
            <button @click="deleteCategory(c.id)" class="btn btn-danger btn-sm">🗑</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="modal" class="modal-overlay" @click.self="modal = null">
    <div class="modal-sm">
      <h2 style="margin-bottom:20px;">{{ editId ? 'Editar' : 'Nueva' }} categoría</h2>
      <div class="field"><label class="label">Emoji / Ícono</label><input v-model="form.icon" class="input" placeholder="🔧" /></div>
      <div class="field"><label class="label">Nombre</label><input v-model="form.name" class="input" placeholder="Plomería" /></div>
      <div class="field"><label class="label">Descripción</label><textarea v-model="form.description" class="input" rows="3"></textarea></div>
      <div style="display:flex;gap:8px;margin-top:16px;">
        <button @click="modal = null" class="btn btn-secondary" style="flex:1;justify-content:center;">Cancelar</button>
        <button @click="saveCategory" class="btn btn-primary" style="flex:1;justify-content:center;" :disabled="saving">
          {{ saving ? 'Guardando...' : 'Guardar' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { categoryApi } from '../../api/index.js'

const categories = ref([])
const modal = ref(false)
const editId = ref(null)
const saving = ref(false)
const form = ref({ name: '', icon: '🔧', description: '' })

onMounted(load)
async function load() {
  const { data } = await categoryApi.list()
  categories.value = data
}

function openCreate() { editId.value = null; form.value = { name: '', icon: '🔧', description: '' }; modal.value = true }
function openEdit(c) { editId.value = c.id; form.value = { name: c.name, icon: c.icon, description: c.description || '' }; modal.value = true }

async function saveCategory() {
  saving.value = true
  try {
    if (editId.value) await categoryApi.update(editId.value, form.value)
    else await categoryApi.create(form.value)
    modal.value = false
    await load()
  } finally {
    saving.value = false
  }
}

async function deleteCategory(id) {
  if (!confirm('¿Eliminar esta categoría?')) return
  await categoryApi.delete(id)
  await load()
}
</script>

<style scoped>
.cats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.cat-card { text-align: center; }
.cat-icon { font-size: 40px; margin-bottom: 8px; }
.cat-name { font-size: 16px; font-weight: 600; }
.cat-desc { font-size: 13px; color: var(--text2); margin-top: 4px; }
.field { margin-bottom: 14px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-sm { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 32px; width: 100%; max-width: 400px; }
</style>
