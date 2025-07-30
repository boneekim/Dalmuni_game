import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // 상대 경로로 설정 (인라인 시에도 일관성을 위해 유지)
  build: {
    assetsInlineLimit: 10000000, // 10MB, 모든 자산을 인라인하도록 매우 큰 값으로 설정
  },
})
