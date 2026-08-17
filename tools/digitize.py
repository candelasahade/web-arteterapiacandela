#!/usr/bin/env python3
"""
digitize.py — turn a photo/scan of a hand-made drawing into web-ready assets.

No Adobe, no cloud services, no paid tools. Pure OpenCV/NumPy/Pillow.

  python3 digitize.py INPUT.jpg --out OUT_DIR --name hoja [--trace] [--ink "#3b3a46"]

Produces
  <name>-master.png    full-res RGBA, paper removed, lossless (the archive copy)
  <name>-1600.webp     web raster w/ transparency (plus -800, -400)
  <name>.svg           real vector trace (only with --trace; for line art / logos)
  <name>-check.png     side-by-side contact sheet to eyeball the result

Pipeline
  1. flatten uneven lighting     (divide by a morphological background estimate)
  2. neutralise the paper cast   (per-channel white point from paper percentile)
  3. build an alpha matte        (paper -> transparent, keeps antialiased edges)
  4. clean speckle + trim        (area filter, autocrop, padding)
  5. export raster / trace vector
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np
import cv2


# ---------------------------------------------------------------- 1. lighting
def flatten_lighting(bgr: np.ndarray, strength: int = 0) -> np.ndarray:
    """Remove vignetting, window gradients and soft shadows.

    Estimates the paper (the local *bright* level) with a large morphological
    closing, then divides the image by it. Anything darker than its local paper
    survives; smooth illumination does not.
    """
    h, w = bgr.shape[:2]
    k = strength or max(31, (int(min(h, w) * 0.06) | 1))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    out = np.empty_like(bgr, np.float32)
    for c in range(3):
        ch = bgr[:, :, c].astype(np.float32)
        bg = cv2.morphologyEx(ch, cv2.MORPH_CLOSE, ker)
        bg = cv2.GaussianBlur(bg, (0, 0), k / 3.0)
        out[:, :, c] = np.clip(ch / np.maximum(bg, 1e-3) * 255.0, 0, 255)
    return out


def flatten_lighting_poly(bgr: np.ndarray, degree: int = 3, iters: int = 3) -> np.ndarray:
    """Same goal, but the paper model is a smooth 2-D polynomial fitted only to
    pixels that look like paper (re-estimated each iteration).

    Preferred default. The morphological estimate above has a hard limit: any
    artwork larger than its kernel gets absorbed into the "background" and
    erased — which silently eats big watercolour washes. A low-degree polynomial
    physically cannot bend around a wash, so washes survive.
    """
    degree = min(degree, 5)   # raw monomials past 5 are ill-conditioned in lstsq
    h, w = bgr.shape[:2]
    ys, xs = np.mgrid[0:h, 0:w]
    xs = (xs / w - 0.5).ravel()
    ys = (ys / h - 0.5).ravel()
    terms = [xs ** i * ys ** j for i in range(degree + 1)
             for j in range(degree + 1 - i)]
    A = np.stack(terms, 1).astype(np.float32)

    out = np.empty_like(bgr, np.float32)
    for c in range(3):
        v = bgr[:, :, c].astype(np.float32).ravel()
        keep = v >= np.percentile(v, 55)          # start from the brighter half
        for _ in range(iters):
            coef, *_ = np.linalg.lstsq(A[keep], v[keep], rcond=None)
            model = A @ coef
            resid = v - model
            keep = resid > np.percentile(resid, 35)   # paper sits above the ink
        model = np.maximum(A @ coef, 1e-3)
        out[:, :, c] = np.clip(v / model * 255.0, 0, 255).reshape(h, w)
    return out


# ------------------------------------------------------------ 2. paper colour
def neutralise_paper(f32: np.ndarray, pct: float = 97.0) -> np.ndarray:
    """Force the paper to neutral white, keeping pigment hue intact."""
    wp = np.percentile(f32.reshape(-1, 3), pct, axis=0)
    return np.clip(f32 / np.maximum(wp, 1e-3) * 255.0, 0, 255)


# ---------------------------------------------------------------- 3. matte
def build_alpha(f32: np.ndarray, white: float = 0.94, black: float = 0.38) -> np.ndarray:
    """Alpha from how far each pixel sits below paper white.

    `white` = anything this bright or brighter is fully paper (alpha 0).
    `black` = anything this dark or darker is fully opaque (alpha 1).
    The soft ramp between them is what preserves pencil grain and wash edges.
    """
    lum = f32.min(axis=2) / 255.0            # min channel: catches coloured ink too
    a = (white - lum) / max(white - black, 1e-6)
    return np.clip(a, 0, 1).astype(np.float32)


def unpremultiply(rgb: np.ndarray, alpha: np.ndarray, paper: float = 255.0) -> np.ndarray:
    """Recover the true pigment colour from a stroke seen over white paper.

    What the camera recorded is already a composite: C = ink*a + paper*(1-a).
    Shipping C as the RGB of a transparent PNG means every soft edge carries a
    ghost of the paper — invisible on a light background, a pale halo on a dark
    one (a browser tab strip in dark mode, for instance). Solving for `ink` fixes
    that.

    Dividing by small alpha amplifies paper grain into noise, so the colour is
    blended toward a blurred copy exactly where alpha is low — the eye can't
    resolve hue in near-transparent pixels anyway, but the PNG encoder pays for it.
    """
    a = np.clip(alpha, 1e-3, 1.0)[..., None]
    ink = np.clip((rgb - paper * (1.0 - a)) / a, 0, 255)
    soft = cv2.GaussianBlur(ink, (0, 0), 1.5)
    w = np.clip((0.35 - alpha) / 0.35, 0, 1)[..., None]
    return ink * (1 - w) + soft * w


def despeckle(alpha: np.ndarray, min_area_frac: float = 2e-5) -> np.ndarray:
    """Drop isolated blobs (paper fibres, dust, JPEG mosquito noise)."""
    h, w = alpha.shape
    mask = (alpha > 0.12).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    keep = np.zeros(n, bool)
    min_area = max(8, int(h * w * min_area_frac))
    for i in range(1, n):
        keep[i] = stats[i, cv2.CC_STAT_AREA] >= min_area
    keep[0] = False
    return alpha * keep[lab]


def drop_border_blobs(alpha: np.ndarray, margin_frac: float = 0.012) -> np.ndarray:
    """Erase anything connected to the edge of the frame.

    A photographed sketchbook brings its own furniture: spiral binding, the dark
    lip of the page, the table showing past the paper, a corner shadow. All of it
    is darker than paper, so the matte keeps it and autocrop then "crops" to the
    whole sheet instead of to the drawing.

    Every one of those artefacts touches the frame edge; a drawing captured with
    the margin the guide asks for does not. So: kill components that reach into a
    thin border band. Disable with --keep-border if a piece deliberately bleeds
    off the paper.
    """
    h, w = alpha.shape
    m = max(2, int(min(h, w) * margin_frac))
    mask = (alpha > 0.12).astype(np.uint8)
    n, lab, _, _ = cv2.connectedComponentsWithStats(mask, 8)
    border = np.zeros((h, w), bool)
    border[:m, :] = border[-m:, :] = True
    border[:, :m] = border[:, -m:] = True
    touching = np.unique(lab[border])
    keep = np.ones(n, bool)
    keep[touching] = False
    keep[0] = False
    return alpha * keep[lab]


def square_canvas(rgba: np.ndarray, margin_frac: float = 0.08,
                  fill: str | None = None) -> np.ndarray:
    """Centre the artwork on a square canvas with `margin_frac` breathing room.

    Size is driven by the artwork's LONGER side, so a tall drawing and a wide one
    both end up with the same margin and neither gets scaled — square framing here
    is padding, never resampling.
    """
    h, w = rgba.shape[:2]
    side = int(round(max(h, w) / max(1e-6, 1 - 2 * margin_frac)))
    out = np.zeros((side, side, 4), np.uint8)
    y0, x0 = (side - h) // 2, (side - w) // 2
    out[y0:y0 + h, x0:x0 + w] = rgba
    if fill:
        f = fill.lstrip('#')
        r, g, b = (int(f[i:i + 2], 16) for i in (0, 2, 4))
        bg = np.zeros((side, side, 3), np.float32)
        bg[:] = (b, g, r)                      # OpenCV is BGR
        a = out[:, :, 3:4].astype(np.float32) / 255.0
        comp = out[:, :, :3].astype(np.float32) * a + bg * (1 - a)
        out = np.dstack([comp, np.full((side, side), 255, np.float32)]).astype(np.uint8)
    return out


def autocrop(rgba: np.ndarray, pad_frac: float = 0.02) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 8)
    if len(xs) == 0:
        return rgba
    pad = int(max(rgba.shape[:2]) * pad_frac)
    y0, y1 = max(0, ys.min() - pad), min(rgba.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(rgba.shape[1], xs.max() + pad + 1)
    return rgba[y0:y1, x0:x1]


# 16/32/48 is what browsers actually pull from an .ico; 64 covers Windows
# shortcuts. Bundling 128 and 256 multiplies the file size for frames nothing
# requests — anything larger belongs in a PNG (apple-touch-icon, PWA manifest).
ICO_SIZES = (16, 32, 48, 64)


def save_ico(rgba: np.ndarray, path: str, sizes=ICO_SIZES) -> None:
    """Write a multi-resolution .ico with a real alpha channel.

    Every size is downsampled here with INTER_AREA rather than left to the ICO
    encoder: at 16 px an area average is the difference between a legible mark
    and a smear. Alpha survives — a favicon with a baked white square looks
    broken on a dark tab strip.
    """
    from PIL import Image
    frames = []
    for s in sizes:
        small = cv2.resize(rgba, (s, s), interpolation=cv2.INTER_AREA)
        frames.append(Image.fromarray(cv2.cvtColor(small, cv2.COLOR_BGRA2RGBA)))
    biggest = frames[-1]
    biggest.save(path, format="ICO", sizes=[(s, s) for s in sizes],
                 append_images=frames[:-1])


def recolour(rgb: np.ndarray, alpha: np.ndarray, hex_colour: str) -> np.ndarray:
    """Replace the artwork colour with a single brand ink (for line art)."""
    h = hex_colour.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    flat = np.zeros_like(rgb)
    flat[:] = (b, g, r)
    return flat


# ---------------------------------------------------------------- 5. tracing
def _smooth_closed(pts: np.ndarray, sigma: float = 1.6) -> np.ndarray:
    """Gaussian-blur a closed contour along its own arc length (kills stair-steps)."""
    if sigma <= 0 or len(pts) < 7:
        return pts
    r = int(max(1, round(sigma * 3)))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.vstack([pts[-r:], pts, pts[:r]])
    return np.column_stack([np.convolve(pad[:, i], k, "valid") for i in (0, 1)])


def _catmull_to_bezier(pts: np.ndarray, alpha: float = 0.5) -> str:
    """Closed polyline -> smooth cubic Bezier `d` string.

    Centripetal Catmull-Rom (alpha=0.5), not uniform: uniform CR overshoots
    badly on long thin shapes, which turned every pen stroke into a chain of
    lens-shaped bulges. Centripetal is guaranteed cusp- and self-intersection-free.
    """
    n = len(pts)
    d = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        d1 = max(np.linalg.norm(p1 - p0), 1e-6) ** alpha
        d2 = max(np.linalg.norm(p2 - p1), 1e-6) ** alpha
        d3 = max(np.linalg.norm(p3 - p2), 1e-6) ** alpha
        c1 = (d1 * d1 * p2 - d2 * d2 * p0 + (2 * d1 * d1 + 3 * d1 * d2 + d2 * d2) * p1) \
            / (3 * d1 * (d1 + d2))
        c2 = (d3 * d3 * p1 - d2 * d2 * p3 + (2 * d3 * d3 + 3 * d3 * d2 + d2 * d2) * p2) \
            / (3 * d3 * (d3 + d2))
        d.append(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    d.append("Z")
    return "".join(d)


def trace_svg(alpha: np.ndarray, colour: str = "#3b3a46",
              thresh: float = 0.45, smooth: float = 0.0006,
              min_area_frac: float = 8e-6, scale: float = 1.0) -> str:
    """Vectorise the matte: contours -> simplified -> smoothed cubic paths.

    A stand-in for potrace/vtracer (both unavailable offline here). Good for
    line art, lettering, logos and flat silhouettes; not for washes.

    Holes matter: each outer contour is emitted as ONE path whose subpaths are
    its own inner contours, so `fill-rule=evenodd` punches them out. Emitting
    holes as separate paths would fill them in (a ring would become a disc).
    """
    h, w = alpha.shape
    mask = (alpha > thresh).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    contours, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hier is None:
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"/>'
    hier = hier[0]
    min_area = max(12, int(h * w * min_area_frac))
    # Simplification tolerance must be ABSOLUTE (pixels), never a fraction of the
    # contour's own perimeter: line art is usually one huge connected contour, and
    # a perimeter-relative epsilon then exceeds the stroke width and collapses
    # every stroke into a chain of lens-shaped bulges.
    eps_px = max(0.5, smooth * max(h, w))

    def subpath(c):
        if cv2.contourArea(c) < min_area or len(c) < 8:
            return None
        c = _smooth_closed(c.reshape(-1, 2).astype(np.float64))
        p = cv2.approxPolyDP(c.astype(np.float32).reshape(-1, 1, 2), eps_px, True)
        p = p.reshape(-1, 2).astype(np.float64)
        return _catmull_to_bezier(p * scale) if len(p) >= 4 else None

    paths = []
    for i, c in enumerate(contours):
        if hier[i][3] != -1:            # a hole: handled by its parent
            continue
        d = subpath(c)
        if d is None:
            continue
        child = hier[i][2]
        while child != -1:              # walk this outer contour's holes
            dh = subpath(contours[child])
            if dh:
                d += dh
            child = hier[child][0]
        paths.append(d)

    vb_w, vb_h = w * scale, h * scale
    body = "\n    ".join(f'<path d="{p}"/>' for p in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.0f} {vb_h:.0f}" '
            f'fill="{colour}" fill-rule="evenodd" role="img">\n    {body}\n</svg>\n')


# ---------------------------------------------------------------- driver
def process(path: str, out_dir: str, name: str, do_trace: bool,
            ink: str | None, widths=(1600, 800, 400), keep_colour=True,
            bg: str = "poly", square: bool = False, margin: float = 0.08,
            fill: str | None = None, keep_border: bool = False,
            ico: bool = False, ico_margin: float = 0.03,
            png: bool = False) -> dict:
    raw = cv2.imread(path, cv2.IMREAD_COLOR)
    if raw is None:
        sys.exit(f"cannot read {path}")
    os.makedirs(out_dir, exist_ok=True)

    flat = flatten_lighting_poly(raw) if bg == 'poly' else flatten_lighting(raw)
    flat = neutralise_paper(flat)
    alpha = despeckle(build_alpha(flat))
    if not keep_border:
        alpha = drop_border_blobs(alpha)

    rgb = recolour(flat, alpha, ink) if ink else unpremultiply(flat, alpha)

    rgba = np.dstack([rgb, alpha * 255.0]).astype(np.uint8)
    # Crop tight first: with --square the margin is applied by the canvas, so
    # padding twice would leave the drawing floating in too much air.
    art = autocrop(rgba, 0.0)
    rgba = square_canvas(art, margin, fill) if square else autocrop(rgba, 0.02)

    made = {}
    if ico:
        # Its own, tighter margin: a favicon is 16 px of real estate and the
        # generous margin that suits a hero wastes a third of it.
        p = os.path.join(out_dir, f"{name}.ico")
        save_ico(square_canvas(art, ico_margin, None), p)
        made["ico"] = p

    master = os.path.join(out_dir, f"{name}-master.png")
    cv2.imwrite(master, rgba, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    made["master"] = master

    usable = [x for x in widths if x <= rgba.shape[1]] or [rgba.shape[1]]
    for wpx in usable:
        s = wpx / rgba.shape[1]
        small = cv2.resize(rgba, (wpx, int(round(rgba.shape[0] * s))),
                           interpolation=cv2.INTER_AREA)
        p = os.path.join(out_dir, f"{name}-{wpx}.webp")
        cv2.imwrite(p, small, [cv2.IMWRITE_WEBP_QUALITY, 88])
        made[f"webp{wpx}"] = p
        if png:
            p = os.path.join(out_dir, f"{name}-{wpx}.png")
            cv2.imwrite(p, small, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            made[f"png{wpx}"] = p

    if do_trace:
        svg = trace_svg(rgba[:, :, 3].astype(np.float32) / 255.0,
                        colour=ink or "#3b3a46")
        p = os.path.join(out_dir, f"{name}.svg")
        open(p, "w").write(svg)
        made["svg"] = p

    # contact sheet: original | flattened | matte on checkerboard
    def fit(im, hh=700):
        return cv2.resize(im, (int(im.shape[1] * hh / im.shape[0]), hh))
    checks = np.indices(rgba.shape[:2]).sum(axis=0) // 24 % 2
    board = np.where(checks[..., None] == 0, 255, 222).astype(np.float32).repeat(3, 2)
    a = rgba[:, :, 3:4] / 255.0
    comp = (rgba[:, :, :3] * a + board * (1 - a)).astype(np.uint8)
    sheet = np.hstack([fit(raw), fit(np.clip(flat, 0, 255).astype(np.uint8)), fit(comp)])
    p = os.path.join(out_dir, f"{name}-check.png")
    cv2.imwrite(p, sheet)
    made["check"] = p
    return made


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", default="out")
    ap.add_argument("--name", default="art")
    ap.add_argument("--trace", action="store_true", help="also emit a vector SVG")
    ap.add_argument("--bg", default="poly", choices=["poly", "morph"],
                    help="paper model: poly (keeps big washes) | morph (harsher light)")
    ap.add_argument("--ink", default=None, help='flatten to one colour, e.g. "#3b3a46"')
    ap.add_argument("--square", action="store_true",
                    help="centre the drawing on a square canvas (pads, never scales)")
    ap.add_argument("--margin", type=float, default=0.08,
                    help="breathing room around the drawing, as a fraction of the square")
    ap.add_argument("--fill", default=None,
                    help='flatten onto a solid background, e.g. "#dedacd" (default: transparent)')
    ap.add_argument("--keep-border", action="store_true",
                    help="keep artefacts touching the frame edge (spiral binding, page lip)")
    ap.add_argument("--ico", action="store_true",
                    help="also emit a multi-size .ico favicon (always transparent)")
    ap.add_argument("--ico-margin", type=float, default=0.03,
                    help="margin for the .ico only; favicons want it tight")
    ap.add_argument("--widths", type=int, nargs="+", default=[1600, 800, 400],
                    help="output widths (widths larger than the source are skipped)")
    ap.add_argument("--png", action="store_true",
                    help="also write PNG at each width (apple-touch-icon, WhatsApp, print)")
    a = ap.parse_args()
    for k, v in process(a.input, a.out, a.name, a.trace, a.ink, bg=a.bg,
                        square=a.square, margin=a.margin, fill=a.fill,
                        keep_border=a.keep_border, ico=a.ico,
                        ico_margin=a.ico_margin, widths=tuple(a.widths),
                        png=a.png).items():
        print(f"{k:10s} {v}  ({os.path.getsize(v)/1024:.1f} kB)")
