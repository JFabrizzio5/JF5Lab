<template>
  <div class="landing">
    <div class="hero">
      <div class="hero-badge">✨ Gestión inteligente para tu negocio</div>
      <h1 class="hero-title">Tu negocio en<br /><span class="gradient-text">un solo lugar</span></h1>
      <p class="hero-subtitle">
        NegocioOS unifica tu punto de venta, inventario, clientes y reportes
        con un asistente de inteligencia artificial que te ayuda a crecer.
      </p>

      <div class="demo-section">
        <p class="demo-label">Acceso demo — haz clic para entrar directamente:</p>
        <div class="demo-buttons">
          <button class="demo-btn admin" @click="quickLogin('admin@negocio.mx')">
            <span class="demo-icon">🔑</span>
            <div>
              <div class="demo-role">Administrador</div>
              <div class="demo-email">admin@negocio.mx</div>
            </div>
          </button>
          <button class="demo-btn owner" @click="quickLogin('dueno@negocio.mx')">
            <span class="demo-icon">🏪</span>
            <div>
              <div class="demo-role">Propietario</div>
              <div class="demo-email">dueno@negocio.mx</div>
            </div>
          </button>
          <button class="demo-btn employee" @click="quickLogin('cajero@negocio.mx')">
            <span class="demo-icon">🧑‍💼</span>
            <div>
              <div class="demo-role">Cajero</div>
              <div class="demo-email">cajero@negocio.mx</div>
            </div>
          </button>
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
      </div>

      <div class="hero-links">
        <router-link to="/login" class="btn btn-ghost">Iniciar sesión</router-link>
        <router-link to="/register" class="btn btn-primary">Crear cuenta gratis</router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">🛒</div>
        <h3>Punto de Venta</h3>
        <p>Cobra rápido con búsqueda de productos, carrito intuitivo y múltiples métodos de pago.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📦</div>
        <h3>Inventario Inteligente</h3>
        <p>Control de stock en tiempo real con alertas automáticas cuando el inventario es bajo.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Reportes Visuales</h3>
        <p>Gráficas de ventas diarias, productos top y análisis por método de pago.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>Asistente IA</h3>
        <p>Consulta a tu asesor con IA que analiza tus datos reales y te da recomendaciones accionables.</p>
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

async function quickLogin(email) {
  error.value = ''
  try {
    await auth.login(email, 'demo123')
    router.push('/pos')
  } catch {
    error.value = 'Error al iniciar sesión. Asegúrate que el backend esté corriendo.'
  }
}
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero {
  max-width: 760px;
  margin: 0 auto;
  padding: 80px 24px 60px;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  background: rgba(249,115,22,0.12);
  color: var(--primary);
  border: 1px solid rgba(249,115,22,0.3);
  border-radius: 20px;
  padding: 6px 18px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
}

.hero-title {
  font-size: 56px;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 20px;
}

.gradient-text {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 48px;
  max-width: 560px;
  margin-left: auto;
  margin-right: auto;
}

.demo-section {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 32px;
}

.demo-label {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.demo-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.demo-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--bg3);
  color: var(--text);
  text-align: left;
  transition: all 0.2s;
}

.demo-btn:hover { border-color: var(--primary); transform: translateY(-2px); }
.demo-btn.admin:hover { border-color: #6366f1; }
.demo-btn.owner:hover { border-color: var(--primary); }
.demo-btn.employee:hover { border-color: var(--success); }

.demo-icon { font-size: 24px; }
.demo-role { font-size: 13px; font-weight: 600; }
.demo-email { font-size: 11px; color: var(--text-muted); }

.error-msg {
  margin-top: 12px;
  color: var(--danger);
  font-size: 13px;
}

.hero-links {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.features {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  max-width: 1100px;
  width: 100%;
  padding: 0 24px 80px;
}

.feature-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
  text-align: center;
  transition: border-color 0.2s;
}

.feature-card:hover { border-color: var(--primary); }

.feature-icon { font-size: 32px; margin-bottom: 12px; }
.feature-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.feature-card p { font-size: 13px; color: var(--text-muted); line-height: 1.5; }

@media (max-width: 768px) {
  .hero-title { font-size: 36px; }
  .demo-buttons { grid-template-columns: 1fr; }
  .features { grid-template-columns: repeat(2, 1fr); }
}
</style>
