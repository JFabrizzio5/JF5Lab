<script setup>
import { RouterLink } from 'vue-router'

const plans = [
  {
    name: 'Gratis',
    price: '$0',
    period: '/siempre',
    desc: 'Para arrancar y probar.',
    highlight: false,
    features: [
      '10 plantillas base',
      '5 paletas',
      'Export PNG/JPG',
      'Hasta 10 slides',
      'Marca CometaX en el footer'
    ],
    cta: 'Empezar',
    to: '/editor'
  },
  {
    name: 'Pro',
    price: '$199',
    period: '/mes MXN',
    desc: 'Para creadores activos.',
    highlight: true,
    features: [
      'Todas las plantillas',
      'Paletas ilimitadas',
      'Sin marca CometaX',
      'Slides ilimitados',
      'Export PNG/JPG/ZIP HD',
      'Logo personalizado',
      'Guardar diseños (local)'
    ],
    cta: 'Próximamente',
    to: '/editor'
  },
  {
    name: 'Team',
    price: '$799',
    period: '/mes MXN',
    desc: 'Para agencias y equipos.',
    highlight: false,
    features: [
      'Todo Pro',
      'Hasta 5 marcas',
      'Plantillas custom',
      'Sync entre dispositivos',
      'Soporte por email'
    ],
    cta: 'Contactar',
    to: '/editor'
  }
]
</script>

<template>
  <div class="pricing">
    <header>
      <RouterLink to="/" class="back">
        <i class="mdi mdi-arrow-left"></i>
        <span>CometaX Carousel</span>
      </RouterLink>
    </header>

    <div class="hero">
      <h1>Precios <span class="grad">simples</span></h1>
      <p>Empieza gratis. Sube de plan cuando lo necesites.</p>
    </div>

    <div class="grid">
      <div v-for="p in plans" :key="p.name" class="plan" :class="{ highlight: p.highlight }">
        <div v-if="p.highlight" class="ribbon">Recomendado</div>
        <h3>{{ p.name }}</h3>
        <p class="desc">{{ p.desc }}</p>
        <div class="price">
          <span class="amount">{{ p.price }}</span>
          <span class="period">{{ p.period }}</span>
        </div>
        <ul>
          <li v-for="f in p.features" :key="f">
            <i class="mdi mdi-check-circle"></i>
            <span>{{ f }}</span>
          </li>
        </ul>
        <RouterLink :to="p.to" class="btn" :class="{ 'btn-primary': p.highlight }">{{ p.cta }}</RouterLink>
      </div>
    </div>

    <div class="faq">
      <h2>Preguntas frecuentes</h2>
      <div class="qa">
        <div class="q">¿Necesito crear cuenta?</div>
        <div class="a">No. Todo corre en tu navegador. Tus diseños no salen de tu equipo.</div>
      </div>
      <div class="qa">
        <div class="q">¿Cómo cancelo?</div>
        <div class="a">Stripe Customer Portal. Self-serve, sin llamadas.</div>
      </div>
      <div class="qa">
        <div class="q">¿Acepta OXXO / SPEI?</div>
        <div class="a">Sí. Stripe MX procesa tarjeta + OXXO + SPEI.</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pricing { max-width: 1100px; margin: 0 auto; padding: 24px; }
header { padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.back { display: flex; align-items: center; gap: 10px; color: var(--text); font-weight: 700; }
.hero { text-align: center; padding: 60px 0; }
.hero h1 { font-size: 56px; margin: 0; }
.grad { background: var(--grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: var(--muted); font-size: 18px; margin-top: 16px; }

.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }
.plan {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 28px; position: relative;
  display: flex; flex-direction: column;
}
.plan.highlight {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3), var(--shadow);
}
.ribbon {
  position: absolute; top: -12px; right: 20px;
  background: var(--grad); color: #fff;
  font-size: 11px; font-weight: 800; letter-spacing: 1px;
  text-transform: uppercase; padding: 4px 12px; border-radius: 999px;
}
.plan h3 { margin: 0; font-size: 22px; }
.plan .desc { color: var(--muted); margin: 6px 0 20px; font-size: 14px; }
.price { display: flex; align-items: baseline; gap: 4px; margin-bottom: 20px; }
.amount { font-size: 44px; font-weight: 900; }
.period { color: var(--muted); font-size: 14px; }
.plan ul { list-style: none; padding: 0; margin: 0 0 24px; flex: 1; }
.plan li {
  display: flex; align-items: center; gap: 10px;
  padding: 6px 0; color: var(--text); font-size: 14px;
}
.plan li i { color: var(--accent); }
.plan .btn { justify-content: center; }

.faq { margin-top: 80px; max-width: 720px; margin-left: auto; margin-right: auto; }
.faq h2 { font-size: 28px; margin-bottom: 24px; }
.qa { padding: 16px 0; border-bottom: 1px solid var(--border); }
.q { font-weight: 700; color: var(--text); margin-bottom: 4px; }
.a { color: var(--muted); font-size: 14px; line-height: 1.6; }
</style>
