<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'

interface ArtTherapyCard {
  title: string
  paragraphs: string[]
  facts?: { label: string; value: string }[]
  quote?: { text: string; author: string }
  list?: string[]
}

const { t, tm } = useI18n()

const cards = computed(() => tm('artTherapy.cards') as ArtTherapyCard[])
</script>

<template>
  <BaseSection id="arteterapia" class="bg-alt">
    <div class="art-therapy">
      <div class="art-therapy__head">
        <h2 class="art-therapy__title">{{ t('artTherapy.title') }}</h2>
        <p class="art-therapy__intro">
          <q class="art-therapy__intro-quote">{{
            t('artTherapy.intro.quote')
          }}</q>
          <cite class="art-therapy__intro-author">{{
            t('artTherapy.intro.author')
          }}</cite>
        </p>

        <!-- Decorative only. On wide screens the pair flanks the heading from
             the section edges (out of the flow, so it can't push text around);
             below 1024px it collapses into a small centred posy under the
             quote, where there is no room to flank without crowding it. -->
        <div class="art-therapy__flowers" aria-hidden="true">
          <img
            class="art-therapy__flower art-therapy__flower--small"
            src="/flor-chica-400.webp"
            alt=""
            loading="lazy"
            decoding="async"
          />
          <img
            class="art-therapy__flower art-therapy__flower--big"
            src="/flor-grande-400.webp"
            alt=""
            loading="lazy"
            decoding="async"
          />
        </div>
      </div>

      <div class="art-therapy__grid">
        <article
          v-for="(card, i) in cards"
          :key="card.title"
          class="art-therapy__card"
        >
          <div
            class="art-therapy__blob"
            :class="
              i % 2 === 0
                ? 'art-therapy__blob--accent'
                : 'art-therapy__blob--secondary'
            "
            aria-hidden="true"
          />
          <h3 class="art-therapy__card-title">{{ card.title }}</h3>

          <blockquote v-if="card.quote" class="art-therapy__card-quote">
            <q>{{ card.quote.text }}</q>
            <cite>{{ card.quote.author }}</cite>
          </blockquote>

          <dl v-if="card.facts" class="art-therapy__facts">
            <div
              v-for="fact in card.facts"
              :key="fact.label"
              class="art-therapy__fact"
            >
              <dt>{{ fact.label }}</dt>
              <dd>{{ fact.value }}</dd>
            </div>
          </dl>

          <ul v-if="card.list" class="art-therapy__list">
            <li v-for="(item, li) in card.list" :key="li">{{ item }}</li>
          </ul>

          <p
            v-for="(paragraph, pi) in card.paragraphs"
            :key="pi"
            class="art-therapy__card-text"
          >
            {{ paragraph }}
          </p>
        </article>
      </div>
    </div>
  </BaseSection>
</template>

<style scoped>
.art-therapy {
  flex: 1;
  width: 100%;
}

.art-therapy__head {
  position: relative;
}

.art-therapy__title {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(1.75rem, 3vw + 1rem, 2.5rem);
  text-align: center;
  margin: 0 0 0.75rem;
}

.art-therapy__intro {
  font-family: var(--font-sans);
  font-size: 1.0625rem;
  text-align: center;
  max-width: 52ch;
  margin: 0 auto 3rem;
  line-height: 1.7;
}

.art-therapy__intro-quote {
  font-family: var(--font-serif);
  font-style: italic;
  color: var(--color-accent);
}

.art-therapy__intro-author {
  display: block;
  margin-top: 0.5rem;
  font-style: normal;
  font-size: 0.875rem;
  color: var(--color-text-light);
}

.art-therapy__intro-author::before {
  content: '— ';
}

.art-therapy__flowers {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 1.25rem;
  margin: -1.25rem 0 2.25rem;
  pointer-events: none;
  user-select: none;
}

/* Height (never width) is the fixed dimension: the space is reserved before
   the lazy-loaded file arrives, so nothing jumps when it does. */
.art-therapy__flower {
  display: block;
  width: auto;
}

.art-therapy__flower--small {
  height: 3.25rem;
  transform: rotate(-6deg);
}

.art-therapy__flower--big {
  height: 4.5rem;
  transform: rotate(5deg);
}

.art-therapy__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

.art-therapy__card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.875rem;
  padding: 2rem;
  background-color: var(--color-background);
  border-radius: 1.25rem;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-soft);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.art-therapy__card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
}

.art-therapy__blob {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  flex-shrink: 0;
}

.art-therapy__blob--accent {
  background-color: color-mix(in srgb, var(--color-accent) 75%, transparent);
}

.art-therapy__blob--secondary {
  background-color: color-mix(in srgb, var(--color-secondary) 75%, transparent);
}

.art-therapy__card-title {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: 1.25rem;
  line-height: 1.3;
  margin: 0;
}

.art-therapy__card-quote {
  margin: 0;
  padding: 0;
  border: none;
  font-family: var(--font-sans);
  font-weight: 700;
  font-size: 0.9375rem;
  line-height: 1.7;
}

.art-therapy__card-quote cite {
  font-style: normal;
}

.art-therapy__list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 0;
  padding-left: 1.1rem;
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.6;
}

.art-therapy__list li::marker {
  color: var(--color-accent);
}

.art-therapy__card-text {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.7;
  margin: 0;
}

.art-therapy__facts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  margin: 0;
  padding: 1rem 1.25rem;
  background-color: var(--color-surface);
  border-radius: 0.875rem;
  border: 1px solid var(--color-border);
}

.art-therapy__fact {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  font-family: var(--font-sans);
  font-size: 0.9375rem;
}

.art-therapy__fact dt {
  font-weight: 600;
}

.art-therapy__fact dt::after {
  content: ':';
}

.art-therapy__fact dd {
  margin: 0;
  color: var(--color-text-light);
}

@media (min-width: 768px) {
  .art-therapy__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Wide enough for the flowers to sit beside the heading instead of under it. */
@media (min-width: 1024px) {
  .art-therapy__head {
    padding-inline: 11rem;
  }

  /* Narrower than the section: the pair tucks in beside the title instead of
     sitting out on the corners, while still clearing the 52ch quote. */
  .art-therapy__flowers {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: min(100%, 57rem);
    transform: translateX(-50%);
    align-items: center;
    justify-content: space-between;
    margin: 0;
  }

  .art-therapy__flower--small {
    height: clamp(6rem, 9vw, 8rem);
    transform: rotate(-4deg);
  }

  .art-therapy__flower--big {
    height: clamp(7.5rem, 11vw, 10.5rem);
    transform: rotate(3deg);
  }
}
</style>
