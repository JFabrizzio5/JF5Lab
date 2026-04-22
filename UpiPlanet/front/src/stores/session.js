import { defineStore } from 'pinia';
import { me as fetchMe } from '../api/upi';

export const useSession = defineStore('session', {
  state: () => ({
    user: null,
    ready: false
  }),
  getters: {
    authed: (s) => !!s.user
  },
  actions: {
    setAuth(user, token) {
      this.user = user;
      if (token) localStorage.setItem('upi_token', token);
    },
    logout() {
      this.user = null;
      localStorage.removeItem('upi_token');
    },
    async rehydrate() {
      const t = localStorage.getItem('upi_token');
      if (!t) { this.ready = true; return; }
      try { this.user = await fetchMe(); }
      catch { localStorage.removeItem('upi_token'); this.user = null; }
      this.ready = true;
    }
  }
});
