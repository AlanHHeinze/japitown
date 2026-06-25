################################################################################
## Sistema de Validaciones de Movimiento
################################################################################
## Extensión del sistema de locaciones para agregar validaciones personalizadas

init python:
    
    class ValidadorMovimiento:
        """
        Clase base para validadores de movimiento.
        Permite crear reglas complejas para permitir o denegar movimientos.
        """
        
        def __init__(self, nombre):
            self.nombre = nombre
        
        def validar(self, origen, destino):
            """
            Valida si el movimiento es permitido.
            Retorna (bool, str): (es_valido, mensaje_error)
            """
            return True, ""
    
    class ValidadorHorario(ValidadorMovimiento):
        """Valida movimientos según el horario del día"""
        
        def __init__(self, horarios_permitidos):
            super(ValidadorHorario, self).__init__("ValidadorHorario")
            self.horarios_permitidos = horarios_permitidos
        
        def validar(self, origen, destino):
            # Verificar si existe el sistema de tiempo
            if not hasattr(store, 'horario_actual'):
                return True, ""
            
            if horario_actual not in self.horarios_permitidos:
                return False, "No puedes ir ahí a esta hora"
            
            return True, ""
    
    class ValidadorItem(ValidadorMovimiento):
        """Valida movimientos según items en el inventario"""
        
        def __init__(self, item_requerido):
            super(ValidadorItem, self).__init__("ValidadorItem")
            self.item_requerido = item_requerido
        
        def validar(self, origen, destino):
            # Aqui deberias verificar tu sistema de inventario
            # Ejemplo simplificado:
            if not hasattr(store, 'inventario'):
                return True, ""
            
            if self.item_requerido not in inventario:
                return False, f"Necesitas: {self.item_requerido}"
            
            return True, ""
    
    class ValidadorEstado(ValidadorMovimiento):
        """Valida movimientos según el estado del juego"""
        
        def __init__(self, condicion_func, mensaje_error):
            super(ValidadorEstado, self).__init__("ValidadorEstado")
            self.condicion_func = condicion_func
            self.mensaje_error = mensaje_error
        
        def validar(self, origen, destino):
            if not self.condicion_func():
                return False, self.mensaje_error
            return True, ""
    
    class ValidadorPersonaje(ValidadorMovimiento):
        """Valida movimientos según la presencia de personajes"""
        
        def __init__(self, personaje_id, debe_estar_presente=True):
            super(ValidadorPersonaje, self).__init__("ValidadorPersonaje")
            self.personaje_id = personaje_id
            self.debe_estar_presente = debe_estar_presente
        
        def validar(self, origen, destino):
            tiene_personaje = destino.tiene_personaje(self.personaje_id)
            
            if self.debe_estar_presente and not tiene_personaje:
                return False, "No hay nadie ahí"
            
            if not self.debe_estar_presente and tiene_personaje:
                return False, "No puedes entrar ahora"
            
            return True, ""

    # Extender el SistemaLocaciones con validaciones
    def validar_movimiento_extendido(self, destino_id):
        """
        Versión extendida de validar_movimiento que usa validadores.
        """
        # Verificar restricción de quest/evento
        _msg_restriccion = accion_bloqueada_movimiento(destino_id)
        if _msg_restriccion:
            pass
            return False, _msg_restriccion
        
        # Validación básica
        if destino_id not in self.locaciones:
            return False, "Locación no existe"
        
        destino = self.locaciones[destino_id]
        origen = self.locacion_actual
        
        # Ejecutar validadores registrados para este movimiento
        if hasattr(self, 'validadores'):
            clave = f"{origen.id if origen else 'none'}_{destino_id}"
            
            if clave in self.validadores:
                for validador in self.validadores[clave]:
                    valido, mensaje = validador.validar(origen, destino)
                    if not valido:
                        return False, mensaje
        
        return True, ""
    
    # Reemplazar el método de validación
    SistemaLocaciones.validar_movimiento = validar_movimiento_extendido
    
    # Agregar método para registrar validadores
    def registrar_validador(self, origen_id, destino_id, validador):
        """Registra un validador para un movimiento específico"""
        if not hasattr(self, 'validadores'):
            self.validadores = {}
        
        clave = f"{origen_id}_{destino_id}"
        
        if clave not in self.validadores:
            self.validadores[clave] = []
        
        self.validadores[clave].append(validador)
    
    SistemaLocaciones.registrar_validador = registrar_validador

################################################################################
## Funciones de utilidad para validaciones
################################################################################

init python:
    
    def _bloqueo_siempre_falso():
        return False

    def bloquear_movimiento(origen_id, destino_id, mensaje="No puedes ir ahí"):
        """Bloquea un movimiento específico"""
        validador = ValidadorEstado(
            condicion_func=_bloqueo_siempre_falso,
            mensaje_error=mensaje
        )
        sistema_locaciones.registrar_validador(origen_id, destino_id, validador)
    
    def desbloquear_movimiento(origen_id, destino_id):
        """Desbloquea un movimiento (remueve validadores)"""
        if hasattr(sistema_locaciones, 'validadores'):
            clave = f"{origen_id}_{destino_id}"
            if clave in sistema_locaciones.validadores:
                sistema_locaciones.validadores[clave] = []
    
    def requerir_item_para_movimiento(origen_id, destino_id, item):
        """Requiere un item para permitir un movimiento"""
        validador = ValidadorItem(item)
        sistema_locaciones.registrar_validador(origen_id, destino_id, validador)
    
    def requerir_horario_para_movimiento(origen_id, destino_id, horarios):
        """Requiere un horario específico para permitir un movimiento"""
        validador = ValidadorHorario(horarios)
        sistema_locaciones.registrar_validador(origen_id, destino_id, validador)

################################################################################
## Ejemplo de uso
################################################################################

# Ejemplo de cómo usar validaciones:
# 
# # Bloquear entrada a una locación hasta que se cumpla una condición
# $ bloquear_movimiento("casa_sala", "casa_dormitorio", "La puerta está cerrada")
# 
# # Requerir un item para entrar
# $ requerir_item_para_movimiento("casa_sala", "casa_sotano", "llave_sotano")
# 
# # Requerir horario específico
# $ requerir_horario_para_movimiento("casa_sala", "calle", [0, 1, 2])  # Solo mañana, tarde, noche
# 
# # Desbloquear cuando se cumpla la condición
# $ desbloquear_movimiento("casa_sala", "casa_dormitorio")
