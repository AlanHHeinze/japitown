################################################################################
## NPC: MÓNICA
################################################################################
## Definición completa del personaje Mónica

    #Mónica
define monica = Character("Mónica", color="#d10b0b")

    # Mónica - Susurro (texto en itálica y más claro para dar efecto de susurro)
define monica_susurro = Character("Mónica", color="#d10b0b", what_prefix="{i}{color=#c8c8c8}", what_suffix="{/color}{/i}")

    # Mónica - Pensando (texto en itálica con color diferente para pensamientos)
define monica_pensando = Character("Mónica", color="#d10b0b", what_prefix="{i}{color=#a8b4c4}", what_suffix="{/color}{/i}")

init python:
    
    # Diccionario para almacenar sprites y posiciones de rutina de Mónica
    # Clave: (dia_semana, horario) -> {"sprite": path, "posicion": (x, y)}
    monica_rutinas_visuales = {}
    
    def establecer_rutina_visual_monica(dia_semana, horario, sprite, posicion):
        """
        Establece el sprite y posición para una rutina específica de Mónica.
        
        Args:
            dia_semana: Índice del día (0=Lunes, 6=Domingo) o lista de días
            horario: Índice del horario (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
            sprite: Ruta del sprite a mostrar
            posicion: Tupla (x, y) con la posición en pantalla
        """
        if isinstance(dia_semana, list):
            for dia in dia_semana:
                clave = (dia, horario)
                monica_rutinas_visuales[clave] = {
                    "sprite": sprite,
                    "posicion": posicion
                }
        else:
            clave = (dia_semana, horario)
            monica_rutinas_visuales[clave] = {
                "sprite": sprite,
                "posicion": posicion
            }
    
    def obtener_sprite_rutina_monica():
        """
        Obtiene el sprite actual de Mónica según el día y horario actual.
        Prioridad: 0) Pasillo, 1) Skin activo (quest/evento), 2) Rutina especial, 3) Rutina base
        """
        # Prioridad 0: Sprite de pasillo (door access)
        npc_m = obtener_npc("monica")
        if npc_m and npc_m.locacion_actual == "casa_pasilloabajo":
            return "images/characters/casa/idle/idle_monica_casa_pasillo_fuera_rutinabase_grupobase_skinbase.png"

        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            # Prioridad 1: Sprite del skin activo (quest/evento)
            sprite_skin = obtener_sprite_idle_rutina("monica")
            if sprite_skin:
                return sprite_skin

            # Prioridad 2: Rutina especial activa
            visual_esp = obtener_visual_npc_rutina_especial("monica")
            if visual_esp:
                return visual_esp[0]

            # Prioridad 3: Rutina visual base
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = monica_rutinas_visuales.get(clave)
            if datos:
                return datos.get("sprite")
        return None

    def obtener_posicion_rutina_monica():
        """
        Obtiene la posición actual de Mónica según el día y horario actual.
        Prioridad: 0) Pasillo, 1) Rutina especial, 2) Rutina base
        """
        # Prioridad 0: NPC en pasillo → posición fija
        npc_m = obtener_npc("monica")
        if npc_m and npc_m.locacion_actual == "casa_pasilloabajo":
            return (284, 1013)

        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            # Prioridad 1: Rutina especial activa
            visual_esp = obtener_visual_npc_rutina_especial("monica")
            if visual_esp:
                return visual_esp[1]

            # Prioridad 2: Rutina visual base
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = monica_rutinas_visuales.get(clave)
            if datos:
                return datos.get("posicion")
        return None
    
    def inicializar_monica():
        """Inicializa el NPC Mónica"""
        
        # Crear instancia del NPC
        monica = NPC(
            id="monica",
            nombre="Mónica",
            nombre_completo="Mónica",
            sprite="images/characters/casa/idle/idle_monica_casa_hmonica_trasnoche_rutinabase_skinbase.png",
            nombre_stat1="amor",
            nombre_stat2="deseo"
        )
        
        # =====================================================================
        # ESTADO INICIAL - Sincronizar con variables default guardables
        # =====================================================================
        
        # Sincronizar el objeto NPC con las variables guardables
        # Las variables default ya tienen los valores iniciales correctos
        monica.estado["amor"] = min(100, max(0, store.monica_amor))
        monica.estado["deseo"] = min(100, max(0, store.monica_deseo))
        monica.estado["progreso"] = max(0, store.monica_progreso)
        monica.estado["conocido"] = True  # Ya la conoces
        
        # =====================================================================
        # ATRIBUTOS PERSONALIZADOS
        # =====================================================================
        
        monica.agregar_atributo("edad", 35)
        monica.agregar_atributo("rol", "Tutora")
        
        # =====================================================================
        # RUTINAS SEMANALES
        # =====================================================================
        
        # Lunes a Viernes
        for dia in range(5):  # 0-4 = Lunes a Viernes
            monica.establecer_rutina(dia, 0, "casa_cocina")      # Mañana: Cocina
            monica.establecer_rutina(dia, 1, "casa_living")      # Tarde: Living
            monica.establecer_rutina(dia, 2, "casa_hmonica")     # Noche: Su habitación
            monica.establecer_rutina(dia, 3, "casa_hmonica")     # Trasnoche: Su habitación
        
        # Sábado
        monica.establecer_rutina(5, 0, "casa_living")       # Mañana: Living
        monica.establecer_rutina(5, 1, "casa_patio")        # Tarde: Patio
        monica.establecer_rutina(5, 2, "casa_cocina")       # Noche: Cocina
        monica.establecer_rutina(5, 3, "casa_hmonica")      # Trasnoche: Su habitación
        
        # Domingo
        monica.establecer_rutina(6, 0, "casa_cocina")       # Mañana: Cocina
        monica.establecer_rutina(6, 1, "casa_living")       # Tarde: Living
        monica.establecer_rutina(6, 2, "casa_hmonica")      # Noche: Su habitación
        monica.establecer_rutina(6, 3, "casa_hmonica")      # Trasnoche: Su habitación
        
        # =====================================================================
        # SPRITES Y POSICIONES DE RUTINA
        # =====================================================================
        # Cada rutina tiene un sprite específico y una posición personalizable
        
        # Lunes a Viernes + Domingo (0-4, 6) - Mañana en Cocina
        establecer_rutina_visual_monica(
            [0, 1, 2, 3, 4, 6], 0,
            "images/characters/casa/idle/idle_monica_casa_cocina_mañana_rutinabase_grupobase_skinbase.png",
            (957, 730)  # Posición personalizable: centro-abajo
        )
        
        # Lunes a Viernes + Domingo (0-4, 6) - Tarde en Living
        establecer_rutina_visual_monica(
            [0, 1, 2, 3, 4, 6], 1,
            "images/characters/casa/idle/idle_monica_casa_living_tarde_rutinabase_grupobase_skinbase.png",
            (1299, 1067)  # Posición personalizable
        )
        
        # Lunes a Viernes + Domingo (0-4, 6) - Noche en H. Mónica
        establecer_rutina_visual_monica(
            [0, 1, 2, 3, 4, 6], 2,
            "images/characters/casa/idle/idle_monica_casa_hmonica_noche_rutinabase_grupobase_skinbase.png",
            (1090, 928)  # Posición personalizable
        )
        
        # Lunes a Domingo (0-6) - Trasnoche en H. Mónica
        establecer_rutina_visual_monica(
            [0, 1, 2, 3, 4, 5, 6], 3,
            "images/characters/casa/idle/idle_monica_casa_hmonica_trasnoche_rutinabase_grupobase_skinbase.png",
            (953, 766)  # Posición personalizable
        )
        
        # Sábado (5) - Mañana en Living
        establecer_rutina_visual_monica(
            5, 0,
            "images/characters/casa/idle/idle_monica_casa_living_mañana_rutinabase_grupobase_skinbase.png",
            (1299, 1065)  # Posición personalizable
        )
        
        # Sábado (5) - Tarde en Patio
        establecer_rutina_visual_monica(
            5, 1,
            "images/characters/casa/idle/idle_monica_casa_patio_tarde_rutinabase_grupobikini_skinbase.png",
            (1564, 961)  # Posición personalizable
        )
        
        # Sábado (5) - Noche en Cocina
        establecer_rutina_visual_monica(
            5, 2,
            "images/characters/casa/idle/idle_monica_casa_cocina_noche_rutinabase_grupobase_skinbae.png",
            (637, 1062)  # Posición personalizable
        )
        
        # =====================================================================
        # RUTINAS ESPECIALES
        # =====================================================================

        monica.agregar_rutina_especial(RutinaEspecial(
            id="monica_salida",
            locacion="fuera",
            sprite=None,
            posicion=None,
            probabilidad=0.20,
            horarios=[0, 1, 2],
            nombre="Monica salió de la casa"
        ))

        monica.agregar_rutina_especial(RutinaEspecial(
            id="monica_ducha",
            locacion="casa_baniomonica",
            sprite=None,
            posicion=None,
            probabilidad=0.25,
            horarios=[0],
            nombre="Monica en la ducha"
        ))

        # =====================================================================
        # DESBLOQUEOS DE RELACIÓN
        # =====================================================================

        # Amor
        monica.agregar_desbloqueo("amor", 10, "💬", "Conversación Diaria",
            "Podés hablar con Mónica todos los días.")
        monica.agregar_desbloqueo("amor", 30, "🚪", "Ingreso Habitación",
            "Mónica te deja entrar a su cuarto durante el día.")

        # Deseo
        monica.agregar_desbloqueo("deseo", 10, "👁", "???",
            "")
        monica.agregar_desbloqueo("deseo", 40, "😘", "???",
            "")
        monica.agregar_desbloqueo("deseo", 60, "🌙", "Ingreso Nocturno",
            "Podés entrar a la habitación de Mónica de noche.")

        # =====================================================================
        # REGISTRAR EN EL SISTEMA
        # =====================================================================

        sistema_npcs.registrar_npc(monica)

        return monica

################################################################################
## DIÁLOGOS DE MÓNICA
################################################################################

# Aquí se pueden agregar diálogos específicos de Mónica en el futuro

################################################################################
## EVENTOS DE MÓNICA
################################################################################

# Aquí se pueden agregar eventos específicos de Mónica en el futuro

################################################################################
## QUESTS DE MÓNICA
################################################################################

# Aquí se pueden agregar quests específicas de Mónica en el futuro

################################################################################
## Datos de Mónica (Guardables)
################################################################################

default monica_amor = 0
default monica_deseo = 0
default monica_progreso = 0
default monica_interacciones = {"hablar": False, "coquetear": False}
