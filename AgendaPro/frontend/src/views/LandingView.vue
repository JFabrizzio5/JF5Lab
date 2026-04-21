<script setup>
import { onMounted, ref } from 'vue'
import { apiPlans } from '../api/endpoints'

const plans = ref([])
const loading = ref(true)

onMounted(async () => {
  try { plans.value = await apiPlans() } catch { plans.value = [] }
  loading.value = false
})

const useCases = [
  { icon: 'content-cut', title: 'Barberías', desc: 'Fades, barbas, combos. Con o sin depósito.' },
  { icon: 'tooth-outline', title: 'Clínicas dentales', desc: 'Limpiezas, ortodoncia, blanqueamientos.' },
  { icon: 'paw-outline', title: 'Veterinarias', desc: 'Consultas, vacunas, estética pet.' },
  { icon: 'bullseye-arrow', title: 'Coaches', desc: 'Sesiones online o presenciales, paquetes.' },
  { icon: 'face-woman-shimmer', title: 'Belleza y spa', desc: 'Uñas, masajes, faciales con depósito.' },
  { icon: 'needle', title: 'Tatuadores', desc: 'Flash, custom, toques gratis.' },
]

const features = [
  { icon: 'whatsapp', title: 'Recordatorios WhatsApp', desc: 'Reduce no-shows hasta 70%. Se programan solos 24h y 2h antes.' },
  { icon: 'credit-card-check-outline', title: 'Pago anticipado', desc: 'Cobra depósito al reservar. Stripe y Conekta integrados.' },
  { icon: 'link-variant', title: 'Tu página de reservas', desc: 'agenda.pro/tu-negocio — responsive, branded, sin apps.' },
  { icon: 'calendar-lock-outline', title: 'Sin dobles citas', desc: 'Agenda compartida por staff, buffer automático entre citas.' },
  { icon: 'star-check-outline', title: 'Reseñas Google', desc: 'Automatiza la petición de review 2h después del servicio.' },
  { icon: 'chart-line-variant', title: 'Dashboard en MXN', desc: 'Ingresos mes, no-show rate, top staff, top servicios.' },
]
</script>

<template>
  <div class="landing">
    <!-- NAV -->
    <nav class="nav">
      <div class="brand">Agenda<strong>Pro</strong></div>
      <div class="links">
        <a href="#casos">Casos</a>
        <a href="#features">Cómo funciona</a>
        <a href="#planes">Planes</a>
        <router-link to="/demo" class="btn btn-primary btn-sm">Probar demo</router-link>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div class="chip chip-gold" style="margin-bottom:22px;">
        <i class="mdi mdi-star-four-points"></i> Cal.com mexicano, con cobros
      </div>
      <h1>Agenda que sí <em>respetan</em>.</h1>
      <p class="sub">
        Reservas 24/7 con depósito anticipado y recordatorio por WhatsApp.
        Para barberos, dentistas, vets, coaches y todo negocio que vive de su hora libre.
      </p>
      <div class="cta">
        <router-link to="/demo" class="btn btn-primary">
          <i class="mdi mdi-rocket-launch-outline"></i> Probar con datos demo
        </router-link>
        <a href="#planes" class="btn btn-ghost">
          <i class="mdi mdi-tag-outline"></i> Ver planes
        </a>
      </div>
      <div class="hero-meta">
        <div><strong>70%</strong><br><span>menos no-shows</span></div>
        <div><strong>24/7</strong><br><span>reservas sin llamadas</span></div>
        <div><strong>$0</strong><br><span>setup, sin contratos</span></div>
      </div>
    </section>

    <!-- DEMO WIDGET MOCKUP -->
    <section class="demo-mockup">
      <div class="mockup-inner">
        <div class="mockup-header">
          <div class="dot" style="background:#ff5f57"></div>
          <div class="dot" style="background:#febc2e"></div>
          <div class="dot" style="background:#28c840"></div>
          <span class="url">agenda.pro/barberia-el-corte</span>
        </div>
        <div class="mockup-body">
          <div class="biz-name serif">Barbería El Corte</div>
          <div class="biz-tag">Clásicos, precisos, puntuales.</div>
          <div class="service-pick">
            <div class="svc-chip selected">Corte + Barba · $350</div>
            <div class="svc-chip">Corte · $250</div>
            <div class="svc-chip">Barba · $150</div>
          </div>
          <div class="cal-grid">
            <div class="cal-cell muted">mié 16</div>
            <div class="cal-cell muted">jue 17</div>
            <div class="cal-cell selected">vie 18</div>
            <div class="cal-cell">sáb 19</div>
            <div class="cal-cell">lun 21</div>
          </div>
          <div class="slots">
            <span class="slot">10:30</span>
            <span class="slot">11:00</span>
            <span class="slot selected">11:30</span>
            <span class="slot">16:00</span>
            <span class="slot">17:30</span>
          </div>
          <div class="pay-cta">Reservar viernes 11:30 · depósito $100 MXN</div>
        </div>
      </div>
    </section>

    <!-- CASOS -->
    <section id="casos" class="section">
      <div class="section-head">
        <h2 class="serif">Hecho para negocios que viven de su agenda.</h2>
        <p class="muted">Cada vertical con sus servicios, precios y reglas.</p>
      </div>
      <div class="cases grid-3">
        <div v-for="c in useCases" :key="c.title" class="case-card">
          <i :class="'mdi mdi-' + c.icon"></i>
          <div class="case-title">{{ c.title }}</div>
          <div class="case-desc">{{ c.desc }}</div>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section id="features" class="section alt">
      <div class="section-head">
        <h2 class="serif">Cómo <em>funciona.</em></h2>
        <p class="muted">Seis razones por las que tus clientes llegan a tiempo.</p>
      </div>
      <div class="features grid-3">
        <div v-for="f in features" :key="f.title" class="feat-card">
          <div class="feat-icon"><i :class="'mdi mdi-' + f.icon"></i></div>
          <div class="feat-title">{{ f.title }}</div>
          <div class="feat-desc">{{ f.desc }}</div>
        </div>
      </div>
    </section>

    <!-- PLANES -->
    <section id="planes" class="section">
      <div class="section-head">
        <h2 class="serif">Elige tu plan.</h2>
        <p class="muted">Paga mensual, cancela cuando quieras.</p>
      </div>
      <div class="plans grid-4">
        <div v-for="p in plans" :key="p.id" :class="['plan', { featured: p.featured }]">
          <div v-if="p.featured" class="plan-badge">MÁS POPULAR</div>
          <div class="plan-name">{{ p.name }}</div>
          <div class="plan-price">
            <span class="mxn">$</span>{{ p.price_mxn }}
            <span class="per">/ mes</span>
          </div>
          <div class="plan-desc">{{ p.description }}</div>
          <ul class="plan-feats">
            <li><i class="mdi mdi-check"></i>{{ p.max_appointments_mo.toLocaleString() }} citas/mes</li>
            <li><i class="mdi mdi-check"></i>{{ p.max_staff }} staff</li>
            <li :class="{ off: !p.has_prepay }"><i :class="'mdi mdi-' + (p.has_prepay?'check':'close')"></i>Cobros Stripe/Conekta</li>
            <li :class="{ off: !p.has_whatsapp }"><i :class="'mdi mdi-' + (p.has_whatsapp?'check':'close')"></i>WhatsApp reminders</li>
            <li :class="{ off: !p.has_custom_brand }"><i :class="'mdi mdi-' + (p.has_custom_brand?'check':'close')"></i>Branding propio</li>
            <li :class="{ off: !p.has_google_review }"><i :class="'mdi mdi-' + (p.has_google_review?'check':'close')"></i>Google Reviews auto</li>
          </ul>
          <router-link to="/demo" :class="['btn', p.featured ? 'btn-gold' : 'btn-primary']" style="width:100%;justify-content:center;">
            Empezar {{ p.name }}
          </router-link>
        </div>
      </div>
      <p v-if="!plans.length && !loading" class="muted" style="text-align:center;margin-top:20px;">
        ¿Primera vez aquí? Ve a la <router-link to="/demo" style="color:var(--gold);font-weight:700;">demo</router-link> para crear un negocio de muestra.
      </p>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="foot-brand">
        <div class="brand">Agenda<strong>Pro</strong></div>
        <div class="foot-tag serif italic">Agenda que sí respetan.</div>
      </div>
      <div class="foot-links">
        <router-link to="/demo">Demo</router-link>
        <a href="/docs" target="_blank">API docs</a>
        <a href="#planes">Planes</a>
      </div>
      <div class="foot-copy">© 2026 AgendaPro · Hecho en México</div>
    </footer>
  </div>
</template>

<style scoped>
.landing { background: var(--cream); }
.nav {
  display: flex; justify-content: space-between; align-items: center;
  padding: 24px 40px; max-width: 1280px; margin: 0 auto;
}
.brand {
  font-family: var(--serif); font-style: italic; font-size: 26px;
  color: var(--navy);
}
.brand strong { color: var(--gold); font-weight: 600; }
.links { display: flex; gap: 28px; align-items: center; }
.links a { color: var(--ink-2); font-size: 14px; font-weight: 500; }
.links a:hover { color: var(--navy); }

.hero-meta {
  display: flex; justify-content: center; gap: 44px;
  margin-top: 44px; flex-wrap: wrap;
}
.hero-meta div {
  text-align: center; color: var(--muted); font-size: 13px;
}
.hero-meta strong {
  display: block; font-family: var(--serif);
  font-size: 36px; color: var(--navy); font-weight: 600;
  letter-spacing: -0.02em; margin-bottom: 4px;
}

.demo-mockup { max-width: 900px; margin: 16px auto 80px; padding: 0 28px; }
.mockup-inner {
  background: white; border: 1px solid var(--border);
  border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-lg);
}
.mockup-header {
  display: flex; align-items: center; gap: 8px;
  padding: 14px 18px; background: var(--cream-2); border-bottom: 1px solid var(--line-soft);
}
.dot { width: 10px; height: 10px; border-radius: 50%; }
.url {
  margin-left: 20px; font-family: 'SF Mono', ui-monospace, monospace;
  font-size: 12px; color: var(--muted);
}
.mockup-body { padding: 28px 32px 32px; background: white; }
.biz-name { font-size: 22px; margin-bottom: 4px; color: var(--navy); font-weight: 600; }
.biz-tag { font-size: 13px; color: var(--muted); font-style: italic; margin-bottom: 20px; }
.service-pick { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.svc-chip {
  padding: 8px 14px; border-radius: 999px; font-size: 13px; font-weight: 500;
  background: var(--cream); border: 1px solid var(--line); color: var(--ink-2);
}
.svc-chip.selected { background: var(--navy); color: var(--cream); border-color: var(--navy); }
.cal-grid {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-bottom: 16px;
}
.cal-cell {
  padding: 12px; text-align: center; border: 1px solid var(--line);
  border-radius: var(--radius-sm); font-size: 13px; font-weight: 600; color: var(--ink-2);
  background: var(--cream);
}
.cal-cell.muted { color: var(--muted); background: transparent; border-color: var(--line-soft); }
.cal-cell.selected { background: var(--navy); color: var(--cream); border-color: var(--navy); }
.slots { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.slot {
  padding: 8px 14px; border: 1px solid var(--line); border-radius: var(--radius-sm);
  font-size: 13px; font-weight: 600; color: var(--ink-2); background: var(--cream);
}
.slot.selected { background: var(--gold); color: var(--navy); border-color: var(--gold); }
.pay-cta {
  padding: 14px; background: var(--navy); color: var(--cream);
  border-radius: var(--radius-sm); text-align: center;
  font-weight: 700; font-size: 14px; letter-spacing: 0.01em;
}

.section { max-width: 1200px; margin: 0 auto; padding: 80px 28px; }
.section.alt { background: var(--cream-2); max-width: none; padding: 80px 28px; }
.section.alt > * { max-width: 1200px; margin-left: auto; margin-right: auto; }
.section-head { text-align: center; margin-bottom: 44px; }
.section-head h2 {
  font-size: clamp(32px, 4vw, 48px); letter-spacing: -0.02em;
  margin: 0 0 10px; color: var(--navy); font-weight: 500;
}
.section-head h2 em { color: var(--gold); font-style: italic; font-weight: 600; }

.case-card {
  background: white; border: 1px solid var(--border); border-radius: var(--radius);
  padding: 28px 22px; text-align: center; transition: all .2s;
}
.case-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--gold); }
.case-card .mdi { font-size: 42px; color: var(--navy); margin-bottom: 14px; display: block; }
.case-title { font-family: var(--serif); font-size: 20px; color: var(--navy); margin-bottom: 6px; font-weight: 600; }
.case-desc { font-size: 13px; color: var(--muted); }

.feat-card {
  background: white; border: 1px solid var(--border); border-radius: var(--radius);
  padding: 28px; transition: all .2s;
}
.feat-card:hover { border-color: var(--navy); }
.feat-icon {
  width: 44px; height: 44px; border-radius: 10px;
  background: var(--navy); color: var(--cream);
  display: grid; place-items: center; font-size: 22px; margin-bottom: 14px;
}
.feat-title { font-family: var(--serif); font-size: 20px; color: var(--navy); margin-bottom: 8px; font-weight: 600; }
.feat-desc { font-size: 14px; color: var(--ink-2); line-height: 1.6; }

.plan {
  background: white; border: 1px solid var(--border); border-radius: var(--radius);
  padding: 32px 24px; position: relative;
}
.plan.featured { border-color: var(--gold); border-width: 2px; transform: translateY(-8px); box-shadow: var(--shadow-md); }
.plan-badge {
  position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  background: var(--gold); color: var(--navy); padding: 4px 14px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: 0.05em;
}
.plan-name {
  font-family: var(--serif); font-size: 24px; color: var(--navy); margin-bottom: 10px;
  font-weight: 600;
}
.plan-price {
  font-family: var(--serif); font-size: 48px; color: var(--navy);
  font-weight: 600; letter-spacing: -0.02em; margin-bottom: 6px;
}
.plan-price .mxn { font-size: 24px; color: var(--muted); vertical-align: top; }
.plan-price .per { font-size: 15px; color: var(--muted); font-weight: 400; font-family: var(--sans); }
.plan-desc { font-size: 13px; color: var(--muted); margin-bottom: 20px; min-height: 40px; }
.plan-feats { list-style: none; padding: 0; margin: 0 0 22px; }
.plan-feats li {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 0; font-size: 13px; color: var(--ink-2);
}
.plan-feats li .mdi { color: var(--success); font-size: 18px; }
.plan-feats li.off { color: var(--muted); opacity: 0.55; }
.plan-feats li.off .mdi { color: var(--muted); }

.footer {
  background: var(--navy); color: var(--cream);
  padding: 48px 40px 32px; text-align: center;
}
.foot-brand .brand { color: var(--cream); }
.foot-tag { color: var(--gold-2); margin-top: 4px; font-size: 14px; }
.foot-links { display: flex; justify-content: center; gap: 28px; margin: 20px 0; }
.foot-links a { color: rgba(253,251,245,0.7); font-size: 14px; }
.foot-links a:hover { color: var(--gold-2); }
.foot-copy { font-size: 12px; color: rgba(253,251,245,0.4); }

@media (max-width: 700px) {
  .nav { padding: 18px 20px; }
  .links { gap: 14px; }
  .links a:not(.btn) { display: none; }
}
</style>
