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
    mc "¿Cómo estás?"
    show mc_parado_base b_felizcerrada

    show violet_parada b_hablandochica
    violet "Bien... ¿Qué quieres?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Nada, solo te saludaba"
    show mc_parado_base b_felizcerrada c_rbase_base with sprite_normal

    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_juzgandonm c_pijama_base with sprite_normal
    else:
        show violet_parada b_hablandochica o_juzgandonm c_rbase_pensando with sprite_normal
    violet "Conozco esa mirada, estás pensando algo"
    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_none o_base c_pijama_base with sprite_normal
    else:
        show violet_parada b_none o_base c_rbase_base with sprite_normal

    show mc_parado_base b_felizabierta o_cerrados
    mc "En nada en particular... bueno... quizás un poco en tu trasero jajaja"
    show mc_parado_base b_felizcerrada o_base

    show violet_parada b_hablandochica o_enojados
    violet "Basta con eso, no quiero que hables más del tema"
    show violet_parada b_none

    show mc_parado_base b_felizabierta
    mc "Es un GRAN tema del que podemos hablar"
    show mc_parado_base b_felizcerrada

    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_normal
    else:
        show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_normal
    violet "No y menos en cualquier lugar de la casa como si fuera algo normal"
    if vq4d_cuerpo == "c_pijama":
        show violet_parada b_none c_pijama_base with sprite_normal
    else:
        show violet_parada b_none c_rbase_base with sprite_normal

    hide violet_parada with dissolve

    piensa "Es muy divertido molestarla pero no sé qué tan buena idea es, a este paso no la voy a poder convencer de que use el cosplay"
    piensa "Todavía quedan fotos que no vi, podría portarme bien y hacer cosas por ella"
    piensa "Puede que así logre que me mande las fotos"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d")

    # Terminal de contenido: jump game_loop (si el camino hasta aca vino con
    # frames, los drena el inicio del game_loop).
    window hide
    $ mostrar_hud()
    jump game_loop
