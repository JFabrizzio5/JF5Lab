<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <span class="logo-icon">🎪</span>
      <span class="logo-text">ConventionOS</span>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="nav-label">Organizer</div>
        <router-link to="/organizer/dashboard" class="nav-item">
          <span class="nav-icon">📊</span> Dashboard
        </router-link>
        <router-link to="/organizer/settings" class="nav-item">
          <span class="nav-icon">⚙️</span> Mi Convención
        </router-link>
        <router-link to="/organizer/stages" class="nav-item">
          <span class="nav-icon">🎭</span> Escenarios
        </router-link>
        <router-link to="/organizer/speakers" class="nav-item">
          <span class="nav-icon">🎤</span> Ponentes
        </router-link>
        <router-link to="/organizer/stands" class="nav-item">
          <span class="nav-icon">🏪</span> Stands
        </router-link>
        <router-link to="/organizer/sponsors" class="nav-item">
          <span class="nav-icon">🤝</span> Patrocinadores
        </router-link>
        <router-link to="/organizer/tickets" class="nav-item">
          <span class="nav-icon">🎫</span> Boletos
        </router-link>
        <router-link to="/organizer/tournaments" class="nav-item">
          <span class="nav-icon">🏆</span> Torneos
        </router-link>
        <router-link to="/organizer/attendees" class="nav-item">
          <span class="nav-icon">👥</span> Asistentes
        </router-link>
        <router-link to="/organizer/payments" class="nav-item">
          <span class="nav-icon">💳</span> Pagos
        </router-link>
      </div>

      <div class="nav-section" v-if="isAdmin">
        <div class="nav-label">Admin</div>
        <router-link to="/admin" class="nav-item">
          <span class="nav-icon">🔧</span> Admin Dashboard
        </router-link>
        <router-link to="/admin/conventions" class="nav-item">
          <span class="nav-icon">🗂️</span> Convenciones
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">{{ userInitial }}</div>
        <div class="user-details">
          <div class="user-name">{{ user?.name }}</div>
          <div class="user-role">{{ user?.role }}</div>
        </div>
      </div>
      <button @click="handleLogout" class="btn-logout" title="Cerrar sesión">⬡</button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const user = computed(() => auth.user)
const isAdmin = computed(() => auth.isAdmin)
const userInitial = computed(() => (auth.user?.name || 'U')[0].toUpperCase())

function handleLogout() {
  auth.logout()
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
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.sidebar-logo {
  padding: 20px 20px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid var(--border);
}

.logo-icon { font-size: 22px; }
.logo-text { font-weight: 800; font-size: 15px; color: var(--text); letter-spacing: -0.3px; }

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-section { margin-bottom: 12px; }
.nav-label {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text2);
  padding: 8px 10px 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: 8px;
  font-size: 14px;
  color: var(--text2);
  transition: all 0.15s;
  text-decoration: none;
}

.nav-item:hover { background: rgba(255,255,255,0.05); color: var(--text); }
.nav-item.router-link-active { background: rgba(124,58,237,0.15); color: var(--primary); font-weight: 600; }
.nav-icon { font-size: 16px; width: 20px; }

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; }
.user-avatar {
  width: 34px;
  height: 34px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}
.user-details { min-width: 0; }
.user-name { font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: var(--text2); text-transform: capitalize; }

.btn-logout {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  flex-shrink: 0;
  font-size: 16px;
}
.btn-logout:hover { border-color: var(--danger); color: var(--danger); }
</style>
