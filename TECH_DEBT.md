# Tech Debt — Arteterapia Candela

Items that cannot be resolved without content or decisions from Candela.
Hand this file back to Claude when each item is ready to close.

---

## Needs: Real photo or logo for social sharing (`og:image`)

Without an image, shares on WhatsApp, Instagram DM, or Twitter/X show no preview.

What to provide:
- A photo of Candela, a branded image, or a logo
- Recommended size: **1200 × 630 px** (16:9), JPG or PNG
- Save it to `/public/og-image.jpg` (or similar name)
- Then add this line to `index.html` inside `<head>`, replacing the TODO comment:
  ```html
  <meta property="og:image" content="https://arteterapiacandela.com/og-image.jpg">
  ```

---

## Needs: Candela's real photo (About section)

The "Sobre mí" section currently shows a placeholder avatar.

What to provide:
- A portrait photo of Candela
- Recommended: square or slightly portrait crop, at least 400 × 400 px
- Save it to `/public/` and replace the placeholder `<div>` in `AboutSection.vue` with:
  ```html
  <img class="about__photo" src="/your-photo.jpg" alt="Foto de Candela, arteterapeuta" />
  ```
- Also remove the `.about__photo-ring` decorative div — it was designed for the placeholder.

---

## Needs: Candela's bio and experience text

The "Sobre mí" section has three blocks that need real content:

- **Qué me llevó a la arteterapia** — current text is approximate, needs her own words
- **Formación** — only has "Magíster en Arteterapia Relacional", confirm if complete
- **Experiencia** — currently a blank placeholder, needs real trajectory and projects

File to edit: `src/components/sections/AboutSection.vue`

---

## Needs: FAQ final answers from Candela

Two FAQ answers are still placeholders and need Candela's input:

| Question | Status |
|---|---|
| ¿Necesito saber dibujar o pintar? | ✓ OK |
| **¿A partir de qué edad pueden participar los niños?** | ⚠ PLACEHOLDER |
| ¿Las sesiones son online o presenciales? | ✓ OK |
| ¿Cómo sé si la arteterapia es adecuada para mi hijo o hija? | ✓ OK |
| **¿Cuánto dura el proceso terapéutico?** | ⚠ PLACEHOLDER |

Once confirmed, update **both** places:
1. `src/components/sections/FaqSection.vue` — what users see on the page
2. `index.html` — the `FAQPage` JSON-LD script (what Google indexes for rich snippets)

---

## Needs: LinkedIn profile URL

The LinkedIn icon is not shown in the footer to avoid a broken link.
When the profile URL is available, re-add this block inside `<ul class="footer__social">` in `SiteFooter.vue`:

```html
<li>
  <a
    class="footer__social-link"
    href="https://www.linkedin.com/in/TU-PERFIL"
    target="_blank"
    rel="noopener noreferrer"
    aria-label="LinkedIn de Arteterapia Candela"
  >
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect x="2" y="2" width="20" height="20" rx="4" stroke="currentColor" stroke-width="1.5" />
      <path d="M7 10v7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
      <path d="M11 17v-4c0-1.657 1.343-3 3-3s3 1.343 3 3v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
      <path d="M11 10v7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
      <circle cx="7" cy="7.5" r="1" fill="currentColor" />
    </svg>
  </a>
</li>
```

---

## Nice to have (no external dependency)

- **Self-host fonts** — currently loaded from Google Fonts (third-party request, GDPR concern). Self-hosting Inter + Libre Baskerville improves LCP and removes the dependency. Use [google-webfonts-helper](https://gwfh.mranftl.com/) to download the woff2 files.
- **LocalBusiness schema enrichment** — add `openingHours`, `priceRange`, and `image` fields to the JSON-LD in `index.html` once confirmed with Candela.
- **Hero image** — the abstract paint composition in the hero is a temporary placeholder. Replace `.main-section__visual` with a real `<img>` (workspace, art materials, or Candela working) when a photo is available.
- **PWA icons** — add `theme-color`, `apple-touch-icon`, and `manifest.json` once a logo exists.
