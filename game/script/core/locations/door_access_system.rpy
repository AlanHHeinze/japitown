################################################################################
## Sistema de Control de Acceso a Habitaciones NPC
################################################################################
## Controla el acceso a habitaciones de NPCs basado en presencia
## Muestra menu de interaccion en la puerta con opciones especiales

# Mapeo de habitaciones a NPCs
define HABITACION_NPC = {
    "casa_hmonica": "monica",
    "casa_hviolet": "violet",
    "casa_hjasmine": "jasmine"
}

# Mapeo de NPC al pasillo correspondiente
define PASILLO_NPC = {
    "monica": "casa_pasilloabajo",
    "violet": "casa_pasilloarriba",
    "jasmine": "casa_pasilloarriba"
}

# Mensaje cuando NPC no esta
define MENSAJES_AUSENTE = {
    "violet": "Violet no esta en su habitacion.",
    "jasmine": "Jasmine no esta en su habitacion.",
    "monica": "Monica no esta en su habitacion."
}

init python:

    def obtener_npc_habitacion(destino_id):
        """
        Obtiene el ID del NPC dueño de una habitación.
        """
        return HABITACION_NPC.get(destino_id, None)

    def retornar_npcs_pasillo_al_salir(locacion_salida_id):
        """
        Llamada al salir de un pasillo: si algún NPC está ahí por door access
        (no por rutina), lo devuelve automáticamente a su habitación.
        """
        if locacion_salida_id not in ("casa_pasilloarriba", "casa_pasilloabajo"):
            return
        for npc_id, pasillo_id in PASILLO_NPC.items():
            if pasillo_id != locacion_salida_id:
                continue
            npc_obj = obtener_npc(npc_id)
            if not npc_obj or npc_obj.locacion_actual != locacion_salida_id:
                continue
            loc_rutina = npc_obj.obtener_locacion_rutina()
            if loc_rutina and loc_rutina != locacion_salida_id:
                npc_obj.locacion_actual = loc_rutina

    def obtener_bg_pasillo_npc(npc_id):
        """
        Obtiene el background del pasillo correspondiente al NPC
        con el horario actual.
        """
        pasillo_id = PASILLO_NPC.get(npc_id)
        if pasillo_id and hasattr(store, 'sistema_locaciones'):
            loc = store.sistema_locaciones.obtener_locacion(pasillo_id)
            if loc:
                return loc.background
        return None

    def obtener_opciones_puerta(npc_id):
        """
        Construye las opciones especiales del menu de puerta para un NPC.

        Returns:
            list: Lista de dicts {"texto": str, "label": str, "ocultar_golpear": bool}
        """
        opciones = []

        if npc_id == "violet":
            # Quest 0: Intentar hablar (solo por la tarde)
            quest_v0 = store.sistema_quests.obtener_quest("violet_questprincipal_0_b")
            if quest_v0 and quest_v0.activa and not quest_v0.completada and store.horario_actual == 1:
                opciones.append({"texto": "Intentar hablar", "label": "quest_violet_questprincipal_0_b", "ocultar_golpear": True})

            # Quest 2: Dar paquete
            if "mangas_violet" in store.inventario and store.inventario.get("mangas_violet", 0) > 0:
                opciones.append({"texto": "Dar paquete", "label": "dar_paquete_quest02_violet"})

            # Quest 02_a: Pedir mangas prestados
            quest_v02a = store.sistema_quests.obtener_quest("violet_questprincipal_02_a")
            if quest_v02a and quest_v02a.activa and not quest_v02a.completada and quest_v02a.etapa_actual == ETAPA_BOTON_LISTO:
                if not getattr(store, 'violet_quest02a_primer_intento_hecho', False) or obtener_stat1("violet") >= 10:
                    opciones.append({"texto": "Pedir mangas prestados", "label": "quest_violet_questprincipal_02_a", "ocultar_golpear": True})

            # Quest 03_a: Devolver mangas (Violet en su habitacion)
            quest_v03a = store.sistema_quests.obtener_quest("violet_questprincipal_03_a")
            if quest_v03a and quest_v03a.activa and not quest_v03a.completada and quest_v03a.etapa_actual == ETAPA_BOTON_LISTO:
                if "mangas_violet_mc" in store.inventario and store.inventario.get("mangas_violet_mc", 0) > 0:
                    opciones.append({"texto": "Devolver mangas", "label": "quest_violet_questprincipal_03_a", "ocultar_golpear": True})

            # Quest 02_b: Vengo por los mangas (por la noche)
            quest_v02b = store.sistema_quests.obtener_quest("violet_questprincipal_02_b")
            if quest_v02b and quest_v02b.activa and not quest_v02b.completada and quest_v02b.etapa_actual == ETAPA_BOTON_LISTO and store.horario_actual == 2:
                opciones.append({"texto": "Vengo por los mangas", "label": "quest_violet_questprincipal_02_b", "ocultar_golpear": True})

            # Quest 04_b: Violet sale al pasillo cuando el MC golpea
            quest_v04b = store.sistema_quests.obtener_quest("violet_questprincipal_04_b")
            if quest_v04b and quest_v04b.activa and not quest_v04b.completada and quest_v04b.etapa_actual == ETAPA_BOTON_LISTO:
                opciones.append({"texto": "Golpear la puerta", "label": "violet_quest04b_puerta", "ocultar_golpear": True})

            # Quest 05_a: Hablar con Violet sobre los cosplays (sale al pasillo)
            quest_v05a = store.sistema_quests.obtener_quest("violet_questprincipal_05_a")
            if quest_v05a and quest_v05a.activa and not quest_v05a.completada and quest_v05a.etapa_actual == ETAPA_BOTON_LISTO:
                if store.sistema_mensajes.grupo_completado("coxplay_q5a_g4"):
                    opciones.append({"texto": "Ya compré los cosplay", "label": "violet_quest05a_puerta", "ocultar_golpear": True})

            # Quest 05_b: Dar la Coxplay Box a Violet (sale al pasillo)
            quest_v05b = store.sistema_quests.obtener_quest("violet_questprincipal_05_b")
            if quest_v05b and quest_v05b.activa and not quest_v05b.completada and quest_v05b.etapa_actual == ETAPA_BOTON_LISTO:
                opciones.append({"texto": "Llegaron los cosplay", "label": "violet_quest05b_puerta", "ocultar_golpear": True})

            # Quest 05_c: Pedirle perdón a Violet (entra a la habitación)
            quest_v05c = store.sistema_quests.obtener_quest("violet_questprincipal_05_c")
            if quest_v05c and quest_v05c.activa and not quest_v05c.completada and quest_v05c.etapa_actual == ETAPA_BOTON_LISTO:
                opciones.append({"texto": "Pedirle perdón", "label": "violet_quest05c_puerta", "ocultar_golpear": True})

            # Quest 06_a: Contarle de las entradas (Violet en habitación, de noche)
            quest_v06a = store.sistema_quests.obtener_quest("violet_questprincipal_06_a")
            if quest_v06a and quest_v06a.activa and not quest_v06a.completada and quest_v06a.etapa_actual == ETAPA_BOTON_LISTO and store.horario_actual == 2:
                opciones.append({"texto": "Tengo las entradas", "label": "violet_quest06a_puerta", "ocultar_golpear": True})

            # Quest 06_b: Me pediste que pasara (solo de noche)
            quest_v06b = store.sistema_quests.obtener_quest("violet_questprincipal_06_b")
            if quest_v06b and quest_v06b.activa and not quest_v06b.completada and quest_v06b.etapa_actual == ETAPA_BOTON_LISTO and store.horario_actual == 2:
                opciones.append({"texto": "Me pediste que pasara", "label": "violet_quest06b_puerta", "ocultar_golpear": True})

            # Quest 07_a: Preguntar por el cosplay
            quest_v07a = store.sistema_quests.obtener_quest("violet_questprincipal_07_a")
            if quest_v07a and quest_v07a.activa and not quest_v07a.completada and quest_v07a.etapa_actual == ETAPA_BOTON_LISTO:
                opciones.append({"texto": "Preguntar por el cosplay", "label": "violet_quest07a_puerta", "ocultar_golpear": True})

            # Quest 07_b: Ya hablé con la tienda
            quest_v07b = store.sistema_quests.obtener_quest("violet_questprincipal_07_b")
            if quest_v07b and quest_v07b.activa and not quest_v07b.completada and quest_v07b.etapa_actual == ETAPA_BOTON_LISTO:
                opciones.append({"texto": "Ya hablé con la tienda", "label": "violet_quest07b_puerta", "ocultar_golpear": True})

            # Evento 03: Despertar a Violet para limpiar (sabado mañana)
            event_limpieza = store.sistema_events.obtener_event("violet_evento_03")
            if event_limpieza and event_limpieza.estado == ESTADO_EVENT_ACTIVO and store.dia_semana_actual == 5 and store.horario_actual == 0:
                opciones.append({"texto": "Despertar a Violet para limpiar", "label": "evento03_violet", "ocultar_golpear": True, "tipo": "evento"})

        return opciones

    def obtener_npc_en_banio(banio_id):
        """Retorna el NPC que está actualmente en el baño indicado, o None."""
        if not hasattr(store, 'sistema_npcs'):
            return None
        for npc in store.sistema_npcs.npcs.values():
            if npc.locacion_actual == banio_id:
                return npc
        return None



################################################################################
## Screen del Menu de Puerta
################################################################################

screen menu_puerta_npc(npc_id, opciones_especiales, bg_path=None):
    # bg_path: None = usar pasillo del NPC (por defecto)
    #          False = no mostrar background (usar el que ya está en escena)

    modal True

    # Fondo
    $ _bg_puerta_final = bg_path if bg_path is not None else obtener_bg_pasillo_npc(npc_id)
    if _bg_puerta_final:
        add _bg_puerta_final

    # Overlay semi-transparente
    add Solid("#00000088")

    # ¿Alguna opción especial pide ocultar el botón de golpear?
    # (quests cuya interacción reemplaza al golpe normal de puerta)
    $ _ocultar_golpear = any(o.get("ocultar_golpear", False) for o in opciones_especiales)

    # Menu de opciones - Mismo layout que screen choice
    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        # Golpear la puerta — siempre primero, salvo que una quest lo oculte
        if not _ocultar_golpear:
            textbutton "Golpear la puerta":
                style "choice_button"
                action [Hide("menu_puerta_npc"),
                        Return("golpear")]

        # Opciones especiales de quest/evento
        for opcion in opciones_especiales:
            $ _tag_opcion = " (Evento)" if opcion.get("tipo") == "evento" else " (Quest)"
            textbutton (renpy.translate_string(opcion.get("texto", "Opcion")) + _tag_opcion):
                style "choice_button"
                action [Hide("menu_puerta_npc"),
                        Return(("opcion_especial", opcion.get("label", "game_loop")))]

        # Volver — siempre al final
        textbutton "Volver":
            style "choice_button"
            action [Hide("menu_puerta_npc"),
                    Return("volver")]


################################################################################
## Screen del Menu de Baño
################################################################################

screen menu_banio_npc(npc_id, bg_path=None):
    modal True

    if bg_path:
        add bg_path

    add Solid("#00000088")

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Golpear la puerta":
            style "choice_button"
            action [Hide("menu_banio_npc"), Return("golpear")]

        textbutton "Espiar (Contenido en desarrollo)":
            style "choice_button"
            sensitive False
            action NullAction()

        textbutton "Entrar (Contenido en desarrollo)":
            style "choice_button"
            sensitive False
            action NullAction()

        textbutton "Volver":
            style "choice_button"
            action [Hide("menu_banio_npc"), Return("volver")]


################################################################################
## Labels del Sistema de Acceso
################################################################################

# Label completo de interaccion con puerta (se usa con jump, no call)
# _destino_puerta debe estar seteado antes de saltar aqui
label interaccion_puerta_npc:
    # Obtener NPC de la habitación destino
    $ _npc_habitacion = obtener_npc_habitacion(_destino_puerta)

    if not _npc_habitacion:
        # No es habitacion de NPC, mover directamente
        $ sistema_locaciones.mover_a_locacion(_destino_puerta)
        return

    $ _npc_obj = obtener_npc(_npc_habitacion)
    $ _habitacion_id = "casa_h" + _npc_habitacion
    $ _npc_presente = _npc_obj and _npc_obj.esta_en_locacion(_habitacion_id)

    # Quest 09_a: interacción de puerta especial durante la enfermedad de Violet
    $ _quest_v09a_door = store.sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if (_quest_v09a_door and _quest_v09a_door.activa and not _quest_v09a_door.completada and
            _quest_v09a_door.etapa_actual == ETAPA_BOTON_LISTO and
            _npc_habitacion == "violet"):
        jump violet_quest09a_manejo_puerta

    # Trasnoche: ingreso_noche requiere que el NPC esté presente
    if store.horario_actual == 3:
        $ _nivel_trasnoche = verificar_nivel_acceso_habitacion(_npc_habitacion)
        if _nivel_trasnoche == "ingreso_noche" and _npc_presente:
            $ sistema_locaciones.mover_a_locacion(_destino_puerta)
            $ mostrar_hud()
            return
        else:
            piensa "Debe estar durmiendo, no voy a molestar."
            return

    # Verificar nivel de acceso diurno
    $ _nivel_acceso = verificar_nivel_acceso_habitacion(_npc_habitacion)

    # Ingreso diurno: acceso libre — entra sin importar si el NPC está presente
    if _nivel_acceso == "ingreso_diurno":
        $ sistema_locaciones.mover_a_locacion(_destino_puerta)
        $ mostrar_hud()
        return

    # Para todos los niveles inferiores el NPC debe estar en su habitacion
    if not _npc_presente:
        $ _loc_npc_actual = _npc_obj.locacion_actual if _npc_obj else None

        if _loc_npc_actual == "fuera":
            # Salió de la casa — mensaje directo
            $ _npc_nombre_door = _npc_obj.nombre if _npc_obj else ""
            piensa "Parece que [_npc_nombre_door] no está en casa, debe haber salido."
            return

        else:
            # Ausente por rutina normal, quest, u otra razón
            $ _msg_ausente = MENSAJES_AUSENTE.get(_npc_habitacion, "No hay nadie.")
            $ _msg_ausente = renpy.translate_string(_msg_ausente)
            piensa "[_msg_ausente]"
            return

    # NPC presente — ocultar HUD y preparar interaccion
    $ ocultar_hud()
    hide screen hud_navegacion
    window hide

    # Mostrar background del pasillo correspondiente
    $ _bg_pasillo = obtener_bg_pasillo_npc(_npc_habitacion)
    scene expression _bg_pasillo with fade

    # Obtener opciones especiales y mostrar menu
    $ _opciones_puerta_list = obtener_opciones_puerta(_npc_habitacion)
    call screen menu_puerta_npc(_npc_habitacion, _opciones_puerta_list)

    # Procesar resultado del menu
    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        # Opcion especial: ejecutar el label correspondiente limpiando el HUD
        $ _label_opcion = _return[1]
        $ mostrar_hud()
        jump expression _label_opcion

    if _return == "golpear":
        # Sonido de tocar puerta
        play sound "audio/sfx/door_knock_3.ogg"
        pause 0.5

        # Caso especial: Violet los sabados por la mañana esta dormida
        if _npc_habitacion == "violet" and store.dia_semana_actual == 5 and store.horario_actual == 0:
            piensa "Violet debe estar dormida."
            $ mostrar_hud()
            return

        # Dispatch por nivel de acceso
        if _nivel_acceso == "dejar_pasar":
            jump interaccion_golpear_dejar_pasar
        elif _nivel_acceso == "sale_pasillo":
            jump interaccion_golpear_sale_pasillo
        else:
            # Sin nivel suficiente — NPC dice que está ocupada
            $ _msg_ocupada = MENSAJES_NPC_PUERTA.get(_npc_habitacion, {}).get("ocupada", "Estoy ocupada.")
            if _npc_habitacion == "violet":
                violet "[_msg_ocupada]"
            elif _npc_habitacion == "jasmine":
                jasmine "[_msg_ocupada]"
            elif _npc_habitacion == "monica":
                monica "[_msg_ocupada]"
            $ mostrar_hud()
            return

    # "volver"
    $ mostrar_hud()
    return


label interaccion_golpear_dejar_pasar:
    # NPC dice "Adelante" y el jugador entra directamente
    $ _msg_adelante = MENSAJES_NPC_PUERTA.get(_npc_habitacion, {}).get("adelante", "Adelante.")
    if _npc_habitacion == "violet":
        violet "[_msg_adelante]"
    elif _npc_habitacion == "jasmine":
        jasmine "[_msg_adelante]"
    elif _npc_habitacion == "monica":
        monica "[_msg_adelante]"
    $ sistema_locaciones.mover_a_locacion(_destino_puerta)
    $ mostrar_hud()
    return


label interaccion_golpear_sale_pasillo:
    # NPC dice "Ahí salgo" y se mueve al pasillo
    $ _msg_ahi_salgo = MENSAJES_NPC_PUERTA.get(_npc_habitacion, {}).get("ahi_salgo", "Ahí salgo.")
    if _npc_habitacion == "violet":
        violet "[_msg_ahi_salgo]"
    elif _npc_habitacion == "jasmine":
        jasmine "[_msg_ahi_salgo]"
    elif _npc_habitacion == "monica":
        monica "[_msg_ahi_salgo]"
    pause 0.5
    $ _pasillo_destino = PASILLO_NPC.get(_npc_habitacion)
    $ sistema_locaciones.mover_a_locacion(_pasillo_destino)
    if _pasillo_destino and _npc_obj:
        $ _npc_obj.locacion_actual = _pasillo_destino
    $ mostrar_hud()
    return


label interaccion_banio_ocupado:
    # El NPC ya puede haber terminado — re-verificar
    $ _npc_banio_obj = obtener_npc_en_banio(_destino_banio_npc)

    if not _npc_banio_obj:
        # Baño libre — entrar normalmente
        $ sistema_locaciones.mover_a_locacion(_destino_banio_npc)
        return

    $ ocultar_hud()
    hide screen hud_navegacion
    window hide

    # Usar el background de la locación actual del jugador (hallway o habitación)
    $ _bg_banio_frente = store.sistema_locaciones.locacion_actual.background if store.sistema_locaciones.locacion_actual else None

    call screen menu_banio_npc(_npc_banio_obj.id, bg_path=_bg_banio_frente)

    if _return == "golpear":
        play sound "audio/sfx/door_knock_3.ogg"
        pause 0.5
        if _npc_banio_obj.id == "violet":
            violet "Me estoy bañando."
        elif _npc_banio_obj.id == "jasmine":
            jasmine "Me estoy bañando."
        elif _npc_banio_obj.id == "monica":
            monica "Me estoy bañando."

    $ mostrar_hud()
    return
