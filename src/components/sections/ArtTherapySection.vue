<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, tm } = useI18n()

const infoLinks = [
  { href: 'https://feapa.es', label: 'feapa.es' },
  { href: 'https://arteterapia.org.es', label: 'arteterapia.org.es' },
]

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
  fadeRefs.value.forEach((el) => {
    if (el.getBoundingClientRect().top < window.innerHeight) {
      el.classList.add('is-visible')
    } else {
      observer?.observe(el)
    }
  })
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <section id="arteterapia" class="at bg-cream">
    <div class="at__inner">

      <!-- Label + large session text -->
      <div
        class="at__intro fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <p class="at__label">{{ t('artTherapy.label') }}</p>
        <p class="at__session-text">
          {{ t('artTherapy.session.prefix') }}<span class="text-blue">{{ t('artTherapy.session.creacio') }}</span>{{ t('artTherapy.session.mid1') }}<span class="text-blue">{{ t('artTherapy.session.joc') }}</span>{{ t('artTherapy.session.mid2') }}<span class="text-gold">{{ t('artTherapy.session.paraula') }}</span>{{ t('artTherapy.session.mid3') }}<span class="text-gold">{{ t('artTherapy.session.reflexio') }}</span>{{ t('artTherapy.session.suffix') }}
        </p>
      </div>

      <!-- Session cards -->
      <div
        class="at__cards fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <!-- Leaf decoration -->
        <img
          class="at__leaf"
          src="/adorno-hoja-master.png"
          alt=""
          aria-hidden="true"
          loading="lazy"
          decoding="async"
        />

        <div class="at__card">
          <img
            class="at__card-icon"
            src="/flor-grande-800.webp"
            alt=""
            aria-hidden="true"
            loading="lazy"
            decoding="async"
          />
          <p class="at__card-text">{{ t('artTherapy.cards.frequency') }}</p>
        </div>

        <div class="at__card">
          <img
            class="at__card-icon"
            src="/arcoiris-800.webp"
            alt=""
            aria-hidden="true"
            loading="lazy"
            decoding="async"
          />
          <p class="at__card-text">{{ t('artTherapy.cards.duration') }}</p>
        </div>

        <div class="at__card">
          <img
            class="at__card-icon at__card-icon--sm"
            src="/adorno-hoja-negro-400.webp"
            alt=""
            aria-hidden="true"
            loading="lazy"
            decoding="async"
          />
          <p class="at__card-text">{{ t('artTherapy.cards.materials') }}</p>
        </div>
      </div>

      <!-- Photo strip -->
      <div
        class="at__strip fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <img
          class="at__strip-photo"
          src="/photo-strip-73bed6.png"
          :alt="t('artTherapy.stripAlt')"
          width="1239"
          height="478"
          loading="lazy"
          decoding="async"
        />
      </div>

      <!-- Definition panel -->
      <div
        class="at__panel fade-in"
        :ref="(el) => el && fadeRefs.push(el as HTMLElement)"
      >
        <!-- Star decorations -->
        <img class="at__star at__star--tl" src="/estrella-400.webp" alt="" aria-hidden="true" loading="lazy" decoding="async" />
        <img class="at__star at__star--br" src="/estrella-400.webp" alt="" aria-hidden="true" loading="lazy" decoding="async" />

        <div class="at__panel-col">
          <h2 class="at__panel-heading">{{ t('artTherapy.what.title') }}</h2>
          <p
            v-for="(para, i) in (tm('artTherapy.what.paragraphs') as string[])"
            :key="i"
            class="at__panel-text"
          >{{ para }}</p>
          <p class="at__panel-text">
            {{ t('artTherapy.what.moreInfo') }}
            <template v-for="(link, i) in infoLinks" :key="link.href">
              <a class="at__panel-link" :href="link.href" target="_blank" rel="noopener noreferrer">{{ link.label }}</a><template v-if="i < infoLinks.length - 1">&nbsp;· </template>
            </template>
          </p>
        </div>

        <div class="at__panel-divider" aria-hidden="true" />

        <div class="at__panel-col">
          <h2 class="at__panel-heading">{{ t('artTherapy.when.title') }}</h2>
          <p class="at__panel-text">{{ t('artTherapy.when.body') }}</p>
        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.at {
  padding-block: var(--section-padding);
}

.at__inner {
  max-width: var(--page-max);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
  display: flex;
  flex-direction: column;
  gap: clamp(2.5rem, 5vw, 4rem);
}

/* ── Label + session text ───────────────────────────────── */
.at__label {
  font-family: var(--font-body);
  font-size: var(--text-label);
  font-weight: 400;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0 0 1rem;
}

.at__session-text {
  font-family: var(--font-body);
  font-size: var(--text-headline);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0;
}

.text-gold { color: var(--color-gold); }
.text-blue { color: var(--color-blue); }

/* ── Session cards ──────────────────────────────────────── */
.at__cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  position: relative;
}

.at__leaf {
  position: absolute;
  top: -3rem;
  right: 0;
  width: auto;
  height: clamp(4rem, 7vw, 6rem);
  pointer-events: none;
  user-select: none;
}

.at__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 1.5rem;
  background-color: var(--color-white);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  text-align: center;
}

.at__card-icon {
  display: block;
  width: auto;
  height: clamp(4rem, 7vw, 5.5rem);
  object-fit: contain;
}

.at__card-icon--sm {
  height: clamp(3rem, 5vw, 4.5rem);
}

.at__card-text {
  font-family: var(--font-body);
  font-size: var(--text-subhead);
  font-weight: 400;
  line-height: 1;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  margin: 0;
  text-align: center;
}

/* ── Photo strip ────────────────────────────────────────── */
.at__strip-photo {
  display: block;
  width: 100%;
  border-radius: var(--card-radius);
  object-fit: cover;
  max-height: 30rem;
}

/* ── Definition panel ───────────────────────────────────── */
.at__panel {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2.5rem;
  background-color: var(--color-white);
  border-radius: var(--card-radius);
}

.at__star {
  position: absolute;
  width: auto;
  height: 3.5rem;
  pointer-events: none;
  user-select: none;
}

.at__star--tl {
  top: -1.5rem;
  left: 2rem;
  transform: rotate(-10deg);
}

.at__star--br {
  bottom: -1.5rem;
  right: 3rem;
  transform: rotate(15deg);
}

.at__panel-divider {
  height: 1px;
  background-color: rgba(0, 0, 0, 0.15);
}

.at__panel-heading {
  font-family: var(--font-body);
  font-size: var(--text-subhead);
  font-weight: 400;
  line-height: 1;
  letter-spacing: var(--tracking-normal);
  color: var(--color-black);
  margin: 0 0 1rem;
}

.at__panel-text {
  font-family: var(--font-body);
  /* 75% of body-lg (~22px at 1280): the definition copy is ~3× longer than
     the original design, so it's scaled down to keep the panel's proportions */
  font-size: max(1rem, calc(var(--text-body-lg) * 0.75));
  font-weight: 300;
  line-height: 1.25;
  color: var(--color-black);
  margin: 0;
}

.at__panel-text + .at__panel-text {
  margin-top: 0.75em;
}

.at__panel-link {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 0.15em;
  transition: color 0.2s ease;
}

.at__panel-link:hover {
  color: var(--color-crimson);
}

/* ── Mobile adjustments ────────────────────────────────── */
@media (max-width: 640px) {
  .at__cards {
    grid-template-columns: 1fr;
  }

  .at__leaf {
    display: none;
  }
}

@media (min-width: 768px) {
  .at__panel {
    flex-direction: row;
    align-items: flex-start;
    gap: 0;
  }

  .at__panel-divider {
    width: 1px;
    height: auto;
    align-self: stretch;
    margin-inline: 2.5rem;
  }

  .at__panel-col {
    flex: 1;
  }
}
</style>
