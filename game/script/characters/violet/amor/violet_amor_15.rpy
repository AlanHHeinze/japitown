################################################################################
## Violet — Amor 15 · "Juegos Viejos"
################################################################################
##     archivo   violet_amor_15.rpy
##     quest     violet_amor_03           (quests_amor_violet.rpy)
##     label     quest_violet_amor_03     (lo fija el motor: "quest_" + id)
##
## La quest tiene TRES tramos y por eso hay varios labels. El orden es:
##
##   1. Amor 15 → un trigger de game_loop dispara el chat. Solo llega cuando el
##      MC y Violet NO estan en la misma locacion (condicion del grupo).
##   2. Chat completo → hay que esperar UN DIA. Los dos tramos son requisitos de
##      la propia quest, asi que hasta que se cumplan la quest no sale de
##      ETAPA_CONDICIONES y la pista va contando en que fase esta.
##   3. Cumplidos los requisitos, la quest pasa por ETAPA_RUTINA (que manda a
##      Violet al altillo por las noches) y queda en ETAPA_BOTON_LISTO. Ahi el
##      trigger de game_loop dispara las escenas.
##
## DISPARADOR UNICO: el trigger de game_loop. No hay boton — por eso la quest
## esta excluida del "Charlar un rato" del menu de interaccion.
##
## POR QUE EL DIA DE ESPERA NO ES `dias_espera`: ese parametro solo gobierna
## ETAPA_ESPERA, que es el arranque de la quest. Una espera en el MEDIO se hace
## con un Requisito("condicion") que compara dias_totales, como acá.
##
## LAS DOS ESCENAS DE ENTRADA SON SECUENCIALES, no alternativas: al altillo solo
## se llega desde el pasillo de arriba, asi que el jugador ve primero la llamada
## y despues, al subir, la charla.


################################################################################
## Estado
################################################################################

# Dia (dias_totales) en que se completo el chat. None = todavia no paso.
default va15_dia_chat = None

# 0 = nada · 1 = Violet ya lo llamo desde el pasillo · 2 = charla hecha, buscando
default va15_fase = 0

# Veces que el jugador clickeo a Violet mientras buscan. Se acumula acá y no en
# una variable de escena porque entre click y click el jugador esta suelto en el
# loop y puede guardar la partida.
default va15_clicks_violet = 0


init python:

    # ── Requisitos y textos de la quest (los usa quests_amor_violet.rpy) ─────

    def _va15_paso_un_dia():
        """
        True cuando paso al menos un dia desde que se completo el chat.

        dias_totales es el contador absoluto (sube en cada dormir()), asi que
        compararlo evita todo el enredo de fin de mes o de semana.
        """
        _dia = getattr(store, 'va15_dia_chat', None)
        if _dia is None:
            return False
        return getattr(store, 'dias_totales', 0) > _dia

    def _pista_va15_condiciones():
        """Pista de ETAPA_CONDICIONES — cambia segun el tramo."""
        if obtener_stat1("violet") < 15:
            return renpy.translate_string("Puedo seguir acercandome a Violet.")
        # NO repetir acá la descripcion de la quest: dos `old` con el mismo
        # texto en el tl rompen el lint.
        return renpy.translate_string("Tengo que ver si aparece la Portatil Boy.")

    def _quehacer_va15_condiciones():
        """Que hacer en ETAPA_CONDICIONES — los tres tramos, en orden."""
        if obtener_stat1("violet") < 15:
            return _quehacer_amor_violet(15)
        if not store.sistema_mensajes.grupo_completado("violet_amor03_chat"):
            return renpy.translate_string("Esperar el mensaje de Violet")
        return renpy.translate_string("Darle tiempo para que la busque")

    # ── Chat ─────────────────────────────────────────────────────────────────

    def _va15_chat_separados():
        """
        condicion_entrega del chat: que NO esten en la misma locacion.

        Si Violet esta fuera de casa tracker_locacion_npc devuelve None, que
        nunca va a coincidir con la locacion del MC — o sea que estando ella
        afuera el mensaje tambien llega, que es lo correcto.
        """
        _loc_mc = store.sistema_locaciones.locacion_actual
        if _loc_mc is None:
            return False
        return tracker_locacion_npc("violet") != _loc_mc.id

    def _va15_chat_completado():
        """
        accion_al_completar del chat: anota el dia para empezar a contar la
        espera. Funcion de MODULO — se guarda en el save via el grupo.
        """
        store.va15_dia_chat = getattr(store, 'dias_totales', 0)

    # ── Disparadores ─────────────────────────────────────────────────────────

    def _gl_trigger_violet_amor_15():
        """
        Trigger de game_loop. Hace dos trabajos distintos segun la etapa:

        - En ETAPA_CONDICIONES con amor >= 15: dispara el chat y devuelve None
          (efecto python, el loop sigue normal). disparar_por_trigger ignora los
          grupos que ya no estan "pendiente", asi que llamarlo en cada vuelta es
          inofensivo y no hace falta un flag de "ya disparado".

        - En ETAPA_BOTON_LISTO: devuelve el label de la escena que toque.
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_03")
        if _q is None or not _q.activa or _q.completada:
            return None

        if _q.etapa_actual == ETAPA_CONDICIONES:
            if obtener_stat1("violet") >= 15:
                store.sistema_mensajes.disparar_por_trigger(
                    "manual", "violet_amor03_chat", "violet")
            return None

        if _q.etapa_actual != ETAPA_BOTON_LISTO:
            return None

        # La charla del altillo ya paso: de acá en mas manda la accion Buscar.
        if store.va15_fase >= 2:
            return None

        if store.horario_actual != 2:
            return None

        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None:
            return None

        if _loc.id == "casa_altillo":
            return "violet_amor_15_altillo"

        if store.va15_fase == 0 and _loc.id == "casa_pasilloarriba":
            return "violet_amor_15_pasillo"

        return None

    def _va15_buscar_visible():
        """
        Condicion de la AccionLocacion 'Buscar' (actions_catalog).

        Es `== 2` y no `>= 2`: la escena de cierre sube la fase a 3 antes de
        empezar, y con `>=` el boton habria quedado en el altillo para siempre
        despues de terminar la quest.
        """
        return getattr(store, 'va15_fase', 0) == 2


init 5 python:

    registrar_trigger_game_loop("violet_amor_15_consola",
                                _gl_trigger_violet_amor_15)


################################################################################
## 1 · EL PASILLO — Violet lo llama desde arriba, sin aparecer
################################################################################

label violet_amor_15_pasillo:

    $ ocultar_hud()
    window show

    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — Violet habla SIN sprite: esta arriba, en el altillo
    # =========================================================================

    violet "..."

    # (Mc ojos arriba)
    show mc_parado_base o_arribanm b_hablando
    mc "..."
    # (Mc ojos base boca neutral)
    show mc_parado_base o_base b_none

    violet "..."

    show mc_parado_base b_hablando
    mc "..."
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # Quedo en ir a ayudarla: hasta subir al altillo no se hace otra cosa.
    $ activar_restriccion(
        locaciones_permitidas=["casa_altillo"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Le dije que la iba a ayudar, primero subo al altillo"),
        mensaje_accion_default=_("Le dije que la iba a ayudar, primero subo al altillo"),
        celular_bloqueado=True,
        mensaje_celular=_("Le dije que la iba a ayudar, primero subo al altillo"),
    )

    $ va15_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · EL ALTILLO — la charla, y arranca la busqueda
################################################################################

label violet_amor_15_altillo:

    $ ocultar_hud()
    window show

    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la charla en el altillo antes de ponerse a buscar
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

    # Encerrado en el altillo hasta encontrar la consola. Violet SI queda
    # interactuable (npcs_interactuables): el click en su sprite es medio
    # disparador de la quest — lo atiende violet_amor_15_molestar.
    $ activar_restriccion(
        locaciones_permitidas=["casa_altillo"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("No me puedo ir hasta encontrarla"),
        mensaje_accion_default=_("No me puedo ir hasta encontrarla"),
        npcs_interactuables=["violet"],
        celular_bloqueado=True,
        mensaje_celular=_("No me puedo ir hasta encontrarla"),
    )

    # Recien acá aparece la accion "Buscar" en el altillo.
    $ va15_fase = 2

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · MOLESTARLA — click en el sprite de Violet mientras buscan
################################################################################
## Entra por el jump del principio de `interaccion_violet`: en vez de abrir el
## menu, Violet contesta una linea y el jugador vuelve al loop. Es la excepcion
## a "clickear al NPC siempre abre el menu" — durante la busqueda no hay nada
## que elegir (talk, quests y evento estan todos bloqueados por la restriccion).
##
## A la QUINTA vez se abre una escena. Despues el contador vuelve a cero, asi
## que el ciclo se puede repetir mientras la quest siga abierta.

label violet_amor_15_molestar:

    $ va15_clicks_violet += 1

    if va15_clicks_violet >= 5:
        $ va15_clicks_violet = 0
        jump violet_amor_15_charla

    $ ocultar_hud()
    window show

    if va15_clicks_violet >= 3:
        violet "Basta de molestarme"
    else:
        violet "Vamos, ponte a buscar vos tambien"

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 4 · LA CHARLA DE LA QUINTA VEZ — escena suelta, la quest sigue abierta
################################################################################

label violet_amor_15_charla:

    $ ocultar_hud()
    window show

    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — de tanto interrumpirla, terminan hablando de otra cosa
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

    # La quest NO se completa acá: la consola sigue sin aparecer.
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 5 · BUSCAR — cierre de la quest (accion de locacion del altillo)
################################################################################

label quest_violet_amor_03:

    # Levantar la restriccion primero: si la escena se cortara mas adelante, el
    # jugador quedaria encerrado en el altillo para siempre.
    $ va15_fase = 3
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    $ _va15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va15_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — PARTE A · aparece la consola, todavia en el altillo
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
    # CONTENIDO — PARTE B · siguen la charla en la habitacion de Violet
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ _va15_loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _va15_bg_hviolet = _va15_loc_hviolet.background if _va15_loc_hviolet else "#1a1a1a"
    scene expression _va15_bg_hviolet with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

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

    $ completar_quest_actual("violet", quest_id="violet_amor_03")

    # El MC sale de la habitacion y se le fue la noche buscando: vuelve al
    # pasillo y el horario avanza (noche → trasnoche).
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop
