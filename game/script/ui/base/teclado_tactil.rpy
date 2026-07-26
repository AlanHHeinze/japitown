################################################################################
## Teclado táctil (web / celular) — override del _touch_keyboard de Ren'Py
################################################################################
## En la versión web sobre un dispositivo táctil, Ren'Py muestra el screen
## "_touch_keyboard" cada vez que un input toma foco (definido en
## renpy/common/00touchkeyboard.rpy). El default es una grilla translúcida
## gigante que se superpone a todo el juego y se ve rota en el celular.
##
## Este override lo reemplaza por un teclado estilo celular: anclado abajo,
## fondo sólido, filas QWERTY con ñ, toggle de mayúsculas y teclas grandes.
## Reusa las acciones del motor (_TouchKeyboardTextInput, _TouchKeyboardBackspace,
## _TouchKeyboardReturn), así el input recibe los mismos eventos de siempre.
## En desktop no cambia nada (el screen solo lo muestra el motor en táctil).

screen _touch_keyboard():
    layer config.interface_layer
    zorder 1100
    style_prefix "jp_teclado"

    default _tk_mayus = False

    frame:
        style "jp_teclado_panel"

        vbox:
            spacing 10
            xalign 0.5

            # Fila de números (por si algún input los permite; el nombre los filtra)
            hbox:
                spacing 8
                xalign 0.5
                for _tk_n in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
                    textbutton _tk_n action _TouchKeyboardTextInput(_tk_n)

            # Filas de letras
            for _tk_fila in (
                ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p"),
                ("a", "s", "d", "f", "g", "h", "j", "k", "l", "ñ"),
                ("z", "x", "c", "v", "b", "n", "m"),
            ):
                hbox:
                    spacing 8
                    xalign 0.5
                    for _tk_letra in _tk_fila:
                        if _tk_mayus:
                            # Tras escribir una mayúscula, volver a minúsculas (como un celular)
                            textbutton _tk_letra.upper():
                                action [_TouchKeyboardTextInput(_tk_letra.upper()), SetScreenVariable("_tk_mayus", False)]
                        else:
                            textbutton _tk_letra action _TouchKeyboardTextInput(_tk_letra)

            # Fila inferior: mayúsculas / espacio / borrar / confirmar
            hbox:
                spacing 8
                xalign 0.5

                textbutton _("Mayús"):
                    action ToggleScreenVariable("_tk_mayus")
                    background ("#0288D1" if _tk_mayus else "#26263A")
                    hover_background ("#4FC3F7" if _tk_mayus else "#3A3A55")

                textbutton _("Espacio"):
                    xminimum 520
                    action _TouchKeyboardTextInput(' ')

                textbutton _("Borrar"):
                    action _TouchKeyboardBackspace()

                textbutton _("Listo"):
                    background "#0288D1"
                    hover_background "#4FC3F7"
                    action _TouchKeyboardReturn()


style jp_teclado_panel:
    xalign 0.5
    yalign 1.0
    xfill True
    background "#101018F2"
    padding (20, 18, 20, 26)

style jp_teclado_button:
    background "#26263A"
    hover_background "#3A3A55"
    xminimum 150
    ysize 104
    padding (10, 8)

style jp_teclado_button_text:
    font "DejaVuSans.ttf"
    color "#FFFFFF"
    size 46
    xalign 0.5
    yalign 0.5
    textalign 0.5


################################################################################
## Área de ingreso de texto en pantalla chica
################################################################################
## El screen `input` por defecto vive dentro de la caja de diálogo, abajo de todo.
## En celular el teclado de arriba la tapa por completo, así que en la variante
## `small` se reemplaza por un panel propio ubicado POR ENCIMA del teclado.
##
## Solo aplica a `small`: en PC/tablet Ren'Py sigue usando el screen `input`
## original de screens.rpy, que no se toca.

# Alto del panel del teclado: 5 filas de 104 px + 4 separaciones de 10 +
# padding vertical (18 arriba + 26 abajo) = 604.
# Si se agregan/quitan filas o cambia jp_teclado_button.ysize, actualizar acá:
# es lo que usa el área de ingreso para saber dónde termina el teclado.
define JP_TECLADO_ALTO = 604

# Aire entre el área de ingreso y el borde superior del teclado.
define JP_TECLADO_MARGEN = 40


screen input(prompt):
    variant "small"
    style_prefix "input"

    # Anclado por abajo (yanchor 1.0) justo arriba del teclado: si el teclado
    # cambia de alto, el panel se reacomoda solo.
    frame:
        xfill True
        ypos (config.screen_height - JP_TECLADO_ALTO - JP_TECLADO_MARGEN)
        yanchor 1.0
        background "#101018F2"
        padding (60, 30, 60, 34)

        vbox:
            xalign 0.5
            spacing 24

            text prompt:
                style "input_prompt"
                xalign 0.5
                textalign 0.5

            input:
                id "input"
                xalign 0.5
