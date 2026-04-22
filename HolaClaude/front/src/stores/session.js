import { defineStore } from 'pinia';

export const useSession = defineStore('session', {
  state: () => ({
    token: '',
    enrolled: false,
    disabled: false,
    verifiedAt: 0,
    gestures: [],
    messages: []
  }),
  actions: {
    setToken(t) { this.token = t; this.verifiedAt = Date.now(); },
    clearToken() { this.token = ''; this.verifiedAt = 0; },
    addMessage(m) { this.messages.push({ ...m, t: Date.now() }); if (this.messages.length > 60) this.messages.shift(); }
  }
});
