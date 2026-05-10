################################################################################
## QUEST 8 — Afinidad 25
################################################################################

label quest_violet_questprincipal_8:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    show mc_parado_base b_hablando
    mc "¿Como estas?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bien"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Veo que te lo volviste a probar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No, esa foto es del otro dia"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Te sacaste mas?"
    show mc_parado_base b_none

    violet "..."

    hide violet_parada with dissolve

    piensa "Es bueno saber que hay más fotos, tendría que seguir mejorando nuestra afinidad"
    
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
