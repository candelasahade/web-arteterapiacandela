# Art pipeline — technical notes

Companion to `GUIA-CAPTURA-DIBUJOS.md` (which is written for Candela, in
Spanish, and deliberately non-technical). This one is for you.

## The decision that matters: raster or vector

The batch is mixed and undecided, so this gets decided per piece, not upfront.
The rule:

| Signal | Verdict |
|---|---|
| Flat, closed shapes, one ink colour, no gradient | **Vector** (`--mode vector`) |
| Will ever render below ~64 px (favicon, PWA icon) | **Vector**, no exceptions |
| Visible brush texture, paper grain, tonal gradient | **Raster** (`--mode raster`) |
| Pencil shading, watercolour bleed, dry-brush edges | **Raster** |
| Ambiguous | Run both, compare, keep the better one |

The failure mode to avoid is vectorising something textured because vector
"sounds more professional". Tracing quantises continuous tone into flat filled
regions — on a watercolour wash it produces contour banding that looks like a
posterised screenshot. The texture *is* the brand here. Raster with alpha is
the correct answer for most of what Candela will send.

Conversely, don't ship a raster logo. A PNG favicon at 32 px from a 2000 px
scan is mush, and PWA icon sets need clean scaling.

## What the pipeline actually does

Raster path:

1. **Load** — ImageMagick normalises HEIC / DNG / TIFF / AVIF if OpenCV can't
   read it directly. Applies `-auto-orient` so EXIF rotation is honoured.
2. **Deskew** — Hough lines, median angle of edges within ±12° of an axis.
   Skips if the correction is under 0.15° (avoids resampling for nothing).
3. **Flatten** — the important one. Illumination is estimated on a 96 px
   thumbnail via grayscale dilation, then blurred and upscaled. At that scale
   even a half-page wash is a small structure that dilation erases, so what
   survives is the paper level: phone shadow gradient plus the paper's warm
   cast. Dividing by it neutralises both without touching midtones.
4. **Alpha** — darkness is measured on the **minimum** channel, not luminance.
   A saturated red stroke is bright in luminance and would come out
   half-transparent; on min-channel it reads as opaque ink. Ramp runs between
   `--white` and `--black` so wash gradients keep their falloff.
5. **Unpremultiply** — recovers true stroke colour over transparency. Colour is
   blurred proportionally to transparency, because dividing by small alpha
   amplifies paper grain into noise that is invisible on screen but roughly
   triples PNG weight.
6. **Trim + export** — crop to content with 2% padding, then WebP (q82) + PNG
   at each width. Largest is the base name; others get a `-<width>` suffix.

Vector path: flatten → min-channel → bilateral filter → Otsu threshold →
`RETR_CCOMP` contours → `approxPolyDP` → Catmull-Rom to cubic Bézier →
single path with `fill-rule="evenodd"`. `RETR_CCOMP` plus evenodd is what
keeps interior holes as holes instead of filled blobs.

Fill defaults to `currentColor`, so the SVG inherits CSS colour — inline it in
the Vue component rather than using `<img>` if you want it to respond to theme.

## Verification

Tested on two synthetic drawings before first delivery:

- Watercolour with a baked-in diagonal shadow, warm paper, grain and 2.4°
  rotation → shadow and cast removed, deskewed, alpha keyed, texture intact.
- Line art with an interior hole → **0.914 IoU** against source ink,
  hole preserved. Loss is sub-pixel thinning on thin strokes from smoothing.

`test/verify_svg.py` rasterises a traced SVG (own Bézier evaluator + `fillPoly`)
and reports IoU against the thresholded source, plus an overlay image where
green is the trace and red is the original. Re-run it if you change tracing
parameters — eyeballing an SVG hides thinning.

## The second decision: is the input raw or already cleaned?

Independent of raster-vs-vector, and easier to get wrong because both failure
modes are silent — you get a plausible-looking file that has quietly lost part of
the drawing.

`digitize.py` defaults assume a **photo of a sheet of paper**: uneven light, a
warm paper cast, the edge of the page, maybe a spiral binding. Two steps handle
that, and both are actively harmful on an input that has already been cut out to
pure white:

- **The paper model** (`flatten_lighting_poly`) fits a smooth surface to the
  pixels it believes are paper and divides it out. A large flat block of
  saturated colour is smooth and low-frequency, so the fit absorbs it as
  background. On `olas.png` — a wide strip whose lower half is one solid blue
  band — this bleached the band to a pale pink and dropped ink retention to 0.83.
  `--bg none` skips flattening. Retention went back to 0.97.
- **Border-blob removal** (`drop_border_blobs`) erases components touching the
  frame, which is what kills spiral binding and page lips. On a tight crop the
  artwork *is* what touches the frame, so it erases the drawing. `--keep-border`
  disables it.

So: raw camera/scanner capture → defaults. Pre-cleaned cut-out → `--bg none
--keep-border`. When in doubt, check ink retention (fraction of source pixels
darker than 230 that survive as alpha > 100); anything under ~0.9 on a solid
piece means something got eaten.

## Colour under transparency

RGB in a keyed PNG is still the camera's composite, `ink*a + paper*(1-a)`.
Shipping that directly means every antialiased edge carries a ghost of white
paper — invisible on the sand background, a pale halo on dark, which is exactly
where a favicon lives. `unpremultiply()` solves for `ink`, blending toward a
blurred copy where alpha is low so that dividing by small alpha doesn't amplify
paper grain into PNG weight.

## Tuning

Defaults are a starting point. Expect to adjust per image:

| Symptom | Fix |
|---|---|
| Paper haze around the drawing | lower `--white` (try `0.92`) |
| Light pencil work vanishing | raise `--white` (try `0.98`) |
| Stroke too transparent | raise `--black` (try `0.45`) |
| Dark areas gone flat/blobby | lower `--black` (try `0.28`) |
| Trace too jagged | raise `--simplify` (`0.003`) |
| Trace losing detail | lower `--simplify` (`0.0008`) |
| Deskew rotated it wrongly | `--no-deskew` |
| Halo on the site background | lower `--white`, check she left paper margin |

## Sandbox constraint

apt, npm and PyPI are blocked in the Cowork cloud container, so potrace,
vtracer, Inkscape and svgo cannot be installed there. Available: ImageMagick
(reads HEIC/RAW/AVIF, writes PNG/WebP — note **no AVIF write**), OpenCV,
scikit-image, NumPy, Pillow. Hence the hand-rolled tracer.

If a logo trace isn't sharp enough, the escape hatch is you running
[vtracer](https://github.com/visioncortex/vtracer) locally — single free
Windows binary, no install, no Adobe — and handing me the SVG to clean,
optimise and wire in.

## Scanner apps — the nuance

Scanner apps do two separable things. Perspective correction and edge detection
are **useful**: they hand me a flat rectangle and save the deskew step. The
tonal "enhance" filter is the **problem**: document and B&W modes apply local
adaptive thresholding that quantises midtones toward pure black and white,
which is unrecoverable — the information is gone before I see the file.

So the instruction to Candela is not "avoid scanner apps", it's "use the app,
set the filter to Photo/Colour". The guide reflects this.

## Usage

```bash
# textured piece
python3 tools/process_art.py raw-art/principal-01.png --name hero --outdir public

# clean line art
python3 tools/process_art.py raw-art/logo-01.png --name logo --mode vector --outdir public

# batch of decorations
python3 tools/process_art.py raw-art/adorno-*.png --outdir public --widths 800 400
```

Requires `python3` with `numpy`, `opencv-python`, `Pillow`. ImageMagick optional
(HEIC/RAW only).
