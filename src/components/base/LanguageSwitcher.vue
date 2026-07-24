<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { AppLocale } from '@/i18n'

const { locale } = useI18n({ useScope: 'global' })

function setLocale(value: AppLocale) {
  locale.value = value
}
</script>

<template>
  <div class="lang-switcher" role="group" aria-label="Idioma / Idioma">
    <button
      type="button"
      class="lang-switcher__btn"
      :class="{ 'lang-switcher__btn--active': locale === 'es' }"
      :aria-pressed="locale === 'es'"
      aria-label="Español"
      @click="setLocale('es')"
    >
      <svg class="lang-switcher__flag" viewBox="0 0 27 18" aria-hidden="true">
        <rect width="27" height="18" fill="#AA151B" />
        <rect y="4.5" width="27" height="9" fill="#F1BF00" />
      </svg>
    </button>
    <button
      type="button"
      class="lang-switcher__btn"
      :class="{ 'lang-switcher__btn--active': locale === 'ca' }"
      :aria-pressed="locale === 'ca'"
      aria-label="Català"
      @click="setLocale('ca')"
    >
      <svg class="lang-switcher__flag" viewBox="0 0 27 18" aria-hidden="true">
        <rect width="27" height="18" fill="#FFD400" />
        <rect y="2" width="27" height="2" fill="#DA121A" />
        <rect y="6" width="27" height="2" fill="#DA121A" />
        <rect y="10" width="27" height="2" fill="#DA121A" />
        <rect y="14" width="27" height="2" fill="#DA121A" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.lang-switcher {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.lang-switcher__btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.75rem;
  height: 2.75rem;
  padding: 0;
  background: none;
  border: 1.5px solid transparent;
  border-radius: 0.5rem;
  cursor: pointer;
  opacity: 0.55;
  transition:
    opacity 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.lang-switcher__btn:hover {
  opacity: 0.85;
}

.lang-switcher__btn--active {
  opacity: 1;
  border-color: var(--color-accent);
  transform: scale(1.05);
}

.lang-switcher__flag {
  width: 1.5rem;
  height: 1rem;
  border-radius: 0.125rem;
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--color-text) 15%, transparent);
}
</style>
