################################################################################
## Menú de Interacción con NPCs - Versión 2.0
################################################################################
## Menú completo con sprite de NPC

################################################################################
## Screen Principal de Interacción
################################################################################

screen menu_interaccion_npc_completo(npc, opciones_extra=None):
    """
    Menú completo de interacción con NPC.
    Muestra background actual, sprite del NPC a la derecha, y menú al centro.
    """
    
    modal True
    
    # Fondo con el background actual de la locación
    $ _bg_actual = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#000000"
    add _bg_actual
    
    # Overlay semi-transparente
    add Solid("#00000088")
    
    # Sprite del NPC a la derecha (usando skin base activo o default)
    $ _sprite_menu = obtener_sprite_menu_npc(npc.id)
    if _sprite_menu:
        add _sprite_menu:
            xalign 0.85
            yalign 1.0
    
    # Escala x2 en pantalla táctil, y el menú se corre a la izquierda para no
    # tapar el sprite del NPC (anclado a la derecha, xalign 0.85).
    $ _mi_k = 2.0 if renpy.variant("small") else 1.0
    $ _mi_xalign = 0.28 if renpy.variant("small") else 0.5

    # Menú de opciones
    frame:
        xalign _mi_xalign
        yalign 0.5
        background "#0288D1EE"
        padding (int(30 * _mi_k), int(20 * _mi_k))

        vbox:
            spacing int(15 * _mi_k)

            # Título con nombre del NPC
            text "[npc.nombre]" size int(32 * _mi_k) color "#FFF8E1" bold True xalign 0.5 outlines [(int(2 * _mi_k), "#1565C0", 0, 0)]

            # Línea separadora
            null height int(5 * _mi_k)
            frame:
                xsize int(300 * _mi_k)
                ysize int(2 * _mi_k)
                background "#4FC3F7"
            null height int(5 * _mi_k)

            # Informacion del NPC
            $ _emojis = {"stat1": "❤️", "stat2": "💋"}

            vbox:
                spacing int(5 * _mi_k)
                xalign 0.5

                # Stats individuales con emojis
                hbox:
                    spacing int(20 * _mi_k)
                    xalign 0.5

                    hbox:
                        spacing int(4 * _mi_k)
                        text "[_emojis['stat1']]" size int(16 * _mi_k)
                        text "[npc.estado[npc.nombre_stat1]]" size int(14 * _mi_k) color "#66BB6A" bold True

                    hbox:
                        spacing int(4 * _mi_k)
                        text "[_emojis['stat2']]" size int(16 * _mi_k)
                        text "[npc.estado[npc.nombre_stat2]]" size int(14 * _mi_k) color "#FFB74D" bold True

            null height int(10 * _mi_k)

            # Opciones de interacción — orden fijo: Quest, Evento, Hablar.
            # Se arma UNA lista ya ordenada y filtrada por condición, y se recorre
            # en un solo vbox: así, si una opción no está disponible, la siguiente
            # sube de lugar en vez de dejar un hueco vacío.
            $ _opciones_quest = [o for o in (opciones_extra or []) if o.get("condicion", True) and o.get("tipo") != "evento"]
            $ _opciones_evento = [o for o in (opciones_extra or []) if o.get("condicion", True) and o.get("tipo") == "evento"]
            $ _opciones_ordenadas = _opciones_quest + _opciones_evento
            $ puede_hablar = npc.puede_interactuar("hablar") if hablar_desbloqueado else False

            vbox:
                spacing int(10 * _mi_k)
                xsize int(300 * _mi_k)

                # 1. Quest, luego 2. Evento (mismo estilo, orden ya resuelto arriba)
                for opcion in _opciones_ordenadas:
                    # El texto se COMPONE (opcion + tag), asi que hay que traducir
                    # cada parte por separado: el string ya concatenado nunca
                    # matchearia un `old`. Mismo criterio que en door_access_system.
                    $ _tag_extra = tag_opcion_quest(opcion.get("label"), opcion.get("tipo") == "evento")
                    $ _texto_extra = renpy.translate_string(opcion.get("texto", "Opción")) + _tag_extra
                    button:
                        xfill True
                        background "#009688"
                        hover_background "#4DB6AC"
                        padding (int(15 * _mi_k), int(10 * _mi_k))
                        action [Hide("menu_interaccion_npc_completo"),
                                Return(("opcion_especial", opcion.get("label", "game_loop")))]

                        text "[_texto_extra]" size int(18 * _mi_k) color "#ffffff"

                # 3. Hablar — siempre al final, oculta hasta completar la quest 0_a de Violet
                if hablar_desbloqueado:
                    if _opciones_ordenadas:
                        null height int(5 * _mi_k)
                        frame:
                            xfill True
                            ysize int(1 * _mi_k)
                            background "#00968844"
                        null height int(5 * _mi_k)

                    if puede_hablar:
                        button:
                            xfill True
                            background "#1565C0"
                            hover_background "#FFB74D"
                            padding (int(15 * _mi_k), int(10 * _mi_k))
                            # Return, NO Call: este screen se muestra con
                            # `call screen`, que solo cierra su frame cuando
                            # recibe un Return. Saliendo con Call(...) el frame
                            # quedaba abierto para siempre — y como "Hablar" es
                            # de lo más usado del juego, el call stack crecía
                            # toda la partida (tracebacks enormes que además
                            # apuntaban a interacciones viejas). Se devuelve el
                            # label igual que las opciones extra de arriba; el
                            # caller hace `jump expression` e interaccion_hablar
                            # cierra con return.
                            action [SetVariable("_npc_id_temp", npc.id),
                                    Hide("menu_interaccion_npc_completo"),
                                    Return(("opcion_especial", "interaccion_hablar"))]

                            text "💬 Hablar" size int(20 * _mi_k) color "#ffffff"
                    else:
                        button:
                            xfill True
                            background "#444444"
                            padding (int(15 * _mi_k), int(10 * _mi_k))
                            action None

                            hbox:
                                spacing int(10 * _mi_k)
                                text "💬 Hablar" size int(20 * _mi_k) color "#666666"
                                text "(ya hecho hoy)" size int(16 * _mi_k) color "#ff6666" italic True

            null height int(10 * _mi_k)

            # Botón cerrar
            textbutton "Cerrar":
                xalign 0.5
                action Hide("menu_interaccion_npc_completo")
                text_size int(20 * _mi_k)
                text_color "#FFF8E1"


################################################################################
## Screen de estadísticas de NPCs (sin cambios)
################################################################################

screen estadisticas_npcs():
    """Estadísticas de relaciones — App Relaciones"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("estadisticas_npcs") if modo_ajuste_celular else None

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("estadisticas_npcs")

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
            use _celular_barra_status("estadisticas_npcs")

            # Header de app
            use _celular_app_header("Relaciones", "📊", [Hide("estadisticas_npcs"), Show("menu_celular")], "estadisticas_npcs")

            # Contenido
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True

                frame:
                    xfill True
                    background None
                    padding (15, 10)

                    vbox:
                        spacing 20
                        xfill True

                        # Mónica
                        $ monica = obtener_npc("monica")
                        if monica:
                            use _npc_stat_card(monica)

                        # Jasmine
                        $ jasmine = obtener_npc("jasmine")
                        if jasmine:
                            use _npc_stat_card(jasmine)

                        # Violet
                        $ violet = obtener_npc("violet")
                        if violet:
                            use _npc_stat_card(violet)


screen _npc_stat_card(npc):
    $ _emojis = {"stat1": "❤️", "stat2": "💋"}
    $ _stat1_val = npc.estado.get(npc.nombre_stat1, 0)
    $ _stat2_val = npc.estado.get(npc.nombre_stat2, 0)

    frame:
        xfill True
        background "#1e1e3aCC"
        padding (30, 24)

        vbox:
            spacing 10
            xfill True

            hbox:
                spacing 20
                yalign 0.5
                # Icon
                $ _icon_path_rel = "images/hud/pista_{}.png".format(npc.id)
                frame:
                    xysize (72, 72)
                    background "#3a3a5aCC"
                    yalign 0.5

                    if renpy.loadable(_icon_path_rel):
                        add _icon_path_rel zoom 0.28 xalign 0.5 yalign 0.5
                    else:
                        text "👤" size 36 xalign 0.5 yalign 0.5

                vbox:
                    spacing 4
                    text "[npc.nombre]" size 30 color "#ffffff" bold True

            hbox:
                spacing 30
                xoffset 92
                hbox:
                    spacing 8
                    text "[_emojis['stat1']]" size 32
                    text "[_stat1_val]" size 28 color "#66BB6A" bold True
                hbox:
                    spacing 8
                    text "[_emojis['stat2']]" size 32
                    text "[_stat2_val]" size 28 color "#FFB74D" bold True


################################################################################
## Estilos
################################################################################

style empty_button:
    background None
    hover_background None
