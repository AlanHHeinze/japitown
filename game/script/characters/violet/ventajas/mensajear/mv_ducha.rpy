################################################################################
## Mensajear · Violet — DUCHA
################################################################################
## Prioridad 5, con ella metida en el baño. No es repetible: al terminar queda
## en "completado".
##
## LA CONDICION ES LA LOCACION, no la rutina. Se pregunta si esta en un baño y
## no si tiene puesta la rutina especial `violet_ducha`, porque lo que importa
## es donde esta —una rutina de quest que la mande a bañarse tendria que servir
## igual—. RUTINA_LOCS_BANIO es el set del motor (npcsystem_core): asi vale
## para cualquier baño y no solo para el de arriba.
##
## Y a diferencia del resto de las conversaciones, acá NO se pide
## npc_interactuable: justamente esta ocupada y detras de una puerta. Ese es el
## chiste de la charla.
##
## ⚠️ LA FOTO ES PRESTADA, igual que en mv_intencion. Hoy apunta a la de la
## quest de deseo 20, que es la unica libre de compromisos de quest, pero el
## guion pide otra: acá ella dice "no estoy desnuda", o sea vestida y por
## entrar a la ducha. Cuando exista el arte se cambia SOLO _MV_DUCHA_FOTO.
##
## ⚠️ LOS GRUPOS DE MENSAJEAR NO LLEVAN CONDICIONES DE ENTREGA (momento_horario,
## momento_locacion, condicion_entrega). Un grupo con condiciones se va a
## "espera" y seleccionar_grupo() no lo encuentra. Las condiciones van en el
## registro de la conversacion.


init python:

    _MV_DUCHA_FOTO = "images/chat/violet/violet_chat_q20d.jpg"

    def _mv_ducha_condicion():
        """Violet metida en un baño."""
        return tracker_locacion_npc("violet") in RUTINA_LOCS_BANIO

    def _mv_ducha_vista():
        """Predicado del catalogo de contenido (el ojo del panel)."""
        return mensaje_completado("violet_mv_ducha")


init 6 python:

    grupo_mv_ducha = GrupoMensajes(
        id="violet_mv_ducha",
        npc_id="violet",
        mensaje_inicial="Me estoy por bañar",
        trigger_id="violet_mv_ducha",
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Se me acelero el corazon de solo imaginarlo",
                        respuesta_npc=["¿De imaginar que?", "😊"],
                        saltar_a_paso=1,
                    ),
                ]
            ),
            # La foto va con la primera burbuja de la respuesta, o sea con
            # "Para tu desgracia no estoy desnuda".
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Desnuda por entrar a la ducha",
                        respuesta_npc="Para tu desgracia no estoy desnuda",
                        foto_respuesta=_MV_DUCHA_FOTO,
                        saltar_a_paso=2,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No, pero me ayuda a imaginarlo mejor",
                        respuesta_npc=["Lo vas a tener que seguir imaginando", "😉"],
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_mv_ducha)

    registrar_conversacion_mensajear(
        "ducha", "violet_mv_ducha",
        condicion=_mv_ducha_condicion,
        prioridad=5,
        saludo="¿Estas para jugar algo?",
    )

    registrar_contenido_ventaja(
        "mensajear", "ducha", "violet",
        "Justo antes de la ducha",
        "Escribile de noche, mientras esté en el baño a punto de bañarse.",
        vista=_mv_ducha_vista,
        orden=20,
    )
