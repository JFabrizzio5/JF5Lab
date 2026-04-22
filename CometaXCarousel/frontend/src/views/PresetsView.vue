<script setup>
import { useRouter, RouterLink } from 'vue-router'
import PresetGallery from '../components/PresetGallery.vue'

const router = useRouter()

function onPicked() {
  router.push('/editor')
}
</script>

<template>
  <div class="presets">
    <header>
      <RouterLink to="/" class="back">
        <i class="mdi mdi-arrow-left"></i>
        <span>CometaX Carousel</span>
      </RouterLink>
      <RouterLink to="/editor" class="btn">
        <i class="mdi mdi-pencil-ruler"></i>
        Editor en blanco
      </RouterLink>
    </header>

    <div class="hero">
      <h1>Carruseles <span class="grad">listos</span></h1>
      <p>Elige un carrusel pre-armado, cambia los textos, exporta. En 2 minutos.</p>
    </div>

    <PresetGallery @picked="onPicked" />

    <footer>
      <span>¿No encuentras lo que buscas? <RouterLink to="/editor">Empieza desde cero</RouterLink></span>
    </footer>
  </div>
</template>

<style scoped>
.presets { max-width: 1300px; margin: 0 auto; padding: 24px; }
header {
  display: flex; justify-content: space-between; align-items: center;
  padding-bottom: 24px; border-bottom: 1px solid var(--border);
}
.back { display: flex; align-items: center; gap: 10px; color: var(--text); font-weight: 700; }

.hero { text-align: center; padding: 48px 0 36px; }
.hero h1 { font-size: 56px; margin: 0; }
.grad { background: var(--grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: var(--muted); font-size: 18px; margin-top: 16px; }

footer {
  text-align: center; padding: 60px 0 30px;
  color: var(--muted); font-size: 14px; margin-top: 40px;
  border-top: 1px solid var(--border);
}

@media (max-width: 640px) {
  .hero h1 { font-size: 38px; }
  .hero p { font-size: 15px; }
}
</style>
