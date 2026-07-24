<script setup lang="ts">
import BaseSection from '../base/BaseSection.vue'
</script>

<template>
  <BaseSection id="sobre-mi">
    <div class="about">
      <h2 class="about__title">Sobre mí</h2>

      <div class="about__intro">
        <!-- PLACEHOLDER: sustituir por foto real -->
        <div class="about__photo-wrap">
          <div class="about__photo" role="img" aria-label="Foto de Candela (próximamente)">
            <svg class="about__photo-icon" viewBox="0 0 80 80" fill="none" aria-hidden="true">
              <circle cx="40" cy="30" r="16" fill="currentColor" opacity="0.35" />
              <path d="M8 76c0-17.673 14.327-32 32-32s32 14.327 32 32" fill="currentColor" opacity="0.22" />
            </svg>
          </div>
          <div class="about__photo-ring" aria-hidden="true"></div>
        </div>

        <!-- PLACEHOLDER: breve presentación a revisar con Candela -->
        <p class="about__intro-text">
          Soy Candela, arteterapeuta especializada en el acompañamiento de
          niños y adolescentes. Creo en el arte como un lenguaje capaz de
          decir aquello que a veces cuesta poner en palabras.
        </p>
      </div>

      <div class="about__details">
        <!-- PLACEHOLDER -->
        <div class="about__block">
          <h3>Qué me llevó a la arteterapia</h3>
          <p>
            Desde siempre el arte fue mi manera de procesar lo que sentía.
            Con el tiempo entendí que quería acompañar a otras personas a
            encontrar ese mismo espacio de expresión y cuidado.
          </p>
        </div>

        <div class="about__block">
          <h3>Formación</h3>
          <p>Magíster en Arteterapia Relacional.</p>
        </div>

        <!-- PLACEHOLDER: completar con la trayectoria real de Candela -->
        <div class="about__block">
          <h3>Experiencia</h3>
          <p>
            Completar con la trayectoria de Candela: dónde trabajó, con qué
            poblaciones y proyectos destacados.
          </p>
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
