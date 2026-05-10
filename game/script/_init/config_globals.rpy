
default mc_name = ""
define mc = Character("[mc_name]", color="#56b6c2")


init python:

    import re as _re_nombre

    _LETRAS_PERMITIDAS_NOMBRE = (
        u"abcdefghijklmnopqrstuvwxyz"
        u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        u" "
        u"áéíóúüñÁÉÍÓÚÜÑàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛäëïöÄËÏÖ"
    )

    def _nombre_mc_valido(nombre):
        s = nombre.strip()
        if not s:
            return True
        return bool(_re_nombre.match(r'^[a-zA-ZÀ-ÿ\s]+$', s))


screen name_input_screen(nombre_previo=u"", error_msg=u""):

    default name = nombre_previo
    default name_iv = ScreenVariableInputValue("name", returnable=True)

    modal True

    add "gui/overlay/confirm.png"

    frame:
        style "name_input_frame"

        vbox:
            xalign 0.5
            spacing 18

            label _("Ingresa el nombre del personaje"):
                style "name_input_title"
                xalign 0.5

            text _("Nombre por defecto: Mc"):
                xalign 0.5
                size 22
                color "#AAAAAA"

            null height 10

            frame:
                xalign 0.5
                xsize 480
                background "#111111CC"
                padding (18, 12, 18, 12)

                input:
                    value name_iv
                    length 20
                    allow _LETRAS_PERMITIDAS_NOMBRE
                    size 28
                    color "#FFFFFF"

            if error_msg:
                text error_msg:
                    xalign 0.5
                    size 20
                    color "#FF5252"
                    xmaximum 520
                    textalign 0.5
                    layout "subtitle"
            else:
                null height 28

            null height 6

            hbox:
                xalign 0.5
                spacing 50

                textbutton _("Confirmar"):
                    style "name_input_button"
                    action Return(name)

                textbutton _("Cancelar"):
                    style "name_input_button"
                    action Return(mc_name)


style name_input_frame is confirm_frame:
    xminimum 640
    padding (50, 44, 50, 44)

style name_input_title is gui_label

style name_input_title_text is gui_label_text:
    size 30
    color "#4FC3F7"
    outlines [(2, "#0288D180", 0, 0)]
    xalign 0.5

style name_input_button is confirm_button

style name_input_button_text is confirm_button_text:
    color "#FFFFFF"
    hover_color "#FFB74D"


label choose_name:

    $ _nc_previo = u""
    $ _nc_error = u""

    label .loop:

        $ _nc_nombre = renpy.call_screen(
            "name_input_screen",
            nombre_previo=_nc_previo,
            error_msg=_nc_error
        )
        $ _nc_nombre = _nc_nombre.strip() if _nc_nombre else u""

        if _nc_nombre and not _nombre_mc_valido(_nc_nombre):
            $ _nc_previo = _nc_nombre
            $ _nc_error = _("El nombre no puede contener números ni caracteres especiales")
            jump .loop

        $ mc_name = _nc_nombre if _nc_nombre else u"Mc"

    return
