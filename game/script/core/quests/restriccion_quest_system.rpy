################################################################################
## Sistema de Restricciones de Quest/Evento
################################################################################
## Controla qué puede hacer el jugador durante quests y eventos activos.
## Permite bloquear movimiento, acciones, interacciones NPC, celular,
## controlar visibilidad de NPCs y agregar elementos interactivos temporales.
##
## Funciona tanto para quests como para eventos — usa una variable global.

init python:

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
                     mensajes_bloqueados=False):
            """
            Args:
                locaciones_permitidas: Set/lista de IDs de locaciones permitidas (whitelist).
                                       None = todas permitidas.
                acciones_bloqueadas: Set/lista de strings de acciones bloqueadas.
                                     Extensible: "entrenar", "trabajar", "avanzar_tiempo",
                                     "dormir", "usar_item", "comprar", etc.
                mensaje_movimiento: Mensaje al intentar ir a locación no permitida.
                mensajes_acciones: Dict {accion_id: mensaje} para mensajes específicos.
                                   Si una acción está bloqueada pero no tiene mensaje
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
            self.mensajes_acciones = mensajes_acciones or {}
            
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
            Verifica si una acción está bloqueada.
            
            Returns:
                str: Mensaje de bloqueo, o None si la acción está permitida.
            """
            if not self.activa:
                return None
            if accion_id not in self.acciones_bloqueadas:
                return None
            # Buscar mensaje específico, o usar genérico
            return self.mensajes_acciones.get(accion_id, renpy.translate_string("No puedo hacer eso ahora"))
        
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
        store.restriccion_quest_activa = RestriccionQuest(**kwargs)
        

        
        return store.restriccion_quest_activa
    
    def desactivar_restriccion():
        """Desactiva la restricción actual."""
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
    
    def accion_bloqueada(accion_id):
        """
        Verifica si una acción está bloqueada por la restricción activa.

        Returns:
            str: Mensaje de bloqueo, o None si la acción está permitida.
        """
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return None
        msg = r.obtener_bloqueo_accion(accion_id)
        if msg is None:
            return None
        return renpy.translate_string(msg)
    
    def accion_bloqueada_movimiento(destino_id):
        """
        Verifica si el movimiento a una locación está bloqueado.

        Returns:
            str: Mensaje de bloqueo, o None si el movimiento está permitido.
        """
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return None
        if r.es_locacion_permitida(destino_id):
            return None
        return renpy.translate_string(r.mensaje_movimiento)
    
    def npc_esta_oculto(npc_id):
        """Verifica si un NPC está oculto por la restricción."""
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return False
        return r.es_npc_oculto(npc_id)
    
    def npc_interactuable(npc_id):
        """
        Verifica si se puede interactuar con un NPC.
        Si hay restricción activa, por defecto NINGÚN NPC es interactuable.
        """
        r = store.restriccion_quest_activa
        if r is None or not r.activa:
            return True
        return r.es_npc_interactuable(npc_id)
    
    def mensaje_npc_bloqueado():
        """Obtiene el mensaje de NPC bloqueado de la restricción activa."""
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
