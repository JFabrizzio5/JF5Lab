<template>
  <div class="landing">
    <!-- Skip-to-content for keyboard / screen-reader users. Hidden until
         focused; WCAG 2.1 requires a bypass for repeated nav blocks. -->
    <a href="#main" class="skip-link">Saltar al contenido</a>

    <!-- Scroll progress bar — visual cue of how deep the reader is. -->
    <div class="scroll-progress" :style="{ transform: `scaleX(${scrollPct})` }" aria-hidden="true"></div>

    <!-- NAV -->
    <header class="nav" role="banner">
      <div class="nav-inner">
        <a href="#main" class="logo" aria-label="HubOS — ir al inicio">
          <span class="logo-mark"><i data-lucide="layers"></i></span>
          <span class="logo-word">HubOS</span>
        </a>

        <nav class="nav-links" aria-label="Secciones">
          <a href="#features">Features</a>
          <a href="#workflow">Cómo funciona</a>
          <a href="#modules">Módulos</a>
          <a href="#stack">Stack</a>
          <a href="#pricing">Precios</a>
        </nav>

        <div class="nav-cta">
          <router-link to="/login" class="link-muted">Ingresar</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Empezar gratis</router-link>
        </div>

        <button
          class="nav-burger"
          :aria-expanded="menuOpen"
          aria-controls="mobile-menu"
          aria-label="Abrir menú"
          @click="menuOpen = !menuOpen"
        >
          <i :data-lucide="menuOpen ? 'x' : 'menu'"></i>
        </button>
      </div>

      <!-- Mobile drawer -->
      <div
        id="mobile-menu"
        class="mobile-menu"
        :class="{ open: menuOpen }"
        role="dialog"
        aria-modal="true"
        aria-label="Menú de navegación"
      >
        <a href="#features" @click="menuOpen = false">Features</a>
        <a href="#workflow" @click="menuOpen = false">Cómo funciona</a>
        <a href="#modules" @click="menuOpen = false">Módulos</a>
        <a href="#stack" @click="menuOpen = false">Stack</a>
        <a href="#pricing" @click="menuOpen = false">Precios</a>
        <div class="mobile-cta">
          <router-link to="/login" class="btn btn-ghost" @click="menuOpen = false">Ingresar</router-link>
          <router-link to="/register" class="btn btn-primary" @click="menuOpen = false">Empezar gratis</router-link>
        </div>
      </div>
    </header>

    <main id="main" role="main">
      <!-- HERO -->
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-bg" aria-hidden="true">
          <div class="bg-grid"></div>
          <div class="bg-orb orb-a"></div>
          <div class="bg-orb orb-b"></div>
        </div>

        <div class="hero-inner">
          <div class="hero-text">
            <div class="pill" role="note">
              <i data-lucide="sparkles" aria-hidden="true"></i>
              <span>Nuevo · WhatsApp con Baileys v7 + LID↔PN</span>
            </div>
            <h1 id="hero-title" class="hero-title">
              Tu <em class="serif-accent">workspace</em> de clientes,
              contenido y conversaciones.
            </h1>
            <p class="hero-sub">
              Un solo hub para CRM, CMS, WhatsApp multi-sesión y plantillas.
              Piensa bloques reutilizables. Siente Notion. Trabaja como equipo.
            </p>

            <div class="hero-cta">
              <router-link to="/register" class="btn btn-primary btn-lg">
                Crear workspace gratis
                <i data-lucide="arrow-right" aria-hidden="true"></i>
              </router-link>
              <a href="#workflow" class="btn btn-ghost btn-lg">
                Ver cómo funciona
              </a>
            </div>

            <dl class="stats">
              <div class="stat">
                <dt>Sesiones WhatsApp</dt>
                <dd>Ilimitadas</dd>
              </div>
              <div class="stat">
                <dt>Historial sync</dt>
                <dd>Nativo</dd>
              </div>
              <div class="stat">
                <dt>Multi-tenant</dt>
                <dd>Por diseño</dd>
              </div>
            </dl>
          </div>

          <!-- App mockup — intentionally simple, static, accessible. No
               parallax on reduced-motion clients. -->
          <aside class="hero-mock" aria-label="Vista previa de la interfaz">
            <div class="mock" :class="{ tilt: allowMotion }">
              <div class="mock-chrome">
                <span class="dot d-r"></span>
                <span class="dot d-y"></span>
                <span class="dot d-g"></span>
                <div class="mock-url">hubos.app / chat</div>
              </div>
              <div class="mock-body">
                <div class="mock-sidebar">
                  <div class="mock-s-head">Sesiones</div>
                  <div class="mock-s-item active">
                    <span class="pulse"></span> Soporte
                  </div>
                  <div class="mock-s-item">Ventas</div>
                  <div class="mock-s-item">Admin</div>
                </div>
                <div class="mock-convs">
                  <div class="mock-conv active">
                    <div class="mock-avatar" style="--c:#a5b4fc">J</div>
                    <div>
                      <div class="mock-n">Joseph F.</div>
                      <div class="mock-p">Va q va, muchas gracias 👌</div>
                    </div>
                    <span class="mock-badge">2</span>
                  </div>
                  <div class="mock-conv">
                    <div class="mock-avatar" style="--c:#22d3ee">L</div>
                    <div>
                      <div class="mock-n">Luis F.</div>
                      <div class="mock-p">Perfecto amigo</div>
                    </div>
                  </div>
                  <div class="mock-conv">
                    <div class="mock-avatar" style="--c:#10b981">E</div>
                    <div>
                      <div class="mock-n">Elisandra</div>
                      <div class="mock-p">[Imagen]</div>
                    </div>
                  </div>
                  <div class="mock-conv">
                    <div class="mock-avatar" style="--c:#f59e0b">B</div>
                    <div>
                      <div class="mock-n">Bryan 🍒</div>
                      <div class="mock-p">Listo, lo reviso.</div>
                    </div>
                  </div>
                </div>
                <div class="mock-chat">
                  <div class="mock-bubble in">Hola! ¿Tienen el reporte de abril?</div>
                  <div class="mock-bubble out">Sí, te lo mando ahora 🚀</div>
                  <div class="mock-bubble in short">👍</div>
                  <div class="mock-typing">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>

      <!-- FEATURES — Notion-style block list -->
      <section id="features" class="block" aria-labelledby="features-title">
        <div class="block-head">
          <span class="eyebrow">01 · Features</span>
          <h2 id="features-title">Un motor, <em class="serif-accent">cuatro superpoderes</em>.</h2>
          <p>Patrón consistente: modular, extensible, todo habla con todo.</p>
        </div>

        <div class="feature-grid">
          <article class="feature">
            <div class="f-emoji" aria-hidden="true">👥</div>
            <h3>CRM</h3>
            <p>Contactos, deals en kanban, pipelines configurables, owners, tags.</p>
          </article>
          <article class="feature">
            <div class="f-emoji" aria-hidden="true">📄</div>
            <h3>CMS</h3>
            <p>Páginas y posts en bloques. Publicación pública por slug vía API.</p>
          </article>
          <article class="feature">
            <div class="f-emoji" aria-hidden="true">💬</div>
            <h3>WhatsApp</h3>
            <p>Evolution v2 + Baileys v7. Multi-sesión, LID↔PN, grupos, media inline.</p>
          </article>
          <article class="feature">
            <div class="f-emoji" aria-hidden="true">🧩</div>
            <h3>Templates</h3>
            <p>Plantillas con variables para soporte, presentaciones y docs técnicas.</p>
          </article>
        </div>
      </section>

      <!-- WORKFLOW — 3 numbered steps -->
      <section id="workflow" class="block alt" aria-labelledby="workflow-title">
        <div class="block-head">
          <span class="eyebrow">02 · Cómo funciona</span>
          <h2 id="workflow-title">De cero a <em class="serif-accent">cerrando deals</em> en 3 pasos.</h2>
        </div>

        <ol class="steps">
          <li class="step">
            <div class="step-num">1</div>
            <h3>Crea tu workspace</h3>
            <p>Un email basta. Cada workspace es su propio tenant, aislado por JWT + workspace_id.</p>
          </li>
          <li class="step">
            <div class="step-num">2</div>
            <h3>Conecta WhatsApp</h3>
            <p>Escanea un QR. Sincroniza historial completo, contactos y grupos como WhatsApp Web.</p>
          </li>
          <li class="step">
            <div class="step-num">3</div>
            <h3>Trabaja en equipo</h3>
            <p>Cada agente tiene su número. Deals en kanban, chat compartido, plantillas al alcance.</p>
          </li>
        </ol>
      </section>

      <!-- MODULES -->
      <section id="modules" class="block" aria-labelledby="modules-title">
        <div class="block-head">
          <span class="eyebrow">03 · Módulos</span>
          <h2 id="modules-title">Cada pieza encaja en tu flujo.</h2>
        </div>

        <div class="mod-grid">
          <article class="mod">
            <i data-lucide="kanban" aria-hidden="true"></i>
            <h3>Deals kanban</h3>
            <p>Drag & drop, pipelines personalizables, forecast al instante.</p>
          </article>
          <article class="mod">
            <i data-lucide="share-2" aria-hidden="true"></i>
            <h3>Webhooks Evolution</h3>
            <p>Entrantes y salientes. Conversación + mensajes sincronizados.</p>
          </article>
          <article class="mod">
            <i data-lucide="variable" aria-hidden="true"></i>
            <h3>Variables de plantilla</h3>
            <p>Tokens <code v-pre>{{variable}}</code> renderizados por API.</p>
          </article>
          <article class="mod">
            <i data-lucide="globe" aria-hidden="true"></i>
            <h3>CMS público</h3>
            <p>Exponé tu CMS por slug, zero auth, cacheable.</p>
          </article>
          <article class="mod">
            <i data-lucide="shield-check" aria-hidden="true"></i>
            <h3>Workspace isolation</h3>
            <p>Tenant-safe. JWT acarrea workspace_id en cada request.</p>
          </article>
          <article class="mod">
            <i data-lucide="radio" aria-hidden="true"></i>
            <h3>WebSockets</h3>
            <p>Eventos de chat en tiempo real al navegador del agente.</p>
          </article>
          <article class="mod">
            <i data-lucide="image" aria-hidden="true"></i>
            <h3>Media inline</h3>
            <p>Imágenes, audios, videos y PDFs, con drag & drop y paste.</p>
          </article>
          <article class="mod">
            <i data-lucide="users-round" aria-hidden="true"></i>
            <h3>Grupos con autor</h3>
            <p>Atribución por participante vía mapping LID↔PN persistente.</p>
          </article>
        </div>
      </section>

      <!-- STACK -->
      <section id="stack" class="block alt" aria-labelledby="stack-title">
        <div class="stack-wrap">
          <div class="stack-left">
            <span class="eyebrow">04 · Stack</span>
            <h2 id="stack-title">Siguiendo el patrón <em class="serif-accent">CometaX</em>.</h2>
            <p>FastAPI + SQLAlchemy + PostgreSQL en el backend. Vue 3 + Vite + Pinia en el frontend. Evolution API v2 + Redis para WhatsApp. Nginx sirve todo.</p>
            <ul class="checklist">
              <li><i data-lucide="check" aria-hidden="true"></i> Docker-compose listo para levantar</li>
              <li><i data-lucide="check" aria-hidden="true"></i> Puertos no colisionan con otros proyectos CometaX</li>
              <li><i data-lucide="check" aria-hidden="true"></i> Patrón idéntico al resto del monorepo</li>
              <li><i data-lucide="check" aria-hidden="true"></i> Migraciones idempotentes al boot</li>
            </ul>
          </div>
          <div class="stack-right">
            <figure class="code">
              <figcaption>docker-compose.yml</figcaption>
              <pre><code>services:
  hubos_postgres:
    image: postgres:15-alpine
  hubos_redis:
    image: redis:7-alpine
  hubos_evolution:
    image: evoapicloud/evolution-api:v2.3.7
  hubos_backend:
    build: ./backend
    ports: ["8075:8075"]
  hubos_frontend:
    build: ./frontend
    ports: ["3035:3035"]</code></pre>
            </figure>
          </div>
        </div>
      </section>

      <!-- CTA / Pricing -->
      <section id="pricing" class="block" aria-labelledby="pricing-title">
        <div class="cta-card">
          <span class="eyebrow">05 · Empezar</span>
          <h2 id="pricing-title">
            Empieza en <em class="serif-accent">30 segundos</em>.
          </h2>
          <p>Crea tu workspace, conecta tu primer número y empieza a cerrar.</p>
          <div class="cta-row">
            <router-link to="/register" class="btn btn-primary btn-lg">
              Crear workspace gratis
              <i data-lucide="arrow-right" aria-hidden="true"></i>
            </router-link>
            <router-link to="/login" class="btn btn-ghost btn-lg">
              Ya tengo cuenta
            </router-link>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer" role="contentinfo">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="logo">
            <span class="logo-mark"><i data-lucide="layers"></i></span>
            <span class="logo-word">HubOS</span>
          </div>
          <p>Un solo hub para CRM, CMS, WhatsApp y plantillas.</p>
        </div>

        <nav aria-label="Producto">
          <h4>Producto</h4>
          <a href="#features">Features</a>
          <a href="#modules">Módulos</a>
          <a href="#pricing">Precios</a>
        </nav>
        <nav aria-label="Recursos">
          <h4>Recursos</h4>
          <a href="#stack">Stack</a>
          <a href="#workflow">Cómo funciona</a>
          <router-link to="/register">Registro</router-link>
        </nav>
        <nav aria-label="Legal">
          <h4>Legal</h4>
          <a href="#">Términos</a>
          <a href="#">Privacidad</a>
        </nav>
      </div>
      <div class="footer-copy">© 2026 HubOS · Built on CometaX</div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const menuOpen = ref(false)
const scrollPct = ref(0)

// Respect OS-level reduced-motion preference. If the user has asked the
// system to minimize motion, we skip the tilt/parallax on the mockup.
const allowMotion = ref(
  typeof window !== 'undefined'
    ? !window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
    : true,
)

function onScroll() {
  const h = document.documentElement
  const max = h.scrollHeight - h.clientHeight
  scrollPct.value = max > 0 ? Math.min(1, h.scrollTop / max) : 0
}

function onEsc(e) {
  if (e.key === 'Escape') menuOpen.value = false
}

function refreshIcons() { if (window.lucide) window.lucide.createIcons() }

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keydown', onEsc)
  refreshIcons()
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', onEsc)
})
</script>

<style scoped>
/* =============================================================
   Notion-flavored landing — minimalist dark, typography-first.
   Serif display accents, generous whitespace, subtle hover.
   ============================================================= */

.landing {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  line-height: 1.55;
}

/* Skip link — visible only on keyboard focus. */
.skip-link {
  position: absolute;
  left: 0.5rem;
  top: -40px;
  padding: 0.5rem 0.9rem;
  background: var(--primary);
  color: white;
  border-radius: 8px;
  font-size: 0.85rem;
  z-index: 100;
  transition: top 0.2s;
}
.skip-link:focus { top: 0.5rem; }

/* Global keyboard focus ring — visible on any tabable element. */
.landing :focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 3px;
  border-radius: 6px;
}

/* Scroll progress bar */
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 2px;
  width: 100%;
  background: linear-gradient(90deg, #818cf8, #22d3ee);
  transform-origin: left center;
  transform: scaleX(0);
  z-index: 60;
  transition: transform 0.08s linear;
}

/* Reusable serif accent — Notion-style elegance without going full serif. */
.serif-accent {
  font-family: 'Fraunces', 'Georgia', serif;
  font-style: italic;
  font-weight: 500;
  letter-spacing: -0.01em;
}

/* ---------- NAV ---------- */
.nav {
  position: sticky;
  top: 0;
  z-index: 40;
  backdrop-filter: blur(14px);
  background: rgba(9, 9, 15, 0.78);
  border-bottom: 1px solid var(--border);
}
.nav-inner {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0.85rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: -0.2px;
  color: var(--text);
}
.logo-mark {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.logo-mark :deep(svg) { width: 16px; height: 16px; }
.nav-links {
  display: flex;
  gap: 1.5rem;
  font-size: 0.88rem;
  color: var(--text2);
  font-weight: 500;
  margin-left: auto;
}
.nav-links a { transition: color 0.15s; }
.nav-links a:hover { color: var(--text); }
.nav-cta {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.link-muted { color: var(--text2); font-size: 0.88rem; font-weight: 500; }
.link-muted:hover { color: var(--text); }
.nav-burger {
  display: none;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  width: 38px;
  height: 38px;
  border-radius: 8px;
  align-items: center;
  justify-content: center;
}
.nav-burger :deep(svg) { width: 18px; height: 18px; }

.mobile-menu {
  display: none;
  flex-direction: column;
  padding: 1rem 1.5rem 1.5rem;
  border-top: 1px solid var(--border);
  background: var(--bg);
  gap: 0.2rem;
}
.mobile-menu a {
  padding: 0.75rem 0;
  font-size: 1rem;
  color: var(--text2);
  border-bottom: 1px solid var(--border);
}
.mobile-menu a:hover { color: var(--text); }
.mobile-cta {
  display: flex;
  gap: 0.6rem;
  margin-top: 1rem;
}
.mobile-cta .btn { flex: 1; justify-content: center; }

@media (max-width: 860px) {
  .nav-links, .nav-cta { display: none; }
  .nav-burger { display: inline-flex; margin-left: auto; }
  .mobile-menu.open { display: flex; }
}

/* ---------- HERO ---------- */
.hero {
  position: relative;
  padding: 5rem 1.5rem 6rem;
  overflow: hidden;
  isolation: isolate;
}
.hero-bg {
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
}
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(circle at 55% 40%, black 0%, transparent 70%);
}
.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.35;
}
.orb-a { width: 460px; height: 460px; background: #6366f1; top: -120px; left: -120px; }
.orb-b { width: 360px; height: 360px; background: #06b6d4; bottom: -80px; right: -60px; }

.hero-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 4rem;
  align-items: center;
}
@media (max-width: 960px) {
  .hero-inner { grid-template-columns: 1fr; gap: 2.5rem; }
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.35rem 0.85rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.03);
  font-size: 0.78rem;
  color: var(--text2);
  margin-bottom: 1.5rem;
}
.pill :deep(svg) { width: 14px; height: 14px; color: #fbbf24; }

.hero-title {
  font-family: 'Fraunces', 'Inter', serif;
  font-size: clamp(2.3rem, 5.2vw, 4rem);
  font-weight: 600;
  line-height: 1.04;
  letter-spacing: -0.03em;
  margin-bottom: 1.5rem;
  color: var(--text);
}
.hero-sub {
  color: var(--text2);
  font-size: 1.08rem;
  max-width: 540px;
  line-height: 1.6;
  margin-bottom: 2rem;
}
.hero-cta {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}
.btn-lg {
  padding: 0.85rem 1.4rem;
  font-size: 0.95rem;
  border-radius: 10px;
}
.btn-lg :deep(svg) { width: 16px; height: 16px; }

.stats {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
}
.stat dt {
  font-size: 0.72rem;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
}
.stat dd {
  font-family: 'Fraunces', serif;
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text);
  margin-top: 0.2rem;
}

/* ---------- Mockup ---------- */
.hero-mock { display: flex; justify-content: center; align-items: center; }
.mock {
  width: 100%;
  max-width: 520px;
  border-radius: 16px;
  background: var(--bg2);
  border: 1px solid var(--border);
  box-shadow:
    0 30px 70px -20px rgba(0, 0, 0, 0.7),
    0 0 0 1px rgba(255, 255, 255, 0.03) inset;
  overflow: hidden;
  transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.mock.tilt:hover {
  transform: perspective(1200px) rotateX(3deg) rotateY(-4deg);
}
.mock-chrome {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 0.9rem;
  background: var(--bg3);
  border-bottom: 1px solid var(--border);
}
.dot { width: 10px; height: 10px; border-radius: 50%; }
.d-r { background: #ef4444; }
.d-y { background: #f59e0b; }
.d-g { background: #10b981; }
.mock-url {
  margin-left: 0.6rem;
  font-size: 0.72rem;
  color: var(--text3);
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 0.25rem 0.6rem;
  flex: 1;
  text-align: center;
}

.mock-body {
  display: grid;
  grid-template-columns: 96px 160px 1fr;
  height: 320px;
}
.mock-sidebar {
  background: var(--bg);
  border-right: 1px solid var(--border);
  padding: 0.8rem 0.55rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.mock-s-head {
  font-size: 0.62rem;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.4rem;
  padding-left: 0.3rem;
}
.mock-s-item {
  font-size: 0.72rem;
  color: var(--text2);
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}
.mock-s-item.active {
  background: rgba(99, 102, 241, 0.12);
  color: #a5b4fc;
  font-weight: 600;
}
.pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
  70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.mock-convs {
  background: var(--bg2);
  border-right: 1px solid var(--border);
  padding: 0.6rem 0.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  overflow: hidden;
}
.mock-conv {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.5rem;
  border-radius: 8px;
  position: relative;
}
.mock-conv.active { background: rgba(255, 255, 255, 0.04); }
.mock-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--c, var(--primary));
  color: #0b0b14;
  font-weight: 800;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.mock-n { font-size: 0.72rem; font-weight: 600; color: var(--text); }
.mock-p {
  font-size: 0.65rem;
  color: var(--text3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100px;
}
.mock-badge {
  position: absolute;
  right: 0.4rem;
  top: 50%;
  transform: translateY(-50%);
  background: var(--primary);
  color: white;
  font-size: 0.6rem;
  padding: 1px 6px;
  border-radius: 10px;
  font-weight: 700;
}

.mock-chat {
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  justify-content: flex-end;
  background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.05), transparent);
}
.mock-bubble {
  max-width: 78%;
  padding: 0.5rem 0.7rem;
  border-radius: 10px;
  font-size: 0.75rem;
  line-height: 1.35;
}
.mock-bubble.short { padding: 0.3rem 0.6rem; font-size: 1rem; }
.mock-bubble.in {
  background: var(--bg3);
  border: 1px solid var(--border);
  color: var(--text);
  align-self: flex-start;
}
.mock-bubble.out {
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  align-self: flex-end;
}
.mock-typing {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.45rem 0.7rem;
  display: inline-flex;
  gap: 3px;
  align-self: flex-start;
  width: fit-content;
}
.mock-typing span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--text2);
  opacity: 0.5;
  animation: typing 1.2s infinite ease-in-out;
}
.mock-typing span:nth-child(2) { animation-delay: 0.15s; }
.mock-typing span:nth-child(3) { animation-delay: 0.3s; }
@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-3px); opacity: 1; }
}

@media (max-width: 680px) {
  .mock-body { grid-template-columns: 0 140px 1fr; }
  .mock-sidebar { display: none; }
}

/* ---------- Blocks (sections) ---------- */
.block {
  max-width: 1120px;
  margin: 0 auto;
  padding: 5rem 1.5rem;
  scroll-margin-top: 80px;
}
.block.alt {
  max-width: none;
  background: var(--bg2);
  margin: 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.block.alt > * { max-width: 1120px; margin-inline: auto; }

.block-head { margin-bottom: 3rem; max-width: 720px; }
.eyebrow {
  display: inline-block;
  font-size: 0.72rem;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 600;
  margin-bottom: 0.8rem;
}
.block-head h2 {
  font-family: 'Fraunces', serif;
  font-size: clamp(1.8rem, 3.5vw, 2.6rem);
  font-weight: 600;
  letter-spacing: -0.025em;
  line-height: 1.1;
  margin-bottom: 0.8rem;
  color: var(--text);
}
.block-head p {
  color: var(--text2);
  font-size: 1.02rem;
  line-height: 1.6;
}

/* ---------- Features ---------- */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}
.feature {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.6rem;
  transition: border-color 0.2s, background 0.2s;
}
.feature:hover {
  border-color: rgba(99, 102, 241, 0.4);
  background: rgba(99, 102, 241, 0.05);
}
.f-emoji {
  font-size: 1.8rem;
  margin-bottom: 0.8rem;
  line-height: 1;
}
.feature h3 {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  color: var(--text);
}
.feature p {
  color: var(--text2);
  font-size: 0.88rem;
  line-height: 1.55;
}

/* ---------- Workflow steps ---------- */
.steps {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 0;
  margin: 0;
}
@media (max-width: 780px) {
  .steps { grid-template-columns: 1fr; }
}
.step {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.8rem;
  position: relative;
}
.step-num {
  font-family: 'Fraunces', serif;
  font-size: 2.4rem;
  font-weight: 600;
  background: linear-gradient(135deg, #a5b4fc, #22d3ee);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  margin-bottom: 0.8rem;
}
.step h3 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.4rem; }
.step p { color: var(--text2); font-size: 0.9rem; line-height: 1.55; }

/* ---------- Modules ---------- */
.mod-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}
.mod {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.3rem;
  transition: border-color 0.2s, background 0.2s;
}
.mod:hover {
  border-color: rgba(99, 102, 241, 0.3);
  background: rgba(99, 102, 241, 0.04);
}
.mod :deep(svg) {
  width: 20px;
  height: 20px;
  color: #a5b4fc;
  margin-bottom: 0.6rem;
}
.mod h3 { font-size: 0.95rem; font-weight: 600; margin-bottom: 0.25rem; }
.mod p { color: var(--text2); font-size: 0.82rem; line-height: 1.55; }
.mod code {
  background: rgba(255, 255, 255, 0.06);
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 0.76rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

/* ---------- Stack ---------- */
.stack-wrap {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}
@media (max-width: 860px) {
  .stack-wrap { grid-template-columns: 1fr; }
}
.stack-left h2 {
  font-family: 'Fraunces', serif;
  font-size: clamp(1.8rem, 3.2vw, 2.4rem);
  font-weight: 600;
  margin: 0.8rem 0 1rem;
  letter-spacing: -0.025em;
  line-height: 1.15;
}
.stack-left > p {
  color: var(--text2);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}
.checklist {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  font-size: 0.92rem;
  color: var(--text2);
  padding: 0;
  margin: 0;
}
.checklist li {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}
.checklist :deep(svg) { width: 15px; height: 15px; color: var(--success); flex-shrink: 0; }

.code {
  background: #0b0b14;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
.code figcaption {
  background: var(--bg3);
  padding: 0.55rem 1rem;
  font-size: 0.75rem;
  color: var(--text3);
  border-bottom: 1px solid var(--border);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
.code pre {
  padding: 1.1rem 1.2rem;
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.82rem;
  color: #cbd5e1;
  overflow-x: auto;
  line-height: 1.55;
}

/* ---------- CTA ---------- */
.cta-card {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
  background:
    radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.22) 0%, transparent 70%),
    var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4rem 2rem;
}
.cta-card .eyebrow { margin-bottom: 1.2rem; }
.cta-card h2 {
  font-family: 'Fraunces', serif;
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 600;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 0.8rem;
}
.cta-card p { color: var(--text2); margin-bottom: 1.8rem; font-size: 1rem; }
.cta-row { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; }

/* ---------- Footer ---------- */
.footer {
  border-top: 1px solid var(--border);
  padding: 3rem 1.5rem 2rem;
  background: var(--bg);
}
.footer-inner {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  gap: 2rem;
}
@media (max-width: 680px) {
  .footer-inner { grid-template-columns: 1fr 1fr; }
}
.footer-brand p {
  color: var(--text3);
  font-size: 0.85rem;
  margin-top: 0.6rem;
  max-width: 240px;
  line-height: 1.5;
}
.footer h4 {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text3);
  font-weight: 700;
  margin-bottom: 0.8rem;
}
.footer nav { display: flex; flex-direction: column; gap: 0.5rem; }
.footer nav a {
  color: var(--text2);
  font-size: 0.88rem;
  transition: color 0.15s;
}
.footer nav a:hover { color: var(--text); }
.footer-copy {
  max-width: 1120px;
  margin: 2.5rem auto 0;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  color: var(--text3);
  font-size: 0.8rem;
}

/* ---------- Motion preferences ---------- */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  .mock.tilt:hover { transform: none; }
}
</style>
