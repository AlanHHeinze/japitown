################################################################################
## Skins de Violet
################################################################################
## Definición de todos los skins y asignación de grupos a rutinas

init 10 python:

    def _cond_pijama_violet():
        """Pijama activo si el skin fue desbloqueado por quest."""
        return store.skins_activos.get("violet", {}).get("pijama") is not None

    def inicializar_skins_violet():
        """Inicializa los skins de Violet y asigna grupos a rutinas."""
        
        # =====================================================================
        # GRUPO: BASE
        # =====================================================================
        
        skin_base = Skin(
            id="violet_base_base",
            npc_id="violet",
            nombre="Ropa Casual",
            grupo="base",
            descripcion="Ropa casual de todos los días.",
            condicion_desbloqueo=None,
            sprite_menu="images/characters/casa/menu/violet_menu_base_base.png"
        )
        sistema_skins.registrar_skin(skin_base)
        
        # =====================================================================
        # GRUPO: PIJAMA
        # =====================================================================
        
        # Skin: Pijama Base
        skin_pijama_base = Skin(
            id="violet_pijama_base",
            npc_id="violet",
            nombre="Pijama",
            grupo="pijama",
            descripcion="Violet en pijama en su habitación.",
            condicion_desbloqueo=None,
            sprite_menu="images/characters/casa/menu/violet_menu_pijama_base.png"
        )
        sistema_skins.registrar_skin(skin_pijama_base)
        
        # =====================================================================
        # ASIGNACIÓN DE GRUPOS A RUTINAS
        # =====================================================================
        
        # Lunes a Sábado (0-5) - Noche en H. Violet = Pijama (requiere desbloqueo)
        establecer_grupo_rutina("violet", [0, 1, 2, 3, 4, 5], 2, "pijama", condicion=_cond_pijama_violet)

        # Todos los dias (0-6) - Trasnoche en H. Violet = Pijama (requiere desbloqueo)
        establecer_grupo_rutina("violet", [0, 1, 2, 3, 4, 5, 6], 3, "pijama", condicion=_cond_pijama_violet)
        
        # El resto de rutinas usará "base" por defecto


# Inicializar skins de Violet al cargar el juego
init 11 python:
    inicializar_skins_violet()
