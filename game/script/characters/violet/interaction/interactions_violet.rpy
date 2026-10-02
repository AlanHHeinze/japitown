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

    # NOTA DE ARQUITECTURA (2026-07-31): acá había un gate que auto-ejecutaba la
    # quest activa y saltaba SIN abrir el menú. Se eliminó — ver la explicación
    # completa en interactions_monica.rpy.
    # Las quests que dependían de ese auto-disparo (0_b, 04_b, 04_c, 04_d, 04_e,
    # 11, 12) tienen ahora su propio botón más abajo. La 07_c no lo necesita: se
    # cierra sola con el accion_al_completar de su chat.

    # (Acá estaba el enganche del click durante la búsqueda del altillo, de la
    # quest de amor 15: clickearla no abría el menú, contestaba una línea, y a
    # la quinta vez se abría una escena. Ese arco se mudó entero a
    # ventajas/juegosnuevos/jn_pocketboy.rpy y quedó parkeado. El enganche se
    # sacó porque contenido inalcanzable no debe interceptar el click al NPC;
    # cómo reponerlo está en la cabecera de ese archivo.)

    # Quest 09_a: interacción especial cuando Violet está enferma en su habitacion
    if (quest_lista_para_boton("violet_questprincipal_09_a") and
            _npc_actual.esta_en_locacion("casa_hviolet")):
        jump violet_quest09a_interaccion

    # Construir opciones extra
    $ _opciones_extra_v = []

    # Quest 0_a: Botón de interacción para romper el hielo (solo antes del intro).
    $ _v0a_lista = quest_lista_para_boton("violet_questprincipal_0_a")
    if _v0a_lista and not getattr(store, "violet_q0a_esperando_talk", False):
        $ _opciones_extra_v.append({"texto": "Saludar", "label": "quest_violet_questprincipal_0_a", "condicion": True})

    # Quest 0_a: tras el intro, botón de quest "Hablar" que dispara el talk especial.
    # El botón real del sistema talk está oculto hasta completar esta quest, asi que
    # este botón de quest es el que permite avanzar (y al completar se desbloquea el real).
    if _v0a_lista and getattr(store, "violet_q0a_esperando_talk", False):
        $ _opciones_extra_v.append({"texto": "Hablar", "label": "violet_q0a_talk_sistema", "condicion": True, "quest_id": "violet_questprincipal_0_a"})

    # Quest 04_a: Preguntar por el cosplay — en la cocina por la mañana (lo
    # dice su demanda de locacion; la capa 2 lo esconde en cualquier otro lado).
    if quest_lista_para_boton("violet_questprincipal_04_a"):
        $ _opciones_extra_v.append({"texto": "Preguntar por el cosplay", "label": "quest_violet_questprincipal_04_a", "condicion": True})

    # Quest 2 nueva: Dar paquete a Violet
    if "mangas_violet" in inventario and inventario.get("mangas_violet", 0) > 0:
        $ _opciones_extra_v.append({"texto": "Dar paquete", "label": "dar_paquete_quest02_violet", "condicion": True, "quest_id": "violet_questprincipal_01_b"})

    # Quest 02_a: Pedir mangas
    if quest_lista_para_boton("violet_questprincipal_02_a"):
        # Tras el primer intento el boton vuelve solo cuando ya se tiene el hito
        # que habilita el prestamo (mismo criterio que el router de la quest).
        if not getattr(store, 'violet_quest02a_primer_intento_hecho', False) or violet_presta_mangas():
            $ _opciones_extra_v.append({"texto": "Pedir mangas", "label": "quest_violet_questprincipal_02_a", "condicion": True})

    # Quest 03_a: Devolver mangas (fuera de la habitacion — solo da pista)
    if quest_lista_para_boton("violet_questprincipal_03_a"):
        if "mangas_violet_mc" in inventario and inventario.get("mangas_violet_mc", 0) > 0:
            $ _opciones_extra_v.append({"texto": "Devolver mangas", "label": "vq3a_devolver_fuera", "condicion": True, "quest_id": "violet_questprincipal_03_a"})

    # Quest 05_a: Hablar con Violet sobre los cosplays
    if quest_lista_para_boton("violet_questprincipal_05_a"):
        if sistema_mensajes.grupo_completado("coxplay_q5a_g4"):
            $ _opciones_extra_v.append({"texto": "Ya compré los cosplay", "label": "violet_quest05a_hablar", "condicion": True, "quest_id": "violet_questprincipal_05_a"})

    # Quest 05_b: Dar la Coxplay Box a Violet
    if quest_lista_para_boton("violet_questprincipal_05_b"):
        $ _opciones_extra_v.append({"texto": "Llegaron los cosplay", "label": "violet_quest05b_hablar", "condicion": True, "quest_id": "violet_questprincipal_05_b"})

    # Quest 05_c: Pedirle perdón a Violet
    if quest_lista_para_boton("violet_questprincipal_05_c"):
        if _npc_actual.esta_en_locacion("casa_hviolet"):
            $ _opciones_extra_v.append({"texto": "Pedirle perdón", "label": "violet_quest05c_habitacion", "condicion": True, "quest_id": "violet_questprincipal_05_c"})
        else:
            $ _opciones_extra_v.append({"texto": "Pedirle perdón", "label": "violet_quest05c_perdon_fuera", "condicion": True, "quest_id": "violet_questprincipal_05_c"})

    # Quest 06_a: Contarle de las entradas. De noche y dentro de su habitacion:
    # lo dice la demanda (npc violet, noche, casa_hviolet), la capa 2 lo aplica.
    if quest_lista_para_boton("violet_questprincipal_06_a"):
        $ _opciones_extra_v.append({"texto": "Tengo las entradas", "label": "violet_quest06a_hablar", "condicion": True, "quest_id": "violet_questprincipal_06_a"})

    # Quest 07_a: Preguntar por el cosplay
    if quest_lista_para_boton("violet_questprincipal_07_a"):
        $ _opciones_extra_v.append({"texto": "Preguntar por el cosplay", "label": "violet_quest07a_hablar", "condicion": True, "quest_id": "violet_questprincipal_07_a"})

    # Quest 07_b: Ya hablé con la tienda
    if quest_lista_para_boton("violet_questprincipal_07_b"):
        $ _opciones_extra_v.append({"texto": "Ya hablé con la tienda", "label": "violet_quest07b_hablar", "condicion": True, "quest_id": "violet_questprincipal_07_b"})

    # -------------------------------------------------------------------------
    # Botones de las quests que antes se AUTO-DISPARABAN al clickear a Violet.
    # Al sacar ese atajo (ver nota de arquitectura arriba) quedaban sin
    # disparador, así que cada una recibe el suyo. Las condiciones replican lo
    # que la quest ya pedía en su `que_hacer`, para que el botón solo aparezca
    # cuando tiene sentido.
    # -------------------------------------------------------------------------

    # Quest 0_b: ¿Qué le pasa a Violet? — en su habitación, por la tarde.
    # (También se puede disparar desde el door access con "Intentar hablar".)
    if (quest_lista_para_boton("violet_questprincipal_0_b") and
            _npc_actual.esta_en_locacion("casa_hviolet") and horario_actual == 1):
        $ _opciones_extra_v.append({"texto": "Preguntarle qué le pasa", "label": "quest_violet_questprincipal_0_b", "condicion": True})

    # La quest 04_b NO lleva botón: ya tiene disparador propio por LOCACIÓN
    # (`_gl_trigger_violet_04b`, trigger de game_loop en violet_quest_04_b.rpy).
    # Se dispara estando donde ella esté, así que un botón sería inalcanzable —
    # nunca llegás a clickearla con la quest activa.

    # Quests 04_c / 04_d / 04_e: solo tras responder el chat nocturno de Violet
    # (antes de eso la pista dice "esperar el mensaje").
    if (quest_lista_para_boton("violet_questprincipal_04_c") and
            sistema_mensajes.grupo_completado("violet_quest04c_chat")):
        $ _opciones_extra_v.append({"texto": "Preguntarle por el cosplay", "label": "quest_violet_questprincipal_04_c", "condicion": True})

    if (quest_lista_para_boton("violet_questprincipal_04_d") and
            sistema_mensajes.grupo_completado("violet_quest04d_chat")):
        $ _opciones_extra_v.append({"texto": "Preguntarle por las fotos", "label": "quest_violet_questprincipal_04_d", "condicion": True})

    # Quest 04_d2: ofrecerle ayuda a Violet. Disparador unico de la quest; sin
    # condicion extra, alcanza con que este lista (activa + BOTON_LISTO).
    if quest_lista_para_boton("violet_questprincipal_04_d2"):
        $ _opciones_extra_v.append({"texto": "¿Puedo hacer algo por ti?", "label": "quest_violet_questprincipal_04_d2", "condicion": True})

    # Arco de los favores: UN solo boton, con el TEXTO segun el punto del arco
    # ("Preguntarle si necesita algo" antes del pedido, "¿Que necesitabas?"
    # despues) y que en varios tramos no va — entre ellos los dias de espera.
    # Toda esa logica vive en violet_favores_boton_texto(); si devuelve None, no
    # hay boton. El despachador violet_favores_boton decide a que label va.
    $ _txt_favores = violet_favores_boton_texto()
    if _txt_favores:
        # La quest concreta cambia segun el tramo del arco (d3/d4/d5), asi que
        # el id del tag se resuelve acá y no se puede escribir fijo.
        $ _q_favores = violet_favores_quest_activa()
        $ _opciones_extra_v.append({"texto": _txt_favores, "label": "violet_favores_boton", "condicion": True, "quest_id": (_q_favores.id if _q_favores else None)})

    # Boton extra de la 04_d3: solo cuando ya pidio las golosinas y el MC las tiene.
    if quest_lista_para_boton("violet_questprincipal_04_d3") and vq4d3_pedido_hecho and inventario.get("golosinas", 0) > 0:
        $ _opciones_extra_v.append({"texto": "Darle las golosinas", "label": "violet_q4d3_entregar", "condicion": True, "quest_id": "violet_questprincipal_04_d3"})

    # Cierre del arco (04_d6): avisarle que la limpieza esta terminada. Reemplaza
    # al boton generico — la d6 esta fuera de VIOLET_FAVORES_QUESTS justamente
    # para que no aparezcan los dos.
    #
    # SOLO dentro de la habitacion de Violet: la escena de cierre pasa ahi. Si
    # la cruzas en otro lado, el camino es la opcion de puerta, que te hace
    # entrar primero.
    if (quest_lista_para_boton("violet_questprincipal_04_d6")
            and sistema_locaciones.locacion_actual
            and sistema_locaciones.locacion_actual.id == "casa_hviolet"):
        $ _opciones_extra_v.append({"texto": "Ya terminé de limpiar", "label": "violet_q4d6_cierre", "condicion": True, "quest_id": "violet_questprincipal_04_d6"})

    if (quest_lista_para_boton("violet_questprincipal_04_e") and
            sistema_mensajes.grupo_completado("violet_quest04e_chat")):
        $ _opciones_extra_v.append({"texto": "Preguntarle por las fotos", "label": "quest_violet_questprincipal_04_e", "condicion": True})

    # Amor 20 ("Jugando juntos"): dos de sus cuatro tramos son botones de este
    # menu, el primero y el ultimo. Los del medio son acciones de la habitacion
    # del MC (comprar y jugar), asi que cada boton desaparece solo en cuanto
    # va20_fase deja de ser el suyo. Nunca conviven: las condiciones son
    # excluyentes por fase.
    if _va20_boton_recomendacion():
        $ _opciones_extra_v.append({"texto": "Algo para jugar", "label": "violet_amor_20_recomendacion", "condicion": True, "quest_id": "violet_amor_04"})

    if _va20_boton_hablar():
        $ _opciones_extra_v.append({"texto": "Hablar del juego", "label": "violet_amor_20_hablar", "condicion": True, "quest_id": "violet_amor_04"})

    # Amor 25 ("Solos en casa"): el domingo por la tarde, con Violet en el
    # living. La condicion entera vive en violet_amor_25.rpy.
    if _va25_boton_matar_tiempo():
        $ _opciones_extra_v.append({"texto": "Matar el tiempo", "label": "violet_amor_25_matar_tiempo", "condicion": True, "quest_id": "violet_amor_05"})

    # (Deseo 25 "En su habitación" NO tiene boton acá. Se dispara sola con la
    # accion "Ver TV" del sotano y sigue por un override de su puerta, los dos
    # registrados desde violet_deseo_25.rpy.)

    # Amor 30 ("¿Qué me pongo?"): mismo momento que la opcion de su puerta,
    # pero visto desde adentro de la habitacion. Nunca conviven: si estas en el
    # pasillo ves la de la puerta, si ya entraste ves esta.

    # (Amor 40 "La solicitud" NO tiene boton acá. Arranca sola con un trigger
    # en la habitacion del MC y sigue por un override de la puerta de Violet y
    # el chat, todo registrado desde violet_amor_40.rpy. La version vieja tenia
    # un boton "Preguntarle por Zowie" en este menu: se borro con la narrativa
    # final, y su llamada quedo colgada acá hasta el reporte del 2026-10-01.)

    # ── LINEAS DE RELACION (amor / deseo) ────────────────────────────────────
    # Un boton por quest de linea (disparador unico, regla 10 del skill).
    # quest_lista_para_boton() ya chequea activa + no completada + BOTON_LISTO.
    # Se recorren TODAS las quests de cada linea: como encadenan, a lo sumo una
    # por linea esta lista a la vez — pero el boton tiene que existir para
    # todas, o la cadena se muere en la primera sin boton (bug real: las 03-06
    # llegaban a BOTON_LISTO y no habia forma de dispararlas).
    python:
        # Hasta 7: la de deseo es una mas que la de amor (la 30 esta partida en
        # 06 + 07). Un numero sin quest no rompe nada: quest_lista_para_boton
        # devuelve False.
        for _vq_rel_n in range(1, 8):
            _vq_rel_id = "violet_amor_{:02d}".format(_vq_rel_n)
            # NINGUNA de las 6 usa este boton: todas tienen disparador propio
            # (trigger de locacion, de dormir, accion, boton con texto propio).
            # El bucle se deja igual para que la linea siga teniendo su boton de
            # respaldo el dia que se agregue una quest sin disparador — sin el,
            # una quest asi llegaria a BOTON_LISTO sin forma de dispararse (bug
            # real de las 03-06 antes de escribirlas).
            _VA_SIN_BOTON = ("violet_amor_01", "violet_amor_02", "violet_amor_03",
                             "violet_amor_04", "violet_amor_05", "violet_amor_06",
                             "violet_amor_07", "violet_amor_08",
                             "violet_amor_09", "violet_amor_10")
            if _vq_rel_id not in _VA_SIN_BOTON and quest_lista_para_boton(_vq_rel_id):
                _opciones_extra_v.append({"texto": "Charlar un rato", "label": "quest_" + _vq_rel_id, "condicion": True})

            _vq_rel_id = "violet_deseo_{:02d}".format(_vq_rel_n)
            # NINGUNA de las 6 usa este boton: todas tienen disparador propio
            # (trigger de locacion, de dormir, accion, chat, boton con texto
            # propio). Ojo con la 04 ("Pensando en Violet"), que pasa entera en
            # el chat: con boton generico el jugador la cerraria sin conversar.
            # El bucle se deja igual como respaldo para una quest futura sin
            # disparador — sin el llegaria a BOTON_LISTO sin forma de dispararse.
            _VD_SIN_BOTON = ("violet_deseo_01", "violet_deseo_02", "violet_deseo_03",
                             "violet_deseo_04", "violet_deseo_05", "violet_deseo_06",
                             "violet_deseo_07")
            if _vq_rel_id not in _VD_SIN_BOTON and quest_lista_para_boton(_vq_rel_id):
                _opciones_extra_v.append({"texto": "Buscar un momento a solas", "label": "quest_" + _vq_rel_id, "condicion": True})

    # ── VENTAJAS DE HITO ─────────────────────────────────────────────────────
    # Sin tag y al final de las extra: son capacidades permanentes del vinculo,
    # no contenido pendiente.

    # Juegos Nuevos (hito de amor 20). La condicion vive en
    # ventajas/juegosnuevos/juegosnuevos_violet.rpy.
    if _violet_boton_juegos_nuevos():
        $ _opciones_extra_v.append({"texto": "Juegos Nuevos", "label": "violet_juegos_nuevos", "condicion": True, "tipo": "ventaja"})

    # Besos (hitos de amor 30 y deseo 30). Son DOS ventajas independientes con
    # su propio limite diario: teniendo las dos se pueden hacer las dos el mismo
    # dia. Sin condicion de locacion — los cortes (compañia y una vez por dia)
    # los resuelve cada label (ventajas/beso_violet.rpy, beso_deseo_violet.rpy).
    if _violet_beso_disponible():
        $ _opciones_extra_v.append({"texto": "Beso (Amor)", "label": "violet_beso_amor", "condicion": True, "tipo": "ventaja"})

    if _violet_beso_deseo_disponible():
        $ _opciones_extra_v.append({"texto": "Beso (Deseo)", "label": "violet_beso_deseo", "condicion": True, "tipo": "ventaja"})

    # Ropa Nueva (hito de amor 30). Solo con ella en su habitacion; la condicion
    # vive en ventajas/ropanueva/ropanueva_violet.rpy.
    if _violet_boton_ropa_nueva():
        $ _opciones_extra_v.append({"texto": "Ropa Nueva", "label": "violet_ropa_nueva", "condicion": True, "tipo": "ventaja"})

    # Casco VR: invitarla a repetir. Era del evento 01, que se retiro — ahora es
    # el primer juego de Juegos Nuevos (ventajas/juegosnuevos/jn_cascovr.rpy).
    if violet_evento1_completado and "casco_realidad_virtual" in inventario and not violet_evento1_repetir:
        $ _opciones_extra_v.append({"texto": "Invitar a jugar VR", "label": "invitar_violet_vr", "condicion": True, "tipo": "ventaja"})

    # Mostrar menú de interacción
    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_v if _opciones_extra_v else None)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_v = despachar_opcion_quest(_return, origen="menu:violet")
        jump expression _label_opcion_v

    return
