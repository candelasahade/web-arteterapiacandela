import { ViteSSG } from 'vite-ssg/single-page'
import App from './App.vue'
import { i18n } from './i18n'
import { initLocaleClientSync } from './i18n/clientSync'
import './components/base/base.css'

export const createApp = ViteSSG(App, ({ app }) => {
  app.use(i18n)
  if (!import.meta.env.SSR) {
    initLocaleClientSync()
  }
})
