################################################################################
## Sistema de Locaciones
################################################################################
## Sistema que trata cada locación como una instancia lógica persistente
## con estado propio, hotspots, y lógica de entrada/salida

init python:
    
    class Hotspot:
        """
        Representa un área interactiva en una locación.
        Puede ser de tipo MOVE (cambio de locación) o ACTION (accion sin movimiento)
        """
        def __init__(self, id, tipo, x, y, w, h, destino=None, accion=None, label=None, condicion=None, nombre="", label_offset_y=0):
            self.id = id
            self.tipo = tipo  # "MOVE" o "ACTION"
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.destino = destino  # ID de locación destino (solo para MOVE)
            self.accion = accion  # Función a ejecutar (solo para ACTION)
            self.label = label  # Label a llamar (alternativa a accion)
            self.condicion = condicion  # Función que retorna True/False para habilitar
            self.nombre = nombre  # Nombre descriptivo del hotspot
            self.label_offset_y = label_offset_y  # Desplazamiento vertical del label fijo
        
        def esta_habilitado(self):
            """Verifica si el hotspot está habilitado según su condición"""
            if self.condicion is None:
                return True
            return self.condicion()
        
        def contiene_punto(self, px, py):
            """Verifica si un punto está dentro del hotspot"""
            return (self.x <= px <= self.x + self.w and 
                    self.y <= py <= self.y + self.h)
    
    class Locacion:
        """
        Representa una locación del juego como instancia lógica persistente.
        Mantiene estado propio y ejecuta lógica al entrar/salir.
        """
        def __init__(self, id, nombre, background_base, descripcion=""):
            self.id = id
            self.nombre = nombre
            self.background_base = background_base  # Base del path sin horario (ej: "images/bg/casa/bg_casa_{horario}_frente.png")
            self.descripcion = descripcion
            self.hotspots = []
            self.personajes_presentes = []
            self.estado = {}  # Estado propio de la locación
            self.visitada = False
            self.veces_visitada = 0
        
        @property
        def background(self):
            """Retorna el background dinámico según el horario actual"""
            return self.obtener_background_por_horario()
        
        def obtener_background_por_horario(self, horario_override=None):
            """
            Genera el path del background según el horario actual o especificado.
            
            Args:
                horario_override: Horario específico (0-3) o None para usar el actual
            
            Returns:
                String con el path del background
            """
            # Mapeo de índices de horario a nombres
            horarios_nombres = ["mañana", "tarde", "noche", "trasnoche"]
            
            # Usar horario especificado o el actual
            if horario_override is not None:
                horario_idx = horario_override
            else:
                horario_idx = getattr(store, 'horario_actual', 0)
            
            # Asegurar que el índice esté en rango válido
            horario_idx = max(0, min(3, horario_idx))
            horario_nombre = horarios_nombres[horario_idx]
            
            # Generar el path del background
            return self.background_base.format(horario=horario_nombre)
        
        def agregar_hotspot(self, hotspot):
            """Agrega un hotspot a la locación"""
            self.hotspots.append(hotspot)
        
        def obtener_hotspot(self, id):
            """Obtiene un hotspot por su ID"""
            for hotspot in self.hotspots:
                if hotspot.id == id:
                    return hotspot
            return None
        
        def obtener_hotspots_habilitados(self):
            """Retorna lista de hotspots habilitados"""
            return [h for h in self.hotspots if h.esta_habilitado()]
        
        def on_enter(self):
            """Lógica ejecutada al entrar a la locación"""
            self.visitada = True
            self.veces_visitada += 1
            # Override en subclases para lógica específica
        
        def on_exit(self):
            """Lógica ejecutada al salir de la locación"""
            # Override en subclases para lógica específica
            pass
        
        def agregar_personaje(self, personaje_id):
            """Agrega un personaje a la locación"""
            if personaje_id not in self.personajes_presentes:
                self.personajes_presentes.append(personaje_id)
        
        def remover_personaje(self, personaje_id):
            """Remueve un personaje de la locación"""
            if personaje_id in self.personajes_presentes:
                self.personajes_presentes.remove(personaje_id)
        
        def tiene_personaje(self, personaje_id):
            """Verifica si un personaje está presente"""
            return personaje_id in self.personajes_presentes

    class SistemaLocaciones:
        """
        Gestor central del sistema de locaciones.
        Maneja el cambio de locaciones y el flujo de entrada/salida.
        """
        def __init__(self):
            self.locaciones = {}
            self.locacion_actual = None
            self.locacion_anterior = None
        
        def registrar_locacion(self, locacion):
            """Registra una locación en el sistema"""
            self.locaciones[locacion.id] = locacion
        
        def obtener_locacion(self, id):
            """Obtiene una locación por su ID"""
            return self.locaciones.get(id)
        
        def validar_movimiento(self, destino_id):
            """
            Valida si el movimiento a una locación está permitido.
            Override este método para agregar validaciones personalizadas.
            """
            # Validación básica: la locación destino existe
            if destino_id not in self.locaciones:
                return False, "Locación no existe"
            
            # Aqui se pueden agregar más validaciones según el estado del juego
            # Por ejemplo: verificar si el jugador tiene una llave, si es el horario correcto, etc.
            
            return True, ""
        
        def mover_a_locacion(self, destino_id):
            """
            Ejecuta el flujo completo de movimiento entre locaciones:
            1. Validar movimiento
            2. Ejecutar lógica de salida
            3. Cambiar locación activa
            4. Ejecutar lógica de entrada
            5. Renderizar background
            6. Activar hotspots
            """
            # 1. Validar movimiento
            valido, mensaje = self.validar_movimiento(destino_id)
            if not valido:
                return False
            
            destino = self.locaciones[destino_id]
            
            # 2. Ejecutar lógica de salida de locación actual
            if self.locacion_actual:
                self.locacion_actual.on_exit()
                retornar_npcs_pasillo_al_salir(self.locacion_actual.id)
            
            # 3. Cambiar locación activa
            self.locacion_anterior = self.locacion_actual
            self.locacion_actual = destino
            
            # 4. Ejecutar lógica de entrada de nueva locación
            destino.on_enter()
            
            # 5. Background se actualiza en game_loop via actualizar_bg_master()
            # 6. Activar hotspots (se hace en el screen)

            return True
        
        def ejecutar_accion_hotspot(self, hotspot):
            """Ejecuta la acción de un hotspot ACTION"""
            if hotspot.tipo != "ACTION":
                return
            
            if hotspot.accion:
                hotspot.accion()
            elif hotspot.label:
                renpy.call(hotspot.label)
        
        def obtener_hotspot_en_posicion(self, x, y):
            """Obtiene el hotspot en una posición específica de la locación actual"""
            if not self.locacion_actual:
                return None
            
            for hotspot in self.locacion_actual.obtener_hotspots_habilitados():
                if hotspot.contiene_punto(x, y):
                    return hotspot
            
            return None

# Instancia global del sistema de locaciones
default sistema_locaciones = SistemaLocaciones()

################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def ir_a_locacion(destino_id):
        """Función helper para mover a una locación"""
        return sistema_locaciones.mover_a_locacion(destino_id)
    
    def locacion_actual():
        """Retorna la locación actual"""
        return sistema_locaciones.locacion_actual
    
    def locacion_anterior():
        """Retorna la locación anterior"""
        return sistema_locaciones.locacion_anterior
    
    def esta_en_locacion(locacion_id):
        """Verifica si el jugador está en una locación específica"""
        return (sistema_locaciones.locacion_actual and 
                sistema_locaciones.locacion_actual.id == locacion_id)
    
    def ir_a_locacion(locacion_id):
        """
        Función de acceso rapido para ir directamente a una locación.
        Útil para botones de acceso rapido en el HUD.
        """
        if sistema_locaciones.mover_a_locacion(locacion_id):
            pass
            # Refrescar el screen para mostrar la nueva locación
            renpy.restart_interaction()
        else:
            pass
