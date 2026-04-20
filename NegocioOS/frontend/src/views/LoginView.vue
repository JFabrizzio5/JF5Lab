<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🏪 NegocioOS</div>
      <h2>Iniciar sesión</h2>
      <p class="auth-sub">Bienvenido de vuelta</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" required />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? 'Iniciando...' : 'Iniciar sesión' }}
        </button>
      </form>

      <div class="auth-footer">
        ¿No tienes cuenta? <router-link to="/register">Regístrate</router-link>
        &nbsp;·&nbsp; <router-link to="/">← Inicio</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/pos')
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
  padding: 24px;
}

.auth-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.auth-logo {
  font-size: 20px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 20px;
}

h2 { font-size: 24px; font-weight: 700; }
.auth-sub { color: var(--text-muted); font-size: 14px; margin-bottom: 28px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 6px; color: var(--text-muted); }

.error-msg { color: var(--danger); font-size: 13px; margin-bottom: 12px; }

.w-full { width: 100%; justify-content: center; }

.auth-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 13px;
  color: var(--text-muted);
}

.auth-footer a { color: var(--primary); }
</style>
