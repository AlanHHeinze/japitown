# -*- coding: utf-8 -*-
"""
Busca DOS LINEAS SEGUIDAS DEL MISMO PERSONAJE SIN CAMBIO DE BOCA.

Es la regla 7 del skill de contenido: si un personaje encadena dos parlamentos
sin que nada toque su sprite, la boca queda congelada mientras el jugador avanza
el texto y la escena parece trabada. Entre linea y linea va un `show` alternando
sus dos bocas de hablar:

    Violet / Monica   b_hablando  <->  b_hablandochica
    el MC             b_hablando  <->  b_abiertachica

QUE CUENTA COMO CASO. Solo lo que se puede arreglar:
  - el personaje tiene SPRITE en pantalla en ese punto, y
  - ese sprite tiene una boca puesta (los de espalda no tienen boca: no hay nada
    que alternar, y hay muchas lineas que se dicen FUERA DE CAMARA —detras de
    una puerta, desde el pasillo— donde meter un `show` mostraria el sprite
    donde no corresponde).
Los dos descartes se listan aparte, para que se vea que fueron mirados.

QUE CORTA LA RACHA: `show`, `hide`, `scene` (el sprite se movio) y los cambios
de flujo (`label`, `jump`, `call`, `return`, `menu`, `if`, `while`). NO la
cortan `pause`, `with`, `window`, `play` ni `$`: no tocan el sprite.

USO
    python tools/validar_bocas.py          # resumen
    python tools/validar_bocas.py -v       # + los descartes, uno por linea

Hermano de validar_sprites.py, validar_bloqueos.py y validar_traducciones.py.
"""
import io
import os
import re
import sys

# Personaje -> prefijo de tag de sus sprites.
HABLANTE_PREFIJO = {
    "mc": "mc_", "violet": "violet_", "monica": "monica_",
    "jasmine": "jasmine_", "zowie": "zowie_", "leah": "leah_",
    "padre": "padre_", "carl": "carl_",
}
# La pareja de bocas de cada uno, para poder sugerir la que va.
PAREJA_BOCA = {
    "mc": ("b_hablando", "b_abiertachica"),
    "violet": ("b_hablando", "b_hablandochica"),
    "monica": ("b_hablando", "b_hablandochica"),
    "jasmine": ("b_hablando", "b_feliz"),
}

PAT_SAY = re.compile(r'^(\s*)(%s)\s+"' % "|".join(HABLANTE_PREFIJO))
PAT_SHOW = re.compile(r'^\s*show\s+(\w+)(.*)$')
PAT_HIDE = re.compile(r'^\s*hide\s+(\w+)')
PAT_SCENE = re.compile(r'^\s*scene\b')
PAT_FLUJO = re.compile(r'^\s*(menu:|jump |call |return|if |elif |else:|while |label |python:)')
PAT_BOCA = re.compile(r'\b(b[a-z0-9]*_\w+)\b')


def _archivos():
    salida = []
    for base, _, fs in os.walk("game/script"):
        for f in sorted(fs):
            if f.endswith(".rpy"):
                salida.append(os.path.join(base, f).replace("\\", "/"))
    return salida


def revisar():
    casos, sin_sprite, sin_boca = [], [], []
    for r in _archivos():
        lineas = io.open(r, encoding="utf-8").read().splitlines()
        visibles = {}        # tag -> ultima boca vista (o None)
        anterior = None      # hablante de la linea de dialogo anterior
        for i, l in enumerate(lineas, 1):
            m = PAT_SAY.match(l)
            if m:
                indent, quien = m.group(1), m.group(2)
                if anterior == quien:
                    pref = HABLANTE_PREFIJO[quien]
                    tags = [t for t in visibles if t.startswith(pref)]
                    tag = tags[-1] if tags else None
                    boca = visibles.get(tag) if tag else None
                    dato = (r.replace("game/script/", ""), i, quien, tag, boca,
                            indent, l.strip()[:56])
                    if tag is None:
                        sin_sprite.append(dato)
                    elif boca is None:
                        sin_boca.append(dato)
                    else:
                        casos.append(dato)
                anterior = quien
                continue

            ms = PAT_SHOW.match(l)
            if ms:
                tag, bocas = ms.group(1), PAT_BOCA.findall(ms.group(2))
                visibles[tag] = bocas[-1] if bocas else visibles.get(tag)
                anterior = None
                continue
            mh = PAT_HIDE.match(l)
            if mh:
                visibles.pop(mh.group(1), None)
                anterior = None
                continue
            if PAT_SCENE.match(l):
                visibles, anterior = {}, None
                continue
            if PAT_FLUJO.match(l):
                anterior = None
    return casos, sin_sprite, sin_boca


casos, sin_sprite, sin_boca = revisar()

print("lineas seguidas sin cambio de boca:   %d" % len(casos))
print("  (descartadas: %d sin sprite en pantalla, %d con sprite sin boca)"
      % (len(sin_sprite), len(sin_boca)))
print("")

for r, i, quien, tag, boca, indent, txt in casos:
    par = PAREJA_BOCA.get(quien)
    sugerida = ""
    if par:
        sugerida = par[1] if boca == par[0] else par[0]
        sugerida = "  -> show %s %s" % (tag, sugerida)
    print("%s:%s  %s tiene %s puesta%s" % (r, i, quien, boca, sugerida))

if "-v" in sys.argv:
    print("\n-- descartados: el personaje habla sin sprite en pantalla --")
    for r, i, quien, _t, _b, _in, txt in sin_sprite:
        print("%s:%s  %s  %s" % (r, i, quien, txt))
    print("\n-- descartados: el sprite en pantalla no tiene boca (de espaldas) --")
    for r, i, quien, tag, _b, _in, txt in sin_boca:
        print("%s:%s  %s (%s)  %s" % (r, i, quien, tag, txt))

if not casos:
    print("Sin lineas con la boca congelada.")
sys.exit(1 if casos else 0)
