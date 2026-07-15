# Arteterapia Candela — TODO / Deuda técnica

Lista de pendientes y deuda técnica del proyecto, para no perderla de vista.

## SEO / metadata

- [ ] Comprar el dominio propio y actualizarlo (hoy se usa el subdominio de Netlify `https://leafy-melba-6cf4bb.netlify.app/`) en:
  - `index.html` (`canonical`, `og:url`)
  - `public/robots.txt` (línea `Sitemap:`)
  - `public/sitemap.xml` (`<loc>`)
- [ ] Conseguir un logo/foto para usar como `og:image` (imagen de previsualización al compartir en redes) y agregar el tag en `index.html`.
- [ ] Crear la cuenta de Instagram y descomentar/completar el enlace:
  - Placeholder en `index.html` (comentario junto a los meta tags)
  - `sameAs` en el bloque JSON-LD de `index.html`
- [ ] Agregar `theme-color`, `apple-touch-icon` y `manifest.json` una vez que exista una paleta de colores / logo definidos.

## Contenido

- [ ] Reemplazar el contenido placeholder de `src/App.vue` ("Pagina web de la Candela" / "La cucuruchita mas linda") por el contenido real del sitio.
- [ ] Definir y crear la(s) ruta(s) reales en `src/router/index.ts` (actualmente `routes: []`, vacío). El sitio se mantiene como SPA de una sola página, sin necesidad de rutas ni SEO por-ruta.
- [ ] Crear estructura de `components/` — hoy no existe.

## Configuración / deuda técnica

- [ ] Corregir el nombre del proyecto en `package.json` (`"name": "web-arteterapiacande"` está truncado/con typo).
- [ ] El deploy real es **Netlify**. El repo todavía tiene un workflow de GitHub Actions (`.github/workflows/deploy.yml`) que despliega a GitHub Pages, y `vite.config.ts` sigue teniendo la rama condicional `GITHUB_PAGES` para ese base path. Decidir si se eliminan (quedaron sin usarse) o si se mantienen como respaldo.
- [ ] Definir esquema de colores / diseño (no hay CSS global ni framework de estilos configurado todavía).
