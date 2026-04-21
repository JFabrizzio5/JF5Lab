<script setup>
import { onMounted, ref, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { apiCustomers, apiCreateCustomer } from '../api/endpoints'

const items = ref([])
const loading = ref(true)
const q = ref('')
const showForm = ref(false)
const form = ref({ name: '', phone: '', email: '', whatsapp_optin: true, notes: '' })

async function load() {
  loading.value = true
  items.value = await apiCustomers()
  loading.value = false
}
onMounted(load)

const filtered = computed(() => {
  const qq = q.value.trim().toLowerCase()
  if (!qq) return items.value
  return items.value.filter(c =>
    c.name.toLowerCase().includes(qq) ||
    (c.phone || '').includes(qq) ||
    (c.email || '').toLowerCase().includes(qq)
  )
})

async function submit() {
  try {
    await apiCreateCustomer(form.value)
    showForm.value = false
    form.value = { name: '', phone: '', email: '', whatsapp_optin: true, notes: '' }
    await load()
  } catch (e) { alert(e?.response?.data?.detail || e.message) }
}

function fmtDate(d) { return new Date(d).toLocaleDateString('es-MX', { day:'numeric', month:'short', year:'numeric' }) }
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1 class="page-title">Clientes</h1>
        <p class="page-subtitle">{{ items.length }} personas en tu cartera.</p>
      </div>
      <div class="row">
        <input v-model="q" placeholder="Buscar por nombre, teléfono, email..." style="width:280px;">
        <button class="btn btn-primary" @click="showForm = true">
          <i class="mdi mdi-plus"></i> Nuevo cliente
        </button>
      </div>
    </div>

    <div v-if="loading" class="muted">Cargando...</div>
    <table v-else class="table">
      <thead><tr><th>Cliente</th><th>Contacto</th><th>WhatsApp</th><th>Visitas</th><th>No-shows</th><th>Desde</th></tr></thead>
      <tbody>
        <tr v-for="c in filtered" :key="c.id">
          <td>
            <div style="font-weight:600;color:var(--navy);">{{ c.name }}</div>
          </td>
          <td>
            <div style="font-size:13px;">{{ c.phone || '—' }}</div>
            <div class="muted" style="font-size:12px;">{{ c.email || '' }}</div>
          </td>
          <td>
            <i v-if="c.whatsapp_optin" class="mdi mdi-whatsapp" style="color:var(--success);font-size:20px;"></i>
            <i v-else class="mdi mdi-close-circle-outline" style="color:var(--muted);"></i>
          </td>
          <td><strong>{{ c.total_visits }}</strong></td>
          <td>
            <span v-if="c.no_show_count > 0" class="chip chip-danger">{{ c.no_show_count }}</span>
            <span v-else class="muted">0</span>
          </td>
          <td class="muted">{{ fmtDate(c.created_at) }}</td>
        </tr>
        <tr v-if="!filtered.length"><td colspan="6" class="muted" style="text-align:center;padding:40px 0;">Sin clientes.</td></tr>
      </tbody>
    </table>

    <div v-if="showForm" class="modal-bg" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-head">
          <h3 class="serif" style="font-weight:600;margin:0;color:var(--navy);">Nuevo cliente</h3>
          <button class="btn btn-ghost btn-sm" @click="showForm = false"><i class="mdi mdi-close"></i></button>
        </div>
        <form @submit.prevent="submit" class="modal-body">
          <label>Nombre</label><input v-model="form.name" required>
          <label>Teléfono (incluye lada)</label><input v-model="form.phone" placeholder="+525555123456">
          <label>Email</label><input v-model="form.email" type="email">
          <label class="chk">
            <input type="checkbox" v-model="form.whatsapp_optin" style="width:auto;"> Acepta WhatsApp
          </label>
          <label>Notas</label><textarea v-model="form.notes" rows="2"></textarea>
          <div style="display:flex;gap:10px;margin-top:12px;">
            <button type="submit" class="btn btn-primary">Crear</button>
            <button type="button" class="btn btn-ghost" @click="showForm = false">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.modal-bg {
  position: fixed; inset: 0; background: rgba(12,25,51,0.55);
  display: grid; place-items: center; z-index: 95; padding: 20px;
}
.modal {
  background: var(--surface); border-radius: var(--radius);
  padding: 0; max-width: 480px; width: 100%;
  box-shadow: var(--shadow-lg);
}
.modal-head {
  padding: 20px 24px; border-bottom: 1px solid var(--line-soft);
  display: flex; justify-content: space-between; align-items: center;
}
.modal-body { padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; }
label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
.chk { display:flex; gap:8px; align-items:center; font-size:14px; color: var(--text); text-transform:none; letter-spacing:0; font-weight:500; margin-top:6px; }
</style>
