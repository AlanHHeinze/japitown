################################################################################
## Evento 2 de Violet - Noche post Quest 3.2
################################################################################
## Este evento se dispara automáticamente la primera vez que el jugador va a
## dormir despues de haber completado la Quest 3.2 de Violet.
## Tambien contiene el label para la versión repetible del evento.

################################################################################
## Imagenes
################################################################################

image violet_evento02_fondo = "images/eventos/violet/evento2/violet_evento02_fondo.jpg"
image violet_evento02_despierto = "images/eventos/violet/evento2/violet_evento02_despierto.jpg"
image violet_evento02_despierto2 = "images/eventos/violet/evento2/violet_evento02_despierto2.jpg"

layeredimage violet_evento_02:
    group pose:
        attribute img1 default:
            "images/eventos/violet/evento2/violet_evento02_img1.webp"
        attribute img2:
            "images/eventos/violet/evento2/violet_evento02_img2.webp"
        attribute img3:
            "images/eventos/violet/evento2/violet_evento02_img3.webp"
        attribute img4:
            "images/eventos/violet/evento2/violet_evento02_img4.webp"
        attribute img5:
            "images/eventos/violet/evento2/violet_evento02_img5.webp"
        attribute img6:
            "images/eventos/violet/evento2/violet_evento02_img6.webp"

################################################################################
## Variables guardables
################################################################################

default violet_evento2_completado = False
default violet_evento2_repetir = False


# ── Trigger de dormir (fase "antes") ────────────────────────────────────────
# El evento nocturno se dispara al dormir, 1 dia despues de completar la
# quest 04_e (corre ANTES de dormir(): la escena maneja el avance del dia y
# hace su propio autoguardado al salir).

init python:

    def _dormir_trigger_violet_evento2():
        q4e = store.sistema_quests.obtener_quest("violet_questprincipal_04_e")
        q5a = store.sistema_quests.obtener_quest("violet_questprincipal_05_a")
        if (not store.violet_evento2_completado
                and q4e and q4e.completada
                and q5a and q5a.dia_inicio is not None
                and getattr(store, 'dias_totales', 1) > q5a.dia_inicio):
            return "evento2_violet"
        return None

init 5 python:
    registrar_trigger_dormir("violet_evento2", "antes", _dormir_trigger_violet_evento2)

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
    violet "¿Esto querías ver? Pervertido"
    mc "Sí, estaba deseando ese trasero"

    # img6
    show violet_evento_02 img6 with dissolve
    violet "Bueno, entonces ven a buscarlo"


    hide violet_evento_02 with dissolve

    scene violet_evento02_despierto with fade
    piensa "Eso fue bastante raro..."
    piensa "Va a ser mejor que me vuelva a dormir"
    scene violet_evento02_despierto2 with fade

    $ violet_evento2_completado = True

    # Ejecutar la accion de dormir
    $ dormir()

    # Este evento se dispara ANTES del dormir() de accion_dormir y salta afuera,
    # asi que necesita su propio autoguardado (si no, la noche del evento 2
    # quedaria sin punto de recuperacion).
    $ autoguardar_partida()

    window hide
    jump game_loop

label evento2_violet_repetir:
    # Este label en la arquitectura original retorna para dejar que el botón de dormir se encargue
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    scene violet_evento02_fondo with fade

    piensa "No puedo dejar de pensar en el trasero de Violet..."
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
