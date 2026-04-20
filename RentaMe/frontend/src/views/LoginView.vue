<template>
  <div class="auth-page">
    <div class="auth-card">
      <router-link to="/" class="back-link">← Volver</router-link>
      <div class="auth-logo">
        <span>🏷️</span>
        <h1>RentaMe</h1>
      </div>
      <h2 class="auth-title">Iniciar sesión</h2>
      <p class="auth-sub">Accede a tu panel de rentas</p>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="label">Correo electrónico</label>
          <input v-model="email" type="email" class="input" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label class="label">Contraseña</label>
          <input v-model="password" type="password" class="input" placeholder="••••••••" required />
        </div>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </form>

      <p class="auth-footer">
        ¿No tienes cuenta?
        <router-link to="/register">Regístrate gratis</router-link>
      </p>

      <div class="demo-logins">
        <p class="demo-title">Cuentas demo:</p>
        <div class="demo-btns">
          <button class="demo-btn" @click="fillDemo('barcos@rentame.mx', 'demo123')">
            ⛵ Demo Barcos
          </button>
          <button class="demo-btn" @click="fillDemo('muebles@rentame.mx', 'demo123')">
            🪑 Demo Muebles
          </button>
          <button class="demo-btn" @click="fillDemo('superadmin@rentame.mx', 'demo123')">
            👑 Admin
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

function fillDemo(e, p) {
  email.value = e
  password.value = p
}

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    router.push(authStore.getHome())
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
  padding: 20px;
}

.auth-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
}

.back-link {
  color: var(--text2);
  text-decoration: none;
  font-size: 13px;
  display: block;
  margin-bottom: 24px;
  transition: color 0.2s;
}
.back-link:hover { color: var(--text); }

.auth-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.auth-logo span { font-size: 28px; }
.auth-logo h1 {
  font-size: 22px;
  font-weight: 800;
  background: linear-gradient(135deg, #6366f1, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
}

.auth-sub {
  color: var(--text2);
  font-size: 14px;
  margin-bottom: 28px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.btn-full { width: 100%; justify-content: center; margin-top: 8px; padding: 12px; font-size: 15px; }

.error-msg {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin: 4px 0;
}

.auth-footer {
  text-align: center;
  color: var(--text2);
  font-size: 13px;
  margin-top: 20px;
}
.auth-footer a { color: var(--primary); text-decoration: none; font-weight: 600; }

.demo-logins {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.demo-title {
  font-size: 12px;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  margin-bottom: 10px;
}

.demo-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.demo-btn {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text3);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.demo-btn:hover {
  border-color: var(--primary);
  color: var(--text);
}
</style>
