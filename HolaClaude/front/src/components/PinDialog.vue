<template>
  <div class="mask" @click.self="$emit('close')">
    <div class="card dialog">
      <h3><i class="mdi mdi-lock-question"></i> PIN requerido</h3>
      <p class="muted">PIN de 8 dígitos. Desactiva o reenrola rostro.</p>
      <input v-model="pin" type="password" inputmode="numeric" maxlength="8" placeholder="••••••••" />
      <div class="actions">
        <button class="ghost" @click="$emit('close')">Cancelar</button>
        <button @click="$emit('disable', pin)" :disabled="pin.length !== 8">
          <i class="mdi mdi-power"></i> Deshabilitar
        </button>
        <button @click="$emit('reset', pin)" :disabled="pin.length !== 8">
          <i class="mdi mdi-refresh"></i> Reenrolar rostro
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
defineEmits(['close', 'disable', 'reset']);
const pin = ref('');
</script>

<style scoped>
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 50; }
.dialog { width: 360px; max-width: 92vw; display: flex; flex-direction: column; gap: 12px; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
.ghost { background: transparent; border-color: var(--border); }
</style>
