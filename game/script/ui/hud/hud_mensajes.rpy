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

# =============================================================================
# LISTA DE CONTACTOS
# =============================================================================

screen lista_contactos_mensajes():
    """Lista de contactos — App Mensajes"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("lista_contactos_mensajes") if modo_ajuste_celular else None

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header de app
            use _celular_app_header("Chat", "💬", [Hide("lista_contactos_mensajes"), Show("menu_celular")])

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
                    padding (10, 8)

                    vbox:
                        spacing 4
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
                                    padding (12, 10)

                                    hbox:
                                        spacing 12
                                        yalign 0.5

                                        # Icono NPC
                                        $ _icon_path = "images/hud/pista_{}.png".format(npc_id)
                                        frame:
                                            xysize (42, 42)
                                            background "#3a3a5aCC"

                                            if renpy.loadable(_icon_path):
                                                add _icon_path zoom 0.164 xalign 0.5 yalign 0.5
                                            else:
                                                text "[_icono]" size 22 xalign 0.5 yalign 0.5

                                        # Nombre y preview
                                        vbox:
                                            spacing 2

                                            text "[_nombre]" size 15 color "#ffffff" bold True

                                            if _ultimo:
                                                $ _texto_sub = renpy.substitute(renpy.translate_string(_ultimo.texto))
                                                $ _preview = _texto_sub[:35] + ("..." if len(_texto_sub) > 35 else "")
                                                text "[_preview]" size 12 color "#aaaaaa"
                                            else:
                                                text _("Sin mensajes") size 12 color "#666666"

                                        # Badge
                                        if _sin_leer > 0:
                                            frame:
                                                xalign 1.0
                                                yalign 0.5
                                                background "#FF4444"
                                                padding (6, 3)
                                                xminimum 24

                                                text "[_sin_leer]" size 12 color "#ffffff" bold True xalign 0.5


# =============================================================================
# PANTALLA DE CHAT
# =============================================================================

screen pantalla_chat(npc_id="monica"):
    """Vista de chat con un NPC — App Chat"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("pantalla_chat") if modo_ajuste_celular else None
    $ _chat = sistema_mensajes.chats.get(npc_id)
    $ _nombre = obtener_nombre_contacto(npc_id)

    # Marcar como leído al abrir
    if _chat:
        on "show" action Function(_chat.marcar_como_leido)

    # Timer para "escribiendo..."
    use _timer_escribiendo()

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header del chat con avatar
            frame:
                xsize ajuste_cel_area_w
                ysize 55
                background "#12122aFF"
                padding (10, 0)

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
                    $ _icon_path_header = "images/hud/pista_{}.png".format(npc_id)
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
                    ysize 1
                    yalign 1.0
                    background "#ffffff11"

            # Área de mensajes (scrollable)
            # Altura = area total - barra status(32) - header(55) - footer(100) - margen inferior(50)
            $ _chat_viewport_h = ajuste_cel_area_h - 32 - 55 - 100 - 50
            viewport:
                xsize ajuste_cel_area_w
                ysize _chat_viewport_h
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 6
                    xfill True
                    box_wrap False

                    null height 8

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
                                        xmaximum 420
                                        background "#1565C0CC"
                                        padding (10, 7)

                                        vbox:
                                            spacing 3
                                            if _msg.foto:
                                                imagebutton:
                                                    idle _msg.foto
                                                    hover _msg.foto
                                                    action Show("vista_foto_ampliada", foto=_msg.foto)
                                                    at transform:
                                                        zoom 0.3
                                            $ _texto_jugador = renpy.substitute(renpy.translate_string(_msg.texto))
                                            text "[_texto_jugador]" size 13 color "#ffffff" xalign 1.0
                            else:
                                # Burbuja del NPC (izquierda)
                                hbox:
                                    xfill True
                                    xalign 0.0

                                    frame:
                                        xalign 0.0
                                        xmaximum 420
                                        background "#1e1e3aCC"
                                        padding (10, 7)

                                        vbox:
                                            spacing 3
                                            text "[_nombre]" size 10 color "#8888bb" bold True
                                            if _msg.foto:
                                                imagebutton:
                                                    idle _msg.foto
                                                    hover _msg.foto
                                                    action Show("vista_foto_ampliada", foto=_msg.foto)
                                                    at transform:
                                                        zoom 0.3
                                            $ _texto_npc = renpy.substitute(renpy.translate_string(_msg.texto))
                                            text "[_texto_npc]" size 13 color "#dddddd"

                                    null
                    else:
                        text _("No hay mensajes aún") size 14 color "#666666" xalign 0.5 yalign 0.5

                    # Indicador "Escribiendo..."
                    if _msg_escribiendo and _msg_npc_chat_actual == npc_id:
                        hbox:
                            xfill True
                            xalign 0.0

                            frame:
                                xalign 0.0
                                background "#1e1e3aCC"
                                padding (10, 7)

                                hbox:
                                    spacing 5
                                    text "[_nombre]" size 10 color "#8888bb" bold True
                                    text _("escribiendo...") size 10 color "#8888bb" italic True

                    null height 8

            # Barra inferior
            frame:
                xsize ajuste_cel_area_w
                ysize 100
                background "#0a0a18FF"
                padding (15, 12)

                hbox:
                    xfill True
                    spacing 10

                    $ _puede_responder = _chat and _chat.puede_responder() and not _msg_escribiendo
                    $ _bg_color = "#4CAF50CC" if _puede_responder else "#1e1e3a66"
                    $ _hover_color = "#66BB6ACC" if _puede_responder else "#1e1e3a66"

                    button:
                        action (Function(_abrir_selector_respuesta, npc_id) if _puede_responder else NullAction())
                        xfill True
                        ysize 76
                        background _bg_color
                        hover_background _hover_color
                        padding (15, 10)
                        
                        hbox:
                            spacing 10
                            yalign 0.5
                            if not _puede_responder:
                                xalign 0.5

                            if _puede_responder:
                                text "📝" size 36 yalign 0.5
                                text _("Escribe un mensaje...") size 28 color "#ffffff" yalign 0.5
                            elif _chat and _chat.tiene_pendientes() and not _msg_escribiendo:
                                text _("[_nombre] responderá más tarde.") size 26 color "#888888" yalign 0.5
                            else:
                                text "—" size 28 color "#444444" yalign 0.5


# =============================================================================
# SELECTOR DE RESPUESTA
# =============================================================================

screen selector_respuesta(npc_id="monica"):
    """Selector de respuesta — overlay dentro del celular"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("selector_respuesta") if modo_ajuste_celular else None
    $ _chat = sistema_mensajes.chats.get(npc_id)

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
        padding (15, 15)

        vbox:
            spacing 10
            xfill True

            # Si hay grupo activo
            if _chat and _chat.grupo_activo:
                $ _grupo = _chat.grupo_activo
                $ _paso = _grupo.obtener_paso_actual()

                if _paso:
                    $ _opciones_visibles = [(i, op) for i, op in enumerate(_paso.opciones_jugador) if op.es_visible()]

                    text _("Elige tu respuesta:") size 14 color "#4FC3F7" bold True xalign 0.5

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
                                padding (12, 8)

                                $ _texto_opcion = renpy.substitute(renpy.translate_string(_opcion.texto))
                                text "[_texto_opcion]" size 13 color "#ffffff"

            elif _chat and len(_chat.grupos_pendientes) > 0:
                $ _grupos_visibles = [g for g in _chat.grupos_pendientes if _chat._horario_valido(g)]
                text _("¿A qué mensaje respondés?") size 14 color "#4FC3F7" bold True xalign 0.5

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
                            padding (12, 8)

                            text "\"[_preview_msg]\"" size 12 color "#aaaaaa" italic True

            # Cancelar
            textbutton "✖ Cancelar":
                action Hide("selector_respuesta")
                xalign 0.5
                text_size 13
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

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header
            use _celular_app_header("Resumen", "✉️", [Hide("resumen_recompensas"), Show("menu_celular")])

            # Contenido
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True

                frame:
                    xfill True
                    background None
                    padding (20, 15)

                    vbox:
                        spacing 15
                        xfill True

                        # Info
                        vbox:
                            spacing 5
                            xalign 0.5
                            text _("Conversación finalizada") size 18 color "#FFD700" bold True xalign 0.5
                            text _("Chat con [_nombre]") size 14 color "#aaaaaa" xalign 0.5

                        # Puntos
                        if puntos_totales:
                            frame:
                                xfill True
                                background "#1e1e3a88"
                                padding (15, 10)

                                vbox:
                                    spacing 6
                                    text _("Puntos obtenidos:") size 13 color "#8888bb" bold True

                                    for _cat, _pts in puntos_totales.items():
                                        hbox:
                                            spacing 8
                                            $ _cat_display = _cat.capitalize()
                                            text "  [_cat_display]:" size 13 color "#cccccc"
                                            text "[_pts]" size 13 color "#FFD700" bold True

                        # Recompensas
                        if recompensas:
                            frame:
                                xfill True
                                background "#1a2e1a88"
                                padding (15, 10)

                                vbox:
                                    spacing 6
                                    text _("🎁 Recompensas:") size 13 color "#4CAF50" bold True

                                    for _rec in recompensas:
                                        $ _tipo = _rec["recompensa"].get("tipo", "")
                                        $ _val = _rec["recompensa"].get("valor", 0)

                                        if _tipo == "amor":
                                            text "  +[_val] ❤️ Amor con [_nombre]" size 13 color "#4CAF50"
                                        elif _tipo == "deseo":
                                            text "  +[_val] 💋 Deseo con [_nombre]" size 13 color "#E91E63"
                                        elif _tipo == "dinero":
                                            text "  +$[_val]" size 13 color "#FFD700"
                                        elif _tipo == "foto":
                                            text _("  📷 Foto desbloqueada!") size 13 color "#2196F3"
                                        elif _tipo == "item":
                                            text _("  📦 Item obtenido!") size 13 color "#FF9800"
                                        elif _tipo == "stat":
                                            $ _stat_id = _rec["recompensa"].get("stat_id", "")
                                            text "  +[_val] [_stat_id]" size 13 color "#9C27B0"
                        elif not puntos_totales:
                            text _("Sin recompensas") size 13 color "#666666" xalign 0.5

                        # Cerrar
                        textbutton _("Cerrar"):
                            action Hide("resumen_recompensas")
                            xalign 0.5
                            text_size 14
                            background "#607D8B"
                            hover_background "#90A4AE"
                            padding (20, 8)
                            text_color "#ffffff"


# =============================================================================
# VISTA DE FOTO AMPLIADA
# =============================================================================

screen vista_foto_ampliada(foto):
    """Muestra una foto en tamaño completo — dentro del celular"""
    
    modal True
    
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
            xysize (ajuste_cel_area_w - 40, ajuste_cel_area_h - 80)
    
    # Botón cerrar dentro del celular
    textbutton "✖":
        action Hide("vista_foto_ampliada")
        xpos ajuste_cel_area_x + ajuste_cel_area_w - 50
        ypos ajuste_cel_area_y + 10
        text_size 28
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
        """Calcula duración del indicador 'escribiendo...' según longitud del texto."""
        if not texto:
            return 0.8
        longitud = len(texto)
        if longitud <= 20:
            return 0.8
        elif longitud <= 50:
            return 1.2
        elif longitud <= 100:
            return 1.8
        else:
            return 2.5

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
