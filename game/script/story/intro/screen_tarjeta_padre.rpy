
screen menu_tarjeta_padre():

    modal True
    zorder 200

    add Solid("#00000088")

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Rechazar la tarjeta":
            style "choice_button"
            action Jump("rechazar_tarjeta_padre")

        textbutton "Tomar la tarjeta":
            style "choice_button"
            action Jump("tomar_tarjeta_padre")
