<template>
  <div class="analysis">
    <a href="#main" class="skip-link">Saltar al contenido</a>

    <header class="top" role="banner">
      <div class="top-inner">
        <router-link to="/" class="logo" aria-label="HubOS inicio">
          <span class="logo-mark"><i data-lucide="layers"></i></span>
          <span>JF5 Lab · Mercado MX</span>
        </router-link>
        <nav aria-label="Índice" class="toc">
          <a href="#scorecard">Scorecard</a>
          <a href="#proyectos">Proyectos</a>
          <a href="#roi">ROI 10k MXN</a>
          <a href="#bundles">Bundles</a>
          <a href="#veredicto">Veredicto</a>
        </nav>
      </div>
    </header>

    <main id="main" class="wrap" role="main">
      <!-- HERO -->
      <section class="hero" aria-labelledby="h1">
        <p class="kicker">Informe · Mercado mexicano · Abril 2026</p>
        <h1 id="h1">
          <em class="serif">Análisis de mercado</em> del portafolio JF5,
          <span class="nowrap">ajustado a México.</span>
        </h1>
        <p class="lead">
          10 proyectos frente a competencia real mexicana. Tamaño del nicho
          local, canales de adquisición viables con <strong>presupuesto
          $10,000 MXN</strong>, margen bruto esperado, y combinaciones donde
          fusionar 2-3 proyectos abre una brecha defendible contra Kommo,
          Clip, Hotmart, Guesty y compañía.
        </p>
        <div class="meta">
          <span><i data-lucide="database"></i> 10 proyectos</span>
          <span><i data-lucide="map-pin"></i> Foco MX (CDMX / GDL / MTY)</span>
          <span><i data-lucide="coins"></i> Budget $10k MXN</span>
          <span><i data-lucide="calendar"></i> Corte 2026-Q2</span>
        </div>
      </section>

      <!-- TL;DR -->
      <section class="block" aria-labelledby="tldr">
        <p class="eyebrow">TL;DR</p>
        <h2 id="tldr">3 que cobran rápido. 3 bundles que valen más juntos. 4 que pesan.</h2>
        <div class="tldr-grid">
          <div class="tldr tldr-win">
            <div class="tldr-h">💰 Cobran en 30 días</div>
            <ol>
              <li><strong>HubOS</strong> — CRM + WhatsApp PyME MX.</li>
              <li><strong>NegocioOS</strong> — POS + CFDI 4.0 con RAG.</li>
              <li><strong>ServiLink vertical</strong> — belleza CDMX.</li>
            </ol>
          </div>
          <div class="tldr tldr-polish">
            <div class="tldr-h">🧬 Fusión = brecha</div>
            <ol>
              <li><strong>RentaCore</strong> = RentaFacil + RentaMe + SalonOS.</li>
              <li><strong>AgendaMX</strong> = EduLink + ServiLink booking engine.</li>
              <li><strong>HubOS + NegocioOS</strong> = CRM operativo PyME.</li>
            </ol>
          </div>
          <div class="tldr tldr-kill">
            <div class="tldr-h">⚰️ Drenan tiempo</div>
            <ol>
              <li><strong>ConventionOS</strong> — Cvent + Eventbrite dueños.</li>
              <li><strong>Tokenizate</strong> — MX no paga editorial review.</li>
              <li><strong>Extensiones / hub</strong> — no son producto.</li>
            </ol>
          </div>
        </div>
      </section>

      <!-- SCORECARD -->
      <section id="scorecard" class="block" aria-labelledby="score-h">
        <p class="eyebrow">Scorecard MX</p>
        <h2 id="score-h">Ranking ajustado a dinero real mexicano.</h2>
        <p class="sub">
          <strong>Mercado MX</strong> = tamaño del nicho local + voluntad de
          pago PyME. <strong>Foso</strong> = qué tan defendible es tu versión
          vs Kommo/Clip/Hotmart/Rappi. <strong>CAC $10k</strong> = qué tanto
          mueve un budget marketing de diez mil pesos. <strong>Margen</strong>
          = % bruto esperado después de Stripe/MP + hosting.
        </p>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th><th>Proyecto</th><th>Nicho MX</th>
                <th>Mercado</th><th>Foso</th><th>CAC $10k</th>
                <th>Margen</th><th>Score</th><th>Jugada</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in scorecard" :key="r.name" :class="rowClass(r.score)">
                <td class="num">{{ i + 1 }}</td>
                <td><strong>{{ r.name }}</strong></td>
                <td>{{ r.niche }}</td>
                <td><span class="bar" :style="barStyle(r.market)"></span> {{ r.market }}</td>
                <td><span class="bar" :style="barStyle(r.moat)"></span> {{ r.moat }}</td>
                <td><span class="bar" :style="barStyle(r.cac)"></span> {{ r.cac }}</td>
                <td><span class="bar bar-g" :style="barStyle(r.margin / 10)"></span> {{ r.margin }}%</td>
                <td><strong>{{ r.score }}</strong></td>
                <td><span class="tag" :class="'tag-' + r.tag">{{ r.verdict }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="foot-note">
          CAC $10k: <em>10</em> = 10k MXN compra 50+ clientes / <em>5</em> = compra 10-20 / <em>1</em> = no alcanza.
          Margen: después de Stripe 3.6% o Mercado Pago 3.5% + hosting $600-1,500 MXN/mes + WhatsApp API costs.
        </p>
      </section>

      <!-- ROI con 10k MXN -->
      <section id="roi" class="block alt" aria-labelledby="roi-h">
        <p class="eyebrow">Simulación con $10,000 MXN</p>
        <h2 id="roi-h">Qué puedes ganar en 90 días con ese budget.</h2>
        <p class="sub">
          Asume: <strong>$6k en Meta/Google Ads</strong> (CPC MX PyME $8-20),
          <strong>$2k en landing + demo</strong> (tu propio tiempo valorado),
          <strong>$2k buffer</strong> (WhatsApp API, herramientas).
          CPL PyME MX realista: $80-200 por lead, conv lead→pago 8-15%.
        </p>

        <div class="roi-grid">
          <article v-for="r in roi" :key="r.name" class="roi-card" :class="'roi-' + r.tag">
            <header>
              <h3>{{ r.emoji }} {{ r.name }}</h3>
              <span class="tag" :class="'tag-' + r.tag">{{ r.verdict }}</span>
            </header>
            <div class="roi-row"><span>Ticket mensual</span><strong>{{ r.ticket }}</strong></div>
            <div class="roi-row"><span>CAC esperado</span><strong>{{ r.cacAmt }}</strong></div>
            <div class="roi-row"><span>Clientes 90d</span><strong>{{ r.clients }}</strong></div>
            <div class="roi-row"><span>MRR mes 3</span><strong>{{ r.mrr }}</strong></div>
            <div class="roi-row highlight"><span>Retorno 90d</span><strong>{{ r.roiPct }}</strong></div>
            <p class="roi-note">{{ r.note }}</p>
          </article>
        </div>
        <p class="foot-note">
          Valores en pesos mexicanos. "Retorno 90d" = (MRR mes 3 × 3) − $10,000, en signo del resultado.
          Negativo = el budget no se recupera en 90d (requiere runway mayor).
          Los <strong>3 de arriba</strong> son los únicos que recuperan la inversión dentro del trimestre.
        </p>
      </section>

      <!-- PROYECTOS DETALLE -->
      <section id="proyectos" class="block" aria-labelledby="det-h">
        <p class="eyebrow">Proyecto por proyecto</p>
        <h2 id="det-h">Deep dive en cada uno, lente mexicano.</h2>

        <article v-for="p in projects" :key="p.slug" :id="p.slug" class="project">
          <header class="p-head">
            <div>
              <span class="p-pill" :class="'pill-' + p.tag">{{ p.tag }}</span>
              <h3>{{ p.emoji }} {{ p.name }}</h3>
              <p class="p-tag">{{ p.what }}</p>
            </div>
            <a :href="`#${p.slug}`" class="anchor" :aria-label="`Enlace a ${p.name}`">#</a>
          </header>

          <div class="p-grid">
            <div class="p-card">
              <div class="p-k">🇲🇽 Mercado mexicano</div>
              <div class="p-v" v-html="p.market"></div>
            </div>
            <div class="p-card">
              <div class="p-k">Competencia local</div>
              <div class="p-v" v-html="p.competitors"></div>
            </div>
            <div class="p-card">
              <div class="p-k">Tu diferenciador real</div>
              <div class="p-v" v-html="p.edge"></div>
            </div>
            <div class="p-card">
              <div class="p-k">Economía unitaria</div>
              <div class="p-v" v-html="p.unit"></div>
            </div>
          </div>

          <div class="p-actions">
            <div class="p-k">🚀 Próximas 3 jugadas con $10k</div>
            <ol>
              <li v-for="(m, j) in p.moves" :key="j">{{ m }}</li>
            </ol>
          </div>
        </article>
      </section>

      <!-- BUNDLES / BRECHAS -->
      <section id="bundles" class="block alt" aria-labelledby="bun-h">
        <p class="eyebrow">Brechas por fusión</p>
        <h2 id="bun-h">Donde combinar 2-3 ideas gana contra todos.</h2>
        <p class="sub">
          Vender un proyecto solo = competir contra gigantes con budget 1000×
          mayor. Combinarlos = crear <em class="serif">categorías nuevas</em>
          sin competencia directa en MX.
        </p>

        <div class="bundle-grid">
          <article class="bundle bundle-1">
            <div class="bundle-n">01</div>
            <h3>RentaCore — "Rappi para renta"</h3>
            <p class="bundle-src">= RentaFacil + RentaMe + SalonOS</p>
            <p>
              Un solo engine de <strong>recurso + calendario + reserva + pago</strong>
              con 3 verticales: <em>inmueble</em> (Airbnb host casual MX, 40k+
              anfitriones), <em>equipo pro</em> (foto/video/drones),
              <em>venue</em> (salones XV años, bodas, coworking horas).
            </p>
            <p class="bundle-why">
              <strong>Por qué gana:</strong> Guesty/Hostaway no hacen venues.
              Peerspace no tiene LatAm. Fat Llama murió. Nadie ofrece un
              "booking engine" MX con CFDI + Mercado Pago split + WhatsApp
              reminders. Precio: $299-999/mes por vertical.
            </p>
            <div class="bundle-stats">
              <div><dt>TAM MX</dt><dd>~$80M USD anual</dd></div>
              <div><dt>Ticket</dt><dd>$499 MXN/mes</dd></div>
              <div><dt>Break-even</dt><dd>25 clientes</dd></div>
              <div><dt>Margen</dt><dd>78%</dd></div>
            </div>
          </article>

          <article class="bundle bundle-2">
            <div class="bundle-n">02</div>
            <h3>SuiteOperativa — "Shopify + Kommo para taquerías"</h3>
            <p class="bundle-src">= HubOS + NegocioOS</p>
            <p>
              <strong>POS con CRM integrado</strong>. Vendes en el POS, el
              cliente aparece automático en CRM con su historial. Le mandas
              promo por WhatsApp. El RAG le sugiere al dueño "tu cliente
              María no ha venido en 30 días, manda este msg".
            </p>
            <p class="bundle-why">
              <strong>Por qué gana:</strong> Loyverse y Kommo venden por
              separado. Clip tiene POS sin CRM. Alegra tiene factura sin
              WhatsApp. La suite integrada MX no existe. Target: cafeterías,
              barberías, clínicas PyME.
            </p>
            <div class="bundle-stats">
              <div><dt>TAM MX</dt><dd>~$120M USD anual</dd></div>
              <div><dt>Ticket</dt><dd>$599 MXN/mes</dd></div>
              <div><dt>Break-even</dt><dd>20 clientes</dd></div>
              <div><dt>Margen</dt><dd>82%</dd></div>
            </div>
          </article>

          <article class="bundle bundle-3">
            <div class="bundle-n">03</div>
            <h3>AgendaMX — "Calendly + marketplace LatAm"</h3>
            <p class="bundle-src">= EduLink + ServiLink (booking core)</p>
            <p>
              Engine de <strong>agenda + video call + cobro</strong> para
              profesionales 1:1: tutores, fisios, coaches, nutriólogos,
              psicólogos. Pagan $199/mes, obtienen link tipo calendly con
              Mercado Pago integrado + reminders WhatsApp + video embebido.
            </p>
            <p class="bundle-why">
              <strong>Por qué gana:</strong> Calendly no cobra pagos. Agendapro
              no tiene marketplace. Classgap tutoría no hace otros servicios.
              Directorio SEO local + pagos = network effects.
            </p>
            <div class="bundle-stats">
              <div><dt>TAM MX</dt><dd>~$200M USD anual</dd></div>
              <div><dt>Ticket</dt><dd>$199-399 MXN/mes</dd></div>
              <div><dt>Break-even</dt><dd>35 clientes</dd></div>
              <div><dt>Margen</dt><dd>75%</dd></div>
            </div>
          </article>

          <article class="bundle bundle-4">
            <div class="bundle-n">04</div>
            <h3>CometaX Suite — jugada enterprise</h3>
            <p class="bundle-src">= RentaCore + SuiteOperativa + AgendaMX bajo una cuenta</p>
            <p>
              Una sola cuenta multi-módulo ("Notion for business ops"). Cada
              módulo $199-599/mes. Suite completa $999/mes con descuento.
              Vendes el <em>ecosistema</em> a agencias y franquicias.
            </p>
            <p class="bundle-why">
              <strong>Por qué gana:</strong> Nadie en MX vende suite modular.
              HubSpot es caro (>$800 USD/mes). Esto es tu moat de largo plazo.
            </p>
            <div class="bundle-stats">
              <div><dt>TAM MX</dt><dd>~$400M USD anual</dd></div>
              <div><dt>Ticket</dt><dd>$999 MXN/mes</dd></div>
              <div><dt>Break-even</dt><dd>15 clientes</dd></div>
              <div><dt>Margen</dt><dd>85%</dd></div>
            </div>
          </article>
        </div>
      </section>

      <!-- VEREDICTO -->
      <section id="veredicto" class="block" aria-labelledby="v-h">
        <p class="eyebrow">Veredicto</p>
        <h2 id="v-h">Tu jugada de 90 días con $10,000 MXN.</h2>

        <div class="steps">
          <div class="step">
            <div class="step-n">30d</div>
            <h3>Lanza HubOS</h3>
            <p>
              Ticket $399 MXN/mes (Pro 3 agentes). Budget ads $6k → ~50 leads → 7-10 clientes pagos.
              <strong>MRR mes 1: ~$3,000 MXN.</strong> Posiciona contra Leadsales
              (ellos $1,600/mes, tú $399). Canal: TikTok/Instagram orgánico + ads Meta B2B PyME MX.
            </p>
          </div>
          <div class="step">
            <div class="step-n">60d</div>
            <h3>Bundle SuiteOperativa</h3>
            <p>
              Integra POS NegocioOS como addon HubOS. Ticket $599 MXN/mes. Upsell
              a los clientes del mes 1 + nuevo traffic. <strong>MRR mes 2: ~$7,000 MXN.</strong>
              Agrega CFDI 4.0 (vía Finkok API) — requisito MX para vender "en serio".
            </p>
          </div>
          <div class="step">
            <div class="step-n">90d</div>
            <h3>RentaCore MVP</h3>
            <p>
              Fusiona RentaFacil + RentaMe + SalonOS en un vertical:
              <strong>salones de XV años/bodas CDMX</strong>. 100 venues onboarded
              gratis por SEO local → 10 clientes pagos a $499/mes.
              <strong>MRR mes 3: ~$12,000 MXN.</strong>
            </p>
          </div>
        </div>

        <div class="finale">
          <h3>Los números reales a 90 días con $10k MXN</h3>
          <div class="finale-grid">
            <div>
              <dt>Inversión total</dt>
              <dd>$10,000 MXN</dd>
            </div>
            <div>
              <dt>MRR proyectado mes 3</dt>
              <dd>$12,000 MXN</dd>
            </div>
            <div>
              <dt>Costos recurrentes</dt>
              <dd>~$2,500 MXN/mes</dd>
            </div>
            <div>
              <dt>Ganancia neta 90d</dt>
              <dd class="pos">+$6,500 MXN</dd>
            </div>
            <div>
              <dt>Ganancia año 1 (si sostiene)</dt>
              <dd class="pos">~$114,000 MXN</dd>
            </div>
            <div>
              <dt>Margen bruto promedio</dt>
              <dd>78-82%</dd>
            </div>
          </div>
          <p class="finale-kicker">
            <strong>La regla dura:</strong> $10k MXN solo alcanza si matas
            4 proyectos y enfocas en HubOS + SuiteOperativa + RentaCore.
            Si insistes en mantener los 10, el presupuesto se diluye en
            hosting + maintenance y no hay MRR suficiente para pagar ads.
          </p>
        </div>
      </section>

      <!-- FUENTES -->
      <section class="block" aria-labelledby="src-h">
        <p class="eyebrow">Metodología + fuentes</p>
        <h2 id="src-h">De dónde vienen los números.</h2>
        <p class="sub">
          Cifras cruzadas entre al menos 2 fuentes independientes.
          Estimaciones MX derivadas de reports LatAm + ratios PyME México
          (INEGI 4.4M PyMEs, adopción SaaS ~8%, ticket promedio MXN).
        </p>
        <ul class="sources">
          <li><a href="https://www.fortunebusinessinsights.com/event-management-software-market-102611" target="_blank" rel="noopener">Fortune — Event Management</a></li>
          <li><a href="https://www.mordorintelligence.com/industry-reports/event-management-software-market" target="_blank" rel="noopener">Mordor — Event Mgmt</a></li>
          <li><a href="https://www.aurorainbox.com/en/2026/01/31/best-crm-whatsapp-mexico/" target="_blank" rel="noopener">Aurora Inbox — CRM WhatsApp MX 2026</a></li>
          <li><a href="https://techcrunch.com/2023/08/28/whatsapp-leadsales-conversational-commerce/" target="_blank" rel="noopener">TechCrunch — Leadsales LatAm</a></li>
          <li><a href="https://www.ycloud.com/blog/top-whatsapp-business-api-solution-providers-latin-america" target="_blank" rel="noopener">YCloud — WhatsApp API LatAm</a></li>
          <li><a href="https://www.marketdataforecast.com/market-reports/latin-america-e-learning-market" target="_blank" rel="noopener">MarketDataForecast — LatAm e-Learning</a></li>
          <li><a href="https://straitsresearch.com/report/lms-market/latam" target="_blank" rel="noopener">Straits Research — LatAm LMS</a></li>
          <li><a href="https://www.globenewswire.com/news-release/2026/01/06/3213915/0/en/Online-Tutoring-Strategic-Market-Analysis-2026-2030-Featuring-42-Companies-Total-Revenues-to-Reach-18-2-Billion-by-2030.html" target="_blank" rel="noopener">GlobeNewswire — Online Tutoring</a></li>
          <li><a href="https://loyverse.com/features" target="_blank" rel="noopener">Loyverse features</a></li>
          <li><a href="https://www.capterra.com/p/150632/Loyverse-POS/" target="_blank" rel="noopener">Capterra — Loyverse reviews</a></li>
          <li><a href="https://www.grandviewresearch.com/horizon/outlook/property-management-software-market/latin-america" target="_blank" rel="noopener">Grand View — LatAm Property Mgmt</a></li>
          <li><a href="https://theglobaleconomics.com/2026/04/15/latam-real-estate/" target="_blank" rel="noopener">Global Economics — LatAm PropTech</a></li>
          <li><a href="https://www.businessresearchinsights.com/market-reports/on-demand-services-market-124836" target="_blank" rel="noopener">BRI — On-Demand Services</a></li>
          <li><a href="https://www.businessresearchinsights.com/market-reports/equipment-rental-software-market-102328" target="_blank" rel="noopener">BRI — Equipment Rental</a></li>
          <li><a href="https://www.eu-startups.com/2022/08/sweden-based-hygglo-acquires-uk-based-fat-llama-in-e41-million-deal-to-create-worlds-biggest-peer-to-peer-rental-platform/" target="_blank" rel="noopener">EU-Startups — Hygglo/Fat Llama</a></li>
          <li><a href="https://www.rentallscript.com/resources/alternatives-to-peerspace/" target="_blank" rel="noopener">Rentall — Peerspace alts</a></li>
          <li><a href="https://www.capterra.com/p/234422/ScholarOne/" target="_blank" rel="noopener">Capterra — ScholarOne</a></li>
          <li><a href="https://scholarlykitchen.sspnet.org/2024/10/28/silverchair-buys-scholarone-from-clarivate/" target="_blank" rel="noopener">Scholarly Kitchen — ScholarOne sale</a></li>
        </ul>
      </section>
    </main>

    <footer class="foot">
      <div class="foot-inner">
        <span>© 2026 JF5 Lab · informe interno · mercado MX</span>
        <router-link to="/">← Volver a HubOS</router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

// Cada valor 1-10. Margen en %. Score: (market*0.35 + moat*0.3 + cac*0.2 + margin/10*0.15), norm 10.
const scorecard = [
  { name: 'HubOS',             niche: 'CRM + WhatsApp PyME',    market: 9, moat: 7, cac: 8, margin: 85, score: 8.7, tag: 'win',    verdict: 'DOBLAR' },
  { name: 'NegocioOS',         niche: 'POS + CFDI + RAG',       market: 8, moat: 8, cac: 7, margin: 82, score: 8.2, tag: 'win',    verdict: 'AI-MOAT' },
  { name: 'ServiLink',         niche: 'Marketplace servicios',  market: 9, moat: 6, cac: 5, margin: 70, score: 7.1, tag: 'win',    verdict: 'FOCUS VERTICAL' },
  { name: 'RentaFacil',        niche: 'Airbnb hosts casuales',  market: 7, moat: 6, cac: 6, margin: 78, score: 6.9, tag: 'polish', verdict: 'FUSIONAR' },
  { name: 'SalonOS',           niche: 'Salones XV/bodas MX',    market: 8, moat: 7, cac: 6, margin: 80, score: 7.3, tag: 'polish', verdict: 'FUSIONAR' },
  { name: 'EduLink',           niche: 'Tutoría 1:1 MX',         market: 8, moat: 5, cac: 5, margin: 72, score: 6.3, tag: 'polish', verdict: 'PIVOTAR' },
  { name: 'RentaMe',           niche: 'Peer rental equipos',    market: 5, moat: 4, cac: 4, margin: 65, score: 4.8, tag: 'kill',   verdict: 'FUSIONAR' },
  { name: 'ConventionOS',      niche: 'Conferencias',           market: 4, moat: 2, cac: 2, margin: 60, score: 3.1, tag: 'kill',   verdict: 'MATAR' },
  { name: 'Tokenizate',        niche: 'Editorial revisión',     market: 2, moat: 3, cac: 2, margin: 55, score: 2.6, tag: 'kill',   verdict: 'MATAR' },
  { name: 'Extensiones / hub', niche: 'Meta',                   market: 1, moat: 1, cac: 1, margin: 0,  score: 1.0, tag: 'kill',   verdict: 'CONSOLIDAR' },
]

function rowClass(s) { return s >= 7 ? 'row-win' : s >= 5 ? 'row-mid' : 'row-low' }
function barStyle(v) { return { width: `${Math.min(100, v * 10)}%` } }

// ROI con $10k MXN — 90 días. Proyecciones conservadoras.
const roi = [
  {
    name: 'HubOS', emoji: '💼', tag: 'win', verdict: 'GANA',
    ticket: '$399 MXN/mes',
    cacAmt: '~$120 MXN',
    clients: '8-12',
    mrr: '$3,200-4,800',
    roiPct: '+$4,400 (44% ROI)',
    note: 'El mejor retorno. Canal: TikTok demo + Meta ads PyME. Competencia directa Leadsales ($1,600/mes) — cualquier PyME que vea ahorro $1,200/mes convierte.',
  },
  {
    name: 'NegocioOS', emoji: '🏪', tag: 'win', verdict: 'GANA',
    ticket: '$299 MXN/mes',
    cacAmt: '~$180 MXN',
    clients: '10-15',
    mrr: '$2,990-4,485',
    roiPct: '+$2,455 (25% ROI)',
    note: 'Requiere CFDI 4.0 antes de cobrar. Target: cafeterías + barberías. Loyverse es gratis pero no factura. Tu diferenciador paga $299.',
  },
  {
    name: 'ServiLink', emoji: '🔧', tag: 'win', verdict: 'GANA',
    ticket: '$249 MXN/mes (pro)',
    cacAmt: '~$90 MXN',
    clients: '15-25',
    mrr: '$3,735-6,225',
    roiPct: '+$1,205 (12% ROI)',
    note: 'Solo si haces vertical UNO (belleza CDMX). Onboarding 50 pros gratis primero = bootstrap. Pago empieza mes 2.',
  },
  {
    name: 'RentaFacil', emoji: '🏠', tag: 'polish', verdict: 'PIERDE',
    ticket: '$399 MXN/mes',
    cacAmt: '~$350 MXN',
    clients: '3-6',
    mrr: '$1,197-2,394',
    roiPct: '-$2,800 (neg)',
    note: 'CAC alto (niche). Hay que educar al host casual. No recupera $10k en 90d solo. Fusionado (RentaCore) sí.',
  },
  {
    name: 'SalonOS', emoji: '🎉', tag: 'polish', verdict: 'PIERDE SOLO',
    ticket: '$499 MXN/mes',
    cacAmt: '~$400 MXN',
    clients: '4-7',
    mrr: '$1,996-3,493',
    roiPct: '-$1,700 (neg)',
    note: 'Salones B2B convierten lento. Demo presencial requerida. Fusionado en RentaCore aprovecha SEO local.',
  },
  {
    name: 'EduLink', emoji: '🎓', tag: 'polish', verdict: 'PIERDE SOLO',
    ticket: '$199 MXN/mes',
    cacAmt: '~$220 MXN',
    clients: '6-10',
    mrr: '$1,194-1,990',
    roiPct: '-$3,400 (neg)',
    note: 'Ticket bajo + CAC medio = no pagan ads. Necesita comisión marketplace para cuadrar.',
  },
  {
    name: 'RentaMe', emoji: '📦', tag: 'kill', verdict: 'NO',
    ticket: 'comisión 12%',
    cacAmt: '~$500 MXN',
    clients: '2-4 transacciones/mes',
    mrr: '$800-1,500',
    roiPct: '-$5,500 (neg)',
    note: 'Marketplace peer-rental necesita liquidez muy alta. $10k es insuficiente para bootstrap. Fat Llama quebró.',
  },
  {
    name: 'ConventionOS', emoji: '🎤', tag: 'kill', verdict: 'NO',
    ticket: '$2,999 MXN/evento',
    cacAmt: 'imposible $10k',
    clients: '0-1',
    mrr: '$0',
    roiPct: '-$10,000 (100% pérdida)',
    note: 'Venta enterprise. CAC B2B conferencias $5-15k MXN. No hay manera con $10k budget.',
  },
  {
    name: 'Tokenizate', emoji: '📝', tag: 'kill', verdict: 'NO',
    ticket: '$1,500 MXN/mes',
    cacAmt: 'imposible LatAm',
    clients: '0-1',
    mrr: '$0',
    roiPct: '-$10,000 (100% pérdida)',
    note: 'Journals académicos MX no pagan SaaS. Mercado hispanoamericano usa OJS gratis.',
  },
]

// Project details — MX-focused
const projects = [
  {
    slug: 'hubos', name: 'HubOS', emoji: '💼', tag: 'DOBLAR',
    what: 'CRM + WhatsApp multi-sesión + CMS + plantillas. Evolution v2 + Baileys v7.',
    market: `<strong>PyME MX: 4.4M establecimientos (INEGI)</strong>, 70% usa WhatsApp como canal primario. Adopción SaaS CRM ~8%, penetrable. Ticket MX típico $199-1,599 MXN. Ola conversational commerce caliente — Leadsales levantó $12M (seed 2022) en LatAm.`,
    competitors: `<strong>Leadsales</strong> MX $1,599/mes (3u), UI simple · <strong>Kommo</strong> $15-45 USD/u/mes · <strong>Aurora Inbox</strong> LatAm · <strong>Callbell</strong> · <strong>Zenvia</strong> BR. Todos ≥$800 MXN/mes. Gap: plan starter $199-399.`,
    edge: `<strong>Multi-sesión nativa</strong> (cada agente su número) — Leadsales comparte una sola línea. Self-host = data en MX, cumple LFPDPPP. LID↔PN nativo = mensajes grupales con nombre real, nadie más lo resuelve en LatAm.`,
    unit: `Ticket $399 MXN · Stripe MX 3.6% + $3 MXN ≈ $17 · Hosting $40/cliente/mes · WhatsApp API si oficial $50/mes · <strong>Margen 85%</strong>. Break-even: 5 clientes cubren costos fijos $2k/mes.`,
    moves: [
      'Lanzar plan Starter $199 MXN/mes (1 WhatsApp, 500 contactos). Canal: TikTok demo "mira cómo atiendo 50 chats con 1 click".',
      'Ads Meta targeted PyME (dueño restaurante, clínica, inmobiliaria MX). CPC $12-18. $6k → ~50 leads → 8-10 clientes.',
      'Integrar Mercado Pago recurrente (PAY MX es regla #1 para cobrar sin fricción).',
    ],
  },
  {
    slug: 'negocioos', name: 'NegocioOS', emoji: '🏪', tag: 'AI-MOAT',
    what: 'POS + inventario + clientes + ventas + reportes + RAG.',
    market: `<strong>POS MX maduro pero fragmentado</strong>. Clip domina hardware (800k+ comercios), Loyverse líder free, Sr. Pago creciendo. Facturación electrónica CFDI 4.0 es obligatoria — ventana para nicho "POS con factura y AI". Gasto PyME MX en software operativo: $200-800 MXN/mes promedio.`,
    competitors: `<strong>Clip POS</strong> (gratis + 2.75% tx) · <strong>Loyverse</strong> (gratis) · <strong>Alegra POS</strong> + factura CFDI $399/mes · <strong>Sr. Pago</strong> · <strong>Treinta</strong> (Colombia, entró MX). Ninguno tiene RAG.`,
    edge: `<strong>RAG sobre inventario + historial</strong> único: "¿qué producto rota más jueves?", "¿qué cliente no vuelve?". Loyverse no lo puede hacer rápido (free tier). <strong>CFDI 4.0 integrado</strong> te pone a la par de Alegra pero con AI.`,
    unit: `Ticket $299 MXN · MP 3.5% · CFDI Finkok $0.30/factura · Hosting $35/cliente · <strong>Margen 82%</strong>. Break-even: 7 clientes cubren infra.`,
    moves: [
      'Integrar Finkok o SW Sapien para CFDI 4.0. SIN esto no vendes a PyME seria en MX.',
      'Video demo RAG: "pregúntale a tu POS qué vender mañana". Postear TikTok/Reels — viral potencial.',
      'Freemium hasta 50 productos/mes → paywall al crecer. Loyverse lo hace, funciona.',
    ],
  },
  {
    slug: 'servilink', name: 'ServiLink', emoji: '🔧', tag: 'FOCUS',
    what: 'Marketplace pros + bookings + reviews + subs + chat + pagos.',
    market: `<strong>Servicios on-demand MX ~$5.2B USD</strong>. Rappi domina delivery/turbo-services pero no pro-services largos (estilista, fisio, masajista). Homeshify, Zolvers (AR), Cornershop Pro fragmentados. Mercado belleza solo CDMX: 20k salones + estilistas independientes.`,
    competitors: `<strong>Rappi Turbo</strong> (solo micro-tareas) · <strong>Homeshify</strong> MX · <strong>Zolvers</strong> AR · <strong>Fixat</strong> (abogados/contadores) · <strong>TaskRabbit</strong> sin MX.`,
    edge: `<strong>Chat + booking integrado</strong> en una sola app (ningún marketplace MX lo tiene nativo sin WhatsApp externo). Subscripciones pro = recurring revenue, no solo comisión. Self-host vertical = "Rappi interno de una cadena".`,
    unit: `Comisión 10% + sub pro $249/mes · MP split automático · Hosting $1.2k/mes fijo · <strong>Margen 70%</strong>. Break-even: 40 pros pagando.`,
    moves: [
      'Escoger vertical: <strong>belleza CDMX</strong>. 50 estilistas gratis onboard + 500 consumidores via Meta Ads $5k.',
      'Reviews con foto obligatoria + respuesta del pro — moat defendible.',
      'Mercado Pago split 90/10 auto. Sin eso, los pros se van.',
    ],
  },
  {
    slug: 'rentafacil', name: 'RentaFacil', emoji: '🏠', tag: 'FUSIONAR',
    what: 'Property mgmt landlords LatAm. Async Redis streams, cache.',
    market: `<strong>MX: 40k+ anfitriones Airbnb</strong>, growing post-pandemia. PropTech LatAm $35B, MX el #2. Gap entre Airbnb host casual y Guesty enterprise (Guesty $150 USD/unit+ fuera de rango PyME MX).`,
    competitors: `<strong>Guesty</strong> $150/unit USD · <strong>Hostaway</strong> · <strong>Houm</strong> MX/CL (rentas largas) · <strong>La Haus</strong> · <strong>Tokko Broker</strong> AR. Ninguno cubre bien host 1-10 unidades MX.`,
    edge: `Ya tienes engine async + Redis. Foco: host casual MX con 1-10 propiedades. Channel manager iCal Airbnb + Booking.com gratis nivel starter.`,
    unit: `Ticket $15 USD/unit/mes = $255 MXN · MP · Hosting proporcional · <strong>Margen 78%</strong>. Break-even: 12 unidades activas.`,
    moves: [
      'Fusionar como module "Inmuebles" en <strong>RentaCore</strong>.',
      'iCal Airbnb/Booking sync mínimo viable.',
      'Cobranza Mercado Pago + reminder WhatsApp (usa HubOS como backend).',
    ],
  },
  {
    slug: 'salonos', name: 'SalonOS', emoji: '🎉', tag: 'FUSIONAR',
    what: 'Venues + spaces + events + bookings + payments + chat. Multi-sucursal.',
    market: `<strong>MX: mercado desatendido brutal</strong>. XV años (industria $800M USD MX), bodas ($1.2B USD), coworking por hora. Peerspace sin LatAm. No hay líder mexicano. Salones fragmentados publican en Facebook marketplace/WhatsApp.`,
    competitors: `<strong>Peerspace</strong> (no MX) · <strong>Spottarium</strong> (peque, MX) · <strong>Wedding Wire MX</strong> (directorio, no booking) · Facebook marketplace (!).`,
    edge: `<strong>SEO local + CFDI + Mercado Pago hold</strong> = todo lo que los salones piden. Multi-sucursal nativo para cadenas. Chat WhatsApp integrado (vía HubOS) — mamás gestionan XV años por WhatsApp 100%.`,
    unit: `Ticket $499 MXN/mes venue · 5% comisión booking · MP · <strong>Margen 80%</strong>. Break-even: 20 venues.`,
    moves: [
      'Fusionar como module "Venues" en <strong>RentaCore</strong>.',
      'SEO: landing por ciudad "salón XV años GDL", "terraza bodas MTY". 50-100 venues gratis = tráfico orgánico real.',
      'Deposit + cancelation policy con MP hold — nadie más lo tiene MX.',
    ],
  },
  {
    slug: 'edulink', name: 'EduLink', emoji: '🎓', tag: 'PIVOTAR',
    what: 'LMS cursos + lecciones + inscripciones + schedule + reviews.',
    market: `<strong>EdTech MX $1.8B USD 2026</strong>. Tutoría 1:1 niños/adultos en auge post-pandemia. Hotmart domina cursos creators (BR + MX), Platzi tech. Gap: plataforma tutoría 1:1 en vivo con Mercado Pago.`,
    competitors: `<strong>Hotmart</strong> cursos async · <strong>Platzi</strong> tech · <strong>Classgap</strong> 1:1 EU · <strong>Udemy / Coursera</strong> · <strong>Eduflow</strong>. Ninguno combina schedule + video + MP + directorio MX.`,
    edge: `<strong>Schedule + video + pago en uno</strong>. Integrate Daily.co/100ms → aula virtual con un click. WhatsApp reminders (HubOS) reducen no-shows (moat real).`,
    unit: `Tutor sub $199/mes + 10% comisión clase · MP · Daily.co $0.004/min · <strong>Margen 72%</strong>. Break-even: 60 tutores.`,
    moves: [
      'Pivot: <strong>AgendaMX</strong> (bundle con ServiLink booking). Drop cursos, foco 1:1.',
      'Video embedded Daily.co + MP split 90/10.',
      'Directorio SEO: "tutor matemáticas prepa CDMX" → trafico orgánico.',
    ],
  },
  {
    slug: 'rentame', name: 'RentaMe', emoji: '📦', tag: 'FUSIONAR',
    what: 'Vendors + items + availability + bookings + payments.',
    market: `<strong>MX: 0 líder peer-rental</strong>. Equipment rental global consolidándose (Hygglo compró Fat Llama $41.5M). Ventana LatAm abierta PERO muerte de Ruckify = señal: bootstrap marketplace peer cuesta $500k+ USD.`,
    competitors: `<strong>Hygglo</strong> SE/DE (sin LatAm) · Facebook marketplace (!) · Milanuncios (MX muy chico) · <strong>Nube.com</strong> MX (e-commerce, no rental).`,
    edge: `Ventaja nula stand-alone con $10k MXN. Fusionado como <em>module equipos</em> en RentaCore sirve para vertical foto/video pro.`,
    unit: `Comisión 12% + seguro $50/booking · MP split · <strong>Margen 65%</strong>. Break-even: 50 bookings/mes.`,
    moves: [
      'Matar app suelta. Canibalizar code a <strong>RentaCore / Equipos</strong>.',
      'Si insistes solo: nicho foto/video/drones CDMX con seguro del item.',
      'Caso contrario: deprecar 60 días.',
    ],
  },
  {
    slug: 'conventionos', name: 'ConventionOS', emoji: '🎤', tag: 'MATAR',
    what: 'Conference + speakers + stands + sponsors + tickets + tournaments.',
    market: `<strong>MX: Eventbrite domina popular</strong> (tickets < $500). Boletia es local. Enterprise B2B conferencias lo lleva Cvent (extranjero caro). Venta B2B requiere CAC $5-15k MXN — imposible con $10k.`,
    competitors: `<strong>Eventbrite</strong> · <strong>Boletia</strong> MX · <strong>Ticketmaster</strong> · <strong>Cvent</strong> enterprise · <strong>Hopin</strong> · <strong>Toornament</strong> (gaming).`,
    edge: `Ninguno. Módulo tournaments es único PERO Start.gg/Toornament gratis matan.`,
    unit: `Imposible con presupuesto dado.`,
    moves: [
      'Deprecar. Canibalizar tickets + pagos a SalonOS/RentaCore.',
      'Si insistes: pivot torneos gaming escolares MX (0 competencia pero mercado chico).',
      'Alternativa: vender módulo "stands/sponsors" como plugin B2B a organizadores existentes.',
    ],
  },
  {
    slug: 'tokenizate', name: 'Tokenizate', emoji: '📝', tag: 'MATAR',
    what: 'Editorial review SaaS.',
    market: `<strong>MX: mercado casi nulo</strong>. Journals académicos mexicanos usan OJS (gratis). CONACYT y universidades no pagan SaaS editorial. ScholarOne enterprise (Silverchair) inalcanzable.`,
    competitors: `<strong>OJS</strong> (gratis, open) · <strong>ScholarOne</strong> enterprise · <strong>Editorial Manager</strong> Elsevier.`,
    edge: `Ninguno viable MX.`,
    unit: `No calculable.`,
    moves: [
      'Deprecar. ROI negativo garantizado.',
      'Si amas el dominio: pivot a editor freelance marketplace (edición tesis/libros self-pub) — menos tech, más mercado MX.',
      'Recuperar code de subscriptions como modulo plans reutilizable.',
    ],
  },
  {
    slug: 'extensiones-hub', name: 'Extensiones + hub', emoji: '🧰', tag: 'CONSOLIDAR',
    what: 'Docs MD colection + hub landing genérico.',
    market: `N/A — no es producto.`,
    competitors: `N/A.`,
    edge: `Meta-infra útil internamente.`,
    unit: `No aplica.`,
    moves: [
      'Mover awesome-design-md a branch del repo JF5Lab.',
      'hub/index.html → landing portfolio (links a cada app live).',
      'Liberar ciclos maintenance.',
    ],
  },
]

function refreshIcons() { if (window.lucide) window.lucide.createIcons() }
onMounted(refreshIcons)
</script>

<style scoped>
.analysis { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; }
.serif { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-weight: 500; }

.skip-link { position: absolute; left: .5rem; top: -40px; padding: .5rem .9rem; background: var(--primary); color: white; border-radius: 8px; font-size: .85rem; z-index: 100; transition: top .2s; }
.skip-link:focus { top: .5rem; }
.analysis :focus-visible { outline: 2px solid var(--primary); outline-offset: 3px; border-radius: 4px; }

.top { position: sticky; top: 0; z-index: 30; backdrop-filter: blur(12px); background: rgba(9,9,15,.75); border-bottom: 1px solid var(--border); }
.top-inner { max-width: 1120px; margin: 0 auto; padding: .8rem 1.5rem; display: flex; align-items: center; gap: 2rem; }
.logo { display: inline-flex; align-items: center; gap: .55rem; font-weight: 700; color: var(--text); }
.logo-mark { width: 28px; height: 28px; border-radius: 7px; background: linear-gradient(135deg, var(--primary), var(--accent)); display: inline-flex; align-items: center; justify-content: center; color: white; }
.logo-mark :deep(svg) { width: 15px; height: 15px; }
.toc { margin-left: auto; display: flex; gap: 1.1rem; font-size: .82rem; color: var(--text2); flex-wrap: wrap; }
.toc a:hover { color: var(--text); }

.wrap { max-width: 1120px; margin: 0 auto; padding: 0 1.5rem; }

.hero { padding: 5rem 0 3rem; border-bottom: 1px solid var(--border); }
.kicker { font-size: .75rem; text-transform: uppercase; letter-spacing: .1em; color: var(--text3); font-weight: 600; margin-bottom: .8rem; }
.hero h1 { font-family: 'Fraunces', serif; font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 600; line-height: 1.05; letter-spacing: -.03em; margin-bottom: 1.2rem; }
.nowrap { white-space: nowrap; }
.lead { font-size: 1.08rem; color: var(--text2); max-width: 720px; line-height: 1.6; margin-bottom: 2rem; }
.lead strong { color: var(--text); }
.meta { display: flex; gap: 1.5rem; color: var(--text3); font-size: .85rem; flex-wrap: wrap; }
.meta span { display: inline-flex; align-items: center; gap: .4rem; }
.meta :deep(svg) { width: 14px; height: 14px; }

.block { padding: 4rem 0; border-bottom: 1px solid var(--border); scroll-margin-top: 72px; }
.block.alt { background: var(--bg2); margin: 0 -50vw; padding-inline: 50vw; border-top: 1px solid var(--border); }
.eyebrow { font-size: .72rem; text-transform: uppercase; letter-spacing: .12em; color: var(--text3); font-weight: 600; margin-bottom: .6rem; }
.block h2 { font-family: 'Fraunces', serif; font-size: clamp(1.6rem, 3.2vw, 2.3rem); font-weight: 600; line-height: 1.15; letter-spacing: -.02em; margin-bottom: .8rem; }
.sub { color: var(--text2); max-width: 760px; margin-bottom: 2rem; }
.sub strong { color: var(--text); }
.foot-note { margin-top: 1rem; color: var(--text3); font-size: .8rem; max-width: 760px; }

.tldr-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
.tldr { padding: 1.4rem; border-radius: 14px; border: 1px solid var(--border); background: rgba(255,255,255,.02); }
.tldr-h { font-weight: 700; font-size: 1rem; margin-bottom: .8rem; }
.tldr ol { padding-left: 1.2rem; color: var(--text2); line-height: 1.8; font-size: .92rem; }
.tldr-win { border-color: rgba(16,185,129,.3); background: rgba(16,185,129,.04); }
.tldr-polish { border-color: rgba(99,102,241,.3); background: rgba(99,102,241,.04); }
.tldr-kill { border-color: rgba(239,68,68,.25); background: rgba(239,68,68,.03); }

.table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 12px; }
.table-wrap table { width: 100%; border-collapse: collapse; min-width: 920px; }
.table-wrap th { background: var(--bg2); font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: var(--text3); text-align: left; padding: .75rem .9rem; border-bottom: 1px solid var(--border); }
.table-wrap td { padding: .8rem .9rem; font-size: .88rem; border-bottom: 1px solid var(--border); color: var(--text); }
.table-wrap tr:last-child td { border-bottom: none; }
.num { color: var(--text3); font-weight: 700; }
.bar { display: inline-block; height: 5px; background: linear-gradient(90deg, #818cf8, #22d3ee); border-radius: 3px; margin-right: .45rem; vertical-align: middle; min-width: 4px; max-width: 70px; }
.bar-g { background: linear-gradient(90deg, #10b981, #34d399); }
.row-win td { background: rgba(16,185,129,.05); }
.row-mid td { background: rgba(99,102,241,.03); }
.row-low td { background: rgba(239,68,68,.03); }

.tag { display: inline-block; padding: .15rem .55rem; border-radius: 999px; font-size: .68rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
.tag-win { background: rgba(16,185,129,.18); color: #34d399; }
.tag-polish { background: rgba(99,102,241,.15); color: #a5b4fc; }
.tag-kill { background: rgba(239,68,68,.15); color: #fca5a5; }

/* ROI cards */
.roi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
.roi-card { padding: 1.3rem; border-radius: 14px; border: 1px solid var(--border); background: var(--bg); }
.roi-card.roi-win { border-color: rgba(16,185,129,.35); background: rgba(16,185,129,.04); }
.roi-card.roi-kill { border-color: rgba(239,68,68,.25); background: rgba(239,68,68,.025); }
.roi-card header { display: flex; justify-content: space-between; align-items: center; margin-bottom: .9rem; gap: .5rem; }
.roi-card h3 { font-size: 1.05rem; font-weight: 700; }
.roi-row { display: flex; justify-content: space-between; padding: .3rem 0; font-size: .85rem; color: var(--text2); border-bottom: 1px dashed rgba(255,255,255,.05); }
.roi-row:last-of-type { border-bottom: none; }
.roi-row strong { color: var(--text); font-weight: 600; }
.roi-row.highlight { margin-top: .3rem; padding-top: .6rem; border-top: 1px solid var(--border); border-bottom: none; }
.roi-row.highlight strong { color: #34d399; font-size: .95rem; }
.roi-card.roi-kill .roi-row.highlight strong { color: #fca5a5; }
.roi-note { margin-top: .7rem; font-size: .8rem; color: var(--text3); line-height: 1.55; }

.project { padding: 2rem 0; border-top: 1px solid var(--border); scroll-margin-top: 72px; }
.project:first-of-type { border-top: none; }
.p-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 1.2rem; }
.p-head h3 { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 600; margin-top: .3rem; }
.p-tag { color: var(--text2); font-size: .92rem; margin-top: .3rem; }
.p-pill { display: inline-block; font-size: .66rem; padding: .2rem .7rem; border-radius: 999px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
.pill-DOBLAR, .pill-FOCUS, .pill-AI-MOAT { background: rgba(16,185,129,.18); color: #34d399; }
.pill-FUSIONAR, .pill-PIVOTAR { background: rgba(99,102,241,.18); color: #a5b4fc; }
.pill-MATAR, .pill-CONSOLIDAR { background: rgba(239,68,68,.18); color: #fca5a5; }
.anchor { color: var(--text3); font-weight: 700; font-size: 1.2rem; padding: .2rem .5rem; }
.anchor:hover { color: var(--primary); }

.p-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1.2rem; }
@media (max-width: 760px) { .p-grid { grid-template-columns: 1fr; } }
.p-card { padding: 1rem 1.1rem; background: rgba(255,255,255,.02); border: 1px solid var(--border); border-radius: 10px; }
.p-k { font-size: .7rem; text-transform: uppercase; letter-spacing: .08em; color: var(--text3); font-weight: 600; margin-bottom: .5rem; }
.p-v { font-size: .9rem; color: var(--text2); line-height: 1.6; }
.p-v :deep(strong) { color: var(--text); font-weight: 600; }
.p-v :deep(em) { color: #a5b4fc; font-style: italic; }

.p-actions { background: linear-gradient(135deg, rgba(99,102,241,.08), rgba(34,211,238,.04)); border: 1px solid rgba(99,102,241,.25); border-radius: 12px; padding: 1.1rem 1.3rem; }
.p-actions ol { margin-top: .6rem; padding-left: 1.3rem; color: var(--text); font-size: .92rem; line-height: 1.7; }

/* Bundles */
.bundle-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.2rem; }
.bundle { padding: 1.8rem; border-radius: 16px; border: 1px solid var(--border); background: var(--bg); position: relative; overflow: hidden; }
.bundle-1 { border-color: rgba(99,102,241,.35); background: linear-gradient(135deg, rgba(99,102,241,.08), transparent); }
.bundle-2 { border-color: rgba(34,211,238,.35); background: linear-gradient(135deg, rgba(34,211,238,.08), transparent); }
.bundle-3 { border-color: rgba(16,185,129,.35); background: linear-gradient(135deg, rgba(16,185,129,.08), transparent); }
.bundle-4 { border-color: rgba(245,158,11,.35); background: linear-gradient(135deg, rgba(245,158,11,.08), transparent); }
.bundle-n { font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 600; line-height: 1; color: var(--text3); position: absolute; right: 1.2rem; top: 1rem; opacity: .3; }
.bundle h3 { font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 600; margin-bottom: .3rem; }
.bundle-src { font-size: .78rem; color: var(--text3); margin-bottom: .9rem; font-family: ui-monospace, monospace; }
.bundle p { color: var(--text2); font-size: .9rem; line-height: 1.6; margin-bottom: .8rem; }
.bundle-why { background: rgba(0,0,0,.2); padding: .7rem .9rem; border-radius: 8px; border-left: 2px solid var(--primary); }
.bundle-stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: .6rem; margin-top: 1rem; }
.bundle-stats div { background: rgba(255,255,255,.03); padding: .5rem .75rem; border-radius: 7px; }
.bundle-stats dt { font-size: .65rem; color: var(--text3); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .15rem; }
.bundle-stats dd { font-weight: 700; font-size: .95rem; color: var(--text); }

/* Veredicto steps */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }
@media (max-width: 780px) { .steps { grid-template-columns: 1fr; } }
.step { padding: 1.6rem; background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; }
.step-n { font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 600; background: linear-gradient(135deg, #a5b4fc, #22d3ee); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: .6rem; }
.step h3 { font-size: 1.05rem; font-weight: 600; margin-bottom: .4rem; }
.step p { color: var(--text2); font-size: .9rem; }
.step strong { color: var(--text); }

.finale { padding: 2rem; border-radius: 14px; background: radial-gradient(circle at 50% 0%, rgba(99,102,241,.18), transparent 70%), var(--bg2); border: 1px solid var(--border); }
.finale h3 { font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; }
.finale-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.3rem; }
.finale-grid div { background: rgba(255,255,255,.03); padding: .9rem 1rem; border-radius: 10px; }
.finale-grid dt { font-size: .7rem; color: var(--text3); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem; }
.finale-grid dd { font-size: 1.3rem; font-weight: 700; color: var(--text); }
.finale-grid dd.pos { color: #34d399; }
.finale-kicker { color: var(--text2); }
.finale-kicker strong { color: var(--text); }

/* Sources */
.sources { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: .4rem; }
.sources li a { color: var(--text2); font-size: .85rem; }
.sources li a:hover { color: var(--primary); }

.foot { padding: 2rem 1.5rem; border-top: 1px solid var(--border); color: var(--text3); font-size: .85rem; }
.foot-inner { max-width: 1120px; margin: 0 auto; display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.foot a { color: var(--text2); }
.foot a:hover { color: var(--primary); }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>
