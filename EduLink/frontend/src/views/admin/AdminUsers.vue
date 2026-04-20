<template>
  <div>
    <div class="page-header">
      <h1>Gestión de Usuarios</h1>
      <p>Administra los usuarios registrados en la plataforma</p>
    </div>

    <div class="page-content">
      <div class="toolbar">
        <input v-model="search" type="text" placeholder="🔍 Buscar por nombre o email..." class="search-input" />
        <select v-model="filterRole" class="filter-select">
          <option value="">Todos los roles</option>
          <option value="student">Estudiante</option>
          <option value="tutor">Tutor</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <div v-if="loading" class="loading">Cargando usuarios...</div>
      <div v-else class="table-wrapper card" style="padding:0;overflow:hidden">
        <table>
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Email</th>
              <th>Rol</th>
              <th>Universidad</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in filteredUsers" :key="u.id">
              <td>
                <div style="display:flex;align-items:center;gap:8px">
                  <img :src="u.avatar_url || defaultAvatar" style="width:32px;height:32px;border-radius:50%;object-fit:cover" />
                  <span>{{ u.name }}</span>
                </div>
              </td>
              <td style="color:var(--text2)">{{ u.email }}</td>
              <td><span class="role-chip" :class="`role-${u.role}`">{{ roleLabel(u.role) }}</span></td>
              <td><span class="badge badge-school">{{ u.school }}</span></td>
              <td>
                <span :class="['status-dot', u.is_active ? 'active' : 'inactive']">
                  {{ u.is_active ? '● Activo' : '● Inactivo' }}
                </span>
              </td>
              <td>
                <div style="display:flex;gap:6px">
                  <button @click="toggleActive(u)" class="btn btn-ghost btn-sm">
                    {{ u.is_active ? 'Desactivar' : 'Activar' }}
                  </button>
                  <button @click="openRoleChange(u)" class="btn btn-ghost btn-sm">Rol</button>
                  <button v-if="u.role !== 'admin'" @click="deleteUser(u.id)" class="btn btn-danger btn-sm">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Change Role Modal -->
    <div v-if="editingUser" class="modal-overlay" @click.self="editingUser = null">
      <div class="modal">
        <h2>Cambiar Rol: {{ editingUser.name }}</h2>
        <div class="form-group" style="margin-top:16px">
          <label>Nuevo rol</label>
          <select v-model="newRole">
            <option value="student">Estudiante</option>
            <option value="tutor">Tutor</option>
            <option value="admin">Administrador</option>
          </select>
        </div>
        <div style="display:flex;gap:10px">
          <button @click="saveRole" class="btn btn-primary">Guardar</button>
          <button @click="editingUser = null" class="btn btn-ghost">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api/index.js'

const users = ref([])
const loading = ref(true)
const search = ref('')
const filterRole = ref('')
const editingUser = ref(null)
const newRole = ref('student')
const defaultAvatar = 'https://ui-avatars.com/api/?name=U&background=334155&color=fff'

function roleLabel(r) {
  return { student: 'Estudiante', tutor: 'Tutor', admin: 'Admin' }[r] || r
}

const filteredUsers = computed(() => {
  return users.value.filter(u => {
    const q = search.value.toLowerCase()
    const matchSearch = !q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)
    const matchRole = !filterRole.value || u.role === filterRole.value
    return matchSearch && matchRole
  })
})

async function fetchUsers() {
  loading.value = true
  try {
    const res = await api.get('/admin/users')
    users.value = res.data
  } finally {
    loading.value = false
  }
}

async function toggleActive(user) {
  await api.put(`/admin/users/${user.id}`, { is_active: !user.is_active })
  user.is_active = !user.is_active
}

function openRoleChange(user) {
  editingUser.value = user
  newRole.value = user.role
}

async function saveRole() {
  await api.put(`/admin/users/${editingUser.value.id}`, { role: newRole.value })
  editingUser.value.role = newRole.value
  editingUser.value = null
}

async function deleteUser(id) {
  if (!confirm('¿Eliminar este usuario? Esta acción es irreversible.')) return
  await api.delete(`/admin/users/${id}`)
  users.value = users.value.filter(u => u.id !== id)
}

onMounted(fetchUsers)
</script>

<style scoped>
.toolbar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.search-input {
  flex: 1;
  min-width: 200px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
}
.search-input:focus { outline: none; border-color: var(--primary); }
.filter-select {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 14px;
}
.filter-select:focus { outline: none; border-color: var(--primary); }

.role-chip { padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }
.role-student { background: rgba(99,102,241,0.2); color: #818cf8; }
.role-tutor { background: rgba(16,185,129,0.2); color: var(--accent); }
.role-admin { background: rgba(245,158,11,0.2); color: var(--primary); }

.status-dot { font-size: 12px; font-weight: 600; }
.status-dot.active { color: var(--accent); }
.status-dot.inactive { color: #f87171; }
</style>
