################################################################################
## Sistema de Talk — Labels
################################################################################

label talk_iniciar:

    $ _msg_r = accion_bloqueada("hablar")
    if _msg_r:
        piensa "[_msg_r]"
        return

    $ _t_npc = obtener_npc(_npc_id_temp)
    if not _t_npc:
        return

    $ _t_config = sistema_talk.obtener_config(_npc_id_temp)
    if not _t_config:
        return

    if not _t_npc.puede_interactuar("hablar"):
        "Ya conversaste con [_t_npc.nombre] hoy."
        return

    $ _t_npc.talk_reconsiderar_usado = False

    $ _t_estado = sistema_talk.obtener_estado_activo(_npc_id_temp)
    $ _t_especiales = _t_config.obtener_opciones_especiales_disponibles()

    # Carisma ≥2: preview de una opción desconocida en el menú
    $ _t_preview_opcion = None
    $ _t_preview_resultado = None
    if store.mc_carisma >= 2 and _t_estado:
        $ _t_sin_mem = [
            o for o in OPCIONES_BASE_IDS
            if sistema_talk.consultar_memoria_mc(_npc_id_temp, _t_estado.id, o) is None
        ]
        if _t_sin_mem:
            $ _t_preview_opcion = renpy.random.choice(_t_sin_mem)
            $ _t_preview_resultado = _t_estado.obtener_resultado(_t_preview_opcion)

    # Escena de conversación
    $ ocultar_hud()
    $ _t_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _t_bg

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    $ _t_sprite = obtener_sprite_menu_npc(_npc_id_temp)
    show expression _t_sprite as talk_npc_sprite at right

    window show

    # Narrador presenta el estado actual del NPC (persiste durante el menú)
    if _t_estado and _t_estado.intro:
        $ _t_intro_tr = renpy.translate_string(_t_estado.intro)
        "[_t_intro_tr]" (interact=False)

    # Loop de menú — permite reconsiderar
    label .menu:

    python:
        _t_items = []
        _t_cheat = getattr(persistent, "mostrar_recompensa", False)
        for opcion_id in OPCIONES_BASE_IDS:
            texto = renpy.translate_string(OPCIONES_BASE_TEXTO[opcion_id])
            if _t_cheat and _t_estado:
                _t_res_id = _t_estado.obtener_resultado(opcion_id)
                _t_res_txt = RESULTADO_TEXTO.get(_t_res_id, "?")
                caption = u"{} {{color=#A5D6A7}}{}{{/color}} {{color=#FF9800}}(Cheat){{/color}}".format(texto, _t_res_txt)
            else:
                recordado = sistema_talk.consultar_memoria_mc(_npc_id_temp, _t_estado.id, opcion_id) if _t_estado else None
                if recordado:
                    resultado_texto = RESULTADO_TEXTO[recordado]
                    caption = u"{} {{color=#A5D6A7}}{}{{/color}}".format(texto, resultado_texto)
                elif opcion_id == _t_preview_opcion:
                    resultado_texto = RESULTADO_TEXTO[_t_preview_resultado]
                    caption = u"{} {{color=#FFF176}}{}?{{/color}}".format(texto, resultado_texto)
                else:
                    caption = texto
            _t_items.append((caption, opcion_id))

        for oesp in _t_especiales:
            _t_items.append((renpy.translate_string(oesp.texto), ("especial", oesp)))

    $ _t_eleccion = renpy.display_menu(_t_items)

    $ _t_es_especial = isinstance(_t_eleccion, tuple) and _t_eleccion[0] == "especial"

    if _t_es_especial:
        $ _t_oesp = _t_eleccion[1]
        $ _t_resultado_id = _t_oesp.resultado_id if _t_oesp.resultado_id else "nada"
        $ _t_opcion_id = None
        if _t_oesp.item_consumible and _t_oesp.item_requerido:
            $ inventario[_t_oesp.item_requerido] = max(0, inventario.get(_t_oesp.item_requerido, 0) - 1)
    else:
        $ _t_opcion_id = _t_eleccion
        $ _t_resultado_id = _t_estado.obtener_resultado(_t_opcion_id) if _t_estado else "nada"
        $ _t_oesp = None

    # Reconsiderar: carisma ≥5, resultado negativo, primer uso en esta interacción
    if not _t_es_especial and _t_resultado_id in ["-2_amor", "-1_deseo"]:
        if store.mc_carisma >= 5 and not _t_npc.talk_reconsiderar_usado:
            $ _t_npc.talk_reconsiderar_usado = True
            piensa "No creo que esto dé buen resultado..."
            jump .menu

    $ _t_npc.registrar_interaccion("hablar")

    if _t_resultado_id and _t_resultado_id != "nada":
        $ _t_stat_info = RESULTADO_A_STAT.get(_t_resultado_id)
        if _t_stat_info:
            $ _t_npc.modificar_stat(_t_stat_info[0], _t_stat_info[1])

    # Resultado: 4 partes en un solo bloque de texto
    python:
        _t_partes = []
        _t_en = (renpy.game.preferences.language or "") == "english"

        # Parte 1: mensaje dinámico con horario y locación
        _t_loc_actual = store.sistema_locaciones.locacion_actual
        _t_loc_id = _t_loc_actual.id if _t_loc_actual else ""

        if _t_en:
            _t_horario_txt = _TALK_HORARIO_NOMBRES_EN.get(store.horario_actual, "day")
            if _t_loc_id == "casa_hmc":
                _t_loc_txt = "your room"
            elif _t_loc_id in _TALK_HABITACIONES_DUENO:
                _t_dueno_id = _TALK_HABITACIONES_DUENO[_t_loc_id]
                if _t_dueno_id == _npc_id_temp:
                    _t_loc_txt = "her room"
                else:
                    _t_dueno_npc = obtener_npc(_t_dueno_id)
                    _t_loc_txt = (_t_dueno_npc.nombre if _t_dueno_npc else _t_dueno_id) + "'s room"
            else:
                _t_loc_txt = _TALK_LOCACIONES_NOMBRES_EN.get(_t_loc_id, "this place")
            _t_partes.append("You took advantage of the {} to talk to {} in {}.".format(
                _t_horario_txt, _t_npc.nombre, _t_loc_txt
            ))
        else:
            _t_horario_txt = _TALK_HORARIO_NOMBRES.get(store.horario_actual, "día")
            if _t_loc_id == "casa_hmc":
                _t_loc_txt = "tu habitación"
            elif _t_loc_id in _TALK_HABITACIONES_DUENO:
                _t_dueno_id = _TALK_HABITACIONES_DUENO[_t_loc_id]
                if _t_dueno_id == _npc_id_temp:
                    _t_loc_txt = "su habitación"
                else:
                    _t_dueno_npc = obtener_npc(_t_dueno_id)
                    _t_loc_txt = "la habitación de " + (_t_dueno_npc.nombre if _t_dueno_npc else _t_dueno_id)
            else:
                _t_loc_txt = _TALK_LOCACIONES_NOMBRES.get(_t_loc_id, "este lugar")
            _t_partes.append("Aprovechaste la {} para hablar con {} en {}.".format(
                _t_horario_txt, _t_npc.nombre, _t_loc_txt
            ))

        if _t_es_especial:
            _t_msg2 = renpy.translate_string(_t_oesp.mensaje_opcion)
        else:
            _t_msg2 = renpy.translate_string(_t_config.mensajes_opciones.get(_t_opcion_id, ""))
        if _t_msg2:
            _t_partes.append(_t_msg2)
        if _t_estado and _t_estado.mensaje:
            _t_partes.append(renpy.translate_string(_t_estado.mensaje))
        if _t_es_especial and _t_oesp.id in _t_config.resoluciones_especiales:
            _t_msg4 = renpy.translate_string(_t_config.resoluciones_especiales[_t_oesp.id])
        else:
            _t_msg4 = renpy.translate_string(_t_config.resoluciones.get(_t_resultado_id, ""))
        if _t_msg4:
            _t_partes.append(_t_msg4)
        _t_limpias = []
        for _i, _p in enumerate(_t_partes):
            _p = _p.rstrip(".,")
            if _i > 0 and _p:
                _p = _p[0].lower() + _p[1:]
            _t_limpias.append(_p)
        _t_resultado_texto = " ".join(_t_limpias)

    # Expresión del NPC según resultado y skin actual
    if _t_resultado_id != "nada":
        python:
            _t_facial = _TALK_EXPRESION_FACIAL.get((_npc_id_temp, _t_resultado_id))
            _t_skin_activo = obtener_skin_activo(_npc_id_temp)
            _t_skin_id = _t_skin_activo.id if _t_skin_activo else None
            _t_skin_data = _TALK_SKIN_CUERPO.get(_t_skin_id)
            if _t_facial and _t_skin_data:
                _t_b, _t_o = _t_facial
                _t_img, _t_c_base, _t_c_caliente = _t_skin_data
                _t_c = _t_c_caliente if _t_resultado_id == "+1_deseo" else _t_c_base
                renpy.show(
                    (_t_img, _t_b, _t_o, _t_c),
                    tag="talk_npc_sprite",
                    at_list=[right])
                renpy.with_statement(dissolve)

    "[_t_resultado_texto]"

    if not _t_es_especial and _t_estado and _t_opcion_id:
        $ sistema_talk.actualizar_memoria_mc(_npc_id_temp, _t_estado.id, _t_opcion_id, _t_resultado_id)

    $ sistema_talk.asignar_estado_posterior(_npc_id_temp, _t_resultado_id, _t_estado, _t_oesp)

    if _t_estado and _t_estado.es_especial:
        $ sistema_talk.consumir_estado_especial(_npc_id_temp)

    if _t_es_especial and _t_oesp.recompensa_extra:
        $ _t_oesp.recompensa_extra()

    hide talk_npc_sprite
    hide mc_parado_base
    scene black with dissolve

    $ avanzar_horario()
    $ mostrar_hud()
    return
