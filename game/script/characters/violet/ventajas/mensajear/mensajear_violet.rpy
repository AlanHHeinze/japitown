################################################################################
## Violet — VENTAJA "Mensajear" · el controlador
################################################################################
## Ventaja del hito de deseo 20. Habilita el boton "Hablar" en su chat: el
## jugador le escribe "¿Todo bien?" cuando quiere y el sistema elige que
## conversacion se arma.
##
## COMO AGREGAR UNA CONVERSACION: crear su `mv_<nombre>.rpy` en esta carpeta con
## su GrupoMensajes y llamar a registrar_conversacion_mensajear() desde su
## init 6. ESTE ARCHIVO NO SE TOCA.
##
##     characters/violet/ventajas/mensajear/
##     ├── mensajear_violet.rpy       ← esto
##     ├── mv_respuestagenerica.rpy   ← la de descarte
##     └── mv_aburrida.rpy            ← la primera especial
##
## Hay una conversacion registrada FUERA de esta carpeta: la de la quest de
## deseo 20 (deseo/violet_deseo_20.rpy), que se queda con su quest porque es la
## quest entera. Va con `forzada=True` — ver el parametro mas abajo.
##
## ⚠️ LOS GRUPOS DE ESTE SISTEMA NO LLEVAN CONDICIONES DE ENTREGA
## (momento_horario, momento_locacion, condicion_entrega). Un grupo con
## condiciones se va a "espera" en vez de a pendientes y seleccionar_grupo() no
## lo encuentra. Las condiciones van en el REGISTRO de acá, que es quien decide
## cual se arma.
##
## MIENTRAS HAY UNA CONVERSACION ABIERTA se bloquea todo el juego (ver el final
## del archivo): no tendria sentido que el MC le escriba y se vaya a entrenar.
##
## El bloqueo NO deja trabado al jugador: abrir el celular pasa por
## celular_esta_bloqueado(), que solo mira la restriccion de quest activa y no
## el embudo de acciones. O sea que siempre puede entrar al chat y contestar,
## que es lo unico que levanta el bloqueo.


# Ultimo dia (dias_totales) en que se le escribio a cada NPC. Se compara contra
# dias_totales, que es el contador absoluto, asi que no hay nada que resetear al
# dormir.
default mensajear_usado_dia = {}


init python:

    # Lo que manda el jugador para abrir la charla. Uno solo y siempre el mismo:
    # el color lo pone la respuesta de ella, no el saludo.
    MENSAJEAR_SALUDO_VIOLET = "¿Todo bien?"

    # Indices de cada campo del registro, para no leer _reg[5] a ciegas.
    MV_PRIO, MV_ORDEN, MV_CONVID, MV_GRUPO, MV_COND, MV_SALUDO, MV_FORZADA = range(7)

    # [(prioridad, orden, conv_id, grupo_id, fn_condicion, saludo, forzada)]
    MENSAJEAR_VIOLET = []

    def registrar_conversacion_mensajear(conv_id, grupo_id, condicion=None,
                                         prioridad=1, saludo=None,
                                         forzada=False):
        """
        Registra una conversacion que Violet puede tener si el jugador le
        escribe.

        Args:
            conv_id: id unico de la conversacion (para debug/lectura)
            grupo_id: id del GrupoMensajes que se va a armar
            condicion: funcion de MODULO sin argumentos → bool. None = siempre.
                Acá van horario, locacion, mood, lo que sea.
            prioridad: mayor gana. Si empatan varias, se sortea entre ellas.
            saludo: con que abre el jugador. None = MENSAJEAR_SALUDO_VIOLET.
                Para el contenido que necesita que escriba otra cosa.
            forzada: True = esta conversacion PRENDE el boton "Hablar" por su
                cuenta, sin la ventaja, sin gastar el uso diario y sin exigir
                que Violet este en otra locacion de la casa. Es para el
                contenido que mete al jugador adentro del celular a escribirle
                — ahi el boton TIENE que estar, o queda trabado. Con forzada la
                `condicion` es la unica puerta: que sea lo bastante estrecha.
        """
        MENSAJEAR_VIOLET.append((prioridad, len(MENSAJEAR_VIOLET),
                                 conv_id, grupo_id, condicion, saludo, forzada))

    def _mv_grupo_disponible(grupo_id):
        """
        True si ese grupo todavia se puede armar.

        Un grupo ya jugado queda en estado "completado" y disparar_por_trigger
        lo ignora — es el mismo mecanismo que impide que se repitan los chats de
        quest. Las conversaciones repetibles se devuelven a "pendiente" solas al
        terminar (ver mv_respuestagenerica).

        OJO: _grupos_registrados esta indexado por `trigger_id`, NO por `id`.
        En los grupos de este sistema los dos son iguales a proposito, asi que
        el mismo string sirve acá y en seleccionar_grupo (que si busca por `id`).
        """
        _g = store.sistema_mensajes._grupos_registrados.get(grupo_id)
        return _g is not None and _g.estado == "pendiente"

    def _mv_elegir():
        """
        Elige que conversacion se arma, o None si no hay ninguna. Devuelve el
        REGISTRO entero (no el grupo_id): quien la use necesita tambien el
        saludo y el flag de forzada.

        Filtra por condicion y por disponible, se queda con las de PRIORIDAD MAS
        ALTA, y entre esas sortea. Una condicion que revienta descarta esa
        conversacion en vez de cortar la eleccion.
        """
        _candidatas = []
        _mejor = None
        for _reg in MENSAJEAR_VIOLET:
            if not _mv_grupo_disponible(_reg[MV_GRUPO]):
                continue
            _cond = _reg[MV_COND]
            if _cond is not None:
                try:
                    if not _cond():
                        continue
                except Exception:
                    continue
            _prio = _reg[MV_PRIO]
            if _mejor is None or _prio > _mejor:
                _mejor = _prio
                _candidatas = [_reg]
            elif _prio == _mejor:
                _candidatas.append(_reg)

        if not _candidatas:
            return None
        return renpy.random.choice(_candidatas)

    def _mv_ids_registrados():
        return set(_c[MV_GRUPO] for _c in MENSAJEAR_VIOLET)

    def _mv_hay_conversacion_abierta():
        """
        True si hay una conversacion DE ESTE SISTEMA sin terminar.

        Se deriva del estado del chat en vez de llevar un flag propio: asi no
        puede quedar desincronizado si una conversacion se cierra por otro lado.
        """
        _chat = store.sistema_mensajes.chats.get("violet")
        if not _chat:
            return False
        _ids = _mv_ids_registrados()
        if _chat.grupo_activo is not None and _chat.grupo_activo.id in _ids:
            return True
        for _g in _chat.grupos_pendientes:
            if _g.id in _ids:
                return True
        return False

    def _mv_puede_hablar():
        """
        ¿Se le puede escribir AHORA? Lo consulta el boton del celular.

        No chequea si hay otra conversacion abierta: de eso se encarga la UI,
        que le da precedencia al boton de Responder.
        """
        # Que haya algo que contestar. Va PRIMERO porque una conversacion
        # forzada se saltea todo lo demas: es contenido que necesita el boton
        # prendido si o si (el jugador puede estar encerrado en el celular).
        _reg = _mv_elegir()
        if _reg is None:
            return False
        if _reg[MV_FORZADA]:
            return True

        if not npc_tiene_ventaja("violet", "mensajear"):
            return False

        # Una vez por dia.
        if store.mensajear_usado_dia.get("violet") == getattr(store, 'dias_totales', 0):
            return False

        # Tiene que estar en casa y en OTRA locacion: escribirle estando al lado
        # no tiene sentido. tracker_locacion_npc devuelve None si esta afuera o
        # si una restriccion la escondio, asi que cubre las dos cosas.
        _loc_v = tracker_locacion_npc("violet")
        if _loc_v is None:
            return False
        _loc_mc = store.sistema_locaciones.locacion_actual
        if _loc_mc is None or _loc_mc.id == _loc_v:
            return False

        return True

    def _mv_iniciar():
        """
        Arranca la conversacion: mete el mensaje del jugador, arma el grupo
        elegido y lo deja activo para que pueda responder.
        """
        _reg = _mv_elegir()
        if _reg is None:
            return
        _gid = _reg[MV_GRUPO]

        store.sistema_mensajes.inicializar_chat("violet")
        store.sistema_mensajes.chats["violet"].agregar_mensaje(
            "jugador",
            renpy.translate_string(_reg[MV_SALUDO] or MENSAJEAR_SALUDO_VIOLET))

        store.sistema_mensajes.disparar_por_trigger("manual", _gid, "violet")
        store.sistema_mensajes.seleccionar_grupo("violet", _gid)

        # El uso se gasta al ESCRIBIR, no segun lo que ella conteste: la generica
        # tambien lo consume. Una forzada NO lo gasta: no es el jugador el que
        # decidio escribirle, y ademas puede no tener todavia la ventaja.
        if not _reg[MV_FORZADA]:
            store.mensajear_usado_dia["violet"] = getattr(store, 'dias_totales', 0)


init 5 python:

    registrar_mensajear("violet", _mv_puede_hablar, _mv_iniciar)

    # Mientras no le conteste, no se hace nada mas. Son los dos lados del
    # bloqueo: el embudo corta las ACCIONES (dormir, avanzar, entrenar, cocinar,
    # hablar...) y el congelamiento corta los TRIGGERS de game_loop, que es por
    # donde entran los inicios de quest y las escenas automaticas.
    registrar_bloqueo_global(_mv_hay_conversacion_abierta,
                             "Debo responderle primero a Violet")
    registrar_congelamiento_triggers(_mv_hay_conversacion_abierta)
