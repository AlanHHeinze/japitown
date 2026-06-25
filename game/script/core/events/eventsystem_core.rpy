################################################################################
## Sistema de Events - Versión 1.0
################################################################################
## Sistema para gestionar eventos dinámicos con condiciones y modificaciones
## Los eventos pueden aparecer/desaparecer y modificar temporalmente el juego

# Estados de un evento
define ESTADO_EVENT_OCULTO = "oculto"
define ESTADO_EVENT_VISIBLE = "visible"
define ESTADO_EVENT_ACTIVO = "activo"
define ESTADO_EVENT_COMPLETADO = "completado"

# Tipos de evento
define TIPO_EVENT_ESPORADICO = "esporadico"      # Se completa y desaparece
define TIPO_EVENT_PERSISTENTE = "persistente"    # Permanece mientras condición se cumpla

init python:
    
    class Event:
        """
        Clase que representa un evento del juego.
        
        Los eventos son más simples que las quests, diseñados para:
        - Aparecer/desaparecer según condiciones
        - Modificar temporalmente elementos del juego
        - Ejecutar contenido cuando se activan
        """
        
        def __init__(self, id, nombre, tipo=TIPO_EVENT_ESPORADICO, prioridad=0,
                     condicion_aparicion=None, condicion_activacion=None,
                     condicion_duracion=None, label_efecto=None, modificaciones=None,
                     descripcion="", npc_id="", mensaje_pista="", mensaje_que_hacer="",
                     condicion_cierre_texto="", mensaje_despertar="",
                     config_etapas=None, on_aparicion=None):
            """
            Args:
                id: ID único del evento
                nombre: Nombre descriptivo
                tipo: "esporadico" o "persistente"
                prioridad: Valor numérico (mayor = más prioridad)
                condicion_aparicion: Callable que retorna bool (cuándo se hace visible)
                condicion_activacion: Callable que retorna bool (cuándo ejecutar efecto)
                                      Si es None, se autoactiva al aparecer
                condicion_duracion: Callable que retorna bool (para persistentes, cuándo termina)
                label_efecto: Label a ejecutar cuando se activa (opcional)
                modificaciones: Dict extensible con cambios temporales
                descripcion: Descripción del evento para mostrar en pistas
                npc_id: ID del NPC asociado (para icono en panel de pistas)
                mensaje_pista: Mensaje de pista para el panel (fallback)
                mensaje_que_hacer: Mensaje de qué hacer para el panel (fallback)
                condicion_cierre_texto: Texto legible de la condición de cierre
                mensaje_despertar: Mensaje para mostrar al despertar (fallback)
                config_etapas: Dict {ESTADO_X: ConfigEtapa} para overrides por estado
            """
            self.id = id
            self.nombre = nombre
            self.tipo = tipo
            self.prioridad = prioridad
            
            # Condiciones (callables)
            self.condicion_aparicion = condicion_aparicion
            self.condicion_activacion = condicion_activacion
            self.condicion_duracion = condicion_duracion
            
            # Efectos
            self.label_efecto = label_efecto
            self.modificaciones = modificaciones or {}
            
            # Campos para panel de pistas (fallback)
            self.descripcion = descripcion
            self.npc_id = npc_id
            self.mensaje_pista = mensaje_pista
            self.mensaje_que_hacer = mensaje_que_hacer
            self.condicion_cierre_texto = condicion_cierre_texto
            self.mensaje_despertar = mensaje_despertar
            
            # Configuración de etapas por estado
            self.config_etapas = config_etapas or {}

            # Callback al volverse visible por primera vez
            self.on_aparicion = on_aparicion

            # Estado
            self.estado = ESTADO_EVENT_OCULTO
        
        def obtener_mensajes(self):
            """
            Obtiene los mensajes de pista y qué hacer del evento.
            Prioridad: config_etapas > campos estáticos.
            Compatible con el formato de Quest.obtener_mensajes().
            
            Returns:
                dict: {"pista": str, "que_hacer": str}
            """
            pista = ""
            que_hacer = ""
            
            # Buscar override en config_etapas
            cfg_etapa = self.config_etapas.get(self.estado)
            if cfg_etapa:
                pista_override = cfg_etapa.obtener_pista()
                que_hacer_override = cfg_etapa.obtener_que_hacer()
                if pista_override:
                    pista = pista_override
                if que_hacer_override:
                    que_hacer = que_hacer_override
                if pista and que_hacer:
                    return {"pista": pista, "que_hacer": que_hacer}
            
            # Fallback a campos estáticos
            if not pista:
                pista = self.mensaje_pista or self.descripcion or self.nombre
            if not que_hacer:
                que_hacer = self.mensaje_que_hacer or pista
            
            # Traducir antes de retornar
            try:
                pista = renpy.translate_string(pista) if pista else pista
                que_hacer = renpy.translate_string(que_hacer) if que_hacer else que_hacer
            except Exception:
                pass
            
            return {"pista": pista, "que_hacer": que_hacer}
        
        def obtener_mensaje_despertar_actual(self):
            """
            Obtiene el mensaje de despertar según el estado actual.
            Prioridad: config_etapas > mensaje_despertar estático.
            
            Returns:
                str: Mensaje para mostrar al despertar, o ""
            """
            cfg_etapa = self.config_etapas.get(self.estado)
            if cfg_etapa:
                msg = cfg_etapa.obtener_mensaje_despertar()
                if msg:
                    return msg
            
            msg = self.mensaje_despertar or ""
            if msg:
                try:
                    msg = renpy.translate_string(msg)
                except Exception:
                    pass
            return msg
        
        def verificar_aparicion(self):
            """Verifica si el evento debe aparecer."""
            if self.condicion_aparicion is None:
                return True
            try:
                return self.condicion_aparicion()
            except:
                return False
        
        def verificar_activacion(self):
            """Verifica si el evento debe activarse."""
            if self.condicion_activacion is None:
                return True  # Autoactivar
            try:
                return self.condicion_activacion()
            except:
                return False
        
        def verificar_duracion(self):
            """Verifica si el evento persistente debe terminar."""
            if self.tipo != TIPO_EVENT_PERSISTENTE:
                return False
            if self.condicion_duracion is None:
                return False  # Sin condición de fin = permanece
            try:
                return self.condicion_duracion()
            except:
                return False
        
        def aparecer(self):
            """Hace visible el evento y aplica modificaciones."""
            if self.estado == ESTADO_EVENT_OCULTO:
                self.estado = ESTADO_EVENT_VISIBLE
                
                # Registrar modificaciones en el sistema
                if self.modificaciones:
                    sistema_events._aplicar_modificaciones(self)
                

                
                return True
            return False
        
        def activar(self):
            """Activa el evento (ejecuta su efecto)."""
            if self.estado == ESTADO_EVENT_VISIBLE:
                self.estado = ESTADO_EVENT_ACTIVO
                

                
                return True
            return False
        
        def completar(self):
            """Completa el evento y limpia modificaciones."""
            # Bloquear rollback para que el jugador no pueda volver a entrar al evento
            renpy.block_rollback()

            self.estado = ESTADO_EVENT_COMPLETADO
            
            # Remover modificaciones
            if self.modificaciones:
                sistema_events._remover_modificaciones(self)
            

            
            # Disparar mensaje de chat si existe
            if hasattr(store, 'sistema_mensajes'):
                store.sistema_mensajes.disparar_por_trigger("event", self.id, self.npc_id)
        
        def ocultar(self):
            """Oculta un evento persistente que ya no cumple condiciones."""
            if self.estado in [ESTADO_EVENT_VISIBLE, ESTADO_EVENT_ACTIVO]:
                # Remover modificaciones
                if self.modificaciones:
                    sistema_events._remover_modificaciones(self)
                
                self.estado = ESTADO_EVENT_OCULTO
                

        
        def actualizar(self):
            """
            Actualiza el estado del evento según sus condiciones.
            Debe llamarse periódicamente.
            """
            # Evento oculto: verificar aparición
            if self.estado == ESTADO_EVENT_OCULTO:
                if self.verificar_aparicion():
                    self.aparecer()
                    # Verificar activación inmediata
                    if self.verificar_activacion():
                        self.activar()
            
            # Evento visible: verificar activación
            elif self.estado == ESTADO_EVENT_VISIBLE:
                if self.verificar_activacion():
                    self.activar()
            
            # Evento activo persistente: verificar fin
            elif self.estado == ESTADO_EVENT_ACTIVO:
                if self.tipo == TIPO_EVENT_PERSISTENTE:
                    if self.verificar_duracion():
                        self.completar()
            
            # Evento completado esporádico: no reaparece
            # Evento completado persistente: verificar si debe reaparecer
            elif self.estado == ESTADO_EVENT_COMPLETADO:
                if self.tipo == TIPO_EVENT_PERSISTENTE:
                    # Resetear para próxima aparición
                    self.estado = ESTADO_EVENT_OCULTO
        
        def guardar_estado(self):
            """Retorna el estado para guardar."""
            return {
                "estado": self.estado
            }
        
        def cargar_estado(self, datos):
            """Carga el estado desde datos guardados."""
            if datos:
                self.estado = datos.get("estado", ESTADO_EVENT_OCULTO)
    
    
    class SistemaEvents:
        """
        Gestor central del sistema de eventos.
        Maneja todos los eventos y sus modificaciones activas.
        """
        
        def __init__(self):
            self.events = {}  # Dict de todos los events por ID
            self.modificaciones_activas = {}  # {clave: {subclave: [(prioridad, valor, event_id)]}}
        
        def registrar_event(self, event):
            """Registra un evento en el sistema."""
            self.events[event.id] = event
        
        def obtener_event(self, event_id):
            """Obtiene un evento por su ID."""
            return self.events.get(event_id)
        
        def _aplicar_modificaciones(self, event):
            """Aplica las modificaciones de un evento al sistema."""
            for clave, valor in event.modificaciones.items():
                if clave not in self.modificaciones_activas:
                    self.modificaciones_activas[clave] = {}
                
                if isinstance(valor, dict):
                    # Modificación con subclaves (ej: rutinas, fondos)
                    for subclave, subvalor in valor.items():
                        if subclave not in self.modificaciones_activas[clave]:
                            self.modificaciones_activas[clave][subclave] = []
                        self.modificaciones_activas[clave][subclave].append(
                            (event.prioridad, subvalor, event.id)
                        )
                        # Ordenar por prioridad descendente
                        self.modificaciones_activas[clave][subclave].sort(
                            key=lambda x: x[0], reverse=True
                        )
                elif isinstance(valor, list):
                    # Modificación tipo lista (ej: bloqueos)
                    if "_list" not in self.modificaciones_activas[clave]:
                        self.modificaciones_activas[clave]["_list"] = []
                    for item in valor:
                        self.modificaciones_activas[clave]["_list"].append(
                            (event.prioridad, item, event.id)
                        )
                else:
                    # Modificación simple
                    if "_value" not in self.modificaciones_activas[clave]:
                        self.modificaciones_activas[clave]["_value"] = []
                    self.modificaciones_activas[clave]["_value"].append(
                        (event.prioridad, valor, event.id)
                    )
                    self.modificaciones_activas[clave]["_value"].sort(
                        key=lambda x: x[0], reverse=True
                    )
        
        def _remover_modificaciones(self, event):
            """Remueve las modificaciones de un evento."""
            for clave in list(self.modificaciones_activas.keys()):
                subdict = self.modificaciones_activas[clave]
                for subclave in list(subdict.keys()):
                    # Filtrar entradas que no sean de este evento
                    subdict[subclave] = [
                        entry for entry in subdict[subclave]
                        if entry[2] != event.id
                    ]
                    # Limpiar sublcaves vacías
                    if not subdict[subclave]:
                        del subdict[subclave]
                # Limpiar claves vacías
                if not subdict:
                    del self.modificaciones_activas[clave]
        
        def obtener_modificacion(self, clave, subclave=None):
            """
            Obtiene el valor de modificación activa con mayor prioridad.
            
            Args:
                clave: Tipo de modificación (ej: "rutinas", "fondos")
                subclave: Subclave específica (ej: "monica", "casa_living")
            
            Returns:
                El valor de la modificación con mayor prioridad, o None
            """
            if clave not in self.modificaciones_activas:
                return None
            
            subdict = self.modificaciones_activas[clave]
            
            if subclave is not None and subclave in subdict:
                entries = subdict[subclave]
                if entries:
                    return entries[0][1]  # Retornar valor de mayor prioridad
            
            # Para valores simples
            if "_value" in subdict and subdict["_value"]:
                return subdict["_value"][0][1]
            
            return None
        
        def hay_bloqueo(self, accion):
            """
            Verifica si una acción está bloqueada por algún evento.
            
            Args:
                accion: Nombre de la acción (ej: "dormir", "avanzar_tiempo")
            
            Returns:
                bool: True si la acción está bloqueada
            """
            if "bloqueos" not in self.modificaciones_activas:
                return False
            
            if "_list" in self.modificaciones_activas["bloqueos"]:
                for _, item, _ in self.modificaciones_activas["bloqueos"]["_list"]:
                    if item == accion:
                        return True
            
            return False
        
        def obtener_override_rutina(self, npc_id, dia, horario):
            """
            Obtiene override de rutina para un NPC.
            
            Args:
                npc_id: ID del NPC
                dia: Día de la semana
                horario: Índice del horario
            
            Returns:
                Locación override o None
            """
            mod = self.obtener_modificacion("rutinas", npc_id)
            if mod and isinstance(mod, dict):
                return mod.get((dia, horario))
            return None
        
        def obtener_override_fondo(self, locacion_id):
            """
            Obtiene override de fondo para una locación.
            
            Args:
                locacion_id: ID de la locación
            
            Returns:
                Ruta del fondo override o None
            """
            return self.obtener_modificacion("fondos", locacion_id)
        
        def obtener_events_visibles(self):
            """Obtiene todos los eventos visibles o activos."""
            return [e for e in self.events.values() 
                    if e.estado in [ESTADO_EVENT_VISIBLE, ESTADO_EVENT_ACTIVO]]
        
        def obtener_events_activos(self):
            """Obtiene todos los eventos activos."""
            return [e for e in self.events.values() 
                    if e.estado == ESTADO_EVENT_ACTIVO]
        
        def actualizar_todos(self):
            """Actualiza el estado de todos los eventos."""
            for event in self.events.values():
                event.actualizar()
        
        def guardar_estados(self):
            """Retorna los estados de todos los eventos para guardar."""
            estados = {}
            for event_id, event in self.events.items():
                estados[event_id] = event.guardar_estado()
            return estados
        
        def cargar_estados(self, estados):
            """Carga los estados de eventos desde datos guardados."""
            if not estados:
                return
            for event_id, datos in estados.items():
                event = self.obtener_event(event_id)
                if event:
                    event.cargar_estado(datos)
                    # Re-aplicar modificaciones si el evento está visible/activo
                    if event.estado in [ESTADO_EVENT_VISIBLE, ESTADO_EVENT_ACTIVO]:
                        if event.modificaciones:
                            self._aplicar_modificaciones(event)


# Instancia global del sistema de eventos
define sistema_events = SistemaEvents()

# Variable guardable para estados de eventos
default event_estados = {}


################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def registrar_event(event):
        """Registra un evento en el sistema."""
        sistema_events.registrar_event(event)
    
    def obtener_event(event_id):
        """Obtiene un evento por su ID."""
        return sistema_events.obtener_event(event_id)
    
    def actualizar_events():
        """Actualiza todos los eventos. Llamar en game loop."""
        sistema_events.actualizar_todos()
    
    def hay_bloqueo_event(accion):
        """Verifica si una acción está bloqueada."""
        return sistema_events.hay_bloqueo(accion)
    
    def obtener_override_rutina_event(npc_id, dia, horario):
        """Obtiene override de rutina de evento."""
        return sistema_events.obtener_override_rutina(npc_id, dia, horario)
    
    def obtener_override_fondo_event(locacion_id):
        """Obtiene override de fondo de evento."""
        return sistema_events.obtener_override_fondo(locacion_id)
    
    def guardar_eventos():
        """Guarda los estados de eventos. Llamar antes de guardar partida."""
        store.event_estados = sistema_events.guardar_estados()
    
    def cargar_eventos():
        """Carga los estados de eventos. Llamar después de cargar partida."""
        sistema_events.cargar_estados(store.event_estados)
    
    def validar_eventos():
        """
        Valida todos los eventos del juego.
        Llamar después de CADA acción del jugador (moverse, interactuar, avanzar tiempo, etc.)

        Si un evento pasa de oculto a visible, ejecuta su callback on_aparicion.
        Retorna una lista de eventos que acaban de aparecer.
        """
        # Verificar condiciones de auto-completado de quests del MC
        if hasattr(store, 'sistema_quests_mc'):
            store.sistema_quests_mc.actualizar()

        eventos_aparecieron = []

        for event in sistema_events.events.values():
            # Si el evento está oculto, verificar si debe aparecer
            if event.estado == ESTADO_EVENT_OCULTO:
                if event.verificar_aparicion():
                    event.aparecer()
                    eventos_aparecieron.append(event)

                    # Ejecutar callback de aparición si existe
                    if hasattr(event, 'on_aparicion') and event.on_aparicion:
                        try:
                            event.on_aparicion()
                        except Exception as e:
                            pass

            # Si el evento está visible, verificar si debe activarse
            elif event.estado == ESTADO_EVENT_VISIBLE:
                if event.verificar_activacion():
                    event.activar()

        return eventos_aparecieron


################################################################################
## Labels del sistema de eventos
################################################################################

# Label para ejecutar el efecto de un evento
label ejecutar_event:
    $ event = obtener_event(_event_id_temp)
    
    if event and event.label_efecto:
        jump expression event.label_efecto
    
    jump game_loop

# Label para completar el evento actual después de su efecto
label completar_event:
    $ event = obtener_event(_event_id_temp)
    
    if event:
        $ event.completar()
    
    jump game_loop
