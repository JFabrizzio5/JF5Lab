<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🏠 RentaFácil</div>
      <h1>Crear cuenta</h1>
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Nombre completo</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="form-group">
          <label>Correo electrónico</label>
          <input v-model="form.email" type="email" required autocomplete="email" />
        </div>
        <div class="form-group">
          <label>Teléfono (opcional)</label>
          <input v-model="form.phone" type="tel" />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input v-model="form.password" type="password" required minlength="8" />
        </div>
        <p v-if="authStore.error" class="error-msg">{{ authStore.error }}</p>
        <button class="btn btn-primary full-width" type="submit" :disabled="authStore.loading">
          {{ authStore.loading ? 'Creando cuenta...' : 'Registrarse' }}
        </button>
      </form>
      <p class="auth-link">¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const form = reactive({ name: '', email: '', phone: '', password: '' })

async function submit() {
  try {
    await authStore.register(form.email, form.password, form.name, form.phone || null)
    router.push('/dashboard')
  } catch {}
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f7fa; }
.auth-card { background: #fff; border-radius: 16px; padding: 40px; width: 100%; max-width: 400px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); display: flex; flex-direction: column; gap: 20px; }
.auth-logo { font-size: 1.4rem; font-weight: 700; text-align: center; }
h1 { font-size: 1.2rem; font-weight: 600; text-align: center; color: #374151; }
form { display: flex; flex-direction: column; gap: 16px; }
.full-width { width: 100%; justify-content: center; }
.auth-link { text-align: center; font-size: 0.85rem; color: #64748b; }
.auth-link a { color: #4f46e5; font-weight: 500; text-decoration: none; }
</style>
