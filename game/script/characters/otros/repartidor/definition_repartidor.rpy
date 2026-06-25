################################################################################
## Definición del Repartidor
################################################################################
## NPC de entregas con sistema de confianza progresiva

################################################################################
## Character Definition
################################################################################

define repartidor = Character("Repartidor", color="#8B4513", what_color="#FFFFFF")


################################################################################
## Variables de estado del repartidor
################################################################################

# Confianza acumulada con el repartidor (aumenta 1 por cada entrega)
default repartidor_confianza = 0


################################################################################
## Funciones del repartidor
################################################################################

init python:
    
    def repartidor_en_puerta():
        """
        Verifica si el repartidor está en la puerta.
        Solo aparece en la mañana si hay entregas pendientes.
        """
        return store.repartidor_presente and store.horario_actual == 0
    
    def aumentar_confianza_repartidor():
        """Aumenta la confianza con el repartidor en 1."""
        store.repartidor_confianza += 1
    
    def obtener_label_entrega():
        """
        Obtiene el label de entrega según el nivel de confianza.
        Verifica primero si hay entregas de quest pendientes.

        - Quest delivery: Label especifico de quest
        - Confianza 0: Primera entrega
        - Confianza 1-5: Entregas iniciales
        - Confianza > 5: Entregas frecuentes
        """
        # Entregas de quest tienen prioridad
        if getattr(store, 'violet_quest1_entrega_pendiente', False) and not getattr(store, 'violet_quest1_en_cama', False):
            return "paqueterepartidor_quest01_violet"

        confianza = store.repartidor_confianza

        if confianza == 0:
            return "entrega_repartidor_0"
        elif confianza <= 5:
            return "entrega_repartidor_1_5"
        else:
            return "entrega_repartidor_5_plus"
    
    def procesar_entrega_repartidor():
        """
        Procesa la entrega del repartidor.
        Aumenta confianza, entrega items al inventario y limpia el estado.
        """
        # Unificar todas las entregas del dia
        items = sistema_compras.unificar_entregas_hoy()
        
        # Entregar al inventario
        sistema_compras.entregar_items_a_inventario(items)
        
        # Marcar órdenes como entregadas
        sistema_compras.marcar_entregas_hoy_como_entregadas()
        
        # Aumentar confianza
        aumentar_confianza_repartidor()
        
        # El repartidor se va
        store.repartidor_presente = False
        
        return items
