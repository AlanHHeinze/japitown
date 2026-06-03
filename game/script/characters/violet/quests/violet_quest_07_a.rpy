################################################################################
## Quest 07_a — El cierre del cosplay
################################################################################

################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_07_a:
    jump violet_quest07a_hablar


################################################################################
## HABLAR — Conversación en la locación actual
################################################################################

label violet_quest07a_hablar:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    if violet_06b_eleccion == "A":
        jump violet_quest07a_outcome_a
    else:
        jump violet_quest07a_outcome_c


################################################################################
## PUERTA — Violet sale al pasillo
################################################################################

label violet_quest07a_puerta:

    $ ocultar_hud()
    window show

    mc "Violet, quería preguntarte por el cosplay"

    violet "Ahí salgo"

    pause 0.5

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    if violet_06b_eleccion == "A":
        jump violet_quest07a_outcome_a
    else:
        jump violet_quest07a_outcome_c


################################################################################
## OUTCOME A — Monica lo pudo destrabar pero el cierre está fallado
################################################################################

label violet_quest07a_outcome_a:

    show violet_parada b_hablandochica
    violet "Monica lo pudo destrabar, pero me dijo que el cierre está fallado"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Y qué hacemos entonces?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Me recomendó pedirle a la tienda que lo cambie"
    show violet_parada b_none

    show violet_parada b_hablandochica
    violet "Se va a seguir trabando, y si me pasa en la convención cuando quiera ir al baño va a ser un problema"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Voy a hablar con la tienda para pedir el cambio"
    show mc_parado_base b_none

    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OUTCOME C — El cierre está totalmente destruido
################################################################################

label violet_quest07a_outcome_c:

    show violet_parada b_hablandochica
    violet "El cierre está totalmente destruido"
    show violet_parada b_none

    show violet_parada b_hablandochica
    violet "Le pregunté a Monica si lo podía arreglar y me dijo que no iba a quedar muy bien"
    show violet_parada b_none

    show violet_parada b_hablandochica
    violet "Hablá con la tienda y probá a ver si te lo cambian"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Voy a hablar con la tienda para pedir el cambio"
    show mc_parado_base b_none

    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop
