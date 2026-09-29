<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

type Status = 'idle' | 'loading' | 'success' | 'error'

const status = ref<Status>('idle')

const fields = reactive({
  nombre: '',
  email: '',
  mensaje: '',
  'bot-field': '',
})

function encode(data: Record<string, string>) {
  return Object.entries(data)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&')
}

async function handleSubmit() {
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
  <section id="contacto" class="contact">
    <div class="contact__inner">
      <!-- Decorative illustrations -->
      <div class="contact__decor" aria-hidden="true">
        <img class="contact__decor-building" src="/edificio-400.webp" alt="" loading="lazy" decoding="async" />
        <img class="contact__decor-rainbow" src="/arcoiris-800.webp" alt="" loading="lazy" decoding="async" />
      </div>

      <!-- Heading -->
      <h2 class="contact__title">{{ t('contact.title') }}</h2>
      <p class="contact__lead">{{ t('contact.lead') }}</p>

      <!-- Success state -->
      <div v-if="status === 'success'" class="contact__success" role="alert">
        <p class="contact__success-title">{{ t('contact.success.title') }}</p>
        <p class="contact__success-body">{{ t('contact.success.body') }}</p>
        <button class="contact__retry" type="button" @click="status = 'idle'">
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

        <div class="contact__honeypot" aria-hidden="true">
          <label>
            {{ t('contact.honeypotLabel') }}
            <input v-model="fields['bot-field']" name="bot-field" type="text" tabindex="-1" autocomplete="off" />
          </label>
        </div>

        <div class="contact__field">
          <label class="contact__label" for="c-nombre">
            {{ t('contact.labels.nombre') }} <span aria-hidden="true">*</span>
          </label>
          <input
            id="c-nombre"
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
          <label class="contact__label" for="c-email">
            {{ t('contact.labels.email') }} <span aria-hidden="true">*</span>
          </label>
          <input
            id="c-email"
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
          <label class="contact__label" for="c-mensaje">
            {{ t('contact.labels.mensaje') }} <span aria-hidden="true">*</span>
          </label>
          <textarea
            id="c-mensaje"
            v-model="fields.mensaje"
            class="contact__input contact__textarea"
            name="mensaje"
            rows="4"
            required
            aria-required="true"
            :disabled="status === 'loading'"
          ></textarea>
        </div>

        <p v-if="status === 'error'" class="contact__error" role="alert">
          {{ t('contact.error') }}
        </p>

        <button
          class="contact__submit"
          type="submit"
          :disabled="status === 'loading' || !fields.nombre || !fields.email || !fields.mensaje"
        >
          <span v-if="status === 'loading'" class="contact__spinner" aria-hidden="true"></span>
          {{ status === 'loading' ? t('contact.submit.loading') : t('contact.submit.idle') }}
        </button>
      </form>

      <p class="contact__phone">
        {{ t('contact.phonePrefix') }}
        <a href="tel:+34692665220">{{ t('contact.phoneCta') }}</a>
      </p>
    </div>
  </section>
</template>

<style scoped>
.contact {
  background-color: var(--color-white);
  padding-block: var(--section-padding);
}

.contact__inner {
  max-width: var(--page-max);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

/* ── Decorations ────────────────────────────────────────── */
.contact__decor {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 4rem;
  pointer-events: none;
  user-select: none;
  margin-bottom: 0.5rem;
}

.contact__decor-building {
  display: block;
  width: auto;
  height: clamp(4rem, 7vw, 7.5rem);
  transform: rotate(-3deg);
}

.contact__decor-rainbow {
  display: block;
  width: auto;
  height: clamp(3.5rem, 6vw, 6rem);
  transform: rotate(5deg);
}

/* ── Heading ────────────────────────────────────────────── */
.contact__title {
  font-family: var(--font-body);
  font-size: var(--text-headline);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: var(--tracking-tight);
  text-align: center;
  color: var(--color-black);
  margin: 0;
}

.contact__lead {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  line-height: 1.17;
  letter-spacing: 0;
  text-align: center;
  color: var(--color-black);
  max-width: 52ch;
  margin: 0;
}

/* ── Form ───────────────────────────────────────────────── */
.contact__form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
  max-width: 44rem;
}

.contact__honeypot {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.contact__field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact__label {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  letter-spacing: var(--tracking-tight);
  color: var(--color-black);
}

.contact__input {
  width: 100%;
  padding: 0 1rem;
  height: 3.8125rem;
  font-family: var(--font-body);
  font-size: 1rem;
  color: var(--color-black);
  background-color: var(--color-cream);
  border: 1px solid var(--color-gray);
  border-radius: var(--card-radius);
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.contact__textarea {
  height: auto;
  padding-top: 1rem;
  padding-bottom: 1rem;
  resize: vertical;
}

.contact__input:focus {
  border-color: var(--color-black);
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.08);
}

.contact__input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.contact__error {
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--color-crimson);
  margin: 0;
}

.contact__submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  align-self: center;
  padding: 0 2.5rem;
  height: 3.8125rem;
  background-color: var(--color-crimson);
  color: var(--color-white);
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  letter-spacing: var(--tracking-tight);
  border: none;
  border-radius: var(--card-radius);
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    transform 0.2s ease;
}

.contact__submit:hover:not(:disabled) {
  background-color: color-mix(in srgb, var(--color-crimson) 85%, black);
  transform: translateY(-2px);
}

.contact__submit:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.contact__spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Success ────────────────────────────────────────────── */
.contact__success {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
  padding: 3rem 2rem;
  background-color: var(--color-cream);
  border-radius: var(--card-radius);
  max-width: 44rem;
  width: 100%;
}

.contact__success-title {
  font-family: var(--font-body);
  font-size: var(--text-subhead);
  font-weight: 400;
  letter-spacing: var(--tracking-tight);
  margin: 0;
}

.contact__success-body {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  color: var(--color-black);
  margin: 0;
}

.contact__retry {
  padding: 0.625rem 1.5rem;
  font-family: var(--font-body);
  font-size: 1rem;
  background: none;
  border: 1px solid var(--color-black);
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.contact__retry:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* ── Phone ──────────────────────────────────────────────── */
.contact__phone {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: 300;
  letter-spacing: 0;
  text-align: center;
  color: var(--color-black);
  margin: 0;
}

.contact__phone a {
  color: var(--color-black);
  text-decoration: underline;
  text-underline-offset: 0.15em;
  transition: color 0.2s ease;
}

.contact__phone a:hover {
  color: var(--color-crimson);
}
</style>
