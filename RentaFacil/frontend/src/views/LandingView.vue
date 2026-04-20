<template>
  <div class="landing">
    <!-- Nav -->
    <nav class="nav" :class="{ scrolled: scrolled }">
      <div class="nav-inner">
        <div class="nav-logo">🏠 RentaFácil</div>
        <div class="nav-links">
          <a href="#features">Características</a>
          <a href="#how">Cómo funciona</a>
          <a href="#pricing">Precios</a>
        </div>
        <div class="nav-cta">
          <router-link to="/login" class="btn-ghost">Iniciar sesión</router-link>
          <router-link to="/register" class="btn-cta">Empezar gratis →</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-grid-bg"></div>
      <div class="hero-glow hero-glow-1"></div>
      <div class="hero-glow hero-glow-2"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          Gestión de rentas sin complicaciones
        </div>
        <h1 class="hero-title">
          Administra tus<br />
          <span class="gradient-text">propiedades en renta</span><br />
          como un profesional
        </h1>
        <p class="hero-sub">
          Contratos digitales, control de pagos, gestión de inquilinos y reportes en tiempo real.
          Todo en un solo lugar, sin hojas de cálculo.
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="btn-hero-primary">
            Comenzar gratis
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </router-link>
          <router-link to="/login" class="btn-hero-secondary">
            Ver demo en vivo
          </router-link>
        </div>
        <div class="hero-stats">
          <div class="hero-stat"><span class="stat-n">+2,400</span><span class="stat-l">Propiedades activas</span></div>
          <div class="hero-stat-div"></div>
          <div class="hero-stat"><span class="stat-n">98%</span><span class="stat-l">Satisfacción</span></div>
          <div class="hero-stat-div"></div>
          <div class="hero-stat"><span class="stat-n">$0</span><span class="stat-l">Para empezar</span></div>
        </div>
      </div>

      <!-- Dashboard mockup -->
      <div class="hero-mockup">
        <div class="mockup-window">
          <div class="mockup-bar">
            <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
          </div>
          <div class="mockup-content">
            <div class="mockup-sidebar">
              <div class="mock-logo">🏠</div>
              <div class="mock-nav-item active">📊 Dashboard</div>
              <div class="mock-nav-item">🏠 Propiedades</div>
              <div class="mock-nav-item">👥 Inquilinos</div>
              <div class="mock-nav-item">📄 Contratos</div>
              <div class="mock-nav-item">💳 Pagos</div>
            </div>
            <div class="mockup-main">
              <div class="mock-stats">
                <div class="mock-stat-card" style="--c:#f59e0b">
                  <div class="mock-stat-val">12</div>
                  <div class="mock-stat-lbl">Propiedades</div>
                </div>
                <div class="mock-stat-card" style="--c:#10b981">
                  <div class="mock-stat-val">$48,000</div>
                  <div class="mock-stat-lbl">Renta mensual</div>
                </div>
                <div class="mock-stat-card" style="--c:#6366f1">
                  <div class="mock-stat-val">8</div>
                  <div class="mock-stat-lbl">Inquilinos</div>
                </div>
              </div>
              <div class="mock-table-header">Pagos recientes</div>
              <div class="mock-row"><div class="mock-avatar"></div><div class="mock-info"><div class="mock-name"></div><div class="mock-date"></div></div><div class="mock-amount green"></div></div>
              <div class="mock-row"><div class="mock-avatar" style="background:#6366f1"></div><div class="mock-info"><div class="mock-name"></div><div class="mock-date"></div></div><div class="mock-amount green"></div></div>
              <div class="mock-row"><div class="mock-avatar" style="background:#f59e0b"></div><div class="mock-info"><div class="mock-name"></div><div class="mock-date"></div></div><div class="mock-amount yellow"></div></div>
            </div>
          </div>
        </div>
        <div class="mockup-float float-1">
          <span>✓</span> Contrato firmado
        </div>
        <div class="mockup-float float-2">
          <span>💳</span> Pago recibido $8,500
        </div>
      </div>
    </section>

    <!-- Logos / Social proof -->
    <section class="logos-section">
      <p class="logos-label">Confiado por administradores en toda México</p>
      <div class="logos-row">
        <div class="logo-item">CDMX</div>
        <div class="logo-item">Monterrey</div>
        <div class="logo-item">Guadalajara</div>
        <div class="logo-item">Puebla</div>
        <div class="logo-item">Querétaro</div>
        <div class="logo-item">Tijuana</div>
      </div>
    </section>

    <!-- Features -->
    <section class="features" id="features">
      <div class="section-header">
        <div class="section-badge">Funcionalidades</div>
        <h2 class="section-title">Todo lo que necesitas para gestionar rentas</h2>
        <p class="section-sub">Sin papeles, sin dolores de cabeza. Digitaliza tu negocio de rentas hoy.</p>
      </div>
      <div class="features-grid">
        <div class="feature-card featured">
          <div class="feature-icon">🏠</div>
          <h3>Gestión de propiedades</h3>
          <p>Registra, edita y monitorea todas tus propiedades en renta desde un panel centralizado.</p>
          <ul class="feature-list">
            <li>✓ Fotos y detalles completos</li>
            <li>✓ Estado en tiempo real</li>
            <li>✓ Historial de ocupación</li>
          </ul>
        </div>
        <div class="feature-card">
          <div class="feature-icon">👥</div>
          <h3>Inquilinos digitales</h3>
          <p>Perfil completo de cada inquilino, historial de pagos y documentos en un clic.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📄</div>
          <h3>Contratos inteligentes</h3>
          <p>Genera y gestiona contratos de arrendamiento con alertas de vencimiento automáticas.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💳</div>
          <h3>Control de pagos</h3>
          <p>Registra pagos, genera recibos y recibe alertas de inquilinos con mora.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Reportes financieros</h3>
          <p>Visualiza ingresos, gastos y rentabilidad de cada propiedad al instante.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔔</div>
          <h3>Alertas automáticas</h3>
          <p>Notificaciones de vencimiento de contratos, pagos pendientes y mantenimientos.</p>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="how" id="how">
      <div class="how-content">
        <div class="section-header" style="text-align:left;margin-bottom:48px;">
          <div class="section-badge">Proceso</div>
          <h2 class="section-title">En 3 pasos, listo</h2>
          <p class="section-sub">Sin curva de aprendizaje. Empieza a gestionar tus rentas en minutos.</p>
        </div>
        <div class="steps">
          <div class="step">
            <div class="step-num">01</div>
            <div class="step-info">
              <h3>Registra tu propiedad</h3>
              <p>Agrega dirección, fotos, precio de renta y características. Toma menos de 5 minutos.</p>
            </div>
          </div>
          <div class="step-connector"></div>
          <div class="step">
            <div class="step-num">02</div>
            <div class="step-info">
              <h3>Agrega tus inquilinos</h3>
              <p>Crea el perfil del inquilino, sube documentos y genera el contrato digital automáticamente.</p>
            </div>
          </div>
          <div class="step-connector"></div>
          <div class="step">
            <div class="step-num">03</div>
            <div class="step-info">
              <h3>Gestiona y cobra</h3>
              <p>Registra pagos, genera recibos y recibe alertas. Tu negocio de rentas en piloto automático.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section class="pricing" id="pricing">
      <div class="section-header">
        <div class="section-badge">Precios</div>
        <h2 class="section-title">Simple y transparente</h2>
        <p class="section-sub">Sin costos ocultos. Sin tarjeta de crédito para empezar.</p>
      </div>
      <div class="pricing-grid">
        <div class="pricing-card">
          <div class="pricing-name">Gratis</div>
          <div class="pricing-price">$0<span>/mes</span></div>
          <ul class="pricing-features">
            <li>✓ Hasta 3 propiedades</li>
            <li>✓ 5 inquilinos</li>
            <li>✓ Contratos básicos</li>
            <li>✓ Registro de pagos</li>
          </ul>
          <router-link to="/register" class="btn-pricing">Empezar gratis</router-link>
        </div>
        <div class="pricing-card featured">
          <div class="pricing-badge">Más popular</div>
          <div class="pricing-name">Profesional</div>
          <div class="pricing-price">$299<span>/mes</span></div>
          <ul class="pricing-features">
            <li>✓ Propiedades ilimitadas</li>
            <li>✓ Inquilinos ilimitados</li>
            <li>✓ Contratos avanzados</li>
            <li>✓ Reportes financieros</li>
            <li>✓ Alertas automáticas</li>
            <li>✓ Soporte prioritario</li>
          </ul>
          <router-link to="/register" class="btn-pricing primary">Comenzar prueba gratis</router-link>
        </div>
        <div class="pricing-card">
          <div class="pricing-name">Empresarial</div>
          <div class="pricing-price">$899<span>/mes</span></div>
          <ul class="pricing-features">
            <li>✓ Todo en Profesional</li>
            <li>✓ Multi-usuario</li>
            <li>✓ API access</li>
            <li>✓ Onboarding dedicado</li>
          </ul>
          <router-link to="/register" class="btn-pricing">Contactar ventas</router-link>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <div class="cta-glow"></div>
      <h2 class="cta-title">¿Listo para modernizar tus rentas?</h2>
      <p class="cta-sub">Únete a más de 2,400 propiedades gestionadas con RentaFácil</p>
      <div class="cta-actions">
        <router-link to="/register" class="btn-hero-primary">Crear cuenta gratis</router-link>
        <router-link to="/login" class="btn-hero-secondary">Ver demo →</router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-logo">🏠 RentaFácil</div>
        <div class="footer-links">
          <router-link to="/login">Iniciar sesión</router-link>
          <router-link to="/register">Registrarse</router-link>
        </div>
        <div class="footer-copy">© 2025 RentaFácil. Todos los derechos reservados.</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)
function onScroll() { scrolled.value = window.scrollY > 20 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
* { box-sizing: border-box; }
.landing { background: #080810; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; overflow-x: hidden; }

/* NAV */
.nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; padding: 16px 0; transition: all 0.3s; }
.nav.scrolled { background: rgba(8,8,16,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.06); }
.nav-inner { max-width: 1200px; margin: 0 auto; padding: 0 32px; display: flex; align-items: center; gap: 32px; }
.nav-logo { font-size: 20px; font-weight: 800; color: #f59e0b; flex-shrink: 0; }
.nav-links { display: flex; gap: 28px; flex: 1; justify-content: center; }
.nav-links a { color: #94a3b8; text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }
.nav-links a:hover { color: #e2e8f0; }
.nav-cta { display: flex; align-items: center; gap: 12px; }
.btn-ghost { color: #94a3b8; text-decoration: none; font-size: 14px; padding: 8px 16px; transition: color 0.2s; }
.btn-ghost:hover { color: #e2e8f0; }
.btn-cta { background: #f59e0b; color: #080810; font-size: 14px; font-weight: 700; padding: 9px 20px; border-radius: 8px; text-decoration: none; transition: all 0.2s; }
.btn-cta:hover { background: #d97706; transform: translateY(-1px); }

/* HERO */
.hero { min-height: 100vh; display: flex; align-items: center; padding: 120px 32px 80px; max-width: 1200px; margin: 0 auto; gap: 60px; position: relative; overflow: visible; }
.hero-grid-bg { position: fixed; inset: 0; background-image: linear-gradient(rgba(245,158,11,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(245,158,11,0.03) 1px, transparent 1px); background-size: 60px 60px; pointer-events: none; z-index: 0; }
.hero-glow { position: absolute; border-radius: 50%; filter: blur(120px); pointer-events: none; }
.hero-glow-1 { width: 600px; height: 600px; background: rgba(245,158,11,0.08); top: -100px; left: -200px; }
.hero-glow-2 { width: 500px; height: 500px; background: rgba(99,102,241,0.06); bottom: -100px; right: -100px; }
.hero-content { flex: 1; position: relative; z-index: 1; }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2); border-radius: 999px; padding: 6px 14px; font-size: 13px; font-weight: 500; color: #f59e0b; margin-bottom: 28px; }
.badge-dot { width: 6px; height: 6px; background: #f59e0b; border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:0.5;transform:scale(1.5);} }
.hero-title { font-size: clamp(40px, 5vw, 68px); font-weight: 800; line-height: 1.1; letter-spacing: -0.03em; margin-bottom: 24px; }
.gradient-text { background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-sub { font-size: 18px; color: #94a3b8; line-height: 1.7; max-width: 500px; margin-bottom: 36px; }
.hero-actions { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 48px; }
.btn-hero-primary { display: inline-flex; align-items: center; gap: 8px; background: #f59e0b; color: #080810; font-weight: 700; font-size: 15px; padding: 14px 28px; border-radius: 10px; text-decoration: none; transition: all 0.2s; }
.btn-hero-primary:hover { background: #d97706; transform: translateY(-2px); box-shadow: 0 8px 30px rgba(245,158,11,0.3); }
.btn-hero-secondary { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); color: #e2e8f0; font-weight: 600; font-size: 15px; padding: 14px 28px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); text-decoration: none; transition: all 0.2s; }
.btn-hero-secondary:hover { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2); }
.hero-stats { display: flex; align-items: center; gap: 24px; }
.hero-stat { display: flex; flex-direction: column; }
.stat-n { font-size: 24px; font-weight: 700; color: #f59e0b; }
.stat-l { font-size: 12px; color: #64748b; }
.hero-stat-div { width: 1px; height: 36px; background: rgba(255,255,255,0.1); }

/* MOCKUP */
.hero-mockup { flex: 1; position: relative; z-index: 1; }
.mockup-window { background: #0f0f1a; border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; overflow: hidden; box-shadow: 0 40px 120px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.05); }
.mockup-bar { background: #1a1a2e; padding: 12px 16px; display: flex; gap: 6px; }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.red { background: #ef4444; }
.dot.yellow { background: #f59e0b; }
.dot.green { background: #10b981; }
.mockup-content { display: flex; }
.mockup-sidebar { width: 120px; background: #0a0a14; padding: 12px 8px; display: flex; flex-direction: column; gap: 4px; border-right: 1px solid rgba(255,255,255,0.05); }
.mock-logo { font-size: 18px; padding: 4px 8px 12px; }
.mock-nav-item { padding: 7px 8px; border-radius: 6px; font-size: 10px; color: #64748b; white-space: nowrap; }
.mock-nav-item.active { background: rgba(245,158,11,0.1); color: #f59e0b; }
.mockup-main { flex: 1; padding: 16px; }
.mock-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 16px; }
.mock-stat-card { background: #1a1a2e; border-radius: 8px; padding: 10px; border: 1px solid rgba(255,255,255,0.05); }
.mock-stat-val { font-size: 13px; font-weight: 700; color: var(--c); }
.mock-stat-lbl { font-size: 9px; color: #64748b; margin-top: 2px; }
.mock-table-header { font-size: 10px; color: #64748b; margin-bottom: 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.mock-row { display: flex; align-items: center; gap: 8px; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.mock-avatar { width: 22px; height: 22px; border-radius: 50%; background: #10b981; flex-shrink: 0; }
.mock-info { flex: 1; display: flex; flex-direction: column; gap: 3px; }
.mock-name { height: 7px; background: rgba(255,255,255,0.1); border-radius: 3px; width: 80px; }
.mock-date { height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; width: 50px; }
.mock-amount { height: 7px; border-radius: 3px; width: 40px; }
.mock-amount.green { background: rgba(16,185,129,0.3); }
.mock-amount.yellow { background: rgba(245,158,11,0.3); }
.mockup-float { position: absolute; background: rgba(15,15,26,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 8px 14px; font-size: 12px; font-weight: 500; backdrop-filter: blur(10px); white-space: nowrap; }
.float-1 { top: -16px; right: -16px; color: #10b981; animation: floatAnim 3s ease-in-out infinite; }
.float-2 { bottom: 40px; left: -20px; color: #f59e0b; animation: floatAnim 3s ease-in-out infinite 1.5s; }
@keyframes floatAnim { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-8px);} }

/* LOGOS */
.logos-section { border-top: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06); padding: 32px; text-align: center; }
.logos-label { font-size: 13px; color: #475569; margin-bottom: 20px; }
.logos-row { display: flex; justify-content: center; gap: 48px; flex-wrap: wrap; }
.logo-item { font-size: 14px; font-weight: 700; color: #475569; letter-spacing: 0.1em; }

/* FEATURES */
.features { padding: 100px 32px; max-width: 1200px; margin: 0 auto; }
.section-header { text-align: center; margin-bottom: 64px; }
.section-badge { display: inline-block; background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2); color: #f59e0b; border-radius: 999px; padding: 5px 14px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; }
.section-title { font-size: clamp(28px, 4vw, 48px); font-weight: 800; letter-spacing: -0.02em; margin-bottom: 16px; }
.section-sub { font-size: 18px; color: #64748b; max-width: 600px; margin: 0 auto; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.feature-card { background: #0f0f1a; border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 28px; transition: all 0.3s; }
.feature-card:hover { border-color: rgba(245,158,11,0.2); transform: translateY(-4px); }
.feature-card.featured { background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(239,68,68,0.05)); border-color: rgba(245,158,11,0.2); grid-row: span 2; }
.feature-icon { font-size: 32px; margin-bottom: 16px; }
.feature-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
.feature-card p { font-size: 14px; color: #64748b; line-height: 1.6; }
.feature-list { list-style: none; margin-top: 16px; display: flex; flex-direction: column; gap: 8px; }
.feature-list li { font-size: 13px; color: #94a3b8; }

/* HOW */
.how { padding: 100px 32px; background: rgba(255,255,255,0.01); border-top: 1px solid rgba(255,255,255,0.04); }
.how-content { max-width: 700px; margin: 0 auto; }
.steps { display: flex; flex-direction: column; gap: 0; }
.step { display: flex; gap: 24px; align-items: flex-start; }
.step-num { font-size: 48px; font-weight: 900; color: rgba(245,158,11,0.15); line-height: 1; min-width: 60px; font-variant-numeric: tabular-nums; }
.step-info h3 { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.step-info p { font-size: 15px; color: #64748b; line-height: 1.6; }
.step-connector { width: 1px; height: 40px; background: rgba(245,158,11,0.15); margin-left: 30px; }

/* PRICING */
.pricing { padding: 100px 32px; max-width: 1200px; margin: 0 auto; }
.pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; margin: 0 auto; }
.pricing-card { background: #0f0f1a; border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 32px; display: flex; flex-direction: column; gap: 20px; position: relative; }
.pricing-card.featured { border-color: rgba(245,158,11,0.3); background: linear-gradient(135deg, rgba(245,158,11,0.06), rgba(239,68,68,0.04)); box-shadow: 0 0 60px rgba(245,158,11,0.08); }
.pricing-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #f59e0b; color: #080810; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 999px; white-space: nowrap; }
.pricing-name { font-size: 16px; font-weight: 600; color: #94a3b8; }
.pricing-price { font-size: 40px; font-weight: 800; color: #e2e8f0; }
.pricing-price span { font-size: 16px; font-weight: 400; color: #64748b; }
.pricing-features { list-style: none; display: flex; flex-direction: column; gap: 10px; flex: 1; }
.pricing-features li { font-size: 14px; color: #94a3b8; }
.btn-pricing { display: block; text-align: center; padding: 12px; border-radius: 10px; font-weight: 600; font-size: 14px; text-decoration: none; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; transition: all 0.2s; }
.btn-pricing:hover { border-color: rgba(255,255,255,0.2); color: #e2e8f0; }
.btn-pricing.primary { background: #f59e0b; color: #080810; border-color: transparent; }
.btn-pricing.primary:hover { background: #d97706; }

/* CTA */
.cta { padding: 120px 32px; text-align: center; position: relative; overflow: hidden; }
.cta-glow { position: absolute; width: 600px; height: 400px; background: radial-gradient(ellipse, rgba(245,158,11,0.08) 0%, transparent 70%); top: 50%; left: 50%; transform: translate(-50%, -50%); pointer-events: none; }
.cta-title { font-size: clamp(32px, 5vw, 56px); font-weight: 800; letter-spacing: -0.02em; margin-bottom: 16px; position: relative; }
.cta-sub { font-size: 18px; color: #64748b; margin-bottom: 36px; position: relative; }
.cta-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; position: relative; }

/* FOOTER */
.footer { border-top: 1px solid rgba(255,255,255,0.06); padding: 32px; }
.footer-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 32px; }
.footer-logo { font-size: 18px; font-weight: 800; color: #f59e0b; flex: 1; }
.footer-links { display: flex; gap: 24px; }
.footer-links a { color: #64748b; text-decoration: none; font-size: 14px; }
.footer-links a:hover { color: #94a3b8; }
.footer-copy { font-size: 13px; color: #475569; }
</style>
