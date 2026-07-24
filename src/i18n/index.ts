import { createI18n } from 'vue-i18n'
import es from './locales/es.json'
import ca from './locales/ca.json'

export const SUPPORTED_LOCALES = ['es', 'ca'] as const
export type AppLocale = (typeof SUPPORTED_LOCALES)[number]

export const DEFAULT_LOCALE: AppLocale = 'es'
export const LOCALE_STORAGE_KEY = 'arteterapiacandela:locale'

export const i18n = createI18n({
  legacy: false,
  locale: DEFAULT_LOCALE,
  fallbackLocale: DEFAULT_LOCALE,
  messages: { es, ca },
})
