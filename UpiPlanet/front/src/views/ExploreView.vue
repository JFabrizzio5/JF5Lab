<template>
  <TopNav />
  <main class="mx-auto max-w-4xl px-6 py-8">
    <div class="upi-card flex items-center gap-3 px-5 py-3">
      <i class="mdi mdi-magnify text-[18px] text-ink-400"></i>
      <input
        v-model="q"
        @input="onSearch"
        class="w-full border-none bg-transparent text-[14.5px] text-ink-900 placeholder:text-ink-400 focus:outline-none"
        placeholder="Buscar personas"
      />
    </div>

    <section class="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="u in users" :key="u.id"
        :to="`/u/${u.username}`"
        class="upi-card p-5 transition-colors hover:border-ink-300"
      >
        <div class="flex items-start gap-3">
          <span class="upi-avatar h-11 w-11 text-[18px]"><i :class="`mdi mdi-${u.avatar_icon}`"></i></span>
          <div class="min-w-0">
            <div class="truncate text-[14.5px] font-semibold text-ink-900">{{ u.display_name }}</div>
            <div class="truncate text-[12.5px] text-ink-400">@{{ u.username }}</div>
          </div>
        </div>
        <p class="mt-3 line-clamp-2 text-[13px] text-ink-500">{{ u.bio || '—' }}</p>
      </router-link>
    </section>

    <p v-if="!users.length" class="py-20 text-center text-[13px] text-ink-400">
      Sin resultados.
    </p>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import TopNav from '../components/TopNav.vue';
import { searchUsers } from '../api/upi';

const q = ref('');
const users = ref([]);
let tmr;

async function load() { users.value = await searchUsers(q.value); }
function onSearch() { clearTimeout(tmr); tmr = setTimeout(load, 220); }
onMounted(load);
</script>
