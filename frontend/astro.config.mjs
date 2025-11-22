// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default {
  devToolbar: {
    enabled: false,
  },

  server: {
    host: true,
    port: 4321
  },

  vite: {
    plugins: [tailwindcss()],
  }
};