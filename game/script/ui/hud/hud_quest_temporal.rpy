################################################################################
## Cartel de "Quest temporal activa"
################################################################################
## Cuadro centrado que avisa que arranca una mision con fecha de vencimiento:
## dura unos dias y su cierre depende de lo que el jugador haga (o deje de
## hacer) mientras tanto.
##
## Es GENERICO a proposito: no sabe de ninguna quest. Se muestra con
##
##     call quest_temporal_aviso
##
## y el label espera el click. Hoy lo usa la 09_a de Violet; cualquier quest
## temporal futura lo reusa sin tocar este archivo.
##
## El azul es el MISMO del celular (#1e1e3a): el juego ya usa ese color para
## "esto es un panel del sistema, no parte de la escena".

define QT_FONDO = "#1e1e3aF5"
define QT_BORDE = "#4FC3F7"

# Los ⚠️ hacen de signos de admiracion: por eso el texto va sin "¡ !".
define QT_TEXTO = "⚠️ Quest temporal activa ⚠️"


screen quest_temporal_cartel():
    zorder 160

    $ _qt_k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Barra superior e inferior del borde: se dibujan como dos frames finos
    # dentro del cuadro en vez de con un borde real, que Ren'Py no tiene para
    # un `frame` de color plano.
    frame:
        xalign 0.5
        yalign 0.5
        xpadding int(60 * _qt_k)
        ypadding int(34 * _qt_k)
        background QT_FONDO

        vbox:
            spacing int(10 * _qt_k)
            xalign 0.5

            frame:
                xfill True
                ysize max(2, int(2 * _qt_k))
                background QT_BORDE

            text renpy.translate_string(QT_TEXTO):
                size int(38 * _qt_k)
                color "#ffffff"
                bold True
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            frame:
                xfill True
                ysize max(2, int(2 * _qt_k))
                background QT_BORDE


################################################################################
## Label — muestra el cartel y espera el click
################################################################################
## SUBRUTINA: el caller sigue con su escena despues, asi que termina en
## `return` (regla 4 del skill).

label quest_temporal_aviso:
    show screen quest_temporal_cartel
    with dissolve
    pause
    hide screen quest_temporal_cartel
    with dissolve
    return
