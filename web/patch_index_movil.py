# -*- coding: utf-8 -*-
"""
Patch del index.html del build WEB — arreglo de pantalla en celulares.

QUE HACE
--------
Edita el CONTENIDO del index.html del build web. NO lo mueve ni lo renombra:
queda en la raiz (que es lo que itch.io y gamecore exigen).

Aplica 3 arreglos:

1. viewport meta -> agrega `user-scalable=no, viewport-fit=cover`
   Sin esto un pinch-zoom accidental manda el juego fuera de pantalla, y el
   contenido no usa el area detras del notch.

2. html, body -> agrega `margin:0; padding:0; overflow:hidden`
   Evita que el contenido pueda desbordar y quedar accesible solo con scroll.

3. #canvas -> agrega `height: 100dvh` despues del `height: 100%`
   ESTE ES EL ARREGLO PRINCIPAL. En navegadores moviles `height: 100%` resuelve
   contra el viewport "grande" (como si la barra de direcciones estuviera
   retraida), asi que la franja inferior del juego queda tapada por la barra.
   `dvh` (dynamic viewport height) usa el alto REAL visible.
   El `height: 100%` se conserva arriba como fallback para navegadores viejos.

4. Arranque -> cartel si no hay WebGL, y espera a que la pestaña este visible
   Sin WebGL, Ren'Py no consigue ningun renderer y muere con "Could not set
   video mode" / "'NoneType' has no attribute 'screenshot'" ANTES de poder
   dibujar nada: el jugador ve la pantalla de error de Ren'Py sin saber por
   que (Sentry S04/S06/S07/S09; tres dispositivos distintos en 36 h el
   17-18/09/2026, Chrome actual — aceleracion por hardware apagada, GPU en
   lista negra, navegadores "con privacidad" como Norton que bloquean WebGL).
   El arranque de renpy.js pasa a un script inline que primero prueba
   getContext('webgl2'/'webgl') en un canvas APARTE (probar en #canvas le
   robaria el contexto al motor) y, si no hay, muestra un cartel HTML
   bilingue con "Reintentar" e "Intentar igual". Ademas espera a que
   document.visibilityState no sea "hidden" antes de lanzar: un arranque en
   una pestaña restaurada en segundo plano puede no recibir contexto de GL.

USO — MODO ACTIVO: EL TEMPLATE DEL SDK (automatico)
---------------------------------------------------
El patch YA ESTA APLICADO al template del SDK, asi que TODO build web sale
arreglado solo. No hay que hacer nada despues de buildear.

    python web/patch_index_movil.py "C:/Renpy/renpy-8.4.1-sdk/web/index.html"

>>> CUANDO HAY QUE VOLVER A CORRER ESE COMANDO <<<
Al ACTUALIZAR REN'PY. El instalador reemplaza web/index.html y se lleva puesto
el patch, sin avisar. Sintoma: vuelve a cortarse la pantalla en celulares.
El script es idempotente, asi que correrlo de mas no rompe nada.

Se eligio el SDK y no un paso post-build porque el build web de Ren'Py NO tiene
hooks (verificado en launcher/game/web.rpy): no hay donde enganchar un script
que corra solo, y un paso manual se olvida.

USO ALTERNATIVO — sobre un build ya generado
--------------------------------------------
Sirve si el SDK quedo sin patchear (ej. justo despues de actualizarlo) y no se
quiere re-buildear. Ren'Py genera la carpeta Y el .zip, pero arma el zip ANTES
de que puedas tocar la carpeta, asi que lo util es patchear el zip:

    python web/patch_index_movil.py "C:/ruta/Japitown-0.1.8c-web.zip"

Tambien acepta la carpeta (para probar local con el webserver de Ren'Py).
En todos los casos deja un backup .orig y es idempotente.

NOTA: Ren'Py lee el index.html del SDK (launcher/game/web.rpy:451) y no soporta
override por proyecto — por eso este script existe en vez de un archivo propio.
"""

import io
import os
import shutil
import sys
import zipfile


# Reemplazo del arranque de renpy.js: el cartel y el script que decide si
# lanzar. Va como constante aparte porque es largo. Los textos van en español
# e ingles, con entidades HTML para no depender del charset del template.
CARTEL_WEBGL = (
    '  <script src="renpy-pre.js"></script>\n'
    '\n'
    '  <!-- Japitown: cartel si el navegador no tiene WebGL (ver web/patch_index_movil.py). -->\n'
    '  <div id="jpSinWebGL" style="display:none; position:fixed; inset:0; z-index:9999; background:#0d0d1e; color:#fff; font-family:sans-serif; align-items:center; justify-content:center; text-align:center; padding:24px; box-sizing:border-box;">\n'
    '    <div style="max-width:640px;">\n'
    '      <div style="font-size:28px; font-weight:bold; margin-bottom:16px;">Este navegador no tiene WebGL activado</div>\n'
    '      <div style="font-size:16px; line-height:1.5; color:#ccc; margin-bottom:12px;">Japitown necesita WebGL para dibujar. Activ&aacute; la <b>aceleraci&oacute;n por hardware</b> en la configuraci&oacute;n del navegador, desactiv&aacute; extensiones o modos de privacidad que bloqueen WebGL, o prob&aacute; con otro navegador (Chrome, Firefox, Edge). Tambi&eacute;n pod&eacute;s descargar la versi&oacute;n de escritorio.</div>\n'
    '      <div style="font-size:14px; line-height:1.5; color:#999; margin-bottom:24px;"><b>This browser doesn\'t have WebGL enabled.</b> Japitown needs WebGL to draw. Turn on <b>hardware acceleration</b> in your browser settings, disable extensions or privacy modes that block WebGL, or try another browser (Chrome, Firefox, Edge). You can also download the desktop version.</div>\n'
    '      <button onclick="location.reload()" style="font-size:16px; padding:10px 22px; margin:6px; cursor:pointer; background:#4FC3F7; color:#000; border:0; border-radius:6px;">Reintentar / Retry</button>\n'
    '      <button onclick="jpLanzarIgual()" style="font-size:16px; padding:10px 22px; margin:6px; cursor:pointer; background:#333; color:#fff; border:0; border-radius:6px;">Intentar igual / Try anyway</button>\n'
    '    </div>\n'
    '  </div>\n'
    '  <script>\n'
    '    (function () {\n'
    '      function jpTieneWebGL() {\n'
    '        try {\n'
    "          var c = document.createElement('canvas');   // canvas APARTE: no tocar #canvas\n"
    "          return !!(c.getContext('webgl2') || c.getContext('webgl') || c.getContext('experimental-webgl'));\n"
    '        } catch (e) { return false; }\n'
    '      }\n'
    '      var lanzado = false;\n'
    '      function jpLanzar() {\n'
    '        if (lanzado) { return; }\n'
    '        lanzado = true;\n'
    "        var s = document.createElement('script');\n"
    '        s.async = true;\n'
    "        s.type = 'text/javascript';\n"
    "        s.src = 'renpy.js';\n"
    '        document.body.appendChild(s);\n'
    '      }\n'
    '      window.jpLanzarIgual = function () {\n'
    "        document.getElementById('jpSinWebGL').style.display = 'none';\n"
    '        jpLanzar();\n'
    '      };\n'
    '      function jpCuandoVisible(fn) {\n'
    "        if (document.visibilityState !== 'hidden') { fn(); return; }\n"
    "        document.addEventListener('visibilitychange', function h() {\n"
    "          if (document.visibilityState !== 'hidden') {\n"
    "            document.removeEventListener('visibilitychange', h);\n"
    '            fn();\n'
    '          }\n'
    '        });\n'
    '      }\n'
    '      jpCuandoVisible(function () {\n'
    '        if (jpTieneWebGL()) { jpLanzar(); return; }\n'
    "        var p = document.getElementById('presplash');\n"
    "        if (p) { p.style.display = 'none'; }\n"
    "        document.getElementById('jpSinWebGL').style.display = 'flex';\n"
    '      });\n'
    '    })();\n'
    '  </script>\n'
)

# (nombre, texto_a_buscar, texto_de_reemplazo, marca_de_ya_aplicado)
PATCHES = [
    (
        "viewport meta (anti pinch-zoom + notch)",
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, '
        'user-scalable=no, viewport-fit=cover">',
        "user-scalable=no",
    ),
    (
        "html/body (sin desborde ni margenes)",
        "    body, html {\n"
        "      overscroll-behavior: none;\n"
        "    }",
        "    body, html {\n"
        "      overscroll-behavior: none;\n"
        "      margin: 0;\n"
        "      padding: 0;\n"
        "      overflow: hidden;\n"
        "    }",
        "overflow: hidden;\n    }",
    ),
    (
        "canvas height 100dvh (barra del navegador movil)",
        "      width: 100%;\n"
        "      height: 100%;\n"
        "\n"
        "      border: 0 none;",
        "      width: 100%;\n"
        "      /* 100% queda de fallback para navegadores viejos; 100dvh usa el\n"
        "         alto REAL del viewport, sin la barra del navegador movil. */\n"
        "      height: 100%;\n"
        "      height: 100dvh;\n"
        "\n"
        "      border: 0 none;",
        "height: 100dvh;",
    ),
    (
        "arranque: cartel sin WebGL + espera a pestaña visible",
        '  <script src="renpy-pre.js"></script>\n'
        '  <script async type="text/javascript" src="renpy.js"></script>\n',
        CARTEL_WEBGL,
        "jpSinWebGL",
    ),
]


def aplicar_patches(html):
    """Devuelve (html_nuevo, aplicados, ya_estaban, fallados)."""
    aplicados, ya_estaban, fallados = [], [], []

    for nombre, buscar, reemplazo, marca in PATCHES:
        if marca in html:
            ya_estaban.append(nombre)
            continue
        if buscar not in html:
            fallados.append(nombre)
            continue
        html = html.replace(buscar, reemplazo, 1)
        aplicados.append(nombre)

    return html, aplicados, ya_estaban, fallados


def reportar(origen, aplicados, ya_estaban, fallados):
    print("")
    print("Archivo: %s" % origen)
    for n in aplicados:
        print("  [APLICADO]   %s" % n)
    for n in ya_estaban:
        print("  [YA ESTABA]  %s" % n)
    for n in fallados:
        print("  [NO ENCONTRO PATRON] %s" % n)

    if fallados:
        print("")
        print("AVISO: algun patron no se encontro. Puede que el SDK de Ren'Py haya")
        print("cambiado el template. Revisar el index.html a mano.")
        return 1

    print("")
    if aplicados:
        print("OK - index.html patcheado EN SU LUGAR (sigue en la raiz).")
    else:
        print("OK - ya estaba todo aplicado, no habia nada que hacer.")
    return 0


def patch_suelto(index):
    """Patchea un index.html en disco (carpeta de build o archivo directo)."""
    if not os.path.isfile(index):
        print("ERROR: no existe %s" % index)
        return 1

    with io.open(index, "r", encoding="utf-8") as f:
        original = f.read()

    html, aplicados, ya_estaban, fallados = aplicar_patches(original)

    if html != original:
        backup = index + ".orig"
        if not os.path.exists(backup):
            with io.open(backup, "w", encoding="utf-8") as f:
                f.write(original)
            print("Backup del original -> %s" % os.path.basename(backup))

        with io.open(index, "w", encoding="utf-8") as f:
            f.write(html)

    return reportar(index, aplicados, ya_estaban, fallados)


def patch_zip(ruta):
    """
    Patchea el index.html DENTRO del .zip del build.

    zipfile no permite reemplazar una entrada in-place, asi que se reescribe el
    zip entero preservando orden, fechas y tipo de compresion de cada entrada.
    """
    with zipfile.ZipFile(ruta, "r") as zin:
        nombres = zin.namelist()
        if "index.html" not in nombres:
            print("ERROR: el zip no tiene index.html en la raiz.")
            print("       Entradas encontradas (primeras 10): %s" % nombres[:10])
            return 1

        original = zin.read("index.html").decode("utf-8")
        html, aplicados, ya_estaban, fallados = aplicar_patches(original)

        if html == original:
            return reportar(ruta, aplicados, ya_estaban, fallados)

        # Backup del zip original, una sola vez.
        backup = ruta + ".orig"
        if not os.path.exists(backup):
            shutil.copy2(ruta, backup)
            print("Backup del zip original -> %s" % os.path.basename(backup))

        tmp = ruta + ".tmp"
        with zipfile.ZipFile(tmp, "w", allowZip64=True) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "index.html":
                    data = html.encode("utf-8")
                # Pasar el ZipInfo preserva fecha y compress_type de la entrada
                zout.writestr(item, data, compress_type=item.compress_type)

    os.replace(tmp, ruta)
    return reportar(ruta, aplicados, ya_estaban, fallados)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("ERROR: falta la ruta del build web (.zip, carpeta o index.html).")
        return 1

    ruta = sys.argv[1]

    if os.path.isdir(ruta):
        return patch_suelto(os.path.join(ruta, "index.html"))

    if ruta.lower().endswith(".zip"):
        if not os.path.isfile(ruta):
            print("ERROR: no existe %s" % ruta)
            return 1
        return patch_zip(ruta)

    return patch_suelto(ruta)


if __name__ == "__main__":
    sys.exit(main())
