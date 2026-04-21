import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3055,
    proxy: {
      '/agenda': { target: 'http://api:8000', changeOrigin: true },
      '/health': { target: 'http://api:8000', changeOrigin: true },
      '/docs':   { target: 'http://api:8000', changeOrigin: true },
      '/openapi.json': { target: 'http://api:8000', changeOrigin: true },
    }
  }
})
