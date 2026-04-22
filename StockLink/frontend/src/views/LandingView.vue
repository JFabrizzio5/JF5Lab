<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { plansApi, demoApi } from '../api/endpoints'
import { useSession } from '../stores/session'

const router = useRouter()
const session = useSession()
const plans = ref([])
const seeding = ref(null)
const error = ref(null)

const industries = [
  { id: 'store',        name: 'Tiendita',     icon: 'mdi-store',                 color: 'coral',    detail: 'Abarrotes, minisuper. Código de barras en caja, corte del día en Excel.' },
  { id: 'restaurant',   name: 'Restaurante',  icon: 'mdi-silverware-fork-knife', color: 'mint',     detail: 'Receta por platillo. El POS descuenta ingredientes solo.' },
  { id: 'shipping',     name: 'Paquetería',   icon: 'mdi-truck-fast',            color: 'lavender', detail: 'Rastreo de paquete de recepción a camión con QR por etapa.' },
  { id: 'construction', name: 'Constructora', icon: 'mdi-hammer-wrench',         color: 'yellow',   detail: 'Herramienta NFC por albañil. Material por piso y partida.' },
]

const features = [
  { icon: 'mdi-qrcode-scan',    title: 'Escáner universal',    desc: 'QR, Code128, EAN13 desde la cámara o subiendo imagen.',  color: 'coral' },
  { icon: 'mdi-nfc-tap',        title: 'NFC nativo',           desc: 'Registra tags por producto, empleado o ubicación.',       color: 'lavender' },
  { icon: 'mdi-webhook',        title: 'Webhooks POS/ERP',     desc: 'Tu POS vende — StockLink descuenta inventario solo.',     color: 'mint' },
  { icon: 'mdi-account-clock',  title: 'Asistencias por QR',   desc: 'Check-in geolocalizado. Turnos y bitácora. Excel.',       color: 'yellow' },
  { icon: 'mdi-file-excel',     title: 'Excel en un clic',     desc: 'Inventario, movimientos, asistencias. Listo para contador.', color: 'mint' },
  { icon: 'mdi-chart-box',      title: 'Reporte de viabilidad',desc: 'Score 0-100, top consumos, valor real del almacén.',      color: 'sky' },
  { icon: 'mdi-printer',        title: 'Impresión masiva',     desc: 'PDF A4 con 21 etiquetas por hoja. Código + nombre.',      color: 'pink' },
  { icon: 'mdi-shield-lock',    title: 'Multi-tenant seguro',  desc: 'Row Level Security de PostgreSQL. Aislamiento a nivel DB.', color: 'coral' },
  { icon: 'mdi-cellphone-link', title: 'Responsive real',      desc: 'Claro/oscuro. Usable desde celular del mesero o almacenista.', color: 'lavender' },
]

async function loadPlans() {
  try {
    const { data } = await plansApi.list()
    plans.value = data.length ? data : fallbackPlans()
  } catch {
    plans.value = fallbackPlans()
  }
}

function fallbackPlans() {
  return [
    { id: 'free', name: 'Gratis', price_mxn: 0, max_warehouses: 1, max_items: 100, max_users: 2, nfc_enabled: false, webhooks_enabled: false, attendance_enabled: false, excel_export: true, featured: false, description: 'Para probar el producto.' },
    { id: 'starter', name: 'Starter', price_mxn: 499, max_warehouses: 3, max_items: 2000, max_users: 5, nfc_enabled: false, webhooks_enabled: true, attendance_enabled: true, excel_export: true, featured: false, description: 'Ideal tiendita o fonda.' },
    { id: 'pro', name: 'Pro', price_mxn: 1499, max_warehouses: 10, max_items: 20000, max_users: 15, nfc_enabled: true, webhooks_enabled: true, attendance_enabled: true, excel_export: true, featured: true, description: 'Cadena, taller o paquetería con NFC.' },
    { id: 'enterprise', name: 'Enterprise', price_mxn: 4999, max_warehouses: 999, max_items: 999999, max_users: 999, nfc_enabled: true, webhooks_enabled: true, attendance_enabled: true, excel_export: true, featured: false, description: 'Constructoras y franquicias.' },
  ]
}

async function tryDemo(industry) {
  seeding.value = industry
  error.value = null
  try {
    const { data } = await demoApi.seed(industry)
    if (data.error) throw new Error(data.error)
    session.set({ tenant_id: data.tenant_id, name: data.name, industry })
    router.push('/app/dashboard')
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || 'Error creando demo'
  } finally {
    seeding.value = null
  }
}

onMounted(loadPlans)
</script>

<template>
  <div class="landing">
    <!-- Blob decorations -->
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <!-- NAV -->
    <nav class="nav">
      <div class="container nav-inner">
        <router-link to="/" class="logo">
          <div class="logo-mark">
            <i class="mdi mdi-package-variant-closed"></i>
          </div>
          <div>
            <div class="logo-title">StockLink</div>
            <div class="logo-sub">Hecho en 🇲🇽</div>
          </div>
        </router-link>
        <div class="nav-links">
          <a href="#industries">Casos</a>
          <a href="#features">Funciones</a>
          <a href="#pricing">Precios</a>
          <router-link to="/demo" class="btn btn-primary btn-sm">Probar gratis</router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-badge">
          <span class="mini-dot"></span>
          En vivo · sin tarjeta · 5 segundos
        </div>
        <h1 class="hero-title">
          Tu inventario<br/>
          <span class="hero-underline">se cuenta solo.</span>
        </h1>
        <p class="hero-lede">
          Para tienditas, fondas, paqueterías y obras.
          QR, código de barras y NFC en una sola app.
          Cuando vendes o consumes, <b>StockLink lo descuenta por ti.</b>
        </p>
        <div class="hero-ctas">
          <router-link to="/demo" class="btn btn-primary btn-lg">
            <i class="mdi mdi-rocket-launch"></i> Probar con datos reales
          </router-link>
          <a href="#pricing" class="btn btn-lg btn-ghost">
            Ver precios MXN
          </a>
        </div>

        <!-- Hero mockup -->
        <div class="hero-mockup">
          <div class="mockup-bg"></div>
          <div class="float-card card-coral">
            <div class="fc-head">
              <div class="fc-avatar"><i class="mdi mdi-bottle-soda-classic"></i></div>
              <div>
                <div class="fc-title">Coca-Cola 600ml</div>
                <div class="fc-sub">Mostrador · 7501055363057</div>
              </div>
              <div class="fc-qty">48</div>
            </div>
            <div class="fc-progress"><div class="fc-bar" style="width:72%;"></div></div>
            <div class="fc-foot">
              <span class="dot-coral"></span>
              Se descontó -1 hace 3s · <span class="mono">ORD-1284</span>
            </div>
          </div>

          <div class="float-card card-mint small-card">
            <div class="mint-ping"></div>
            <div class="fc-title" style="font-size:13px;">Asistencia</div>
            <div class="fc-big">✓ Luis Pérez</div>
            <div class="fc-sub">08:02 · QR check-in</div>
          </div>

          <div class="float-card card-lavender small-card">
            <i class="mdi mdi-nfc-variant lav-icon"></i>
            <div class="fc-title" style="font-size:13px;">Taladro DW-01</div>
            <div class="fc-sub">Tag escrito ✓</div>
          </div>

          <div class="float-card card-yellow mini-card">
            <i class="mdi mdi-file-excel"></i>
            <span>inventario.xlsx</span>
          </div>
        </div>

        <div class="hero-trust">
          <div class="trust-item"><i class="mdi mdi-check-decagram"></i> CFDI 4.0</div>
          <div class="trust-item"><i class="mdi mdi-check-decagram"></i> Multi-tenant</div>
          <div class="trust-item"><i class="mdi mdi-check-decagram"></i> API abierta</div>
          <div class="trust-item"><i class="mdi mdi-check-decagram"></i> Sentry integrado</div>
        </div>
      </div>
    </section>

    <!-- INDUSTRIES -->
    <section id="industries" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Prueba en vivo</span>
          <h2>Elige tu negocio. Creamos el demo.</h2>
          <p class="muted">Un clic y tienes productos, empleados, asistencias y reportes listos.</p>
        </div>
        <div class="industries-grid">
          <button v-for="i in industries" :key="i.id" class="industry" :class="[`c-${i.color}`, { busy: seeding === i.id }]" @click="tryDemo(i.id)">
            <div class="industry-icon"><i :class="['mdi', i.icon]"></i></div>
            <div class="industry-name">{{ i.name }}</div>
            <p class="industry-desc">{{ i.detail }}</p>
            <div class="industry-cta">
              <span v-if="seeding === i.id"><i class="mdi mdi-loading mdi-spin"></i> Creando…</span>
              <span v-else>Crear demo <i class="mdi mdi-arrow-right"></i></span>
            </div>
          </button>
        </div>
        <p v-if="error" class="center muted" style="color:var(--danger); margin-top:16px;">{{ error }}</p>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="section section-cream">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Cómo funciona</span>
          <h2>Tres pasos. Un almacén vivo.</h2>
        </div>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-ico"><i class="mdi mdi-qrcode-plus"></i></div>
            <h3>Genera etiquetas</h3>
            <p class="muted">QR, Code128 o NFC por cada producto, ubicación o empleado. Imprime 21 por hoja en PDF A4.</p>
          </div>
          <div class="step-arrow"><i class="mdi mdi-arrow-right"></i></div>
          <div class="step">
            <div class="step-num">2</div>
            <div class="step-ico"><i class="mdi mdi-cellphone-wireless"></i></div>
            <h3>Escanea o conecta tu POS</h3>
            <p class="muted">Usa la cámara, lector USB, o manda un webhook desde tu POS/ERP cuando vendas o consumas.</p>
          </div>
          <div class="step-arrow"><i class="mdi mdi-arrow-right"></i></div>
          <div class="step">
            <div class="step-num">3</div>
            <div class="step-ico"><i class="mdi mdi-chart-box-outline"></i></div>
            <h3>Stock vivo + Excel</h3>
            <p class="muted">Tu inventario se mueve solo. Descargas Excel, ves el score de viabilidad y recibes alertas.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section id="features" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Incluido en todos los planes</span>
          <h2>Todo lo que un almacén real necesita</h2>
        </div>
        <div class="features-grid">
          <div v-for="f in features" :key="f.title" class="feature" :class="`c-${f.color}`">
            <div class="feature-icon"><i :class="['mdi', f.icon]"></i></div>
            <h3>{{ f.title }}</h3>
            <p class="muted">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SCENARIOS -->
    <section class="section section-cream">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Ejemplos reales</span>
          <h2>Así se siente usarlo</h2>
        </div>
        <div class="scenarios">
          <div class="scenario c-coral">
            <div class="sc-head"><span class="sc-num">01</span><i class="mdi mdi-store"></i></div>
            <h3>Tiendita Don Memo</h3>
            <p class="muted">Pasas una Coca por el lector. Se descuenta 1 pieza de <span class="mono">MOSTRADOR</span>. Cuando bajan de 24, StockLink te avisa pedir con Coca-Cola FEMSA.</p>
          </div>
          <div class="scenario c-mint">
            <div class="sc-head"><span class="sc-num">02</span><i class="mdi mdi-silverware-fork-knife"></i></div>
            <h3>Fonda La Esquina</h3>
            <p class="muted">Tu POS manda <span class="mono">order.placed</span> con 3 arracheras. Se descuenta kg de carne, tortilla, limón y vaso — receta por platillo.</p>
          </div>
          <div class="scenario c-lavender">
            <div class="sc-head"><span class="sc-num">03</span><i class="mdi mdi-truck-fast"></i></div>
            <h3>PaqueExpress Norte</h3>
            <p class="muted">Cada paquete llega con QR en recepción. Lo mueves a <span class="mono">SORT-A</span>, luego <span class="mono">TRUCK-01</span>. Cada movimiento trazado con hora y operador.</p>
          </div>
          <div class="scenario c-yellow">
            <div class="sc-head"><span class="sc-num">04</span><i class="mdi mdi-hammer-wrench"></i></div>
            <h3>Constructora Norte</h3>
            <p class="muted">Taladro con NFC. Se asigna al maestro al entrar a obra (check-in) y se libera al salir. Cemento sale de <span class="mono">PATIO</span> a <span class="mono">PISO-2</span>.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- PRICING -->
    <section id="pricing" class="section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Planes en MXN</span>
          <h2>Paga lo justo. Escala cuando crezcas.</h2>
          <p class="muted">Todos más IVA. Cancela cuando quieras. CFDI 4.0 al día siguiente.</p>
        </div>
        <div class="pricing-grid">
          <div v-for="(p, idx) in plans" :key="p.id" class="plan" :class="[{ featured: p.featured }, `plan-${idx}`]">
            <div v-if="p.featured" class="ribbon"><i class="mdi mdi-star"></i> Más popular</div>
            <div class="plan-name">{{ p.name }}</div>
            <div class="plan-price">
              <template v-if="Number(p.price_mxn) === 0"><span class="free">Gratis</span></template>
              <template v-else>
                <span class="currency">$</span><span class="pv">{{ Number(p.price_mxn).toLocaleString('es-MX') }}</span>
                <span class="per">/mes</span>
              </template>
            </div>
            <p class="plan-desc muted">{{ p.description }}</p>
            <ul class="plan-list">
              <li><i class="mdi mdi-check-circle"></i> {{ p.max_warehouses >= 999 ? 'Almacenes ilimitados' : `${p.max_warehouses} almacenes` }}</li>
              <li><i class="mdi mdi-check-circle"></i> {{ p.max_items >= 999999 ? 'SKUs ilimitados' : `${p.max_items.toLocaleString('es-MX')} SKUs` }}</li>
              <li><i class="mdi mdi-check-circle"></i> {{ p.max_users >= 999 ? 'Usuarios ilimitados' : `${p.max_users} usuarios` }}</li>
              <li :class="{ dim: !p.nfc_enabled }"><i :class="['mdi', p.nfc_enabled ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> NFC</li>
              <li :class="{ dim: !p.webhooks_enabled }"><i :class="['mdi', p.webhooks_enabled ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> Webhooks POS/ERP</li>
              <li :class="{ dim: !p.attendance_enabled }"><i :class="['mdi', p.attendance_enabled ? 'mdi-check-circle' : 'mdi-circle-outline']"></i> Asistencias por QR</li>
              <li><i class="mdi mdi-check-circle"></i> Exportar a Excel</li>
            </ul>
            <router-link to="/demo" class="btn plan-cta" :class="{ 'btn-primary': p.featured }">
              {{ Number(p.price_mxn) === 0 ? 'Empezar gratis' : 'Probar 14 días' }}
            </router-link>
          </div>
        </div>
        <div class="pricing-note muted center">
          ¿Más de 100k SKUs o integración a medida? <a href="mailto:ventas@stocklink.mx">ventas@stocklink.mx</a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-box">
          <div class="cta-decor"></div>
          <h2>Prueba gratis. <br>Sin tarjeta.</h2>
          <p>Un demo real con productos, empleados y asistencias, listo en 5 segundos.</p>
          <router-link to="/demo" class="btn btn-lg cta-btn">
            <i class="mdi mdi-rocket-launch"></i> Crear mi demo
          </router-link>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container footer-inner">
        <div>
          <b style="color:var(--coral);">StockLink</b> · Parte de <a href="https://cometax.dev">CometaX</a> · Hecho en 🇲🇽
        </div>
        <div class="muted small">
          API <span class="mono">/inventory/v1</span> · <a href="/docs">Docs</a> · <a href="/health">Health</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing { position: relative; overflow-x: hidden; }

/* Blobs decorativos */
.blob { position: absolute; z-index: -1; border-radius: 50%; filter: blur(80px); opacity: .55; pointer-events: none; }
.blob-1 { width: 420px; height: 420px; background: radial-gradient(circle, var(--coral), transparent 65%); top: -100px; left: -100px; }
.blob-2 { width: 520px; height: 520px; background: radial-gradient(circle, var(--mint), transparent 65%); top: 280px; right: -180px; }
.blob-3 { width: 380px; height: 380px; background: radial-gradient(circle, var(--yellow), transparent 65%); top: 800px; left: 40%; opacity: .35; }

/* NAV */
.nav { position: sticky; top: 0; z-index: 50; backdrop-filter: saturate(180%) blur(16px);
  background: color-mix(in srgb, var(--bg) 78%, transparent);
  border-bottom: 1px solid var(--border-soft); }
.nav-inner { display: flex; justify-content: space-between; align-items: center; padding: 14px 24px; }
.logo { display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit; }
.logo:hover { text-decoration: none; }
.logo-mark { width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, var(--coral), #ff8866);
  display: grid; place-items: center; color: white; font-size: 20px;
  box-shadow: var(--shadow-coral); transition: transform .2s; }
.logo:hover .logo-mark { transform: rotate(-6deg) scale(1.05); }
.logo-title { font-weight: 800; font-size: 17px; letter-spacing: -0.01em; }
.logo-sub { font-size: 11px; color: var(--text-muted); margin-top: 1px; }
.nav-links { display: flex; align-items: center; gap: 26px; }
.nav-links a { color: var(--text); font-size: 14px; font-weight: 500; transition: color .15s; }
.nav-links a:not(.btn):hover { color: var(--coral); text-decoration: none; }

/* HERO */
.hero { padding: 70px 24px 60px; }
.hero-inner { text-align: center; max-width: 860px; margin: 0 auto; }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; padding: 7px 16px; border-radius: 999px;
  background: white; border: 1.5px solid var(--coral-soft); font-size: 13px; color: var(--text); margin-bottom: 28px;
  box-shadow: var(--shadow-sm); font-weight: 600; }
.mini-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--mint); box-shadow: 0 0 0 4px var(--mint-soft); animation: dotPulse 2s infinite; }
@keyframes dotPulse { 0%,100% { box-shadow: 0 0 0 4px var(--mint-soft); } 50% { box-shadow: 0 0 0 8px transparent; } }

.hero-title { font-size: clamp(40px, 7vw, 82px); font-weight: 800; line-height: 1.02; letter-spacing: -0.035em; margin: 0 0 20px; color: var(--text); }
.hero-underline { position: relative; display: inline-block; color: var(--coral); }
.hero-underline::after { content: ""; position: absolute; left: 0; right: 0; bottom: 4px; height: 14px;
  background: var(--yellow); z-index: -1; border-radius: 4px; opacity: .65;
  transform: skewX(-6deg); animation: underlinePop 2.5s ease-out; }
@keyframes underlinePop { from { transform: skewX(-6deg) scaleX(0); transform-origin: left; } to { transform: skewX(-6deg) scaleX(1); } }

.hero-lede { max-width: 620px; margin: 0 auto 36px; font-size: 19px; color: var(--text-muted); line-height: 1.55; }
.hero-lede b { color: var(--text); font-weight: 600; }
.hero-ctas { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

/* Hero mockup */
.hero-mockup { position: relative; margin: 72px auto 0; height: 280px; max-width: 720px; }
.mockup-bg { position: absolute; inset: 20px; border-radius: 32px;
  background: linear-gradient(135deg, var(--mint-soft), var(--coral-soft), var(--yellow-soft));
  filter: blur(40px); opacity: .7; }
.float-card { position: absolute; background: var(--surface); border-radius: 16px; padding: 16px 18px;
  box-shadow: var(--shadow-lg); border: 1.5px solid var(--border-soft); animation: floatGentle 6s ease-in-out infinite; }
.card-coral { left: 50%; top: 0; transform: translateX(-50%); width: min(380px, 90vw); z-index: 3;
  border-left: 4px solid var(--coral); }
.card-mint { left: 2%; top: 80px; width: 200px; animation-delay: -2s; border-left: 4px solid var(--mint); z-index: 2; }
.card-lavender { right: 2%; top: 40px; width: 210px; animation-delay: -4s; border-left: 4px solid var(--lavender); z-index: 2; }
.card-yellow { right: 14%; top: 200px; display: flex; align-items: center; gap: 8px; padding: 10px 16px; animation-delay: -1s;
  background: var(--yellow); border-color: transparent; color: #7d5400; font-weight: 600; font-size: 13px; border-radius: 999px; }
.card-yellow .mdi { font-size: 18px; }

.fc-head { display: flex; align-items: center; gap: 12px; }
.fc-avatar { width: 40px; height: 40px; border-radius: 10px; background: var(--coral-soft); color: var(--coral); display: grid; place-items: center; font-size: 20px; flex-shrink: 0; }
.fc-title { font-weight: 700; font-size: 14px; }
.fc-sub { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
.fc-qty { margin-left: auto; font-size: 28px; font-weight: 800; color: var(--coral); font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
.fc-progress { height: 6px; background: var(--surface-2); border-radius: 3px; margin: 12px 0 8px; overflow: hidden; }
.fc-bar { height: 100%; background: linear-gradient(90deg, var(--coral), var(--yellow)); border-radius: 3px; animation: barGrow 1s ease-out; }
@keyframes barGrow { from { width: 0 !important; } }
.fc-foot { font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }
.dot-coral { width: 6px; height: 6px; border-radius: 50%; background: var(--coral); box-shadow: 0 0 0 3px var(--coral-soft); }
.fc-big { font-size: 18px; font-weight: 800; color: var(--mint); margin: 4px 0 2px; letter-spacing: -0.02em; }
.mint-ping { position: absolute; top: 12px; right: 12px; width: 10px; height: 10px; border-radius: 50%; background: var(--mint); box-shadow: 0 0 0 5px var(--mint-soft); animation: dotPulse 1.5s infinite; }
.lav-icon { font-size: 26px; color: var(--lavender); float: right; margin-top: -2px; }

@keyframes floatGentle { 0%,100% { transform: var(--base-transform, none) translateY(0); } 50% { transform: var(--base-transform, none) translateY(-10px); } }
.card-coral { --base-transform: translateX(-50%); }

@media (max-width: 780px) {
  .hero-mockup { height: 420px; }
  .card-coral { width: 90vw; }
  .card-mint, .card-lavender { top: 200px; width: 46%; }
  .card-mint { left: 2%; }
  .card-lavender { right: 2%; }
  .card-yellow { display: none; }
}

.hero-trust { margin-top: 56px; display: flex; gap: 22px; justify-content: center; flex-wrap: wrap; }
.trust-item { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-muted); font-weight: 500; }
.trust-item .mdi { color: var(--mint); font-size: 16px; }

/* SECTIONS */
.section { padding: 90px 24px; position: relative; }
.section-cream { background: var(--bg-alt); }
.section-head { text-align: center; max-width: 680px; margin: 0 auto 56px; }
.eyebrow { display: inline-block; font-size: 12px; text-transform: uppercase; letter-spacing: .14em; color: var(--coral); font-weight: 800; padding: 5px 12px; border-radius: 999px; background: var(--coral-soft); }
.section-head h2 { font-size: clamp(28px, 4vw, 44px); font-weight: 800; letter-spacing: -0.028em; margin: 16px 0 12px; line-height: 1.12; }
.section-head p { font-size: 16px; line-height: 1.5; margin: 0; }
.center { text-align: center; }

/* INDUSTRIES — color per card */
.industries-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; }
.industry { position: relative; text-align: left; background: var(--surface); border: 2px solid var(--border-soft); border-radius: 20px; padding: 28px 24px; cursor: pointer; font-family: inherit; color: inherit; transition: all .25s cubic-bezier(.4,0,.2,1); overflow: hidden; }
.industry::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: var(--card-color, var(--coral)); }
.industry:hover { transform: translateY(-6px) rotate(-0.3deg); border-color: var(--card-color); box-shadow: 0 22px 40px color-mix(in srgb, var(--card-color) 25%, transparent); }
.industry.busy { opacity: .6; pointer-events: none; }
.industry-icon { width: 56px; height: 56px; border-radius: 14px; background: var(--card-color-soft); color: var(--card-color); display: grid; place-items: center; font-size: 28px; margin-bottom: 18px; transition: transform .3s; }
.industry:hover .industry-icon { transform: rotate(-8deg) scale(1.1); }
.industry-name { font-weight: 800; font-size: 19px; margin-bottom: 8px; letter-spacing: -0.01em; }
.industry-desc { font-size: 13px; color: var(--text-muted); line-height: 1.55; margin: 0 0 16px; min-height: 56px; }
.industry-cta { font-size: 13px; color: var(--card-color); font-weight: 700; display: inline-flex; align-items: center; gap: 4px; }

.industry.c-coral { --card-color: var(--coral); --card-color-soft: var(--coral-soft); }
.industry.c-mint { --card-color: var(--mint); --card-color-soft: var(--mint-soft); }
.industry.c-lavender { --card-color: var(--lavender); --card-color-soft: var(--lavender-soft); }
.industry.c-yellow { --card-color: #d97706; --card-color-soft: var(--yellow-soft); }

/* STEPS */
.steps { display: flex; gap: 20px; align-items: stretch; justify-content: center; }
.step { flex: 1; max-width: 280px; text-align: center; padding: 24px; background: var(--surface); border: 1.5px solid var(--border-soft); border-radius: 20px; box-shadow: var(--shadow-sm); position: relative; }
.step-num { position: absolute; top: -16px; left: 50%; transform: translateX(-50%); width: 36px; height: 36px; border-radius: 50%; background: var(--coral); color: white; display: grid; place-items: center; font-weight: 800; font-size: 15px; box-shadow: var(--shadow-coral); }
.step-ico { width: 60px; height: 60px; border-radius: 16px; background: var(--coral-soft); color: var(--coral); display: grid; place-items: center; font-size: 30px; margin: 20px auto 16px; }
.step h3 { margin: 0 0 8px; font-size: 17px; font-weight: 700; }
.step p { margin: 0; font-size: 14px; line-height: 1.55; }
.step-arrow { display: grid; place-items: center; color: var(--coral); font-size: 32px; flex-shrink: 0; }
@media (max-width: 760px) {
  .steps { flex-direction: column; align-items: center; }
  .step-arrow { transform: rotate(90deg); }
}

/* FEATURES */
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }
.feature { background: var(--surface); border: 1.5px solid var(--border-soft); border-radius: 18px; padding: 24px 22px; transition: all .2s; }
.feature:hover { transform: translateY(-3px); border-color: var(--feat-color, var(--coral)); box-shadow: var(--shadow-md); }
.feature-icon { width: 46px; height: 46px; border-radius: 12px; background: var(--feat-color-soft, var(--coral-soft)); color: var(--feat-color, var(--coral)); display: grid; place-items: center; font-size: 22px; margin-bottom: 14px; transition: transform .3s; }
.feature:hover .feature-icon { transform: rotate(-10deg); }
.feature h3 { font-size: 16px; margin: 0 0 6px; font-weight: 700; }
.feature p { font-size: 14px; line-height: 1.55; margin: 0; }
.feature.c-coral { --feat-color: var(--coral); --feat-color-soft: var(--coral-soft); }
.feature.c-mint { --feat-color: var(--mint); --feat-color-soft: var(--mint-soft); }
.feature.c-lavender { --feat-color: var(--lavender); --feat-color-soft: var(--lavender-soft); }
.feature.c-yellow { --feat-color: #d97706; --feat-color-soft: var(--yellow-soft); }
.feature.c-pink { --feat-color: var(--pink); --feat-color-soft: var(--pink-soft); }
.feature.c-sky { --feat-color: var(--sky); --feat-color-soft: var(--sky-soft); }

/* SCENARIOS */
.scenarios { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
.scenario { background: var(--surface); border: 1.5px solid var(--border-soft); border-radius: 20px; padding: 26px 24px; border-top: 5px solid var(--sc-color, var(--coral)); transition: transform .2s; }
.scenario:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.sc-head { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.sc-num { font-size: 13px; font-weight: 800; color: var(--sc-color); background: var(--sc-color-soft); padding: 3px 10px; border-radius: 999px; letter-spacing: .05em; }
.sc-head .mdi { font-size: 24px; color: var(--sc-color); }
.scenario h3 { margin: 0 0 8px; font-size: 18px; font-weight: 700; letter-spacing: -0.01em; }
.scenario p { margin: 0; font-size: 14px; line-height: 1.6; }
.scenario.c-coral { --sc-color: var(--coral); --sc-color-soft: var(--coral-soft); }
.scenario.c-mint { --sc-color: var(--mint); --sc-color-soft: var(--mint-soft); }
.scenario.c-lavender { --sc-color: var(--lavender); --sc-color-soft: var(--lavender-soft); }
.scenario.c-yellow { --sc-color: #d97706; --sc-color-soft: var(--yellow-soft); }
.mono { font-family: ui-monospace, monospace; font-size: .9em; background: var(--surface-2); padding: 2px 7px; border-radius: 5px; border: 1px solid var(--border-soft); }

/* PRICING */
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
.plan { position: relative; background: var(--surface); border: 2px solid var(--border-soft); border-radius: 22px; padding: 32px 26px; display: flex; flex-direction: column; transition: all .25s; }
.plan:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.plan.featured { border-color: var(--coral); box-shadow: 0 0 0 4px var(--coral-soft), var(--shadow-lg); transform: translateY(-6px); background: linear-gradient(180deg, var(--coral-soft), var(--surface) 22%); }
.ribbon { position: absolute; top: -14px; left: 50%; transform: translateX(-50%); padding: 6px 16px;
  background: var(--coral); color: white; font-size: 11px; border-radius: 999px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase;
  box-shadow: var(--shadow-coral); display: inline-flex; align-items: center; gap: 4px; }
.ribbon .mdi { font-size: 14px; color: var(--yellow); }
.plan-name { font-size: 13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .1em; font-weight: 800; }
.plan-price { margin: 12px 0 8px; line-height: 1; }
.plan-price .currency { font-size: 24px; font-weight: 700; color: var(--text-muted); vertical-align: top; }
.plan-price .pv { font-size: 46px; font-weight: 800; letter-spacing: -0.035em; }
.plan-price .per { font-size: 14px; color: var(--text-muted); font-weight: 500; }
.plan-price .free { font-size: 40px; font-weight: 800; letter-spacing: -0.02em; color: var(--mint); }
.plan-desc { font-size: 13px; line-height: 1.5; min-height: 42px; margin: 10px 0 20px; }
.plan-list { list-style: none; padding: 0; margin: 0 0 22px; font-size: 14px; flex: 1; }
.plan-list li { padding: 7px 0; display: flex; align-items: center; gap: 10px; }
.plan-list li .mdi { flex-shrink: 0; color: var(--mint); font-size: 18px; }
.plan-list li.dim { color: var(--text-muted); }
.plan-list li.dim .mdi { color: var(--border); }
.plan-cta { width: 100%; justify-content: center; font-weight: 700; }
.pricing-note { margin-top: 36px; font-size: 14px; }

/* CTA */
.cta-section { padding: 80px 24px; }
.cta-box { position: relative; overflow: hidden;
  text-align: center; background: linear-gradient(135deg, var(--coral) 0%, #ff8866 50%, var(--yellow) 100%);
  border-radius: 32px; padding: 72px 32px; color: white;
  box-shadow: var(--shadow-lg); }
.cta-decor { position: absolute; top: -40%; right: -10%; width: 400px; height: 400px; border-radius: 50%; background: rgba(255,255,255,.15); }
.cta-box h2 { font-size: clamp(30px, 4.5vw, 48px); font-weight: 800; letter-spacing: -0.025em; margin: 0 0 16px; line-height: 1.05; color: white; }
.cta-box p { font-size: 17px; opacity: .95; margin: 0 0 32px; }
.cta-btn { background: white; color: var(--coral); border: none; font-weight: 800; padding: 16px 30px; font-size: 16px; box-shadow: 0 8px 24px rgba(0,0,0,.15); }
.cta-btn:hover { background: white; transform: translateY(-2px) scale(1.02); box-shadow: 0 12px 32px rgba(0,0,0,.2); }

/* FOOTER */
.footer { padding: 32px 24px; border-top: 1px solid var(--border-soft); background: var(--surface); }
.footer-inner { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 14px; color: var(--text-muted); }
.small { font-size: 12px; }

@media (max-width: 700px) {
  .nav-links a:not(.btn) { display: none; }
  .section { padding: 60px 20px; }
  .section-head { margin-bottom: 40px; }
  .hero { padding: 40px 20px 30px; }
}
</style>
