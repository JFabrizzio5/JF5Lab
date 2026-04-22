<script setup>
import { computed } from 'vue'
import { useCarouselStore } from '../stores/carousel'

const store = useCarouselStore()
const slide = computed(() => store.activeSlide)

const editableTypes = ['text', 'badge', 'code-block']

function update(i, key, val) {
  store.updateLayer(store.activeIndex, i, { [key]: val })
}
</script>

<template>
  <div v-if="slide" class="layers">
    <div v-for="(layer, i) in slide.layers" :key="i" class="layer-card">
      <div class="layer-head">
        <i :class="['mdi', iconFor(layer.type)]"></i>
        <span>{{ labelFor(layer.type) }}</span>
      </div>

      <textarea
        v-if="layer.type === 'text' || layer.type === 'code-block'"
        class="textarea"
        :value="layer.text || layer.code"
        @input="update(i, layer.type === 'code-block' ? 'code' : 'text', $event.target.value)"
        :placeholder="layer.type === 'code-block' ? 'Código...' : 'Texto...'"
      ></textarea>

      <input
        v-else-if="layer.type === 'badge'"
        class="input"
        :value="layer.text"
        @input="update(i, 'text', $event.target.value)"
      />

      <div v-else-if="layer.type === 'icon-list'" class="sublayers">
        <div v-for="(it, j) in layer.items" :key="j" class="sub">
          <input class="input" :value="it.text" @input="(ev) => { layer.items[j].text = ev.target.value }" />
        </div>
      </div>

      <div v-else-if="layer.type === 'split'" class="sublayers">
        <input class="input" :value="layer.leftLabel" @input="update(i, 'leftLabel', $event.target.value)" placeholder="Etiqueta izq" />
        <input v-for="(it, j) in layer.leftItems" :key="'l'+j" class="input" :value="it" @input="(ev) => { layer.leftItems[j] = ev.target.value }" />
        <hr style="border-color:var(--border); margin:8px 0;" />
        <input class="input" :value="layer.rightLabel" @input="update(i, 'rightLabel', $event.target.value)" placeholder="Etiqueta der" />
        <input v-for="(it, j) in layer.rightItems" :key="'r'+j" class="input" :value="it" @input="(ev) => { layer.rightItems[j] = ev.target.value }" />
      </div>

      <div v-else class="muted-note">Decorativo (sin edición)</div>
    </div>
  </div>
</template>

<script>
function iconFor(type) {
  const m = {
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
    logo: 'mdi-image-outline'
  }
  return m[type] || 'mdi-shape'
}
function labelFor(type) {
  const m = {
    text: 'Texto',
    badge: 'Badge',
    icon: 'Icono',
    'icon-list': 'Lista con iconos',
    'code-block': 'Código',
    'gradient-blob': 'Blob',
    'comet-trail': 'Cola cometa',
    'progress-dots': 'Pasos',
    split: 'Comparación',
    avatar: 'Avatar',
    logo: 'Logo'
  }
  return m[type] || type
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
}
.layer-head i { color: var(--accent); }
.sublayers { display: flex; flex-direction: column; gap: 6px; }
.sub { }
.muted-note { color: var(--muted); font-size: 12px; font-style: italic; }
</style>
