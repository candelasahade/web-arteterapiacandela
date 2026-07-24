<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'

interface ArtTherapyCard {
  title: string
  paragraphs: string[]
  facts?: { label: string; value: string }[]
}

const { t, tm } = useI18n()

const cards = computed(() => tm('artTherapy.cards') as ArtTherapyCard[])
</script>

<template>
  <BaseSection id="arteterapia" class="bg-alt">
    <div class="art-therapy">
      <h2 class="art-therapy__title">{{ t('artTherapy.title') }}</h2>
      <p class="art-therapy__intro">
        {{ t('artTherapy.intro') }}
      </p>

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
  color: var(--color-text-light);
  text-align: center;
  max-width: 52ch;
  margin: 0 auto 3rem;
  line-height: 1.7;
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
</style>
