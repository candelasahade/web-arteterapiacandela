import { watch } from 'vue'
import {
  i18n,
  LOCALE_STORAGE_KEY,
  SUPPORTED_LOCALES,
  type AppLocale,
} from './index'

function isSupportedLocale(value: string | null): value is AppLocale {
  return SUPPORTED_LOCALES.includes(value as AppLocale)
}

function detectInitialLocale(): AppLocale {
  const stored = localStorage.getItem(LOCALE_STORAGE_KEY)
  if (isSupportedLocale(stored)) return stored
  return navigator.language.toLowerCase().startsWith('ca') ? 'ca' : 'es'
}

export function initLocaleClientSync() {
  i18n.global.locale.value = detectInitialLocale()

  watch(
    i18n.global.locale,
    (value) => {
      document.documentElement.lang = value === 'ca' ? 'ca-ES' : 'es-ES'
      localStorage.setItem(LOCALE_STORAGE_KEY, value)

      const t = i18n.global.t
      document.title = t('meta.title')
      const descEl = document.querySelector<HTMLMetaElement>('meta[name="description"]')
      if (descEl) descEl.content = t('meta.description')
    },
    { immediate: true },
  )
}
