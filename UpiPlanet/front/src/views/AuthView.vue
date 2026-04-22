<template>
  <TopNav />
  <main class="mx-auto max-w-md px-6 py-20">
    <div class="upi-card p-8">
      <h1 class="text-[22px] font-semibold tracking-tight text-ink-900">
        {{ mode === 'login' ? 'Entrar' : 'Crear cuenta' }}
      </h1>
      <p class="mt-1.5 text-[13.5px] text-ink-500">
        {{ mode === 'login' ? 'Accede con tu usuario.' : 'Elige un nombre y un ícono.' }}
      </p>

      <div class="mt-6 grid grid-cols-2 gap-1 rounded-xl bg-ink-100 p-1">
        <button :class="['tab', mode === 'login' && 'tab-on']" @click="mode = 'login'">Entrar</button>
        <button :class="['tab', mode === 'register' && 'tab-on']" @click="mode = 'register'">Crear</button>
      </div>

      <form v-if="mode === 'login'" @submit.prevent="doLogin" class="mt-6 space-y-4">
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Usuario</span>
          <input v-model="form.username" class="upi-input" required />
        </label>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Contraseña</span>
          <input v-model="form.password" type="password" class="upi-input" required />
        </label>
        <button type="submit" :disabled="busy" class="upi-btn-primary w-full">Entrar</button>
      </form>

      <form v-else @submit.prevent="doRegister" class="mt-6 space-y-4">
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Usuario</span>
          <input v-model="reg.username" class="upi-input" pattern="[a-zA-Z0-9_]+" minlength="3" maxlength="32" required />
        </label>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Nombre visible</span>
          <input v-model="reg.display_name" class="upi-input" maxlength="80" required />
        </label>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Bio · opcional</span>
          <input v-model="reg.bio" class="upi-input" maxlength="280" />
        </label>
        <div>
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Ícono</span>
          <div class="grid grid-cols-6 gap-1.5">
            <button type="button" v-for="i in iconOptions" :key="i"
              :class="['icon-opt', reg.avatar_icon === i && 'icon-on']"
              @click="reg.avatar_icon = i">
              <i :class="`mdi mdi-${i}`"></i>
            </button>
          </div>
        </div>
        <label class="block">
          <span class="mb-1.5 block text-[12px] font-medium text-ink-500">Contraseña</span>
          <input v-model="reg.password" type="password" class="upi-input" minlength="6" required />
        </label>
        <button type="submit" :disabled="busy" class="upi-btn-primary w-full">Crear cuenta</button>
      </form>

      <p v-if="err" class="mt-4 rounded-lg bg-rose-50 px-3 py-2 text-center text-[13px] text-rose-700">
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
  @apply inline-flex items-center justify-center rounded-lg py-2 text-[13px] font-medium text-ink-500 transition-colors;
}
.tab-on { @apply bg-white text-ink-900 shadow-sm; }
.icon-opt {
  @apply grid place-items-center rounded-lg bg-white py-2.5 text-[16px] text-ink-500 border border-ink-200 transition-colors hover:border-ink-400 hover:text-ink-900;
}
.icon-on { @apply bg-ink-900 text-white border-ink-900; }
</style>
