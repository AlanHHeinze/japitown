################################################################################
## Menú de Cheats
################################################################################

screen menu_cheats():
    """Menú de cheats — App Cheats"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("menu_cheats") if modo_ajuste_celular else None

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header de app
            use _celular_app_header("Cheats", "⚡", [Hide("menu_cheats"), Show("menu_celular")])

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
                    padding (12, 10)

                    vbox:
                        spacing 12
                        xfill True

                        # Toggle de recompensas
                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (12, 10)

                            hbox:
                                spacing 10
                                yalign 0.5
                                xfill True
                                text "Ver resultados Talk:" size 13 color "#ffffff" bold True yalign 0.5

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

                        # Separador NPCs
                        text "NPC STATS" size 12 color "#4FC3F7" bold True

                        # Mónica
                        $ monica = obtener_npc("monica")
                        if monica:
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (12, 10)

                                vbox:
                                    spacing 8
                                    xfill True

                                    text "[monica.nombre]" size 15 color "#ffffff" bold True

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "❤️ Amor: [monica.estado['amor']]" size 12 color "#00ff00"
                                        textbutton "+1" action Function(monica.modificar_stat1, 1) style "cheat_button"
                                        textbutton "-1" action Function(monica.modificar_stat1, -1) style "cheat_button"
                                        textbutton "Max" action SetDict(monica.estado, "amor", 100) style "cheat_button"
                                        textbutton "0" action SetDict(monica.estado, "amor", 0) style "cheat_button"

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "💋 Deseo: [monica.estado['deseo']]" size 12 color "#ff69b4"
                                        textbutton "+1" action Function(monica.modificar_stat2, 1) style "cheat_button"
                                        textbutton "-1" action Function(monica.modificar_stat2, -1) style "cheat_button"
                                        textbutton "Max" action SetDict(monica.estado, "deseo", 100) style "cheat_button"
                                        textbutton "0" action SetDict(monica.estado, "deseo", 0) style "cheat_button"

                        # Jasmine
                        $ jasmine = obtener_npc("jasmine")
                        if jasmine:
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (12, 10)

                                vbox:
                                    spacing 8
                                    xfill True

                                    text "[jasmine.nombre]" size 15 color "#ffffff" bold True

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "❤️ Amor: [jasmine.estado['amor']]" size 12 color "#00ff00"
                                        textbutton "+1" action Function(jasmine.modificar_stat1, 1) style "cheat_button"
                                        textbutton "-1" action Function(jasmine.modificar_stat1, -1) style "cheat_button"
                                        textbutton "Max" action SetDict(jasmine.estado, "amor", 100) style "cheat_button"
                                        textbutton "0" action SetDict(jasmine.estado, "amor", 0) style "cheat_button"

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "💋 Deseo: [jasmine.estado['deseo']]" size 12 color "#ff69b4"
                                        textbutton "+1" action Function(jasmine.modificar_stat2, 1) style "cheat_button"
                                        textbutton "-1" action Function(jasmine.modificar_stat2, -1) style "cheat_button"
                                        textbutton "Max" action SetDict(jasmine.estado, "deseo", 100) style "cheat_button"
                                        textbutton "0" action SetDict(jasmine.estado, "deseo", 0) style "cheat_button"

                        # Violet
                        $ violet = obtener_npc("violet")
                        if violet:
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (12, 10)

                                vbox:
                                    spacing 8
                                    xfill True

                                    text "[violet.nombre]" size 15 color "#ffffff" bold True

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "❤️ Amor: [violet.estado['amor']]" size 12 color "#00ff00"
                                        textbutton "+1" action Function(violet.modificar_stat1, 1) style "cheat_button"
                                        textbutton "-1" action Function(violet.modificar_stat1, -1) style "cheat_button"
                                        textbutton "Max" action SetDict(violet.estado, "amor", 100) style "cheat_button"
                                        textbutton "0" action SetDict(violet.estado, "amor", 0) style "cheat_button"

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "💋 Deseo: [violet.estado['deseo']]" size 12 color "#ff69b4"
                                        textbutton "+1" action Function(violet.modificar_stat2, 1) style "cheat_button"
                                        textbutton "-1" action Function(violet.modificar_stat2, -1) style "cheat_button"
                                        textbutton "Max" action SetDict(violet.estado, "deseo", 100) style "cheat_button"
                                        textbutton "0" action SetDict(violet.estado, "deseo", 0) style "cheat_button"

                        # Separador MC stats
                        frame:
                            xfill True
                            ysize 1
                            background "#ffffff11"

                        text "STATS DEL MC" size 12 color "#4FC3F7" bold True

                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (12, 10)

                            vbox:
                                spacing 8
                                xfill True

                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "💪 Fuerza: [mc_fuerza]" size 12 color "#FF6B6B"
                                    textbutton "+1" action Function(modificar_stat, "fuerza", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "fuerza", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "fuerza", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_fuerza", 0) style "cheat_button"

                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "💬 Carisma: [mc_carisma]" size 12 color "#FFB74D"
                                    textbutton "+1" action Function(modificar_stat, "carisma", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "carisma", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "carisma", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_carisma", 0) style "cheat_button"

                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "🎯 Destreza: [mc_destreza]" size 12 color "#4FC3F7"
                                    textbutton "+1" action Function(modificar_stat, "destreza", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "destreza", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "destreza", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_destreza", 0) style "cheat_button"

                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "🧠 Inteligencia: [mc_inteligencia]" size 12 color "#81C784"
                                    textbutton "+1" action Function(modificar_stat, "inteligencia", 1) style "cheat_button"
                                    textbutton "-1" action Function(modificar_stat, "inteligencia", -1) style "cheat_button"
                                    textbutton "+10" action Function(modificar_stat, "inteligencia", 10) style "cheat_button"
                                    textbutton "0" action SetVariable("mc_inteligencia", 0) style "cheat_button"

                                hbox:
                                    spacing 8
                                    yalign 0.5
                                    text "💰 Dinero: $[dinero]" size 12 color "#4CAF50"
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

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header de app
            use _celular_app_header("Completar Quests", "🏆", [Hide("menu_completar_quests"), Show("menu_cheats")])

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
                    padding (12, 10)

                    vbox:
                        spacing 10
                        xfill True

                        # Iterar por NPC
                        for _npc_id_cq in ["violet", "jasmine", "monica"]:
                            $ _quests_npc_cq = sistema_quests.obtener_quests_npc(_npc_id_cq)
                            if _quests_npc_cq:
                                frame:
                                    xfill True
                                    background "#1e1e3aCC"
                                    padding (12, 10)

                                    vbox:
                                        spacing 8
                                        xfill True

                                        text "[_npc_id_cq!c]" size 15 color "#ffffff" bold True

                                        for _q_cq in _quests_npc_cq:
                                            hbox:
                                                spacing 8
                                                yalign 0.5
                                                xfill True

                                                # Indicador de estado
                                                if _q_cq.completada:
                                                    text "✅" size 14 yalign 0.5
                                                elif _q_cq.activa:
                                                    text "🔶" size 14 yalign 0.5
                                                else:
                                                    text "⬜" size 14 yalign 0.5

                                                # Nombre y estado
                                                vbox:
                                                    text "[_q_cq.nombre]" size 13 color "#ffffff"
                                                    if _q_cq.completada:
                                                        text "Completada" size 11 color "#4CAF50"
                                                    elif _q_cq.activa:
                                                        text "Activa - Etapa [_q_cq.etapa_actual]" size 11 color "#FFB74D"
                                                    else:
                                                        text "Pendiente" size 11 color "#888888"

                                                # Botón completar
                                                if not _q_cq.completada:
                                                    textbutton "Completar":
                                                        action [Function(forzar_completar_quest, _q_cq.id), renpy.restart_interaction]
                                                        style "cheat_button"
                                                        yalign 0.5

################################################################################
## Estilos para botones de cheats
################################################################################

style cheat_button is button:
    background "#4a4a00"
    hover_background "#6a6a00"
    padding (8, 5)
    xsize 80
    
style cheat_button_text is button_text:
    size 14
    color "#ffff00"
    hover_color "#ffffff"
    xalign 0.5
