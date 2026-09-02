################################################################################
## Violet — Deseo 20 · "Pensando en Violet"
################################################################################
##     archivo   violet_deseo_20.rpy
##     quest     violet_deseo_04          (quests_deseo_violet.rpy)
##     grupo     violet_deseo04_chat      (acá abajo)
##
## LA QUEST PASA CASI ENTERA EN EL CELULAR. Tres tramos:
##
##   fase 0 → el MC entra de NOCHE a su habitacion y se acuerda de ella. Lo
##            dispara un trigger de game_loop (disparador UNICO de la quest;
##            por eso violet_deseo_04 esta en _VD_SIN_BOTON del menu de Violet).
##   fase 1 → no se puede mover ni hacer ninguna otra accion: la unica salida
##            es escribirle. El celular se abre y se cierra normal —afuera no
##            hay nada que hacer igual—; el boton del chat dice "Hablar", no
##            "Responder".
##   fase 2 → terminada la conversacion se destraba la salida; al cerrar el
##            celular entra el label de cierre y se completa la quest.
##
## POR QUE "Hablar" Y NO UN CHAT NORMAL: acá el que escribe primero es el MC.
## Eso es exactamente el sistema Mensajear (ventajas/mensajear/), asi que la
## conversacion se registra ahi en vez de entregarse como grupo pendiente.
##
## EL HUEVO Y LA GALLINA: la ventaja "mensajear" la otorga el hito de deseo 20,
## o sea ESTA quest — cuando se juega todavia no la tiene. Para eso la
## conversacion va registrada con `forzada=True`: prende el boton por su cuenta,
## sin ventaja, sin gastar el uso diario y sin pedir que Violet este en otra
## locacion. Es imprescindible, no una comodidad: con TODO lo demas bloqueado,
## un boton apagado dejaria la partida trabada.
##
## ⚠️ LOS GRUPOS DE MENSAJEAR NO LLEVAN CONDICIONES DE ENTREGA (momento_horario,
## momento_locacion, condicion_entrega). Un grupo con condiciones se va a
## "espera" y seleccionar_grupo() no lo encuentra. Las condiciones van en el
## registro de la conversacion, que es _vd20_conversacion_lista.


# Fase de la quest. Se guarda: la conversacion puede quedar a medias entre
# sesiones y al cargar hay que saber en que tramo estaba.
#   0 sin empezar · 1 escribiendole · 2 chat hecho, falta cerrar · 3 terminada
default vd20_fase = 0


init python:

    def _gl_trigger_violet_deseo_20():
        """
        Trigger de game_loop: el MC entra de noche a su habitacion.

        Las condiciones van de la mas barata a la mas cara. `vd20_fase == 0`
        es la que impide que la escena se repita: una vez arrancada, la quest
        no vuelve a pasar por acá.
        """
        if getattr(store, 'vd20_fase', 0) != 0:
            return None

        if not quest_lista_para_boton("violet_deseo_04"):
            return None

        if store.horario_actual != 2:          # Noche
            return None

        _loc_d20 = store.sistema_locaciones.locacion_actual
        if _loc_d20 is None or _loc_d20.id != "casa_hmc":
            return None

        return "violet_deseo_20_inicio"

    def _vd20_esperando_mensaje():
        """
        True mientras el jugador tiene que escribirle y no lo hizo.

        Es la condicion de los DOS bloqueos: el de acciones (no se puede hacer
        nada mas) y el de salida del celular (no se puede cerrar). Se apaga
        sola en fase 2, cuando la conversacion termina.
        """
        return getattr(store, 'vd20_fase', 0) == 1

    def _vd20_escena_en_curso():
        """
        Congela los triggers de game_loop mientras dura la secuencia. Sin esto,
        otra quest podria meter su escena entre el pensamiento y el chat, y el
        jugador quedaria con la restriccion puesta adentro de contenido ajeno.
        """
        return getattr(store, 'vd20_fase', 0) in (1, 2)

    def _vd20_conversacion_lista():
        """
        Condicion de la conversacion de Mensajear. Es la UNICA puerta —
        `forzada=True` se saltea todo lo demas—, asi que es estrecha a
        proposito: solo durante la fase 1 de esta quest.
        """
        return getattr(store, 'vd20_fase', 0) == 1

    def _vd20_chat_completado():
        """
        accion_al_completar del grupo: pasa a fase 2. NO cierra la quest — eso
        pasa recien cuando el jugador sale del celular y corre el label de
        cierre, que es donde esta el ultimo pensamiento.

        Funcion de MODULO (no lambda ni def anidada): se guarda en el save via
        el grupo de mensajes.
        """
        store.vd20_fase = 2

    def _vd20_chat_visto():
        """Predicado del catalogo de contenido de "Mensajear" (el ojo del panel)."""
        return mensaje_completado("violet_deseo04_chat")

    def _cel_trigger_violet_deseo_20():
        """
        Trigger de salir del celular: ya converso, ahora el cierre.
        """
        if getattr(store, 'vd20_fase', 0) == 2:
            return "violet_deseo_20_cierre"
        return None


init 5 python:

    registrar_trigger_game_loop("violet_deseo_20_inicio",
                                _gl_trigger_violet_deseo_20)

    registrar_trigger_salir_celular("violet_deseo_20_cierre",
                                    _cel_trigger_violet_deseo_20)

    # Los dos lados del encierro de la fase 1. El jugador SIEMPRE puede salir
    # por su cuenta —le escribe y listo—, que es la condicion para poder usar
    # un bloqueo tan amplio.
    #
    # El celular se puede CERRAR sin problema: al salir no hay nada que hacer
    # igual, asi que impedirlo era una traba de mas.
    registrar_bloqueo_global(_vd20_esperando_mensaje,
                             "Deberia escribirle a Violet")
    registrar_congelamiento_triggers(_vd20_escena_en_curso)


init 6 python:

    # =========================================================================
    # LA CONVERSACION
    # =========================================================================
    # Va en este archivo y no en chat_violet.rpy porque no es un chat reactivo
    # de quest sino una conversacion del sistema Mensajear (ver el encabezado).
    #
    # El saludo del jugador lo manda _mv_iniciar con el `saludo` del registro;
    # `mensaje_inicial` es la PRIMERA respuesta de ella, y va como LISTA porque
    # son dos burbujas seguidas ("En la cama" / "Aburrida").
    #
    # Varios mensajes seguidos —de cualquiera de los dos— van como LISTA:
    # `texto`, `respuesta_npc` y `mensaje_inicial` aceptan las tres formas (str,
    # lista o callable) y cada elemento sale como una burbuja propia.
    #
    # LA FOTO llega sola, sin texto: es el `foto_respuesta` de los pasos 3 y 4
    # con respuesta_npc="". Eso recien funciona desde el arreglo de
    # _finalizar_escribiendo (hud_mensajes) — antes una foto sin texto se perdia.
    #
    # ESTRUCTURA — dos ramas que se juntan justo en la foto:
    #
    #     paso 0 --> a "Es una propuesta?"        --> paso 1 --> paso 3 --+
    #            \-> b "Te puedo decir que hacer" --> paso 2 --> paso 4 --+
    #     paso 5 en adelante, lineal <----------------------------------+
    #
    # La rama a es la del MC que se hace el gracioso y despues se disculpa; la
    # b es la del que se planta. Cambian tres burbujas y confluyen: la foto
    # llega igual, pero el jugador eligio como se la gano.

    grupo_violet_deseo04 = GrupoMensajes(
        id="violet_deseo04_chat",
        npc_id="violet",
        mensaje_inicial=["En la cama", "Aburrida"],
        trigger_id="violet_deseo04_chat",
        accion_al_completar=_vd20_chat_completado,
        pasos=[
            # Paso 0: se abren las dos ramas.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Es una propuesta? jajaja",
                        respuesta_npc="Ultimamente todo para vos es una propuesta",
                        saltar_a_paso=1,
                    ),
                    OpcionRespuesta(
                        texto="Si queres te puedo decir que hacer",
                        respuesta_npc="Me imagino tu sugerencia",
                        saltar_a_paso=2,
                    ),
                ]
            ),
            # Paso 1 - rama a.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto=["Mala mia supongo", "Se me esta haciendo dificil"],
                        respuesta_npc="¿Que cosa se te esta haciendo dificil?",
                        saltar_a_paso=3,
                    ),
                ]
            ),
            # Paso 2 - rama b.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="A ver",
                        respuesta_npc="¿Que clase de peticion es esa?",
                        saltar_a_paso=4,
                    ),
                ]
            ),
            # Pasos 3 y 4: cada rama cierra con lo suyo y ella manda la foto.
            # Las dos siguen en el paso 5.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Ver eso dando vueltas todo el dia por la casa",
                        respuesta_npc="",
                        foto_respuesta="images/chat/violet/violet_chat_q20d.jpg",
                        saltar_a_paso=5,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Una muy comun supongo",
                        respuesta_npc="",
                        foto_respuesta="images/chat/violet/violet_chat_q20d.jpg",
                        saltar_a_paso=5,
                    ),
                ]
            ),
            # Paso 5 en adelante: tronco unico.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No me lo esperaba 😲",
                        respuesta_npc="¿Que cosa?",
                        saltar_a_paso=6,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Una foto de mi cosa favorita",
                        respuesta_npc="¿Ahora soy tu cosa favorita?",
                        saltar_a_paso=7,
                    ),
                ]
            ),
            # Paso 7: LA CONFESION. Ella lee mal a proposito —o no— y el la
            # corrige en serio antes de volver al chiste. Es el unico momento
            # del chat en que ninguno de los dos se esconde, y es de donde sale
            # el nombre del hito de esta quest ("Confesión").
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto=["Siempre fuiste mi cosa favorita", "Pero no hablaba de eso ahora"],
                        respuesta_npc=["😊", "¿Y de que hablabas?"],
                        saltar_a_paso=8,
                    ),
                ]
            ),
            # Las dos pistas. Ella contesta lo mismo las dos veces a proposito:
            # el chiste es que se hace la desentendida.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto=["De mi otra cosa favorita", "Lo tenes atras"],
                        respuesta_npc="¿Los slimes?",
                        saltar_a_paso=9,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto=["Pista dos", "Es algo redondo que dan ganas de morder"],
                        respuesta_npc="¿Los slimes?",
                        saltar_a_paso=10,
                    ),
                ]
            ),
            # Y aca se cobra lo de la cocina: el premio que prometio en la quest
            # de deseo 10 y quedo sin pagar ("Nunca dije que iba a ser ahora").
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Jajaja no te hagas",
                        respuesta_npc="Bueno, con esto ya no te debo nada",
                        saltar_a_paso=11,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No recuerdo que me debias",
                        respuesta_npc="El premio de la cocina",
                        saltar_a_paso=12,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Nunca pense que ibas a cumplir, estabas dormida y lo hacias para molestarme",
                        respuesta_npc="Si a ambas cosas, pero siempre cumplo",
                        saltar_a_paso=13,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Entonces voy a tener que hacerte prometer mas cosas",
                        respuesta_npc=["Depende solo de vos lograr eso",
                                       "😉",
                                       "Ahi se conectaron mis amigos para la partida"],
                        saltar_a_paso=14,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Hablamos despues",
                        respuesta_npc="Hablamos despues 👋",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_violet_deseo04)

    registrar_conversacion_mensajear(
        "deseo20", "violet_deseo04_chat",
        condicion=_vd20_conversacion_lista,
        prioridad=100,                 # le gana a cualquier otra mientras dure
        saludo="¿Como estas?",
        forzada=True,
    )

    # Aparece en el ojo de "Mensajear" como una charla mas, aunque sea de quest:
    # para el jugador es una conversacion del chat como cualquier otra.
    registrar_contenido_ventaja(
        "mensajear", "deseo20", "violet",
        "Pensando en Violet",
        "Es la quest de 20 💋. Entrá de noche a tu habitación y escribile desde el celular.",
        vista=_vd20_chat_visto,
        orden=1,
    )


################################################################################
## FASE 0 → 1 · El MC se acuerda de ella
################################################################################

label violet_deseo_20_inicio:

    $ ocultar_hud()
    window show

    # Su habitacion de noche: el trigger solo salta ahi y a esa hora, asi que
    # la locacion actual ya es la correcta.
    $ _vd20_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd20_bg

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    piensa "Hace un rato que no veo a Violet ¿Que estara haciendo?"
    piensa "Podria enviarle un mensaje"

    hide mc_parado_base with dissolve

    # El encierro. El movimiento lo corta la restriccion; las acciones y la
    # salida del celular, los bloqueos registrados en init 5 (que leen la fase).
    $ vd20_fase = 1
    $ activar_restriccion(
        locaciones_permitidas=["casa_hmc"],
        mensaje_movimiento="Deberia escribirle a Violet",
        mensaje_npc_bloqueado="Deberia escribirle a Violet",
        celular_bloqueado=False,
    )

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## FASE 2 → 3 · Cierre, al salir del celular
################################################################################

label violet_deseo_20_cierre:

    $ ocultar_hud()
    window show

    $ _vd20_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd20_bg

    # (Mc cuerpo celular ojos base boca neutral)
    show mc_parado_base c_rbase_celular o_base b_none at center with sprite_normal

    piensa "No me dijo que no"
    piensa "Con Violet eso es mucho mas que un tal vez"

    hide mc_parado_base with dissolve

    $ vd20_fase = 3
    $ desactivar_restriccion()
    $ completar_quest_actual("violet", quest_id="violet_deseo_04")

    window hide
    $ mostrar_hud()
    jump game_loop
