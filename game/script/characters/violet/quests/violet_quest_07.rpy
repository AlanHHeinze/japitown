################################################################################
## Violet Quest 07 — Cadena de afinidad del cosplay
################################################################################
## Labels narrativos para quests 4, 5 y 6
## La conversacion principal ocurre en el chat (chat_violet.rpy)
## Estos labels se ejecutan al completar el chat y hacer click en Violet


################################################################################
## QUEST 7 — Afinidad 20
################################################################################

label quest_violet_questprincipal_7:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    show mc_parado_base b_hablando
    mc "Tenía razón, el cosplay te queda genial, deberías usarlo"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Ya te dije que no, solo te lo mostré porque tanto insististe"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Bueno... no te voy a insistir mas"
    show mc_parado_base b_none

    violet "..."

    show violet_parada b_hablandochica
    violet "Gracias"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Nos vemos luego"
    show mc_parado_base b_none

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop




