import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
    // When running Vite inside WSL against files on the Windows mount
    // (e.g. /mnt/c/...), inotify events may not fire. Enable polling
    // so HMR reliably detects file saves.
    watch: {
      usePolling: true,
      interval: 100,
    },
    hmr: {
      // ensures websocket HMR connects correctly from the browser
      host: 'localhost',
    },
  },
  build: {
    sourcemap: true,
  },
})
