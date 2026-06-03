################################################################################
## Chat de Tienda CoXplay — Quest 05_a
################################################################################
## Conversación completa con la tienda para comprar el conjunto de cosplays.
## Se divide en 4 grupos encadenados via accion_al_completar.

init 6 python:

    # =========================================================================
    # Helpers
    # =========================================================================

    def _coxplay_es_horario_laboral():
        """Lunes a Sábado (0-5), mañana (0) o tarde (1)."""
        return (
            getattr(store, 'dia_semana_actual', 0) <= 5
            and getattr(store, 'horario_actual', 0) in [0, 1]
        )

    def _coxplay_saludo_jugador():
        """Saludo del jugador según horario al escribir."""
        if getattr(store, 'horario_actual', 0) == 0:
            return "buen día"
        return "buenas tardes"

    def _coxplay_saludo_tienda():
        """Saludo de la tienda según horario al abrir el grupo."""
        if getattr(store, 'horario_actual', 0) == 0:
            return "buen día"
        return "buenas tardes"

    def _coxplay_nombre_mc():
        return getattr(store, 'mc_name', 'Mc') or 'Mc'

    def _coxplay_realizar_pago():
        """Descuenta $200 al ejecutarse como respuesta del jugador."""
        store.dinero = max(0, getattr(store, 'dinero', 0) - 200)
        return ""

    def _coxplay_condicion_pago():
        """Grupo de pago se entrega cuando el jugador tiene $200."""
        return getattr(store, 'dinero', 0) >= 200

    def _coxplay_disparar_g2():
        disparar_mensaje("coxplay_q5a_g2", "tienda_coxplay")

    def _coxplay_disparar_g3():
        disparar_mensaje("coxplay_q5a_g3", "tienda_coxplay")

    def _coxplay_disparar_g4():
        disparar_mensaje("coxplay_q5a_g4", "tienda_coxplay")

    def _coxplay_texto_contacto():
        return "Hola {}, mi nombre es {}, hice hace algunos días una compra con ustedes y estoy buscando un cosplay nuevo.".format(
            _coxplay_saludo_jugador(), _coxplay_nombre_mc()
        )

    def _coxplay_cond_manana():
        return getattr(store, 'horario_actual', 0) == 0

    def _coxplay_cond_no_manana():
        return getattr(store, 'horario_actual', 0) != 0

    def _coxplay_msg_recordar():
        return "Hola {} {}, si me acuerdo ¿Qué estabas buscando?".format(
            _coxplay_nombre_mc(), _coxplay_saludo_tienda()
        )

    # =========================================================================
    # GRUPO 1 — El jugador inicia contacto (sin timing, sin mensaje NPC)
    # =========================================================================

    chat_coxplay_q5a_g1 = GrupoMensajes(
        id="coxplay_q5a_g1",
        npc_id="tienda_coxplay",
        mensaje_inicial="",
        trigger_id="coxplay_q5a_g1",
        accion_al_completar=_coxplay_disparar_g2,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto=_coxplay_texto_contacto,
                        respuesta_npc="",
                        condicion=_coxplay_cond_manana,
                        saltar_a_paso=-1,
                    ),
                    OpcionRespuesta(
                        texto=_coxplay_texto_contacto,
                        respuesta_npc="",
                        condicion=_coxplay_cond_no_manana,
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("tienda_coxplay", chat_coxplay_q5a_g1)

    # =========================================================================
    # GRUPO 2 — Respuesta de la tienda + negociación (horario laboral)
    # =========================================================================

    chat_coxplay_q5a_g2 = GrupoMensajes(
        id="coxplay_q5a_g2",
        npc_id="tienda_coxplay",
        mensaje_inicial="Hola gracias por comunicarte con Tienda CoXplay, recuerda que nuestro horario de atención es de Lunes a Sábado por la mañana y tarde",
        trigger_id="coxplay_q5a_g2",
        condicion_entrega=_coxplay_es_horario_laboral,
        accion_al_completar=_coxplay_disparar_g3,
        pasos=[
            # Paso 0: Pregunta de la tienda → jugador cuenta lo que busca
            PasoConversacion(
                mensaje_npc=_coxplay_msg_recordar,
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Estoy buscando algo para la misma persona, el cosplay que le llevé no lo quiere usar en el evento",
                        respuesta_npc=["Entiendo, tenemos una box en promoción que incluye tres cosplay, te sale $200", "Vas a tener más alternativas"],
                        saltar_a_paso=1,
                    ),
                ]
            ),
            # Paso 1: Jugador acepta → tienda confirma pago y envío
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Es una buena idea, presentarle tres y que ella elija el que más le gusta, el precio también es conveniente",
                        respuesta_npc=["Perfecto, podés abonar a la misma cuenta", "Una vez realizado el pago hacemos el envío"],
                        saltar_a_paso=2,
                    ),
                ]
            ),
            # Paso 2: Jugador se despide → tienda cierra la conversación
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Muchas gracias, les aviso cuando les haga el pago",
                        respuesta_npc="Gracias a vos",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("tienda_coxplay", chat_coxplay_q5a_g2)

    # =========================================================================
    # GRUPO 3 — Confirmación de pago (se entrega cuando el jugador tiene $200)
    # =========================================================================

    chat_coxplay_q5a_g3 = GrupoMensajes(
        id="coxplay_q5a_g3",
        npc_id="tienda_coxplay",
        mensaje_inicial="",
        trigger_id="coxplay_q5a_g3",
        condicion_entrega=_coxplay_condicion_pago,
        accion_al_completar=_coxplay_disparar_g4,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="El pago está realizado",
                        respuesta_npc=_coxplay_realizar_pago,
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("tienda_coxplay", chat_coxplay_q5a_g3)

    def _coxplay_registrar_pedido():
        """Registra el día en que se confirmó el pedido y crea la orden de entrega."""
        store.coxplay_pedido_dia = getattr(store, 'dias_totales', 1)
        if hasattr(store, 'sistema_compras'):
            dia, dia_sem, estacion, año = store.sistema_compras.calcular_fecha_entrega(2)
            store.sistema_compras.crear_orden({"coxplay_box": 1}, dia, dia_sem, estacion, año)

    # =========================================================================
    # GRUPO 4 — Dirección de envío (horario laboral)
    # =========================================================================

    chat_coxplay_q5a_g4 = GrupoMensajes(
        id="coxplay_q5a_g4",
        npc_id="tienda_coxplay",
        mensaje_inicial="Sí ya lo recibimos ¿Para dónde sería el envío?",
        trigger_id="coxplay_q5a_g4",
        condicion_entrega=_coxplay_es_horario_laboral,
        accion_al_completar=_coxplay_registrar_pedido,
        pasos=[
            # Paso 0: Jugador da la dirección → tienda confirma plazo
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Calle 69 casa 22, en Japitown",
                        respuesta_npc="Perfecto, el paquete estará en su domicilio en 2 días",
                        saltar_a_paso=1,
                    ),
                ]
            ),
            # Paso 1: Jugador cierra la conversación
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Lo estaré esperando",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("tienda_coxplay", chat_coxplay_q5a_g4)
