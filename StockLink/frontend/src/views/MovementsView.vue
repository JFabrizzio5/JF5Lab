<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { movementsApi, itemsApi, locationsApi, exportsApi } from '../api/endpoints'

const moves = ref([])
const items = ref([])
const locs = ref([])
const showNew = ref(false)
const form = ref({ item_id: '', kind: 'IN', qty: 1, from_location_id: '', to_location_id: '', reason: '' })
const saveError = ref(null)

async function load() {
  const [m, i, l] = await Promise.all([movementsApi.list({ limit: 500 }), itemsApi.list(), locationsApi.list()])
  moves.value = m.data; items.value = i.data; locs.value = l.data
}
async function create() {
  saveError.value = null
  try {
    const body = { ...form.value }
    if (!body.from_location_id) delete body.from_location_id
    if (!body.to_location_id) delete body.to_location_id
    await movementsApi.create(body)
    showNew.value = false
    form.value = { item_id: '', kind: 'IN', qty: 1, from_location_id: '', to_location_id: '', reason: '' }
    load()
  } catch (e) {
    saveError.value = e?.response?.data?.detail || e.message
  }
}
onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div><h1>Movimientos</h1><p class="muted">Entradas, salidas, traslados, consumos y ajustes.</p></div>
      <div class="actions">
        <button class="btn btn-sm" @click="exportsApi.movements()"><i class="mdi mdi-file-excel"></i> Exportar</button>
        <button class="btn btn-primary btn-sm" @click="showNew=!showNew"><i class="mdi mdi-plus"></i> Nuevo movimiento</button>
      </div>
    </div>

    <div v-if="showNew" class="card" style="margin-bottom:20px;">
      <div class="grid-3">
        <div><label>Artículo *</label>
          <select v-model="form.item_id"><option value="">—</option><option v-for="i in items" :key="i.id" :value="i.id">{{ i.name }} ({{ i.sku }})</option></select>
        </div>
        <div><label>Tipo</label>
          <select v-model="form.kind">
            <option>IN</option><option>OUT</option><option>TRANSFER</option><option>ADJUST</option>
            <option>CONSUME</option><option>RETURN</option><option>RESERVE</option><option>RELEASE</option>
          </select>
        </div>
        <div><label>Cantidad</label><input type="number" step="0.001" v-model.number="form.qty" /></div>
        <div><label>Desde</label>
          <select v-model="form.from_location_id"><option value="">—</option><option v-for="l in locs" :key="l.id" :value="l.id">{{ l.path || l.name }}</option></select>
        </div>
        <div><label>Hacia</label>
          <select v-model="form.to_location_id"><option value="">—</option><option v-for="l in locs" :key="l.id" :value="l.id">{{ l.path || l.name }}</option></select>
        </div>
        <div><label>Motivo</label><input v-model="form.reason" placeholder="Venta, traslado, merma…" /></div>
      </div>
      <div v-if="saveError" class="badge danger" style="margin-top:10px;">{{ saveError }}</div>
      <div style="margin-top:14px; display:flex; gap:8px;">
        <button class="btn btn-primary" :disabled="!form.item_id" @click="create">Registrar</button>
        <button class="btn" @click="showNew=false">Cancelar</button>
      </div>
    </div>

    <div class="card" style="padding:0; overflow:auto;">
      <table class="table">
        <thead><tr><th>Cuándo</th><th>Tipo</th><th>Qty</th><th>Ref</th><th>Motivo</th></tr></thead>
        <tbody>
          <tr v-for="m in moves" :key="m.id">
            <td class="muted">{{ m.occurred_at }}</td>
            <td><span class="badge accent">{{ m.kind }}</span></td>
            <td class="mono">{{ m.qty }}</td>
            <td class="mono muted">{{ m.ref_type || '—' }} {{ m.ref_id || '' }}</td>
            <td>{{ m.reason || '—' }}</td>
          </tr>
          <tr v-if="!moves.length"><td colspan="5" class="muted" style="text-align:center; padding:40px;">Sin movimientos.</td></tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.actions { display: flex; gap: 8px; }
</style>
