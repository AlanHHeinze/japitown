################################################################################
## Sistema de Mensajes - Versión 1.0
################################################################################
## Motor principal del sistema de mensajes/chat del juego.
## Gestiona conversaciones por NPC, sistema de puntos, recompensas y galería.

init python:
    
    class Mensaje:
        """
        Mensaje individual dentro del historial de chat.
        """
        
        def __init__(self, emisor, texto, foto=None, timestamp=None):
            """
            Args:
                emisor: "jugador" o npc_id (quien envía el mensaje)
                texto: Contenido del mensaje
                foto: Ruta de imagen adjunta (o None)
                timestamp: Tupla (dia_total, horario) cuando se envió
            """
            self.emisor = emisor
            self.texto = texto
            self.foto = foto
            self.timestamp = timestamp or (
                getattr(store, 'dias_totales', 1),
                getattr(store, 'horario_actual', 0)
            )
    
    
    class OpcionRespuesta:
        """
        Opción de respuesta disponible para el jugador en un paso de conversación.
        """
        
        def __init__(self, texto, respuesta_npc, puntos=None, foto_respuesta=None,
                     condicion=None, saltar_a_paso=None):
            """
            Args:
                texto: Texto que envía el jugador
                respuesta_npc: Texto(s) de respuesta del NPC (str, list de str, o callable)
                puntos: Dict de puntos por categoría (ej: {"relacion": 2, "afinidad": -1})
                foto_respuesta: Ruta de foto adjunta a la respuesta del NPC (o None)
                condicion: Callable que retorna True/False (None = siempre visible)
                saltar_a_paso: Índice del paso al que saltar después de responder (None = paso+1, -1 = fin)
            """
            self.texto = texto
            self.respuesta_npc = respuesta_npc
            self.puntos = puntos or {}
            self.foto_respuesta = foto_respuesta
            self.condicion = condicion
            self.saltar_a_paso = saltar_a_paso
        
        def es_visible(self):
            """Retorna True si la opción es visible según su condición."""
            if self.condicion is None:
                return True
            try:
                return bool(self.condicion())
            except Exception as e:
                if config.developer:
                    print(f"[MsgSys] Error en condicion de opcion '{self.texto}': {e}")
                return False
    
    
    class PasoConversacion:
        """
        Un turno de ida y vuelta dentro de una conversación.
        NPC dice algo → jugador elige respuesta → NPC responde.
        """
        
        def __init__(self, opciones_jugador, mensaje_npc=None):
            """
            Args:
                opciones_jugador: Lista de OpcionRespuesta (2-4 opciones)
                mensaje_npc: Texto del NPC antes de las opciones (None = usar respuesta anterior)
            """
            self.mensaje_npc = mensaje_npc
            self.opciones_jugador = opciones_jugador
    
    
    class RangoRecompensa:
        """
        Define un rango de puntos y la recompensa asociada.
        """
        
        def __init__(self, min_puntos, max_puntos, recompensa):
            """
            Args:
                min_puntos: Mínimo de puntos (inclusive)
                max_puntos: Máximo de puntos (inclusive)
                recompensa: Dict con tipo y valor
                    Tipos: "relacion", "afinidad", "stat", "item", "foto", "dinero"
                    Ej: {"tipo": "relacion", "valor": 3}
                    Ej: {"tipo": "foto", "valor": "images/fotos/jasmine_01.png", "descripcion": "Selfie de Jasmine"}
                    Ej: {"tipo": "item", "valor": "regalo_jasmine", "cantidad": 1}
            """
            self.min_puntos = min_puntos
            self.max_puntos = max_puntos
            self.recompensa = recompensa
        
        def aplica(self, puntos):
            """Verifica si los puntos caen dentro de este rango."""
            return self.min_puntos <= puntos <= self.max_puntos
    
    
    class TablaRecompensas:
        """
        Tabla completa de recompensas por categoría de puntos.
        Al finalizar una conversación, se evalúa cada categoría.
        """
        
        def __init__(self, rangos_por_categoria):
            """
            Args:
                rangos_por_categoria: Dict {categoria: [RangoRecompensa, ...]}
                    Ej: {"relacion": [RangoRecompensa(1,5,{...}), ...], "afinidad": [...]}
            """
            self.rangos = rangos_por_categoria
        
        def calcular_recompensas(self, puntos_acumulados):
            """
            Calcula las recompensas según los puntos acumulados.
            
            Args:
                puntos_acumulados: Dict {categoria: total_puntos}
                
            Returns:
                Lista de dicts con recompensas a aplicar
            """
            recompensas = []
            
            for categoria, rangos in self.rangos.items():
                puntos = puntos_acumulados.get(categoria, 0)
                if puntos <= 0:
                    continue
                    
                for rango in rangos:
                    if rango.aplica(puntos):
                        recompensas.append({
                            "categoria": categoria,
                            "puntos_obtenidos": puntos,
                            "recompensa": rango.recompensa
                        })
                        break  # Solo una recompensa por categoría
            
            return recompensas
    
    
    class GrupoMensajes:
        """
        Representa una conversación completa disparada por un trigger.
        Contiene el mensaje inicial del NPC y todos los pasos de ida y vuelta.
        """
        
        def __init__(self, id, npc_id, mensaje_inicial, pasos,
                     trigger_id=None, foto_inicial=None, tabla_recompensas=None,
                     horario_respuesta=None,
                     momento_locacion=None, momento_horario=None):
            """
            Args:
                id: ID único del grupo
                npc_id: ID del NPC que envía el mensaje
                mensaje_inicial: Primer mensaje del NPC
                pasos: Lista de PasoConversacion
                trigger_id: ID del trigger que lo dispara (quest_id o event_id)
                foto_inicial: Foto adjunta al primer mensaje (o None)
                tabla_recompensas: TablaRecompensas (o None si no hay recompensas)
                horario_respuesta: Lista de horarios válidos [0,1,2] o None (siempre)
                momento_locacion: Locacion donde debe estar el NPC emisor para enviar (o None)
                momento_horario: Horario requerido para enviar: 0-3 (o None)
            """
            self.id = id
            self.npc_id = npc_id
            self.mensaje_inicial = mensaje_inicial
            self.pasos = pasos
            self.trigger_id = trigger_id
            self.foto_inicial = foto_inicial
            self.tabla_recompensas = tabla_recompensas
            self.horario_respuesta = horario_respuesta

            # Condiciones de entrega
            self.momento_locacion = momento_locacion
            self.momento_horario = momento_horario

            # Estado: pendiente / espera / en_curso / completado
            self.estado = "pendiente"
            self.paso_actual = 0
            self.puntos_acumulados = {}  # {categoria: total}
            self.recompensas_otorgadas = []  # Lista de recompensas aplicadas

        def tiene_condiciones_entrega(self):
            """Retorna True si este grupo tiene condiciones de entrega configuradas."""
            return self.momento_locacion is not None or self.momento_horario is not None
        
        def acumular_puntos(self, puntos):
            """
            Acumula puntos de una respuesta.
            
            Args:
                puntos: Dict {categoria: cantidad}
            """
            for categoria, cantidad in puntos.items():
                if categoria not in self.puntos_acumulados:
                    self.puntos_acumulados[categoria] = 0
                self.puntos_acumulados[categoria] += cantidad
        
        def avanzar_paso(self, target=None):
            """Avanza al siguiente paso o salta a uno específico.
            
            Args:
                target: Índice del paso destino (None=siguiente, -1=fin)
            Returns:
                True si hay más pasos.
            """
            if target == -1:
                self.paso_actual = len(self.pasos)
                return False
            elif target is not None:
                self.paso_actual = target
            else:
                self.paso_actual += 1
            return self.paso_actual < len(self.pasos)
        
        def obtener_paso_actual(self):
            """Retorna el PasoConversacion actual o None si terminó."""
            if self.paso_actual < len(self.pasos):
                return self.pasos[self.paso_actual]
            return None
        
        def finalizar(self):
            """
            Finaliza la conversación: calcula y aplica recompensas.
            
            Returns:
                Lista de recompensas otorgadas
            """
            self.estado = "completado"
            
            if self.tabla_recompensas:
                self.recompensas_otorgadas = self.tabla_recompensas.calcular_recompensas(
                    self.puntos_acumulados
                )
                # Aplicar recompensas
                for item in self.recompensas_otorgadas:
                    self._aplicar_recompensa(item["recompensa"])
            
            return self.recompensas_otorgadas
        
        def _aplicar_recompensa(self, recompensa):
            """Aplica una recompensa individual al juego."""
            tipo = recompensa.get("tipo", "")
            valor = recompensa.get("valor", 0)
            
            if tipo == "amor":
                npc = obtener_npc(self.npc_id)
                if npc:
                    npc.modificar_stat1(valor)

            elif tipo == "deseo":
                npc = obtener_npc(self.npc_id)
                if npc:
                    npc.modificar_stat2(valor)

            elif tipo == "relacion":
                npc = obtener_npc(self.npc_id)
                if npc:
                    npc.modificar_stat1(valor)

            elif tipo == "afinidad":
                npc = obtener_npc(self.npc_id)
                if npc:
                    npc.modificar_stat2(valor)
            
            elif tipo == "stat":
                stat_id = recompensa.get("stat_id", "")
                stat_var = f"mc_{stat_id}"
                current = getattr(store, stat_var, 0)
                setattr(store, stat_var, current + valor)
                if hasattr(store, 'notificar_cambio_stat'):
                    notificar_cambio_stat(stat_id, valor)
            
            elif tipo == "item":
                item_id = valor
                cantidad = recompensa.get("cantidad", 1)
                inventario = getattr(store, "inventario", {})
                inventario[item_id] = inventario.get(item_id, 0) + cantidad
                store.inventario = inventario
            
            elif tipo == "dinero":
                store.dinero = getattr(store, "dinero", 0) + valor
                if hasattr(store, 'notificar_cambio_stat'):
                    notificar_cambio_stat("dinero", valor)
            
            elif tipo == "foto":
                descripcion = recompensa.get("descripcion", "")
                if hasattr(store, 'sistema_mensajes'):
                    store.sistema_mensajes.agregar_foto_galeria(
                        valor, self.npc_id, descripcion
                    )
        
        def resetear(self):
            """Resetea el grupo para poder volver a jugarlo (si fuera necesario)."""
            self.estado = "pendiente"
            self.paso_actual = 0
            self.puntos_acumulados = {}
            self.recompensas_otorgadas = []
    
    
    class ChatNPC:
        """
        Historial completo de chat con un NPC.
        Almacena todos los mensajes y gestiona grupos de conversación.
        """
        
        def __init__(self, npc_id):
            self.npc_id = npc_id
            self.historial = []            # Lista de Mensaje (todo el historial)
            self.grupos_pendientes = []    # Lista de GrupoMensajes sin responder
            self.grupo_activo = None       # GrupoMensajes en curso (o None)
            self.mensajes_sin_leer = 0
            self.bloqueado = False         # Si True, el NPC no puede responder
        
        def agregar_mensaje(self, emisor, texto, foto=None):
            """Agrega un mensaje al historial."""
            msg = Mensaje(emisor, texto, foto)
            self.historial.append(msg)
            
            if emisor != "jugador":
                self.mensajes_sin_leer += 1
            
            return msg
        
        def marcar_como_leido(self):
            """Marca todos los mensajes como leídos."""
            self.mensajes_sin_leer = 0
        
        def obtener_ultimo_mensaje(self):
            """Retorna el último mensaje o None."""
            if self.historial:
                return self.historial[-1]
            return None
        
        def tiene_pendientes(self):
            """Verifica si hay grupos pendientes o un grupo activo."""
            return len(self.grupos_pendientes) > 0 or self.grupo_activo is not None
        
        def _horario_valido(self, grupo):
            """Verifica si el horario actual permite responder a este grupo."""
            hr = getattr(grupo, 'horario_respuesta', None)
            if hr is None:
                return True
            return getattr(store, 'horario_actual', 0) in hr

        def puede_responder(self):
            """Verifica si el jugador puede responder algo."""
            if getattr(self, 'bloqueado', False):
                return False
            # Tiene grupo activo con paso disponible y horario válido
            if self.grupo_activo and self.grupo_activo.obtener_paso_actual():
                return self._horario_valido(self.grupo_activo)
            # Tiene grupos pendientes con horario válido
            for grupo in self.grupos_pendientes:
                if self._horario_valido(grupo):
                    return True
            return False
    
    
    class SistemaMensajes:
        """
        Gestor central del sistema de mensajes.
        Maneja todos los chats por NPC, disparadores, y galería de fotos.
        """
        
        def __init__(self):
            self.chats = {}    # {npc_id: ChatNPC}
            self.galeria = []  # Lista de {"ruta": str, "npc_id": str, "descripcion": str}
            self._grupos_registrados = {}  # {trigger_id: GrupoMensajes} para lookup rápido
            self._todos_grupos = {}  # {grupo_id: GrupoMensajes}
            self._grupos_en_espera = []  # GrupoMensajes esperando condiciones de entrega
        
        def inicializar_chat(self, npc_id):
            """Crea un ChatNPC para un NPC si no existe."""
            if npc_id not in self.chats:
                self.chats[npc_id] = ChatNPC(npc_id)
        
        def registrar_grupo(self, npc_id, grupo):
            """
            Registra un GrupoMensajes para ser disparado posteriormente.
            
            Args:
                npc_id: ID del NPC
                grupo: GrupoMensajes a registrar
            """
            self._todos_grupos[grupo.id] = grupo
            if grupo.trigger_id:
                self._grupos_registrados[grupo.trigger_id] = grupo
        
        def disparar_por_trigger(self, tipo_trigger, trigger_id, npc_id):
            """
            Busca y activa un GrupoMensajes asociado a un trigger.
            Si el grupo tiene condiciones de entrega, lo pone en espera.

            Args:
                tipo_trigger: "quest" o "event" (informativo)
                trigger_id: ID del trigger (quest_id o event_id)
                npc_id: ID del NPC (fallback si no está en el grupo)
            """
            grupo = self._grupos_registrados.get(trigger_id)
            if not grupo:
                return False

            # Verificar que no esté ya disparado
            if grupo.estado != "pendiente":
                return False

            target_npc = grupo.npc_id or npc_id
            self.inicializar_chat(target_npc)

            # Si tiene condiciones de entrega, poner en espera
            if grupo.tiene_condiciones_entrega():
                grupo.estado = "espera"
                if not hasattr(self, '_grupos_en_espera'):
                    self._grupos_en_espera = []
                self._grupos_en_espera.append(grupo)
                # Intentar entrega inmediata por si las condiciones ya se cumplen
                self._intentar_entrega(grupo)
                return True

            # Sin condiciones: entrega inmediata (comportamiento original)
            self._entregar_grupo(grupo, target_npc)
            return True

        def _entregar_grupo(self, grupo, target_npc=None):
            """
            Entrega un grupo al historial del chat.
            Se llama cuando las condiciones se cumplen o no hay condiciones.
            """
            target_npc = target_npc or grupo.npc_id
            self.inicializar_chat(target_npc)
            chat = self.chats[target_npc]

            # Agregar mensaje inicial al historial
            chat.agregar_mensaje(
                target_npc,
                grupo.mensaje_inicial,
                grupo.foto_inicial
            )

            # Si la foto inicial existe, agregarla a la galería
            if grupo.foto_inicial:
                self.agregar_foto_galeria(
                    grupo.foto_inicial, target_npc,
                    "Foto de {}".format(target_npc.capitalize())
                )

            # Agregar a pendientes del chat
            chat.grupos_pendientes.append(grupo)

            # Restaurar estado para que seleccionar_grupo lo pase a en_curso
            if grupo.estado == "espera":
                grupo.estado = "pendiente"

            # Remover de la lista de espera
            if hasattr(self, '_grupos_en_espera') and grupo in self._grupos_en_espera:
                self._grupos_en_espera.remove(grupo)

        def _intentar_entrega(self, grupo):
            """
            Verifica las 3 condiciones de entrega para un grupo en espera.
            Si se cumplen todas, entrega el grupo.

            Returns:
                True si fue entregado, False si sigue en espera.
            """
            if grupo.estado != "espera":
                return False

            target_npc = grupo.npc_id

            # Condicion 3: Bloqueo global de mensajes
            if mensajes_estan_bloqueados():
                return False

            # Condicion 1: Momento (locacion + horario del NPC emisor)
            npc = obtener_npc(target_npc)
            if not npc:
                return False

            if grupo.momento_locacion is not None:
                if npc.locacion_actual != grupo.momento_locacion:
                    return False

            if grupo.momento_horario is not None:
                if getattr(store, 'horario_actual', 0) != grupo.momento_horario:
                    return False

            # Condicion 2: NPC emisor NO comparte locacion con el MC
            if npc.locacion_actual:
                loc_mc = None
                if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
                    loc_mc = store.sistema_locaciones.locacion_actual.id
                if loc_mc and npc.locacion_actual == loc_mc:
                    return False

            # Todas las condiciones cumplidas: entregar
            self._entregar_grupo(grupo, target_npc)
            return True

        def verificar_mensajes_en_espera(self):
            """
            Revisa todos los grupos en espera e intenta entregarlos.
            Se llama al avanzar horario, al cambiar de locacion, y al dormir.
            """
            if not hasattr(self, '_grupos_en_espera'):
                self._grupos_en_espera = []
                return
            if not self._grupos_en_espera:
                return

            for grupo in list(self._grupos_en_espera):
                self._intentar_entrega(grupo)
        
        def seleccionar_grupo(self, npc_id, grupo_id):
            """
            El jugador selecciona un grupo pendiente para empezar a responder.
            
            Args:
                npc_id: ID del NPC
                grupo_id: ID del GrupoMensajes a seleccionar
            """
            chat = self.chats.get(npc_id)
            if not chat:
                return False
            
            # Buscar el grupo en pendientes
            grupo = None
            for g in chat.grupos_pendientes:
                if g.id == grupo_id:
                    grupo = g
                    break
            
            if not grupo:
                return False
            
            # Mover de pendientes a activo
            chat.grupos_pendientes.remove(grupo)
            chat.grupo_activo = grupo
            grupo.estado = "en_curso"
            
            # Si el primer paso tiene mensaje_npc, agregarlo al historial
            paso = grupo.obtener_paso_actual()
            if paso and paso.mensaje_npc:
                chat.agregar_mensaje(npc_id, paso.mensaje_npc)
            
            return True
        
        def responder(self, npc_id, opcion_idx):
            """
            El jugador envía una respuesta.
            
            Args:
                npc_id: ID del NPC
                opcion_idx: Índice de la opción elegida
                
            Returns:
                Dict con resultado: {"exito": bool, "respuesta_npc": str, 
                "foto": str/None, "finalizado": bool, "recompensas": list}
            """
            chat = self.chats.get(npc_id)
            if not chat or not chat.grupo_activo:
                return {"exito": False}
            
            grupo = chat.grupo_activo
            paso = grupo.obtener_paso_actual()
            
            if not paso or opcion_idx >= len(paso.opciones_jugador):
                return {"exito": False}
            
            opcion = paso.opciones_jugador[opcion_idx]
            
            # Agregar mensaje del jugador al historial
            chat.agregar_mensaje("jugador", opcion.texto)
            
            # Acumular puntos
            grupo.acumular_puntos(opcion.puntos)
            
            # Obtener respuesta del NPC (puede ser str, list, o callable)
            respuesta_raw = opcion.respuesta_npc
            if callable(respuesta_raw):
                respuesta_raw = respuesta_raw()
            
            # Normalizar a lista
            if isinstance(respuesta_raw, list):
                respuestas_lista = respuesta_raw
            else:
                respuestas_lista = [respuesta_raw] if respuesta_raw else []
            
            # Resultado base
            resultado = {
                "exito": True,
                "respuestas_npc": respuestas_lista,
                "foto": opcion.foto_respuesta,
                "finalizado": False,
                "recompensas": [],
                "saltar_a_paso": opcion.saltar_a_paso
            }
            
            # Si hay foto en la respuesta, agregar a galería
            if opcion.foto_respuesta:
                self.agregar_foto_galeria(
                    opcion.foto_respuesta, npc_id,
                    f"Foto de {npc_id.capitalize()}"
                )
            
            # Avanzar al siguiente paso (con posible salto)
            hay_mas = grupo.avanzar_paso(opcion.saltar_a_paso)
            
            if hay_mas:
                # Hay más pasos, preparar el siguiente
                siguiente_paso = grupo.obtener_paso_actual()
                if siguiente_paso and siguiente_paso.mensaje_npc:
                    resultado["mensaje_siguiente"] = siguiente_paso.mensaje_npc
            else:
                # Conversación terminada
                resultado["finalizado"] = True
                resultado["recompensas"] = grupo.finalizar()
                resultado["puntos_totales"] = grupo.puntos_acumulados.copy()
                chat.grupo_activo = None
            
            return resultado
        
        def obtener_pendientes_total(self):
            """Total de mensajes sin leer en todos los chats."""
            total = 0
            for chat in self.chats.values():
                total += chat.mensajes_sin_leer
            return total
        
        def obtener_pendientes_npc(self, npc_id):
            """Mensajes sin leer de un NPC específico."""
            chat = self.chats.get(npc_id)
            if chat:
                return chat.mensajes_sin_leer
            return 0
        
        def grupo_completado(self, grupo_id):
            """Verifica si un grupo de mensajes está completado."""
            grupo = self._todos_grupos.get(grupo_id)
            if grupo:
                return grupo.estado == "completado"
            return False
        
        def agregar_foto_galeria(self, ruta, npc_id, descripcion=""):
            """
            Agrega una foto a la galería.
            Evita duplicados por ruta.
            """
            # Verificar duplicado
            for foto in self.galeria:
                if foto["ruta"] == ruta:
                    return False
            
            self.galeria.append({
                "ruta": ruta,
                "npc_id": npc_id,
                "descripcion": descripcion
            })
            return True
        
        def obtener_galeria(self, npc_filtro=None):
            """
            Obtiene las fotos de la galería, opcionalmente filtradas por NPC.
            
            Args:
                npc_filtro: ID del NPC para filtrar (None = todas)
            """
            if npc_filtro:
                return [f for f in self.galeria if f["npc_id"] == npc_filtro]
            return self.galeria


# =============================================================================
# Variables guardables
# =============================================================================

define sistema_mensajes = SistemaMensajes()


# =============================================================================
# Contactos especiales (no-NPC)
# =============================================================================

init python:

    CONTACTOS_ESPECIALES = {
        "libre_mercado": {"nombre": "Libre Mercado", "icono": "🛒"},
    }

    def obtener_nombre_contacto(contacto_id):
        """Obtiene el nombre para mostrar de un contacto (NPC o especial)."""
        npc = obtener_npc(contacto_id)
        if npc:
            return renpy.translate_string(npc.nombre)
        nombre = CONTACTOS_ESPECIALES.get(contacto_id, {}).get("nombre", contacto_id.replace("_", " ").title())
        return renpy.translate_string(nombre)

# =============================================================================
# Funciones de utilidad
# =============================================================================

init python:

    def inicializar_chats():
        """Inicializa los chats para todos los NPCs del juego."""
        sistema_mensajes.inicializar_chat("jasmine")
        sistema_mensajes.inicializar_chat("monica")
        sistema_mensajes.inicializar_chat("violet")
    
    def disparar_mensaje(trigger_id, npc_id):
        """
        Dispara un mensaje desde cualquier parte del juego.
        
        Args:
            trigger_id: ID del trigger (quest_id, event_id, etc.)
            npc_id: ID del NPC que envía el mensaje
        """
        sistema_mensajes.disparar_por_trigger("manual", trigger_id, npc_id)
    
    def mensaje_completado(grupo_id):
        """
        Verifica si una conversación de mensajes está completada.
        Para usar en Requisitos de quests.

        Args:
            grupo_id: ID del GrupoMensajes

        Returns:
            bool: True si el grupo está completado
        """
        return sistema_mensajes.grupo_completado(grupo_id)

    def bloquear_chat_npc(npc_id):
        """Bloquea el chat de un NPC (no podrá responder hasta desbloquear)."""
        sistema_mensajes.inicializar_chat(npc_id)
        chat = sistema_mensajes.chats.get(npc_id)
        if chat:
            chat.bloqueado = True

    def desbloquear_chat_npc(npc_id):
        """Desbloquea el chat de un NPC."""
        chat = sistema_mensajes.chats.get(npc_id)
        if chat:
            chat.bloqueado = False
