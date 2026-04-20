<template>
  <div>
    <div class="page-header">
      <div class="header-row">
        <div>
          <h1>Clientes</h1>
          <p>Directorio de clientes del negocio</p>
        </div>
        <button class="btn btn-primary" @click="showAdd = true">+ Nuevo cliente</button>
      </div>
    </div>

    <div class="page-body">
      <div class="card">
        <div class="table-toolbar">
          <input v-model="search" placeholder="🔍 Buscar cliente..." style="max-width: 300px" />
        </div>
        <div v-if="loading" class="empty-state">Cargando...</div>
        <table v-else>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Total compras</th>
              <th>Notas</th>
              <th>Registrado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in filteredCustomers" :key="c.id">
              <td>
                <div class="customer-name">
                  <div class="cust-avatar">{{ c.name[0].toUpperCase() }}</div>
                  {{ c.name }}
                </div>
              </td>
              <td>{{ c.email || '—' }}</td>
              <td>{{ c.phone || '—' }}</td>
              <td><strong class="total-purchases">${{ c.total_purchases.toFixed(2) }}</strong></td>
              <td><span class="notes-text">{{ c.notes || '—' }}</span></td>
              <td>{{ formatDate(c.created_at) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="!loading && filteredCustomers.length === 0" class="empty-state">No hay clientes registrados</div>
      </div>
    </div>

    <!-- Add Customer Modal -->
    <div v-if="showAdd" class="modal-overlay" @click.self="showAdd = false">
      <div class="modal">
        <h3>Nuevo Cliente</h3>
        <div class="form-group">
          <label>Nombre *</label>
          <input v-model="newCust.name" />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="newCust.email" type="email" />
        </div>
        <div class="form-group">
          <label>Teléfono</label>
          <input v-model="newCust.phone" />
        </div>
        <div class="form-group">
          <label>Notas</label>
          <textarea v-model="newCust.notes" rows="2" />
        </div>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="showAdd = false">Cancelar</button>
          <button class="btn btn-primary" @click="submitAdd">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index.js'

const customers = ref([])
const loading = ref(false)
const search = ref('')
const showAdd = ref(false)
const newCust = ref({ name: '', email: '', phone: '', notes: '' })

const filteredCustomers = computed(() => {
  if (!search.value) return customers.value
  const q = search.value.toLowerCase()
  return customers.value.filter(c =>
    c.name.toLowerCase().includes(q) ||
    (c.email || '').toLowerCase().includes(q) ||
    (c.phone || '').includes(q)
  )
})

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('es-MX')
}

async function submitAdd() {
  if (!newCust.value.name) return
  await api.post('/customers/', newCust.value)
  showAdd.value = false
  newCust.value = { name: '', email: '', phone: '', notes: '' }
  await load()
}

async function load() {
  loading.value = true
  try {
    const res = await api.get('/customers/')
    customers.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.header-row { display: flex; align-items: flex-start; justify-content: space-between; }
.table-toolbar { margin-bottom: 16px; }
.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }
.customer-name { display: flex; align-items: center; gap: 10px; font-weight: 600; }
.cust-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; flex-shrink: 0;
}
.total-purchases { color: var(--success); font-size: 15px; }
.notes-text { color: var(--text-muted); font-size: 13px; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; padding: 28px; width: 400px; }
.modal h3 { font-size: 18px; font-weight: 700; margin-bottom: 20px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 5px; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }
</style>
