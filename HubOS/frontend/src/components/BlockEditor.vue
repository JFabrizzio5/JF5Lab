<template>
  <div class="block-editor">
    <div class="toolbar">
      <button v-for="t in types" :key="t.type" @click="addBlock(t.type)" class="tool-btn" :title="t.label">
        <i :data-lucide="t.icon" class="lucide-icon" style="width:14px;height:14px"></i>
        {{ t.label }}
      </button>
    </div>

    <div class="blocks">
      <div v-for="(b, i) in model" :key="i" class="block" :class="`block-${b.type}`">
        <div class="block-head">
          <span class="block-type">{{ labelFor(b.type) }}</span>
          <div class="block-actions">
            <button @click="move(i, -1)" :disabled="i === 0" class="mini-btn">
              <i data-lucide="chevron-up" class="lucide-icon" style="width:14px;height:14px"></i>
            </button>
            <button @click="move(i, 1)" :disabled="i === model.length - 1" class="mini-btn">
              <i data-lucide="chevron-down" class="lucide-icon" style="width:14px;height:14px"></i>
            </button>
            <button @click="remove(i)" class="mini-btn danger">
              <i data-lucide="trash-2" class="lucide-icon" style="width:14px;height:14px"></i>
            </button>
          </div>
        </div>

        <input v-if="b.type === 'heading'" v-model="b.content" placeholder="Encabezado" class="block-heading" />
        <textarea v-else-if="b.type === 'text' || b.type === 'callout'" v-model="b.content" rows="3" :placeholder="b.type === 'callout' ? 'Nota destacada…' : 'Texto…'" />
        <textarea v-else-if="b.type === 'code'" v-model="b.content" rows="5" class="mono" placeholder="Código…" />
        <input v-else-if="b.type === 'image'" v-model="b.content" placeholder="URL de la imagen" />
        <input v-else-if="b.type === 'divider'" disabled value="— separador —" class="disabled" />
      </div>
      <div v-if="!model.length" class="empty-state">Agrega bloques desde la barra superior.</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const props = defineProps({ modelValue: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue'])

const model = props.modelValue  // bound by reference; parents treat array as source of truth

const types = [
  { type: 'heading', label: 'Título', icon: 'heading' },
  { type: 'text', label: 'Texto', icon: 'type' },
  { type: 'callout', label: 'Callout', icon: 'megaphone' },
  { type: 'code', label: 'Código', icon: 'code' },
  { type: 'image', label: 'Imagen', icon: 'image' },
  { type: 'divider', label: 'Separador', icon: 'minus' },
]

function labelFor(t) { return (types.find(x => x.type === t) || {}).label || t }

function addBlock(type) {
  model.push({ type, content: '' })
  emit('update:modelValue', model)
  setTimeout(refresh, 10)
}
function move(i, delta) {
  const j = i + delta
  if (j < 0 || j >= model.length) return
  const [it] = model.splice(i, 1)
  model.splice(j, 0, it)
  emit('update:modelValue', model)
}
function remove(i) {
  model.splice(i, 1)
  emit('update:modelValue', model)
}
function refresh() { if (window.lucide) window.lucide.createIcons() }
onMounted(refresh)
</script>

<style scoped>
.block-editor { display: flex; flex-direction: column; gap: 0.75rem; }
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding: 0.6rem;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 10px;
}
.tool-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  padding: 0.35rem 0.7rem;
  border-radius: 7px;
  font-size: 0.75rem;
  font-weight: 500;
}
.tool-btn:hover { border-color: var(--primary); color: var(--text); }

.blocks { display: flex; flex-direction: column; gap: 0.6rem; }
.block {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.block-head { display: flex; justify-content: space-between; align-items: center; }
.block-type {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text3);
  font-weight: 700;
}
.block-actions { display: flex; gap: 0.25rem; }
.mini-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.mini-btn:hover { border-color: var(--primary); color: var(--text); }
.mini-btn.danger:hover { border-color: var(--danger); color: var(--danger); }
.mini-btn:disabled { opacity: 0.35; }

.block-heading { font-size: 1.1rem; font-weight: 700; }
.block-callout textarea { border-left: 3px solid var(--accent); padding-left: 0.7rem; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82rem; }
.disabled { opacity: 0.5; text-align: center; letter-spacing: 0.1em; }
.empty-state { text-align: center; color: var(--text3); padding: 2rem; border: 1px dashed var(--border); border-radius: 10px; }
</style>
