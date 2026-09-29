<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from './LanguageSwitcher.vue'

const { t } = useI18n()

const isMenuOpen = ref(false)
const showBackToTop = ref(false)

const navItems = [
  { key: 'home', href: '#main' },
  { key: 'artTherapy', href: '#arteterapia' },
  { key: 'about', href: '#sobre-mi' },
  { key: 'faq', href: '#preguntas-frecuentes' },
  { key: 'contact', href: '#contacto' },
]

function onScroll() {
  showBackToTop.value = window.scrollY > window.innerHeight * 0.8
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <nav class="nav" :aria-label="t('nav.ariaLabel')">
    <div class="nav__inner">
      <ul class="nav__list nav__list--desktop" role="list">
        <li v-for="item in navItems" :key="item.href">
          <a class="nav__pill" :href="item.href">
            {{ t(`nav.items.${item.key}`) }}
          </a>
        </li>
        <li>
          <LanguageSwitcher class="nav__lang-pill" />
        </li>
      </ul>

      <!-- Mobile: just show brand pill + hamburger -->
      <div class="nav__mobile-bar">
        <a class="nav__pill" href="#main">Candela</a>
        <button
          type="button"
          class="nav__hamburger"
          :aria-expanded="isMenuOpen"
          aria-controls="nav-mobile-menu"
          @click="isMenuOpen = !isMenuOpen"
        >
          <span class="nav__bar" />
          <span class="nav__bar" />
          <span class="nav__bar" />
          <span class="sr-only">{{
            isMenuOpen ? t('nav.toggleClose') : t('nav.toggleOpen')
          }}</span>
        </button>
      </div>

      <!-- Mobile dropdown -->
      <ul
        id="nav-mobile-menu"
        class="nav__list nav__list--mobile"
        :class="{ 'nav__list--open': isMenuOpen }"
        role="list"
      >
        <li v-for="item in navItems" :key="item.href">
          <a class="nav__pill nav__pill--mobile" :href="item.href" @click="isMenuOpen = false">
            {{ t(`nav.items.${item.key}`) }}
          </a>
        </li>
        <li>
          <LanguageSwitcher class="nav__lang-pill" />
        </li>
      </ul>
    </div>
  </nav>

  <!-- Back-to-top -->
  <Transition name="btt">
    <button
      v-if="showBackToTop"
      type="button"
      class="back-to-top"
      :aria-label="t('nav.backToTop')"
      @click="scrollToTop"
    >
      ↑
    </button>
  </Transition>
</template>

<style scoped>
.nav {
  position: relative;
  z-index: 100;
  padding: 1.0625rem var(--page-gutter) 0.3125rem;
  background-color: var(--color-white);
}

.nav__inner {
  max-width: var(--page-max);
  margin-inline: auto;
}

/* Desktop */
.nav__list--desktop {
  display: none;
  justify-content: space-between;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav__pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 3.75rem;
  padding: 0 1.875rem;
  background-color: rgba(255, 255, 255, 0.61);
  box-shadow: var(--shadow-pill);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 1.875rem;
  font-family: var(--font-body);
  font-size: var(--text-label);
  font-weight: 400;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
  text-decoration: none;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    box-shadow 0.2s ease;
}

.nav__pill:hover,
.nav__pill:focus-visible {
  background-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08), var(--shadow-pill);
}

/* Mobile bar */
.nav__mobile-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav__hamburger {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 3rem;
  height: 3rem;
  padding: 0;
  background: rgba(255, 255, 255, 0.61);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  align-items: center;
  box-shadow: var(--shadow-pill);
}

.nav__bar {
  display: block;
  width: 1.25rem;
  height: 2px;
  background-color: var(--color-black);
  border-radius: 1px;
}

.nav__list--mobile {
  list-style: none;
  margin: 0.5rem 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.3s ease;
}

.nav__list--open {
  max-height: 30rem;
}

.nav__pill--mobile {
  width: 100%;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.61);
}

.nav__lang-pill {
  height: 3.75rem;
  display: inline-flex;
  align-items: center;
  padding: 0 1.25rem;
  background-color: rgba(255, 255, 255, 0.61);
  box-shadow: var(--shadow-pill);
  border-radius: 1.875rem;
  font-size: var(--text-label);
  letter-spacing: var(--tracking-tight);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Back to top */
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 200;
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 50%;
  border: none;
  background-color: var(--color-black);
  color: var(--color-white);
  font-size: 1.125rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition:
    background-color 0.2s ease,
    transform 0.2s ease;
}

.back-to-top:hover {
  background-color: var(--color-crimson);
  transform: translateY(-2px);
}

.btt-enter-active,
.btt-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.btt-enter-from,
.btt-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

/* Desktop layout */
@media (min-width: 768px) {
  .nav__mobile-bar {
    display: none;
  }

  .nav__list--mobile {
    display: none !important;
  }

  .nav__list--desktop {
    display: flex;
    width: 100%;
  }
}
</style>
