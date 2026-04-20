import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import './style.css'

// One-time migration: wipe legacy localStorage tokens (now stored in sessionStorage).
try { localStorage.removeItem('hubos_token'); localStorage.removeItem('hubos_user') } catch {}

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
