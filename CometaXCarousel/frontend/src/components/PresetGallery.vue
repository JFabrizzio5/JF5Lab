<script setup>
import { CAROUSEL_PRESETS } from '../presets'
import { PRESETS as PALETTES, SIZES } from '../templates'
import { useCarouselStore } from '../stores/carousel'
import SlideCanvas from './SlideCanvas.vue'

const store = useCarouselStore()
const emit = defineEmits(['picked'])

function pick(id) {
  store.loadPreset(id)
  emit('picked', id)
}

function presetData(p) {
  return PALETTES[p.presetKey]
}
function sizeData(p) {
  return SIZES[p.sizeKey]
}

// Escala miniatura: cabe ~240px de ancho
function thumbScale(p) {
  return 240 / sizeData(p).w
}
</script>

<template>
  <div class="gallery">
    <div class="gallery-grid">
      <button type="button" v-for="p in CAROUSEL_PRESETS" :key="p.id" class="preset-card" @click="pick(p.id)">
        <div class="thumb-wrap">
          <div class="mini-render">
            <SlideCanvas
              :slide="p.slides[0]"
              :scale="thumbScale(p)"
              :preset-override="presetData(p)"
              :size-override="sizeData(p)"
            />
          </div>
          <div class="slides-count">
            <i class="mdi mdi-image-multiple"></i>
            {{ p.slides.length }}
          </div>
        </div>
        <div class="meta">
          <div class="name">{{ p.name }}</div>
          <div class="desc">{{ p.description }}</div>
          <div class="cta">
            <i class="mdi mdi-cursor-default-click"></i>
            Click para cargar
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}
.preset-card {
  display: flex;
  flex-direction: column;
  text-align: left;
  padding: 0;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.18s;
  cursor: pointer;
}
.preset-card:hover {
  border-color: var(--accent);
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.4);
}
.thumb-wrap {
  position: relative;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  background: var(--bg-2);
  display: grid;
  place-items: center;
  padding: 8px;
}
.mini-render {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  overflow: hidden;
}
.mini-render :deep(.slide-canvas) {
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.slides-count {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0,0,0,0.7);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  backdrop-filter: blur(8px);
}
.meta {
  padding: 14px 16px 16px;
}
.name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}
.desc {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.4;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.cta {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 700;
  color: var(--accent);
}
.preset-card:hover .cta { color: var(--accent-2); }
</style>
