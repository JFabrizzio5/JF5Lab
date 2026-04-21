import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3045,
    proxy: {
      '/membership': { target: 'http://localhost:8100', changeOrigin: true },
      '/billing':    { target: 'http://localhost:8100', changeOrigin: true, rewrite: p => p.replace(/^\/billing/, '/membership/v1/billing') },
      '/health':     { target: 'http://localhost:8100', changeOrigin: true },
      '/docs':       { target: 'http://localhost:8100', changeOrigin: true },
      '/openapi.json': { target: 'http://localhost:8100', changeOrigin: true },
    }
  }
})
