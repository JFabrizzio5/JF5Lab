<script setup>
import { onMounted, ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useCarouselStore } from '../stores/carousel'
import SlideCanvas from '../components/SlideCanvas.vue'
import SlideStrip from '../components/SlideStrip.vue'
import TemplatePicker from '../components/TemplatePicker.vue'
import BrandPanel from '../components/BrandPanel.vue'
import LayerEditor from '../components/LayerEditor.vue'
import ExportModal from '../components/ExportModal.vue'

const store = useCarouselStore()
const showPicker = ref(false)
const showExport = ref(false)
const sidebarTab = ref('layers')

const previewScale = computed(() => {
  const maxW = 480
  const maxH = 600
  const sw = maxW / store.size.w
  const sh = maxH / store.size.h
  return Math.min(sw, sh)
})

onMounted(() => {
  store.init()
})
</script>

<template>
  <div class="editor">
    <header class="topbar">
      <RouterLink to="/" class="back">
        <i class="mdi mdi-arrow-left"></i>
        <span>CometaX Carousel</span>
      </RouterLink>
      <div class="actions">
        <button class="btn" @click="store.reset(); store.init()" title="Reiniciar">
          <i class="mdi mdi-refresh"></i>
        </button>
        <button class="btn btn-primary" @click="showExport = true">
          <i class="mdi mdi-download"></i>
          Exportar
        </button>
      </div>
    </header>

    <div class="grid">
      <aside class="left">
        <div class="panel-head">
          <i class="mdi mdi-image-multiple"></i>
          <span>Slides ({{ store.slides.length }})</span>
        </div>
        <SlideStrip />
        <button class="btn add" @click="showPicker = true">
          <i class="mdi mdi-plus"></i>
          Agregar slide
        </button>
      </aside>

      <main class="canvas-area">
        <div v-if="store.activeSlide" class="canvas-wrap">
          <SlideCanvas :slide="store.activeSlide" :scale="previewScale" />
        </div>
        <div v-else class="empty">
          <i class="mdi mdi-image-plus"></i>
          <p>Sin slides. Agrega uno desde el panel izquierdo.</p>
        </div>
      </main>

      <aside class="right">
        <div class="tabs">
          <button class="tab" :class="{ active: sidebarTab === 'layers' }" @click="sidebarTab = 'layers'">
            <i class="mdi mdi-layers"></i> Capas
          </button>
          <button class="tab" :class="{ active: sidebarTab === 'brand' }" @click="sidebarTab = 'brand'">
            <i class="mdi mdi-palette"></i> Marca
          </button>
        </div>
        <div class="tab-body">
          <LayerEditor v-if="sidebarTab === 'layers'" />
          <BrandPanel v-else-if="sidebarTab === 'brand'" />
        </div>
      </aside>
    </div>

    <!-- Picker overlay -->
    <Transition name="fade">
      <div v-if="showPicker" class="overlay" @click.self="showPicker = false">
        <div class="modal big">
          <div class="modal-head">
            <h3>Elegir plantilla</h3>
            <button class="icon-btn" @click="showPicker = false"><i class="mdi mdi-close"></i></button>
          </div>
          <TemplatePicker @picked="showPicker = false" />
        </div>
      </div>
    </Transition>

    <ExportModal :open="showExport" @close="showExport = false" />
  </div>
</template>

<style scoped>
.editor { height: 100vh; display: flex; flex-direction: column; }

.topbar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 20px; border-bottom: 1px solid var(--border);
  background: rgba(10, 14, 26, 0.6); backdrop-filter: blur(10px);
}
.back { display: flex; align-items: center; gap: 10px; color: var(--text); font-weight: 700; }
.actions { display: flex; gap: 10px; }

.grid {
  flex: 1; display: grid; grid-template-columns: 200px 1fr 320px;
  overflow: hidden;
}

.left, .right {
  border-right: 1px solid var(--border);
  background: var(--bg-2); overflow-y: auto;
  padding: 16px;
}
.right { border-right: none; border-left: 1px solid var(--border); }

.panel-head {
  display: flex; align-items: center; gap: 8px;
  font-size: 11px; font-weight: 800; letter-spacing: 1px;
  text-transform: uppercase; color: var(--muted); margin-bottom: 14px;
}
.add {
  width: 100%; justify-content: center; margin-top: 14px;
  border-style: dashed;
}

.canvas-area {
  display: grid; place-items: center;
  background: radial-gradient(ellipse at center, #1e1b4b22 0%, transparent 60%);
  padding: 30px; overflow: auto;
}
.canvas-wrap { display: grid; place-items: center; }
.empty { text-align: center; color: var(--muted); }
.empty i { font-size: 64px; opacity: 0.3; }
.empty p { margin-top: 10px; }

.tabs { display: flex; gap: 4px; margin-bottom: 16px; }
.tab {
  flex: 1; padding: 8px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  color: var(--muted); font-size: 13px; font-weight: 600;
}
.tab.active { background: var(--accent); color: #fff; }

.overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.65);
  backdrop-filter: blur(6px); display: grid; place-items: center;
  z-index: 50; padding: 20px;
}
.modal {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px; max-width: 760px; width: 100%;
  max-height: 80vh; overflow-y: auto;
}
.modal-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modal-head h3 { margin: 0; font-size: 20px; }
.icon-btn { width: 32px; height: 32px; border-radius: 8px; display: grid; place-items: center; color: var(--muted); }
.icon-btn:hover { background: var(--bg-2); color: var(--text); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 1024px) {
  .grid { grid-template-columns: 160px 1fr 280px; }
}
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; grid-template-rows: auto 1fr auto; }
  .left, .right { max-height: 200px; border: none; border-bottom: 1px solid var(--border); }
}
</style>
