# -*- coding: utf-8 -*-
"""
Recupera las traducciones al ingles que quedaron desenganchadas por la pasada
ortografica.

EL PROBLEMA: Ren'Py ata cada traduccion de dialogo al hash del texto original.
Al corregir una tilde o una coma, el bloque viejo deja de coincidir y
`renpy translate english` crea uno NUEVO con la traduccion vacia. El ingles que
ya existia sigue en el archivo, pero en un bloque que ya no usa nadie.

QUE HACE: por cada bloque vacio busca su hermano huerfano —el que dice casi lo
mismo en español— y le copia el ingles.

COMO LOS EMPAREJA, en dos pasadas:

  1. NORMALIZANDO: saca tildes, mayusculas y puntuacion de los dos textos y los
     compara. Con eso caza de una todas las correcciones de tilde, coma, signo
     de apertura y mayuscula, que son la enorme mayoria.

  2. POR EL REGISTRO DE PARES (tools/ortografia_pares.txt): para lo que cambio
     de palabra —voseo, typos— reconstruye el texto viejo aplicando los pares al
     reves y busca coincidencia exacta.

Lo que no logra emparejar lo lista al final: eso es contenido genuinamente
nuevo, y hay que traducirlo a mano.

USO
    python tools/reenganchar_traducciones.py            # muestra que haria
    python tools/reenganchar_traducciones.py --aplicar  # escribe los archivos
"""
import io
import os
import re
import sys
import unicodedata

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_TL = os.path.join(RAIZ_REPO, "game", "tl", "english")
PARES = os.path.join(RAIZ_REPO, "tools", "ortografia_pares.txt")

# Una linea de bloque: `    # piensa "texto"` y despues `    piensa "texto"`.
RE_COMENTARIO = re.compile(r'^(\s*)#\s*(\w[\w.]*\s+)?"((?:[^"\\]|\\.)*)"\s*$')
RE_CONTENIDO = re.compile(r'^(\s*)(\w[\w.]*\s+)?"((?:[^"\\]|\\.)*)"\s*$')


def normalizar(t):
    """Sin tildes, sin mayusculas y sin nada que no sea letra o numero."""
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r'[^0-9a-zA-Z]+', '', t).lower()


def leer_pares():
    """[(viejo, nuevo)] del registro de la pasada ortografica."""
    if not os.path.exists(PARES):
        return []
    rv, viejo = [], None
    for linea in io.open(PARES, encoding="utf-8"):
        if linea.startswith("VIEJO   "):
            viejo = linea[8:].rstrip("\n")
        elif linea.startswith("NUEVO   ") and viejo is not None:
            rv.append((viejo, linea[8:].rstrip("\n")))
            viejo = None
    return rv


def archivos_tl():
    rv = []
    for base, _, files in os.walk(DIR_TL):
        for f in files:
            if f.endswith(".rpy"):
                rv.append(os.path.join(base, f))
    return sorted(rv)


def escanear(lineas):
    """
    Recorre un archivo tl y devuelve la lista de bloques de dialogo:
    (indice_de_la_linea_de_contenido, español, ingles).

    Un bloque es un comentario con el original seguido de la linea traducida.
    """
    rv = []
    for i in range(len(lineas) - 1):
        mc = RE_COMENTARIO.match(lineas[i])
        if not mc:
            continue
        mt = RE_CONTENIDO.match(lineas[i + 1])
        if not mt:
            continue
        # El personaje tiene que ser el mismo en las dos lineas.
        if (mc.group(2) or "").strip() != (mt.group(2) or "").strip():
            continue
        rv.append((i + 1, mc.group(3), mt.group(3)))
    return rv


def main():
    aplicar = "--aplicar" in sys.argv
    pares = leer_pares()

    # ── 1. Mapa de traducciones vivas, por texto normalizado ────────────────
    por_norma = {}
    exactos = {}
    colisiones = set()
    todos = {}
    # Mapa por ARCHIVO: un texto corto y ambiguo ("Si", "En serio?") casi
    # siempre se traduce igual dentro de la misma escena, aunque en otra
    # parte del juego tenga otra version. Se consulta antes que el global.
    por_norma_archivo = {}

    for ruta in archivos_tl():
        lineas = io.open(ruta, encoding="utf-8").read().split("\n")
        todos[ruta] = lineas
        local = {}
        local_col = set()
        for _, es, en in escanear(lineas):
            if not en:
                continue
            exactos.setdefault(es, en)
            k = normalizar(es)
            if k in por_norma and por_norma[k] != en:
                colisiones.add(k)
            por_norma[k] = en
            if k in local and local[k] != en:
                local_col.add(k)
            local[k] = en
        # Lo ambiguo DENTRO del archivo tampoco sirve: se descarta.
        for k in local_col:
            local.pop(k, None)
        por_norma_archivo[ruta] = local

    # ── 2. Rellenar los vacios ──────────────────────────────────────────────
    recuperados, sin_par, por_archivo = 0, [], {}

    for ruta, lineas in todos.items():
        cambios = 0
        for idx, es, en in escanear(lineas):
            if en:
                continue

            ingles = None
            k = normalizar(es)
            local = por_norma_archivo.get(ruta, {})
            if k in local:
                # Mismo archivo: gana aunque en el resto del juego sea ambiguo.
                ingles = local[k]
            elif k in por_norma and k not in colisiones:
                ingles = por_norma[k]
            else:
                # Reconstruir el español viejo aplicando los pares al reves.
                for viejo, nuevo in pares:
                    if nuevo and nuevo in es:
                        cand = es.replace(nuevo, viejo)
                        if cand in exactos:
                            ingles = exactos[cand]
                            break

            if ingles is None:
                sin_par.append((os.path.relpath(ruta, RAIZ_REPO).replace("\\", "/"), es))
                continue

            linea = lineas[idx]
            m = RE_CONTENIDO.match(linea)
            prefijo = (m.group(2) or "")
            lineas[idx] = '{}{}"{}"'.format(m.group(1), prefijo, ingles)
            recuperados += 1
            cambios += 1

        if cambios:
            por_archivo[ruta] = cambios
            if aplicar:
                io.open(ruta, "w", encoding="utf-8", newline="").write("\n".join(lineas))

    # ── 3. Informe ──────────────────────────────────────────────────────────
    print("pares en el registro:      {}".format(len(pares)))
    print("traducciones recuperadas:  {}".format(recuperados))
    print("sin par (a traducir):      {}".format(len(sin_par)))
    if colisiones:
        print("claves ambiguas salteadas: {}".format(len(colisiones)))
    print("")

    if por_archivo:
        print("Archivos tocados:")
        for ruta in sorted(por_archivo):
            print("  {:>4}  {}".format(
                por_archivo[ruta], os.path.relpath(ruta, RAIZ_REPO).replace("\\", "/")))
        print("")

    if sin_par:
        print("SIN PAR — hay que traducirlas a mano:")
        for ruta, es in sin_par[:60]:
            print(u"  {}".format(ruta))
            print(u"      {}".format(es[:95]))
        if len(sin_par) > 60:
            print("  ... y {} mas".format(len(sin_par) - 60))

    if not aplicar:
        print("")
        print("(simulacion: no se escribio nada. Correr con --aplicar)")


if __name__ == "__main__":
    main()
