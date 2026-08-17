<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'

interface AboutBlock {
  title: string
  body?: string
  list?: string[]
  link?: { label: string; url: string }
}

const { t, tm } = useI18n()

const blocks = computed(() => tm('about.blocks') as AboutBlock[])

// Fixed, hand-placed values (not random) — this site prerenders at build
// time, so Math.random() here would mismatch between server and client.
const heroWatermarks = [
  { left: '-1%', bottom: '-0.5rem', rotate: -18, size: '5.75rem' },
  { left: '16%', bottom: '1.5rem', rotate: 24, size: '4.25rem' },
  { left: '34%', bottom: '-1.25rem', rotate: -8, size: '6.25rem' },
  { left: '52%', bottom: '1.25rem', rotate: 33, size: '4.5rem' },
  { left: '70%', bottom: '-0.75rem', rotate: -28, size: '6rem' },
  { left: '88%', bottom: '1rem', rotate: 12, size: '5.25rem' },
]
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
        <div
          v-for="(block, index) in blocks"
          :key="block.title"
          class="about__block"
          :class="{ 'about__block--hero': index === 0 }"
        >
          <template v-if="index === 0">
            <img
              v-for="(w, wi) in heroWatermarks"
              :key="wi"
              class="about__block-watermark"
              :style="{
                left: w.left,
                bottom: w.bottom,
                width: w.size,
                transform: `rotate(${w.rotate}deg)`,
              }"
              src="/adorno-hoja-negro-400.webp"
              alt=""
              aria-hidden="true"
              loading="lazy"
            />
          </template>
          <h3>{{ block.title }}</h3>
          <p v-if="block.body">{{ block.body }}</p>
          <ul v-if="block.list" class="about__block-list">
            <li v-for="(item, li) in block.list" :key="li">{{ item }}</li>
          </ul>
          <a
            v-if="block.link"
            class="about__block-link"
            :href="block.link.url"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <rect
                x="2"
                y="2"
                width="20"
                height="20"
                rx="4"
                stroke="currentColor"
                stroke-width="1.5"
              />
              <path
                d="M7 10v7"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
              <path
                d="M11 17v-4c0-1.657 1.343-3 3-3s3 1.343 3 3v4"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
              <path
                d="M11 10v7"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
              <circle cx="7" cy="7.5" r="1" fill="currentColor" />
            </svg>
            {{ block.link.label }}
          </a>
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

.about__block--hero {
  position: relative;
  z-index: 0;
  overflow: hidden;
}

.about__block-watermark {
  position: absolute;
  z-index: -1;
  height: auto;
  opacity: 0.2;
  pointer-events: none;
  user-select: none;
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

.about__block-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin: 0;
  padding-left: 1.1rem;
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.6;
}

.about__block-list li::marker {
  color: var(--color-accent);
}

.about__block-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.25rem;
  padding: 0.5rem 0.9375rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  color: var(--color-accent);
  font-family: var(--font-sans);
  font-size: 0.8125rem;
  font-weight: 600;
  text-decoration: none;
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.about__block-link svg {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.about__block-link:hover,
.about__block-link:focus-visible {
  border-color: var(--color-accent);
  background-color: color-mix(in srgb, var(--color-accent) 7%, transparent);
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
    grid-template-columns: 2fr 1fr;
    grid-template-rows: auto auto;
  }

  .about__block:first-child {
    grid-row: 1 / 3;
  }
}
</style>
