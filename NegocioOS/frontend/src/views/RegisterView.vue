<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🏪 NegocioOS</div>
      <h2>Crear cuenta</h2>
      <p class="auth-sub">Empieza a gestionar tu negocio hoy</p>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Nombre completo</label>
          <input v-model="form.name" type="text" placeholder="Juan García" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label>Nombre del negocio</label>
          <input v-model="form.business_name" type="text" placeholder="Mi Tienda" />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required minlength="6" />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? 'Creando...' : 'Crear cuenta' }}
        </button>
      </form>

      <div class="auth-footer">
        ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link>
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
const error = ref('')
const loading = ref(false)
const form = ref({ name: '', email: '', password: '', business_name: '' })

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(form.value)
    router.push('/pos')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear cuenta'
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
.auth-footer { text-align: center; margin-top: 24px; font-size: 13px; color: var(--text-muted); }
.auth-footer a { color: var(--primary); }
</style>
