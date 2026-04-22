<script setup>
import { useCarouselStore } from '../stores/carousel'
import SlideCanvas from './SlideCanvas.vue'

const store = useCarouselStore()

function setActive(i) { store.activeIndex = i }
</script>

<template>
  <div class="strip">
    <div
      v-for="(s, i) in store.slides"
      :key="s.uid"
      class="thumb"
      :class="{ active: store.activeIndex === i }"
      @click="setActive(i)"
    >
      <div class="thumb-inner">
        <SlideCanvas :slide="s" :scale="0.1" />
      </div>
      <div class="thumb-actions">
        <button class="icon" @click.stop="store.move(i, i - 1)" title="Subir"><i class="mdi mdi-arrow-up"></i></button>
        <button class="icon" @click.stop="store.move(i, i + 1)" title="Bajar"><i class="mdi mdi-arrow-down"></i></button>
        <button class="icon" @click.stop="store.duplicate(i)" title="Duplicar"><i class="mdi mdi-content-copy"></i></button>
        <button class="icon danger" @click.stop="store.remove(i)" title="Eliminar"><i class="mdi mdi-delete-outline"></i></button>
      </div>
      <div class="thumb-num">{{ i + 1 }}</div>
    </div>
  </div>
</template>

<style scoped>
.strip {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 4px;
}
.thumb {
  position: relative;
  border: 2px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s;
  overflow: hidden;
}
.thumb.active { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2); }
.thumb:hover { border-color: var(--accent); }
.thumb-inner { display: flex; justify-content: center; align-items: center; padding: 4px; }
.thumb-num {
  position: absolute; top: 6px; left: 6px;
  background: rgba(0,0,0,0.6); color: #fff;
  font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 4px;
}
.thumb-actions {
  position: absolute; top: 6px; right: 6px;
  display: none; flex-direction: column; gap: 4px;
}
.thumb:hover .thumb-actions, .thumb.active .thumb-actions { display: flex; }
.icon {
  background: rgba(0,0,0,0.7); color: #fff;
  width: 22px; height: 22px; border-radius: 4px;
  font-size: 14px; display: grid; place-items: center;
}
.icon:hover { background: var(--accent); }
.icon.danger:hover { background: var(--bad); }
</style>
