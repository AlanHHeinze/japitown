################################################################################
## Sistema de Memorias del Jugador
################################################################################
## Sistema para almacenar decisiones y recuerdos que afectan el futuro del juego

# Diccionario global de memorias (se guarda con la partida)
default memorias_jugador = {}

init python:
    
    def guardar_memoria(categoria, clave, valor):
        """
        Guarda una memoria del jugador para referencia futura.
        
        Args:
            categoria: Categoría de la memoria (ej: "monica", "decisiones", "eventos")
            clave: Clave identificadora de la memoria
            valor: Valor a guardar (puede ser cualquier tipo)
        
        Ejemplo:
            guardar_memoria("monica", "primera_cita", "romantica")
            guardar_memoria("decisiones", "ayudo_jasmine_cocina", True)
        """
        if categoria not in store.memorias_jugador:
            store.memorias_jugador[categoria] = {}
        store.memorias_jugador[categoria][clave] = valor
        
        
    
    def obtener_memoria(categoria, clave, default=None):
        """
        Recupera una memoria guardada.
        
        Args:
            categoria: Categoría de la memoria
            clave: Clave de la memoria
            default: Valor por defecto si no existe
        
        Returns:
            El valor de la memoria o el default
        """
        return store.memorias_jugador.get(categoria, {}).get(clave, default)
    
    def tiene_memoria(categoria, clave, valor=None):
        """
        Verifica si existe una memoria (opcionalmente con un valor específico).
        
        Args:
            categoria: Categoría de la memoria
            clave: Clave de la memoria
            valor: Si se especifica, verifica que el valor coincida
        
        Returns:
            bool: True si la memoria existe (y coincide con el valor si se especificó)
        """
        mem = obtener_memoria(categoria, clave)
        if valor is None:
            return mem is not None
        return mem == valor
    
    def borrar_memoria(categoria, clave=None):
        """
        Borra una memoria o toda una categoría.
        
        Args:
            categoria: Categoría de la memoria
            clave: Si se especifica, borra solo esa clave. Si no, borra toda la categoría.
        """
        if categoria in store.memorias_jugador:
            if clave is None:
                del store.memorias_jugador[categoria]
            elif clave in store.memorias_jugador[categoria]:
                del store.memorias_jugador[categoria][clave]
    
    def obtener_todas_memorias(categoria=None):
        """
        Obtiene todas las memorias de una categoría o todas las memorias.
        
        Args:
            categoria: Si se especifica, retorna solo esas memorias
        
        Returns:
            Dict con las memorias
        """
        if categoria:
            return store.memorias_jugador.get(categoria, {}).copy()
        return store.memorias_jugador.copy()
    
    def contar_memorias(categoria=None):
        """
        Cuenta el número de memorias guardadas.
        
        Args:
            categoria: Si se especifica, cuenta solo esa categoría
        
        Returns:
            int: Número de memorias
        """
        if categoria:
            return len(store.memorias_jugador.get(categoria, {}))
        total = 0
        for cat in store.memorias_jugador.values():
            total += len(cat)
        return total
