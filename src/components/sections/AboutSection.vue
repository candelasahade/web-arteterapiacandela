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
      <!-- Label + heading -->
      <div class="about__header">
        <p class="about__label">{{ t('about.label') }}</p>
        <h2 class="about__heading">{{ t('about.heading') }}</h2>
        <img
          class="about__waves"
          src="/olas-800.webp"
          alt=""
          aria-hidden="true"
          loading="lazy"
          decoding="async"
        />
      </div>

      <!-- Content: photo + bio -->
      <div
        class="about__content fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <div class="about__photo-wrap">
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

.about__inner {
  max-width: var(--page-max);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
  display: flex;
  flex-direction: column;
  gap: clamp(2rem, 4vw, 3rem);
}

/* ── Header ─────────────────────────────────────────────── */
.about__header {
  position: relative;
}

.about__label {
  font-family: var(--font-body);
  font-size: var(--text-label);
  font-weight: 400;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0 0 1rem;
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

.about__waves {
  position: absolute;
  top: 0;
  right: 0;
  width: auto;
  height: clamp(2rem, 4vw, 3.2rem);
  pointer-events: none;
  user-select: none;
  opacity: 0.7;
}

/* ── Content ────────────────────────────────────────────── */
.about__content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.about__photo-wrap {
  min-width: 0;
}

.about__photo {
  display: block;
  width: 100%;
  max-width: 22rem;
  height: auto;
  object-fit: cover;
  border-radius: var(--card-radius);
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

@media (min-width: 768px) {
  .about__content {
    display: grid;
    grid-template-columns: clamp(16rem, 30%, 26rem) 1fr;
    align-items: start;
    gap: 3rem;
  }

  .about__photo {
    max-width: 100%;
    width: 100%;
  }
}
</style>
