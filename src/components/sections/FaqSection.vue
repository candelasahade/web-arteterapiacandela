<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'

interface FaqItem {
  question: string
  answer: string
}

const { t, tm } = useI18n()

const faqs = computed(() => tm('faq.items') as FaqItem[])

const openIndex = ref<number | null>(0) // first item open by default

function toggle(index: number) {
  openIndex.value = openIndex.value === index ? null : index
}
</script>

<template>
  <section id="preguntas-frecuentes" class="faq bg-cream">
    <div class="faq__inner">
      <p class="faq__label">{{ t('faq.label') }}</p>
      <h2 class="faq__heading">{{ t('faq.heading') }}</h2>

      <div class="faq__list">
        <div
          v-for="(item, index) in faqs"
          :key="item.question"
          class="faq__item"
          :class="{ 'faq__item--open': openIndex === index }"
        >
          <button
            :id="`faq-q-${index}`"
            class="faq__trigger"
            :aria-expanded="openIndex === index"
            :aria-controls="`faq-a-${index}`"
            @click="toggle(index)"
          >
            <span
              class="faq__question-text"
              :class="{ 'faq__question-text--active': openIndex === index }"
            >{{ item.question }}</span>
            <span class="faq__chevron" aria-hidden="true">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </span>
          </button>

          <div
            :id="`faq-a-${index}`"
            role="region"
            :aria-labelledby="`faq-q-${index}`"
            class="faq__panel"
          >
            <div class="faq__panel-inner">
              <p class="faq__answer">{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq {
  padding-block: var(--section-padding);
}

.faq__inner {
  max-width: var(--page-max);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
}

.faq__label {
  font-family: var(--font-body);
  font-size: var(--text-label);
  font-weight: 400;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0 0 1rem;
}

.faq__heading {
  font-family: var(--font-body);
  font-size: var(--text-subhead);
  font-weight: 400;
  line-height: 1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0 0 2.5rem;
}

.faq__list {
  border-top: 1px solid var(--color-black);
}

.faq__item {
  border-bottom: 1px solid var(--color-black);
}

.faq__trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  color: inherit;
}

.faq__question-text {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  line-height: 1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  transition: color 0.2s ease;
}

.faq__question-text--active {
  font-weight: 700;
  color: var(--color-gold);
}

.faq__chevron {
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-black);
  transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}

.faq__item--open .faq__chevron {
  transform: rotate(180deg);
}

/* CSS grid height trick for smooth expand */
.faq__panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.faq__item--open .faq__panel {
  grid-template-rows: 1fr;
}

.faq__panel-inner {
  overflow: hidden;
}

.faq__answer {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  line-height: 1.17;
  color: var(--color-black);
  margin: 0;
  padding-bottom: 1.5rem;
}
</style>
