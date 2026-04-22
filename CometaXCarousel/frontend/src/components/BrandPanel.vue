<script setup>
import { useCarouselStore } from '../stores/carousel'
import { PRESETS, SIZES } from '../templates'

const store = useCarouselStore()

function onLogoUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => store.setLogo(ev.target.result)
  reader.readAsDataURL(file)
}

function clearLogo() { store.setLogo(null) }
</script>

<template>
  <div class="brand">
    <div class="section">
      <div class="label">Tamaño</div>
      <div class="row">
        <button v-for="(s, key) in SIZES" :key="key" class="chip" :class="{ active: store.sizeKey === key }" @click="store.setSize(key)">{{ s.name }}</button>
      </div>
    </div>

    <div class="section">
      <div class="label">Paleta</div>
      <div class="row">
        <button v-for="(p, key) in PRESETS" :key="key" class="palette" :class="{ active: store.presetKey === key && !store.customPreset }" @click="store.setPreset(key)" :title="p.name">
          <span :style="{ background: p.bg }"></span>
        </button>
      </div>
    </div>

    <div class="section">
      <div class="label">Acento personalizado</div>
      <div class="grid-2">
        <label>
          <span class="mini">Acento 1</span>
          <input type="color" :value="store.preset.accent" @input="store.setCustomColor('accent', $event.target.value)" />
        </label>
        <label>
          <span class="mini">Acento 2</span>
          <input type="color" :value="store.preset.accent2" @input="store.setCustomColor('accent2', $event.target.value)" />
        </label>
      </div>
    </div>

    <div class="section">
      <div class="label">Marca</div>
      <input class="input" :value="store.logoText" @input="store.logoText = $event.target.value" placeholder="CometaX" />
      <input class="input" :value="store.handle" @input="store.setHandle($event.target.value)" placeholder="@cometax" style="margin-top:8px;" />
    </div>

    <div class="section">
      <div class="label">Logo</div>
      <div class="logo-row">
        <label class="btn" style="flex:1; justify-content:center;">
          <i class="mdi mdi-upload"></i>
          <span>{{ store.logoDataUrl ? 'Cambiar' : 'Subir PNG/SVG' }}</span>
          <input type="file" accept="image/*" @change="onLogoUpload" hidden />
        </label>
        <button v-if="store.logoDataUrl" class="btn" @click="clearLogo" title="Quitar logo">
          <i class="mdi mdi-close"></i>
        </button>
      </div>
      <div v-if="store.logoDataUrl" class="logo-preview">
        <img :src="store.logoDataUrl" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.brand { display: flex; flex-direction: column; gap: 20px; }
.section { display: flex; flex-direction: column; gap: 8px; }
.row { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  padding: 6px 12px; border-radius: 999px;
  background: var(--bg-2); border: 1px solid var(--border);
  color: var(--muted); font-size: 12px; font-weight: 600;
}
.chip.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.palette {
  width: 36px; height: 36px; border-radius: 8px;
  border: 2px solid transparent; padding: 0; overflow: hidden;
}
.palette span { display: block; width: 100%; height: 100%; }
.palette.active { border-color: var(--accent); }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.mini { display: block; font-size: 11px; color: var(--muted); margin-bottom: 4px; }
input[type="color"] {
  width: 100%; height: 36px; border: 1px solid var(--border);
  border-radius: 8px; background: var(--bg-2); cursor: pointer;
}
.logo-row { display: flex; gap: 8px; }
.logo-preview {
  margin-top: 8px; padding: 12px; background: var(--bg-2);
  border: 1px solid var(--border); border-radius: 8px;
  display: flex; justify-content: center;
}
.logo-preview img { max-height: 48px; max-width: 100%; }
</style>
