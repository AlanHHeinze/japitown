################################################################################
## Sistema de Pistas de Quest y Eventos
################################################################################
## Panel visual para mostrar pistas de quests y eventos activos

# Variable para alternar entre pistas y qué hacer
default mostrar_que_hacer = False

screen panel_pistas():
    """Panel que muestra las quests y eventos activos — App Pistas"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_pistas") if modo_ajuste_celular else None

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("panel_pistas")

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
            use _celular_app_header(_("Pistas"), "📋", [Hide("panel_pistas"), Show("menu_celular")])

            # Toggle entre Pistas y Qué hacer
            frame:
                xfill True
                background "#12122aCC"
                padding (10, 8)

                hbox:
                    xalign 0.5
                    spacing 5

                    textbutton _("💡 Pistas"):
                        action SetVariable("mostrar_que_hacer", False)
                        text_size 14
                        if not mostrar_que_hacer:
                            background "#4CAF50"
                            text_color "#ffffff"
                        else:
                            background "#1e1e3aCC"
                            text_color "#aaaaaa"
                        padding (15, 8)

                    textbutton _("📍 Qué Hacer"):
                        action SetVariable("mostrar_que_hacer", True)
                        text_size 14
                        if mostrar_que_hacer:
                            background "#2196F3"
                            text_color "#ffffff"
                        else:
                            background "#1e1e3aCC"
                            text_color "#aaaaaa"
                        padding (15, 8)

            # Contenido scrollable — organizado por NPC
            python:
                _quests_activas = sistema_quests.obtener_quests_activas()
                _eventos_activos = sistema_events.obtener_events_visibles()

                # Mapa npc_id → (quest, [eventos])
                _quests_por_npc = {}
                for _q in _quests_activas:
                    _quests_por_npc[_q.npc_id] = _q

                _eventos_por_npc = {}
                for _e in _eventos_activos:
                    _nid = _e.npc_id or "__sin_npc__"
                    _eventos_por_npc.setdefault(_nid, []).append(_e)

                # NPCs conocidos ordenados por nombre
                _npcs_conocidos = [
                    _n for _n in sistema_npcs.npcs.values()
                    if _n.obtener_estado("conocido", False)
                ]
                _npcs_conocidos.sort(key=lambda _n: _n.nombre)

                _hay_algo = bool(_quests_activas or _eventos_activos or _npcs_conocidos)

            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (15, 10)

                    vbox:
                        spacing 10
                        xfill True

                        if _hay_algo:

                            # ── Un bloque por NPC conocido ──
                            for _npc_p in _npcs_conocidos:
                                $ _npc_quest = _quests_por_npc.get(_npc_p.id)
                                $ _npc_eventos = _eventos_por_npc.get(_npc_p.id, [])

                                # Bloque de quest (si tiene quest activa)
                                if _npc_quest:
                                    frame:
                                        background "#1e1e3aCC"
                                        padding (15, 12)
                                        xfill True

                                        hbox:
                                            spacing 15
                                            yalign 0.5

                                            $ _icon_q = f"images/hud/pista_{_npc_quest.npc_id}.png"
                                            if renpy.loadable(_icon_q):
                                                add _icon_q zoom 0.2
                                            else:
                                                frame:
                                                    xysize (52, 52)
                                                    background "#3a3a5a"
                                                    text "?" size 26 xalign 0.5 yalign 0.5 color "#ffffff"

                                            vbox:
                                                spacing 5

                                                $ _qtitulo = renpy.translate_string(_npc_quest.nombre) + " " + renpy.translate_string("(Quest)")
                                                text "[_qtitulo]" size 16 color "#FFD700" bold True

                                                $ _qmsg = _npc_quest.obtener_mensajes()
                                                $ _qmsg_txt = _qmsg["que_hacer"] if mostrar_que_hacer else _qmsg["pista"]
                                                $ _qmsg_sub = renpy.substitute(_qmsg_txt)
                                                text "[_qmsg_sub]" size 13 color "#cccccc"

                                                if mostrar_debug_hud:
                                                    $ _etapa_nombres = {1:"Inicialización",2:"Espera",3:"Condiciones",4:"Rutina",5:"Listo",6:"Validación",7:"Desarrollo",8:"Memorias",9:"Finalización"}
                                                    $ _etapa_txt = "Etapa {}: {}".format(_npc_quest.etapa_actual, _etapa_nombres.get(_npc_quest.etapa_actual, "?"))
                                                    text "[[" + _etapa_txt + "]]" size 11 color "#888888"

                                # Bloque "sin quest" (siempre que no haya quest activa)
                                else:
                                    frame:
                                        background "#1e1e3aCC"
                                        padding (15, 12)
                                        xfill True

                                        hbox:
                                            spacing 15
                                            yalign 0.5

                                            $ _icon_s = f"images/hud/pista_{_npc_p.id}.png"
                                            if renpy.loadable(_icon_s):
                                                add _icon_s zoom 0.2
                                            else:
                                                frame:
                                                    xysize (52, 52)
                                                    background "#3a3a5a"
                                                    text "?" size 26 xalign 0.5 yalign 0.5 color "#ffffff"

                                            vbox:
                                                spacing 5

                                                $ _ntitulo = renpy.translate_string(_npc_p.nombre)
                                                text "[_ntitulo]" size 16 color "#888888" bold True

                                                if not mostrar_que_hacer:
                                                    text _("Nuevo contenido en futuras actualizaciones.") size 13 color "#666666" italic True
                                                else:
                                                    text _("No hay acciones pendientes por ahora.") size 13 color "#666666" italic True

                                # Bloques de eventos (uno por evento, independiente de si hay quest)
                                for _ev in _npc_eventos:
                                    frame:
                                        background "#1a2a1aCC"
                                        padding (15, 12)
                                        xfill True

                                        hbox:
                                            spacing 15
                                            yalign 0.5

                                            $ _icon_ev = f"images/hud/pista_{_ev.npc_id}.png" if _ev.npc_id else ""
                                            if _icon_ev and renpy.loadable(_icon_ev):
                                                add _icon_ev zoom 0.2
                                            else:
                                                frame:
                                                    xysize (52, 52)
                                                    background "#1a3a1a"
                                                    text "⚡" size 26 xalign 0.5 yalign 0.5

                                            vbox:
                                                spacing 5

                                                $ _etitulo = renpy.translate_string(_ev.nombre) + " " + renpy.translate_string("(Evento)")
                                                text "[_etitulo]" size 16 color "#4CAF50" bold True

                                                $ _emsg = _ev.obtener_mensajes()
                                                $ _emsg_txt = _emsg["que_hacer"] if mostrar_que_hacer else _emsg["pista"]
                                                $ _emsg_sub = renpy.substitute(_emsg_txt)
                                                text "[_emsg_sub]" size 13 color "#cccccc"

                                                if _ev.condicion_cierre_texto:
                                                    hbox:
                                                        spacing 5
                                                        text "🔒" size 12
                                                        text renpy.translate_string(_ev.condicion_cierre_texto) size 12 color "#FF9800" italic True

                                                if mostrar_debug_hud:
                                                    $ _ev_estado = _ev.estado
                                                    text "[[Estado: [_ev_estado]]" size 11 color "#888888"

                            # Eventos sin NPC asociado
                            for _ev_libre in _eventos_por_npc.get("__sin_npc__", []):
                                frame:
                                    background "#1a2a1aCC"
                                    padding (15, 12)
                                    xfill True

                                    hbox:
                                        spacing 15
                                        yalign 0.5

                                        frame:
                                            xysize (52, 52)
                                            background "#1a3a1a"
                                            text "⚡" size 26 xalign 0.5 yalign 0.5

                                        vbox:
                                            spacing 5

                                            $ _etitulo_l = renpy.translate_string(_ev_libre.nombre) + " " + renpy.translate_string("(Evento)")
                                            text "[_etitulo_l]" size 16 color "#4CAF50" bold True

                                            $ _emsg_l = _ev_libre.obtener_mensajes()
                                            $ _emsg_l_txt = _emsg_l["que_hacer"] if mostrar_que_hacer else _emsg_l["pista"]
                                            $ _emsg_l_sub = renpy.substitute(_emsg_l_txt)
                                            text "[_emsg_l_sub]" size 13 color "#cccccc"

                        else:
                            null height 40
                            vbox:
                                spacing 10
                                xalign 0.5
                                text "🔍" size 48 xalign 0.5
                                text _("No hay actividades activas") size 16 color "#888888" xalign 0.5
                                text _("Explora y habla con los personajes") size 13 color "#666666" xalign 0.5


screen boton_pistas():
    """Botón flotante para abrir el panel de pistas"""
    
    # Obtener quests y eventos activos
    $ quests_activas = sistema_quests.obtener_quests_activas()
    $ eventos_activos = sistema_events.obtener_events_visibles()
    $ total_activos = len(quests_activas) + len(eventos_activos)
    $ _npcs_conocidos_btn = [n for n in sistema_npcs.npcs.values() if n.obtener_estado("conocido", False)]
    
    if total_activos > 0 or _npcs_conocidos_btn:
        frame:
            xalign 1.0
            yalign 0.0
            xoffset -180
            yoffset 10
            background "#9C27B0BB"
            padding (15, 10)
            
            textbutton _("📋 Pistas ([total_activos])"):
                action Show("panel_pistas")
                text_size 18
                text_color "#ffffff"
                text_bold True
                background None
                hover_background None


################################################################################
## Screen de mensajes de validación fallida
################################################################################

screen mensaje_validacion_fallida(mensajes):
    """Muestra los mensajes cuando la validación de quest falla"""
    
    modal True
    
    # Fondo oscuro
    add Solid("#000000CC")
    
    frame:
        xalign 0.5
        yalign 0.5
        background "#2d1f1fEE"
        padding (40, 30)
        minimum (500, 200)
        
        vbox:
            spacing 20
            xalign 0.5
            
            # Título
            hbox:
                xalign 0.5
                spacing 10
                text "⚠️" size 28
                text _("No puedo hacer esto aún...") size 24 color "#FF6B6B" bold True
            
            null height 10
            
            # Lista de requisitos faltantes
            for mensaje in mensajes:
                frame:
                    background "#3d2f2fCC"
                    padding (20, 12)
                    xfill True
                    
                    hbox:
                        spacing 15
                        text "•" size 18 color "#FF6B6B"
                        $ mensaje_sub = renpy.substitute(renpy.translate_string(mensaje))
                        text "[mensaje_sub]" size 16 color "#ffcccc"
            
            null height 15
            
            # Botón cerrar
            textbutton _("Entendido"):
                action Hide("mensaje_validacion_fallida")
                xalign 0.5
                text_size 18
                background "#607D8B"
                hover_background "#90A4AE"
                padding (30, 12)
