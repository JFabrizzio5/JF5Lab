<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <span class="logo-icon">🏛️</span>
      <span class="logo-text">SalonOS</span>
    </div>

    <nav class="sidebar-nav">
      <template v-if="role === 'superadmin'">
        <router-link to="/admin" class="nav-item">
          <span class="nav-icon">📊</span> Dashboard
        </router-link>
        <router-link to="/admin/venues" class="nav-item">
          <span class="nav-icon">🏢</span> Venues
        </router-link>
      </template>

      <template v-else>
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">📊</span> Dashboard
        </router-link>
        <router-link to="/events" class="nav-item">
          <span class="nav-icon">📅</span> Eventos
        </router-link>
        <router-link to="/clients" class="nav-item">
          <span class="nav-icon">👥</span> Clientes
        </router-link>
        <router-link to="/calendar" class="nav-item">
          <span class="nav-icon">🗓️</span> Calendario
        </router-link>
        <router-link to="/chats" class="nav-item">
          <span class="nav-icon">💬</span> Chats
        </router-link>
        <template v-if="role === 'venue_owner'">
          <div class="nav-section">Configuración</div>
          <router-link to="/spaces" class="nav-item">
            <span class="nav-icon">🏠</span> Espacios
          </router-link>
          <router-link to="/branches" class="nav-item">
            <span class="nav-icon">📍</span> Sucursales
          </router-link>
          <router-link to="/settings" class="nav-item">
            <span class="nav-icon">⚙️</span> Ajustes
          </router-link>
        </template>
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
      <button @click="handleLogout" class="logout-btn" title="Cerrar sesión">⏻</button>
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
const role = computed(() => auth.role)
const userInitial = computed(() => auth.user?.name?.charAt(0)?.toUpperCase() || '?')
const roleLabel = computed(() => ({
  superadmin: 'Super Admin',
  venue_owner: 'Propietario',
  venue_staff: 'Staff',
  client: 'Cliente',
}[auth.role] || auth.role))

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: var(--bg2);
  border-right: 1px solid var(--border);
  position: fixed;
  left: 0; top: 0; bottom: 0;
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow-y: auto;
}

.sidebar-logo {
  padding: 1.5rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.logo-icon { font-size: 1.5rem; }

.logo-text {
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.9rem;
  border-radius: 8px;
  color: var(--text2);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-item:hover {
  background: rgba(124,58,237,0.1);
  color: var(--text);
}

.nav-item.router-link-active {
  background: rgba(124,58,237,0.15);
  color: var(--primary);
}

.nav-icon { font-size: 1rem; width: 1.25rem; text-align: center; }

.nav-section {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text2);
  padding: 0.75rem 0.9rem 0.25rem;
  font-weight: 600;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex: 1;
  min-width: 0;
}

.user-avatar {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.user-details { min-width: 0; }

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.72rem;
  color: var(--text2);
}

.logout-btn {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  font-size: 1.1rem;
  padding: 0.25rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.logout-btn:hover { color: var(--danger); }
</style>
