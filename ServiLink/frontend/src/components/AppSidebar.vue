<template>
  <div class="sidebar">
    <div class="sidebar-logo">⚡ ServiLink</div>

    <template v-if="auth.isAdmin">
      <router-link to="/admin">📊 Dashboard</router-link>
      <router-link to="/admin/users">👥 Usuarios</router-link>
      <router-link to="/admin/categories">🏷️ Categorías</router-link>
      <router-link to="/admin/bookings">📋 Reservas</router-link>
    </template>

    <template v-if="auth.isClient">
      <router-link to="/marketplace">🛒 Marketplace</router-link>
      <router-link to="/home">🗺️ Mapa en vivo</router-link>
      <router-link to="/my-bookings">📋 Mis reservas</router-link>
      <router-link to="/chats">💬 Chats</router-link>
    </template>

    <template v-if="auth.isFreelancer">
      <router-link to="/dashboard">📊 Dashboard</router-link>
      <router-link to="/my-profile">👤 Mi perfil</router-link>
      <router-link to="/subscriptions">⭐ Suscripción</router-link>
      <router-link to="/chats">💬 Chats</router-link>
    </template>

    <div class="sidebar-bottom">
      <div class="user-info">
        <img :src="auth.user?.avatar_url" class="avatar" :alt="auth.user?.name" />
        <div>
          <div class="user-name">{{ auth.user?.name }}</div>
          <div class="user-role">{{ roleLabel }}</div>
        </div>
      </div>
      <button @click="handleLogout" class="logout-btn">🚪 Salir</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const roleLabel = computed(() => ({
  superadmin: '👑 Superadmin',
  client: '👤 Cliente',
  freelancer: '🔧 Profesional',
}[auth.user?.role] || ''))

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar-bottom { margin-top: auto; border-top: 1px solid var(--border); padding-top: 16px; display: flex; flex-direction: column; gap: 10px; }
.user-info { display: flex; align-items: center; gap: 10px; padding: 0 4px; }
.user-name { font-size: 13px; font-weight: 600; }
.user-role { font-size: 11px; color: var(--text2); }
.logout-btn { width: 100%; background: transparent; border: 1px solid var(--border); border-radius: 8px; padding: 8px; color: var(--text2); cursor: pointer; font-size: 13px; transition: all 0.2s; }
.logout-btn:hover { border-color: var(--danger); color: var(--danger); }
</style>
