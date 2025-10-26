import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/method': 'http://localhost:8000',
      '/socket.io': {
        target: 'http://localhost:8000',
        ws: true
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
