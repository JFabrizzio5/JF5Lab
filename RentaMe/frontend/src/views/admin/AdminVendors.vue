<template>
  <div class="layout">
    <AppSidebar />
    <main class="main-content">
      <h1 class="page-title">Vendedores</h1>
      <p class="page-subtitle">Gestiona todos los vendedores de la plataforma</p>

      <div v-if="loading" class="loading">Cargando vendedores...</div>

      <div v-else class="card">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Negocio</th>
                <th>Email</th>
                <th>Ciudad</th>
                <th>Artículos</th>
                <th>Reservas</th>
                <th>Fee %</th>
                <th>Stripe</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="v in vendors" :key="v.id">
                <td>
                  <div class="vendor-cell">
                    <div class="vendor-dot" :style="{ background: v.theme_color }"></div>
                    <div>
                      <div class="vendor-name">{{ v.business_name }}</div>
                      <div class="vendor-slug">/r/{{ v.slug }}</div>
                    </div>
                  </div>
                </td>
                <td class="email-cell">{{ v.user_email }}</td>
                <td>{{ v.city || '—' }}</td>
                <td class="center">{{ v.items_count }}</td>
                <td class="center">{{ v.bookings_count }}</td>
                <td>
                  <div class="fee-edit">
                    <input
                      type="number"
                      :value="v.platform_fee_percent"
                      @change="updateFee(v.id, $event.target.value)"
                      class="fee-input"
                      min="0"
                      max="50"
                      step="0.5"
                    />%
                  </div>
                </td>
                <td>
                  <span v-if="v.stripe_onboarding_complete" class="badge badge-success">✅ Conectado</span>
                  <span v-else class="badge badge-gray">Sin conectar</span>
                </td>
                <td>
                  <span :class="`badge badge-${v.is_active ? 'success' : 'danger'}`">
                    {{ v.is_active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td>
                  <div class="action-btns">
                    <a :href="`/r/${v.slug}`" target="_blank" class="btn btn-secondary btn-sm" title="Ver landing">↗</a>
                    <button class="btn btn-sm" :class="v.is_active ? 'btn-danger' : 'btn-success'" @click="toggleVendor(v.id)">
                      {{ v.is_active ? 'Desactivar' : 'Activar' }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { adminAPI } from '../../api/index.js'

const vendors = ref([])
const loading = ref(true)

async function loadVendors() {
  const res = await adminAPI.vendors()
  vendors.value = res.data
  loading.value = false
}

async function toggleVendor(id) {
  try {
    const res = await adminAPI.toggleVendor(id)
    const v = vendors.value.find(v => v.id === id)
    if (v) v.is_active = res.data.is_active
  } catch {}
}

async function updateFee(id, fee) {
  const feeNum = parseFloat(fee)
  if (isNaN(feeNum) || feeNum < 0 || feeNum > 50) return
  try {
    await adminAPI.setFee(id, feeNum)
    const v = vendors.value.find(v => v.id === id)
    if (v) v.platform_fee_percent = feeNum
  } catch {}
}

onMounted(loadVendors)
</script>

<style scoped>
.loading { text-align: center; padding: 40px; color: var(--text2); }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; min-width: 900px; }
th {
  font-size: 11px;
  font-weight: 700;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
td { padding: 12px; font-size: 13px; border-bottom: 1px solid var(--border); vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }
.center { text-align: center; }

.vendor-cell { display: flex; align-items: center; gap: 10px; }
.vendor-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.vendor-name { font-weight: 600; font-size: 13px; }
.vendor-slug { font-size: 11px; color: var(--text2); }
.email-cell { color: var(--text2); font-size: 12px; }

.fee-edit { display: flex; align-items: center; gap: 4px; }
.fee-input {
  width: 52px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 6px;
  color: var(--text);
  font-size: 12px;
}

.action-btns { display: flex; gap: 6px; }
</style>
