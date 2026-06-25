################################################################################
## Chat de Carl
################################################################################

init 6 python:

    def _carl_q0b_completado():
        """Se ejecuta cuando se completa el chat con Carl en quest 0_b."""
        # Desactivar restricción
        if hasattr(store, 'desactivar_restriccion'):
            store.desactivar_restriccion()
        # Completar la quest
        if hasattr(store, 'completar_quest_actual'):
            store.completar_quest_actual("jasmine")

    # =========================================================================
    # Chat Quest 0_b de Jasmine - Carl pregunta cómo te fue
    # =========================================================================

    chat_carl_quest_j0b = GrupoMensajes(
        id="carl_chat_quest_j0b",
        npc_id="carl",
        mensaje_inicial="¿Como te fue con el regreso a Japitown?",
        trigger_id="carl_quest_j0b",
        foto_inicial=None,
        prioritario=False,
        tabla_recompensas=None,
        accion_al_completar=_carl_q0b_completado,
        pasos=[
            # =================================================================
            # PASO 0: Respuesta inicial del jugador
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Bien, estoy acomodandome, son muchas cosas que hacer y procesar",
                        respuesta_npc="Si, debe ser un monton y estresante\nComo lo venis llevando",
                        puntos={},
                        saltar_a_paso=1
                    ),
                ]
            ),
            # =================================================================
            # PASO 1: Carl pregunta cómo lo lleva (dos opciones)
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Bien, la verdad que es lo que necesitaba para avanzar con mi vida",
                        respuesta_npc="Que bueno que asi sea\nCuando ya estes mas tranquilo nos tenemos que ver y charlar",
                        puntos={},
                        saltar_a_paso=2
                    ),
                    OpcionRespuesta(
                        texto="Es un poco complicado, creo que me va a costar adaptarme",
                        respuesta_npc="Va a ser asi solo al principio, es lo mejor que te podia pasar\nCuando ya estes mas tranquilo nos tenemos que ver y charlar",
                        puntos={},
                        saltar_a_paso=2
                    ),
                ]
            ),
            # =================================================================
            # PASO 2: Respuesta final del jugador
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Gracias Carl, cuando este mas tranquilo te escribo",
                        respuesta_npc="😉",
                        puntos={},
                        saltar_a_paso=-1
                    ),
                ]
            ),
        ]
    )

    sistema_mensajes.registrar_grupo("carl", chat_carl_quest_j0b)
