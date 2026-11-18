import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Cross-Origin Isolation headers required for SharedArrayBuffer (FFmpeg.wasm)
const coiHeaders = {
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Embedder-Policy': 'require-corp',
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    headers: coiHeaders,
  },
  preview: {
    headers: coiHeaders,
  },
  optimizeDeps: {
    exclude: ['@ffmpeg/ffmpeg', '@ffmpeg/util']
  }
})
