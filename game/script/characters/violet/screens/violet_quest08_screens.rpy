################################################################################
## Screens de la Quest 8 de Violet — Los ruidos nocturnos
################################################################################
## Menu de seleccion de items para aplicar a Violet


screen violet_quest8_menu_items():

    modal True

    # Fondo oscuro semi-transparente
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background "#00000088"
        action Return("volver")

    # Panel central con opciones
    frame:
        xalign 0.5
        yalign 0.5
        xsize 400
        ypadding 20
        xpadding 20
        background "#1a1a2e"

        vbox:
            spacing 10
            xfill True

            text "Que quieres usar?" size 22 color "#ffffff" xalign 0.5

            null height 10

            # Opcion: Jabon
            if "jabon_quest" in inventario and inventario["jabon_quest"] > 0 and not vq7_opcion_jabon:
                button:
                    xfill True
                    background "#009688"
                    hover_background "#4DB6AC"
                    padding (15, 10)
                    action Return("jabon")
                    text "🧼 Usar jabon" size 18 color "#ffffff"

            # Opcion: Aceite
            if "aceite_quest" in inventario and inventario["aceite_quest"] > 0 and not vq7_opcion_aceite:
                button:
                    xfill True
                    background "#009688"
                    hover_background "#4DB6AC"
                    padding (15, 10)
                    action Return("aceite")
                    text "🫗 Usar aceite" size 18 color "#ffffff"

            # Opcion: Silicona
            if "silicona_quest" in inventario and inventario["silicona_quest"] > 0 and not vq7_opcion_silicona:
                button:
                    xfill True
                    background "#009688"
                    hover_background "#4DB6AC"
                    padding (15, 10)
                    action Return("silicona")
                    text "🧴 Usar silicona" size 18 color "#ffffff"

            null height 5

            # Boton volver
            button:
                xfill True
                background "#333355"
                hover_background "#444466"
                padding (15, 10)
                action Return("volver")
                text "Volver" size 18 color "#aaaaaa" xalign 0.5
