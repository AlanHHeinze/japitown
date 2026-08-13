################################################################################
## Autosave: solo el de dormir
################################################################################
## El juego autoguarda UNICAMENTE al dormir (ver autoguardar_partida() en
## core/time/timesystem_core.rpy), para que los 10 slots sean un historial de
## dias y el jugador sepa siempre cual cargar para seguir.
##
## Apagar config.autosave_frequency / autosave_on_choice / autosave_on_input
## (options.rpy) NO alcanza: hay disparadores del motor que llaman a
## force_autosave() DIRECTAMENTE, sin mirar ninguno de esos flags —
##   - 00layout.rpy:77 y :86      → prompts de si/no (salir, ir al menu, cargar)
##   - 00action_menu.rpy:233,:269 → acciones MainMenu / Quit
##   - 00action_file.rpy:495      → maquinaria de guardar/cargar
## y lo unico que chequean es config.has_autosave, que tiene que quedar en True
## porque de el depende el autoguardado al dormir (loadsave.py:325).
##
## Solucion: se pisa force_autosave con una version que descarta todo, y
## autoguardar_partida() se guarda una referencia a la ORIGINAL y llama a esa.
## Asi el unico camino que realmente guarda es el del dormir, por construccion:
## no hay flag global que pueda quedar mal seteado si algo falla a mitad.

init -50 python:

    def _jp_autosave_descartado(take_screenshot=False, block=False):
        """
        Reemplazo de force_autosave: no guarda nada.

        Mantiene la firma de la original (loadsave.py:309) porque los llamadores
        del motor pasan tanto posicional (force_autosave(True)) como por nombre.
        """
        if config.developer:
            print("[Autosave] descartado: disparador del motor, no es el de dormir")
        return

    # Marca para reconocer la version ya pisada (ver el guard de abajo)
    _jp_autosave_descartado._jp_filtrado = True

    # Guardar la ORIGINAL una sola vez, COMO ATRIBUTO DEL MODULO renpy.loadsave
    # y no como variable del store.
    #
    # Por que no en el store (bug real, 2026-08-11 — NameError al dormir):
    # un reload de Ren'Py (Shift+R en desarrollo) arranca un store NUEVO pero NO
    # recarga los modulos de Python. Entonces en el segundo init
    # renpy.loadsave.force_autosave ya era la version pisada, el guard daba
    # False, y la variable del store nunca se volvia a crear: al dormir,
    # autoguardar_partida() reventaba con NameError.
    #
    # En el modulo el valor sobrevive a los reloads, y el hasattr garantiza que
    # se capture la ORIGINAL una unica vez por proceso — que es justo lo que el
    # guard viejo intentaba proteger.
    if not hasattr(renpy.loadsave, "_jp_force_autosave_real"):
        renpy.loadsave._jp_force_autosave_real = renpy.loadsave.force_autosave

    # Hay que pisar las DOS rutas: renpy.force_autosave es una referencia
    # importada en exports/__init__.py:194, asi que pisar solo renpy.loadsave
    # dejaria pasar a los llamadores que usan el export (00layout, 00action_menu)
    # y viceversa. Cada modulo resolvio su referencia por separado.
    renpy.loadsave.force_autosave = _jp_autosave_descartado
    renpy.force_autosave = _jp_autosave_descartado
