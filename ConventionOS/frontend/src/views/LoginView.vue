<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🎪 ConventionOS</div>
      <h1>Iniciar Sesión</h1>
      <p class="auth-sub">Administra tu convención</p>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" required />
        </div>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? 'Iniciando...' : 'Iniciar Sesión' }}
        </button>
      </form>

      <div class="auth-hint">
        <strong>Demo:</strong><br>
        org@comiccon.mx / demo123 (Organizer)<br>
        admin@convention.mx / demo123 (Admin)
      </div>

      <div class="auth-footer">
        ¿No tienes cuenta? <router-link to="/register">Regístrate</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    const user = await auth.login(email.value, password.value)
    if (user.role === 'superadmin') router.push('/admin')
    else if (user.role === 'organizer') router.push('/organizer/dashboard')
    else router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Credenciales incorrectas'
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
  padding: 20px;
}

.auth-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.auth-logo {
  font-size: 20px;
  font-weight: 800;
  margin-bottom: 24px;
  text-align: center;
}

h1 { font-size: 24px; font-weight: 800; margin-bottom: 6px; }
.auth-sub { color: var(--text2); font-size: 14px; margin-bottom: 28px; }

.auth-form { display: flex; flex-direction: column; gap: 16px; margin-bottom: 20px; }

.error-msg {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #ef4444;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
}

.auth-hint {
  background: var(--bg3);
  border-radius: 8px;
  padding: 14px;
  font-size: 12px;
  color: var(--text2);
  line-height: 1.8;
  margin-bottom: 20px;
}

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: var(--text2);
}
.auth-footer a { color: var(--primary); font-weight: 600; }
</style>
