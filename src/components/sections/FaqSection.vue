<script setup lang="ts">
import { ref } from 'vue'
import BaseSection from '../base/BaseSection.vue'

// PLACEHOLDER: preguntas y respuestas a revisar/confirmar con Candela
const faqs = [
  {
    question: '¿Necesito saber dibujar o pintar?',
    answer:
      'No. La arteterapia no busca resultados estéticos ni habilidad artística: el proceso creativo es el medio, no el objetivo.',
  },
  {
    question: '¿A partir de qué edad pueden participar los niños?',
    answer:
      'Completar con la edad mínima recomendada según la experiencia de Candela.',
  },
  {
    question: '¿Las sesiones son online o presenciales?',
    answer:
      'Ambas modalidades están disponibles: presencial en Barcelona y Sant Cugat, u online.',
  },
  {
    question: '¿Cómo sé si la arteterapia es adecuada para mi hijo o hija?',
    answer:
      'En la primera entrevista conversamos sobre la situación particular y evaluamos juntas si este es el espacio adecuado.',
  },
  {
    question: '¿Cuánto dura el proceso terapéutico?',
    answer:
      'Completar con los criterios habituales de duración según cada proceso.',
  },
]

const openIndex = ref<number | null>(null)

function toggle(index: number) {
  openIndex.value = openIndex.value === index ? null : index
}
</script>

<template>
  <BaseSection id="preguntas-frecuentes" class="bg-alt">
    <div class="faq">
      <header class="faq__header">
        <p class="faq__eyebrow">Todo lo que necesitás saber</p>
        <h2 class="faq__title">Preguntas frecuentes</h2>
      </header>

      <div class="faq__list">
        <div
          v-for="(item, index) in faqs"
          :key="item.question"
          class="faq__item"
          :class="{ 'faq__item--open': openIndex === index }"
        >
          <button
            :id="`faq-question-${index}`"
            class="faq__trigger"
            :aria-expanded="openIndex === index"
            :aria-controls="`faq-answer-${index}`"
            @click="toggle(index)"
          >
            <span class="faq__num" aria-hidden="true">{{
              String(index + 1).padStart(2, '0')
            }}</span>
            <span class="faq__question-text">{{ item.question }}</span>
            <span class="faq__chevron" aria-hidden="true">
              <svg
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M5 7.5L10 12.5L15 7.5"
                  stroke="currentColor"
                  stroke-width="1.75"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </span>
          </button>

          <!-- Panel always in DOM; height animated via CSS grid trick -->
          <div
            :id="`faq-answer-${index}`"
            role="region"
            :aria-labelledby="`faq-question-${index}`"
            class="faq__panel"
          >
            <div class="faq__panel-inner">
              <p class="faq__answer">{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseSection>
</template>

<style scoped>
.faq {
  width: 100%;
  max-width: 50rem;
  margin-inline: auto;
}

.faq__header {
  text-align: center;
  margin-bottom: 3rem;
}

.faq__eyebrow {
  font-family: var(--font-sans);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-secondary);
  margin: 0 0 0.875rem;
}

.faq__title {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(1.75rem, 3vw + 1rem, 2.5rem);
  color: var(--color-text);
  margin: 0;
}

.faq__list {
  border-top: 1px solid var(--color-border);
}

.faq__item {
  border-bottom: 1px solid var(--color-border);
  transition: background-color 0.25s ease;
}

.faq__item--open {
  background-color: color-mix(
    in srgb,
    var(--color-secondary) 6%,
    var(--color-surface)
  );
}

.faq__trigger {
  width: 100%;
  display: grid;
  grid-template-columns: 2.25rem 1fr 1.25rem;
  align-items: start;
  gap: 1.25rem;
  padding: 1.5rem 0.25rem 1.5rem 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  color: inherit;
}

.faq__num {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 2rem;
  color: var(--color-accent);
  opacity: 0.45;
  line-height: 1.4;
  padding-top: 0.1rem;
  transition: opacity 0.22s ease;
  user-select: none;
}

.faq__item--open .faq__num {
  opacity: 1;
}

.faq__question-text {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.45;
  transition: color 0.22s ease;
  margin: auto 0;
}

.faq__trigger:hover .faq__question-text {
  color: var(--color-accent);
}

.faq__item--open .faq__question-text {
  color: color-mix(in srgb, var(--color-accent) 75%, var(--color-text));
}

.faq__chevron {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-accent);
  opacity: 0.55;
  padding-top: 0.1rem;
  flex-shrink: 0;
  transition:
    transform 0.28s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.22s ease;
}

.faq__item--open .faq__chevron {
  transform: rotate(180deg);
  opacity: 1;
}

/* CSS grid height trick: animates 0 → auto without JavaScript */
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

/* Indent answer to align under the question text (number col + gap) */
.faq__answer {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.75;
  margin: 0;
  padding: 0 0.25rem 1.625rem calc(2.25rem + 1.25rem);
}
</style>
