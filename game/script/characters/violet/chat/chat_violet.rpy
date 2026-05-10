################################################################################
## Chat de Violet — Conversaciones por Mensajes
################################################################################
## Definiciones de conversaciones que se disparan por quests, eventos, etc.

init 6 python:

    def set_vq6_rama_a(): store.vq6_rama_a = True; return ""
    def set_vq6_rama_b(): store.vq6_rama_b = True; return ""
    def set_vq6_rama_c(): store.vq6_rama_c = True; return ""
    
    def set_vq7_rama_a(): store.vq7_rama_a = True; return ""
    def set_vq7_rama_b(): store.vq7_rama_b = True; return ""
    def set_vq7_rama_c(): store.vq7_rama_c = True; return ""


    # =========================================================================
    # QUEST 6 — Chat de deseo 20
    # =========================================================================

    chat_violet_quest6 = GrupoMensajes(
        id="violet_quest7_chat",
        npc_id="violet",
        mensaje_inicial="Acá está...",
        trigger_id="violet_quest7_chat",
        momento_locacion="casa_hviolet",
        momento_horario=2,
        foto_inicial="images/chat/violet/violet_chat_foto_01.png",
        tabla_recompensas=TablaRecompensas({
            "amor": [
                RangoRecompensa(1, 99, {"tipo": "amor", "valor": 1}),
            ],
        }),
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Te dije que te iba a quedar perfecto",
                        respuesta_npc="",
                        puntos={"amor": 2},
                        saltar_a_paso=-1
                    ),
                    OpcionRespuesta(
                        texto="Te dije que era sexy",
                        respuesta_npc="",
                        puntos={"deseo": 2},
                        saltar_a_paso=-1
                    ),
                ]
            ),
        ]
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_quest6)

    # =========================================================================
    # QUEST 7 — Chat de deseo 25
    # =========================================================================

    chat_violet_quest7 = GrupoMensajes(
        id="violet_quest8_chat",
        npc_id="violet",
        mensaje_inicial="Acá está el motivo por el que no lo quiero usar",
        trigger_id="violet_quest8_chat",
        momento_locacion="casa_hviolet",
        momento_horario=2,
        foto_inicial="images/chat/violet/violet_chat_foto_02.png",
        tabla_recompensas=TablaRecompensas({
            "amor": [
                RangoRecompensa(1, 99, {"tipo": "amor", "valor": 1}),
            ],
        }),
        pasos=[
            # Paso 0: Inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No veo el por qué",
                        respuesta_npc=["No te hagas...", "Me aprieta mucho la cola"],
                        puntos={},
                        saltar_a_paso=1
                    ),
                    OpcionRespuesta(
                        texto="Veo que tenes un gran y redondo problema jajaja",
                        respuesta_npc=["No es gracioso...", "Con mi gordo trasero no puedo usar esto"],
                        puntos={},
                        saltar_a_paso=1
                    ),
                ]
            ),
            # Paso 1: Divergencia principal (Ramas A, B, C)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Para mi tu trasero es perfecto",
                        respuesta_npc=["...", "Te volviste un pervertido"],
                        puntos={},
                        saltar_a_paso=2 # Rama A
                    ),
                    OpcionRespuesta(
                        texto="Sí lo podés usar",
                        respuesta_npc="No insistas no lo voy a usar",
                        puntos={},
                        saltar_a_paso=4 # Rama B
                    ),
                    OpcionRespuesta(
                        texto="Entiendo, no deberías usarlo",
                        respuesta_npc="Por fin estamos de acuerdo en algo",
                        puntos={},
                        saltar_a_paso=6 # Rama C
                    ),
                ]
            ),
            # ======================== RAMA A ========================
            # Paso 2: Rama A inicio 
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Jajajaja solo te fui sincero",
                        respuesta_npc="¿Desde el principio esto era lo que querias?",
                        puntos={},
                        saltar_a_paso=3
                    ),
                    OpcionRespuesta(
                        texto="¿Mala mía?",
                        respuesta_npc="¿Desde el principio esto era lo que querias?",
                        puntos={},
                        saltar_a_paso=3
                    ),
                ]
            ),
            # Paso 3: Rama A continuacion
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No, te lo compre con buenas intenciones",
                        respuesta_npc="No lo parece",
                        puntos={},
                        saltar_a_paso=8
                    ),
                    OpcionRespuesta(
                        texto="¿Eso piensas de mi?",
                        respuesta_npc="Si...",
                        puntos={},
                        saltar_a_paso=8
                    ),
                ]
            ),
            # Paso 8 (Rama A extension)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Esta bien que no me creas",
                        respuesta_npc="",
                        puntos={},
                        saltar_a_paso=9
                    )
                ]
            ),
            # Paso 9 (Rama A extension 2)
            PasoConversacion(
                mensaje_npc="",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Pero no sabia de ese trasero cuando lo compre",
                        respuesta_npc="...",
                        puntos={},
                        saltar_a_paso=10
                    )
                ]
            ),
            # Paso 10 (Rama A final)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No te enojes, sabes que siempre me gusto y me va a gustar pelearte",
                        respuesta_npc="Idiota",
                        puntos={},
                        saltar_a_paso=11
                    ),
                    OpcionRespuesta(
                        texto="Si lo hubiera sabido tampoco hubiera cambiado la elección, me encanta cómo te queda",
                        respuesta_npc="Idiota",
                        puntos={},
                        saltar_a_paso=11
                    ),
                ]
            ),
            # Paso 11 (Rama A cierre y variable)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Solo un poco jajaja",
                        respuesta_npc=set_vq6_rama_a,
                        puntos={},
                        saltar_a_paso=-1
                    )
                ]
            ),
            # ======================== RAMA B ========================
            # Paso 4: Rama B inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No digo que lo uses, solo que si quieres lo puedes usar",
                        respuesta_npc="Llamar la atencion no es lo mio",
                        puntos={},
                        saltar_a_paso=5
                    ),
                    OpcionRespuesta(
                        texto="Entiendo que no quieras ser la envidia del lugar",
                        respuesta_npc="Llamar la atencion no es lo mio",
                        puntos={},
                        saltar_a_paso=5
                    )
                ]
            ),
            # Paso 5: Rama B final
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Eres linda, uses lo que uses vas a llamar la atención",
                        respuesta_npc="Idiota",
                        puntos={},
                        saltar_a_paso=12
                    ),
                    OpcionRespuesta(
                        texto="Mientras llames la mia yo estoy conforme",
                        respuesta_npc="Idiota",
                        puntos={},
                        saltar_a_paso=12
                    ),
                ]
            ),
            # Paso 12 (Rama B cierre y variable)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Jajajaja un poco si",
                        respuesta_npc=set_vq6_rama_b,
                        puntos={},
                        saltar_a_paso=-1
                    )
                ]
            ),
            # ======================== RAMA C ========================
            # Paso 6: Rama C inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Me sentiria un poco celoso con todos mirandote",
                        respuesta_npc="",
                        puntos={},
                        saltar_a_paso=13
                    )
                ]
            ),
            # Paso 13: Rama C extension
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="jeje",
                        respuesta_npc=["😲", "¿Celoso por qué?"],
                        puntos={},
                        saltar_a_paso=7
                    )
                ]
            ),
            # Paso 7: Rama C continuacion
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Ya te lo dije",
                        respuesta_npc=["Dimelo de nuevo", "¿En serio te molestaría?"],
                        puntos={},
                        saltar_a_paso=14
                    ),
                    OpcionRespuesta(
                        texto="No se, me imagine la situacion y senti celos",
                        respuesta_npc=["No me lo hubiera imaginado", "¿Encerio te molestaria?"],
                        puntos={},
                        saltar_a_paso=14
                    ),
                ]
            ),
            # Paso 14: Rama C final
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No es que me moleste, solo un poquito de celos",
                        respuesta_npc="idiota",
                        puntos={},
                        saltar_a_paso=15
                    )
                ]
            ),
            # Paso 15 (Rama C cierre y variable)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="jajaja solo un poco",
                        respuesta_npc=set_vq6_rama_c,
                        puntos={},
                        saltar_a_paso=-1
                    )
                ]
            ),
        ]
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_quest7)

    # =========================================================================
    # QUEST 8 — Chat de deseo 30
    # =========================================================================

    chat_violet_quest8 = GrupoMensajes(
        id="violet_quest9_chat",
        npc_id="violet",
        mensaje_inicial="Tengo un trato",
        trigger_id="violet_quest9_chat",
        momento_locacion="casa_hviolet",
        momento_horario=2,
        tabla_recompensas=TablaRecompensas({
            "amor": [
                RangoRecompensa(1, 99, {"tipo": "amor", "valor": 1}),
            ],
        }),
        pasos=[
            # Paso 0: Inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Tienes toda mi atencion",
                        respuesta_npc=["Me había sacado una foto más...", "Te la puedo pasar, pero con una condición"],
                        puntos={},
                        saltar_a_paso=1
                    ),
                    OpcionRespuesta(
                        texto="Mmm... esto me preocupa",
                        respuesta_npc=["Me había sacado una foto más...", "Te la puedo pasar, pero con una condición"],
                        puntos={},
                        saltar_a_paso=1
                    ),
                ]
            ),
            # Paso 1
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Esto suena peligroso",
                        respuesta_npc=["Peligroso es para mí que sigas hablando de mi trasero por toda la casa", "Te la paso así estás feliz, pero dejas de estar por toda la casa hablando de mi trasero", "Trato?"],
                        puntos={},
                        saltar_a_paso=2
                    ),
                    OpcionRespuesta(
                        texto="Depende de la foto",
                        respuesta_npc=["Una de espalda", "😳", "Te la paso así estás feliz, pero dejas de estar por toda la casa hablando de mi trasero", "Trato?"],
                        puntos={},
                        saltar_a_paso=2
                    )
                ]
            ),
            # Paso 2: Mensaje previo luego division
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Podria ser...",
                        respuesta_npc=["Listo, nada de podria ser", "Ya esta"],
                        foto_respuesta="images/chat/violet/violet_chat_foto_03.png",
                        puntos={},
                        saltar_a_paso=3 # Rama A
                    ),
                    OpcionRespuesta(
                        texto="Es un trato justo",
                        respuesta_npc="Bueno tenemos un trato",
                        foto_respuesta="images/chat/violet/violet_chat_foto_03.png",
                        puntos={},
                        saltar_a_paso=5 # Rama B
                    ),
                    OpcionRespuesta(
                        texto="Primero tendría que ver la foto",
                        respuesta_npc="...",
                        foto_respuesta="images/chat/violet/violet_chat_foto_03.png",
                        puntos={},
                        saltar_a_paso=7 # Rama C
                    ),
                ]
            ),
            # ======================== RAMA A ========================
            # Paso 3: Rama A inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Woooow",
                        respuesta_npc="",
                        puntos={},
                        saltar_a_paso=4
                    )
                ]
            ),
            # Paso 4: Rama A final
            PasoConversacion(
                mensaje_npc="",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Esta bien prometo",
                        respuesta_npc=set_vq7_rama_a,
                        puntos={},
                        saltar_a_paso=-1
                    )
                ]
            ),
            # ======================== RAMA B ========================
            # Paso 5: Rama B inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Woooow",
                        respuesta_npc="",
                        puntos={},
                        saltar_a_paso=6
                    )
                ]
            ),
            # Paso 6: Rama B final
            PasoConversacion(
                mensaje_npc="",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Tenemos un trato",
                        respuesta_npc=set_vq7_rama_b,
                        puntos={},
                        saltar_a_paso=-1
                    )
                ]
            ),
            # ======================== RAMA C ========================
            # Paso 7: Rama C inicio
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No hay trato",
                        respuesta_npc=["Pero te mande la foto", "😡"],
                        puntos={},
                        saltar_a_paso=8
                    )
                ]
            ),
            # Paso 8
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Pero te dije que lo iba a pensar segun la foto",
                        respuesta_npc="¿Qué tiene de malo la foto?",
                        puntos={},
                        saltar_a_paso=9
                    )
                ]
            ),
            # Paso 9
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Nada, pero con ese trasero mas ganas me dan de hablar jajaja",
                        respuesta_npc="eres un idiota",
                        puntos={},
                        saltar_a_paso=10
                    )
                ]
            ),
            # Paso 10
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No te enojes, prometo no andar por la casa hablando de tu trasero",
                        respuesta_npc=set_vq7_rama_c,
                        puntos={},
                        saltar_a_paso=-1
                    )
                ]
            ),
        ]
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_quest8)

    # =========================================================================
    # QUEST 12 — Chat visita nocturna
    # =========================================================================

    chat_violet_quest12 = GrupoMensajes(
        id="violet_quest12_chat",
        npc_id="violet",
        mensaje_inicial="Placeholder: Hola, cuando puedas pasate por mi habitacion a la noche...",
        trigger_id="violet_quest12_chat",
        momento_locacion="casa_hviolet",
        momento_horario=1,
        tabla_recompensas=TablaRecompensas({
            "amor": [
                RangoRecompensa(1, 99, {"tipo": "amor", "valor": 1}),
            ],
        }),
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Placeholder: Dale, paso a la noche",
                        respuesta_npc="Placeholder: Genial, te espero",
                        puntos={},
                        saltar_a_paso=-1
                    ),
                    OpcionRespuesta(
                        texto="Placeholder: Esta todo bien?",
                        respuesta_npc="Placeholder: Si, tranquilo, solo quiero mostrarte algo",
                        puntos={},
                        saltar_a_paso=-1
                    ),
                ]
            ),
        ]
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_quest12)
