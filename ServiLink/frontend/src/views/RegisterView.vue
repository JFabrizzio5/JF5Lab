<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">⚡ ServiLink</div>
      <h1 class="auth-title">Crear cuenta</h1>

      <div v-if="error" class="alert-error">{{ error }}</div>

      <form @submit.prevent="handleRegister">
        <div class="field">
          <label class="label">Nombre completo</label>
          <input v-model="form.name" class="input" placeholder="Tu nombre" required />
        </div>
        <div class="field">
          <label class="label">Email</label>
          <input v-model="form.email" type="email" class="input" placeholder="tu@email.com" required />
        </div>
        <div class="field">
          <label class="label">Teléfono</label>
          <input v-model="form.phone" class="input" placeholder="+52 55 0000 0000" />
        </div>
        <div class="field">
          <label class="label">Contraseña</label>
          <input v-model="form.password" type="password" class="input" placeholder="Mínimo 6 caracteres" required />
        </div>
        <div class="field">
          <label class="label">Tipo de cuenta</label>
          <div class="role-select">
            <button type="button" @click="form.role = 'client'" :class="['role-btn', form.role === 'client' && 'active']">
              👤 Cliente
            </button>
            <button type="button" @click="form.role = 'freelancer'" :class="['role-btn', form.role === 'freelancer' && 'active']">
              🔧 Profesional
            </button>
          </div>
        </div>
        <button type="submit" class="btn btn-primary btn-lg" style="width:100%;justify-content:center;" :disabled="loading">
          {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
        </button>
      </form>

      <p class="auth-link">¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const form = ref({ name: '', email: '', password: '', phone: '', role: 'client' })
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    const user = await auth.register(form.value)
    const redirects = { freelancer: '/dashboard', client: '/marketplace' }
    router.push(redirects[user.role] || '/marketplace')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear cuenta'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.15) 0%, transparent 60%); }
.auth-card { width: 100%; max-width: 420px; background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 40px; }
.auth-logo { font-size: 28px; font-weight: 900; color: var(--primary); text-align: center; margin-bottom: 16px; }
.auth-title { font-size: 22px; font-weight: 700; text-align: center; margin-bottom: 24px; }
.field { margin-bottom: 16px; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 10px 14px; font-size: 14px; color: var(--danger); margin-bottom: 16px; }
.auth-link { text-align: center; margin-top: 20px; font-size: 14px; color: var(--text2); }
.auth-link a { color: var(--primary); text-decoration: none; }
.role-select { display: flex; gap: 8px; }
.role-btn { flex: 1; padding: 10px; background: var(--bg3); border: 1px solid var(--border); border-radius: 8px; color: var(--text2); cursor: pointer; font-size: 14px; transition: all 0.2s; }
.role-btn.active { border-color: var(--primary); color: var(--primary); background: rgba(99,102,241,0.1); }
</style>
