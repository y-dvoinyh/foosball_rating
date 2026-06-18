import { fileURLToPath } from 'node:url';

import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      boot: fileURLToPath(new URL('./src/boot', import.meta.url)),
      src: fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts']
  }
});
