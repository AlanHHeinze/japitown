# -*- coding: utf-8 -*-
"""Que globals del store necesita cada .save para poder abrirse.

Lee los opcodes del pickle (SIN ejecutarlo) y junta los GLOBAL/STACK_GLOBAL del
modulo `store`; despues los cruza contra lo que el codigo define hoy. Lo que
aparezca en la ultima columna es un nombre que el unpickler NO va a poder
resolver: ese save no abre (AttributeError adentro de renpy.load, ver S12 en
docs/errores/errores_sentry_registro.md). El arreglo es agregar el nombre a
JP_NOMBRES_MUERTOS (game/script/core/utils/compat_nombres_muertos.rpy).

Uso: python tools/escanear_saves.py    (desde la raiz del proyecto)

Ojo: los nombres del propio Ren'Py (VoiceInfo, etc.) salen como faltantes
porque no estan en game/script — se ignoran.
"""
import io, os, re, json, zipfile, glob, pickletools

SAVEDIR = os.path.expandvars(r"%APPDATA%\RenPy\Japitown-1758721792")

def globals_de_pickle(datos):
    """(modulo, nombre) de cada GLOBAL/STACK_GLOBAL, sin ejecutar nada."""
    out = set()
    ultimos = []
    try:
        for op, arg, pos in pickletools.genops(datos):
            if op.name == "GLOBAL":
                mod, _, nom = str(arg).partition(" ")
                out.add((mod, nom))
            elif op.name in ("SHORT_BINUNICODE", "BINUNICODE", "UNICODE", "STRING",
                             "SHORT_BINSTRING", "BINSTRING", "MEMOIZE"):
                if op.name != "MEMOIZE":
                    ultimos.append(arg)
                    if len(ultimos) > 4:
                        ultimos.pop(0)
            elif op.name == "STACK_GLOBAL":
                if len(ultimos) >= 2:
                    out.add((ultimos[-2], ultimos[-1]))
    except Exception:
        pass
    return out

# Lo que el codigo define HOY en el store.
definidas = set()
for p in glob.glob("game/script/**/*.rpy", recursive=True):
    t = io.open(p, encoding="utf-8").read()
    definidas.update(re.findall(r"^\s*def\s+([A-Za-z_]\w*)", t, re.M))
    definidas.update(re.findall(r"^\s*(?:default|define)\s+(?:-?\d+\s+)?([A-Za-z_]\w*)", t, re.M))
    definidas.update(re.findall(r"^\s*class\s+([A-Za-z_]\w*)", t, re.M))
    definidas.update(re.findall(r"^\s*image\s+([A-Za-z_]\w*)", t, re.M))

print("%-24s %-10s %-6s %s" % ("save", "version", "gen", "globals de store que faltan"))
for f in sorted(glob.glob(os.path.join(SAVEDIR, "*.save"))):
    try:
        z = zipfile.ZipFile(f)
        meta = json.loads(z.read("json").decode("utf-8"))
    except Exception as e:
        print("%-24s NO ABRE: %r" % (os.path.basename(f), e))
        continue
    faltan = set()
    for nombre in z.namelist():
        if nombre in ("json", "screenshot.png"):
            continue
        try:
            datos = z.read(nombre)
        except Exception:
            continue
        for mod, nom in globals_de_pickle(datos):
            if mod == "store" and nom not in definidas:
                faltan.add(nom)
    print("%-24s %-10s %-6s %s" % (
        os.path.basename(f), meta.get("_version", "?"),
        meta.get("jp_save_gen", "-"),
        ", ".join(sorted(faltan)) if faltan else "(ninguno)"))
