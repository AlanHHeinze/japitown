################################################################################
## Skins de Jasmine
################################################################################
## Definición de todos los skins y asignación de grupos a rutinas

init 10 python:

    # Función de MÓDULO (no anidada): la condicion_desbloqueo queda guardada en
    # el save via el objeto Skin — una función local rompería el pickle al guardar.
    def _jasmine_desbloqueo_deportiva():
        quest = sistema_quests.obtener_quest("jasmine_questprincipal_0")
        return quest and quest.completada

    def _jasmine_entrenamiento_en_gym():
        """La ropa de entrenamiento es del gym: si no esta ahi, no corresponde."""
        return tracker_locacion_npc("jasmine") == "casa_gym"

    def _jasmine_bikini_en_patio():
        """El bikini es del patio: si no esta ahi, no corresponde."""
        return tracker_locacion_npc("jasmine") == "casa_patio"

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
            sprite_menu="images/characters/casa/menu/jasmine_menu_base_base.webp"
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
            sprite_idle="images/characters/casa/idle/idle_jasmine_casa_gym_tarde_rutinabase_grupobase_skinbase.jpg",
            sprite_menu="images/characters/casa/menu/jasmine_menu_entrenamiento_base.webp"
        )
        sistema_skins.registrar_skin(skin_entrenamiento_base)
        
        # Skin: Ropa Deportiva
        skin_entrenamiento_deportiva = Skin(
            id="jasmine_entrenamiento_deportiva",
            npc_id="jasmine",
            nombre="Ropa Deportiva",
            grupo="entrenamiento",
            descripcion="Jasmine viste su ropa de gym cuando entrena.",
            condicion_desbloqueo=_jasmine_desbloqueo_deportiva,
            sprite_idle="images/characters/casa/idle/idle_jasmine_casa_gym_tarde_rutinabase_grupoentrenamiento_skinropadeportiva.webp",
            sprite_menu="images/characters/casa/menu/jasmine_menu_entrenamiento_deportiva.webp"
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
            sprite_menu="images/characters/casa/menu/jasmine_menu_bikini_base.webp"  # Ahora disponible
        )
        sistema_skins.registrar_skin(skin_bikini_base)
        
        # =====================================================================
        # ASIGNACIÓN DE GRUPOS A RUTINAS
        # =====================================================================
        
        # Lunes a Viernes (0-4) - Tarde en Gym = Entrenamiento
        # La condicion pide que este DE VERDAD en esa locacion. El grupo va
        # por (dia, horario), asi que sin esto una quest que la reubique la
        # deja con la ropa del lugar donde ya no esta — pasaba en la 09_a de
        # Violet con Monica, y le puede pasar igual a Jasmine. Si falla, obtener_grupo_rutina cae a
        # "base", que es exactamente lo que corresponde.
        establecer_grupo_rutina("jasmine", [0, 1, 2, 3, 4], 1, "entrenamiento",
                                condicion=_jasmine_entrenamiento_en_gym)
        
        # Sábado y Domingo (5, 6) - Tarde en Patio = Bikini
        establecer_grupo_rutina("jasmine", [5, 6], 1, "bikini",
                                condicion=_jasmine_bikini_en_patio)
        
        # El resto de rutinas usará "base" por defecto (no es necesario definirlas)


# Inicializar skins de Jasmine al cargar el juego
init 11 python:
    inicializar_skins_jasmine()
