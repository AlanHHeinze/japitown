################################################################################
## NPC: JASMINE
################################################################################
## Definición completa del personaje Jasmine

    # Jasmine
define jasmine = Character("Jasmine", color="#D4A574")

    # Jasmine - Susurro (texto en itálica y más claro para dar efecto de susurro)
define jasmine_susurro = Character("Jasmine", color="#D4A574", what_prefix="{i}{color=#c8c8c8}", what_suffix="{/color}{/i}")

    # Jasmine - Pensando (texto en itálica con color diferente para pensamientos)
define jasmine_pensando = Character("Jasmine", color="#D4A574", what_prefix="{i}{color=#a8b4c4}", what_suffix="{/color}{/i}")

init python:
    
    # Diccionario para almacenar sprites y posiciones de rutina de Jasmine
    # Clave: (dia_semana, horario) -> {"sprite": path, "posicion": (x, y)}
    jasmine_rutinas_visuales = {}
    
    def establecer_rutina_visual_jasmine(dia_semana, horario, sprite, posicion):
        """
        Establece el sprite y posición para una rutina específica de Jasmine.
        
        Args:
            dia_semana: Índice del día (0=Lunes, 6=Domingo) o lista de días
            horario: Índice del horario (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
            sprite: Ruta del sprite a mostrar
            posicion: Tupla (x, y) con la posición en pantalla
        """
        if isinstance(dia_semana, list):
            for dia in dia_semana:
                clave = (dia, horario)
                jasmine_rutinas_visuales[clave] = {
                    "sprite": sprite,
                    "posicion": posicion
                }
        else:
            clave = (dia_semana, horario)
            jasmine_rutinas_visuales[clave] = {
                "sprite": sprite,
                "posicion": posicion
            }
    
    def obtener_sprite_rutina_jasmine():
        """
        Obtiene el sprite actual de Jasmine según el día y horario actual.
        Prioridad: 1) Sprite idle del skin activo, 2) Rutina visual base
        Retorna None si no hay sprite definido para la rutina actual.
        """
        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            # Prioridad 1: Verificar sprite del skin activo basado en grupo de rutina
            sprite_skin = obtener_sprite_idle_rutina("jasmine")
            if sprite_skin:
                return sprite_skin
            
            # Prioridad 2: Rutina visual base
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = jasmine_rutinas_visuales.get(clave)
            if datos:
                return datos.get("sprite")
        return None
    
    def obtener_posicion_rutina_jasmine():
        """
        Obtiene la posición actual de Jasmine según el día y horario actual.
        Retorna None si no hay posición definida para la rutina actual.
        """
        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = jasmine_rutinas_visuales.get(clave)
            if datos:
                return datos.get("posicion")
        return None
    
    def inicializar_jasmine():
        """Inicializa el NPC Jasmine"""
        
        # Crear instancia del NPC
        jasmine = NPC(
            id="jasmine",
            nombre="Jasmine",
            nombre_completo="Jasmine",
            sprite="images/characters/casa/idle/idlet_jasmine_casa_hjasmine_trasnoche_rutinabase_skinbase.png",
            nombre_stat1="amor",
            nombre_stat2="deseo"
        )
        
        # =====================================================================
        # ESTADO INICIAL - Sincronizar con variables default guardables
        # =====================================================================
        
        # Sincronizar el objeto NPC con las variables guardables
        # Las variables default ya tienen los valores        # Cargar estado guardado
        jasmine.estado["amor"] = store.jasmine_amor
        jasmine.estado["deseo"] = store.jasmine_deseo
        jasmine.estado["progreso"] = store.jasmine_progreso
        jasmine.estado["conocido"] = True
        
        # =====================================================================
        # ATRIBUTOS PERSONALIZADOS
        # =====================================================================
        # Agregar atributos
        jasmine.agregar_atributo("edad", 18)
        jasmine.agregar_atributo("rol", "Hermanastra")
        
        # =====================================================================
        # RUTINAS SEMANALES
        # =====================================================================
        
        # Lunes a Viernes
        for dia in range(5):  # 0-4 = Lunes a Viernes
            jasmine.establecer_rutina(dia, 0, "casa_cocina")    # Mañana: Cocina
            jasmine.establecer_rutina(dia, 1, "casa_gym")       # Tarde: Gym
            jasmine.establecer_rutina(dia, 2, "casa_living")    # Noche: Living
            jasmine.establecer_rutina(dia, 3, "casa_hjasmine")  # Trasnoche: Su habitación
        
        # Sábado
        jasmine.establecer_rutina(5, 0, "casa_hjasmine")  # Mañana: Su habitación
        jasmine.establecer_rutina(5, 1, "casa_patio")     # Tarde: Patio
        jasmine.establecer_rutina(5, 2, "casa_patio")     # Noche: Patio
        jasmine.establecer_rutina(5, 3, "casa_hjasmine")  # Trasnoche: Su habitación
        
        # Domingo
        jasmine.establecer_rutina(6, 0, "casa_cocina")    # Mañana: Cocina
        jasmine.establecer_rutina(6, 1, "casa_patio")     # Tarde: Patio
        jasmine.establecer_rutina(6, 2, "casa_patio")     # Noche: Patio
        jasmine.establecer_rutina(6, 3, "casa_hjasmine")  # Trasnoche: Su habitación
        
        # =====================================================================
        # SPRITES Y POSICIONES DE RUTINA
        # =====================================================================
        # Cada rutina tiene un sprite específico y una posición personalizable
        
        # Lunes a Viernes + Domingo (0-4, 6) - Mañana en Cocina
        establecer_rutina_visual_jasmine(
            [0, 1, 2, 3, 4, 6], 0,
            "images/characters/casa/idle/idlet_jasmine_casa_cocina_mañana_rutinabase_grupobase_skinbase.png",
            (1637, 938)  # Posición personalizable
        )
        
        # Lunes a Viernes (0-4) - Tarde en Gym
        establecer_rutina_visual_jasmine(
            [0, 1, 2, 3, 4], 1,
            "images/characters/casa/idle/idlet_jasmine_casa_gym_tarde_rutinabase_grupobase_skinbase.png",
            (1005, 1080)  # Posición personalizable
        )
        
        # Lunes a Viernes (0-4) - Noche en Living
        establecer_rutina_visual_jasmine(
            [0, 1, 2, 3, 4], 2,
            "images/characters/casa/idle/idlet_jasmine_casa_living_noche_rutinabase_grupobase_skinbase.png",
            (126, 958)  # Posición personalizable
        )
        
        # Lunes a Domingo (0-6) - Trasnoche en H. Jasmine
        establecer_rutina_visual_jasmine(
            [0, 1, 2, 3, 4, 5, 6], 3,
            "images/characters/casa/idle/idlet_jasmine_casa_hjasmine_trasnoche_rutinabase_grupobase_skinbase.png",
            (1519, 956)  # Posición personalizable
        )
        
        # Sábado (5) - Mañana en H. Jasmine
        establecer_rutina_visual_jasmine(
            5, 0,
            "images/characters/casa/idle/idlet_jasmine_casa_hjasmine_mañana_rutinabase_grupobase_skinbase.png",
            (527, 976)  # Posición personalizable
        )
        
        # Sábado y Domingo (5, 6) - Tarde en Patio
        establecer_rutina_visual_jasmine(
            [5, 6], 1,
            "images/characters/casa/idle/idlet_jasmine_casa_patio_tarde_rutinabase_grupobase_skinbase.png",
            (541, 1078)  # Posición personalizable
        )
        
        # Sábado y Domingo (5, 6) - Noche en Patio
        establecer_rutina_visual_jasmine(
            [5, 6], 2,
            "images/characters/casa/idle/idlet_jasmine_casa_patio_noche_rutinabase_grupobase_skinbase.png",
            (808, 983)  # Posición personalizable
        )
        
        # =====================================================================
        # REGISTRAR EN EL SISTEMA
        # =====================================================================
        
        sistema_npcs.registrar_npc(jasmine)
        
        return jasmine

################################################################################
## DIÁLOGOS DE JASMINE
################################################################################

# Aquí se pueden agregar diálogos específicos de Jasmine en el futuro

################################################################################
## EVENTOS DE JASMINE
################################################################################

# Aquí se pueden agregar eventos específicos de Jasmine en el futuro

################################################################################
## QUESTS DE JASMINE
################################################################################

# Aquí se pueden agregar quests específicas de Jasmine en el futuro

################################################################################
## Datos de Jasmine (Guardables)
################################################################################

default jasmine_amor = 0
default jasmine_deseo = 0
default jasmine_progreso = 0
default jasmine_interacciones = {"hablar": False, "coquetear": False}
