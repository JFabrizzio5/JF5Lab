<template>
  <TopNav />
  <main class="mx-auto max-w-md px-6 py-16">
    <div class="upi-card p-8 upi-fade-up">
      <div class="mb-1 flex items-center gap-2 text-[12px] font-semibold uppercase tracking-wider text-upi-300">
        <i class="mdi mdi-orbit"></i> UpiPlanet
      </div>
      <h1 class="text-[24px] font-semibold tracking-tight text-white">
        <span class="upi-glow-text">{{ mode === 'login' ? 'Regresa a tu órbita' : 'Crea tu planeta' }}</span>
      </h1>
      <p class="mt-1.5 text-[14px] text-ink-200">
        {{ mode === 'login' ? 'Usa tu cuenta existente.' : 'Tu identidad viaja contigo. Elige un ícono.' }}
      </p>

      <div class="mt-6 grid grid-cols-2 gap-1 rounded-xl border border-white/10 bg-white/5 p-1">
        <button :class="['tab', mode === 'login' && 'tab-on']" @click="mode = 'login'">
          <i class="mdi mdi-login-variant"></i> Entrar
        </button>
        <button :class="['tab', mode === 'register' && 'tab-on']" @click="mode = 'register'">
          <i class="mdi mdi-account-plus-outline"></i> Crear
        </button>
      </div>

      <form v-if="mode === 'login'" @submit.prevent="doLogin" class="mt-6 space-y-4">
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Usuario</span>
          <input v-model="form.username" class="upi-input" placeholder="nova" required />
        </label>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Contraseña</span>
          <input v-model="form.password" type="password" class="upi-input" placeholder="••••••" required />
        </label>
        <button type="submit" :disabled="busy" class="upi-btn-primary w-full">
          <i class="mdi mdi-arrow-right-thin"></i> Entrar
        </button>
        <p class="text-center text-[12px] text-ink-300">
          Demo: <code class="rounded bg-upi-500/15 px-1.5 py-0.5 text-upi-200 border border-upi-400/30">nova</code> /
          <code class="rounded bg-upi-500/15 px-1.5 py-0.5 text-upi-200 border border-upi-400/30">upiplanet</code>
        </p>
      </form>

      <form v-else @submit.prevent="doRegister" class="mt-6 space-y-4">
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Usuario</span>
          <input v-model="reg.username" class="upi-input" pattern="[a-zA-Z0-9_]+" minlength="3" maxlength="32" required />
        </label>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Nombre visible</span>
          <input v-model="reg.display_name" class="upi-input" maxlength="80" required />
        </label>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Bio · opcional</span>
          <input v-model="reg.bio" class="upi-input" maxlength="280" />
        </label>
        <div>
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Ícono</span>
          <div class="grid grid-cols-6 gap-1.5">
            <button type="button" v-for="i in iconOptions" :key="i"
              :class="['icon-opt', reg.avatar_icon === i && 'icon-on']"
              @click="reg.avatar_icon = i">
              <i :class="`mdi mdi-${i}`"></i>
            </button>
          </div>
        </div>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-semibold text-ink-200">Contraseña</span>
          <input v-model="reg.password" type="password" class="upi-input" minlength="6" required />
        </label>
        <button type="submit" :disabled="busy" class="upi-btn-primary w-full">
          <i class="mdi mdi-account-star-outline"></i> Crear cuenta
        </button>
      </form>

      <p v-if="err" class="mt-4 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-center text-[13px] text-rose-300">
        {{ err }}
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import TopNav from '../components/TopNav.vue';
import { login, register } from '../api/upi';
import { useSession } from '../stores/session';

const mode = ref('login');
const session = useSession();
const router = useRouter();
const busy = ref(false);
const err = ref('');
const form = ref({ username: '', password: '' });
const reg = ref({ username: '', display_name: '', bio: '', password: '', avatar_icon: 'rocket-launch' });
const iconOptions = ['rocket-launch', 'star-four-points', 'music', 'palette', 'account-heart', 'earth', 'white-balance-sunny', 'shimmer', 'cat', 'coffee', 'lightning-bolt', 'camera'];

async function doLogin() {
  busy.value = true; err.value = '';
  try {
    const r = await login(form.value);
    session.setAuth(r.user, r.token);
    router.push('/feed');
  } catch (e) { err.value = e.response?.data?.detail || 'error'; }
  finally { busy.value = false; }
}
async function doRegister() {
  busy.value = true; err.value = '';
  try {
    const r = await register(reg.value);
    session.setAuth(r.user, r.token);
    router.push('/feed');
  } catch (e) { err.value = e.response?.data?.detail || 'error'; }
  finally { busy.value = false; }
}
</script>

<style scoped>
@reference "../styles.css";
.tab {
  @apply inline-flex items-center justify-center gap-1.5 rounded-lg py-2 text-[13px] font-semibold text-ink-200 transition-colors;
}
.tab-on {
  @apply text-white;
  background: linear-gradient(135deg, var(--color-upi-500), var(--color-upi-700));
  box-shadow: 0 4px 14px -4px rgba(109,53,255,0.7);
}
.icon-opt {
  @apply grid place-items-center rounded-lg border border-white/10 bg-white/5 py-2.5 text-[18px] text-ink-200 transition-colors;
}
.icon-opt:hover { @apply text-upi-200 border-upi-400/40 bg-upi-500/10; }
.icon-on {
  @apply text-white;
  background: linear-gradient(135deg, var(--color-upi-500), var(--color-upi-700)) !important;
  border-color: var(--color-upi-400) !important;
  box-shadow: 0 4px 14px -4px rgba(109,53,255,0.6);
}
</style>
