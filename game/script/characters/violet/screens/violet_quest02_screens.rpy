################################################################################
## Screens de la Quest 2 de Violet — Limpieza del Sábado
################################################################################

# =============================================================================
# VARIABLES DE ESTADO — Limpieza del Living
# =============================================================================

# Posiciones de los elementos (ajustables con el posicionador)
default vq2_pos_chimenea = (1361, 876)
default vq2_pos_escalera = (281, 964)
default vq2_pos_sillon   = (880, 1024)

# Posición del sprite de Violet barriendo (en el pasillo arriba)
default vq2_pos_violet_barriendo = (881, 987)

# Estado de los elementos (True = aún no limpiado)
default vq2_chimenea_pendiente = True
default vq2_escalera_pendiente = True
default vq2_sillon_pendiente   = True

# Controla si se mostró el texto inicial del screen
default vq2_texto_inicial_mostrado = False

# Posición del elemento alacena en la cocina
default vq2_pos_alacena = (651, 795)  # 20/02/2026 12:04


# =============================================================================
# SCREEN: Buscar trapeador en la cocina
# =============================================================================

screen buscar_trapeador_quest2_violet():

    # Área clickeable de fondo (click fuera de elementos)
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("fuera")

    # Elemento: Alacena (donde está el trapeador)
    # Posición leída desde sistema_pos para poder editarla con la herramienta (grupo: quest_elemento)
    $ _alacena_elem = sistema_pos.obtener("casa_cocina_alacena_vq2")
    $ _alacena_x = _alacena_elem.x if _alacena_elem else vq2_pos_alacena[0]
    $ _alacena_y = _alacena_elem.y if _alacena_elem else vq2_pos_alacena[1]

    imagebutton:
        idle Transform("images/quest/violet/quest1/violet_quest01_interaccion_alacena.png", alpha=0.0)
        hover "images/quest/violet/quest1/violet_quest01_interaccion_alacena.png"
        xpos _alacena_x
        ypos _alacena_y
        xanchor 0.5
        yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("alacena")



# =============================================================================
# SCREEN: Limpieza interactiva del Living
# =============================================================================

screen limpieza_quest2_violet():
    
    # Fondo: living de mañana (ya se muestra como scene)
    
    # Texto inicial (solo la primera vez que se abre el screen)
    if not vq2_texto_inicial_mostrado:
        $ renpy.set_return_stack([])
    
    # Área clickeable de fondo (click fuera de elementos)
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        if modo_posicionamiento:
            action NullAction()
        else:
            action Function(_vq2_click_fuera)
    
    # Posiciones leídas desde sistema_pos (editables con herramienta → tab Otros → grupo quest_elemento)
    $ _chimenea_elem = sistema_pos.obtener("casa_living_chimenea_vq2")
    $ _chimenea_x = _chimenea_elem.x if _chimenea_elem else vq2_pos_chimenea[0]
    $ _chimenea_y = _chimenea_elem.y if _chimenea_elem else vq2_pos_chimenea[1]

    $ _escalera_elem = sistema_pos.obtener("casa_living_escalera_vq2")
    $ _escalera_x = _escalera_elem.x if _escalera_elem else vq2_pos_escalera[0]
    $ _escalera_y = _escalera_elem.y if _escalera_elem else vq2_pos_escalera[1]

    $ _sillon_elem = sistema_pos.obtener("casa_living_sillon_vq2")
    $ _sillon_x = _sillon_elem.x if _sillon_elem else vq2_pos_sillon[0]
    $ _sillon_y = _sillon_elem.y if _sillon_elem else vq2_pos_sillon[1]

    # =========================================================================
    # Elemento 1: Chimenea
    # =========================================================================
    if vq2_chimenea_pendiente:
        imagebutton:
            # Invisible en idle, visible en hover
            idle Transform("images/quest/violet/quest1/violet_quest01_interaccion_chimenea.png", alpha=0.0)
            hover "images/quest/violet/quest1/violet_quest01_interaccion_chimenea.png"
            xpos _chimenea_x
            ypos _chimenea_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("chimenea")

    # =========================================================================
    # Elemento 2: Escalera
    # =========================================================================
    if vq2_escalera_pendiente:
        imagebutton:
            idle Transform("images/quest/violet/quest1/violet_quest01_interaccion_escalera.png", alpha=0.0)
            hover "images/quest/violet/quest1/violet_quest01_interaccion_escalera.png"
            xpos _escalera_x
            ypos _escalera_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("escalera")

    # =========================================================================
    # Elemento 3: Sillón
    # =========================================================================
    if vq2_sillon_pendiente:
        imagebutton:
            idle Transform("images/quest/violet/quest1/violet_quest01_interaccion_sillon.png", alpha=0.0)
            hover "images/quest/violet/quest1/violet_quest01_interaccion_sillon.png"
            xpos _sillon_x
            ypos _sillon_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("sillon")




# =============================================================================
# Funciones Python del posicionador de quest
# =============================================================================
# NOTA: Las posiciones se gestionan ahora desde sistema_pos (tab Otros de la
# herramienta de posicionamiento, grupo "quest_elemento"). Los IDs son:
#   casa_living_chimenea_vq2
#   casa_living_escalera_vq2
#   casa_living_sillon_vq2
#   casa_cocina_alacena_vq2
#   casa_pasilloarriba_violet_barriendo_vq2
# El export se hace desde la barra de sesión de la herramienta (botón Exportar).
# =============================================================================

init python:

    def _vq2_click_fuera():
        """Muestra mensaje con los elementos pendientes al hacer click fuera."""
        pendientes = []
        if store.vq2_chimenea_pendiente:
            pendientes.append("la chimenea")
        if store.vq2_escalera_pendiente:
            pendientes.append("las escaleras")
        if store.vq2_sillon_pendiente:
            pendientes.append("el sillon")

        if pendientes:
            lista = ", ".join(pendientes)
            store._msg_restriccion_texto = "Todavia me falta limpiar: {}".format(lista)
            renpy.show_screen("mensaje_restriccion")
