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
        desactivar_restriccion()
        if hay_restriccion_activa():
            return _jpt_fallo("desactivar_restriccion no libero la restriccion")
        if accion_bloqueada("dormir"):
            return _jpt_fallo("dormir sigue bloqueado tras desactivar")
        return _jpt_ok("restriccion liberada, bloqueos levantados")

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
        for origen, destino in VIAJE_RAPIDO_PREVIA.items():
            for loc_id in (origen, destino):
                if store.sistema_locaciones.obtener_locacion(loc_id) is None:
                    problemas.append("VIAJE_RAPIDO_PREVIA: '{}' no existe".format(loc_id))
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
            for _cond, _lbl in regs:
                if not renpy.has_label(_lbl):
                    problemas.append("override {}: label '{}' no existe".format(
                        npc_id, _lbl))
                try:
                    _cond()
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
        "registros": {
            "nombre": "Integridad de los registros declarativos",
            "sistemas": "door access, embudo de bloqueos, triggers de motor",
            "destructiva": False,
            "pasos": [
                ("registros de puerta", _jpt_registros_puertas),
                ("bloqueos de accion del embudo", _jpt_registros_bloqueos_accion),
                ("triggers de motor", _jpt_registros_triggers),
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
