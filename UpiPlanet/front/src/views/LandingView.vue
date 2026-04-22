<template>
  <TopNav />

  <main class="mx-auto max-w-5xl px-6">
    <section class="py-24 md:py-32">
      <h1 class="max-w-3xl text-[clamp(40px,6vw,72px)] font-semibold leading-[1.02] tracking-[-0.02em] text-ink-900">
        Una red social sin ruido.
      </h1>
      <p class="mt-6 max-w-xl text-[17px] leading-relaxed text-ink-500">
        Conversaciones reales, feed cronológico y una IA que ayuda solo cuando se lo pides.
      </p>
      <div class="mt-9 flex flex-wrap items-center gap-3">
        <router-link to="/auth" class="upi-btn-primary">Crear cuenta</router-link>
        <router-link to="/feed" class="upi-btn-ghost">Ver el feed</router-link>
      </div>
    </section>

    <section class="grid gap-px overflow-hidden rounded-2xl border border-ink-100 bg-ink-100 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="f in features" :key="f.t" class="bg-white p-6">
        <i :class="`mdi mdi-${f.i} text-[20px] text-ink-900`"></i>
        <h3 class="mt-4 text-[14px] font-semibold text-ink-900">{{ f.t }}</h3>
        <p class="mt-1.5 text-[13px] leading-relaxed text-ink-500">{{ f.d }}</p>
      </div>
    </section>

    <footer class="mt-24 flex items-center justify-between border-t border-ink-100 py-8 text-[12px] text-ink-400">
      <span>UpiPlanet · {{ year }}</span>
      <span>hecho con CometaX</span>
    </footer>
  </main>
</template>

<script setup>
import { onMounted } from 'vue';
import TopNav from '../components/TopNav.vue';
import { useSession } from '../stores/session';

const session = useSession();
const year = new Date().getFullYear();

const features = [
  { i: 'circle-small',         t: 'Sin algoritmo',     d: 'Feed cronológico. Lo que sigues, cuando pasa.' },
  { i: 'sparkles-outline',     t: 'IA opcional',       d: 'Resumen y sugerencias a demanda. Nunca impuestas.' },
  { i: 'lock-outline',         t: 'Privado por diseño', d: 'Sin trackers. Control de visibilidad por post.' },
  { i: 'account-multiple-outline', t: 'Conversación',  d: 'Pensado para hilos, no para métricas vanidosas.' },
];

onMounted(() => session.rehydrate());
</script>
