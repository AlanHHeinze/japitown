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
        # Caso especial: la 0_b ofrece "Intentar hablar" durante TODA la quest
        # (sin exigir BOTON_LISTO), solo por la tarde.
        q = store.sistema_quests.obtener_quest("violet_questprincipal_0_b")
        return bool(q and q.activa and not q.completada and store.horario_actual == 1)

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
        return (quest_lista_para_boton("violet_questprincipal_02_b")
                and store.horario_actual == 2)

    def _puerta_v_04b():
        return quest_lista_para_boton("violet_questprincipal_04_b")

    def _puerta_v_favores_noche():
        # Cadena de los favores (04_d2 → 04_d6): de noche se le puede preguntar
        # desde la puerta, pero Violet solo contesta — no abre. La condicion
        # entera vive en violet_quest_04_favores.rpy.
        return violet_favores_puerta_de_noche()

    def _puerta_v_amor_01():
        # "¿Mejor?" — unico disparador de la quest de amor 5. Solo por la tarde
        # y con Violet en su habitacion: el MC la llama desde el pasillo y ella
        # sale, asi que si no esta adentro no hay a quien llamar.
        if not quest_lista_para_boton("violet_amor_01"):
            return False
        if store.horario_actual != 1:
            return False
        _v = obtener_npc("violet")
        return bool(_v and _v.esta_en_locacion("casa_hviolet"))

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
        return (quest_lista_para_boton("violet_questprincipal_06_a")
                and store.horario_actual == 2)

    def _puerta_v_06b():
        return (quest_lista_para_boton("violet_questprincipal_06_b")
                and store.horario_actual == 2)

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
                            "dar_paquete_quest02_violet", _puerta_v_dar_paquete)
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
                            ocultar_golpear=True)
    # Sin ocultar_golpear: contesta sin abrir, asi que "Golpear la puerta" sigue
    # teniendo sentido y queda disponible al lado.
    registrar_opcion_puerta("violet", "Preguntarle si necesita algo",
                            "violet_q4dfav_de_noche_puerta", _puerta_v_favores_noche)
    registrar_opcion_puerta("violet", "Ya está la comida",
                            "violet_q4d4_avisar", _puerta_v_04d4_avisar,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Ya terminé de limpiar",
                            "violet_q4d6_cierre", _puerta_v_04d6_cierre,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Llamarla",
                            "quest_violet_amor_01", _puerta_v_amor_01,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Ya compré los cosplay",
                            "violet_quest05a_puerta", _puerta_v_05a,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Llegaron los cosplay",
                            "violet_quest05b_puerta", _puerta_v_05b,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Pedirle perdón",
                            "violet_quest05c_puerta", _puerta_v_05c,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Tengo las entradas",
                            "violet_quest06a_puerta", _puerta_v_06a,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Me pediste que pasara",
                            "violet_quest06b_puerta", _puerta_v_06b,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Preguntar por el cosplay",
                            "violet_quest07a_puerta", _puerta_v_07a,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Ya hablé con la tienda",
                            "violet_quest07b_puerta", _puerta_v_07b,
                            ocultar_golpear=True)
    registrar_opcion_puerta("violet", "Despertar a Violet para limpiar",
                            "evento03_violet", _puerta_v_evento03,
                            ocultar_golpear=True, tipo="evento")

    # Override: la 09_a reemplaza el flujo completo de la puerta.
    registrar_override_puerta("violet", _puerta_v_09a_override,
                              "violet_quest09a_manejo_puerta")

    # Bloqueo de golpe: sabado a la mañana esta dormida.
    registrar_bloqueo_golpe("violet", _puerta_v_sabado_dormida,
                            "Violet debe estar dormida.")
