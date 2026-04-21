<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { apiServices, apiCreateService, apiStaff } from '../api/endpoints'

const items = ref([])
const staff = ref([])
const loading = ref(true)
const showForm = ref(false)
const form = ref({
  name: '', description: '', category: '',
  duration_minutes: 30, buffer_minutes: 5,
  price_mxn: 0, deposit_mxn: 0,
  requires_prepay: false, color: '#0c1933',
  staff_ids: [],
})

const colors = ['#0c1933', '#1e40af', '#b6892b', '#0891b2', '#059669', '#7c3aed', '#ef4444', '#f59e0b']

function fmtMoney(n) { return '$' + Number(n||0).toLocaleString('es-MX') }

async function load() {
  loading.value = true
  const [s, st] = await Promise.all([apiServices(), apiStaff()])
  items.value = s; staff.value = st
  loading.value = false
}
onMounted(load)

async function submit() {
  try {
    await apiCreateService(form.value)
    showForm.value = false
    form.value = { name: '', description: '', category: '', duration_minutes: 30, buffer_minutes: 5, price_mxn: 0, deposit_mxn: 0, requires_prepay: false, color: '#0c1933', staff_ids: [] }
    await load()
  } catch (e) { alert(e?.response?.data?.detail || e.message) }
}

function toggleStaff(sid) {
  const i = form.value.staff_ids.indexOf(sid)
  if (i >= 0) form.value.staff_ids.splice(i, 1)
  else form.value.staff_ids.push(sid)
}
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1 class="page-title">Servicios</h1>
        <p class="page-subtitle">Lo que cobras: duración, precio, depósito y color.</p>
      </div>
      <button class="btn btn-primary" @click="showForm = true">
        <i class="mdi mdi-plus"></i> Nuevo servicio
      </button>
    </div>

    <div v-if="loading" class="muted">Cargando...</div>
    <div v-else class="grid-3">
      <div v-for="s in items" :key="s.id" class="svc-card" :style="{ '--svc-color': s.color }">
        <div class="svc-head">
          <div class="svc-name">{{ s.name }}</div>
          <span class="chip" style="background:transparent;">{{ s.duration_minutes }} min</span>
        </div>
        <div class="svc-price">{{ fmtMoney(s.price_mxn) }}</div>
        <div v-if="s.deposit_mxn > 0" class="muted" style="font-size:12px;">
          Depósito: {{ fmtMoney(s.deposit_mxn) }}
        </div>
        <div class="muted" style="font-size:12px;margin-top:6px;" v-if="s.category">
          {{ s.category }}
        </div>
        <div class="svc-flags">
          <span v-if="s.requires_prepay" class="chip chip-gold">Requiere depósito</span>
        </div>
      </div>
      <div v-if="!items.length" class="muted" style="grid-column: 1/-1; text-align:center; padding:48px 0;">
        Aún no hay servicios. Crea el primero.
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showForm" class="modal-bg" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-head">
          <h3 class="serif" style="font-weight:600;margin:0;color:var(--navy);">Nuevo servicio</h3>
          <button class="btn btn-ghost btn-sm" @click="showForm = false"><i class="mdi mdi-close"></i></button>
        </div>
        <form @submit.prevent="submit" class="modal-body">
          <label>Nombre</label>
          <input v-model="form.name" required placeholder="Corte + Barba">
          <div class="grid-2">
            <div>
              <label>Duración (min)</label>
              <input type="number" v-model.number="form.duration_minutes" required>
            </div>
            <div>
              <label>Buffer (min)</label>
              <input type="number" v-model.number="form.buffer_minutes">
            </div>
          </div>
          <div class="grid-2">
            <div>
              <label>Precio MXN</label>
              <input type="number" step="0.01" v-model.number="form.price_mxn" required>
            </div>
            <div>
              <label>Depósito MXN</label>
              <input type="number" step="0.01" v-model.number="form.deposit_mxn">
            </div>
          </div>
          <label>Categoría</label>
          <input v-model="form.category" placeholder="clásico, combo, color">
          <label>Descripción</label>
          <textarea v-model="form.description" rows="2"></textarea>

          <label>Color</label>
          <div class="color-picker">
            <button v-for="c in colors" :key="c" type="button"
                    :class="['color-swatch', { selected: form.color === c }]"
                    :style="{ background: c }" @click="form.color = c"></button>
          </div>

          <label>Quién lo atiende</label>
          <div class="staff-pick">
            <button v-for="s in staff" :key="s.id" type="button"
                    :class="['staff-chip', { selected: form.staff_ids.includes(s.id) }]"
                    @click="toggleStaff(s.id)">{{ s.name }}</button>
          </div>

          <label class="chk">
            <input type="checkbox" v-model="form.requires_prepay" style="width:auto;">
            Requiere depósito anticipado
          </label>

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
.svc-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 22px;
  position: relative; overflow: hidden;
}
.svc-card::before {
  content: ''; position: absolute; top:0; left:0; right:0; height: 4px;
  background: var(--svc-color, var(--navy));
}
.svc-head { display:flex; justify-content:space-between; align-items:start; gap:10px; margin-bottom:8px; }
.svc-name { font-family: var(--serif); font-size: 20px; color: var(--navy); font-weight: 600; }
.svc-price { font-family: var(--serif); font-size: 30px; color: var(--navy); font-weight: 600; letter-spacing: -0.02em; }
.svc-flags { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }

.modal-bg {
  position: fixed; inset: 0; background: rgba(12,25,51,0.55);
  display: grid; place-items: center; z-index: 95; padding: 20px;
}
.modal {
  background: var(--surface); border-radius: var(--radius);
  padding: 0; max-width: 520px; width: 100%; max-height: 90vh; overflow-y: auto;
  box-shadow: var(--shadow-lg);
}
.modal-head {
  padding: 20px 24px; border-bottom: 1px solid var(--line-soft);
  display: flex; justify-content: space-between; align-items: center;
}
.modal-body { padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; }
label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
.chk { display:flex; gap:8px; align-items:center; font-size:14px; color: var(--text); text-transform:none; letter-spacing:0; font-weight:500; margin-top:6px; }

.color-picker { display: flex; gap: 8px; flex-wrap: wrap; }
.color-swatch {
  width: 34px; height: 34px; border-radius: 50%;
  border: 2px solid var(--border); cursor: pointer; transition: all .15s;
}
.color-swatch.selected { border-color: var(--navy); transform: scale(1.15); }
.staff-pick { display: flex; flex-wrap: wrap; gap: 6px; }
.staff-chip {
  padding: 7px 12px; border-radius: 999px; font-size: 13px; font-weight: 500;
  background: var(--cream); border: 1.5px solid var(--line); color: var(--ink-2);
  cursor: pointer;
}
.staff-chip.selected { background: var(--navy); color: var(--cream); border-color: var(--navy); }
</style>
