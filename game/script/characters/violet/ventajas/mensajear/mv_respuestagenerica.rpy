################################################################################
## Mensajear · Violet — RESPUESTA GENERICA
################################################################################
## La de descarte: prioridad 1 y sin condiciones, asi que es la que sale cuando
## ninguna especial cumple lo suyo. Cualquier conversacion nueva con prioridad
## mayor a 1 le gana automaticamente.
##
## ES LA UNICA REPETIBLE. Al terminar se devuelve a estado "pendiente" para que
## vuelva a estar disponible; el resto queda "completado" y no se repite.

init 6 python:

    def _mv_generica_al_completar():
        """
        Devuelve el grupo a "pendiente" para que se pueda repetir.

        Funcion de MODULO: queda guardada en el save via el grupo de mensajes.
        """
        _g = store.sistema_mensajes._grupos_registrados.get("violet_mv_generica")
        if _g is not None:
            _g.estado = "pendiente"

    # Sin momento_horario / momento_locacion / condicion_entrega: los grupos de
    # Mensajear no llevan condiciones de entrega (ver mensajear_violet.rpy).
    grupo_mv_generica = GrupoMensajes(
        id="violet_mv_generica",
        npc_id="violet",
        mensaje_inicial="Que raro que me estes escribiendo\n¿Necesitas algo?",
        trigger_id="violet_mv_generica",
        accion_al_completar=_mv_generica_al_completar,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No solo queria hablar un rato",
                        respuesta_npc=["Ahora estoy con otra cosa",
                                       "Hablamos despues"],
                        saltar_a_paso=1,
                    ),
                ]
            ),
            PasoConversacion(
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
    sistema_mensajes.registrar_grupo("violet", grupo_mv_generica)

    registrar_conversacion_mensajear(
        "generica", "violet_mv_generica",
        condicion=None,
        prioridad=1,
    )
