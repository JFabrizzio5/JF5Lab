<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">
        <span>🏛️</span>
        <span class="brand-name">SalonOS</span>
      </div>
      <h1>Bienvenido de nuevo</h1>
      <p class="auth-sub">Inicia sesión en tu cuenta</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center" :disabled="loading">
          {{ loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
        </button>
      </form>

      <p class="auth-link">
        ¿No tienes cuenta? <router-link to="/register">Regístrate</router-link>
      </p>
      <router-link to="/" class="back-link">← Volver al inicio</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

const ROLE_HOME = {
  superadmin: '/admin',
  venue_owner: '/dashboard',
  venue_staff: '/dashboard',
  client: '/',
}

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const user = await auth.login(form.value.email, form.value.password)
    router.push(ROLE_HOME[user.role] || '/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 2rem;
}

.auth-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
}

.auth-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.brand-name {
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.35rem; }

.auth-sub { color: var(--text2); font-size: 0.9rem; margin-bottom: 2rem; }

.error-msg {
  color: var(--danger);
  font-size: 0.85rem;
  margin-bottom: 1rem;
  background: rgba(239,68,68,0.1);
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
}

.auth-link {
  text-align: center;
  font-size: 0.875rem;
  color: var(--text2);
  margin-top: 1.5rem;
}

.auth-link a { color: var(--primary); text-decoration: none; }

.back-link {
  display: block;
  text-align: center;
  font-size: 0.82rem;
  color: var(--text2);
  text-decoration: none;
  margin-top: 1rem;
}

.back-link:hover { color: var(--text); }
</style>
