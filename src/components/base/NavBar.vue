<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from './LanguageSwitcher.vue'

const { t } = useI18n()

const isMenuOpen = ref(false)

const navItems = [
  { key: 'home', href: '#main' },
  { key: 'artTherapy', href: '#arteterapia' },
  { key: 'about', href: '#sobre-mi' },
  { key: 'faq', href: '#preguntas-frecuentes' },
  { key: 'contact', href: '#contacto' },
]

// Which section is currently sitting behind the sticky nav — used to flip
// the nav's own background so it never blends into a same-colored section.
type SectionTone = 'base' | 'surface'
const SECTION_TONES: Record<string, SectionTone> = {
  main: 'base',
  arteterapia: 'surface',
  'sobre-mi': 'base',
  'preguntas-frecuentes': 'surface',
  contacto: 'surface',
}

const navRef = ref<HTMLElement | null>(null)
const activeTone = ref<SectionTone>('base')

let observer: IntersectionObserver | null = null

function observeSections() {
  observer?.disconnect()

  const navHeight = navRef.value?.offsetHeight ?? 64
  // Shrink the observed root down to a 1px line just below the nav, so
  // whichever section crosses that line is the one currently behind it.
  const bottomInset = Math.max(window.innerHeight - navHeight - 1, 0)

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const tone = SECTION_TONES[entry.target.id]
          if (tone) activeTone.value = tone
        }
      }
    },
    { rootMargin: `-${navHeight}px 0px -${bottomInset}px 0px`, threshold: 0 },
  )

  for (const id of Object.keys(SECTION_TONES)) {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  }
}

onMounted(() => {
  observeSections()
  window.addEventListener('resize', observeSections)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('resize', observeSections)
})
</script>

<template>
  <nav
    ref="navRef"
    class="nav-bar"
    :class="[
      activeTone === 'base' ? 'nav-bar--on-base' : 'nav-bar--on-surface',
    ]"
    :aria-label="t('nav.ariaLabel')"
  >
    <a class="nav-bar__brand" href="#main"
      >Arteterapia
      <span class="nav-bar__brand-dot" aria-hidden="true"></span> Candela</a
    >

    <div class="nav-bar__actions">
      <LanguageSwitcher />

      <button
        type="button"
        class="nav-bar__toggle"
        :class="{ 'nav-bar__toggle--open': isMenuOpen }"
        aria-controls="nav-bar-menu"
        :aria-expanded="isMenuOpen"
        @click="isMenuOpen = !isMenuOpen"
      >
        <span class="nav-bar__toggle-bar" />
        <span class="nav-bar__toggle-bar" />
        <span class="nav-bar__toggle-bar" />
        <span class="nav-bar__sr-only">{{
          isMenuOpen ? t('nav.toggleClose') : t('nav.toggleOpen')
        }}</span>
      </button>
    </div>

    <ul
      id="nav-bar-menu"
      class="nav-bar__list"
      :class="{ 'nav-bar__list--open': isMenuOpen }"
    >
      <li v-for="item in navItems" :key="item.href" class="nav-bar__item">
        <a class="nav-bar__link" :href="item.href" @click="isMenuOpen = false">
          {{ t(`nav.items.${item.key}`) }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.nav-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  height: var(--nav-height);
  padding-inline: 1.25rem;
  border-bottom: 1px solid transparent;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition:
    background-color 0.4s ease,
    border-color 0.4s ease,
    box-shadow 0.4s ease;
}

/* Section behind is plain --color-background (Main/About): lift the nav
   with the lighter surface tone so it doesn't disappear into it. */
.nav-bar--on-base {
  background-color: color-mix(in srgb, var(--color-surface) 92%, transparent);
  border-bottom-color: var(--color-border);
  box-shadow: var(--shadow-soft);
}

/* Section behind is already surface/tinted (ArtTherapy/FAQ/Contact): the
   original background-tinted nav reads fine against it. */
.nav-bar--on-surface {
  background-color: color-mix(
    in srgb,
    var(--color-background) 90%,
    transparent
  );
  border-bottom-color: color-mix(in srgb, var(--color-border) 55%, transparent);
  box-shadow: none;
}

.nav-bar__brand {
  font-family: var(--font-serif);
  font-size: 1.1875rem;
  font-weight: 400;
  color: var(--color-text);
  text-decoration: none;
  white-space: nowrap;
  letter-spacing: 0.01em;
  transition: color 0.2s ease;
}

.nav-bar__brand:hover,
.nav-bar__brand:focus-visible {
  color: var(--color-accent);
}

.nav-bar__brand-dot {
  display: inline-block;
  width: 0.3em;
  height: 0.3em;
  border-radius: 50%;
  background-color: var(--color-accent);
  vertical-align: middle;
}

.nav-bar__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}

.nav-bar__toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 2.25rem;
  height: 2.25rem;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
}

.nav-bar__toggle-bar {
  width: 1.5rem;
  height: 2px;
  background-color: var(--color-text);
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.nav-bar__toggle--open .nav-bar__toggle-bar:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.nav-bar__toggle--open .nav-bar__toggle-bar:nth-child(2) {
  opacity: 0;
}

.nav-bar__toggle--open .nav-bar__toggle-bar:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.nav-bar__sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.nav-bar__list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-bar__link {
  display: inline-block;
  padding: 0.5rem 0.75rem;
  color: var(--color-text);
  text-decoration: none;
  font-family: var(--font-sans);
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;
}

.nav-bar__link:hover,
.nav-bar__link:focus-visible {
  color: var(--color-accent);
  background-color: color-mix(in srgb, var(--color-border) 50%, transparent);
}

/* Mobile: hamburger + collapsible dropdown */
@media (max-width: 767px) {
  .nav-bar__list {
    position: absolute;
    top: var(--nav-height);
    left: 0;
    right: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    padding: 0.75rem 1rem 1.25rem;
    background-color: var(--color-background);
    border-bottom: 1px solid var(--color-border);
    box-shadow: var(--shadow-card);
    transform: translateY(-8px);
    opacity: 0;
    pointer-events: none;
    visibility: hidden;
    transition:
      transform 0.2s ease,
      opacity 0.2s ease,
      visibility 0s 0.2s;
  }

  .nav-bar__list--open {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
    visibility: visible;
    transition:
      transform 0.2s ease,
      opacity 0.2s ease,
      visibility 0s 0s;
  }

  .nav-bar__item {
    width: 100%;
    text-align: center;
  }
}

/* Desktop: brand left, language switcher + links right */
@media (min-width: 768px) {
  .nav-bar {
    justify-content: flex-start;
    gap: 1.5rem;
    padding-inline: 2rem;
  }

  .nav-bar__toggle {
    display: none;
  }

  .nav-bar__list {
    display: flex;
    gap: 0.25rem;
  }
}
</style>
