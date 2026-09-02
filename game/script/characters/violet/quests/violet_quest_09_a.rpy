################################################################################
## Quest 09_a — Violet enferma
################################################################################

# =============================================================================
# VARIABLES
# =============================================================================
default mc_sabe_violet_enferma      = False
default violet_9a_pedido_actual     = None
default violet_9a_tiene_entregable  = False
default violet_9a_entrega_completada = False
default violet_9a_piensa_mostrado   = False
default violet_9a_enfermedad_dia    = 0
default violet_enferma_atencion     = 0

init python:

    # Pedidos posibles de Violet enferma. El valor se guarda en el save y se usa
    # como CLAVE de comparacion en varios labels y en interactions_monica, asi que
    # violet_9a_pedido_actual SIEMPRE queda en español: se traduce solo al mostrarlo.
    VQ9A_PEDIDOS = [
        "Quiero algo de comer",
        "Necesito tomar el medicamento",
        "Un poco de agua",
        "Dile a Monica que venga",
        "Tráeme una toalla",
    ]

    # Lo que manda la tienda esa mañana. Entran al historial del chat ya leidos
    # desde violet_quest09a_inicio; el `piensa` del MC los resume.
    VQ9A_MENSAJES_TIENDA = [
        "Buen día [mc_name], ya revisamos el cosplay y vamos a realizar el cambio.",
        "Por el momento no tenemos stock. Apenas nos entre nos comunicamos.",
    ]

    def vq9a_pedido_texto():
        """Texto traducido del pedido actual (para mostrar, nunca para comparar)."""
        pedido = getattr(store, 'violet_9a_pedido_actual', None)
        return renpy.translate_string(pedido) if pedido else ""

    # --- Triggers de motor (registros de triggers_contenido) -----------------

    def _dormir_trigger_violet_09a_inicio():
        """
        Trigger de dormir, fase "despues": la escena de arranque, una sola vez.

        Va en "despues" y no en "antes" porque tiene que pasar al DESPERTAR, con
        el dia nuevo ya puesto: es la mañana en que la tienda le contesta.

        El flag lo pone el propio label. Prioridad alta para que corra antes que
        la gestion diaria de la enfermedad — el primer dia no tiene que penalizar
        nada todavia.
        """
        if (quest_lista_para_boton("violet_questprincipal_09_a")
                and not getattr(store, 'violet_9a_piensa_mostrado', True)):
            return "violet_quest09a_inicio"
        return None

    def _dormir_trigger_violet_09a():
        """
        Gestion diaria de la enfermedad: penaliza el pedido que quedo sin
        entregar, limpia el estado del dia y suma uno al contador.

        YA NO DECIDE EL DESENLACE. Eso pasa la NOCHE del tercer dia y lo maneja
        la 09_b (violet_quest_09_b.rpy), que reparte las tres ramas segun el
        signo de `violet_enferma_atencion`.

        Devuelve None siempre: hace sus efectos en python y el flujo sigue.
        """
        if not _vq9b_quest_viva():
            return None
        if (getattr(store, 'violet_9a_pedido_actual', None)
                and not getattr(store, 'violet_9a_entrega_completada', False)):
            store.violet_enferma_atencion -= 1
        store.violet_9a_pedido_actual = None
        store.violet_9a_tiene_entregable = False
        store.violet_9a_entrega_completada = False
        store.violet_9a_enfermedad_dia = getattr(store, 'violet_9a_enfermedad_dia', 0) + 1
        return None

init 5 python:
    # El de arranque va con MAS prioridad que el diario: el dia que la quest se
    # estrena tiene que salir la escena, no la cuenta de la enfermedad.
    registrar_trigger_dormir(
        "violet_09a_inicio", "despues", _dormir_trigger_violet_09a_inicio,
        prioridad=40)
    registrar_trigger_dormir(
        "violet_09a_diaria", "despues", _dormir_trigger_violet_09a, prioridad=20)

################################################################################
## LABELS
################################################################################

################################################################################
## ARRANQUE — la mañana en que la tienda contesta
################################################################################
## Lo dispara el trigger de DORMIR en fase "despues", una sola vez.
##
## EL CHAT DE LA TIENDA NO SE JUEGA: los mensajes se meten directo en el
## historial y el chat queda LEIDO. Es a proposito — hacer que el jugador abra
## el celular, lea dos lineas y salga no agrega nada, y de paso el `piensa` del
## MC ya dice lo que dicen. Al terminar la escena estan ahi para releerlos,
## pero sin globo de "sin leer".
##
## Por lo mismo la quest ya NO tiene el Requisito("mensaje", ...) que tenia
## antes: nadie los va a "responder", asi que esperar por eso la trababa.

label violet_quest09a_inicio:

    $ violet_9a_piensa_mostrado = True

    # El dia 1 de la enfermedad es HOY. El trigger diario suma uno por noche,
    # asi que la noche del dia 3 el contador vale 3 — que es lo que mira la
    # 09_b para repartir las ramas.
    $ violet_9a_enfermedad_dia = 1

    $ ocultar_hud()
    window show

    # Su habitacion: se despierta ahi.
    $ _v9a_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _v9a_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # Los mensajes entran al historial YA LEIDOS. Se agregan a mano en vez de
    # con un GrupoMensajes porque un grupo entregado deja la conversacion
    # "pendiente de responder" y el badge del celular prendido.
    python:
        sistema_mensajes.inicializar_chat("tienda_coxplay")
        _chat_v9a = sistema_mensajes.chats["tienda_coxplay"]
        for _m_v9a in VQ9A_MENSAJES_TIENDA:
            _chat_v9a.agregar_mensaje("tienda_coxplay",
                                      renpy.translate_string(_m_v9a))
        _chat_v9a.marcar_como_leido()

    # (Mc cuerpo celular ojos abajo sin mirar boca neutral)
    show mc_parado_base c_rbase_celular o_abajonm with sprite_fast

    piensa "Me respondieron de la tienda"
    piensa "Van a realizar el cambio, cuando vuelvan a tener stock se van a comunicar"

    # (Mc cuerpo pensando ojos base)
    show mc_parado_base c_rbase_pensando o_base with sprite_fast

    piensa "Tengo que buscar a Violet para avisarle"

    hide mc_parado_base with dissolve

    # El cartel generico de quest temporal (ui/hud/hud_quest_temporal.rpy) y
    # despues la explicacion de que es.
    call quest_temporal_aviso from _call_v9a_quest_temporal

    tutorial "Este tipo de misiones solo estaran disponible durante un tiempo, el cierre de la misma cambiara segun tus acciones"

    window hide
    $ mostrar_hud()
    jump game_loop


# Manejo de la puerta de Violet durante la enfermedad.
# Salta desde interaccion_puerta_npc antes del flujo normal.
label violet_quest09a_manejo_puerta:

    # Desenlace de la 09_b: o esta fuera de juego, o lo esta esperando adentro.
    # Los dos casos le ganan a todo lo de abajo.
    if _vq9b_puerta_no_molestar():
        window show
        piensa "Monica pidio que no la molestemos"
        window hide
        return

    $ _v9b_destino = _vq9b_puerta_entrar()
    if _v9b_destino:
        jump expression _v9b_destino

    if not getattr(store, 'mc_sabe_violet_enferma', False):
        # MC todavía no sabe que Violet está enferma
        if store.horario_actual in (0, 1):
            # Mañana / tarde: nadie responde
            window show
            piensa "Violet no está... debe estar en su habitación."
            window hide
            return

        elif store.horario_actual == 2:
            # Noche: Violet responde y el MC descubre que está enferma
            $ ocultar_hud()
            hide screen hud_navegacion
            window show
            play sound "audio/sfx/door_knock_3.ogg"
            pause 0.5
            violet "Pasa."
            $ store.mc_sabe_violet_enferma = True
            $ sistema_locaciones.mover_a_locacion("casa_hviolet")
            window hide
            $ mostrar_hud()
            return

        else:
            # Trasnoche
            window show
            piensa "Debe estar durmiendo, no voy a molestar."
            window hide
            return

    else:
        # MC ya sabe que Violet está enferma.
        #
        # LOS DOS HORARIOS EN QUE SE PUEDE ENTRAR SON TARDE Y NOCHE, que son
        # justo los dos para los que existe el idle de Violet enferma
        # (_vq9a_sprites_violet en quest_violet.rpy). De mañana y de trasnoche
        # duerme, y ademas ahi no tiene sprite: entrar seria encontrar la pieza
        # vacia.
        if store.horario_actual == 0:
            # Mañana: durmiendo
            window show
            piensa "Violet debe estar durmiendo, no voy a molestarla."
            window hide
            return

        elif store.horario_actual == 1:
            # Tarde: puede entrar
            $ ocultar_hud()
            hide screen hud_navegacion
            window show
            play sound "audio/sfx/door_knock_3.ogg"
            pause 0.5
            violet "Adelante."
            $ sistema_locaciones.mover_a_locacion("casa_hviolet")
            window hide
            $ mostrar_hud()
            return

        elif store.horario_actual == 2:
            # Noche: puede entrar
            $ ocultar_hud()
            hide screen hud_navegacion
            window show
            play sound "audio/sfx/door_knock_3.ogg"
            pause 0.5
            violet "Adelante."
            $ sistema_locaciones.mover_a_locacion("casa_hviolet")
            window hide
            $ mostrar_hud()
            return

        else:
            # Trasnoche
            window show
            piensa "Debe estar durmiendo, no voy a molestar."
            window hide
            return


# Interacción con Violet enferma en su habitacion.
# Reemplaza el menú de interacción normal durante la quest.
label violet_quest09a_interaccion:
    # Si tiene algo para entregar y no lo ha entregado aún, ir directo a entrega
    if (getattr(store, 'violet_9a_tiene_entregable', False) and
            not getattr(store, 'violet_9a_entrega_completada', False)):
        jump violet_quest09a_entregar_directo

    $ ocultar_hud()
    window show

    show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve

    menu:
        "¿Necesitas algo?":
            if getattr(store, 'violet_9a_pedido_actual', None) is not None:
                show violet_parada b_hablandochica
                violet "Está bien por ahora."
                show violet_parada b_none
            else:
                $ store.violet_9a_pedido_actual = renpy.random.choice(VQ9A_PEDIDOS)
                $ _pedido_vq9_txt = vq9a_pedido_texto()
                show violet_parada b_hablandochica
                violet "[_pedido_vq9_txt]."
                show violet_parada b_none
        "Volver":
            pass

    hide violet_parada with dissolve
    window hide
    $ mostrar_hud()
    return


# Entrega a Violet: se llama automáticamente cuando tiene_entregable=True.
label violet_quest09a_entregar_directo:
    $ _pedido_vq9 = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show

    show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve

    if _pedido_vq9 == "Dile a Monica que venga":
        mc "Ya le avisé a Monica, dijo que en un momento va."
    else:
        mc "Aquí tengo lo que querías."

    show violet_parada b_sonrisaleve
    violet "Gracias."
    show violet_parada b_none

    hide violet_parada with dissolve

    if not getattr(store, 'violet_9a_entrega_completada', False):
        $ store.violet_enferma_atencion += 1
    $ store.violet_9a_entrega_completada = True

    window hide
    $ mostrar_hud()
    return


# Monica explica que Violet está enferma (opción "Preguntar por Violet").
label violet_quest09a_monica_preguntar:
    $ ocultar_hud()
    window show
    mc "¿No viste a Violet? Quería hablar con ella."
    show monica_parada c_rbase_base o_base b_hablandochica at right with dissolve
    monica "Está en su cuarto. Creo que se pescó algo, estaba medio mal."
    show monica_parada b_none
    hide monica_parada with dissolve
    $ store.mc_sabe_violet_enferma = True
    window hide
    $ mostrar_hud()
    return


# MC le dice a Monica que Violet la llama (opción "Te llama Violet").
label violet_quest09a_monica_llamar:
    $ ocultar_hud()
    window show
    mc "Monica, Violet te llama."
    show monica_parada c_rbase_base o_base b_hablandochica at right with dissolve
    monica "Dile que en un momento voy."
    show monica_parada b_none
    hide monica_parada with dissolve
    $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


# Jasmine explica que Violet está enferma (opción "Preguntar por Violet").
label violet_quest09a_jasmine_preguntar:
    $ ocultar_hud()
    window show
    mc "¿Viste a Violet? Quería decirle algo."
    show jasmine_parada c_rbase_base o_base b_hablando at right with dissolve
    jasmine "Está en su habitación. Me parece que está enferma, no salió en todo el día."
    show jasmine_parada b_none
    hide jasmine_parada with dissolve
    $ store.mc_sabe_violet_enferma = True
    window hide
    $ mostrar_hud()
    return


################################################################################
## ACCIONES DE LOCACIÓN — Mini-juego de cuidado
################################################################################

label accion_violet_heladera:
    $ _pedido_h = getattr(store, 'violet_9a_pedido_actual', None)
    $ _pedido_h_txt = vq9a_pedido_texto()
    $ ocultar_hud()
    window show
    if _pedido_h != "Quiero algo de comer":
        piensa "Violet me pidió [_pedido_h_txt]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Aquí tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


label accion_violet_agua:
    $ _pedido_a = getattr(store, 'violet_9a_pedido_actual', None)
    $ _pedido_a_txt = vq9a_pedido_texto()
    $ ocultar_hud()
    window show
    if _pedido_a != "Un poco de agua":
        piensa "Violet me pidió [_pedido_a_txt]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Aquí tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


label accion_violet_medicina:
    $ _pedido_m = getattr(store, 'violet_9a_pedido_actual', None)
    $ _pedido_m_txt = vq9a_pedido_texto()
    $ ocultar_hud()
    window show
    if _pedido_m != "Necesito tomar el medicamento":
        piensa "Violet me pidió [_pedido_m_txt]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Aquí tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


label accion_violet_toalla:

    # Desenlace de la 09_b: la toalla que le pidio al visitarla. Con eso la
    # segunda visita ya no pasa por el menu, entra directo a la escena.
    if _vq9b_toalla_activa():
        $ vq9b_toalla = True
        $ ocultar_hud()
        window show
        piensa "Ya tengo la toalla, se la llevo"
        window hide
        $ mostrar_hud()
        return

    $ _pedido_t = getattr(store, 'violet_9a_pedido_actual', None)
    $ _pedido_t_txt = vq9a_pedido_texto()
    $ ocultar_hud()
    window show
    if _pedido_t != "Tráeme una toalla":
        piensa "Violet me pidió [_pedido_t_txt]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Aquí tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


################################################################################
## LABEL DE QUEST (ETAPA_DESARROLLO) — seguridad
################################################################################

label quest_violet_questprincipal_09_a:
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_09_a")
    window hide
    $ mostrar_hud()
    jump game_loop
