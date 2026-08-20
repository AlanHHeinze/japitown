################################################################################
## Mensajear · Violet — ABURRIDA
################################################################################
## Prioridad 5, de NOCHE y con ella en su habitacion. Al tener mas prioridad que
## la generica, cuando se dan las dos condiciones esta le gana siempre.
##
## No es repetible: al terminar queda en "completado" y no vuelve a salir.
##
## ⚠️ FALTA LA FOTO. En el guion Violet manda una imagen antes de "Ahi me
## hablaron"; el arte todavia no existe, asi que por ahora la linea va como
## texto. Cuando llegue, se agrega `foto_respuesta="images/chat/violet/<archivo>"`
## a esa OpcionRespuesta — el sistema la muestra en la burbuja y la suma a la
## galeria del celular.

init 6 python:

    def _mv_aburrida_condicion():
        """De noche y con Violet en su habitacion."""
        if getattr(store, 'horario_actual', 0) != 2:
            return False
        return tracker_locacion_npc("violet") == "casa_hviolet"

    grupo_mv_aburrida = GrupoMensajes(
        id="violet_mv_aburrida",
        npc_id="violet",
        mensaje_inicial="Aburrida\n¿Vos?",
        trigger_id="violet_mv_aburrida",
        tabla_recompensas=TablaRecompensas({
            "deseo": [
                RangoRecompensa(1, 99, {"tipo": "deseo", "valor": 1}),
            ],
        }),
        pasos=[
            # Los dos mensajes seguidos del jugador van en una sola burbuja
            # separados por \n: la API manda un solo `texto` por opcion (varias
            # burbujas seguidas solo se pueden del lado del NPC, con
            # respuesta_npc como lista).
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Si yo tambien\nPero no tengo ganas de hacer nada, asi que me merezco el aburrimiento",
                        respuesta_npc=["Jajaja", "Si suele pasar"],
                        saltar_a_paso=1,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Y vos por que no estas haciendo nada?",
                        respuesta_npc=["Estoy esperando a que se conecten unas amigas para jugar",
                                       "Envia una foto"],
                        saltar_a_paso=2,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="🔥\nEstas linda",
                        respuesta_npc=["😊",
                                       "Ahi me hablaron de que ya estan conectadas",
                                       "Hablamos despues"],
                        puntos={"deseo": 5},
                        saltar_a_paso=3,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Hablamos despues",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_mv_aburrida)

    registrar_conversacion_mensajear(
        "aburrida", "violet_mv_aburrida",
        condicion=_mv_aburrida_condicion,
        prioridad=5,
    )
