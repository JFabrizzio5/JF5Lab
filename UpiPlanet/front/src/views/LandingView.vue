<template>
  <TopNav />

  <main class="relative mx-auto max-w-6xl px-6">
    <section class="grid gap-10 py-20 md:grid-cols-[1.15fr_1fr] md:items-center md:py-28">
      <div>
        <span class="upi-chip upi-fade-up">
          <i class="mdi mdi-star-four-points"></i> Red social con órbita propia
        </span>
        <h1 class="mt-5 text-[clamp(44px,6vw,72px)] font-semibold leading-[1.02] tracking-[-0.02em] text-white upi-fade-up delay-1">
          Tu universo social.<br />
          <span class="upi-glow-text">Sin ruido, con vida.</span>
        </h1>
        <p class="mt-6 max-w-xl text-[17px] leading-relaxed text-ink-200 upi-fade-up delay-2">
          Feed cronológico, conversaciones reales y una IA que ayuda solo cuando se lo pides. Diseñado para respirar en la oscuridad del espacio.
        </p>
        <div class="mt-8 flex flex-wrap items-center gap-3 upi-fade-up delay-3">
          <router-link to="/auth" class="upi-btn-primary">
            <i class="mdi mdi-arrow-right-thin"></i> Crear mi planeta
          </router-link>
          <router-link to="/feed" class="upi-btn-ghost">
            <i class="mdi mdi-telescope"></i> Ver el feed
          </router-link>
        </div>
        <div class="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-[13px] text-ink-300">
          <span class="inline-flex items-center gap-1.5"><i class="mdi mdi-shield-check text-upi-300"></i> Privacidad primero</span>
          <span class="inline-flex items-center gap-1.5"><i class="mdi mdi-heart-pulse text-upi-300"></i> Sin métricas vanidosas</span>
          <span class="inline-flex items-center gap-1.5"><i class="mdi mdi-sparkles text-upi-300"></i> IA opcional</span>
        </div>
      </div>

      <div class="relative hidden md:block">
        <div class="upi-orbit">
          <div class="ring"></div>
          <div class="ring slow"></div>
          <div class="planet"></div>
          <div class="moon"></div>
        </div>
      </div>
    </section>

    <section class="grid gap-4 pb-14 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="(f, i) in features" :key="f.t" class="upi-card upi-card-lift p-6 upi-fade-up" :style="`animation-delay:${i*0.08}s`">
        <div class="grid h-11 w-11 place-items-center rounded-xl bg-upi-500/15 text-upi-200 border border-upi-400/30">
          <i :class="`mdi mdi-${f.i} text-[20px]`"></i>
        </div>
        <h3 class="mt-4 text-[15px] font-semibold text-white">{{ f.t }}</h3>
        <p class="mt-1.5 text-[13px] leading-relaxed text-ink-200">{{ f.d }}</p>
      </div>
    </section>

    <footer class="flex flex-col items-center gap-1 border-t border-white/5 py-10 text-center text-[13px] text-ink-300">
      <span class="inline-flex items-center gap-1.5"><i class="mdi mdi-orbit text-upi-300"></i> UpiPlanet · órbita morada</span>
      <span class="text-ink-400">{{ year }} · hecho con CometaX</span>
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
  { i: 'clock-time-eight-outline', t: 'Feed cronológico', d: 'Lo que sigues, cuando pasa. Sin algoritmo que decida por ti.' },
  { i: 'sparkles-outline',         t: 'IA a demanda',     d: 'Resúmenes y sugerencias solo cuando las pides. Nunca impuestas.' },
  { i: 'account-group-outline',    t: 'Conversación',     d: 'Hilos pensados para responder, no para scrollear vacío.' },
  { i: 'shield-lock-outline',      t: 'Privado por diseño', d: 'Sin trackers de terceros. Visibilidad fina en cada post.' },
];

onMounted(() => session.rehydrate());
</script>
