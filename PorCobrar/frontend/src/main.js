import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import '@mdi/font/css/materialdesignicons.css'
import './assets/styles.css'

// Theme: dark default, toggle persistente
const saved = localStorage.getItem('pc_theme') || 'dark'
document.documentElement.setAttribute('data-theme', saved)

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
