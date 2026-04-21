<script setup>
import { ref, onMounted, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { membersApi, exportsApi } from '../api/endpoints'

const list = ref([]); const q = ref(''); const showNew = ref(false); const selected = ref(null)
const form = ref({ first_name:'', last_name:'', email:'', phone:'' })

async function load() { const { data } = await membersApi.list(q.value); list.value = data }
async function create() { await membersApi.create(form.value); form.value = { first_name:'', last_name:'', email:'', phone:'' }; showNew.value=false; load() }
onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="head">
      <div><h1>Miembros</h1><p class="muted">{{ list.length }} registrados</p></div>
      <div class="acts">
        <button class="btn btn-sm" @click="exportsApi.members()"><i class="mdi mdi-file-excel"></i> Exportar</button>
        <button class="btn btn-primary btn-sm" @click="showNew=!showNew"><i class="mdi mdi-plus"></i> Nuevo</button>
      </div>
    </div>

    <div class="card" v-if="showNew" style="margin-bottom:18px;">
      <div class="grid-2">
        <div><label>Nombre</label><input v-model="form.first_name" /></div>
        <div><label>Apellido</label><input v-model="form.last_name" /></div>
        <div><label>Email</label><input v-model="form.email" type="email" /></div>
        <div><label>Teléfono</label><input v-model="form.phone" /></div>
      </div>
      <div style="margin-top:12px; display:flex; gap:8px;">
        <button class="btn btn-primary" :disabled="!form.first_name" @click="create">Crear</button>
        <button class="btn" @click="showNew=false">Cancelar</button>
      </div>
    </div>

    <input v-model="q" placeholder="Buscar..." @input="load" style="max-width:360px; margin-bottom:14px;" />

    <div class="grid-2" style="align-items:start;">
      <div class="card" style="padding:0; overflow:auto;">
        <table class="table">
          <thead><tr><th>Código</th><th>Nombre</th><th>Email</th><th>Ingresó</th></tr></thead>
          <tbody>
            <tr v-for="m in list" :key="m.id" @click="selected=m" style="cursor:pointer;" :class="{ sel: selected?.id===m.id }">
              <td class="mono">{{ m.code }}</td>
              <td>{{ m.first_name }} {{ m.last_name }}</td>
              <td class="muted">{{ m.email || '—' }}</td>
              <td class="muted">{{ m.joined_at?.slice(0,10) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="selected" class="card" style="text-align:center;">
        <h3 style="margin:0 0 8px;">{{ selected.first_name }} {{ selected.last_name }}</h3>
        <div class="muted mono" style="margin-bottom:16px;">{{ selected.code }}</div>
        <img :src="membersApi.qrUrl(selected.id, 260)" alt="qr" style="width:220px; height:220px; border:1px solid var(--border); border-radius:14px; padding:12px; background:white;" />
        <div class="muted" style="font-size:12px; margin-top:10px;">Imprime o manda al miembro para check-in rápido</div>
      </div>
      <div v-else class="card muted" style="text-align:center; padding:40px;">Selecciona un miembro para ver su QR</div>
    </div>
  </AppLayout>
</template>

<style scoped>
.head { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:24px; }
.head h1 { margin:0; font-size:30px; letter-spacing:-0.03em; font-weight:800; }
.acts { display:flex; gap:8px; }
.sel { background: var(--violet-soft) !important; }
</style>
