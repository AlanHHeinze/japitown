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

    def _cond_pijama_desbloqueo():
        """Quest 02_b completada — condición extra para el desbloqueo del skin pijama."""
        q = store.sistema_quests.obtener_quest("violet_questprincipal_02_b")
        return bool(q and q.completada)

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
        Prioridad: 0) Pasillo, 1) Skin activo (quest/evento), 2) Rutina especial, 3) Rutina base
        """
        # Prioridad 0: Sprite de pasillo (door access) — respeta el grupo de skin activo
        npc_v = obtener_npc("violet")
        if npc_v and npc_v.locacion_actual == "casa_pasilloarriba":
            grupo = obtener_grupo_rutina_actual("violet")
            if grupo == "pijama":
                return "images/characters/casa/idle/idle_violet_casa_pasillo_fuera_rutinabase_grupopijama_skinbase.png"
            return "images/characters/casa/idle/idle_violet_casa_pasillo_fuera_rutinabase_grupobase_skinbase.png"

        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            # Prioridad 1: Sprite del skin activo (quest/evento)
            sprite_skin = obtener_sprite_idle_rutina("violet")
            if sprite_skin:
                return sprite_skin

            # Prioridad 2: Rutina especial activa
            visual_esp = obtener_visual_npc_rutina_especial("violet")
            if visual_esp:
                return visual_esp[0]

            # Prioridad 3: Rutina visual base
            clave = (store.dia_semana_actual, store.horario_actual)
            datos = violet_rutinas_visuales.get(clave)
            if datos:
                return datos.get("sprite")
        return None

    def obtener_posicion_rutina_violet():
        """
        Obtiene la posición actual de Violet según el día y horario actual.
        Prioridad: 0) Pasillo, 1) Rutina especial, 2) Rutina base
        """
        # Prioridad 0: NPC en pasillo → posición fija según skin
        npc_v = obtener_npc("violet")
        if npc_v and npc_v.locacion_actual == "casa_pasilloarriba":
            grupo = obtener_grupo_rutina_actual("violet")
            if grupo == "pijama":
                return (671, 793)
            return (663, 804)

        if hasattr(store, 'dia_semana_actual') and hasattr(store, 'horario_actual'):
            # Prioridad 1: Rutina especial activa
            visual_esp = obtener_visual_npc_rutina_especial("violet")
            if visual_esp:
                return visual_esp[1]

            # Prioridad 2: Rutina visual base
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
        violet.estado["amor"] = min(100, max(0, store.violet_amor))
        violet.estado["deseo"] = min(100, max(0, store.violet_deseo))
        violet.estado["progreso"] = max(0, store.violet_progreso)
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
        # AJUSTE TEMPORAL: usa sprite de tarde hasta que se cargue uno de noche propio
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 5], 2,
            "images/characters/casa/idle/idle_violet_casa_hviolet_tarde_rutinabase_grupobase_skinbase.png",
            (721, 793)
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
            (549, 991)  # Posición personalizable
        )

        # Domingo (6) - Noche en Living
        establecer_rutina_visual_violet(
            6, 2,
            "images/characters/casa/idle/idle_violet_casa_living_noche_rutinabase_grupobase_skinbase.png",
            (689, 808)  # Posición personalizable
        )
        
        # =====================================================================
        # RUTINAS ESPECIALES
        # =====================================================================

        violet.agregar_rutina_especial(RutinaEspecial(
            id="violet_salida",
            locacion="fuera",
            sprite=None,
            posicion=None,
            probabilidad=0.20,
            horarios=[1, 2],
            nombre="Violet salió de la casa"
        ))

        violet.agregar_rutina_especial(RutinaEspecial(
            id="violet_ducha",
            locacion="casa_banioarriba",
            sprite=None,
            posicion=None,
            probabilidad=0.25,
            horarios=[1, 2],
            nombre="Violet en la ducha"
        ))

        # =====================================================================
        # DESBLOQUEOS DE RELACIÓN
        # =====================================================================

        # Amor
        violet.agregar_desbloqueo("amor", 10, "💬", "Conversación Diaria",
            "Podés hablar con Violet todos los días.")
        violet.agregar_desbloqueo("amor", 30, "🚪", "Ingreso Habitación",
            "Violet te deja entrar a su cuarto durante el día.")
        violet.agregar_desbloqueo("amor", 60, "📺", "Ver TV Juntos",
            "Pueden ver televisión juntos en el living.")

        # Deseo
        violet.agregar_desbloqueo("deseo", 10, "👗", "Skin Pijama",
            "Violet sale al pasillo en pijama.",
            condicion_extra=_cond_pijama_desbloqueo,
            nombre_pendiente="Completar Quest: Mangas Prestados")
        violet.agregar_desbloqueo("deseo", 40, "😘", "???",
            "")
        violet.agregar_desbloqueo("deseo", 60, "🌙", "Ingreso Nocturno",
            "Podés entrar a la habitación de Violet de noche.")

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
