# Digitizing Candela's hand-made drawings

How original drawings get from paper into `public/` as production assets, with no
Adobe tool anywhere in the chain. Candela's side of this is one page:
`docs/Guia-fotos-dibujos-Candela.pdf` — send her that, not this file.

---

## 1. The handoff contract

| | Preferred | Acceptable | Rejected |
|---|---|---|---|
| **Device** | Flatbed scanner / MFP, 600 dpi, colour | Phone + built-in scanner app (iOS Notes, Google Drive) | Plain phone photo at an angle |
| **Format** | PNG or TIFF | JPEG at max quality, HEIC | Anything re-encoded by a chat app |
| **Colour mode** | Colour / Photo, no auto-enhance | — | "Document" / "Black & white" filters |
| **Transport** | Email attachment, Drive, or dropped straight into this repo folder | WhatsApp **as document** | WhatsApp **as photo** |
| **Per file** | one drawing, `01-hoja.png` | — | collages, multi-drawing sheets |

The one thing worth being strict about is **shadows** (see §5). Everything else I
can compensate for computationally; a shadow I can only trade against the artwork.

Alongside the files, one line per drawing is enough:

```
01-hoja      line   — small divider between sections
02-flor      line   — logo candidate
03-mancha    wash   — hero background
```

`line` = one-colour strokes (pen, marker, fineliner) → can become true vector.
`wash` = watercolour, pencil shading, gradients → stays raster, keeps its texture.

Drop the originals in `assets-originales/` (gitignored) and tell me they're there —
I stage them from the connected folder and work from a copy.

## 2. What I run

`tools/digitize.py` — pure NumPy/OpenCV/Pillow, no network, no binaries beyond
what's already in the container.

```bash
python3 tools/digitize.py assets-originales/01-hoja.png \
        --out public/img --name hoja --trace --ink "#3b3a46"
```

| Flag | Effect |
|---|---|
| `--trace` | also emit `<name>.svg` — only for `line` drawings |
| `--ink "#hex"` | flatten the artwork to a single brand colour |
| `--bg poly` (default) | polynomial paper model — **keeps large washes** |
| `--bg morph` | morphological paper model — kills shadows, **also eats large washes** |

Outputs per drawing:

```
<name>-master.png   full-res RGBA, paper removed, lossless — archive copy
<name>-1600.webp    web raster with alpha (+ -800, -400 for srcset)
<name>.svg          vector trace (with --trace)
<name>-check.png    original | flattened | matte-on-checkerboard, for eyeballing
```

Pipeline: flatten uneven lighting → neutralise the paper's colour cast → build a
soft alpha matte (paper transparent, antialiased strokes preserved) → despeckle →
autocrop → export. The tracer is contour-based: contours are Gaussian-smoothed
along arc length, simplified with an **absolute** pixel tolerance, then fitted with
**centripetal** Catmull-Rom → cubic Béziers, with holes emitted as subpaths of
their parent so `fill-rule="evenodd"` punches them out.

Validated end to end on a synthetic phone-scan (uneven window light + soft shadow +
warm cast + JPEG artefacts): the 27 kB traced SVG is visually indistinguishable
from the 1 MB master raster, including stroke-weight variation and hand wobble.

## 3. Which format per asset

| Asset | Output | Why |
|---|---|---|
| Logo, favicon, PWA icons | **SVG** (+ ICO/PNG derivatives) | must stay crisp at 16 px and 512 px |
| Section dividers, small flourishes | **SVG**, inlined in the Vue component | recolourable with `currentColor`, no extra request |
| Hero / section illustrations | **WebP** with alpha, `srcset` 400/800/1600 | vectorising a wash destroys the exact thing that makes it hers |
| `og:image` | **JPEG 1200×630**, composited on `#dedacd` | social scrapers don't do transparency reliably |

Inlined SVG is preferred for anything small and monochrome — it can inherit the
palette from `base.css` instead of hard-coding `#3b3a46`:

```vue
<span class="divider" aria-hidden="true" v-html="dividerSvg" />
```
```css
.divider svg { width: 100%; height: auto; fill: var(--color-secondary); }
```

## 4. Why not the usual tools

`potrace`, `vtracer`, `autotrace`, `inkscape` and `svgo` are all blocked in this
sandbox — apt, PyPI and npm are behind an allowlist that returns 403 for them. That
is why `tools/digitize.py` implements its own tracer rather than shelling out to
potrace. It is not a compromise on output quality, but it *is* the reason the code
is longer than a wrapper script would be.

If you ever want to hand-tune a path on your own machine, the non-Adobe options are
[Inkscape](https://inkscape.org) (free, `Path → Trace Bitmap`, potrace under the
hood), [VTracer](https://www.visioncortex.org/vtracer/) (better on colour), or
[SVGcode](https://svgco.de/) (potrace in the browser, nothing to install). None of
them are needed for the normal flow.

## 5. Known limits — read before blaming the script

**Shadow vs. wash is a real trade-off, not a bug.** The paper model has to be
smooth enough to not confuse artwork with lighting. A degree-3 polynomial can't
bend around a soft shadow, so the shadow survives into the matte as a grey halo; a
degree-5 polynomial or the morphological estimate removes the shadow *and* any
large soft wash along with it. Measured on the test scan: `--bg poly` leaves 13% of
the frame as halo when a shadow is present, `--bg morph` leaves 0.5% but drops the
wash entirely. **The fix is at capture time, not in post.** Hence the emphasis in
Candela's guide.

Other limits:

- **Curled paper** produces a shadow band along the curl. Same problem, same fix.
- **Very light pencil** may fall under the matte's white point. Tune `build_alpha(white=…)` downward per drawing rather than globally.
- **Coloured paper** breaks the white-point assumption. Tell me and I'll change the model.
- The tracer handles **line art and flat silhouettes**. It has no multi-colour region mode — feeding it a watercolour gives you a posterised blob, which is why `wash` drawings go out as WebP.

## 6. Open items this unblocks

From `TECH_DEBT.md`: `og:image`, the About-section portrait placeholder, the hero
placeholder, and the whole `theme-color` / `apple-touch-icon` / `manifest.json`
group, all of which were waiting on "a logo exists".
