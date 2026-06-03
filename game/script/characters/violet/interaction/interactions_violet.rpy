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
        # Quests que usan opciones_extra en vez de auto-trigger
        if _quest_activa.id not in ("violet_questprincipal_04_a", "violet_questprincipal_02_a", "violet_questprincipal_02_c", "violet_questprincipal_03_a", "violet_questprincipal_05_a", "violet_questprincipal_05_b", "violet_questprincipal_05_c", "violet_questprincipal_06_a", "violet_questprincipal_06_b", "violet_questprincipal_07_a", "violet_questprincipal_07_b", "violet_questprincipal_09_a"):
            $ exito, mensajes = _quest_activa.intentar_ejecutar()
            if exito:
                $ _npc_id_temp = "violet"
                jump ejecutar_quest_activa

    # Quest 09_a: interacción especial cuando Violet está enferma en su habitación
    $ _quest_v09a_int = sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if (_quest_v09a_int and _quest_v09a_int.activa and not _quest_v09a_int.completada and
            _quest_v09a_int.etapa_actual == ETAPA_BOTON_LISTO and
            _npc_actual.esta_en_locacion("casa_hviolet")):
        jump violet_quest09a_interaccion

    # Construir opciones extra
    $ _opciones_extra_v = []

    # Quest 04_a: Preguntar por el cosplay — solo en cocina por la mañana
    if _quest_activa and _quest_activa.id == "violet_questprincipal_04_a" and _quest_activa.etapa_actual == 5:
        $ _vq04a_cond = (horario_actual == 0 and sistema_locaciones.locacion_actual and sistema_locaciones.locacion_actual.id == "casa_cocina")
        $ _opciones_extra_v.append({"texto": "Preguntar por el cosplay", "label": "quest_violet_questprincipal_04_a", "condicion": _vq04a_cond})

    # Quest 2 nueva: Dar paquete a Violet
    if "mangas_violet" in inventario and inventario.get("mangas_violet", 0) > 0:
        $ _opciones_extra_v.append({"texto": "Dar paquete", "label": "dar_paquete_quest02_violet", "condicion": True})

    # Quest 02_a: Pedir mangas
    $ _quest_v02a = sistema_quests.obtener_quest("violet_questprincipal_02_a")
    if _quest_v02a and _quest_v02a.activa and not _quest_v02a.completada and _quest_v02a.etapa_actual == ETAPA_BOTON_LISTO:
        if not getattr(store, 'violet_quest02a_primer_intento_hecho', False) or obtener_stat1("violet") >= 10:
            $ _opciones_extra_v.append({"texto": "Pedir mangas", "label": "quest_violet_questprincipal_02_a", "condicion": True})

    # Quest 03_a: Devolver mangas (fuera de la habitacion — solo da pista)
    $ _quest_v03a = sistema_quests.obtener_quest("violet_questprincipal_03_a")
    if _quest_v03a and _quest_v03a.activa and not _quest_v03a.completada and _quest_v03a.etapa_actual == ETAPA_BOTON_LISTO:
        if "mangas_violet_mc" in inventario and inventario.get("mangas_violet_mc", 0) > 0:
            $ _opciones_extra_v.append({"texto": "Devolver mangas", "label": "vq3a_devolver_fuera", "condicion": True})

    # Quest 05_a: Hablar con Violet sobre los cosplays
    $ _quest_v05a = sistema_quests.obtener_quest("violet_questprincipal_05_a")
    if _quest_v05a and _quest_v05a.activa and not _quest_v05a.completada and _quest_v05a.etapa_actual == ETAPA_BOTON_LISTO:
        if sistema_mensajes.grupo_completado("coxplay_q5a_g4"):
            $ _opciones_extra_v.append({"texto": "Ya compré los cosplay", "label": "violet_quest05a_hablar", "condicion": True})

    # Quest 05_b: Dar la Coxplay Box a Violet
    $ _quest_v05b = sistema_quests.obtener_quest("violet_questprincipal_05_b")
    if _quest_v05b and _quest_v05b.activa and not _quest_v05b.completada and _quest_v05b.etapa_actual == ETAPA_BOTON_LISTO:
        $ _opciones_extra_v.append({"texto": "Llegaron los cosplay", "label": "violet_quest05b_hablar", "condicion": True})

    # Quest 05_c: Pedirle perdón a Violet
    $ _quest_v05c = sistema_quests.obtener_quest("violet_questprincipal_05_c")
    if _quest_v05c and _quest_v05c.activa and not _quest_v05c.completada and _quest_v05c.etapa_actual == ETAPA_BOTON_LISTO:
        if _npc_actual.esta_en_locacion("casa_hviolet"):
            $ _opciones_extra_v.append({"texto": "Pedirle perdón", "label": "violet_quest05c_habitacion", "condicion": True})
        else:
            $ _opciones_extra_v.append({"texto": "Pedirle perdón", "label": "violet_quest05c_perdon_fuera", "condicion": True})

    # Quest 06_a: Contarle de las entradas
    $ _quest_v06a = sistema_quests.obtener_quest("violet_questprincipal_06_a")
    if _quest_v06a and _quest_v06a.activa and not _quest_v06a.completada and _quest_v06a.etapa_actual == ETAPA_BOTON_LISTO:
        $ _opciones_extra_v.append({"texto": "Tengo las entradas", "label": "violet_quest06a_hablar", "condicion": True})

    # Quest 07_a: Preguntar por el cosplay
    $ _quest_v07a = sistema_quests.obtener_quest("violet_questprincipal_07_a")
    if _quest_v07a and _quest_v07a.activa and not _quest_v07a.completada and _quest_v07a.etapa_actual == ETAPA_BOTON_LISTO:
        $ _opciones_extra_v.append({"texto": "Preguntar por el cosplay", "label": "violet_quest07a_hablar", "condicion": True})

    # Quest 07_b: Ya hablé con la tienda
    $ _quest_v07b = sistema_quests.obtener_quest("violet_questprincipal_07_b")
    if _quest_v07b and _quest_v07b.activa and not _quest_v07b.completada and _quest_v07b.etapa_actual == ETAPA_BOTON_LISTO:
        $ _opciones_extra_v.append({"texto": "Ya hablé con la tienda", "label": "violet_quest07b_hablar", "condicion": True})

    # Evento 1: Invitar a jugar VR
    if violet_evento1_completado and "casco_realidad_virtual" in inventario and not violet_evento1_repetir:
        $ _opciones_extra_v.append({"texto": "Invitar a jugar VR", "label": "invitar_violet_vr", "condicion": True})

    # Mostrar menú de interacción
    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_v if _opciones_extra_v else None)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_v = _return[1]
        jump expression _label_opcion_v

    return
