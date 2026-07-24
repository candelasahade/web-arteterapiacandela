import { ViteSSG } from 'vite-ssg/single-page'
import App from './App.vue'
import './components/base/base.css'

export const createApp = ViteSSG(App)
