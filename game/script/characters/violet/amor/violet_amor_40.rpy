################################################################################
## Violet — Amor 40 · "La solicitud"
################################################################################
##     archivo   violet_amor_40.rpy
##     quest     violet_amor_08          (quests_amor_violet.rpy)
##     label     quest_violet_amor_08    (lo fija el motor: "quest_" + id)
##     esquema   docs/narrativa/mecanica_amor_40.md
##
## DE QUE VA: Violet va a la habitacion del MC a pedirle perdon por la noche del
## sotano, y en el medio le llega a EL la solicitud de Zowie. Ella la ve, se va
## sin terminar de decir lo que venia a decir, y lo que importa termina pasando
## por chat — que es donde ella dice lo que en persona no diria.
##
## LAS FASES (flag `va40_fase`):
##
##   0  esperando la noche en su habitacion  → trigger de game_loop (la visita)
##   1  ella se fue; hay que ir a su puerta  → override de la puerta de Violet
##   2  esta ocupada: hay que escribirle     → conversacion de Mensajear
##   3  el chat termino                      → trigger de salir del celular
##   4  terminada
##
## LAS FASES 1 Y 2 CORREN CON EL JUEGO "LIBRE PERO ACOTADO": una restriccion
## propia (duenio="violet_amor_40") deja el camino de su habitacion al pasillo y
## frena el reloj, para que la secuencia no se corte por dormir en el medio.
## NO bloquea el celular — en la fase 2 el celular ES la salida.
##
################################################################################
## LO QUE FALTA
################################################################################
##
## 1. TRADUCCION AL INGLES de la escena y del chat.
##
## 2. NOMBRE Y DESCRIPCION de la quest ("La solicitud" / "Una amiga de Violet me
##    agrego en XGram."), en quests_amor_violet.rpy: se ven en Pistas.
##
## 3. EL HITO. `violet_hito_amor_04` ya es real y otorga "puerta_ingreso_diurno",
##    la unica de las candidatas que funciona sin contenido nuevo. Las otras
##    (Hablar en serio, Su ritmo, Salidas, XGram) se PRESENTAN en el cierre y no
##    se registran: una ventaja en el panel sin escena detras promete algo que
##    no existe.
##
## 4. EL CHAT NO TIENE ELECCION y no deja ningun flag (el `va40_acuerdo` que
##    preveia el esquema se saco el 2026-09-28, por lo mismo que el de la 35: un
##    flag que nadie elige es deuda invisible). Si mas adelante se le suma una,
##    el lugar natural es "¿Celos?" — es donde el jugador se posiciona.
##
################################################################################


################################################################################
## Estado
################################################################################

# 0 esperando · 1 hay que ir a su puerta · 2 hay que escribirle · 3 chat hecho ·
# 4 terminada
default va40_fase = 0

# La solicitud de Zowie. No es una eleccion —siempre termina aceptada— pero se
# guarda porque la app XGram lee este flag para cambiar su texto
# (`xgra_texto_app`, mas abajo), y porque si algun dia se agrega la rama de
# rechazarla el dato ya esta en los saves viejos.
default va40_solicitud = None

# Locaciones del tramo acotado, una lista por fase.
#
# FASE 1 — hasta la puerta de Violet, CON su habitacion adentro. No es que lo
# deje pasar: al tocar una puerta el movimiento consulta la restriccion ANTES
# que la puerta (accion_hotspot_move), asi que sin su habitacion en la lista la
# puerta se cortaba con el mensaje de bloqueo y el override que corre la escena
# no llegaba nunca. Bug real del 2026-10-01: la quest se trababa ahi.
define VA40_CAMINO_PUERTA = ["casa_hmc", "casa_pasilloarriba", "casa_hviolet"]

# FASE 2 — ya le contesto desde adentro: su habitacion vuelve a quedar afuera.
# Sin el override puerta (es solo de la fase 1), la puerta seguiria su flujo
# normal y el MC podria entrar en vez de escribirle, que es la salida.
define VA40_CAMINO = ["casa_hmc", "casa_pasilloarriba"]


init python:

    # ── Estado de la quest ───────────────────────────────────────────────────

    def _va40_lista():
        """
        Viva y en la etapa del disparo.

        NO es `quest_lista_para_boton` por lo mismo que en la 35: ese predicado
        corre la capa 2 entera, y el motor ya chequea los conflictos por su
        cuenta antes de evaluar un trigger con `quest_id=`.
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_08")
        return (_q is not None and _q.activa and not _q.completada
                and _q.etapa_actual == ETAPA_BOTON_LISTO)

    def _va40_viva():
        """Activa y sin completar, sin pedir etapa. La usan la puerta y el cierre."""
        _q = store.sistema_quests.obtener_quest("violet_amor_08")
        return _q is not None and _q.activa and not _q.completada

    def _va40_fase(n):
        return _va40_viva() and getattr(store, "va40_fase", 0) == n

    # ── Textos de ETAPA_BOTON_LISTO (los usa quests_amor_violet.rpy) ─────────
    # Funciones de MODULO: quedan guardadas dentro del ConfigEtapa de la quest.

    _VA40_PISTAS = {
        0: "Podría pasar un rato en mi habitación esta noche.",
        1: "Violet se fue sin terminar de decirme lo que venía a decirme.",
        2: "Está encerrada mandando mensajes.",
        3: "Quedamos en algo.",
    }
    _VA40_QUEHACER = {
        0: "Estar en mi habitación por la noche",
        1: "Tocar la puerta de Violet",
        2: "Escribirle a Violet desde el celular",
        3: "Salir del celular",
    }

    def _pista_va40_listo():
        return renpy.translate_string(
            _VA40_PISTAS.get(getattr(store, "va40_fase", 0), _VA40_PISTAS[0]))

    def _quehacer_va40_listo():
        return renpy.translate_string(
            _VA40_QUEHACER.get(getattr(store, "va40_fase", 0), _VA40_QUEHACER[0]))

    # ── La app XGram ──────────────────────────────────────────────────────────

    def xgra_texto_app():
        """
        Lo que narra el boton de XGram. Lo llama hud_celular.rpy.

        La app no tiene pantalla propia, pero EXISTE en el mundo: despues de
        aceptar la solicitud, seguir diciendo "Contenido en desarrollo" le
        contradice al jugador algo que acaba de hacer.
        """
        # SIN traducir: `narrar_mensaje` hace el translate_string (hud_navigation).
        if getattr(store, "va40_solicitud", None) == "aceptada":
            return "Zowie subió tres fotos de esa noche. En ninguna salgo yo."
        return "Contenido en desarrollo"

    # ── Disparadores ─────────────────────────────────────────────────────────

    def _gl_va40_migrar_restriccion():
        """
        Saves del medio de la fase 1 grabados antes del arreglo del
        2026-10-01: tienen la restriccion vieja, SIN la habitacion de Violet,
        y la puerta se cortaba antes de llegar al override (la quest trabada).
        La vuelve a poner con el camino nuevo. Solo efectos python: nunca
        devuelve label.
        """
        if getattr(store, "va40_fase", 0) != 1:
            return None
        _r = getattr(store, "restriccion_quest_activa", None)
        if (_r is not None and _r.activa
                and getattr(_r, "duenio", None) == "violet_amor_40"
                and "casa_hviolet" not in (_r.locaciones_permitidas or [])):
            _va40_restringir(VA40_CAMINO_PUERTA, "Mejor voy a ver qué le pasa a Violet")
        return None

    def _gl_trigger_va40_visita():
        """
        Fase 0: el MC esta en su habitacion de noche y Violet va a hablarle.

        Ella tiene que estar disponible y en la casa. Eso va acá y no solo en
        las demandas porque `planificador_trigger_permitido` gatea por
        conflictos y a proposito NO mira la parte momentanea.
        """
        if not _va40_lista() or getattr(store, "va40_fase", 0) != 0:
            return None
        if getattr(store, "horario_actual", 0) != 2:
            return None
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_hmc":
            return None
        if not npc_disponible("violet") or npc_esta_oculto("violet"):
            return None
        # La escena entera pasa por el celular (la solicitud, los mensajes): si
        # otro contenido lo tiene tomado, esta espera en vez de pisarlo.
        if celular_esta_bloqueado():
            return None
        return "quest_violet_amor_08"

    def _va40_restringir(locaciones, mensaje):
        """
        La restriccion de la quest: el reloj congelado para que la secuencia
        no se corte durmiendo, y el mundo acotado a `locaciones`. El CELULAR NO
        se bloquea: en la fase 2 es la unica salida. Se vuelve a llamar al
        cambiar de fase; con el mismo dueño reemplaza a la anterior.
        """
        activar_restriccion(
            duenio="violet_amor_40",
            congelar_reloj=True,
            locaciones_permitidas=list(locaciones),
            acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                                 "usar_item", "comprar", "cocinar", "ver_tv"],
            mensaje_movimiento=mensaje,
            mensaje_accion_default=mensaje,
            npcs_interactuables=["violet"],
        )

    def _va40_puerta_ocupada():
        """
        Fase 1: la puerta de Violet reemplaza todo su flujo.

        Es un OVERRIDE y no un bloqueo de golpe porque acá PASA algo: ella
        contesta, el MC piensa y la quest avanza de fase. Un bloqueo solo
        mostraria un mensaje y dejaria la quest donde estaba.
        """
        return _va40_fase(1)

    def _va40_conversacion_lista():
        """
        Condicion de la conversacion de Mensajear. Con `forzada=True` es la
        UNICA puerta, asi que va estrecha: solo en la fase 2 de esta quest.
        """
        return _va40_fase(2)

    def _va40_chat_completado():
        """
        accion_al_completar del grupo. Funcion de MODULO: se guarda en el save
        junto con el grupo.

        No cierra la quest — eso pasa al salir del celular, que es donde se
        levanta la restriccion y entra el ultimo pensamiento.
        """
        store.va40_fase = 3

    def _va40_chat_visto():
        """Predicado del catalogo de contenido de "Mensajear" (el ojo del panel)."""
        return mensaje_completado("violet_amor40_chat")

    def _cel_trigger_va40_cierre():
        """Trigger de salir del celular: ya conversaron, ahora el cierre."""
        if _va40_fase(3):
            return "violet_amor_40_cierre"
        return None


init 5 python:

    # `duenio`: la quest pone su propia restriccion en la fase 1, asi que sus
    # triggers tienen que poder saltar adentro de ella.
    registrar_trigger_game_loop("violet_amor_40_visita", _gl_trigger_va40_visita,
                                duenio="violet_amor_40",
                                quest_id="violet_amor_08")

    registrar_trigger_game_loop("violet_amor_40_migrar_restriccion",
                                _gl_va40_migrar_restriccion,
                                duenio="violet_amor_40")

    registrar_trigger_salir_celular("violet_amor_40_cierre",
                                    _cel_trigger_va40_cierre,
                                    quest_id="violet_amor_08")

    registrar_override_puerta("violet", _va40_puerta_ocupada,
                              "violet_amor_40_puerta",
                              quest_id="violet_amor_08")


init 6 python:

    # ── El chat de la fase 2 ─────────────────────────────────────────────────
    # ESCRIBE EL MC, no ella. Es el gesto que la quest esta midiendo: ella se
    # encerro, y el jugador elige seguirla por el unico lado que queda abierto.
    # Por eso va por el sistema Mensajear y no como grupo entregado.
    #
    # ⚠️ LOS GRUPOS DE MENSAJEAR NO LLEVAN CONDICIONES DE ENTREGA
    # (momento_horario, momento_locacion, condicion_entrega): un grupo con
    # condiciones se va a "espera" y seleccionar_grupo() no lo encuentra. Las
    # condiciones viven en el registro de la conversacion.
    #
    # Es LINEAL: un solo camino, una opcion por paso. La conversacion ES la
    # escena central de la quest, no un menu de respuestas.
    #
    # Varias burbujas seguidas de ELLA van como LISTA en `respuesta_npc`: le
    # llegan una tras otra, cada una con su "escribiendo...".
    #
    # Varias seguidas del MC NO van como lista en `texto` (eso las manda todas
    # juntas con un solo click): van en pasos separados, uno por mensaje, con
    # `respuesta_npc=""` en todos menos el ultimo. Asi el jugador manda cada
    # una con su click, como si las escribiera.

    grupo_violet_amor40 = GrupoMensajes(
        id="violet_amor40_chat",
        npc_id="violet",
        mensaje_inicial="¿De qué?",
        trigger_id="violet_amor40_chat",
        accion_al_completar=_va40_chat_completado,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No sé, viniste a pedirme perdón por algo y te fuiste",
                        respuesta_npc="No te preocupes, cambié de opinión",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Respecto a pedirme perdón?",
                        respuesta_npc="Sí",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Igual no tenías que pedirme perdón por eso",
                        respuesta_npc="",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Era una noche de amigas y yo no tenía nada que hacer ahí",
                        respuesta_npc="Listo, asunto solucionado",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Pero sí por lo otro",
                        respuesta_npc="¿Por qué otro?",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Por la manera en que dijiste las cosas",
                        respuesta_npc="No dije nada de mala manera",
                    ),
                ]
            ),
            # EL PUNTO DE LA QUEST: el MC le pone nombre a lo que pasó.
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Sí, cuando tu amiga me invitó cambiaste la actitud, igual que ahora cuando me agregó",
                        respuesta_npc="",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Celos?",
                        respuesta_npc="¿De qué? No somos nada como para tener celos",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Eso lo decides tú",
                        respuesta_npc="¿Qué cosa decido yo?",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Qué relación tenemos",
                        respuesta_npc=["Ahhh",
                                       "Es algo muy difícil, no niego que están pasando cosas"],
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="¿Pero...?",
                        respuesta_npc="Pero vivimos juntos, hay más gente en la casa y es todo muy raro",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No le veo nada de raro",
                        respuesta_npc="Sé que estás buscando todo el tiempo un poco más, no es que no quiera, es que tengo otros tiempos",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Si te estás sintiendo presionada no es la intención",
                        respuesta_npc="Gracias por entenderme y perdón por lo otro",
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No hay problema",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_violet_amor40)

    # `forzada=True` prende el boton "Hablar" sin la ventaja Mensajear, sin
    # gastar el uso diario y sin pedir que Violet este en otra locacion. Es
    # imprescindible: si el boton no estuviera, la fase 2 no tendria salida.
    registrar_conversacion_mensajear(
        "amor40", "violet_amor40_chat",
        condicion=_va40_conversacion_lista,
        prioridad=100,                 # le gana a cualquier otra mientras dure
        saludo="Bueno, entonces por acá podemos hablar",
        forzada=True,
    )

    # Aparece en el ojo de "Mensajear" como una charla mas, igual que la de
    # deseo 20: para el jugador es una conversacion del chat como cualquiera.
    registrar_contenido_ventaja(
        "mensajear", "amor40", "violet",
        "La solicitud",
        "Es la quest de 40 ❤️. Después de que Violet se vaya de tu habitación, escríbele.",
        vista=_va40_chat_visto,
    )


################################################################################
## 1 · LA VISITA — ella golpea la puerta de su habitacion
################################################################################
## El MC ya esta en su cuarto (lo exige el trigger), asi que el fondo sale de la
## locacion actual.

label quest_violet_amor_08:

    $ ocultar_hud()
    window show

    $ _va40_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va40_bg

    # mc_izquierda y no center: el sprite base del MC mira a la izquierda, y
    # Violet entra por la derecha. En center le daba la espalda.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    vozoff "Toc toc"

    show mc_parado_base b_hablando
    mc "Adelante"
    show mc_parado_base b_none

    # Entra EN PIJAMA: ya estaba por acostarse, o sea que vino a proposito.
    show violet_parada c_pijama_base ca_pijama o_base b_none at right with sprite_normal

    show violet_parada b_hablando c_pijama_saludando with sprite_normal
    violet "Buenas"
    show violet_parada b_none c_pijama_base with sprite_normal

    show mc_parado_base b_hablando 
    mc "Hola"
    show mc_parado_base b_abiertachica c_rbase_pensando with sprite_normal
    mc "¿Qué pasó?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_pijama_brazoscruzados with sprite_normal
    violet "Te quería pedir perdón por lo del otro día"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Perdón por qué cosa?"
    show mc_parado_base b_none

    # ── LA SOLICITUD, justo en el medio de la disculpa ───────────────────────
    vozoff "Brrrr Brrrr"

    # Mira su celular y vuelve a lo suyo: el telefono que sonó no es el de ella,
    # y eso ya la pone en guardia.
    show violet_parada c_pijama_celu o_abajonm with sprite_normal
    pause 0.5
    show violet_parada c_pijama_base o_base with sprite_normal

    show violet_parada b_hablando
    violet "No fue mi teléfono, te llegó a ti"
    show violet_parada b_none

    show mc_parado_base c_rbase_celular o_abajonm with sprite_normal
    pause 0.5

    show mc_parado_base b_hablando o_base
    mc "Sí, fue el mío"
    show mc_parado_base b_abiertachica o_arribanm
    mc "Zowie era una de tus amigas que estuvo el otro día, ¿no?"
    show mc_parado_base b_none o_base

    show violet_parada b_hablando
    violet "Sí, ¿por?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Me llegó una solicitud de amistad de alguien en XGram y tenía dudas de si era ella"
    show mc_parado_base b_none

    $ va40_solicitud = "aceptada"

    show mc_parado_base b_hablando o_abajonm
    mc "Listo, ahí la acepté"
    show mc_parado_base b_abiertachica o_base c_rbase_avergonzado with sprite_normal
    mc "¿Qué me decías?"
    show mc_parado_base b_none

    vozoff "Brrrr Brrrr"

    show mc_parado_base b_hablando c_rbase_celular o_abajonm with sprite_normal
    mc "Perdón, me está escribiendo"
    show mc_parado_base b_none

    # ── Ella se va sin terminar ──────────────────────────────────────────────
    show violet_parada b_hablando o_arribanm
    violet "Bueno, te dejo, parece que estás ocupado con tu nueva amiga"
    show violet_parada b_none o_base

    hide violet_parada with dissolve

    show mc_parado_base c_rbase_pensando o_base b_none with sprite_normal
    piensa "¿Qué le pasa ahora? Se fue sin terminar de decir lo que venía a decirme"
    piensa "Mejor voy a ver qué le pasa"

    hide mc_parado_base with dissolve

    # LIBRE PERO ACOTADO: el camino a su puerta y nada mas (ver
    # VA40_CAMINO_PUERTA: su habitacion esta en la lista a proposito).
    $ _va40_restringir(VA40_CAMINO_PUERTA, "Mejor voy a ver qué le pasa a Violet")

    $ va40_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA PUERTA — está ocupada
################################################################################
## Override de la puerta de Violet: reemplaza el flujo entero (menu, niveles de
## acceso, todo). El MC toca y ella contesta de adentro, sin sprite.

label violet_amor_40_puerta:

    $ ocultar_hud()
    window show

    $ _va40_bg = sistema_locaciones.obtener_locacion("casa_pasilloarriba").background
    scene expression _va40_bg

    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    vozoff "Toc toc"

    violet "¿Qué pasa?"

    show mc_parado_base b_hablando
    mc "Quiero hablar"
    show mc_parado_base b_none

    # Contesta desde adentro: sin sprite, a proposito.
    violet "No puedo, estoy ocupada mandando mensajes"

    show mc_parado_base b_hablando
    mc "No seas chiquilina"
    show mc_parado_base b_none

    show mc_parado_base c_rbase_pensando b_seria o_arribanm with sprite_normal
    piensa "Se enojo... no me va a dejar entrar"
    piensa "Si está ocupada mandando mensajes, tendra que responder uno mas"

    hide mc_parado_base with dissolve

    # Le contesto desde adentro: ahora la salida es escribirle, y su
    # habitacion vuelve a quedar afuera.
    $ _va40_restringir(VA40_CAMINO, "Le voy a escribir a Violet")

    $ va40_fase = 2

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · EL CIERRE — al salir del celular
################################################################################
## El chat ya paso (accion_al_completar dejo la fase en 3). Acá se levanta la
## restriccion, entra el ultimo pensamiento y se completa la quest, que es lo
## que otorga el HITO de amor 40 y sus ventajas.

label violet_amor_40_cierre:

    # SIN ESCENA NI PENSAMIENTO, a proposito: el chat ya cerro todo lo que la
    # quest tenia para decir, y un "lo que quedo claro fue..." despues de que
    # ella lo dijera con todas las letras solo repetiria. El label es mecanico:
    # suelta el mundo y completa.
    $ desactivar_restriccion(duenio="violet_amor_40")

    $ va40_fase = 4
    $ completar_quest_actual("violet", quest_id="violet_amor_08")

    $ mostrar_hud()
    jump game_loop
