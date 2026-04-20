<template>
  <div class="card" style="padding:0;overflow:hidden">
    <table>
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" :style="col.width ? `width:${col.width}` : ''">
            {{ col.label }}
          </th>
          <th v-if="$slots.actions" style="width:120px;text-align:right">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td v-for="col in columns" :key="col.key">
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
          <td v-if="$slots.actions" style="text-align:right">
            <slot name="actions" :row="row" />
          </td>
        </tr>
        <tr v-if="!rows.length">
          <td :colspan="columns.length + ($slots.actions ? 1 : 0)" style="text-align:center;color:var(--text3);padding:2rem">
            Sin datos.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns: { type: Array, required: true }, // [{ key, label, width? }]
  rows: { type: Array, default: () => [] },
})
</script>
