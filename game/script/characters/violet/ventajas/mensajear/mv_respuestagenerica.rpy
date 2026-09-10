################################################################################
## Mensajear · Violet — RESPUESTA GENERICA
################################################################################
## La de descarte: prioridad 1 y sin condiciones, asi que es la que sale cuando
## ninguna especial cumple lo suyo. Cualquier conversacion nueva con prioridad
## mayor a 1 le gana automaticamente.
##
## ES LA UNICA REPETIBLE. Al terminar se devuelve a estado "pendiente" para que
## vuelva a estar disponible; el resto queda "completado" y no se repite.
##
## DE TRASNOCHE NO CONTESTA: a esa hora esta durmiendo. Al ser la unica sin
## condicion, era la que mantenia el boton "Hablar" prendido toda la madrugada.

init 6 python:

    def _mv_generica_condicion():
        """
        Condicion de la conversacion: cualquier hora MENOS el trasnoche.

        Va acá y no en _mv_puede_hablar() porque es una regla de ESTA
        conversacion, no del sistema: una conversacion de quest puede necesitar
        que conteste de madrugada, y esas ya declaran su propia condicion.

        Al quedarse sin la de descarte, si a esa hora ninguna otra cumple lo
        suyo, _mv_elegir() no devuelve nada y el boton "Hablar" queda apagado —
        que es lo correcto: mejor no poder escribirle que escribirle y que no
        conteste.
        """
        return store.horario_actual != HORARIO_TRASNOCHE

    def _mv_generica_al_completar():
        """
        Devuelve el grupo a "pendiente" para que se pueda repetir.

        Funcion de MODULO: queda guardada en el save via el grupo de mensajes.

        ⚠️ SIEMPRE resetear(), NUNCA tocar los campos a mano. Aca antes se
        bajaban `estado` y `_disparado` uno por uno y quedaba `paso_actual`
        en el final: la segunda vez que salia, la conversacion arrancaba ya
        terminada, sin opciones, y como Mensajear bloquea todas las acciones
        mientras hay una charla abierta, la partida quedaba trabada. Dos
        jugadores lo reportaron en la 0.1.9. resetear() es el unico que sabe
        cuales son TODOS los campos que hay que volver a cero.
        """
        _g = store.sistema_mensajes._grupos_registrados.get("violet_mv_generica")
        if _g is not None:
            _g.resetear()

    # Sin momento_horario / momento_locacion / condicion_entrega: los grupos de
    # Mensajear no llevan condiciones de entrega (ver mensajear_violet.rpy).
    grupo_mv_generica = GrupoMensajes(
        id="violet_mv_generica",
        npc_id="violet",
        mensaje_inicial="Qué raro que me estés escribiendo\n¿Necesitas algo?",
        trigger_id="violet_mv_generica",
        accion_al_completar=_mv_generica_al_completar,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No, solo quería hablar un rato",
                        respuesta_npc=["Ahora estoy con otra cosa",
                                       "Hablamos después"],
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
        condicion=_mv_generica_condicion,
        prioridad=1,
    )
