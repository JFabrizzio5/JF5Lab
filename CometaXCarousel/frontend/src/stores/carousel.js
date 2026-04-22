import { defineStore } from 'pinia'
import { TEMPLATES, PRESETS, SIZES, findTemplate } from '../templates'
import { findPreset } from '../presets'

const clone = (o) => JSON.parse(JSON.stringify(o))

export const useCarouselStore = defineStore('carousel', {
  state: () => ({
    sizeKey: 'post',
    presetKey: 'cosmic',
    customPreset: null,
    logoDataUrl: null,
    logoText: 'CometaX',
    handle: '@cometax',
    slides: [],
    activeIndex: 0
  }),
  getters: {
    size: (s) => SIZES[s.sizeKey],
    preset: (s) => s.customPreset || PRESETS[s.presetKey],
    activeSlide: (s) => s.slides[s.activeIndex] || null
  },
  actions: {
    init() {
      if (this.slides.length === 0) {
        this.addFromTemplate('cosmic-quote')
        this.addFromTemplate('feature-list')
        this.addFromTemplate('cta-final')
      }
    },
    addFromTemplate(templateId) {
      const tpl = findTemplate(templateId)
      if (!tpl) return
      this.slides.push({
        uid: crypto.randomUUID(),
        templateId,
        layers: clone(tpl.layers)
      })
      this.activeIndex = this.slides.length - 1
    },
    duplicate(index) {
      const s = this.slides[index]
      if (!s) return
      this.slides.splice(index + 1, 0, { ...clone(s), uid: crypto.randomUUID() })
      this.activeIndex = index + 1
    },
    remove(index) {
      this.slides.splice(index, 1)
      if (this.activeIndex >= this.slides.length) this.activeIndex = this.slides.length - 1
      if (this.activeIndex < 0) this.activeIndex = 0
    },
    move(from, to) {
      if (to < 0 || to >= this.slides.length) return
      const [s] = this.slides.splice(from, 1)
      this.slides.splice(to, 0, s)
      this.activeIndex = to
    },
    updateLayer(slideIndex, layerIndex, patch) {
      Object.assign(this.slides[slideIndex].layers[layerIndex], patch)
    },
    setPreset(key) {
      this.presetKey = key
      this.customPreset = null
    },
    setCustomColor(field, value) {
      if (!this.customPreset) this.customPreset = clone(this.preset)
      this.customPreset[field] = value
    },
    setSize(key) { this.sizeKey = key },
    setLogo(dataUrl) { this.logoDataUrl = dataUrl },
    setHandle(h) { this.handle = h },
    reset() {
      this.slides = []
      this.activeIndex = 0
      this.customPreset = null
    },
    loadPreset(presetId) {
      const p = findPreset(presetId)
      if (!p) return
      this.slides = clone(p.slides).map(s => ({ ...s, uid: crypto.randomUUID() }))
      this.activeIndex = 0
      this.presetKey = p.presetKey
      this.sizeKey = p.sizeKey
      this.customPreset = null
    }
  }
})
