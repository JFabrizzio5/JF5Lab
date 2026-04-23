<script setup>
import { computed } from 'vue'
import { useCarouselStore } from '../stores/carousel'

const props = defineProps({
  slide: { type: Object, required: true },
  scale: { type: Number, default: 1 },
  exportMode: { type: Boolean, default: false },
  presetOverride: { type: Object, default: null },
  sizeOverride: { type: Object, default: null }
})

const store = useCarouselStore()
const size = computed(() => props.sizeOverride || store.size)
const preset = computed(() => props.presetOverride || store.preset)

function colorToken(c) {
  if (!c) return 'inherit'
  if (preset.value[c]) return preset.value[c]
  return c
}

function pos(layer) {
  const align = layer.align || 'left'
  const w = layer.w ?? null
  const style = {
    position: 'absolute',
    top: `${layer.y}%`
  }
  if (align === 'center') {
    style.left = `${layer.x}%`
    style.transform = 'translate(-50%, -50%)'
    if (w) style.width = `${w}%`
    style.textAlign = 'center'
  } else if (align === 'right') {
    style.right = `${100 - layer.x}%`
    style.transform = 'translateY(-50%)'
    if (w) style.width = `${w}%`
    style.textAlign = 'right'
  } else {
    style.left = `${layer.x}%`
    style.transform = 'translateY(-50%)'
    if (w) style.width = `${w}%`
  }
  return style
}

function fontStack(font) {
  if (font === 'mono') return '"SF Mono", "JetBrains Mono", Consolas, monospace'
  if (font === 'serif') return 'Georgia, "Times New Roman", serif'
  return '-apple-system, "Inter", "Segoe UI", Roboto, sans-serif'
}
</script>

<template>
  <div
    class="slide-canvas"
    :style="{
      width: size.w * scale + 'px',
      height: size.h * scale + 'px',
      background: preset.bg
    }"
  >
    <div class="slide-inner" :style="{ width: size.w + 'px', height: size.h + 'px', transform: `scale(${scale})` }">
      <template v-for="(layer, i) in slide.layers" :key="i">
        <div v-if="layer.type === 'text'" :style="{ ...pos(layer), fontSize: layer.size + 'px', fontWeight: layer.weight, color: colorToken(layer.color), fontFamily: fontStack(layer.font), lineHeight: 1.15, whiteSpace: 'pre-line', letterSpacing: layer.tracking || 'normal' }">{{ layer.text }}</div>

        <div v-else-if="layer.type === 'icon'" :style="{ ...pos(layer), color: colorToken(layer.color), fontSize: layer.size + 'px', lineHeight: 1 }">
          <i :class="['mdi', layer.icon]"></i>
        </div>

        <div v-else-if="layer.type === 'badge'" :style="{ ...pos(layer), background: colorToken(layer.color), color: '#fff', padding: '8px 18px', borderRadius: '999px', fontSize: '22px', fontWeight: 800, letterSpacing: '2px', display: 'inline-block' }">{{ layer.text }}</div>

        <div v-else-if="layer.type === 'icon-list'" :style="{ ...pos(layer), display: 'flex', flexDirection: 'column', gap: layer.gap + '%' }">
          <div v-for="(it, j) in layer.items" :key="j" style="display:flex; align-items:center; gap:24px;">
            <i :class="['mdi', it.icon]" :style="{ fontSize: layer.size * 1.6 + 'px', color: colorToken(layer.accent) }"></i>
            <span :style="{ fontSize: layer.size + 'px', color: colorToken(layer.color), fontWeight: 600 }">{{ it.text }}</span>
          </div>
        </div>

        <div v-else-if="layer.type === 'code-block'" :style="{ ...pos(layer), background: 'rgba(0,0,0,0.55)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '20px', padding: '36px 40px', fontFamily: fontStack('mono'), fontSize: layer.size + 'px', color: '#e2e8f0', lineHeight: 1.5, whiteSpace: 'pre' }">{{ layer.code }}</div>

        <div v-else-if="layer.type === 'progress-dots'" :style="{ ...pos(layer), display: 'flex', gap: '14px' }">
          <span v-for="i in layer.count" :key="i" :style="{ width: '24px', height: '8px', borderRadius: '4px', background: i - 1 <= layer.active ? colorToken('accent') : colorToken('muted'), opacity: i - 1 <= layer.active ? 1 : 0.3 }"></span>
        </div>

        <div v-else-if="layer.type === 'gradient-blob'" :style="{ ...pos(layer), width: layer.size + '%', aspectRatio: '1', borderRadius: '50%', background: `radial-gradient(circle, ${preset.accent2}, transparent 70%)`, opacity: layer.opacity, filter: 'blur(40px)', pointerEvents: 'none' }"></div>

        <svg v-else-if="layer.type === 'comet-trail'" :style="{ ...pos(layer), width: layer.size + '%', aspectRatio: '1', opacity: layer.opacity }" viewBox="0 0 100 100">
          <defs>
            <linearGradient :id="`ct-${i}`" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0" :stop-color="preset.accent" />
              <stop offset="1" :stop-color="preset.accent2" />
            </linearGradient>
          </defs>
          <circle cx="78" cy="22" r="10" :fill="`url(#ct-${i})`" />
          <path d="M70 30 L20 80" :stroke="`url(#ct-${i})`" stroke-width="6" stroke-linecap="round" />
          <path d="M64 28 L18 70" :stroke="preset.accent2" stroke-width="3" stroke-linecap="round" opacity="0.5" />
          <path d="M58 26 L16 60" :stroke="preset.accent" stroke-width="2" stroke-linecap="round" opacity="0.3" />
        </svg>

        <div v-else-if="layer.type === 'split'" :style="{ ...pos(layer), width: '90%', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }">
          <div style="background:rgba(0,0,0,0.3); border-radius:20px; padding:40px;">
            <div :style="{ color: colorToken('muted'), fontSize: '24px', fontWeight: 800, letterSpacing: '3px', marginBottom: '24px' }">{{ layer.leftLabel }}</div>
            <div v-for="(it, j) in layer.leftItems" :key="j" :style="{ color: colorToken('text'), fontSize: '32px', marginBottom: '16px', opacity: 0.8 }">— {{ it }}</div>
          </div>
          <div :style="{ background: `linear-gradient(135deg, ${preset.accent}30, ${preset.accent2}30)`, border: `2px solid ${preset.accent}`, borderRadius: '20px', padding: '40px' }">
            <div :style="{ color: colorToken('accent'), fontSize: '24px', fontWeight: 800, letterSpacing: '3px', marginBottom: '24px' }">{{ layer.rightLabel }}</div>
            <div v-for="(it, j) in layer.rightItems" :key="j" :style="{ color: colorToken('text'), fontSize: '32px', marginBottom: '16px', fontWeight: 600 }">+ {{ it }}</div>
          </div>
        </div>

        <div v-else-if="layer.type === 'avatar'" :style="{ ...pos(layer), width: layer.size + 'px', height: layer.size + 'px', borderRadius: '50%', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: layer.size * 0.5 + 'px', color: '#fff', fontWeight: 700 }">M</div>

        <div v-else-if="layer.type === 'logo'" :style="pos(layer)">
          <div v-if="store.logoDataUrl" :style="{ display: 'flex', alignItems: 'center', gap: '14px' }">
            <img :src="store.logoDataUrl" :style="{ height: layer.size + 'px', width: 'auto' }" />
          </div>
          <div v-else :style="{ display: 'flex', alignItems: 'center', gap: '14px' }">
            <div :style="{ width: layer.size + 'px', height: layer.size + 'px', borderRadius: layer.size * 0.25 + 'px', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, display: 'flex', alignItems: 'center', justifyContent: 'center' }">
              <svg :width="layer.size * 0.6" :height="layer.size * 0.6" viewBox="0 0 32 32">
                <circle cx="22" cy="10" r="3.2" fill="#fff" />
                <path d="M19.6 12.4 L8 24" stroke="#fff" stroke-width="2.6" stroke-linecap="round" opacity="0.9" />
              </svg>
            </div>
            <span :style="{ fontSize: layer.size * 0.6 + 'px', fontWeight: 700, color: colorToken('text') }">{{ store.logoText }}</span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.slide-canvas {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
}
.slide-inner {
  position: absolute;
  top: 0;
  left: 0;
  transform-origin: top left;
}
</style>
