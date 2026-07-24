<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'

interface AboutBlock {
  title: string
  body: string
}

const { t, tm } = useI18n()

const blocks = computed(() => tm('about.blocks') as AboutBlock[])
</script>

<template>
  <BaseSection id="sobre-mi">
    <div class="about">
      <h2 class="about__title">{{ t('about.title') }}</h2>

      <div class="about__intro">
        <!-- PLACEHOLDER: sustituir por foto real -->
        <div class="about__photo-wrap">
          <div
            class="about__photo"
            role="img"
            :aria-label="t('about.photoAlt')"
          >
            <svg
              class="about__photo-icon"
              viewBox="0 0 80 80"
              fill="none"
              aria-hidden="true"
            >
              <circle
                cx="40"
                cy="30"
                r="16"
                fill="currentColor"
                opacity="0.35"
              />
              <path
                d="M8 76c0-17.673 14.327-32 32-32s32 14.327 32 32"
                fill="currentColor"
                opacity="0.22"
              />
            </svg>
          </div>
          <div class="about__photo-ring" aria-hidden="true"></div>
        </div>

        <p class="about__intro-text">
          {{ t('about.introText') }}
        </p>
      </div>

      <div class="about__details">
        <div v-for="block in blocks" :key="block.title" class="about__block">
          <h3>{{ block.title }}</h3>
          <p>{{ block.body }}</p>
        </div>
      </div>
    </div>
  </BaseSection>
</template>

<style scoped>
.about {
  flex: 1;
  width: 100%;
}

.about__title {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(1.75rem, 3vw + 1rem, 2.5rem);
  text-align: center;
  margin: 0 0 3rem;
}

.about__intro {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  text-align: center;
  margin-bottom: 3.5rem;
}

.about__photo-wrap {
  position: relative;
  flex-shrink: 0;
}

.about__photo {
  position: relative;
  z-index: 1;
  width: 10rem;
  height: 10rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-surface);
  border: 2px solid var(--color-border);
  color: var(--color-secondary);
  overflow: hidden;
}

.about__photo-icon {
  width: 65%;
  height: 65%;
}

.about__photo-ring {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px dashed color-mix(in srgb, var(--color-secondary) 45%, transparent);
  z-index: 0;
}

.about__intro-text {
  font-family: var(--font-sans);
  font-size: 1.0625rem;
  line-height: 1.7;
  color: var(--color-text-light);
  max-width: 44ch;
  margin: 0;
}

.about__details {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

.about__block {
  padding: 2rem;
  background-color: var(--color-surface);
  border-radius: 1.25rem;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-soft);
}

.about__block h3 {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: 1.125rem;
  margin: 0 0 0.75rem;
  color: var(--color-text);
}

.about__block p {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.7;
  margin: 0;
}

@media (min-width: 768px) {
  .about__intro {
    flex-direction: row;
    text-align: left;
    gap: 3rem;
  }

  .about__photo {
    width: 11rem;
    height: 11rem;
  }

  .about__details {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
