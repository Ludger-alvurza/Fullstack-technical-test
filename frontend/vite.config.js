import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/login': 'http://localhost:8000',
      '/sales': 'http://localhost:8000',
      '/predict': 'http://localhost:8000',
    },
  },
})
