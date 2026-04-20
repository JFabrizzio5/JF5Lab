<template>
  <div>
    <div class="page-header">
      <h1>Historial de Ventas</h1>
      <p>Todas las transacciones registradas</p>
    </div>

    <div class="page-body">
      <div class="card">
        <div class="table-toolbar">
          <input v-model="search" placeholder="🔍 Buscar venta, cliente..." style="max-width: 280px" />
          <select v-model="filterMethod" style="max-width: 180px">
            <option value="">Todos los métodos</option>
            <option value="cash">Efectivo</option>
            <option value="card">Tarjeta</option>
            <option value="transfer">Transferencia</option>
          </select>
          <select v-model="filterStatus" style="max-width: 160px">
            <option value="">Todos los estados</option>
            <option value="completed">Completada</option>
            <option value="cancelled">Cancelada</option>
            <option value="refunded">Reembolsada</option>
          </select>
        </div>

        <div v-if="loading" class="empty-state">Cargando ventas...</div>
        <table v-else>
          <thead>
            <tr>
              <th>ID</th>
              <th>Fecha</th>
              <th>Cajero</th>
              <th>Cliente</th>
              <th>Método</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredSales" :key="s.id">
              <td>#{{ s.id }}</td>
              <td>{{ formatDate(s.created_at) }}</td>
              <td>{{ s.user_name || '—' }}</td>
              <td>{{ s.customer_name || '—' }}</td>
              <td>
                <span class="badge badge-accent">{{ methodLabel(s.payment_method) }}</span>
              </td>
              <td><strong>${{ s.total.toFixed(2) }}</strong></td>
              <td>
                <span class="badge" :class="statusClass(s.status)">{{ statusLabel(s.status) }}</span>
              </td>
              <td>
                <button class="btn btn-ghost btn-xs" @click="toggleTicket(s)">
                  {{ openTicket === s.id ? '▲ Cerrar' : '▼ Ticket' }}
                </button>
              </td>
            </tr>
            <!-- Ticket row -->
            <tr v-if="openTicket" v-for="s in filteredSales.filter(x => x.id === openTicket)" :key="'t'+s.id">
              <td colspan="8" class="ticket-row-cell">
                <div class="ticket-box">
                  <div class="ticket-title">📋 Ticket #{{ s.id }}</div>
                  <table class="ticket-table">
                    <thead>
                      <tr>
                        <th>Producto</th>
                        <th>Cant.</th>
                        <th>Precio unit.</th>
                        <th>Subtotal</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in s.items" :key="item.id">
                        <td>{{ item.product_name }}</td>
                        <td>{{ item.quantity }}</td>
                        <td>${{ item.unit_price.toFixed(2) }}</td>
                        <td>${{ item.subtotal.toFixed(2) }}</td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="ticket-footer">
                    <span>Subtotal: ${{ s.subtotal.toFixed(2) }}</span>
                    <span>IVA: ${{ s.tax.toFixed(2) }}</span>
                    <strong>Total: ${{ s.total.toFixed(2) }}</strong>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="!loading && filteredSales.length === 0" class="empty-state">No hay ventas con los filtros seleccionados</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index.js'

const sales = ref([])
const loading = ref(false)
const search = ref('')
const filterMethod = ref('')
const filterStatus = ref('')
const openTicket = ref(null)

const filteredSales = computed(() => {
  let list = sales.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(s =>
      String(s.id).includes(q) ||
      (s.customer_name || '').toLowerCase().includes(q) ||
      (s.user_name || '').toLowerCase().includes(q)
    )
  }
  if (filterMethod.value) list = list.filter(s => s.payment_method === filterMethod.value)
  if (filterStatus.value) list = list.filter(s => s.status === filterStatus.value)
  return list
})

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('es-MX', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}

function methodLabel(m) {
  return { cash: '💵 Efectivo', card: '💳 Tarjeta', transfer: '📲 Transferencia' }[m] || m
}

function statusLabel(s) {
  return { completed: 'Completada', cancelled: 'Cancelada', refunded: 'Reembolsada' }[s] || s
}

function statusClass(s) {
  return { completed: 'badge-success', cancelled: 'badge-danger', refunded: 'badge-warning' }[s] || ''
}

function toggleTicket(s) {
  openTicket.value = openTicket.value === s.id ? null : s.id
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/sales/')
    sales.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.table-toolbar { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }
.btn-xs { padding: 4px 10px; font-size: 12px; }
.ticket-row-cell { padding: 0 !important; background: var(--bg3); }
.ticket-box { padding: 16px 24px; }
.ticket-title { font-weight: 700; margin-bottom: 12px; font-size: 15px; }
.ticket-table { width: 100%; border-collapse: collapse; margin-bottom: 12px; }
.ticket-table th, .ticket-table td { padding: 6px 10px; font-size: 13px; border-bottom: 1px solid var(--border); }
.ticket-footer { display: flex; gap: 24px; font-size: 14px; color: var(--text-muted); }
.ticket-footer strong { color: var(--text); }
</style>
