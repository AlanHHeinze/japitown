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
            quest_v0 = store.sistema_quests.obtener_quest("violet_questprincipal_0")
            if quest_v0 and quest_v0.activa and not quest_v0.completada and store.horario_actual == 1:
                opciones.append({"texto": "Intentar hablar", "label": "quest_violet_questprincipal_0", "ocultar_golpear": True})

            # Quest 2: Dar paquete
            if "mangas_violet" in store.inventario and store.inventario.get("mangas_violet", 0) > 0:
                opciones.append({"texto": "Dar paquete", "label": "dar_paquete_quest02_violet"})

            # Quest 4: Despertar a Violet para limpiar (sabado mañana, quest lista pero no iniciada)
            quest_v3 = store.sistema_quests.obtener_quest("violet_questprincipal_4")
            if quest_v3 and quest_v3.activa and not quest_v3.completada and quest_v3.etapa_actual == ETAPA_BOTON_LISTO and store.dia_semana_actual == 5 and store.horario_actual == 0:
                opciones.append({"texto": "Despertar a Violet para limpiar", "label": "quest_violet_questprincipal_4", "ocultar_golpear": True})

        return opciones

    def puede_hablar_puerta(npc_id):
        """
        Verifica si el jugador puede entrar a hablar con el NPC.
        Por defecto True, excepto Violet que requiere 30+ de relacion.
        """
        if npc_id == "violet":
            return obtener_stat1("violet") >= 30
        return True


################################################################################
## Screen del Menu de Puerta
################################################################################

screen menu_puerta_npc(npc_id, opciones_especiales):
    """
    Menu de interaccion en la puerta de un NPC.
    Muestra background del pasillo, opciones con estilo choice de Ren'Py.
    """

    modal True

    # Fondo con el background del pasillo
    $ _bg_pasillo_menu = obtener_bg_pasillo_npc(npc_id)
    if _bg_pasillo_menu:
        add _bg_pasillo_menu

    # Overlay semi-transparente
    add Solid("#00000088")

    # Menu de opciones - Mismo layout que screen choice
    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        # Opciones especiales
        for opcion in opciones_especiales:
            textbutton opcion.get("texto", "Opcion"):
                style "choice_button"
                action [Hide("menu_puerta_npc"),
                        Return(("opcion_especial", opcion.get("label", "game_loop")))]

        # Opcion: Golpear la puerta (ocultar si una opcion especial lo indica)
        $ _ocultar_golpear = any(op.get("ocultar_golpear", False) for op in opciones_especiales)
        if not _ocultar_golpear:
            textbutton "Golpear la puerta":
                style "choice_button"
                action [Hide("menu_puerta_npc"),
                        Return("golpear")]

        # Opcion: Volver
        textbutton "Volver":
            style "choice_button"
            action [Hide("menu_puerta_npc"),
                    Return("volver")]


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

    # Verificar si NPC esta en su habitacion
    $ _npc_obj = obtener_npc(_npc_habitacion)
    $ _habitacion_id = "casa_h" + _npc_habitacion
    $ _npc_presente = _npc_obj and _npc_obj.esta_en_locacion(_habitacion_id)

    if not _npc_presente:
        # NPC no esta — mostrar mensaje y no entrar
        $ _msg_ausente = MENSAJES_AUSENTE.get(_npc_habitacion, "No hay nadie.")
        $ _msg_ausente = renpy.translate_string(_msg_ausente)
        piensa "[_msg_ausente]"
        return

    # Trasnoche — no molestar
    if store.horario_actual == 3:
        piensa "Debe estar durmiendo, no voy a molestar."
        return

    # NPC esta presente — ocultar HUD y preparar interaccion
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

        # Verificar si puede hablar (relacion)
        if not puede_hablar_puerta(_npc_habitacion):
            # Violet sin suficiente relacion
            if _npc_habitacion == "violet":
                violet "Estoy ocupada."
            $ mostrar_hud()
            return

        # NPC responde adelante y el jugador entra
        if _npc_habitacion == "violet":
            violet "Adelante."
        elif _npc_habitacion == "jasmine":
            jasmine "Adelante."
        elif _npc_habitacion == "monica":
            monica "Adelante."

        $ sistema_locaciones.mover_a_locacion(_destino_puerta)
        $ mostrar_hud()
        return

    # "volver"
    $ mostrar_hud()
    return
