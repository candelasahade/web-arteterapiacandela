# raw-art/ — originales sin procesar

Aquí van los escaneos y fotos **originales** de los dibujos de Candela, tal cual
salen del escáner o del móvil. Sin retocar, sin recortar, sin comprimir.

Esta carpeta está en `.gitignore`: los originales pesan mucho y no tienen por
qué vivir en el repositorio. Es una bandeja de entrada local — Claude lee de
aquí y escribe los assets finales en `public/`.

## Cómo usarla

1. Candela captura los dibujos siguiendo `GUIA-CAPTURA-DIBUJOS.md`.
2. Los archivos se dejan aquí con nombres descriptivos.
3. Se lanza el procesado (o se le pide a Claude en la sesión de Cowork).
4. Los resultados aparecen en `public/` listos para usar.

## Nombres

El nombre del archivo determina el nombre del asset final, así que conviene que
sea claro y sin espacios ni acentos:

| Archivo aquí | Sale en `public/` como |
|---|---|
| `logo-01.png` | `logo.svg` |
| `principal-01.png` | `hero.webp` + `hero.png` + variantes |
| `adorno-hoja.png` | `adorno-hoja.webp` + `adorno-hoja.png` |

## Formatos aceptados

PNG, TIFF, JPG, HEIC/HEIF (iPhone) y RAW de cámara (DNG, CR2, NEF, ARW).
Se convierten automáticamente.

**Preferencia:** PNG o TIFF a 600 ppp desde escáner. Ver la guía para el porqué.

## Procesado

```bash
# Dibujo con textura (acuarela, lápiz, color) -> raster con fondo transparente
python3 tools/process_art.py raw-art/principal-01.png --name hero --outdir public

# Trazo limpio (logo, iconos) -> SVG
python3 tools/process_art.py raw-art/logo-01.png --name logo --mode vector --outdir public

# Lote entero
python3 tools/process_art.py raw-art/adorno-*.png --outdir public --widths 800 400
```

Los parámetros útiles cuando algo no sale a la primera:

| Parámetro | Para qué |
|---|---|
| `--white 0.92` | Bájalo si queda "suciedad" de papel alrededor del dibujo |
| `--black 0.45` | Súbelo si el trazo queda demasiado transparente |
| `--simplify 0.003` | (vector) Súbelo para un trazo más simplificado, bájalo para más fiel |
| `--no-deskew` | Si el enderezado automático se equivoca |

Requiere `python3` con `numpy`, `opencv-python` y `Pillow`. ImageMagick es
opcional (sólo para HEIC y RAW).
