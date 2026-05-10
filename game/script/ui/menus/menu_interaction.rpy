################################################################################
## Menú de Interacción con NPCs - Versión 2.0
################################################################################
## Incluye menú completo con sprite de NPC y skins agrupados

# Variable para preview de skin en menú
default _skin_preview_actual = None
default _grupo_skin_seleccionado = "base"

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
            
            # Información del NPC
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
                
                # Opción: Hablar
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
                # OPCIÓN DE CAMBIAR SKIN (SIEMPRE VISIBLE)
                # =====================================================================
                
                null height 5
                frame:
                    xfill True
                    ysize 1
                    background "#9C27B044"
                null height 5
                
                button:
                    xfill True
                    background "#9C27B0"
                    hover_background "#BA68C8"
                    padding (15, 10)
                    action [Hide("menu_interaccion_npc_completo"),
                            SetVariable("_grupo_skin_seleccionado", "base"),
                            Show("menu_skins_grupos", npc=npc)]
                    
                    hbox:
                        spacing 10
                        text "👕" size 20 color "#ffffff"
                        text "Cambiar Skin" size 18 color "#ffffff" bold True
                
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
                            button:
                                xfill True
                                background "#009688"
                                hover_background "#4DB6AC"
                                padding (15, 10)
                                action [Hide("menu_interaccion_npc_completo"),
                                        Return(("opcion_especial", opcion.get("label", "game_loop")))]

                                text opcion.get("texto", "Opción") size 18 color "#ffffff"
            
            null height 10
            
            # Botón cerrar
            textbutton "Cerrar":
                xalign 0.5
                action Hide("menu_interaccion_npc_completo")
                text_size 20
                text_color "#FFF8E1"


################################################################################
## Screen de Skins Agrupados
################################################################################

screen menu_skins_grupos(npc):
    """
    Menú de skins agrupados con vista previa.
    """
    
    modal True
    
    # Fondo con el background actual
    $ _bg_actual = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#000000"
    add _bg_actual
    
    # Overlay
    add Solid("#00000088")
    
    # Sprite de preview a la derecha
    $ _preview = getattr(store, "_skin_preview_actual", None)
    $ _sprite_mostrar = _preview if _preview else obtener_sprite_menu_npc(npc.id)
    
    if _sprite_mostrar:
        add _sprite_mostrar at skin_preview_transform:
            xalign 0.85
            yalign 1.0
    
    # Panel de grupos y skins
    frame:
        xalign 0.2
        yalign 0.5
        background "#0288D1EE"
        padding (25, 20)
        
        vbox:
            spacing 15
            
            # Título
            text "Skins de [npc.nombre]" size 28 color "#FFF8E1" bold True xalign 0.5
            
            null height 5
            frame:
                xsize 350
                ysize 2
                background "#4FC3F7"
            null height 10
            
            # Lista de grupos (solo grupos con al menos 1 skin desbloqueado)
            $ grupos = obtener_grupos_con_skins(npc.id)
            
            for grupo in grupos:
                # Encabezado del grupo
                frame:
                    xsize 350
                    background "#1565C0"
                    padding (15, 8)
                    
                    text "[grupo.capitalize()]" size 22 color "#FFF8E1" bold True
                
                # Skins del grupo
                $ skins_grupo = sistema_skins.obtener_skins_grupo(npc.id, grupo)
                $ skin_activo = sistema_skins.obtener_skin_activo_grupo(npc.id, grupo)
                
                vbox:
                    spacing 5
                    xoffset 15
                    
                    for skin in skins_grupo:
                        $ esta_desbloqueado = skin.esta_desbloqueado()
                        $ es_activo = (skin_activo and skin_activo.id == skin.id)
                        
                        if esta_desbloqueado:
                            button:
                                xsize 320
                                if es_activo:
                                    background "#4CAF50"
                                    hover_background "#66BB6A"
                                else:
                                    background "#37474F"
                                    hover_background "#546E7A"
                                padding (12, 8)
                                
                                # Al hacer hover, mostrar preview
                                hovered SetVariable("_skin_preview_actual", skin.sprite_menu)
                                unhovered SetVariable("_skin_preview_actual", None)
                                
                                # Al hacer click, activar skin
                                action [Function(activar_skin, npc.id, skin.id),
                                        renpy.restart_interaction]
                                
                                hbox:
                                    spacing 10
                                    if es_activo:
                                        text "✓" size 18 color "#ffffff"
                                    text "[skin.nombre]" size 18 color "#ffffff"
                        else:
                            # Skin bloqueado
                            button:
                                xsize 320
                                background "#1a1a1a"
                                padding (12, 8)
                                action None
                                
                                hbox:
                                    spacing 10
                                    text "🔒" size 18 color "#666666"
                                    text "[skin.nombre]" size 18 color "#666666"
                
                null height 10
            
            null height 10
            
            # Botón volver
            textbutton "← Volver":
                xalign 0.5
                action [SetVariable("_skin_preview_actual", None),
                        Hide("menu_skins_grupos"),
                        Show("menu_interaccion_npc_completo", npc=npc)]
                text_size 20
                text_color "#FFF8E1"


################################################################################
## Transform para preview de skin
################################################################################

transform skin_preview_transform:
    on replace:
        alpha 0.0
        linear 0.3 alpha 1.0


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
