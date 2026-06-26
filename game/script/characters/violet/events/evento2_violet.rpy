################################################################################
## Evento 2 de Violet - Noche post Quest 3.2
################################################################################
## Este evento se dispara automáticamente la primera vez que el jugador va a
## dormir despues de haber completado la Quest 3.2 de Violet.
## Tambien contiene el label para la versión repetible del evento.

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
    
    violet "¿Este era el cosplay que tanto querías ver?"
    mc "Sí... te queda muy bien"

    # img2
    show violet_evento_02 img2 with dissolve
    violet "¿Me lo vuelvo a poner o me lo termino de quitar?"
    mc "Ehhh"
    

    # img3
    show violet_evento_02 img3 with dissolve
    violet "¿Así o un poco más?"
    mc "Un poco más"


    # img5
    show violet_evento_02 img5 with dissolve
    violet "¿Esto querías ver? Perverido"
    mc "Sí, estaba deseando ese trasero"

    # img6
    show violet_evento_02 img6 with dissolve
    violet "Bueno entonces veni a buscarlo"


    hide violet_evento_02 with dissolve

    scene violet_evento02_despierto with fade
    piensa "Eso fue bastante raro..."
    piensa "Va a ser mejor que me vuelva a dormir"
    scene violet_evento02_despierto2 with fade

    $ violet_evento2_completado = True

    # Ejecutar la accion de dormir
    $ dormir()

    window hide
    jump game_loop

label evento2_violet_repetir:
    # Este label en la arquitectura original retorna para dejar que el botón de dormir se encargue
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    scene violet_evento02_fondo with fade

    piensa "No puedo dejar de pensar en el trasero de violet..."
    piensa "Tengo ese sueño grabado en la cabeza"

    # img1
    show violet_evento_02 img1 with dissolve
    pause 1.0
    # img2
    show violet_evento_02 img2 with dissolve
    pause 1.0
    # img3
    show violet_evento_02 img3 with dissolve
    pause 1.0
    # img5
    show violet_evento_02 img5 with dissolve
    pause 1.0
    # img6
    show violet_evento_02 img6 with dissolve
    pause 1.0
    
    piensa "Esto me va a terminar volviendo loco"

    hide violet_evento_02 with dissolve
    return
