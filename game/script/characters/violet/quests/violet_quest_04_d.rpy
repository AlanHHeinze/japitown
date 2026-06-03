################################################################################
## Violet Quest 04_D — Cadena de afinidad del cosplay (deseo 25)
################################################################################
## La conversacion principal ocurre en el chat (chat_violet.rpy)
## Este label se ejecuta al completar el chat y hacer click en Violet


################################################################################
## QUEST 04_D — Deseo 25
################################################################################

label quest_violet_questprincipal_04_d:

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
    violet "Bien... ¿Que queres?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Nada, solo te saludaba"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Conozco esa mirada, estas pensando algo"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "En nada en particular... bueno... quizas un poco en tu trasero jajaja"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Basta con eso, no quiero que hables mas del tema"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Es un GRAN tema del que podemos hablar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No y menos en cualquier lugar de la casa como si fuera algo normal"
    show violet_parada b_none

    hide violet_parada with dissolve

    piensa "Es muy divertido molestarla pero no se que tan buena idea es, a este paso no la voy a poder convencer de que use el cosplay"
    piensa "Le queda muy bien y lo que dice de su trasero es solo un complejo"
    piensa "Tengo que lograr que se sienta comoda y no lo vea como algo malo"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
