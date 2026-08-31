<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'
import { heroCarouselSlides } from '@/data/heroCarousel'

const { t, tm } = useI18n()

const phraseLines = computed(() => tm('main.phraseLines') as string[])

// Hand-picked crop focal points per photo (object-fit: cover crops
// landscape photos horizontally and portrait photos vertically — these
// keep the subject in frame instead of a blind center crop). Falls back
// to 'center' for any photo without an entry here.
const FOCAL_POSITIONS: Record<string, string> = {
  'carrusel-1': '60% center',
  'carrusel-2': '65% center',
  'carrusel-3': 'center 25%',
  'carrusel-5': 'center 35%',
}

const AUTOPLAY_MS = 5500

const activeIndex = ref(0)
let timer: ReturnType<typeof setInterval> | undefined
let reduceMotion = false

function slideAlt(index: number): string {
  const alts = tm('main.carouselAlt') as string[]
  return alts[index] ?? t('main.carouselAltFallback', { n: index + 1 })
}

function stopAutoplay() {
  clearInterval(timer)
  timer = undefined
}

function startAutoplay() {
  if (reduceMotion || heroCarouselSlides.length < 2) return
  stopAutoplay()
  timer = setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % heroCarouselSlides.length
  }, AUTOPLAY_MS)
}

function goTo(index: number) {
  activeIndex.value = index
  startAutoplay()
}

let touchStartX = 0

function onTouchStart(event: TouchEvent) {
  touchStartX = event.touches[0]?.clientX ?? 0
}

function onTouchEnd(event: TouchEvent) {
  const endX = event.changedTouches[0]?.clientX
  if (endX === undefined) return
  const delta = endX - touchStartX
  if (Math.abs(delta) < 40) return
  const count = heroCarouselSlides.length
  activeIndex.value =
    delta < 0
      ? (activeIndex.value + 1) % count
      : (activeIndex.value - 1 + count) % count
  startAutoplay()
}

onMounted(() => {
  reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  startAutoplay()
})

onBeforeUnmount(stopAutoplay)
</script>

<template>
  <BaseSection id="main" :full-height="true">
    <div class="main-section">
      <div class="main-section__text">
        <p class="main-section__eyebrow">{{ t('main.eyebrow') }}</p>
        <h1 class="main-section__phrase">
          <template v-for="(line, i) in phraseLines" :key="i"
            >{{ line }}<br v-if="i < phraseLines.length - 1"
          /></template>
        </h1>
        <p class="main-section__lead">
          {{ t('main.lead') }}
        </p>
        <a class="main-section__cta" href="#contacto">{{ t('main.cta') }}</a>
      </div>

      <div
        class="hero-carousel"
        @mouseenter="stopAutoplay"
        @mouseleave="startAutoplay"
        @focusin="stopAutoplay"
        @focusout="startAutoplay"
        @touchstart.passive="onTouchStart"
        @touchend.passive="onTouchEnd"
      >
        <div class="hero-carousel__frame">
          <img
            v-for="(slide, index) in heroCarouselSlides"
            :key="slide.id"
            class="hero-carousel__slide"
            :class="{ 'hero-carousel__slide--active': index === activeIndex }"
            :style="{ objectPosition: FOCAL_POSITIONS[slide.id] ?? 'center' }"
            :src="slide.src"
            :srcset="slide.srcset"
            sizes="(min-width: 768px) 624px, 546px"
            :width="slide.width"
            :height="slide.height"
            :alt="slideAlt(index)"
            :loading="index === 0 ? undefined : 'lazy'"
            :fetchpriority="index === 0 ? 'high' : undefined"
            decoding="async"
          />
        </div>

        <div
          v-if="heroCarouselSlides.length > 1"
          class="hero-carousel__dots"
          role="tablist"
        >
          <button
            v-for="(slide, index) in heroCarouselSlides"
            :key="slide.id"
            type="button"
            class="hero-carousel__dot"
            :class="{ 'hero-carousel__dot--active': index === activeIndex }"
            role="tab"
            :aria-selected="index === activeIndex"
            :aria-label="t('main.carouselDotLabel', { n: index + 1 })"
            @click="goTo(index)"
          />
        </div>
      </div>
    </div>
  </BaseSection>
</template>

<style scoped>
.main-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  width: 100%;
}

.main-section__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
  text-align: center;
}

.main-section__eyebrow {
  font-family: var(--font-sans);
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-secondary);
  margin: 0;
}

.main-section__phrase {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(2rem, 5vw + 0.75rem, 3.5rem);
  line-height: 1.2;
  margin: 0;
  color: var(--color-text);
}

.main-section__lead {
  font-family: var(--font-sans);
  font-size: clamp(1rem, 1vw + 0.875rem, 1.125rem);
  line-height: 1.7;
  color: var(--color-text-light);
  max-width: 42ch;
  margin: 0;
}

.main-section__cta {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.9375rem 2rem;
  background-color: var(--color-accent);
  color: var(--color-surface);
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 0.9375rem;
  text-decoration: none;
  border-radius: 999px;
  letter-spacing: 0.02em;
  box-shadow: 0 4px 16px
    color-mix(in srgb, var(--color-accent) 30%, transparent);
  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.main-section__cta:hover,
.main-section__cta:focus-visible {
  background-color: color-mix(in srgb, var(--color-accent) 85%, black);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px
    color-mix(in srgb, var(--color-accent) 40%, transparent);
}

/* Photo carousel — same slot the single hero drawing used to occupy */
.hero-carousel {
  flex-shrink: 0;
  width: min(628px, 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.hero-carousel__frame {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  background-color: var(--color-surface);
  border-radius: 1.5rem;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  touch-action: pan-y;
}

.hero-carousel__slide {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.6s ease;
  pointer-events: none;
}

.hero-carousel__slide--active {
  opacity: 1;
  pointer-events: auto;
}

.hero-carousel__dots {
  display: flex;
  gap: 0.5rem;
}

.hero-carousel__dot {
  width: 2rem;
  height: 2rem;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-carousel__dot::before {
  content: '';
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--color-border);
  transition:
    background-color 0.2s ease,
    transform 0.2s ease;
}

.hero-carousel__dot--active::before {
  background-color: var(--color-accent);
  transform: scale(1.35);
}

@media (min-width: 768px) {
  .main-section {
    flex-direction: row;
    gap: 4rem;
  }

  .main-section__text {
    flex: 1;
    align-items: flex-start;
    text-align: left;
  }

  .hero-carousel {
    width: min(718px, 46%);
  }
}
</style>
