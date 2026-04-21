<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { customersApi } from '../api/endpoints'

const items = ref([]); const loading = ref(false); const error = ref(null)
const q = ref(''); const showForm = ref(false); const saving = ref(false)
const form = ref({ name: '', rfc: '', email: '', phone: '', whatsapp: '', uso_cfdi: 'G03', regimen_fiscal: '612', codigo_postal: '' })

async function load() {
  loading.value = true
  try { const { data } = await customersApi.list(q.value); items.value = data }
  catch (e) { error.value = e.message } finally { loading.value = false }
}
async function submit() {
  saving.value = true
  try {
    const payload = { ...form.value }
    Object.keys(payload).forEach(k => { if (payload[k] === '') payload[k] = null })
    await customersApi.create(payload)
    showForm.value = false
    form.value = { name: '', rfc: '', email: '', phone: '', whatsapp: '', uso_cfdi: 'G03', regimen_fiscal: '612', codigo_postal: '' }
    load()
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { saving.value = false }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="app-top">
      <div>
        <h1 class="page-title">Clientes</h1>
        <p class="page-sub">Tu lista de clientes. Datos fiscales para CFDI.</p>
      </div>
      <button class="btn btn-primary" @click="showForm = true"><i class="mdi mdi-plus"></i> Nuevo cliente</button>
    </div>
    <div style="display:flex; gap: 8px; margin-bottom: 14px; max-width: 400px;">
      <input v-model="q" @input="load" placeholder="Buscar por nombre…" />
    </div>
    <div class="card" style="padding: 0;">
      <table class="table">
        <thead><tr><th>Nombre</th><th>RFC</th><th>Email</th><th>Teléfono</th><th>WhatsApp</th></tr></thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="muted" style="padding: 30px; text-align:center;">Cargando…</td></tr>
          <tr v-else-if="!items.length"><td colspan="5" class="muted" style="padding: 30px; text-align:center;">Sin clientes aún.</td></tr>
          <tr v-for="c in items" :key="c.id">
            <td style="font-weight: 600;">{{ c.name }}</td>
            <td class="mono">{{ c.rfc || '-' }}</td>
            <td class="muted">{{ c.email || '-' }}</td>
            <td class="muted">{{ c.phone || '-' }}</td>
            <td class="muted">{{ c.whatsapp || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showForm" class="modal-back" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-head"><h2>Nuevo cliente</h2><button class="btn btn-ghost btn-sm" @click="showForm = false"><i class="mdi mdi-close"></i></button></div>
        <div class="modal-body">
          <div class="grid-2">
            <div><label>Nombre</label><input v-model="form.name" /></div>
            <div><label>RFC</label><input v-model="form.rfc" /></div>
            <div><label>Email</label><input v-model="form.email" /></div>
            <div><label>Teléfono</label><input v-model="form.phone" /></div>
            <div><label>WhatsApp</label><input v-model="form.whatsapp" /></div>
            <div><label>Código postal</label><input v-model="form.codigo_postal" /></div>
            <div><label>Uso CFDI</label><select v-model="form.uso_cfdi"><option>G01</option><option>G03</option><option>P01</option></select></div>
            <div><label>Régimen fiscal</label><input v-model="form.regimen_fiscal" placeholder="612, 601, 621..." /></div>
          </div>
        </div>
        <div class="modal-foot">
          <button class="btn btn-ghost" @click="showForm = false">Cancelar</button>
          <button class="btn btn-primary" :disabled="saving || !form.name" @click="submit">{{ saving ? 'Guardando…' : 'Crear cliente' }}</button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.modal-back { position: fixed; inset: 0; background: rgba(0,0,0,.5); display: grid; place-items: center; z-index: 100; padding: 20px; }
.modal { background: var(--surface); border-radius: 18px; width: 100%; max-width: 620px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: var(--shadow-lg); }
.modal-head, .modal-foot { padding: 18px 22px; display: flex; justify-content: space-between; align-items: center; }
.modal-head { border-bottom: 1px solid var(--border); }
.modal-head h2 { margin: 0; font-size: 20px; font-weight: 800; }
.modal-body { padding: 18px 22px; overflow-y: auto; }
.modal-foot { border-top: 1px solid var(--border); justify-content: flex-end; gap: 8px; }
</style>
