################################################################################
## Skins de Jasmine
################################################################################
## Definición de todos los skins y asignación de grupos a rutinas

init 10 python:
    
    def inicializar_skins_jasmine():
        """Inicializa los skins de Jasmine y asigna grupos a rutinas."""
        
        # =====================================================================
        # GRUPO: BASE
        # =====================================================================
        
        skin_base = Skin(
            id="jasmine_base_base",
            npc_id="jasmine",
            nombre="Ropa Casual",
            grupo="base",
            descripcion="Ropa casual de todos los días.",
            condicion_desbloqueo=None,  # Siempre desbloqueado
            sprite_menu="images/characters/casa/menu/jasmine_menu_base_base.png"
        )
        sistema_skins.registrar_skin(skin_base)
        
        # =====================================================================
        # GRUPO: ENTRENAMIENTO
        # =====================================================================
        
        # Skin: Entrenamiento Base (ropa normal en gym)
        skin_entrenamiento_base = Skin(
            id="jasmine_entrenamiento_base",
            npc_id="jasmine",
            nombre="Ropa Casual",
            grupo="entrenamiento",
            descripcion="Jasmine en ropa casual cuando va al gym.",
            condicion_desbloqueo=None,  # Siempre desbloqueado
            sprite_idle="images/characters/casa/idle/idle_jasmine_casa_gym_tarde_rutinabase_grupobase_skinbase.png",
            sprite_menu="images/characters/casa/menu/jasmine_menu_entrenamiento_base.png"
        )
        sistema_skins.registrar_skin(skin_entrenamiento_base)
        
        # Skin: Ropa Deportiva
        def condicion_desbloqueo_deportiva():
            quest = sistema_quests.obtener_quest("jasmine_questprincipal_0")
            return quest and quest.completada
        
        skin_entrenamiento_deportiva = Skin(
            id="jasmine_entrenamiento_deportiva",
            npc_id="jasmine",
            nombre="Ropa Deportiva",
            grupo="entrenamiento",
            descripcion="Jasmine viste su ropa de gym cuando entrena.",
            condicion_desbloqueo=condicion_desbloqueo_deportiva,
            sprite_idle="images/characters/casa/idle/idle_jasmine_casa_gym_tarde_rutinabase_grupoentrenamiento_skinropadeportiva.png",
            sprite_menu="images/characters/casa/menu/jasmine_menu_entrenamiento_deportiva.png"
        )
        sistema_skins.registrar_skin(skin_entrenamiento_deportiva)
        
        # =====================================================================
        # GRUPO: BIKINI
        # =====================================================================
        
        # Skin: Bikini Base (por ahora usa sprite base hasta tener el específico)
        skin_bikini_base = Skin(
            id="jasmine_bikini_base",
            npc_id="jasmine",
            nombre="Bikini",
            grupo="bikini",
            descripcion="Jasmine en bikini en el patio.",
            condicion_desbloqueo=None,
            sprite_menu="images/characters/casa/menu/jasmine_menu_bikini_base.png"  # Ahora disponible
        )
        sistema_skins.registrar_skin(skin_bikini_base)
        
        # =====================================================================
        # ASIGNACIÓN DE GRUPOS A RUTINAS
        # =====================================================================
        
        # Lunes a Viernes (0-4) - Tarde en Gym = Entrenamiento
        establecer_grupo_rutina("jasmine", [0, 1, 2, 3, 4], 1, "entrenamiento")
        
        # Sábado y Domingo (5, 6) - Tarde en Patio = Bikini
        establecer_grupo_rutina("jasmine", [5, 6], 1, "bikini")
        
        # El resto de rutinas usará "base" por defecto (no es necesario definirlas)


# Inicializar skins de Jasmine al cargar el juego
init 11 python:
    inicializar_skins_jasmine()
