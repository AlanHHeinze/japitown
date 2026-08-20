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

    # [(prioridad, orden, conv_id, grupo_id, fn_condicion)]
    MENSAJEAR_VIOLET = []

    def registrar_conversacion_mensajear(conv_id, grupo_id, condicion=None,
                                         prioridad=1):
        """
        Registra una conversacion que Violet puede tener si el jugador le
        escribe.

        Args:
            conv_id: id unico de la conversacion (para debug/lectura)
            grupo_id: id del GrupoMensajes que se va a armar
            condicion: funcion de MODULO sin argumentos → bool. None = siempre.
                Acá van horario, locacion, mood, lo que sea.
            prioridad: mayor gana. Si empatan varias, se sortea entre ellas.
        """
        MENSAJEAR_VIOLET.append((prioridad, len(MENSAJEAR_VIOLET),
                                 conv_id, grupo_id, condicion))

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
        Elige que conversacion se arma, o None si no hay ninguna.

        Filtra por condicion y por disponible, se queda con las de PRIORIDAD MAS
        ALTA, y entre esas sortea. Una condicion que revienta descarta esa
        conversacion en vez de cortar la eleccion.
        """
        _candidatas = []
        _mejor = None
        for _prio, _reg, _cid, _gid, _cond in MENSAJEAR_VIOLET:
            if not _mv_grupo_disponible(_gid):
                continue
            if _cond is not None:
                try:
                    if not _cond():
                        continue
                except Exception:
                    continue
            if _mejor is None or _prio > _mejor:
                _mejor = _prio
                _candidatas = [_gid]
            elif _prio == _mejor:
                _candidatas.append(_gid)

        if not _candidatas:
            return None
        return renpy.random.choice(_candidatas)

    def _mv_ids_registrados():
        return set(_c[3] for _c in MENSAJEAR_VIOLET)

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

        # Y que haya algo que contestar. Con la generica registrada siempre lo
        # hay, pero el chequeo evita que el boton dispare en falso si alguna vez
        # todas quedan sin cumplir condiciones.
        return _mv_elegir() is not None

    def _mv_iniciar():
        """
        Arranca la conversacion: mete el mensaje del jugador, arma el grupo
        elegido y lo deja activo para que pueda responder.
        """
        _gid = _mv_elegir()
        if _gid is None:
            return

        store.sistema_mensajes.inicializar_chat("violet")
        store.sistema_mensajes.chats["violet"].agregar_mensaje(
            "jugador", renpy.translate_string(MENSAJEAR_SALUDO_VIOLET))

        store.sistema_mensajes.disparar_por_trigger("manual", _gid, "violet")
        store.sistema_mensajes.seleccionar_grupo("violet", _gid)

        # El uso se gasta al ESCRIBIR, no segun lo que ella conteste: la generica
        # tambien lo consume.
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
