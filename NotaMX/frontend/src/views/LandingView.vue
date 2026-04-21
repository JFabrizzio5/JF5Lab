<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { plansApi, demoApi, tenantsApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const plans = ref([])
const seeding = ref(null)
const error = ref(null)

const industries = [
  { id: 'freelance',   name: 'Freelancers',  icon: 'mdi-palette-outline',     tint: 'emerald',
    quote: '"Mando la cotización por WhatsApp y al cliente le llega con link de pago. Cobro el mismo día."' },
  { id: 'consultorio', name: 'Consultorios', icon: 'mdi-stethoscope',          tint: 'teal',
    quote: '"Cada paciente recibe su nota antes de salir. El recibo CFDI llega solo. Cero papeleo."' },
  { id: 'abogados',    name: 'Despachos',    icon: 'mdi-gavel',                tint: 'violet',
    quote: '"Mis clientes corporativos piden factura siempre. Ahora la emito desde el mismo flujo de cobro."' },
  { id: 'agencia',     name: 'Agencias',     icon: 'mdi-rocket-launch-outline', tint: 'coral',
    quote: '"Retainers mensuales automáticos. El flujo con Conekta OXXO/SPEI nos destrabó el efectivo."' },
]

const steps = [
  { n: 1, icon: 'mdi-file-document-edit-outline', t: 'Creas la nota', d: 'Cliente, conceptos y totales. IVA calculado automático.' },
  { n: 2, icon: 'mdi-whatsapp',                   t: 'Mandas por WhatsApp', d: 'Un link público con tu marca. Ven la nota y pagan ahí mismo.' },
  { n: 3, icon: 'mdi-credit-card-fast-outline',   t: 'Cliente paga', d: 'Tarjeta con Stripe o OXXO/SPEI con Conekta. Cobras desde $10 MXN.' },
  { n: 4, icon: 'mdi-file-certificate-outline',   t: 'CFDI auto', d: 'Emites factura 4.0 del mismo registro. XML + PDF al correo del cliente.' },
]

const features = [
  { icon: 'mdi-whatsapp',                     t: 'WhatsApp nativo',          d: 'Plantillas aprobadas. Recordatorios, confirmaciones y gracias post-pago.' },
  { icon: 'mdi-credit-card-outline',          t: 'Stripe + Conekta',         d: 'Tarjeta, OXXO, SPEI y transferencia. Una sola cuenta en NotaMX.' },
  { icon: 'mdi-file-certificate-outline',     t: 'CFDI 4.0 automático',      d: 'Con tu e.firma y CSD. Timbrado y cancelación al mismo click.' },
  { icon: 'mdi-link-variant',                 t: 'Link público de pago',     d: 'Tu cliente ve tu marca, tu nota y paga sin crear cuenta.' },
  { icon: 'mdi-qrcode',                       t: 'QR para mostrador',        d: 'Pega el QR en tu caja. Tu cliente escanea y paga desde el cel.' },
  { icon: 'mdi-chart-line',                   t: 'Dashboard con MTD',        d: 'Notas enviadas, cobradas, conversión. Top clientes y serie mensual.' },
  { icon: 'mdi-file-excel-outline',           t: 'Exportar Excel',           d: 'Notas y pagos. Entrega contable en 1 clic.' },
  { icon: 'mdi-palette-outline',              t: 'Tu marca',                 d: 'Logo, color y RFC. Tus clientes ven una experiencia tuya.' },
]

async function loadPlans() {
  try {
    const { data } = await plansApi.list()
    plans.value = data.length ? data : fallback()
  } catch { plans.value = fallback() }
}
function fallback() {
  return [
    { id:'free', name:'Gratis', price_mxn:0, max_notes_month:5, max_customers:20, has_whatsapp:false, has_cfdi:false, has_branding:false, has_api:false, featured:false,
      description:'Ideal para empezar: 5 notas por mes, link público de pago.' },
    { id:'pro', name:'Pro', price_mxn:299, max_notes_month:60, max_customers:200, has_whatsapp:true, has_cfdi:true, has_branding:false, has_api:false, featured:false,
      description:'Notas ilimitadas dentro del plan, WhatsApp y CFDI 4.0 automático.' },
    { id:'growth', name:'Growth', price_mxn:999, max_notes_month:500, max_customers:2000, has_whatsapp:true, has_cfdi:true, has_branding:true, has_api:false, featured:true,
      description:'PYMEs en crecimiento. Branding propio, recordatorios WhatsApp, reportes.' },
    { id:'business', name:'Business', price_mxn:2499, max_notes_month:999999, max_customers:999999, has_whatsapp:true, has_cfdi:true, has_branding:true, has_api:true, featured:false,
      description:'Negocios con volumen. API, multi-usuario, SLA prioritario.' },
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

const paying = ref(null)
async function startCheckout(plan_id, provider) {
  paying.value = `${plan_id}-${provider}`
  error.value = null
  try {
    // Crear tenant trial si no hay
    let tid = session.tenantId
    if (!tid) {
      const { data: t } = await tenantsApi.create({ name: `Trial ${Date.now()}`, industry: 'freelance', plan_id })
      session.set(t)
    }
    // para planes SaaS, no hay nota; abrimos demo checkout directo
    const base = window.location.origin
    const ref = `plan_${plan_id}_${Date.now()}`
    const plan = plans.value.find(p => p.id === plan_id)
    const amount = plan?.price_mxn || 0
    const url = `${base}/billing/demo-checkout/${provider}?ref=${ref}&amount=${amount}`
    // Intentamos real checkout endpoint primero (simulado con una nota "saas"): pero MVP: abrir demo directo
    window.location.href = url
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally { paying.value = null }
}

onMounted(loadPlans)
</script>

<template>
  <div class="landing">
    <div class="aura aura-1"></div>
    <div class="aura aura-2"></div>

    <!-- NAV -->
    <nav class="nav">
      <div class="container nav-inner">
        <router-link to="/" class="brand">
          <div class="brand-mark">
            <i class="mdi mdi-receipt-text-check"></i>
          </div>
          <div class="brand-name">Nota<span class="gradient-text">MX</span></div>
        </router-link>
        <div class="nav-links">
          <a href="#como-funciona">Cómo funciona</a>
          <a href="#casos">Casos</a>
          <a href="#precios">Precios</a>
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
          <span>Stripe + Conekta listo · CFDI 4.0 incluido · 14 días gratis</span>
        </div>
        <h1 class="hero-title">
          Cobra como los <span class="serif">grandes</span>,<br/>
          <span class="gradient-text">sin la burocracia</span>.
        </h1>
        <p class="hero-lede">
          Freelancers, consultorios y PYMEs de México.
          Mandas la nota por WhatsApp, tu cliente paga con tarjeta u OXXO, y el CFDI sale solo.
        </p>
        <div class="hero-ctas">
          <router-link to="/demo" class="btn btn-gradient btn-lg">
            <i class="mdi mdi-whatsapp"></i> Probar con datos reales
          </router-link>
          <a href="#precios" class="btn btn-lg btn-ghost">Ver precios</a>
        </div>

        <!-- MOCKUP -->
        <div class="mockup">
          <div class="mockup-shadow"></div>

          <div class="m-dash">
            <div class="m-dash-top">
              <div class="m-brand">
                <div class="m-logo"><i class="mdi mdi-palette-outline"></i></div>
                <div>
                  <div class="m-title">Estudio Mora</div>
                  <div class="m-sub muted">Dashboard · abril</div>
                </div>
              </div>
              <div class="m-top-badges">
                <span class="pill pill-emerald"><span class="dot"></span> En vivo</span>
              </div>
            </div>

            <div class="m-kpis">
              <div class="kpi-box"><div class="kpi-label">Notas enviadas</div><div class="kpi-val">24</div><div class="kpi-chip up">+9%</div></div>
              <div class="kpi-box"><div class="kpi-label">Cobradas</div><div class="kpi-val">18</div><div class="kpi-chip up">75%</div></div>
              <div class="kpi-box"><div class="kpi-label">Ingresos MTD</div><div class="kpi-val">$91,060</div><div class="kpi-chip up">+18%</div></div>
            </div>

            <div class="m-chart">
              <svg viewBox="0 0 400 80" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0" stop-color="#10b981" stop-opacity=".35"/>
                    <stop offset="1" stop-color="#10b981" stop-opacity="0"/>
                  </linearGradient>
                </defs>
                <path d="M0 60 C 40 40, 80 50, 120 35 S 200 20, 240 30 S 320 10, 400 20 L 400 80 L 0 80 Z" fill="url(#g1)"/>
                <path d="M0 60 C 40 40, 80 50, 120 35 S 200 20, 240 30 S 320 10, 400 20" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
          </div>

          <!-- Floating WA card -->
          <div class="m-float m-wa">
            <div class="wa-head">
              <i class="mdi mdi-whatsapp" style="color:#25d366;font-size:20px;"></i>
              <div style="font-weight:700;font-size:13px;">Fernanda Torres</div>
            </div>
            <div class="wa-msg">
              Hola Fernanda, te compartimos la nota <b>NT-0012</b> por <b>$8,500.00 MXN</b>. Link de pago: <span class="wa-link">notamx.mx/n/a9f2</span>
            </div>
            <div class="wa-tick muted"><i class="mdi mdi-check-all"></i> Entregado · visto</div>
          </div>

          <!-- Floating CFDI -->
          <div class="m-float m-cfdi">
            <div class="cfdi-head">
              <i class="mdi mdi-file-certificate-outline" style="color:var(--emerald);font-size:20px;"></i>
              <div>
                <div style="font-weight:700;font-size:13px;">CFDI A-1012</div>
                <div class="muted" style="font-size:11px;">UUID · SAT</div>
              </div>
            </div>
            <div class="cfdi-amount">$8,500.00 <span class="muted" style="font-size:11px;">MXN</span></div>
            <div class="cfdi-state"><i class="mdi mdi-check-circle"></i> Timbrado</div>
          </div>
        </div>

        <div class="trust-row">
          <div class="trust-brands muted">Integra:</div>
          <div class="trust-logo">Stripe</div>
          <div class="trust-sep">·</div>
          <div class="trust-logo">Conekta</div>
          <div class="trust-sep">·</div>
          <div class="trust-logo">WhatsApp Cloud</div>
          <div class="trust-sep">·</div>
          <div class="trust-logo">SAT · CFDI 4.0</div>
        </div>
      </div>
    </section>

    <!-- COMO FUNCIONA -->
    <section id="como-funciona" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Cómo funciona</span>
          <h2 class="h2">Del <span class="serif">pitch</span> al pago, en <span class="gradient-text">4 pasos</span>.</h2>
          <p class="muted lead">Sin instalaciones. Sin capacitaciones. Entras, creas tu primera nota y ya estás cobrando.</p>
        </div>
        <div class="steps-grid">
          <div v-for="s in steps" :key="s.n" class="step">
            <div class="step-n">{{ s.n }}</div>
            <div class="step-ico"><i :class="['mdi', s.icon]"></i></div>
            <h3>{{ s.t }}</h3>
            <p>{{ s.d }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CASOS -->
    <section id="casos" class="section section-surface">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Casos</span>
          <h2 class="h2">Hecho para quienes <span class="serif">venden</span> su tiempo.</h2>
          <p class="muted lead">Clic para crear un tenant demo con clientes, productos y notas en estados reales.</p>
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
    <section class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow light">Todo lo esencial</span>
          <h2 class="h2 light">Sin marañas. Solo lo que cobra.</h2>
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
        <div class="stat"><div class="stat-val gradient-text">3 min</div><div class="stat-lbl">Crear y cobrar tu primera nota</div></div>
        <div class="stat"><div class="stat-val gradient-text">0%</div><div class="stat-lbl">Comisión de plataforma</div></div>
        <div class="stat"><div class="stat-val gradient-text">CFDI 4.0</div><div class="stat-lbl">Certificado SAT incluido</div></div>
        <div class="stat"><div class="stat-val gradient-text">14 días</div><div class="stat-lbl">Gratis, sin tarjeta</div></div>
      </div>
    </section>

    <!-- PRICING -->
    <section id="precios" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Precios en MXN</span>
          <h2 class="h2">Empieza <span class="serif">gratis</span>. Paga solo cuando cobres más.</h2>
          <p class="muted lead">Los botones abajo abren <b>Stripe Checkout</b> o <b>Conekta</b>. Si no hay API key configurada, usamos el demo checkout.</p>
        </div>
        <div class="pricing-grid">
          <div v-for="p in plans" :key="p.id" class="plan" :class="{ featured: p.featured }">
            <div v-if="p.featured" class="plan-ribbon"><i class="mdi mdi-star"></i> Más elegido</div>
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
              <li><i class="mdi mdi-check-circle"></i>
                {{ p.max_notes_month >= 999999 ? 'Notas ilimitadas' : `${p.max_notes_month.toLocaleString('es-MX')} notas al mes` }}
              </li>
              <li><i class="mdi mdi-check-circle"></i>
                {{ p.max_customers >= 999999 ? 'Clientes ilimitados' : `${p.max_customers.toLocaleString('es-MX')} clientes` }}
              </li>
              <li :class="{ dim: !p.has_whatsapp }"><i :class="['mdi', p.has_whatsapp ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> WhatsApp nativo</li>
              <li :class="{ dim: !p.has_cfdi }"><i :class="['mdi', p.has_cfdi ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> CFDI 4.0 automático</li>
              <li :class="{ dim: !p.has_branding }"><i :class="['mdi', p.has_branding ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> Branding propio</li>
              <li :class="{ dim: !p.has_api }"><i :class="['mdi', p.has_api ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> API pública</li>
              <li><i class="mdi mdi-check-circle"></i> Stripe + Conekta</li>
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
          ¿Volumen corporativo o franquicia? <a href="mailto:ventas@notamx.mx">Habla con ventas</a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section">
      <div class="container">
        <div class="cta-card">
          <div class="cta-grid-dots"></div>
          <h2>Tu primera cobrada en <span class="serif">3 minutos</span>.</h2>
          <p>Creas una nota demo, mandas el link, y el "pago recibido" llega a tu WhatsApp.</p>
          <router-link to="/demo" class="btn btn-lg"><i class="mdi mdi-rocket-launch"></i> Crear mi demo</router-link>
        </div>
      </div>
    </section>

    <footer class="foot">
      <div class="container foot-in">
        <div><b class="gradient-text">NotaMX</b> · Parte de <a href="https://cometax.dev">CometaX</a> · Hecho en Mexico</div>
        <div class="muted small">
          API <span class="mono">/notas/v1</span> · <a href="/docs">Docs</a> · <a href="/health">Health</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing { position: relative; overflow-x: clip; }

.aura { position: absolute; border-radius: 50%; filter: blur(120px); opacity: .4; z-index: -1; pointer-events: none; }
.aura-1 { width: 620px; height: 620px; background: #10b981; top: -220px; left: -180px; }
.aura-2 { width: 560px; height: 560px; background: #14b8a6; top: 280px; right: -200px; opacity: .3; }
[data-theme="dark"] .aura { opacity: .2; }

.nav { position: sticky; top: 0; z-index: 50;
  background: color-mix(in srgb, var(--bg) 85%, transparent);
  backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border); }
.nav-inner { display: flex; justify-content: space-between; align-items: center; padding: 14px 24px; }
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit; font-weight: 700; }
.brand:hover { text-decoration: none; }
.brand-mark { width: 34px; height: 34px; border-radius: 10px;
  background: var(--brand-grad); color: white; display: grid; place-items: center;
  box-shadow: 0 4px 12px rgba(16,185,129,.35); font-size: 18px; }
.brand-name { font-size: 17px; letter-spacing: -0.02em; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-links a { color: var(--text-muted); font-size: 14px; font-weight: 500; }
.nav-links a:not(.btn):hover { color: var(--text); text-decoration: none; }
.nav-demo { background: transparent !important; border-color: var(--border-strong) !important; color: var(--text) !important; }

/* HERO */
.hero { padding: 64px 24px 30px; }
.hero-inner { text-align: center; max-width: 960px; margin: 0 auto; }
.hero-pill { display: inline-flex; align-items: center; gap: 8px; padding: 7px 16px; border-radius: 999px;
  background: var(--surface); border: 1px solid var(--border-strong);
  font-size: 13px; font-weight: 500; color: var(--text-muted); margin-bottom: 28px;
  box-shadow: var(--shadow-sm); }
.pill-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 0 3px var(--emerald-soft); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { box-shadow: 0 0 0 3px var(--emerald-soft); } 50% { box-shadow: 0 0 0 6px transparent; } }

.hero-title { font-size: clamp(42px, 7vw, 88px); font-weight: 800; line-height: 1; letter-spacing: -0.04em; margin: 0 0 22px; }

.hero-lede { max-width: 620px; margin: 0 auto 36px; font-size: 19px; color: var(--text-muted); line-height: 1.55; }
.hero-ctas { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 64px; }

/* Mockup */
.mockup { position: relative; max-width: 860px; margin: 0 auto; height: 360px; }
.mockup-shadow { position: absolute; inset: 10% 5% -5% 5%; background: radial-gradient(ellipse 60% 50% at center, rgba(16,185,129,.35), transparent 70%); filter: blur(30px); z-index: -1; }
.m-dash { position: relative; z-index: 3; background: var(--surface); border: 1px solid var(--border);
  border-radius: 18px; padding: 20px; box-shadow: var(--shadow-lg); max-width: 520px; margin: 0 auto;
  animation: floatA 8s ease-in-out infinite; text-align: left; }
.m-dash-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.m-brand { display: flex; align-items: center; gap: 10px; }
.m-logo { width: 36px; height: 36px; border-radius: 10px; background: var(--emerald-soft); color: var(--emerald-dark); display: grid; place-items: center; font-size: 18px; }
.m-title { font-weight: 700; font-size: 15px; }
.m-sub { font-size: 11px; }
.pill { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; }
.pill-emerald { background: var(--emerald-soft); color: var(--emerald-dark); }
.pill .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

.m-kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-box { padding: 12px; background: var(--bg-subtle); border-radius: 12px; }
.kpi-label { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: .05em; }
.kpi-val { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin: 4px 0; }
.kpi-chip { display: inline-block; font-size: 11px; padding: 2px 7px; border-radius: 999px; font-weight: 600; }
.kpi-chip.up { background: var(--emerald-soft); color: var(--emerald-dark); }
.m-chart { height: 60px; margin-top: 4px; }
.m-chart svg { width: 100%; height: 100%; }

.m-float { position: absolute; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 14px; box-shadow: var(--shadow-md); z-index: 4; }
.m-wa { left: 0; top: 50px; width: 240px; animation: floatB 7s ease-in-out infinite; }
.wa-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.wa-msg { font-size: 12px; line-height: 1.4; background: #dcf8c6; color: #0b1613; padding: 8px 10px; border-radius: 10px; margin-bottom: 6px; }
.wa-link { color: #0369a1; font-weight: 600; text-decoration: underline; }
.wa-tick { font-size: 11px; }
[data-theme="dark"] .wa-msg { background: #1a2f26; color: #d7efe3; }

.m-cfdi { right: 0; top: 24px; width: 220px; animation: floatC 9s ease-in-out infinite; }
.cfdi-head { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.cfdi-amount { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 4px; }
.cfdi-state { font-size: 11px; color: var(--emerald-dark); background: var(--emerald-soft); padding: 3px 8px; border-radius: 999px; display: inline-flex; align-items: center; gap: 4px; font-weight: 600; }

@keyframes floatA { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes floatB { 0%,100% { transform: translateY(0) rotate(-3deg); } 50% { transform: translateY(-10px) rotate(-3deg); } }
@keyframes floatC { 0%,100% { transform: translateY(0) rotate(3deg); } 50% { transform: translateY(-8px) rotate(3deg); } }

@media (max-width: 720px) {
  .mockup { height: 660px; }
  .m-wa, .m-cfdi { position: static; width: 90%; margin: 14px auto; animation: none; transform: none !important; }
  .m-dash { max-width: 92%; }
}

.trust-row { margin-top: 48px; display: flex; gap: 14px; justify-content: center; align-items: center; flex-wrap: wrap; font-size: 13px; color: var(--text-muted); }
.trust-brands { font-weight: 500; }
.trust-logo { font-weight: 700; letter-spacing: -0.01em; font-size: 15px; color: var(--text); }
.trust-sep { opacity: .4; }

/* SECTIONS */
.section { padding: 96px 24px; }
.section-surface { background: var(--surface); }
.section-dark { background: #06150f; color: #e5f4ec; }
.section-dark .h2, .section-dark h3 { color: #e5f4ec; }
.section-dark .eyebrow.light { background: rgba(255,255,255,.08); color: #86efac; }

.section-head { text-align: center; max-width: 760px; margin: 0 auto 64px; }
.eyebrow { display: inline-block; font-size: 12px; text-transform: uppercase; letter-spacing: .14em; color: var(--emerald-dark); font-weight: 700; padding: 5px 12px; border-radius: 999px; background: var(--emerald-soft); }
.h2 { font-size: clamp(32px, 5vw, 56px); font-weight: 800; letter-spacing: -0.035em; margin: 18px 0 14px; line-height: 1.05; }
.lead { font-size: 17px; line-height: 1.55; margin: 0; }
.light { color: #e5f4ec; }
.center { text-align: center; }

/* STEPS */
.steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.step { position: relative; background: var(--surface); border: 1px solid var(--border); border-radius: 18px; padding: 26px 22px; }
.step-n { position: absolute; top: -12px; left: 20px; width: 28px; height: 28px; border-radius: 50%; background: var(--brand-grad); color: white; font-weight: 800; font-size: 13px; display: grid; place-items: center; box-shadow: 0 4px 12px rgba(16,185,129,.4); }
.step-ico { width: 42px; height: 42px; border-radius: 10px; background: var(--emerald-soft); color: var(--emerald-dark); display: grid; place-items: center; font-size: 22px; margin-bottom: 14px; }
.step h3 { font-size: 17px; margin: 0 0 6px; font-weight: 700; letter-spacing: -0.01em; }
.step p { font-size: 14px; line-height: 1.55; margin: 0; color: var(--text-muted); }

/* CASES */
.cases-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
.case { position: relative; text-align: left; background: var(--surface); border: 1px solid var(--border);
  border-radius: 18px; padding: 22px; cursor: pointer; font-family: inherit; color: inherit;
  transition: all .25s cubic-bezier(.4,0,.2,1); overflow: hidden; }
.case:hover { transform: translateY(-6px); border-color: var(--c, var(--emerald)); box-shadow: 0 20px 40px color-mix(in srgb, var(--c) 30%, transparent); }
.case.busy { opacity: .6; pointer-events: none; }
.case-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.case-ico { width: 48px; height: 48px; border-radius: 12px; background: var(--c-soft); color: var(--c); display: grid; place-items: center; font-size: 24px; transition: transform .3s; }
.case:hover .case-ico { transform: rotate(-6deg) scale(1.08); }
.case-arrow { color: var(--text-subtle); font-size: 18px; transition: transform .3s; }
.case:hover .case-arrow { color: var(--c); transform: translate(4px, -4px); }
.case-name { font-weight: 800; font-size: 19px; letter-spacing: -0.01em; margin-bottom: 8px; }
.case-quote { font-size: 14.5px; color: var(--text-muted); line-height: 1.55; margin: 0 0 16px; min-height: 64px; }
.case-cta { font-size: 13px; color: var(--c); font-weight: 700; display: inline-flex; align-items: center; gap: 4px; }
.case.c-emerald { --c: #10b981; --c-soft: var(--emerald-soft); }
.case.c-teal    { --c: #14b8a6; --c-soft: var(--teal-soft); }
.case.c-violet  { --c: #7c3aed; --c-soft: var(--violet-soft); }
.case.c-coral   { --c: #fb7185; --c-soft: var(--coral-soft); }

/* FEATURES dark */
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1px; background: #0f2319; border-radius: 20px; overflow: hidden; border: 1px solid #0f2319; }
.feature { background: #06150f; padding: 28px 26px; transition: background .2s; }
.feature:hover { background: #0a1d14; }
.feat-ico { width: 42px; height: 42px; border-radius: 10px; background: linear-gradient(135deg, #10b981, #14b8a6); color: white; display: grid; place-items: center; font-size: 22px; margin-bottom: 14px; }
.feature h3 { font-size: 16px; margin: 0 0 6px; font-weight: 700; letter-spacing: -0.01em; color: #e5f4ec; }
.feature p { font-size: 13.5px; line-height: 1.55; margin: 0; color: #86aa9a; }

/* STATS */
.section-stats { padding: 40px 24px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 24px; text-align: center; }
.stat-val { font-size: clamp(32px, 4.5vw, 52px); font-weight: 800; letter-spacing: -0.03em; line-height: 1; }
.stat-lbl { font-size: 14px; color: var(--text-muted); margin-top: 6px; font-weight: 500; }

/* PRICING */
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; align-items: stretch; }
.plan { position: relative; background: var(--surface); border: 1px solid var(--border); border-radius: 22px;
  padding: 30px 26px; display: flex; flex-direction: column; transition: all .25s;
  box-shadow: var(--shadow-sm); }
.plan:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.plan.featured { border: 2px solid transparent;
  background:
    linear-gradient(var(--surface), var(--surface)) padding-box,
    var(--brand-grad) border-box;
  box-shadow: 0 20px 48px rgba(16,185,129,.2); }
.plan-ribbon { position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  padding: 5px 14px; background: var(--brand-grad); color: white; font-size: 11px;
  border-radius: 999px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase;
  box-shadow: 0 6px 14px rgba(16,185,129,.4); display: inline-flex; align-items: center; gap: 4px; }
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
.cokdot { width: 10px; height: 10px; border-radius: 50%; background: #00b884; }

.pricing-foot { margin-top: 40px; font-size: 14px; }

/* CTA */
.cta-card { position: relative; overflow: hidden;
  background: var(--brand-grad); border-radius: 32px;
  padding: 80px 40px; text-align: center; color: white;
  box-shadow: var(--shadow-lg); }
.cta-grid-dots { position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,.22) 1px, transparent 1px);
  background-size: 20px 20px; opacity: .35; mask: radial-gradient(ellipse at center, black 30%, transparent 75%); }
.cta-card h2 { font-size: clamp(32px, 5vw, 52px); font-weight: 800; letter-spacing: -0.03em; margin: 0 0 16px; line-height: 1.05; color: white; position: relative; }
.cta-card p { font-size: 17px; opacity: .95; margin: 0 0 32px; position: relative; }
.cta-card .btn { position: relative; background: white; color: var(--emerald-dark); border: none; box-shadow: 0 8px 24px rgba(0,0,0,.2); font-weight: 800; }
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
