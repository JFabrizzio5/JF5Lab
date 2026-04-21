<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { productsApi } from '../api/endpoints'

const items = ref([]); const loading = ref(false); const error = ref(null)
const showForm = ref(false); const saving = ref(false)
const form = ref({ sku: '', name: '', description: '', price_mxn: 0, unit: 'servicio', tax_rate: 0.16 })
const peso = (n) => new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN' }).format(n || 0)

async function load() {
  loading.value = true
  try { const { data } = await productsApi.list(); items.value = data }
  catch (e) { error.value = e.message } finally { loading.value = false }
}
async function submit() {
  saving.value = true
  try {
    await productsApi.create({ ...form.value, price_mxn: Number(form.value.price_mxn), tax_rate: Number(form.value.tax_rate) })
    showForm.value = false
    form.value = { sku: '', name: '', description: '', price_mxn: 0, unit: 'servicio', tax_rate: 0.16 }
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
        <h1 class="page-title">Productos y servicios</h1>
        <p class="page-sub">Catálogo para armar notas más rápido.</p>
      </div>
      <button class="btn btn-primary" @click="showForm = true"><i class="mdi mdi-plus"></i> Nuevo producto</button>
    </div>
    <div class="card" style="padding: 0;">
      <table class="table">
        <thead><tr><th>SKU</th><th>Nombre</th><th>Unidad</th><th>Precio</th><th>IVA</th></tr></thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="muted" style="padding: 30px; text-align:center;">Cargando…</td></tr>
          <tr v-else-if="!items.length"><td colspan="5" class="muted" style="padding: 30px; text-align:center;">Sin productos aún.</td></tr>
          <tr v-for="p in items" :key="p.id">
            <td class="mono">{{ p.sku || '-' }}</td>
            <td style="font-weight: 600;">{{ p.name }}<br/><span class="muted" style="font-weight:400;font-size:12px;">{{ p.description }}</span></td>
            <td class="muted">{{ p.unit }}</td>
            <td style="font-weight: 700;">{{ peso(p.price_mxn) }}</td>
            <td class="muted">{{ (p.tax_rate*100).toFixed(0) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showForm" class="modal-back" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-head"><h2>Nuevo producto</h2><button class="btn btn-ghost btn-sm" @click="showForm = false"><i class="mdi mdi-close"></i></button></div>
        <div class="modal-body">
          <div class="grid-2">
            <div><label>SKU</label><input v-model="form.sku" /></div>
            <div><label>Nombre</label><input v-model="form.name" /></div>
            <div style="grid-column: 1/3;"><label>Descripción</label><textarea v-model="form.description" rows="2"></textarea></div>
            <div><label>Precio (MXN)</label><input v-model.number="form.price_mxn" type="number" step="0.01" /></div>
            <div><label>Unidad</label>
              <select v-model="form.unit"><option>servicio</option><option>hora</option><option>pieza</option><option>paquete</option><option>mes</option></select>
            </div>
            <div><label>Tasa IVA</label><input v-model.number="form.tax_rate" type="number" step="0.01" /></div>
          </div>
        </div>
        <div class="modal-foot">
          <button class="btn btn-ghost" @click="showForm = false">Cancelar</button>
          <button class="btn btn-primary" :disabled="saving || !form.name" @click="submit">{{ saving ? 'Guardando…' : 'Crear' }}</button>
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
