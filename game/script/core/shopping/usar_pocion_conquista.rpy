################################################################################
## Label: Usar Poción de Conquista
################################################################################
## Se llama cuando el jugador usa la poción desde el inventario (el sistema ya
## la consumió). Activa por un día el ver los resultados de las opciones del
## sistema talk; el efecto termina al dormir (se limpia en def dormir()).
##
## condicion_uso del catálogo garantiza que no se use con el efecto ya activo.
## La primera vez muestra al MC en la locación actual con el tutorial.

default pocion_conquista_activa = False
default pocion_conquista_tutorial_visto = False

label usar_pocion_conquista:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    $ pocion_conquista_activa = True

    if not pocion_conquista_tutorial_visto:
        $ pocion_conquista_tutorial_visto = True

        # MC en la locación actual
        $ _loc_pocion = sistema_locaciones.locacion_actual
        $ _bg_pocion = _loc_pocion.background if _loc_pocion else None
        if _bg_pocion:
            scene expression _bg_pocion with fade
        show mc_parado_base c_rbase_base o_base b_none at center with dissolve

        $ _pocion_txt = renpy.translate_string("Esta poción te permite ver los resultados de la interacción Hablar por un día")
        tutorial "[_pocion_txt]"

        hide mc_parado_base with dissolve
    else:
        $ _pocion_txt = renpy.translate_string("Los efectos de la poción se activaron, van a durar hasta que me duerma")
        piensa "[_pocion_txt]"

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop
