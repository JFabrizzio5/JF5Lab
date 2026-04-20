<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <router-link to="/" class="logo-link">
        <span class="logo-icon">🏷️</span>
        <span class="logo-text">RentaMe</span>
      </router-link>
    </div>

    <nav class="sidebar-nav">
      <template v-if="isVendor">
        <router-link to="/vendor/dashboard" class="nav-item" active-class="active">
          <span class="nav-icon">📊</span>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/vendor/items" class="nav-item" active-class="active">
          <span class="nav-icon">📦</span>
          <span>Artículos</span>
        </router-link>
        <router-link to="/vendor/bookings" class="nav-item" active-class="active">
          <span class="nav-icon">📅</span>
          <span>Reservas</span>
        </router-link>
        <router-link to="/vendor/availability" class="nav-item" active-class="active">
          <span class="nav-icon">🗓️</span>
          <span>Disponibilidad</span>
        </router-link>
        <router-link to="/vendor/payments" class="nav-item" active-class="active">
          <span class="nav-icon">💳</span>
          <span>Pagos</span>
        </router-link>
        <router-link to="/vendor/settings" class="nav-item" active-class="active">
          <span class="nav-icon">⚙️</span>
          <span>Configuración</span>
        </router-link>
        <div class="nav-divider"></div>
        <a v-if="vendorSlug" :href="`/r/${vendorSlug}`" target="_blank" class="nav-item nav-external">
          <span class="nav-icon">🌐</span>
          <span>Ver mi landing</span>
          <span class="nav-ext-icon">↗</span>
        </a>
      </template>

      <template v-if="isAdmin">
        <router-link to="/admin" class="nav-item" active-class="active">
          <span class="nav-icon">🏠</span>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/admin/vendors" class="nav-item" active-class="active">
          <span class="nav-icon">🏪</span>
          <span>Vendedores</span>
        </router-link>
      </template>
    </nav>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">{{ userInitial }}</div>
        <div class="user-details">
          <div class="user-name">{{ user?.name }}</div>
          <div class="user-role">{{ roleLabel }}</div>
        </div>
      </div>
      <button class="logout-btn" @click="handleLogout" title="Cerrar sesión">
        ↩
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { vendorAPI } from '../api/index.js'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const isVendor = computed(() => authStore.isVendor)
const isAdmin = computed(() => authStore.isAdmin)
const userInitial = computed(() => user.value?.name?.charAt(0)?.toUpperCase() || '?')
const roleLabel = computed(() => {
  const labels = { vendor: 'Vendedor', superadmin: 'Super Admin', customer: 'Cliente' }
  return labels[user.value?.role] || user.value?.role
})

const vendorSlug = ref(null)

onMounted(async () => {
  if (isVendor.value) {
    try {
      const res = await vendorAPI.getProfile()
      vendorSlug.value = res.data.slug
    } catch {}
  }
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: var(--bg2);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 0;
  flex-shrink: 0;
}

.sidebar-logo {
  padding: 20px 20px 16px;
  border-bottom: 1px solid var(--border);
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-icon {
  font-size: 22px;
}

.logo-text {
  font-size: 18px;
  font-weight: 800;
  background: linear-gradient(135deg, #6366f1, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text2);
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
  background: rgba(99, 102, 241, 0.12);
  color: #818cf8;
}

.nav-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.nav-ext-icon {
  margin-left: auto;
  font-size: 12px;
}

.nav-divider {
  height: 1px;
  background: var(--border);
  margin: 8px 0;
}

.nav-external {
  color: var(--text2);
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.user-details {
  min-width: 0;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 11px;
  color: var(--text2);
}

.logout-btn {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text2);
  width: 30px;
  height: 30px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.logout-btn:hover {
  color: var(--danger);
  border-color: var(--danger);
}
</style>
