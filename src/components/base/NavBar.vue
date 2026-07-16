<script setup lang="ts">
import { ref } from 'vue'

const isMenuOpen = ref(false)

const navItems = [
  { label: 'Inicio', href: '#main' },
  { label: 'Sobre mí', href: '#sobre-mi' },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Testimonios', href: '#testimonios' },
  { label: 'Contacto', href: '#contacto' },
]
</script>

<template>
  <nav class="nav-bar">
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
      <span class="nav-bar__sr-only">Abrir menú</span>
    </button>

    <ul
      id="nav-bar-menu"
      class="nav-bar__list"
      :class="{ 'nav-bar__list--open': isMenuOpen }"
    >
      <li v-for="item in navItems" :key="item.href" class="nav-bar__item">
        <a class="nav-bar__link" :href="item.href" @click="isMenuOpen = false">
          {{ item.label }}
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
  padding-inline: 1rem;
  background-color: var(--color-bg);
  border-bottom: 1px solid var(--color-accent-soft);
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
  font-weight: 500;
  border-radius: 0.375rem;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;
}

.nav-bar__link:hover,
.nav-bar__link:focus-visible {
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
}

/* Mobile: hamburger + collapsible dropdown panel */
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
    padding: 0.5rem 1rem 1rem;
    background-color: var(--color-bg);
    border-bottom: 1px solid var(--color-accent-soft);
    transform: translateY(-8px);
    opacity: 0;
    pointer-events: none;
    transition:
      transform 0.2s ease,
      opacity 0.2s ease;
  }

  .nav-bar__list--open {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }

  .nav-bar__item {
    width: 100%;
    text-align: center;
  }
}

/* Desktop: centered row, no hamburger */
@media (min-width: 768px) {
  .nav-bar {
    justify-content: center;
  }

  .nav-bar__toggle {
    display: none;
  }

  .nav-bar__list {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
  }
}
</style>
