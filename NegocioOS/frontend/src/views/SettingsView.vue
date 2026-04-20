<template>
  <div>
    <div class="page-header">
      <h1>Configuración</h1>
      <p>Perfil del negocio y ajustes de la cuenta</p>
    </div>

    <div class="page-body settings-grid">
      <!-- Profile card -->
      <div class="card">
        <h3 class="section-title">👤 Perfil de usuario</h3>
        <div class="avatar-section">
          <div class="big-avatar">{{ userInitial }}</div>
          <div>
            <div class="user-name-big">{{ user?.name }}</div>
            <div class="user-role-badge badge" :class="roleBadgeClass">{{ roleLabel }}</div>
          </div>
        </div>

        <div class="info-list">
          <div class="info-item">
            <span class="info-label">Email</span>
            <span class="info-val">{{ user?.email }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Negocio</span>
            <span class="info-val">{{ user?.business_name || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Rol</span>
            <span class="info-val">{{ roleLabel }}</span>
          </div>
        </div>
      </div>

      <!-- Demo accounts -->
      <div class="card">
        <h3 class="section-title">🔐 Cuentas demo</h3>
        <p class="section-desc">Contraseña: <code>demo123</code> para todas las cuentas</p>
        <div class="demo-list">
          <div v-for="acc in demoAccounts" :key="acc.email" class="demo-account">
            <div class="demo-avatar">{{ acc.icon }}</div>
            <div>
              <div class="demo-name">{{ acc.name }}</div>
              <div class="demo-email-text">{{ acc.email }}</div>
            </div>
            <span class="badge" :class="acc.badgeClass">{{ acc.role }}</span>
          </div>
        </div>
      </div>

      <!-- Tech stack -->
      <div class="card">
        <h3 class="section-title">⚙️ Stack técnico</h3>
        <div class="stack-list">
          <div class="stack-item" v-for="s in stack" :key="s.name">
            <span class="stack-icon">{{ s.icon }}</span>
            <div>
              <div class="stack-name">{{ s.name }}</div>
              <div class="stack-desc">{{ s.desc }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="card">
        <h3 class="section-title">🚪 Sesión</h3>
        <p class="section-desc">Cierra sesión de forma segura</p>
        <button class="btn btn-danger" @click="handleLogout">⏏ Cerrar sesión</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const user = computed(() => auth.user)

const userInitial = computed(() => (user.value?.name || 'U')[0].toUpperCase())
const roleLabel = computed(() => ({ admin: 'Administrador', owner: 'Propietario', employee: 'Empleado' }[user.value?.role] || 'Empleado'))
const roleBadgeClass = computed(() => ({ admin: 'badge-accent', owner: 'badge-primary', employee: 'badge-success' }[user.value?.role] || 'badge-success'))

function handleLogout() {
  auth.logout()
  router.push('/login')
}

const demoAccounts = [
  { email: 'admin@negocio.mx', name: 'Administrador', role: 'Admin', icon: '🔑', badgeClass: 'badge-accent' },
  { email: 'dueno@negocio.mx', name: 'Dueño Demo', role: 'Propietario', icon: '🏪', badgeClass: 'badge-primary' },
  { email: 'cajero@negocio.mx', name: 'Cajero Demo', role: 'Empleado', icon: '🧑‍💼', badgeClass: 'badge-success' },
]

const stack = [
  { icon: '🐍', name: 'FastAPI + SQLAlchemy', desc: 'Backend Python en puerto 8041' },
  { icon: '🐘', name: 'PostgreSQL 15', desc: 'Base de datos relacional' },
  { icon: '💚', name: 'Vue 3 + Vite', desc: 'Frontend en puerto 3015' },
  { icon: '🤖', name: 'Anthropic Claude', desc: 'Asistente IA (claude-haiku-4-5)' },
  { icon: '🐳', name: 'Docker Compose', desc: 'Red aislada negocio_net' },
]
</script>

<style scoped>
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.section-title { font-size: 15px; font-weight: 700; margin-bottom: 16px; }
.section-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.section-desc code { background: var(--bg3); padding: 2px 6px; border-radius: 4px; color: var(--primary); }

.avatar-section { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.big-avatar {
  width: 64px; height: 64px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 800;
}
.user-name-big { font-size: 18px; font-weight: 700; margin-bottom: 6px; }

.info-list { display: flex; flex-direction: column; gap: 12px; }
.info-item { display: flex; justify-content: space-between; font-size: 14px; padding: 10px 0; border-bottom: 1px solid var(--border); }
.info-item:last-child { border-bottom: none; }
.info-label { color: var(--text-muted); }
.info-val { font-weight: 600; }

.demo-list { display: flex; flex-direction: column; gap: 12px; }
.demo-account { display: flex; align-items: center; gap: 12px; padding: 10px; background: var(--bg3); border-radius: 8px; }
.demo-avatar { font-size: 24px; width: 36px; text-align: center; }
.demo-name { font-size: 13px; font-weight: 600; }
.demo-email-text { font-size: 12px; color: var(--text-muted); }
.demo-account .badge { margin-left: auto; }

.stack-list { display: flex; flex-direction: column; gap: 12px; }
.stack-item { display: flex; align-items: center; gap: 12px; }
.stack-icon { font-size: 20px; width: 28px; text-align: center; }
.stack-name { font-size: 13px; font-weight: 600; }
.stack-desc { font-size: 12px; color: var(--text-muted); }

.btn-danger { margin-top: 4px; }
</style>
