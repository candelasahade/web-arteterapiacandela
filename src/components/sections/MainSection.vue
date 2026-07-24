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

      <!-- Abstract art composition — replaced by a real photo when available -->
      <div
        class="main-section__visual"
        role="img"
        :aria-label="t('main.visualAlt')"
      >
        <div class="main-section__paint main-section__paint--1"></div>
        <div class="main-section__paint main-section__paint--2"></div>
        <div class="main-section__paint main-section__paint--3"></div>
        <div class="main-section__paint main-section__paint--4"></div>
      </div>
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
  flex: 1;
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

/* Abstract paint composition */
.main-section__visual {
  position: relative;
  flex-shrink: 0;
  width: min(360px, 100%);
  aspect-ratio: 1;
  border-radius: 42% 58% 52% 48% / 48% 52% 48% 52%;
  background-color: var(--color-surface);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.main-section__paint {
  position: absolute;
  border-radius: 50%;
  filter: blur(32px);
}

.main-section__paint--1 {
  width: 70%;
  height: 70%;
  top: -15%;
  left: -15%;
  background-color: color-mix(in srgb, var(--color-secondary) 55%, transparent);
}

.main-section__paint--2 {
  width: 60%;
  height: 60%;
  bottom: -10%;
  right: -10%;
  background-color: color-mix(in srgb, var(--color-accent) 45%, transparent);
}

.main-section__paint--3 {
  width: 50%;
  height: 50%;
  top: 30%;
  left: 20%;
  background-color: color-mix(in srgb, var(--color-primary) 80%, transparent);
}

.main-section__paint--4 {
  width: 35%;
  height: 35%;
  top: 5%;
  right: 10%;
  background-color: color-mix(
    in srgb,
    var(--color-accent) 20%,
    var(--color-secondary)
  );
  opacity: 0.7;
  filter: blur(20px);
}

@media (min-width: 768px) {
  .main-section {
    flex-direction: row;
    gap: 4rem;
  }

  .main-section__text {
    align-items: flex-start;
    text-align: left;
  }

  .main-section__visual {
    width: min(400px, 42%);
  }
}
</style>
