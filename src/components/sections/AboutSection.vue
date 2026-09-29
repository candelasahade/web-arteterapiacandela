<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, tm } = useI18n()
const bios = computed(() => tm('about.bioParagraphs') as string[])

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
    { threshold: 0.1 },
  )
  fadeRefs.value.forEach((el) => observer?.observe(el))
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <section id="sobre-mi" class="about">
    <div class="about__inner">

      <!-- Left column: label + portrait -->
      <div
        class="about__left fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <p class="about__label">{{ t('about.label') }}</p>
        <img
          class="about__photo"
          src="/about-portrait-4892dc.png"
          :alt="t('about.photoAlt')"
          width="972"
          height="1776"
          loading="lazy"
          decoding="async"
        />
      </div>

      <!-- Right column: heading + waves + bio -->
      <div
        class="about__right fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <h2 class="about__heading">{{ t('about.heading') }}</h2>

        <img
          class="about__waves"
          src="/olas-800.webp"
          alt=""
          aria-hidden="true"
          loading="lazy"
          decoding="async"
        />

        <div class="about__bio">
          <p class="about__bio-text" v-for="(para, i) in bios" :key="i">
            {{ para }}
          </p>
          <a
            class="about__linkedin"
            href="https://es.linkedin.com/in/candela-sahade-508b11257"
            target="_blank"
            rel="noopener noreferrer"
          >
            → {{ t('about.linkedinCta') }}
          </a>
        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.about {
  background-color: var(--color-white);
  padding-block: var(--section-padding);
}

/* ── Grid ───────────────────────────────────────────────── */
.about__inner {
  max-width: var(--page-max);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ── Left column ────────────────────────────────────────── */
.about__left {
  display: flex;
  flex-direction: column;
  gap: 2.5rem; /* 40px — Figma: label bottom y=4518, portrait top y=4558 */
}

.about__label {
  font-family: var(--font-body);
  font-size: var(--text-label);
  font-weight: 400;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0;
}

.about__photo {
  display: block;
  width: 100%;
  max-width: 22rem;
  height: auto;
  object-fit: cover;
  border-radius: var(--card-radius);
}

/* ── Right column ───────────────────────────────────────── */
.about__right {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.about__heading {
  font-family: var(--font-body);
  font-size: var(--text-subhead);
  font-weight: 400;
  line-height: 1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0;
}

/* Figma: waves 183×51px, 41px below heading bottom, 63px above bio */
.about__waves {
  display: block;
  width: 11.4375rem; /* 183px — matches Figma 1280px frame */
  height: auto;
  margin-top: 2.5625rem;   /* 41px */
  margin-bottom: 3.9375rem; /* 63px */
  pointer-events: none;
  user-select: none;
}

.about__bio {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.about__bio-text {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  line-height: 1.17;
  color: var(--color-black);
  margin: 0;
}

.about__linkedin {
  display: inline-block;
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 700;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  text-decoration: underline;
  text-underline-offset: 0.15em;
  transition: color 0.2s ease;
}

.about__linkedin:hover {
  color: var(--color-crimson);
}

/* ── Desktop: 2-column grid ─────────────────────────────── */
@media (min-width: 768px) {
  .about__inner {
    display: grid;
    /* Left col ≈ 400px (32% of 1240px content), gap 55px, right col fills rest */
    grid-template-columns: clamp(16rem, 32%, 26rem) 1fr;
    column-gap: 3.4375rem; /* 55px */
    row-gap: 0;
    align-items: start;
  }

  .about__photo {
    max-width: 100%;
    width: 100%;
  }

  /* Push heading down to align with portrait top: label (1.5rem) + gap (2.5rem) = 4rem */
  .about__right {
    padding-top: 4rem;
  }
}
</style>
