################################################################################
## Quest 09_b — El desenlace de la enfermedad
################################################################################
## No es una Quest registrada: es el CIERRE de la 09_a. Arranca la NOCHE DEL
## TERCER DIA y se resuelve segun `violet_enferma_atencion`, o sea cuanto la
## cuido el jugador.
##
## TRES RAMAS, y las decide el signo del contador:
##
##   == 0  NULO      → nunca hizo nada con ella. No le llega ningun mensaje;
##                     Violet queda NO DISPONIBLE y en su puerta solo sale que
##                     no la molesten. Al dia siguiente la quest se cierra sola.
##   <  0  NEGATIVO  → le escribe agradeciendo con ironia. Contestarle cuesta
##                     -5 de cada stat, y despues queda no disponible igual.
##   >  0  POSITIVO  → lo invita a su habitacion. De acá salen DOS finales:
##                       - va          → la escena en su pieza (y la toalla)
##                       - no va       → a la mañana siguiente le llega el
##                                       MISMO mensaje del negativo, pero
##                                       costando -2 en vez de -5
##
## EL CASO 0 ES RARO PERO POSIBLE: un +1 y un -1 dan 0 igual que no haber hecho
## nada. Se trata como "no hizo nada" a proposito — es el resultado neto.
##
## POR QUE EL MENSAJE DEL REPROCHE ES UNO SOLO: el texto es identico en las dos
## ramas que lo usan y dos `old` iguales rompen el lint. Lo que cambia es el
## precio, que se decide al dispararlo (`vq9b_penalizacion`).
##
## LA DISPONIBILIDAD hace el trabajo pesado del "no la molestes"
## (core/npcs/npc_disponibilidad.rpy): con Violet fuera de juego no se la ve, no
## se la clickea, no contesta mensajes y ninguna quest suya avanza. Lo unico que
## hay que poner a mano es el texto de su puerta.


# Rama del desenlace: None (sin resolver) | "nulo" | "negativo" | "positivo"
default vq9b_rama = None

# Cuanto cuesta contestar el mensaje de reproche. Lo fija quien lo dispara: 5
# si nunca lo invito, 2 si lo invito y el jugador no fue.
default vq9b_penalizacion = 5

# Rama positiva: si ya entro a su habitacion y si consiguio la toalla.
default vq9b_visito = False
default vq9b_toalla = False

# Dia (dias_totales) en que se resolvio la noche. Al siguiente se cierra todo.
default vq9b_dia_resuelto = 0


init python:

    # Cuanto se pierde en cada rama. Van como constantes para que el numero se
    # lea una sola vez y no quede escondido en medio de un label.
    VQ9B_CASTIGO_SIN_INVITAR = 5
    VQ9B_CASTIGO_NO_FUE = 2

    def _vq9b_quest_viva():
        """
        La 09_a sigue abierta y en juego.

        NO usa quest_lista_para_boton a proposito: ese helper devuelve False con
        el NPC no disponible, y justamente las ramas de esta quest dejan a Violet
        fuera de juego. Acá hace falta saber si la quest existe, no si se la
        puede disparar.
        """
        _q = store.sistema_quests.obtener_quest("violet_questprincipal_09_a")
        return bool(_q and _q.activa and not _q.completada
                    and _q.etapa_actual == ETAPA_BOTON_LISTO)

    def _gl_trigger_vq9b_noche():
        """
        Trigger de game_loop: la noche del tercer dia reparte las tres ramas.

        Va por game_loop y no por registrar_trigger_avanzar porque el horario
        tambien lo mueven las acciones y el talk, que llaman a avanzar_horario()
        directo sin pasar por el label del boton.
        """
        if not _vq9b_quest_viva():
            return None
        if getattr(store, 'vq9b_rama', None) is not None:
            return None
        if store.horario_actual != 2:                       # Noche
            return None
        if getattr(store, 'violet_9a_enfermedad_dia', 0) < 3:
            return None
        return "violet_quest09b_noche"

    def _dormir_trigger_vq9b_cierre():
        """
        Trigger de dormir, fase "despues": el dia despues de la noche del
        desenlace.

        Cierra las ramas que terminan solas (nulo y negativo) y, en la positiva,
        castiga al que no fue. La rama positiva jugada se cierra en su propia
        escena, asi que para entonces la quest ya no esta viva y esto no corre.
        """
        if not _vq9b_quest_viva():
            return None

        _rama = getattr(store, 'vq9b_rama', None)
        if _rama is None:
            return None

        # Todavia es la misma noche: el cierre es al dia SIGUIENTE.
        if getattr(store, 'dias_totales', 0) <= getattr(store, 'vq9b_dia_resuelto', 0):
            return None

        if _rama == "positivo" and not getattr(store, 'vq9b_visito', False):
            # Lo invito y no fue. Mismo reproche, mas barato.
            return "violet_quest09b_plantado"

        if _rama in ("nulo", "negativo"):
            return "violet_quest09b_cerrar"

        return None

    # ── Puerta ───────────────────────────────────────────────────────────────

    def _vq9b_puerta_no_molestar():
        """True si al golpear su puerta solo hay que decir que no la molesten."""
        return _vq9b_quest_viva() and not npc_disponible("violet")

    def _vq9b_puerta_entrar():
        """
        Label al que manda la puerta en la rama positiva, o None.

        Dos visitas con la MISMA puerta: la primera es la charla y el pedido de
        la toalla; la segunda solo existe una vez que la trajo. Entre las dos el
        jugador anda suelto y si golpea sin la toalla no pasa nada — cae al
        flujo normal de la puerta.
        """
        if not _vq9b_quest_viva():
            return None
        if getattr(store, 'vq9b_rama', None) != "positivo":
            return None
        if not getattr(store, 'vq9b_visito', False):
            return "violet_quest09b_visita"
        if getattr(store, 'vq9b_toalla', False):
            return "violet_quest09b_toalla"
        return None

    # ── Chats ────────────────────────────────────────────────────────────────

    def _vq9b_chat_reproche_completado():
        """
        accion_al_completar del reproche: cobra el precio que dejo puesto quien
        disparo el mensaje y saca a Violet de juego hasta el dia siguiente.

        Funcion de MODULO: se guarda en el save via el grupo de mensajes.
        """
        _cuanto = getattr(store, 'vq9b_penalizacion', VQ9B_CASTIGO_SIN_INVITAR)
        _v = obtener_npc("violet")
        if _v:
            _v.modificar_stat1(-_cuanto)
            _v.modificar_stat2(-_cuanto)
        if hasattr(store, 'notificar_recordara'):
            store.notificar_recordara("violet")
        marcar_npc_no_disponible("violet", "Mónica pidió que no la molestemos")

    def _vq9b_chat_invitacion_completado():
        """accion_al_completar de la invitacion: no cobra nada, solo deja pasar."""
        pass


init 5 python:

    registrar_trigger_game_loop("vq9b_noche", _gl_trigger_vq9b_noche,
                                prioridad=30, quest_id="violet_questprincipal_09_a")
    registrar_trigger_dormir("vq9b_cierre", "despues",
                             _dormir_trigger_vq9b_cierre, prioridad=45,
                             quest_id="violet_questprincipal_09_a")


init 6 python:

    # ── El reproche ──────────────────────────────────────────────────────────
    # LO COMPARTEN LAS DOS RAMAS que lo usan (el negativo directo y el positivo
    # plantado): mismo texto, distinto precio. Un segundo grupo con el mismo
    # `mensaje_inicial` daria dos `old` iguales y rompe el lint.

    grupo_vq9b_reproche = GrupoMensajes(
        id="violet_q9b_reproche",
        npc_id="violet",
        mensaje_inicial="Gracias por ayudarme estos días...",
        trigger_id="violet_q9b_reproche",
        prioritario=True,
        accion_al_completar=_vq9b_chat_reproche_completado,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Perdón, estuve muy ocupado",
                        respuesta_npc="💔",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_vq9b_reproche)

    # ── La invitacion ────────────────────────────────────────────────────────

    grupo_vq9b_invitacion = GrupoMensajes(
        id="violet_q9b_invitacion",
        npc_id="violet",
        mensaje_inicial="Ven a mi habitación, por favor",
        trigger_id="violet_q9b_invitacion",
        prioritario=True,
        accion_al_completar=_vq9b_chat_invitacion_completado,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Voy para allá",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_vq9b_invitacion)


################################################################################
## 1 · LA NOCHE DEL TERCER DIA — se reparten las ramas
################################################################################
## Ninguna rama muestra escena acá: o llega un mensaje al celular, o no llega
## nada. El label solo decide y devuelve el control.

label violet_quest09b_noche:

    $ vq9b_dia_resuelto = getattr(store, 'dias_totales', 0)
    $ _vq9b_atencion = getattr(store, 'violet_enferma_atencion', 0)

    if _vq9b_atencion > 0:
        # La cuido: la invita.
        $ vq9b_rama = "positivo"
        $ sistema_mensajes.disparar_por_trigger(
            "manual", "violet_q9b_invitacion", "violet")

    elif _vq9b_atencion < 0:
        # La dejo tirada habiendo empezado: el reproche completo.
        $ vq9b_rama = "negativo"
        $ vq9b_penalizacion = VQ9B_CASTIGO_SIN_INVITAR
        $ sistema_mensajes.disparar_por_trigger(
            "manual", "violet_q9b_reproche", "violet")

    else:
        # Ni se acerco. No hay mensaje: se entera al golpear la puerta.
        $ vq9b_rama = "nulo"
        $ ocultar_hud()
        window show
        piensa "Estuve tres días sin acordarme de Violet"
        window hide
        $ mostrar_hud()
        $ notificar_recordara("violet")
        $ marcar_npc_no_disponible("violet", "Mónica pidió que no la molestemos")

    jump game_loop


################################################################################
## 2 · CIERRE AUTOMATICO — al dia siguiente
################################################################################
## Las ramas nulo y negativo se cierran solas: Violet vuelve al juego y la quest
## se completa sin escena.

label violet_quest09b_cerrar:

    $ marcar_npc_disponible("violet")
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_09_a")

    call mensajes_al_despertar from _call_vq9b_cerrar_msgs

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · LO PLANTO — la invito y no fue
################################################################################
## Mismo reproche que la rama negativa pero mas barato: al menos la cuido.
## El chat es prioritario, asi que el jugador lo va a tener que contestar antes
## de seguir con el dia.

label violet_quest09b_plantado:

    $ vq9b_penalizacion = VQ9B_CASTIGO_NO_FUE
    $ sistema_mensajes.disparar_por_trigger(
        "manual", "violet_q9b_reproche", "violet")

    # La quest se cierra ya: el desenlace fue este. Violet queda no disponible
    # por el accion_al_completar del chat y vuelve con el cierre del dia
    # siguiente... pero como la quest ya no esta viva, ese trigger no corre.
    # Por eso se la devuelve al juego acá mismo, apenas termine el mensaje —
    # que es lo unico que falta.
    $ vq9b_rama = "cerrado"
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_09_a")

    call mensajes_al_despertar from _call_vq9b_plantado_msgs

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 4 · LA VISITA — entro a su habitacion
################################################################################
## Se llega por la puerta (override de la 09_a). El MC entra y se queda en la
## posicion del NPC; Violet no tiene sprite de pie: esta en la cama, asi que se
## dibuja con su idle.
##
## ⚠️ LA POSICION DEL IDLE ESTA SIN AJUSTAR. Va con el transform de siempre;
## cuando este el arte definitivo se acomoda con la herramienta de
## posicionamiento (tecla P).

label violet_quest09b_visita:

    $ vq9b_visito = True

    $ ocultar_hud()
    window show

    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    $ _vq9b_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vq9b_bg with fade

    # Violet en la cama (su idle de enferma) y el MC en el lugar que suele
    # ocupar el NPC.
    # La posicion sale de la misma tabla que usa el HUD y la 09_a: `at
    # center` la dejaba en el medio de la pantalla, lejos de la cama.
    $ _vq9b_idle = "images/characters/casa/idle/idle_violet_casa_hviolet_noche_enferma.jpg"
    $ _vq9b_pos = _vq9a_pos_violet[2]
    show expression _vq9b_idle as violet_cama onlayer personajes:
        xpos _vq9b_pos[0] ypos _vq9b_pos[1] xanchor 0.5 yanchor 1.0
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la charla antes de secarla
    # =========================================================================

    show mc_parado_base b_hablando
    mc "Hola ¿Con que te ayudo?"
    show mc_parado_base b_none
    
    violet "Estoy toda transpirada ¿Me podrias secar un poco?"

    show mc_parado_base b_hablando
    mc "Si, ahi te ayudo con eso"
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    # DIRECTO AL MINIJUEGO. Antes acá salia a buscar una toalla al baño de
    # arriba y volvia a golpear la puerta para la segunda visita
    # (violet_quest09b_toalla). Ese rodeo queda fuera: el dialogo que lo
    # pedia todavia no esta escrito, asi que el jugador salia de la escena
    # sin ninguna indicacion y la quest parecia trabada.
    #
    # `secar` se encarga de sacar los sprites: dibuja su propia escena a
    # pantalla completa, asi que no hay que esconderlos acá.
    jump violet_quest09b_secar


################################################################################
## 5 · CON LA TOALLA — la segunda visita
################################################################################

label violet_quest09b_toalla:

    $ ocultar_hud()
    window show

    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    $ _vq9b_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vq9b_bg with fade

    # La posicion sale de la misma tabla que usa el HUD y la 09_a: `at
    # center` la dejaba en el medio de la pantalla, lejos de la cama.
    $ _vq9b_idle = "images/characters/casa/idle/idle_violet_casa_hviolet_noche_enferma.jpg"
    $ _vq9b_pos = _vq9a_pos_violet[2]
    show expression _vq9b_idle as violet_cama onlayer personajes:
        xpos _vq9b_pos[0] ypos _vq9b_pos[1] xanchor 0.5 yanchor 1.0
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la charla antes de secarla
    # =========================================================================

    show mc_parado_base b_hablando
    mc "Hola ¿Con que te ayudo?"
    show mc_parado_base b_none
    
    violet "Estoy toda transpirada ¿Me podrias secar un poco?"

    show mc_parado_base b_hablando
    mc "Si, ahi te ayudo con eso"
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    jump violet_quest09b_secar


################################################################################
## 6 · SECARLE LA TRANSPIRACION — pendiente de contenido
################################################################################
## ⚠️ ESCENA SIN ESCRIBIR. Cierra la quest para que el arco no quede colgado,
## pero el contenido va acá.

label violet_quest09b_secar:

    # Se van los sprites de la charla: de acá en adelante manda el minijuego,
    # que dibuja su propia escena a pantalla completa.
    hide violet_cama
    hide mc_parado_base
    with dissolve

    $ ocultar_hud()
    window show

    # La colcha esta puesta al entrar y se saca antes de jugar.
    $ vq9_colcha = True
    show screen vq9_escena
    with fade

    # =========================================================================
    # CONTENIDO — la charla antes de destaparla
    # =========================================================================

    mc "Te voy a destapar ¿Si?"

    $ vq9_boca_estado = "b_hablando"
    violet "Te vas a tenes que ocupar de todo vos"
    $ vq9_boca_estado = "b_none"

    mc "Si, yo me encargo"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    # Se destapa y empieza la parte jugable. El minijuego se cierra solo por
    # el boton de salir (vq9_salir), que salta a vq9_cierre.
    $ vq9_colcha = False
    $ vq9_boca_estado = "b_none"

    window hide
    hide screen vq9_escena
    $ vq9_cursor_ocultar()

    # El bucle muestra la screen y se queda ahi hasta que el jugador confirme
    # que sale; de ahi salta solo a vq9_cierre.
    jump vq9_bucle
