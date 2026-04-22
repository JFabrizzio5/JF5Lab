<script setup>
import { ref, nextTick } from 'vue'
import { toPng, toJpeg } from 'html-to-image'
import JSZip from 'jszip'
import { useCarouselStore } from '../stores/carousel'
import SlideCanvas from './SlideCanvas.vue'

const props = defineProps({ open: Boolean })
const emit = defineEmits(['close'])

const store = useCarouselStore()
const stage = ref(null)
const busy = ref(false)
const progress = ref(0)
const format = ref('png')

async function renderSlide(slide) {
  const wrapper = document.createElement('div')
  wrapper.style.position = 'fixed'
  wrapper.style.left = '-99999px'
  wrapper.style.top = '0'
  document.body.appendChild(wrapper)

  const { createApp, h } = await import('vue')
  const { createPinia } = await import('pinia')
  const piniaInstance = createPinia()
  const app = createApp({
    render: () => h(SlideCanvas, { slide, scale: 1 })
  })
  app.use(piniaInstance)
  // Re-hydrate state in isolated pinia
  const isoStore = (await import('../stores/carousel')).useCarouselStore(piniaInstance)
  isoStore.$state = JSON.parse(JSON.stringify(store.$state))
  app.mount(wrapper)
  await nextTick()
  await new Promise(r => setTimeout(r, 80))

  const node = wrapper.firstElementChild
  const opts = { pixelRatio: 1, cacheBust: true }
  const dataUrl = format.value === 'jpg'
    ? await toJpeg(node, { ...opts, quality: 0.92 })
    : await toPng(node, opts)

  app.unmount()
  wrapper.remove()
  return dataUrl
}

async function downloadSingle() {
  busy.value = true
  progress.value = 0
  try {
    const slide = store.activeSlide
    const dataUrl = await renderSlide(slide)
    triggerDownload(dataUrl, `cometax-slide-${store.activeIndex + 1}.${format.value}`)
  } finally {
    busy.value = false
  }
}

async function downloadAllZip() {
  busy.value = true
  progress.value = 0
  try {
    const zip = new JSZip()
    for (let i = 0; i < store.slides.length; i++) {
      const dataUrl = await renderSlide(store.slides[i])
      const base64 = dataUrl.split(',')[1]
      zip.file(`slide-${String(i + 1).padStart(2, '0')}.${format.value}`, base64, { base64: true })
      progress.value = Math.round(((i + 1) / store.slides.length) * 100)
    }
    const blob = await zip.generateAsync({ type: 'blob' })
    const url = URL.createObjectURL(blob)
    triggerDownload(url, `cometax-carousel-${Date.now()}.zip`)
    URL.revokeObjectURL(url)
  } finally {
    busy.value = false
  }
}

function triggerDownload(url, filename) {
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
}
</script>

<template>
  <Transition name="fade">
    <div v-if="open" class="overlay" @click.self="emit('close')">
      <div class="modal">
        <div class="modal-head">
          <h3>Exportar carrusel</h3>
          <button class="icon-btn" @click="emit('close')"><i class="mdi mdi-close"></i></button>
        </div>

        <div class="modal-body">
          <div class="info">
            <div><strong>{{ store.slides.length }}</strong> slides · <strong>{{ store.size.w }}×{{ store.size.h }}</strong> px</div>
          </div>

          <div class="row">
            <button class="chip" :class="{ active: format === 'png' }" @click="format = 'png'">PNG (mejor calidad)</button>
            <button class="chip" :class="{ active: format === 'jpg' }" @click="format = 'jpg'">JPG (más liviano)</button>
          </div>

          <div v-if="busy" class="progress">
            <div class="bar" :style="{ width: progress + '%' }"></div>
            <span>{{ progress }}%</span>
          </div>

          <div class="actions">
            <button class="btn" @click="downloadSingle" :disabled="busy">
              <i class="mdi mdi-download"></i>
              Slide actual
            </button>
            <button class="btn btn-primary" @click="downloadAllZip" :disabled="busy">
              <i class="mdi mdi-folder-zip"></i>
              {{ busy ? 'Generando...' : `Carrusel completo (.zip)` }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.overlay {
  position: fixed; inset: 0; background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  display: grid; place-items: center; z-index: 50; padding: 20px;
}
.modal {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px; max-width: 520px; width: 100%;
  box-shadow: var(--shadow);
}
.modal-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modal-head h3 { margin: 0; font-size: 20px; }
.icon-btn { width: 32px; height: 32px; border-radius: 8px; display: grid; place-items: center; color: var(--muted); }
.icon-btn:hover { background: var(--bg-2); color: var(--text); }
.modal-body { display: flex; flex-direction: column; gap: 16px; }
.info { color: var(--muted); font-size: 14px; }
.row { display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
  padding: 8px 14px; border-radius: 999px;
  background: var(--bg-2); border: 1px solid var(--border);
  color: var(--muted); font-size: 13px; font-weight: 600;
}
.chip.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.actions { display: flex; gap: 10px; margin-top: 8px; }
.actions .btn { flex: 1; justify-content: center; }
.progress {
  position: relative; height: 32px; background: var(--bg-2);
  border-radius: 8px; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}
.bar { position: absolute; left: 0; top: 0; bottom: 0; background: var(--grad); transition: width 0.2s; }
.progress span { position: relative; color: #fff; font-weight: 700; font-size: 13px; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
