<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseSection from '../base/BaseSection.vue'

const { t } = useI18n()

type Status = 'idle' | 'loading' | 'success' | 'error'

const status = ref<Status>('idle')

const fields = reactive({
  nombre: '',
  email: '',
  mensaje: '',
  'bot-field': '', // honeypot — must stay empty for real users
})

function encode(data: Record<string, string>) {
  return Object.entries(data)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&')
}

async function handleSubmit() {
  // Honeypot triggered — silently abort
  if (fields['bot-field']) return

  status.value = 'loading'

  try {
    const res = await fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: encode({
        'form-name': 'contacto',
        nombre: fields.nombre,
        email: fields.email,
        mensaje: fields.mensaje,
      }),
    })

    if (!res.ok) throw new Error(`HTTP ${res.status}`)

    status.value = 'success'
    fields.nombre = ''
    fields.email = ''
    fields.mensaje = ''
  } catch {
    status.value = 'error'
  }
}
</script>

<template>
  <BaseSection id="contacto" class="bg-tinted">
    <div class="contact">
      <div class="contact__header">
        <h2 class="contact__title">{{ t('contact.title') }}</h2>
        <p class="contact__lead">
          {{ t('contact.lead') }}
        </p>

        <!-- Decorative only, same treatment as the FAQ heading: flanking the
             heading on wide screens (out of the flow), a small centred pair
             under it below 1024px. -->
        <div class="contact__decor" aria-hidden="true">
          <img
            class="contact__drawing contact__drawing--building"
            src="/edificio-400.webp"
            alt=""
            loading="lazy"
            decoding="async"
          />
          <img
            class="contact__drawing contact__drawing--star"
            src="/estrella-400.webp"
            alt=""
            loading="lazy"
            decoding="async"
          />
        </div>
      </div>

      <div class="contact__body">
        <!-- Contact form -->
        <div class="contact__form-wrap">
          <!-- Success state -->
          <div
            v-if="status === 'success'"
            class="contact__success"
            role="alert"
          >
            <span class="contact__success-icon" aria-hidden="true">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="9"
                  stroke="currentColor"
                  stroke-width="1.5"
                />
                <path
                  d="M8 12.5l2.5 2.5L16 9"
                  stroke="currentColor"
                  stroke-width="1.75"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </span>
            <h3>{{ t('contact.success.title') }}</h3>
            <p>{{ t('contact.success.body') }}</p>
            <button class="contact__retry-btn" @click="status = 'idle'">
              {{ t('contact.success.retry') }}
            </button>
          </div>

          <!-- Form -->
          <form
            v-else
            class="contact__form"
            name="contacto"
            method="POST"
            data-netlify="true"
            netlify-honeypot="bot-field"
            novalidate
            @submit.prevent="handleSubmit"
          >
            <input type="hidden" name="form-name" value="contacto" />

            <!-- Honeypot: visually hidden, bots fill it, humans don't -->
            <div class="contact__honeypot" aria-hidden="true">
              <label>
                {{ t('contact.honeypotLabel') }}
                <input
                  v-model="fields['bot-field']"
                  name="bot-field"
                  type="text"
                  tabindex="-1"
                  autocomplete="off"
                />
              </label>
            </div>

            <p class="contact__required-note">
              <span aria-hidden="true">*</span> {{ t('contact.requiredNote') }}
            </p>

            <div class="contact__field">
              <label class="contact__label" for="contact-nombre">
                {{ t('contact.labels.nombre') }}
                <span class="contact__required-mark" aria-hidden="true">*</span>
              </label>
              <input
                id="contact-nombre"
                v-model="fields.nombre"
                class="contact__input"
                name="nombre"
                type="text"
                autocomplete="name"
                required
                aria-required="true"
                :disabled="status === 'loading'"
              />
            </div>

            <div class="contact__field">
              <label class="contact__label" for="contact-email">
                {{ t('contact.labels.email') }}
                <span class="contact__required-mark" aria-hidden="true">*</span>
              </label>
              <input
                id="contact-email"
                v-model="fields.email"
                class="contact__input"
                name="email"
                type="email"
                autocomplete="email"
                required
                aria-required="true"
                :disabled="status === 'loading'"
              />
            </div>

            <div class="contact__field">
              <label class="contact__label" for="contact-mensaje">
                {{ t('contact.labels.mensaje') }}
                <span class="contact__required-mark" aria-hidden="true">*</span>
              </label>
              <textarea
                id="contact-mensaje"
                v-model="fields.mensaje"
                class="contact__textarea"
                name="mensaje"
                rows="5"
                required
                aria-required="true"
                :disabled="status === 'loading'"
              ></textarea>
            </div>

            <!-- Error banner -->
            <p v-if="status === 'error'" class="contact__error" role="alert">
              {{ t('contact.error') }}
            </p>

            <button
              class="contact__submit"
              type="submit"
              :disabled="
                status === 'loading' ||
                !fields.nombre ||
                !fields.email ||
                !fields.mensaje
              "
            >
              <span
                v-if="status === 'loading'"
                class="contact__spinner"
                aria-hidden="true"
              ></span>
              {{
                status === 'loading'
                  ? t('contact.submit.loading')
                  : t('contact.submit.idle')
              }}
            </button>
          </form>
        </div>
      </div>

      <p class="contact__phone">
        {{ t('contact.phonePrefix') }}
        <a href="tel:+34692665220">{{ t('contact.phoneCta') }}</a>
      </p>
    </div>
  </BaseSection>
</template>

<style scoped>
.contact {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.5rem;
}

.contact__header {
  position: relative;
  text-align: center;
  width: 100%;
}

.contact__decor {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1.5rem;
  pointer-events: none;
  user-select: none;
}

/* Height (never width) is the fixed dimension, so the row's space is reserved
   before the lazy-loaded files arrive and nothing jumps when they do. */
.contact__drawing {
  display: block;
  width: auto;
}

.contact__drawing--building {
  height: 3.5rem;
  transform: rotate(-3deg);
}

.contact__drawing--star {
  height: 2.75rem;
  transform: rotate(6deg);
}

.contact__title {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(1.75rem, 3vw + 1rem, 2.5rem);
  margin: 0 0 0.875rem;
}

.contact__lead {
  font-family: var(--font-sans);
  font-size: 1.0625rem;
  line-height: 1.7;
  color: var(--color-text-light);
  max-width: 50ch;
  margin: 0 auto;
}

.contact__body {
  width: 100%;
}

/* --- Form --- */
.contact__form-wrap {
  flex: 1;
}

.contact__form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: var(--shadow-soft);
}

/* Honeypot: completely invisible to real users */
.contact__honeypot {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.contact__required-note {
  font-family: var(--font-sans);
  font-size: 0.8125rem;
  color: var(--color-text-light);
  margin: 0;
}

.contact__required-mark {
  color: var(--color-accent);
  font-weight: 700;
  margin-left: 0.125rem;
}

.contact__field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.contact__label {
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text);
}

.contact__input,
.contact__textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  font-family: var(--font-sans);
  font-size: 1rem;
  color: var(--color-text);
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 0.625rem;
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
  resize: vertical;
}

.contact__input::placeholder,
.contact__textarea::placeholder {
  color: var(--color-text-light);
  opacity: 0.6;
}

.contact__input:focus,
.contact__textarea:focus {
  border-color: var(--color-secondary);
  box-shadow: 0 0 0 3px
    color-mix(in srgb, var(--color-secondary) 20%, transparent);
}

.contact__input:disabled,
.contact__textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.contact__error {
  font-family: var(--font-sans);
  font-size: 0.9rem;
  color: #b91c1c;
  background-color: color-mix(in srgb, #b91c1c 8%, transparent);
  border: 1px solid color-mix(in srgb, #b91c1c 25%, transparent);
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  margin: 0;
}

.contact__submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  padding: 0.9375rem 2rem;
  background-color: var(--color-accent);
  color: var(--color-surface);
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 0.9375rem;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  letter-spacing: 0.02em;
  box-shadow: 0 4px 16px
    color-mix(in srgb, var(--color-accent) 30%, transparent);
  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.contact__submit:hover:not(:disabled) {
  background-color: color-mix(in srgb, var(--color-accent) 85%, black);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px
    color-mix(in srgb, var(--color-accent) 40%, transparent);
}

.contact__submit:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Loading spinner */
.contact__spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid color-mix(in srgb, var(--color-surface) 40%, transparent);
  border-top-color: var(--color-surface);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Success state */
.contact__success {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.875rem;
  padding: 2.5rem 2rem;
  background-color: var(--color-surface);
  border: 1px solid
    color-mix(in srgb, var(--color-secondary) 50%, var(--color-border));
  border-radius: 1.5rem;
  box-shadow: var(--shadow-soft);
}

.contact__success-icon {
  width: 3rem;
  height: 3rem;
  color: var(--color-secondary);
}

.contact__success-icon svg {
  width: 100%;
  height: 100%;
}

.contact__success h3 {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: 1.375rem;
  margin: 0;
}

.contact__success p {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  line-height: 1.6;
  margin: 0;
  max-width: 36ch;
}

.contact__retry-btn {
  margin-top: 0.5rem;
  padding: 0.5rem 1.25rem;
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-light);
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  cursor: pointer;
  transition:
    color 0.2s ease,
    border-color 0.2s ease;
}

.contact__retry-btn:hover {
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.contact__phone {
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  color: var(--color-text-light);
  text-align: center;
  margin: 0;
}

.contact__phone a {
  color: var(--color-text);
  font-weight: 500;
  text-decoration: none;
  border-bottom: 1px solid var(--color-border);
  transition:
    color 0.2s ease,
    border-color 0.2s ease;
}

.contact__phone a:hover,
.contact__phone a:focus-visible {
  color: var(--color-accent);
  border-color: var(--color-accent);
}

@media (min-width: 768px) {
  .contact__form-wrap {
    max-width: 44rem;
    margin-inline: auto;
    width: 100%;
  }
}

/* Same 52rem band as the FAQ heading, so both sections sit their drawings at
   an identical distance from the title. */
@media (min-width: 1024px) {
  .contact__decor {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: min(52rem, calc(100vw - 8rem));
    transform: translateX(-50%);
    justify-content: space-between;
    margin: 0;
  }

  /* The building is much narrower than the star, so it needs a nudge inward
     to look equally close to the title. */
  .contact__drawing--building {
    height: clamp(5rem, 7vw, 7.5rem);
    margin-left: 2.5rem;
    transform: rotate(-3deg);
  }

  .contact__drawing--star {
    height: clamp(4rem, 5.5vw, 5.5rem);
    transform: rotate(5deg);
  }
}
</style>
