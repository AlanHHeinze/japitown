# -*- coding: utf-8 -*-
"""
Valida los atributos de cada `show <tag> <attrs>` contra su layeredimage.

POR QUE HACE FALTA: el lint de Ren'Py NO chequea esto. Un `show monica_parada
b_abiertachica` —una boca que existe en el MC pero no en Monica— pasa el lint
sin decir nada y revienta recien cuando el jugador llega a esa linea.

El error tipico es siempre el mismo: un atributo que existe en OTRO personaje.
Los nombres se parecen mucho entre layereds (`c_rbase_celu` es de Violet,
`c_rbase_celular` del MC) y se copian lineas de una quest a otra.

USO
    python tools/validar_sprites.py                 # todo game/script
    python tools/validar_sprites.py archivo.rpy ... # solo esos archivos

Sale con codigo 1 si encuentra algo, asi que sirve para un hook o para correrlo
antes de commitear.

HISTORIA: reemplaza al verify_sprites.py de febrero, que hacia lo mismo pero
solo leia los layeredimage de los archivos `sprites_*.rpy`. Hay una decena
definidos fuera de ahi —`vq9_boca` en el minijuego, `beso_amor` en la quest 06,
`violet_ducha_quest` en la 08— y para esos no tenia catalogo, asi que ni los
miraba. Ademas tenia la ruta del proyecto escrita a mano adentro.
"""
import io
import os
import re
import sys

# La raiz del repo es la carpeta que contiene a tools/.
RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_SCRIPT = os.path.join(RAIZ_REPO, "game", "script")

# Los nombres de atributo pueden llevar ñ y tildes a proposito (son
# identificadores, no nombres de archivo — ver la regla de nombres ASCII).
NOMBRE = r'[A-Za-z_][\wÀ-ɏ]*'

RE_LAYEREDIMAGE = re.compile(r'^layeredimage\s+(' + NOMBRE + r')\s*:')
RE_ATTRIBUTE = re.compile(r'^\s*attribute\s+(' + NOMBRE + r')')

# `show <tag> <attrs...>` hasta la primera palabra clave de Ren'Py. El `-` de
# adelante es la forma de SACAR un atributo (`show x -b_hablando`).
RE_SHOW = re.compile(
    r'^\s*show\s+(' + NOMBRE + r')((?:\s+-?' + NOMBRE + r')*)'
    r'\s*(?:\bat\b|\bwith\b|\bas\b|\bbehind\b|\bonlayer\b|\bzorder\b|:|$)'
)

# `show screen`, `show expression` y `show text` no muestran un layeredimage.
PALABRAS_CLAVE = {"at", "with", "as", "behind", "onlayer", "zorder",
                  "expression", "screen", "text", "layer"}


def construir_catalogo(dir_script):
    """{tag del layeredimage: set de atributos validos}, mirando TODO script/."""
    catalogo = {}
    for base, _, archivos in os.walk(dir_script):
        for nombre in archivos:
            if not nombre.endswith(".rpy"):
                continue
            tag = None
            ruta = os.path.join(base, nombre)
            for linea in io.open(ruta, encoding="utf-8"):
                m = RE_LAYEREDIMAGE.match(linea)
                if m:
                    tag = m.group(1)
                    catalogo.setdefault(tag, set())
                    continue
                # Una linea sin indentar cierra el bloque del layeredimage.
                if tag and linea.strip() and not linea[:1].isspace():
                    tag = None
                if tag:
                    ma = RE_ATTRIBUTE.match(linea)
                    if ma:
                        catalogo[tag].add(ma.group(1))
    return catalogo


def revisar(rutas, catalogo):
    """Lista de (ruta, linea, tag, atributo, texto) con lo que no existe."""
    problemas = []
    for ruta in rutas:
        for n, linea in enumerate(io.open(ruta, encoding="utf-8"), 1):
            m = RE_SHOW.match(linea)
            if not m:
                continue
            tag = m.group(1)
            # Un tag desconocido no es error: puede ser una `image` comun.
            if tag in PALABRAS_CLAVE or tag not in catalogo:
                continue
            for attr in m.group(2).split():
                if attr in PALABRAS_CLAVE:
                    break
                if attr.lstrip("-") not in catalogo[tag]:
                    problemas.append((ruta, n, tag, attr, linea.strip()))
    return problemas


def main():
    catalogo = construir_catalogo(DIR_SCRIPT)

    rutas = sys.argv[1:]
    if not rutas:
        rutas = [os.path.join(base, f)
                 for base, _, archivos in os.walk(DIR_SCRIPT)
                 for f in archivos if f.endswith(".rpy")]

    problemas = revisar(rutas, catalogo)

    # Sin acentos ni simbolos raros en la salida: la consola de Windows suele
    # estar en cp1252 y los rompe.
    print(u"{} layeredimage en el catalogo, {} archivos revisados".format(
        len(catalogo), len(rutas)))

    if not problemas:
        print(u"Sin atributos invalidos.")
        return 0

    print(u"\n{} atributo(s) que no existen:\n".format(len(problemas)))
    for ruta, n, tag, attr, texto in problemas:
        rel = os.path.relpath(ruta, RAIZ_REPO).replace("\\", "/")
        print(u"{}:{}".format(rel, n))
        print(u"    {}".format(texto))
        print(u"    '{}' no esta en {}\n".format(attr, tag))
    return 1


if __name__ == "__main__":
    sys.exit(main())
