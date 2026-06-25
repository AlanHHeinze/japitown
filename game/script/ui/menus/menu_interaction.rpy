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
    
    # Menú de opciones - Centro izquierda
    frame:
        xalign 0.25
        yalign 0.5
        background "#0288D1EE"
        padding (30, 20)
        
        vbox:
            spacing 15
            
            # Título con nombre del NPC
            text "[npc.nombre]" size 32 color "#FFF8E1" bold True xalign 0.5 outlines [(2, "#1565C0", 0, 0)]
            
            # Línea separadora
            null height 5
            frame:
                xsize 300
                ysize 2
                background "#4FC3F7"
            null height 5
            
            # Informacion del NPC
            $ _emojis = {"stat1": "❤️", "stat2": "💋"}

            vbox:
                spacing 5
                xalign 0.5

                # Stats individuales con emojis
                hbox:
                    spacing 20
                    xalign 0.5

                    hbox:
                        spacing 4
                        text "[_emojis['stat1']]" size 16
                        text "[npc.estado[npc.nombre_stat1]]" size 14 color "#66BB6A" bold True

                    hbox:
                        spacing 4
                        text "[_emojis['stat2']]" size 16
                        text "[npc.estado[npc.nombre_stat2]]" size 14 color "#FFB74D" bold True
            
            null height 10
            
            # Opciones de interacción
            vbox:
                spacing 10
                xsize 300
                
                # Opción: Hablar — oculta hasta completar la quest 0_a de Violet
                if hablar_desbloqueado:
                    $ puede_hablar = npc.puede_interactuar("hablar")

                    if puede_hablar:
                        button:
                            xfill True
                            background "#1565C0"
                            hover_background "#FFB74D"
                            padding (15, 10)
                            action [SetVariable("_npc_id_temp", npc.id),
                                    Hide("menu_interaccion_npc_completo"),
                                    Call("interaccion_hablar")]

                            text "💬 Hablar" size 20 color "#ffffff"
                    else:
                        button:
                            xfill True
                            background "#444444"
                            padding (15, 10)
                            action None

                            hbox:
                                spacing 10
                                text "💬 Hablar" size 20 color "#666666"
                                text "(ya hecho hoy)" size 16 color "#ff6666" italic True
                
                # =====================================================================
                # OPCIONES EXTRA (de eventos completados, etc.)
                # =====================================================================
                
                if opciones_extra:
                    null height 5
                    frame:
                        xfill True
                        ysize 1
                        background "#00968844"
                    null height 5
                    
                    for opcion in opciones_extra:
                        if opcion.get("condicion", True):
                            $ _tag_extra = " (Evento)" if opcion.get("tipo") == "evento" else " (Quest)"
                            button:
                                xfill True
                                background "#009688"
                                hover_background "#4DB6AC"
                                padding (15, 10)
                                action [Hide("menu_interaccion_npc_completo"),
                                        Return(("opcion_especial", opcion.get("label", "game_loop")))]

                                text (opcion.get("texto", "Opción") + _tag_extra) size 18 color "#ffffff"
            
            null height 10
            
            # Botón cerrar
            textbutton "Cerrar":
                xalign 0.5
                action Hide("menu_interaccion_npc_completo")
                text_size 20
                text_color "#FFF8E1"


################################################################################
## Screen de estadísticas de NPCs (sin cambios)
################################################################################

screen estadisticas_npcs():
    """Estadísticas de relaciones — App Relaciones"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("estadisticas_npcs") if modo_ajuste_celular else None

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header de app
            use _celular_app_header("Relaciones", "📊", [Hide("estadisticas_npcs"), Show("menu_celular")])

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
