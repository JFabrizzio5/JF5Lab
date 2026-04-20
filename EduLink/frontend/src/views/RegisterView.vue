<template>
  <div class="auth-page">
    <div class="auth-card">
      <RouterLink to="/" class="back-link">← Volver al inicio</RouterLink>
      <div class="auth-brand">🎓 EduLink</div>
      <h1>Crear Cuenta</h1>
      <p class="auth-sub">Únete a la comunidad universitaria</p>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Nombre completo</label>
          <input v-model="form.name" type="text" placeholder="Tu nombre" required />
        </div>
        <div class="form-group">
          <label>Correo electrónico</label>
          <input v-model="form.email" type="email" placeholder="tu@correo.mx" required />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="form.password" type="password" placeholder="Mínimo 6 caracteres" required minlength="6" />
        </div>
        <div class="form-group">
          <label>Rol</label>
          <select v-model="form.role">
            <option value="student">Estudiante</option>
            <option value="tutor">Tutor</option>
          </select>
        </div>
        <div class="form-group">
          <label>Universidad</label>
          <select v-model="form.school">
            <option value="UNAM">UNAM</option>
            <option value="UAM">UAM</option>
            <option value="IPN">IPN</option>
            <option value="POLI">POLI</option>
            <option value="ITESM">ITESM</option>
            <option value="OTHER">Otra</option>
          </select>
        </div>
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? 'Registrando...' : 'Crear Cuenta' }}
        </button>
      </form>

      <p class="auth-footer">¿Ya tienes cuenta? <RouterLink to="/login">Iniciar sesión</RouterLink></p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const error = ref('')
const loading = ref(false)

const form = reactive({
  name: '',
  email: '',
  password: '',
  role: 'student',
  school: 'UNAM'
})

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    const data = await auth.register(form)
    const role = data.user.role
    if (role === 'tutor') router.push('/tutor/dashboard')
    else router.push('/courses')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al registrarse'
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
  padding: 20px;
  background: radial-gradient(ellipse at 50% 0%, rgba(16,185,129,0.06), transparent 60%);
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
.auth-footer { text-align: center; margin-top: 24px; font-size: 14px; color: var(--text2); }
</style>
