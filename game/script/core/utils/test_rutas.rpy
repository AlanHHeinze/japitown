################################################################################
## Rutas de testeo de sistemas — SOLO DESARROLLO
################################################################################
## Corre rutas completas por sistema sin jugar a mano: cada ruta es una lista de
## pasos ordenados (que probar primero, que se dispara, a donde deriva) y se
## corta en el primer paso que falla, reportando exactamente donde se rompio.
##
## COMO USAR (guia completa en docs/arquitectura/testing_sistemas.md):
##   1. Iniciar una PARTIDA DESCARTABLE (Comenzar) — nunca en el menu principal.
##   2. Abrir la consola (Shift+O) y ejecutar:
##        jp_test_correr("quests")        # una ruta
##        jp_test_correr_todas()          # todas las NO destructivas
##        jp_test_correr_todas(True)      # todas, incluidas las destructivas
##   3. El resultado se imprime en consola y se acumula en
##      test_rutas_resultado.txt (raiz del proyecto).
##
## Las rutas marcadas destructiva=True MUTAN la partida (avanzan dias, compran,
## activan restricciones): correrlas solo en partidas descartables.
##
## init 999 (el maximo permitido): despues de todos los registros de contenido
## (init 5-11). Nada de aca se guarda en saves: el registro se construye en init
## y no se muta en runtime.

init 999 python:

    import os as _jpt_os
    import time as _jpt_time

    # Contexto compartido entre pasos de una misma ruta (se limpia al arrancar cada ruta)
    _JPT_CTX = {}

    def _jpt_ok(detalle=""):
        return (True, detalle)

    def _jpt_fallo(detalle):
        return (False, detalle)

    # =========================================================================
    # RUTA: tiempo — ciclo de dia completo (DESTRUCTIVA: avanza el reloj)
    # =========================================================================

    def _jpt_tiempo_estado_inicial():
        h = getattr(store, "horario_actual", None)
        d = getattr(store, "dias_totales", None)
        if h is None or not (0 <= h <= 3):
            return _jpt_fallo("horario_actual invalido: {!r}".format(h))
        if not d or d < 1:
            return _jpt_fallo("dias_totales invalido: {!r}".format(d))
        return _jpt_ok("horario={} dia={}".format(h, d))

    def _jpt_tiempo_avanzar():
        # Tras el refactor C2 no hay quests que congelen el motor: los bloqueos
        # de tiempo van por restriccion (que frena el LABEL, no esta funcion).
        h0 = store.horario_actual
        esperado = h0 if h0 >= 3 else h0 + 1
        avanzar_horario()
        h1 = store.horario_actual
        if h1 != esperado:
            return _jpt_fallo("horario {} -> {} (esperaba {})".format(h0, h1, esperado))
        return _jpt_ok("horario {} -> {}".format(h0, h1))

    def _jpt_tiempo_dormir():
        d0 = store.dias_totales
        dormir()
        if store.dias_totales != d0 + 1:
            return _jpt_fallo("dias_totales {} -> {} (esperaba {})".format(
                d0, store.dias_totales, d0 + 1))
        if store.horario_actual != 0:
            return _jpt_fallo("horario tras dormir = {} (esperaba 0)".format(
                store.horario_actual))
        return _jpt_ok("dia {} -> {}, horario reseteado".format(d0, d0 + 1))

    def _jpt_tiempo_save_name():
        # dormir() debe refrescar la etiqueta de los slots de guardado
        nombre = getattr(store, "save_name", "")
        if str(store.dias_totales) not in str(nombre):
            return _jpt_fallo("save_name '{}' no contiene el dia {}".format(
                nombre, store.dias_totales))
        return _jpt_ok("save_name = '{}'".format(nombre))

    def _jpt_tiempo_resets():
        if getattr(store, "entrenamiento_hoy", False):
            return _jpt_fallo("entrenamiento_hoy no se reseteo al dormir")
        if getattr(store, "trabajo_hoy", 0) != 0:
            return _jpt_fallo("trabajo_hoy no se reseteo al dormir")
        return _jpt_ok("limites diarios reseteados")

    # =========================================================================
    # RUTA: quests — integridad del catalogo (no destructiva)
    # =========================================================================

    def _jpt_quests_catalogo():
        sq = getattr(store, "sistema_quests", None)
        if not sq or not getattr(sq, "quests", None):
            return _jpt_fallo("sistema_quests vacio o inexistente")
        return _jpt_ok("{} quests registradas".format(len(sq.quests)))

    def _jpt_quests_npcs():
        problemas = []
        for qid, q in store.sistema_quests.quests.items():
            if q.npc_id and obtener_npc(q.npc_id) is None:
                problemas.append("{}: npc '{}' no existe".format(qid, q.npc_id))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("todos los npc_id de las quests existen")

    def _jpt_quests_rutinas():
        problemas = []
        for qid, q in store.sistema_quests.quests.items():
            rutinas = list(getattr(q, "rutina_quest", {}).values())
            for adicional in getattr(q, "rutinas_adicionales", {}).values():
                if isinstance(adicional, dict):
                    rutinas.extend(adicional.values())
            for r in rutinas:
                loc_id = getattr(r, "locacion", None)
                if loc_id and store.sistema_locaciones.obtener_locacion(loc_id) is None:
                    problemas.append("{}: rutina apunta a locacion inexistente '{}'".format(
                        qid, loc_id))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("todas las rutinas de quest apuntan a locaciones existentes")

    def _jpt_quests_mensajes():
        problemas = []
        for qid, q in store.sistema_quests.quests.items():
            try:
                msgs = q.obtener_mensajes()
                if not isinstance(msgs, dict) or "pista" not in msgs or "que_hacer" not in msgs:
                    problemas.append("{}: obtener_mensajes devolvio {!r}".format(qid, msgs))
            except Exception as e:
                problemas.append("{}: obtener_mensajes exploto: {!r}".format(qid, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("obtener_mensajes() ejecuta en todas las quests")

    # =========================================================================
    # RUTA: eventos — integridad y validacion (no destructiva*)
    # (*) validar_eventos() puede cambiar estados de eventos, pero eso mismo
    #     ocurre en cada vuelta del game_loop, asi que no altera nada nuevo.
    # =========================================================================

    def _jpt_eventos_catalogo():
        se = getattr(store, "sistema_events", None)
        if not se or not getattr(se, "events", None):
            return _jpt_fallo("sistema_events vacio o inexistente")
        return _jpt_ok("{} eventos registrados".format(len(se.events)))

    def _jpt_eventos_condiciones():
        problemas = []
        for eid, ev in store.sistema_events.events.items():
            for nombre_cond in ("condicion_aparicion", "condicion_activacion",
                                "condicion_duracion"):
                cond = getattr(ev, nombre_cond, None)
                if cond is None:
                    continue
                try:
                    cond()
                except Exception as e:
                    problemas.append("{}.{}: {!r}".format(eid, nombre_cond, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("todas las condiciones de eventos ejecutan sin excepcion")

    def _jpt_eventos_labels():
        problemas = []
        for eid, ev in store.sistema_events.events.items():
            lbl = getattr(ev, "label_efecto", None)
            if lbl and not renpy.has_label(lbl):
                problemas.append("{}: label_efecto '{}' no existe".format(eid, lbl))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("todos los label_efecto existen")

    def _jpt_eventos_validar():
        validar_eventos()
        return _jpt_ok("validar_eventos() ejecuto sin excepcion")

    # =========================================================================
    # RUTA: mensajes — integridad de grupos y chats (no destructiva)
    # =========================================================================

    def _jpt_mensajes_grupos():
        sm = getattr(store, "sistema_mensajes", None)
        grupos = getattr(sm, "_todos_grupos", None) if sm else None
        if not grupos:
            return _jpt_fallo("sistema_mensajes sin grupos registrados")
        return _jpt_ok("{} grupos de mensajes".format(len(grupos)))

    def _jpt_mensajes_estructura():
        problemas = []
        for gid, g in store.sistema_mensajes._todos_grupos.items():
            if not getattr(g, "pasos", None):
                problemas.append("{}: sin pasos".format(gid))
                continue
            for i, paso in enumerate(g.pasos):
                opciones = getattr(paso, "opciones_jugador", None)
                if not opciones:
                    problemas.append("{}: paso {} sin opciones".format(gid, i))
                    continue
                for j, op in enumerate(opciones):
                    if getattr(op, "respuesta_npc", None) is None:
                        problemas.append("{}: paso {} opcion {} sin respuesta_npc".format(
                            gid, i, j))
            if g.npc_id and obtener_npc(g.npc_id) is None:
                problemas.append("{}: npc '{}' no existe".format(gid, g.npc_id))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("estructura de todos los grupos valida")

    def _jpt_mensajes_condiciones():
        problemas = []
        for gid, g in store.sistema_mensajes._todos_grupos.items():
            cond = getattr(g, "condicion_entrega", None)
            if cond is None:
                continue
            try:
                cond()
            except Exception as e:
                problemas.append("{}: condicion_entrega exploto: {!r}".format(gid, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("todas las condiciones de entrega ejecutan sin excepcion")

    def _jpt_mensajes_saltos():
        """
        Cada `saltar_a_paso` apunta a un paso que existe (o a -1, terminar).

        Un salto fuera de rango deja `paso_actual` mas alla del final:
        obtener_paso_actual() devuelve None, el grupo queda activo sin opciones
        y nunca se completa. Si el grupo bloquea algo, la partida se traba.
        """
        problemas = []
        for gid, g in store.sistema_mensajes._todos_grupos.items():
            n = len(getattr(g, "pasos", None) or [])
            for i, paso in enumerate(g.pasos or []):
                for j, op in enumerate(getattr(paso, "opciones_jugador", None) or []):
                    t = getattr(op, "saltar_a_paso", None)
                    if t is None or t == -1:
                        continue
                    if not (0 <= t < n):
                        problemas.append("{}: paso {} opcion {} salta a {} (hay {})".format(
                            gid, i, j, t, n))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("todos los saltos de paso apuntan a pasos existentes")

    def _jpt_mensajes_rejugables():
        """
        Un grupo se puede jugar DOS veces seguidas y las dos arranca del paso 0.

        Simula lo que le pasa a un grupo repetible: se juega hasta el final
        (paso_actual queda en len(pasos)) y se vuelve a entregar. Si la segunda
        entrega no reinicia el progreso, el grupo arranca ya terminado y no se
        puede contestar — el bug de la conversacion generica de Mensajear
        (dos reportes en la 0.1.9).

        Trabaja sobre COPIAS: no toca el estado real de la partida.
        """
        import copy as _cp
        problemas = []
        sm = store.sistema_mensajes
        for gid, g in sm._todos_grupos.items():
            if not getattr(g, "pasos", None):
                continue
            c = _cp.deepcopy(g)
            # Primera partida, hasta el final.
            c.paso_actual = 0
            c.estado = "en_curso"
            c.avanzar_paso(-1)
            c.estado = "completado"
            # Lo que hace un repetible al terminar, y lo que hace la entrega.
            c.resetear()
            c.reiniciar_progreso()
            if c.obtener_paso_actual() is None:
                problemas.append("{}: tras reentregar no tiene paso".format(gid))
            if c.puntos_acumulados:
                problemas.append("{}: puntos de la partida anterior".format(gid))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("todos los grupos arrancan de cero al reentregarse")

    def _jpt_mensajes_bloqueo_respondible():
        """
        Un mensaje que no se puede contestar NO bloquea el avance.

        Es la regla que evita la partida trabada: obtener_bloqueo_mensaje_
        prioritario() tiene que devolver None para un chat cuyo
        puede_responder() da False. Se prueba con un chat sintetico que
        tiene un grupo prioritario activo y SIN paso valido — exactamente el
        estado del bug.

        Trabaja sobre un chat temporal que se saca al final.
        """
        sm = store.sistema_mensajes
        _npc = "__jpt_fantasma"
        if _npc in sm.chats:
            return _jpt_fallo("el chat de prueba ya existia")
        try:
            sm.inicializar_chat(_npc)
            chat = sm.chats[_npc]
            g = GrupoMensajes(
                id="__jpt_prio", npc_id=_npc, mensaje_inicial="x",
                trigger_id="__jpt_prio", prioritario=True,
                pasos=[PasoConversacion(opciones_jugador=[
                    OpcionRespuesta(texto="a", respuesta_npc="b", saltar_a_paso=-1)])],
            )
            g.paso_actual = len(g.pasos)        # activo pero sin paso
            g.estado = "en_curso"
            chat.grupo_activo = g
            if chat.puede_responder():
                return _jpt_fallo("puede_responder() dio True sin paso valido")
            if obtener_bloqueo_mensaje_prioritario() == _npc.capitalize():
                return _jpt_fallo("un prioritario sin paso valido sigue bloqueando")
            # Y con paso valido SI tiene que bloquear.
            g.paso_actual = 0
            if obtener_bloqueo_mensaje_prioritario() != _npc.capitalize():
                return _jpt_fallo("un prioritario contestable no bloquea")
        finally:
            sm.chats.pop(_npc, None)
        return _jpt_ok("el bloqueo prioritario solo lo sostiene lo contestable")

    # =========================================================================
    # RUTA: acciones — integridad del catalogo (no destructiva)
    # =========================================================================

    def _jpt_acciones_catalogo():
        sa = getattr(store, "sistema_acciones", None)
        if not sa or not getattr(sa, "acciones", None):
            return _jpt_fallo("sistema_acciones vacio o inexistente")
        return _jpt_ok("{} acciones registradas".format(len(sa.acciones)))

    def _jpt_acciones_labels():
        problemas = []
        for aid, a in store.sistema_acciones.acciones.items():
            lbl = getattr(a, "label_generico", None)
            if lbl and not renpy.has_label(lbl):
                problemas.append("{}: label_generico '{}' no existe".format(aid, lbl))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("todos los label_generico existen")

    def _jpt_acciones_disponibilidad():
        problemas = []
        for aid in store.sistema_acciones.acciones:
            try:
                store.sistema_acciones.esta_disponible(aid)
            except Exception as e:
                problemas.append("{}: esta_disponible exploto: {!r}".format(aid, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("esta_disponible() ejecuta en todas las acciones")

    # =========================================================================
    # RUTA: restriccion — activar, bloquear, liberar (DESTRUCTIVA reversible)
    # =========================================================================

    def _jpt_restriccion_precondicion():
        if hay_restriccion_activa():
            return _jpt_fallo(
                "ya hay una restriccion activa — no se pisa; correr esta ruta "
                "en un momento de juego libre")
        return _jpt_ok("sin restriccion previa")

    def _jpt_restriccion_activar():
        activar_restriccion(
            duenio="test",
            locaciones_permitidas=["casa_hmc"],
            acciones_bloqueadas=["dormir"],
            mensaje_movimiento="TEST: movimiento bloqueado",
        )
        if not hay_restriccion_activa():
            return _jpt_fallo("activar_restriccion no dejo restriccion activa")
        return _jpt_ok("restriccion de prueba activada")

    def _jpt_restriccion_bloqueo_accion():
        msg = accion_bloqueada("dormir")
        if not msg:
            return _jpt_fallo("accion_bloqueada('dormir') no devolvio mensaje")
        return _jpt_ok("dormir bloqueado: '{}'".format(msg))

    def _jpt_restriccion_bloqueo_movimiento():
        msg_bloqueado = accion_bloqueada_movimiento("casa_living")
        msg_permitido = accion_bloqueada_movimiento("casa_hmc")
        if not msg_bloqueado:
            return _jpt_fallo("moverse a casa_living deberia estar bloqueado")
        if msg_permitido:
            return _jpt_fallo(
                "moverse a casa_hmc deberia estar permitido, "
                "pero devolvio: '{}'".format(msg_permitido))
        return _jpt_ok("bloqueo por locacion correcto (living no, hmc si)")

    def _jpt_restriccion_label_locacion():
        restriccion_quest_activa.registrar_label_locacion("casa_hmc", "game_loop")
        lbl = restriccion_quest_activa.obtener_label_locacion("casa_hmc")
        if lbl != "game_loop":
            return _jpt_fallo("obtener_label_locacion devolvio {!r}".format(lbl))
        return _jpt_ok("registro y lookup de label por locacion funciona")

    def _jpt_restriccion_desactivar():
        desactivar_restriccion(duenio="test")
        if hay_restriccion_activa():
            return _jpt_fallo("desactivar_restriccion no libero la restriccion")
        if accion_bloqueada("dormir"):
            return _jpt_fallo("dormir sigue bloqueado tras desactivar")
        return _jpt_ok("restriccion liberada, bloqueos levantados")

    _jpt_loc_cerrada = False

    def _jpt_cond_loc_cerrada():
        return _jpt_loc_cerrada

    def _jpt_bloqueo_locacion_registrado():
        """
        registrar_bloqueo_locacion cierra UNA locacion, con o sin restriccion
        activa (corre despues de liberarla a proposito), y la suelta apenas su
        condicion se apaga — que es lo unico que evita el soft lock.
        """
        global _jpt_loc_cerrada
        _previo = list(BLOQUEOS_LOCACION_REGISTRO.get("casa_sotano", []))
        registrar_bloqueo_locacion(
            "casa_sotano", _jpt_cond_loc_cerrada, "Mejor no bajar ahora")
        try:
            _jpt_loc_cerrada = True
            msg = accion_bloqueada_movimiento("casa_sotano")
            if not msg:
                return _jpt_fallo("el bloqueo de locacion registrado no corto el movimiento")
            if accion_bloqueada_movimiento("casa_living"):
                return _jpt_fallo("el bloqueo de casa_sotano se llevo puesta otra locacion")
            _jpt_loc_cerrada = False
            if accion_bloqueada_movimiento("casa_sotano"):
                return _jpt_fallo("con la condicion apagada el sotano tendria que abrirse")
        finally:
            _jpt_loc_cerrada = False
            if _previo:
                BLOQUEOS_LOCACION_REGISTRO["casa_sotano"] = _previo
            else:
                BLOQUEOS_LOCACION_REGISTRO.pop("casa_sotano", None)
        return _jpt_ok("bloqueo de locacion: cierra solo la suya y se suelta ('{}')".format(msg))

    # =========================================================================
    # RUTA: shopping — compra, entrega, paquete, inventario (DESTRUCTIVA)
    # =========================================================================

    def _jpt_shop_elegir_item():
        for item_id in obtener_todos_los_items():
            if store.stock_tienda.get(item_id, 0) > 0:
                _JPT_CTX["item"] = item_id
                return _jpt_ok("item de prueba: '{}'".format(item_id))
        return _jpt_fallo("ningun item con stock en la tienda")

    def _jpt_shop_fondos():
        precio = obtener_precio_item(_JPT_CTX["item"])
        store.dinero += precio
        _JPT_CTX["precio"] = precio
        return _jpt_ok("fondos asegurados (+{} de dinero)".format(precio))

    def _jpt_shop_comprar():
        if not store.sistema_compras.comprar_item(_JPT_CTX["item"]):
            return _jpt_fallo("comprar_item('{}') devolvio False".format(_JPT_CTX["item"]))
        return _jpt_ok("orden creada para '{}'".format(_JPT_CTX["item"]))

    def _jpt_shop_esperar_entrega():
        for _ in range(10):
            if store.sistema_compras.verificar_entregas_hoy():
                break
            dormir()
        else:
            return _jpt_fallo("tras 10 dias no llego la entrega")
        if not store.repartidor_presente:
            return _jpt_fallo(
                "hay entrega hoy pero repartidor_presente es False "
                "(dormir() deberia haberlo prendido)")
        return _jpt_ok("dia de entrega alcanzado, repartidor presente (dia {})".format(
            store.dias_totales))

    def _jpt_shop_paquete():
        # Al pasar de mañana a tarde sin atender al repartidor, deja el paquete
        avanzar_horario()
        if store.repartidor_presente:
            return _jpt_fallo("el repartidor sigue presente tras avanzar el horario")
        if not getattr(store, "paquete_en_habitacion", False):
            return _jpt_fallo("no quedo paquete_en_habitacion tras irse el repartidor")
        return _jpt_ok("repartidor se fue y dejo el paquete en la habitacion")

    def _jpt_shop_inventario():
        item = _JPT_CTX["item"]
        antes = store.inventario.get(item, 0)
        store.sistema_compras.entregar_items_a_inventario({item: 1})
        despues = store.inventario.get(item, 0)
        if despues != antes + 1:
            return _jpt_fallo("inventario['{}'] {} -> {} (esperaba {})".format(
                item, antes, despues, antes + 1))
        return _jpt_ok("'{}' entregado al inventario ({} -> {})".format(
            item, antes, despues))

    # =========================================================================
    # RUTA: talk — asignacion diaria de estados (DESTRUCTIVA: reasigna el dia)
    # =========================================================================

    def _jpt_talk_asignar():
        problemas = []
        for npc_id in ("violet", "monica", "jasmine"):
            try:
                store.sistema_talk.decrementar_estados_especiales(npc_id)
                store.sistema_talk.asignar_estado_aleatorio(npc_id)
            except Exception as e:
                problemas.append("{}: {!r}".format(npc_id, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("estados diarios reasignados para los 3 NPCs")

    def _jpt_talk_estado_activo():
        detalles = []
        for npc_id in ("violet", "monica", "jasmine"):
            estado = store.sistema_talk.obtener_estado_activo(npc_id)
            detalles.append("{}={}".format(
                npc_id, getattr(estado, "id", estado) if estado else "sin estado"))
        return _jpt_ok(", ".join(detalles))

    # =========================================================================
    # RUTA: mapa — door access y viaje rapido (no destructiva)
    # =========================================================================

    def _jpt_mapa_puertas():
        problemas = []
        for loc_id, npc_id in HABITACION_NPC.items():
            if store.sistema_locaciones.obtener_locacion(loc_id) is None:
                problemas.append("habitacion '{}' no existe".format(loc_id))
            if obtener_npc(npc_id) is None:
                problemas.append("npc '{}' de HABITACION_NPC no existe".format(npc_id))
        for npc_id, loc_id in PASILLO_NPC.items():
            if store.sistema_locaciones.obtener_locacion(loc_id) is None:
                problemas.append("pasillo '{}' de {} no existe".format(loc_id, npc_id))
        # El acceso a habitaciones ya no sale de TABLA_ACCESO_HABITACION (se
        # eliminó): lo otorgan las ventajas de los Hitos de relacion. Se valida
        # que cada NPC con habitacion tenga algun hito que le de acceso, y de
        # paso se corre el chequeo de coherencia del sistema de hitos.
        _ventajas_puerta = (
            "puerta_sale_pasillo", "puerta_dejar_pasar",
            "puerta_ingreso_diurno", "puerta_ingreso_noche",
        )
        for npc_id in HABITACION_NPC.values():
            _tiene = False
            for _h in obtener_hitos_npc(npc_id):
                if any(_v in _h.ventajas for _v in _ventajas_puerta):
                    _tiene = True
                    break
            if not _tiene:
                problemas.append("'{}' sin ningun hito que otorgue acceso a su habitacion".format(npc_id))

        problemas.extend(verificar_coherencia_hitos())

        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("puertas, pasillos e hitos de acceso consistentes")

    def _jpt_mapa_viaje_rapido():
        problemas = []
        locaciones = getattr(store.sistema_locaciones, "locaciones", {}) or {}
        for madre_id, cfg in LOCACIONES_MADRE.items():
            prefijo = cfg.get("prefijo", "")
            if locaciones and not any(l.startswith(prefijo) for l in locaciones):
                problemas.append("madre '{}': ninguna locacion con prefijo '{}'".format(
                    madre_id, prefijo))
        # El viaje recorre la ruta, asi que lo que hay que validar es que el
        # mapa este CONECTADO: un destino del menu al que no se llega caminando
        # cae al salto directo y se pierde el recorrido (y los disparadores del
        # camino). Se prueba contra la locacion destacada de cada madre.
        for madre_id, cfg in LOCACIONES_MADRE.items():
            _destacada = cfg.get("destacada")
            if not _destacada or store.sistema_locaciones.obtener_locacion(_destacada) is None:
                continue
            for _loc in sublocaciones_de_madre(madre_id):
                if _loc.id == _destacada:
                    continue
                if not calcular_ruta(_destacada, _loc.id):
                    problemas.append("sin ruta de '{}' a '{}'".format(
                        _destacada, _loc.id))
        for loc_id in VIAJE_RAPIDO_OCULTAS:
            if store.sistema_locaciones.obtener_locacion(loc_id) is None:
                problemas.append("VIAJE_RAPIDO_OCULTAS: '{}' no existe".format(loc_id))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("viaje rapido consistente con el mapa")

    # =========================================================================
    # RUTA: registros — integridad de los registros declarativos (no destructiva)
    # Cubre la arquitectura post-optimizacion: opciones/overrides/bloqueos de
    # puerta, bloqueos de accion del embudo y triggers de motor. Las condiciones
    # de puerta/bloqueo son lecturas puras y se ejecutan; las funciones de
    # trigger NO se ejecutan (tienen efectos: marcan flags, disparan mensajes) —
    # de ellas solo se valida estructura.
    # =========================================================================

    def _jpt_registros_puertas():
        problemas = []
        for npc_id, regs in OPCIONES_PUERTA_REGISTRO.items():
            for reg in regs:
                if not renpy.has_label(reg["label"]):
                    problemas.append("puerta {}: label '{}' no existe".format(
                        npc_id, reg["label"]))
                if reg["condicion"] is not None:
                    try:
                        reg["condicion"]()
                    except Exception as e:
                        problemas.append("puerta {} '{}': condicion exploto: {!r}".format(
                            npc_id, reg["texto"], e))
        for npc_id, regs in OVERRIDES_PUERTA_REGISTRO.items():
            for _ov in regs:
                if not renpy.has_label(_ov["label"]):
                    problemas.append("override {}: label '{}' no existe".format(
                        npc_id, _ov["label"]))
                try:
                    _ov["condicion"]()
                except Exception as e:
                    problemas.append("override {}: condicion exploto: {!r}".format(
                        npc_id, e))
        for npc_id, regs in BLOQUEOS_GOLPE_REGISTRO.items():
            for _cond, _msg in regs:
                try:
                    _cond()
                except Exception as e:
                    problemas.append("bloqueo golpe {}: condicion exploto: {!r}".format(
                        npc_id, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("registros de puerta validos")

    def _jpt_registros_bloqueos_accion():
        problemas = []
        for accion_id, regs in BLOQUEOS_ACCION_REGISTRO.items():
            for _cond, _msg in regs:
                if not _msg:
                    problemas.append("{}: bloqueo sin mensaje".format(accion_id))
                try:
                    _cond()
                except Exception as e:
                    problemas.append("{}: condicion exploto: {!r}".format(accion_id, e))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("bloqueos de accion del embudo validos")

    def _jpt_registros_triggers():
        problemas = []
        vistos = set()
        registros = (
            ("game_loop", TRIGGERS_GAME_LOOP),
            ("dormir_antes", TRIGGERS_DORMIR_ANTES),
            ("dormir_despues", TRIGGERS_DORMIR_DESPUES),
            ("avanzar", TRIGGERS_AVANZAR),
        )
        total = 0
        for nombre_reg, registro in registros:
            for _prio, _orden, _tid, _fn in registro:
                total += 1
                clave = (nombre_reg, _tid)
                if clave in vistos:
                    problemas.append("{}: id '{}' duplicado".format(nombre_reg, _tid))
                vistos.add(clave)
                if not callable(_fn):
                    problemas.append("{}: '{}' no es callable".format(nombre_reg, _tid))
        if problemas:
            return _jpt_fallo("; ".join(problemas))
        return _jpt_ok("{} triggers registrados, ids unicos, todos callables".format(total))

    def _jpt_registros_activacion():
        """
        Punto de activacion (questsystem_core.activar_quest): todo quest_id
        declarado en un disparador tiene que ser una quest del catalogo, y las
        opciones de puerta/override de las que se deduce la quest por el
        prefijo `quest_` del label tambien. Un id mal escrito no rompe el
        juego (activar_quest lo ignora) pero deja la quest sin activacion, y
        el planificador no la veria nunca.
        """
        problemas = []
        declarados = 0

        def _chequear(origen, label, quest_id):
            _qid = resolver_quest_id_opcion(label, quest_id)
            if not _qid:
                return
            if store.sistema_quests.obtener_quest(_qid) is None:
                problemas.append("{}: quest_id '{}' no existe".format(origen, _qid))

        for _tid, _qid in TRIGGER_QUEST.items():
            if _qid:
                declarados += 1
                _chequear("trigger " + _tid, None, _qid)
        for npc_id, regs in OPCIONES_PUERTA_REGISTRO.items():
            for reg in regs:
                _chequear("puerta {} '{}'".format(npc_id, reg["texto"]),
                          reg["label"], reg.get("quest_id"))
        for npc_id, regs in OVERRIDES_PUERTA_REGISTRO.items():
            for _ov in regs:
                _chequear("override {} '{}'".format(npc_id, _ov["label"]),
                          _ov["label"], _ov.get("quest_id"))
        for _aid, _acc in store.sistema_acciones.acciones.items():
            _chequear("accion " + _aid, _acc.label_generico,
                      getattr(_acc, "quest_id", None))
        for _l in store.sistema_acciones.listeners:
            _chequear("listener {} -> {}".format(_l.accion_id, _l.label), _l.label,
                      getattr(_l, "quest_id", None))
        for _iid, _info in CATALOGO_ITEMS.items():
            _chequear("item " + _iid, _info.get("label_uso"), _info.get("quest_id"))
        if problemas:
            return _jpt_fallo("; ".join(problemas[:8]))
        return _jpt_ok("{} triggers con quest_id; puertas, acciones e items resuelven".format(declarados))

    def _jpt_registros_activar_quest():
        """
        activar_quest sobre una copia: prende narrativa_activa una sola vez,
        no toca la etapa, completar() lo apaga. Corre sobre un deepcopy de una
        quest del catalogo para no ensuciar el estado.
        """
        import copy as _cp
        _q = None
        for _cand in store.sistema_quests.quests.values():
            if getattr(_cand, "linea", "principal") == "principal":
                _q = _cand
                break
        if _q is None:
            return _jpt_fallo("no hay quests en el catalogo")
        _c = _cp.deepcopy(_q)
        _c.activa = True
        _c.completada = False
        _c.etapa_actual = ETAPA_BOTON_LISTO
        _c.narrativa_activa = False
        if not _c.activar():
            return _jpt_fallo("activar() devolvio False en una quest lista")
        if _c.activar():
            return _jpt_fallo("activar() no es idempotente")
        if not getattr(_c, "narrativa_activa", False):
            return _jpt_fallo("narrativa_activa no quedo prendida")
        if _c.etapa_actual != ETAPA_BOTON_LISTO:
            return _jpt_fallo("activar() movio la etapa a {}".format(_c.etapa_actual))
        if _c.activada_dia is None:
            return _jpt_fallo("activada_dia no quedo seteado")
        # Solo la marca: sin memorias, rutinas ni retorno (es una copia).
        _c.narrativa_activa = False
        _c.completada = True
        if activar_quest("__no_es_quest__", origen="test") is not False:
            return _jpt_fallo("activar_quest con id inexistente no devolvio False")
        return _jpt_ok("activar() marca una vez, no mueve la etapa")

    # =========================================================================
    # RUTA: planificador — cobertura, capas y reserva (no destructiva)
    # Corre sobre Recs sueltos y copias de quests: no toca el estado.
    # =========================================================================

    def _jpt_pl_cobertura():
        casos = [
            (Rec("npc", "violet", horario=2, en="casa_hviolet"), Rec("npc", "violet", horario=2, en="casa_living"), True, "npc mismo slot, lugar distinto"),
            (Rec("npc", "violet", horario=2, en="casa_hviolet"), Rec("npc", "violet", horario=2, en="casa_hviolet"), False, "npc mismo lugar"),
            (Rec("npc", "violet", horario=2, en="casa_hviolet"), Rec("npc", "violet", horario=2), False, "npc demanda sin atributos"),
            (Rec("npc", "violet", horario=2, en="casa_hviolet"), Rec("npc", "violet", horario=1, en="casa_living"), False, "npc slots distintos"),
            (Rec("npc", "violet", en="casa_hviolet"), Rec("npc", "violet", dia=6, horario=1, en="casa_living"), True, "npc todo el dia vs slot"),
            (Rec("npc", "violet", en="casa_hviolet"), Rec("npc", "monica", en="casa_living"), False, "npc distinto"),
            (Rec("interaccion", "violet"), Rec("interaccion", "violet", accion="jugar"), True, "interaccion total cubre accion"),
            (Rec("interaccion", "violet", accion="beso"), Rec("interaccion", "violet", accion="jugar"), False, "interaccion acciones distintas"),
            (Rec("puerta", "violet"), Rec("puerta", "violet"), True, "puerta"),
            (Rec("locaciones", locaciones=["casa_hmc", "casa_pasilloarriba"]), Rec("locacion", en="casa_cocina"), True, "locacion fuera de la whitelist"),
            (Rec("locaciones", locaciones=["casa_hmc", "casa_cocina"]), Rec("locacion", en="casa_cocina"), False, "locacion dentro de la whitelist"),
            (Rec("reloj"), Rec("accion", accion="dormir"), True, "reloj cubre dormir"),
            (Rec("mc", horario=2), Rec("mc", horario=2), True, "mc mismo slot"),
            (Rec("mc", horario=2), Rec("mc", horario=1), False, "mc slots distintos"),
            (Rec("mc"), Rec("npc", "violet"), False, "mc no cubre un npc"),
            (Rec("reloj"), Rec("accion", accion="usar_item"), True, "reloj cubre usar_item"),
            (Rec("reloj"), Rec("accion", accion="comprar"), False, "reloj no cubre comprar"),
            (Rec("accion", accion="cocinar"), Rec("accion", accion="cocinar"), True, "accion igual"),
            (Rec("celular"), Rec("mensajes"), True, "celular cubre mensajes"),
            (Rec("mensajes"), Rec("celular"), False, "mensajes no cubre celular"),
        ]
        fallos = [nombre for c, d, esperado, nombre in casos if rec_cubre(c, d) != esperado]
        if fallos:
            return _jpt_fallo("cobertura mal en: " + "; ".join(fallos))
        return _jpt_ok("{} casos de cobertura".format(len(casos)))

    def _jpt_pl_declaraciones():
        """Toda quest de NPC del catalogo tiene declaracion, y las de corrido son las 8 previstas."""
        sin = []
        corrido = []
        for q in store.sistema_quests.quests.values():
            if not getattr(q, "planificada", False):
                sin.append(q.id)
            elif getattr(q, "de_corrido", False):
                corrido.append(q.id)
        if sin:
            return _jpt_fallo("sin declarar_planificacion: " + ", ".join(sorted(sin)[:8]))
        for q in store.sistema_quests.quests.values():
            if not any(r.tipo == "npc" and r.npc == q.npc_id for r in q.demandas):
                return _jpt_fallo("{}: no demanda a su propio NPC".format(q.id))
            for r in list(q.demandas) + list(q.consumos):
                if r.tipo == "npc" and r.npc is None:
                    return _jpt_fallo("{}: Rec npc sin npc".format(q.id))
                if r.tipo in ("interaccion", "puerta") and r.npc is None:
                    return _jpt_fallo("{}: Rec {} sin npc".format(q.id, r.tipo))
                if r.tipo == "accion" and not r.accion:
                    return _jpt_fallo("{}: Rec accion sin accion".format(q.id))
                if r.reserva and not getattr(q, "de_corrido", False):
                    return _jpt_fallo("{}: reserva en una quest que no es de corrido".format(q.id))
        return _jpt_ok("{} quests declaradas, {} de corrido: {}".format(
            len(store.sistema_quests.quests), len(corrido), ", ".join(sorted(corrido))))

    def _jpt_pl_capa1():
        """Capa 1 sobre copias: una de corrido activa frena a la que le pisa la demanda, no a la que no."""
        import copy as _cp
        _reg = store.sistema_quests
        _orig = _reg.quests
        try:
            _qs = {k: _cp.deepcopy(v) for k, v in _orig.items()}
            _reg.quests = _qs
            for q in _qs.values():
                q.activa = False
                q.completada = False
                q.etapa_actual = 0
            a = _qs["violet_questprincipal_09_a"]       # de corrido: Violet en su cuarto
            a.activa = True; a.etapa_actual = ETAPA_BOTON_LISTO
            b = _qs["violet_questprincipal_04_d5"]      # consume: Violet en el pasillo a la tarde
            b.activa = True; b.etapa_actual = ETAPA_CONDICIONES
            c = _qs["violet_questprincipal_04_c"]       # no consume nada
            c.activa = True; c.etapa_actual = ETAPA_CONDICIONES
            _r_guard = store.restriccion_quest_activa
            store.restriccion_quest_activa = None
            try:
                ok_b, por_b = planificador_puede_nacer(b)
                ok_c, por_c = planificador_puede_nacer(c)
            finally:
                store.restriccion_quest_activa = _r_guard
            if ok_b or por_b != a.id:
                return _jpt_fallo("04_d5 tendria que esperar detras de 09_a (dio {!r}, {!r})".format(ok_b, por_b))
            if not ok_c:
                return _jpt_fallo("04_c no consume nada y no nacio ({!r})".format(por_c))
        finally:
            _reg.quests = _orig
        return _jpt_ok("09_a frena a 04_d5 y deja pasar a 04_c")

    def _jpt_pl_capa2():
        """Capa 2 sobre copias: el consumo de puerta de 09_a esconde a 07_a; en narrativa no se mide."""
        import copy as _cp
        _reg = store.sistema_quests
        _orig = _reg.quests
        try:
            _qs = {k: _cp.deepcopy(v) for k, v in _orig.items()}
            _reg.quests = _qs
            for q in _qs.values():
                q.activa = False
                q.completada = False
                q.etapa_actual = 0
                q.narrativa_activa = False
            a = _qs["violet_questprincipal_09_a"]
            a.activa = True; a.etapa_actual = ETAPA_BOTON_LISTO
            b = _qs["violet_questprincipal_07_a"]       # demanda puerta:violet
            b.activa = True; b.etapa_actual = ETAPA_BOTON_LISTO
            _r_guard = store.restriccion_quest_activa
            store.restriccion_quest_activa = None
            try:
                ok, motivo = planificador_puede_activarse(b)
                if ok or not motivo:
                    return _jpt_fallo("07_a tendria que estar frenada por la puerta de 09_a")
                if b.bloqueo_activacion != motivo:
                    return _jpt_fallo("bloqueo_activacion no quedo escrito")
                if b.obtener_mensajes()["que_hacer"] != motivo:
                    return _jpt_fallo("el que hacer no muestra el motivo")
                b.narrativa_activa = True
                ok2, _ = planificador_puede_activarse(b)
                if not ok2:
                    return _jpt_fallo("en narrativa no se tiene que medir")
                if b.bloqueo_activacion:
                    return _jpt_fallo("bloqueo_activacion no se limpio en narrativa")
            finally:
                store.restriccion_quest_activa = _r_guard
        finally:
            _reg.quests = _orig
        return _jpt_ok("09_a esconde a 07_a y escribe el que hacer; en narrativa pasa")

    def _jpt_pl_momentaneo():
        """
        Capa 2 estricta (paso A): el 'cuando y donde' sale de las demandas.
        Sobre una copia de 06_a (Violet de noche en su pieza) y de 04_a (MC en
        la cocina a la mañana). Necesita el motor corriendo (NPCs y locaciones).
        """
        import copy as _cp
        _reg = store.sistema_quests
        _orig = _reg.quests
        _h_guard = store.horario_actual
        _loc_guard = store.sistema_locaciones.locacion_actual
        _v = obtener_npc("violet")
        _vloc_guard = _v.locacion_actual
        try:
            _qs = {k: _cp.deepcopy(v) for k, v in _orig.items()}
            _reg.quests = _qs
            for q in _qs.values():
                q.activa = False; q.completada = False; q.etapa_actual = 0; q.narrativa_activa = False
            a = _qs["violet_questprincipal_06_a"]
            a.activa = True; a.etapa_actual = ETAPA_BOTON_LISTO
            store.horario_actual = 1
            _v.locacion_actual = "casa_hviolet"
            if _pl_mundo_cumple(a) is None:
                return _jpt_fallo("06_a a la tarde tendria que dar 'no es el momento'")
            store.horario_actual = 2
            _v.locacion_actual = "casa_living"
            if _pl_mundo_cumple(a) is None:
                return _jpt_fallo("06_a con Violet en el living tendria que fallar")
            _v.locacion_actual = "casa_hviolet"
            _m = _pl_mundo_cumple(a)
            if _m is not None:
                return _jpt_fallo("06_a de noche con Violet en su pieza tendria que pasar: {!r}".format(_m))
            # Madres: "casa" es cualquier casa_*; "fuera" es su propia madre.
            if not _pl_npc_en("violet", "casa") or _pl_npc_en("violet", "fuera"):
                return _jpt_fallo("en su pieza: en=casa tendria que dar True y en=fuera False")
            _v.locacion_actual = "fuera"
            if _pl_npc_en("violet", "casa") or not _pl_npc_en("violet", "fuera"):
                return _jpt_fallo("afuera: en=casa tendria que dar False y en=fuera True")
            b = _qs["violet_questprincipal_04_a"]
            b.activa = True; b.etapa_actual = ETAPA_BOTON_LISTO
            store.horario_actual = 0
            store.sistema_locaciones.locacion_actual = store.sistema_locaciones.obtener_locacion("casa_living")
            if _pl_mundo_cumple(b) is None:
                return _jpt_fallo("04_a con el MC en el living tendria que fallar")
            store.sistema_locaciones.locacion_actual = store.sistema_locaciones.obtener_locacion("casa_cocina")
            _m = _pl_mundo_cumple(b)
            if _m is not None:
                return _jpt_fallo("04_a en la cocina a la mañana tendria que pasar: {!r}".format(_m))
        finally:
            _reg.quests = _orig
            store.horario_actual = _h_guard
            store.sistema_locaciones.locacion_actual = _loc_guard
            _v.locacion_actual = _vloc_guard
        return _jpt_ok("hora y lugar salen de las demandas (06_a, 04_a)")

    def _jpt_pl_reserva():
        """Reserva sobre una copia: toma el proximo slot, bloquea el reloj, vence."""
        import copy as _cp
        _reg = store.sistema_quests
        _orig = _reg.quests
        _res_guard = list(store.planificador_reservas)
        _h_guard = store.horario_actual
        try:
            _qs = {k: _cp.deepcopy(v) for k, v in _orig.items()}
            _reg.quests = _qs
            q = _qs["violet_deseo_06"]                  # reserva violet@noche
            q.activa = True; q.completada = False; q.etapa_actual = ETAPA_BOTON_LISTO
            store.planificador_reservas = []
            store.horario_actual = 1
            planificador_reservar(q)
            if len(store.planificador_reservas) != 1:
                return _jpt_fallo("no reservo ({} reservas)".format(len(store.planificador_reservas)))
            res = store.planificador_reservas[0]
            if res["dia_total"] != store.dias_totales or res["horario"] != 2:
                return _jpt_fallo("slot mal: {!r}".format(res))
            if planificador_reserva_vigente("violet") is not None:
                return _jpt_fallo("a la tarde la reserva de la noche no tendria que regir")
            store.horario_actual = 2
            if planificador_reserva_vigente("violet") is None:
                return _jpt_fallo("a la noche la reserva tendria que regir")
            if not planificador_bloqueo_reloj():
                return _jpt_fallo("el reloj no quedo bloqueado en el slot reservado")
            # El golpe a la puerta NO se bloquea con reserva de slot: la
            # secuencia de Sinceridad entra golpeando (soft lock real 0.1.9.1).
            if obtener_bloqueo_golpe("violet"):
                return _jpt_fallo("la reserva de slot no tendria que bloquear el golpe: {!r}".format(
                    obtener_bloqueo_golpe("violet")))
            planificador_reservar(q)
            if len(store.planificador_reservas) != 1:
                return _jpt_fallo("reservo dos veces")
            store.horario_actual = 3
            planificador_limpiar_reservas()
            if store.planificador_reservas:
                return _jpt_fallo("la reserva vencida no se limpio")
            # Reserva de VIDA (09_a: Violet y Monica hasta completar): rige a
            # cualquier hora, no congela el reloj, filtra el menu, se va al
            # completar.
            a = _qs["violet_questprincipal_09_a"]
            a.activa = True; a.completada = False; a.etapa_actual = ETAPA_BOTON_LISTO
            store.horario_actual = 1
            planificador_reservar(a)
            _npcs = sorted(r["npc"] for r in store.planificador_reservas)
            if _npcs != ["monica", "violet"]:
                return _jpt_fallo("09_a tendria que reservar a monica y violet: {!r}".format(_npcs))
            if planificador_npc_reservado_por("monica") != a.id:
                return _jpt_fallo("monica no quedo reservada por 09_a")
            if planificador_bloqueo_reloj():
                return _jpt_fallo("una reserva de vida no congela el reloj")
            if not obtener_bloqueo_golpe("monica"):
                return _jpt_fallo("la reserva de vida si tendria que bloquear el golpe")
            if planificador_opcion_permitida("monica", "monica_q0_agradecer", "monica_questprincipal_0"):
                return _jpt_fallo("el boton de otra quest tendria que esconderse")
            if not planificador_opcion_permitida("monica", "violet_quest09a_monica_preguntar", a.id):
                return _jpt_fallo("el boton de la 09_a tendria que quedar")
            # Una quest de Violet que no demanda nada de ella (Deseo 15: Ver TV
            # en el sotano) igual queda frenada: es SU quest y ella esta
            # reservada. Una de Jasmine, no.
            d3 = _qs["violet_deseo_03"]
            d3.activa = True; d3.completada = False; d3.etapa_actual = ETAPA_BOTON_LISTO; d3.narrativa_activa = False
            if _pl_conflicto_activacion(d3) is None:
                return _jpt_fallo("deseo 15 tendria que estar frenada por la reserva de Violet")
            j = _qs["jasmine_questprincipal_0_c"]
            j.activa = True; j.completada = False; j.etapa_actual = ETAPA_BOTON_LISTO; j.narrativa_activa = False
            if _pl_conflicto_activacion(j) is not None:
                return _jpt_fallo("una quest de Jasmine no tendria que frenarse por la reserva de Violet/Monica")
            # Deadlock 0_b de Monica <-> 09_a (auditoria 2026-09-15): la 0_b
            # bloquea dormir con su restriccion hasta ir al living, y la 09_a
            # reserva a Monica de vida. (1) Con la restriccion de la 0_b
            # puesta, la reserva no puede esconder su disparador: la duenia de
            # la restriccion activa salta la capa de conflicto. (2) Con esa
            # restriccion puesta, la 09_a (Disp dormir, demanda accion:dormir)
            # no arranca: una restriccion ajena que bloquea dormir la frena.
            m = _qs["monica_questprincipal_0_b"]
            m.activa = True; m.completada = False; m.etapa_actual = ETAPA_BOTON_LISTO; m.narrativa_activa = False
            if _pl_conflicto_activacion(m) is None:
                return _jpt_fallo("la 0_b de Monica tendria que ver la reserva de vida sobre Monica")
            _r_guard2 = store.restriccion_quest_activa
            store.restriccion_quest_activa = RestriccionQuest(
                acciones_bloqueadas=["avanzar_tiempo", "dormir"], duenio="monica_0_b")
            try:
                if not planificador_trigger_permitido(m.id):
                    return _jpt_fallo("con su restriccion puesta, la 0_b de Monica no puede quedar frenada por la reserva")
                a.narrativa_activa = False
                if _pl_conflicto_activacion(a) is None:
                    return _jpt_fallo("la 09_a (dormir) tendria que esperar a una restriccion ajena que bloquea dormir")
            finally:
                store.restriccion_quest_activa = _r_guard2
            store.horario_actual = 3
            store.dias_totales += 5
            planificador_limpiar_reservas()
            if len(store.planificador_reservas) != 2:
                return _jpt_fallo("la reserva de vida no vence con el reloj")
            store.dias_totales -= 5
            planificador_liberar(a.id)
            if store.planificador_reservas:
                return _jpt_fallo("liberar no saco las reservas de vida")

            # ── Reserva del MC ──────────────────────────────────────────
            # Una reserva sobre "mc" frena a CUALQUIER quest ajena (el MC esta
            # en todas las escenas), pero NO a la dueña — si la frenara, la
            # quest no podria correr su propia escena y quedaria trabada, que
            # es la forma exacta de E10/E11.
            store.planificador_reservas = []
            store.horario_actual = 2
            # Aislar: los pasos de arriba dejaron quests activas y sus consumos
            # frenarian a la de prueba por otro motivo, tapando lo que se mide.
            for _q_off in _qs.values():
                _q_off.activa = False
                _q_off.narrativa_activa = False
            _mc = _qs["violet_amor_07"] if "violet_amor_07" in _qs else None
            if _mc is None:
                # Todavia no existe la quest que la usa: se arma la reserva a
                # mano sobre una cualquiera para probar el mecanismo igual.
                _mc = _qs["violet_deseo_06"]
            store.planificador_reservas = [{
                "quest_id": _mc.id, "npc": "mc",
                "dia_total": store.dias_totales, "horario": 2,
                "texto": "reserva de prueba del MC",
            }]
            if planificador_mc_reservado_por() != _mc.id:
                return _jpt_fallo("planificador_mc_reservado_por no devolvio la dueña")
            _mc.activa = True; _mc.completada = False
            _mc.etapa_actual = ETAPA_BOTON_LISTO; _mc.narrativa_activa = False
            if _pl_conflicto_activacion(_mc) is not None:
                return _jpt_fallo("la dueña de la reserva del MC no puede quedar frenada por su propia reserva")
            _otra = _qs["jasmine_questprincipal_0_c"]
            _otra.activa = True; _otra.completada = False
            _otra.etapa_actual = ETAPA_BOTON_LISTO; _otra.narrativa_activa = False
            if _pl_conflicto_activacion(_otra) is None:
                return _jpt_fallo("con el MC reservado, una quest ajena tendria que estar frenada")
            if not planificador_bloqueo_reloj():
                return _jpt_fallo("la reserva del MC tendria que congelar el reloj")
            store.horario_actual = 1
            if planificador_mc_reservado_por() is not None:
                return _jpt_fallo("fuera del slot el MC no tendria que estar reservado")
            store.planificador_reservas = []
        finally:
            _reg.quests = _orig
            store.planificador_reservas = _res_guard
            store.horario_actual = _h_guard
        return _jpt_ok("slot: toma esta noche, bloquea el reloj y vence (el golpe sigue); vida: filtra el menu, bloquea el golpe y dura hasta completar; la duenia de la restriccion no queda frenada; el MC reservado frena a las ajenas y no a la dueña")

    # =========================================================================
    # RUTA: guardado — picklabilidad de todo el estado (no destructiva)
    # =========================================================================

    def _jpt_guardado_picklable():
        fallos = jp_buscar_no_picklables()
        if fallos:
            _muestra = "; ".join(str(f) for f in fallos[:3])
            return _jpt_fallo(
                "{} objetos no picklables (ver "
                "diagnostico_guardado.txt): {}".format(len(fallos), _muestra))
        return _jpt_ok("todo el estado guardable es picklable")

    # =========================================================================
    # Registro de rutas
    # =========================================================================

    JP_RUTAS_TEST = {
        "tiempo": {
            "nombre": "Ciclo de dia completo",
            "sistemas": "tiempo, npcs, quests, mensajes, talk, acciones, compras",
            "destructiva": True,
            "pasos": [
                ("estado inicial valido", _jpt_tiempo_estado_inicial),
                ("avanzar horario", _jpt_tiempo_avanzar),
                ("dormir avanza el dia", _jpt_tiempo_dormir),
                ("save_name refrescado", _jpt_tiempo_save_name),
                ("resets diarios aplicados", _jpt_tiempo_resets),
            ],
        },
        "quests": {
            "nombre": "Integridad del catalogo de quests",
            "sistemas": "quests, npcs, locaciones",
            "destructiva": False,
            "pasos": [
                ("catalogo poblado", _jpt_quests_catalogo),
                ("npc_id de cada quest existe", _jpt_quests_npcs),
                ("rutinas apuntan a locaciones reales", _jpt_quests_rutinas),
                ("pistas/que_hacer ejecutan", _jpt_quests_mensajes),
            ],
        },
        "eventos": {
            "nombre": "Integridad y validacion de eventos",
            "sistemas": "events",
            "destructiva": False,
            "pasos": [
                ("catalogo poblado", _jpt_eventos_catalogo),
                ("condiciones ejecutan", _jpt_eventos_condiciones),
                ("labels de efecto existen", _jpt_eventos_labels),
                ("validar_eventos() corre", _jpt_eventos_validar),
            ],
        },
        "mensajes": {
            "nombre": "Integridad de grupos de mensajes",
            "sistemas": "mensajes, npcs",
            "destructiva": False,
            "pasos": [
                ("grupos registrados", _jpt_mensajes_grupos),
                ("estructura de pasos/opciones", _jpt_mensajes_estructura),
                ("condiciones de entrega ejecutan", _jpt_mensajes_condiciones),
                ("saltos de paso en rango", _jpt_mensajes_saltos),
                ("grupos arrancan de cero al reentregarse", _jpt_mensajes_rejugables),
                ("un mensaje no contestable no bloquea", _jpt_mensajes_bloqueo_respondible),
            ],
        },
        "acciones": {
            "nombre": "Integridad del catalogo de acciones",
            "sistemas": "acciones",
            "destructiva": False,
            "pasos": [
                ("catalogo poblado", _jpt_acciones_catalogo),
                ("labels genericos existen", _jpt_acciones_labels),
                ("disponibilidad ejecuta", _jpt_acciones_disponibilidad),
            ],
        },
        "restriccion": {
            "nombre": "Restriccion: activar, bloquear, liberar",
            "sistemas": "restriccion, quests, locaciones",
            "destructiva": True,
            "pasos": [
                ("sin restriccion previa", _jpt_restriccion_precondicion),
                ("activar restriccion de prueba", _jpt_restriccion_activar),
                ("bloqueo de accion", _jpt_restriccion_bloqueo_accion),
                ("bloqueo de movimiento", _jpt_restriccion_bloqueo_movimiento),
                ("label por locacion", _jpt_restriccion_label_locacion),
                ("desactivar y liberar", _jpt_restriccion_desactivar),
                ("bloqueo de locacion registrado", _jpt_bloqueo_locacion_registrado),
            ],
        },
        "shopping": {
            "nombre": "Compra completa: orden, entrega, paquete, inventario",
            "sistemas": "shopping, tiempo, inventario",
            "destructiva": True,
            "pasos": [
                ("elegir item con stock", _jpt_shop_elegir_item),
                ("asegurar fondos", _jpt_shop_fondos),
                ("comprar (crea orden)", _jpt_shop_comprar),
                ("dormir hasta el dia de entrega", _jpt_shop_esperar_entrega),
                ("repartidor deja el paquete", _jpt_shop_paquete),
                ("entrega al inventario", _jpt_shop_inventario),
            ],
        },
        "talk": {
            "nombre": "Asignacion diaria de estados de talk",
            "sistemas": "talk, npcs",
            "destructiva": True,
            "pasos": [
                ("reasignar estados del dia", _jpt_talk_asignar),
                ("estado activo por NPC", _jpt_talk_estado_activo),
            ],
        },
        "mapa": {
            "nombre": "Door access y viaje rapido consistentes",
            "sistemas": "locaciones, door access, viaje rapido, npcs",
            "destructiva": False,
            "pasos": [
                ("puertas y tabla de acceso", _jpt_mapa_puertas),
                ("viaje rapido", _jpt_mapa_viaje_rapido),
            ],
        },
        "guardado": {
            "nombre": "Picklabilidad del estado guardable",
            "sistemas": "persistencia, todos los sistemas con estado",
            "destructiva": False,
            "pasos": [
                ("todo picklable", _jpt_guardado_picklable),
            ],
        },
        "planificador": {
            "nombre": "Planificador: cobertura, capas y reserva",
            "sistemas": "planificador, quests",
            "destructiva": False,
            "pasos": [
                ("tabla de cobertura", _jpt_pl_cobertura),
                ("declaraciones del catalogo", _jpt_pl_declaraciones),
                ("capa 1: nacer", _jpt_pl_capa1),
                ("capa 2: activar", _jpt_pl_capa2),
                ("capa 2: cuando y donde", _jpt_pl_momentaneo),
                ("reserva", _jpt_pl_reserva),
            ],
        },
        "registros": {
            "nombre": "Integridad de los registros declarativos",
            "sistemas": "door access, embudo de bloqueos, triggers de motor",
            "destructiva": False,
            "pasos": [
                ("registros de puerta", _jpt_registros_puertas),
                ("bloqueos de accion del embudo", _jpt_registros_bloqueos_accion),
                ("triggers de motor", _jpt_registros_triggers),
                ("punto de activacion: ids", _jpt_registros_activacion),
                ("punto de activacion: activar()", _jpt_registros_activar_quest),
            ],
        },
    }

    # =========================================================================
    # Runner
    # =========================================================================

    def _jpt_escribir_reporte(lineas):
        try:
            ruta_archivo = _jpt_os.path.join(config.basedir, "test_rutas_resultado.txt")
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n".join(lineas) + "\n")
        except Exception as e:
            print("[test_rutas] no se pudo escribir el reporte: {!r}".format(e))

    def jp_test_correr(ruta_id):
        """
        Corre una ruta de testeo. La ruta se corta en el primer paso que falla.
        Devuelve True si todos los pasos pasaron.
        """
        if not config.developer:
            return False
        ruta = JP_RUTAS_TEST.get(ruta_id)
        if not ruta:
            print("[test_rutas] ruta '{}' no existe. Disponibles: {}".format(
                ruta_id, ", ".join(sorted(JP_RUTAS_TEST))))
            return False

        _JPT_CTX.clear()
        lineas = [
            "=" * 70,
            "RUTA: {} — {}".format(ruta_id, ruta["nombre"]),
            "Sistemas: {}{}".format(
                ruta["sistemas"], "  [DESTRUCTIVA]" if ruta["destructiva"] else ""),
            "Fecha: {}  |  dia {}, horario {}".format(
                _jpt_time.strftime("%Y-%m-%d %H:%M:%S"),
                getattr(store, "dias_totales", "?"),
                getattr(store, "horario_actual", "?")),
        ]

        todo_ok = True
        for i, (nombre, fn) in enumerate(ruta["pasos"], 1):
            try:
                ok, detalle = fn()
            except Exception as e:
                ok, detalle = False, "EXCEPCION: {!r}".format(e)
            marca = "[OK]   " if ok else "[FALLO]"
            lineas.append("{} {}. {} — {}".format(marca, i, nombre, detalle))
            if not ok:
                todo_ok = False
                lineas.append("Ruta detenida en el paso {} de {}.".format(
                    i, len(ruta["pasos"])))
                break
        if todo_ok:
            lineas.append("Ruta completa: {} pasos OK.".format(len(ruta["pasos"])))

        for linea in lineas:
            print(linea)
        _jpt_escribir_reporte(lineas)
        return todo_ok

    def jp_test_correr_todas(incluir_destructivas=False):
        """
        Corre todas las rutas. Por defecto solo las NO destructivas; con
        incluir_destructivas=True corre tambien las que mutan la partida
        (solo en partidas descartables).
        """
        if not config.developer:
            return
        resultados = {}
        for ruta_id in sorted(JP_RUTAS_TEST):
            if JP_RUTAS_TEST[ruta_id]["destructiva"] and not incluir_destructivas:
                resultados[ruta_id] = "omitida (destructiva)"
                continue
            resultados[ruta_id] = "OK" if jp_test_correr(ruta_id) else "FALLO"

        resumen = ["", "RESUMEN: " + ", ".join(
            "{}={}".format(k, v) for k, v in sorted(resultados.items()))]
        for linea in resumen:
            print(linea)
        _jpt_escribir_reporte(resumen)
