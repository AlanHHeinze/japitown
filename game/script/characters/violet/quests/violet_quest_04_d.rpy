################################################################################
## Violet Quest 04_D — Cadena de afinidad del cosplay (deseo 25)
################################################################################
## La conversacion principal ocurre en el chat (chat_violet.rpy)
## Este label se ejecuta al completar el chat y hacer click en Violet

default vq4d_cuerpo = "c_rbase"

################################################################################
## QUEST 04_D — Deseo 25
################################################################################

label quest_violet_questprincipal_04_d:

    $ vq4d_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4d_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    show mc_parado_base b_hablando
    mc "¿Cómo estas?"
    show mc_parado_base b_felizcerrada

    show violet_parada b_hablandochica
    violet "Bien... ¿Qué queres?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Nada, solo te saludaba"
    show mc_parado_base b_felizcerrada c_rbase_base with sprite_fast

    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_juzgandonm c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica o_juzgandonm c_rbase_pensando with sprite_fast
    violet "Conozco esa mirada, estas pensando algo"
    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_none o_base c_pijama_base with sprite_fast
    else:
        show violet_parada b_none o_base c_rbase_base with sprite_fast

    show mc_parado_base b_felizabierta o_cerrados
    mc "En nada en particular... bueno... quizás un poco en tu trasero jajaja"
    show mc_parado_base b_felizcerrada o_base

    show violet_parada b_hablandochica o_enojados
    violet "Basta con eso, no quiero que hables mas del tema"
    show violet_parada b_none

    show mc_parado_base b_felizabierta
    mc "Es un GRAN tema del que podemos hablar"
    show mc_parado_base b_felizcerrada

    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_fast
    violet "No y menos en cualquier lugar de la casa como si fuera algo normal"
    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_none c_pijama_base with sprite_fast
    else:
        show violet_parada b_none c_rbase_base with sprite_fast

    hide violet_parada with dissolve

    piensa "Es muy divertido molestarla pero no sé que tan buena idea es, a este paso no la voy a poder convencer de que use el cosplay"
    piensa "Le queda muy bien y lo que dice de su trasero es solo un complejo"
    piensa "Tengo que lograr que se sienta comoda y no lo vea como algo malo"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
