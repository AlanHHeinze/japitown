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
    # QUEST 04_C — Chat de deseo 20
    # =========================================================================

    chat_violet_quest6 = GrupoMensajes(
        id="violet_quest04c_chat",
        npc_id="violet",
        mensaje_inicial="Aquí está...",
        trigger_id="violet_quest04c_chat",
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
                        texto="Es perfecto para ti",
                        respuesta_npc="",
                        puntos={"amor": 5},
                        saltar_a_paso=-1
                    ),
                    OpcionRespuesta(
                        texto="No diria apretado, diria sexy",
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
    # QUEST 04_D — Chat de deseo 25
    # =========================================================================

    chat_violet_quest7 = GrupoMensajes(
        id="violet_quest04d_chat",
        npc_id="violet",
        mensaje_inicial="Aquí está el motivo por el que no lo quiero usar",
        trigger_id="violet_quest04d_chat",
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
                        texto="Sí lo puedes usar",
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
                        respuesta_npc="¿Desde el principio esto era lo que querías?",
                        puntos={},
                        saltar_a_paso=3
                    ),
                    OpcionRespuesta(
                        texto="¿Mala mía?",
                        respuesta_npc="¿Desde el principio esto era lo que querías?",
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
                        respuesta_npc="Sí...",
                        puntos={},
                        saltar_a_paso=8
                    ),
                ]
            ),
            # Paso 8 (Rama A extension)
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Está bien que no me creas",
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
                        respuesta_npc="Llamar la atención no es lo mío",
                        puntos={},
                        saltar_a_paso=5
                    ),
                    OpcionRespuesta(
                        texto="Entiendo que no quieras ser la envidia del lugar",
                        respuesta_npc="Llamar la atención no es lo mío",
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
                        texto="Mientras llames la mía yo estoy conforme",
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
                        texto="No se, me imagine la situación y senti celos",
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
    # QUEST 04_E — Chat de deseo 30
    # =========================================================================

    chat_violet_quest8 = GrupoMensajes(
        id="violet_quest04e_chat",
        npc_id="violet",
        mensaje_inicial="Tengo un trato",
        trigger_id="violet_quest04e_chat",
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
                        texto="Tienes toda mi atención",
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
                        texto="Podría ser...",
                        respuesta_npc=["Listo, nada de podría ser", "Ya esta"],
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
                        texto="Está bien prometo",
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
                        texto="Nada, pero con ese trasero más ganas me dan de hablar jajaja",
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
        mensaje_inicial="Placeholder: Hola, cuando puedas pasate por mi habitación a la noche...",
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

    # =========================================================================
    # QUEST 05_C — Violet le escribe al MC (noche, Violet en su habitacion)
    # =========================================================================

    chat_violet_q5c_g1 = GrupoMensajes(
        id="violet_q5c_g1",
        npc_id="violet",
        mensaje_inicial="No sé si lo estás haciendo a propósito o eres idiota",
        trigger_id="violet_q5c_g1",
        momento_locacion="casa_hviolet",
        momento_horario=2,
        pasos=[
            # Paso 0: Reacción inicial del jugador
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Qué pasó ahora?",
                        respuesta_npc="",
                        saltar_a_paso=1,
                    ),
                    OpcionRespuesta(
                        texto="No sé qué hice, así que idiota",
                        respuesta_npc="",
                        saltar_a_paso=1,
                    ),
                ]
            ),
            # Paso 1: Violet pregunta por la tienda
            PasoConversacion(
                mensaje_npc="¿Cuándo fuiste a la tienda no notaste nada raro?",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No, la verdad que no",
                        respuesta_npc="¿Cómo encontraste la tienda esa?",
                        saltar_a_paso=2,
                    ),
                    OpcionRespuesta(
                        texto="Sí, había una persona muy extraña, toda tapada",
                        respuesta_npc=["Me imagino por qué...", "¿Cómo encontraste la tienda esa?"],
                        saltar_a_paso=2,
                    ),
                ]
            ),
            # Paso 2: MC explica cómo encontró la tienda
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Estaba en la misma calle que el edificio donde vivía",
                        respuesta_npc=["Es una tienda de cosplays eróticos", "Por eso era tan ajustado el otro", "Y estos son peor"],
                        saltar_a_paso=3,
                    ),
                ]
            ),
            # Paso 3: MC afirma que no sabía
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No lo sabía",
                        respuesta_npc=["Te puedes ir olvidando de la Japicon", "No voy a usar nada de esto"],
                        saltar_a_paso=4,
                    ),
                ]
            ),
            # Paso 4: Primeras opciones de respuesta
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Sabes que no lo hice con mala intención",
                        respuesta_npc=["Ya tengo dudas de tus intenciones", "Todo lo que haces de casualidad es lo que un pervertido haría"],
                        saltar_a_paso=5,
                    ),
                    OpcionRespuesta(
                        texto="Podemos ir sin cosplay",
                        respuesta_npc="La verdad es que no sé si tengo ganas de ir contigo",
                        saltar_a_paso=5,
                    ),
                ]
            ),
            # Paso 5: Disculpa final
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Perdón Violet, realmente no fue mi intención",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_q5c_g1)

    # =========================================================================
    # QUEST 06_A — Libre Mercado avisa que las entradas estan disponibles
    # =========================================================================

    chat_libre_mercado_japicon_g1 = GrupoMensajes(
        id="japicon_tickets_g1",
        npc_id="libre_mercado",
        mensaje_inicial="La venta de entradas para la Japicon ya está disponible",
        trigger_id="japicon_tickets_g1",
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Tengo que comprar las entradas",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("libre_mercado", chat_libre_mercado_japicon_g1)

    # =========================================================================
    # QUEST 06_B — Violet invita al MC a su habitacion de noche
    # =========================================================================

    chat_violet_q6b_g1 = GrupoMensajes(
        id="violet_q6b_g1",
        npc_id="violet",
        mensaje_inicial="Pasate a la noche por mi habitación",
        trigger_id="violet_q6b_g1",
        momento_locacion="casa_hviolet",
        momento_horario=2,
        pasos=[
            PasoConversacion(
                mensaje_npc="Te quiero consultar algo",
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Ok",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_q6b_g1)

    # =========================================================================
    # QUEST 07_B — MC contacta a la Tienda Coxplay para el cambio del cosplay
    # =========================================================================

    chat_tienda_coxplay_q7b_g1 = GrupoMensajes(
        id="tienda_coxplay_q7b_g1",
        npc_id="tienda_coxplay",
        mensaje_inicial="",
        trigger_id="tienda_coxplay_q7b_g1",
        pasos=[
            # Paso 0: MC inicia contacto
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Hola, buen día, me comunico porque tuve un problema con una compra",
                        respuesta_npc=["Hola [mc_name], buen día", "Tengo dos compras con tu usuario: el traje de piloto 77 y el Coxplay Box", "¿Con cuál tuvo el problema?"],
                        saltar_a_paso=1,
                    ),
                    OpcionRespuesta(
                        texto="Hola, buenas tardes, me comunico porque tuve un problema con una compra",
                        respuesta_npc=["Hola [mc_name], buenas tardes", "Tengo dos compras con tu usuario: el traje de piloto 77 y el Coxplay Box", "¿Con cuál tuvo el problema?"],
                        saltar_a_paso=1,
                    ),
                ]
            ),
            # Paso 1: MC identifica el producto
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Con el traje de piloto 77",
                        respuesta_npc="",
                        saltar_a_paso=2,
                    ),
                ]
            ),
            # Paso 2: MC describe el problema
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="El cierre está fallado y se traba",
                        respuesta_npc=["Lo sentimos mucho", "Se puede acercar a la tienda o enviarlo y le haremos el cambio del mismo"],
                        saltar_a_paso=3,
                    ),
                ]
            ),
            # Paso 3: MC decide enviar el cosplay
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Lo envío entonces",
                        respuesta_npc="Una vez que lo recibamos hacemos las revisiones y le enviamos el cambio",
                        saltar_a_paso=4,
                    ),
                ]
            ),
            # Paso 4: Despedida
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Muchas gracias por todo",
                        respuesta_npc=["Muchas gracias a ti", "y nuevamente perdón por el inconveniente"],
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("tienda_coxplay", chat_tienda_coxplay_q7b_g1)

    # =========================================================================
    # QUEST 07_C — Violet le informa al MC sobre el envío del cosplay
    # =========================================================================

    chat_violet_q7c_g1 = GrupoMensajes(
        id="violet_q7c_g1",
        npc_id="violet",
        mensaje_inicial="Ya hablé con la tienda, voy a enviar el paquete para que lo vean",
        trigger_id="violet_q7c_g1",
        momento_horario=0,
        pasos=[
            # Paso 0: MC pregunta si hay algo más que hacer
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Hay algo más que hacer?",
                        respuesta_npc=["No, hay que esperar", "Esto va a tardar varios días"],
                        saltar_a_paso=1,
                    ),
                ]
            ),
            # Paso 1: MC pregunta cuántos dias
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Te dijeron cuántos?",
                        respuesta_npc=["No, pero van a ser varios días", "Aparte del envío tienen que esperar que entre nuevo stock"],
                        saltar_a_paso=2,
                    ),
                ]
            ),
            # Paso 2: MC espera que llegue para la Japicon
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Esperemos que esté listo para la Japicon",
                        respuesta_npc=["No lo sé", "Igual hablé con una amiga que va a ir y hace cosplay, me dijo que me podría prestar alguno por si no llega"],
                        saltar_a_paso=3,
                    ),
                ]
            ),
            # Paso 3: MC reconoce el plan B
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Qué bien, ya tienes un plan B",
                        respuesta_npc="Sí, en estos días voy a ir",
                        saltar_a_paso=4,
                    ),
                ]
            ),
            # Paso 4: MC ofrece ayudar a elegir cosplay
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Si quieres mándame fotos y te puedo ayudar a elegir",
                        respuesta_npc=["Jajajaja no", "Vas a tener que esperar al día del evento para verlo"],
                        saltar_a_paso=5,
                    ),
                ]
            ),
            # Paso 5: MC acepta
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Puedo con eso",
                        respuesta_npc="❤️",
                        saltar_a_paso=6,
                    ),
                ]
            ),
            # Paso 6: MC responde con corazon — fin de la quest
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="❤️",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_q7c_g1)

    # =========================================================================
    # QUEST 09_A — Notificación de Tienda Coxplay (paquete recibido)
    # =========================================================================

    chat_tienda_coxplay_q9a_g1 = GrupoMensajes(
        id="tienda_coxplay_q9a_g1",
        npc_id="tienda_coxplay",
        mensaje_inicial="Buen día [mc_name], recibimos el paquete. Cuando esté la revisión lista le avisamos.",
        trigger_id="tienda_coxplay_q9a_g1",
        momento_horario=0,
        pasos=[
            # Paso 0: MC responde
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Gracias",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("tienda_coxplay", chat_tienda_coxplay_q9a_g1)
