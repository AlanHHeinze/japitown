################################################################################
## Quest 05_a — Un nuevo cosplay
################################################################################

################################################################################
## Variables de estado
################################################################################

default coxplay_q5a_completada = False
default coxplay_pedido_dia = 0

################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_05_a:
    jump violet_quest05a_hablar

################################################################################
## HABLAR — versión genérica (desde interacción directa o botón Listo)
################################################################################

label violet_quest05a_hablar:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, quería contarte que compré los cosplay."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Que compraste?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Compré una promo de tres, una box armada"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Qué personajes son?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No sé exactamente, era un combo ya armado."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Raro... ¿Y vos qué te compraste?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Voy a esperar que elijas uno de los tres y me compro algo acorde."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Está bien, avisame cuando llegue el pedido."
    show violet_parada b_none

    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## PUERTA — Violet sale al pasillo arriba
################################################################################

label violet_quest05a_puerta:

    $ ocultar_hud()
    window show

    mc "Violet, tengo algo para contarte."

    violet "Ahí salgo."

    pause 0.5

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Conseguí los cosplay que te comenté, quería avisarte."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Cosplay?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Compré una promo de tres, una box armada. Son para vos."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Qué personajes son?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No sé exactamente, era un combo ya armado."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Y vos qué te compraste?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Voy a esperar que elijas uno de los tres y me compro algo acorde."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Está bien, avisame cuando llegue el pedido."
    show violet_parada b_none

    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop
