#!/usr/bin/env python3
"""
process_art.py — convierte escaneos/fotos de dibujos a mano en assets web.

Pipeline (raster):
  1. Normaliza el formato de entrada (HEIC, DNG, TIFF, JPG...) con ImageMagick.
  2. Corrige la rotación EXIF y endereza el papel.
  3. Estima la iluminación del papel y la divide -> fondo blanco plano,
     sin quemar los grises ni la textura de la acuarela.
  4. Convierte el papel en transparencia (alpha) conservando el color real
     de la tinta/pintura (unpremultiply).
  5. Recorta al contenido con margen y exporta WebP + PNG a varios anchos.

Pipeline (vector, sólo para línea limpia / logo):
  Umbral adaptativo -> contornos OpenCV -> simplificación -> suavizado
  Catmull-Rom a Bézier cúbica -> SVG con fill-rule evenodd (respeta huecos).

Uso:
    python3 tools/process_art.py entrada.png --name logo --mode vector
    python3 tools/process_art.py entrada.jpg --name hero --mode raster --widths 1600 800
    python3 tools/process_art.py raw-art/*.png --outdir public/

Requisitos: python3, numpy, opencv-python, Pillow y (opcional) ImageMagick.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image

# --------------------------------------------------------------------------
# Entrada
# --------------------------------------------------------------------------

RAW_EXTS = {".heic", ".heif", ".dng", ".cr2", ".nef", ".arw", ".tif", ".tiff", ".avif"}


def load_image(path: str) -> np.ndarray:
    """Devuelve un BGR uint8. Usa ImageMagick para formatos que OpenCV no lee."""
    ext = os.path.splitext(path)[1].lower()
    if ext in RAW_EXTS or cv2.imread(path) is None:
        magick = shutil.which("magick") or shutil.which("convert")
        if not magick:
            raise RuntimeError(f"No puedo leer {path} y no hay ImageMagick disponible.")
        tmp = tempfile.mktemp(suffix=".png")
        cmd = [magick, path] if "magick" in os.path.basename(magick) else [magick, path]
        subprocess.run(cmd + ["-auto-orient", tmp], check=True)
        img = cv2.imread(tmp, cv2.IMREAD_COLOR)
        os.unlink(tmp)
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    return img


# --------------------------------------------------------------------------
# Enderezado
# --------------------------------------------------------------------------


def deskew(img: np.ndarray, max_angle: float = 12.0) -> np.ndarray:
    """Endereza rotaciones pequeñas usando los bordes dominantes del dibujo."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 720, threshold=max(120, img.shape[0] // 8))
    if lines is None:
        return img

    angles = []
    for rho_theta in lines[:200]:
        theta = rho_theta[0][1]
        deg = np.degrees(theta) % 180.0
        # Distancia al eje horizontal o vertical más cercano
        for ref in (0.0, 90.0, 180.0):
            if abs(deg - ref) <= max_angle:
                angles.append(deg - ref)
                break
    if not angles:
        return img

    angle = float(np.median(angles))
    if abs(angle) < 0.15:
        return img

    h, w = img.shape[:2]
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(
        img, m, (w, h), flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )


# --------------------------------------------------------------------------
# Iluminación y papel
# --------------------------------------------------------------------------


def flatten_paper(
    img: np.ndarray, bg_scale: int = 96, kernel_frac: float = 0.22
) -> tuple[np.ndarray, np.ndarray]:
    """
    Divide la imagen por su mapa de iluminación estimado.

    Devuelve (imagen_normalizada_float01, mapa_iluminacion_float01).

    La estimación se hace sobre una miniatura: a esa escala hasta una mancha
    de acuarela que ocupa media hoja es una estructura pequeña, así que una
    dilatación la borra y deja sólo el papel. Reescalado y suavizado, eso da
    la iluminación real (sombra del móvil + tono cálido del papel) sin tocar
    los grises intermedios — que es justo lo que arruina el 'auto contrast'.
    """
    f = img.astype(np.float32) / 255.0
    h, w = img.shape[:2]

    scale = bg_scale / max(h, w)
    small = cv2.resize(f, (max(8, round(w * scale)), max(8, round(h * scale))), interpolation=cv2.INTER_AREA)

    k = max(3, int(min(small.shape[:2]) * kernel_frac) | 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    bg_small = cv2.dilate(small, kernel)  # se queda con el nivel del papel
    bg_small = cv2.GaussianBlur(bg_small, (0, 0), sigmaX=max(1.0, k / 3.0))

    bg = cv2.resize(bg_small, (w, h), interpolation=cv2.INTER_CUBIC)
    bg = np.clip(bg, 0.15, 1.0)

    flat = np.clip(f / bg, 0.0, 1.0)
    return flat, bg


def paper_to_alpha(
    flat: np.ndarray,
    white_point: float = 0.96,
    black_point: float = 0.35,
    keep_color: bool = True,
) -> np.ndarray:
    """
    Convierte el blanco del papel en transparencia.

    white_point: por encima de esta luminancia es papel puro (alpha 0).
    black_point: por debajo es trazo opaco (alpha 1).
    Entre ambos la transición es suave -> conserva el degradado de la acuarela.

    La "oscuridad" se mide sobre el canal MÍNIMO, no sobre la luminancia: así
    un rojo o un verde saturado cuenta como trazo opaco en vez de quedarse
    medio transparente por ser un color claro en luminancia.
    """
    darkness = 1.0 - flat.min(axis=2)
    lo = 1.0 - white_point
    hi = 1.0 - black_point
    alpha = (darkness - lo) / max(1e-6, (hi - lo))
    alpha = np.clip(alpha, 0.0, 1.0)
    alpha = cv2.GaussianBlur(alpha, (0, 0), sigmaX=0.6)

    if keep_color:
        # Unpremultiply: recupera el color real del trazo sobre fondo transparente.
        # Donde no hay trazo se fuerza un blanco plano: el grano del papel ahí
        # es invisible pero multiplica por 3 el peso del PNG si se conserva.
        a = np.repeat(alpha[:, :, None], 3, axis=2)
        rgb = np.where(a > 0.02, np.clip((flat - (1.0 - a)) / np.maximum(a, 0.08), 0, 1), 1.0)
        # En los bordes semitransparentes la división amplifica el ruido del
        # papel: invisible en pantalla, pero dispara el peso del PNG/WebP.
        # Se suaviza el color proporcionalmente a lo transparente que sea.
        rgb = a * rgb + (1.0 - a) * cv2.GaussianBlur(rgb, (0, 0), sigmaX=1.5)
    else:
        rgb = flat

    out = np.dstack([rgb, alpha])
    return (out * 255.0).astype(np.uint8)


def trim(rgba: np.ndarray, pad_frac: float = 0.02, alpha_thresh: int = 8) -> np.ndarray:
    """Recorta al contenido visible dejando un margen proporcional."""
    a = rgba[:, :, 3]
    ys, xs = np.where(a > alpha_thresh)
    if len(xs) == 0:
        return rgba
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    pad = int(max(y1 - y0, x1 - x0) * pad_frac)
    y0 = max(0, y0 - pad)
    x0 = max(0, x0 - pad)
    y1 = min(rgba.shape[0] - 1, y1 + pad)
    x1 = min(rgba.shape[1] - 1, x1 + pad)
    return rgba[y0 : y1 + 1, x0 : x1 + 1]


# --------------------------------------------------------------------------
# Exportación raster
# --------------------------------------------------------------------------


def export_raster(rgba: np.ndarray, outdir: str, name: str, widths: list[int]) -> list[str]:
    written = []
    # OpenCV entrega BGRA; Pillow espera RGBA.
    pil = Image.fromarray(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA), mode="RGBA")
    os.makedirs(outdir, exist_ok=True)

    targets = sorted({min(w_, pil.width) for w_ in widths}, reverse=True)
    for i, wpx in enumerate(targets):
        # El más grande es el asset "base" (sin sufijo); el resto son variantes.
        suffix = "" if i == 0 else f"-{wpx}"
        if wpx >= pil.width:
            scaled = pil
        else:
            hpx = max(1, round(pil.height * wpx / pil.width))
            scaled = pil.resize((wpx, hpx), Image.LANCZOS)

        webp = os.path.join(outdir, f"{name}{suffix}.webp")
        png = os.path.join(outdir, f"{name}{suffix}.png")
        scaled.save(webp, "WEBP", quality=82, method=6)
        scaled.save(png, "PNG", optimize=True)
        written += [webp, png]
    return written


# --------------------------------------------------------------------------
# Trazado vectorial
# --------------------------------------------------------------------------


def _catmull_rom_to_bezier(pts: np.ndarray, closed: bool = True, tension: float = 1.0) -> str:
    """Convierte una polilínea en un path SVG de béziers cúbicas suaves."""
    n = len(pts)
    if n < 3:
        return ""
    d = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    last = n if closed else n - 1
    for i in range(last):
        p0 = pts[(i - 1) % n] if closed else pts[max(i - 1, 0)]
        p1 = pts[i % n]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed else pts[min(i + 2, n - 1)]
        c1 = p1 + (p2 - p0) / (6.0 / tension)
        c2 = p2 - (p3 - p1) / (6.0 / tension)
        d.append(
            f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f}"
        )
    if closed:
        d.append("Z")
    return " ".join(d)


def trace_svg(
    img: np.ndarray,
    fill: str = "currentColor",
    simplify: float = 0.0015,
    min_area_frac: float = 0.00015,
    smooth: bool = True,
) -> str:
    """
    Traza línea limpia / silueta a SVG.

    Usa jerarquía de contornos para que los huecos interiores queden como
    huecos reales (fill-rule evenodd), no como manchas rellenas.
    """
    flat, _ = flatten_paper(img)
    # Canal mínimo: un trazo de color cuenta igual que uno negro.
    gray = (flat.min(axis=2) * 255).astype(np.uint8)
    gray = cv2.bilateralFilter(gray, 7, 60, 60)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binary = cv2.morphologyEx(
        binary, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    )

    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        raise RuntimeError("No se detectó ningún trazo. ¿La imagen tiene suficiente contraste?")

    h, w = binary.shape
    min_area = h * w * min_area_frac
    paths = []
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, simplify * peri, True)
        pts = approx.reshape(-1, 2).astype(np.float64)
        if len(pts) < 3:
            continue
        if smooth:
            seg = _catmull_rom_to_bezier(pts, closed=True)
        else:
            seg = (
                "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"
            )
        if seg:
            paths.append(seg)

    if not paths:
        raise RuntimeError("Todos los contornos quedaron por debajo del área mínima.")

    d = " ".join(paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'fill="none" role="img">\n'
        f'  <path d="{d}" fill="{fill}" fill-rule="evenodd" />\n'
        f"</svg>\n"
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def process(path: str, args) -> list[str]:
    name = args.name or os.path.splitext(os.path.basename(path))[0].lower().replace(" ", "-")
    img = load_image(path)
    if not args.no_deskew:
        img = deskew(img)

    if args.mode == "vector":
        svg = trace_svg(img, fill=args.fill, simplify=args.simplify)
        os.makedirs(args.outdir, exist_ok=True)
        out = os.path.join(args.outdir, f"{name}.svg")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(svg)
        return [out]

    flat, _ = flatten_paper(img)
    rgba = paper_to_alpha(flat, white_point=args.white, black_point=args.black)
    if not args.no_trim:
        rgba = trim(rgba)
    return export_raster(rgba, args.outdir, name, args.widths)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inputs", nargs="+", help="Imágenes de entrada")
    p.add_argument("--outdir", default="public", help="Carpeta de salida (def: public)")
    p.add_argument("--name", help="Nombre base del asset (def: el del archivo)")
    p.add_argument("--mode", choices=["raster", "vector"], default="raster")
    p.add_argument("--widths", type=int, nargs="+", default=[1600, 800, 400])
    p.add_argument("--white", type=float, default=0.96, help="Punto de blanco del papel")
    p.add_argument("--black", type=float, default=0.35, help="Punto de negro de la tinta")
    p.add_argument("--fill", default="currentColor", help="Relleno del SVG")
    p.add_argument("--simplify", type=float, default=0.0015)
    p.add_argument("--no-deskew", action="store_true")
    p.add_argument("--no-trim", action="store_true")
    args = p.parse_args()

    written: list[str] = []
    for path in args.inputs:
        try:
            files = process(path, args)
            written += files
            for f in files:
                print(f"  ✓ {f}  ({os.path.getsize(f) / 1024:.1f} KB)")
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ {path}: {exc}", file=sys.stderr)
    return 0 if written else 1


if __name__ == "__main__":
    raise SystemExit(main())
