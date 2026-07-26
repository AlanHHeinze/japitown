default inventario_pagina = 0

# Límites diarios de entrenamiento y trabajo
default entrenamiento_hoy = False  # True si ya entrenó hoy (1 vez al dia)
default trabajo_hoy = 0  # Contador de veces que trabajó hoy (máx 2)

################################################################################
## Sistema de Stats del MC
################################################################################
## Pantallas y funciones para gestionar los atributos del protagonista

init python:
    
    def entrenar_stat(stat_id):
        """
        Entrena un stat específico del MC.
        Aumenta el stat en 1 y avanza el horario.
        
        Args:
            stat_id: ID del stat ("fuerza", "carisma", "destreza", "inteligencia")
        
        Returns:
            bool: True si se pudo entrenar, False si es trasnoche
        """
        # Verificar restricción de quest/evento
        _msg = accion_bloqueada("entrenar")
        if _msg:
            return False
        
        # Verificar si es trasnoche
        if getattr(store, 'horario_actual', 0) == 3:
            return False
        
        # Verificar límite diario (1 vez por dia)
        if store.entrenamiento_hoy:
            return False
        
        # Aumentar el stat correspondiente
        stat_var = f"mc_{stat_id}"
        valor_actual = getattr(store, stat_var, 0)
        setattr(store, stat_var, valor_actual + 1)
        
        # Notificación visual
        notificar_cambio_stat(stat_id, 1)
        
        # Marcar que ya entrenó hoy
        store.entrenamiento_hoy = True
        
        # Avanzar horario
        if hasattr(store, 'avanzar_horario'):
            avanzar_horario()
        
        return True
    
    def trabajar():
        """
        El MC trabaja para ganar dinero.
        Aumenta dinero en 20 y avanza el horario.
        
        Returns:
            bool: True si se pudo trabajar, False si es trasnoche
        """
        # Verificar restricción de quest/evento
        _msg = accion_bloqueada("trabajar")
        if _msg:
            return False
        
        # Verificar si es trasnoche
        if getattr(store, 'horario_actual', 0) == 3:
            return False
        
        # Verificar límite diario (2 veces por dia)
        if store.trabajo_hoy >= 2:
            return False
        
        # Aumentar dinero
        store.dinero += 20
        
        # Notificación visual
        notificar_cambio_stat("dinero", 20)
        
        # Incrementar contador de trabajo diario
        store.trabajo_hoy += 1
        
        # Avanzar horario
        if hasattr(store, 'avanzar_horario'):
            avanzar_horario()
        
        return True
    
    def obtener_stat(stat_id):
        """Obtiene el valor de un stat del MC."""
        stat_var = f"mc_{stat_id}"
        return getattr(store, stat_var, 0)
    
    def modificar_stat(stat_id, cantidad):
        """
        Modifica un stat del MC (para cheats).
        
        Args:
            stat_id: ID del stat
            cantidad: Cantidad a sumar (puede ser negativa)
        """
        stat_var = f"mc_{stat_id}"
        valor_actual = getattr(store, stat_var, 0)
        nuevo_valor = max(0, valor_actual + cantidad)  # No puede ser negativo
        setattr(store, stat_var, nuevo_valor)
    
    # NOTA: Las funciones de compra fueron movidas a core/shopping/shopping_system.rpy
    # NOTA: Los items fueron movidos a core/shopping/items_shopping.rpy


# Inventario del jugador
default inventario = {}


################################################################################
## Panel de Stats del MC
################################################################################

screen panel_stats_mc():
    """Panel que muestra los stats — App Stats"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_stats_mc") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("panel_stats_mc")

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
            use _celular_barra_status("panel_stats_mc")

            # Header de app
            use _celular_app_header("Stats", "🎮", [Hide("panel_stats_mc"), Show("menu_celular")], "panel_stats_mc")

            # Contenido
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True

                frame:
                    xfill True
                    background None
                    padding (int(25 * _k), int(20 * _k))

                    vbox:
                        spacing int(20 * _k)
                        xfill True

                        # Sección stats
                        text "Atributos" size int(16 * _k) color "#4FC3F7" bold True

                        vbox:
                            spacing int(12 * _k)
                            xfill True

                            # Fuerza
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(15 * _k), int(10 * _k))

                                hbox:
                                    spacing int(12 * _k)
                                    yalign 0.5
                                    text "💪" size int(22 * _k)
                                    text "Fuerza" size int(16 * _k) color "#ffffff"
                                    text "[mc_fuerza]" size int(20 * _k) color "#FF6B6B" bold True xalign 1.0

                            # Carisma
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(15 * _k), int(10 * _k))

                                hbox:
                                    spacing int(12 * _k)
                                    yalign 0.5
                                    text "💬" size int(22 * _k)
                                    text "Carisma" size int(16 * _k) color "#ffffff"
                                    text "[mc_carisma]" size int(20 * _k) color "#FFB74D" bold True xalign 1.0

                            # Destreza
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(15 * _k), int(10 * _k))

                                hbox:
                                    spacing int(12 * _k)
                                    yalign 0.5
                                    text "🎯" size int(22 * _k)
                                    text "Destreza" size int(16 * _k) color "#ffffff"
                                    text "[mc_destreza]" size int(20 * _k) color "#4FC3F7" bold True xalign 1.0

                            # Inteligencia
                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                padding (int(15 * _k), int(10 * _k))

                                hbox:
                                    spacing int(12 * _k)
                                    yalign 0.5
                                    text "🧠" size int(22 * _k)
                                    text "Inteligencia" size int(16 * _k) color "#ffffff"
                                    text "[mc_inteligencia]" size int(20 * _k) color "#81C784" bold True xalign 1.0

                        # Separador
                        frame:
                            xfill True
                            ysize int(1 * _k)
                            background "#ffffff11"

                        # Dinero
                        frame:
                            xfill True
                            background "#1a2e1aCC"
                            padding (int(15 * _k), int(12 * _k))

                            hbox:
                                spacing int(12 * _k)
                                yalign 0.5
                                text "💰" size int(24 * _k)
                                text "Dinero" size int(18 * _k) color "#ffffff"
                                text "$[dinero]" size int(22 * _k) color "#4CAF50" bold True xalign 1.0


################################################################################
## Panel de Entrenamiento (Solo en habitacion del MC)
################################################################################

screen panel_entrenamiento():
    """Panel de entrenamiento que aparece en la habitación del MC"""

    # Misma escala que el HUD superior y el panel de acciones de locación
    # (HUD_ESCALA_SMALL, en hud_navigation.rpy / actionsystem_screen.rpy).
    $ _pe_k = HUD_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Solo mostrar si estamos en la habitacion del MC
    if sistema_locaciones.locacion_actual and sistema_locaciones.locacion_actual.id == "casa_hmc":

        # Verificar si es trasnoche
        $ es_trasnoche = (horario_actual == 3)

        frame:
            xalign 0.5
            yalign 0.0
            yoffset int(120 * _pe_k)  # Debajo del panel de tiempo
            background "#1e112180"
            padding (int(20 * _pe_k), int(12 * _pe_k))
            at hud_panel_fadein

            # Borde redondeado simulado con frame interior
            has hbox
            spacing int(15 * _pe_k)
            yalign 0.5

            if es_trasnoche:
                text "Es muy tarde para hacer actividades" size int(14 * _pe_k) color "#ff6666" yalign 0.5
            else:
                # Botón Fuerza (circular)
                vbox:
                    spacing int(4 * _pe_k)
                    xalign 0.5

                    button:
                        action Call("accion_entrenar", "fuerza")
                        xsize int(48 * _pe_k) ysize int(48 * _pe_k)
                        background "#D32F2F"
                        hover_background "#EF5350"
                        xalign 0.5
                        tooltip "Entrenar Fuerza"
                        at hud_train_hover(_pe_k)
                        text "💪" size int(22 * _pe_k) xalign 0.5 yalign 0.5

                    text "STR" size int(10 * _pe_k) color "#EF9A9A" bold True xalign 0.5

                # Botón Carisma (circular)
                vbox:
                    spacing int(4 * _pe_k)
                    xalign 0.5

                    button:
                        action Call("accion_entrenar", "carisma")
                        xsize int(48 * _pe_k) ysize int(48 * _pe_k)
                        background "#FF8F00"
                        hover_background "#FFB74D"
                        xalign 0.5
                        tooltip "Entrenar Carisma"
                        at hud_train_hover(_pe_k)
                        text "💬" size int(22 * _pe_k) xalign 0.5 yalign 0.5

                    text "CHR" size int(10 * _pe_k) color "#FFCC80" bold True xalign 0.5

                # Botón Destreza (circular)
                vbox:
                    spacing int(4 * _pe_k)
                    xalign 0.5

                    button:
                        action Call("accion_entrenar", "destreza")
                        xsize int(48 * _pe_k) ysize int(48 * _pe_k)
                        background "#0288D1"
                        hover_background "#4FC3F7"
                        xalign 0.5
                        tooltip "Entrenar Destreza"
                        at hud_train_hover(_pe_k)
                        text "🎯" size int(22 * _pe_k) xalign 0.5 yalign 0.5

                    text "DEX" size int(10 * _pe_k) color "#81D4FA" bold True xalign 0.5

                # Botón Inteligencia (circular)
                vbox:
                    spacing int(4 * _pe_k)
                    xalign 0.5

                    button:
                        action Call("accion_entrenar", "inteligencia")
                        xsize int(48 * _pe_k) ysize int(48 * _pe_k)
                        background "#388E3C"
                        hover_background "#81C784"
                        xalign 0.5
                        tooltip "Entrenar Inteligencia"
                        at hud_train_hover(_pe_k)
                        text "🧠" size int(22 * _pe_k) xalign 0.5 yalign 0.5

                    text "INT" size int(10 * _pe_k) color "#A5D6A7" bold True xalign 0.5

                # Separador vertical
                frame:
                    xsize int(1 * _pe_k)
                    ysize int(40 * _pe_k)
                    yalign 0.5
                    background "#ffffff33"

                # Botón Trabajar (circular)
                vbox:
                    spacing int(4 * _pe_k)
                    xalign 0.5

                    button:
                        action Call("accion_trabajar")
                        xsize int(48 * _pe_k) ysize int(48 * _pe_k)
                        background "#795548"
                        hover_background "#A1887F"
                        xalign 0.5
                        tooltip "Trabajar (+$20)"
                        at hud_train_hover(_pe_k)
                        text "💼" size int(22 * _pe_k) xalign 0.5 yalign 0.5

                    text "WORK" size int(10 * _pe_k) color "#BCAAA4" bold True xalign 0.5


################################################################################
## Panel de Tienda / Comprar
################################################################################

screen panel_tienda():
    """Panel de tienda — App Tienda"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_tienda") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("panel_tienda")

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
            use _celular_barra_status("panel_tienda")

            # Header de app con dinero
            frame:
                xfill True
                ysize int(55 * _k)
                background "#12122aFF"
                padding (int(10 * _k), 0)

                if renpy.variant("small"):
                    # Táctil: volver (izquierda), título centrado, dinero + cerrar (derecha)
                    fixed:
                        xfill True
                        yfill True

                        textbutton "◀":
                            xalign 0.0
                            yalign 0.5
                            action [Hide("panel_tienda"), Show("menu_celular")]
                            text_size int(44 * _k)
                            text_color "#4FC3F7"
                            text_hover_color "#81D4FA"
                            padding (int(8 * _k), int(5 * _k))

                        hbox:
                            xalign 0.5
                            yalign 0.5
                            spacing int(8 * _k)
                            text "🛒" size int(20 * _k) yalign 0.5
                            text _("Tienda") size int(18 * _k) color "#ffffff" bold True yalign 0.5

                        hbox:
                            xalign 1.0
                            yalign 0.5
                            spacing int(14 * _k)

                            hbox:
                                spacing int(5 * _k)
                                yalign 0.5
                                text "💰" size int(16 * _k) yalign 0.5
                                text "$[dinero]" size int(16 * _k) color "#4CAF50" bold True yalign 0.5

                            button:
                                yalign 0.5
                                xysize (int(44 * _k), int(44 * _k))
                                background "#E53935EE"
                                hover_background "#FF5449"
                                if modo_ajuste_celular:
                                    action NullAction()
                                else:
                                    action [Hide("panel_tienda"), SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
                                text "X" size int(24 * _k) color "#ffffff" bold True xalign 0.5 yalign 0.5

                else:
                    hbox:
                        yalign 0.5
                        xfill True
                        spacing 10

                        textbutton "◀":
                            action [Hide("panel_tienda"), Show("menu_celular")]
                            text_size 44
                            text_color "#4FC3F7"
                            text_hover_color "#81D4FA"
                            yalign 0.5
                            padding (8, 5)

                        hbox:
                            spacing 8
                            yalign 0.5
                            text "🛒" size 20 yalign 0.5
                            text _("Tienda") size 18 color "#ffffff" bold True yalign 0.5

                        # Dinero a la derecha
                        hbox:
                            spacing 5
                            xalign 1.0
                            yalign 0.5
                            text "💰" size 16 yalign 0.5
                            text "$[dinero]" size 16 color "#4CAF50" bold True yalign 0.5

                frame:
                    xfill True
                    ysize int(1 * _k)
                    yalign 1.0
                    background "#ffffff11"

            # Info reposición
            frame:
                xfill True
                background "#12122a88"
                padding (int(15 * _k), int(5 * _k))
                $ dias_repo = obtener_dias_para_reposicion()
                text _("📦 Reposición en [dias_repo] días") size int(12 * _k) color "#888888" xalign 0.5

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
                    padding (int(15 * _k), int(10 * _k))

                    vbox:
                        spacing int(15 * _k)
                        xfill True

                        # Grid de items
                        text _("Productos") size int(14 * _k) color "#4FC3F7" bold True

                        for item_id, item_info in CATALOGO_ITEMS.items():
                            $ _item_visible_cond = item_info.get("condicion_visible")
                            if item_info.get("vendible", True) and (_item_visible_cond is None or _item_visible_cond()):
                                $ item_stock = stock_tienda.get(item_id, 0)
                                $ agotado = (item_stock <= 0)

                                frame:
                                    xfill True
                                    background "#1e1e3aCC"
                                    hover_background "#2a2a50CC"
                                    padding (int(15 * _k), int(10 * _k))

                                    hbox:
                                        spacing int(12 * _k)
                                        yalign 0.5
                                        xfill True

                                        text item_info["emoji"] size int(32 * _k) yalign 0.5

                                        vbox:
                                            spacing int(2 * _k)
                                            text renpy.translate_string(item_info["nombre"]) size int(14 * _k) color "#ffffff" bold True
                                            $ dias = item_info.get("dias_entrega", 1)
                                            if dias == 1:
                                                text _("📦 Entrega en 1 día") size int(11 * _k) color "#888888"
                                            else:
                                                text _("📦 Entrega en [dias] días") size int(11 * _k) color "#888888"
                                            if agotado:
                                                text _("AGOTADO") size int(11 * _k) color "#FF4444" bold True
                                            else:
                                                text _("Stock: [item_stock]") size int(11 * _k) color "#aaaaaa"

                                        vbox:
                                            xalign 1.0
                                            yalign 0.5
                                            spacing int(5 * _k)
                                            text "$[item_info['precio']]" size int(16 * _k) color "#4CAF50" bold True xalign 1.0
                                            $ _sin_dinero = (not agotado and dinero < item_info["precio"])
                                            textbutton _("Comprar"):
                                                text_size int(12 * _k)
                                                padding (int(10 * _k), int(4 * _k))
                                                if agotado:
                                                    action Function(renpy.notify, renpy.translate_string("Producto sin stock"))
                                                    background "#666666"
                                                    text_color "#999999"
                                                elif _sin_dinero:
                                                    action Function(renpy.notify, renpy.translate_string("Dinero insuficiente"))
                                                    background "#666666"
                                                    text_color "#999999"
                                                else:
                                                    action Function(comprar_item_tienda, item_id)
                                                    background "#4CAF50"
                                                    hover_background "#81C784"

                        # Separador
                        frame:
                            xfill True
                            ysize int(1 * _k)
                            background "#ffffff11"

                        # Órdenes pendientes
                        $ ordenes = obtener_ordenes_pendientes()

                        text _("📋 Órdenes Pendientes") size int(14 * _k) color "#4FC3F7" bold True

                        if ordenes:
                            for orden in ordenes:
                                frame:
                                    background "#1e1e3aCC"
                                    padding (int(15 * _k), int(10 * _k))
                                    xfill True

                                    hbox:
                                        spacing int(15 * _k)

                                        vbox:
                                            spacing int(3 * _k)
                                            text _("Orden N°[orden.numero]") size int(13 * _k) color "#ffffff" bold True
                                            text orden.obtener_texto_dias() size int(11 * _k) color "#4FC3F7"

                                        vbox:
                                            spacing int(2 * _k)
                                            for texto_item in orden.obtener_contenido_texto():
                                                text texto_item size int(11 * _k) color "#cccccc"
                        else:
                            text _("Sin órdenes pendientes") size int(13 * _k) color "#888888"


################################################################################
## Panel de Inventario
################################################################################

screen panel_inventario():
    """Panel de inventario — grilla paginada 4x5"""

    modal True

    # Imagen de mochila centrada horizontalmente
    add "images/hud/mochila_inventario.png" xalign 0.5 yalign 0.0

    # Click en cualquier lugar cierra el inventario
    button:
        style "empty_button"
        xfill True
        yfill True
        action Hide("panel_inventario")

    python:
        _inv_items = [(k, v) for k, v in inventario.items() if v > 0]
        _inv_total = len(_inv_items)
        _inv_ipp = 12
        _inv_total_pag = max(1, (_inv_total + _inv_ipp - 1) // _inv_ipp) if _inv_total > 0 else 1
        _inv_pag = min(inventario_pagina, _inv_total_pag - 1)
        _inv_slice = _inv_items[_inv_pag * _inv_ipp : (_inv_pag + 1) * _inv_ipp]
        _inv_padded = _inv_slice + [(None, None)] * (_inv_ipp - len(_inv_slice))

    if _inv_total == 0:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10
            text "📦" size 48 xalign 0.5
            text _("Inventario vacío") size 16 color "#888888" xalign 0.5

    else:
        hbox:
            xalign 0.5
            ypos 420
            yanchor 0.0
            spacing 15

            # Flecha izquierda
            frame:
                background None
                xsize 55
                ysize 510
                if _inv_total_pag > 1 and _inv_pag > 0:
                    textbutton "◀":
                        xalign 0.5
                        yalign 0.5
                        action SetVariable("inventario_pagina", _inv_pag - 1)
                        text_size 44
                        text_color "#ffffff"
                        text_hover_color "#4FC3F7"
                else:
                    null

            # Grilla 3 columnas x 4 filas
            grid 3 4:
                xspacing 10
                yspacing 10
                for _inv_id, _inv_qty in _inv_padded:
                    if _inv_id is not None:
                        $ _inv_info = CATALOGO_ITEMS.get(_inv_id, {"emoji": "❓", "nombre": _inv_id})
                        button:
                            background None
                            hover_background None
                            action Function(usar_item, _inv_id)
                            fixed:
                                xsize 120
                                ysize 120
                                vbox:
                                    xalign 0.5
                                    ypos 5
                                    spacing 2
                                    text _inv_info["emoji"] size 56 xalign 0.5
                                    text renpy.translate_string(_inv_info["nombre"]) size 22 color "#ffffff" xalign 0.5
                                text "[_inv_qty]" size 22 color "#ffffff" bold True xalign 1.0 yalign 0.0
                    else:
                        fixed:
                            xsize 120
                            ysize 120

            # Flecha derecha
            frame:
                background None
                xsize 55
                ysize 510
                if _inv_total_pag > 1 and _inv_pag < _inv_total_pag - 1:
                    textbutton "▶":
                        xalign 0.5
                        yalign 0.5
                        action SetVariable("inventario_pagina", _inv_pag + 1)
                        text_size 44
                        text_color "#ffffff"
                        text_hover_color "#4FC3F7"
                else:
                    null


################################################################################
## Labels wrapper para acciones desde screen (entrar en contexto de label)
################################################################################

label accion_entrenar(stat_id):
    # Verificar restricción de quest/evento
    $ _msg_restriccion = accion_bloqueada("entrenar")
    if _msg_restriccion:
        $ _blk_guardar_toque()
        piensa "[_msg_restriccion]"
        return

    # Verificar si es trasnoche
    if horario_actual == 3:
        $ _blk_guardar_toque()
        piensa "Es muy tarde para entrenar."
        return
    
    # Verificar límite diario
    if entrenamiento_hoy:
        call pensar_mensaje("Estoy cansado por hoy, debería intentarlo mañana.") from _call_pensar_entrenar_limite
        return

    # Bloquear rollback — la recompensa no se puede deshacer
    $ renpy.block_rollback()
    $ entrenar_stat(stat_id)
    return


label accion_trabajar:
    # Verificar restricción de quest/evento
    $ _msg_restriccion = accion_bloqueada("trabajar")
    if _msg_restriccion:
        $ _blk_guardar_toque()
        piensa "[_msg_restriccion]"
        return

    # Verificar si es trasnoche
    if horario_actual == 3:
        $ _blk_guardar_toque()
        piensa "Es muy tarde para trabajar."
        return
    
    # Verificar límite diario
    if trabajo_hoy >= 2:
        call pensar_mensaje("No tengo tareas para hoy, debería esperar hasta mañana.") from _call_pensar_trabajar_limite
        return

    # Bloquear rollback — la recompensa no se puede deshacer
    $ renpy.block_rollback()
    $ trabajar()
    return

