<template>
  <div class="landing">
    <!-- Nav -->
    <nav class="nav" :class="{ scrolled: scrolled }">
      <div class="nav-inner">
        <div class="nav-logo">⚡ ServiLink</div>
        <div class="nav-links">
          <a href="#features">Servicios</a>
          <a href="#how">Cómo funciona</a>
          <a href="#plans">Planes</a>
        </div>
        <div class="nav-cta">
          <router-link to="/login" class="btn-ghost">Entrar</router-link>
          <router-link to="/register" class="btn-cta">Comenzar →</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-noise"></div>
      <div class="hero-beams">
        <div class="beam beam-1"></div>
        <div class="beam beam-2"></div>
        <div class="beam beam-3"></div>
      </div>
      <div class="hero-content">
        <div class="hero-eyebrow">
          <span class="eyebrow-dot"></span>
          El profesional correcto, ahora mismo
        </div>
        <h1 class="hero-title">
          Servicios profesionales<br />
          <span class="word-highlight">cerca de ti</span>,<br />
          en el mapa
        </h1>
        <p class="hero-sub">
          Plomeros, electricistas, carpinteros y más.
          Encuentra profesionales verificados en tu zona, ve dónde están en tiempo real y contrátalo en segundos.
        </p>
        <div class="hero-actions">
          <router-link to="/register?role=client" class="btn-primary-glow">
            Buscar profesional
          </router-link>
          <router-link to="/register?role=freelancer" class="btn-outline">
            Ofrecer mis servicios
          </router-link>
        </div>
        <div class="hero-proof">
          <div class="proof-avatars">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a1" class="proof-avatar" />
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a2" class="proof-avatar" />
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a3" class="proof-avatar" />
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=a4" class="proof-avatar" />
          </div>
          <span class="proof-text">+5,000 servicios completados este mes</span>
        </div>
      </div>

      <!-- Map visual -->
      <div class="hero-visual">
        <div class="map-container-demo">
          <div class="map-bg">
            <div class="map-grid"></div>
            <!-- Streets -->
            <div class="street h" style="top:30%;"></div>
            <div class="street h" style="top:55%;"></div>
            <div class="street h" style="top:75%;"></div>
            <div class="street v" style="left:25%;"></div>
            <div class="street v" style="left:55%;"></div>
            <div class="street v" style="left:75%;"></div>
          </div>
          <!-- Pins -->
          <div class="map-pin user-pin" style="top:50%;left:48%;">
            <div class="pin-pulse"></div>
            <div class="pin-dot user"></div>
          </div>
          <div class="map-pin pro-pin" style="top:28%;left:30%;">
            <div class="pin-icon">🔧</div>
            <div class="pin-label">Carlos · $350/hr</div>
          </div>
          <div class="map-pin pro-pin" style="top:40%;left:65%;">
            <div class="pin-icon">⚡</div>
            <div class="pin-label">Ana · $400/hr</div>
          </div>
          <div class="map-pin pro-pin" style="top:65%;left:42%;">
            <div class="pin-icon">🧹</div>
            <div class="pin-label">Roberto · $200/hr</div>
          </div>
          <!-- Radius circle -->
          <div class="radius-circle"></div>
          <!-- Cards floating -->
          <div class="map-card card-top">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=carlos" class="mc-avatar" />
            <div>
              <div class="mc-name">Carlos Ramírez</div>
              <div class="mc-meta">⭐ 4.8 · Plomero · 2.3km</div>
            </div>
            <div class="mc-badge available">Disponible</div>
          </div>
          <div class="map-card card-bottom">
            <div class="mc-status">🚀 En camino</div>
            <div class="mc-eta">Llega en ~15 min</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section class="categories">
      <div class="categories-inner">
        <p class="cats-label">Servicios disponibles</p>
        <div class="cats-row">
          <div class="cat-chip">🔧 Plomería</div>
          <div class="cat-chip">⚡ Electricidad</div>
          <div class="cat-chip">🧹 Limpieza</div>
          <div class="cat-chip">🌿 Jardinería</div>
          <div class="cat-chip">🎨 Pintura</div>
          <div class="cat-chip">🪚 Carpintería</div>
          <div class="cat-chip">🔑 Cerrajería</div>
          <div class="cat-chip">📦 Mudanzas</div>
          <div class="cat-chip">❄️ A/C</div>
          <div class="cat-chip">💻 Tecnología</div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features" id="features">
      <div class="features-inner">
        <div class="section-tag">Plataforma</div>
        <h2 class="section-h2">Diseñado para la velocidad<br />y la confianza</h2>
        <div class="features-bento">
          <div class="bento-card bento-map">
            <div class="bento-icon">🗺️</div>
            <h3>Mapa en tiempo real</h3>
            <p>Ve exactamente dónde están los profesionales disponibles cerca de ti. Filtra por servicio, distancia y calificación.</p>
            <div class="bento-tag">OpenStreetMap · GPS</div>
          </div>
          <div class="bento-card bento-reviews">
            <div class="bento-icon">⭐</div>
            <h3>Reseñas verificadas</h3>
            <p>Solo clientes reales que completaron el servicio pueden dejar reseñas. Transparencia total.</p>
            <div class="stars-demo">
              <div class="star-row"><span>★★★★★</span><div class="star-bar" style="width:80%;"></div></div>
              <div class="star-row"><span>★★★★☆</span><div class="star-bar" style="width:15%;"></div></div>
              <div class="star-row"><span>★★★☆☆</span><div class="star-bar" style="width:5%;"></div></div>
            </div>
          </div>
          <div class="bento-card bento-tracking">
            <div class="bento-icon">🚀</div>
            <h3>Tracking en tiempo real</h3>
            <p>Una vez aceptada tu solicitud, ve la ubicación del profesional moviéndose hacia tu domicilio.</p>
          </div>
          <div class="bento-card bento-subs">
            <div class="bento-icon">⭐</div>
            <h3>Planes para profesionales</h3>
            <p>Freelancers con plan Pro aparecen primero en búsquedas y tienen badge verificado.</p>
            <div class="plan-pills">
              <span class="pill free">Free</span>
              <span class="pill basic">Básico</span>
              <span class="pill pro">Pro ✓</span>
              <span class="pill premium">Premium</span>
            </div>
          </div>
          <div class="bento-card bento-booking">
            <div class="bento-icon">📋</div>
            <h3>Contratos en 1 clic</h3>
            <p>Solicita, acepta y gestiona servicios. El profesional recibe la notificación al instante.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="how" id="how">
      <div class="how-inner">
        <div class="how-left">
          <div class="section-tag">Proceso</div>
          <h2 class="section-h2">Contratar un profesional<br />nunca fue tan fácil</h2>
          <div class="how-steps">
            <div class="how-step" v-for="(step, i) in steps" :key="i">
              <div class="how-step-num">{{ String(i+1).padStart(2,'0') }}</div>
              <div>
                <h3>{{ step.title }}</h3>
                <p>{{ step.desc }}</p>
              </div>
            </div>
          </div>
          <router-link to="/register" class="btn-primary-glow" style="margin-top:32px;display:inline-block;">
            Empezar ahora →
          </router-link>
        </div>
        <div class="how-visual">
          <div class="phone-mockup">
            <div class="phone-screen">
              <div class="phone-nav">⚡ ServiLink</div>
              <div class="phone-search">🔍 ¿Qué servicio necesitas?</div>
              <div class="phone-cats-row">
                <div class="phone-cat">🔧</div>
                <div class="phone-cat active">⚡</div>
                <div class="phone-cat">🧹</div>
                <div class="phone-cat">🌿</div>
              </div>
              <div class="phone-prof-card">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=carlos" class="phone-avatar" />
                <div>
                  <div class="phone-name">Carlos R.</div>
                  <div class="phone-meta">★ 4.8 · 2.3 km · $350/hr</div>
                </div>
                <div class="phone-avail">✓</div>
              </div>
              <div class="phone-prof-card">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=ana" class="phone-avatar" />
                <div>
                  <div class="phone-name">Ana M.</div>
                  <div class="phone-meta">★ 4.6 · 3.1 km · $400/hr</div>
                </div>
                <div class="phone-avail">✓</div>
              </div>
              <div class="phone-btn">Contratar a Carlos →</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Roles -->
    <section class="roles">
      <div class="roles-inner">
        <div class="section-tag">Para todos</div>
        <h2 class="section-h2">Una plataforma, dos roles</h2>
        <div class="roles-grid">
          <div class="role-card client-card">
            <div class="role-icon">👤</div>
            <h3>Para clientes</h3>
            <p>Encuentra profesionales verificados en tu colonia. Ve quién está disponible ahora mismo en el mapa.</p>
            <ul class="role-list">
              <li>Búsqueda por ubicación GPS</li>
              <li>Filtros por categoría y rating</li>
              <li>Reseñas de clientes reales</li>
              <li>Tracking en tiempo real</li>
              <li>Historial de servicios</li>
            </ul>
            <router-link to="/register?role=client" class="role-cta">Buscar servicios →</router-link>
          </div>
          <div class="role-card freelancer-card">
            <div class="role-icon">🔧</div>
            <h3>Para profesionales</h3>
            <p>Aparece en el mapa de tu zona, recibe solicitudes y cobra por tu trabajo. Tú decides cuándo estar disponible.</p>
            <ul class="role-list">
              <li>Perfil verificado con badge</li>
              <li>Aparece en el mapa de búsqueda</li>
              <li>Gestiona solicitudes fácilmente</li>
              <li>Cobra por hora o por servicio</li>
              <li>Suscripciones desde $0</li>
            </ul>
            <router-link to="/register?role=freelancer" class="role-cta freelancer">Ofrecer servicios →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Plans -->
    <section class="plans" id="plans">
      <div class="plans-inner">
        <div class="section-tag">Para freelancers</div>
        <h2 class="section-h2">Elige tu plan</h2>
        <p class="plans-sub">Empieza gratis. Escala cuando tu negocio crezca.</p>
        <div class="plans-grid">
          <div v-for="plan in plansList" :key="plan.id" class="plan-card" :class="{ featured: plan.featured }">
            <div v-if="plan.featured" class="plan-ribbon">⭐ Más popular</div>
            <div class="plan-name">{{ plan.name }}</div>
            <div class="plan-price">${{ plan.price }}<span>/mes</span></div>
            <ul class="plan-features">
              <li v-for="f in plan.features" :key="f">{{ f }}</li>
            </ul>
            <router-link to="/register?role=freelancer" :class="['plan-btn', plan.featured && 'featured']">
              {{ plan.cta }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Final -->
    <section class="cta-final">
      <div class="cta-orbs">
        <div class="orb orb1"></div>
        <div class="orb orb2"></div>
      </div>
      <div class="cta-content">
        <h2>¿Necesitas algo reparado hoy?</h2>
        <p>Un profesional cerca de ti está listo para ayudarte. Ahora mismo.</p>
        <div class="cta-btns">
          <router-link to="/register?role=client" class="btn-primary-glow">Buscar profesional →</router-link>
          <router-link to="/register?role=freelancer" class="btn-outline">Unirme como profesional</router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">⚡ ServiLink</div>
          <p class="footer-tagline">Servicios profesionales, donde los necesitas.</p>
        </div>
        <div class="footer-links">
          <router-link to="/login">Iniciar sesión</router-link>
          <router-link to="/register">Registrarse</router-link>
        </div>
      </div>
      <div class="footer-copy">© 2025 ServiLink. Construido con ❤️ en México.</div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)
function onScroll() { scrolled.value = window.scrollY > 20 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const steps = [
  { title: 'Abre el mapa', desc: 'Ve los profesionales disponibles en tu zona en tiempo real. Filtra por servicio y distancia.' },
  { title: 'Elige y contrata', desc: 'Lee reseñas, ve el perfil y contrata en un clic. El profesional recibe la solicitud al instante.' },
  { title: 'Sigue su ubicación', desc: 'Monitorea al profesional en el mapa mientras se acerca a tu domicilio.' },
  { title: 'Califica el servicio', desc: 'Una vez terminado, deja tu reseña para ayudar a la comunidad.' },
]

const plansList = [
  { id: 'free', name: 'Free', price: 0, features: ['1 servicio activo', 'Aparece en el mapa', 'Gestión básica'], cta: 'Empezar gratis', featured: false },
  { id: 'pro', name: 'Pro', price: 499, features: ['Hasta 20 servicios', 'Badge verificado ✓', 'Aparece primero', 'Estadísticas'], cta: 'Activar Pro', featured: true },
  { id: 'premium', name: 'Premium', price: 999, features: ['Servicios ilimitados', 'Badge premium ✓✓', 'Prioridad máxima', 'Soporte 24/7'], cta: 'Ir a Premium', featured: false },
]
</script>

<style scoped>
* { box-sizing: border-box; }
.landing { background: #0a0a0f; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; overflow-x: hidden; }

/* NAV */
.nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; padding: 16px 0; transition: all 0.3s; }
.nav.scrolled { background: rgba(10,10,15,0.85); backdrop-filter: blur(24px); border-bottom: 1px solid rgba(99,102,241,0.1); }
.nav-inner { max-width: 1280px; margin: 0 auto; padding: 0 32px; display: flex; align-items: center; gap: 32px; }
.nav-logo { font-size: 20px; font-weight: 900; color: #6366f1; flex-shrink: 0; }
.nav-links { display: flex; gap: 32px; flex: 1; justify-content: center; }
.nav-links a { color: #64748b; text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }
.nav-links a:hover { color: #e2e8f0; }
.nav-cta { display: flex; align-items: center; gap: 12px; }
.btn-ghost { color: #64748b; text-decoration: none; font-size: 14px; padding: 8px 16px; transition: color 0.2s; font-weight: 500; }
.btn-ghost:hover { color: #e2e8f0; }
.btn-cta { background: #6366f1; color: white; font-size: 14px; font-weight: 700; padding: 9px 20px; border-radius: 8px; text-decoration: none; transition: all 0.2s; }
.btn-cta:hover { background: #4f46e5; }

/* HERO */
.hero { min-height: 100vh; display: flex; align-items: center; padding: 100px 32px 60px; max-width: 1280px; margin: 0 auto; gap: 80px; position: relative; }
.hero-noise { position: fixed; inset: 0; opacity: 0.03; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); background-size: 200px; pointer-events: none; z-index: 0; }
.hero-beams { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
.beam { position: absolute; width: 1px; background: linear-gradient(to bottom, transparent, rgba(99,102,241,0.4) 40%, rgba(16,185,129,0.2) 70%, transparent); animation: beamFall 4s linear infinite; }
.beam-1 { left: 20%; height: 40%; top: -10%; animation-delay: 0s; }
.beam-2 { left: 60%; height: 60%; top: -20%; animation-delay: 1.5s; opacity: 0.6; }
.beam-3 { left: 85%; height: 30%; top: -5%; animation-delay: 3s; opacity: 0.4; }
@keyframes beamFall { 0%{transform:translateY(-100%);opacity:0;} 10%{opacity:1;} 90%{opacity:1;} 100%{transform:translateY(200vh);opacity:0;} }

.hero-content { flex: 1; position: relative; z-index: 1; }
.hero-eyebrow { display: inline-flex; align-items: center; gap: 8px; color: #6366f1; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 24px; }
.eyebrow-dot { width: 6px; height: 6px; background: #10b981; border-radius: 50%; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.hero-title { font-size: clamp(42px, 5.5vw, 72px); font-weight: 900; line-height: 1.05; letter-spacing: -0.04em; margin-bottom: 24px; }
.word-highlight { position: relative; color: #6366f1; }
.word-highlight::after { content: ''; position: absolute; bottom: -4px; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #6366f1, #10b981); border-radius: 2px; }
.hero-sub { font-size: 18px; color: #64748b; line-height: 1.7; max-width: 480px; margin-bottom: 36px; }
.hero-actions { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 40px; }
.btn-primary-glow { display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; font-weight: 700; font-size: 15px; padding: 14px 28px; border-radius: 10px; text-decoration: none; transition: all 0.3s; box-shadow: 0 0 40px rgba(99,102,241,0.3); }
.btn-primary-glow:hover { transform: translateY(-2px); box-shadow: 0 8px 40px rgba(99,102,241,0.5); }
.btn-outline { display: inline-flex; align-items: center; gap: 8px; background: transparent; color: #e2e8f0; font-weight: 600; font-size: 15px; padding: 14px 28px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); text-decoration: none; transition: all 0.2s; }
.btn-outline:hover { border-color: rgba(99,102,241,0.4); background: rgba(99,102,241,0.06); }
.hero-proof { display: flex; align-items: center; gap: 12px; }
.proof-avatars { display: flex; }
.proof-avatar { width: 28px; height: 28px; border-radius: 50%; border: 2px solid #0a0a0f; margin-left: -8px; }
.proof-avatar:first-child { margin-left: 0; }
.proof-text { font-size: 13px; color: #475569; }

/* MAP DEMO */
.hero-visual { flex: 1; position: relative; z-index: 1; }
.map-container-demo { position: relative; background: #111120; border: 1px solid rgba(99,102,241,0.2); border-radius: 20px; overflow: hidden; aspect-ratio: 1; box-shadow: 0 40px 100px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.04), inset 0 0 80px rgba(99,102,241,0.03); max-width: 500px; }
.map-bg { position: absolute; inset: 0; }
.map-grid { position: absolute; inset: 0; background-image: linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px); background-size: 40px 40px; }
.street { position: absolute; background: rgba(99,102,241,0.06); }
.street.h { left: 0; right: 0; height: 12px; }
.street.v { top: 0; bottom: 0; width: 10px; }
.map-pin { position: absolute; transform: translate(-50%, -50%); z-index: 10; }
.pin-pulse { position: absolute; inset: -8px; background: rgba(99,102,241,0.15); border-radius: 50%; animation: ripple 2s infinite; }
.pin-dot { width: 14px; height: 14px; border-radius: 50%; border: 3px solid white; position: relative; }
.pin-dot.user { background: #6366f1; }
@keyframes ripple { 0%{transform:scale(1);opacity:1;} 100%{transform:scale(3);opacity:0;} }
.pro-pin { cursor: pointer; }
.pin-icon { width: 36px; height: 36px; background: #10b981; border-radius: 50%; border: 3px solid white; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.4); animation: floatPin 3s ease-in-out infinite; }
.pro-pin:nth-child(3) .pin-icon { background: #6366f1; animation-delay: 1s; }
.pro-pin:nth-child(4) .pin-icon { background: #f59e0b; animation-delay: 2s; }
@keyframes floatPin { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-5px);} }
.pin-label { position: absolute; bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%); background: rgba(10,10,15,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 4px 8px; font-size: 10px; white-space: nowrap; color: #e2e8f0; backdrop-filter: blur(8px); }
.radius-circle { position: absolute; width: 40%; height: 40%; top: 30%; left: 28%; border: 1px dashed rgba(99,102,241,0.3); border-radius: 50%; }
.map-card { position: absolute; background: rgba(17,17,32,0.95); border: 1px solid rgba(99,102,241,0.2); border-radius: 12px; padding: 10px 14px; backdrop-filter: blur(16px); min-width: 200px; }
.card-top { top: 8px; right: 8px; display: flex; align-items: center; gap: 10px; }
.card-bottom { bottom: 12px; left: 12px; }
.mc-avatar { width: 32px; height: 32px; border-radius: 50%; }
.mc-name { font-size: 12px; font-weight: 600; }
.mc-meta { font-size: 10px; color: #64748b; }
.mc-badge { font-size: 10px; padding: 2px 8px; border-radius: 999px; margin-left: auto; }
.mc-badge.available { background: rgba(16,185,129,0.2); color: #10b981; }
.mc-status { font-size: 12px; font-weight: 600; color: #6366f1; }
.mc-eta { font-size: 11px; color: #64748b; margin-top: 2px; }

/* CATEGORIES */
.categories { border-top: 1px solid rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04); padding: 28px 32px; }
.categories-inner { max-width: 1280px; margin: 0 auto; }
.cats-label { font-size: 12px; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; }
.cats-row { display: flex; gap: 10px; flex-wrap: wrap; }
.cat-chip { background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.15); border-radius: 999px; padding: 6px 14px; font-size: 13px; font-weight: 500; color: #94a3b8; transition: all 0.2s; cursor: default; }
.cat-chip:hover { border-color: rgba(99,102,241,0.4); color: #e2e8f0; }

/* FEATURES */
.features { padding: 100px 32px; }
.features-inner { max-width: 1280px; margin: 0 auto; }
.section-tag { display: inline-block; background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); color: #6366f1; border-radius: 999px; padding: 4px 14px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 20px; }
.section-h2 { font-size: clamp(28px, 4vw, 48px); font-weight: 800; letter-spacing: -0.03em; line-height: 1.15; margin-bottom: 48px; }
.features-bento { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: auto auto; gap: 16px; }
.bento-card { background: #111118; border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 32px; transition: all 0.3s; }
.bento-card:hover { border-color: rgba(99,102,241,0.25); transform: translateY(-3px); }
.bento-map { grid-column: span 2; background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(16,185,129,0.03)); }
.bento-reviews { grid-column: span 1; }
.bento-tracking { grid-column: span 1; }
.bento-subs { grid-column: span 1; }
.bento-booking { grid-column: span 1; }
.bento-icon { font-size: 28px; margin-bottom: 16px; }
.bento-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
.bento-card p { font-size: 14px; color: #64748b; line-height: 1.6; }
.bento-tag { display: inline-block; margin-top: 16px; background: rgba(16,185,129,0.1); color: #10b981; border-radius: 6px; padding: 4px 10px; font-size: 11px; font-weight: 600; }
.stars-demo { margin-top: 16px; display: flex; flex-direction: column; gap: 6px; }
.star-row { display: flex; align-items: center; gap: 8px; font-size: 11px; color: #f59e0b; }
.star-bar { height: 4px; background: rgba(245,158,11,0.3); border-radius: 2px; flex: 1; }
.plan-pills { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 16px; }
.pill { padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; }
.pill.free { background: rgba(255,255,255,0.06); color: #64748b; }
.pill.basic { background: rgba(99,102,241,0.15); color: #6366f1; }
.pill.pro { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.pill.premium { background: rgba(245,158,11,0.15); color: #f59e0b; }

/* HOW */
.how { padding: 100px 32px; background: rgba(99,102,241,0.02); border-top: 1px solid rgba(99,102,241,0.06); border-bottom: 1px solid rgba(99,102,241,0.06); }
.how-inner { max-width: 1280px; margin: 0 auto; display: flex; gap: 80px; align-items: flex-start; }
.how-left { flex: 1; }
.how-steps { display: flex; flex-direction: column; gap: 32px; }
.how-step { display: flex; gap: 20px; }
.how-step-num { font-size: 32px; font-weight: 900; color: rgba(99,102,241,0.2); line-height: 1; min-width: 48px; }
.how-step h3 { font-size: 17px; font-weight: 700; margin-bottom: 6px; }
.how-step p { font-size: 14px; color: #64748b; line-height: 1.6; }
.how-visual { flex: 1; display: flex; justify-content: center; }
.phone-mockup { width: 260px; background: #0f0f1a; border: 2px solid rgba(255,255,255,0.08); border-radius: 36px; padding: 24px 16px; box-shadow: 0 40px 80px rgba(0,0,0,0.5); }
.phone-screen { display: flex; flex-direction: column; gap: 12px; }
.phone-nav { font-size: 16px; font-weight: 800; color: #6366f1; text-align: center; }
.phone-search { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 10px 12px; font-size: 12px; color: #475569; }
.phone-cats-row { display: flex; gap: 8px; justify-content: center; }
.phone-cat { width: 36px; height: 36px; background: rgba(255,255,255,0.04); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.phone-cat.active { background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4); }
.phone-prof-card { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px; }
.phone-avatar { width: 32px; height: 32px; border-radius: 50%; }
.phone-name { font-size: 12px; font-weight: 600; }
.phone-meta { font-size: 10px; color: #64748b; }
.phone-avail { margin-left: auto; width: 20px; height: 20px; background: rgba(16,185,129,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #10b981; }
.phone-btn { background: #6366f1; color: white; text-align: center; border-radius: 10px; padding: 12px; font-size: 13px; font-weight: 700; }

/* ROLES */
.roles { padding: 100px 32px; }
.roles-inner { max-width: 1280px; margin: 0 auto; }
.roles-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.role-card { background: #111118; border: 1px solid rgba(255,255,255,0.06); border-radius: 24px; padding: 40px; display: flex; flex-direction: column; gap: 20px; }
.client-card { border-color: rgba(99,102,241,0.15); }
.freelancer-card { border-color: rgba(16,185,129,0.15); background: linear-gradient(135deg, #111118, rgba(16,185,129,0.03)); }
.role-icon { font-size: 36px; }
.role-card h3 { font-size: 22px; font-weight: 800; }
.role-card p { font-size: 15px; color: #64748b; line-height: 1.6; }
.role-list { list-style: none; display: flex; flex-direction: column; gap: 10px; flex: 1; }
.role-list li { font-size: 14px; color: #94a3b8; padding-left: 16px; position: relative; }
.role-list li::before { content: '→'; position: absolute; left: 0; color: #6366f1; }
.freelancer-card .role-list li::before { color: #10b981; }
.role-cta { display: inline-block; padding: 12px 24px; background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); border-radius: 10px; color: #6366f1; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.2s; }
.role-cta:hover { background: rgba(99,102,241,0.2); }
.role-cta.freelancer { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.2); color: #10b981; }
.role-cta.freelancer:hover { background: rgba(16,185,129,0.2); }

/* PLANS */
.plans { padding: 100px 32px; background: rgba(255,255,255,0.01); border-top: 1px solid rgba(255,255,255,0.04); }
.plans-inner { max-width: 1000px; margin: 0 auto; }
.plans-sub { font-size: 18px; color: #64748b; margin-bottom: 48px; }
.plans-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.plan-card { background: #111118; border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 32px; display: flex; flex-direction: column; gap: 20px; position: relative; }
.plan-card.featured { border-color: rgba(99,102,241,0.3); background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(16,185,129,0.03)); box-shadow: 0 0 60px rgba(99,102,241,0.08); }
.plan-ribbon { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 999px; white-space: nowrap; }
.plan-name { font-size: 15px; font-weight: 600; color: #64748b; }
.plan-price { font-size: 40px; font-weight: 900; }
.plan-price span { font-size: 16px; font-weight: 400; color: #64748b; }
.plan-features { list-style: none; display: flex; flex-direction: column; gap: 10px; flex: 1; }
.plan-features li { font-size: 14px; color: #94a3b8; padding-left: 16px; position: relative; }
.plan-features li::before { content: '✓'; position: absolute; left: 0; color: #10b981; }
.plan-btn { display: block; text-align: center; padding: 12px; border-radius: 10px; font-weight: 700; font-size: 14px; text-decoration: none; border: 1px solid rgba(255,255,255,0.08); color: #94a3b8; transition: all 0.2s; }
.plan-btn:hover { border-color: rgba(99,102,241,0.3); color: #e2e8f0; }
.plan-btn.featured { background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border-color: transparent; box-shadow: 0 4px 24px rgba(99,102,241,0.3); }
.plan-btn.featured:hover { box-shadow: 0 8px 32px rgba(99,102,241,0.4); }

/* CTA FINAL */
.cta-final { padding: 120px 32px; text-align: center; position: relative; overflow: hidden; }
.cta-orbs { position: absolute; inset: 0; pointer-events: none; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); }
.orb1 { width: 400px; height: 400px; background: rgba(99,102,241,0.1); top: 50%; left: 30%; transform: translate(-50%, -50%); }
.orb2 { width: 300px; height: 300px; background: rgba(16,185,129,0.08); top: 50%; left: 70%; transform: translate(-50%, -50%); }
.cta-content { position: relative; z-index: 1; }
.cta-content h2 { font-size: clamp(32px, 5vw, 56px); font-weight: 900; letter-spacing: -0.03em; margin-bottom: 16px; }
.cta-content p { font-size: 18px; color: #64748b; margin-bottom: 36px; }
.cta-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

/* FOOTER */
.footer { border-top: 1px solid rgba(255,255,255,0.06); padding: 40px 32px 24px; }
.footer-inner { max-width: 1280px; margin: 0 auto; display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
.footer-logo { font-size: 20px; font-weight: 900; color: #6366f1; margin-bottom: 8px; }
.footer-tagline { font-size: 13px; color: #475569; }
.footer-links { display: flex; gap: 24px; }
.footer-links a { color: #64748b; text-decoration: none; font-size: 14px; transition: color 0.2s; }
.footer-links a:hover { color: #94a3b8; }
.footer-copy { max-width: 1280px; margin: 0 auto; font-size: 12px; color: #374151; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 24px; }
</style>
