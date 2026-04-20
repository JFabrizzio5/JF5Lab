<template>
  <div class="layout">
    <AppSidebar />
    <main class="main">
      <div class="page-header">
        <h1>Patrocinadores</h1>
        <button @click="openModal(null)" class="btn btn-primary">+ Agregar Patrocinador</button>
      </div>

      <div class="tiers-view">
        <div v-for="tier in tiers" :key="tier.key" class="tier-section" v-if="byTier[tier.key]?.length">
          <div class="tier-header" :class="`tier-${tier.key}`">{{ tier.label }}</div>
          <div class="tier-items">
            <div v-for="sp in byTier[tier.key]" :key="sp.id" class="sponsor-card">
              <img :src="sp.logo_url || `https://api.dicebear.com/7.x/initials/svg?seed=${sp.name}`" class="sp-logo" />
              <div class="sp-info">
                <div class="sp-name">{{ sp.name }}</div>
                <div class="sp-website" v-if="sp.website">{{ sp.website }}</div>
                <div class="sp-amount" v-if="sp.amount_sponsored">${{ sp.amount_sponsored.toLocaleString() }} MXN</div>
              </div>
              <div class="sp-actions">
                <button @click="openModal(sp)" class="btn btn-ghost btn-sm">Editar</button>
                <button @click="deleteItem(sp)" class="btn btn-danger btn-sm">✕</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!sponsors.length" class="empty-state card">Sin patrocinadores aún</div>
      </div>

      <!-- Preview -->
      <div class="preview-section" v-if="sponsors.length">
        <h2>Vista previa en la landing</h2>
        <div class="preview-box">
          <div v-for="tier in tiers" :key="tier.key" v-if="byTier[tier.key]?.length" class="preview-tier">
            <div class="preview-tier-label">{{ tier.label }}</div>
            <div class="preview-logos" :class="`size-${tier.size}`">
              <a v-for="sp in byTier[tier.key]" :key="sp.id" :href="sp.website || '#'" target="_blank" class="preview-logo-link">
                <img :src="sp.logo_url || `https://api.dicebear.com/7.x/initials/svg?seed=${sp.name}`" :alt="sp.name" class="preview-logo" />
                <span>{{ sp.name }}</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
        <div class="modal">
          <h2>{{ editing?.id ? 'Editar Patrocinador' : 'Nuevo Patrocinador' }}</h2>
          <div class="form-group"><label>Nombre *</label><input v-model="form.name" /></div>
          <div class="form-group"><label>Logo URL</label><input v-model="form.logo_url" placeholder="https://..." /></div>
          <div class="form-group"><label>Sitio web</label><input v-model="form.website" placeholder="https://..." /></div>
          <div class="form-group"><label>Nivel</label>
            <select v-model="form.tier">
              <option v-for="t in tiers" :key="t.key" :value="t.key">{{ t.label }}</option>
            </select>
          </div>
          <div class="form-group"><label>Monto patrocinado (MXN)</label><input v-model.number="form.amount_sponsored" type="number" /></div>
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
import { ref, computed, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import api from '../../api/index.js'

const conv = ref(null)
const sponsors = ref([])
const showModal = ref(false)
const editing = ref(null)
const form = ref({ name: '', logo_url: '', website: '', tier: 'bronze', amount_sponsored: 0 })

const tiers = [
  { key: 'title', label: 'Título', size: 'xl' },
  { key: 'diamond', label: 'Diamante', size: 'lg' },
  { key: 'platinum', label: 'Platino', size: 'lg' },
  { key: 'gold', label: 'Oro', size: 'md' },
  { key: 'silver', label: 'Plata', size: 'sm' },
  { key: 'bronze', label: 'Bronce', size: 'sm' },
  { key: 'media', label: 'Media Partner', size: 'sm' },
]

const byTier = computed(() => {
  const map = {}
  for (const t of tiers) {
    map[t.key] = sponsors.value.filter(s => s.tier === t.key)
  }
  return map
})

function openModal(sp) {
  editing.value = sp
  if (sp) Object.assign(form.value, { ...sp })
  else form.value = { name: '', logo_url: '', website: '', tier: 'bronze', amount_sponsored: 0 }
  showModal.value = true
}

async function save() {
  const payload = { ...form.value, convention_id: conv.value.id }
  if (editing.value?.id) {
    const { data } = await api.put(`/sponsors/${editing.value.id}`, payload)
    const idx = sponsors.value.findIndex(s => s.id === data.id)
    if (idx >= 0) sponsors.value[idx] = data
  } else {
    const { data } = await api.post('/sponsors/', payload)
    sponsors.value.push(data)
  }
  showModal.value = false
}

async function deleteItem(sp) {
  if (!confirm('¿Eliminar patrocinador?')) return
  await api.delete(`/sponsors/${sp.id}`)
  sponsors.value = sponsors.value.filter(s => s.id !== sp.id)
}

onMounted(async () => {
  conv.value = await api.get('/conventions/my').then(r => r.data)
  sponsors.value = await api.get(`/sponsors/convention/${conv.value.id}`).then(r => r.data)
})
</script>

<style scoped>
.layout { display: flex; }
.main { margin-left: 240px; flex: 1; padding: 32px; max-width: calc(100vw - 240px); }

.tiers-view { display: flex; flex-direction: column; gap: 24px; }
.tier-section { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.tier-header { padding: 12px 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid var(--border); }
.tier-title { color: #ffd700; }
.tier-diamond { color: #b9f2ff; }
.tier-platinum { color: #e5e7eb; }
.tier-gold { color: #f59e0b; }
.tier-silver { color: #94a3b8; }
.tier-bronze { color: #d97706; }
.tier-media { color: var(--text2); }
.tier-items { padding: 12px; display: flex; flex-direction: column; gap: 8px; }
.sponsor-card { display: flex; align-items: center; gap: 14px; padding: 12px; background: var(--bg3); border-radius: 8px; }
.sp-logo { width: 48px; height: 48px; object-fit: contain; border-radius: 8px; background: white; padding: 4px; flex-shrink: 0; }
.sp-info { flex: 1; }
.sp-name { font-weight: 700; }
.sp-website { font-size: 12px; color: var(--primary); }
.sp-amount { font-size: 12px; color: var(--success); }
.sp-actions { display: flex; gap: 8px; }
.empty-state { padding: 40px; text-align: center; color: var(--text2); }

.preview-section { margin-top: 32px; }
.preview-section h2 { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
.preview-box { background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; padding: 32px; }
.preview-tier { margin-bottom: 24px; }
.preview-tier-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--text2); margin-bottom: 12px; }
.preview-logos { display: flex; flex-wrap: wrap; gap: 16px; align-items: center; }
.size-xl .preview-logo { width: 120px; height: 80px; }
.size-lg .preview-logo { width: 90px; height: 60px; }
.size-md .preview-logo { width: 70px; height: 50px; }
.size-sm .preview-logo { width: 55px; height: 40px; }
.preview-logo-link { display: flex; flex-direction: column; align-items: center; gap: 6px; text-decoration: none; color: var(--text2); font-size: 11px; }
.preview-logo { object-fit: contain; border-radius: 8px; background: white; padding: 6px; }
.modal .form-group { margin-top: 12px; }
</style>
