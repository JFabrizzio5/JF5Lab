<script setup>
import { TEMPLATES } from '../templates'
import { useCarouselStore } from '../stores/carousel'

const store = useCarouselStore()
const emit = defineEmits(['picked'])

function pick(id) {
  store.addFromTemplate(id)
  emit('picked')
}
</script>

<template>
  <div class="picker">
    <div class="picker-grid">
      <button v-for="t in TEMPLATES" :key="t.id" class="picker-card" @click="pick(t.id)">
        <div class="picker-thumb">
          <span class="cat">{{ t.category }}</span>
        </div>
        <div class="picker-name">{{ t.name }}</div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.picker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 14px;
}
.picker-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0;
  border-radius: 10px;
  background: var(--card);
  border: 1px solid var(--border);
  overflow: hidden;
  transition: all 0.15s;
}
.picker-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}
.picker-thumb {
  aspect-ratio: 4 / 5;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  display: grid;
  place-items: center;
  position: relative;
}
.cat {
  position: absolute;
  bottom: 8px;
  right: 8px;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #fff;
  background: rgba(0, 0, 0, 0.4);
  padding: 3px 8px;
  border-radius: 999px;
}
.picker-name {
  padding: 6px 10px 10px;
  font-size: 13px;
  font-weight: 600;
  text-align: left;
  color: var(--text);
}
</style>
