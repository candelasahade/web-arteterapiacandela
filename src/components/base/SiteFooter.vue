<script setup lang="ts">
</script>

<template>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__content">
        <div class="footer__brand">
          <p class="footer__name">Arteterapia Candela</p>
          <p class="footer__tagline">
            Un espacio terapéutico y creativo para crecer a través del arte.
          </p>
        </div>

        <nav class="footer__nav" aria-label="Redes sociales">
          <ul class="footer__social">
            <li>
              <a
                class="footer__social-link"
                href="https://www.instagram.com/arteterapia.candela"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Instagram de Arteterapia Candela"
              >
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <rect x="2" y="2" width="20" height="20" rx="5.5" stroke="currentColor" stroke-width="1.5" />
                  <circle cx="12" cy="12" r="4.5" stroke="currentColor" stroke-width="1.5" />
                  <circle cx="17.5" cy="6.5" r="1" fill="currentColor" />
                </svg>
              </a>
            </li>
            <!-- TODO: add LinkedIn link once URL is available (see TECH_DEBT.md) -->
          </ul>
        </nav>
      </div>

      <hr class="footer__divider" />

      <div class="footer__bottom">
        <p class="footer__copyright">© {{ new Date().getFullYear() }} Arteterapia Candela</p>
        <p class="footer__location">Barcelona · Sant Cugat del Vallès</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  width: 100%;
  background-color: var(--color-surface);
  border-top: 1px solid var(--color-border);
}

.footer__inner {
  max-width: 1200px;
  margin-inline: auto;
  padding: 3rem 1.25rem 2rem;
}

.footer__content {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  padding-bottom: 2rem;
}

.footer__brand {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.footer__name {
  font-family: var(--font-serif);
  font-size: 1.125rem;
  margin: 0;
  color: var(--color-text);
}

.footer__tagline {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  margin: 0;
  line-height: 1.5;
  max-width: 36ch;
}

.footer__social {
  display: flex;
  gap: 0.625rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.footer__social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.375rem;
  height: 2.375rem;
  color: var(--color-text-light);
  text-decoration: none;
  border: 1px solid var(--color-border);
  border-radius: 0.625rem;
  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.footer__social-link svg {
  width: 1.125rem;
  height: 1.125rem;
}

.footer__social-link:hover,
.footer__social-link:focus-visible {
  color: var(--color-accent);
  border-color: var(--color-accent);
  background-color: color-mix(in srgb, var(--color-accent) 7%, transparent);
}

.footer__divider {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 0;
}

.footer__bottom {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding-top: 1.5rem;
  text-align: center;
}

.footer__copyright,
.footer__location {
  font-family: var(--font-sans);
  font-size: 0.8125rem;
  color: var(--color-text-light);
  margin: 0;
}

@media (min-width: 640px) {
  .footer__inner {
    padding-inline: 2rem;
  }
}

@media (min-width: 768px) {
  .footer__content {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }

  .footer__bottom {
    flex-direction: row;
    justify-content: space-between;
    text-align: left;
  }
}

@media (min-width: 1024px) {
  .footer__inner {
    padding-inline: 3rem;
  }
}
</style>
