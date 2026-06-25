################################################################################
## Quest 07_b — El cambio del cosplay
################################################################################

################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_07_b:
    jump violet_quest07b_hablar


################################################################################
## HABLAR — Conversacion en la locación actual
################################################################################

label violet_quest07b_hablar:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    jump violet_quest07b_conversacion


################################################################################
## PUERTA — Violet sale al pasillo
################################################################################

label violet_quest07b_puerta:

    $ ocultar_hud()
    window show

    mc "Violet, te quería contar algo"

    violet "Ahí salgo"

    pause 0.5

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    jump violet_quest07b_conversacion


################################################################################
## CONVERSACIÓN — Compartida entre hablar y puerta
################################################################################

label violet_quest07b_conversacion:

    show mc_parado_base b_hablando
    mc "Hablé con la tienda por el cosplay"
    show mc_parado_base b_none

    show mc_parado_base b_hablando
    mc "Hay que enviarlo para que le hagan el cambio del cierre"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bien, yo me encargo de mandarlo"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Perfecto"
    show mc_parado_base b_none

    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop
