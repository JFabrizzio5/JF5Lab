<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
      <div class="modal">
        <div class="modal-head">
          <h2>{{ title }}</h2>
          <button @click="close" class="close-btn">
            <i data-lucide="x" class="lucide-icon" style="width:18px;height:18px"></i>
          </button>
        </div>
        <slot />
        <div v-if="$slots.footer" class="modal-footer">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { onMounted, watch } from 'vue'
const props = defineProps({ modelValue: Boolean, title: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue'])
function close() { emit('update:modelValue', false) }
function refresh() { if (window.lucide) window.lucide.createIcons() }
onMounted(refresh)
watch(() => props.modelValue, refresh)
</script>

<style scoped>
.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.close-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  width: 30px;
  height: 30px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover { color: var(--danger); border-color: var(--danger); }
</style>
