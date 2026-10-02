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

## Escala del contenido interno de cada app (títulos, textos, emojis, íconos)
## en pantalla táctil. Cada screen de app computa su propio "$ _k = ..." local
## a partir de esta constante (igual que _celular_barra_status ya hace consigo
## misma): no hace falta pasarlo como parámetro entre screens anidados, cada
## uno puede volver a preguntar renpy.variant("small") sin costo.
define CEL_APP_ESCALA_SMALL = 3.0

################################################################################
## Fondo del celular
################################################################################
## En PC/tablet: la imagen del celular. En táctil no hay imagen propia todavía,
## así que se usa un color plano de pantalla completa (gris oscuro, estilo modo
## incógnito). Screen único: evita que cada panel repita el "add" de la imagen
## y se olvide de la rama táctil (fue justo lo que pasó: cada panel nuevo
## seguía cargando la imagen de escritorio en table small).

screen _celular_fondo():
    if renpy.variant("small"):
        frame:
            xfill True
            yfill True
            background "#1C1C1EFF"
    else:
        add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

################################################################################
## Cierre exterior + botón cerrar del celular
################################################################################
## Clickear FUERA del celular lo cierra. Clickear DENTRO (zonas vacías entre
## botones, márgenes) no hace nada: un bloqueador cubre el rectángulo del
## celular y traga esos clicks. También hay un botón de cerrar en la esquina.

screen _celular_cerrar_exterior(screen_actual):

    if renpy.variant("small"):
        # Pantalla táctil: el celular ocupa toda la pantalla, no hay "afuera".
        # El botón de cerrar vive en _celular_app_header (o, en el home, en su
        # propio botón) ahora; acá solo queda el bloqueador para que no se
        # filtren clicks a lo de atrás.
        button:
            style "empty_button"
            xfill True
            yfill True
            action NullAction()

    else:
        # Capa 1 — fuera del celular: cierra todo
        button:
            style "empty_button"
            xfill True
            yfill True
            if modo_ajuste_celular:
                action NullAction()
            else:
                action [Hide(screen_actual), SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]

        # Capa 2 — dentro del celular (con margen por el marco): traga los clicks
        button:
            style "empty_button"
            xpos (ajuste_cel_area_x - 30)
            ypos ajuste_cel_area_y
            xysize (ajuste_cel_area_w + 60, ajuste_cel_area_h)
            action NullAction()

        # Botón cerrar — junto a la esquina superior derecha del celular.
        # Dice "X" (letra) y no "✕" (U+2715): ese es un dingbat que las fuentes
        # del juego no traen y salia como cuadradito de glifo faltante. Es el
        # mismo criterio que ya usaba el boton de cerrar de la variante tactil,
        # mas abajo en este archivo.
        button:
            xpos (ajuste_cel_area_x + ajuste_cel_area_w + 42)
            ypos (ajuste_cel_area_y + 8)
            xysize (52, 52)
            background "#1e1e3aEE"
            hover_background "#E53935"
            if modo_ajuste_celular:
                action NullAction()
            else:
                action [Hide(screen_actual), SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
            text "X" size 26 color "#ffffff" bold True xalign 0.5 yalign 0.5


################################################################################
## Barra de Estado (Status Bar) — parte superior del celular
################################################################################

screen _celular_barra_status(screen_actual=None):

    if renpy.variant("small"):
        # Táctil: eliminada. El título de la app + botón volver + botón cerrar
        # de _celular_app_header pasaron a ser la única fila superior (el home,
        # que no tiene app_header, pone su propio botón de cerrar).
        null
    else:
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

screen _celular_app_header(titulo, icono="", accion_volver=None, screen_actual=None):
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    if renpy.variant("small"):
        # Táctil: única fila superior — volver (izquierda), título centrado,
        # cerrar (derecha). Reemplaza a la barra de estado eliminada.
        frame:
            xsize ajuste_cel_area_w
            ysize int(55 * _k)
            background "#12122aFF"
            padding (int(10 * _k), 0)

            fixed:
                xfill True
                yfill True

                if accion_volver:
                    textbutton "◀":
                        xalign 0.0
                        yalign 0.5
                        action accion_volver
                        text_size int(44 * _k)
                        text_color "#4FC3F7"
                        text_hover_color "#81D4FA"
                        padding (int(8 * _k), int(5 * _k))

                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing int(8 * _k)
                    if icono:
                        text icono size int(20 * _k) yalign 0.5
                    text titulo size int(18 * _k) color "#ffffff" bold True yalign 0.5

                if screen_actual:
                    button:
                        xalign 1.0
                        yalign 0.5
                        xysize (int(44 * _k), int(44 * _k))
                        background "#E53935EE"
                        hover_background "#FF5449"
                        if modo_ajuste_celular:
                            action NullAction()
                        else:
                            action [Hide(screen_actual), SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
                        text "X" size int(24 * _k) color "#ffffff" bold True xalign 0.5 yalign 0.5

            # Linea inferior sutil
            frame:
                xfill True
                ysize int(1 * _k)
                yalign 1.0
                background "#ffffff11"

    else:
        frame:
            xsize ajuste_cel_area_w
            ysize 55
            background "#12122aFF"
            padding (10, 0)

            # Mismo layout que la variante tactil: el titulo se centra en el
            # ancho del header (fixed + xalign 0.5), no despues del boton
            # volver — con el hbox de antes quedaba corrido a la derecha.
            fixed:
                xfill True
                yfill True

                # Boton volver
                if accion_volver:
                    textbutton "◀":
                        xalign 0.0
                        yalign 0.5
                        action accion_volver
                        text_size 44
                        text_color "#4FC3F7"
                        text_hover_color "#81D4FA"
                        padding (8, 5)

                # Icono + titulo, centrados
                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 8
                    if icono:
                        text icono size 20 yalign 0.5
                    text titulo size 18 color "#ffffff" bold True yalign 0.5

            # Linea inferior sutil
            frame:
                xfill True
                ysize 1
                yalign 1.0
                background "#ffffff11"
