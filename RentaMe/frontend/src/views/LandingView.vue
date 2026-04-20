<template>
  <div class="landing">
    <!-- NAV -->
    <nav class="nav">
      <div class="nav-inner">
        <div class="nav-logo">
          <span>🏷️</span>
          <span class="logo-text">RentaMe</span>
        </div>
        <div class="nav-actions">
          <router-link to="/login" class="btn btn-secondary btn-sm">Iniciar sesión</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Crear mi página →</router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-glow glow-1"></div>
        <div class="hero-glow glow-2"></div>
      </div>
      <div class="hero-content">
        <div class="hero-badge">✨ Plataforma de rentas profesional</div>
        <h1 class="hero-title">
          Renta cualquier cosa,<br />
          <span class="gradient-text">crea tu negocio digital</span>
        </h1>
        <p class="hero-sub">
          Barcos · Vehículos · Muebles · Equipo · Lo que sea<br />
          Tu propia landing profesional lista en minutos, sin código.
        </p>
        <div class="hero-ctas">
          <router-link to="/register" class="btn btn-accent hero-btn">
            Crear mi página gratis →
          </router-link>
          <a href="/r/aqua-adventures" target="_blank" class="btn btn-secondary hero-btn">
            Ver demo live ↗
          </a>
        </div>
        <p class="hero-note">Sin costo de setup · Tu propio link /r/tu-negocio</p>
      </div>

      <!-- Mockup -->
      <div class="hero-mockup">
        <div class="mockup-browser">
          <div class="mockup-bar">
            <div class="mockup-dots">
              <span></span><span></span><span></span>
            </div>
            <div class="mockup-url">rentame.mx/r/aqua-adventures</div>
          </div>
          <div class="mockup-screen">
            <div class="mockup-cover" style="background: linear-gradient(135deg, #0ea5e9, #0c4a6e)">
              <div class="mockup-vendor-name">Aqua Adventures</div>
              <div class="mockup-tagline">Vive el mar como nunca antes</div>
            </div>
            <div class="mockup-items">
              <div class="mockup-item" v-for="i in 3" :key="i">
                <div class="mockup-item-img"></div>
                <div class="mockup-item-info">
                  <div class="mockup-item-name"></div>
                  <div class="mockup-item-price"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CATEGORÍAS -->
    <section class="categories-section">
      <div class="section-inner">
        <p class="categories-label">Lo que los vendedores rentan en RentaMe</p>
        <div class="categories-chips">
          <div class="cat-chip" v-for="cat in categories" :key="cat.name">
            <span>{{ cat.icon }}</span>
            <span>{{ cat.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES BENTO -->
    <section class="features-section">
      <div class="section-inner">
        <h2 class="section-title">Todo lo que necesitas para rentar</h2>
        <p class="section-sub">Una plataforma completa. Tu marca, tu link, tus clientes.</p>
        <div class="bento-grid">
          <div class="bento-card bento-wide">
            <div class="bento-icon">🎨</div>
            <h3>Landing personalizada con tus colores</h3>
            <p>Tu logo, tu paleta de color, tu foto de portada. Una landing que se ve como tu marca, no como plantilla genérica.</p>
          </div>
          <div class="bento-card">
            <div class="bento-icon">📅</div>
            <h3>Calendario de disponibilidad</h3>
            <p>Bloquea fechas, gestiona horarios y nunca pierdas una renta por doble reserva.</p>
          </div>
          <div class="bento-card">
            <div class="bento-icon">💬</div>
            <h3>Contacto directo por WhatsApp</h3>
            <p>Cada solicitud se redirige a tu WhatsApp con el mensaje listo. Cierras ventas más rápido.</p>
          </div>
          <div class="bento-card">
            <div class="bento-icon">💳</div>
            <h3>Pagos con Stripe automáticos</h3>
            <p>Recibe pagos en tu cuenta bancaria. La plataforma descuenta su comisión automáticamente.</p>
          </div>
          <div class="bento-card">
            <div class="bento-icon">📱</div>
            <h3>Comparte tu link en redes</h3>
            <p>Un solo link para compartir en Instagram, TikTok, Facebook y WhatsApp. Así de simple.</p>
          </div>
          <div class="bento-card">
            <div class="bento-icon">📊</div>
            <h3>Dashboard con tus reservas</h3>
            <p>Kanban de reservas, estadísticas del mes, historial de pagos. Tu negocio bajo control.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CÓMO FUNCIONA -->
    <section class="how-section">
      <div class="section-inner">
        <h2 class="section-title">¿Cómo funciona?</h2>
        <p class="section-sub">Tres pasos para tener tu negocio digital listo</p>
        <div class="steps">
          <div class="step" v-for="(step, i) in steps" :key="i">
            <div class="step-num">{{ i + 1 }}</div>
            <div class="step-icon">{{ step.icon }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </div>
          <div class="step-connector"></div>
          <div class="step-connector"></div>
        </div>
      </div>
    </section>

    <!-- DEMO LOGINS -->
    <section class="demo-section">
      <div class="section-inner">
        <h2 class="section-title">Pruébalo ahora</h2>
        <p class="section-sub">Ingresa con una cuenta demo y explora la plataforma</p>
        <div class="demo-cards">
          <div class="demo-card" @click="goDemo('barcos@rentame.mx')">
            <div class="demo-card-icon">⛵</div>
            <h3>Demo Vendedor (Barcos)</h3>
            <p>Aqua Adventures — Acapulco</p>
            <div class="demo-card-creds">barcos@rentame.mx / demo123</div>
            <div class="demo-btn-inner">Acceder →</div>
          </div>
          <div class="demo-card" @click="goDemo('muebles@rentame.mx')">
            <div class="demo-card-icon">🪑</div>
            <h3>Demo Vendedor (Muebles)</h3>
            <p>Renta Muebles MX — CDMX</p>
            <div class="demo-card-creds">muebles@rentame.mx / demo123</div>
            <div class="demo-btn-inner">Acceder →</div>
          </div>
          <div class="demo-card" @click="goDemo('superadmin@rentame.mx')">
            <div class="demo-card-icon">👑</div>
            <h3>Super Admin</h3>
            <p>Panel de administración global</p>
            <div class="demo-card-creds">superadmin@rentame.mx / demo123</div>
            <div class="demo-btn-inner">Acceder →</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA FINAL -->
    <section class="cta-section">
      <div class="cta-glow"></div>
      <div class="section-inner">
        <h2 class="cta-title">Empieza gratis hoy</h2>
        <p class="cta-sub">Crea tu página de rentas profesional en menos de 5 minutos</p>
        <router-link to="/register" class="btn btn-accent cta-btn">
          Crear mi página gratis →
        </router-link>
        <p class="cta-note">Sin tarjeta de crédito · Sin código · Cancela cuando quieras</p>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="section-inner">
        <div class="footer-logo">
          <span>🏷️</span>
          <span class="logo-text">RentaMe</span>
        </div>
        <p class="footer-copy">© 2024 RentaMe. Tu plataforma de rentas profesional.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const categories = [
  { icon: '⛵', name: 'Barcos' },
  { icon: '🚗', name: 'Vehículos' },
  { icon: '🪑', name: 'Muebles' },
  { icon: '🎉', name: 'Fiestas' },
  { icon: '⚽', name: 'Deportes' },
  { icon: '🏠', name: 'Inmuebles' },
  { icon: '🔧', name: 'Equipo' },
  { icon: '🛶', name: 'Kayaks' },
  { icon: '🏄', name: 'Motos de agua' },
  { icon: '📷', name: 'Cámaras' },
  { icon: '🎸', name: 'Instrumentos' },
  { icon: '🎪', name: 'Carpas' },
]

const steps = [
  {
    icon: '✏️',
    title: 'Crea tu cuenta',
    desc: 'Regístrate gratis, elige tu slug y personaliza tu landing con tus colores y logo.',
  },
  {
    icon: '📦',
    title: 'Agrega tus artículos',
    desc: 'Sube fotos, describe lo que rentas, define precios por hora, día o semana.',
  },
  {
    icon: '🚀',
    title: 'Comparte tu link',
    desc: 'Pega tu link /r/tu-negocio en redes. Los clientes reservan y tú recibes notificaciones.',
  },
]

async function goDemo(email) {
  try {
    await authStore.login(email, 'demo123')
    router.push(authStore.getHome())
  } catch (e) {
    router.push(`/login`)
  }
}
</script>

<style scoped>
.landing {
  background: var(--bg);
  color: var(--text);
}

/* NAV */
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(7, 7, 13, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
}
.logo-text {
  font-size: 20px;
  font-weight: 800;
  background: linear-gradient(135deg, #6366f1, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-actions { display: flex; align-items: center; gap: 10px; }

/* HERO */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 120px 24px 80px;
  position: relative;
  overflow: hidden;
  text-align: center;
}
.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.hero-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}
.glow-1 {
  width: 600px;
  height: 600px;
  background: #6366f1;
  top: -100px;
  left: -100px;
}
.glow-2 {
  width: 500px;
  height: 500px;
  background: #f59e0b;
  bottom: -100px;
  right: -100px;
}
.hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
}
.hero-badge {
  display: inline-block;
  background: rgba(99, 102, 241, 0.12);
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: #818cf8;
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
}
.hero-title {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 20px;
}
.gradient-text {
  background: linear-gradient(135deg, #6366f1, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 18px;
  color: var(--text3);
  margin-bottom: 36px;
  line-height: 1.7;
}
.hero-ctas {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
.hero-btn {
  padding: 14px 28px;
  font-size: 16px;
}
.hero-note {
  margin-top: 16px;
  font-size: 12px;
  color: var(--text2);
}

/* MOCKUP */
.hero-mockup {
  margin-top: 60px;
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 580px;
}
.mockup-browser {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.6);
}
.mockup-bar {
  background: var(--bg3);
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border);
}
.mockup-dots { display: flex; gap: 6px; }
.mockup-dots span { width: 10px; height: 10px; border-radius: 50%; background: var(--surface); }
.mockup-url { font-size: 12px; color: var(--text2); }
.mockup-screen { padding: 0; }
.mockup-cover {
  height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.mockup-vendor-name { font-size: 18px; font-weight: 700; color: white; }
.mockup-tagline { font-size: 13px; color: rgba(255,255,255,0.7); }
.mockup-items { display: flex; gap: 12px; padding: 16px; }
.mockup-item {
  flex: 1;
  background: var(--bg3);
  border-radius: 8px;
  overflow: hidden;
}
.mockup-item-img {
  height: 70px;
  background: linear-gradient(135deg, var(--surface), var(--bg));
}
.mockup-item-info { padding: 8px; }
.mockup-item-name {
  height: 8px;
  background: var(--surface);
  border-radius: 4px;
  margin-bottom: 6px;
}
.mockup-item-price {
  height: 6px;
  width: 60%;
  background: rgba(99, 102, 241, 0.3);
  border-radius: 4px;
}

/* SECTIONS */
.section-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}
.section-title {
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 700;
  text-align: center;
  margin-bottom: 10px;
}
.section-sub {
  text-align: center;
  color: var(--text2);
  font-size: 16px;
  margin-bottom: 48px;
}

/* CATEGORIES */
.categories-section { padding: 40px 0; border-top: 1px solid var(--border); }
.categories-label {
  text-align: center;
  font-size: 13px;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
  margin-bottom: 20px;
}
.categories-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}
.cat-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 6px 14px;
  font-size: 13px;
  color: var(--text3);
}

/* BENTO */
.features-section { padding: 80px 0; }
.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.bento-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  transition: border-color 0.2s, transform 0.2s;
}
.bento-card:hover {
  border-color: var(--border2);
  transform: translateY(-2px);
}
.bento-wide { grid-column: span 2; }
.bento-icon { font-size: 28px; margin-bottom: 12px; }
.bento-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.bento-card p { font-size: 14px; color: var(--text2); line-height: 1.6; }

/* HOW */
.how-section { padding: 80px 0; }
.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  position: relative;
}
.step {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  text-align: center;
}
.step-num {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
  color: white;
  margin: 0 auto 12px;
}
.step-icon { font-size: 28px; margin-bottom: 12px; }
.step h3 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.step p { font-size: 14px; color: var(--text2); line-height: 1.6; }

/* DEMO */
.demo-section { padding: 80px 0; }
.demo-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.demo-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}
.demo-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
}
.demo-card-icon { font-size: 36px; margin-bottom: 12px; }
.demo-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.demo-card p { font-size: 13px; color: var(--text2); margin-bottom: 12px; }
.demo-card-creds {
  font-size: 11px;
  color: var(--text2);
  background: var(--bg3);
  border-radius: 6px;
  padding: 6px 10px;
  margin-bottom: 16px;
  font-family: monospace;
}
.demo-btn-inner {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

/* CTA FINAL */
.cta-section {
  padding: 100px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.cta-glow {
  position: absolute;
  width: 800px;
  height: 400px;
  background: radial-gradient(ellipse, rgba(99, 102, 241, 0.15), transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}
.cta-title {
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 800;
  margin-bottom: 16px;
}
.cta-sub {
  font-size: 18px;
  color: var(--text2);
  margin-bottom: 36px;
}
.cta-btn { padding: 16px 36px; font-size: 17px; }
.cta-note {
  margin-top: 16px;
  font-size: 13px;
  color: var(--text2);
}

/* FOOTER */
.footer {
  padding: 40px 0;
  border-top: 1px solid var(--border);
  text-align: center;
}
.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 18px;
  margin-bottom: 12px;
}
.footer-copy { font-size: 13px; color: var(--text2); }

@media (max-width: 768px) {
  .bento-grid { grid-template-columns: 1fr; }
  .bento-wide { grid-column: span 1; }
  .steps { grid-template-columns: 1fr; }
  .demo-cards { grid-template-columns: 1fr; }
  .hero-ctas { flex-direction: column; align-items: center; }
  .mockup-items { flex-direction: column; }
}
</style>
