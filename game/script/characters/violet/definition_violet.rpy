################################################################################
## NPC: VIOLET
################################################################################
## Definición completa del personaje Violet


# Violet
# El color va como constante: lo usan el personaje, su susurro y su
# pensamiento. Asi los tres no se pueden desfasar.
define VIOLET_COLOR = "#956db3"

define violet = Character("Violet", color=VIOLET_COLOR)

    # Violet - Susurro (texto en itálica y más claro para dar efecto de susurro)
define violet_susurro = Character("Violet", color=VIOLET_COLOR, what_prefix="{i}{color=#c8c8c8}", what_suffix="{/color}{/i}")

    # Violet - Pensamiento (mismo nombre y color, texto en gris e itálica)
define violet_piensa = Character("Violet", kind=piensa_base, color=VIOLET_COLOR)

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
            dia_semana: Índice del dia (0=Lunes, 6=Domingo) o lista de dias
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
        Obtiene el sprite actual de Violet según el dia y horario actual.
        Prioridad: 0) Pasillo, 1) Skin activo (quest/evento), 2) Rutina especial, 3) Rutina base
        """
        # Prioridad 0: Sprite de pasillo (door access) — respeta el grupo de skin activo
        npc_v = obtener_npc("violet")
        if npc_v and npc_v.locacion_actual == "casa_pasilloarriba":
            grupo = obtener_grupo_rutina_actual("violet")
            if grupo == "pijama":
                return "images/characters/casa/idle/idle_violet_casa_pasillo_fuera_rutinabase_grupopijama_skinbase.webp"
            return "images/characters/casa/idle/idle_violet_casa_pasillo_fuera_rutinabase_grupobase_skinbase.webp"

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

    def poblar_rutinas_visuales_violet():
        """
        Llena violet_rutinas_visuales (sprite+posicion por dia/horario).
        Se llama al iniciar partida nueva (dentro de inicializar_violet) y
        tambien despues de cargar un save / reload de script: ese diccionario
        vive en memoria (no es parte del save), asi que si no se repuebla,
        obtener_sprite_rutina_violet() no encuentra nada y cae al sprite
        generico de la Prioridad 3, con ruta desactualizada y en el lugar
        equivocado.
        """
        # Lunes a Viernes + Domingo (0-4, 6) - Mañana en Cocina
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 6], 0,
            "images/characters/casa/idle/idle_violet_casa_cocina_manana_rutinabase_grupobase_skinbase.webp",
            (765, 1060)  # Posición personalizable
        )

        # Lunes a Viernes + Domingo (0-4, 6) - Tarde en H. Violet
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 6], 1,
            "images/characters/casa/idle/idle_violet_casa_hviolet_tarde_rutinabase_grupobase_skinbase.jpg",
            (721, 793)  # Posición personalizable
        )

        # Lunes a Sábado (0-5) - Noche en H. Violet (pijama)
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 5], 2,
            "images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.jpg",
            (1537, 1020)
        )

        # Lunes a Domingo (0-6) - Trasnoche en H. Violet
        establecer_rutina_visual_violet(
            [0, 1, 2, 3, 4, 5, 6], 3,
            "images/characters/casa/idle/idle_violet_casa_hviolet_trasnoche_rutinabase_grupobase_skinbase.jpg",
            (725, 862)  # Posición personalizable
        )

        # Sábado (5) - Mañana en H. Violet
        establecer_rutina_visual_violet(
            5, 0,
            "images/characters/casa/idle/idle_violet_casa_hviolet_manana_rutinabase_grupobase_skinbase.jpg",
            (728, 815)  # Posición personalizable
        )

        # Sábado (5) - Tarde en Living
        establecer_rutina_visual_violet(
            5, 1,
            "images/characters/casa/idle/idle_violet_casa_living_tarde_rutinabase_grupobase_skinbase.webp",
            (549, 991)  # Posición personalizable
        )

        # Domingo (6) - Noche en Living
        establecer_rutina_visual_violet(
            6, 2,
            "images/characters/casa/idle/idle_violet_casa_living_noche_rutinabase_grupobase_skinbase.webp",
            (689, 808)  # Posición personalizable
        )

    def obtener_posicion_rutina_violet():
        """
        Obtiene la posición actual de Violet según el dia y horario actual.
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
            sprite="images/characters/casa/idle/idle_violet_casa_hviolet_trasnoche_rutinabase_grupobase_skinbase.jpg",
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
            violet.establecer_rutina(dia, 1, "casa_hviolet")        # Tarde: Su habitacion (leyendo)
            violet.establecer_rutina(dia, 2, "casa_hviolet")        # Noche: Su habitacion
            violet.establecer_rutina(dia, 3, "casa_hviolet")        # Trasnoche: Su habitacion
        
        # Sábado
        violet.establecer_rutina(5, 0, "casa_hviolet")       # Mañana: Su habitacion
        violet.establecer_rutina(5, 1, "casa_living")        # Tarde: Living (leyendo)
        violet.establecer_rutina(5, 2, "casa_hviolet")       # Noche: Su habitacion
        violet.establecer_rutina(5, 3, "casa_hviolet")       # Trasnoche: Su habitacion
        
        # Domingo
        violet.establecer_rutina(6, 0, "casa_cocina")        # Mañana: Cocina
        violet.establecer_rutina(6, 1, "casa_hviolet")       # Tarde: Su habitacion
        violet.establecer_rutina(6, 2, "casa_living")        # Noche: Living
        violet.establecer_rutina(6, 3, "casa_hviolet")       # Trasnoche: Su habitacion
        
        # =====================================================================
        # SPRITES Y POSICIONES DE RUTINA
        # =====================================================================
        poblar_rutinas_visuales_violet()

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
            horarios=[2],
            nombre="Violet en la ducha"
        ))

        # Los desbloqueos de relación ya no se declaran acá: son HITOS y viven en
        # characters/violet/hitos_violet.rpy.

        # =====================================================================
        # REGISTRAR EN EL SISTEMA
        # =====================================================================

        sistema_npcs.registrar_npc(violet)

        return violet

################################################################################
## DIÁLOGOS DE VIOLET
################################################################################

# Aqui se pueden agregar diálogos específicos de Violet en el futuro

################################################################################
## EVENTOS DE VIOLET
################################################################################

# Aqui se pueden agregar eventos específicos de Violet en el futuro

################################################################################
## QUESTS DE VIOLET
################################################################################

# Aqui se pueden agregar quests específicas de Violet en el futuro

################################################################################
## Datos de Violet (Guardables)
################################################################################

default violet_amor = 0
default violet_deseo = 0
default violet_progreso = 0
default violet_interacciones = {"hablar": False, "coquetear": False}
default violet_quest2_trajesexy = False

# Ya tuvo sexo con Violet. La prende CADA escena donde lo tienen (hoy solo la
# cama de amor 50) y la leen las que cambian si es la primera vez o no. Es UNA
# variable para todas a proposito: cualquier quest nueva con sexo solo tiene que
# prenderla, sin que las demas tengan que enterarse de que existe.
default violet_tuvo_sexo = False
