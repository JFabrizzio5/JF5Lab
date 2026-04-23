<script setup>
import { computed, ref } from 'vue'
import { useCarouselStore } from '../stores/carousel'

const store = useCarouselStore()
const slide = computed(() => store.activeSlide)
const expanded = ref({})

function update(i, key, val) {
  store.updateLayer(store.activeIndex, i, { [key]: val })
}

function onImageUpload(layerIdx, e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => update(layerIdx, 'src', ev.target.result)
  reader.readAsDataURL(file)
}

function clearSrc(i) { update(i, 'src', null) }

function toggle(i) { expanded.value[i] = !expanded.value[i] }

const placeholderOpts = ['photo', 'phone', 'laptop', 'card', 'product', 'food', 'chart']
const peopleOpts = [
  '/people/01.svg', '/people/02.svg', '/people/03.svg',
  ...Array.from({ length: 20 }, (_, i) => `https://i.pravatar.cc/200?img=${i + 1}`)
]
const brandOpts = ['cometax', 'stocklink', 'notamx', 'porcobrar', 'pulsomx', 'agendapro', 'rentafacil', 'rankit', 'consultoria']

const photoLib = [
  { q: 'office', src: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=200&h=250&fit=crop' },
  { q: 'workspace', src: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=200&h=250&fit=crop' },
  { q: 'team', src: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=200&h=250&fit=crop' },
  { q: 'portrait', src: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=250&fit=crop' },
  { q: 'man', src: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=250&fit=crop' },
  { q: 'product', src: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=200&h=250&fit=crop' },
  { q: 'abstract', src: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=200&h=250&fit=crop' },
  { q: 'gradient', src: 'https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=200&h=250&fit=crop' },
  { q: 'mountain', src: 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=200&h=250&fit=crop' },
  { q: 'sunset', src: 'https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=200&h=250&fit=crop' },
  { q: 'food', src: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=200&h=250&fit=crop' },
  { q: 'laptop', src: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=200&h=250&fit=crop' }
]
const galleryOpen = ref({})
function toggleGallery(i) { galleryOpen.value[i] = !galleryOpen.value[i] }
</script>

<template>
  <div v-if="slide" class="layers">
    <div v-for="(layer, i) in slide.layers" :key="i" class="layer-card">
      <div class="layer-head">
        <i :class="['mdi', iconFor(layer.type)]"></i>
        <span>{{ labelFor(layer.type) }}</span>
      </div>

      <!-- Editable content -->
      <textarea
        v-if="layer.type === 'text' || layer.type === 'code-block'"
        class="textarea"
        :value="layer.text || layer.code"
        @input="update(i, layer.type === 'code-block' ? 'code' : 'text', $event.target.value)"
        :placeholder="layer.type === 'code-block' ? 'Código...' : 'Texto...'"
      ></textarea>

      <input
        v-else-if="layer.type === 'badge' || layer.type === 'diagonal-band'"
        class="input"
        :value="layer.text"
        @input="update(i, 'text', $event.target.value)"
        placeholder="Texto"
      />

      <div v-else-if="layer.type === 'icon-list'" class="sublayers">
        <div v-for="(it, j) in layer.items" :key="j" class="sub-row">
          <i :class="['mdi', it.icon]" style="color:var(--accent); font-size:18px;"></i>
          <input class="input" :value="it.text" @input="(ev) => { layer.items[j].text = ev.target.value }" />
        </div>
      </div>

      <div v-else-if="layer.type === 'step-row'" class="sublayers">
        <div v-for="(s, j) in layer.steps" :key="j" class="step-edit">
          <div class="step-num">{{ j + 1 }}</div>
          <div style="flex:1; display:flex; flex-direction:column; gap:4px;">
            <input class="input" :value="s.title" @input="(ev) => { layer.steps[j].title = ev.target.value }" placeholder="Título del paso" />
            <input class="input" :value="s.desc" @input="(ev) => { layer.steps[j].desc = ev.target.value }" placeholder="Descripción" style="font-size:12px;" />
          </div>
        </div>
      </div>

      <div v-else-if="layer.type === 'split'" class="sublayers">
        <input class="input" :value="layer.leftLabel" @input="update(i, 'leftLabel', $event.target.value)" placeholder="Etiqueta izq" />
        <input v-for="(it, j) in layer.leftItems" :key="'l'+j" class="input" :value="it" @input="(ev) => { layer.leftItems[j] = ev.target.value }" />
        <hr style="border-color:var(--border); margin:8px 0; opacity:0.4;" />
        <input class="input" :value="layer.rightLabel" @input="update(i, 'rightLabel', $event.target.value)" placeholder="Etiqueta der" />
        <input v-for="(it, j) in layer.rightItems" :key="'r'+j" class="input" :value="it" @input="(ev) => { layer.rightItems[j] = ev.target.value }" />
      </div>

      <div v-else-if="layer.type === 'image' || layer.type === 'avatar' || layer.type === 'blur-image' || layer.type === 'laptop-mockup' || layer.type === 'phone-mockup' || layer.type === 'browser-mockup'" class="image-controls">
        <input v-if="layer.type === 'browser-mockup'" class="input" :value="layer.url" @input="update(i, 'url', $event.target.value)" placeholder="URL (ej: cometax.mx)" style="margin-bottom:6px;" />
        <div class="row">
          <label class="btn" style="flex:1;">
            <i class="mdi mdi-upload"></i>
            <span>{{ layer.src ? 'Cambiar' : 'Subir' }}</span>
            <input type="file" accept="image/*" @change="onImageUpload(i, $event)" hidden />
          </label>
          <button class="btn" @click="toggleGallery(i)" title="Galería">
            <i class="mdi mdi-image-multiple"></i>
            <span>Galería</span>
          </button>
          <button v-if="layer.src" class="btn" @click="clearSrc(i)" title="Quitar"><i class="mdi mdi-close"></i></button>
        </div>

        <div v-if="galleryOpen[i]" class="gallery">
          <div v-if="layer.type === 'avatar'" class="gallery-section">
            <div class="mini">Personas (click para usar)</div>
            <div class="thumbs">
              <button v-for="p in peopleOpts" :key="p" class="person-thumb" @click="update(i, 'src', p); galleryOpen[i] = false">
                <img :src="p" loading="lazy" />
              </button>
            </div>
          </div>
          <div v-else class="gallery-section">
            <div class="mini">Fotos sin copyright (click para usar)</div>
            <div class="photo-grid">
              <button v-for="ph in photoLib" :key="ph.q" class="photo-thumb" @click="update(i, 'src', ph.src.replace('w=200&h=250', 'w=1080&h=1350')); galleryOpen[i] = false" :title="ph.q">
                <img :src="ph.src" loading="lazy" />
                <span>{{ ph.q }}</span>
              </button>
            </div>
            <div class="mini" style="margin-top:8px;">O personas/avatares</div>
            <div class="thumbs">
              <button v-for="p in peopleOpts.slice(0, 12)" :key="p" class="person-thumb" @click="update(i, 'src', p); galleryOpen[i] = false">
                <img :src="p" loading="lazy" />
              </button>
            </div>
          </div>
        </div>

        <div v-if="layer.type === 'image' && !layer.src && !galleryOpen[i]" class="placeholder-options">
          <div class="mini">O placeholder icon:</div>
          <div class="row wrap">
            <button v-for="opt in placeholderOpts" :key="opt" class="chip" :class="{ active: layer.placeholder === opt }" @click="update(i, 'placeholder', opt)">{{ opt }}</button>
          </div>
        </div>
      </div>

      <div v-else-if="layer.type === 'logo'" class="logo-controls">
        <div class="mini">Marca CometaX:</div>
        <div class="brand-grid">
          <button v-for="b in brandOpts" :key="b" class="brand-chip" :class="{ active: layer.brand === b }" @click="update(i, 'brand', b)">
            <img :src="`/logos/${b}.svg`" />
            <span>{{ b }}</span>
          </button>
        </div>
        <button class="btn" style="margin-top:8px;" @click="update(i, 'brand', null)">
          <i class="mdi mdi-close"></i>
          Usar logo subido / default
        </button>
        <label style="display:flex; gap:8px; align-items:center; margin-top:8px; font-size:13px; color:var(--muted);">
          <input type="checkbox" :checked="layer.hideText" @change="update(i, 'hideText', $event.target.checked)" />
          Ocultar nombre
        </label>
      </div>

      <div v-else class="muted-note">Decorativo</div>

      <!-- Position/size controls — siempre visibles -->
      <div class="advanced">
        <div v-if="hasXY(layer)" class="grid-2">
          <label>
            <span class="mini">X · {{ Math.round(layer.x || 0) }}%</span>
            <input type="range" min="0" max="100" step="1" :value="layer.x || 0" @input="update(i, 'x', Number($event.target.value))" />
          </label>
          <label>
            <span class="mini">Y · {{ Math.round(layer.y || 0) }}%</span>
            <input type="range" min="0" max="100" step="1" :value="layer.y || 0" @input="update(i, 'y', Number($event.target.value))" />
          </label>
        </div>

        <label v-if="hasSize(layer)">
          <span class="mini">Tamaño · {{ layer.size || (layer.type === 'text' ? 32 : 50) }}px</span>
          <input type="range" :min="sizeRange(layer).min" :max="sizeRange(layer).max" :step="sizeRange(layer).step" :value="layer.size || (layer.type === 'text' ? 32 : 50)" @input="update(i, 'size', Number($event.target.value))" />
        </label>

        <label v-if="layer.type === 'image' || layer.type === 'icon-list'">
          <span class="mini">Ancho · {{ layer.w || 50 }}%</span>
          <input type="range" min="20" max="100" step="2" :value="layer.w || 50" @input="update(i, 'w', Number($event.target.value))" />
        </label>

        <label v-if="layer.type === 'text' && layer.weight">
          <span class="mini">Peso · {{ layer.weight }}</span>
          <input type="range" min="300" max="900" step="100" :value="layer.weight" @input="update(i, 'weight', Number($event.target.value))" />
        </label>

        <div v-if="hasAlign(layer)" class="row">
          <button v-for="a in ['left','center','right']" :key="a" class="chip small" :class="{ active: (layer.align || 'left') === a }" @click="update(i, 'align', a)">
            <i :class="['mdi', `mdi-format-align-${a}`]"></i>
          </button>
        </div>

        <div v-if="hasColor(layer)" class="row wrap">
          <button v-for="c in ['text','muted','accent','accent2']" :key="c" class="chip small" :class="{ active: layer.color === c }" @click="update(i, 'color', c)">{{ c }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
function iconFor(type) {
  const m = {
    'laptop-mockup': 'mdi-laptop',
    'phone-mockup': 'mdi-cellphone',
    'browser-mockup': 'mdi-web',
    'step-row': 'mdi-format-list-numbered',
    text: 'mdi-format-text',
    badge: 'mdi-label',
    icon: 'mdi-shape',
    'icon-list': 'mdi-format-list-bulleted',
    'code-block': 'mdi-code-tags',
    'gradient-blob': 'mdi-blur-radial',
    'comet-trail': 'mdi-meteor',
    'progress-dots': 'mdi-dots-horizontal',
    split: 'mdi-compare',
    avatar: 'mdi-account-circle',
    image: 'mdi-image',
    logo: 'mdi-image-outline',
    sparkle: 'mdi-creation',
    'corner-shape': 'mdi-square-rounded-outline',
    'wave-bottom': 'mdi-wave',
    'wave-top': 'mdi-wave',
    'half-split': 'mdi-format-color-fill',
    'gradient-overlay': 'mdi-gradient-vertical',
    'diagonal-band': 'mdi-rotate-3d-variant',
    'dots-pattern': 'mdi-dots-grid',
    'grid-pattern': 'mdi-grid',
    'blur-image': 'mdi-blur',
    'shine-line': 'mdi-minus-thick'
  }
  return m[type] || 'mdi-shape'
}
function labelFor(type) {
  const m = {
    'laptop-mockup': 'Mockup laptop',
    'phone-mockup': 'Mockup celular',
    'browser-mockup': 'Mockup navegador',
    'step-row': 'Filas con pasos',
    text: 'Texto',
    badge: 'Badge',
    icon: 'Icono',
    'icon-list': 'Lista con iconos',
    'code-block': 'Código',
    'gradient-blob': 'Blob difuso',
    'comet-trail': 'Cola cometa',
    'progress-dots': 'Pasos',
    split: 'Comparación',
    avatar: 'Avatar / Persona',
    image: 'Imagen',
    logo: 'Logo de marca',
    sparkle: 'Estrella',
    'corner-shape': 'Forma decorativa',
    'wave-bottom': 'Onda inferior',
    'wave-top': 'Onda superior',
    'half-split': 'Mitad y mitad',
    'gradient-overlay': 'Overlay degradado',
    'diagonal-band': 'Banda diagonal',
    'dots-pattern': 'Patrón puntos',
    'grid-pattern': 'Patrón cuadrícula',
    'blur-image': 'Imagen difuminada',
    'shine-line': 'Línea brillante'
  }
  return m[type] || type
}
function hasXY(l) {
  return !['half-split', 'gradient-overlay', 'dots-pattern', 'grid-pattern', 'blur-image', 'wave-top', 'wave-bottom', 'shine-line'].includes(l.type)
}
function hasSize(l) {
  return ['text', 'icon', 'icon-list', 'avatar', 'logo', 'sparkle', 'corner-shape', 'iso-card', 'iso-cube', 'glossy-ball', 'big-number', 'tag-pill', 'badge', 'progress-dots', 'laptop-mockup', 'phone-mockup', 'browser-mockup'].includes(l.type)
}
function sizeRange(l) {
  if (l.type === 'text' || l.type === 'big-number') return { min: 14, max: 360, step: 2 }
  if (l.type === 'icon' || l.type === 'avatar' || l.type === 'glossy-ball') return { min: 30, max: 360, step: 4 }
  if (l.type === 'iso-card' || l.type === 'iso-cube') return { min: 80, max: 500, step: 10 }
  if (l.type === 'laptop-mockup' || l.type === 'browser-mockup') return { min: 280, max: 800, step: 10 }
  if (l.type === 'phone-mockup') return { min: 140, max: 400, step: 10 }
  if (l.type === 'logo' || l.type === 'badge' || l.type === 'tag-pill') return { min: 16, max: 80, step: 2 }
  if (l.type === 'icon-list') return { min: 16, max: 60, step: 2 }
  if (l.type === 'sparkle' || l.type === 'progress-dots') return { min: 20, max: 200, step: 4 }
  return { min: 20, max: 400, step: 4 }
}
function hasAlign(l) {
  return ['text', 'logo', 'badge', 'icon', 'avatar'].includes(l.type)
}
function hasColor(l) {
  return ['text', 'icon', 'sparkle'].includes(l.type)
}
</script>

<style scoped>
.layers { display: flex; flex-direction: column; gap: 10px; }
.layer-card {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px;
}
.layer-head {
  display: flex; align-items: center; gap: 8px;
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  color: var(--muted); letter-spacing: 0.5px; margin-bottom: 8px;
  cursor: pointer; user-select: none;
}
.layer-head i:first-child { color: var(--accent); }
.sublayers { display: flex; flex-direction: column; gap: 6px; }
.sub-row { display: flex; align-items: center; gap: 8px; }
.sub-row .input { flex: 1; }
.step-edit { display: flex; gap: 8px; align-items: flex-start; padding: 6px; background: var(--card); border-radius: 6px; }
.step-num {
  flex-shrink: 0; width: 28px; height: 28px; border-radius: 6px;
  background: var(--grad); color: #fff; display: grid; place-items: center;
  font-weight: 800; font-size: 13px;
}
.muted-note { color: var(--muted); font-size: 12px; font-style: italic; }
.image-controls, .logo-controls { display: flex; flex-direction: column; gap: 8px; }
.row { display: flex; gap: 6px; align-items: center; }
.row.wrap { flex-wrap: wrap; }
.mini { display: block; font-size: 11px; color: var(--muted); margin-bottom: 4px; }

.placeholder-options, .people-row { display: flex; flex-direction: column; gap: 6px; }
.gallery {
  background: var(--card); border-radius: 8px; padding: 10px;
  border: 1px solid var(--border); margin-top: 6px;
  max-height: 320px; overflow-y: auto;
}
.gallery-section { display: flex; flex-direction: column; gap: 6px; }
.thumbs { display: flex; gap: 6px; flex-wrap: wrap; }
.person-thumb {
  width: 44px; height: 44px; border-radius: 50%; overflow: hidden;
  padding: 0; border: 2px solid transparent; background: var(--bg-2);
}
.person-thumb:hover { border-color: var(--accent); }
.person-thumb img { width: 100%; height: 100%; object-fit: cover; }
.photo-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
}
.photo-thumb {
  position: relative; aspect-ratio: 4/5; border-radius: 8px;
  overflow: hidden; padding: 0; border: 2px solid transparent;
  background: var(--bg-2); cursor: pointer;
}
.photo-thumb:hover { border-color: var(--accent); }
.photo-thumb img { width: 100%; height: 100%; object-fit: cover; }
.photo-thumb span {
  position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%);
  font-size: 9px; font-weight: 700; color: #fff; background: rgba(0,0,0,0.6);
  padding: 2px 6px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;
}

.brand-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
  max-height: 180px; overflow-y: auto; padding-right: 4px;
}
.brand-chip {
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 6px 4px; background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; cursor: pointer;
}
.brand-chip.active { border-color: var(--accent); background: rgba(129,140,248,0.1); }
.brand-chip:hover { border-color: var(--accent); }
.brand-chip img { width: 28px; height: 28px; }
.brand-chip span { font-size: 10px; color: var(--muted); }

.advanced {
  display: flex; flex-direction: column; gap: 10px;
  margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border);
}
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
input[type="range"] {
  width: 100%; -webkit-appearance: none; appearance: none;
  background: transparent; cursor: pointer; height: 18px;
}
input[type="range"]::-webkit-slider-runnable-track {
  height: 4px; background: var(--border); border-radius: 2px;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none; appearance: none; width: 14px; height: 14px;
  background: var(--accent); border-radius: 50%; margin-top: -5px;
}
.chip {
  padding: 6px 12px; border-radius: 999px;
  background: var(--card); border: 1px solid var(--border);
  color: var(--muted); font-size: 12px; font-weight: 600;
}
.chip.small { padding: 4px 10px; font-size: 11px; }
.chip.active { background: var(--accent); color: #fff; border-color: var(--accent); }
</style>
