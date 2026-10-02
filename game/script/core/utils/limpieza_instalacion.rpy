################################################################################
## Limpieza de instalacion — archivos de versiones viejas que quedaron en disco
################################################################################
## EL PROBLEMA (Sentry cabeccb7, 2026-09-17, jugador de escritorio en 0.1.9.1):
##
##     Exception: A translation for "Desbloqueos" already exists at
##     game/tl/english/relaciones_strings.rpy:39.
##       en game/tl/english/script/ui/hud/hud_relaciones.rpy:6
##
## Ese archivo no existe en la 0.1.9.1: se borro en agosto (d64faec), cuando sus
## strings pasaron a relaciones_strings.rpy. El jugador DESCOMPRIMIO LA VERSION
## NUEVA ENCIMA DE UNA INSTALACION VIEJA: los archivos nuevos pisan a los que
## siguen existiendo, pero los que ya no estan en el zip quedan en disco, y
## Ren'Py los carga como si fueran parte del juego. Dos archivos traduciendo el
## mismo string = excepcion en init = el juego no arranca. Y sin traducciones de
## por medio, un .rpy viejo suelto puede registrar labels, screens o quests que
## ya no existen — bugs imposibles de reproducir desde el repo.
##
## LA SOLUCION: al arrancar, ANTES de que corra ningun init del juego
## (prioridad -999; los `translate strings` corren en 0), se buscan en disco los
## archivos que existieron en alguna version publicada y hoy no estan. Si hay
## alguno, se borra (con su .rpyc) y se hace renpy.utter_restart(): Ren'Py
## vuelve a cargar todo desde cero, ya sin el archivo. El jugador ve un
## parpadeo en el arranque y nada mas.
##
## SOLO EN ESCRITORIO (Windows/Linux) y NUNCA EN DESARROLLO:
##   - web: los archivos viven dentro de game.zip, siempre fresco; no aplica.
##   - mac: el .app es un bundle firmado; el jugador reemplaza el .app entero.
##   - android/ios: el paquete se reemplaza entero.
##   - config.developer (SDK): jamas borrar nada del working tree.
##
## LA LISTA se saca del historial de git — todo .rpy borrado alguna vez que no
## exista hoy:
##
##     git log --diff-filter=D --name-only --format="" -- "game/**/*.rpy" | sort -u
##
## Al BORRAR un .rpy del proyecto, su ruta se agrega aca. Solo se borran rutas
## de esta lista: nunca se toca un archivo que el juego no haya despachado antes.
################################################################################

init -999 python:

    import os as _li_os

    # Rutas relativas a la carpeta del juego (config.basedir), sin extension.
    JP_ARCHIVOS_VERSIONES_VIEJAS = [
        # ── Estructura vieja (antes de script/core, script/characters) ──
        "game/script/intro",
        "game/script/elements/elements",
        "game/script/mechanics/locations_intro",
        "game/script/mechanics/mechanics",
        "game/script/mechanics/transforms",
        "game/script/story/intro/intro_airport",
        "game/script/story/intro/intro_main",
        "game/script/story/intro/screen_aeropuerto_nuevo",
        "game/script/story/intro/screen_tarjeta_padre",
        "game/script/story/intro/tutorial",
        "game/script/ui/gui",
        "game/script/ui/style",
        "game/script/characters/characters_intro",
        # ── Conversaciones viejas (reemplazadas por el talk) ──
        "game/script/characters/jasmine/interaction/conversacion_jasmine",
        "game/script/characters/monica/interaction/conversacion_monica",
        "game/script/characters/violet/interaction/conversacion_violet",
        "game/tl/english/script/characters/jasmine/interaction/conversacion_jasmine",
        "game/tl/english/script/characters/monica/interaction/conversacion_monica",
        "game/tl/english/script/characters/violet/interaction/conversacion_violet",
        # ── Quests de Violet renumeradas / partidas ──
        "game/script/characters/violet/quests/violet_quest_05",
        "game/script/characters/violet/quests/violet_quest_06",
        "game/script/characters/violet/quests/violet_quest_08",
        "game/script/characters/violet/quests/violet_quest_09",
        "game/script/characters/violet/quests/violet_quest_11",
        "game/script/characters/violet/quests/violet_quest_12",
        "game/tl/english/script/characters/violet/quests/violet_quest_04",
        "game/tl/english/script/characters/violet/quests/violet_quest_06",
        "game/tl/english/script/characters/violet/quests/violet_quest_07",
        "game/tl/english/script/characters/violet/quests/violet_quest_08",
        "game/tl/english/script/characters/violet/quests/violet_quest_09",
        "game/tl/english/script/characters/violet/quests/violet_quest_11",
        "game/tl/english/script/characters/violet/quests/violet_quest_12",
        # ── Lineas de amor/deseo, primera version ──
        "game/script/characters/violet/amor/violet_amor_labels",
        "game/script/characters/violet/deseo/violet_deseo_labels",
        "game/tl/english/script/characters/violet/amor/violet_amor_labels",
        "game/tl/english/script/characters/violet/deseo/violet_deseo_labels",
        # ── Ventajas y espiar ──
        "game/script/characters/violet/ventajas/mensajear/mv_aburrida",
        "game/tl/english/script/characters/violet/interaction/espiar_violet",
        "game/script/core/shopping/usar_casco_vr",
        # ── HUD: relaciones → hitos, tracker, tutorial de exploracion ──
        "game/tl/english/script/ui/hud/hud_relaciones",      # el de Sentry cabeccb7
        "game/tl/english/script/ui/hud/hud_tracker",
        "game/tl/english/tutorial_exploracion_strings",
    ]

    def _jp_limpiar_instalacion():
        """
        Borra los archivos de versiones viejas que hayan quedado en disco.
        Devuelve la lista de los borrados. Nunca tira: si un borrado falla
        (permisos), se saltea y el juego sigue como pudo.
        """
        if config.developer:
            return []
        if renpy.emscripten or renpy.mobile or renpy.macapp:
            return []
        borrados = []
        for _rel in JP_ARCHIVOS_VERSIONES_VIEJAS:
            for _ext in (".rpy", ".rpyc"):
                _ruta = _li_os.path.join(config.basedir, *(_rel + _ext).split("/"))
                if not _li_os.path.isfile(_ruta):
                    continue
                try:
                    _li_os.remove(_ruta)
                    borrados.append(_rel + _ext)
                except Exception as _e:
                    try:
                        renpy.display.log.write("[limpieza] no se pudo borrar %s: %r" % (_ruta, _e))
                    except Exception:
                        pass
        return borrados

    _jp_li_borrados = _jp_limpiar_instalacion()
    if _jp_li_borrados:
        try:
            # El literal NO va solo en su linea: el detector de `%` sueltos de
            # validar_traducciones.py lee una linea que es solo un string como
            # si fuera dialogo, y lo marcaria como crash.
            renpy.display.log.write("[limpieza] %d archivo(s) de una version "
                                    "anterior borrados; reinicio: %s" % (
                                        len(_jp_li_borrados),
                                        ", ".join(_jp_li_borrados)))
        except Exception:
            pass
        # Todo el script ya esta cargado en memoria, con los archivos viejos
        # adentro: hay que volver a cargar desde cero. UtterRestartException
        # la atrapa bootstrap.py y reinicia Ren'Py completo. Solo se reinicia
        # si se borro algo, asi que no puede quedar en bucle.
        renpy.utter_restart()
