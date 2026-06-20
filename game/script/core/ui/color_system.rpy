################################################################################
## Sistema de Colores - Resalte de Elementos en Texto
################################################################################
## Configuración centralizada de colores para resaltar diferentes tipos de
## elementos en el texto del juego.

init python:

    # =========================================================================
    # COLORES DE NPCs
    # =========================================================================
    COLORES_NPC = {
        "jasmine": "#D4A574",   # Marrón
        "monica": "#d10b0b",    # Rojo
        "violet": "#956db3",    # Púrpura
    }

    # =========================================================================
    # COLORES DE ELEMENTOS DEL JUEGO
    # =========================================================================
    COLORES_ELEMENTOS = {
        "quest": "#FFD700",         # Amarillo (mismo que en menú de pistas)
        "locacion": "#4dd0e1",      # Verde agua
        "item": "#4a90e2",          # Celeste oscuro
    }

    # =========================================================================
    # FUNCIONES DE UTILIDAD PARA APLICAR COLORES
    # =========================================================================

    def colorear_npc(nombre_npc, texto):
        """Colorea el nombre de un NPC."""
        color = COLORES_NPC.get(nombre_npc.lower())
        if color:
            return "{{color={}}}{}{{/color}}".format(color, texto)
        return texto

    def colorear_quest(texto):
        """Colorea un elemento de quest."""
        color = COLORES_ELEMENTOS.get("quest")
        return "{{color={}}}{}{{/color}}".format(color, texto)

    def colorear_locacion(texto):
        """Colorea una locación."""
        color = COLORES_ELEMENTOS.get("locacion")
        return "{{color={}}}{}{{/color}}".format(color, texto)

    def colorear_item(texto):
        """Colorea un item."""
        color = COLORES_ELEMENTOS.get("item")
        return "{{color={}}}{}{{/color}}".format(color, texto)
