<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Fade-in on scroll
const fadeRefs = ref<HTMLElement[]>([])
let observer: IntersectionObserver | null = null

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible')
          observer?.unobserve(e.target)
        }
      })
    },
    { threshold: 0.12 },
  )
  fadeRefs.value.forEach((el) => observer?.observe(el))
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <section id="main" class="main">
    <!-- Hero photo -->
    <div class="hero">
      <div class="hero__inner">
        <div class="hero__photo-wrap">
          <img
            class="hero__photo"
            src="/hero.png"
            alt=""
            width="2048"
            height="1365"
            fetchpriority="high"
            decoding="async"
          />
          <div class="hero__overlay" aria-hidden="true" />
          <p class="hero__tagline">{{ t('main.tagline') }}</p>
        </div>
      </div>
    </div>

    <!-- Birds row -->
    <div class="birds" aria-hidden="true">
      <img class="birds__img birds__img--1" src="/pajaro-800.webp" alt="" loading="lazy" decoding="async" />
      <img class="birds__img birds__img--2" src="/pajaro-400.webp" alt="" loading="lazy" decoding="async" />
      <img class="birds__img birds__img--3" src="/pajaro-800.webp" alt="" loading="lazy" decoding="async" />
    </div>

    <!-- Large intro text -->
    <div
      class="intro fade-in"
      :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
    >
      <div class="intro__inner">
        <p class="intro__text">
          {{ t('main.intro.prefix') }}
          <span class="text-gold">{{ t('main.intro.art') }}</span>{{ t('main.intro.mid1') }}<span class="text-crimson">{{ t('main.intro.escolta') }}</span>{{ t('main.intro.mid2') }}<span class="text-blue">{{ t('main.intro.presencia') }}</span>{{ t('main.intro.mid3') }}<span class="text-gold">{{ t('main.intro.creativitat') }}</span>{{ t('main.intro.suffix') }}
        </p>
      </div>
    </div>

    <!-- Photo grid -->
    <div
      class="photo-grid fade-in"
      :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
    >
      <div class="photo-grid__inner">
        <img
          class="photo-grid__wide"
          src="/photo-grid-wide.png"
          :alt="t('main.photoGridAlt1')"
          width="819"
          height="546"
          loading="lazy"
          decoding="async"
        />
        <img
          class="photo-grid__tall"
          src="/photo-grid-tall.png"
          :alt="t('main.photoGridAlt2')"
          width="400"
          height="698"
          loading="lazy"
          decoding="async"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.main {
  background-color: var(--color-white);
}

/* ── Hero ───────────────────────────────────────────────── */
.hero {
  padding-bottom: 2rem;
}

.hero__inner {
  width: 100%;
}

.hero__photo-wrap {
  position: relative;
  overflow: hidden;
  aspect-ratio: 16 / 10;
  background-color: var(--color-cream);
}

.hero__photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero__overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.15);
  pointer-events: none;
}

.hero__tagline {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 1rem;
  font-family: var(--font-body);
  font-size: var(--text-headline);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-white);
  text-align: center;
}

/* ── Birds ──────────────────────────────────────────────── */
.birds {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: clamp(2rem, 6vw, 6rem);
  padding: 0 var(--page-gutter);
  pointer-events: none;
  user-select: none;
  margin-bottom: clamp(2rem, 4vw, 3rem);
}

.birds__img {
  display: block;
  width: auto;
  height: clamp(4rem, 8vw, 7rem);
}

.birds__img--1 {
  transform: scaleX(-1) rotate(-5deg);
}

.birds__img--2 {
  height: clamp(3.5rem, 7vw, 6rem);
  transform: rotate(3deg);
}

.birds__img--3 {
  transform: rotate(6deg);
}

/* ── Intro text ─────────────────────────────────────────── */
.intro {
  padding: 0 var(--page-gutter) clamp(3rem, 5vw, 5rem);
}

.intro__inner {
  max-width: var(--page-max);
  margin-inline: auto;
}

.intro__text {
  font-family: var(--font-body);
  font-size: var(--text-headline);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0;
}

.text-gold { color: var(--color-gold); }
.text-crimson { color: var(--color-crimson); }
.text-blue { color: var(--color-blue); }

/* ── Photo grid ─────────────────────────────────────────── */
.photo-grid {
  padding: 0 var(--page-gutter) clamp(3rem, 5vw, 5rem);
}

.photo-grid__inner {
  max-width: var(--page-max);
  margin-inline: auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.photo-grid__wide,
.photo-grid__tall {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--card-radius);
}

.photo-grid__wide {
  aspect-ratio: 16 / 10;
}

.photo-grid__tall {
  aspect-ratio: 9 / 16;
  max-height: 30rem;
  width: 100%;
  object-position: center top;
}

@media (min-width: 768px) {
  .photo-grid__inner {
    grid-template-columns: 2fr 1fr;
    align-items: start;
  }

  .photo-grid__wide {
    aspect-ratio: 3 / 2;
  }

  .photo-grid__tall {
    max-height: none;
    aspect-ratio: 9 / 14;
  }
}
</style>
