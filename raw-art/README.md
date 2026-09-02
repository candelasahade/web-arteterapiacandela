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
# Foto de un dibujo sobre papel (con sombras, tono cálido, borde de hoja)
python3 tools/digitize.py raw-art/principal-01.png --name hero --out public \
    --square --fill "#dedacd"

# Escaneo ya recortado a blanco puro (fondo limpio, sin márgenes)
python3 tools/digitize.py raw-art/nube.png --name nube --out public \
    --bg none --keep-border --widths 800 400

# Favicon
python3 tools/digitize.py raw-art/logo-01.png --name favicon --out public --square --ico
```

### Los dos casos que hay que distinguir

Antes de lanzar nada, mira el original y decide cuál es:

| El original es… | Flags | Por qué |
|---|---|---|
| **Foto o escaneo de una hoja**: se ve el papel, sombras, el borde de la hoja, la espiral del cuaderno | (por defecto) | El modelo polinómico quita la sombra y el tono del papel; el filtro de bordes se lleva la espiral y el canto de la hoja |
| **Ya recortado a blanco puro**, el dibujo llega hasta el borde de la imagen | `--bg none --keep-border` | Sin `--bg none` el modelo de papel confunde una mancha grande de color con fondo y **se la come**; sin `--keep-border` se borra todo lo que toque el borde, que aquí es el propio dibujo |

Los parámetros útiles cuando algo no sale a la primera:

| Parámetro | Para qué |
|---|---|
| `--white 0.92` | Bájalo si queda "suciedad" de papel alrededor del dibujo |
| `--black 0.45` | Súbelo si el trazo queda demasiado transparente |
| `--bg none` | El original ya viene limpio sobre blanco (ver tabla de arriba) |
| `--keep-border` | El dibujo toca el borde de la imagen y no hay que recortarlo |
| `--square --margin 0.08` | Lienzo cuadrado con el dibujo centrado (no reescala, sólo rellena) |
| `--fill "#dedacd"` | Fondo sólido en vez de transparente |
| `--ico` | Genera además un favicon .ico multi-tamaño |
| `--png` | Escribe también PNG en cada ancho, no sólo WebP |
| `--ink "#0d0d0d"` | Versión monocroma conservando la textura |
| `--trace` | (sólo trazo limpio) Genera además un SVG vectorial |

Requiere `python3` con `numpy`, `opencv-python` y `Pillow`. ImageMagick es
opcional (sólo para HEIC y RAW).
