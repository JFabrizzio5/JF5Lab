<template>
  <div class="landing">
    <nav class="nav">
      <div class="nav-brand">🎪 <strong>ConventionOS</strong></div>
      <div class="nav-links">
        <router-link to="/login" class="btn btn-ghost btn-sm">Iniciar Sesión</router-link>
        <router-link to="/register" class="btn btn-primary btn-sm">Crear Convención</router-link>
      </div>
    </nav>

    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">White-Label Convention Platform</div>
        <h1 class="hero-title">Tu convención,<br><span class="gradient-text">tus reglas</span></h1>
        <p class="hero-subtitle">Crea, administra y monetiza tu convención de gaming, anime, cómics o cualquier temática. Landing page personalizada, torneos, boletos con Stripe Connect y mucho más.</p>
        <div class="hero-cta">
          <router-link to="/register" class="btn btn-primary">Crear mi convención gratis</router-link>
          <router-link to="/c/mexican-2025" class="btn btn-ghost">Ver demo: MexiCon 2025 →</router-link>
        </div>
      </div>
      <div class="hero-visual">
        <div class="floating-card card1">
          <div class="fc-icon">🎭</div>
          <div class="fc-text">Escenarios & Agenda</div>
        </div>
        <div class="floating-card card2">
          <div class="fc-icon">🏆</div>
          <div class="fc-text">Torneos integrados</div>
        </div>
        <div class="floating-card card3">
          <div class="fc-icon">💳</div>
          <div class="fc-text">Stripe Connect</div>
        </div>
        <div class="floating-card card4">
          <div class="fc-icon">🎫</div>
          <div class="fc-text">Boletos con QR</div>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="features-grid">
        <div class="feature-card" v-for="f in features" :key="f.icon">
          <div class="feature-icon">{{ f.icon }}</div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <section class="conventions-section" v-if="conventions.length">
      <h2 class="section-title">Convenciones Activas</h2>
      <div class="conventions-grid">
        <router-link :to="`/c/${c.slug}`" class="conv-card" v-for="c in conventions" :key="c.id"
          :style="`--theme: ${c.theme_color}`">
          <div class="conv-cover" :style="c.cover_url ? `background-image:url(${c.cover_url})` : ''"></div>
          <div class="conv-info">
            <img v-if="c.logo_url" :src="c.logo_url" class="conv-logo" />
            <h3>{{ c.name }}</h3>
            <p>{{ c.edition }}</p>
            <span class="conv-date" v-if="c.start_date">{{ formatDate(c.start_date) }}</span>
            <div class="conv-city" v-if="c.city">📍 {{ c.city }}</div>
          </div>
        </router-link>
      </div>
    </section>

    <footer class="footer">
      <div>© 2025 ConventionOS — Plataforma blanca para convenciones</div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'

const conventions = ref([])

const features = [
  { icon: '🎨', title: 'Landing 100% personalizable', desc: 'Colores, fuentes, logos, banners. Tu convención con tu identidad.' },
  { icon: '🎭', title: 'Escenarios & Agenda', desc: 'Múltiples escenarios con schedule por día, ponentes y transmisión en vivo.' },
  { icon: '🏪', title: 'Plano de stands', desc: 'Mapa visual de tu planta baja. Gestiona stands disponibles, reservados y vendidos.' },
  { icon: '💳', title: 'Stripe Connect', desc: 'Los pagos van directo a tu cuenta. Nosotros retenemos solo el fee de plataforma.' },
  { icon: '🏆', title: 'Torneos integrados', desc: 'Eliminations, swiss, round robin. Registros y seguimiento desde el dashboard.' },
  { icon: '🤝', title: 'Patrocinadores', desc: 'Niveles de patrocinio desde Título hasta Bronce. Exhibición prioritizada en la landing.' },
]

function formatDate(d) {
  return new Date(d).toLocaleDateString('es-MX', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/public/conventions')
    conventions.value = data
  } catch {}
})
</script>

<style scoped>
.landing { min-height: 100vh; background: var(--bg); }

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 60px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(7,7,13,0.9);
  backdrop-filter: blur(12px);
}

.nav-brand { font-size: 18px; display: flex; align-items: center; gap: 8px; }
.nav-links { display: flex; gap: 12px; }

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 100px 60px;
  align-items: center;
}

.hero-badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(124,58,237,0.15);
  border: 1px solid rgba(124,58,237,0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #a78bfa;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 20px;
}

.hero-title {
  font-size: 56px;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -1px;
}

.gradient-text {
  background: linear-gradient(135deg, #7c3aed, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 17px;
  color: var(--text2);
  line-height: 1.7;
  margin-bottom: 36px;
  max-width: 520px;
}

.hero-cta { display: flex; gap: 14px; flex-wrap: wrap; }

.hero-visual {
  position: relative;
  height: 320px;
}

.floating-card {
  position: absolute;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

.fc-icon { font-size: 24px; }
.fc-text { font-weight: 600; font-size: 14px; white-space: nowrap; }

.card1 { top: 0; left: 0; animation: float1 4s ease-in-out infinite; }
.card2 { top: 80px; right: 0; animation: float2 4.5s ease-in-out infinite; }
.card3 { bottom: 80px; left: 20px; animation: float1 5s ease-in-out infinite; }
.card4 { bottom: 0; right: 40px; animation: float2 3.5s ease-in-out infinite; }

@keyframes float1 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
@keyframes float2 { 0%,100%{transform:translateY(-6px)} 50%{transform:translateY(6px)} }

.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.feature-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
  transition: border-color 0.2s;
}
.feature-card:hover { border-color: var(--primary); }
.feature-icon { font-size: 28px; margin-bottom: 12px; }
.feature-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.feature-card p { font-size: 14px; color: var(--text2); line-height: 1.6; }

.conventions-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 60px 60px;
}

.section-title { font-size: 24px; font-weight: 800; margin-bottom: 24px; }

.conventions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.conv-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  transition: transform 0.2s, border-color 0.2s;
  text-decoration: none;
  color: inherit;
}
.conv-card:hover { transform: translateY(-3px); border-color: var(--theme, var(--primary)); }

.conv-cover {
  height: 140px;
  background: linear-gradient(135deg, #1a1a2e, #0f0f1a);
  background-size: cover;
  background-position: center;
}

.conv-info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.conv-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  margin-bottom: 4px;
  border: 2px solid var(--border);
}

.conv-info h3 { font-size: 16px; font-weight: 700; }
.conv-info p { font-size: 12px; color: var(--text2); }
.conv-date { font-size: 12px; color: var(--accent); font-weight: 600; }
.conv-city { font-size: 12px; color: var(--text2); }

.footer {
  border-top: 1px solid var(--border);
  text-align: center;
  padding: 24px;
  font-size: 13px;
  color: var(--text2);
}
</style>
