################################################################################
## Chat de Monica — Conversaciones por Mensajes
################################################################################
## Definiciones de conversaciones que se disparan por quests, eventos, etc.

init 6 python:
    
    # =========================================================================
    # Chat: Violet Quest 01 — Disparador (limpieza del sábado)
    # =========================================================================
    # Se dispara al completar la quest 0 de Violet.
    # Monica pide al MC que limpie con Violet el sábado.
    #
    # FLUJO:
    # Mensaje inicial (Monica) → Paso 0 (MC responde) → Paso 1 (MC responde) → FIN
    #
    
    chat_monica_violet_quest2 = GrupoMensajes(
        id="monica_chat_violet_quest2",
        npc_id="monica",
        mensaje_inicial="[mc_name] con jasmine vamos a estar fuera de casa el próximo sábado durante la mañana",
        trigger_id="violet_quest2_chat_monica",
        tabla_recompensas=TablaRecompensas({}),
        pasos=[
            # =================================================================
            # PASO 0: Monica pide ayuda, MC acepta
            # =================================================================
            PasoConversacion(
                mensaje_npc="Te pido si con Violet pueden colaborar con la limpieza hasta que Raquel vuelva de sus vacaciones",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Ok yo me encargo",
                        respuesta_npc="Quiero que Violet ayude, despertala temprano el sábado",
                        puntos={}
                    ),
                ]
            ),
            # =================================================================
            # PASO 1: MC confirma, Monica cierra con emoji
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Sí Monica, despreocupate",
                        respuesta_npc="👍",
                        puntos={}
                    ),
                ]
            ),
        ]
    )
    sistema_mensajes.registrar_grupo("monica", chat_monica_violet_quest2)
    
    # =========================================================================
    # Chat: Violet Quest 01 — Fallo (no limpió el sábado)
    # =========================================================================
    # Se dispara si llega sábado tarde y la quest no se completó.
    # Monica se decepciona y relación baja.
    #
    # FLUJO:
    # Mensaje inicial (Monica) → Paso 0 (MC responde) → FIN
    #
    
    chat_monica_violet_quest2_fallo = GrupoMensajes(
        id="monica_chat_violet_quest2_fallo",
        npc_id="monica",
        mensaje_inicial="Me dijiste que te ibas a encargar de la limpieza",
        trigger_id="violet_quest2_fallo",
        tabla_recompensas=TablaRecompensas({
            "amor": [
                RangoRecompensa(0, 99, {"tipo": "amor", "valor": -1}),
            ],
        }),
        pasos=[
            # =================================================================
            # PASO 0: MC se disculpa, Monica responde con emoji triste
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Perdon Monica estuve muy ocupado",
                        respuesta_npc="😢",
                        puntos={"amor": 1}
                    ),
                ]
            ),
        ]
    )
    sistema_mensajes.registrar_grupo("monica", chat_monica_violet_quest2_fallo)

