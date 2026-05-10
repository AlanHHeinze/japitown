################################################################################
## Violet Quest 12 — Visita nocturna
################################################################################
## Label narrativo principal con 4 opciones, cada una lleva a un label propio
## Se dispara al entrar a la habitacion de Violet por la noche


################################################################################
## LABEL PRINCIPAL — Quest 8 de Violet
################################################################################

label quest_violet_questprincipal_12:

    $ ocultar_hud()
    window show

    # Escena nocturna en la habitacion de Violet
    scene expression "images/bg/casa/bg_casa_noche_hviolet.png" with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    # Dialogo introductorio placeholder
    show mc_parado_base b_hablando
    mc "Placeholder: Vine como me pediste, que pasa?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Placeholder: Queria mostrarte algo..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Placeholder: Que cosa?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Placeholder: (Violet explica la situacion)"
    show violet_parada b_none

    # Menu con 4 opciones
    menu:
        "Placeholder: Opcion A":
            jump violet_quest12_opcion_a
        "Placeholder: Opcion B":
            jump violet_quest12_opcion_b
        "Placeholder: Opcion C":
            jump violet_quest12_opcion_c
        "Placeholder: Opcion D":
            jump violet_quest12_opcion_d


################################################################################
## OPCION A
################################################################################

label violet_quest12_opcion_a:

    show mc_parado_base b_hablando
    mc "Placeholder: (Respuesta A del MC)"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Placeholder: (Reaccion de Violet a opcion A)"
    show violet_parada b_none

    piensa "Placeholder: (Pensamiento final del MC)"

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCION B
################################################################################

label violet_quest12_opcion_b:

    show mc_parado_base b_hablando
    mc "Placeholder: (Respuesta B del MC)"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Placeholder: (Reaccion de Violet a opcion B)"
    show violet_parada b_none

    piensa "Placeholder: (Pensamiento final del MC)"

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCION C
################################################################################

label violet_quest12_opcion_c:

    show mc_parado_base b_hablando
    mc "Placeholder: (Respuesta C del MC)"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Placeholder: (Reaccion de Violet a opcion C)"
    show violet_parada b_none

    piensa "Placeholder: (Pensamiento final del MC)"

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCION D
################################################################################

label violet_quest12_opcion_d:

    show mc_parado_base b_hablando
    mc "Placeholder: (Respuesta D del MC)"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Placeholder: (Reaccion de Violet a opcion D)"
    show violet_parada b_none

    piensa "Placeholder: (Pensamiento final del MC)"

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
