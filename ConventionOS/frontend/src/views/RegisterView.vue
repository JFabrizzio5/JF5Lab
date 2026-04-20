<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🎪 ConventionOS</div>
      <h1>Crear Cuenta</h1>
      <p class="auth-sub">Empieza a organizar tu convención hoy</p>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Nombre completo</label>
          <input v-model="name" type="text" placeholder="Tu nombre" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="Mín. 6 caracteres" required minlength="6" />
        </div>
        <div class="form-group">
          <label>Tipo de cuenta</label>
          <select v-model="role">
            <option value="organizer">Organizador — quiero crear convenciones</option>
            <option value="attendee">Asistente — quiero comprar boletos</option>
          </select>
        </div>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? 'Creando...' : 'Crear Cuenta' }}
        </button>
      </form>

      <div class="auth-footer">
        ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link>
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
const name = ref('')
const email = ref('')
const password = ref('')
const role = ref('organizer')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    const user = await auth.register(email.value, name.value, password.value, role.value)
    if (user.role === 'superadmin') router.push('/admin')
    else if (user.role === 'organizer') router.push('/organizer/dashboard')
    else router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear la cuenta'
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
  max-width: 420px;
}
.auth-logo { font-size: 20px; font-weight: 800; margin-bottom: 24px; text-align: center; }
h1 { font-size: 24px; font-weight: 800; margin-bottom: 6px; }
.auth-sub { color: var(--text2); font-size: 14px; margin-bottom: 28px; }
.auth-form { display: flex; flex-direction: column; gap: 16px; margin-bottom: 20px; }
.error-msg { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #ef4444; padding: 10px 14px; border-radius: 8px; font-size: 14px; }
.auth-footer { text-align: center; font-size: 14px; color: var(--text2); }
.auth-footer a { color: var(--primary); font-weight: 600; }
</style>
