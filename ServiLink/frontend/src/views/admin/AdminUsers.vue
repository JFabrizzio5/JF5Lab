<template>
  <div class="layout">
    <AppSidebar />
    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Usuarios</h1>
        <p class="page-subtitle">{{ users.length }} usuarios registrados</p>
      </div>
      <div class="card">
        <div v-if="loading" class="loading-state">Cargando...</div>
        <table v-else class="table">
          <thead>
            <tr><th>Usuario</th><th>Email</th><th>Rol</th><th>Estado</th><th>Registro</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>
                <div style="display:flex;align-items:center;gap:10px;">
                  <img :src="u.avatar_url" class="avatar" />
                  {{ u.name }}
                </div>
              </td>
              <td style="color:var(--text2);font-size:13px;">{{ u.email }}</td>
              <td>
                <span :class="roleBadge(u.role)" class="badge">{{ roleLabel(u.role) }}</span>
              </td>
              <td>
                <span :class="u.is_active ? 'badge-accent' : 'badge-danger'" class="badge">
                  {{ u.is_active ? '✓ Activo' : '✗ Inactivo' }}
                </span>
              </td>
              <td style="color:var(--text2);font-size:13px;">{{ formatDate(u.created_at) }}</td>
              <td>
                <button v-if="u.role !== 'superadmin'" @click="toggleUser(u.id)" :class="['btn btn-sm', u.is_active ? 'btn-danger' : 'btn-accent']">
                  {{ u.is_active ? 'Desactivar' : 'Activar' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppSidebar from '../../components/AppSidebar.vue'
import { adminApi } from '../../api/index.js'

const users = ref([])
const loading = ref(true)

onMounted(async () => {
  const { data } = await adminApi.users()
  users.value = data
  loading.value = false
})

function roleBadge(r) { return { superadmin: 'badge-warning', freelancer: 'badge-accent', client: 'badge-primary' }[r] || 'badge-primary' }
function roleLabel(r) { return { superadmin: '👑 Admin', freelancer: '🔧 Freelancer', client: '👤 Cliente' }[r] || r }
function formatDate(dt) { return dt ? new Date(dt).toLocaleDateString('es-MX') : '—' }

async function toggleUser(id) {
  await adminApi.toggleUser(id)
  const { data } = await adminApi.users()
  users.value = data
}
</script>

<style scoped>
.loading-state { padding: 32px; text-align: center; color: var(--text2); }
</style>
