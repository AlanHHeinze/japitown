################################################################################
## Quest 09_a — Violet enferma
################################################################################

# =============================================================================
# VARIABLES
# =============================================================================
default mc_sabe_violet_enferma      = False
default violet_9a_pedido_actual     = None
# Los que YA SALIERON en esta quest, para no repetir ninguno
# (ver _vq9a_elegir_pedido). Lo limpia la escena de arranque.
default violet_9a_pedidos_usados    = []
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

    # Donde esta cada cosa. La dice Violet despues del pedido, asi el jugador
    # no tiene que recorrer la casa probando acciones.
    #
    # Las locaciones salen de donde esta registrada cada accion
    # (core/actions/actions_catalog.rpy): heladera y agua en la cocina, la
    # medicina en el baño de abajo y la toalla en el de arriba.
    #
    # "Dile a Monica que venga" NO esta en la tabla a proposito: no es un
    # objeto que haya que ir a buscar a ningun lado, es hablar con ella este
    # donde este. Un `.get()` de mas devuelve None y la linea no sale.
    VQ9A_PEDIDOS_DONDE = {
        "Quiero algo de comer":         "Quedó algo en la heladera de la cocina",
        "Necesito tomar el medicamento": "El remedio está en el baño de abajo",
        "Un poco de agua":              "Hay agua fría en la cocina",
        "Tráeme una toalla":            "Hay toallas limpias en el baño de arriba",
    }

    # Lo que manda la tienda esa mañana. Entran al historial del chat ya leidos
    # desde violet_quest09a_inicio; el `piensa` del MC los resume.
    VQ9A_MENSAJES_TIENDA = [
        "Buen día [mc_name], ya revisamos el cosplay y vamos a realizar el cambio.",
        "Por el momento no tenemos stock. Apenas nos entre nos comunicamos.",
    ]

    def _vq9a_elegir_pedido():
        """
        Sortea el pedido del dia entre los que TODAVIA NO PIDIO.

        Sortear sobre la lista entera repartia parejo, pero la quest dura
        tres dias: con tres tiradas sobre cinco opciones, en el 48% de las
        partidas se repetia alguno y se leia como que el sorteo no andaba.
        Sacando de la bolsa los que ya salieron, cada dia trae un pedido
        distinto y el jugador ve las tres tareas.

        Marca el elegido ACÁ ADENTRO y no en el label: si el registro
        quedara del lado de quien llama, alcanza con olvidarlo una vez para
        que la bolsa nunca se vacie y vuelvan los repetidos.

        El `or VQ9A_PEDIDOS` es una red: la quest dura menos dias que
        pedidos hay, pero si algun dia se alargara, con la bolsa vacia
        vuelve a sortear sobre todos en vez de reventar.
        """
        _usados = getattr(store, 'violet_9a_pedidos_usados', None) or []
        _bolsa = [_p for _p in VQ9A_PEDIDOS if _p not in _usados] or VQ9A_PEDIDOS
        _elegido = renpy.random.choice(_bolsa)
        store.violet_9a_pedidos_usados = list(_usados) + [_elegido]
        return _elegido

    def vq9a_pedido_texto():
        """Texto traducido del pedido actual (para mostrar, nunca para comparar)."""
        pedido = getattr(store, 'violet_9a_pedido_actual', None)
        return renpy.translate_string(pedido) if pedido else ""

    def vq9a_donde_texto():
        """
        Donde esta lo que pidio, ya traducido. Cadena vacia si el pedido no
        tiene lugar — el de Monica.
        """
        pedido = getattr(store, 'violet_9a_pedido_actual', None)
        donde = VQ9A_PEDIDOS_DONDE.get(pedido)
        return renpy.translate_string(donde) if donde else ""

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

    def _gl_trigger_violet_09a_precarga():
        """
        Mantiene los dos idles de enferma PRECARGADOS mientras dure la quest.

        Sin esto entrabas a su habitacion y el fondo aparecia solo: el sprite
        llegaba uno o dos segundos despues, y la escena es justamente ella
        acostada al entrar. El HUD lo dibuja con `idle sprite_actual`, donde
        `sprite_actual` sale de una funcion — el predictor de Ren'Py no puede
        adivinar ese valor leyendo la screen, asi que la imagen se cargaba de
        disco recien al mostrarse.

        `start_predict` es acumulativo y no repite trabajo: llamarlo en cada
        vuelta del loop con la imagen ya predicha no cuesta nada.

        Devuelve None SIEMPRE: es un trigger de efecto, no de salto.
        """
        # _vq9b_quest_viva y no quest_lista_para_boton: las ramas de la 09_b
        # dejan a Violet fuera de juego y ese helper devolveria False, pero
        # el sprite se sigue necesitando mientras la quest exista.
        if not _vq9b_quest_viva():
            return None
        renpy.start_predict(
            "images/characters/casa/idle/idle_violet_casa_hviolet_tarde_enferma.jpg",
            "images/characters/casa/idle/idle_violet_casa_hviolet_noche_enferma.jpg",
        )
        return None


init 5 python:
    # El de arranque va con MAS prioridad que el diario: el dia que la quest se
    # estrena tiene que salir la escena, no la cuenta de la enfermedad.
    registrar_trigger_dormir(
        "violet_09a_inicio", "despues", _dormir_trigger_violet_09a_inicio,
        prioridad=40)
    registrar_trigger_dormir(
        "violet_09a_diaria", "despues", _dormir_trigger_violet_09a, prioridad=20)

    registrar_trigger_game_loop(
        "violet_09a_precarga", _gl_trigger_violet_09a_precarga)

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
    # Bolsa de pedidos en cero: si la quest se rejugara desde el debug, no
    # tiene que arrastrar los de la corrida anterior.
    $ violet_9a_pedidos_usados = []

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
    show mc_parado_base c_rbase_celular o_abajonm with sprite_normal

    piensa "Me respondieron de la tienda"
    piensa "Van a realizar el cambio, cuando vuelvan a tener stock se van a comunicar"

    # (Mc cuerpo pensando ojos base)
    show mc_parado_base c_rbase_pensando o_base with sprite_normal

    piensa "Tengo que buscar a Violet para avisarle"

    hide mc_parado_base with dissolve

    # El cartel generico de quest temporal (ui/hud/hud_quest_temporal.rpy) y
    # despues la explicacion de que es.
    call quest_temporal_aviso from _call_v9a_quest_temporal

    tutorial "Este tipo de misiones solo estarán disponibles durante un tiempo, el cierre de la misma cambiará según tus acciones"

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
        piensa "Mónica pidió que no la molestemos"
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

    # ⚠️ NI VIOLET DE PIE NI EL MC EN ESCENA. Violet esta ACOSTADA: el cuadro
    # que corresponde es el de su idle de enferma en la cama, el mismo que se ve
    # al entrar. Pararla con `violet_parada` en pijama lo contradecia, y sumar
    # al MC enfrentado a ella tampoco: el jugador esta al lado de la cama.
    #
    # El idle se repinta a mano en vez de dejar el HUD prendido porque la screen
    # `choice` NO es modal: con el HUD visible se podrian clickear los hotspots
    # de movimiento —o a la propia Violet— con el menu abierto.
    #
    # El sprite y su posicion salen de las mismas tablas que usa la rutina de la
    # quest (quest_violet.rpy), asi no hay dos fuentes que se puedan desfasar.
    $ _v9a_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _v9a_bg

    $ _v9a_idle = _vq9a_sprites_violet.get(horario_actual)
    $ _v9a_pos = _vq9a_pos_violet.get(horario_actual)
    if _v9a_idle and _v9a_pos:
        show expression _v9a_idle as violet_cama:
            xpos _v9a_pos[0] ypos _v9a_pos[1] xanchor 0.5 yanchor 1.0
        with sprite_normal

    menu:
        "¿Necesitas algo?":
            if getattr(store, 'violet_9a_pedido_actual', None) is not None:
                violet "Está bien por ahora."
            else:
                $ store.violet_9a_pedido_actual = _vq9a_elegir_pedido()
                $ _pedido_vq9_txt = vq9a_pedido_texto()
                violet "[_pedido_vq9_txt]."
                # El pedido de Monica no lleva esta linea: no hay nada que ir
                # a buscar. vq9a_donde_texto devuelve "" y el `if` la saltea.
                $ _donde_vq9_txt = vq9a_donde_texto()
                if _donde_vq9_txt:
                    violet "[_donde_vq9_txt]."
        "Volver":
            pass

    hide violet_cama with dissolve
    window hide
    $ mostrar_hud()
    return


# Entrega a Violet: se llama automáticamente cuando tiene_entregable=True.
label violet_quest09a_entregar_directo:
    $ _pedido_vq9 = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show

    # DESDE LA CAMA, igual que el menu de "¿Necesitas algo?". En ningun momento
    # de esta quest se la ve de pie: `violet_parada` la mostraba parada y en
    # pijama justo cuando esta enferma y acostada.
    #
    # El sprite y su posicion salen de las mismas tablas que la rutina de la
    # quest (quest_violet.rpy), asi no hay dos fuentes que se puedan desfasar.
    # Solo hay idle de tarde y de noche, que son los unicos horarios en que se
    # la puede clickear — sin sprite en el HUD no hay como entrar acá.
    $ _v9a_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _v9a_bg

    $ _v9a_idle = _vq9a_sprites_violet.get(horario_actual)
    $ _v9a_pos = _vq9a_pos_violet.get(horario_actual)
    if _v9a_idle and _v9a_pos:
        show expression _v9a_idle as violet_cama:
            xpos _v9a_pos[0] ypos _v9a_pos[1] xanchor 0.5 yanchor 1.0
        with sprite_normal

    if _pedido_vq9 == "Dile a Monica que venga":
        mc "Ya le avisé a Mónica, dijo que en un momento va."
    else:
        mc "Aquí tengo lo que querías."

    violet "Gracias."

    hide violet_cama with dissolve

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
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show monica_parada c_rbase_base o_base b_none at right
    with dissolve

    show mc_parado_base b_hablando
    mc "¿No viste a Violet? Quería hablar con ella."
    show mc_parado_base b_none

    show monica_parada b_hablandochica
    monica "Está en su cuarto. Creo que se pescó algo, estaba medio mal."
    show monica_parada b_none

    hide mc_parado_base
    hide monica_parada
    with dissolve
    $ store.mc_sabe_violet_enferma = True
    window hide
    $ mostrar_hud()
    return


# MC le dice a Monica que Violet la llama (opción "Te llama Violet").
label violet_quest09a_monica_llamar:
    $ ocultar_hud()
    window show
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show monica_parada c_rbase_base o_base b_none at right
    with dissolve

    show mc_parado_base b_hablando
    mc "Mónica, Violet te llama."
    show mc_parado_base b_none

    show monica_parada b_hablandochica
    monica "Dile que en un momento voy."
    show monica_parada b_none

    hide mc_parado_base
    hide monica_parada
    with dissolve
    $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


# Jasmine explica que Violet está enferma (opción "Preguntar por Violet").
label violet_quest09a_jasmine_preguntar:
    $ ocultar_hud()
    window show
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show jasmine_parada c_rbase_base o_base b_none at right
    with dissolve

    show mc_parado_base b_hablando
    mc "¿Viste a Violet? Quería decirle algo."
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "Está en su habitación. Me parece que está enferma, no salió en todo el día."
    show jasmine_parada b_none

    hide mc_parado_base
    hide jasmine_parada
    with dissolve
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
