<template>
  <div class="analysis">
    <a href="#main" class="skip-link">Saltar al contenido</a>

    <header class="top" role="banner">
      <div class="top-inner">
        <router-link to="/" class="logo" aria-label="HubOS inicio">
          <span class="logo-mark"><i data-lucide="layers"></i></span>
          <span>Ruta al millón · MX</span>
        </router-link>
        <nav aria-label="Índice" class="toc">
          <a href="#tesis">Tesis</a>
          <a href="#timeline">Timeline</a>
          <a href="#productos">Productos</a>
          <a href="#consultoria">Consultoría</a>
          <a href="#vivir">Vivir de esto</a>
          <a href="#calculadora">Calcu</a>
        </nav>
      </div>
    </header>

    <main id="main" class="wrap" role="main">
      <!-- HERO -->
      <section class="hero" aria-labelledby="h1">
        <p class="kicker">Plan de negocio · $10,000 MXN · 24 meses</p>
        <h1 id="h1">
          Cómo llegar a <em class="serif">tu primer millón</em><br/>
          de pesos vendiendo software +<br/>
          <span class="highlight">consultoría</span> al mismo tiempo.
        </h1>
        <p class="lead">
          No es magia. Es matemática sencilla:
          <strong>consultoría paga la renta hoy</strong>,
          <strong>software compone mañana</strong>.
          Aquí te explico el cómo, con números reales para México.
        </p>
        <div class="hero-big">
          <div>
            <dt>Meta</dt>
            <dd>$1,000,000 MXN</dd>
          </div>
          <div>
            <dt>Plazo</dt>
            <dd>24 meses</dd>
          </div>
          <div>
            <dt>Capital</dt>
            <dd>$10,000 MXN</dd>
          </div>
        </div>
      </section>

      <!-- TESIS -->
      <section id="tesis" class="block" aria-labelledby="tesis-h">
        <p class="eyebrow">La tesis en 90 segundos</p>
        <h2 id="tesis-h">Dos motores. Mismo tanque.</h2>

        <div class="two-col">
          <article class="motor motor-a">
            <div class="motor-n">1</div>
            <h3>Consultoría</h3>
            <p class="motor-sub">Dinero rápido. Aprendes el mercado.</p>
            <ul>
              <li>Cobras <strong>$400-800 MXN/hora</strong> desde el día 1.</li>
              <li>20 hrs/semana = <strong>$32-64 mil MXN/mes</strong>.</li>
              <li>Cada cliente es un laboratorio. Sales con casos reales.</li>
              <li>No requiere capital. Solo reputación + LinkedIn + 10 DMs/día.</li>
            </ul>
          </article>

          <article class="motor motor-b">
            <div class="motor-n">2</div>
            <h3>Software (HubOS + bundles)</h3>
            <p class="motor-sub">Dinero lento. Compone exponencial.</p>
            <ul>
              <li>Ticket <strong>$199-999 MXN/mes</strong> por cliente.</li>
              <li>Margen <strong>78-85%</strong> después de infra y pagos.</li>
              <li>Cada cliente paga <em>todos los meses</em> sin que hagas nada nuevo.</li>
              <li>100 clientes = <strong>$50k MXN/mes recurrente</strong>.</li>
            </ul>
          </article>
        </div>

        <div class="thesis-punch">
          <h3>🎯 La magia está en combinarlos</h3>
          <p>
            Cobras consultoría a una PyME → instalas <strong>HubOS dentro de su
            operación</strong> como parte del proyecto → terminas la consultoría
            → el software se queda cobrando para siempre. <strong>Cada cliente
            de consultoría = 1 cliente recurrente software gratis.</strong>
            Eso es el hack.
          </p>
        </div>
      </section>

      <!-- TIMELINE -->
      <section id="timeline" class="block alt" aria-labelledby="tl-h">
        <p class="eyebrow">Timeline</p>
        <h2 id="tl-h">Los 6 hitos de aquí al millón.</h2>
        <p class="sub">
          Cada hito tiene un número objetivo, una acción específica y
          cuánto debería haber en la cuenta al terminarlo.
        </p>

        <ol class="timeline">
          <li v-for="(m, i) in milestones" :key="i" class="milestone">
            <div class="ms-head">
              <span class="ms-num">{{ m.mes }}</span>
              <div>
                <h3>{{ m.title }}</h3>
                <p class="ms-goal">{{ m.goal }}</p>
              </div>
              <div class="ms-money">
                <div class="ms-money-v">{{ m.acum }}</div>
                <div class="ms-money-l">acumulado</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-split">
                <div>
                  <div class="ms-k">💼 Consultoría</div>
                  <p>{{ m.consult }}</p>
                </div>
                <div>
                  <div class="ms-k">📦 Software</div>
                  <p>{{ m.software }}</p>
                </div>
              </div>
              <div class="ms-what">
                <div class="ms-k">✅ Qué hacer este mes</div>
                <ul><li v-for="(a, j) in m.actions" :key="j">{{ a }}</li></ul>
              </div>
            </div>
          </li>
        </ol>
      </section>

      <!-- PRODUCTOS -->
      <section id="productos" class="block" aria-labelledby="prod-h">
        <p class="eyebrow">Qué construyes</p>
        <h2 id="prod-h">3 productos. Punto. Lo demás son distracciones.</h2>
        <p class="sub">
          Tienes 10 proyectos. Mantener 10 = fracasar 10 veces en paralelo.
          <strong>Mata 7, enfoca 3</strong>. Estos son los que importan:
        </p>

        <div class="prods-grid">
          <article v-for="p in productos" :key="p.name" class="prod" :class="'prod-' + p.rank">
            <div class="prod-rank">#{{ p.rank }}</div>
            <h3>{{ p.emoji }} {{ p.name }}</h3>
            <p class="prod-tag">{{ p.pitch }}</p>

            <div class="prod-nums">
              <div><dt>Cliente paga</dt><dd>{{ p.ticket }}</dd></div>
              <div><dt>Tu costo real</dt><dd>{{ p.cost }}</dd></div>
              <div><dt>Margen</dt><dd class="pos">{{ p.margin }}</dd></div>
            </div>

            <div class="prod-section">
              <h4>👥 A quién le vendes</h4>
              <p>{{ p.who }}</p>
            </div>
            <div class="prod-section">
              <h4>⚔️ Contra quién compites</h4>
              <p>{{ p.vs }}</p>
            </div>
            <div class="prod-section">
              <h4>🎯 Por qué ganas</h4>
              <p>{{ p.edge }}</p>
            </div>
          </article>
        </div>

        <div class="kill-list">
          <h3>⚰️ Lo que matas esta semana</h3>
          <ul>
            <li><strong>ConventionOS</strong> — Cvent/Eventbrite imbatibles, CAC imposible con $10k.</li>
            <li><strong>Tokenizate</strong> — journals MX usan OJS gratis, no pagan SaaS.</li>
            <li><strong>RentaMe</strong> — canibaliza code a RentaCore, mata como app.</li>
            <li><strong>EduLink</strong> como LMS → pivot a módulo de agenda dentro de ServiLink.</li>
            <li><strong>Extensiones / hub</strong> — no son producto, son meta-infra.</li>
            <li><strong>RentaFacil + SalonOS</strong> como apps sueltas → fusionan en <em>RentaCore</em>.</li>
          </ul>
          <p class="kill-why">
            <strong>Por qué importa:</strong> cada app viva = 3-5 hrs/sem de
            maintenance. 10 apps × 4 hrs = 40 hrs/sem solo sobreviviendo.
            Sin tiempo para consultoría ni ventas. Mata 7 → libera 28 hrs/sem
            → canaliza a ingresos reales.
          </p>
        </div>
      </section>

      <!-- CONSULTORÍA -->
      <section id="consultoria" class="block alt" aria-labelledby="con-h">
        <p class="eyebrow">El motor de cash</p>
        <h2 id="con-h">Consultoría práctica para devs en MX.</h2>
        <p class="sub">
          No necesitas ser gurú. Necesitas <strong>resolver un problema
          concreto</strong> que una PyME ya tiene y paga de inmediato.
          Aquí las 4 que venden hoy:
        </p>

        <div class="offers">
          <article v-for="o in offers" :key="o.name" class="offer">
            <div class="offer-head">
              <h3>{{ o.emoji }} {{ o.name }}</h3>
              <div class="offer-price">{{ o.price }}</div>
            </div>
            <p class="offer-what">{{ o.what }}</p>
            <div class="offer-grid">
              <div>
                <div class="offer-k">Dura</div>
                <div class="offer-v">{{ o.time }}</div>
              </div>
              <div>
                <div class="offer-k">Cliente tipo</div>
                <div class="offer-v">{{ o.who }}</div>
              </div>
              <div>
                <div class="offer-k">Dónde conseguirlos</div>
                <div class="offer-v">{{ o.where }}</div>
              </div>
            </div>
            <div class="offer-upsell">
              <strong>🚀 Upsell automático:</strong> {{ o.upsell }}
            </div>
          </article>
        </div>

        <div class="consult-math">
          <h3>La matemática del combo</h3>
          <div class="cm-grid">
            <div>
              <dt>1 proyecto consultoría/mes</dt>
              <dd>$30-60k MXN one-shot</dd>
            </div>
            <div>
              <dt>Deja 1 cliente software</dt>
              <dd>$399-999 MXN/mes recurrente</dd>
            </div>
            <div>
              <dt>Año 1: 12 proyectos</dt>
              <dd>~$480k MXN consult + <strong class="pos">~$60k MRR</strong></dd>
            </div>
            <div>
              <dt>Año 2: MRR crece, consult baja</dt>
              <dd><strong class="pos">$500k MRR + $300k consult = $800k/año</strong></dd>
            </div>
          </div>
        </div>
      </section>

      <!-- COMO VIVIR DE ESTO -->
      <section id="vivir" class="block" aria-labelledby="viv-h">
        <p class="eyebrow">Cómo vivir de esto</p>
        <h2 id="viv-h">Estrategia para vivir simple y sostenible con el portafolio.</h2>
        <p class="sub">
          No basta con facturar. Hay que <strong>sobrevivir el mes</strong>,
          <strong>reinvertir sin quebrar</strong>, y <strong>no morir de
          burnout</strong>. Aquí el playbook mes a mes.
        </p>

        <!-- Split del dinero -->
        <div class="vivir-split">
          <h3>📊 Cómo repartir cada peso que entra</h3>
          <div class="split-bars">
            <div class="split-bar" style="--w:40%; --c:#34d399">
              <div class="split-label"><strong>40%</strong> Vida personal</div>
              <p>Renta + comida + transporte + salud. Meta: vivir con $15-20k MXN/mes en CDMX/GDL.</p>
            </div>
            <div class="split-bar" style="--w:25%; --c:#818cf8">
              <div class="split-label"><strong>25%</strong> Impuestos + RESICO</div>
              <p>SAT no perdona. Aparta esto cada mes. RESICO para freelance = 1-2.5% si facturas &lt;$3.5M MXN/año.</p>
            </div>
            <div class="split-bar" style="--w:20%; --c:#22d3ee">
              <div class="split-label"><strong>20%</strong> Reinversión</div>
              <p>Meta Ads + herramientas (Evolution API hosting, Mercado Pago, CFDI provider, VA). No contratar full-time hasta mes 12+.</p>
            </div>
            <div class="split-bar" style="--w:10%; --c:#fbbf24">
              <div class="split-label"><strong>10%</strong> Fondo emergencia</div>
              <p>Runway 3-6 meses en cuenta aparte (CETES 28d 10% anual). Si un cliente no paga o te enfermas, no se muere el negocio.</p>
            </div>
            <div class="split-bar" style="--w:5%; --c:#f472b6">
              <div class="split-label"><strong>5%</strong> Tú mismo</div>
              <p>Libros, cursos, conferencias, salud mental. Esto es el motor — si se apaga, todo para.</p>
            </div>
          </div>
        </div>

        <!-- Rutina semanal -->
        <div class="vivir-routine">
          <h3>⏱️ Tu semana tipo (para no morir)</h3>
          <div class="routine-grid">
            <div class="routine-day">
              <div class="rd-day">Lun</div>
              <div class="rd-focus">🔨 Construcción</div>
              <p>Días de código puro. Sin reuniones. Avanzas features del producto que menos MRR tiene todavía.</p>
            </div>
            <div class="routine-day">
              <div class="rd-day">Mar</div>
              <div class="rd-focus">🔨 Construcción</div>
              <p>Continúa Lunes. Deep work 6-8 hrs. Cero notificaciones.</p>
            </div>
            <div class="routine-day">
              <div class="rd-day">Mié</div>
              <div class="rd-focus">💼 Consultoría</div>
              <p>Todas las calls + entregas consult de la semana apretadas aquí. Cobras más por día completo.</p>
            </div>
            <div class="routine-day">
              <div class="rd-day">Jue</div>
              <div class="rd-focus">💼 Consultoría</div>
              <p>Continúa Miércoles. Facturación + seguimientos.</p>
            </div>
            <div class="routine-day">
              <div class="rd-day">Vie</div>
              <div class="rd-focus">📣 Ventas + marketing</div>
              <p>30 DMs LinkedIn + 2 posts + 1 video. Calls descubrimiento con leads nuevos.</p>
            </div>
            <div class="routine-day">
              <div class="rd-day">Sáb</div>
              <div class="rd-focus">🧠 Estrategia</div>
              <p>2 hrs: revisar métricas (MRR, churn, pipeline). El resto del día para ti. Sin laptop después de mediodía.</p>
            </div>
            <div class="routine-day">
              <div class="rd-day">Dom</div>
              <div class="rd-focus">🌴 Off</div>
              <p>Día <strong>real</strong> de descanso. Sin Slack, sin email, sin "solo reviso una cosita". El burnout es el asesino #1 de solopreneurs.</p>
            </div>
          </div>
        </div>

        <!-- Guardrails -->
        <div class="guardrails">
          <h3>🚧 Las 5 reglas para no quebrar</h3>
          <ol>
            <li>
              <strong>No contrates full-time antes del mes 12.</strong>
              Freelancers pagados por proyecto, no payroll fijo.
              Un empleado = $25-35k MXN/mes de compromiso. Primero llega a $80k MRR estables.
            </li>
            <li>
              <strong>Factura todo desde el mes 1.</strong>
              RESICO (Régimen Simplificado de Confianza) o Actividad Empresarial.
              Sin facturas = no puedes vender a empresa seria en MX = no escalas.
              Usa Alegra o Konfío para contabilidad ($300-600 MXN/mes).
            </li>
            <li>
              <strong>Reinvierte mientras crezca MRR, no mientras crezcan apps.</strong>
              10 apps sin clientes = $0. 1 app con 200 clientes = $100k MRR.
              Prioriza crecer clientes, no features.
            </li>
            <li>
              <strong>Cobra por adelantado consultoría.</strong>
              50% al firmar, 50% al entregar. Si un cliente pelea esto, huye.
              Te salva de 3 meses de flujo de caja negativo por un cliente que no paga.
            </li>
            <li>
              <strong>Trabaja máximo 50 hrs/sem reales.</strong>
              Más que eso = menos calidad + burnout en 6-12 meses.
              Los que trabajan 80 hrs/sem no llegan a año 3. Es matemática.
            </li>
          </ol>
        </div>

        <!-- Ejemplo concreto mes típico -->
        <div class="sample-month">
          <h3>🗓️ Cómo se ve un mes real en el mes 12</h3>
          <div class="sample-grid">
            <div class="sample-col">
              <div class="sample-k">Ingresos</div>
              <div class="sample-row"><span>Consultoría (3 proyectos)</span><strong>+$120,000</strong></div>
              <div class="sample-row"><span>Software MRR (80 clientes)</span><strong>+$40,000</strong></div>
              <div class="sample-row total"><span>Total bruto</span><strong class="pos">$160,000</strong></div>
            </div>
            <div class="sample-col">
              <div class="sample-k">Egresos</div>
              <div class="sample-row"><span>Infra + herramientas</span><strong>-$8,000</strong></div>
              <div class="sample-row"><span>Meta/Google Ads</span><strong>-$15,000</strong></div>
              <div class="sample-row"><span>VA + contabilidad</span><strong>-$7,000</strong></div>
              <div class="sample-row"><span>Impuestos RESICO (~2%)</span><strong>-$3,200</strong></div>
              <div class="sample-row total"><span>Total gastos</span><strong class="neg">-$33,200</strong></div>
            </div>
          </div>
          <div class="sample-net">
            <div>
              <dt>Neto para ti</dt>
              <dd class="pos">$126,800 MXN</dd>
            </div>
            <div>
              <dt>Pagas impuestos</dt>
              <dd>$3,200</dd>
            </div>
            <div>
              <dt>Vida personal (40%)</dt>
              <dd>$50,720</dd>
            </div>
            <div>
              <dt>Fondo + tú mismo (15%)</dt>
              <dd>$19,020</dd>
            </div>
            <div>
              <dt>Libre (reinvertir o ahorrar)</dt>
              <dd class="pos">$57,060</dd>
            </div>
          </div>
        </div>
      </section>

      <!-- CALCULADORA -->
      <section id="calculadora" class="block" aria-labelledby="calc-h">
        <p class="eyebrow">Calculadora interactiva</p>
        <h2 id="calc-h">¿Cuándo te haces millonario? Mueve los deslizadores.</h2>

        <div class="calc">
          <div class="calc-controls">
            <label>
              Clientes consultoría / mes
              <span class="calc-v">{{ consult }}</span>
              <input type="range" min="0" max="6" step="1" v-model.number="consult" />
            </label>
            <label>
              Ticket promedio consultoría (MXN)
              <span class="calc-v">${{ fmt(ticket) }}</span>
              <input type="range" min="15000" max="80000" step="5000" v-model.number="ticket" />
            </label>
            <label>
              Software: nuevos clientes/mes
              <span class="calc-v">{{ swNew }}</span>
              <input type="range" min="0" max="25" step="1" v-model.number="swNew" />
            </label>
            <label>
              Software: ticket MXN/mes
              <span class="calc-v">${{ fmt(swTicket) }}</span>
              <input type="range" min="199" max="1500" step="50" v-model.number="swTicket" />
            </label>
            <label>
              Churn software mensual
              <span class="calc-v">{{ churn }}%</span>
              <input type="range" min="0" max="15" step="1" v-model.number="churn" />
            </label>
          </div>

          <div class="calc-result">
            <div class="calc-big">
              <dt>Mes que cruzas $1M acumulado</dt>
              <dd :class="milestoneMonth > 0 ? 'pos' : 'neg'">
                {{ milestoneMonth > 0 ? `Mes ${milestoneMonth}` : 'Nunca con estos números' }}
              </dd>
            </div>
            <div class="calc-row"><span>Ingreso mes 12</span><strong>${{ fmt(month12) }} MXN</strong></div>
            <div class="calc-row"><span>MRR mes 12</span><strong>${{ fmt(mrr12) }} MXN</strong></div>
            <div class="calc-row"><span>Ingreso mes 24</span><strong>${{ fmt(month24) }} MXN</strong></div>
            <div class="calc-row highlight"><span>Acumulado 24 meses</span><strong class="pos">${{ fmt(total24) }} MXN</strong></div>
            <p class="calc-note">
              Supuestos: margen software 80%, consultoría se cobra misma del mes.
              Churn aplica al MRR acumulado cada mes. Si la gráfica no cruza
              $1M en 24 meses, necesitas <em>más clientes</em>, no más apps.
            </p>
          </div>
        </div>
      </section>

      <!-- REGLA -->
      <section class="block finale-block" aria-labelledby="regla-h">
        <h2 id="regla-h">La regla de hierro.</h2>
        <div class="regla">
          <p>
            Los 10 proyectos no te hacen millonario.
            <strong>La concentración + la recurrencia sí.</strong>
          </p>
          <p>
            Consultoría es el trampolín. Software es el elevador.
            <strong>Úsalos en ese orden</strong>: cobra consult hoy, mete HubOS
            en cada cliente, y en 18-24 meses el MRR supera a la consultoría
            y te liberas de las horas.
          </p>
          <p class="regla-final">
            Un millón MXN en 24 meses con $10k iniciales =
            <strong class="pos">absolutamente posible</strong> si ejecutas.
            <br/>Con los 10 proyectos vivos = imposible.
          </p>
        </div>
      </section>

      <!-- FUENTES -->
      <section class="block" aria-labelledby="src-h">
        <p class="eyebrow">De dónde salen los números</p>
        <h2 id="src-h">Fuentes + supuestos.</h2>
        <ul class="sources">
          <li><a href="https://www.aurorainbox.com/en/2026/01/31/best-crm-whatsapp-mexico/" target="_blank" rel="noopener">Aurora Inbox — CRM WhatsApp MX 2026</a></li>
          <li><a href="https://techcrunch.com/2023/08/28/whatsapp-leadsales-conversational-commerce/" target="_blank" rel="noopener">TechCrunch — Leadsales LatAm</a></li>
          <li><a href="https://loyverse.com/features" target="_blank" rel="noopener">Loyverse POS</a></li>
          <li><a href="https://www.grandviewresearch.com/horizon/outlook/property-management-software-market/latin-america" target="_blank" rel="noopener">Grand View — LatAm PropTech</a></li>
          <li><a href="https://theglobaleconomics.com/2026/04/15/latam-real-estate/" target="_blank" rel="noopener">Global Economics — LatAm PropTech 2026</a></li>
          <li><a href="https://www.businessresearchinsights.com/market-reports/on-demand-services-market-124836" target="_blank" rel="noopener">BRI — On-Demand Services</a></li>
          <li><a href="https://straitsresearch.com/report/lms-market/latam" target="_blank" rel="noopener">Straits Research — LatAm LMS</a></li>
          <li><a href="https://www.marketdataforecast.com/market-reports/latin-america-e-learning-market" target="_blank" rel="noopener">MarketDataForecast — LatAm eLearning</a></li>
        </ul>
        <p class="foot-note">
          Tarifas consultoría: rangos reales dev MX seniors 2026 (LinkedIn + Glassdoor + WorkAna).
          Tickets software: ratios internos escalados a PyME MX según reporte adopción SaaS INEGI 2024.
        </p>
      </section>
    </main>

    <footer class="foot">
      <div class="foot-inner">
        <span>© 2026 JF5 Lab · plan 24 meses</span>
        <router-link to="/">← Volver a HubOS</router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const milestones = [
  {
    mes: 'Mes 1-2', title: 'Cash inmediato', goal: 'Sobrevivir sin quemar los $10k.',
    acum: '$60,000 MXN',
    consult: '2 clientes consultoría × $30k promedio = $60k. Enfoque: setup WhatsApp Business + CRM para PyMEs que ya te pidan.',
    software: '0 clientes pagos todavía. Estás puliendo HubOS + onboarding con los 2 clientes consult.',
    actions: [
      'Publica 3 videos en LinkedIn mostrando antes/después de HubOS en PyME real.',
      'Envía 30 DMs/semana a dueños de negocios en CDMX (comercio local, clínicas, inmobiliarias).',
      'Cobra $30-40k por proyecto "llave en mano". Incluye HubOS gratis 3 meses.',
    ],
  },
  {
    mes: 'Mes 3-4', title: 'Primer MRR', goal: 'Convertir clientes consult → software.',
    acum: '$160,000 MXN',
    consult: '2 más × $35k = $70k.',
    software: 'Los 4 de consultoría convierten tras prueba gratis. 4 × $499 = ~$2k MRR.',
    actions: [
      'Lanza landing de HubOS con precios públicos. 3 planes: $199/$399/$699 MXN.',
      'Integra Mercado Pago recurrente. Sin eso no cobras en MX.',
      'Meta Ads $2k/mes targeting "dueños PyME CDMX".',
    ],
  },
  {
    mes: 'Mes 5-8', title: 'Bundle SuiteOperativa', goal: 'Upsell a los que ya tienes.',
    acum: '$380,000 MXN',
    consult: '3 proyectos/mes × $40k = $120k mensuales brutos.',
    software: '15-20 clientes totales × promedio $550 = ~$10k MRR.',
    actions: [
      'Integra NegocioOS (POS + CFDI 4.0) como addon de HubOS.',
      'Sube precio paquete a $999/mes. Los clientes nuevos pagan más.',
      'Contrata 1 freelance VA para agendar ventas (tú solo cierras).',
    ],
  },
  {
    mes: 'Mes 9-12', title: 'RentaCore MVP', goal: 'Entrar al segundo vertical.',
    acum: '$700,000 MXN',
    consult: '3-4 proyectos/mes = $140k/mes brutos.',
    software: '35-45 clientes activos = ~$25k MRR. Churn <5%.',
    actions: [
      'Fusiona RentaFacil + RentaMe + SalonOS → RentaCore. Lanzamiento vertical salones XV años CDMX.',
      'SEO local: 100 landings por ciudad/tipo venue.',
      'Caso de éxito en video: cliente con $X aumento de reservas.',
    ],
  },
  {
    mes: 'Mes 13-18', title: 'Escala horizontal', goal: 'Convertir consultoría en contratos anuales.',
    acum: '$1,050,000 MXN',
    consult: 'Cambia a retainer: 4 clientes × $25k/mes = $100k/mes fijo.',
    software: '80-120 clientes × promedio $650 = ~$55k MRR.',
    actions: [
      'Transforma 4 clientes consult en retainers anuales con SLA + HubOS.',
      'Publica curso grabado "Cómo escalar tu PyME con WhatsApp" → lead magnet.',
      'Primera contratación full-time: dev junior $18-22k/mes para soporte.',
    ],
  },
  {
    mes: 'Mes 19-24', title: 'MRR > Consultoría', goal: 'Libertad — el software paga más que tú cobras hora.',
    acum: '$1,800,000+ MXN',
    consult: 'Rechazas 50% de proyectos. Solo tomas retainers premium.',
    software: '200+ clientes × $700 = $140k MRR. Este es el flywheel.',
    actions: [
      'Contratar sales closer comisionista (15% + base $15k).',
      'Primer round pre-seed opcional ($2-5M MXN) para acelerar.',
      'Plantear sucesión: si te atropella un camión, el negocio sigue.',
    ],
  },
]

const productos = [
  {
    rank: 1, name: 'HubOS', emoji: '💼',
    pitch: 'CRM + WhatsApp multi-sesión para PyMEs mexicanas que venden por chat.',
    ticket: '$399 MXN/mes', cost: '$60/cliente/mes', margin: '85%',
    who: 'Clínicas, inmobiliarias, escuelas, tiendas que atienden 20-500 chats/día. Ya pagan Leadsales a $1,600/mes o usan WhatsApp manual.',
    vs: 'Leadsales ($1,600/mes MX), Kommo ($300/u/mes), Callbell. Todos ≥$800 MXN. Tu plan starter $199 los saca del mercado en micro-PyME.',
    edge: 'Multi-sesión nativa (cada agente su número), LID↔PN resuelto, data en MX (LFPDPPP). Self-host opcional para empresas paranoicas.',
  },
  {
    rank: 2, name: 'NegocioOS', emoji: '🏪',
    pitch: 'POS con CFDI 4.0 + IA que le dice al dueño qué producto empujar.',
    ticket: '$299 MXN/mes', cost: '$40/cliente/mes', margin: '82%',
    who: 'Cafeterías, barberías, abarrotes, papelerías. Ya usan Clip o Loyverse pero no pueden facturar fácil.',
    vs: 'Clip (gratis + 2.75% tx), Loyverse (gratis, sin CFDI), Alegra POS ($399 sin IA).',
    edge: 'CFDI 4.0 integrado + RAG sobre ventas: "¿qué vender el viernes?" es único en LatAm.',
  },
  {
    rank: 3, name: 'RentaCore', emoji: '🏠',
    pitch: 'Booking engine con 3 verticales: salones, inmuebles, equipos pro.',
    ticket: '$499 MXN/mes', cost: '$80/cliente/mes', margin: '78%',
    who: 'Salones XV años, Airbnb hosts 1-10 unidades, renta de foto/video/drones.',
    vs: 'Guesty ($150 USD/unit caro), Peerspace (sin MX), Facebook marketplace (!).',
    edge: 'Multi-vertical bajo un engine. Mercado Pago hold + CFDI + WhatsApp reminders. SEO local por ciudad.',
  },
]

const offers = [
  {
    emoji: '📲', name: 'Setup WhatsApp Business + HubOS',
    price: '$15-30k MXN',
    what: 'Conectas WhatsApp, migras contactos, armas plantillas, capacitas al equipo. Dejas la PyME usando HubOS.',
    time: '1-2 semanas',
    who: 'Clínicas dentales, inmobiliarias chicas, escuelas privadas.',
    where: 'LinkedIn (manda DMs a dueños), grupos Facebook de emprendedores MX, referidos de tu red.',
    upsell: 'Los dejas pagando HubOS $399-999/mes después del proyecto. Uno de cada 2 se queda.',
  },
  {
    emoji: '🤖', name: 'Automatización flujos PyME',
    price: '$25-50k MXN',
    what: 'Conectas WhatsApp + CRM + POS + email. Bots, plantillas por etapa, reports semanales.',
    time: '3-4 semanas',
    who: 'Negocios con 5-30 empleados, ventas B2C.',
    where: 'LinkedIn ads ($500 MXN target CEO PyME MX), networking en cámaras (Coparmex, Canaco).',
    upsell: 'HubOS + NegocioOS bundle $999/mes permanente.',
  },
  {
    emoji: '🏗️', name: 'Web + tienda + ventas WhatsApp',
    price: '$20-40k MXN',
    what: 'Landing + Mercado Pago + CRM + WhatsApp integrado. "Llave en mano" digital para PyME.',
    time: '2-3 semanas',
    who: 'Negocios sin presencia digital que reciben pedidos por WhatsApp.',
    where: 'Grupos Facebook locales, Coworks, referidos.',
    upsell: 'HubOS $399/mes + comisión 3% sobre ventas que pasen por tu stack.',
  },
  {
    emoji: '📊', name: 'Diagnóstico + roadmap 90d',
    price: '$8-15k MXN',
    what: 'Audita procesos, mapeas dolores, entregas roadmap priorizado. Es la puerta para proyectos grandes.',
    time: '1 semana',
    who: 'Dueños que "sienten que algo no jala" pero no saben qué.',
    where: 'Publicaciones LinkedIn + cold DM offer gratis 30 min call.',
    upsell: 'El 70% de diagnósticos termina en proyecto de $25-50k. Además, HubOS entra.',
  },
]

/* Calculadora */
const consult = ref(2)
const ticket = ref(35000)
const swNew = ref(4)
const swTicket = ref(499)
const churn = ref(3)

function fmt(n) { return Math.round(n).toLocaleString('es-MX') }

const series = computed(() => {
  const rows = []
  let mrr = 0
  let total = 0
  const retain = 1 - churn.value / 100
  for (let m = 1; m <= 24; m++) {
    mrr = mrr * retain + swNew.value * swTicket.value
    const consultRev = consult.value * ticket.value
    const income = consultRev + mrr
    total += income
    rows.push({ m, mrr, income, total })
  }
  return rows
})
const month12 = computed(() => series.value[11]?.income || 0)
const mrr12 = computed(() => series.value[11]?.mrr || 0)
const month24 = computed(() => series.value[23]?.income || 0)
const total24 = computed(() => series.value[23]?.total || 0)
const milestoneMonth = computed(() => {
  const r = series.value.find(x => x.total >= 1_000_000)
  return r ? r.m : 0
})

function refreshIcons() { if (window.lucide) window.lucide.createIcons() }
onMounted(refreshIcons)
</script>

<style scoped>
.analysis { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; line-height: 1.65; }
.serif { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-weight: 500; }
.highlight { background: linear-gradient(120deg, transparent 0%, rgba(245,158,11,.25) 0%, rgba(245,158,11,.25) 100%, transparent 100%); padding: 0 .2em; }

.skip-link { position: absolute; left: .5rem; top: -40px; padding: .5rem .9rem; background: var(--primary); color: white; border-radius: 8px; font-size: .85rem; z-index: 100; transition: top .2s; }
.skip-link:focus { top: .5rem; }
.analysis :focus-visible { outline: 2px solid var(--primary); outline-offset: 3px; border-radius: 4px; }

.top { position: sticky; top: 0; z-index: 30; backdrop-filter: blur(12px); background: rgba(9,9,15,.78); border-bottom: 1px solid var(--border); }
.top-inner { max-width: 960px; margin: 0 auto; padding: .85rem 1.5rem; display: flex; align-items: center; gap: 1.5rem; }
.logo { display: inline-flex; align-items: center; gap: .55rem; font-weight: 700; color: var(--text); }
.logo-mark { width: 28px; height: 28px; border-radius: 7px; background: linear-gradient(135deg, var(--primary), var(--accent)); display: inline-flex; align-items: center; justify-content: center; color: white; }
.logo-mark :deep(svg) { width: 15px; height: 15px; }
.toc { margin-left: auto; display: flex; gap: 1.1rem; font-size: .82rem; color: var(--text2); flex-wrap: wrap; }
.toc a:hover { color: var(--text); }

.wrap { max-width: 960px; margin: 0 auto; padding: 0 1.5rem; }

.hero { padding: 5rem 0 3rem; border-bottom: 1px solid var(--border); }
.kicker { font-size: .75rem; text-transform: uppercase; letter-spacing: .1em; color: var(--text3); font-weight: 600; margin-bottom: 1rem; }
.hero h1 { font-family: 'Fraunces', serif; font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 600; line-height: 1.1; letter-spacing: -.03em; margin-bottom: 1.3rem; }
.lead { font-size: 1.1rem; color: var(--text2); max-width: 680px; margin-bottom: 2.5rem; }
.lead strong { color: var(--text); }

.hero-big { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.hero-big > div { background: rgba(255,255,255,.03); border: 1px solid var(--border); border-radius: 12px; padding: 1.2rem 1.4rem; }
.hero-big dt { font-size: .7rem; text-transform: uppercase; letter-spacing: .1em; color: var(--text3); margin-bottom: .3rem; }
.hero-big dd { font-family: 'Fraunces', serif; font-size: 1.7rem; font-weight: 600; color: var(--text); }

.block { padding: 4rem 0; border-bottom: 1px solid var(--border); scroll-margin-top: 80px; }
.block.alt { background: var(--bg2); margin: 0 -50vw; padding-inline: 50vw; border-top: 1px solid var(--border); }
.eyebrow { font-size: .72rem; text-transform: uppercase; letter-spacing: .12em; color: var(--text3); font-weight: 600; margin-bottom: .6rem; }
.block h2 { font-family: 'Fraunces', serif; font-size: clamp(1.8rem, 3.5vw, 2.6rem); font-weight: 600; line-height: 1.15; letter-spacing: -.025em; margin-bottom: .9rem; }
.sub { color: var(--text2); max-width: 720px; margin-bottom: 2rem; font-size: 1rem; }
.sub strong { color: var(--text); }
.foot-note { margin-top: 1rem; color: var(--text3); font-size: .85rem; max-width: 760px; }

/* 2-col motors */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-bottom: 1.5rem; }
@media (max-width: 780px) { .two-col { grid-template-columns: 1fr; } }
.motor { padding: 1.8rem; border-radius: 14px; border: 1px solid var(--border); position: relative; }
.motor-a { background: linear-gradient(135deg, rgba(245,158,11,.08), transparent); border-color: rgba(245,158,11,.25); }
.motor-b { background: linear-gradient(135deg, rgba(99,102,241,.08), transparent); border-color: rgba(99,102,241,.25); }
.motor-n { position: absolute; top: 1rem; right: 1.2rem; font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 600; opacity: .2; line-height: 1; }
.motor h3 { font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 600; margin-bottom: .3rem; }
.motor-sub { color: var(--text3); font-size: .88rem; margin-bottom: 1rem; font-style: italic; }
.motor ul { padding-left: 1.2rem; color: var(--text2); }
.motor ul li { margin-bottom: .5rem; }
.motor strong { color: var(--text); }
.motor em { color: #fbbf24; font-style: normal; }

.thesis-punch { margin-top: 1.5rem; padding: 1.8rem 2rem; border-radius: 14px; background: radial-gradient(circle at 50% 0%, rgba(16,185,129,.15), transparent 70%), var(--bg2); border: 1px solid rgba(16,185,129,.3); }
.thesis-punch h3 { font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 600; margin-bottom: .6rem; }
.thesis-punch p { color: var(--text); font-size: 1rem; }
.thesis-punch strong { color: #34d399; }

/* TIMELINE */
.timeline { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 1rem; }
.milestone { background: var(--bg); border: 1px solid var(--border); border-radius: 14px; padding: 1.5rem 1.8rem; }
.ms-head { display: grid; grid-template-columns: auto 1fr auto; gap: 1.2rem; align-items: center; margin-bottom: 1.2rem; }
@media (max-width: 680px) { .ms-head { grid-template-columns: 1fr; } }
.ms-num { font-family: 'Fraunces', serif; font-size: 1rem; font-weight: 600; padding: .5rem .9rem; border-radius: 8px; background: linear-gradient(135deg, #818cf8, #22d3ee); color: #0b0b14; white-space: nowrap; }
.ms-head h3 { font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 600; margin-bottom: .2rem; }
.ms-goal { color: var(--text3); font-size: .9rem; }
.ms-money { text-align: right; }
.ms-money-v { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 700; color: #34d399; }
.ms-money-l { font-size: .7rem; text-transform: uppercase; letter-spacing: .08em; color: var(--text3); }

.ms-body { border-top: 1px solid var(--border); padding-top: 1.1rem; }
.ms-split { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-bottom: 1.2rem; }
@media (max-width: 680px) { .ms-split { grid-template-columns: 1fr; } }
.ms-k { font-size: .78rem; font-weight: 600; color: var(--text3); margin-bottom: .3rem; }
.ms-split p, .ms-what p { color: var(--text2); font-size: .9rem; }
.ms-what ul { margin-top: .5rem; padding-left: 1.3rem; color: var(--text); font-size: .9rem; }
.ms-what ul li { margin-bottom: .35rem; }

/* PRODUCTOS */
.prods-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.prod { padding: 1.6rem; border-radius: 14px; border: 1px solid var(--border); background: var(--bg); position: relative; }
.prod-1 { border-color: rgba(16,185,129,.35); background: linear-gradient(180deg, rgba(16,185,129,.08), transparent 60%); }
.prod-2 { border-color: rgba(99,102,241,.35); background: linear-gradient(180deg, rgba(99,102,241,.08), transparent 60%); }
.prod-3 { border-color: rgba(34,211,238,.35); background: linear-gradient(180deg, rgba(34,211,238,.08), transparent 60%); }
.prod-rank { position: absolute; top: 1rem; right: 1.2rem; font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 600; opacity: .3; line-height: 1; }
.prod h3 { font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 600; margin-bottom: .3rem; }
.prod-tag { color: var(--text2); font-size: .9rem; margin-bottom: 1rem; }
.prod-nums { display: grid; grid-template-columns: repeat(3, 1fr); gap: .4rem; padding: .8rem; background: rgba(0,0,0,.25); border-radius: 10px; margin-bottom: 1.2rem; }
.prod-nums dt { font-size: .65rem; color: var(--text3); text-transform: uppercase; letter-spacing: .06em; margin-bottom: .2rem; }
.prod-nums dd { font-size: .95rem; font-weight: 700; color: var(--text); }
.prod-nums .pos { color: #34d399; }
.prod-section { margin-top: .9rem; }
.prod-section h4 { font-size: .82rem; color: var(--text3); margin-bottom: .3rem; font-weight: 600; }
.prod-section p { color: var(--text2); font-size: .88rem; line-height: 1.55; }

.kill-list { padding: 1.8rem 2rem; border-radius: 14px; background: rgba(239,68,68,.05); border: 1px solid rgba(239,68,68,.25); }
.kill-list h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: .8rem; }
.kill-list ul { padding-left: 1.3rem; color: var(--text2); }
.kill-list ul li { margin-bottom: .35rem; font-size: .92rem; }
.kill-list strong { color: #fca5a5; }
.kill-why { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(239,68,68,.2); color: var(--text2); font-size: .9rem; }
.kill-why strong { color: var(--text); }

/* CONSULTORIA OFFERS */
.offers { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.offer { padding: 1.5rem; border-radius: 14px; background: var(--bg); border: 1px solid var(--border); }
.offer-head { display: flex; justify-content: space-between; align-items: start; gap: 1rem; margin-bottom: .8rem; }
.offer h3 { font-family: 'Fraunces', serif; font-size: 1.2rem; font-weight: 600; }
.offer-price { font-family: 'Fraunces', serif; font-size: 1.1rem; font-weight: 700; color: #34d399; white-space: nowrap; }
.offer-what { color: var(--text2); font-size: .9rem; margin-bottom: 1rem; }
.offer-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: .4rem; margin-bottom: 1rem; padding: .7rem; background: rgba(0,0,0,.2); border-radius: 8px; }
.offer-k { font-size: .65rem; color: var(--text3); text-transform: uppercase; letter-spacing: .06em; margin-bottom: .2rem; }
.offer-v { font-size: .78rem; font-weight: 600; color: var(--text); line-height: 1.3; }
.offer-upsell { padding: .7rem .9rem; background: rgba(99,102,241,.08); border-left: 2px solid var(--primary); border-radius: 6px; font-size: .85rem; color: var(--text2); }
.offer-upsell strong { color: var(--text); }

.consult-math { padding: 1.8rem 2rem; border-radius: 14px; background: var(--bg); border: 1px solid var(--border); }
.consult-math h3 { font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.2rem; }
.cm-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: .8rem; }
.cm-grid > div { padding: 1rem 1.2rem; background: rgba(255,255,255,.03); border-radius: 10px; }
.cm-grid dt { font-size: .72rem; color: var(--text3); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem; }
.cm-grid dd { font-size: 1rem; font-weight: 600; color: var(--text); }
.cm-grid .pos { color: #34d399; font-size: 1.05rem; }

/* VIVIR */
.vivir-split { padding: 1.8rem 2rem; border-radius: 14px; background: var(--bg2); border: 1px solid var(--border); margin-bottom: 1.2rem; }
.vivir-split h3 { font-family: 'Fraunces', serif; font-size: 1.25rem; font-weight: 600; margin-bottom: 1.2rem; }
.split-bars { display: flex; flex-direction: column; gap: .8rem; }
.split-bar { position: relative; padding: .9rem 1.1rem; border-radius: 10px; background: var(--bg); border: 1px solid var(--border); overflow: hidden; }
.split-bar::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: var(--w); background: color-mix(in srgb, var(--c) 15%, transparent); z-index: 0; }
.split-bar > * { position: relative; z-index: 1; }
.split-label { font-size: .9rem; margin-bottom: .3rem; color: var(--text); }
.split-label strong { color: var(--c); font-size: 1.15rem; font-weight: 800; margin-right: .4rem; font-family: 'Fraunces', serif; }
.split-bar p { color: var(--text2); font-size: .85rem; line-height: 1.5; }

.vivir-routine { padding: 1.8rem 2rem; border-radius: 14px; background: var(--bg2); border: 1px solid var(--border); margin-bottom: 1.2rem; }
.vivir-routine h3 { font-family: 'Fraunces', serif; font-size: 1.25rem; font-weight: 600; margin-bottom: 1.2rem; }
.routine-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: .5rem; }
@media (max-width: 980px) { .routine-grid { grid-template-columns: repeat(2, 1fr); } }
.routine-day { padding: .9rem; background: var(--bg); border: 1px solid var(--border); border-radius: 10px; }
.rd-day { font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: var(--text3); font-weight: 700; margin-bottom: .3rem; }
.rd-focus { font-weight: 700; font-size: .88rem; margin-bottom: .45rem; color: var(--text); }
.routine-day p { font-size: .78rem; color: var(--text2); line-height: 1.45; }
.routine-day p strong { color: var(--text); }

.guardrails { padding: 1.8rem 2rem; border-radius: 14px; background: rgba(245,158,11,.04); border: 1px solid rgba(245,158,11,.25); margin-bottom: 1.2rem; }
.guardrails h3 { font-family: 'Fraunces', serif; font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; }
.guardrails ol { padding-left: 1.3rem; display: flex; flex-direction: column; gap: .9rem; color: var(--text2); font-size: .92rem; line-height: 1.6; }
.guardrails ol li strong { color: var(--text); }

.sample-month { padding: 1.8rem 2rem; border-radius: 14px; background: linear-gradient(135deg, rgba(16,185,129,.05), transparent), var(--bg2); border: 1px solid rgba(16,185,129,.25); }
.sample-month h3 { font-family: 'Fraunces', serif; font-size: 1.25rem; font-weight: 600; margin-bottom: 1.2rem; }
.sample-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.3rem; }
@media (max-width: 680px) { .sample-grid { grid-template-columns: 1fr; } }
.sample-col { padding: 1rem 1.2rem; background: var(--bg); border: 1px solid var(--border); border-radius: 10px; }
.sample-k { font-size: .75rem; text-transform: uppercase; letter-spacing: .1em; color: var(--text3); font-weight: 700; margin-bottom: .5rem; }
.sample-row { display: flex; justify-content: space-between; padding: .35rem 0; font-size: .88rem; color: var(--text2); border-bottom: 1px dashed rgba(255,255,255,.05); }
.sample-row:last-of-type { border-bottom: none; }
.sample-row strong { color: var(--text); font-weight: 700; }
.sample-row.total { margin-top: .3rem; padding-top: .5rem; border-top: 1px solid var(--border); border-bottom: none; }
.sample-row .pos { color: #34d399; }
.sample-row .neg { color: #fca5a5; }
.sample-net { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: .6rem; padding-top: 1.2rem; border-top: 1px solid var(--border); }
.sample-net div { padding: .7rem .9rem; background: rgba(255,255,255,.03); border-radius: 8px; }
.sample-net dt { font-size: .65rem; color: var(--text3); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .25rem; }
.sample-net dd { font-size: 1rem; font-weight: 700; color: var(--text); }
.sample-net dd.pos { color: #34d399; font-family: 'Fraunces', serif; font-size: 1.15rem; }

/* CALCULADORA */
.calc { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
@media (max-width: 860px) { .calc { grid-template-columns: 1fr; } }
.calc-controls { display: flex; flex-direction: column; gap: 1.2rem; padding: 1.8rem; border-radius: 14px; background: var(--bg); border: 1px solid var(--border); }
.calc-controls label { display: flex; flex-direction: column; gap: .35rem; font-size: .85rem; color: var(--text2); font-weight: 500; position: relative; }
.calc-v { position: absolute; top: 0; right: 0; color: var(--text); font-weight: 700; font-size: .95rem; }
.calc-controls input[type=range] { width: 100%; accent-color: var(--primary); }

.calc-result { padding: 1.8rem; border-radius: 14px; background: radial-gradient(circle at 50% 0%, rgba(99,102,241,.15), transparent 70%), var(--bg2); border: 1px solid var(--border); }
.calc-big { margin-bottom: 1.3rem; padding-bottom: 1.2rem; border-bottom: 1px solid var(--border); }
.calc-big dt { font-size: .75rem; color: var(--text3); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .4rem; }
.calc-big dd { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 700; }
.calc-big dd.pos { color: #34d399; }
.calc-big dd.neg { color: #fca5a5; }
.calc-row { display: flex; justify-content: space-between; padding: .45rem 0; font-size: .9rem; color: var(--text2); border-bottom: 1px dashed rgba(255,255,255,.05); }
.calc-row:last-of-type { border-bottom: none; }
.calc-row strong { color: var(--text); font-weight: 700; }
.calc-row.highlight { margin-top: .5rem; padding-top: .7rem; border-top: 1px solid var(--border); border-bottom: none; }
.calc-row.highlight strong.pos { color: #34d399; font-size: 1rem; }
.calc-note { margin-top: 1rem; font-size: .78rem; color: var(--text3); line-height: 1.55; }
.calc-note em { color: var(--text); font-style: italic; }

/* FINALE */
.finale-block { background: linear-gradient(180deg, transparent, rgba(16,185,129,.04)); }
.regla { max-width: 720px; font-size: 1.05rem; color: var(--text2); }
.regla p { margin-bottom: 1rem; }
.regla strong { color: var(--text); }
.regla-final { font-family: 'Fraunces', serif; font-size: 1.15rem; font-style: italic; padding: 1.2rem 1.4rem; background: rgba(16,185,129,.08); border-left: 3px solid #34d399; border-radius: 6px; }
.regla-final .pos { color: #34d399; font-style: normal; font-weight: 700; }

.sources { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: .4rem; }
.sources li a { color: var(--text2); font-size: .85rem; }
.sources li a:hover { color: var(--primary); }

.foot { padding: 2rem 1.5rem; border-top: 1px solid var(--border); color: var(--text3); font-size: .85rem; }
.foot-inner { max-width: 960px; margin: 0 auto; display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.foot a { color: var(--text2); }
.foot a:hover { color: var(--primary); }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>
