################################################################################
## Componentes UI Comunes del Celular
################################################################################
## Screens reutilizables para simular la interfaz de un smartphone.
## Barra de estado, header de app, y frame contenedor.

## Constantes del area del celular
define CEL_XPOS = 630
define CEL_YPOS = 0
define CEL_WIDTH = 660
define CEL_HEIGHT = 1080

################################################################################
## Fondo clickeable para cerrar celular desde cualquier sub-screen
################################################################################

screen _celular_cerrar_exterior(screen_actual):
    """Boton invisible full-screen que cierra el sub-screen y el celular al clickear fuera."""
    button:
        style "empty_button"
        xfill True
        yfill True
        if modo_ajuste_celular:
            action NullAction()
        else:
            action [Hide(screen_actual), SetVariable("menu_celular_abierto", False), Hide("menu_celular")]


################################################################################
## Barra de Estado (Status Bar) — parte superior del celular
################################################################################

screen _celular_barra_status():
    frame:
        xsize ajuste_cel_area_w
        ysize 32
        background "#0a0a18FF"
        padding (15, 0)

        hbox:
            yalign 0.5
            xfill True

            # Lado izquierdo — hora del juego
            hbox:
                spacing 6
                yalign 0.5
                $ _horario_texto = ["Mañana", "Tarde", "Noche", "Trasnoche"][horario_actual]
                text _horario_texto size 12 color "#aaaaaa" yalign 0.5

            # Lado derecho — íconos decorativos
            hbox:
                spacing 8
                xalign 1.0
                yalign 0.5
                text "📶" size 11 yalign 0.5
                text "🔋" size 11 yalign 0.5


################################################################################
## Header de App — barra de navegacion con titulo y volver
################################################################################

screen _celular_app_header(titulo, icono="", accion_volver=None):
    frame:
        xsize ajuste_cel_area_w
        ysize 55
        background "#12122aFF"
        padding (10, 0)

        hbox:
            yalign 0.5
            xfill True
            spacing 10

            # Boton volver
            if accion_volver:
                textbutton "◀":
                    action accion_volver
                    text_size 44
                    text_color "#4FC3F7"
                    text_hover_color "#81D4FA"
                    yalign 0.5
                    padding (8, 5)

            # Icono + titulo
            hbox:
                spacing 8
                yalign 0.5
                if icono:
                    text icono size 20 yalign 0.5
                text titulo size 18 color "#ffffff" bold True yalign 0.5

        # Linea inferior sutil
        frame:
            xfill True
            ysize 1
            yalign 1.0
            background "#ffffff11"
