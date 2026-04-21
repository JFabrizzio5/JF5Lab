<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import api from '../api/client'

const plans = ref([])
onMounted(async () => {
  try { plans.value = (await api.get('/plans')).data } catch(e) {}
})

const testimonios = [
  { name: "Ana García", role: "CFO · Agencia creativa", text: "Recuperamos $420K en 40 días. Sin una llamada incómoda.", color: "#10b981" },
  { name: "Mario Espinoza", role: "Director · Distribuidora",  text: "Antes perseguíamos cobros en Excel. Hoy PorCobrar lo hace solo.", color: "#f59e0b" },
  { name: "Laura Téllez", role: "Contadora · Despacho legal",  text: "DSO bajó de 68 a 37 días. Los clientes pagan antes con el link.", color: "#a78bfa" },
]
</script>

<template>
  <div class="hero-grad" style="min-height:100vh;">
    <header class="container" style="display:flex; align-items:center; justify-content:space-between; padding: 22px 22px;">
      <div style="display:flex; align-items:center; gap:10px; font-weight:700; letter-spacing:-0.02em; font-size: 18px;">
        <i class="mdi mdi-cash-fast" style="color:var(--cash); font-size:24px"></i> PorCobrar
      </div>
      <nav style="display:flex; gap: 16px; align-items:center;">
        <a href="#planes" class="muted" style="font-size:13px">Planes</a>
        <a href="#features" class="muted" style="font-size:13px">Cómo funciona</a>
        <RouterLink to="/demo" class="btn btn-primary btn-sm"><i class="mdi mdi-play-circle-outline"></i> Probar demo</RouterLink>
      </nav>
    </header>

    <section class="container" style="padding: 70px 22px 60px; text-align:center;">
      <div class="badge cash" style="margin-bottom: 18px"><i class="mdi mdi-shield-check"></i> Beta privada México</div>
      <h1 style="font-size: 56px; line-height: 1.05; max-width: 820px; margin: 0 auto;">
        Cobra lo que te deben.<br/>
        <span style="color: var(--cash)">Sin llamadas incómodas.</span>
      </h1>
      <p class="muted" style="max-width: 640px; margin: 22px auto 30px; font-size: 17px; line-height: 1.5;">
        Cobranza automática de cartera vencida B2B. Subes tus CFDI, PorCobrar programa recordatorios escalados
        por WhatsApp, email y SMS con un link de pago Stripe/Conekta. IA que predice quién paga.
      </p>
      <div style="display:flex; gap: 12px; justify-content: center; flex-wrap:wrap;">
        <RouterLink to="/demo" class="btn btn-primary btn-lg"><i class="mdi mdi-rocket-launch-outline"></i> Generar demo en 10s</RouterLink>
        <a href="#planes" class="btn btn-ghost btn-lg"><i class="mdi mdi-credit-card-outline"></i> Ver planes</a>
      </div>

      <div class="terminal-line" style="margin-top: 40px;">
        <span class="prompt">$</span> curl POST /cobrar/v1/invoices/&lt;id&gt;/payment-link &nbsp; · &nbsp;  <span class="stat-up">+$42,380 cobrados</span> en esta demo hace 3 min
      </div>
    </section>

    <section class="container" id="features" style="padding: 40px 22px;">
      <div class="grid-3">
        <div class="card">
          <i class="mdi mdi-file-upload-outline" style="font-size:28px; color:var(--cash)"></i>
          <h3 style="margin: 10px 0 6px">1. Sube tus CFDI</h3>
          <p class="muted" style="font-size:13.5px">XML directo del SAT o CSV con folios y vencimientos. PorCobrar parsea UUID, emisor, receptor y total.</p>
        </div>
        <div class="card">
          <i class="mdi mdi-transit-connection-variant" style="font-size:28px; color:var(--warn)"></i>
          <h3 style="margin: 10px 0 6px">2. Asigna un dunning flow</h3>
          <p class="muted" style="font-size:13.5px">Plantilla de 3 toques: email al vencer, WhatsApp a 7d, SMS a 15d. Editable paso a paso.</p>
        </div>
        <div class="card">
          <i class="mdi mdi-cash-check" style="font-size:28px; color:var(--cash)"></i>
          <h3 style="margin: 10px 0 6px">3. El cliente paga con un link</h3>
          <p class="muted" style="font-size:13.5px">Link público con tu marca. Acepta tarjeta (Stripe), SPEI y OXXO (Conekta). Score IA se actualiza solo.</p>
        </div>
      </div>
    </section>

    <section class="container" style="padding: 40px 22px;">
      <div class="grid-3">
        <div class="card" v-for="t in testimonios" :key="t.name">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom: 12px">
            <div style="width:36px; height:36px; border-radius:999px; background: linear-gradient(135deg, currentColor, transparent); display:flex; align-items:center; justify-content:center; font-weight:700;" :style="{color: t.color}">
              {{ t.name.split(' ').map(n => n[0]).join('') }}
            </div>
            <div>
              <div style="font-weight:600; font-size:13.5px">{{ t.name }}</div>
              <div class="muted" style="font-size:12px">{{ t.role }}</div>
            </div>
          </div>
          <div style="font-size:14.5px; line-height: 1.5;">“{{ t.text }}”</div>
        </div>
      </div>
    </section>

    <section class="container" id="planes" style="padding: 60px 22px;">
      <div style="text-align:center; margin-bottom: 32px;">
        <div class="badge" style="margin-bottom: 10px">Planes</div>
        <h2>Un plan para cada tamaño de cartera.</h2>
        <p class="muted">Sin comisión por cobranza, sólo mensualidad. Puedes escalar cuando quieras.</p>
      </div>
      <div class="grid-4">
        <div class="card" v-for="p in plans" :key="p.id" :class="{ 'featured-card': p.featured }"
             :style="{ borderColor: p.featured ? 'var(--cash)' : '' }">
          <div class="badge" v-if="p.featured" style="background: var(--cash-soft); color: var(--cash);">POPULAR</div>
          <h3 style="margin-top: 8px">{{ p.name }}</h3>
          <div style="margin: 10px 0">
            <span class="kpi-number" style="font-size: 28px">${{ p.price_mxn }}</span>
            <span class="muted" style="font-size:12px"> /mes MXN</span>
          </div>
          <div class="muted" style="font-size: 13px; margin-bottom: 12px">{{ p.description }}</div>
          <ul style="list-style:none; padding:0; margin:0 0 14px; font-size:12.5px">
            <li><i class="mdi mdi-check" style="color:var(--cash)"></i> {{ p.max_invoices_month >= 999999 ? 'Ilimitadas' : p.max_invoices_month }} facturas/mes</li>
            <li v-if="p.has_whatsapp"><i class="mdi mdi-check" style="color:var(--cash)"></i> Envíos WhatsApp</li>
            <li v-if="p.has_ai_scoring"><i class="mdi mdi-check" style="color:var(--cash)"></i> IA payment score</li>
            <li v-if="p.has_custom_brand"><i class="mdi mdi-check" style="color:var(--cash)"></i> Marca propia</li>
          </ul>
          <RouterLink to="/demo" class="btn btn-primary" style="width:100%; justify-content:center;">Empezar</RouterLink>
        </div>
      </div>
    </section>

    <footer class="container" style="padding: 40px 22px; border-top:1px solid var(--border); margin-top: 30px; text-align:center;" class_="muted">
      <span class="muted">PorCobrar © 2026 · Hecho para CFOs y contadores MX</span>
    </footer>
  </div>
</template>

<style scoped>
.featured-card {
  background: linear-gradient(180deg, var(--surface) 0%, var(--cash-soft) 200%);
}
</style>
