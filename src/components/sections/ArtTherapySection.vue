<script setup lang="ts">
import BaseSection from '../base/BaseSection.vue'
</script>

<template>
  <BaseSection id="arteterapia" class="bg-alt">
    <div class="art-therapy">
      <h2 class="art-therapy__title">Arteterapia</h2>
      <p class="art-therapy__intro">
        Un acompañamiento donde el proceso creativo abre caminos que las palabras a veces no alcanzan.
      </p>

      <div class="art-therapy__grid">
        <article class="art-therapy__card">
          <div class="art-therapy__blob art-therapy__blob--accent" aria-hidden="true" />
          <h3 class="art-therapy__card-title">¿Qué es la arteterapia?</h3>
          <!-- Definición basada en ATE/FEAPA -->
          <p class="art-therapy__card-text">
            Es una vía de acompañamiento que utiliza el proceso de creación
            artística para facilitar procesos terapéuticos y promover el
            bienestar emocional, dentro de una relación terapéutica segura y
            de confianza.
          </p>
          <p class="art-therapy__card-text">
            No es lo mismo que el "arte como sanación" por sí solo: en
            arteterapia el arte no se usa como herramienta de diagnóstico,
            sino como un medio para abordar dificultades emocionales,
            siempre acompañado por una profesional formada específicamente
            en esta disciplina.
          </p>
        </article>

        <!-- PLACEHOLDER: situaciones concretas a confirmar con Candela -->
        <article class="art-therapy__card">
          <div class="art-therapy__blob art-therapy__blob--secondary" aria-hidden="true" />
          <h3 class="art-therapy__card-title">¿En qué situaciones puede ayudar?</h3>
          <p class="art-therapy__card-text">
            Puede acompañar procesos como la dificultad para expresar
            emociones, momentos de cambio, situaciones de ansiedad o estrés,
            o etapas del desarrollo especialmente sensibles en la infancia y
            la adolescencia. Cada proceso es distinto y se adapta a la
            persona, no a un diagnóstico.
          </p>
        </article>

        <!-- PLACEHOLDER: duración, frecuencia y materiales reales a confirmar -->
        <article class="art-therapy__card">
          <div class="art-therapy__blob art-therapy__blob--accent" aria-hidden="true" />
          <h3 class="art-therapy__card-title">¿Cómo es una sesión?</h3>
          <dl class="art-therapy__facts">
            <div class="art-therapy__fact">
              <dt>Duración</dt>
              <dd>50–60 minutos</dd>
            </div>
            <div class="art-therapy__fact">
              <dt>Frecuencia</dt>
              <dd>Semanal o quincenal, según el proceso</dd>
            </div>
            <div class="art-therapy__fact">
              <dt>Materiales</dt>
              <dd>Pintura, arcilla, collage y otros materiales plásticos</dd>
            </div>
          </dl>
          <p class="art-therapy__card-text">
            Cada sesión combina un espacio de creación con un momento de
            palabra y reflexión sobre lo que fue apareciendo, siempre
            respetando el ritmo de cada persona. El proceso comienza con una
            primera entrevista para conocernos.
          </p>
        </article>

        <!-- PLACEHOLDER: ajustar con las palabras propias de Candela -->
        <article class="art-therapy__card">
          <div class="art-therapy__blob art-therapy__blob--secondary" aria-hidden="true" />
          <h3 class="art-therapy__card-title">Mi forma de acompañar</h3>
          <p class="art-therapy__card-text">
            Entiendo la arteterapia desde un enfoque relacional: el vínculo
            que construimos juntas es, en sí mismo, parte del proceso
            terapéutico. Mi lugar es sostener un espacio seguro donde el
            arte pueda abrir caminos que a veces las palabras no alcanzan.
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
