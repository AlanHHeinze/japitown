################################################################################
## Skins de Mónica
################################################################################
## Definición de todos los skins y asignación de grupos a rutinas

init 10 python:

    # Funcion de MODULO (no anidada): la entrada de rutinas_skin_grupos guarda
    # la referencia, y una funcion local romperia el guardado.
    def _monica_bikini_en_patio():
        """El bikini es del patio: si no esta ahi, no corresponde."""
        return tracker_locacion_npc("monica") == "casa_patio"

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
            sprite_menu="images/characters/casa/menu/monica_menu_base_base.webp"
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
            sprite_menu="images/characters/casa/menu/monica_menu_bikini_base.webp"  # Ahora disponible
        )
        sistema_skins.registrar_skin(skin_bikini_base)
        
        # =====================================================================
        # ASIGNACIÓN DE GRUPOS A RUTINAS
        # =====================================================================
        
        # Sábado (5) - Tarde en Patio = Bikini
        # La condicion pide que este DE VERDAD en esa locacion. El grupo va
        # por (dia, horario), asi que sin esto una quest que la reubique la
        # deja con la ropa del lugar donde ya no esta — pasaba en la 09_a de
        # Violet, que la mueve al living un sabado a la tarde y el menu la
        # seguia mostrando en bikini. Si falla, obtener_grupo_rutina cae a
        # "base", que es exactamente lo que corresponde.
        establecer_grupo_rutina("monica", 5, 1, "bikini",
                                condicion=_monica_bikini_en_patio)
        
        # El resto de rutinas usará "base" por defecto


# Inicializar skins de Mónica al cargar el juego
init 11 python:
    inicializar_skins_monica()
