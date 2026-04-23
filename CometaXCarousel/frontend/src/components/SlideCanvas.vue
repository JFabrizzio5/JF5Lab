<script setup>
import { computed, ref } from 'vue'
import { useCarouselStore } from '../stores/carousel'

const props = defineProps({
  slide: { type: Object, required: true },
  scale: { type: Number, default: 1 },
  exportMode: { type: Boolean, default: false },
  presetOverride: { type: Object, default: null },
  sizeOverride: { type: Object, default: null },
  interactive: { type: Boolean, default: false }
})

const store = useCarouselStore()
const size = computed(() => props.sizeOverride || store.size)
const preset = computed(() => props.presetOverride || store.preset)

const slideBg = computed(() => {
  if (!props.interactive) return preset.value.bg
  if (store.customBgImage) {
    return `url("${store.customBgImage}") center/cover no-repeat`
  }
  return store.customBg || preset.value.bg
})

// Drag state
const dragState = ref(null)

function onLayerClick(e, layerIdx) {
  if (!props.interactive) return
  e.stopPropagation()
  store.selectLayer(layerIdx)
}

function onLayerDown(e, layerIdx) {
  if (!props.interactive) return
  if (e.button !== 0) return
  e.stopPropagation()
  store.selectLayer(layerIdx)
  const layer = props.slide.layers[layerIdx]
  if (!hasMovableXY(layer)) return
  const startX = e.clientX
  const startY = e.clientY
  const startLX = layer.x ?? 50
  const startLY = layer.y ?? 50
  const slideEl = e.currentTarget.closest('.slide-canvas')
  const rect = slideEl.getBoundingClientRect()
  dragState.value = { layerIdx, startX, startY, startLX, startLY, rectW: rect.width, rectH: rect.height }
  window.addEventListener('mousemove', onDragMove)
  window.addEventListener('mouseup', onDragEnd, { once: true })
}

function onDragMove(e) {
  if (!dragState.value) return
  const d = dragState.value
  const dx = ((e.clientX - d.startX) / d.rectW) * 100
  const dy = ((e.clientY - d.startY) / d.rectH) * 100
  const nx = Math.max(0, Math.min(100, d.startLX + dx))
  const ny = Math.max(0, Math.min(100, d.startLY + dy))
  store.updateLayer(store.activeIndex, d.layerIdx, { x: nx, y: ny })
}

function onDragEnd() {
  dragState.value = null
  window.removeEventListener('mousemove', onDragMove)
}

function hasMovableXY(l) {
  return !['half-split', 'gradient-overlay', 'dots-pattern', 'grid-pattern', 'blur-image', 'wave-top', 'wave-bottom', 'shine-line', 'photo-bg'].includes(l.type)
}

function onCanvasClick() {
  if (!props.interactive) return
  store.deselectLayer()
}

function isSelected(idx) {
  return props.interactive && store.selectedLayerIdx === idx
}

function selectionRect(layer) {
  const align = layer.align || 'left'
  const style = {
    position: 'absolute',
    border: '2px dashed var(--accent)',
    borderRadius: '6px',
    padding: '6px',
    pointerEvents: 'none',
    transition: 'all 0.05s'
  }
  if (align === 'center') {
    style.top = `${layer.y || 50}%`
    style.left = `${layer.x || 50}%`
    style.transform = 'translate(-50%, -50%)'
  } else if (align === 'right') {
    style.top = `${layer.y || 50}%`
    style.right = `${100 - (layer.x || 50)}%`
    style.transform = 'translateY(-50%)'
  } else {
    style.top = `${layer.y || 50}%`
    style.left = `${layer.x || 50}%`
    style.transform = 'translateY(-50%)'
  }
  if (layer.size) {
    style.minWidth = layer.size + 'px'
    style.minHeight = layer.size + 'px'
  } else {
    style.minWidth = '40px'
    style.minHeight = '40px'
  }
  return style
}

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

// Curated Unsplash photo IDs (CORS-friendly via images.unsplash.com)
const CURATED_PHOTOS = {
  office: ['1497366216548-37526070297c', '1521737711867-e3b97375f902', '1556761175-5973dc0f32e7', '1497032628192-86f99bcd76bc'],
  workspace: ['1499750310107-5fef28a66643', '1517245386807-bb43f82c33c4', '1531403009284-440f080d1e12'],
  team: ['1522071820081-009f0129c71c', '1542744173-8e7e53415bb0', '1552664730-d307ca884978'],
  portrait: ['1494790108377-be9c29b29330', '1500648767791-00dcc994a43e', '1506794778202-cad84cf45f1d', '1573496359142-b8d87734a5a2'],
  woman: ['1494790108377-be9c29b29330', '1438761681033-6461ffad8d80', '1517841905240-472988babdf9'],
  man: ['1500648767791-00dcc994a43e', '1506794778202-cad84cf45f1d', '1472099645785-5658abf4ff4e'],
  product: ['1505740420928-5e560c06d30e', '1572569511254-d8f925fe2cbb', '1523275335684-37898b6baf30'],
  abstract: ['1557672172-298e090bd0f1', '1558591710-4b4a1ae0f04d', '1614851099175-e5b30eb6f696'],
  gradient: ['1557682250-33bd709cbe85', '1557682224-5b8590cd9ec5', '1557682268-edc7d68d8d9d'],
  mountain: ['1469474968028-56623f02e42e', '1464822759023-fed622ff2c3b', '1486870591958-9b9d0d1dda99'],
  sunset: ['1502082553048-f009c37129b9', '1495567720989-cebdbdd97913', '1506905925346-21bda4d32df4'],
  food: ['1565299624946-b28f40a0ae38', '1567620905732-2d1ec7ab7445', '1546069901-ba9599a7e63c'],
  laptop: ['1496181133206-80ce9b88a853', '1517694712202-14dd9538aa97', '1498050108023-c5249f4df085']
}

function pickCurated(query, seed) {
  const keys = (query || '').split(/[\s,]+/).filter(Boolean)
  for (const k of keys) {
    const list = CURATED_PHOTOS[k.toLowerCase()]
    if (list) return list[(seed || 0) % list.length]
  }
  // fallback first key
  const flat = Object.values(CURATED_PHOTOS).flat()
  return flat[(seed || 1) % flat.length]
}

function photoSrc(layer) {
  if (layer.src) return layer.src
  if (layer.unsplashId) return `https://images.unsplash.com/photo-${layer.unsplashId}?w=1080&h=1350&fit=crop&q=80`
  if (layer.query) {
    const id = pickCurated(layer.query, layer.seed)
    return `https://images.unsplash.com/photo-${id}?w=1080&h=1350&fit=crop&q=80`
  }
  if (layer.pravatar) return `https://i.pravatar.cc/600?img=${layer.pravatar}`
  return `https://picsum.photos/seed/${layer.seed || 'cometax'}/1080/1350`
}

function placeholderIcon(p) {
  const map = {
    phone: 'mdi-cellphone',
    laptop: 'mdi-laptop',
    card: 'mdi-credit-card',
    avatar: 'mdi-account-circle',
    photo: 'mdi-image',
    food: 'mdi-food',
    product: 'mdi-package-variant',
    chart: 'mdi-chart-line'
  }
  return map[p] || 'mdi-image-outline'
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
    :class="{ interactive }"
    :style="{
      width: size.w * scale + 'px',
      height: size.h * scale + 'px',
      background: slideBg
    }"
    @click="onCanvasClick"
  >
    <div v-if="interactive && store.customBgImage && store.customBgBlur" :style="{ position: 'absolute', inset: 0, background: `url('${store.customBgImage}') center/cover no-repeat`, filter: `blur(${store.customBgBlur}px)`, transform: 'scale(1.1)', pointerEvents: 'none' }"></div>
    <div class="slide-inner" :style="{ width: size.w + 'px', height: size.h + 'px', transform: `scale(${scale})` }">
      <template v-for="(layer, i) in slide.layers" :key="i">
        <div v-if="isSelected(i)" :style="{ ...selectionRect(layer), pointerEvents: 'none' }" class="selection-outline"></div>
        <div v-if="layer.type === 'text'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), fontSize: layer.size + 'px', fontWeight: layer.weight, color: colorToken(layer.color), fontFamily: fontStack(layer.font), lineHeight: layer.lineHeight || 1.15, whiteSpace: 'pre-line', letterSpacing: layer.tracking || 'normal', wordBreak: 'break-word', overflowWrap: 'break-word', maxWidth: layer.w ? layer.w + '%' : (layer.align === 'center' ? '90%' : '92%') }">{{ layer.text }}</div>

        <div v-else-if="layer.type === 'icon'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), color: colorToken(layer.color), fontSize: layer.size + 'px', lineHeight: 1 }">
          <i :class="['mdi', layer.icon]"></i>
        </div>

        <div v-else-if="layer.type === 'badge'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), background: colorToken(layer.color), color: '#fff', padding: '8px 18px', borderRadius: '999px', fontSize: '22px', fontWeight: 800, letterSpacing: '2px', display: 'inline-block' }">{{ layer.text }}</div>

        <div v-else-if="layer.type === 'icon-list'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), display: 'flex', flexDirection: 'column', gap: (layer.gap || 7) + '%' }">
          <div v-for="(it, j) in layer.items" :key="j" style="display:flex; align-items:center; gap:24px;">
            <i :class="['mdi', it.icon]" :style="{ fontSize: layer.size * 1.6 + 'px', color: colorToken(layer.accent) }"></i>
            <span :style="{ fontSize: layer.size + 'px', color: colorToken(layer.color), fontWeight: 600 }">{{ it.text }}</span>
          </div>
        </div>

        <div v-else-if="layer.type === 'code-block'" :style="{ ...pos(layer), background: 'rgba(0,0,0,0.6)', border: `1px solid ${preset.accent}30`, borderRadius: '20px', padding: '36px 40px', fontFamily: fontStack('mono'), fontSize: layer.size + 'px', color: '#e2e8f0', lineHeight: 1.5, whiteSpace: 'pre-wrap', wordBreak: 'break-word', overflow: 'hidden', maxWidth: (layer.w || 84) + '%', boxShadow: `0 12px 40px ${preset.accent}20` }">
          <div :style="{ display: 'flex', gap: '8px', marginBottom: '20px' }">
            <span :style="{ width: '14px', height: '14px', borderRadius: '50%', background: '#ff5f57' }"></span>
            <span :style="{ width: '14px', height: '14px', borderRadius: '50%', background: '#febc2e' }"></span>
            <span :style="{ width: '14px', height: '14px', borderRadius: '50%', background: '#28c840' }"></span>
          </div>
          <div>{{ layer.code }}</div>
        </div>

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

        <div v-else-if="layer.type === 'split'" :style="{ ...pos(layer), width: '88%', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }">
          <div :style="{ background: 'rgba(0,0,0,0.35)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '20px', padding: '32px 24px', minHeight: '280px' }">
            <div :style="{ color: colorToken('muted'), fontSize: '20px', fontWeight: 800, letterSpacing: '3px', marginBottom: '20px' }">{{ layer.leftLabel }}</div>
            <div v-for="(it, j) in layer.leftItems" :key="j" :style="{ color: colorToken('text'), fontSize: (layer.itemSize || 26) + 'px', marginBottom: '14px', opacity: 0.75, lineHeight: 1.3, wordBreak: 'break-word' }">— {{ it }}</div>
          </div>
          <div :style="{ background: `linear-gradient(135deg, ${preset.accent}20, ${preset.accent2}20)`, border: `2px solid ${preset.accent}`, borderRadius: '20px', padding: '32px 24px', minHeight: '280px', boxShadow: `0 12px 40px ${preset.accent}30` }">
            <div :style="{ color: colorToken('accent'), fontSize: '20px', fontWeight: 800, letterSpacing: '3px', marginBottom: '20px' }">{{ layer.rightLabel }}</div>
            <div v-for="(it, j) in layer.rightItems" :key="j" :style="{ color: colorToken('text'), fontSize: (layer.itemSize || 26) + 'px', marginBottom: '14px', fontWeight: 600, lineHeight: 1.3, wordBreak: 'break-word' }">+ {{ it }}</div>
          </div>
        </div>

        <div v-else-if="layer.type === 'avatar'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), width: layer.size + 'px', height: layer.size + 'px', borderRadius: '50%', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: layer.size * 0.5 + 'px', color: '#fff', fontWeight: 700, overflow: 'hidden' }">
          <img v-if="layer.src" :src="layer.src" style="width:100%; height:100%; object-fit:cover;" />
          <span v-else>{{ layer.initial || 'M' }}</span>
        </div>

        <div v-else-if="layer.type === 'image'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), width: (layer.w || 50) + '%', aspectRatio: layer.aspect || '1 / 1', borderRadius: (layer.radius ?? 16) + 'px', overflow: 'hidden', background: 'rgba(255,255,255,0.05)', border: layer.bordered ? `2px solid ${preset.accent}40` : 'none' }">
          <img v-if="layer.src" :src="layer.src" :style="{ width: '100%', height: '100%', objectFit: layer.fit || 'cover', display: 'block' }" />
          <div v-else :style="{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, position: 'relative' }">
            <i :class="['mdi', placeholderIcon(layer.placeholder)]" :style="{ fontSize: '120px', color: '#fff', opacity: 0.85 }"></i>
            <span :style="{ position: 'absolute', bottom: '12px', left: '50%', transform: 'translateX(-50%)', fontSize: '14px', fontWeight: 700, color: '#fff', opacity: 0.7, letterSpacing: '1px', textTransform: 'uppercase' }">{{ layer.label || 'Imagen' }}</span>
          </div>
        </div>

        <svg v-else-if="layer.type === 'sparkle'" :style="{ ...pos(layer), width: (layer.size || 60) + 'px', height: (layer.size || 60) + 'px', overflow: 'visible' }" viewBox="0 0 100 100">
          <path d="M50 0 L55 45 L100 50 L55 55 L50 100 L45 55 L0 50 L45 45 Z" :fill="colorToken(layer.color || 'accent')" />
        </svg>

        <div v-else-if="layer.type === 'corner-shape'" :style="{ ...pos(layer), width: (layer.size || 200) + 'px', height: (layer.size || 200) + 'px', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, borderRadius: layer.shape === 'circle' ? '50%' : '24px', opacity: layer.opacity || 0.15, transform: 'translate(-50%,-50%) rotate(' + (layer.rotate || 0) + 'deg)' }"></div>

        <div v-else-if="layer.type === 'logo'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="pos(layer)">
          <div :style="{ display: 'flex', alignItems: 'center', gap: '14px' }">
            <img v-if="layer.brand" :src="`/logos/${layer.brand}.svg`" :style="{ height: layer.size + 'px', width: layer.size + 'px' }" />
            <img v-else-if="store.logoDataUrl" :src="store.logoDataUrl" :style="{ height: layer.size + 'px', width: 'auto' }" />
            <div v-else :style="{ width: layer.size + 'px', height: layer.size + 'px', borderRadius: layer.size * 0.25 + 'px', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, display: 'flex', alignItems: 'center', justifyContent: 'center' }">
              <svg :width="layer.size * 0.6" :height="layer.size * 0.6" viewBox="0 0 32 32">
                <circle cx="22" cy="10" r="3.2" fill="#fff" />
                <path d="M19.6 12.4 L8 24" stroke="#fff" stroke-width="2.6" stroke-linecap="round" opacity="0.9" />
              </svg>
            </div>
            <span v-if="!layer.hideText" :style="{ fontSize: layer.size * 0.6 + 'px', fontWeight: 700, color: colorToken(layer.color || 'text') }">{{ layer.text || store.logoText }}</span>
          </div>
        </div>

        <svg v-else-if="layer.type === 'wave-bottom'" :style="{ position: 'absolute', left: 0, right: 0, bottom: 0, width: '100%', height: (layer.h || 30) + '%', pointerEvents: 'none' }" preserveAspectRatio="none" viewBox="0 0 100 100">
          <defs><linearGradient :id="`wb-${i}`" x1="0" x2="0" y1="0" y2="1"><stop offset="0" :stop-color="preset.accent" :stop-opacity="layer.opacity || 0.7"/><stop offset="1" :stop-color="preset.accent2" :stop-opacity="(layer.opacity || 0.7) * 0.8"/></linearGradient></defs>
          <path :d="layer.variant === 'soft' ? 'M0,60 Q25,30 50,55 T100,50 L100,100 L0,100 Z' : 'M0,40 Q25,80 50,40 T100,40 L100,100 L0,100 Z'" :fill="`url(#wb-${i})`" />
        </svg>

        <svg v-else-if="layer.type === 'wave-top'" :style="{ position: 'absolute', left: 0, right: 0, top: 0, width: '100%', height: (layer.h || 30) + '%', pointerEvents: 'none' }" preserveAspectRatio="none" viewBox="0 0 100 100">
          <defs><linearGradient :id="`wt-${i}`" x1="0" x2="0" y1="0" y2="1"><stop offset="0" :stop-color="preset.accent2" :stop-opacity="layer.opacity || 0.7"/><stop offset="1" :stop-color="preset.accent" :stop-opacity="0"/></linearGradient></defs>
          <path d="M0,0 L100,0 L100,60 Q75,20 50,50 T0,40 Z" :fill="`url(#wt-${i})`" />
        </svg>

        <div v-else-if="layer.type === 'half-split'" :style="{ position: 'absolute', inset: 0, background: `linear-gradient(${layer.angle || 90}deg, ${layer.colorA || preset.accent} 50%, ${layer.colorB || preset.accent2} 50%)`, opacity: layer.opacity || 1, pointerEvents: 'none' }"></div>

        <div v-else-if="layer.type === 'gradient-overlay'" :style="{ position: 'absolute', inset: 0, background: `linear-gradient(${layer.angle || 180}deg, ${preset.accent}cc 0%, transparent 60%)`, pointerEvents: 'none' }"></div>

        <div v-else-if="layer.type === 'diagonal-band'" :style="{ position: 'absolute', left: '-10%', right: '-10%', top: (layer.y || 50) + '%', height: (layer.h || 12) + '%', background: `linear-gradient(90deg, ${preset.accent}, ${preset.accent2})`, transform: `translateY(-50%) rotate(${layer.angle || -8}deg)`, opacity: layer.opacity || 0.9, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', pointerEvents: 'none' }">
          <span v-if="layer.text" :style="{ color: '#fff', fontSize: (layer.fontSize || 28) + 'px', fontWeight: 800, letterSpacing: '4px', textTransform: 'uppercase', whiteSpace: 'nowrap' }">{{ layer.text }} · {{ layer.text }} · {{ layer.text }}</span>
        </div>

        <div v-else-if="layer.type === 'dots-pattern'" :style="{ position: 'absolute', inset: 0, opacity: layer.opacity || 0.18, pointerEvents: 'none', backgroundImage: `radial-gradient(${preset.accent} 1.5px, transparent 1.5px)`, backgroundSize: (layer.gap || 24) + 'px ' + (layer.gap || 24) + 'px' }"></div>

        <div v-else-if="layer.type === 'grid-pattern'" :style="{ position: 'absolute', inset: 0, opacity: layer.opacity || 0.12, pointerEvents: 'none', backgroundImage: `linear-gradient(${preset.accent} 1px, transparent 1px), linear-gradient(90deg, ${preset.accent} 1px, transparent 1px)`, backgroundSize: (layer.gap || 40) + 'px ' + (layer.gap || 40) + 'px' }"></div>

        <div v-else-if="layer.type === 'blur-image'" :style="{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }">
          <img v-if="layer.src" :src="layer.src" :style="{ width: '100%', height: '100%', objectFit: 'cover', filter: `blur(${layer.blur || 60}px) saturate(1.4)`, opacity: layer.opacity || 0.5, transform: 'scale(1.2)' }" />
          <div v-else :style="{ width: '100%', height: '100%', background: `radial-gradient(ellipse at ${layer.x || 30}% ${layer.y || 30}%, ${preset.accent2}, transparent 60%), radial-gradient(ellipse at ${layer.x2 || 70}% ${layer.y2 || 70}%, ${preset.accent}, transparent 60%)`, filter: `blur(${layer.blur || 80}px)`, opacity: layer.opacity || 0.7 }"></div>
        </div>

        <div v-else-if="layer.type === 'shine-line'" :style="{ position: 'absolute', left: 0, right: 0, top: (layer.y || 50) + '%', height: '2px', background: `linear-gradient(90deg, transparent, ${preset.accent}, ${preset.accent2}, transparent)`, opacity: layer.opacity || 0.7, pointerEvents: 'none' }"></div>

        <div v-else-if="layer.type === 'photo-bg'" :style="{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }">
          <img :src="photoSrc(layer)" :style="{ width: '100%', height: '100%', objectFit: 'cover', filter: layer.grayscale ? 'grayscale(1)' : 'none' }" referrerpolicy="no-referrer" crossorigin="anonymous" />
          <div v-if="layer.overlay !== false" :style="{ position: 'absolute', inset: 0, background: layer.overlayGrad || `linear-gradient(${layer.overlayAngle || 180}deg, ${preset.accent}cc 0%, ${preset.bg} 100%)`, opacity: layer.overlayOpacity ?? 0.75 }"></div>
        </div>

        <div v-else-if="layer.type === 'iso-card'" :style="{ ...pos(layer), width: (layer.size || 280) + 'px', height: (layer.size || 280) * 1.2 + 'px', background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, borderRadius: '24px', transform: `translate(-50%,-50%) perspective(800px) rotateY(${layer.rotateY ?? -18}deg) rotateX(${layer.rotateX ?? 8}deg)`, boxShadow: `0 30px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.1) inset`, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }">
          <i v-if="layer.icon" :class="['mdi', layer.icon]" :style="{ fontSize: (layer.size || 280) * 0.4 + 'px', color: '#fff', opacity: 0.95, filter: 'drop-shadow(0 8px 16px rgba(0,0,0,0.3))' }"></i>
          <img v-else-if="layer.src" :src="layer.src" :style="{ width: '100%', height: '100%', objectFit: 'cover' }" />
        </div>

        <svg v-else-if="layer.type === 'iso-cube'" :style="{ ...pos(layer), width: (layer.size || 200) + 'px', height: (layer.size || 200) + 'px', overflow: 'visible' }" viewBox="0 0 100 100">
          <defs>
            <linearGradient :id="`ic-top-${i}`" x1="0" x2="1" y1="0" y2="0"><stop offset="0" :stop-color="preset.accent2"/><stop offset="1" :stop-color="preset.accent"/></linearGradient>
            <linearGradient :id="`ic-left-${i}`" x1="0" x2="0" y1="0" y2="1"><stop offset="0" :stop-color="preset.accent"/><stop offset="1" stop-color="#000" stop-opacity="0.4"/></linearGradient>
            <linearGradient :id="`ic-right-${i}`" x1="0" x2="0" y1="0" y2="1"><stop offset="0" :stop-color="preset.accent2"/><stop offset="1" stop-color="#000" stop-opacity="0.5"/></linearGradient>
          </defs>
          <polygon points="50,10 90,30 50,50 10,30" :fill="`url(#ic-top-${i})`" />
          <polygon points="10,30 50,50 50,90 10,70" :fill="`url(#ic-left-${i})`" />
          <polygon points="90,30 50,50 50,90 90,70" :fill="`url(#ic-right-${i})`" />
        </svg>

        <div v-else-if="layer.type === 'glossy-ball'" :style="{ ...pos(layer), width: (layer.size || 120) + 'px', height: (layer.size || 120) + 'px', borderRadius: '50%', background: `radial-gradient(circle at 30% 25%, #fff 0%, ${preset.accent} 35%, ${preset.accent2} 80%, #1a0a3a 100%)`, transform: 'translate(-50%, -50%)', boxShadow: `0 20px 40px ${preset.accent}66, inset -8px -12px 30px rgba(0,0,0,0.3)` }"></div>

        <div v-else-if="layer.type === 'tag-pill'" :style="{ ...pos(layer), display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 18px', background: 'rgba(255,255,255,0.1)', border: `1px solid ${preset.accent}40`, borderRadius: '999px', backdropFilter: 'blur(10px)' }">
          <span :style="{ width: '8px', height: '8px', borderRadius: '50%', background: preset.accent, boxShadow: `0 0 12px ${preset.accent}` }"></span>
          <span :style="{ fontSize: (layer.size || 18) + 'px', fontWeight: 600, color: colorToken('text'), letterSpacing: '0.5px' }">{{ layer.text }}</span>
        </div>

        <div v-else-if="layer.type === 'big-number'" :class="{ 'l-int': interactive }" @mousedown="onLayerDown($event, i)" @click="onLayerClick($event, i)" :style="{ ...pos(layer), fontSize: (layer.size || 280) + 'px', fontWeight: 900, lineHeight: 0.85, background: `linear-gradient(135deg, ${preset.accent}, ${preset.accent2})`, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', letterSpacing: '-0.04em', fontFamily: 'system-ui' }">{{ layer.text }}</div>
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
.slide-canvas.interactive { cursor: default; }
.slide-inner {
  position: absolute;
  top: 0;
  left: 0;
  transform-origin: top left;
}
.l-int {
  cursor: move;
  user-select: none;
  transition: outline 0.05s;
}
.l-int:hover {
  outline: 2px solid rgba(129,140,248,0.5);
  outline-offset: 4px;
  border-radius: 4px;
}
.selection-outline {
  z-index: 999;
  box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3);
}
</style>
