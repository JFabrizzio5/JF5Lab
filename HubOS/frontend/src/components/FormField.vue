<template>
  <div class="form-group" style="margin-bottom:0.9rem">
    <label v-if="label">{{ label }}<span v-if="required" style="color:var(--danger)"> *</span></label>
    <textarea v-if="type === 'textarea'" v-model="proxy" :rows="rows" :placeholder="placeholder" />
    <select v-else-if="type === 'select'" v-model="proxy">
      <option v-for="o in options" :key="o.value ?? o" :value="o.value ?? o">{{ o.label ?? o }}</option>
    </select>
    <input v-else :type="type" v-model="proxy" :placeholder="placeholder" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  modelValue: { type: [String, Number, Boolean], default: '' },
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  rows: { type: Number, default: 3 },
  options: { type: Array, default: () => [] },
  required: Boolean,
})
const emit = defineEmits(['update:modelValue'])
const proxy = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})
</script>
