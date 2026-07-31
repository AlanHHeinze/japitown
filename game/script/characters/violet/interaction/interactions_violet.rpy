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

    # NOTA DE ARQUITECTURA (2026-07-31): acá había un gate que auto-ejecutaba la
    # quest activa y saltaba SIN abrir el menú. Se eliminó — ver la explicación
    # completa en interactions_monica.rpy.
    # Las quests que dependían de ese auto-disparo (0_b, 04_b, 04_c, 04_d, 04_e,
    # 11, 12) tienen ahora su propio botón más abajo. La 07_c no lo necesita: se
    # cierra sola con el accion_al_completar de su chat.

    # Quest 09_a: interacción especial cuando Violet está enferma en su habitacion
    $ _quest_v09a_int = sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if (_quest_v09a_int and _quest_v09a_int.activa and not _quest_v09a_int.completada and
            _quest_v09a_int.etapa_actual == ETAPA_BOTON_LISTO and
            _npc_actual.esta_en_locacion("casa_hviolet")):
        jump violet_quest09a_interaccion

    # Construir opciones extra
    $ _opciones_extra_v = []

    # Quest 0_a: Botón de interacción para romper el hielo (solo antes del intro).
    $ _quest_v0a = sistema_quests.obtener_quest("violet_questprincipal_0_a")
    if _quest_v0a and _quest_v0a.activa and not _quest_v0a.completada and _quest_v0a.etapa_actual == ETAPA_BOTON_LISTO and not getattr(store, "violet_q0a_esperando_talk", False):
        $ _opciones_extra_v.append({"texto": "Hablar (quest)", "label": "quest_violet_questprincipal_0_a", "condicion": True})

    # Quest 0_a: tras el intro, botón de quest "Hablar" que dispara el talk especial.
    # El botón real del sistema talk está oculto hasta completar esta quest, asi que
    # este botón de quest es el que permite avanzar (y al completar se desbloquea el real).
    if _quest_v0a and _quest_v0a.activa and not _quest_v0a.completada and _quest_v0a.etapa_actual == ETAPA_BOTON_LISTO and getattr(store, "violet_q0a_esperando_talk", False):
        $ _opciones_extra_v.append({"texto": "Hablar", "label": "violet_q0a_talk_sistema", "condicion": True})

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

    # Quest 06_a: Contarle de las entradas (de noche, dentro de la habitacion)
    $ _quest_v06a = sistema_quests.obtener_quest("violet_questprincipal_06_a")
    if _quest_v06a and _quest_v06a.activa and not _quest_v06a.completada and _quest_v06a.etapa_actual == ETAPA_BOTON_LISTO:
        if _npc_actual.esta_en_locacion("casa_hviolet") and horario_actual == 2:
            $ _opciones_extra_v.append({"texto": "Tengo las entradas", "label": "violet_quest06a_hablar", "condicion": True})

    # Quest 07_a: Preguntar por el cosplay
    $ _quest_v07a = sistema_quests.obtener_quest("violet_questprincipal_07_a")
    if _quest_v07a and _quest_v07a.activa and not _quest_v07a.completada and _quest_v07a.etapa_actual == ETAPA_BOTON_LISTO:
        $ _opciones_extra_v.append({"texto": "Preguntar por el cosplay", "label": "violet_quest07a_hablar", "condicion": True})

    # Quest 07_b: Ya hablé con la tienda
    $ _quest_v07b = sistema_quests.obtener_quest("violet_questprincipal_07_b")
    if _quest_v07b and _quest_v07b.activa and not _quest_v07b.completada and _quest_v07b.etapa_actual == ETAPA_BOTON_LISTO:
        $ _opciones_extra_v.append({"texto": "Ya hablé con la tienda", "label": "violet_quest07b_hablar", "condicion": True})

    # -------------------------------------------------------------------------
    # Botones de las quests que antes se AUTO-DISPARABAN al clickear a Violet.
    # Al sacar ese atajo (ver nota de arquitectura arriba) quedaban sin
    # disparador, así que cada una recibe el suyo. Las condiciones replican lo
    # que la quest ya pedía en su `que_hacer`, para que el botón solo aparezca
    # cuando tiene sentido.
    # -------------------------------------------------------------------------

    # Quest 0_b: ¿Qué le pasa a Violet? — en su habitación, por la tarde.
    # (También se puede disparar desde el door access con "Intentar hablar".)
    $ _quest_v0b = sistema_quests.obtener_quest("violet_questprincipal_0_b")
    if (_quest_v0b and _quest_v0b.activa and not _quest_v0b.completada and
            _quest_v0b.etapa_actual == ETAPA_BOTON_LISTO and
            _npc_actual.esta_en_locacion("casa_hviolet") and horario_actual == 1):
        $ _opciones_extra_v.append({"texto": "Preguntarle qué le pasa", "label": "quest_violet_questprincipal_0_b", "condicion": True})

    # La quest 04_b NO lleva botón: ya tiene disparador propio por LOCACIÓN
    # (`violet_quest04b_check_locacion`, registrado en las 5 locaciones de Violet
    # desde quest_violet.rpy). Se dispara al ENTRAR donde ella esté, así que un
    # botón sería inalcanzable — nunca llegás a clickearla con la quest activa.

    # Quests 04_c / 04_d / 04_e: solo tras responder el chat nocturno de Violet
    # (antes de eso la pista dice "esperar el mensaje").
    $ _quest_v04c = sistema_quests.obtener_quest("violet_questprincipal_04_c")
    if (_quest_v04c and _quest_v04c.activa and not _quest_v04c.completada and
            _quest_v04c.etapa_actual == ETAPA_BOTON_LISTO and
            sistema_mensajes.grupo_completado("violet_quest04c_chat")):
        $ _opciones_extra_v.append({"texto": "Preguntarle por el cosplay", "label": "quest_violet_questprincipal_04_c", "condicion": True})

    $ _quest_v04d = sistema_quests.obtener_quest("violet_questprincipal_04_d")
    if (_quest_v04d and _quest_v04d.activa and not _quest_v04d.completada and
            _quest_v04d.etapa_actual == ETAPA_BOTON_LISTO and
            sistema_mensajes.grupo_completado("violet_quest04d_chat")):
        $ _opciones_extra_v.append({"texto": "Preguntarle por las fotos", "label": "quest_violet_questprincipal_04_d", "condicion": True})

    $ _quest_v04e = sistema_quests.obtener_quest("violet_questprincipal_04_e")
    if (_quest_v04e and _quest_v04e.activa and not _quest_v04e.completada and
            _quest_v04e.etapa_actual == ETAPA_BOTON_LISTO and
            sistema_mensajes.grupo_completado("violet_quest04e_chat")):
        $ _opciones_extra_v.append({"texto": "Preguntarle por las fotos", "label": "quest_violet_questprincipal_04_e", "condicion": True})

    # Quest 11: mostrarle los cosplays comprados — en su habitación, de noche.
    $ _quest_v11 = sistema_quests.obtener_quest("violet_questprincipal_11")
    if (_quest_v11 and _quest_v11.activa and not _quest_v11.completada and
            _quest_v11.etapa_actual == ETAPA_BOTON_LISTO and
            _npc_actual.esta_en_locacion("casa_hviolet") and horario_actual == 2):
        $ _opciones_extra_v.append({"texto": "Mostrarle los cosplays", "label": "quest_violet_questprincipal_11", "condicion": True})

    # Quest 12: visita nocturna — en su habitación, de noche, tras responder el chat.
    $ _quest_v12 = sistema_quests.obtener_quest("violet_questprincipal_12")
    if (_quest_v12 and _quest_v12.activa and not _quest_v12.completada and
            _quest_v12.etapa_actual == ETAPA_BOTON_LISTO and
            sistema_mensajes.grupo_completado("violet_quest12_chat") and
            _npc_actual.esta_en_locacion("casa_hviolet") and horario_actual == 2):
        $ _opciones_extra_v.append({"texto": "Vine como me pediste", "label": "quest_violet_questprincipal_12", "condicion": True})

    # Evento 1: Invitar a jugar VR
    if violet_evento1_completado and "casco_realidad_virtual" in inventario and not violet_evento1_repetir:
        $ _opciones_extra_v.append({"texto": "Invitar a jugar VR", "label": "invitar_violet_vr", "condicion": True, "tipo": "evento"})

    # Mostrar menú de interacción
    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_v if _opciones_extra_v else None)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_v = _return[1]
        jump expression _label_opcion_v

    return
