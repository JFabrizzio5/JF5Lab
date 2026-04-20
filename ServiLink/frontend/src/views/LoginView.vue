<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">⚡ ServiLink</div>
      <h1 class="auth-title">Bienvenido de vuelta</h1>
      <p class="auth-sub">Servicios profesionales cerca de ti</p>

      <div v-if="error" class="alert-error">{{ error }}</div>

      <div class="demo-accounts">
        <p class="demo-title">Cuentas demo:</p>
        <button @click="fillDemo('admin')" class="demo-btn">👑 Admin</button>
        <button @click="fillDemo('client')" class="demo-btn">👤 Cliente</button>
        <button @click="fillDemo('freelancer')" class="demo-btn">🔧 Freelancer</button>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label class="label">Email</label>
          <input v-model="form.email" type="email" class="input" placeholder="tu@email.com" required />
        </div>
        <div class="field">
          <label class="label">Contraseña</label>
          <input v-model="form.password" type="password" class="input" placeholder="••••••••" required />
        </div>
        <button type="submit" class="btn btn-primary btn-lg" style="width:100%;justify-content:center;" :disabled="loading">
          {{ loading ? 'Entrando...' : 'Iniciar sesión' }}
        </button>
      </form>

      <p class="auth-link">¿No tienes cuenta? <router-link to="/register">Regístrate</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

const demos = {
  admin: { email: 'admin@servilink.com', password: 'admin123' },
  client: { email: 'cliente@servilink.com', password: 'cliente123' },
  freelancer: { email: 'freelancer@servilink.com', password: 'freelancer123' },
}

async function fillDemo(type) {
  form.value = { ...demos[type] }
  await handleLogin()
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    const user = await auth.login(form.value.email, form.value.password)
    const redirects = { superadmin: '/admin', freelancer: '/dashboard', client: '/marketplace' }
    router.push(redirects[user.role] || '/marketplace')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.15) 0%, transparent 60%); }
.auth-card { width: 100%; max-width: 420px; background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 40px; }
.auth-logo { font-size: 28px; font-weight: 900; color: var(--primary); text-align: center; margin-bottom: 16px; }
.auth-title { font-size: 22px; font-weight: 700; text-align: center; }
.auth-sub { color: var(--text2); text-align: center; margin-bottom: 24px; font-size: 14px; }
.field { margin-bottom: 16px; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 10px 14px; font-size: 14px; color: var(--danger); margin-bottom: 16px; }
.auth-link { text-align: center; margin-top: 20px; font-size: 14px; color: var(--text2); }
.auth-link a { color: var(--primary); text-decoration: none; }
.demo-accounts { background: var(--bg3); border-radius: 8px; padding: 12px; margin-bottom: 20px; display: flex; flex-direction: column; gap: 8px; }
.demo-title { font-size: 12px; color: var(--text2); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.demo-accounts { display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px; align-items: center; }
.demo-title { width: 100%; }
.demo-btn { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 6px 12px; color: var(--text); cursor: pointer; font-size: 13px; transition: border-color 0.2s; }
.demo-btn:hover { border-color: var(--primary); }
</style>
