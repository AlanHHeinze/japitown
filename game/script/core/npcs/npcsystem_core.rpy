################################################################################
## Sistema de NPCs
################################################################################
## Sistema para gestionar personajes no jugables con rutinas dinámicas

init python:

    class RutinaEspecial:
        """
        Actividad opcional que un NPC puede realizar en un slot de horario dado.
        Se evalúa al inicio de cada dia. Tiene prioridad sobre la rutina base,
        pero es subordinada a overrides de quests y eventos.
        """
        def __init__(self, id, locacion, sprite, posicion,
                     probabilidad=0.3,
                     horarios=None,
                     dias=None,
                     condicion=None,
                     nombre=""):
            self.id = id
            self.locacion = locacion
            self.sprite = sprite
            self.posicion = posicion
            self.probabilidad = probabilidad
            self.horarios = horarios    # None = todos; lista = slots válidos [0,1,2,3]
            self.dias = dias            # None = todos; lista = dias válidos [0-6]
            self.condicion = condicion  # lambda → bool, o None
            self.nombre = nombre

        def es_candidata(self, dia, horario):
            if self.dias is not None and dia not in self.dias:
                return False
            if self.horarios is not None and horario not in self.horarios:
                return False
            if self.condicion is not None:
                try:
                    return bool(self.condicion())
                except:
                    return False
            return True

    class NPC:
        """
        Clase base para personajes no jugables.
        Cada NPC tiene rutinas, estado y puede estar en diferentes locaciones.
        Stats configurables por NPC (ej: amor/deseo)
        """
        
        def __init__(self, id, nombre, nombre_completo="", sprite=None, nombre_stat1="amor", nombre_stat2="deseo"):
            self.id = id
            self.nombre = nombre
            self.nombre_completo = nombre_completo if nombre_completo else nombre
            
            # Nombres de stats específicos de este NPC
            self.nombre_stat1 = nombre_stat1
            self.nombre_stat2 = nombre_stat2
            
            # Sprite del NPC
            self.sprite = sprite
            
            # Ubicación actual
            self.locacion_actual = None
            
            # Rutinas: diccionario de horarios y dias
            self.rutinas = {}
            
            # Estado del NPC (usa nombres de stat configurables)
            self.estado = {
                nombre_stat1: 0,    # Stat principal: amor
                nombre_stat2: 0,    # Stat secundario: deseo
                "progreso": 0,      # Progreso de quests (oculto al jugador)
                "conocido": False,  # Si el jugador ya conoce al NPC
                "disponible": True, # Si está disponible para interactuar
            }
            
            # Interacciones diarias (se resetean cada dia)
            self.interacciones_hoy = {
                "hablar": False,  # Si ya habló hoy
                "coquetear": False,  # Si ya coqueteó hoy
            }

            # Sistema de talk
            self.talk_estado_id = None           # ID del estado general activo hoy
            self.talk_estados_especiales = []    # Lista de EstadoTalkActivo
            self.talk_reconsiderar_usado = False # Resetea por interacción
            self.estado_posterior_id = None      # Estado asignado post-interacción
            
            # Atributos personalizables
            self.atributos = {}

            # Lista de desbloqueos por stat (amor/deseo)
            self.desbloqueos = []

            # Quests relacionadas con este NPC
            self.quests = []
            
            # Eventos especiales
            self.eventos = []
            
            # Diálogos
            self.dialogos = {}

            # Rutinas especiales dinámicas
            self.rutinas_especiales = []
            self._rutina_especial_dia = {}   # {horario: RutinaEspecial|None} — resultado diario

            # Overrides de rutina aplicados por quests activas
            self.rutinas_quest = {}          # {(dia, horario): locacion_id}

        def establecer_rutina(self, dia_semana, horario, locacion_id):
            """
            Establece la rutina del NPC para un dia y horario específico.
            
            Args:
                dia_semana: Índice del dia (0=Lunes, 6=Domingo) o "todos"
                horario: Índice del horario (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
                locacion_id: ID de la locación donde estará el NPC
            """
            if dia_semana == "todos":
                # Aplicar a todos los dias
                for dia in range(7):
                    clave = (dia, horario)
                    self.rutinas[clave] = locacion_id
            else:
                clave = (dia_semana, horario)
                self.rutinas[clave] = locacion_id
        
        def agregar_desbloqueo(self, stat, umbral, icono, nombre, desc="",
                               condicion_extra=None, nombre_pendiente=None):
            self.desbloqueos.append({
                "stat":             stat,
                "umbral":           umbral,
                "icono":            icono,
                "nombre":           nombre,
                "desc":             desc,
                "condicion_extra":  condicion_extra,
                "nombre_pendiente": nombre_pendiente,
            })

        def agregar_rutina_especial(self, rutina_especial):
            if not hasattr(self, 'rutinas_especiales'):
                self.rutinas_especiales = []
            self.rutinas_especiales.append(rutina_especial)

        def evaluar_rutinas_especiales_dia(self, dia):
            """Evalúa qué rutinas especiales se activan para cada slot del día dado."""
            rutinas = getattr(self, 'rutinas_especiales', [])
            dias_hoy = getattr(store, 'dias_totales', 0)

            if not hasattr(self, '_rutina_cooldown'):
                self._rutina_cooldown = {}

            _loc_fuera = "fuera"
            _loc_banio = {"casa_banioarriba", "casa_baniomonica", "casa_banioabajo"}

            self._rutina_especial_dia = {}
            for horario in range(4):
                candidatas = [r for r in rutinas if r.es_candidata(dia, horario)]
                # Excluir rutinas "fuera" y "baño" que estén en cooldown (< 2 dias)
                candidatas = [
                    r for r in candidatas
                    if (r.locacion != _loc_fuera and r.locacion not in _loc_banio)
                    or dias_hoy - self._rutina_cooldown.get(r.id, -99) >= 2
                ]
                renpy.random.shuffle(candidatas)
                activa = None
                for candidata in candidatas:
                    if renpy.random.random() < candidata.probabilidad:
                        activa = candidata
                        break
                self._rutina_especial_dia[horario] = activa

            # Restricción: no puede tener "fuera" Y "baño" el mismo dia
            slots_fuera = [h for h, r in self._rutina_especial_dia.items()
                           if r and r.locacion == _loc_fuera]
            slots_banio = [h for h, r in self._rutina_especial_dia.items()
                           if r and r.locacion in _loc_banio]

            if slots_fuera and slots_banio:
                # Cancelar uno de los dos aleatoriamente
                if renpy.random.random() < 0.5:
                    for h in slots_fuera:
                        self._rutina_especial_dia[h] = None
                else:
                    for h in slots_banio:
                        self._rutina_especial_dia[h] = None

            # Registrar cooldown para las rutinas "fuera"/"baño" que quedaron activas
            for rutina in self._rutina_especial_dia.values():
                if rutina and (rutina.locacion == _loc_fuera or rutina.locacion in _loc_banio):
                    self._rutina_cooldown[rutina.id] = dias_hoy

        def obtener_rutina_especial_actual(self, horario=None):
            if horario is None and hasattr(store, 'horario_actual'):
                horario = store.horario_actual
            return getattr(self, '_rutina_especial_dia', {}).get(horario, None)

        def obtener_visual_rutina_especial(self, horario=None):
            """Retorna (sprite, posicion) de la rutina especial activa, o None."""
            rutina = self.obtener_rutina_especial_actual(horario)
            if rutina:
                return (rutina.sprite, rutina.posicion)
            return None

        def obtener_locacion_rutina(self, dia_semana=None, horario=None):
            """
            Obtiene la locación donde deberia estar el NPC según su rutina.
            Prioridad: 1) Override de evento, 2) Rutina de quest, 3) Rutina especial, 4) Rutina base
            """
            # Usar tiempo actual si no se especifica
            if dia_semana is None and hasattr(store, 'dia_semana_actual'):
                dia_semana = store.dia_semana_actual
            if horario is None and hasattr(store, 'horario_actual'):
                horario = store.horario_actual

            clave = (dia_semana, horario)

            # Prioridad 1: Override de evento
            if hasattr(store, 'sistema_events'):
                override = store.sistema_events.obtener_override_rutina(self.id, dia_semana, horario)
                if override:
                    return override

            # Prioridad 2: Rutina de quest activa (manda sobre especiales)
            rutinas_q = getattr(self, 'rutinas_quest', {})
            if clave in rutinas_q:
                return rutinas_q[clave]

            # Prioridad 3: Rutina especial del dia (fuera/baño)
            rutina_esp = self.obtener_rutina_especial_actual(horario)
            if rutina_esp:
                return rutina_esp.locacion

            # Prioridad 4: Rutina base
            return self.rutinas.get(clave, None)

        
        def actualizar_ubicacion(self):
            """
            Actualiza la ubicación del NPC según su rutina actual.
            Debe llamarse cuando cambia el tiempo.
            """
            nueva_locacion = self.obtener_locacion_rutina()

            if nueva_locacion and nueva_locacion != self.locacion_actual:
                # Remover de locación anterior
                if self.locacion_actual and hasattr(store, 'sistema_locaciones'):
                    loc_anterior = store.sistema_locaciones.obtener_locacion(self.locacion_actual)
                    if loc_anterior:
                        loc_anterior.remover_personaje(self.id)

                # Agregar a nueva locación
                if hasattr(store, 'sistema_locaciones'):
                    loc_nueva = store.sistema_locaciones.obtener_locacion(nueva_locacion)
                    if loc_nueva:
                        loc_nueva.agregar_personaje(self.id)

                # Sincronizar disponibilidad al cruzar el estado "fuera"
                if nueva_locacion == "fuera" and self.locacion_actual != "fuera":
                    self.estado["disponible"] = False
                elif nueva_locacion != "fuera" and self.locacion_actual == "fuera":
                    self.estado["disponible"] = True

                self.locacion_actual = nueva_locacion
        
        def esta_en_locacion(self, locacion_id):
            """Verifica si el NPC está en una locación específica"""
            return self.locacion_actual == locacion_id
        
        def cambiar_estado(self, clave, valor):
            """Cambia un valor del estado del NPC"""
            self.estado[clave] = valor
        
        def obtener_estado(self, clave, default=None):
            """Obtiene un valor del estado del NPC"""
            return self.estado.get(clave, default)
        
        def agregar_atributo(self, clave, valor):
            """Agrega un atributo personalizado al NPC"""
            self.atributos[clave] = valor
        
        def obtener_atributo(self, clave, default=None):
            """Obtiene un atributo personalizado del NPC"""
            return self.atributos.get(clave, default)
        
        def modificar_stat1(self, cantidad):
            """Modifica el stat principal del NPC y sincroniza con variables default"""
            self.estado[self.nombre_stat1] += cantidad
            self.estado[self.nombre_stat1] = max(0, min(100, self.estado[self.nombre_stat1]))
            
            # Sincronizar con variable default guardable: {npc_id}_{nombre_stat1}
            var_name = f"{self.id}_{self.nombre_stat1}"
            setattr(store, var_name, self.estado[self.nombre_stat1])
            
            # Notificación visual
            if hasattr(store, 'notificar_cambio_stat'):
                notificar_cambio_stat(self.nombre_stat1, cantidad, self.nombre)
        
        def modificar_stat2(self, cantidad):
            """Modifica el stat secundario del NPC y sincroniza con variables default"""
            self.estado[self.nombre_stat2] += cantidad
            self.estado[self.nombre_stat2] = max(0, min(100, self.estado[self.nombre_stat2]))

            # Sincronizar con variable default guardable: {npc_id}_{nombre_stat2}
            var_name = f"{self.id}_{self.nombre_stat2}"
            setattr(store, var_name, self.estado[self.nombre_stat2])
            
            # Notificación visual
            if hasattr(store, 'notificar_cambio_stat'):
                notificar_cambio_stat(self.nombre_stat2, cantidad, self.nombre)

        def modificar_stat(self, stat, cantidad):
            """Dispatcher: modifica el stat indicado por nombre"""
            if stat == self.nombre_stat1:
                self.modificar_stat1(cantidad)
            elif stat == self.nombre_stat2:
                self.modificar_stat2(cantidad)

        def establecer_stat1(self, valor):
            """Fija el stat principal a un valor absoluto sincronizando el store.

            Usar esto (no estado[...] directo) para no desincronizar la variable
            guardable {npc_id}_{nombre_stat1}, que varios sistemas leen aparte de estado.
            """
            self.estado[self.nombre_stat1] = max(0, min(100, valor))
            setattr(store, f"{self.id}_{self.nombre_stat1}", self.estado[self.nombre_stat1])

        def establecer_stat2(self, valor):
            """Fija el stat secundario a un valor absoluto sincronizando el store."""
            self.estado[self.nombre_stat2] = max(0, min(100, valor))
            setattr(store, f"{self.id}_{self.nombre_stat2}", self.estado[self.nombre_stat2])

        def modificar_progreso(self, cantidad):
            """Modifica el progreso del NPC y sincroniza con variables default"""
            self.estado["progreso"] += cantidad
            self.estado["progreso"] = max(0, self.estado["progreso"])
            
            # Sincronizar con variable default guardable: {npc_id}_progreso
            var_name = f"{self.id}_progreso"
            setattr(store, var_name, self.estado["progreso"])

        def obtener_relacion_total(self):
            """Retorna la relación total: stat1 + stat2 + progreso"""
            return self.estado.get(self.nombre_stat1, 0) + self.estado.get(self.nombre_stat2, 0) + self.estado.get("progreso", 0)

        def resetear_interacciones_diarias(self):
            """Resetea las interacciones diarias (llamar al dormir)"""
            self.interacciones_hoy = {
                "hablar": False,
                "coquetear": False,
            }
        
        def puede_interactuar(self, tipo_interaccion):
            """Verifica si se puede realizar una interacción específica hoy"""
            return not self.interacciones_hoy.get(tipo_interaccion, False)
        
        def registrar_interaccion(self, tipo_interaccion):
            """Registra que se realizó una interacción hoy"""
            self.interacciones_hoy[tipo_interaccion] = True

    class SistemaNPCs:
        """
        Gestor central del sistema de NPCs.
        Maneja todos los NPCs y sus rutinas.
        """
        
        def __init__(self):
            self.npcs = {}
        
        def registrar_npc(self, npc):
            """Registra un NPC en el sistema"""
            self.npcs[npc.id] = npc
        
        def obtener_npc(self, npc_id):
            """Obtiene un NPC por su ID"""
            return self.npcs.get(npc_id)
        
        def actualizar_todas_ubicaciones(self):
            """Actualiza las ubicaciones de todos los NPCs según sus rutinas"""
            for npc in self.npcs.values():
                npc.actualizar_ubicacion()

        def evaluar_todas_rutinas_especiales_dia(self, dia):
            """Evalúa las rutinas especiales de todos los NPCs y resuelve conflictos."""
            for npc in self.npcs.values():
                npc.evaluar_rutinas_especiales_dia(dia)
            self._resolver_conflictos_banio()

        def _resolver_conflictos_banio(self):
            """Si Violet y Jasmine tienen ducha asignada al mismo horario, solo una la usa."""
            violet = self.npcs.get("violet")
            jasmine = self.npcs.get("jasmine")
            if not violet or not jasmine:
                return
            for horario in range(4):
                v_rutina = getattr(violet, '_rutina_especial_dia', {}).get(horario)
                j_rutina = getattr(jasmine, '_rutina_especial_dia', {}).get(horario)
                if (v_rutina and v_rutina.locacion == "casa_banioarriba" and
                        j_rutina and j_rutina.locacion == "casa_banioarriba"):
                    if renpy.random.random() < 0.5:
                        violet._rutina_especial_dia[horario] = None
                    else:
                        jasmine._rutina_especial_dia[horario] = None
        
        def obtener_npcs_en_locacion(self, locacion_id):
            """Obtiene lista de NPCs en una locación específica"""
            npcs_en_locacion = []
            for npc in self.npcs.values():
                if npc.esta_en_locacion(locacion_id):
                    npcs_en_locacion.append(npc)
            return npcs_en_locacion
        
        def obtener_npc_en_locacion_actual(self):
            """Obtiene NPCs en la locación actual del jugador"""
            if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
                return self.obtener_npcs_en_locacion(store.sistema_locaciones.locacion_actual.id)
            return []

# Instancia global del sistema de NPCs
default sistema_npcs = SistemaNPCs()

################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def obtener_npc(npc_id):
        """Función helper para obtener un NPC"""
        return sistema_npcs.obtener_npc(npc_id)

    def obtener_stat1(npc_id):
        """Obtiene el valor del stat principal de un NPC"""
        npc = obtener_npc(npc_id)
        if npc:
            return npc.obtener_estado(npc.nombre_stat1, 0)
        return 0

    def obtener_stat2(npc_id):
        """Obtiene el valor del stat secundario de un NPC"""
        npc = obtener_npc(npc_id)
        if npc:
            return npc.obtener_estado(npc.nombre_stat2, 0)
        return 0

    def cambiar_stat1(npc_id, cantidad):
        """Modifica el stat principal de un NPC"""
        npc = obtener_npc(npc_id)
        if npc:
            npc.modificar_stat1(cantidad)

    def cambiar_stat2(npc_id, cantidad):
        """Modifica el stat secundario de un NPC"""
        npc = obtener_npc(npc_id)
        if npc:
            npc.modificar_stat2(cantidad)

    def obtener_progreso(npc_id):
        """Obtiene el valor de progreso de un NPC"""
        npc = obtener_npc(npc_id)
        if npc:
            return npc.obtener_estado("progreso", 0)
        return 0

    def obtener_relacion_total(npc_id):
        """Obtiene la relación total de un NPC (stat1 + stat2 + progreso)"""
        npc = obtener_npc(npc_id)
        if npc:
            return npc.obtener_relacion_total()
        return 0

    def incrementar_progreso(npc_id, cantidad=1):
        """Incrementa el progreso de un NPC"""
        npc = obtener_npc(npc_id)
        if npc:
            npc.modificar_progreso(cantidad)

    def formatear_opcion_recompensa(texto, stat):
        """
        Agrega un emoji al final del texto si el cheat 'Mostrar recompensa' está activo.
        Stat1 (cualquier nombre) = 😊, Stat2 (cualquier nombre) = 🔥
        """
        if getattr(persistent, "mostrar_recompensa", False):
            if stat == "deseo":
                return f"{texto} 💋"
            elif stat == "amor":
                return f"{texto} ❤️"
        return texto

    
    def npcs_en_locacion_actual():
        """Retorna lista de NPCs en la locación actual"""
        return sistema_npcs.obtener_npc_en_locacion_actual()
    
    def actualizar_rutinas_npcs():
        """Actualiza las ubicaciones de todos los NPCs"""
        sistema_npcs.actualizar_todas_ubicaciones()

    def obtener_visual_npc_rutina_especial(npc_id, horario=None):
        """Retorna (sprite, posicion) de la rutina especial activa del NPC, o None."""
        npc = obtener_npc(npc_id)
        if npc:
            return npc.obtener_visual_rutina_especial(horario)
        return None
    
    def resetear_interacciones_todos_npcs():
        """Resetea las interacciones diarias de todos los NPCs"""
        # Resetear variables guardables (store)
        store.monica_interacciones = {"hablar": False, "coquetear": False}
        store.jasmine_interacciones = {"hablar": False, "coquetear": False}
        store.violet_interacciones = {"hablar": False, "coquetear": False}

        # Resetear objetos NPC (interacciones_hoy en memoria)
        for npc in sistema_npcs.npcs.values():
            npc.resetear_interacciones_diarias()
    
    def interactuar_con_npc(npc_id, tipo_interaccion):
        """
        Realiza una interacción con un NPC.
        tipo_interaccion: "hablar", "coquetear"
        """
        # Obtener datos de interacciones
        interacciones = None
        if npc_id == "monica":
            interacciones = store.monica_interacciones
        elif npc_id == "jasmine":
            interacciones = store.jasmine_interacciones
        elif npc_id == "violet":
            interacciones = store.violet_interacciones
        
        if not interacciones:
            return False
        
        # Verificar si ya interactuó hoy
        if interacciones.get(tipo_interaccion, False):
            return False
        
        # Realizar la interacción
        if tipo_interaccion == "hablar":
            cambiar_stat1(npc_id, 1)
        elif tipo_interaccion == "coquetear":
            cambiar_stat2(npc_id, 1)
        
        # Registrar la interacción
        interacciones[tipo_interaccion] = True
        
        return True
    
    def obtener_posiciones_npcs(num_npcs):
        """
        Calcula posiciones para distribuir NPCs en la pantalla.
        Retorna lista de tuplas (xalign, yalign) para cada NPC.
        yalign = 1.0 para que toquen el borde inferior (posición 0 en altura)
        """
        if num_npcs == 0:
            return []
        elif num_npcs == 1:
            # Un solo NPC: centro
            return [(0.5, 1.0)]
        elif num_npcs == 2:
            # Dos NPCs: izquierda y derecha
            return [(0.35, 1.0), (0.65, 1.0)]
        elif num_npcs == 3:
            # Tres NPCs: izquierda, centro, derecha
            return [(0.25, 1.0), (0.5, 1.0), (0.75, 1.0)]
        else:
            # Más de 3: distribuir uniformemente
            spacing = 1.0 / (num_npcs + 1)
            return [(spacing * (i + 1), 1.0) for i in range(num_npcs)]
    
    def inicializar_npcs_casa():
        """
        Inicializa todos los NPCs de la casa.
        Llama a las funciones de inicialización de cada NPC.
        """
        # Inicializar cada NPC de la casa
        inicializar_monica()
        inicializar_jasmine()
        inicializar_violet()
        
        # Actualizar ubicaciones según rutinas
        sistema_npcs.actualizar_todas_ubicaciones()
        


