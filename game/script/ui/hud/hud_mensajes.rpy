################################################################################
## Pantallas del Sistema de Mensajes
################################################################################
## UI para lista de contactos, chat individual, selector de respuesta,
## y resumen de recompensas.

# Variable para controlar la pantalla de "escribiendo..."
default _msg_escribiendo = False
default _msg_respuestas_pendientes = []
default _msg_foto_pendiente = None
default _msg_resultado_pendiente = None
default _msg_npc_chat_actual = ""
default _msg_tiempo_escribiendo = 1.5
default _msg_timer_id = 0

# -----------------------------------------------------------------------------
# Auto-scroll del chat
# -----------------------------------------------------------------------------
# El "yinitial 1.0" del viewport solo se aplica cuando el viewport se crea, asi
# que al llegar un mensaje nuevo el scroll se quedaba donde estaba. Usamos un
# adjustment propio para poder empujarlo al fondo cada vez que cambia el
# contenido del chat (mensaje nuevo, respuesta del jugador, "escribiendo...").
# Es "define" a proposito: es estado de UI, no va al save.
define _chat_yadj = ui.adjustment()

# Ultimo contenido visto: (npc_id, cantidad de mensajes, escribiendo?)
default _chat_scroll_estado = None

init python:

    def _chat_scroll_al_fondo():
        """Lleva el viewport del chat al ultimo mensaje."""
        try:
            _chat_yadj.change(_chat_yadj.range)
        except Exception:
            pass

# =============================================================================
# LISTA DE CONTACTOS
# =============================================================================

screen lista_contactos_mensajes():
    """Lista de contactos — App Mensajes"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("lista_contactos_mensajes") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("lista_contactos_mensajes")

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
            use _celular_barra_status("lista_contactos_mensajes")

            # Header de app
            use _celular_app_header("Chat", "💬", [Hide("lista_contactos_mensajes"), Show("menu_celular")], "lista_contactos_mensajes")

            # Lista de contactos
            $ _contactos_fijos = ["jasmine", "monica", "violet"]
            $ _contactos_extra = [k for k in sistema_mensajes.chats.keys() if k not in _contactos_fijos and sistema_mensajes.chats[k].historial]
            $ _todos_contactos = _contactos_fijos + _contactos_extra

            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (int(10 * _k), int(8 * _k))

                    vbox:
                        spacing int(4 * _k)
                        xfill True

                        for npc_id in _todos_contactos:
                            $ _chat = sistema_mensajes.chats.get(npc_id)
                            $ _sin_leer = sistema_mensajes.obtener_pendientes_npc(npc_id)
                            $ _ultimo = _chat.obtener_ultimo_mensaje() if _chat else None
                            $ _nombre = obtener_nombre_contacto(npc_id)
                            $ _icono = CONTACTOS_ESPECIALES.get(npc_id, {}).get("icono", "👤")

                            button:
                                action [
                                    SetVariable("_msg_npc_chat_actual", npc_id),
                                    Hide("lista_contactos_mensajes"),
                                    Show("pantalla_chat", npc_id=npc_id)
                                ]
                                xfill True

                                frame:
                                    xfill True
                                    background "#1e1e3aCC"
                                    hover_background "#2a2a50CC"
                                    padding (int(12 * _k), int(10 * _k))

                                    hbox:
                                        spacing int(12 * _k)
                                        yalign 0.5

                                        # Icono NPC
                                        $ _icon_path = "images/hud/pista_{}.png".format(npc_id)
                                        frame:
                                            xysize (int(42 * _k), int(42 * _k))
                                            background "#3a3a5aCC"

                                            if renpy.loadable(_icon_path):
                                                add _icon_path zoom (0.164 * _k) xalign 0.5 yalign 0.5
                                            else:
                                                text "[_icono]" size int(22 * _k) xalign 0.5 yalign 0.5

                                        # Nombre y preview
                                        vbox:
                                            spacing int(2 * _k)

                                            text "[_nombre]" size int(15 * _k) color "#ffffff" bold True

                                            if _ultimo:
                                                $ _texto_sub = renpy.substitute(renpy.translate_string(_ultimo.texto))
                                                $ _preview = _texto_sub[:35] + ("..." if len(_texto_sub) > 35 else "")
                                                text "[_preview]" size int(12 * _k) color "#aaaaaa"
                                            else:
                                                text _("Sin mensajes") size int(12 * _k) color "#666666"

                                        # Badge
                                        if _sin_leer > 0:
                                            frame:
                                                xalign 1.0
                                                yalign 0.5
                                                background "#FF4444"
                                                padding (int(6 * _k), int(3 * _k))
                                                xminimum int(24 * _k)

                                                text "[_sin_leer]" size int(12 * _k) color "#ffffff" bold True xalign 0.5


# =============================================================================
# PANTALLA DE CHAT
# =============================================================================

screen pantalla_chat(npc_id="monica"):
    """Vista de chat con un NPC — App Chat"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("pantalla_chat") if modo_ajuste_celular else None
    $ _chat = sistema_mensajes.chats.get(npc_id)
    $ _nombre = obtener_nombre_contacto(npc_id)
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Marcar como leído al abrir
    if _chat:
        on "show" action Function(_chat.marcar_como_leido)

    # Timer para "escribiendo..."
    use _timer_escribiendo()

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("pantalla_chat")

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
            use _celular_barra_status("pantalla_chat")

            # Header del chat con avatar
            frame:
                xsize ajuste_cel_area_w
                ysize int(55 * _k)
                background "#12122aFF"
                padding (int(10 * _k), 0)

                $ _icon_path_header = "images/hud/pista_{}.png".format(npc_id)

                if renpy.variant("small"):
                    # Táctil: volver (izquierda), avatar+nombre centrado, cerrar (derecha)
                    fixed:
                        xfill True
                        yfill True

                        textbutton "◀":
                            xalign 0.0
                            yalign 0.5
                            action [Hide("pantalla_chat"), Show("lista_contactos_mensajes")]
                            text_size int(44 * _k)
                            text_color "#4FC3F7"
                            text_hover_color "#81D4FA"
                            padding (int(8 * _k), int(5 * _k))

                        hbox:
                            xalign 0.5
                            yalign 0.5
                            spacing int(10 * _k)

                            frame:
                                xysize (int(32 * _k), int(32 * _k))
                                background "#3a3a5aCC"
                                yalign 0.5

                                if renpy.loadable(_icon_path_header):
                                    add _icon_path_header zoom (0.125 * _k) xalign 0.5 yalign 0.5
                                else:
                                    text "👤" size int(16 * _k) xalign 0.5 yalign 0.5

                            text "[_nombre]" size int(16 * _k) color "#ffffff" bold True yalign 0.5

                        button:
                            xalign 1.0
                            yalign 0.5
                            xysize (int(44 * _k), int(44 * _k))
                            background "#E53935EE"
                            hover_background "#FF5449"
                            if modo_ajuste_celular:
                                action NullAction()
                            else:
                                action [Hide("pantalla_chat"), SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
                            text "X" size int(24 * _k) color "#ffffff" bold True xalign 0.5 yalign 0.5

                else:
                    hbox:
                        yalign 0.5
                        spacing 10

                        textbutton "◀":
                            action [Hide("pantalla_chat"), Show("lista_contactos_mensajes")]
                            text_size 44
                            text_color "#4FC3F7"
                            text_hover_color "#81D4FA"
                            yalign 0.5
                            padding (8, 5)

                        # Icono NPC
                        frame:
                            xysize (32, 32)
                            background "#3a3a5aCC"
                            yalign 0.5

                            if renpy.loadable(_icon_path_header):
                                add _icon_path_header zoom 0.125 xalign 0.5 yalign 0.5
                            else:
                                text "👤" size 16 xalign 0.5 yalign 0.5

                        text "[_nombre]" size 16 color "#ffffff" bold True yalign 0.5

                frame:
                    xfill True
                    ysize int(1 * _k)
                    yalign 1.0
                    background "#ffffff11"

            # Área de mensajes (scrollable)
            # Altura = area total - header - footer [- barra status - margen
            # inferior, en PC: en táctil no hay barra de estado (se sacó) y el
            # footer tiene que tocar el borde inferior de la pantalla, sin margen].
            if renpy.variant("small"):
                $ _chat_viewport_h = ajuste_cel_area_h - int(55 * _k) - int(100 * _k)
            else:
                $ _chat_viewport_h = ajuste_cel_area_h - 32 - 55 - 100 - 50

            # Auto-scroll al ultimo mensaje: si cambio el contenido del chat,
            # el timer deja que se re-renderice (para que el adjustment conozca
            # el alto nuevo) y recien ahi empuja el scroll al fondo. En táctil
            # el framerate real del dispositivo puede ser mucho mas bajo que en
            # PC, asi que un solo timer corto puede disparar antes de que el
            # viewport termine de acomodar el contenido nuevo: se reintenta un
            # par de veces mas con mas margen, a modo de red de seguridad
            # (los timers de mas no hacen nada si el primero ya alcanzo).
            $ _chat_contenido = (npc_id, len(_chat.historial) if _chat else 0, bool(_msg_escribiendo))
            if _chat_contenido != _chat_scroll_estado:
                if renpy.variant("small"):
                    timer 0.15 action Function(_chat_scroll_al_fondo)
                    timer 0.4 action Function(_chat_scroll_al_fondo)
                    timer 0.8 action [SetVariable("_chat_scroll_estado", _chat_contenido), Function(_chat_scroll_al_fondo)]
                else:
                    timer 0.01 action [SetVariable("_chat_scroll_estado", _chat_contenido), Function(_chat_scroll_al_fondo)]

            viewport:
                xsize ajuste_cel_area_w
                ysize _chat_viewport_h
                yadjustment _chat_yadj
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing int(6 * _k)
                    xfill True
                    box_wrap False

                    null height int(8 * _k)

                    if _chat and len(_chat.historial) > 0:
                        for _msg in _chat.historial:
                            if _msg.emisor == "jugador":
                                # Burbuja del jugador (derecha)
                                hbox:
                                    xfill True
                                    xalign 1.0

                                    null

                                    frame:
                                        xalign 1.0
                                        xmaximum int(420 * _k)
                                        background "#1565C0CC"
                                        padding (int(10 * _k), int(7 * _k))

                                        vbox:
                                            spacing int(3 * _k)
                                            if _msg.foto:
                                                imagebutton:
                                                    idle _msg.foto
                                                    hover _msg.foto
                                                    action Show("vista_foto_ampliada", foto=_msg.foto)
                                                    at transform:
                                                        zoom (0.3 * _k)
                                            $ _texto_jugador = renpy.substitute(renpy.translate_string(_msg.texto))
                                            text "[_texto_jugador]" size int(13 * _k) color "#ffffff" xalign 1.0
                            else:
                                # Burbuja del NPC (izquierda)
                                hbox:
                                    xfill True
                                    xalign 0.0

                                    frame:
                                        xalign 0.0
                                        xmaximum int(420 * _k)
                                        background "#1e1e3aCC"
                                        padding (int(10 * _k), int(7 * _k))

                                        vbox:
                                            spacing int(3 * _k)
                                            text "[_nombre]" size int(10 * _k) color "#8888bb" bold True
                                            if _msg.foto:
                                                imagebutton:
                                                    idle _msg.foto
                                                    hover _msg.foto
                                                    action Show("vista_foto_ampliada", foto=_msg.foto)
                                                    at transform:
                                                        zoom (0.3 * _k)
                                            $ _texto_npc = renpy.substitute(renpy.translate_string(_msg.texto))
                                            text "[_texto_npc]" size int(13 * _k) color "#dddddd"

                                    null
                    else:
                        text _("No hay mensajes aún") size int(14 * _k) color "#666666" xalign 0.5 yalign 0.5

                    # Indicador "Escribiendo..."
                    if _msg_escribiendo and _msg_npc_chat_actual == npc_id:
                        hbox:
                            xfill True
                            xalign 0.0

                            frame:
                                xalign 0.0
                                background "#1e1e3aCC"
                                padding (int(10 * _k), int(7 * _k))

                                hbox:
                                    spacing int(5 * _k)
                                    text "[_nombre]" size int(10 * _k) color "#8888bb" bold True
                                    text _("escribiendo...") size int(10 * _k) color "#8888bb" italic True

                    null height int(8 * _k)

            # Barra inferior
            frame:
                xsize ajuste_cel_area_w
                ysize int(100 * _k)
                background "#0a0a18FF"
                padding (int(15 * _k), int(12 * _k))

                hbox:
                    xfill True
                    spacing int(10 * _k)

                    $ _puede_responder = _chat and _chat.puede_responder() and not _msg_escribiendo and not _msg_respuestas_pendientes
                    $ _bg_color = "#4CAF50CC" if _puede_responder else "#1e1e3a66"
                    $ _hover_color = "#66BB6ACC" if _puede_responder else "#1e1e3a66"

                    button:
                        action (Function(_abrir_selector_respuesta, npc_id) if _puede_responder else NullAction())
                        xfill True
                        ysize int(76 * _k)
                        background _bg_color
                        hover_background _hover_color
                        padding (int(15 * _k), int(10 * _k))

                        hbox:
                            spacing int(10 * _k)
                            yalign 0.5
                            if not _puede_responder:
                                xalign 0.5

                            if _puede_responder:
                                text "📝" size int(36 * _k) yalign 0.5
                                text _("Escribe un mensaje...") size int(28 * _k) color "#ffffff" yalign 0.5
                            elif _chat and _chat.tiene_pendientes() and not _msg_escribiendo:
                                text _("[_nombre] responderá más tarde.") size int(26 * _k) color "#888888" yalign 0.5
                            else:
                                text "—" size int(28 * _k) color "#444444" yalign 0.5


# =============================================================================
# SELECTOR DE RESPUESTA
# =============================================================================

screen selector_respuesta(npc_id="monica"):
    """Selector de respuesta — overlay dentro del celular"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("selector_respuesta") if modo_ajuste_celular else None
    $ _chat = sistema_mensajes.chats.get(npc_id)
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo semi-transparente solo en area del celular
    button:
        style "empty_button"
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        action Hide("selector_respuesta")

    # Panel de opciones — parte inferior del celular
    frame:
        xpos ajuste_cel_area_x
        xsize ajuste_cel_area_w
        yalign 1.0
        background "#12122aF5"
        padding (int(15 * _k), int(15 * _k))

        vbox:
            spacing int(10 * _k)
            xfill True

            # Si hay grupo activo
            if _chat and _chat.grupo_activo:
                $ _grupo = _chat.grupo_activo
                $ _paso = _grupo.obtener_paso_actual()

                if _paso:
                    $ _opciones_visibles = [(i, op) for i, op in enumerate(_paso.opciones_jugador) if op.es_visible()]

                    text _("Elige tu respuesta:") size int(14 * _k) color "#4FC3F7" bold True xalign 0.5

                    for _i_real, _opcion in _opciones_visibles:
                        button:
                            action [
                                Hide("selector_respuesta"),
                                Function(_procesar_respuesta, npc_id, _i_real)
                            ]
                            xfill True

                            frame:
                                xfill True
                                background "#1e1e3aCC"
                                hover_background "#2a2a50CC"
                                padding (int(12 * _k), int(8 * _k))

                                # texto puede ser callable (igual que en seleccionar_respuesta,
                                # messagesystem_core): resolverlo antes de traducir, o se
                                # renderiza el repr de la funcion.
                                $ _texto_crudo = _opcion.texto() if callable(_opcion.texto) else _opcion.texto
                                $ _texto_opcion = renpy.substitute(renpy.translate_string(_texto_crudo))
                                text "[_texto_opcion]" size int(13 * _k) color "#ffffff"

            elif _chat and len(_chat.grupos_pendientes) > 0:
                $ _grupos_visibles = [g for g in _chat.grupos_pendientes if _chat._horario_valido(g)]
                text _("¿A qué mensaje respondés?") size int(14 * _k) color "#4FC3F7" bold True xalign 0.5

                for _grupo in _grupos_visibles:
                    $ _texto_preview = renpy.substitute(_grupo.mensaje_inicial)
                    $ _preview_msg = _texto_preview[:45] + ("..." if len(_texto_preview) > 45 else "")

                    button:
                        action [
                            Function(sistema_mensajes.seleccionar_grupo, npc_id, _grupo.id),
                            Hide("selector_respuesta"),
                            Show("selector_respuesta", npc_id=npc_id)
                        ]
                        xfill True

                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            hover_background "#2a2a50CC"
                            padding (int(12 * _k), int(8 * _k))

                            text "\"[_preview_msg]\"" size int(12 * _k) color "#aaaaaa" italic True

            # Cancelar
            textbutton "✖ Cancelar":
                action Hide("selector_respuesta")
                xalign 0.5
                text_size int(13 * _k)
                text_color "#888888"
                text_hover_color "#ffffff"


# =============================================================================
# RESUMEN DE RECOMPENSAS
# =============================================================================

screen resumen_recompensas(npc_id="monica", recompensas=None, puntos_totales=None):
    """Resumen al finalizar conversación — dentro del celular"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("resumen_recompensas") if modo_ajuste_celular else None
    $ _npc = obtener_npc(npc_id)
    $ _nombre = _npc.nombre if _npc else npc_id.capitalize()
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("resumen_recompensas")

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
            use _celular_barra_status("resumen_recompensas")

            # Header
            use _celular_app_header("Resumen", "✉️", [Hide("resumen_recompensas"), Show("menu_celular")], "resumen_recompensas")

            # Contenido
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True

                frame:
                    xfill True
                    background None
                    padding (int(20 * _k), int(15 * _k))

                    vbox:
                        spacing int(15 * _k)
                        xfill True

                        # Info
                        vbox:
                            spacing int(5 * _k)
                            xalign 0.5
                            text _("Conversación finalizada") size int(18 * _k) color "#FFD700" bold True xalign 0.5
                            text _("Chat con [_nombre]") size int(14 * _k) color "#aaaaaa" xalign 0.5

                        # Puntos
                        if puntos_totales:
                            frame:
                                xfill True
                                background "#1e1e3a88"
                                padding (int(15 * _k), int(10 * _k))

                                vbox:
                                    spacing int(6 * _k)
                                    text _("Puntos obtenidos:") size int(13 * _k) color "#8888bb" bold True

                                    for _cat, _pts in puntos_totales.items():
                                        hbox:
                                            spacing int(8 * _k)
                                            $ _cat_display = _cat.capitalize()
                                            text "  [_cat_display]:" size int(13 * _k) color "#cccccc"
                                            text "[_pts]" size int(13 * _k) color "#FFD700" bold True

                        # Recompensas
                        if recompensas:
                            frame:
                                xfill True
                                background "#1a2e1a88"
                                padding (int(15 * _k), int(10 * _k))

                                vbox:
                                    spacing int(6 * _k)
                                    text _("🎁 Recompensas:") size int(13 * _k) color "#4CAF50" bold True

                                    for _rec in recompensas:
                                        $ _tipo = _rec["recompensa"].get("tipo", "")
                                        $ _val = _rec["recompensa"].get("valor", 0)

                                        if _tipo == "amor":
                                            text "  +[_val] ❤️ Amor con [_nombre]" size int(13 * _k) color "#4CAF50"
                                        elif _tipo == "deseo":
                                            text "  +[_val] 💋 Deseo con [_nombre]" size int(13 * _k) color "#E91E63"
                                        elif _tipo == "dinero":
                                            text "  +$[_val]" size int(13 * _k) color "#FFD700"
                                        elif _tipo == "foto":
                                            text _("  📷 Foto desbloqueada!") size int(13 * _k) color "#2196F3"
                                        elif _tipo == "item":
                                            text _("  📦 Item obtenido!") size int(13 * _k) color "#FF9800"
                                        elif _tipo == "stat":
                                            $ _stat_id = _rec["recompensa"].get("stat_id", "")
                                            text "  +[_val] [_stat_id]" size int(13 * _k) color "#9C27B0"
                        elif not puntos_totales:
                            text _("Sin recompensas") size int(13 * _k) color "#666666" xalign 0.5

                        # Cerrar
                        textbutton _("Cerrar"):
                            action Hide("resumen_recompensas")
                            xalign 0.5
                            text_size int(14 * _k)
                            background "#607D8B"
                            hover_background "#90A4AE"
                            padding (int(20 * _k), int(8 * _k))
                            text_color "#ffffff"


# =============================================================================
# VISTA DE FOTO AMPLIADA
# =============================================================================

screen vista_foto_ampliada(foto):
    """Muestra una foto en tamaño completo — dentro del celular"""

    modal True

    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo dentro del area del celular
    button:
        style "empty_button"
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        action Hide("vista_foto_ampliada")

        add Solid("#000000EE")

    # Foto dentro del area del celular
    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None

        add foto xalign 0.5 yalign 0.5 at transform:
            fit "contain"
            xysize (ajuste_cel_area_w - int(40 * _k), ajuste_cel_area_h - int(80 * _k))

    # Botón cerrar dentro del celular
    textbutton "✖":
        action Hide("vista_foto_ampliada")
        xpos ajuste_cel_area_x + ajuste_cel_area_w - int(50 * _k)
        ypos ajuste_cel_area_y + int(10 * _k)
        text_size int(28 * _k)
        text_color "#ffffff"


# =============================================================================
# FUNCIÓN AUXILIAR: Procesar respuesta con delay "Escribiendo..."
# =============================================================================

init python:
    
    def _abrir_selector_respuesta(npc_id):
        """
        Abre el selector de respuesta con auto-selección de grupo único
        y auto-envío de respuesta única.
        """
        chat = store.sistema_mensajes.chats.get(npc_id)
        if not chat:
            return

        # Auto-seleccionar si solo hay 1 grupo pendiente y no hay grupo activo
        if not chat.grupo_activo and len(chat.grupos_pendientes) == 1:
            store.sistema_mensajes.seleccionar_grupo(npc_id, chat.grupos_pendientes[0].id)

        # Auto-enviar si solo hay 1 opción visible
        if chat.grupo_activo:
            paso = chat.grupo_activo.obtener_paso_actual()
            if paso:
                opciones_visibles = [(i, op) for i, op in enumerate(paso.opciones_jugador) if op.es_visible()]
                if len(opciones_visibles) == 1:
                    _procesar_respuesta(npc_id, opciones_visibles[0][0])
                    return

        renpy.show_screen("selector_respuesta", npc_id=npc_id)

    def calcular_tiempo_escribiendo(texto):
        """Calcula duración del indicador 'escribiendo...' según longitud del texto.
        Tiempos reducidos a la mitad para respuestas más rápidas."""
        if not texto:
            return 0.4
        longitud = len(texto)
        if longitud <= 20:
            return 0.4
        elif longitud <= 50:
            return 0.6
        elif longitud <= 100:
            return 0.9
        else:
            return 1.25

    def _procesar_respuesta(npc_id, opcion_idx):
        """
        Procesa la respuesta del jugador con delay de 'escribiendo...'
        Los mensajes se procesan uno a la vez con su propio indicador.
        """
        resultado = store.sistema_mensajes.responder(npc_id, opcion_idx)

        if not resultado.get("exito"):
            return

        respuestas = resultado.get("respuestas_npc", [])
        msg_siguiente = resultado.get("mensaje_siguiente")

        # Filtrar mensajes vacíos
        respuestas_filtradas = [r for r in respuestas if r]

        # Agregar mensaje_siguiente al final de la cola si existe
        if msg_siguiente:
            respuestas_filtradas.append(msg_siguiente)

        store._msg_npc_chat_actual = npc_id
        store._msg_respuestas_pendientes = respuestas_filtradas
        store._msg_foto_pendiente = resultado.get("foto")
        store._msg_resultado_pendiente = resultado

        if respuestas_filtradas:
            # Calcular tiempo del primer mensaje y activar escribiendo
            store._msg_tiempo_escribiendo = calcular_tiempo_escribiendo(respuestas_filtradas[0])
            store._msg_timer_id += 1
            store._msg_escribiendo = True
            renpy.restart_interaction()
        else:
            # Sin respuestas de texto, finalizar directamente
            _finalizar_escribiendo(npc_id)

    def _finalizar_escribiendo(npc_id):
        """
        Callback del timer: agrega UN mensaje del NPC al historial.
        Si quedan más, pasa a estado 'cooldown' para que el screen
        destruya el timer viejo y cree uno nuevo.
        """
        chat = store.sistema_mensajes.chats.get(npc_id)
        if not chat:
            return

        respuestas = store._msg_respuestas_pendientes or []
        foto = store._msg_foto_pendiente

        if respuestas:
            # Pop el primer mensaje
            texto_actual = respuestas.pop(0)
            # La foto va solo en el primer mensaje (cuando foto existe y es el primero)
            msg_foto = foto if foto else None
            if msg_foto:
                store._msg_foto_pendiente = None  # Ya se usó la foto

            chat.agregar_mensaje(npc_id, texto_actual, msg_foto)
            chat.mensajes_sin_leer = max(0, chat.mensajes_sin_leer - 1)

        store._msg_respuestas_pendientes = respuestas

        if respuestas:
            # Quedan más mensajes: apagar escribiendo temporalmente (cooldown)
            # El screen detecta esto y lanza un mini-timer que lo re-enciende
            store._msg_tiempo_escribiendo = calcular_tiempo_escribiendo(respuestas[0])
            store._msg_escribiendo = False
            store._msg_timer_id += 1  # Señal de que hay más pendientes
        else:
            # No quedan más mensajes: limpiar estado
            store._msg_escribiendo = False
            store._msg_respuestas_pendientes = []
            store._msg_foto_pendiente = None
            store._msg_resultado_pendiente = None
            store._msg_timer_id = 0

        renpy.restart_interaction()

    def _reactivar_escribiendo():
        """Callback del mini-timer: re-activa el indicador de escribiendo."""
        if store._msg_respuestas_pendientes:
            store._msg_escribiendo = True
            renpy.restart_interaction()


# Timer screen que se muestra sobre el chat para el delay de "escribiendo..."
screen _timer_escribiendo():
    """Timer invisible para el delay de 'escribiendo...'"""

    if _msg_escribiendo and _msg_npc_chat_actual:
        # Timer principal: espera el tiempo calculado y entrega el mensaje
        timer _msg_tiempo_escribiendo action Function(_finalizar_escribiendo, _msg_npc_chat_actual)
    elif not _msg_escribiendo and _msg_timer_id > 0 and _msg_respuestas_pendientes:
        # Cooldown: el timer anterior terminó, hay más mensajes pendientes
        # Mini-timer de 0.05s para re-activar escribiendo (fuerza nuevo ciclo de timer)
        timer 0.05 action Function(_reactivar_escribiendo)
