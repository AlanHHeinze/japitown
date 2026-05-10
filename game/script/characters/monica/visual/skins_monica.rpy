################################################################################
## Skins de Mónica
################################################################################
## Definición de todos los skins y asignación de grupos a rutinas

init 10 python:
    
    def inicializar_skins_monica():
        """Inicializa los skins de Mónica y asigna grupos a rutinas."""
        
        # =====================================================================
        # GRUPO: BASE
        # =====================================================================
        
        skin_base = Skin(
            id="monica_base_base",
            npc_id="monica",
            nombre="Ropa Casual",
            grupo="base",
            descripcion="Ropa casual de todos los días.",
            condicion_desbloqueo=None,
            sprite_menu="images/characters/casa/menu/monica_menu_base_base.png"
        )
        sistema_skins.registrar_skin(skin_base)
        
        # =====================================================================
        # GRUPO: BIKINI
        # =====================================================================
        
        # Skin: Bikini Base
        skin_bikini_base = Skin(
            id="monica_bikini_base",
            npc_id="monica",
            nombre="Bikini",
            grupo="bikini",
            descripcion="Mónica en bikini en el patio.",
            condicion_desbloqueo=None,
            sprite_menu="images/characters/casa/menu/monica_menu_bikini_base.png"  # Ahora disponible
        )
        sistema_skins.registrar_skin(skin_bikini_base)
        
        # =====================================================================
        # ASIGNACIÓN DE GRUPOS A RUTINAS
        # =====================================================================
        
        # Sábado (5) - Tarde en Patio = Bikini
        establecer_grupo_rutina("monica", 5, 1, "bikini")
        
        # El resto de rutinas usará "base" por defecto


# Inicializar skins de Mónica al cargar el juego
init 11 python:
    inicializar_skins_monica()
