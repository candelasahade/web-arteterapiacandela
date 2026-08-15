# Tech Debt — Arteterapia Candela

Items that cannot be resolved without content or decisions from Candela.
Hand this file back to Claude when each item is ready to close.

> **Dibujos a mano.** Varios de los ítems de abajo (og:image, logo, imagen del
> hero, iconos PWA) se resuelven con dibujos de Candela. El circuito ya está
> montado: ella captura siguiendo `GUIA-CAPTURA-DIBUJOS.md`, los originales se
> dejan en `raw-art/`, y `tools/process_art.py` / `tools/digitize.py` generan
> los assets finales en `public/`. No hace falta Adobe ni ninguna herramienta
> de pago.

---

## Needs: Real photo or logo for social sharing (`og:image`)

Without an image, shares on WhatsApp, Instagram DM, or Twitter/X show no preview.

The leaf drawings digitized so far (`adorno-hoja*`) are square (1407×1407) and
won't work directly here — this needs a **landscape** asset.

What to provide:
- A photo of Candela, a branded image, or a logo, composed/cropped to 16:9
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
- **Proper apple-touch-icon crop** — currently points at `/adorno-hoja-negro-master.png`, the full 1407×1407 master (188 KB). Works, but a purpose-cropped 180×180 opaque PNG would be much lighter. `tools/digitize.py` now supports `--sizes 180 --png`; just needs a sandbox run against the source drawing, e.g. `python3 tools/digitize.py raw-art/PruebaIcono1.PNG --out public --name apple-touch-icon --square --fill "#dedacd" --sizes 180 --png`, then swap the `index.html` link over.
- **PWA manifest** — add `theme-color` and a `manifest.json` (with 192/512 icons) now that a logo mark exists, if an installable/PWA experience is wanted.
