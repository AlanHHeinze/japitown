################################################################################
## Menú de Cheats
################################################################################

init python:
    def cheat_violet_al_bano():
        """Fuerza a Violet al baño para testear el minijuego de espiar."""
        # Guardar rutina original si no está guardada
        if not hasattr(store, '_cheat_violet_rutina_original'):
            store._cheat_violet_rutina_original = {}

        violet = obtener_npc("violet")
        horario = store.horario_actual

        # Guardar rutina actual de este horario si no la tenemos
        if horario not in store._cheat_violet_rutina_original:
            store._cheat_violet_rutina_original[horario] = violet.locacion_actual

        # Forzar a Violet al baño
        violet.locacion_actual = "casa_banioarriba"

        # Mensaje de confirmación
        renpy.show_screen("say", who=None, what="Violet está en el baño ahora (cheat activado).")

    def cheat_violet_restaurar():
        """Restaura la rutina original de Violet."""
        if hasattr(store, '_cheat_violet_rutina_original'):
            violet = obtener_npc("violet")
            horario = store.horario_actual

            if horario in store._cheat_violet_rutina_original:
                violet.locacion_actual = store._cheat_violet_rutina_original[horario]
                # Limpiar el registro para este horario
                del store._cheat_violet_rutina_original[horario]
                renpy.show_screen("say", who=None, what="Rutina de Violet restaurada.")
            else:
                renpy.show_screen("say", who=None, what="No hay rutina original guardada para este horario.")

screen menu_cheats():
    """Menú de cheats — App Cheats"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("menu_cheats") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("menu_cheats")

    # Frame constrainido al area del celular
    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            # Barra de estado
            use _celular_barra_status("menu_cheats")

            # Header de app
            use _celular_app_header("Cheats", "⚡", [Hide("menu_cheats"), Show("menu_celular")], "menu_cheats")

            # Contenido scrollable
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (int(12 * _k), int(10 * _k))

                    vbox:
                        spacing int(12 * _k)
                        xfill True

                        # ── Tests de quests (saltar directo al contenido) ──
                        text "TESTEO DE QUESTS" size int(12 * _k) color "#4FC3F7" bold True

                        button:
                            xfill True
                            background "#4a1e3aCC"
                            hover_background "#6a2a50CC"
                            padding (int(12 * _k), int(10 * _k))
                            action [
                                Hide("menu_cheats"),
                                SetVariable("menu_celular_abierto", False),
                                Hide("menu_celular"),
                                Jump("test_quest06a_violet")
                            ]

                            text "🧪 Quest 06_a Violet" size int(14 * _k) color "#FFD54F" bold True

                        button:
                            xfill True
                            background "#4a1e3aCC"
                            hover_background "#6a2a50CC"
                            padding (int(12 * _k), int(10 * _k))
                            action [
                                Hide("menu_cheats"),
                                SetVariable("menu_celular_abierto", False),
                                Hide("menu_celular"),
                                Jump("test_quest08a_violet")
                            ]

                            text "🧪 Quest 08_a Violet" size int(14 * _k) color "#FFD54F" bold True

                        # ── Test de sistema: forzar un error para probar Sentry ──
                        text "TESTEO DE SISTEMA" size int(12 * _k) color "#4FC3F7" bold True

                        button:
                            xfill True
                            background "#5a1e1eCC"
                            hover_background "#7a2a2aCC"
                            padding (int(12 * _k), int(10 * _k))
                            action [
                                Hide("menu_cheats"),
                                SetVariable("menu_celular_abierto", False),
                                Hide("menu_celular"),
                                Function(jp_forzar_error_prueba)
                            ]

                            text "💥 Forzar error (test Sentry)" size int(14 * _k) color "#ff8888" bold True

                        # Testeo del minijuego de espiar
                        button:
                            xfill True
                            background "#3a2a5aCC"
                            hover_background "#5a3a7aCC"
                            padding (int(12 * _k), int(10 * _k))
                            action Function(cheat_violet_al_bano)

                            text "🚿 Violet al baño (minijuego)" size int(14 * _k) color "#FFB74D" bold True

                        button:
                            xfill True
                            background "#3a2a5aCC"
                            hover_background "#5a3a7aCC"
                            padding (int(12 * _k), int(10 * _k))
                            action Function(cheat_violet_restaurar)

                            text "↩️ Restaurar rutina Violet" size int(14 * _k) color "#FFB74D" bold True

                        # Diagnóstico de "cannot pickle X" al guardar: lista los
                        # objetos del estado que no se pueden serializar y por
                        # qué camino se llega a ellos (diagnostico_guardado.rpy).
                        button:
                            xfill True
                            background "#1e3a5aCC"
                            hover_background "#2a4a7aCC"
                            padding (int(12 * _k), int(10 * _k))
                            action Function(jp_reportar_no_picklables)

                            text "🔍 Revisar guardado (no picklables)" size int(14 * _k) color "#88ccff" bold True

                        # Repara una partida donde una variable del store tapó un
                        # builtin (ej. escribir `int = 5` en la consola), que hace
                        # crashear el HUD entero. Ver builtins_pisados.rpy.
                        button:
                            xfill True
                            background "#1e3a5aCC"
                            hover_background "#2a4a7aCC"
                            padding (int(12 * _k), int(10 * _k))
                            action Function(jp_limpiar_builtins_pisados)

                            text "🧹 Limpiar builtins pisados" size int(14 * _k) color "#88ccff" bold True

                        # Toggle de recompensas
                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (int(12 * _k), int(10 * _k))

                            hbox:
                                spacing int(10 * _k)
                                yalign 0.5
                                xfill True
                                text "Ver resultados Talk:" size int(13 * _k) color "#ffffff" bold True yalign 0.5

                                if getattr(persistent, "mostrar_recompensa", False):
                                    textbutton "ON":
                                        action ToggleField(persistent, "mostrar_recompensa", True, False)
                                        style "cheat_button"
                                        xalign 1.0
                                else:
                                    textbutton "OFF":
                                        action ToggleField(persistent, "mostrar_recompensa", True, False)
                                        style "cheat_button"
                                        xalign 1.0

                        # Toggle de botones de movimiento visibles
                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (int(12 * _k), int(10 * _k))

                            hbox:
                                spacing int(10 * _k)
                                yalign 0.5
                                xfill True
                                text "Botones de movimiento:" size int(13 * _k) color "#ffffff" bold True yalign 0.5

                                if getattr(persistent, "hotspots_visibles", True):
                                    textbutton "ON":
                                        action ToggleField(persistent, "hotspots_visibles", True, False)
                                        style "cheat_button"
                                        xalign 1.0
                                else:
                                    textbutton "OFF":
                                        action ToggleField(persistent, "hotspots_visibles", True, False)
                                        style "cheat_button"
                                        xalign 1.0

                        # Separador NPCs
                        text "NPC STATS" size int(12 * _k) color "#4FC3F7" bold True

                        # Mónica
                        $ monica = obtener_npc("monica")
                        if monica:
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(12 * _k), int(10 * _k))

                                vbox:
                                    spacing int(8 * _k)
                                    xfill True

                                    text "[monica.nombre]" size int(15 * _k) color "#ffffff" bold True

                                    hbox:
                                        spacing int(8 * _k)
                                        yalign 0.5
                                        text "❤️ Amor: [monica.estado['amor']]" size int(12 * _k) color "#00ff00"
                                        textbutton "+1" action Function(monica.modificar_stat1, 1) style "cheat_button"
                                        textbutton "-1" action Function(monica.modificar_stat1, -1) style "cheat_button"
                                        textbutton "Max" action Function(monica.establecer_stat1, 100) style "cheat_button"
                                        textbutton "0" action Function(monica.establecer_stat1, 0) style "cheat_button"

                                    hbox:
                                        spacing int(8 * _k)
                                        yalign 0.5
                                        text "💋 Deseo: [monica.estado['deseo']]" size int(12 * _k) color "#ff69b4"
                                        textbutton "+1" action Function(monica.modificar_stat2, 1) style "cheat_button"
                                        textbutton "-1" action Function(monica.modificar_stat2, -1) style "cheat_button"
                                        textbutton "Max" action Function(monica.establecer_stat2, 100) style "cheat_button"
                                        textbutton "0" action Function(monica.establecer_stat2, 0) style "cheat_button"

                        # Jasmine
                        $ jasmine = obtener_npc("jasmine")
                        if jasmine:
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(12 * _k), int(10 * _k))

                                vbox:
                                    spacing int(8 * _k)
                                    xfill True

                                    text "[jasmine.nombre]" size int(15 * _k) color "#ffffff" bold True

                                    hbox:
                                        spacing int(8 * _k)
                                        yalign 0.5
                                        text "❤️ Amor: [jasmine.estado['amor']]" size int(12 * _k) color "#00ff00"
                                        textbutton "+1" action Function(jasmine.modificar_stat1, 1) style "cheat_button"
                                        textbutton "-1" action Function(jasmine.modificar_stat1, -1) style "cheat_button"
                                        textbutton "Max" action Function(jasmine.establecer_stat1, 100) style "cheat_button"
                                        textbutton "0" action Function(jasmine.establecer_stat1, 0) style "cheat_button"

                                    hbox:
                                        spacing int(8 * _k)
                                        yalign 0.5
                                        text "💋 Deseo: [jasmine.estado['deseo']]" size int(12 * _k) color "#ff69b4"
                                        textbutton "+1" action Function(jasmine.modificar_stat2, 1) style "cheat_button"
                                        textbutton "-1" action Function(jasmine.modificar_stat2, -1) style "cheat_button"
                                        textbutton "Max" action Function(jasmine.establecer_stat2, 100) style "cheat_button"
                                        textbutton "0" action Function(jasmine.establecer_stat2, 0) style "cheat_button"

                        # Violet
                        $ violet = obtener_npc("violet")
                        if violet:
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(12 * _k), int(10 * _k))

                                vbox:
                                    spacing int(8 * _k)
                                    xfill True

                                    text "[violet.nombre]" size int(15 * _k) color "#ffffff" bold True

                                    hbox:
                                        spacing int(8 * _k)
                                        yalign 0.5
                                        text "❤️ Amor: [violet.estado['amor']]" size int(12 * _k) color "#00ff00"
                                        textbutton "+1" action Function(violet.modificar_stat1, 1) style "cheat_button"
                                        textbutton "-1" action Function(violet.modificar_stat1, -1) style "cheat_button"
                                        textbutton "Max" action Function(violet.establecer_stat1, 100) style "cheat_button"
                                        textbutton "0" action Function(violet.establecer_stat1, 0) style "cheat_button"

                                    hbox:
                                        spacing int(8 * _k)
                                        yalign 0.5
                                        text "💋 Deseo: [violet.estado['deseo']]" size int(12 * _k) color "#ff69b4"
                                        textbutton "+1" action Function(violet.modificar_stat2, 1) style "cheat_button"
                                        textbutton "-1" action Function(violet.modificar_stat2, -1) style "cheat_button"
                                        textbutton "Max" action Function(violet.establecer_stat2, 100) style "cheat_button"
                                        textbutton "0" action Function(violet.establecer_stat2, 0) style "cheat_button"

                        # Separador MC stats
                        frame:
                            xfill True
                            ysize int(1 * _k)
                            background "#ffffff11"

                        text "STATS DEL MC" size int(12 * _k) color "#4FC3F7" bold True

                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (int(12 * _k), int(10 * _k))

                            vbox:
                                spacing int(8 * _k)
                                xfill True

                                hbox:
                                    spacing int(8 * _k)
                                    yalign 0.5
                                    text "💪 Fuerza: [mc_fuerza]" size int(12 * _k) color "#FF6B6B"
                                    textbutton "+1" action Function(modificar_stat, "fuerza", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "fuerza", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "fuerza", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_fuerza", 0) style "cheat_button"

                                hbox:
                                    spacing int(8 * _k)
                                    yalign 0.5
                                    text "💬 Carisma: [mc_carisma]" size int(12 * _k) color "#FFB74D"
                                    textbutton "+1" action Function(modificar_stat, "carisma", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "carisma", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "carisma", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_carisma", 0) style "cheat_button"

                                hbox:
                                    spacing int(8 * _k)
                                    yalign 0.5
                                    text "🎯 Destreza: [mc_destreza]" size int(12 * _k) color "#4FC3F7"
                                    textbutton "+1" action Function(modificar_stat, "destreza", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "destreza", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "destreza", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_destreza", 0) style "cheat_button"

                                hbox:
                                    spacing int(8 * _k)
                                    yalign 0.5
                                    text "🧠 Inteligencia: [mc_inteligencia]" size int(12 * _k) color "#81C784"
                                    textbutton "+1" action Function(modificar_stat, "inteligencia", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "inteligencia", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "inteligencia", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_inteligencia", 0) style "cheat_button"

                                hbox:
                                    spacing int(8 * _k)
                                    yalign 0.5
                                    text "💰 Dinero: $[dinero]" size int(12 * _k) color "#4CAF50"
                                    textbutton "+100" action SetVariable("dinero", dinero + 100) style "cheat_button"
                                    textbutton "-100" action SetVariable("dinero", max(0, dinero - 100)) style "cheat_button"
                                    textbutton "+1k" action SetVariable("dinero", dinero + 1000) style "cheat_button"
                                    textbutton "100" action SetVariable("dinero", 100) style "cheat_button"

################################################################################
## Screen de Completar Quests (herramienta de testeo)
################################################################################

init python:

    def forzar_completar_quest(quest_id):
        """Fuerza la completación de una quest sin importar su estado."""
        quest = sistema_quests.obtener_quest(quest_id)
        if quest and not quest.completada:
            # Si no estaba activa, activarla primero para que la cadena funcione
            if not quest.activa:
                quest.activa = True
                quest.dia_inicio = getattr(store, 'dias_totales', 1)

            quest.completar()

screen menu_completar_quests():
    """Completar Quests — App Cheats"""

    modal True

    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("menu_completar_quests")

    # Frame constrainido al area del celular
    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            # Barra de estado
            use _celular_barra_status("menu_completar_quests")

            # Header de app
            use _celular_app_header("Completar Quests", "🏆", [Hide("menu_completar_quests"), Show("menu_cheats")], "menu_completar_quests")

            # Contenedor scrollable
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (int(12 * _k), int(10 * _k))

                    vbox:
                        spacing int(10 * _k)
                        xfill True

                        # Iterar por NPC
                        for _npc_id_cq in ["violet", "jasmine", "monica"]:
                            $ _quests_npc_cq = sistema_quests.obtener_quests_npc(_npc_id_cq)
                            if _quests_npc_cq:
                                frame:
                                    xfill True
                                    background "#1e1e3aCC"
                                    padding (int(12 * _k), int(10 * _k))

                                    vbox:
                                        spacing int(8 * _k)
                                        xfill True

                                        text "[_npc_id_cq!c]" size int(15 * _k) color "#ffffff" bold True

                                        for _q_cq in _quests_npc_cq:
                                            hbox:
                                                spacing int(8 * _k)
                                                yalign 0.5
                                                xfill True

                                                # Indicador de estado
                                                if _q_cq.completada:
                                                    text "✅" size int(14 * _k) yalign 0.5
                                                elif _q_cq.activa:
                                                    text "🔶" size int(14 * _k) yalign 0.5
                                                else:
                                                    text "⬜" size int(14 * _k) yalign 0.5

                                                # Nombre y estado
                                                vbox:
                                                    text "[_q_cq.nombre]" size int(13 * _k) color "#ffffff"
                                                    if _q_cq.completada:
                                                        text "Completada" size int(11 * _k) color "#4CAF50"
                                                    elif _q_cq.activa:
                                                        text "Activa - Etapa [_q_cq.etapa_actual]" size int(11 * _k) color "#FFB74D"
                                                    else:
                                                        text "Pendiente" size int(11 * _k) color "#888888"

                                                # Botón completar
                                                if not _q_cq.completada:
                                                    textbutton "Completar":
                                                        action [Function(forzar_completar_quest, _q_cq.id), renpy.restart_interaction]
                                                        style "cheat_button"
                                                        yalign 0.5

################################################################################
## Estilos para botones de cheats
################################################################################
## Escalados en pantalla táctil: CEL_APP_ESCALA_SMALL se evalúa una sola vez,
## al declarar el estilo, y renpy.variant() ya es estable en ese momento
## (definido antes de que arranque el juego) — igual criterio que los
## "default ajuste_cel_area_*" de ajuste_celular.rpy.

style cheat_button is button:
    background "#4a4a00"
    hover_background "#6a6a00"
    padding ((int(8 * CEL_APP_ESCALA_SMALL), int(5 * CEL_APP_ESCALA_SMALL)) if renpy.variant("small") else (8, 5))
    xsize (int(80 * CEL_APP_ESCALA_SMALL) if renpy.variant("small") else 80)

style cheat_button_text is button_text:
    size (int(14 * CEL_APP_ESCALA_SMALL) if renpy.variant("small") else 14)
    color "#ffff00"
    hover_color "#ffffff"
    xalign 0.5
