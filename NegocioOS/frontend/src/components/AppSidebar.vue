<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <span class="logo-icon">🏪</span>
      <span class="logo-text">NegocioOS</span>
    </div>

    <nav class="sidebar-nav">
      <router-link to="/pos" class="nav-item" active-class="active">
        <span class="nav-icon">🛒</span>
        <span>Punto de Venta</span>
      </router-link>
      <router-link to="/inventory" class="nav-item" active-class="active">
        <span class="nav-icon">📦</span>
        <span>Inventario</span>
        <span v-if="lowStockCount > 0" class="nav-badge">{{ lowStockCount }}</span>
      </router-link>
      <router-link to="/sales" class="nav-item" active-class="active">
        <span class="nav-icon">📋</span>
        <span>Ventas</span>
      </router-link>
      <router-link to="/customers" class="nav-item" active-class="active">
        <span class="nav-icon">👥</span>
        <span>Clientes</span>
      </router-link>
      <router-link to="/reports" class="nav-item" active-class="active">
        <span class="nav-icon">📊</span>
        <span>Reportes</span>
      </router-link>
      <router-link to="/rag" class="nav-item" active-class="active">
        <span class="nav-icon">🤖</span>
        <span>Asistente IA</span>
      </router-link>
      <router-link to="/settings" class="nav-item" active-class="active">
        <span class="nav-icon">⚙️</span>
        <span>Configuración</span>
      </router-link>
    </nav>

    <div class="sidebar-user">
      <div class="user-avatar">{{ userInitial }}</div>
      <div class="user-info">
        <div class="user-name">{{ user?.name || 'Usuario' }}</div>
        <div class="user-role">{{ roleLabel }}</div>
      </div>
      <button class="logout-btn" @click="handleLogout" title="Cerrar sesión">⏏</button>
    </div>
  </aside>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import api from '../api/index.js'

const router = useRouter()
const auth = useAuthStore()
const user = computed(() => auth.user)
const lowStockCount = ref(0)

const userInitial = computed(() => (user.value?.name || 'U')[0].toUpperCase())
const roleLabel = computed(() => {
  const map = { admin: 'Admin', owner: 'Propietario', employee: 'Empleado' }
  return map[user.value?.role] || 'Empleado'
})

async function handleLogout() {
  auth.logout()
  router.push('/login')
}

onMounted(async () => {
  try {
    const res = await api.get('/inventory/low-stock')
    lowStockCount.value = res.data.length
  } catch {}
})
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--bg2);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 20px 24px;
  border-bottom: 1px solid var(--border);
}

.logo-icon { font-size: 24px; }
.logo-text {
  font-size: 18px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s;
  position: relative;
}

.nav-item:hover {
  background: var(--bg3);
  color: var(--text);
}

.nav-item.active {
  background: rgba(249,115,22,0.12);
  color: var(--primary);
  font-weight: 600;
}

.nav-icon { font-size: 16px; width: 20px; text-align: center; }

.nav-badge {
  margin-left: auto;
  background: var(--danger);
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 12px;
  min-width: 20px;
  text-align: center;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 16px;
  border-top: 1px solid var(--border);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.user-info { flex: 1; min-width: 0; }
.user-name { font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: var(--text-muted); }

.logout-btn {
  background: none;
  color: var(--text-muted);
  font-size: 16px;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.15s;
  flex-shrink: 0;
}

.logout-btn:hover { color: var(--danger); }
</style>
