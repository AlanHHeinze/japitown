################################################################################
## Puerta de Violet — registro declarativo (refactor C8)
################################################################################
## Todo el contenido de la puerta de Violet vive ACA, no en el motor
## (door_access_system.rpy solo itera los registros). El orden de registro de
## las opciones es el orden en que aparecen en el menu de puerta.
##
## Reglas:
## - Condiciones = funciones de MODULO (nunca lambdas: regla anti-pickle).
## - Los textos de las opciones se traducen via renpy.translate_string en el
##   screen; sus `old` viven en tl/english (door_access_system.rpy y
##   botones_interaccion_strings.rpy). Texto nuevo => `old/new` nuevo.
## - El predicado estandar es quest_lista_para_boton(id); solo se agregan
##   condiciones extra cuando la quest las pide (horario, item, chat).

init python:

    # --- Condiciones de opciones de puerta -----------------------------------

    def _puerta_v_0b():
        # "Intentar hablar" durante toda la quest, solo por la tarde. La 0_b no
        # tiene espera ni requisitos, asi que esta en BOTON_LISTO desde que
        # nace: el predicado estandar cubre "toda la quest".
        return quest_lista_para_boton("violet_questprincipal_0_b") and store.horario_actual == 1

    def _puerta_v_dar_paquete():
        return store.inventario.get("mangas_violet", 0) > 0

    def _puerta_v_02a():
        if not quest_lista_para_boton("violet_questprincipal_02_a"):
            return False
        return (not getattr(store, 'violet_quest02a_primer_intento_hecho', False)
                or obtener_stat1("violet") >= 10)

    def _puerta_v_03a():
        return (quest_lista_para_boton("violet_questprincipal_03_a")
                and store.inventario.get("mangas_violet_mc", 0) > 0)

    def _puerta_v_02b():
        # De noche: lo dice la demanda de la quest (capa 2).
        return quest_lista_para_boton("violet_questprincipal_02_b")

    def _puerta_v_04b():
        return quest_lista_para_boton("violet_questprincipal_04_b")

    def _puerta_v_favores_quest_id():
        """Quest del tramo activo del arco, para el tag del boton."""
        _q = violet_favores_cadena_activa()
        return _q.id if _q else None

    def _puerta_v_favores_noche():
        # Cadena de los favores (04_d2 → 04_d6): de noche se le puede preguntar
        # desde la puerta, pero Violet solo contesta — no abre. La condicion
        # entera vive en violet_quest_04_favores.rpy.
        return violet_favores_puerta_de_noche()

    def _puerta_v_amor_01():
        # "¿Mejor?" — unico disparador de la quest de amor 5. Solo por la tarde
        # y con Violet en su habitacion: el MC la llama desde el pasillo y ella
        # sale, asi que si no esta adentro no hay a quien llamar.
        # La tarde y "Violet adentro" son la demanda de la quest (capa 2).
        return quest_lista_para_boton("violet_amor_01")

    def _puerta_v_04d6_cierre():
        # Cierre del arco de los favores: avisarle que ya limpio todo. Va
        # tambien en la puerta porque si Violet esta en su cuarto no hay otra
        # forma de llegar a ella.
        return quest_lista_para_boton("violet_questprincipal_04_d6")

    def _puerta_v_04d4_avisar():
        # Arco de los favores: avisarle que la pizza esta lista. Solo despues de
        # cocinarla (la charla pasa en el pasillo, no adentro).
        return (quest_lista_para_boton("violet_questprincipal_04_d4")
                and getattr(store, 'vq4d4_pizza_cocinada', False))

    def _puerta_v_05a():
        return (quest_lista_para_boton("violet_questprincipal_05_a")
                and store.sistema_mensajes.grupo_completado("coxplay_q5a_g4"))

    def _puerta_v_05b():
        return quest_lista_para_boton("violet_questprincipal_05_b")

    def _puerta_v_05c():
        return quest_lista_para_boton("violet_questprincipal_05_c")

    def _puerta_v_06a():
        # De noche: lo dice la demanda de la quest (capa 2).
        return quest_lista_para_boton("violet_questprincipal_06_a")

    def _puerta_v_06b():
        return quest_lista_para_boton("violet_questprincipal_06_b")

    def _puerta_v_07a():
        return quest_lista_para_boton("violet_questprincipal_07_a")

    def _puerta_v_07b():
        return quest_lista_para_boton("violet_questprincipal_07_b")

    def _puerta_v_evento03():
        ev = store.sistema_events.obtener_event("violet_evento_03")
        return bool(ev and ev.estado == ESTADO_EVENT_ACTIVO
                    and store.dia_semana_actual == 5 and store.horario_actual == 0)

    # --- Condiciones de override y bloqueo de golpe --------------------------

    def _puerta_v_09a_override():
        """
        Durante la enfermedad la puerta entera la maneja la quest.

        NO usa quest_lista_para_boton: ese helper devuelve False con el NPC no
        disponible, y el desenlace de la 09_b deja a Violet justamente asi. Si
        el override se apagara ahi, la puerta caeria al flujo normal y en vez
        de "no la molestes" saldria que no esta en su habitacion.
        """
        return _vq9b_quest_viva()

    def _puerta_v_sabado_dormida():
        # Sabado a la mañana Violet duerme: golpear no hace nada.
        return store.dia_semana_actual == 5 and store.horario_actual == 0


init 5 python:

    # Opciones del menu de puerta, en el orden del menu.
    registrar_opcion_puerta("violet", "Intentar hablar",
                            "quest_violet_questprincipal_0_b", _puerta_v_0b,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Dar paquete",
                            "dar_paquete_quest02_violet", _puerta_v_dar_paquete,
                            quest_id="violet_questprincipal_01_b")
    registrar_opcion_puerta("violet", "Pedir mangas prestados",
                            "quest_violet_questprincipal_02_a", _puerta_v_02a,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Devolver mangas",
                            "quest_violet_questprincipal_03_a", _puerta_v_03a,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Vengo por los mangas",
                            "quest_violet_questprincipal_02_b", _puerta_v_02b,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Golpear la puerta",
                            "violet_quest04b_puerta", _puerta_v_04b,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_04_b")
    # Sin ocultar_golpear: contesta sin abrir, asi que "Golpear la puerta" sigue
    # teniendo sentido y queda disponible al lado.
    # El quest_id va como FUNCION: el boton cubre toda la cadena de favores
    # (04_d2 a 04_d6) y cual esta activa cambia con el tramo, asi que no se
    # puede fijar acá, en init 5.
    registrar_opcion_puerta("violet", "Preguntarle si necesita algo",
                            "violet_q4dfav_de_noche_puerta", _puerta_v_favores_noche,
                            quest_id=_puerta_v_favores_quest_id)
    registrar_opcion_puerta("violet", "Ya está la comida",
                            "violet_q4d4_avisar", _puerta_v_04d4_avisar,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_04_d4")
    registrar_opcion_puerta("violet", "Ya terminé de limpiar",
                            "violet_q4d6_cierre", _puerta_v_04d6_cierre,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_04_d6")
    # Ropa Nueva: la red por si no puede entrar a su pieza. La condicion vive
    # en ventajas/ropanueva/ropanueva_violet.rpy, al lado de la cita.
    # Sin ocultar_golpear: golpear sigue teniendo sentido, y si puede entrar,
    # que entre — la escena la dispara igual el trigger de game_loop.
    registrar_opcion_puerta("violet", "Ver ropa",
                            "violet_rn_puerta", _rn_puerta_ver_ropa)
    registrar_opcion_puerta("violet", "Llamarla",
                            "quest_violet_amor_01", _puerta_v_amor_01,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Ya compré los cosplay",
                            "violet_quest05a_puerta", _puerta_v_05a,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_05_a")
    registrar_opcion_puerta("violet", "Llegaron los cosplay",
                            "violet_quest05b_puerta", _puerta_v_05b,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_05_b")
    registrar_opcion_puerta("violet", "Pedirle perdón",
                            "violet_quest05c_puerta", _puerta_v_05c,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_05_c")
    registrar_opcion_puerta("violet", "Tengo las entradas",
                            "violet_quest06a_puerta", _puerta_v_06a,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_06_a")
    registrar_opcion_puerta("violet", "Me pediste que pasara",
                            "violet_quest06b_puerta", _puerta_v_06b,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_06_b")
    registrar_opcion_puerta("violet", "Preguntar por el cosplay",
                            "violet_quest07a_puerta", _puerta_v_07a,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_07_a")
    registrar_opcion_puerta("violet", "Ya hablé con la tienda",
                            "violet_quest07b_puerta", _puerta_v_07b,
                            ocultar_golpear=True,
                            quest_id="violet_questprincipal_07_b")
    registrar_opcion_puerta("violet", "Despertar a Violet para limpiar",
                            "evento03_violet", _puerta_v_evento03,
                            ocultar_golpear=True, tipo="evento")

    # Override: la 09_a reemplaza el flujo completo de la puerta.
    registrar_override_puerta("violet", _puerta_v_09a_override,
                              "violet_quest09a_manejo_puerta",
                              quest_id="violet_questprincipal_09_a")

    # Bloqueo de golpe: sabado a la mañana esta dormida.
    registrar_bloqueo_golpe("violet", _puerta_v_sabado_dormida,
                            "Violet debe estar dormida.")
