################################################################################
## Sistema de Quests - Versión 2.0
################################################################################
## Sistema completo para gestionar misiones/quests con NPCs
## Incluye sistema de etapas, requisitos con mensajes, y pistas

# Constantes para las etapas de quest
define ETAPA_INICIALIZACION = 1
define ETAPA_ESPERA = 2
define ETAPA_CONDICIONES = 3
define ETAPA_RUTINA = 4
define ETAPA_BOTON_LISTO = 5
define ETAPA_VALIDACION = 6
define ETAPA_DESARROLLO = 7
define ETAPA_MEMORIAS = 8
define ETAPA_FINALIZACION = 9

# Lineas de quest. Cada NPC puede tener una quest activa por linea al mismo
# tiempo; el campo `linea` de Quest usa estos valores.
#   principal → la historia del personaje
#   amor / deseo → las lineas de relacion, atadas a los Hitos (core/hitos/)
# Vivian en core/quests/lineas_relacion.rpy, que se absorbio en el sistema de
# Hitos: ese archivo describia quest → umbral → desbloqueo, que es exactamente
# lo que ahora declara el Hito.
define LINEA_PRINCIPAL = "principal"
define LINEA_AMOR = "amor"
define LINEA_DESEO = "deseo"

init python:

    # -------------------------------------------------------------------------
    # Helpers de texto traducible para las pistas genéricas
    # -------------------------------------------------------------------------
    # Las pistas se COMPONEN (plantilla + dias/nombres/items), asi que hay que
    # traducir cada pieza por separado: un `old` con los valores ya incrustados
    # nunca matchearia. Las plantillas usan placeholders con NOMBRE ({dias}, {npc})
    # para que el ingles pueda reordenarlos o ignorarlos.

    def _q_unir(partes):
        """Une instrucciones con el conector traducido (' y ' / ' and ')."""
        return renpy.translate_string(" y ").join(partes)

    def _q_habla_con(npc_id):
        npc = obtener_npc(npc_id) if hasattr(store, 'sistema_npcs') else None
        nombre = npc.nombre if npc else npc_id.capitalize()
        return renpy.translate_string("Habla con {npc}").format(npc=nombre)

    def _q_nombre_item(item_id):
        """Nombre visible y traducido de un item (antes se mostraba el id crudo)."""
        info = getattr(store, 'CATALOGO_ITEMS', {}).get(item_id, {})
        return renpy.translate_string(info.get("nombre", item_id))

    def _q_nombre_horario(horario_id):
        nombres = ["la Mañana", "la Tarde", "la Noche", "la Trasnoche"]
        if 0 <= horario_id < len(nombres):
            return renpy.translate_string(nombres[horario_id])
        return "?"

    def _q_nombre_dia(dia_id):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        if 0 <= dia_id < len(dias):
            return renpy.translate_string(dias[dia_id])
        return "?"

    def _q_ir_a(nombre_loc, articulo):
        """
        'Ve al Living' / 'Ve a la Cocina'. El articulo es gramatica del español;
        el `new` en ingles simplemente lo ignora y usa solo {lugar}.
        """
        return renpy.translate_string("Ve {articulo} {lugar}").format(
            articulo=articulo, lugar=nombre_loc
        )

    # -------------------------------------------------------------------------
    # Registro de callables para serialización de quests
    # -------------------------------------------------------------------------
    # Se reconstruye en cada inicio del juego; nunca se guarda en el save.
    # Permite almacenar lambdas en Quest/ConfigEtapa sin romper el pickle.

    _quest_callable_registry = {}

    class CallableRef:
        """
        Referencia picklable a un callable del registro _quest_callable_registry.
        Permite almacenar lambdas en objetos Quest/ConfigEtapa sin romper el guardado.
        Se serializa solo como la clave (str); al ejecutarse busca la lambda en el
        registro que se reconstruye en cada inicio antes de cargar cualquier save.
        """
        def __init__(self, key):
            self.key = key

        def __call__(self, *args, **kwargs):
            fn = _quest_callable_registry.get(self.key)
            if fn is None:
                return None
            try:
                return fn(*args, **kwargs)
            except Exception:
                return None

    def _qc(key, fn):
        """
        Registra un callable con clave estable y devuelve un CallableRef picklable.
        Usar en ConfigEtapa/Quest en lugar de lambdas directas:

            pista=_qc("vq01a_pista", lambda: calcular_pista())

        Para funciones definidas con 'def' (que ya son picklables), usar
        referencia directa sin _qc:

            pista=mi_funcion
        """
        _quest_callable_registry[key] = fn
        return CallableRef(key)

    # -------------------------------------------------------------------------

    class Requisito:
        """
        Clase que representa un requisito para una quest.
        Cada requisito tiene un tipo, parámetros y un mensaje personalizado para pistas.
        """
        
        def __init__(self, tipo, mensaje, **params):
            """
            Args:
                tipo: uno de los tipos soportados por verificar() (ver abajo).
                    OJO: un tipo desconocido da el requisito por NO cumplido y
                    avisa por consola en modo desarrollador.
                mensaje: Mensaje personalizado para mostrar en pistas si no se cumple
                **params: Parámetros específicos según el tipo:
                    - hito: npc_id, hito_id      ← preferido sobre amor/deseo
                    - amor/deseo: npc_id, valor
                    - stat: stat_id, valor        (stat del MC, no del NPC)
                    - item: item_id, cantidad (default 1)
                    - dinero: valor
                    - memoria: categoria, clave, valor (opcional)
                    - locacion: locacion_id
                    - horario: horario_id
                    - dia: dia_id
                    - mensaje: grupo_id
                    - npc_presente: npc_id, locacion_id
                    - quest_mc: quest_id
                    - condicion: condicion (callable picklable o _qc(...))
            """
            self.tipo = tipo
            self.mensaje = mensaje
            self.params = params
        
        def verificar(self):
            """
            Verifica si el requisito se cumple.
            
            Returns:
                bool: True si el requisito se cumple
            """
            # stat1 genérico
            if self.tipo == "amor":
                npc_id = self.params.get("npc_id")
                valor_requerido = self.params.get("valor", 0)
                return obtener_stat1(npc_id) >= valor_requerido

            # stat2 genérico
            elif self.tipo == "deseo":
                npc_id = self.params.get("npc_id")
                valor_requerido = self.params.get("valor", 0)
                return obtener_stat2(npc_id) >= valor_requerido

            # Hito de relacion alcanzado (core/hitos/). Preferir SIEMPRE este
            # tipo sobre amor/deseo con numero suelto: el hito es la fuente de
            # verdad del progreso y le muestra al jugador un nombre en vez de
            # un umbral.
            elif self.tipo == "hito":
                npc_id = self.params.get("npc_id")
                hito_id = self.params.get("hito_id")
                return tiene_hito(npc_id, hito_id)

            elif self.tipo == "stat":
                stat_id = self.params.get("stat_id")
                valor_requerido = self.params.get("valor", 0)
                stat_actual = getattr(store, f"mc_{stat_id}", 0)
                return stat_actual >= valor_requerido
            
            elif self.tipo == "item":
                item_id = self.params.get("item_id")
                cantidad = self.params.get("cantidad", 1)
                inventario = getattr(store, "inventario", {})
                return inventario.get(item_id, 0) >= cantidad
            
            elif self.tipo == "dinero":
                valor_requerido = self.params.get("valor", 0)
                dinero_actual = getattr(store, "dinero", 0)
                return dinero_actual >= valor_requerido
            
            elif self.tipo == "memoria":
                categoria = self.params.get("categoria")
                clave = self.params.get("clave")
                valor = self.params.get("valor")
                return tiene_memoria(categoria, clave, valor)
            
            elif self.tipo == "locacion":
                locacion_id = self.params.get("locacion_id")
                if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
                    return store.sistema_locaciones.locacion_actual.id == locacion_id
                return False
            
            elif self.tipo == "horario":
                horario_id = self.params.get("horario_id")
                return getattr(store, 'horario_actual', -1) == horario_id
            
            elif self.tipo == "dia":
                dia_id = self.params.get("dia_id")
                return getattr(store, 'dia_semana_actual', -1) == dia_id
            
            elif self.tipo == "mensaje":
                grupo_id = self.params.get("grupo_id")
                if hasattr(store, 'sistema_mensajes'):
                    return store.sistema_mensajes.grupo_completado(grupo_id)
                return False
            
            elif self.tipo == "npc_presente":
                npc_id = self.params.get("npc_id")
                locacion_id = self.params.get("locacion_id")
                npc = obtener_npc(npc_id)
                if npc and locacion_id:
                    return npc.esta_en_locacion(locacion_id)
                return False

            elif self.tipo == "quest_mc":
                # Requiere que una quest del sistema propio del MC esté completada.
                quest_id = self.params.get("quest_id")
                if hasattr(store, 'sistema_quests_mc'):
                    q = store.sistema_quests_mc.quests.get(quest_id)
                    return q is not None and q.completada
                return False

            elif self.tipo == "condicion":
                # Condición libre para casos que no cubren los tipos anteriores.
                # El callable DEBE ser picklable (función de módulo o _qc(...)):
                # los Requisito viven dentro de sistema_quests, que se guarda.
                cond = self.params.get("condicion")
                if cond is None:
                    return True
                try:
                    return bool(cond())
                except Exception:
                    return False

            # Tipo desconocido → NO cumplido.
            #
            # Antes devolvia True ("asumir cumplido") y eso hacia que un typo en
            # el nombre del tipo diera el requisito por bueno EN SILENCIO: la
            # quest avanzaba sola y no habia forma de notarlo. Con False el fallo
            # es visible (la quest se traba) y ademas avisa por consola.
            if config.developer:
                print("[Quests] Requisito de tipo desconocido: '{}' — se toma como NO cumplido".format(self.tipo))
            return False
    
    
    class RutinaQuest:
        """
        Clase que representa una rutina modificada durante una quest.
        Incluye locación y sprite personalizado.
        """
        
        def __init__(self, locacion, sprite=None, posicion=None):
            """
            Args:
                locacion: ID de la locación donde estará el NPC
                sprite: Ruta del sprite personalizado (opcional)
                posicion: Tupla (x, y) para posición del sprite (opcional)
            """
            self.locacion = locacion
            self.sprite = sprite
            self.posicion = posicion
    
    
    class ConfiguracionRetorno:
        """
        Configuración para retornar al jugador despues de completar una quest.
        """
        
        def __init__(self, locacion=None, horario=None, dia_semana=None, avanzar_dia=False):
            """
            Args:
                locacion: ID de la locación destino (None = mantener actual)
                horario: Índice del horario (None = mantener actual)
                dia_semana: Índice del dia (None = mantener actual)
                avanzar_dia: Si True, avanza al siguiente dia
            """
            self.locacion = locacion
            self.horario = horario
            self.dia_semana = dia_semana
            self.avanzar_dia = avanzar_dia
    
    
    class ConfigEtapa:
        """
        Configuración por etapa para una quest o evento.
        Permite definir notificaciones y acciones específicas por etapa.
        Todos los campos de texto (pista, que_hacer, mensaje_despertar) pueden ser:
        - str: texto fijo
        - callable: función que retorna str (para contenido dinámico)
        """
        
        def __init__(self, pista="", que_hacer="", mensaje_despertar="",
                    trigger_mensaje=None, accion_al_entrar=None):
            """
            Args:
                pista: Texto o callable para el panel de pistas
                que_hacer: Texto o callable para el panel de qué hacer
                mensaje_despertar: Texto o callable para mostrar al despertar
                trigger_mensaje: Tupla (trigger_id, npc_id) para disparar un chat al entrar a la etapa
                accion_al_entrar: Callable a ejecutar al entrar a la etapa
            """
            self.pista = pista
            self.que_hacer = que_hacer
            self.mensaje_despertar = mensaje_despertar
            self.trigger_mensaje = trigger_mensaje
            self.accion_al_entrar = accion_al_entrar
        
        def _resolver(self, campo):
            """Resuelve un campo que puede ser str o callable."""
            valor = getattr(self, campo, "")
            if callable(valor):
                try:
                    resultado = valor()
                except Exception:
                    return ""
            else:
                resultado = valor
            # Traducir el string si hay traducción disponible
            if resultado and isinstance(resultado, str):
                try:
                    resultado = renpy.translate_string(resultado)
                except Exception:
                    pass
            return resultado
        
        def obtener_pista(self):
            return self._resolver("pista")
        
        def obtener_que_hacer(self):
            return self._resolver("que_hacer")
        
        def obtener_mensaje_despertar(self):
            return self._resolver("mensaje_despertar")
    
    
    class ConfigFallo:
        """
        Configuración de fallo para una quest.
        Define una condición que, al cumplirse, aplica penalidades y
        cambia los mensajes de pista/que_hacer.
        El fallo puede repetirse (ej: cada sábado que no se complete la quest).
        """
        
        def __init__(self, condicion, trigger_mensaje=None,
                    cambio_relacion=None, pista="", que_hacer=""):
            """
            Args:
                condicion: Callable que retorna bool (cuándo se produce el fallo)
                trigger_mensaje: Tupla (trigger_id, npc_id) para disparar chat de fallo
                cambio_relacion: Tupla (npc_id, cantidad) para modificar relacion
                pista: Texto o callable para pista post-fallo
                que_hacer: Texto o callable para qué hacer post-fallo
            """
            self.condicion = condicion
            self.trigger_mensaje = trigger_mensaje
            self.cambio_relacion = cambio_relacion
            self.pista = pista
            self.que_hacer = que_hacer
        
        def obtener_pista(self):
            if callable(self.pista):
                try:
                    return self.pista()
                except Exception:
                    return ""
            return self.pista
        
        def obtener_que_hacer(self):
            if callable(self.que_hacer):
                try:
                    return self.que_hacer()
                except Exception:
                    return ""
            return self.que_hacer
    
    
    class Quest:
        """
        Clase que representa una quest del juego con sistema de etapas.
        
        Etapas:
        1. INICIALIZACION - Requiere quest anterior completada
        2. ESPERA - Dias que deben pasar
        3. CONDICIONES - Verificar requisitos especiales
        4. RUTINA - Modificar rutina del NPC con sprite personalizado
        5. BOTON_LISTO - Botón para iniciar quest disponible
        6. VALIDACION - Verificación final antes de ejecutar label
        7. DESARROLLO - Ejecución del label de la quest
        8. MEMORIAS - Guardado de decisiones
        9. FINALIZACION - Completar y retornar jugador
        """
        
        def __init__(self, id, npc_id, nombre, descripcion, numero_quest,
                    dias_espera=0, condicion_espera=None, requisitos=None, validacion_especial=None,
                    rutina_quest=None, rutinas_adicionales=None, prioridad_rutina=0,
                    mensaje_pista="", retorno=None,
                    mostrar_en_menu=True, quest_anterior=None, mensaje_despertar="",
                    config_etapas=None, config_fallo=None, linea="principal"):
            """
            Args:
                id: ID único de la quest
                npc_id: ID del NPC que da la quest
                nombre: Nombre visible de la quest
                descripcion: Descripción de la quest
                numero_quest: Numero secuencial de la quest
                dias_espera: Dias a esperar antes de avanzar de etapa 2
                condicion_espera: Callable extra que debe retornar True para salir de espera
                requisitos: Lista de objetos Requisito para etapa 3
                validacion_especial: Lista de objetos Requisito para etapa 6
                rutina_quest: Dict {(dia, horario): RutinaQuest} para etapa 4
                rutinas_adicionales: Dict {npc_id: {(dia, horario): RutinaQuest}} para otros NPCs
                prioridad_rutina: Int, prioridad de rutina (mayor gana si hay conflicto)
                mensaje_pista: Mensaje para pistas durante etapa 4-5 (fallback)
                retorno: Objeto ConfiguracionRetorno para etapa 9
                mostrar_en_menu: Si debe aparecer en menú de interacción
                quest_anterior: ID de la quest que debe estar completada
                mensaje_despertar: Mensaje para mostrar al despertar (fallback)
                config_etapas: Dict {ETAPA_X: ConfigEtapa} para overrides por etapa
                config_fallo: ConfigFallo para condiciones de fallo repetible
                linea: "principal" | "amor" | "deseo". Un NPC puede tener una quest
                    activa por linea al mismo tiempo. Va al final de la firma y con
                    default para no tocar las ~40 definiciones ya existentes.

                    OJO al leerlo: las Quest deserializadas de un save ANTERIOR a
                    este campo NO tienen el atributo (el merge de after_load agrega
                    claves faltantes, no campos nuevos en instancias existentes).
                    Usar siempre getattr(q, "linea", "principal"), nunca q.linea.
            """
            self.id = id
            self.npc_id = npc_id
            self.nombre = nombre
            self.descripcion = descripcion
            self.numero_quest = numero_quest
            self.mostrar_en_menu = mostrar_en_menu
            self.quest_anterior = quest_anterior
            self.linea = linea
            
            # Configuración de etapas
            self.dias_espera = dias_espera
            self.condicion_espera = condicion_espera
            self.requisitos = requisitos or []
            self.validacion_especial = validacion_especial or []
            self.rutina_quest = rutina_quest or {}
            self.rutinas_adicionales = rutinas_adicionales or {}
            self.prioridad_rutina = prioridad_rutina
            self.mensaje_pista = mensaje_pista
            self.mensaje_despertar = mensaje_despertar
            self.retorno = retorno or ConfiguracionRetorno()
            
            # Configuración de etapas y fallo
            self.config_etapas = config_etapas or {}
            self.config_fallo = config_fallo
            
            # Estado de la quest
            self.etapa_actual = 0  # 0 = No iniciada
            self.activa = False
            self.completada = False
            self.dia_inicio = None  # Dia del juego cuando inició
            
            # Estado de fallo
            self.fallo_ocurrido = False
            self.ultimo_fallo_dia = 0
            
            # Label de la quest
            self.label_quest = f"quest_{self.id}"
            
            # Recuerdos/variables de la quest (compatibilidad con sistema anterior)
            self.recuerdos = {}
        
        def puede_iniciar(self):
            """
            Verifica si la quest puede iniciarse (pasar a etapa 1).
            
            Returns:
                bool: True si puede iniciarse
            """
            if self.activa or self.completada:
                return False
            
            # Verificar quest anterior completada
            if self.quest_anterior:
                quest_prev = sistema_quests.obtener_quest(self.quest_anterior)
                if not quest_prev or not quest_prev.completada:
                    return False
            
            return True
        
        def iniciar(self):
            """Inicia la quest (etapa 1 -> avanza automáticamente)"""
            if not self.puede_iniciar():
                return False
            
            self.activa = True
            self.etapa_actual = ETAPA_INICIALIZACION
            self.dia_inicio = getattr(store, 'dias_totales', 1)
            

            
            # Avanzar automáticamente según configuración
            self._procesar_avance_etapas()
            
            return True
        
        def _procesar_avance_etapas(self):
            """
            Procesa el avance automático de etapas.
            Cada etapa verifica si puede avanzar a la siguiente.
            Al cambiar de etapa, ejecuta acciones de entrada (triggers, callbacks).
            """
            while True:
                etapa_anterior = self.etapa_actual
                
                # Etapa 1 -> 2: Siempre avanza (inicialización completa)
                if self.etapa_actual == ETAPA_INICIALIZACION:
                    self.etapa_actual = ETAPA_ESPERA
                
                # Etapa 2 -> 3: Verificar dias de espera
                elif self.etapa_actual == ETAPA_ESPERA:
                    if self._verificar_espera():
                        self.etapa_actual = ETAPA_CONDICIONES
                
                # Etapa 3 -> 4: Verificar requisitos
                elif self.etapa_actual == ETAPA_CONDICIONES:
                    requisitos_faltantes = self.obtener_requisitos_faltantes()
                    if not requisitos_faltantes:
                        self.etapa_actual = ETAPA_RUTINA
                        self._aplicar_rutina_quest()
                
                # Etapa 4 -> 5: La rutina está aplicada, botón listo
                elif self.etapa_actual == ETAPA_RUTINA:
                    self.etapa_actual = ETAPA_BOTON_LISTO
                
                # Si hubo cambio de etapa, ejecutar acciones de entrada
                if self.etapa_actual != etapa_anterior:
                    self._ejecutar_entrada_etapa(self.etapa_actual)
                else:
                    # No hubo cambio, terminar el loop
                    break
        
        def _ejecutar_entrada_etapa(self, etapa):
            """
            Ejecuta acciones automáticas al entrar a una nueva etapa.
            Busca ConfigEtapa y ejecuta trigger_mensaje y accion_al_entrar.
            """
            cfg_etapa = self.config_etapas.get(etapa)
            if not cfg_etapa:
                return
            
            # Disparar mensaje si hay trigger configurado
            if cfg_etapa.trigger_mensaje:
                trigger_id, npc_id = cfg_etapa.trigger_mensaje
                if hasattr(store, 'sistema_mensajes'):
                    store.sistema_mensajes.disparar_por_trigger("quest_etapa", trigger_id, npc_id)

            
            # Ejecutar accion de entrada si existe
            if cfg_etapa.accion_al_entrar:
                try:
                    cfg_etapa.accion_al_entrar()
                except Exception as e:
                    pass
        
        def _verificar_espera(self):
            """Verifica si pasaron los días de espera y condiciones extra."""
            if self.dias_espera <= 0 and not self.condicion_espera:
                return True

            dia_total_actual = getattr(store, 'dias_totales', 1)
            dias_pasados = dia_total_actual - self.dia_inicio

            if dias_pasados < self.dias_espera:
                return False

            if self.condicion_espera and not self.condicion_espera():
                return False

            return True
        
        def obtener_requisitos_faltantes(self):
            """
            Obtiene la lista de requisitos que no se cumplen.
            
            Returns:
                Lista de objetos Requisito que no se cumplen
            """
            faltantes = []
            for req in self.requisitos:
                if not req.verificar():
                    faltantes.append(req)
            return faltantes
        
        def obtener_validacion_faltante(self):
            """
            Obtiene la lista de validaciones especiales que no se cumplen.
            
            Returns:
                Lista de objetos Requisito de validación que no se cumplen
            """
            faltantes = []
            for req in self.validacion_especial:
                if not req.verificar():
                    faltantes.append(req)
            return faltantes
        
        def intentar_ejecutar(self):
            """
            Intenta ejecutar la quest (cuando el jugador presiona el botón).
            
            Returns:
                tuple: (exito: bool, mensajes: list)
                    - exito: True si puede ejecutarse
                    - mensajes: Lista de mensajes de requisitos faltantes
            """
            if self.etapa_actual != ETAPA_BOTON_LISTO:
                return (False, ["La quest no está lista para iniciarse."])
            
            # Verificar validación especial (etapa 6)
            validacion_faltante = self.obtener_validacion_faltante()
            if validacion_faltante:
                mensajes = [req.mensaje for req in validacion_faltante]
                return (False, mensajes)
            
            # Validación exitosa, pasar a etapa de desarrollo
            self.etapa_actual = ETAPA_DESARROLLO
            return (True, [])
        
        def obtener_mensajes(self):
            """
            Obtiene los mensajes según la etapa actual.
            Prioridad: config_fallo (si fallo) > config_etapas > lógica genérica.
            
            Returns:
                dict: {"pista": str, "que_hacer": str}
            """
            pista = ""
            que_hacer = ""
            
            # 1. Si hubo fallo y hay config_fallo con mensajes, usar esos
            if self.fallo_ocurrido and self.config_fallo:
                pista_fallo = self.config_fallo.obtener_pista()
                que_hacer_fallo = self.config_fallo.obtener_que_hacer()
                if pista_fallo:
                    pista = pista_fallo
                if que_hacer_fallo:
                    que_hacer = que_hacer_fallo
                if pista and que_hacer:
                    return {"pista": pista, "que_hacer": que_hacer}
            
            # 2. Buscar override en config_etapas
            cfg_etapa = self.config_etapas.get(self.etapa_actual)
            if cfg_etapa:
                pista_override = cfg_etapa.obtener_pista()
                que_hacer_override = cfg_etapa.obtener_que_hacer()
                if pista_override:
                    pista = pista_override
                if que_hacer_override:
                    que_hacer = que_hacer_override
                # Si ambos estan definidos, retornar sin genéricos
                if pista and que_hacer:
                    return {"pista": pista, "que_hacer": que_hacer}
            
            # 3. Lógica genérica (fallback para campos no definidos en config)
            if not pista or not que_hacer:
                pista_gen = ""
                que_hacer_gen = ""
                
                if self.etapa_actual == ETAPA_ESPERA:
                    dias_restantes = self.dias_espera - (getattr(store, 'dias_totales', 1) - self.dia_inicio)
                    partes_que_hacer = []

                    if dias_restantes > 1:
                        pista_gen = renpy.translate_string("Debo esperar {dias} días más.").format(dias=dias_restantes)
                        partes_que_hacer.append(renpy.translate_string("Esperar {dias} días").format(dias=dias_restantes))
                    elif dias_restantes == 1:
                        pista_gen = renpy.translate_string("Debo esperar hasta mañana.")
                        partes_que_hacer.append(renpy.translate_string("Esperar hasta mañana"))
                    else:
                        pista_gen = renpy.translate_string("Debo esperar algunos días.")
                        partes_que_hacer.append(renpy.translate_string("Esperar algunos días"))

                    # Agregar requisitos faltantes
                    faltantes = self.obtener_requisitos_faltantes()
                    for req in faltantes:
                        partes_que_hacer.append(self._requisito_a_instruccion(req))

                    que_hacer_gen = _q_unir(partes_que_hacer) if partes_que_hacer else ""

                elif self.etapa_actual == ETAPA_CONDICIONES:
                    faltantes = self.obtener_requisitos_faltantes()
                    if faltantes:
                        pista_gen = renpy.translate_string(faltantes[0].mensaje)
                        instrucciones = [self._requisito_a_instruccion(req) for req in faltantes]
                        que_hacer_gen = _q_unir(instrucciones)
                    else:
                        pista_gen = renpy.translate_string("Verificando condiciones...")
                        que_hacer_gen = renpy.translate_string("Verificando...")

                elif self.etapa_actual in [ETAPA_RUTINA, ETAPA_BOTON_LISTO]:
                    pista_gen = self.mensaje_pista or _q_habla_con(self.npc_id)
                    que_hacer_gen = self._generar_que_hacer_validacion()

                elif self.etapa_actual == ETAPA_DESARROLLO:
                    pista_gen = renpy.translate_string("Quest en progreso...")
                    que_hacer_gen = renpy.translate_string("Continuar la quest.")
                
                # Usar genéricos solo para campos que no tienen override
                if not pista:
                    pista = pista_gen
                if not que_hacer:
                    que_hacer = que_hacer_gen
            
            # Fallback final
            if not pista:
                pista = self.descripcion
            if not que_hacer:
                que_hacer = pista
            
            # Traducir antes de retornar
            try:
                pista = renpy.translate_string(pista) if pista else pista
                que_hacer = renpy.translate_string(que_hacer) if que_hacer else que_hacer
            except Exception:
                pass
            
            return {"pista": pista, "que_hacer": que_hacer}
        
        def obtener_mensaje_pista(self):
            """
            Obtiene el mensaje de pista según la etapa actual.
            Método de compatibilidad que llama a obtener_mensajes().
            
            Returns:
                str: Mensaje para mostrar en el panel de pistas
            """
            return self.obtener_mensajes()["pista"]
        
        def _requisito_a_instruccion(self, req):
            """
            Convierte un requisito a instrucción directa para que_hacer.
            
            Args:
                req: Objeto Requisito
            
            Returns:
                str: Instrucción directa
            """
            if req.tipo == "locacion":
                loc_id = req.params.get("locacion_id", "")
                nombre_loc, articulo = self._obtener_nombre_locacion_con_articulo(loc_id)
                return _q_ir_a(nombre_loc, articulo)

            elif req.tipo == "horario":
                horario_id = req.params.get("horario_id", 0)
                return renpy.translate_string("durante {horario}").format(
                    horario=_q_nombre_horario(horario_id)
                )

            elif req.tipo == "dia":
                dia_id = req.params.get("dia_id", 0)
                return renpy.translate_string("El día {dia}").format(dia=_q_nombre_dia(dia_id))

            elif req.tipo == "amor":
                npc_id = req.params.get("npc_id", "")
                valor = req.params.get("valor", 0)
                return renpy.translate_string("Tener {valor} de Amor con {npc}").format(
                    valor=valor, npc=npc_id.capitalize()
                )

            elif req.tipo == "deseo":
                npc_id = req.params.get("npc_id", "")
                valor = req.params.get("valor", 0)
                return renpy.translate_string("Tener {valor} de Deseo con {npc}").format(
                    valor=valor, npc=npc_id.capitalize()
                )

            elif req.tipo == "hito":
                # Se muestra el NOMBRE del hito, no el umbral: el sentido del
                # sistema es que el jugador lea "Buena relación" y no "10 de amor".
                npc_id = req.params.get("npc_id", "")
                hito_id = req.params.get("hito_id", "")
                _h_req = obtener_hito(hito_id)
                _h_nombre = renpy.translate_string(_h_req.nombre) if _h_req else hito_id
                return renpy.translate_string("Alcanzar {hito} con {npc}").format(
                    hito=_h_nombre, npc=npc_id.capitalize()
                )

            elif req.tipo == "stat":
                stat_id = req.params.get("stat_id", "")
                valor = req.params.get("valor", 0)
                return renpy.translate_string("Tener {valor} de {stat}").format(
                    valor=valor, stat=renpy.translate_string(stat_id)
                )

            elif req.tipo == "item":
                item_id = req.params.get("item_id", "")
                cantidad = req.params.get("cantidad", 1)
                # Antes mostraba el id crudo del item ("coxplay_box"); ahora el nombre.
                return renpy.translate_string("Tener {cantidad}x {item}").format(
                    cantidad=cantidad, item=_q_nombre_item(item_id)
                )

            elif req.tipo == "dinero":
                valor = req.params.get("valor", 0)
                return renpy.translate_string("Tener ${valor}").format(valor=valor)

            elif req.tipo == "memoria":
                return renpy.translate_string(req.mensaje)

            return renpy.translate_string(req.mensaje)  # Fallback al mensaje original
        
        def _obtener_nombre_locacion(self, loc_id):
            """
            Obtiene el nombre legible de una locación.
            
            Args:
                loc_id: ID de la locación
            
            Returns:
                str: Nombre legible
            """
            # Intentar obtener del sistema de locaciones
            if hasattr(store, 'sistema_locaciones'):
                loc = store.sistema_locaciones.obtener_locacion(loc_id)
                if loc and hasattr(loc, 'nombre'):
                    return renpy.translate_string(loc.nombre)

            # Fallback: convertir ID a nombre legible
            # ej: "casa_living" -> "el Living"
            partes = loc_id.split("_")
            if len(partes) > 1:
                nombre = partes[-1].capitalize()
                return renpy.translate_string("el {lugar}").format(lugar=nombre)
            return loc_id.capitalize()
        
        def _obtener_nombre_locacion_con_articulo(self, loc_id):
            """
            Obtiene el nombre de una locación con el artículo correcto (al/a la).
            
            Args:
                loc_id: ID de la locación
            
            Returns:
                tuple: (nombre, articulo) - ej: ("Living", "al") o ("Cocina", "a la")
            """
            # Locaciones que usan "al" (masculinas o con artículo contracto)
            locaciones_al = ["frente", "living", "baño", "pasillo", "garage", "sotano", 
                            "patio", "gym", "comedor"]
            
            # Locaciones que usan "a la" (femeninas)
            locaciones_a_la = ["cocina", "habitacion", "hmonica", "hjasmine", "hviolet", "hmc"]
            
            # Obtener nombre legible
            nombre = self._obtener_nombre_locacion(loc_id)
            
            # Determinar artículo basado en el ID
            loc_id_lower = loc_id.lower()
            for loc in locaciones_a_la:
                if loc in loc_id_lower:
                    return (nombre, "a la")
            
            for loc in locaciones_al:
                if loc in loc_id_lower:
                    return (nombre, "al")
            
            # Default: usar "al"
            return (nombre, "al")
        
        def _generar_que_hacer_validacion(self):
            """
            Genera mensaje que_hacer para etapa BOTON_LISTO.
            Siempre muestra la locación y horario de la quest, sin importar si ya estan cumplidos.
            Formato: "Ve al [lugar] durante [horario]" + " y " + otros requisitos
            
            Returns:
                str: Instrucciones combinadas
            """
            locacion_texto = None
            horario_texto = None
            otros_requisitos = []
            
            # Procesar validación especial primero
            for req in self.validacion_especial:
                if req.tipo == "locacion":
                    loc_id = req.params.get("locacion_id", "")
                    nombre_loc, articulo = self._obtener_nombre_locacion_con_articulo(loc_id)
                    locacion_texto = _q_ir_a(nombre_loc, articulo)
                elif req.tipo == "horario":
                    horario_id = req.params.get("horario_id", 0)
                    horario_texto = renpy.translate_string("durante {horario}").format(
                        horario=_q_nombre_horario(horario_id)
                    )
                elif req.tipo == "dia":
                    otros_requisitos.append(self._requisito_a_instruccion(req))
                elif not req.verificar():
                    otros_requisitos.append(self._requisito_a_instruccion(req))

            # Si no hay en validación especial, buscar en requisitos normales
            if not locacion_texto or not horario_texto:
                for req in self.requisitos:
                    if req.tipo == "locacion" and not locacion_texto:
                        loc_id = req.params.get("locacion_id", "")
                        nombre_loc, articulo = self._obtener_nombre_locacion_con_articulo(loc_id)
                        locacion_texto = _q_ir_a(nombre_loc, articulo)
                    elif req.tipo == "horario" and not horario_texto:
                        horario_id = req.params.get("horario_id", 0)
                        horario_texto = renpy.translate_string("durante {horario}").format(
                            horario=_q_nombre_horario(horario_id)
                        )

            # Construir mensaje
            partes = []

            # Combinar locación + horario (sin "y" entre ellos)
            if locacion_texto and horario_texto:
                partes.append("{} {}".format(locacion_texto, horario_texto))
            elif locacion_texto:
                partes.append(locacion_texto)
            elif horario_texto:
                # Solo horario: va como frase suelta, con la primera en mayuscula
                partes.append(horario_texto[:1].upper() + horario_texto[1:])

            # Agregar otros requisitos con "y"
            partes.extend(otros_requisitos)

            if partes:
                return _q_unir(partes)

            # Si no hay nada definido, indicar que hable con el NPC
            return _q_habla_con(self.npc_id)
        
        def _aplicar_rutina_quest(self):
            """Aplica la rutina especial de la quest al NPC principal y NPCs adicionales."""
            # Aplicar rutina al NPC principal
            if self.rutina_quest:
                self._aplicar_rutina_a_npc(self.npc_id, self.rutina_quest)
            
            # Aplicar rutinas adicionales a otros NPCs
            for npc_id_adicional, rutinas in self.rutinas_adicionales.items():
                self._aplicar_rutina_a_npc(npc_id_adicional, rutinas)
        
        def _aplicar_rutina_a_npc(self, npc_id, rutinas):
            """
            Aplica rutinas de quest a un NPC específico, respetando prioridades.
            Solo aplica si no hay otra quest con mayor prioridad afectando al mismo NPC.
            
            Args:
                npc_id: ID del NPC a modificar
                rutinas: Dict {(dia, horario): RutinaQuest o str}
            """
            npc = obtener_npc(npc_id)
            if not npc:
                return
            
            # Verificar si otra quest activa tiene mayor prioridad sobre este NPC
            if self._hay_prioridad_mayor(npc_id):
                return
            
            # Aplicar rutina de quest en el dict dedicado (prioridad sobre especiales)
            if not hasattr(npc, 'rutinas_quest'):
                npc.rutinas_quest = {}

            for (dia, horario), rutina in rutinas.items():
                if isinstance(rutina, RutinaQuest):
                    npc.rutinas_quest[(dia, horario)] = rutina.locacion
                else:
                    npc.rutinas_quest[(dia, horario)] = rutina

            npc.actualizar_ubicacion()
        
        def _hay_prioridad_mayor(self, npc_id):
            """
            Verifica si hay otra quest activa con mayor prioridad que afecte al mismo NPC.
            
            Args:
                npc_id: ID del NPC a verificar
            
            Returns:
                bool: True si hay otra quest con mayor prioridad
            """
            for quest in sistema_quests.quests.values():
                if quest.id == self.id or not quest.activa:
                    continue
                if quest.prioridad_rutina <= self.prioridad_rutina:
                    continue
                # Verificar si esa quest afecta al mismo NPC
                if quest.npc_id == npc_id and quest.rutina_quest:
                    return True
                if npc_id in quest.rutinas_adicionales:
                    return True
            return False
        
        def _rutina_quest_vigente(self, npc_id=None):
            """
            Devuelve la RutinaQuest de este momento para `npc_id` SOLO si esta
            realmente aplicada, o sea si el NPC esta parado en la locacion que
            ella define. Sin npc_id, se refiere al NPC principal de la quest.

            Sirve tanto para el NPC principal (rutina_quest) como para los que la
            quest mueve de prestado (rutinas_adicionales).

            Por que el chequeo de locacion: la rutina de quest recien se le aplica
            al NPC en ETAPA_RUTINA (_aplicar_rutina_quest, al pasar de etapa 3 a
            4), pero el sprite y la posicion se consultaban desde la etapa 1.
            En el medio el NPC sigue en su rutina normal, asi que el HUD lo
            dibujaba en su locacion de siempre pero con el sprite y la posicion de
            la quest. Bug real (0.1.8c): quest 04_b "Violet y el Cosplay" en
            ETAPA_ESPERA mostraba a Violet en la cocina con el sprite del pasillo
            del door access, y ubicada en la posicion del pasillo.

            Comparar contra locacion_actual mantiene sprite y posicion
            sincronizados con donde esta parado el NPC, sin importar la etapa ni
            quien lo haya movido (rutina, door access, evento).
            """
            if npc_id is None:
                npc_id = self.npc_id

            if npc_id == self.npc_id:
                rutinas = self.rutina_quest
            else:
                rutinas = self.rutinas_adicionales.get(npc_id)

            if not rutinas:
                return None

            dia = getattr(store, 'dia_semana_actual', 0)
            horario = getattr(store, 'horario_actual', 0)

            rutina = rutinas.get((dia, horario))
            if not (rutina and isinstance(rutina, RutinaQuest)):
                return None

            # Si la rutina define locacion, el NPC tiene que estar ahi para que
            # su visual de quest valga. Sin locacion, no hay con que contrastar.
            if rutina.locacion:
                npc = obtener_npc(npc_id)
                if not npc or npc.locacion_actual != rutina.locacion:
                    return None

            return rutina

        def obtener_sprite_quest(self, npc_id=None):
            """
            Obtiene el sprite de la quest para el momento actual.

            Returns:
                str o None: Ruta del sprite o None si no hay sprite de quest
            """
            rutina = self._rutina_quest_vigente(npc_id)
            return rutina.sprite if rutina else None

        def obtener_posicion_quest(self, npc_id=None):
            """
            Obtiene la posición del sprite de la quest para el momento actual.

            Returns:
                tuple o None: (x, y) o None si no hay posición definida
            """
            rutina = self._rutina_quest_vigente(npc_id)
            return rutina.posicion if rutina else None
        
        def _restaurar_rutina_normal(self):
            """Restaura la rutina normal del NPC principal y NPCs adicionales."""
            # Restaurar NPC principal
            self._restaurar_rutina_npc(self.npc_id)
            
            # Restaurar NPCs adicionales
            for npc_id_adicional in self.rutinas_adicionales:
                self._restaurar_rutina_npc(npc_id_adicional)
        
        def _restaurar_rutina_npc(self, npc_id):
            """Restaura la rutina normal de un NPC eliminando las entradas de esta quest."""
            npc = obtener_npc(npc_id)
            if not npc:
                return

            # Nuevo formato: eliminar las claves de esta quest de rutinas_quest
            rutinas_a_limpiar = self.rutina_quest if npc_id == self.npc_id else self.rutinas_adicionales.get(npc_id, {})
            rutinas_q = getattr(npc, 'rutinas_quest', {})
            for clave in rutinas_a_limpiar:
                rutinas_q.pop(clave, None)
            npc.rutinas_quest = rutinas_q

            # Compatibilidad con saves anteriores que usaban rutina_original
            if hasattr(npc, 'rutina_original'):
                npc.rutinas = npc.rutina_original.copy()
                delattr(npc, 'rutina_original')

            npc.actualizar_ubicacion()
        
        def completar(self, recuerdos_finales=None):
            """
            Completa la quest (etapa 8-9).
            
            Args:
                recuerdos_finales: Dict con recuerdos a guardar
            """
            self.etapa_actual = ETAPA_MEMORIAS
            
            # Guardar recuerdos
            if recuerdos_finales:
                self.recuerdos.update(recuerdos_finales)
                # Tambien guardar en el sistema de memorias global
                for clave, valor in recuerdos_finales.items():
                    guardar_memoria(self.npc_id, clave, valor)
            
            self.etapa_actual = ETAPA_FINALIZACION
            
            # Restaurar rutina normal del NPC
            self._restaurar_rutina_normal()
            
            # Aplicar configuración de retorno
            self._aplicar_retorno()
            
            # Marcar como completada
            self.activa = False
            self.completada = True
            
            # Incrementar progreso del NPC
            npc = obtener_npc(self.npc_id)
            if npc:
                npc.modificar_progreso(1)
            
            # Avanzar numero de quest global
            store.quest_actual += 1

            # NOTA: acá había un hook aplicar_desbloqueo_relacion(self.id) del
            # sistema lineas_relacion, que se absorbió en los Hitos. Ya no hace
            # falta enganchar nada al completar: si esta quest otorga un hito,
            # el trigger de game_loop lo detecta por su quest_id en la vuelta
            # siguiente (ver core/hitos/hitos_main.rpy → actualizar_hitos).

            # Disparar mensaje de chat si existe
            if hasattr(store, 'sistema_mensajes'):
                store.sistema_mensajes.disparar_por_trigger("quest", self.id, self.npc_id)
            
            # Buscar e iniciar la siguiente quest del mismo NPC
            self._iniciar_siguiente_quest()
        
        def _aplicar_retorno(self):
            """Aplica la configuración de retorno al completar la quest."""
            if not self.retorno:
                return
            
            if self.retorno.avanzar_dia:
                # Avanzar al siguiente dia
                if hasattr(store, 'avanzar_dia'):
                    avanzar_dia()
            
            if self.retorno.horario is not None:
                store.horario_actual = self.retorno.horario
            
            if self.retorno.dia_semana is not None:
                store.dia_semana_actual = self.retorno.dia_semana
            
            if self.retorno.locacion:
                # Ir a la locación especificada (mover_a_locacion es el método
                # real del sistema; ir_a_locacion no existe en la clase)
                sistema_locaciones.mover_a_locacion(self.retorno.locacion)
        
        def _iniciar_siguiente_quest(self):
            """
            Inicia TODAS las quests del mismo NPC que declaran esta como anterior.

            Antes cortaba con un `break` en la primera coincidencia. Con las lineas
            eso rompia el encadenamiento: si la Principal y la primera de Amor
            encadenan de la misma quest, solo arrancaba la registrada primero y la
            otra quedaba dormida PARA SIEMPRE, porque nadie vuelve a evaluar el
            encadenamiento despues.

            Sigue filtrando por npc_id: una quest no abre la linea de otro NPC.
            """
            for quest in sistema_quests.quests.values():
                if quest.npc_id == self.npc_id and quest.quest_anterior == self.id:
                    if quest.puede_iniciar():
                        quest.iniciar()
        
        def obtener_mensaje_despertar_actual(self):
            """
            Obtiene el mensaje de despertar según la etapa actual.
            A diferencia del mensaje_despertar estático, este puede cambiar
            según la etapa y usar callables para contenido dinámico.
            
            Returns:
                str: Mensaje para mostrar al despertar, o "" si no hay
            """
            # Buscar en config_etapas primero
            cfg_etapa = self.config_etapas.get(self.etapa_actual)
            if cfg_etapa:
                msg = cfg_etapa.obtener_mensaje_despertar()
                if msg:
                    return msg
            
            # Fallback al mensaje estático
            msg = self.mensaje_despertar or ""
            if msg:
                try:
                    msg = renpy.translate_string(msg)
                except Exception:
                    pass
            return msg
        
        def verificar_fallo(self):
            """
            Verifica si se produce un fallo en la quest.
            Solo se puede fallar una vez por dia (evita repetir el mismo dia).
            Si se detecta fallo, dispara acciones y marca fallo_ocurrido.
            
            Returns:
                bool: True si se produjo un fallo en esta llamada
            """
            if not self.config_fallo:
                return False
            if not self.activa or self.completada:
                return False
            
            # Solo verificar en etapas donde tiene sentido fallar (BOTON_LISTO)
            if self.etapa_actual not in [ETAPA_BOTON_LISTO, ETAPA_RUTINA]:
                return False
            
            # Evitar fallar dos veces el mismo dia
            dia_actual = getattr(store, 'dias_totales', 1)
            if self.ultimo_fallo_dia == dia_actual:
                return False
            
            # Verificar condición de fallo
            try:
                if not self.config_fallo.condicion():
                    return False
            except Exception:
                return False
            
            # ¡Fallo detectado!
            self.fallo_ocurrido = True
            self.ultimo_fallo_dia = dia_actual
            
            # Disparar chat de fallo
            if self.config_fallo.trigger_mensaje:
                trigger_id, npc_id = self.config_fallo.trigger_mensaje
                if hasattr(store, 'sistema_mensajes'):
                    store.sistema_mensajes.disparar_por_trigger("quest_fallo", trigger_id, npc_id)
            
            # Aplicar cambio de stat1
            if self.config_fallo.cambio_relacion:
                npc_id, cantidad = self.config_fallo.cambio_relacion
                npc = obtener_npc(npc_id)
                if npc:
                    npc.modificar_stat1(cantidad)
            

            
            return True
        
        def actualizar(self):
            """
            Actualiza el estado de la quest.
            Debe llamarse periódicamente (ej: al cambiar de horario).
            """
            if not self.activa or self.completada:
                return
            
            self._procesar_avance_etapas()
            
            # Verificar condición de fallo
            self.verificar_fallo()
        
        # Métodos de compatibilidad con sistema anterior
        def guardar_recuerdo(self, clave, valor):
            """Guarda un recuerdo de la quest"""
            self.recuerdos[clave] = valor
            guardar_memoria(self.npc_id, clave, valor)
        
        def obtener_recuerdo(self, clave, default=None):
            """Obtiene un recuerdo de la quest"""
            return self.recuerdos.get(clave, default)
        
        # Alias para compatibilidad
        def puede_activarse(self):
            """Alias de puede_iniciar para compatibilidad"""
            # Verificar tambien que estemos en las condiciones correctas
            if not self.puede_iniciar():
                return False
            
            # Verificar condiciones adicionales del sistema anterior
            return True
        
        def activar(self):
            """Alias de iniciar para compatibilidad"""
            return self.iniciar()
        
        def resetear(self):
            """Resetea el estado de la quest a su estado inicial"""
            self.activa = False
            self.completada = False
            self.etapa_actual = 0
            self.dia_inicio = 0
            self.recuerdos = {}


    class SistemaQuests:
        """
        Gestor central del sistema de quests.
        """
        
        def __init__(self):
            self.quests = {}  # Dict de todas las quests por ID
            self.quests_por_npc = {}  # Dict de quests agrupadas por NPC
        
        def registrar_quest(self, quest):
            """Registra una quest en el sistema"""
            self.quests[quest.id] = quest
            
            # Agrupar por NPC
            if quest.npc_id not in self.quests_por_npc:
                self.quests_por_npc[quest.npc_id] = []
            self.quests_por_npc[quest.npc_id].append(quest)
        
        def obtener_quest(self, quest_id):
            """Obtiene una quest por su ID"""
            return self.quests.get(quest_id)
        
        def obtener_quests_npc(self, npc_id):
            """Obtiene todas las quests de un NPC"""
            return self.quests_por_npc.get(npc_id, [])
        
        def obtener_quests_disponibles(self, npc_id):
            """Obtiene quests disponibles para activar de un NPC que deben mostrarse en el menú"""
            quests_npc = self.obtener_quests_npc(npc_id)
            return [q for q in quests_npc if q.puede_activarse() and q.mostrar_en_menu]
        
        def obtener_quest_activa(self, npc_id=None):
            """
            Obtiene la quest activa, PRIORIZANDO la de la linea principal.

            Args:
                npc_id: Si se especifica, busca quest activa de ese NPC

            Returns:
                Quest activa o None

            POR QUE PRIORIZA LA PRINCIPAL:
            desde que existen las lineas (principal / amor / deseo) un NPC tiene
            varias quests activas a la vez. Esta funcion devolvia la PRIMERA por
            orden de registro, y los archivos de linea (characters/violet/amor/,
            .../deseo/) se cargan ANTES que characters/violet/quests/ por orden
            alfabetico — asi que "la quest activa de Violet" pasaba a ser
            violet_amor_01 y los botones que preguntan por una quest principal
            dejaban de aparecer (bug real: el boton de la 04_a en la cocina).

            "La quest activa" de un NPC es la de su HISTORIA. Las de relacion se
            piden aparte con obtener_quests_activas_npc(npc_id, linea).
            """
            fallback = None

            for quest in self.quests.values():
                if not quest.activa:
                    continue
                if npc_id is not None and quest.npc_id != npc_id:
                    continue

                # getattr: las Quest de un save anterior al campo `linea` no lo
                # tienen y cuentan como principales.
                if getattr(quest, "linea", LINEA_PRINCIPAL) == LINEA_PRINCIPAL:
                    return quest

                # Solo de relacion activa: se devuelve igual, para no romper a
                # quien esperaba "alguna quest" (ej. el indicador del HUD).
                if fallback is None:
                    fallback = quest

            return fallback
        
        def obtener_quests_activas(self):
            """
            Obtiene todas las quests activas.

            Returns:
                Lista de quests activas
            """
            return [q for q in self.quests.values() if q.activa]

        def obtener_quests_activas_npc(self, npc_id, linea=None):
            """
            Todas las quests activas de un NPC, opcionalmente filtradas por linea.

            Complementa a obtener_quest_activa(), que devuelve SOLO una (la de
            la linea principal) y por eso no alcanza cuando hace falta ver las
            de relacion corriendo en paralelo.

            Se construye sobre self.quests y NO sobre quests_por_npc a proposito:
            en un save viejo el merge de after_load llena .quests pero deja
            quests_por_npc sin las quests nuevas, asi que las lineas nuevas serian
            invisibles en partidas existentes.

            La linea se lee con getattr: las Quest deserializadas de un save
            anterior al campo no tienen el atributo.

            Returns:
                Lista de quests activas (puede estar vacia)
            """
            rv = []
            for q in self.quests.values():
                if not q.activa or q.npc_id != npc_id:
                    continue
                if linea is not None and getattr(q, "linea", "principal") != linea:
                    continue
                rv.append(q)
            return rv
        
        def hay_quest_activa(self):
            """Verifica si hay alguna quest activa"""
            return self.obtener_quest_activa() is not None
        
        def verificar_recuerdo(self, npc_id, recuerdo_key, valor_esperado):
            """
            Verifica un recuerdo de quests anteriores.
            
            Args:
                npc_id: ID del NPC
                recuerdo_key: Clave del recuerdo
                valor_esperado: Valor esperado
            
            Returns:
                bool: True si el recuerdo coincide
            """
            # Primero verificar en el sistema de memorias global
            if tiene_memoria(npc_id, recuerdo_key, valor_esperado):
                return True
            
            # Fallback: verificar en recuerdos de quests completadas
            quests_npc = self.obtener_quests_npc(npc_id)
            for quest in quests_npc:
                if quest.completada:
                    valor_actual = quest.obtener_recuerdo(recuerdo_key)
                    if valor_actual == valor_esperado:
                        return True
            return False
        
        def obtener_pista_actual(self):
            """
            Obtiene la pista para la quest actual según el numero de quest.
            
            Returns:
                Dict con informacion de la pista o None
            """
            # Buscar quest activa
            quest_activa = self.obtener_quest_activa()
            if quest_activa:
                npc = obtener_npc(quest_activa.npc_id)
                if npc:
                    return {
                        "npc_nombre": npc.nombre,
                        "npc_id": quest_activa.npc_id,
                        "locacion": npc.locacion_actual,
                        "quest_nombre": quest_activa.nombre,
                        "descripcion": quest_activa.descripcion,
                        "mensaje": quest_activa.obtener_mensaje_pista()
                    }
            
            return None
        
        def actualizar_todas(self):
            """Actualiza el estado de todas las quests activas"""
            for quest in self.quests.values():
                if quest.activa:
                    quest.actualizar()
        
        def resetear_todas(self):
            """Resetea el estado de todas las quests (para nuevo juego)"""
            for quest in self.quests.values():
                quest.resetear()


# Instancia global del sistema de quests (define para estar disponible en init)
# Instancia creada en init 4 (los registros de init 5-11 la llenan) y declarada
# con default para que se guarde en el save: el progreso de quests vive dentro del sistema y debe guardarse.
init 4 python:
    sistema_quests = SistemaQuests()
# OJO: el default se re-evalúa en CADA partida nueva. Debe devolver una COPIA
# del catálogo poblado en init — una instancia vacía (SistemaQuests()) borraría todo
# el contenido registrado. Ver _ps_copia_fresca en persistencia_sistemas.rpy.
default sistema_quests = _ps_copia_fresca("sistema_quests")

# Variable global para el numero de quest actual
default quest_actual = 0

################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def iniciar_quest(quest_id):
        """
        Inicia una quest específica.
        
        Args:
            quest_id: ID de la quest a iniciar
        
        Returns:
            bool: True si se pudo iniciar
        """
        quest = sistema_quests.obtener_quest(quest_id)
        if quest and quest.puede_iniciar():
            return quest.iniciar()
        return False
    
    def completar_quest_actual(npc_id=None, recuerdos=None, quest_id=None):
        """
        Completa una quest activa.

        Args:
            npc_id: ID del NPC (completa su PRIMERA quest activa)
            recuerdos: Dict con recuerdos a guardar
            quest_id: ID exacto de la quest a completar. Tiene prioridad sobre npc_id.

        POR QUE EXISTE quest_id:
        con las lineas (principal / amor / deseo) un mismo NPC puede tener varias
        quests activas a la vez. Buscar "la activa del NPC" devuelve la PRIMERA por
        orden de registro, asi que el label de una quest de Amor completaria la
        Principal — disparando su chat, su `retorno`, el progreso del NPC y el
        arranque de la quest siguiente de esa otra linea.

        REGLA: TODO label de contenido pasa quest_id. Ya estan migrados los 40
        callsites del juego (violet, monica, jasmine y los chats de carl/violet).
        El fallback por npc_id queda SOLO para la herramienta de desarrollo
        (tools/quests/herramienta_quests.rpy), que completa "la activa de este
        NPC" sin saber cual es.
        """
        # Bloquear rollback para que el jugador no pueda volver a entrar a la quest
        renpy.block_rollback()

        quest_a_completar = None

        if quest_id:
            _q = sistema_quests.obtener_quest(quest_id)
            if _q and _q.activa:
                quest_a_completar = _q
        elif npc_id:
            # Buscar la quest activa del NPC específico
            for quest in sistema_quests.quests.values():
                if quest.activa and quest.npc_id == npc_id:
                    quest_a_completar = quest
                    break
        else:
            quest_a_completar = sistema_quests.obtener_quest_activa()

        if quest_a_completar:
            quest_a_completar.completar(recuerdos)
            # Cerrar una quest cuenta como contacto con su NPC (ver
            # core/npcs/npc_contacto.rpy). No alcanza con el embudo de stats:
            # hay quests que no mueven ninguno.
            if hasattr(store, 'marcar_contacto_npc'):
                store.marcar_contacto_npc(quest_a_completar.npc_id)
    
    def guardar_recuerdo_quest(clave, valor):
        """
        Guarda un recuerdo en la quest activa.
        
        Args:
            clave: Clave del recuerdo
            valor: Valor a guardar
        """
        quest_activa = sistema_quests.obtener_quest_activa()
        if quest_activa:
            quest_activa.guardar_recuerdo(clave, valor)
    
    def obtener_pista_quest():
        """Obtiene la pista de la quest actual"""
        return sistema_quests.obtener_pista_actual()
    
    def intentar_iniciar_quest_actual():
        """
        Intenta iniciar la quest activa (cuando el jugador presiona el botón).
        
        Returns:
            tuple: (exito, mensajes)
        """
        quest_activa = sistema_quests.obtener_quest_activa()
        if quest_activa:
            return quest_activa.intentar_ejecutar()
        return (False, ["No hay quest activa."])
    
    def _buscar_rutina_quest_vigente(npc_id):
        """
        Busca entre las quests activas la RutinaQuest vigente para este NPC.

        Mira DOS lugares, porque a un NPC lo puede reubicar tanto su propia quest
        como la quest de otro personaje:
        1. `rutina_quest` de la quest activa del propio NPC.
        2. `rutinas_adicionales` de las quests de OTROS NPCs (ej: la quest 09_a
        de Violet mueve a Monica). Sin este paso, esos NPCs se movian de
        locacion pero se seguian dibujando con el sprite de su rutina normal,
        que corresponde a otra habitacion — el mismo bug que E07.

        DESEMPATA POR `prioridad_rutina`, mayor gana. Antes devolvia la primera
        vigente que encontraba, con este razonamiento: "un NPC esta en una sola
        locacion, asi que como mucho una rutina puede coincidir". Es FALSO —
        dos quests pueden mandarlo al MISMO lugar a la misma hora, y ahi decidia
        el orden de iteracion, que es arbitrario.

        Bug real: con la 09_a (Violet enferma) y la de deseo 25 o 30 activas a
        la vez, las dos la ponen en su habitacion por la noche. La de deseo trae
        el idle de pijama y la 09_a el de enferma, y de noche salia el de
        pijama — se la veia sana estando enferma.

        A igual prioridad gana la primera, como antes: `>` y no `>=`.
        """
        _mejor = None
        _mejor_prio = None

        # 1. Rutina propia. Se recorren TODAS las quests activas del NPC y no solo
        #    la primera: con varias lineas en paralelo, la que define la rutina
        #    puede no ser la primera por orden de registro.
        # 2. rutinas_adicionales de quests de OTROS NPCs (ej: la 09_a de Violet
        #    mueve a Monica).
        _candidatas = list(sistema_quests.obtener_quests_activas_npc(npc_id))
        for q in sistema_quests.quests.values():
            if not q.activa or q.npc_id == npc_id:
                continue
            if npc_id in q.rutinas_adicionales:
                _candidatas.append(q)

        for quest in _candidatas:
            rutina = quest._rutina_quest_vigente(npc_id)
            if not rutina:
                continue
            _prio = getattr(quest, "prioridad_rutina", 0)
            if _mejor_prio is None or _prio > _mejor_prio:
                _mejor, _mejor_prio = rutina, _prio

        return _mejor

    def obtener_sprite_quest_npc(npc_id):
        """
        Obtiene el sprite de quest para un NPC si está en una quest activa.

        Args:
            npc_id: ID del NPC

        Returns:
            str o None: Ruta del sprite o None
        """
        rutina = _buscar_rutina_quest_vigente(npc_id)
        return rutina.sprite if rutina else None
    
    def obtener_posicion_quest_npc(npc_id):
        """
        Obtiene la posición del sprite de quest para un NPC.
        
        Args:
            npc_id: ID del NPC
        
        Returns:
            tuple o None: (x, y) o None
        """
        rutina = _buscar_rutina_quest_vigente(npc_id)
        return rutina.posicion if rutina else None
    
    def quest_lista_para_boton(quest_id):
        """
        True si la quest esta activa, sin completar y en ETAPA_BOTON_LISTO.

        Es EL predicado estandar de los disparadores manuales (botones del menu
        de interaccion, opciones de puerta, triggers de dormir/game_loop). Las
        condiciones registradas por el contenido deben usarlo en vez de repetir
        la cadena `activa and not completada and etapa == ...` a mano.
        """
        q = store.sistema_quests.obtener_quest(quest_id)
        if not (q and q.activa and not q.completada and
                q.etapa_actual == ETAPA_BOTON_LISTO):
            return False

        # Con el NPC fuera de juego ninguna de sus quests se puede disparar
        # (core/npcs/npc_disponibilidad.rpy). Acá alcanza para TODAS: este es
        # el predicado que usan los botones, las opciones de puerta y los
        # triggers de dormir/game_loop.
        return npc_disponible(q.npc_id)

    # Icono por linea, para los tags de los botones. Mismos emojis que usa el
    # panel de Pistas en sus pestañas, asi el jugador los asocia.
    _ICONO_LINEA_QUEST = {
        LINEA_PRINCIPAL: "⭐",
        LINEA_AMOR:      "❤️",
        LINEA_DESEO:     "💋",
    }

    def tag_opcion_quest(label, es_evento=False, tipo=None, quest_id=None):
        """
        Tag que va al final de un boton del menu de NPC o de puerta.

        Devuelve "" para tipo "ventaja", " (Evento)" para eventos, o
        " (<icono> Quest)" segun la LINEA de la quest.

        DE DONDE SALE LA QUEST, en dos pasos.
        Primero `quest_id`, si la opcion lo trae: es la via para los botones
        cuyo label es PROPIO y no `quest_<id>` — que son muchos, porque casi
        toda quest con una escena de entrada aparte ("Ya compré los cosplay",
        "Tengo las entradas", "Matar el tiempo") tiene su label propio.
        Si no viene, se deduce del label: los labels de quest se llaman
        `quest_<quest_id>`. Eso cubre solo a las que entran derecho al label de
        la quest, sin tener que declarar nada.

        Sin ninguna de las dos —eventos, contenido suelto— cae al " (Quest)"
        pelado, sin icono.
        """
        # Las opciones de VENTAJA no llevan tag: no son contenido puntual que
        # aparece y se va, son capacidades permanentes del vinculo — se leen
        # como "Hablar", no como una quest pendiente.
        if tipo == "ventaja":
            return ""

        if es_evento:
            return renpy.translate_string(" (Evento)")

        # `quest_id` puede venir como funcion: las opciones de PUERTA se
        # registran en init 5 con un valor fijo, y el arco de los favores cambia
        # de quest segun el tramo, asi que necesita resolverse al mostrar el
        # menu y no al registrarse.
        _qid_tag = quest_id
        if callable(_qid_tag):
            try:
                _qid_tag = _qid_tag()
            except Exception:
                _qid_tag = None
        if not _qid_tag and label and label.startswith("quest_"):
            _qid_tag = label[len("quest_"):]

        _linea = None
        if _qid_tag:
            _q_tag = store.sistema_quests.obtener_quest(_qid_tag)
            if _q_tag is not None:
                _linea = getattr(_q_tag, "linea", LINEA_PRINCIPAL)

        _icono = _ICONO_LINEA_QUEST.get(_linea)
        if _icono:
            return renpy.translate_string(" ({icono} Quest)").format(icono=_icono)
        return renpy.translate_string(" (Quest)")

    def actualizar_quests():
        """
        Actualiza el estado de todas las quests activas.
        Se llama al dormir para verificar tiempos de espera y avanzar etapas.
        Tambien verifica condiciones de fallo.
        """
        sistema_quests.actualizar_todas()
    
    def verificar_fallos_quests():
        """
        Verifica condiciones de fallo para todas las quests activas.
        Se llama al avanzar horario.
        """
        for quest in sistema_quests.quests.values():
            if quest.activa and not quest.completada:
                quest.verificar_fallo()
    
    def inicializar_todas_las_quests():
        """
        Arranca la primera quest de CADA linea de cada NPC.

        "Primera de la linea" = la que no declara quest_anterior: si nadie la
        encadena, es una apertura. Con eso alcanza para las tres lineas
        (principal / amor / deseo) sin que el motor conozca ningun id.

        Antes esto hardcodeaba las tres quests iniciales por nombre, lo que
        rompia la regla de que el motor no conoce contenido: agregar una linea
        obligaba a editar este archivo. Ahora agregar una linea es solo definir
        su primera quest sin quest_anterior.

        puede_iniciar() ya filtra las que estan activas o completadas, asi que
        es seguro llamarla en cada arranque.
        """
        for _quest in sistema_quests.quests.values():
            if _quest.quest_anterior:
                continue
            if _quest.puede_iniciar():
                _quest.iniciar()


################################################################################
## Labels de sistema de quests
################################################################################

# Label para ejecutar la quest activa del NPC
label ejecutar_quest_activa:
    # Obtener el NPC temporalmente almacenado
    $ npc_actual = obtener_npc(_npc_id_temp)
    
    if npc_actual:
        # Obtener la quest activa para este NPC
        $ quest = sistema_quests.obtener_quest_activa(npc_actual.id)
        
        if quest:
            # Construir el nombre del label de la quest
            $ label_quest = "quest_" + quest.id

            # Saltar al label de la quest SOLO si existe. Red de seguridad
            # universal (E03): una quest que llega al auto-trigger sin tener un
            # label 'quest_<id>' (porque usa triggers custom y se la olvidó de la
            # tupla de exclusión) tiraba LabelNotFound y crasheaba. Ahora se
            # ignora en silencio en vez de romper.
            # OJO: el label destino hereda el frame de este call-chain
            # (interaccion_<npc> se invoca con Call desde el HUD), asi que DEBE
            # terminar en `return`, nunca en `jump game_loop`.
            if renpy.has_label(label_quest):
                jump expression label_quest

    # Sin quest ni NPC: cerrar el frame con return. Antes hacia `jump game_loop`
    # y dejaba abierto el frame del Call("interaccion_<npc>"), acumulando uno
    # por interacción durante toda la partida.
    return

# Label para iniciar una quest desde el menú
label iniciar_quest_menu:
    $ quest = sistema_quests.obtener_quest(_quest_id_temp)
    
    if quest and quest.puede_iniciar():
        $ quest.iniciar()
    
    jump game_loop