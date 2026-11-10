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
  const browserLang = navigator.language.toLowerCase()
  if (browserLang.startsWith('ca')) return 'ca'
  if (browserLang.startsWith('en')) return 'en'
  return 'es'
}

const HTML_LANG: Record<AppLocale, string> = {
  es: 'es-ES',
  ca: 'ca-ES',
  en: 'en',
}

export function initLocaleClientSync() {
  i18n.global.locale.value = detectInitialLocale()

  watch(
    i18n.global.locale,
    (value) => {
      document.documentElement.lang = HTML_LANG[value as AppLocale]
      localStorage.setItem(LOCALE_STORAGE_KEY, value)

      const t = i18n.global.t
      document.title = t('meta.title')
      const descEl = document.querySelector<HTMLMetaElement>('meta[name="description"]')
      if (descEl) descEl.content = t('meta.description')
    },
    { immediate: true },
  )
}
