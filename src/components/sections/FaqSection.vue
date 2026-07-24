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
    answer: 'Completar con la edad mínima recomendada según la experiencia de Candela.',
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
    answer: 'Completar con los criterios habituales de duración según cada proceso.',
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
      <h2 class="faq__title">Preguntas frecuentes</h2>

      <div class="faq__list">
        <div
          v-for="(item, index) in faqs"
          :key="item.question"
          class="faq__item"
          :class="{ 'faq__item--open': openIndex === index }"
        >
          <button
            :id="`faq-question-${index}`"
            class="faq__question"
            :aria-expanded="openIndex === index"
            :aria-controls="`faq-answer-${index}`"
            @click="toggle(index)"
          >
            <span>{{ item.question }}</span>
            <span class="faq__icon" aria-hidden="true">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
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

          <div
            :id="`faq-answer-${index}`"
            role="region"
            :aria-labelledby="`faq-question-${index}`"
          >
            <Transition name="faq-slide">
              <div v-if="openIndex === index" class="faq__answer-wrap">
                <p class="faq__answer">{{ item.answer }}</p>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>
  </BaseSection>
</template>

<style scoped>
.faq {
  flex: 1;
  width: 100%;
  max-width: 48rem;
  margin-inline: auto;
}

.faq__title {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(1.75rem, 3vw + 1rem, 2.5rem);
  text-align: center;
  margin: 0 0 2.5rem;
}

.faq__list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.faq__item {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 1.25rem;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
  transition:
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.faq__item--open {
  box-shadow: var(--shadow-card);
  border-color: color-mix(in srgb, var(--color-secondary) 55%, var(--color-border));
}

.faq__question {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 0.9375rem;
  color: var(--color-text);
  text-align: left;
  transition: color 0.2s ease;
}

.faq__question:hover {
  color: var(--color-accent);
}

.faq__icon {
  flex-shrink: 0;
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-accent);
  transition: transform 0.25s ease;
}

.faq__item--open .faq__icon {
  transform: rotate(180deg);
}

.faq__answer-wrap {
  padding: 0 1.5rem 1.375rem;
}

.faq__answer {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.7;
  margin: 0;
}

/* Slide transition */
.faq-slide-enter-active,
.faq-slide-leave-active {
  transition:
    opacity 0.22s ease,
    transform 0.22s ease;
}

.faq-slide-enter-from,
.faq-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
