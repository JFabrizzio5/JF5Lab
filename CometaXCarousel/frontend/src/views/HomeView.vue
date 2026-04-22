<script setup>
import { RouterLink } from 'vue-router'
import PresetGallery from '../components/PresetGallery.vue'
</script>

<template>
  <div class="home">
    <header>
      <div class="logo">
        <div class="logo-mark">
          <svg width="28" height="28" viewBox="0 0 32 32">
            <circle cx="22" cy="10" r="3.2" fill="#fff" />
            <path d="M19.6 12.4 L8 24" stroke="#fff" stroke-width="2.6" stroke-linecap="round" />
            <path d="M17 14 L7 22" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity="0.55" />
          </svg>
        </div>
        <div>
          <h1>CometaX Carousel</h1>
          <p>Carruseles Instagram en minutos</p>
        </div>
      </div>
      <nav>
        <RouterLink to="/presets" class="link">Plantillas</RouterLink>
        <RouterLink to="/pricing" class="link">Planes</RouterLink>
        <RouterLink to="/editor" class="btn btn-primary">
          <i class="mdi mdi-rocket-launch"></i>
          Empezar gratis
        </RouterLink>
      </nav>
    </header>

    <section class="hero">
      <div class="badge">CometaX · Sin login · 100% en tu navegador</div>
      <h2>Diseña carruseles que <span class="grad">brillan</span> como un cometa</h2>
      <p>10 plantillas SVG editables, 5 paletas listas, export PNG/ZIP en un clic. Sin watermarks, sin cuentas, sin pagar para empezar.</p>
      <div class="cta-row">
        <RouterLink to="/presets" class="btn btn-primary big">
          <i class="mdi mdi-view-dashboard"></i>
          Ver carruseles listos
        </RouterLink>
        <RouterLink to="/editor" class="btn big">
          <i class="mdi mdi-pencil-ruler"></i>
          Editor en blanco
        </RouterLink>
      </div>
      <div class="stat-row">
        <div><strong>10</strong> plantillas</div>
        <div><strong>5</strong> paletas</div>
        <div><strong>3</strong> tamaños IG</div>
        <div><strong>0</strong> watermarks</div>
      </div>
    </section>

    <section class="presets-section">
      <div class="section-head">
        <div>
          <h2>Carruseles <span class="grad">listos para editar</span></h2>
          <p>12 plantillas con copy real y paleta sugerida. Edita los textos y exporta PNG.</p>
        </div>
        <RouterLink to="/presets" class="btn">Ver todos</RouterLink>
      </div>
      <PresetGallery @picked="$router.push('/editor')" />
    </section>

    <section class="features">
      <div class="feat">
        <i class="mdi mdi-lightning-bolt"></i>
        <h3>Setup cero</h3>
        <p>Abres el editor y diseñas. Nada que instalar, nada que configurar.</p>
      </div>
      <div class="feat">
        <i class="mdi mdi-palette-swatch"></i>
        <h3>Marca consistente</h3>
        <p>Sube tu logo y aplica colores a todos los slides en un toque.</p>
      </div>
      <div class="feat">
        <i class="mdi mdi-folder-zip"></i>
        <h3>Export ZIP</h3>
        <p>Descarga el carrusel completo numerado y listo para subir.</p>
      </div>
      <div class="feat">
        <i class="mdi mdi-shield-lock"></i>
        <h3>Privado</h3>
        <p>Todo corre en tu navegador. Tus diseños no se suben a ningún servidor.</p>
      </div>
    </section>

    <footer>
      <span>Parte del ecosistema <a href="http://62.72.3.139:8888">CometaX</a></span>
    </footer>
  </div>
</template>

<style scoped>
.home { max-width: 1200px; margin: 0 auto; padding: 24px; }
header {
  display: flex; justify-content: space-between; align-items: center;
  padding-bottom: 24px; border-bottom: 1px solid var(--border);
}
.logo { display: flex; align-items: center; gap: 14px; }
.logo-mark {
  width: 44px; height: 44px; border-radius: 11px;
  background: var(--grad); display: grid; place-items: center;
}
.logo h1 { margin: 0; font-size: 20px; letter-spacing: 0.3px; }
.logo p { margin: 0; font-size: 12px; color: var(--muted); }
nav { display: flex; align-items: center; gap: 14px; }
.link { color: var(--muted); font-weight: 600; }
.link:hover { color: var(--text); }

.hero { padding: 80px 0 60px; text-align: center; max-width: 820px; margin: 0 auto; }
.badge {
  display: inline-block; font-size: 12px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
  color: var(--accent); background: rgba(129, 140, 248, 0.12);
  padding: 6px 14px; border-radius: 999px; margin-bottom: 24px;
}
.hero h2 { font-size: 64px; line-height: 1.05; margin: 0; }
.grad { background: var(--grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { font-size: 20px; color: var(--muted); margin-top: 24px; line-height: 1.5; }
.cta-row { display: flex; gap: 14px; justify-content: center; margin-top: 36px; flex-wrap: wrap; }
.big { padding: 14px 28px; font-size: 16px; }
.stat-row {
  display: flex; gap: 36px; justify-content: center; margin-top: 60px;
  flex-wrap: wrap; color: var(--muted); font-size: 14px;
}
.stat-row strong { color: var(--text); font-size: 28px; display: block; }

.presets-section { margin: 80px 0; }
.section-head {
  display: flex; justify-content: space-between; align-items: end;
  margin-bottom: 28px; gap: 20px; flex-wrap: wrap;
}
.section-head h2 { margin: 0; font-size: 36px; line-height: 1.1; }
.section-head p { margin: 8px 0 0; color: var(--muted); font-size: 16px; }

.features {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px; margin: 80px 0;
}
.feat {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 14px; padding: 24px;
}
.feat i { font-size: 28px; color: var(--accent); }
.feat h3 { margin: 12px 0 6px; font-size: 18px; }
.feat p { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.5; }

footer {
  text-align: center; padding: 40px 0 20px;
  color: var(--muted); font-size: 13px; border-top: 1px solid var(--border);
}

@media (max-width: 640px) {
  .hero h2 { font-size: 42px; }
  .hero p { font-size: 16px; }
}
</style>
