<template>
  <div class="auth-page">
    <div class="auth-card">
      <router-link to="/" class="back">
        <i data-lucide="arrow-left" style="width:14px;height:14px"></i> Inicio
      </router-link>
      <div class="logo-mark">
        <i data-lucide="layers" style="width:22px;height:22px;color:white"></i>
      </div>
      <h2>Bienvenido de vuelta</h2>
      <p class="sub">Ingresa a tu workspace HubOS.</p>

      <form @submit.prevent="handleLogin" autocomplete="on">
        <div class="form-group">
          <label for="login-email">Email</label>
          <input
            id="login-email"
            name="email"
            type="email"
            autocomplete="username"
            v-model="email"
            placeholder="tu@email.com"
            required
          />
        </div>
        <div class="form-group">
          <label for="login-password">Contraseña</label>
          <input
            id="login-password"
            name="password"
            type="password"
            autocomplete="current-password"
            v-model="password"
            placeholder="••••••••"
            required
          />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? 'Ingresando…' : 'Ingresar' }}
        </button>
      </form>

      <div class="foot">
        ¿No tienes cuenta? <router-link to="/register">Regístrate</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const email = ref('admin@hubos.dev')
const password = ref('admin123')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al ingresar'
  } finally {
    loading.value = false
  }
}
onMounted(() => { if (window.lucide) window.lucide.createIcons() })
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(circle at 20% 20%, rgba(99,102,241,0.18), transparent 60%),
    radial-gradient(circle at 80% 80%, rgba(6,182,212,0.14), transparent 55%),
    var(--bg);
  padding: 1rem;
}
.auth-card {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
}
.back {
  position: absolute;
  top: 1rem;
  left: 1rem;
  color: var(--text3);
  font-size: 0.78rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.back:hover { color: var(--text); }
.logo-mark {
  width: 44px;
  height: 44px;
  border-radius: 11px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.2rem;
}
h2 { font-size: 1.4rem; font-weight: 800; margin-bottom: 0.4rem; }
.sub { color: var(--text2); font-size: 0.88rem; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 0.9rem; }
.form-group label { display: block; font-size: 0.8rem; color: var(--text2); margin-bottom: 0.35rem; font-weight: 500; }
.w-full { width: 100%; justify-content: center; margin-top: 0.3rem; }
.error-msg {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #ef4444;
  padding: 0.55rem 0.8rem;
  border-radius: 8px;
  font-size: 0.8rem;
  margin-bottom: 0.75rem;
}
.foot { text-align: center; margin-top: 1.25rem; font-size: 0.82rem; color: var(--text2); }
.foot a { color: var(--primary); font-weight: 600; }
</style>
