################################################################################
## Triggers de contenido en puntos del motor (refactors C5 y C6)
################################################################################
## El motor tiene tres "puntos de enganche" donde el contenido puede intervenir:
##   - game_loop (cada vuelta del loop, antes del pause)
##   - accion_dormir (fase "antes" de dormir() y fase "despues" del autosave)
##   - accion_avanzar_tiempo (despues de avanzar el horario)
##
## El contenido se registra desde SUS archivos en init 5 con funciones de
## MODULO. Cada funcion chequea su propia condicion y devuelve:
##   - un label (str)  -> el motor hace jump a ese label (y corta: primer
##                        trigger que devuelve label gana, igual que los jumps
##                        encadenados que reemplaza este sistema)
##   - None            -> no aplica, o ya hizo sus efectos python y el flujo
##                        continua normal
##
## La PRIORIDAD ordena la evaluacion (mayor primero) y es deterministica:
## no depende del orden alfabetico de archivos. Los ids se usan ademas como
## tag `gl_trigger` de Sentry (instrumentacion del bug S11).
##
## El motor NO conoce ninguna quest por nombre: solo itera estos registros.

init python:

    TRIGGERS_GAME_LOOP = []       # [(prioridad, orden, id, funcion)]
    TRIGGERS_DORMIR_ANTES = []    # idem — corren ANTES de dormir()
    TRIGGERS_DORMIR_DESPUES = []  # idem — corren DESPUES del autosave
    TRIGGERS_AVANZAR = []         # idem — corren tras avanzar el horario
    TRIGGERS_SALIR_CELULAR = []   # idem — corren al cerrar el celular

    # Condiciones que CONGELAN los triggers de game_loop mientras dan True. Sirve
    # para cortar de raiz los inicios de quest y las escenas automaticas cuando
    # el juego esta esperando algo del jugador — por ejemplo una conversacion de
    # chat sin contestar.
    #
    # Congela TODOS los triggers, no solo los inicios: una transicion de fase a
    # mitad de camino tambien es una escena que interrumpe. Solo registrar
    # condiciones de las que el jugador pueda salir por su cuenta.
    CONGELAMIENTOS_TRIGGER = []   # [condicion]

    def registrar_congelamiento_triggers(condicion):
        """
        Registra una condicion que congela los triggers de game_loop.
        `condicion` es funcion de MODULO sin argumentos (regla anti-pickle).
        """
        CONGELAMIENTOS_TRIGGER.append(condicion)

    def _registrar_trigger(registro, trigger_id, funcion, prioridad):
        registro.append((prioridad, len(registro), trigger_id, funcion))

    # trigger_id -> duenio. Ver registrar_trigger_game_loop.
    TRIGGER_DUENIO = {}
    # trigger_id -> quest_id. Ver registrar_trigger_game_loop.
    TRIGGER_QUEST = {}

    def registrar_trigger_game_loop(trigger_id, funcion, prioridad=0, duenio=None,
                                    quest_id=None):
        """
        Registra un trigger evaluado en cada vuelta del game_loop.

        `quest_id`: la quest que este trigger DISPARA. Cuando devuelve label,
        el motor pasa por activar_quest(quest_id) antes de saltar — es el
        punto de activacion (questsystem_core). Un trigger que solo hace
        efectos python, o que salta a una escena que no es de quest, no lo
        declara.

        `duenio` es el id del contenido (el mismo que usa en activar_restriccion,
        si tiene una). MIENTRAS HAYA UNA RESTRICCION CON DUEÑO ACTIVA, SOLO
        SALTAN LOS TRIGGERS DE ESE DUEÑO: los demas se evaluan igual (pueden
        tener efectos python) pero el label que devuelvan se ignora.

        Por que: una restriccion es una secuencia en curso — el jugador esta
        adentro de una quest que le acoto el mundo. Que otra quest meta su
        escena en el medio rompe las dos (paso con la 04_b de Violet pisando
        la cadena de evento03). Un trigger sin duenio cuenta como ajeno: si
        tiene que poder saltar adentro de su propia restriccion, declara el
        duenio.
        """
        _registrar_trigger(TRIGGERS_GAME_LOOP, trigger_id, funcion, prioridad)
        TRIGGER_DUENIO[trigger_id] = duenio
        TRIGGER_QUEST[trigger_id] = quest_id

    def registrar_trigger_dormir(trigger_id, fase, funcion, prioridad=0, quest_id=None):
        """
        Registra un trigger de la accion dormir. `fase` es "antes" (corre antes
        de avanzar el dia; ej. eventos nocturnos) o "despues" (corre despues
        del autosave; ej. escenas al despertar). El orden importa: si un
        trigger "despues" devuelve label, se saltean los siguientes Y los
        mensajes al despertar (misma semantica que los jumps que reemplaza).
        """
        if fase == "antes":
            _registrar_trigger(TRIGGERS_DORMIR_ANTES, trigger_id, funcion, prioridad)
        else:
            _registrar_trigger(TRIGGERS_DORMIR_DESPUES, trigger_id, funcion, prioridad)
        TRIGGER_QUEST[trigger_id] = quest_id

    def registrar_trigger_avanzar(trigger_id, funcion, prioridad=0, quest_id=None):
        """Registra un trigger evaluado tras avanzar el horario con el boton."""
        _registrar_trigger(TRIGGERS_AVANZAR, trigger_id, funcion, prioridad)
        TRIGGER_QUEST[trigger_id] = quest_id

    def registrar_trigger_salir_celular(trigger_id, funcion, prioridad=0, quest_id=None):
        """
        Registra un trigger evaluado al CERRAR el celular.

        Es el enganche para el contenido que le pide algo al jugador adentro
        del celular (leer una app, contestar un chat) y sigue la escena cuando
        sale. El label destino es CONTENIDO: termina en `jump game_loop`.
        """
        _registrar_trigger(TRIGGERS_SALIR_CELULAR, trigger_id, funcion, prioridad)
        TRIGGER_QUEST[trigger_id] = quest_id

    def _ejecutar_triggers(registro, marcar_gl=False, solo_duenio=None):
        """
        Evalua los triggers de un registro en orden de prioridad (mayor
        primero; a igual prioridad, orden de registro). Devuelve el label del
        primero que pida saltar, o None. Si marcar_gl, deja el id del trigger
        en _gl_ultimo_trigger (tag de Sentry para el diagnostico S11).

        `solo_duenio`: si viene, el label de un trigger cuyo duenio no sea ese
        se IGNORA (el trigger corre igual por sus efectos). Lo usa game_loop
        mientras hay una restriccion con dueño activa.
        """
        for _prio, _orden, _tid, _fn in sorted(
                registro, key=lambda t: (-t[0], t[1])):
            # Autodisparos: un trigger de quest no se evalua si su quest no
            # esta viva o la frena un conflicto (planificador, capa 2).
            _qid_t = TRIGGER_QUEST.get(_tid)
            if _qid_t and not planificador_trigger_permitido(_qid_t):
                continue
            _lbl = _fn()
            if _lbl:
                if (solo_duenio is not None
                        and TRIGGER_DUENIO.get(_tid) != solo_duenio):
                    if config.developer:
                        print("[Triggers] '%s' quiso saltar a '%s' dentro de la "
                              "restriccion de %r: se ignora" % (_tid, _lbl, solo_duenio))
                    continue
                if marcar_gl:
                    store._gl_ultimo_trigger = _tid
                # Punto de activacion: el motor salta a una quest, la registra.
                activar_quest(TRIGGER_QUEST.get(_tid), origen="trigger:" + _tid)
                return _lbl
        if marcar_gl:
            store._gl_ultimo_trigger = ""
        return None

    def ejecutar_triggers_game_loop():
        """
        Evalua los triggers del game_loop, salvo que alguien los tenga
        congelados (ver registrar_congelamiento_triggers).
        """
        for _fn_cong in CONGELAMIENTOS_TRIGGER:
            try:
                if _fn_cong():
                    store._gl_ultimo_trigger = ""
                    return None
            except Exception:
                pass
        # Con una restriccion con dueño activa, solo sus propios triggers
        # pueden saltar (ver registrar_trigger_game_loop).
        _r = getattr(store, 'restriccion_quest_activa', None)
        _duenio = getattr(_r, 'duenio', None) if (_r is not None and _r.activa) else None
        return _ejecutar_triggers(TRIGGERS_GAME_LOOP, marcar_gl=True,
                                  solo_duenio=_duenio)

    def ejecutar_triggers_dormir(fase):
        registro = TRIGGERS_DORMIR_ANTES if fase == "antes" else TRIGGERS_DORMIR_DESPUES
        return _ejecutar_triggers(registro)

    def ejecutar_triggers_avanzar():
        return _ejecutar_triggers(TRIGGERS_AVANZAR)

    def ejecutar_triggers_salir_celular():
        return _ejecutar_triggers(TRIGGERS_SALIR_CELULAR)
