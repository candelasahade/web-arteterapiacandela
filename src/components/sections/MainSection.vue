<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'

const { t, tm } = useI18n()

const phraseLines = computed(() => tm('main.phraseLines') as string[])
</script>

<template>
  <BaseSection id="main" :full-height="true">
    <div class="main-section">
      <div class="main-section__text">
        <p class="main-section__eyebrow">{{ t('main.eyebrow') }}</p>
        <h1 class="main-section__phrase">
          <template v-for="(line, i) in phraseLines" :key="i"
            >{{ line }}<br v-if="i < phraseLines.length - 1"
          /></template>
        </h1>
        <p class="main-section__lead">
          {{ t('main.lead') }}
        </p>
        <a class="main-section__cta" href="#contacto">{{ t('main.cta') }}</a>
      </div>

      <img
        class="main-section__visual"
        src="/hero-1600.webp"
        srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1600.webp 1600w"
        sizes="(min-width: 768px) 480px, 420px"
        width="1600"
        height="1600"
        :alt="t('main.visualAlt')"
        decoding="async"
        fetchpriority="high"
      />
    </div>
  </BaseSection>
</template>

<style scoped>
.main-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  width: 100%;
}

.main-section__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
  text-align: center;
}

.main-section__eyebrow {
  font-family: var(--font-sans);
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-secondary);
  margin: 0;
}

.main-section__phrase {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(2rem, 5vw + 0.75rem, 3.5rem);
  line-height: 1.2;
  margin: 0;
  color: var(--color-text);
}

.main-section__lead {
  font-family: var(--font-sans);
  font-size: clamp(1rem, 1vw + 0.875rem, 1.125rem);
  line-height: 1.7;
  color: var(--color-text-light);
  max-width: 42ch;
  margin: 0;
}

.main-section__cta {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.9375rem 2rem;
  background-color: var(--color-accent);
  color: var(--color-surface);
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 0.9375rem;
  text-decoration: none;
  border-radius: 999px;
  letter-spacing: 0.02em;
  box-shadow: 0 4px 16px
    color-mix(in srgb, var(--color-accent) 30%, transparent);
  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.main-section__cta:hover,
.main-section__cta:focus-visible {
  background-color: color-mix(in srgb, var(--color-accent) 85%, black);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px
    color-mix(in srgb, var(--color-accent) 40%, transparent);
}

/* Dibujo principal — mismo hueco que ocupaba la composición abstracta */
.main-section__visual {
  flex-shrink: 0;
  width: min(420px, 100%);
  height: auto;
  aspect-ratio: 1;
  object-fit: contain;
}

@media (min-width: 768px) {
  .main-section {
    flex-direction: row;
    gap: 4rem;
  }

  .main-section__text {
    flex: 1;
    align-items: flex-start;
    text-align: left;
  }

  .main-section__visual {
    width: min(480px, 46%);
  }
}
</style>
