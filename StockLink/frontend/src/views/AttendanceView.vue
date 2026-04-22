<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { employeesApi, attendanceApi, exportsApi } from '../api/endpoints'

const employees = ref([])
const punches = ref([])
const form = ref({ code: '', name: '', role: 'operador', email: '' })
const showNew = ref(false)

async function load() {
  const [e, a] = await Promise.all([employeesApi.list(), attendanceApi.list()])
  employees.value = e.data; punches.value = a.data
}
async function create() {
  await employeesApi.create(form.value)
  form.value = { code: '', name: '', role: 'operador', email: '' }
  showNew.value = false
  load()
}
onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div><h1>Asistencias</h1><p class="muted">Empleados, QR de checada y bitácora.</p></div>
      <div class="actions">
        <button class="btn btn-sm" @click="exportsApi.attendance()"><i class="mdi mdi-file-excel"></i> Exportar</button>
        <button class="btn btn-primary btn-sm" @click="showNew=!showNew"><i class="mdi mdi-account-plus"></i> Nuevo empleado</button>
      </div>
    </div>

    <div v-if="showNew" class="card" style="margin-bottom:20px;">
      <div class="grid-3">
        <div><label>Código</label><input v-model="form.code" placeholder="EMP-010" /></div>
        <div><label>Nombre</label><input v-model="form.name" placeholder="Juan Pérez" /></div>
        <div><label>Rol</label>
          <select v-model="form.role">
            <option>operador</option><option>supervisor</option><option>admin</option><option>chofer</option><option>mesero</option><option>cocinero</option><option>cajero</option>
          </select>
        </div>
        <div style="grid-column: span 3;"><label>Email</label><input v-model="form.email" type="email" /></div>
      </div>
      <div style="margin-top:14px;">
        <button class="btn btn-primary" :disabled="!form.code || !form.name" @click="create">Crear y generar QR</button>
        <button class="btn" @click="showNew=false">Cancelar</button>
      </div>
    </div>

    <div class="grid-2">
      <div class="card" style="padding:0; overflow:auto;">
        <h3 style="padding:16px 20px 0; margin:0;">Empleados</h3>
        <table class="table">
          <thead><tr><th>Código</th><th>Nombre</th><th>Rol</th><th>Email</th></tr></thead>
          <tbody>
            <tr v-for="e in employees" :key="e.id">
              <td class="mono">{{ e.code }}</td>
              <td>{{ e.name }}</td>
              <td><span class="badge">{{ e.role }}</span></td>
              <td class="muted">{{ e.email || '—' }}</td>
            </tr>
            <tr v-if="!employees.length"><td colspan="4" class="muted" style="text-align:center; padding:30px;">Sin empleados aún.</td></tr>
          </tbody>
        </table>
      </div>

      <div class="card" style="padding:0; overflow:auto;">
        <h3 style="padding:16px 20px 0; margin:0;">Bitácora de checadas</h3>
        <table class="table">
          <thead><tr><th>Cuándo</th><th>Empleado</th><th>Tipo</th><th>Método</th></tr></thead>
          <tbody>
            <tr v-for="p in punches" :key="p.id">
              <td class="muted">{{ p.at }}</td>
              <td class="mono">{{ p.employee_id.slice(0,8) }}…</td>
              <td><span class="badge accent">{{ p.kind }}</span></td>
              <td>{{ p.method }}</td>
            </tr>
            <tr v-if="!punches.length"><td colspan="4" class="muted" style="text-align:center; padding:30px;">Sin checadas.</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-head { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.page-head h1 { margin: 0; font-size: 28px; letter-spacing: -0.02em; }
.actions { display: flex; gap: 8px; }
</style>
