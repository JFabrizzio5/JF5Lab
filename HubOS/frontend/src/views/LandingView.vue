<template>
  <div class="landing">
    <!-- NAV -->
    <nav class="nav">
      <div class="nav-inner">
        <div class="logo">
          <div class="logo-mark"><i data-lucide="layers"></i></div>
          <span>HubOS</span>
        </div>
        <div class="nav-links hidden md:flex">
          <a href="#features">Features</a>
          <a href="#modules">Módulos</a>
          <a href="#stack">Stack</a>
          <a href="#pricing">Precios</a>
        </div>
        <div class="nav-cta">
          <router-link to="/login" class="link-muted">Ingresar</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Empezar gratis</router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero" @mousemove="onMove" @mouseleave="resetTilt">
      <div class="bg-grid"></div>
      <div class="bg-orb orb-a" :style="orbStyle(0.02, 0.015)"></div>
      <div class="bg-orb orb-b" :style="orbStyle(-0.018, 0.022)"></div>
      <div class="bg-orb orb-c" :style="orbStyle(0.03, -0.02)"></div>

      <div class="hero-inner">
        <div class="hero-text" :style="textParallax">
          <div class="pill">
            <i data-lucide="sparkles" style="width:14px;height:14px"></i>
            <span>Un solo hub para todo tu go-to-market</span>
          </div>
          <h1 class="hero-title">
            <span class="grad-text">CRM, CMS y WhatsApp</span><br />
            en un solo lugar.
          </h1>
          <p class="hero-sub">
            Gestiona clientes, contenidos y conversaciones de WhatsApp con sesiones independientes
            por agente. Todo con bloques reutilizables para soporte, presentaciones y documentación.
          </p>
          <div class="hero-cta">
            <router-link to="/register" class="btn btn-primary">
              <i data-lucide="rocket" style="width:16px;height:16px"></i>
              Crear workspace
            </router-link>
            <a href="#modules" class="btn btn-ghost">
              <i data-lucide="play" style="width:16px;height:16px"></i>
              Ver módulos
            </a>
          </div>
          <div class="trust-row">
            <div class="trust-item">
              <i data-lucide="shield-check" style="width:16px;height:16px;color:#22d3ee"></i>
              <span>Multi-tenant</span>
            </div>
            <div class="trust-item">
              <i data-lucide="zap" style="width:16px;height:16px;color:#f59e0b"></i>
              <span>Evolution API</span>
            </div>
            <div class="trust-item">
              <i data-lucide="blocks" style="width:16px;height:16px;color:#10b981"></i>
              <span>Block-based</span>
            </div>
          </div>
        </div>

        <!-- 3D PARALLAX SHOWCASE -->
        <div class="hero-3d" :style="sceneStyle">
          <div class="scene">
            <!-- back layers -->
            <div class="ring ring-1" :style="layer(0.02, 0.01)"></div>
            <div class="ring ring-2" :style="layer(-0.03, 0.02)"></div>

            <!-- glow -->
            <div class="product-glow" :style="layer(0.01, 0.01)"></div>

            <!-- product: stylized 3D can rendered purely in CSS -->
            <div class="can-wrap" :style="productTilt">
              <div class="can">
                <div class="can-top">
                  <div class="can-lid"></div>
                  <div class="can-tab"></div>
                </div>
                <div class="can-body">
                  <div class="can-shine"></div>
                  <div class="can-stripe-top"></div>
                  <div class="can-stripe-bot"></div>
                  <div class="can-label">
                    <div class="label-brand">HubOS</div>
                    <div class="label-sub">Customer OS</div>
                    <div class="label-barcode"></div>
                  </div>
                </div>
                <div class="can-bottom"></div>
              </div>
              <div class="can-shadow"></div>
            </div>

            <!-- floating module cards -->
            <div class="float-card card-crm" :style="layer(-0.04, 0.03)">
              <i data-lucide="users" style="width:16px;height:16px;color:#818cf8"></i>
              <div>
                <div class="fc-title">Contactos</div>
                <div class="fc-num">12,430</div>
              </div>
            </div>
            <div class="float-card card-chat" :style="layer(0.05, -0.03)">
              <i data-lucide="message-circle" style="width:16px;height:16px;color:#22d3ee"></i>
              <div>
                <div class="fc-title">Chats activos</div>
                <div class="fc-num">89</div>
              </div>
            </div>
            <div class="float-card card-deal" :style="layer(-0.03, -0.04)">
              <i data-lucide="trending-up" style="width:16px;height:16px;color:#10b981"></i>
              <div>
                <div class="fc-title">Deals ganados</div>
                <div class="fc-num">$1.2M</div>
              </div>
            </div>

            <!-- sparkles / particles -->
            <span v-for="i in 14" :key="i" class="sparkle" :style="sparkleStyle(i)"></span>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section id="features" class="section">
      <div class="container">
        <div class="section-head">
          <div class="tag">Features</div>
          <h2>Un motor, cuatro superpoderes.</h2>
          <p>Patrón consistente: todo es modular, todo es extensible, todo habla con todo.</p>
        </div>

        <div class="grid-4">
          <div class="feature">
            <div class="f-icon" style="background:linear-gradient(135deg,#6366f1,#818cf8)">
              <i data-lucide="users" style="color:white"></i>
            </div>
            <h3>CRM</h3>
            <p>Contactos, deals en kanban, pipelines configurables, propietarios y tags.</p>
          </div>
          <div class="feature">
            <div class="f-icon" style="background:linear-gradient(135deg,#06b6d4,#22d3ee)">
              <i data-lucide="file-text" style="color:white"></i>
            </div>
            <h3>CMS</h3>
            <p>Páginas y posts en bloques. Publicación pública por slug vía API pública.</p>
          </div>
          <div class="feature">
            <div class="f-icon" style="background:linear-gradient(135deg,#10b981,#34d399)">
              <i data-lucide="message-circle" style="color:white"></i>
            </div>
            <h3>WhatsApp</h3>
            <p>Evolution API multi-sesión. Cada agente tiene su propio número y sus propios chats.</p>
          </div>
          <div class="feature">
            <div class="f-icon" style="background:linear-gradient(135deg,#f59e0b,#fbbf24)">
              <i data-lucide="layout-template" style="color:#0b1d23"></i>
            </div>
            <h3>Templates</h3>
            <p>Constructor de plantillas con variables para soporte, presentaciones y docs técnicas.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- MODULES -->
    <section id="modules" class="section dark">
      <div class="container">
        <div class="section-head">
          <div class="tag">Módulos</div>
          <h2>Cada pieza encaja en tu flujo.</h2>
        </div>

        <div class="grid-3">
          <div class="mod-card">
            <i data-lucide="kanban" style="color:#818cf8"></i>
            <h3>Deals kanban</h3>
            <p>Arrastra y suelta, pipelines personalizados, forecast al instante.</p>
          </div>
          <div class="mod-card">
            <i data-lucide="share-2" style="color:#22d3ee"></i>
            <h3>Webhooks Evolution</h3>
            <p>Entrantes y salientes. Conversación + mensajes sincronizados en Postgres.</p>
          </div>
          <div class="mod-card">
            <i data-lucide="variable" style="color:#10b981"></i>
            <h3>Variables de plantilla</h3>
            <p>Tokens <code v-pre>{{variable}}</code> renderizados al vuelo con el API.</p>
          </div>
          <div class="mod-card">
            <i data-lucide="globe" style="color:#f59e0b"></i>
            <h3>Endpoints públicos</h3>
            <p>Expon tu CMS por workspace slug + contenido slug, zero auth.</p>
          </div>
          <div class="mod-card">
            <i data-lucide="lock" style="color:#f472b6"></i>
            <h3>Workspace isolation</h3>
            <p>Tenant-safe. JWT acarrea el workspace_id en cada llamada.</p>
          </div>
          <div class="mod-card">
            <i data-lucide="radio" style="color:#a78bfa"></i>
            <h3>WebSockets</h3>
            <p>Eventos de chat en tiempo real al navegador del agente.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- STACK -->
    <section id="stack" class="section">
      <div class="container stack-wrap">
        <div class="stack-left">
          <div class="tag">Stack</div>
          <h2>Siguiendo el patrón CometaX.</h2>
          <p>FastAPI + SQLAlchemy + PostgreSQL en el backend. Vue 3 + Vite + Pinia en el frontend. Nginx sirve todo como build estático.</p>
          <ul class="stack-list">
            <li><i data-lucide="check" style="width:14px;height:14px;color:#10b981"></i> Docker-compose listo para levantar</li>
            <li><i data-lucide="check" style="width:14px;height:14px;color:#10b981"></i> Puertos no colisionan con otros proyectos</li>
            <li><i data-lucide="check" style="width:14px;height:14px;color:#10b981"></i> Patrón de módulos idéntico al de RentaFacil/SalonOS</li>
          </ul>
        </div>
        <div class="stack-right">
          <pre class="code-block"><code>services:
  hubos_postgres:
    image: postgres:15-alpine
  hubos_backend:
    ports: ["8070:8070"]
    env: EVOLUTION_API_URL, JWT_SECRET
  hubos_frontend:
    ports: ["3035:3035"]</code></pre>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section id="pricing" class="section">
      <div class="container cta-card">
        <h2>Empieza en 30 segundos.</h2>
        <p>Crea tu workspace, conecta tu primer número de WhatsApp y empieza a cerrar.</p>
        <router-link to="/register" class="btn btn-primary">
          <i data-lucide="rocket" style="width:16px;height:16px"></i>
          Crear workspace
        </router-link>
      </div>
    </section>

    <footer class="footer">
      <div class="container footer-inner">
        <div class="logo">
          <div class="logo-mark"><i data-lucide="layers"></i></div>
          <span>HubOS</span>
        </div>
        <div class="footer-links">
          <a href="#features">Features</a>
          <a href="#modules">Módulos</a>
          <a href="#stack">Stack</a>
        </div>
        <div class="footer-copy">© 2026 HubOS · Built on CometaX</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const mx = ref(0)  // mouse x (-1 … 1)
const my = ref(0)
let rafId = null

function onMove(e) {
  const r = e.currentTarget.getBoundingClientRect()
  const nx = ((e.clientX - r.left) / r.width) * 2 - 1
  const ny = ((e.clientY - r.top) / r.height) * 2 - 1
  if (rafId) cancelAnimationFrame(rafId)
  rafId = requestAnimationFrame(() => {
    mx.value = nx
    my.value = ny
  })
}
function resetTilt() {
  mx.value = 0
  my.value = 0
}

const sceneStyle = computed(() => ({
  perspective: '1400px',
}))
const productTilt = computed(() => ({
  transform: `rotateY(${mx.value * 12}deg) rotateX(${-my.value * 10}deg) translateZ(40px)`,
}))
const textParallax = computed(() => ({
  transform: `translate3d(${mx.value * -8}px, ${my.value * -4}px, 0)`,
}))

function layer(strengthX, strengthY) {
  return {
    transform: `translate3d(${mx.value * strengthX * 100}px, ${my.value * strengthY * 100}px, 0)`,
  }
}
function orbStyle(sx, sy) {
  return { transform: `translate3d(${mx.value * sx * 200}px, ${my.value * sy * 200}px, 0)` }
}
function sparkleStyle(i) {
  const sx = (i * 37) % 100
  const sy = (i * 53) % 100
  const d = ((i * 73) % 40) + 20
  return {
    left: `${sx}%`,
    top: `${sy}%`,
    animationDelay: `${(i * 0.3) % 4}s`,
    transform: `translate3d(${mx.value * (i % 5) * 4}px, ${my.value * (i % 5) * 4}px, 0)`,
    width: `${3 + (i % 3)}px`,
    height: `${3 + (i % 3)}px`,
    '--dur': `${d / 10}s`,
  }
}

function refreshIcons() { if (window.lucide) window.lucide.createIcons() }
onMounted(refreshIcons)
onUnmounted(() => { if (rafId) cancelAnimationFrame(rafId) })
</script>

<style scoped>
.landing {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', sans-serif;
}

/* NAV */
.nav {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(16px);
  background: rgba(9, 9, 15, 0.72);
  border-bottom: 1px solid var(--border);
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.85rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.logo { display: flex; align-items: center; gap: 0.55rem; font-weight: 800; font-size: 1rem; letter-spacing: -0.3px; }
.logo-mark {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.logo-mark i, .logo-mark :deep(svg) { width: 18px; height: 18px; }
.nav-links { display: flex; gap: 1.5rem; font-size: 0.85rem; color: var(--text2); font-weight: 500; }
.nav-links a:hover { color: var(--text); }
.nav-cta { display: flex; align-items: center; gap: 0.8rem; }
.link-muted { color: var(--text2); font-size: 0.85rem; font-weight: 500; }
.link-muted:hover { color: var(--text); }

/* HERO */
.hero {
  position: relative;
  min-height: 92vh;
  padding: 4rem 1.5rem 6rem;
  overflow: hidden;
  isolation: isolate;
}
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(circle at 60% 40%, black 0%, transparent 75%);
  z-index: -1;
}
.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.55;
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  z-index: -1;
}
.orb-a { width: 460px; height: 460px; background: #6366f1; top: -80px; left: -80px; }
.orb-b { width: 360px; height: 360px; background: #06b6d4; bottom: -60px; right: -40px; }
.orb-c { width: 280px; height: 280px; background: #f472b6; top: 40%; left: 40%; opacity: 0.35; }

.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 3rem;
  align-items: center;
}
@media (max-width: 960px) {
  .hero-inner { grid-template-columns: 1fr; }
}

.hero-text { transition: transform 0.3s cubic-bezier(0.2,0.8,0.2,1); }
.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.35rem 0.85rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: rgba(255,255,255,0.02);
  font-size: 0.78rem;
  color: var(--text2);
  margin-bottom: 1.25rem;
}
.hero-title {
  font-family: 'Space Grotesk', 'Inter', sans-serif;
  font-size: clamp(2.4rem, 5vw, 4.2rem);
  font-weight: 800;
  line-height: 1.02;
  letter-spacing: -0.04em;
  margin-bottom: 1.25rem;
}
.grad-text {
  background: linear-gradient(120deg, #a5b4fc 0%, #22d3ee 50%, #818cf8 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub {
  color: var(--text2);
  font-size: 1.05rem;
  max-width: 540px;
  line-height: 1.6;
  margin-bottom: 2rem;
}
.hero-cta { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 2rem; }
.trust-row { display: flex; gap: 1.5rem; color: var(--text3); font-size: 0.8rem; flex-wrap: wrap; }
.trust-item { display: inline-flex; align-items: center; gap: 0.4rem; }

/* 3D scene */
.hero-3d {
  position: relative;
  height: 520px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.06);
  pointer-events: none;
  transition: transform 0.3s cubic-bezier(0.2,0.8,0.2,1);
}
.ring-1 { width: 440px; height: 440px; transform: translate(-50%, -50%); border-color: rgba(99,102,241,0.18); }
.ring-2 { width: 320px; height: 320px; transform: translate(-50%, -50%); border-color: rgba(34,211,238,0.16); }
.product-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 260px;
  height: 260px;
  background: radial-gradient(circle, rgba(99,102,241,0.5) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  filter: blur(30px);
  pointer-events: none;
}

/* soda can — pure CSS */
.can-wrap {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 340px;
  transition: transform 0.25s cubic-bezier(0.2,0.8,0.2,1);
  transform-style: preserve-3d;
}
.can {
  position: relative;
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 30px 40px rgba(0,0,0,0.5));
}
.can-top {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  height: 24px;
  background: linear-gradient(to bottom,
    #e5e7eb 0%, #94a3b8 20%, #64748b 50%, #475569 90%);
  border-radius: 100px / 12px;
  z-index: 3;
}
.can-lid {
  position: absolute;
  inset: 3px 6px;
  background: radial-gradient(ellipse at 30% 30%, #cbd5e1 0%, #475569 70%);
  border-radius: 50%;
}
.can-tab {
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 10px;
  background: linear-gradient(to bottom, #94a3b8, #475569);
  border-radius: 8px / 4px;
  border: 1px solid #334155;
}
.can-body {
  position: absolute;
  top: 18px;
  left: 0;
  right: 0;
  bottom: 18px;
  background: linear-gradient(90deg,
    #3730a3 0%,
    #4f46e5 20%,
    #6366f1 40%,
    #818cf8 50%,
    #6366f1 60%,
    #4f46e5 80%,
    #3730a3 100%
  );
  border-radius: 6px;
  overflow: hidden;
  z-index: 2;
}
.can-shine {
  position: absolute;
  top: 0;
  left: 15%;
  width: 12px;
  height: 100%;
  background: linear-gradient(to bottom, rgba(255,255,255,0.5), rgba(255,255,255,0.05));
  filter: blur(2px);
}
.can-stripe-top {
  position: absolute;
  top: 12%;
  left: 0;
  right: 0;
  height: 8px;
  background: linear-gradient(90deg, rgba(34,211,238,0.85), rgba(34,211,238,0.4));
}
.can-stripe-bot {
  position: absolute;
  bottom: 12%;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, rgba(34,211,238,0.6), rgba(34,211,238,0.2));
}
.can-label {
  position: absolute;
  top: 30%;
  left: 0;
  right: 0;
  text-align: center;
  color: white;
  padding: 0 1rem;
}
.label-brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  text-shadow: 0 1px 2px rgba(0,0,0,0.4);
}
.label-sub {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: #c7d2fe;
  margin-top: 0.3rem;
}
.label-barcode {
  margin: 0.9rem auto 0;
  width: 60px;
  height: 22px;
  background: repeating-linear-gradient(90deg, white 0 2px, transparent 2px 4px);
  opacity: 0.9;
}
.can-bottom {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  height: 24px;
  background: linear-gradient(to top,
    #1e293b 0%, #334155 40%, #64748b 80%);
  border-radius: 100px / 12px;
  z-index: 3;
}
.can-shadow {
  position: absolute;
  left: 50%;
  bottom: -34px;
  transform: translateX(-50%);
  width: 220px;
  height: 36px;
  background: radial-gradient(ellipse, rgba(99,102,241,0.5) 0%, transparent 65%);
  filter: blur(16px);
}

/* floating cards */
.float-card {
  position: absolute;
  padding: 0.7rem 0.9rem;
  background: rgba(30, 30, 46, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 150px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  transition: transform 0.3s cubic-bezier(0.2,0.8,0.2,1);
}
.fc-title { font-size: 0.7rem; color: var(--text3); font-weight: 500; }
.fc-num { font-size: 1rem; font-weight: 700; color: var(--text); line-height: 1.15; }
.card-crm { top: 10%; left: 2%; }
.card-chat { top: 30%; right: 2%; }
.card-deal { bottom: 10%; left: 10%; }

/* sparkles */
.sparkle {
  position: absolute;
  background: white;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(255,255,255,0.6);
  animation: twinkle var(--dur, 3s) ease-in-out infinite;
  pointer-events: none;
  opacity: 0.45;
}
@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.9; transform: scale(1.5); }
}

/* SECTIONS */
.section {
  padding: 6rem 1.5rem;
  position: relative;
}
.section.dark { background: var(--bg2); }
.container { max-width: 1200px; margin: 0 auto; }

.section-head { text-align: center; margin-bottom: 3.5rem; }
.tag {
  display: inline-block;
  padding: 0.3rem 0.85rem;
  background: rgba(99,102,241,0.15);
  color: #a5b4fc;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
}
.section-head h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(1.7rem, 3.5vw, 2.6rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 0.8rem;
}
.section-head p { color: var(--text2); max-width: 600px; margin: 0 auto; font-size: 1rem; }

.grid-4 { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1.25rem; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.25rem; }

.feature {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.6rem;
  transition: all 0.25s;
}
.feature:hover { transform: translateY(-4px); border-color: rgba(99,102,241,0.3); }
.f-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}
.feature h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.4rem; }
.feature p { color: var(--text2); font-size: 0.9rem; line-height: 1.55; }

.mod-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.5rem;
  transition: all 0.2s;
}
.mod-card:hover { border-color: rgba(99,102,241,0.3); background: rgba(99,102,241,0.05); }
.mod-card i, .mod-card :deep(svg) { width: 22px; height: 22px; margin-bottom: 0.8rem; }
.mod-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }
.mod-card p { color: var(--text2); font-size: 0.87rem; line-height: 1.5; }
.mod-card code {
  background: rgba(255,255,255,0.06);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.78rem;
}

/* STACK */
.stack-wrap { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }
@media (max-width: 860px) { .stack-wrap { grid-template-columns: 1fr; } }
.stack-left h2 { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 800; margin: 0.8rem 0 1rem; letter-spacing: -0.03em; }
.stack-left p { color: var(--text2); margin-bottom: 1.25rem; line-height: 1.6; }
.stack-list { list-style: none; display: flex; flex-direction: column; gap: 0.55rem; font-size: 0.9rem; color: var(--text2); }
.stack-list li { display: flex; align-items: center; gap: 0.55rem; }
.code-block {
  background: #0b0b14;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.82rem;
  color: #cbd5e1;
  overflow-x: auto;
}
.code-block code { font-family: inherit; }

/* CTA */
.cta-card {
  text-align: center;
  background: radial-gradient(circle at 50% 0%, rgba(99,102,241,0.2) 0%, transparent 70%), var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3.5rem 2rem;
}
.cta-card h2 { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.6rem; }
.cta-card p { color: var(--text2); margin-bottom: 1.5rem; }

/* FOOTER */
.footer { border-top: 1px solid var(--border); padding: 2rem 1.5rem; }
.footer-inner { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.footer-links { display: flex; gap: 1.5rem; font-size: 0.85rem; color: var(--text2); }
.footer-copy { color: var(--text3); font-size: 0.8rem; }
</style>
