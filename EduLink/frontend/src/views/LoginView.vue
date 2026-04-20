<template>
  <div class="auth-page">
    <div class="auth-card">
      <RouterLink to="/" class="back-link">← Volver al inicio</RouterLink>
      <div class="auth-brand">🎓 EduLink</div>
      <h1>Iniciar Sesión</h1>
      <p class="auth-sub">Accede a tu plataforma educativa</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Correo electrónico</label>
          <input v-model="email" type="email" placeholder="tu@correo.mx" required />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" required />
        </div>
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? 'Iniciando...' : 'Iniciar Sesión' }}
        </button>
      </form>

      <div class="quick-access">
        <p>Acceso demo rápido:</p>
        <div class="quick-btns">
          <button @click="quickLogin('alumno@edulink.mx')" class="quick-btn">👩‍🎓 Estudiante</button>
          <button @click="quickLogin('tutor@edulink.mx')" class="quick-btn">👨‍🏫 Tutor</button>
          <button @click="quickLogin('admin@edulink.mx')" class="quick-btn">⚙️ Admin</button>
        </div>
      </div>

      <p class="auth-footer">¿No tienes cuenta? <RouterLink to="/register">Regístrate</RouterLink></p>
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
    const data = await auth.login(email.value, password.value)
    redirect(data.user.role)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}

async function quickLogin(e) {
  loading.value = true
  error.value = ''
  try {
    const data = await auth.login(e, 'demo123')
    redirect(data.user.role)
  } catch (err) {
    error.value = 'Error al iniciar sesión demo'
  } finally {
    loading.value = false
  }
}

function redirect(role) {
  if (role === 'admin') router.push('/admin')
  else if (role === 'tutor') router.push('/tutor/dashboard')
  else router.push('/courses')
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: radial-gradient(ellipse at 50% 0%, rgba(245,158,11,0.08), transparent 60%);
}
.auth-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
}
.back-link { font-size: 13px; color: var(--text2); display: block; margin-bottom: 20px; }
.back-link:hover { color: var(--text); text-decoration: none; }
.auth-brand { font-size: 26px; font-weight: 900; color: var(--primary); margin-bottom: 12px; }
h1 { font-size: 24px; font-weight: 800; margin-bottom: 6px; }
.auth-sub { color: var(--text2); font-size: 14px; margin-bottom: 28px; }

.quick-access { margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--border); }
.quick-access p { font-size: 13px; color: var(--text2); margin-bottom: 10px; }
.quick-btns { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.quick-btn {
  padding: 8px 4px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 11px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}
.quick-btn:hover { border-color: var(--primary); background: rgba(245,158,11,0.1); }

.auth-footer { text-align: center; margin-top: 24px; font-size: 14px; color: var(--text2); }
</style>
