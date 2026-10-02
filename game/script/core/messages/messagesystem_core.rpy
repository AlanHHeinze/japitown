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
    
    
    def mensaje_partes(texto):
        """
        Normaliza el texto de un mensaje a una LISTA de burbujas.

        Acepta las tres formas con las que el contenido puede declarar un
        mensaje: un str (una burbuja), una lista de str (varias seguidas) o un
        callable que devuelve cualquiera de las dos.

        Lo usan los tres lugares que tocan estos textos —el historial del chat,
        el selector de respuesta y el preview de un grupo pendiente—, asi que
        agregar la forma de lista se hizo una sola vez y en un solo lado.

        Returns:
            list[str] — sin los elementos vacios.
        """
        if callable(texto):
            texto = texto()
        if texto is None:
            return []
        if not isinstance(texto, list):
            texto = [texto]
        return [_p for _p in texto if _p]


    class OpcionRespuesta:
        """
        Opción de respuesta disponible para el jugador en un paso de conversacion.
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
                saltar_a_paso: Índice del paso al que saltar despues de responder (None = paso+1, -1 = fin)
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
        Un turno de ida y vuelta dentro de una conversacion.
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
                    Tipos: "amor", "deseo", "stat", "item", "foto", "dinero"
                    Ej: {"tipo": "amor", "valor": 3}
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
        Al finalizar una conversacion, se evalúa cada categoría.
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
        Representa una conversacion completa disparada por un trigger.
        Contiene el mensaje inicial del NPC y todos los pasos de ida y vuelta.
        """
        
        def __init__(self, id, npc_id, mensaje_inicial, pasos,
                trigger_id=None, foto_inicial=None, tabla_recompensas=None,
                horario_respuesta=None,
                momento_locacion=None, momento_horario=None,
                condicion_entrega=None, accion_al_completar=None,
                prioritario=False):
            """
            Args:
                id: ID único del grupo
                npc_id: ID del NPC que envía el mensaje
                mensaje_inicial: Primer mensaje del NPC (None o "" = no muestra
                    mensaje inicial). Acepta str o LISTA de str; una lista sale
                    como varias burbujas seguidas, igual que respuesta_npc.
                pasos: Lista de PasoConversacion
                trigger_id: ID del trigger que lo dispara (quest_id o event_id)
                foto_inicial: Foto adjunta al primer mensaje (o None)
                tabla_recompensas: TablaRecompensas (o None si no hay recompensas)
                horario_respuesta: Lista de horarios válidos [0,1,2] o None (siempre)
                momento_locacion: Locacion donde debe estar el NPC emisor para enviar (o None)
                momento_horario: Horario requerido para enviar: 0-3 (o None)
                condicion_entrega: Callable () -> bool extra para entrega (ej: horario laboral)
                accion_al_completar: Callable () -> None que se ejecuta al finalizar el grupo
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
            self.condicion_entrega = condicion_entrega
            self.accion_al_completar = accion_al_completar
            self.prioritario = prioritario

            # Estado: pendiente / espera / en_curso / completado
            self.estado = "pendiente"
            # "Este grupo ya fue disparado por su trigger". Va aparte del estado
            # porque _entregar_grupo devuelve el estado a "pendiente" y si no
            # el trigger lo re-entregaria (ver disparar_por_trigger).
            # Los grupos repetibles lo bajan junto con el estado.
            self._disparado = False
            self.paso_actual = 0
            self.puntos_acumulados = {}  # {categoria: total}
            self.recompensas_otorgadas = []  # Lista de recompensas aplicadas

        def tiene_condiciones_entrega(self):
            """Retorna True si este grupo tiene condiciones de entrega configuradas."""
            return (self.momento_locacion is not None
                    or self.momento_horario is not None
                    or self.condicion_entrega is not None)
        
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
            Finaliza la conversacion: calcula recompensas y ejecuta accion_al_completar.

            Returns:
                Lista de recompensas otorgadas
            """
            self.estado = "completado"

            # Terminar una conversacion cuenta como contacto con ese NPC.
            if hasattr(store, 'marcar_contacto_npc'):
                store.marcar_contacto_npc(self.npc_id)

            if self.tabla_recompensas:
                self.recompensas_otorgadas = self.tabla_recompensas.calcular_recompensas(
                    self.puntos_acumulados
                )
                for item in self.recompensas_otorgadas:
                    self._aplicar_recompensa(item["recompensa"])

            if self.accion_al_completar:
                try:
                    self.accion_al_completar()
                except Exception as _e:
                    if renpy.config.developer:
                        print("[MsgSys] Error en accion_al_completar de {}: {}".format(self.id, _e))

            # Revalidar las quests ACÁ mismo: muchas tienen un Requisito("mensaje")
            # que se cumple justo ahora. El game_loop también las revalida, pero
            # solo corre al cerrar el celular — y la app de Pistas está DENTRO del
            # celular, así que sin esto la pista seguiría desactualizada mientras
            # el jugador no salga. Es seguro: las accion_al_entrar de las etapas
            # solo setean flags/restricciones, no saltan labels.
            try:
                store.actualizar_quests()
            except Exception:
                pass

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

            elif tipo == "amor":
                npc = obtener_npc(self.npc_id)
                if npc:
                    npc.modificar_stat1(valor)

            elif tipo == "deseo":
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
                if hasattr(store, 'notificar_item_obtenido'):
                    notificar_item_obtenido(item_id)
            
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
        
        def reiniciar_progreso(self):
            """
            Deja el grupo listo para jugarse desde el primer paso.

            NO toca `estado` ni `_disparado`: eso es de resetear(), que es para
            volver a DISPARARLO. Esto es para volver a JUGARLO, y lo llama
            _entregar_grupo en cada entrega.

            POR QUE EXISTE: los grupos se registran una vez y se reusan. Al
            terminar una conversacion, avanzar_paso(-1) deja `paso_actual` en
            len(pasos). Si el grupo se vuelve a entregar sin pasar por aca,
            arranca ya terminado: obtener_paso_actual() devuelve None, no hay
            opciones para contestar, y si el grupo bloquea algo (prioritario,
            Mensajear) el jugador queda trabado sin salida. Paso con la
            conversacion generica de Mensajear, que es repetible y volvia a
            "pendiente" a mano sin reiniciar el paso (dos reportes de jugadores,
            2026-09-10).
            """
            self.paso_actual = 0
            self.puntos_acumulados = {}
            self.recompensas_otorgadas = []

        def resetear(self):
            """Resetea el grupo para poder volver a dispararlo y jugarlo."""
            self.estado = "pendiente"
            # Sin esto el trigger no lo volveria a disparar nunca.
            self._disparado = False
            self.reiniciar_progreso()
    
    
    class ChatNPC:
        """
        Historial completo de chat con un NPC.
        Almacena todos los mensajes y gestiona grupos de conversacion.
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
            """
            Verifica si el jugador puede responder algo.

            Es tambien la condicion de los bloqueos que dependen de contestar
            (prioritario, Mensajear): si esto da False, no bloquean. Por eso
            mira TODO lo que impide llegar a la respuesta, incluido el celular:
            un mensaje que no se puede abrir no puede exigir que se conteste.
            """
            if getattr(self, 'bloqueado', False):
                return False
            # NPC fuera de juego: no contesta nada
            # (core/npcs/npc_disponibilidad.rpy).
            if not npc_disponible(self.npc_id):
                return False
            # Celular bloqueado por una restriccion: no hay forma de llegar al
            # chat, asi que tampoco hay forma de que el mensaje bloquee.
            if celular_esta_bloqueado():
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
            self._grupos_registrados = {}  # {trigger_id: GrupoMensajes} para lookup rapido
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
        
        def disparar_por_trigger(self, tipo_trigger, trigger_id, npc_id, quest_id=None):
            """
            Busca y activa un GrupoMensajes asociado a un trigger.
            Si el grupo tiene condiciones de entrega, lo pone en espera.

            Args:
                tipo_trigger: "quest" o "event" (informativo)
                trigger_id: ID del trigger (quest_id o event_id)
                npc_id: ID del NPC (fallback si no está en el grupo)
                quest_id: quest cuyo DISPARADOR es este chat (lo pasa
                    Quest._ejecutar_entrada_etapa). Queda en el grupo y, cuando
                    el jugador lo abre, seleccionar_grupo pasa por
                    activar_quest — el punto de activacion, igual que apretar
                    el boton de esa quest.
            """
            grupo = self._grupos_registrados.get(trigger_id)
            if not grupo:
                return False
            if quest_id:
                grupo.quest_id = quest_id

            # Verificar que no esté ya disparado.
            #
            # NO alcanza con mirar `estado`: _entregar_grupo devuelve el grupo a
            # "pendiente" a proposito, para que seleccionar_grupo lo pueda pasar
            # a "en_curso". O sea que un grupo YA entregado vuelve a verse como
            # "sin disparar", y cualquier llamador que insista lo re-entrega.
            #
            # Con un trigger que corre en CADA vuelta del game_loop (violet
            # amor 15) eso lo re-entregaba una vez por accion del jugador, con
            # dos efectos encadenados:
            #   1. El mensaje inicial se agregaba al historial N veces — el
            #      duplicado que se ve en el chat.
            #   2. El grupo quedaba N veces en chat.grupos_pendientes. Como
            #      seleccionar_grupo saca UNA sola copia, al reabrir el chat
            #      pisaba el "completado" con "en_curso", y toda quest que
            #      esperara ese grupo (Requisito "mensaje") se trababa para
            #      siempre.
            #
            # Por eso la marca va aparte del estado.
            if getattr(grupo, '_disparado', False):
                return False

            if grupo.estado != "pendiente":
                return False

            grupo._disparado = True

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

            # Sin condiciones de entrega — pero NO sin la etapa previa. Si hoy
            # no se puede contestar, va a espera igual que los otros y se
            # entrega cuando se pueda. Entregarlo igual dejaba el grupo activo
            # y sin respuesta posible: con los prioritarios eso bloqueaba dormir
            # y avanzar sin forma de destrabarlo.
            if not self._puede_entregarse(grupo):
                grupo.estado = "espera"
                if not hasattr(self, '_grupos_en_espera'):
                    self._grupos_en_espera = []
                self._grupos_en_espera.append(grupo)
                return True

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

            # Agregar mensaje inicial al historial (omitir si está vacío — el
            # jugador inicia).
            #
            # Acepta str o LISTA de str, igual que respuesta_npc: una lista sale
            # como varias burbujas seguidas. La foto va con la primera, que es
            # el mismo criterio que usa _finalizar_escribiendo del lado de la UI.
            _foto_pendiente = grupo.foto_inicial
            for _texto_ini in mensaje_partes(grupo.mensaje_inicial):
                chat.agregar_mensaje(target_npc, _texto_ini, _foto_pendiente)
                _foto_pendiente = None

            # Si la foto inicial existe, agregarla a la galería
            if grupo.foto_inicial:
                self.agregar_foto_galeria(
                    grupo.foto_inicial, target_npc,
                    renpy.translate_string("Foto de {npc}").format(npc=target_npc.capitalize())
                )

            # Grupo INFORMATIVO (sin pasos): es un aviso que no se responde.
            # Se da por completado apenas se entrega, en vez de mandarlo a
            # pendientes. Si entrara a pendientes quedaria trabado: la UI solo
            # dibuja opciones si hay paso, y un grupo solo se completa desde
            # responder(), que sin opciones nunca se llama — o sea, badge de
            # "sin responder" para siempre y un grupo_activo que no se cierra.
            if not grupo.pasos:
                grupo.finalizar()
                if hasattr(self, '_grupos_en_espera') and grupo in self._grupos_en_espera:
                    self._grupos_en_espera.remove(grupo)
                return

            # CADA ENTREGA ES UNA PARTIDA NUEVA del grupo: el objeto es el
            # mismo de siempre (se registra una vez), asi que trae el paso y
            # los puntos de la ultima vez que se jugo. Sin esto un grupo
            # repetible arranca en el paso final, sin opciones — ver
            # reiniciar_progreso.
            grupo.reiniciar_progreso()

            # Agregar a pendientes del chat.
            #
            # El `not in` es una segunda red: seleccionar_grupo saca UNA sola
            # copia de la lista, asi que un grupo repetido queda ahi como
            # pendiente fantasma y al reabrirlo pisa su propio "completado".
            # La primera red es la marca _disparado de disparar_por_trigger.
            if grupo not in chat.grupos_pendientes:
                chat.grupos_pendientes.append(grupo)

            # Restaurar estado para que seleccionar_grupo lo pase a en_curso
            if grupo.estado == "espera":
                grupo.estado = "pendiente"

            # Remover de la lista de espera
            if hasattr(self, '_grupos_en_espera') and grupo in self._grupos_en_espera:
                self._grupos_en_espera.remove(grupo)

        def _puede_entregarse(self, grupo):
            """
            LA ETAPA PREVIA A LA ENTREGA: ¿si este grupo se entrega ahora, el
            jugador va a poder contestarlo?

            Si la respuesta es no, el grupo NO se entrega — se queda en espera
            y se reintenta en cada vuelta del game_loop. Es lo que impide que
            un mensaje que bloquea el avance (prioritario, Mensajear) entre en
            un estado del que el jugador no puede salir.

            Va en un solo lugar y la consultan los DOS caminos de entrega: el
            de los grupos con condiciones (_intentar_entrega) y el atajo de
            los que no las tienen (disparar_por_trigger). Antes el atajo la
            salteaba entera, asi que un grupo sin condiciones se entregaba
            aunque el NPC estuviera fuera de juego, y despues no se podia
            contestar.

            Chequea lo mismo que ChatNPC.puede_responder(), que es el otro lado
            del contrato: lo que se entrega tiene que poder responderse.
            """
            # NPC fuera de juego: no manda mensajes nuevos. El grupo se queda
            # en espera y se entrega cuando vuelva
            # (core/npcs/npc_disponibilidad.rpy).
            if not npc_disponible(grupo.npc_id):
                return False

            if mensajes_estan_bloqueados():
                return False

            # MC reservado por una quest (planificador): un PRIORITARIO ajeno
            # no entra en el medio — un prioritario bloquea dormir y avanzar,
            # o sea que le pisa la noche a la quest que la reservo. El grupo se
            # queda en espera y se reintenta cuando la reserva vence.
            #
            # Solo los prioritarios: uno normal no traba nada, y cuanto mas
            # chico el radio del bloqueo, mejor (ver S15/E10 — un bloqueo que
            # tapa de mas es como se hacen los soft locks).
            if getattr(grupo, "prioritario", False):
                _res_mc = planificador_mc_reservado_por()
                if _res_mc is not None and getattr(grupo, "quest_id", None) != _res_mc:
                    return False

            # Un grupo con pasos tiene que poder arrancar del primero. Con
            # reiniciar_progreso() en la entrega esto no falla nunca; queda
            # como cinturon por si alguien lo saltea.
            if grupo.pasos and not grupo.pasos[0].opciones_jugador:
                return False

            return True

        def _intentar_entrega(self, grupo):
            """
            Verifica las condiciones de entrega para un grupo en espera.
            Soporta NPCs normales y contactos especiales (sin NPC en sistema_npcs).

            Returns:
                True si fue entregado, False si sigue en espera.
            """
            if grupo.estado != "espera":
                return False

            target_npc = grupo.npc_id

            if not self._puede_entregarse(grupo):
                return False

            # Condición personalizada (horario laboral, saldo, etc.)
            if grupo.condicion_entrega is not None:
                try:
                    if not grupo.condicion_entrega():
                        return False
                except Exception:
                    return False

            npc = obtener_npc(target_npc)
            if npc:
                # NPC real: verificar locación, horario y co-locación con el MC
                if grupo.momento_locacion is not None:
                    if npc.locacion_actual != grupo.momento_locacion:
                        return False
                if grupo.momento_horario is not None:
                    if getattr(store, 'horario_actual', 0) != grupo.momento_horario:
                        return False
                if npc.locacion_actual:
                    loc_mc = None
                    if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
                        loc_mc = store.sistema_locaciones.locacion_actual.id
                    if loc_mc and npc.locacion_actual == loc_mc:
                        return False
            else:
                # Contacto especial (sin NPC): solo se verifica momento_horario
                if grupo.momento_horario is not None:
                    if getattr(store, 'horario_actual', 0) != grupo.momento_horario:
                        return False

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

        def verificar_mensajes_horarios_omitidos(self, horario_desde):
            """
            Al dormir, simula los horarios omitidos para entregar mensajes que
            debían llegar esa noche. Debe llamarse DESPUÉS de actualizar_quests()
            (para que los grupos ya estén en espera) y con horario ya en 0.

            horario_desde: horario en el que el jugador se durmió (0-3)
            """
            if not hasattr(self, '_grupos_en_espera') or not self._grupos_en_espera:
                return
            if mensajes_estan_bloqueados():
                return

            # Horarios a simular: desde el horario en que durmió (inclusive) hasta
            # trasnoche. Se incluye el propio horario_desde porque un mensaje puede
            # haberse puesto en espera recién durante este dormir() (vía
            # actualizar_quests, que avanza una quest a BOTON_LISTO y dispara su
            # mensaje). Si ese mensaje es para el mismo horario en que el jugador se
            # durmió, excluirlo haría que nunca se entregue esa noche.
            horarios_omitidos = list(range(horario_desde, 4))
            if not horarios_omitidos:
                return

            horario_original = store.horario_actual
            try:
                for horario in horarios_omitidos:
                    if not self._grupos_en_espera:
                        break
                    store.horario_actual = horario
                    # Actualizar posiciones de NPCs para este horario simulado
                    if hasattr(store, 'actualizar_rutinas_npcs'):
                        store.actualizar_rutinas_npcs()
                    for grupo in list(self._grupos_en_espera):
                        # Los prioritarios NO se entregan mientras el jugador duerme:
                        # por definicion no se pueden "dormir de largo". O lo despiertan
                        # (obtener_horario_despertar_prioritario, antes de dormir) o
                        # esperan a que el horario real llegue estando despierto.
                        # Sin esto, una quest que recien habilita su mensaje al cambiar
                        # el dia (dias_espera) lo dispara dentro de dormir() y se
                        # entregaba en el trasnoche simulado, sin despertar ni bloquear.
                        if getattr(grupo, 'prioritario', False):
                            continue
                        self._intentar_entrega(grupo)
            finally:
                store.horario_actual = horario_original
                # Restaurar posiciones de NPCs al horario real (mañana)
                if hasattr(store, 'actualizar_rutinas_npcs'):
                    store.actualizar_rutinas_npcs()
        
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

            # Punto de activacion: abrir el chat que dispara una quest es
            # "apretar el boton" de esa quest (ver disparar_por_trigger).
            activar_quest(getattr(grupo, "quest_id", None), origen="chat:" + grupo.id)
            
            # Si el primer paso tiene mensaje_npc, agregarlo al historial
            paso = grupo.obtener_paso_actual()
            if paso and paso.mensaje_npc:
                msg_npc = paso.mensaje_npc() if callable(paso.mensaje_npc) else paso.mensaje_npc
                chat.agregar_mensaje(npc_id, msg_npc)

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
            
            # Agregar mensaje(s) del jugador al historial. `texto` acepta str,
            # lista o callable: una lista sale como varias burbujas seguidas,
            # igual que del lado del NPC.
            for _texto_jugador in mensaje_partes(opcion.texto):
                chat.agregar_mensaje("jugador", _texto_jugador)
            
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
                    renpy.translate_string("Foto de {npc}").format(npc=npc_id.capitalize())
                )
            
            # Avanzar al siguiente paso (con posible salto)
            hay_mas = grupo.avanzar_paso(opcion.saltar_a_paso)
            
            if hay_mas:
                # Hay más pasos, preparar el siguiente (mensaje_npc puede ser callable)
                siguiente_paso = grupo.obtener_paso_actual()
                if siguiente_paso and siguiente_paso.mensaje_npc:
                    msg_sig = siguiente_paso.mensaje_npc() if callable(siguiente_paso.mensaje_npc) else siguiente_paso.mensaje_npc
                    resultado["mensaje_siguiente"] = msg_sig
            else:
                # Conversacion terminada
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

# Instancia creada en init 4 (los registros de init 5-11 la llenan) y declarada
# con default para que se guarde en el save: historiales de chat y galeria de fotos deben guardarse.
init 4 python:
    sistema_mensajes = SistemaMensajes()
# OJO: el default se re-evalúa en CADA partida nueva. Debe devolver una COPIA
# del catálogo poblado en init — una instancia vacía (SistemaMensajes()) borraría todo
# el contenido registrado. Ver _ps_copia_fresca en persistencia_sistemas.rpy.
default sistema_mensajes = _ps_copia_fresca("sistema_mensajes")


# =============================================================================
# Contactos especiales (no-NPC)
# =============================================================================

init python:

    CONTACTOS_ESPECIALES = {
        "libre_mercado": {"nombre": "Libre Mercado", "icono": "🛒"},
        "tienda_coxplay": {"nombre": "Tienda CoXplay", "icono": "🛍️"},
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

        # Tienda CoXplay — mensaje de bienvenida presente desde el inicio del juego
        sistema_mensajes.inicializar_chat("tienda_coxplay")
        if not sistema_mensajes.chats["tienda_coxplay"].historial:
            sistema_mensajes.chats["tienda_coxplay"].agregar_mensaje(
                "tienda_coxplay",
                "Gracias por su compra en Coxplay, para futuras compras y consultas puede usar este canal"
            )
            # El mensaje de bienvenida no bloquea la lectura como pendiente
            sistema_mensajes.chats["tienda_coxplay"].mensajes_sin_leer = 0
    
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
        Verifica si una conversacion de mensajes está completada.
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

    # Grupos que ya avisaron por consola que no se pueden contestar. Es solo
    # para no repetir el aviso en cada vuelta del loop.
    _BLOQUEO_AVISADOS = set()

    def obtener_bloqueo_mensaje_prioritario():
        """
        Verifica si hay algun mensaje prioritario ya entregado esperando respuesta.
        Retorna el nombre del NPC remitente, o None si no hay bloqueo.
        Un mensaje prioritario bloquea avanzar tiempo y dormir hasta ser respondido.

        REGLA: UN BLOQUEO SOLO LO PUEDE SOSTENER ALGO QUE EL JUGADOR PUEDA
        RESOLVER. Si el chat no se puede contestar ahora (NPC fuera de juego,
        grupo sin paso valido, horario de respuesta que no es este), el
        mensaje no bloquea: el jugador sigue jugando y el bloqueo vuelve solo
        cuando se pueda contestar. Es la red de seguridad de _puede_entregarse
        — lo que se escape de la etapa previa no puede trabar la partida.

        En desarrollo se avisa por consola, una vez por grupo, para que el
        caso no quede escondido: que no trabe no significa que este bien.
        """
        for npc_id, chat in sistema_mensajes.chats.items():
            if not chat.puede_responder():
                _pend = [g.id for g in chat.grupos_pendientes
                         if getattr(g, 'prioritario', False)]
                if chat.grupo_activo and getattr(chat.grupo_activo, 'prioritario', False):
                    _pend.append(chat.grupo_activo.id)
                if _pend and config.developer:
                    for _gid in _pend:
                        if _gid not in _BLOQUEO_AVISADOS:
                            _BLOQUEO_AVISADOS.add(_gid)
                            print("[Mensajes] prioritario '%s' de %s no se puede "
                                  "contestar ahora: no bloquea" % (_gid, npc_id))
                continue
            if chat.grupo_activo and getattr(chat.grupo_activo, 'prioritario', False):
                npc = obtener_npc(npc_id)
                return npc.nombre if npc else npc_id.capitalize()
            for grupo in chat.grupos_pendientes:
                if getattr(grupo, 'prioritario', False):
                    npc = obtener_npc(npc_id)
                    return npc.nombre if npc else npc_id.capitalize()
        return None

    def obtener_horario_despertar_prioritario():
        """
        Busca mensajes prioritarios en espera que se entregarán en un horario futuro.
        Verifica todas las condiciones de entrega (horario, locación del NPC, condicion_entrega)
        para garantizar que el mensaje realmente llegará a ese horario.
        Retorna el menor horario futuro válido, o None si ninguno se va a entregar.
        """
        horario_hoy = getattr(store, 'horario_actual', 0)
        dia_hoy = getattr(store, 'dia_semana_actual', 0)
        grupos_en_espera = getattr(sistema_mensajes, '_grupos_en_espera', [])
        horario_min = None

        for grupo in grupos_en_espera:
            if not getattr(grupo, 'prioritario', False):
                continue
            mh = getattr(grupo, 'momento_horario', None)
            if mh is None or mh <= horario_hoy:
                continue

            # Verificar condicion_entrega si existe (se evalúa ahora como aproximación)
            if grupo.condicion_entrega is not None:
                try:
                    if not grupo.condicion_entrega():
                        continue
                except Exception:
                    continue

            # Verificar locación del NPC en el horario futuro usando su rutina predicha
            if grupo.momento_locacion is not None:
                npc = obtener_npc(grupo.npc_id)
                if npc is None:
                    continue
                loc_futura = npc.obtener_locacion_rutina(dia_hoy, mh)
                if loc_futura != grupo.momento_locacion:
                    continue

            if horario_min is None or mh < horario_min:
                horario_min = mh

        return horario_min
