################################################################################
## Mensajear · Violet — INTENCION (dos partes)
################################################################################
## Prioridad 5 las dos, asi que cuando cumplen condiciones le ganan siempre a la
## generica. Ninguna es repetible: al terminar quedan en "completado".
##
## LA PARTE 2 SOLO EXISTE SI EL JUGADOR FUE POR LA RAMA A. En la parte 1 hay una
## bifurcacion:
##
##   rama a  "No, no era por eso"  →  ella corta seco, conversacion corta,
##                                    y SE ABRE la parte 2 (el arrepentimiento)
##   rama b  "No voy a mentirte"   →  sinceridad, foto y la charla larga.
##                                    Cierra el arco: no hay parte 2
##
## O sea que las dos ramas dan lo mismo, por caminos distintos: la b lo cobra en
## el momento y la a lo hace esperar a la siguiente charla. El que se hace el
## disimulado no pierde contenido, lo pospone.
##
## COMO SE SABE QUE RAMA TOMO: la opcion de la rama a lleva `puntos={"rama_a": 1}`
## y `accion_al_completar` los lee de puntos_acumulados. Es la unica via —
## OpcionRespuesta no tiene callback propio— y es la que ya usa el sistema de
## recompensas, asi que no agrega maquinaria.
##
## LA FOTO ES PROPIA de esta conversacion. Las dos partes mandan la misma
## imagen y sale de _MV_INTENCION_FOTO, que es de donde salen los dos usos.
## Hasta que existio ese arte apuntaba prestada a la de la quest de deseo 20.
##
## ⚠️ LOS GRUPOS DE MENSAJEAR NO LLEVAN CONDICIONES DE ENTREGA (momento_horario,
## momento_locacion, condicion_entrega). Un grupo con condiciones se va a
## "espera" y seleccionar_grupo() no lo encuentra. Las condiciones van en el
## registro de la conversacion.


# True si en la parte 1 se eligio la rama a. Habilita la parte 2.
default mv_intencion_parte2 = False


init python:

    # Una sola definicion para los dos usos: ver la nota de arriba.
    _MV_INTENCION_FOTO = "images/chat/violet/violet_chat_intencion.jpg"

    def _mv_intencion_condicion():
        """
        Violet en su habitacion y libre.

        La locacion ya descarta casi todo lo de "ocupada" (si se esta bañando
        esta en el baño, si salio esta afuera), pero igual se chequean las otras
        dos: una rutina de quest puede tenerla en su pieza metida en otra cosa,
        y npc_interactuable ademas corta el trasnoche, cuando duerme.
        """
        if tracker_locacion_npc("violet") != "casa_hviolet":
            return False

        _v_int = obtener_npc("violet")
        if _v_int is None or _v_int.obtener_rutina_especial_actual() is not None:
            return False

        return not npc_esta_oculto("violet") and npc_interactuable("violet")

    def _mv_intencion2_condicion():
        """La parte 2, ademas, pide haber ido por la rama a."""
        if not getattr(store, 'mv_intencion_parte2', False):
            return False
        return _mv_intencion_condicion()

    # Predicados del catalogo de contenido de la ventaja (el ojo del panel de
    # Desbloqueos). Van como funciones de modulo, igual que todo lo demas.
    def _mv_intencion_vista():
        return mensaje_completado("violet_mv_intencion")

    def _mv_intencion2_vista():
        return mensaje_completado("violet_mv_intencion2")

    def _mv_intencion2_desbloqueada():
        """La parte 2 no existe hasta que la 1 se juega por la rama a."""
        return getattr(store, 'mv_intencion_parte2', False)

    def _mv_intencion_al_completar():
        """
        Abre la parte 2 si se fue por la rama a.

        Funcion de MODULO: queda guardada en el save via el grupo de mensajes.
        """
        _g = store.sistema_mensajes._grupos_registrados.get("violet_mv_intencion")
        if _g is not None and _g.puntos_acumulados.get("rama_a", 0) > 0:
            store.mv_intencion_parte2 = True


init 6 python:

    # =========================================================================
    # PARTE 1 — "¿que estas buscando?"
    # =========================================================================
    # El saludo del jugador lo manda _mv_iniciar con el `saludo` del registro;
    # `mensaje_inicial` es la primera respuesta de ella.
    #
    # Varios mensajes seguidos del jugador van en UNA burbuja separados por \n:
    # la API manda un solo `texto` por opcion. Del lado del NPC si se pueden
    # varias burbujas, con respuesta_npc como lista.

    grupo_mv_intencion = GrupoMensajes(
        id="violet_mv_intencion",
        npc_id="violet",
        mensaje_inicial="Bien, ¿tú?",
        trigger_id="violet_mv_intencion",
        accion_al_completar=_mv_intencion_al_completar,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Algo aburrido\n¿Qué hacías?",
                        respuesta_npc="Mmmmm, ¿qué estás buscando?",
                        saltar_a_paso=1,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Nada, solo quería hablar",
                        respuesta_npc="Pensé que me escribías a ver si te mandaba una foto otra vez",
                        saltar_a_paso=2,
                    ),
                ]
            ),
            # Paso 2: LA BIFURCACION.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No, no era por eso, solo quería hablar",
                        respuesta_npc="Ok, entonces no te mando nada",
                        # Lo unico que distingue la rama al terminar. Sin esto
                        # no habria forma de saber cual se jugo.
                        puntos={"rama_a": 1},
                        saltar_a_paso=3,
                    ),
                    OpcionRespuesta(
                        texto="No voy a mentirte que estaba pensando en la foto antes de escribirte",
                        respuesta_npc="Lo sabía, es en lo único que piensas",
                        saltar_a_paso=4,
                    ),
                ]
            ),
            # Paso 3 — rama a: se corta acá. La parte 2 lo retoma.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Si quieres igual me puedes mandar algo",
                        respuesta_npc="Mmm no, no quiero",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
            # Paso 4 en adelante — rama b: la charla larga.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Está mal que piense todo el día en ti?",
                        respuesta_npc="Premio a la sinceridad",
                        foto_respuesta=_MV_INTENCION_FOTO,
                        saltar_a_paso=5,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Me encantas\nQuiero ir para allá y agarrar eso",
                        respuesta_npc=["Se mira y no se toca", "😈"],
                        saltar_a_paso=6,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No sé cuánto me voy a poder controlar",
                        respuesta_npc="Si no te podes controlar no te mando mas nada entonces",
                        saltar_a_paso=7,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Prometo portarme bien",
                        respuesta_npc=["Ese es el camino", "❤️"],
                        saltar_a_paso=8,
                    ),
                ]
            ),
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
    sistema_mensajes.registrar_grupo("violet", grupo_mv_intencion)

    registrar_conversacion_mensajear(
        "intencion", "violet_mv_intencion",
        condicion=_mv_intencion_condicion,
        prioridad=5,
        saludo="Hola ¿Como estas?",
    )

    registrar_contenido_ventaja(
        "mensajear", "intencion", "violet",
        "La intención",
        "Escríbele estando ella en su habitación y libre. Según cómo le contestes cuando pregunte qué buscas, la charla sigue o se corta.",
        vista=_mv_intencion_vista,
        orden=10,
    )


    # =========================================================================
    # PARTE 2 — el arrepentimiento (solo despues de la rama a)
    # =========================================================================
    # Mismo saludo que la conversacion de la quest de deseo 20 ("¿Como estas?")
    # a proposito: es el mismo MC escribiendo, y ademas comparten la entrada de
    # traduccion.

    grupo_mv_intencion2 = GrupoMensajes(
        id="violet_mv_intencion2",
        npc_id="violet",
        mensaje_inicial="Volviste",
        trigger_id="violet_mv_intencion2",
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Volvi?",
                        respuesta_npc="Me imagine que te ibas a quedar pensando en lo que te dije",
                        saltar_a_paso=1,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Si, la intencion verdadera no era solo hablar",
                        respuesta_npc="¿Y por que no lo dijiste?",
                        saltar_a_paso=2,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Me dio verguenza",
                        respuesta_npc="¿Desde cuando el de la verguenza sos vos?",
                        saltar_a_paso=3,
                    ),
                ]
            ),
            # La foto va con la primera burbuja de la respuesta, o sea con
            # "No y no te queda bien".
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No lo se\nNo es mi estilo",
                        respuesta_npc="No y no te queda bien",
                        foto_respuesta=_MV_INTENCION_FOTO,
                        saltar_a_paso=4,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Si seguimos con la sinceridad quiero ir a agarrarlo",
                        respuesta_npc="Todavia te falta para eso",
                        saltar_a_paso=5,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Que me falta?",
                        respuesta_npc=["De momento que sigas siendo sincero", "❤️"],
                        saltar_a_paso=6,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Lo voy a ser",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_mv_intencion2)

    registrar_conversacion_mensajear(
        "intencion2", "violet_mv_intencion2",
        condicion=_mv_intencion2_condicion,
        prioridad=5,
        saludo="¿Como estas?",
    )

    registrar_contenido_ventaja(
        "mensajear", "intencion2", "violet",
        "La intención · segunda parte",
        "Sale sola la próxima vez que le escribas, pero solo si en la charla anterior te hiciste el disimulado.",
        vista=_mv_intencion2_vista,
        desbloqueada=_mv_intencion2_desbloqueada,
        orden=11,
    )
