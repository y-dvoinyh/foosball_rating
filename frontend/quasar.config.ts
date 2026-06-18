import { configure } from 'quasar/wrappers';

export default configure(() => ({
  boot: ['axios'],
  css: ['app.scss'],
  extras: ['roboto-font', 'material-icons'],
  build: {
    target: {
      browser: ['es2022', 'firefox115', 'chrome115', 'safari14'],
      node: 'node20'
    },
    vueRouterMode: 'history'
  },
  devServer: {
    open: false,
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_DEV_API_PROXY_TARGET || 'http://backend:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  framework: {
    config: {},
    plugins: []
  }
}));
