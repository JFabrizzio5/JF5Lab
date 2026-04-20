<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Ponentes</h1>
        <button @click="openModal(null)" class="btn btn-primary">+ Añadir Ponente</button>
      </div>

      <div class="speakers-grid">
        <div v-for="sp in speakers" :key="sp.id" class="speaker-card">
          <div class="keynote-badge" v-if="sp.is_keynote">KEYNOTE</div>
          <img :src="sp.photo_url || `https://api.dicebear.com/7.x/personas/svg?seed=${sp.name}`" class="sp-photo" />
          <div class="sp-name">{{ sp.name }}</div>
          <div class="sp-title" v-if="sp.title">{{ sp.title }}</div>
          <div class="sp-company" v-if="sp.company">{{ sp.company }}</div>
          <div class="sp-twitter" v-if="sp.twitter">{{ sp.twitter }}</div>
          <div class="sp-actions">
            <button @click="openModal(sp)" class="btn btn-ghost btn-sm">Editar</button>
            <button @click="deleteItem(sp)" class="btn btn-danger btn-sm">Eliminar</button>
          </div>
        </div>
        <div v-if="!speakers.length" class="empty-card">Sin ponentes aún</div>
      </div>

      <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
        <div class="modal">
          <h2>{{ editing?.id ? 'Editar Ponente' : 'Nuevo Ponente' }}</h2>
          <div class="form-group"><label>Nombre *</label><input v-model="form.name" /></div>
          <div class="form-group"><label>Título / Cargo</label><input v-model="form.title" placeholder="CEO de X" /></div>
          <div class="form-group"><label>Empresa</label><input v-model="form.company" /></div>
          <div class="form-group"><label>Foto URL</label><input v-model="form.photo_url" placeholder="https://..." /></div>
          <div class="form-group"><label>Twitter</label><input v-model="form.twitter" placeholder="@handle" /></div>
          <div class="form-group"><label>Bio</label><textarea v-model="form.bio" rows="3"></textarea></div>
          <div class="form-group" style="flex-direction:row;align-items:center;gap:10px">
            <input type="checkbox" v-model="form.is_keynote" id="keynote" style="width:auto" />
            <label for="keynote" style="cursor:pointer;color:var(--text)">¿Es Keynote?</label>
          </div>
          <div style="display:flex;gap:10px;margin-top:20px">
            <button @click="showModal = false" class="btn btn-ghost" style="flex:1">Cancelar</button>
            <button @click="save" :disabled="!form.name" class="btn btn-primary" style="flex:1">Guardar</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const speakers = ref([])
const showModal = ref(false)
const editing = ref(null)
const form = ref({ name: '', title: '', company: '', photo_url: '', twitter: '', bio: '', is_keynote: false })

function openModal(sp) {
  editing.value = sp
  if (sp) Object.assign(form.value, { ...sp })
  else form.value = { name: '', title: '', company: '', photo_url: '', twitter: '', bio: '', is_keynote: false }
  showModal.value = true
}

async function save() {
  const payload = { ...form.value, convention_id: conv.value.id }
  if (editing.value?.id) {
    const { data } = await api.put(`/speakers/${editing.value.id}`, payload)
    const idx = speakers.value.findIndex(s => s.id === data.id)
    if (idx >= 0) speakers.value[idx] = data
  } else {
    const { data } = await api.post('/speakers/', payload)
    speakers.value.push(data)
  }
  showModal.value = false
}

async function deleteItem(sp) {
  if (!confirm('¿Eliminar ponente?')) return
  await api.delete(`/speakers/${sp.id}`)
  speakers.value = speakers.value.filter(s => s.id !== sp.id)
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  speakers.value = await api.get(`/speakers/convention/${conv.value.id}`).then(r => r.data)
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }
.speakers-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.speaker-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  text-align: center;
  position: relative;
}
.keynote-badge { position: absolute; top: 10px; right: 10px; background: var(--accent); color: #000; font-size: 9px; font-weight: 800; padding: 2px 8px; border-radius: 4px; letter-spacing: 1px; }
.sp-photo { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin: 0 auto 12px; display: block; border: 2px solid var(--border); }
.sp-name { font-weight: 700; font-size: 15px; margin-bottom: 4px; }
.sp-title { font-size: 12px; color: var(--accent); margin-bottom: 2px; }
.sp-company { font-size: 12px; color: var(--text2); margin-bottom: 2px; }
.sp-twitter { font-size: 11px; color: var(--primary); margin-bottom: 12px; }
.sp-actions { display: flex; gap: 8px; justify-content: center; }
.empty-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 40px; text-align: center; color: var(--text2); grid-column: 1/-1; }
.modal .form-group { margin-top: 12px; }
</style>
