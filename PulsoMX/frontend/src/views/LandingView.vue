<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { plansApi, demoApi, billingApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const plans = ref([])
const seeding = ref(null)
const paying = ref(null)
const error = ref(null)

const industries = [
  { id: 'gym',         name: 'Gimnasio',     icon: 'mdi-dumbbell',          tint: 'violet', quote: '"Bajé a la mitad el tiempo en caja y duplique mis reinscripciones."' },
  { id: 'yoga',        name: 'Yoga / Pilates', icon: 'mdi-meditation',      tint: 'emerald', quote: '"Mis alumnos reservan desde el cel. Ya no pierdo clases por no-shows."' },
  { id: 'coworking',   name: 'Coworking',    icon: 'mdi-monitor-dashboard', tint: 'sky',     quote: '"Cada miembro entra con QR. Veo ocupación por hora del día."' },
  { id: 'dojo',        name: 'Dojo / MMA',   icon: 'mdi-karate',            tint: 'pink',    quote: '"Exámenes de grado con bitácora limpia. Papás felices."' },
]

const features = [
  { icon: 'mdi-qrcode-scan',       t: 'Check-in por QR', d: 'Cada miembro con su QR. Tablet en recepción, cámara del cel, NFC. 2 segundos.' },
  { icon: 'mdi-calendar-check',    t: 'Clases + reservas', d: 'Capacidad, instructor, sala. Tu alumno reserva desde su cel.' },
  { icon: 'mdi-credit-card-outline', t: 'Cobros Stripe + Conekta', d: 'Tarjeta, OXXO, SPEI. Suscripciones automáticas. CFDI 4.0.' },
  { icon: 'mdi-account-multiple',  t: 'Miembros 360', d: 'Historial, foto, membresías, visitas restantes, notas. Todo junto.' },
  { icon: 'mdi-chart-line',        t: 'Retención y churn', d: 'MRR, churn, cohortes, nuevas altas, clases más llenas. Listo.' },
  { icon: 'mdi-file-excel',        t: 'Excel + CFDI', d: 'Miembros, asistencias y pagos a Excel. Factura al día siguiente.' },
  { icon: 'mdi-message-text',      t: 'WhatsApp reminders', d: 'Confirma reserva, avisa vencimiento de pago, felicita cumpleaños.' },
  { icon: 'mdi-palette',           t: 'Tu marca', d: 'Logo, color brand, dominio propio. Tus alumnos ven TU app.' },
]

async function loadPlans() {
  try {
    const { data } = await plansApi.list()
    plans.value = data.length ? data : fallback()
  } catch { plans.value = fallback() }
}
function fallback() {
  return [
    { id:'free', name:'Gratis', price_mxn:0, max_members:30, max_venues:1, max_staff:2, has_bookings:true, has_payments:false, has_whatsapp:false, has_custom_brand:false, featured:false, description:'Para empezar: 30 miembros, QR check-in, agenda de clases.' },
    { id:'starter', name:'Starter', price_mxn:699, max_members:200, max_venues:1, max_staff:5, has_bookings:true, has_payments:true, has_whatsapp:false, has_custom_brand:false, featured:false, description:'Perfecto para estudios pequeños. Cobros Stripe/Conekta.' },
    { id:'pro', name:'Pro', price_mxn:1499, max_members:1000, max_venues:3, max_staff:15, has_bookings:true, has_payments:true, has_whatsapp:true, has_custom_brand:true, featured:true, description:'Cadena con varias sucursales. WhatsApp + branding propio.' },
    { id:'enterprise', name:'Enterprise', price_mxn:4999, max_members:999999, max_venues:999, max_staff:999, has_bookings:true, has_payments:true, has_whatsapp:true, has_custom_brand:true, featured:false, description:'Franquicias. CFDI, SSO, multi-región.' },
  ]
}

async function tryDemo(industry) {
  seeding.value = industry; error.value = null
  try {
    const { data } = await demoApi.seed(industry)
    if (data.error) throw new Error(data.error)
    session.set({ tenant_id: data.tenant_id, name: data.name, industry, brand_color: data.brand_color })
    router.push('/app/dashboard')
  } catch (e) { error.value = e?.response?.data?.detail || e.message }
  finally { seeding.value = null }
}

async function startCheckout(plan_id, provider) {
  paying.value = `${plan_id}-${provider}`
  error.value = null
  try {
    // Crear tenant ghost si no hay sesión
    let tid = session.tenantId
    if (!tid) {
      const { data: t } = await (await import('../api/endpoints')).tenantsApi.create({ name: `Trial ${Date.now()}`, industry: 'gym', plan_id })
      session.set(t)
    }
    const { data } = await billingApi.checkout({ plan_id, provider })
    window.location.href = data.checkout_url
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { paying.value = null }
}

function peso(n) { return new Intl.NumberFormat('es-MX', { style:'currency', currency:'MXN', maximumFractionDigits:0 }).format(n) }

onMounted(loadPlans)
</script>

<template>
  <div class="landing">
    <!-- Animated aura -->
    <div class="aura aura-1"></div>
    <div class="aura aura-2"></div>
    <div class="aura aura-3"></div>

    <!-- NAV -->
    <nav class="nav">
      <div class="container nav-inner">
        <router-link to="/" class="brand">
          <div class="brand-mark">
            <span class="bm-glow"></span>
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h3l2-6 3 12 2-8 2 4h6"/></svg>
          </div>
          <div class="brand-name">Pulso<span class="gradient-text">MX</span></div>
        </router-link>
        <div class="nav-links">
          <a href="#cases">Casos</a>
          <a href="#features">Funciones</a>
          <a href="#pricing">Precios</a>
          <router-link to="/demo" class="btn btn-sm nav-demo">Entrar al demo</router-link>
          <router-link to="/demo" class="btn btn-gradient btn-sm">Empezar <i class="mdi mdi-arrow-right"></i></router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-pill">
          <span class="pill-dot"></span>
          <span>En vivo · Stripe + Conekta listo · 14 días gratis</span>
        </div>
        <h1 class="hero-title">
          El software para tu <span class="serif">estudio</span><br/>
          que <span class="gradient-text">tus miembros aman</span>.
        </h1>
        <p class="hero-lede">
          Gimnasios, yoga, coworkings y dojos.
          Check-in por QR, clases con reservas, cobros recurrentes y WhatsApp — todo en una.
        </p>
        <div class="hero-ctas">
          <router-link to="/demo" class="btn btn-gradient btn-lg">
            <i class="mdi mdi-rocket-launch"></i> Probar con datos reales
          </router-link>
          <a href="#pricing" class="btn btn-lg btn-ghost">Ver precios</a>
        </div>

        <!-- MOCKUP -->
        <div class="mockup">
          <div class="mockup-shadow"></div>

          <!-- Big dashboard card -->
          <div class="m-dash">
            <div class="m-dash-top">
              <div class="m-brand">
                <div class="m-logo"><i class="mdi mdi-meditation"></i></div>
                <div>
                  <div class="m-title">Soma Yoga</div>
                  <div class="m-sub muted">Dashboard · hoy</div>
                </div>
              </div>
              <div class="m-top-badges">
                <span class="pill pill-violet"><span class="dot"></span> En vivo</span>
              </div>
            </div>

            <div class="m-kpis">
              <div class="kpi-box"><div class="kpi-label">Check-ins hoy</div><div class="kpi-val">48</div><div class="kpi-chip up">+12%</div></div>
              <div class="kpi-box"><div class="kpi-label">Miembros activos</div><div class="kpi-val">312</div><div class="kpi-chip up">+8</div></div>
              <div class="kpi-box"><div class="kpi-label">MRR este mes</div><div class="kpi-val">$48,720</div><div class="kpi-chip up">+14%</div></div>
            </div>

            <div class="m-chart">
              <svg viewBox="0 0 400 80" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0" stop-color="#ec4899" stop-opacity=".35"/>
                    <stop offset="1" stop-color="#ec4899" stop-opacity="0"/>
                  </linearGradient>
                </defs>
                <path d="M0 60 C 40 40, 80 50, 120 35 S 200 20, 240 30 S 320 10, 400 20 L 400 80 L 0 80 Z" fill="url(#g1)"/>
                <path d="M0 60 C 40 40, 80 50, 120 35 S 200 20, 240 30 S 320 10, 400 20" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
          </div>

          <!-- Floating QR card -->
          <div class="m-float m-qr">
            <div class="qr-art">
              <div class="qr-grid">
                <div v-for="i in 64" :key="i" class="qr-dot" :class="{ on: [0,1,2,5,6,7,9,11,14,18,20,23,27,28,31,33,36,39,42,45,48,52,55,58,61,62,63].includes(i-1) }"></div>
              </div>
            </div>
            <div class="qr-txt">
              <div style="font-weight:700;font-size:13px;">Ana Ramírez</div>
              <div class="muted" style="font-size:11px;">PM-1024 · Activo</div>
            </div>
          </div>

          <!-- Floating payment card -->
          <div class="m-float m-pay">
            <div class="pay-head">
              <div class="pay-logo">
                <svg viewBox="0 0 60 25" height="16"><path fill="#6772e5" d="M5.8 9.9c0-.6.5-.9 1.3-.9 1.2 0 2.7.4 3.9 1V6.3c-1.3-.5-2.6-.7-3.9-.7C3.9 5.6 1.7 7.3 1.7 10c0 4.3 5.9 3.6 5.9 5.5 0 .8-.7 1-1.5 1-1.3 0-3-.5-4.3-1.3v3.9c1.4.6 2.9.9 4.3.9 3.3 0 5.6-1.6 5.6-4.3 0-4.6-6-3.7-6-5.8zm7.8-6l-3.9.8-.1 12.8c0 2.4 1.8 4.1 4.2 4.1 1.3 0 2.3-.2 2.9-.5v-3.3c-.5.2-3.1 1-3.1-1.4v-5.3h3.1v-3.4h-3.1zM21 10.7l-.3-1.2h-3.4v13.9h3.9v-9.4c.9-1.2 2.5-1 3-.8V9.5c-.5-.2-2.3-.5-3.2 1.2zm4.3-5.3v3.5l3.9-.8V5zm0 4.1h3.9v13.9h-3.9zm8.4 0l-3.9.8v13.1h3.9zm3.1-8.2v1.6h-1v1.4h1v11.5c0 2.3 1.7 3.2 3.4 3.2.9 0 1.6-.2 2-.3v-1.5c-.4.1-2.4.7-2.4-1.4V4.3H41V2.9h-1.3V.9zm9.6 8.1c-4 0-6.4 3.4-6.4 7.1 0 4.4 2.5 7.2 6.5 7.2 1.9 0 3.4-.5 4.6-1.2v-3.1c-1.2.6-2.5 1-4.2 1-1.7 0-3.1-.6-3.3-2.6h8.3c0-.2 0-1.1 0-1.4.1-3.9-1.8-7-5.5-7zm-1.9 5.7c0-1.9 1.2-2.8 2.3-2.8 1.1 0 2.2.9 2.2 2.8z"/></svg>
                <span>Checkout</span>
              </div>
              <span class="pay-ok"><i class="mdi mdi-check-circle"></i></span>
            </div>
            <div class="pay-amount">$1,499.00 <span class="muted" style="font-size:12px;font-weight:500;">MXN</span></div>
            <div class="muted" style="font-size:11px;">Plan Mensual Ilimitado · Tarjeta ••4242</div>
          </div>

          <!-- Floating class card -->
          <div class="m-float m-class">
            <div class="class-time">18:00</div>
            <div>
              <div style="font-weight:700;font-size:13px;">Vinyasa Flow</div>
              <div class="muted" style="font-size:11px;">Laura M. · 18/22</div>
            </div>
            <div class="capacity-bar"><div class="cap-fill" style="width:82%;"></div></div>
          </div>
        </div>

        <!-- Trust row -->
        <div class="trust-row">
          <div class="trust-brands muted">Construido con:</div>
          <div class="trust-logo">Stripe</div>
          <div class="trust-sep">·</div>
          <div class="trust-logo">Conekta</div>
          <div class="trust-sep">·</div>
          <div class="trust-logo">WhatsApp Cloud</div>
          <div class="trust-sep">·</div>
          <div class="trust-logo">CFDI 4.0</div>
        </div>
      </div>
    </section>

    <!-- CASES -->
    <section id="cases" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Casos</span>
          <h2 class="h2">Funciona para <span class="serif">cualquier</span> estudio</h2>
          <p class="muted lead">Clic para crear un tenant demo con miembros, clases, pagos e instructores reales.</p>
        </div>
        <div class="cases-grid">
          <button v-for="i in industries" :key="i.id" class="case" :class="[`c-${i.tint}`, { busy: seeding === i.id }]" @click="tryDemo(i.id)">
            <div class="case-top">
              <div class="case-ico"><i :class="['mdi', i.icon]"></i></div>
              <div class="case-arrow"><i class="mdi mdi-arrow-top-right"></i></div>
            </div>
            <div class="case-name">{{ i.name }}</div>
            <p class="case-quote serif">{{ i.quote }}</p>
            <div class="case-cta">
              <span v-if="seeding === i.id"><i class="mdi mdi-loading mdi-spin"></i> Creando demo…</span>
              <span v-else>Probar <i class="mdi mdi-arrow-right"></i></span>
            </div>
          </button>
        </div>
        <p v-if="error" class="center muted" style="color:var(--danger); margin-top:14px;">{{ error }}</p>
      </div>
    </section>

    <!-- FEATURES -->
    <section id="features" class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow light">Todo lo que necesitas</span>
          <h2 class="h2 light">Una suite completa, no un chunche más.</h2>
        </div>
        <div class="features-grid">
          <div v-for="f in features" :key="f.t" class="feature">
            <div class="feat-ico"><i :class="['mdi', f.icon]"></i></div>
            <h3>{{ f.t }}</h3>
            <p>{{ f.d }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS -->
    <section class="section section-stats">
      <div class="container stats-grid">
        <div class="stat"><div class="stat-val gradient-text">5s</div><div class="stat-lbl">Check-in por QR</div></div>
        <div class="stat"><div class="stat-val gradient-text">$0</div><div class="stat-lbl">Comisión de plataforma</div></div>
        <div class="stat"><div class="stat-val gradient-text">99.9%</div><div class="stat-lbl">Uptime garantizado</div></div>
        <div class="stat"><div class="stat-val gradient-text">14 días</div><div class="stat-lbl">Prueba gratis, sin tarjeta</div></div>
      </div>
    </section>

    <!-- PRICING -->
    <section id="pricing" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Planes en MXN</span>
          <h2 class="h2">Empieza <span class="serif">gratis</span>. Paga cuando crezcas.</h2>
          <p class="muted lead">Los botones abajo te llevan a <b>Stripe Checkout</b> o <b>Conekta</b>. Modo demo activo si aún no conectas tus keys.</p>
        </div>
        <div class="pricing-grid">
          <div v-for="p in plans" :key="p.id" class="plan" :class="{ featured: p.featured }">
            <div v-if="p.featured" class="plan-ribbon"><i class="mdi mdi-star"></i> Más popular</div>
            <div class="plan-head">
              <div class="plan-name">{{ p.name }}</div>
              <div class="plan-price">
                <template v-if="Number(p.price_mxn) === 0"><span class="pp-free">Gratis</span></template>
                <template v-else>
                  <span class="pp-cur">$</span><span class="pp-num">{{ Number(p.price_mxn).toLocaleString('es-MX') }}</span>
                  <span class="pp-per">/mes</span>
                </template>
              </div>
              <p class="plan-desc muted">{{ p.description }}</p>
            </div>
            <ul class="plan-feats">
              <li><i class="mdi mdi-check-circle"></i> {{ p.max_members >= 999999 ? 'Miembros ilimitados' : `Hasta ${p.max_members.toLocaleString('es-MX')} miembros` }}</li>
              <li><i class="mdi mdi-check-circle"></i> {{ p.max_venues >= 999 ? 'Sucursales ilimitadas' : `${p.max_venues} sucursal${p.max_venues>1?'es':''}` }}</li>
              <li><i class="mdi mdi-check-circle"></i> {{ p.max_staff >= 999 ? 'Staff ilimitado' : `${p.max_staff} usuarios staff` }}</li>
              <li :class="{ dim: !p.has_payments }"><i :class="['mdi', p.has_payments ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> Stripe + Conekta</li>
              <li :class="{ dim: !p.has_whatsapp }"><i :class="['mdi', p.has_whatsapp ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> Recordatorios WhatsApp</li>
              <li :class="{ dim: !p.has_custom_brand }"><i :class="['mdi', p.has_custom_brand ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> Branding propio</li>
              <li><i class="mdi mdi-check-circle"></i> Export Excel + CFDI</li>
            </ul>
            <div class="plan-pay">
              <button v-if="Number(p.price_mxn) === 0" class="btn plan-cta" @click="router.push('/demo')">Empezar gratis</button>
              <template v-else>
                <button class="btn btn-primary plan-cta" :disabled="paying === `${p.id}-stripe`" @click="startCheckout(p.id,'stripe')">
                  <i class="mdi mdi-credit-card-outline"></i>
                  {{ paying === `${p.id}-stripe` ? 'Abriendo…' : 'Pagar con Stripe' }}
                </button>
                <button class="btn plan-cta btn-conekta" :disabled="paying === `${p.id}-conekta`" @click="startCheckout(p.id,'conekta')">
                  <span class="cokdot"></span>
                  Conekta (OXXO/SPEI)
                </button>
              </template>
            </div>
          </div>
        </div>
        <div class="pricing-foot center muted">
          ¿Franquicia o +1000 miembros? <a href="mailto:ventas@pulsomx.mx">Habla con ventas</a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section">
      <div class="container">
        <div class="cta-card">
          <div class="cta-grid-dots"></div>
          <h2>Tu estudio merece <span class="serif">mejor software</span>.</h2>
          <p>Sin contratos, sin implementación eterna. Creas el demo, lo pruebas, decides.</p>
          <router-link to="/demo" class="btn btn-gradient btn-lg"><i class="mdi mdi-rocket-launch"></i> Crear mi demo</router-link>
        </div>
      </div>
    </section>

    <footer class="foot">
      <div class="container foot-in">
        <div><b class="gradient-text">PulsoMX</b> · Parte de <a href="https://cometax.dev">CometaX</a> · Hecho en 🇲🇽</div>
        <div class="muted small">
          API <span class="mono">/membership/v1</span> · <a href="/docs">Docs</a> · <a href="/health">Health</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing { position: relative; overflow-x: clip; }

/* Auras (ambient background glow) */
.aura { position: absolute; border-radius: 50%; filter: blur(120px); opacity: .4; z-index: -1; pointer-events: none; }
.aura-1 { width: 600px; height: 600px; background: #7c3aed; top: -200px; left: -150px; }
.aura-2 { width: 580px; height: 580px; background: #ec4899; top: 260px; right: -220px; }
.aura-3 { width: 480px; height: 480px; background: #f59e0b; top: 900px; left: 30%; opacity: .25; }
[data-theme="dark"] .aura { opacity: .22; }

/* NAV */
.nav { position: sticky; top: 0; z-index: 50;
  background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border); }
.nav-inner { display: flex; justify-content: space-between; align-items: center; padding: 14px 24px; }
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit; font-weight: 700; }
.brand:hover { text-decoration: none; }
.brand-mark { position: relative; width: 34px; height: 34px; border-radius: 10px;
  background: var(--brand-grad); color: white; display: grid; place-items: center;
  box-shadow: 0 4px 12px rgba(124,58,237,.35); overflow: hidden; }
.bm-glow { position: absolute; inset: -50%; background: conic-gradient(from 0deg, transparent, white 20%, transparent 40%); animation: spin 4s linear infinite; opacity: .3; }
@keyframes spin { to { transform: rotate(360deg); } }
.brand-name { font-size: 17px; letter-spacing: -0.02em; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-links a { color: var(--text-muted); font-size: 14px; font-weight: 500; }
.nav-links a:not(.btn):hover { color: var(--text); text-decoration: none; }
.nav-demo { background: transparent !important; border-color: var(--border-strong) !important; color: var(--text) !important; }

/* HERO */
.hero { padding: 64px 24px 30px; }
.hero-inner { text-align: center; max-width: 900px; margin: 0 auto; }
.hero-pill { display: inline-flex; align-items: center; gap: 8px; padding: 7px 16px; border-radius: 999px;
  background: var(--surface); border: 1px solid var(--border-strong);
  font-size: 13px; font-weight: 500; color: var(--text-muted); margin-bottom: 28px;
  box-shadow: var(--shadow-sm); }
.pill-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 0 3px var(--emerald-soft); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { box-shadow: 0 0 0 3px var(--emerald-soft); } 50% { box-shadow: 0 0 0 6px transparent; } }

.hero-title { font-size: clamp(42px, 7vw, 88px); font-weight: 800; line-height: 1; letter-spacing: -0.04em; margin: 0 0 22px; }
.serif { font-family: var(--font-serif); font-style: italic; font-weight: 400; }

.hero-lede { max-width: 580px; margin: 0 auto 36px; font-size: 19px; color: var(--text-muted); line-height: 1.55; }
.hero-ctas { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 64px; }

/* Mockup */
.mockup { position: relative; max-width: 820px; margin: 0 auto; height: 380px; perspective: 1500px; }
.mockup-shadow { position: absolute; inset: 10% 5% -5% 5%; background: radial-gradient(ellipse 60% 50% at center, rgba(124,58,237,.35), transparent 70%); filter: blur(30px); z-index: -1; }
.m-dash { position: relative; z-index: 3; background: var(--surface); border: 1px solid var(--border);
  border-radius: 18px; padding: 20px; box-shadow: var(--shadow-lg); max-width: 520px; margin: 0 auto;
  animation: floatA 8s ease-in-out infinite; text-align: left; }
.m-dash-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.m-brand { display: flex; align-items: center; gap: 10px; }
.m-logo { width: 36px; height: 36px; border-radius: 10px; background: var(--emerald-soft); color: var(--emerald); display: grid; place-items: center; font-size: 18px; }
.m-title { font-weight: 700; font-size: 15px; }
.m-sub { font-size: 11px; }
.pill { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; }
.pill-violet { background: var(--violet-soft); color: var(--violet); }
.pill .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

.m-kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-box { padding: 12px; background: var(--bg-subtle); border-radius: 12px; }
.kpi-label { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: .05em; }
.kpi-val { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin: 4px 0; }
.kpi-chip { display: inline-block; font-size: 11px; padding: 2px 7px; border-radius: 999px; font-weight: 600; }
.kpi-chip.up { background: var(--emerald-soft); color: var(--emerald); }
.m-chart { height: 60px; margin-top: 4px; }
.m-chart svg { width: 100%; height: 100%; }

.m-float { position: absolute; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 14px; box-shadow: var(--shadow-md); }
.m-qr { left: 0; top: 50px; width: 210px; display: flex; gap: 12px; align-items: center; z-index: 4; animation: floatB 7s ease-in-out infinite; }
.qr-art { width: 60px; flex-shrink: 0; }
.qr-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 1.5px; padding: 5px; background: white; border-radius: 6px; }
.qr-dot { aspect-ratio: 1; background: transparent; border-radius: 1px; }
.qr-dot.on { background: #09090b; }
.qr-txt {}

.m-pay { right: 0; top: 24px; width: 230px; z-index: 4; animation: floatC 9s ease-in-out infinite; }
.pay-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.pay-logo { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--text-muted); font-weight: 600; }
.pay-ok { color: var(--emerald); font-size: 18px; }
.pay-amount { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 2px; }

.m-class { right: 6%; bottom: 0; width: 220px; display: flex; align-items: center; gap: 10px; z-index: 4; animation: floatB 8s ease-in-out infinite -2s; }
.class-time { font-weight: 800; font-size: 20px; color: var(--pink); letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.capacity-bar { position: absolute; bottom: 6px; left: 14px; right: 14px; height: 3px; background: var(--bg-subtle); border-radius: 2px; overflow: hidden; }
.cap-fill { height: 100%; background: var(--brand-grad); border-radius: 2px; }

@keyframes floatA { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes floatB { 0%,100% { transform: translateY(0) rotate(-3deg); } 50% { transform: translateY(-10px) rotate(-3deg); } }
@keyframes floatC { 0%,100% { transform: translateY(0) rotate(3deg); } 50% { transform: translateY(-8px) rotate(3deg); } }

@media (max-width: 720px) {
  .mockup { height: 620px; }
  .m-qr, .m-pay, .m-class { position: static; width: 90%; margin: 14px auto; animation: none; transform: none !important; }
  .m-dash { max-width: 90%; }
}

.trust-row { margin-top: 48px; display: flex; gap: 14px; justify-content: center; align-items: center; flex-wrap: wrap; font-size: 13px; color: var(--text-muted); }
.trust-brands { font-weight: 500; }
.trust-logo { font-weight: 700; letter-spacing: -0.01em; font-size: 15px; color: var(--text); }
.trust-sep { opacity: .4; }

/* SECTIONS */
.section { padding: 96px 24px; }
.section-dark { background: #09090b; color: #fafafa; }
.section-dark .h2, .section-dark h3 { color: white; }
.section-dark .eyebrow.light { background: rgba(255,255,255,.1); color: #f9a8d4; }

.section-head { text-align: center; max-width: 720px; margin: 0 auto 64px; }
.eyebrow { display: inline-block; font-size: 12px; text-transform: uppercase; letter-spacing: .14em; color: var(--violet); font-weight: 700; padding: 5px 12px; border-radius: 999px; background: var(--violet-soft); }
.h2 { font-size: clamp(32px, 5vw, 56px); font-weight: 800; letter-spacing: -0.035em; margin: 18px 0 14px; line-height: 1.05; }
.lead { font-size: 17px; line-height: 1.55; margin: 0; }
.light { color: white; }
.center { text-align: center; }

/* CASES */
.cases-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
.case { position: relative; text-align: left; background: var(--surface); border: 1px solid var(--border);
  border-radius: 18px; padding: 22px; cursor: pointer; font-family: inherit; color: inherit;
  transition: all .25s cubic-bezier(.4,0,.2,1); overflow: hidden; }
.case:hover { transform: translateY(-6px); border-color: var(--c, var(--violet)); box-shadow: 0 20px 40px color-mix(in srgb, var(--c) 30%, transparent); }
.case.busy { opacity: .6; pointer-events: none; }
.case-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.case-ico { width: 48px; height: 48px; border-radius: 12px; background: var(--c-soft); color: var(--c); display: grid; place-items: center; font-size: 24px; transition: transform .3s; }
.case:hover .case-ico { transform: rotate(-8deg) scale(1.1); }
.case-arrow { color: var(--text-subtle); font-size: 18px; transition: transform .3s; }
.case:hover .case-arrow { color: var(--c); transform: translate(4px, -4px); }
.case-name { font-weight: 800; font-size: 19px; letter-spacing: -0.01em; margin-bottom: 8px; }
.case-quote { font-size: 14px; color: var(--text-muted); line-height: 1.55; margin: 0 0 16px; min-height: 64px; }
.case-cta { font-size: 13px; color: var(--c); font-weight: 700; display: inline-flex; align-items: center; gap: 4px; }
.case.c-violet  { --c: #7c3aed; --c-soft: var(--violet-soft); }
.case.c-emerald { --c: #10b981; --c-soft: var(--emerald-soft); }
.case.c-sky     { --c: #0ea5e9; --c-soft: var(--sky-soft); }
.case.c-pink    { --c: #ec4899; --c-soft: var(--pink-soft); }

/* FEATURES dark */
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 2px; background: #27272e; border-radius: 20px; overflow: hidden; border: 1px solid #27272e; }
.feature { background: #09090b; padding: 28px 26px; transition: background .2s; }
.feature:hover { background: #111114; }
.feat-ico { width: 42px; height: 42px; border-radius: 10px; background: linear-gradient(135deg, #7c3aed, #ec4899); color: white; display: grid; place-items: center; font-size: 22px; margin-bottom: 14px; }
.feature h3 { font-size: 16px; margin: 0 0 6px; font-weight: 700; letter-spacing: -0.01em; color: white; }
.feature p { font-size: 13.5px; line-height: 1.55; margin: 0; color: #a1a1aa; }

/* STATS */
.section-stats { padding: 40px 24px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 24px; text-align: center; }
.stat-val { font-size: clamp(38px, 5vw, 56px); font-weight: 800; letter-spacing: -0.03em; line-height: 1; }
.stat-lbl { font-size: 14px; color: var(--text-muted); margin-top: 6px; font-weight: 500; }

/* PRICING */
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; align-items: stretch; }
.plan { position: relative; background: var(--surface); border: 1px solid var(--border); border-radius: 22px;
  padding: 30px 26px; display: flex; flex-direction: column; transition: all .25s;
  box-shadow: var(--shadow-sm); }
.plan:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.plan.featured { border: 2px solid transparent;
  background:
    linear-gradient(var(--surface), var(--surface)) padding-box,
    var(--brand-grad) border-box;
  box-shadow: 0 20px 48px rgba(124,58,237,.18); }
.plan-ribbon { position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  padding: 5px 14px; background: var(--brand-grad); color: white; font-size: 11px;
  border-radius: 999px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase;
  box-shadow: 0 6px 14px rgba(124,58,237,.4); display: inline-flex; align-items: center; gap: 4px; }
.plan-ribbon .mdi { font-size: 13px; color: #fef3c7; }
.plan-head { margin-bottom: 20px; }
.plan-name { font-size: 13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .1em; font-weight: 800; }
.plan-price { margin: 12px 0 6px; line-height: 1; }
.pp-cur { font-size: 22px; color: var(--text-muted); vertical-align: top; font-weight: 700; }
.pp-num { font-size: 44px; font-weight: 800; letter-spacing: -0.035em; }
.pp-per { font-size: 14px; color: var(--text-muted); font-weight: 500; }
.pp-free { font-size: 40px; font-weight: 800; letter-spacing: -0.02em; background: var(--brand-grad); -webkit-background-clip: text; background-clip: text; color: transparent; }
.plan-desc { font-size: 13px; line-height: 1.5; min-height: 40px; margin: 8px 0 0; }
.plan-feats { list-style: none; padding: 0; margin: 0 0 22px; font-size: 14px; flex: 1; }
.plan-feats li { padding: 6px 0; display: flex; align-items: center; gap: 10px; }
.plan-feats li .mdi { flex-shrink: 0; color: var(--emerald); font-size: 17px; }
.plan-feats li.dim { color: var(--text-muted); }
.plan-feats li.dim .mdi { color: var(--text-subtle); }
.plan-pay { display: flex; flex-direction: column; gap: 8px; }
.plan-cta { width: 100%; justify-content: center; font-weight: 700; }
.btn-conekta { background: white; color: #00b884; border: 1.5px solid #00b884; }
.btn-conekta:hover { background: #f0fdf4; }
.cokdot { width: 10px; height: 10px; border-radius: 50%; background: #00b884; }

.pricing-foot { margin-top: 40px; font-size: 14px; }

/* CTA */
.cta-card { position: relative; overflow: hidden;
  background: var(--brand-grad); border-radius: 32px;
  padding: 80px 40px; text-align: center; color: white;
  box-shadow: var(--shadow-lg); }
.cta-grid-dots { position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,.2) 1px, transparent 1px);
  background-size: 20px 20px; opacity: .3; mask: radial-gradient(ellipse at center, black 30%, transparent 75%); }
.cta-card h2 { font-size: clamp(32px, 5vw, 52px); font-weight: 800; letter-spacing: -0.03em; margin: 0 0 16px; line-height: 1.05; color: white; position: relative; }
.cta-card p { font-size: 17px; opacity: .95; margin: 0 0 32px; position: relative; }
.cta-card .btn { position: relative; background: white; color: var(--violet); border: none; box-shadow: 0 8px 24px rgba(0,0,0,.2); font-weight: 800; }
.cta-card .btn:hover { transform: translateY(-2px); box-shadow: 0 12px 32px rgba(0,0,0,.3); }

/* FOOT */
.foot { padding: 32px 24px; border-top: 1px solid var(--border); }
.foot-in { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 14px; color: var(--text-muted); }
.small { font-size: 12px; }

@media (max-width: 700px) {
  .nav-links a:not(.btn) { display: none; }
  .section { padding: 60px 20px; }
  .section-head { margin-bottom: 40px; }
  .hero { padding: 40px 20px 20px; }
}
</style>
