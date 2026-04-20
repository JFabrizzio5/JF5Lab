<template>
  <div class="auth-page">
    <div class="auth-card">
      <router-link to="/" class="back-link">← Volver</router-link>
      <div class="auth-logo">
        <span>🏷️</span>
        <h1>RentaMe</h1>
      </div>
      <h2 class="auth-title">Crear cuenta</h2>
      <p class="auth-sub">Empieza a rentar en minutos</p>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label class="label">Nombre completo</label>
          <input v-model="form.name" type="text" class="input" placeholder="Tu nombre" required />
        </div>
        <div class="form-group">
          <label class="label">Correo electrónico</label>
          <input v-model="form.email" type="email" class="input" placeholder="tu@email.com" required />
        </div>
        <div class="form-group">
          <label class="label">Contraseña</label>
          <input v-model="form.password" type="password" class="input" placeholder="Mínimo 6 caracteres" required minlength="6" />
        </div>
        <div class="form-group">
          <label class="label">Tipo de cuenta</label>
          <select v-model="form.role" class="input">
            <option value="vendor">Vendedor — Quiero rentar mis artículos</option>
            <option value="customer">Cliente — Quiero rentar artículos</option>
          </select>
        </div>
        <template v-if="form.role === 'vendor'">
          <div class="form-group">
            <label class="label">Nombre de tu negocio</label>
            <input v-model="form.business_name" type="text" class="input" placeholder="Ej: Aqua Adventures" />
          </div>
          <div class="form-group">
            <label class="label">URL de tu landing (slug)</label>
            <div class="slug-preview">
              <span class="slug-prefix">rentame.mx/r/</span>
              <input v-model="form.slug" type="text" class="input slug-input" placeholder="mi-negocio" />
            </div>
          </div>
        </template>

        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? 'Creando cuenta...' : 'Crear cuenta gratis' }}
        </button>
      </form>

      <p class="auth-footer">
        ¿Ya tienes cuenta?
        <router-link to="/login">Iniciar sesión</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'vendor',
  business_name: '',
  slug: '',
})
const error = ref('')
const loading = ref(false)

// Auto-generate slug from business name
watch(() => form.value.business_name, (val) => {
  if (val && !form.value.slug) {
    form.value.slug = val
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .substring(0, 40)
  }
})

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await authStore.register(form.value)
    router.push(authStore.getHome())
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
  padding: 20px;
}

.auth-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 460px;
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

.auth-title { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.auth-sub { color: var(--text2); font-size: 14px; margin-bottom: 28px; }

.auth-form { display: flex; flex-direction: column; gap: 4px; }
.btn-full { width: 100%; justify-content: center; margin-top: 8px; padding: 12px; font-size: 15px; }

.error-msg {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
}

.slug-preview {
  display: flex;
  align-items: center;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.slug-prefix {
  padding: 10px 12px;
  font-size: 13px;
  color: var(--text2);
  border-right: 1px solid var(--border);
  white-space: nowrap;
  background: var(--surface);
}
.slug-input {
  border: none;
  border-radius: 0;
  background: transparent;
}
.slug-input:focus { border-color: transparent; }

.auth-footer {
  text-align: center;
  color: var(--text2);
  font-size: 13px;
  margin-top: 20px;
}
.auth-footer a { color: var(--primary); text-decoration: none; font-weight: 600; }
</style>
