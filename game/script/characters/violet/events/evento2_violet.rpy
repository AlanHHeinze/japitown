################################################################################
## Evento 2 de Violet - Noche post Quest 3.2
################################################################################
## Este evento se dispara automáticamente la primera vez que el jugador va a
## dormir después de haber completado la Quest 3.2 de Violet.
## También contiene el label para la versión repetible del evento.

################################################################################
## Imagenes
################################################################################

image violet_evento02_fondo = "images/eventos/violet/evento2/violet_evento02_fondo.png"
image violet_evento02_despierto = "images/eventos/violet/evento2/violet_evento02_despierto.png"
image violet_evento02_despierto2 = "images/eventos/violet/evento2/violet_evento02_despierto2.png"

layeredimage violet_evento_02:
    group pose:
        attribute img1 default:
            "images/eventos/violet/evento2/violet_evento02_img1.png"
        attribute img2:
            "images/eventos/violet/evento2/violet_evento02_img2.png"
        attribute img3:
            "images/eventos/violet/evento2/violet_evento02_img3.png"
        attribute img4:
            "images/eventos/violet/evento2/violet_evento02_img4.png"
        attribute img5:
            "images/eventos/violet/evento2/violet_evento02_img5.png"
        attribute img6:
            "images/eventos/violet/evento2/violet_evento02_img6.png"

################################################################################
## Variables guardables
################################################################################

default violet_evento2_completado = False
default violet_evento2_repetir = False

################################################################################
## Labels
################################################################################

label evento2_violet:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    scene violet_evento02_fondo with fade

    # img1
    show violet_evento_02 img1 with dissolve
    mc ""
    violet ""

    # img2
    show violet_evento_02 img2 with dissolve
    mc ""
    violet ""

    # img3
    show violet_evento_02 img3 with dissolve
    mc ""
    violet ""

    # img4
    show violet_evento_02 img4 with dissolve
    mc ""
    violet ""

    # img5
    show violet_evento_02 img5 with dissolve
    mc ""
    violet ""

    # img6
    show violet_evento_02 img6 with dissolve
    mc ""
    violet ""

    hide violet_evento_02 with dissolve

    scene violet_evento02_despierto with fade
    piensa "Eso fue raro..."
    piensa "Va a ser mejor que me vuelva a dormir"
    scene violet_evento02_despierto2 with fade

    $ violet_evento2_completado = True

    # Ejecutar la acción de dormir
    $ dormir()

    window hide
    jump game_loop

label evento2_violet_repetir:
    # Este label en la arquitectura original retorna para dejar que el botón de dormir se encargue
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    scene violet_evento02_fondo with fade

    show violet_evento_02 img1 with dissolve
    mc ""
    violet ""

    hide violet_evento_02 with dissolve
    return
