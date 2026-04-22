<template>
  <TopNav />
  <main class="mx-auto max-w-5xl px-6 py-6">
    <div class="upi-card flex items-center gap-3 px-5 py-3">
      <i class="mdi mdi-magnify text-xl text-upi-300"></i>
      <input
        v-model="q"
        @input="onSearch"
        class="w-full border-none bg-transparent text-[15px] text-white placeholder:text-ink-300 focus:outline-none"
        placeholder="Busca habitantes por nombre o usuario"
      />
    </div>

    <section class="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="(u, i) in users" :key="u.id"
        :to="`/u/${u.username}`"
        class="upi-card upi-card-lift p-5 upi-fade-up"
        :style="`animation-delay:${Math.min(i*0.04, 0.4)}s`"
      >
        <div class="flex items-start gap-3">
          <span class="upi-avatar h-14 w-14 text-[26px]"><i :class="`mdi mdi-${u.avatar_icon}`"></i></span>
          <div class="min-w-0">
            <div class="truncate text-[15px] font-semibold text-white">{{ u.display_name }}</div>
            <div class="truncate text-[12.5px] text-ink-300">@{{ u.username }}</div>
          </div>
        </div>
        <p class="mt-3 line-clamp-2 text-[13.5px] text-ink-200">{{ u.bio || '— sin bio —' }}</p>
      </router-link>
    </section>

    <p v-if="!users.length" class="py-16 text-center text-[13px] text-ink-300">
      <i class="mdi mdi-account-question-outline"></i> Sin resultados.
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
