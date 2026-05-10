################################################################################
## NPC: VIOLET
################################################################################
## Definición completa del personaje Violet


# Violet
define violet = Character("Violet", color="#956db3")

    # Violet - Susurro (texto en itálica y más claro para dar efecto de susurro)
define violet_susurro = Character("Violet", color="#956db3", what_prefix="{i}{color=#c8c8c8}", what_suffix="{/color}{/i}")

    # Violet - Pensando (texto en itálica con color diferente para pensamientos)
define violet_pensando = Character("Violet", color="#956db3", what_prefix="{i}{color=#a8b4c4}", what_suffix="{/color}{/i}")

init python:
    
    # Diccionario para almacenar sprites y posiciones de rutina de Violet
    # Clave: (dia_semana, horario) -> {"sprite": path, "posicion": (x, y)}
    violet_rutinas_visuales = {}
    
    def establecer_rutina_visual_violet(dia_semana, horario, sprite, posicion):
        """
        Establece el sprite y posición para una rutina específica de Violet.
        
        Args:
            dia_semana: Índice del día (0=Lunes, 6=Domingo) o lista de días
            horario: Índice del horario (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
            sprite: Ruta del sprite a mostrar
            posicion: Tupla (x, y) con la posición en pantalla
        """
        if isinstance(dia_semana, list):
            for dia in dia_semana:
                clave = (dia, horario)
                violet_rutinas_visuales[clave] = {
                    "sprite": sprite,
                    "posicion": posicion
                }
        else:
            clave = (dia_semana, horario)
            violet_rutinas_visuales[clave] = {
                "sprite": sprite,
                "posicion": posicion
            }
    
    def obtener_sprite_rutina_violet():
        """
        Obtiene el sprite actual de Violet según el día y horario actual.
        Prioridad: 1) Sprite idle del skin activo, 2) Rutina visual base
        Retorna None si no hay sprite definido para la rutina actual.
        """
        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            # Prioridad 1: Verificar sprite del skin activo basado en grupo de rutina
            sprite_skin = obtener_sprite_idle_rutina("violet")
            if sprite_skin:
                return sprite_skin
            
            # Prioridad 2: Rutina visual base
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = violet_rutinas_visuales.get(clave)
            if datos:
                return datos.get("sprite")
        return None
    
    def obtener_posicion_rutina_violet():
        """
        Obtiene la posición actual de Violet según el día y horario actual.
        Retorna None si no hay posición definida para la rutina actual.
        """
        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = violet_rutinas_visuales.get(clave)
            if datos:
                return datos.get("posicion")
        return None
    
    def inicializar_violet():
        """Inicializa el NPC Violet"""
        
        # Crear instancia del NPC
        violet = NPC(
            id="violet",
            nombre="Violet",
            nombre_completo="Violet",
            sprite="images/characters/casa/idle/idle_violet_casa_hviolet_trasnoche_rutinabase_skinbase.png",
            nombre_stat1="amor",
            nombre_stat2="deseo"
        )
        
        # =====================================================================
        # ESTADO INICIAL - Sincronizar con variables default guardables
        # =====================================================================
        
        # Sincronizar el objeto NPC con las variables guardables
        # Las variables default ya tienen los valores
        violet.estado["amor"] = store.violet_amor
        violet.estado["deseo"] = store.violet_deseo
        violet.estado["progreso"] = store.violet_progreso
        violet.estado["conocido"] = True
        
        # =====================================================================
        # ATRIBUTOS PERSONALIZADOS
        # =====================================================================
        # Agregar atributos
        violet.agregar_atributo("edad", "20")
        violet.agregar_atributo("ocupacion", "Estudiante universitaria")
        
        # =====================================================================
        # RUTINAS SEMANALES
        # =====================================================================
        
        # Lunes a Viernes
        for dia in range(5):
            violet.establecer_rutina(dia, 0, "casa_cocina")         # Mañana: Cocina
            violet.establecer_rutina(dia, 1, "casa_hviolet")        # Tarde: Su habitación (leyendo)
            violet.establecer_rutina(dia, 2, "casa_hviolet")        # Noche: Su habitación
            violet.establecer_rutina(dia, 3, "casa_hviolet")        # Trasnoche: Su habitación
        
        # Sábado
        violet.establecer_rutina(5, 0, "casa_hviolet")       # Mañana: Su habitación
        violet.establecer_rutina(5, 1, "casa_living")        # Tarde: Living (leyendo)
        violet.establecer_rutina(5, 2, "casa_hviolet")       # Noche: Su habitación
        violet.establecer_rutina(5, 3, "casa_hviolet")       # Trasnoche: Su habitación
        
        # Domingo
        violet.establecer_rutina(6, 0, "casa_cocina")        # Mañana: Cocina
        violet.establecer_rutina(6, 1, "casa_hviolet")       # Tarde: Su habitación
        violet.establecer_rutina(6, 2, "casa_living")        # Noche: Living
        violet.establecer_rutina(6, 3, "casa_hviolet")       # Trasnoche: Su habitación
        
        # =====================================================================
        # SPRITES Y POSICIONES DE RUTINA
        # =====================================================================
        # Cada rutina tiene un sprite específico y una posición personalizable
        
        # Lunes a Viernes + Domingo (0-4, 6) - Mañana en Cocina
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 6], 0,
            "images/characters/casa/idle/idle_violet_casa_cocina_mañana_rutinabase_grupobase_skinbase.png",
            (765, 1060)  # Posición personalizable
        )
        
        # Lunes a Viernes + Domingo (0-4, 6) - Tarde en H. Violet
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 6], 1,
            "images/characters/casa/idle/idle_violet_casa_hviolet_tarde_rutinabase_grupobase_skinbase.png",
            (721, 793)  # Posición personalizable
        )
        
        # Lunes a Sábado (0-5) - Noche en H. Violet
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 5], 2,
            "images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.png",
            (1558, 988)  # Posición personalizable
        )
        
        # Lunes a Domingo (0-6) - Trasnoche en H. Violet
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 5, 6], 3,
            "images/characters/casa/idle/idle_violet_casa_hviolet_trasnoche_rutinabase_grupobase_skinbase.png",
            (725, 862)  # Posición personalizable
        )
        
        # Sábado (5) - Mañana en H. Violet
        establecer_rutina_visual_violet(
            5, 0,
            "images/characters/casa/idle/idle_violet_casa_hviolet_mañana_rutinabase_grupobase_skinbase.png",
            (728, 815)  # Posición personalizable
        )
        
        # Sábado (5) - Tarde en Living
        establecer_rutina_visual_violet(
            5, 1,
            "images/characters/casa/idle/idle_violet_casa_living_tarde_rutinabase_grupobase_skinbase.png",
            (648, 816)  # Posición personalizable
        )
        
        # Domingo (6) - Noche en Living
        establecer_rutina_visual_violet(
            6, 2,
            "images/characters/casa/idle/idle_violet_casa_living_noche_rutinabase_grupobase_skinbase.png",
            (648, 994)  # Posición personalizable
        )
        
        # =====================================================================
        # REGISTRAR EN EL SISTEMA
        # =====================================================================
        
        sistema_npcs.registrar_npc(violet)
        
        return violet

################################################################################
## DIÁLOGOS DE VIOLET
################################################################################

# Aquí se pueden agregar diálogos específicos de Violet en el futuro

################################################################################
## EVENTOS DE VIOLET
################################################################################

# Aquí se pueden agregar eventos específicos de Violet en el futuro

################################################################################
## QUESTS DE VIOLET
################################################################################

# Aquí se pueden agregar quests específicas de Violet en el futuro

################################################################################
## Datos de Violet (Guardables)
################################################################################

default violet_amor = 0
default violet_deseo = 0
default violet_progreso = 0
default violet_interacciones = {"hablar": False, "coquetear": False}
default violet_quest2_trajesexy = False
default vq4_rama_elegida = None
