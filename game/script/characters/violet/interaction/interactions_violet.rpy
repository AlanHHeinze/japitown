################################################################################
## Interacciones de Violet
################################################################################

# Variable temporal para preview de skin
default _skin_preview_violet = None

label interaccion_violet:
    # Guardar NPC actual
    $ _npc_actual = obtener_npc("violet")

    if not _npc_actual:
        return

    # Verificar si hay quest lista para ejecutar
    $ _quest_activa = sistema_quests.obtener_quest_activa("violet")

    if _quest_activa and _quest_activa.etapa_actual == 5:
        # Quest 2 usa opciones_extra en vez de auto-trigger
        if _quest_activa.id != "violet_questprincipal_6":
            $ exito, mensajes = _quest_activa.intentar_ejecutar()
            if exito:
                $ _npc_id_temp = "violet"
                jump ejecutar_quest_activa

    # Construir opciones extra
    $ _opciones_extra_v = []

    # Quest 3: Preguntar por el cosplay
    if _quest_activa and _quest_activa.id == "violet_questprincipal_6" and _quest_activa.etapa_actual == 5:
        $ _opciones_extra_v.append({"texto": "Preguntar por el cosplay", "label": "quest_violet_questprincipal_6", "condicion": True})

    # Quest 2 nueva: Dar paquete a Violet
    if "mangas_violet" in inventario and inventario.get("mangas_violet", 0) > 0:
        $ _opciones_extra_v.append({"texto": "Dar paquete", "label": "dar_paquete_quest02_violet", "condicion": True})

    # Evento 1: Invitar a jugar VR
    if violet_evento1_completado and "casco_realidad_virtual" in inventario and not violet_evento1_repetir:
        $ _opciones_extra_v.append({"texto": "Invitar a jugar VR", "label": "invitar_violet_vr", "condicion": True})

    # Mostrar menú de interacción
    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_v if _opciones_extra_v else None)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_v = _return[1]
        jump expression _label_opcion_v

    return
