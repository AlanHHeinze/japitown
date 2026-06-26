################################################################################
## Violet Quest 04_E — Cadena de afinidad del cosplay (deseo 30)
################################################################################
## La conversacion principal ocurre en el chat (chat_violet.rpy)
## Este label se ejecuta al completar el chat y hacer click en Violet

default vq4e_cuerpo = "c_rbase"

################################################################################
## QUEST 04_E — Deseo 30
################################################################################

label quest_violet_questprincipal_04_e:

    $ vq4e_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4e_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando c_rbase_idea with sprite_fast
    mc "Violet tengo una idea"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_pensando with sprite_fast
    violet "No se si quiero saberla, ultimamente tus ideas no son buenas para mi"
    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_none c_pijama_base with sprite_fast
    else:
        show violet_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_hablando 
    mc "No, esta es buena, podría encargar en la tienda un cosplay nuevo y que lo envien, si no queres usar el que tenes, podemos comprar otro"
    show mc_parado_base b_abiertachica c_rbase_brazoscruzados with sprite_fast
    mc "No voy a insistirte más con el cosplay, pero si en que vayamos a la Japicon"
    show mc_parado_base b_none

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica ot_avergonzada c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica ot_avergonzada c_rbase_dedolabio with sprite_fast
    violet "No se... sigue dandome verguenza la idea"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_idea with sprite_fast
    mc "Piensa que va a ir mucha gente y mucha va a usar cosplay, no te tiene que dar verguenza"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica ot_none c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica ot_none c_rbase_pensando with sprite_fast
    violet "¿Y tú vas a usar algo?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "No lo pense, pero si te hace sentir más comoda, puedo usar algún cosplay también"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_base with sprite_fast
    violet "Esta bien, pero que no sea algo tan llamativo y apretado esta vez"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Tengo el contacto del chico de la tienda, le voy a escribir para ver que opciones hay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "Esta bien... pero no te emociones, no es que ya acepte usarlo, depende mucho de lo que sea"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Cuando sepa algo te aviso"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Nos vemos"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Nos vemos"
    show mc_parado_base b_none

    hide violet_parada with dissolve

    piensa "Bueno tengo que conseguir un cosplay para Violet y uno para mi, espero que esto no me cueste mucho dinero"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
