<template>
  <div class="landing">
    <!-- Nav -->
    <nav class="landing-nav">
      <div class="nav-brand">
        <span class="brand-icon">🏛️</span>
        <span class="brand-name">SalonOS</span>
      </div>
      <div class="nav-actions">
        <router-link to="/login" class="btn btn-ghost btn-sm">Iniciar sesión</router-link>
        <router-link to="/register" class="btn btn-primary btn-sm">Comenzar gratis</router-link>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-badge">✨ White-label CRM para salones de eventos</div>
      <h1 class="hero-title">
        Crea la presencia digital<br />de tu <span class="gradient-text">salón de eventos</span>
      </h1>
      <p class="hero-subtitle">
        Landing personalizada, mapa de sucursales, CRM de clientes, chat en tiempo real
        y pagos con Stripe Connect — todo en una plataforma.
      </p>
      <div class="hero-ctas">
        <router-link to="/register" class="btn btn-primary">Crear mi salón gratis →</router-link>
        <a href="/v/jardines-del-valle" class="btn btn-ghost">Ver demo en vivo</a>
      </div>
      <div class="hero-demo-img">
        <img src="https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200&h=600&fit=crop" alt="Demo" />
        <div class="hero-img-overlay"></div>
      </div>
    </section>

    <!-- Features -->
    <section class="features">
      <div class="features-header">
        <h2>Todo lo que tu salón necesita</h2>
        <p>Una plataforma completa para gestionar tu negocio de eventos</p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🌐</div>
          <h3>Landing personalizada</h3>
          <p>Tu propio sitio web con tu logo, colores, galería, descripción y formulario de contacto. URL única /v/tu-salon.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🗺️</div>
          <h3>Mapa de sucursales</h3>
          <p>Muestra todas tus ubicaciones en un mapa interactivo con Leaflet. Clientes te encuentran fácilmente.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">👥</div>
          <h3>CRM de clientes</h3>
          <p>Gestiona prospectos, historial de eventos, notas y seguimiento desde un solo panel.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>Chat en tiempo real</h3>
          <p>Comunícate con tus clientes directamente desde el CRM. También botón de WhatsApp integrado.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💳</div>
          <h3>Pagos con Stripe Connect</h3>
          <p>Recibe depósitos y pagos directamente en tu cuenta. Nosotros solo retenemos un pequeño porcentaje.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>Calendario de eventos</h3>
          <p>Vista mensual de todos tus eventos. Nunca pierdas una reservación.</p>
        </div>
      </div>
    </section>

    <!-- Demo logins -->
    <section class="demo-section">
      <h2>Prueba el demo ahora</h2>
      <p>Accede con cualquiera de estas cuentas demo (contraseña: <code>demo123</code>)</p>
      <div class="demo-cards">
        <div class="demo-card" @click="quickLogin('admin@salonos.mx')">
          <div class="demo-badge admin">Super Admin</div>
          <div class="demo-email">admin@salonos.mx</div>
          <div class="demo-desc">Gestión de todos los venues, panel global</div>
          <button class="btn btn-ghost btn-sm" :disabled="logging">
            {{ logging === 'admin@salonos.mx' ? 'Entrando...' : 'Entrar como Admin →' }}
          </button>
        </div>
        <div class="demo-card featured" @click="quickLogin('dueno@jardines.mx')">
          <div class="demo-badge owner">Propietario</div>
          <div class="demo-email">dueno@jardines.mx</div>
          <div class="demo-desc">Dueño de "Jardines del Valle" — CRM completo</div>
          <button class="btn btn-primary btn-sm" :disabled="logging">
            {{ logging === 'dueno@jardines.mx' ? 'Entrando...' : 'Entrar como Dueño →' }}
          </button>
        </div>
        <div class="demo-card" @click="quickLogin('cliente@test.mx')">
          <div class="demo-badge client">Cliente</div>
          <div class="demo-email">cliente@test.mx</div>
          <div class="demo-desc">Vista pública del venue</div>
          <button class="btn btn-ghost btn-sm" :disabled="logging">
            {{ logging === 'cliente@test.mx' ? 'Entrando...' : 'Entrar como Cliente →' }}
          </button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="footer-brand">
        <span class="brand-icon">🏛️</span>
        <span class="brand-name">SalonOS</span>
      </div>
      <p>© 2024 SalonOS. Plataforma white-label para salones de eventos.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const logging = ref(null)

const ROLE_HOME = {
  superadmin: '/admin',
  venue_owner: '/dashboard',
  venue_staff: '/dashboard',
  client: '/',
}

async function quickLogin(email) {
  if (logging.value) return
  logging.value = email
  try {
    const user = await auth.login(email, 'demo123')
    router.push(ROLE_HOME[user.role] || '/')
  } catch (e) {
    alert('Error al iniciar sesión demo')
  } finally {
    logging.value = null
  }
}
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
}

.landing-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 2rem;
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10,10,15,0.9);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1.25rem;
  font-weight: 800;
}

.brand-icon { font-size: 1.5rem; }

.brand-name {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-actions { display: flex; gap: 0.75rem; align-items: center; }

.hero {
  text-align: center;
  padding: 6rem 2rem 4rem;
  max-width: 900px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-block;
  background: rgba(124,58,237,0.15);
  border: 1px solid rgba(124,58,237,0.3);
  color: #a78bfa;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 2rem;
}

.hero-title {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: var(--text2);
  max-width: 600px;
  margin: 0 auto 2.5rem;
  line-height: 1.7;
}

.hero-ctas {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}

.hero-demo-img {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border);
}

.hero-demo-img img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  display: block;
}

.hero-img-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, var(--bg) 0%, transparent 50%);
}

.features {
  padding: 5rem 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

.features-header {
  text-align: center;
  margin-bottom: 3rem;
}

.features-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
}

.features-header p {
  color: var(--text2);
  font-size: 1.1rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  transition: border-color 0.2s;
}

.feature-card:hover { border-color: rgba(124,58,237,0.4); }

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: var(--text2);
  font-size: 0.9rem;
  line-height: 1.6;
}

.demo-section {
  padding: 5rem 2rem;
  text-align: center;
  background: var(--bg2);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.demo-section h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
}

.demo-section p {
  color: var(--text2);
  margin-bottom: 2.5rem;
}

.demo-section code {
  background: rgba(124,58,237,0.2);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: #a78bfa;
}

.demo-cards {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 900px;
  margin: 0 auto;
}

.demo-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  width: 260px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.demo-card:hover {
  border-color: rgba(124,58,237,0.4);
  transform: translateY(-2px);
}

.demo-card.featured {
  border-color: rgba(124,58,237,0.5);
  background: rgba(124,58,237,0.05);
}

.demo-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.demo-badge.admin { background: rgba(239,68,68,0.2); color: #f87171; }
.demo-badge.owner { background: rgba(124,58,237,0.2); color: #a78bfa; }
.demo-badge.client { background: rgba(16,185,129,0.2); color: #34d399; }

.demo-email {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.demo-desc {
  font-size: 0.82rem;
  color: var(--text2);
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.landing-footer {
  padding: 3rem 2rem;
  text-align: center;
  border-top: 1px solid var(--border);
  color: var(--text2);
}

.landing-footer .nav-brand {
  justify-content: center;
  margin-bottom: 0.75rem;
}

.landing-footer p { font-size: 0.85rem; }
</style>
