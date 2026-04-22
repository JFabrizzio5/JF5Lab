<script setup>
import { CAROUSEL_PRESETS } from '../presets'
import { PRESETS as PALETTES } from '../templates'
import { useCarouselStore } from '../stores/carousel'

const store = useCarouselStore()
const emit = defineEmits(['picked'])

function pick(id) {
  store.loadPreset(id)
  emit('picked', id)
}

function paletteBg(presetKey) {
  return PALETTES[presetKey]?.bg || 'var(--grad)'
}
</script>

<template>
  <div class="gallery">
    <div class="gallery-grid">
      <button v-for="p in CAROUSEL_PRESETS" :key="p.id" class="preset-card" @click="pick(p.id)">
        <div class="thumb" :style="{ background: paletteBg(p.presetKey) }">
          <div class="slides-count">
            <i class="mdi mdi-image-multiple"></i>
            {{ p.slides.length }} slides
          </div>
          <div class="thumb-deco" :style="{ background: `radial-gradient(circle at 70% 30%, ${p.thumbColor}80, transparent 60%)` }"></div>
          <div class="thumb-title">{{ p.name }}</div>
        </div>
        <div class="meta">
          <div class="name">{{ p.name }}</div>
          <div class="desc">{{ p.description }}</div>
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
}
.preset-card:hover {
  border-color: var(--accent);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.thumb {
  position: relative;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
  padding: 18px;
}
.thumb-deco {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.thumb-title {
  position: relative;
  font-size: 26px;
  font-weight: 900;
  color: #fff;
  letter-spacing: -0.5px;
  line-height: 1.1;
  text-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.slides-count {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0,0,0,0.5);
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
  font-size: 13px;
  color: var(--muted);
  line-height: 1.4;
}
</style>
