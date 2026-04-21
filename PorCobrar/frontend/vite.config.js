import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3060,
    proxy: {
      '/cobrar': { target: 'http://localhost:8130', changeOrigin: true },
      '/health': { target: 'http://localhost:8130', changeOrigin: true },
      '/docs':   { target: 'http://localhost:8130', changeOrigin: true },
      '/openapi.json': { target: 'http://localhost:8130', changeOrigin: true },
    }
  }
})
