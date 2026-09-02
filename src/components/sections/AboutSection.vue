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
</script>

<template>
  <BaseSection id="sobre-mi">
    <div class="about">
      <h2 class="about__title">{{ t('about.title') }}</h2>

      <div class="about__intro">
        <div class="about__photo-wrap">
          <img
            class="about__photo"
            src="/sobre-mi-640.webp"
            srcset="/sobre-mi-320.webp 320w, /sobre-mi-640.webp 640w"
            sizes="(min-width: 768px) 11rem, 10rem"
            width="640"
            height="616"
            :alt="t('about.photoAlt')"
            decoding="async"
          />
          <div class="about__photo-ring" aria-hidden="true"></div>
        </div>

        <p class="about__intro-text">
          {{ t('about.introText') }}
        </p>

        <!-- Decorative: closes the intro row on the right; on narrow screens
             the row stacks, so it lands centred under the text instead. -->
        <img
          class="about__bird"
          src="/pajaro-400.webp"
          alt=""
          aria-hidden="true"
          loading="lazy"
          decoding="async"
        />
      </div>

      <div class="about__details">
        <div
          v-for="(block, index) in blocks"
          :key="block.title"
          class="about__block"
          :class="{ 'about__block--hero': index === 0 }"
        >
          <img
            v-if="index === 0"
            class="about__block-waves"
            src="/olas-800.webp"
            alt=""
            aria-hidden="true"
            loading="lazy"
            decoding="async"
          />
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
  display: block;
  object-fit: cover;
  background-color: var(--color-surface);
  border: 2px solid var(--color-border);
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

/* Height (never width) is the fixed dimension, so the space is reserved
   before the lazy-loaded file arrives and nothing jumps when it does. */
.about__bird {
  display: block;
  flex-shrink: 0;
  width: auto;
  height: 5rem;
  transform: rotate(-4deg);
  pointer-events: none;
  user-select: none;
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

.about__block-waves {
  position: absolute;
  z-index: -1;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: auto;
  opacity: 0.22;
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

  /* Occupies exactly the right-hand track of the .about__details grid below
     (2fr 1fr with a 1.25rem gap) and centres itself inside it, so the bird
     sits over the "Formación" card rather than flush with the section edge. */
  .about__bird {
    width: calc((100% - 1.25rem) / 3);
    height: clamp(7rem, 10vw, 9.5rem);
    object-fit: contain;
    margin-left: auto;
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
