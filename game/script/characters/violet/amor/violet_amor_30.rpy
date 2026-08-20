################################################################################
## Violet — Amor 30 · "¿Que me pongo?"
################################################################################
##     archivo   violet_amor_30.rpy
##     quest     violet_amor_06          (quests_amor_violet.rpy)
##     grupo     violet_amor06_chat      (chat/chat_violet.rpy)
##     label     quest_violet_amor_06    (lo fija el motor: "quest_" + id)
##
## Ultima quest de la linea. Dos tramos:
##
##   1. Al llegar a 30 de amor, Violet escribe. El mensaje sale una TARDE en
##      que ella este en casa y el MC no este con ella — mientras no se den las
##      tres cosas, el grupo queda en espera.
##   2. Con el chat respondido aparece el boton "Necesitabas ayuda con algo",
##      de noche, en su puerta y tambien en ella si estas adentro.
##
## EL CHAT ES UN REQUISITO DE LA QUEST, no un paso suelto: hasta responderlo la
## quest se queda en ETAPA_CONDICIONES y la pista dice que hay que esperar.
##
## LOS DOS BOTONES NO ROMPEN LA REGLA DE "UN SOLO DISPARADOR": son el mismo
## momento visto desde los dos lados de la puerta. Si estas en el pasillo la
## opcion esta en la puerta; si ya entraste, en ella. Nunca se ven los dos.


init python:

    def _va30_activa():
        return quest_lista_para_boton("violet_amor_06")

    # ── Textos de ETAPA_CONDICIONES ──────────────────────────────────────────

    def _pista_va30_condiciones():
        if obtener_stat1("violet") < 30:
            return renpy.translate_string("Puedo seguir acercandome a Violet.")
        return renpy.translate_string("Tengo que esperar por ahora")

    def _quehacer_va30_condiciones():
        if obtener_stat1("violet") < 30:
            return _quehacer_amor_violet(30)
        return renpy.translate_string("Esperar que violet te escriba")

    # ── Chat ─────────────────────────────────────────────────────────────────

    def _va30_chat_condiciones():
        """
        condicion_entrega: Violet en casa y el MC en otra locacion.

        El horario (la tarde) NO se chequea acá — lo cubre momento_horario, que
        es la via declarativa que el motor ya consulta.

        tracker_locacion_npc devuelve None si esta fuera de casa o si una
        restriccion la escondio, asi que "esta en casa" y "no la escondieron"
        salen de la misma consulta.
        """
        _loc_v = tracker_locacion_npc("violet")
        if _loc_v is None:
            return False
        _loc_mc = store.sistema_locaciones.locacion_actual
        if _loc_mc is None:
            return False
        return _loc_mc.id != _loc_v

    def _va30_disparar_chat():
        """
        Trigger de game_loop: habilita el chat al llegar a 30 de amor.

        Devuelve None SIEMPRE — hace su efecto en python y el loop sigue. No
        hace falta un flag de "ya disparado": disparar_por_trigger ignora los
        grupos que ya no estan "pendiente", asi que llamarlo en cada vuelta es
        inofensivo.
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_06")
        if _q is None or not _q.activa or _q.completada:
            return None
        if _q.etapa_actual != ETAPA_CONDICIONES:
            return None
        if obtener_stat1("violet") >= 30:
            store.sistema_mensajes.disparar_por_trigger(
                "manual", "violet_amor06_chat", "violet")
        return None

    # ── Disparadores de la escena ────────────────────────────────────────────

    def _va30_puerta_ayuda():
        """Opcion de puerta. Solo de noche, que es cuando quedaron."""
        return _va30_activa() and store.horario_actual == 2

    def _va30_boton_violet():
        """
        Boton del menu de Violet: lo mismo, pero desde adentro. Pide que ella
        este en su habitacion — si te la cruzas en otro lado, la charla no es
        ahi.
        """
        return (_va30_activa()
                and store.horario_actual == 2
                and tracker_locacion_npc("violet") == "casa_hviolet")


init 5 python:

    registrar_trigger_game_loop("violet_amor_30_chat", _va30_disparar_chat)

    registrar_opcion_puerta("violet", "Necesitabas ayuda con algo",
                            "quest_violet_amor_06", _va30_puerta_ayuda,
                            ocultar_golpear=True)


################################################################################
## La escena — cierre de la quest y de la linea
################################################################################

label quest_violet_amor_06:

    $ ocultar_hud()
    window show

    # Su habitacion explicitamente y no locacion_actual: acá se llega desde el
    # pasillo (opcion de puerta) o desde adentro (click en ella), y la escena
    # pasa siempre en su pieza.
    $ _va30_loc_hv = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _va30_bg = _va30_loc_hv.background if _va30_loc_hv else "#1a1a1a"
    scene expression _va30_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — le pide opinion sobre que ponerse
    # =========================================================================

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_06")

    # Sale al pasillo. El horario NO avanza: la escena es corta.
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    window hide
    $ mostrar_hud()
    jump game_loop
