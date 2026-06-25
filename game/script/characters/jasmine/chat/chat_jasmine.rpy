################################################################################
## Chat de Jasmine
################################################################################
## Conversaciones de mensajes de Jasmine.

init 6 python:
    
    # =========================================================================
    # Funciones de condición para el chat de Jasmine quest 0
    # =========================================================================
    
    def _jasmine_dia_mensaje_inicial():
        """Retorna el día en que llegó el primer mensaje de Jasmine (o None)."""
        chat = sistema_mensajes.chats.get("jasmine")
        if chat:
            for msg in chat.historial:
                if msg.emisor == "jasmine":
                    return msg.timestamp[0]
        return None
    
    def _jasmine_quest0b_completada():
        """Retorna True si la quest 0_b de Jasmine ya se completó."""
        try:
            q = sistema_quests.obtener_quest("jasmine_questprincipal_0_b")
            return q is not None and q.completada
        except Exception:
            return False
    
    def _jasmine_chat_cond_normal():
        """Ruta 1: Es el día 1 (mismo día que llegó el mensaje)."""
        dia_msg = _jasmine_dia_mensaje_inicial()
        if dia_msg is None:
            return True
        return dias_totales <= dia_msg
    
    def _jasmine_chat_cond_evento1():
        """Ruta 2: Es día 2+ Y el jugador ya completó el evento de Jasmine."""
        dia_msg = _jasmine_dia_mensaje_inicial()
        if dia_msg is None:
            return False
        if dias_totales <= dia_msg:
            return False  # Todavía es dia 1
        return _jasmine_quest0b_completada()
    
    def _jasmine_chat_cond_tarde():
        """Ruta 3: Es día 2+ Y el jugador NO completó el evento de Jasmine."""
        dia_msg = _jasmine_dia_mensaje_inicial()
        if dia_msg is None:
            return False
        if dias_totales <= dia_msg:
            return False  # Todavía es dia 1
        return not _jasmine_quest0b_completada()

    # =========================================================================
    # Conversacion: Quest 0 completada
    # =========================================================================
    # 
    # RUTAS:
    # Ruta 1 (Normal): paso 0 → 1 → 2 → 3 → FIN
    # Ruta 2 (Evento 1 ya pasó): paso 0 → salto a 5 → FIN
    # Ruta 3 (Más de 1 dia): paso 0 → salto a 4 → salto a 1 → 2 → 3 → FIN
    #
    
    chat_jasmine_quest0 = GrupoMensajes(
        id="jasmine_chat_quest0",
        npc_id="jasmine",
        mensaje_inicial="Gracias por el conjunto que me regalaste, me encantó! Mañana lo voy a empezar a usar 😊",
        trigger_id="jasmine_questprincipal_0_b",
        momento_locacion="casa_hjasmine",
        momento_horario=3,
        prioritario=True,
        tabla_recompensas=TablaRecompensas({
            "amor": [
                RangoRecompensa(1, 5, {"tipo": "amor", "valor": 1}),
                RangoRecompensa(6, 10, {"tipo": "amor", "valor": 2}),
                RangoRecompensa(11, 99, {"tipo": "amor", "valor": 3}),
            ],
        }),
        pasos=[
            # =================================================================
            # PASO 0: Primera respuesta del jugador
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    # --- Ruta 1 (normal): dos opciones ---
                    OpcionRespuesta(
                        texto="Estoy muy contento que te haya gustado",
                        respuesta_npc="❤️",
                        puntos={},
                        condicion=_jasmine_chat_cond_normal
                    ),
                    OpcionRespuesta(
                        texto="Lo sabía, soy muy bueno eligiendo regalos",
                        respuesta_npc="Jajaja sí que tienes ego 😂",
                        puntos={},
                        condicion=_jasmine_chat_cond_normal
                    ),
                    # --- Ruta 2 (evento 1 completado) ---
                    OpcionRespuesta(
                        texto="Perdón, no lo vi",
                        respuesta_npc=["No importa", "La idea era que vengas a verme y lo hiciste", "❤️"],
                        puntos={},
                        condicion=_jasmine_chat_cond_evento1,
                        saltar_a_paso=5
                    ),
                    # --- Ruta 3 (más de 1 dia, sin evento) ---
                    OpcionRespuesta(
                        texto="Perdón, no lo vi",
                        respuesta_npc=["Sí, me di cuenta ya que no me viniste a ver", "😢"],
                        puntos={},
                        condicion=_jasmine_chat_cond_tarde,
                        saltar_a_paso=4
                    ),
                ]
            ),
            
            # =================================================================
            # PASO 1: Jasmine dice que se lo probó (Ruta 1 directa, Ruta 3 llega aqui vía salto)
            # =================================================================
            PasoConversacion(
                mensaje_npc="Aparte me lo acabo de probar y me queda genial",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Todo te debe quedar genial",
                        respuesta_npc="Mm... no sé si es verdad o estás siendo complaciente",
                        puntos={},
                    ),
                    OpcionRespuesta(
                        texto="Viste, tengo buen gusto",
                        respuesta_npc="Aunque me gustaría pelearte, no te lo puedo negar",
                        puntos={},
                    ),
                    OpcionRespuesta(
                        texto="Mañana paso a verte",
                        respuesta_npc="Sí, mañana a la tarde ven a verme",
                        puntos={},
                    ),
                ]
            ),
            
            # =================================================================
            # PASO 2: Jasmine dice "Espera..."
            # =================================================================
            PasoConversacion(
                mensaje_npc="Espera...",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Qué pasa?",
                        respuesta_npc="Un adelanto",
                        puntos={},
                        foto_respuesta="images/chat/jasmine/jasmine_chat_foto_01.png"
                    ),
                ]
            ),
            
            # =================================================================
            # PASO 3: Respuesta a la foto (FIN de Ruta 1 y Ruta 3)
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Hermosa",
                        respuesta_npc=["❤️", "Lo voy a estar usando, cuando quieras pasa a verlo"],
                        puntos={},
                        saltar_a_paso=-1
                    ),
                    OpcionRespuesta(
                        texto="Eso no se hace",
                        respuesta_npc=["Jajaja 😏", "Lo voy a estar usando, cuando quieras pasa a verlo ❤️"],
                        puntos={},
                        saltar_a_paso=-1
                    ),
                ]
            ),
            
            # =================================================================
            # PASO 4: Ruta 3 - Respuesta despues de "no lo vi" (tarde)
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Estuve un poco ocupado pero ya voy a pasar",
                        respuesta_npc=["❤️", "Te estás perdiendo vos de verlo"],
                        puntos={},
                        saltar_a_paso=1
                    ),
                    OpcionRespuesta(
                        texto="Mañana te prometo que voy",
                        respuesta_npc=["❤️", "Te estás perdiendo vos de verlo"],
                        puntos={},
                        saltar_a_paso=1
                    ),
                ]
            ),
            
            # =================================================================
            # PASO 5: Ruta 2 - Respuesta final (evento 1 ya completado)
            # =================================================================
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="❤️",
                        respuesta_npc="",
                        puntos={},
                        saltar_a_paso=-1
                    ),
                ]
            ),
        ]
    )

    sistema_mensajes.registrar_grupo("jasmine", chat_jasmine_quest0)
