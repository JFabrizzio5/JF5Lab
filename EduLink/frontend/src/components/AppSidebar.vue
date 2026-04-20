<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <span class="brand-icon">🎓</span>
      <span class="brand-name">EduLink</span>
    </div>

    <div class="sidebar-user" v-if="user">
      <img :src="user.avatar_url || defaultAvatar" class="user-avatar" alt="avatar" />
      <div class="user-info">
        <div class="user-name">{{ user.name }}</div>
        <div class="user-role">
          <span class="badge badge-school">{{ user.school }}</span>
          <span class="role-text">{{ roleLabel }}</span>
        </div>
      </div>
    </div>

    <nav class="sidebar-nav">
      <!-- Student nav -->
      <template v-if="user?.role === 'student'">
        <RouterLink to="/courses" class="nav-item">
          <span class="nav-icon">🏠</span> Explorar Cursos
        </RouterLink>
        <RouterLink to="/my-courses" class="nav-item">
          <span class="nav-icon">📚</span> Mis Cursos
        </RouterLink>
        <RouterLink to="/schedule" class="nav-item">
          <span class="nav-icon">📅</span> Reservar Tutoría
        </RouterLink>
      </template>

      <!-- Tutor nav -->
      <template v-if="user?.role === 'tutor'">
        <RouterLink to="/tutor/dashboard" class="nav-item">
          <span class="nav-icon">📊</span> Dashboard
        </RouterLink>
        <RouterLink to="/tutor/courses" class="nav-item">
          <span class="nav-icon">🎬</span> Mis Cursos
        </RouterLink>
        <RouterLink to="/tutor/schedule" class="nav-item">
          <span class="nav-icon">🗓️</span> Mi Horario
        </RouterLink>
      </template>

      <!-- Admin nav -->
      <template v-if="user?.role === 'admin'">
        <RouterLink to="/admin" class="nav-item">
          <span class="nav-icon">📊</span> Dashboard
        </RouterLink>
        <RouterLink to="/admin/users" class="nav-item">
          <span class="nav-icon">👥</span> Usuarios
        </RouterLink>
        <RouterLink to="/admin/courses" class="nav-item">
          <span class="nav-icon">🎬</span> Cursos
        </RouterLink>
      </template>
    </nav>

    <div class="sidebar-footer">
      <button @click="handleLogout" class="logout-btn">
        <span>🚪</span> Cerrar Sesión
      </button>
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
const defaultAvatar = 'https://ui-avatars.com/api/?name=User&background=334155&color=fff'

const roleLabel = computed(() => {
  const map = { student: 'Estudiante', tutor: 'Tutor', admin: 'Administrador' }
  return map[user.value?.role] || ''
})

function handleLogout() {
  auth.logout()
  router.push('/')
}
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

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  border-bottom: 1px solid var(--border);
}
.brand-icon { font-size: 24px; }
.brand-name { font-size: 20px; font-weight: 800; color: var(--primary); }

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  border-bottom: 1px solid var(--border);
}
.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}
.user-name { font-size: 13px; font-weight: 600; }
.user-role { display: flex; align-items: center; gap: 6px; margin-top: 4px; }
.role-text { font-size: 11px; color: var(--text2); }

.sidebar-nav {
  flex: 1;
  padding: 12px 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 16px;
  color: var(--text2);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  border-radius: 0;
}
.nav-item:hover { background: var(--bg3); color: var(--text); text-decoration: none; }
.nav-item.router-link-active {
  background: rgba(245, 158, 11, 0.1);
  color: var(--primary);
  border-right: 3px solid var(--primary);
}
.nav-icon { font-size: 16px; width: 20px; text-align: center; }

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
}
.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text2);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}
.logout-btn:hover { background: rgba(239, 68, 68, 0.1); color: #fca5a5; border-color: rgba(239, 68, 68, 0.3); }
</style>
