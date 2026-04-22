import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3040,
    proxy: {
      '/inventory':  { target: 'http://localhost:8090', changeOrigin: true },
      '/health':     { target: 'http://localhost:8090', changeOrigin: true },
      '/docs':       { target: 'http://localhost:8090', changeOrigin: true },
      '/openapi.json': { target: 'http://localhost:8090', changeOrigin: true },
    }
  }
})
