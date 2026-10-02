# -*- coding: utf-8 -*-
"""
Busca traducciones DESENGANCHADAS: entradas `old` de game/tl/ cuyo texto ya no
existe tal cual en game/script porque el original se edito despues.

EL PROBLEMA: una entrada `old`/`new` se aplica por COINCIDENCIA EXACTA del
texto. Si a la linea de la fuente se le agrega una tilde, se le cambia una
mayuscula o se le corrige una coma, el `old` deja de matchear y la traduccion
simplemente no se usa — el jugador en ingles ve la linea en español.

⚠️ NI EL LINT DE REN'PY NI NADA MAS AVISA DE ESTO. El juego corre perfecto; el
sintoma es texto en español apareciendo suelto en la partida en ingles, y hay
que toparselo jugando. Asi se encontro: un "Violet no está en su habitación."
saliendo en español al tocar su puerta (2026-09-04, tras la pasada ortografica
que agrego tildes a todo el juego y dejo 40 `old` apuntando a la version vieja).

QUE CUENTA COMO ROTO, y que no: un `old` huerfano puede ser dos cosas.
Contenido BORRADO —la entrada sobra pero no rompe nada— o texto EDITADO —el
`old` quedo viejo y la traduccion se perdio—. Solo el segundo es un bug, y se
detecta comparando sin tildes ni mayusculas: si asi coincide con un literal de
la fuente, el texto sigue existiendo y lo unico que cambio fue la forma.

USO
    python tools/validar_traducciones.py            # lista lo roto
    python tools/validar_traducciones.py --aplicar  # reescribe los `old`

Hermano de validar_sprites.py: los dos cubren un agujero que el lint no ve.
"""
import io
import os
import re
import sys
import unicodedata

RE_OLD = re.compile(r'^(\s*)old "((?:[^"\\]|\\.)*)"\s*$')
# Literales de la fuente: cualquier "..." de un .rpy de game/script.
RE_LIT = re.compile(r'"((?:[^"\\\n]|\\.)*)"')


def normalizar(t):
    """Saca SOLO tildes y mayusculas.

    Deliberadamente NO saca puntuacion ni espacios: con eso adentro,
    `old "Mostrar recompensa:"` matcheaba contra el nombre de variable
    `mostrar_recompensa` de la fuente y daba un falso positivo. La diferencia
    que buscamos es siempre de tilde o de mayuscula; cualquier otra cosa es
    otro texto.
    """
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.lower()


# ── 1. Todos los literales de la fuente, por forma normalizada ──────────────
fuente_txt = []
literales = {}
for base, _, fs in os.walk("game/script"):
    for f in fs:
        if not f.endswith(".rpy"):
            continue
        s = io.open(os.path.join(base, f), encoding="utf-8").read()
        fuente_txt.append(s)
        for m in RE_LIT.finditer(s):
            lit = m.group(1)
            if len(lit) < 4:
                continue
            k = normalizar(lit)
            if k:
                literales.setdefault(k, set()).add(lit)
fuente_txt = "\n".join(fuente_txt)

# ── 2. Los `old` que ya no matchean, pero cuyo texto SI existe normalizado ──
rotos = []
for base, _, fs in os.walk("game/tl"):
    for f in sorted(fs):
        if not f.endswith(".rpy") or f == "common.rpy":
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        for n, linea in enumerate(io.open(ruta, encoding="utf-8"), 1):
            m = RE_OLD.match(linea.rstrip("\n"))
            if not m:
                continue
            viejo = m.group(2)
            if not viejo or viejo in fuente_txt:
                continue
            cand = literales.get(normalizar(viejo))
            if not cand or len(cand) != 1:
                continue
            rotos.append((ruta, n, viejo, list(cand)[0]))

# ── 3. `new` vacios: la otra forma silenciosa de perder una traduccion ──────
# Un `old` que engancha bien pero con el `new` en blanco es PEOR que uno roto:
# el roto al menos cae en el español, y este deja el texto VACIO. Aparecio en
# una opcion de menu de la quest 02_b de Violet, que en ingles se veia como una
# opcion en blanco (2026-09-04).
RE_NEW = re.compile(r'^\s*new "((?:[^"\\]|\\.)*)"\s*$')

vacios = []
for base, _, fs in os.walk("game/tl"):
    for f in sorted(fs):
        if not f.endswith(".rpy"):
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        lineas = io.open(ruta, encoding="utf-8").read().split("\n")
        for i in range(1, len(lineas)):
            mn = RE_NEW.match(lineas[i])
            if mn is None or mn.group(1) != "":
                continue
            mo = RE_OLD.match(lineas[i - 1])
            if mo:
                vacios.append((ruta, i + 1, mo.group(1)))

# ── 4. `%` sueltos: revientan el juego en runtime ───────────────────────────
# renpy/exports/sayexports.py:118 hace `what = what % tag_quoting_dict` en TODA
# linea de dialogo, asi que un `%` literal se lee como especificador de formato:
# "30% de descuento" es `% d` (flag espacio + conversion d), pide un entero y
# tira TypeError al mostrarse. El lint NO lo ve. Se escribe `%%`.
# Reportado por un jugador el 2026-09-04 en la quest de amor 20 de Violet.
RE_DIALOGO = re.compile(r'^\s*(?:\w[\w.]*\s+)?"((?:[^"\\]|\\.)*)"\s*$')
RE_PCT = re.compile(r'(?<!%)%(?!%)')

pct = []
for raiz in ("game/script", "game/tl/english/script"):
    for base, _, fs in os.walk(raiz):
        for f in sorted(fs):
            if not f.endswith(".rpy"):
                continue
            ruta = os.path.join(base, f).replace("\\", "/")
            for n, linea in enumerate(io.open(ruta, encoding="utf-8"), 1):
                m = RE_DIALOGO.match(linea.rstrip("\n"))
                if m and RE_PCT.search(m.group(1)):
                    pct.append((ruta, n, m.group(1)))

# ── 5. Dialogos traducidos que quedaron en español ──────────────────────────
# El bloque existe y engancha, pero la linea traducida es el mismo texto
# original: alguien copio y no tradujo. En pantalla se ve español.
#
# MUCHO DE LO QUE COINCIDE ES LEGITIMO y hay que filtrarlo o el informe es
# ruido: los `...`, las onomatopeyas, las lineas que son solo una `[variable]`
# —el texto sale de ahi ya traducido con translate_string, asi que el bloque
# TIENE que ser identico— y las palabras que se escriben igual en los dos
# idiomas ("No", "Ok", "Sexy"). Se filtra por forma, no por lista negra:
# cualquier texto sin al menos dos palabras de letras de verdad se ignora.
RE_COM_D = re.compile(r'^(\s*)#\s*(\w[\w.]*\s+)?"((?:[^"\\]|\\.)*)"\s*$')
RE_TXT_D = re.compile(r'^(\s*)(\w[\w.]*\s+)?"((?:[^"\\]|\\.)*)"\s*$')
RE_INTERP = re.compile(r'^[\s.,!?¡¿]*\[[^\]]+\][\s.,!?¡¿]*$')


def _palabras(t):
    return re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{3,}', t)


sin_traducir = []
for base, _, fs in os.walk("game/tl/english/script"):
    for f in sorted(fs):
        if not f.endswith(".rpy"):
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        lineas = io.open(ruta, encoding="utf-8").read().split("\n")
        for i in range(len(lineas) - 1):
            mc = RE_COM_D.match(lineas[i])
            if not mc:
                continue
            mt = RE_TXT_D.match(lineas[i + 1])
            if not mt or not mt.group(3):
                continue
            if (mc.group(2) or "").strip() != (mt.group(2) or "").strip():
                continue
            txt = mt.group(3)
            if RE_INTERP.match(txt) or len(_palabras(txt)) < 2:
                continue
            # Bloque HUERFANO: su original ya no esta en la fuente, asi que no
            # se usa y da igual en que idioma quedo. Solo interesa lo vivo.
            if mc.group(3) not in fuente_txt:
                continue
            if normalizar(mc.group(3)) == normalizar(txt):
                sin_traducir.append((ruta, i + 2, txt))

# ── 6. Pares old/new donde el `new` es el mismo español ─────────────────────
# La version old/new del chequeo anterior. Importa sobre todo para el sistema
# de TALK, que muestra casi todo desde variables —nombre e intro del estado,
# mensaje de cada opcion, texto de la resolucion— y por lo tanto va todo por
# old/new: ahi un `new` copiado del español no lo detecta nada mas.
#
# Se descartan los que llevan `[interpolacion]` o `{markup}` y los que estan
# TODO EN MAYUSCULAS: esos son iguales en los dos idiomas por diseño.
# ── 6b. Dialogos con la traduccion VACIA ────────────────────────────────────
# Lo que deja Ren'Py al regenerar: el bloque nuevo sale con el original en el
# comentario y la linea traducida en `""`. Si se publica asi, el jugador en
# ingles ve el cuadro de dialogo EN BLANCO — peor que verlo en español.
#
# El chequeo 5 no los ve a proposito: ahi se comparan dos textos y uno vacio no
# se parece a nada. Este mira justamente eso, que el comentario tenga texto y
# la linea de abajo no.
vacios_dialogo = []
for base, _, fs in os.walk("game/tl/english/script"):
    for f in sorted(fs):
        if not f.endswith(".rpy"):
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        lineas = io.open(ruta, encoding="utf-8").read().split("\n")
        for i in range(len(lineas) - 1):
            mc2 = RE_COM_D.match(lineas[i])
            if not mc2 or not mc2.group(3):
                continue
            mt2 = RE_TXT_D.match(lineas[i + 1])
            if not mt2 or mt2.group(3):
                continue
            if (mc2.group(2) or "").strip() != (mt2.group(2) or "").strip():
                continue
            vacios_dialogo.append((ruta, i + 2, mc2.group(3)))


igual = []
for base, _, fs in os.walk("game/tl"):
    for f in sorted(fs):
        if not f.endswith(".rpy") or f == "common.rpy":
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        lineas = io.open(ruta, encoding="utf-8").read().split("\n")
        for i in range(len(lineas) - 1):
            mo = RE_OLD.match(lineas[i])
            if not mo:
                continue
            mn = RE_NEW.match(lineas[i + 1])
            if not mn or not mn.group(1):
                continue
            txt = mn.group(1)
            if "[" in txt or "{" in txt or txt.isupper():
                continue
            if len(_palabras(txt)) < 2:
                continue
            if normalizar(mo.group(1)) == normalizar(txt):
                igual.append((ruta, i + 2, txt))

# ── 7. translate_string(...).format() con tags de Ren'Py (CRASH) ────────────
# str.format lee {size=+8} / {color=#fff} como un campo y tira KeyError. Pasa
# con el texto original Y con su traduccion: una traduccion puede traer un tag
# que el original no tenia, y ahi solo crashea en ingles. Bug real: el aviso de
# "Partida incompatible" nunca se pudo mostrar (Sentry S15).
import string as _string

_fmt = _string.Formatter()

_pares_tl = {}
for base, _, fs in os.walk("game/tl/english"):
    for f in sorted(fs):
        if not f.endswith(".rpy"):
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        txt = io.open(ruta, encoding="utf-8-sig").read()
        for m in re.finditer(r'^\s*old\s+"((?:[^"\\]|\\.)*)"\s*\n\s*new\s+"((?:[^"\\]|\\.)*)"',
                             txt, re.M):
            _pares_tl[m.group(1)] = m.group(2)

_RE_TS_FMT = re.compile(
    r'translate_string\(\s*\n?\s*((?:u?"(?:[^"\\]|\\.)*"\s*\n?\s*)+)\)\s*\.?\s*\n?\s*\.format\(', re.S)
_RE_LIT = re.compile(r'u?"((?:[^"\\]|\\.)*)"')

fmt_tags = []
for base, _, fs in os.walk("game/script"):
    for f in sorted(fs):
        if not f.endswith(".rpy"):
            continue
        ruta = os.path.join(base, f).replace("\\", "/")
        txt = io.open(ruta, encoding="utf-8").read()
        for m in _RE_TS_FMT.finditer(txt):
            fuente = "".join(_RE_LIT.findall(m.group(1)))
            n = txt[:m.start()].count("\n") + 1
            for etiqueta, s in (("ES", fuente), ("EN", _pares_tl.get(fuente))):
                if s is None:
                    continue
                try:
                    campos = [c for (_l, c, _sp, _cv) in _fmt.parse(s) if c is not None]
                except Exception as e:
                    fmt_tags.append((ruta, n, etiqueta, "%s: %s" % (type(e).__name__, e), s))
                    continue
                for c in campos:
                    if "=" in c or c.startswith("/"):
                        fmt_tags.append((ruta, n, etiqueta, "tag {%s} leido como campo" % c, s))

print("`old` rotos por edicion del texto: {}".format(len(rotos)))
print("`new` vacios (sin traducir):       {}".format(len(vacios)))
print("dialogos con traduccion VACIA:     {}".format(len(vacios_dialogo)))
print("`%` sueltos en dialogo (CRASH):    {}".format(len(pct)))
print("dialogos que quedaron en español:  {}".format(len(sin_traducir)))
print("old/new sin traducir (new==old):   {}".format(len(igual)))
print("format() sobre tags de Ren'Py:     {}".format(len(fmt_tags)))
for ruta, n, etiqueta, err, s in fmt_tags:
    print(u"{}:{}  [{}] CRASH AL FORMATEAR — {}".format(ruta, n, etiqueta, err))
    print(u"    {}".format(s[:95]))
for ruta, n, txt in igual:
    print(u"{}:{}  `new` IGUAL AL ESPAÑOL".format(
        ruta.replace("game/tl/english/", ""), n))
    print(u"    {}".format(txt[:95]))
for ruta, n, txt in sin_traducir:
    print(u"{}:{}  SIN TRADUCIR (copia del original)".format(
        ruta.replace("game/tl/english/script/", ""), n))
    print(u"    {}".format(txt[:95]))
print("")
for ruta, n, txt in pct:
    print(u"{}:{}  `%` SUELTO — va `%%`".format(ruta, n))
    print(u"    {}".format(txt[:95]))
for ruta, n, viejo, nuevo in rotos:
    print(u"{}:{}".format(ruta.replace("game/tl/english/", ""), n))
    print(u"    tl:     {}".format(viejo[:95]))
    print(u"    fuente: {}".format(nuevo[:95]))
for ruta, n, viejo in vacios:
    print(u"{}:{}  SIN TRADUCIR".format(ruta.replace("game/tl/english/", ""), n))
    print(u"    {}".format(viejo[:95]))
for ruta, n, orig in vacios_dialogo:
    print(u"{}:{}  DIALOGO VACIO".format(
        ruta.replace("game/tl/english/script/", ""), n))
    print(u"    {}".format(orig[:95]))

if "--aplicar" in sys.argv:
    por_archivo = {}
    for ruta, n, viejo, nuevo in rotos:
        por_archivo.setdefault(ruta, []).append((viejo, nuevo))
    for ruta, pares in por_archivo.items():
        s = io.open(ruta, encoding="utf-8").read()
        for viejo, nuevo in pares:
            a = u'old "{}"'.format(viejo)
            b = u'old "{}"'.format(nuevo)
            assert s.count(a) == 1, (ruta, s.count(a), viejo[:50])
            s = s.replace(a, b)
        io.open(ruta, "w", encoding="utf-8", newline="").write(s)
    print("")
    print("aplicado en {} archivos".format(len(por_archivo)))
else:
    print("")
    print("(simulacion: no se escribio nada. Correr con --aplicar)")
