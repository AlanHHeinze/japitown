################################################################################
## Sistema de Restricciones de Quest/Evento
################################################################################
## Controla qué puede hacer el jugador durante quests y eventos activos.
## Permite bloquear movimiento, acciones, interacciones NPC, celular,
## controlar visibilidad de NPCs y agregar elementos interactivos temporales.
##
## Funciona tanto para quests como para eventos — usa una variable global.

init python:

    # TODO LO QUE MUEVE EL HORARIO, en un solo lugar. `congelar_reloj=True`
    # bloquea este set entero. Una accion nueva que llame a avanzar_horario()
    # se agrega ACA y queda cubierta en todas las restricciones existentes.
    #
    #   avanzar_tiempo  el boton
    #   dormir          cambia el dia
    #   entrenar / trabajar   panel de la habitacion del MC (hud_stats)
    #   ver_tv / cocinar      acciones de locacion (actions_catalog)
    #   hablar          el talk termina con avanzar_horario()
    #   usar_item       el casco VR gasta el horario
    ACCIONES_RELOJ = ("avanzar_tiempo", "dormir", "entrenar", "trabajar",
                      "ver_tv", "cocinar", "hablar", "usar_item")

    class RestriccionQuest:
        """
        Define las restricciones activas durante una quest o evento.
        
        Por defecto, cuando una restricción está activa:
        - La interacción con NPCs queda BLOQUEADA (se puede desbloquear por NPC)
        - El movimiento es libre a menos que se defina whitelist
        - Las acciones son libres a menos que se bloqueen explícitamente
        """
        
        def __init__(self,
            locaciones_permitidas=None,
            acciones_bloqueadas=None,
            mensaje_movimiento="No puedo ir ahí ahora",
            mensajes_acciones=None,
            npcs_ocultos=None,
            npcs_interactuables=None,
            mensaje_npc_bloqueado="No tengo tiempo para eso ahora",
            celular_bloqueado=False,
            mensaje_celular="No es momento de usar el celular",
            elementos_escena=None,
            mensajes_bloqueados=False,
            mensaje_accion_default=None,
            duenio=None,
            congelar_reloj=False):
            """
            Args:
                duenio: Id del contenido que la activa ("violet_ev03",
                        "mc_0_a"...). Otro contenido NO puede pisarla ni
                        levantarla — ver activar_restriccion.
                congelar_reloj: True = bloquea TODO lo que mueve el horario
                        (ACCIONES_RELOJ), ademas de lo que venga en
                        acciones_bloqueadas. Es la forma correcta de decir "el
                        tiempo no avanza hasta que se resuelva esto": listar los
                        ids a mano se olvida de alguno (ver TV, el talk...) y el
                        jugador se escapa a otro horario donde la salida ya no
                        existe.
                locaciones_permitidas: Set/lista de IDs de locaciones permitidas (whitelist).
                                       None = todas permitidas.
                acciones_bloqueadas: Set/lista de strings de acciones bloqueadas.
                                     Extensible: "entrenar", "trabajar", "avanzar_tiempo",
                                     "dormir", "usar_item", "comprar", etc.
                mensaje_movimiento: Mensaje al intentar ir a locación no permitida.
                mensajes_acciones: Dict {accion_id: mensaje} para mensajes específicos.
                                   Si una accion está bloqueada pero no tiene mensaje
                                   específico, se usa un genérico.
                npcs_ocultos: Set/lista de NPC IDs a ocultar de la escena.
                npcs_interactuables: Set/lista de NPC IDs con los que SÍ se puede
                                     interactuar. Por defecto NINGUNO es interactuable
                                     cuando hay restricción activa. None = ninguno.
                mensaje_npc_bloqueado: Mensaje al intentar interactuar con NPC bloqueado.
                celular_bloqueado: Bool, si se bloquea el acceso al celular.
                mensaje_celular: Mensaje al intentar abrir el celular.
                elementos_escena: Lista de dicts definiendo elementos interactivos
                                   temporales por locación. Formato:
                                   [{"locacion": str, "tipo": str, "id": str,
                                     "imagen": str, "pos": (x,y), "label": str}, ...]
            """
            # Movimiento
            self.locaciones_permitidas = set(locaciones_permitidas) if locaciones_permitidas else None
            self.mensaje_movimiento = mensaje_movimiento
            
            # Acciones
            self.acciones_bloqueadas = set(acciones_bloqueadas) if acciones_bloqueadas else set()
            self.congelar_reloj = bool(congelar_reloj)
            if self.congelar_reloj:
                self.acciones_bloqueadas |= set(ACCIONES_RELOJ)
            self.mensajes_acciones = mensajes_acciones or {}

            # Quien la puso. None = anonima (codigo viejo): cualquiera la levanta.
            self.duenio = duenio
            
            # NPCs
            self.npcs_ocultos = set(npcs_ocultos) if npcs_ocultos else set()
            self.npcs_interactuables = set(npcs_interactuables) if npcs_interactuables else set()
            self.mensaje_npc_bloqueado = mensaje_npc_bloqueado
            
            # Celular
            self.celular_bloqueado = celular_bloqueado
            self.mensaje_celular = mensaje_celular

            # Mensajes (bloqueo de entrega de mensajes en espera)
            self.mensajes_bloqueados = mensajes_bloqueados
            
            # Elementos de escena
            self.elementos_escena = list(elementos_escena) if elementos_escena else []

            # Mensaje genérico para acciones bloqueadas sin mensaje específico
            self.mensaje_accion_default = mensaje_accion_default
            
            # Labels por locación — se disparan al entrar a una locación
            self.labels_por_locacion = {}
            
            # Estado
            self.activa = True
        
        def es_locacion_permitida(self, locacion_id):
            """Verifica si una locación está permitida."""
            if not self.activa:
                return True
            if self.locaciones_permitidas is None:
                return True
            return locacion_id in self.locaciones_permitidas
        
        def obtener_bloqueo_accion(self, accion_id):
            """
            Verifica si una accion está bloqueada.
            
            Returns:
                str: Mensaje de bloqueo, o None si la accion está permitida.
            """
            if not self.activa:
                return None
            if accion_id not in self.acciones_bloqueadas:
                return None
            # Buscar mensaje específico → default de la restricción → genérico
            if accion_id in self.mensajes_acciones:
                return renpy.translate_string(self.mensajes_acciones[accion_id])
            if self.mensaje_accion_default:
                return renpy.translate_string(self.mensaje_accion_default)
            return renpy.translate_string("No puedo hacer eso ahora")
        
        def es_npc_oculto(self, npc_id):
            """Verifica si un NPC debe estar oculto."""
            if not self.activa:
                return False
            return npc_id in self.npcs_ocultos
        
        def es_npc_interactuable(self, npc_id):
            """
            Verifica si se puede interactuar con un NPC.
            Por defecto, NINGÚN NPC es interactuable cuando hay restricción activa.
            Solo los que estén explícitamente en npcs_interactuables lo son.
            """
            if not self.activa:
                return True
            return npc_id in self.npcs_interactuables
        
        def obtener_elementos_para_locacion(self, locacion_id):
            """Obtiene los elementos de escena para una locación específica."""
            if not self.activa:
                return []
            return [e for e in self.elementos_escena if e.get("locacion") == locacion_id]
        
        def remover_elemento(self, elemento_id):
            """Remueve un elemento de escena por su ID."""
            self.elementos_escena = [
                e for e in self.elementos_escena if e.get("id") != elemento_id
            ]
        
        def hay_elementos(self):
            """Verifica si quedan elementos de escena."""
            return len(self.elementos_escena) > 0
        
        def agregar_locacion_permitida(self, locacion_id):
            """Agrega una locación a la whitelist."""
            if self.locaciones_permitidas is None:
                self.locaciones_permitidas = set()
            self.locaciones_permitidas.add(locacion_id)
        
        def remover_locacion_permitida(self, locacion_id):
            """Remueve una locación de la whitelist."""
            if self.locaciones_permitidas:
                self.locaciones_permitidas.discard(locacion_id)
        
        def agregar_accion_bloqueada(self, accion_id, mensaje=None):
            """Agrega una acción al set de bloqueadas."""
            self.acciones_bloqueadas.add(accion_id)
            if mensaje:
                self.mensajes_acciones[accion_id] = mensaje
        
        def remover_accion_bloqueada(self, accion_id):
            """Remueve una acción del set de bloqueadas."""
            self.acciones_bloqueadas.discard(accion_id)
            self.mensajes_acciones.pop(accion_id, None)
        
        def hacer_npc_interactuable(self, npc_id):
            """Permite interactuar con un NPC específico."""
            self.npcs_interactuables.add(npc_id)
        
        def hacer_npc_no_interactuable(self, npc_id):
            """Bloquea la interacción con un NPC específico."""
            self.npcs_interactuables.discard(npc_id)
        
        def ocultar_npc(self, npc_id):
            """Oculta un NPC de la escena."""
            self.npcs_ocultos.add(npc_id)
        
        def mostrar_npc(self, npc_id):
            """Muestra un NPC que estaba oculto."""
            self.npcs_ocultos.discard(npc_id)
        
        def agregar_elemento_escena(self, elemento):
            """Agrega un elemento de escena dinámico."""
            self.elementos_escena.append(elemento)
        
        def registrar_label_locacion(self, locacion_id, label_name):
            """Registra un label para disparar al entrar a una locación."""
            self.labels_por_locacion[locacion_id] = label_name
        
        def obtener_label_locacion(self, locacion_id):
            """Obtiene el label a disparar al entrar a una locación, o None."""
            if not self.activa:
                return None
            return self.labels_por_locacion.get(locacion_id)


# Variable global de restricción activa
default restriccion_quest_activa = None


################################################################################
## Funciones Helper — Interfaz simple para usar desde labels
################################################################################

init python:
    
    def activar_restriccion(**kwargs):
        """
        Activa una restricción de quest/evento.
        
        Ejemplo de uso:
            $ activar_restriccion(
                locaciones_permitidas=["casa_living", "casa_hmc"],
                acciones_bloqueadas=["entrenar", "trabajar", "avanzar_tiempo", "dormir"],
                mensaje_movimiento="Debo ir a mi habitación",
                mensaje_npc_bloqueado="No tengo tiempo para hablar",
                celular_bloqueado=True,
                elementos_escena=[
                    {"locacion": "casa_hmc", "tipo": "imagebutton", "id": "camisa",
                     "imagen": "images/quest/camisa.png", "pos": (400, 300),
                     "label": "recoger_camisa"},
                ]
            )
        """
        # EL SLOT ES UNO SOLO, y eso fue bug de jugadores: un contenido activaba
        # la suya encima de la de otro (o la levantaba con un desactivar_
        # restriccion() suelto) y se llevaba puesta la maquina de estados
        # ajena — los registrar_label_locacion, el recorrido acotado, todo. La
        # otra quest quedaba muerta a mitad de camino.
        #
        # Regla: una restriccion CON dueño solo la LEVANTA su dueño (ver
        # desactivar_restriccion). Activar encima de una ajena si se permite
        # —con aviso en desarrollo— porque hay "gates blandos" que duran dias
        # (Monica 0_b frenando dormir hasta ir al living, la 04_b con solo
        # npcs_interactuables) y rechazar la activacion dejaria a la otra quest
        # corriendo sin su recorrido. Lo que de verdad protege una cadena en
        # curso es la regla de los triggers (triggers_contenido: adentro de una
        # restriccion con dueño no salta ningun trigger ajeno) — por ahi entraba
        # el contenido que pisaba. Auditoria 2026-09-10.
        _actual = store.restriccion_quest_activa
        _nuevo_duenio = kwargs.get("duenio")
        if (config.developer and _actual is not None and _actual.activa
                and getattr(_actual, "duenio", None) is not None
                and _nuevo_duenio != _actual.duenio):
            print("[Restriccion] %r activa encima de la de %r (se reemplaza)"
                  % (_nuevo_duenio, _actual.duenio))

        store.restriccion_quest_activa = RestriccionQuest(**kwargs)
        return store.restriccion_quest_activa

    def desactivar_restriccion(duenio=None):
        """
        Desactiva la restricción actual.

        `duenio` tiene que ser el mismo que la activo. "*" la levanta sea de
        quien sea — es para labels de test y cheats, nunca para contenido.
        """
        _actual = store.restriccion_quest_activa
        if (_actual is not None
                and getattr(_actual, "duenio", None) is not None
                and duenio != "*" and duenio != _actual.duenio):
            if config.developer:
                print("[Restriccion] %r intento levantar la de %r: se ignora"
                      % (duenio, _actual.duenio))
            return
        store.restriccion_quest_activa = None

    def hay_restriccion_activa():
        """Verifica si hay una restricción activa."""
        r = store.restriccion_quest_activa
        return r is not None and r.activa

    def mensajes_estan_bloqueados():
        """
        Verifica si la entrega de mensajes en espera esta bloqueada.
        Diferente de celular_esta_bloqueado() que bloquea ABRIR el celular.
        """
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return False
        return getattr(r, 'mensajes_bloqueados', False)
    
    # ==========================================================================
    # Embudo unico de bloqueos (refactor C11)
    #
    # accion_bloqueada() es LA UNICA puerta para saber si una accion esta
    # bloqueada. Consulta las cuatro fuentes en orden fijo; los labels hacen un
    # solo `if accion_bloqueada(...)` y no replican chequeos por su cuenta.
    # El contenido agrega bloqueos propios con registrar_bloqueo_accion()
    # (condicion = funcion de MODULO), nunca con ifs en los labels del motor.
    #
    # Los mensajes se traducen aca via translate_string; los `old` viven en
    # tl/english/bloqueos_strings.rpy.
    # ==========================================================================

    BLOQUEOS_ACCION_REGISTRO = {}  # {accion_id: [(condicion, mensaje)]}

    # Bloqueos que valen para CUALQUIER accion, no para una lista de ids.
    # Para las situaciones de "mientras pase esto no se puede hacer nada" — por
    # ejemplo una conversacion de chat abierta que hay que contestar primero.
    #
    # Se usa esto y no un registro por id para cada accion porque la lista de
    # acciones que gastan tiempo crece: `avanzar_tiempo`, `dormir`, `entrenar`,
    # `trabajar`, `hablar`, `usar_item`, y todas las AccionLocacion (cocinar,
    # ver_tv, las de quest...). Enumerarlas seria una lista a mantener que se
    # desactualiza sola en cuanto se agrega una accion nueva; asi, la accion
    # nueva queda cubierta sin tocar nada.
    BLOQUEOS_GLOBALES = []  # [(condicion, mensaje)]

    # Bloqueos de UNA locacion, con su propio mensaje.
    #
    # La restriccion de quest ya sabe acotar el movimiento, pero al reves: dice
    # a donde SI se puede ir, y tiene un unico `mensaje_movimiento` para todos
    # los destinos prohibidos. Para "todo abierto menos el sotano, y porque
    # Violet sigue con las amigas" eso no alcanza: habria que listar las 17
    # locaciones restantes (y actualizar la lista cada vez que se agrega una) y
    # el texto quedaria generico.
    BLOQUEOS_LOCACION_REGISTRO = {}  # {locacion_id: [(condicion, mensaje)]}

    MENSAJES_BLOQUEO_EVENTS = {
        "avanzar_tiempo": "No puedes avanzar el tiempo ahora.",
    }
    MENSAJE_BLOQUEO_EVENTS_DEFAULT = "No puedo hacer eso ahora."
    MENSAJE_BLOQUEO_PRIORITARIO = "Debo responder el mensaje de {npc} antes de continuar"

    def registrar_bloqueo_accion(accion_id, condicion, mensaje):
        """
        Registra un bloqueo de contenido para una accion (ej. una quest que
        impide dormir mientras tiene una entrega pendiente). `condicion` es una
        funcion de modulo sin argumentos; `mensaje` se muestra como pensamiento.
        """
        BLOQUEOS_ACCION_REGISTRO.setdefault(accion_id, []).append(
            (condicion, mensaje))

    def registrar_bloqueo_global(condicion, mensaje):
        """
        Registra un bloqueo que aplica a TODAS las acciones.

        `condicion` es una funcion de modulo sin argumentos; `mensaje` se muestra
        como pensamiento. Se evalua ultimo en accion_bloqueada(), asi que un
        bloqueo mas especifico (restriccion de quest, evento, por accion) le gana
        y puede dar un texto mejor.

        OJO: bloquea de verdad TODO. Solo para situaciones de las que el jugador
        pueda salir por su cuenta — si no, se traba la partida.
        """
        BLOQUEOS_GLOBALES.append((condicion, mensaje))

    def registrar_bloqueo_locacion(locacion_id, condicion, mensaje):
        """
        Cierra UNA locacion mientras `condicion()` sea verdadera, con su propio
        mensaje. Lo consulta accion_bloqueada_movimiento() ANTES de la
        restriccion de quest, asi que vale con restriccion activa o sin ella.

        `condicion` es una funcion de modulo sin argumentos; `mensaje` se
        muestra como pensamiento (se traduce aca, el `old` va en
        tl/english/bloqueos_strings.rpy).

            registrar_bloqueo_locacion(
                "casa_sotano", _va35_sotano_cerrado,
                "Violet sigue con las amigas, mejor no molestarlas")

        Cuando lo que hay que acotar es a donde PUEDE ir el jugador durante una
        escena (unas pocas locaciones habilitadas), eso sigue siendo
        `activar_restriccion(locaciones_permitidas=[...])`. Esto es para lo
        contrario: el mundo abierto con una puerta cerrada.

        OJO: como todo bloqueo, solo lo puede sostener algo que el jugador
        pueda resolver — una condicion que se apaga al completar la quest, al
        dormir o al cambiar el horario. Una que dependa de entrar a la locacion
        bloqueada es un soft lock.
        """
        BLOQUEOS_LOCACION_REGISTRO.setdefault(locacion_id, []).append(
            (condicion, mensaje))

    def accion_bloqueada(accion_id, incluir_globales=True):
        """
        Verifica si una accion esta bloqueada. Consulta EN ORDEN:
        1. la restriccion de quest activa,
        2. los bloqueos declarados por events (sistema_events.hay_bloqueo),
        3. mensajes prioritarios sin responder (solo dormir/avanzar_tiempo),
        4. los bloqueos registrados por contenido,
        5. los bloqueos GLOBALES.

        `incluir_globales=False` saltea el paso 5. Es para ABRIR UNA APP del
        celular: ver ver app_celular_bloqueada().

        Returns:
            str: Mensaje de bloqueo (ya traducido), o None si esta permitida.
        """
        # 0. Reserva del planificador: durante el slot reservado por una quest
        #    de corrido el reloj no pasa de largo (core/quests/planificador.rpy).
        if accion_id in ACCIONES_RELOJ:
            _msg_res = planificador_bloqueo_reloj()
            if _msg_res:
                return _msg_res

        # 1. Restriccion de quest activa
        r = store.restriccion_quest_activa
        if r is not None and r.activa:
            msg = r.obtener_bloqueo_accion(accion_id)
            if msg is not None:
                return renpy.translate_string(msg)

        # 2. Bloqueos de events
        if hasattr(store, 'sistema_events') and store.sistema_events.hay_bloqueo(accion_id):
            plantilla = MENSAJES_BLOQUEO_EVENTS.get(
                accion_id, MENSAJE_BLOQUEO_EVENTS_DEFAULT)
            return renpy.translate_string(plantilla)

        # 3. Mensaje prioritario ya entregado y sin responder
        if accion_id in ("dormir", "avanzar_tiempo") and hasattr(store, 'sistema_mensajes'):
            npc_prio = obtener_bloqueo_mensaje_prioritario()
            if npc_prio:
                return renpy.translate_string(
                    MENSAJE_BLOQUEO_PRIORITARIO).format(npc=npc_prio)

        # 4. Bloqueos registrados por el contenido
        for _cond, _msg in BLOQUEOS_ACCION_REGISTRO.get(accion_id, []):
            if _cond():
                return renpy.translate_string(_msg)

        # 5. Bloqueos GLOBALES: valen para cualquier accion_id.
        if incluir_globales:
            for _cond, _msg in BLOQUEOS_GLOBALES:
                if _cond():
                    return renpy.translate_string(_msg)

        return None

    def app_celular_bloqueada(app_id):
        """
        ¿Se puede ABRIR esta app del celular?

        Es accion_bloqueada() SIN los bloqueos globales. Abrir una app es
        navegar por una UI, no hacer algo en el mundo, y un bloqueo global no
        tiene forma de distinguirlas: cubre cualquier accion_id que le pasen.

        BUG REAL (2026-08-31): la quest de deseo 20 encierra al jugador con un
        bloqueo global hasta que le escriba a Violet... y ese mismo bloqueo le
        tapaba la app de Chat, que es lo unico que lo destraba. La partida
        quedaba muerta. El sistema Mensajear tenia el mismo agujero latente.

        Los bloqueos ESPECIFICOS (restriccion de quest, events, los registrados
        por accion) siguen valiendo: una quest que quiera cerrar la Tienda o las
        Pistas lo sigue pudiendo hacer nombrandolas.
        """
        return accion_bloqueada(app_id, incluir_globales=False)


    def accion_bloqueada_movimiento(destino_id):
        """
        Verifica si el movimiento a una locación está bloqueado. Consulta EN
        ORDEN:
        1. los bloqueos de locacion registrados por contenido,
        2. la restriccion de quest activa (whitelist + mensaje_movimiento).

        Los registrados van primero porque son mas especificos: nombran UNA
        locacion y traen su propio texto, mientras que la restriccion tiene un
        solo mensaje para todo lo que deja afuera.

        Returns:
            str: Mensaje de bloqueo, o None si el movimiento está permitido.
        """
        # 1. Bloqueos de locacion registrados por el contenido
        for _cond, _msg in BLOQUEOS_LOCACION_REGISTRO.get(destino_id, []):
            if _cond():
                return renpy.translate_string(_msg)

        # 2. Restriccion de quest activa
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return None
        if r.es_locacion_permitida(destino_id):
            return None
        return renpy.translate_string(r.mensaje_movimiento)
    
    def npc_esta_oculto(npc_id):
        """
        Verifica si un NPC no debe dibujarse en la escena.

        Ademas de la restriccion, mira la DISPONIBILIDAD: un NPC fuera de juego
        no se dibuja (core/npcs/npc_disponibilidad.rpy). Sin esto el sprite
        seguiria en la locacion pero sin responder al click — se veria como un
        bug, no como que no esta.
        """
        if not npc_disponible(npc_id):
            return True

        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return False
        return r.es_npc_oculto(npc_id)
    
    # ── Trasnoche: los NPC duermen ───────────────────────────────────────────
    # Regla GENERAL del juego, no de una quest: de madrugada nadie se deja
    # molestar. La puerta ya lo resolvia por su lado (door_access_system corta
    # el trasnoche salvo con la ventaja de ingreso), pero faltaba el click
    # directo sobre el NPC: si lograbas estar en la misma locacion que el,
    # se abria el menu de interaccion como a cualquier hora.
    #
    # Se sale del bloqueo por DOS vias, las dos declarativas:
    #   1. La ventaja "npc_interaccion_trasnoche" — para cuando un hito habilite
    #      hablarle de madrugada. Hoy no la otorga ninguno.
    #   2. registrar_excepcion_trasnoche(fn) — para el contenido que necesita
    #      la escena igual (una quest que te hace despertarla, por ejemplo).
    #
    # Ojo si se agrega contenido nocturno: sin excepcion registrada, el NPC no
    # se puede clickear en trasnoche.

    MENSAJE_NPC_DURMIENDO = "Debe estar durmiendo, no voy a molestar."

    # [fn(npc_id) -> bool]. True = se puede interactuar igual.
    EXCEPCIONES_TRASNOCHE = []

    def registrar_excepcion_trasnoche(fn):
        """
        Registra una excepcion al bloqueo de trasnoche. `fn` recibe el npc_id y
        devuelve True si con ESE NPC se puede interactuar igual.

        Funcion de MODULO, nunca lambda: queda en una lista de init (regla
        anti-PicklingError del proyecto).
        """
        EXCEPCIONES_TRASNOCHE.append(fn)

    def npc_durmiendo(npc_id):
        """True si el NPC esta durmiendo y no corresponde molestarlo."""
        if getattr(store, 'horario_actual', 0) != HORARIO_TRASNOCHE:
            return False

        # Ventaja de hito (el catalogo puede no estar cargado en un save viejo)
        try:
            if npc_tiene_ventaja(npc_id, "npc_interaccion_trasnoche"):
                return False
        except Exception:
            pass

        for _fn_exc in EXCEPCIONES_TRASNOCHE:
            try:
                if _fn_exc(npc_id):
                    return False
            except Exception:
                pass

        return True

    def npc_interactuable(npc_id):
        """
        Verifica si se puede interactuar con un NPC.
        De trasnoche duermen; despues, si hay restricción activa, por defecto
        NINGÚN NPC es interactuable.

        La DISPONIBILIDAD va primero que todo (core/npcs/npc_disponibilidad):
        un NPC fuera de juego no se toca, ni siquiera con una restriccion que
        lo declare interactuable.
        """
        if not npc_disponible(npc_id):
            return False

        if npc_durmiendo(npc_id):
            return False

        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return True
        return r.es_npc_interactuable(npc_id)

    def mensaje_npc_bloqueado(npc_id=None):
        # Si esta fuera de juego, el motivo lo da la disponibilidad y no la
        # restriccion: es mas especifico y ademas puede no haber restriccion.
        _m_disp = motivo_npc_no_disponible(npc_id) if npc_id else None
        if _m_disp:
            return _m_disp

        """
        Mensaje al intentar interactuar con un NPC bloqueado.

        `npc_id` es opcional por compatibilidad, pero conviene pasarlo: sin el
        no se puede distinguir "esta durmiendo" de un bloqueo de quest, y si el
        bloqueo es solo por el horario no hay restricción activa de la que sacar
        texto — devolveria "" y saldria un pensamiento vacio.
        """
        if npc_id is not None and npc_durmiendo(npc_id):
            return renpy.translate_string(MENSAJE_NPC_DURMIENDO)

        r = store.restriccion_quest_activa
        if r is None:
            return ""
        return renpy.translate_string(r.mensaje_npc_bloqueado)
    
    def celular_esta_bloqueado():
        """
        Verifica si el celular está bloqueado.

        Returns:
            str: Mensaje de bloqueo, o None si el celular está permitido.
        """
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return None
        if not r.celular_bloqueado:
            return None
        return renpy.translate_string(r.mensaje_celular)
    
    def obtener_elementos_escena(locacion_id):
        """Obtiene los elementos de escena de la restricción para una locación."""
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return []
        return r.obtener_elementos_para_locacion(locacion_id)
    
    def remover_elemento_escena(elemento_id):
        """Remueve un elemento de escena de la restricción activa."""
        r = store.restriccion_quest_activa
        if r and r.activa:
            r.remover_elemento(elemento_id)
