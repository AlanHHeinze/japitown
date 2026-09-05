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

    show mc_parado_base b_hablando c_rbase_idea with sprite_normal
    mc "Violet, tengo una idea"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_normal
    else:
        show violet_parada b_hablandochica c_rbase_pensando with sprite_normal
    violet "No sé si quiero saberla, últimamente tus ideas no son buenas para mí"
    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_none c_pijama_base with sprite_normal
    else:
        show violet_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base b_hablando
    mc "No, esta es buena, podría encargar en la tienda un cosplay nuevo y que lo envíen, si no quieres usar el que tienes, podemos comprar otro"
    show mc_parado_base b_abiertachica c_rbase_brazoscruzados with sprite_normal
    mc "No voy a insistirte más con el cosplay, pero si en que vayamos a la Japicon"
    show mc_parado_base b_none

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica ot_avergonzada c_pijama_base with sprite_normal
    else:
        show violet_parada b_hablandochica ot_avergonzada c_rbase_dedolabio with sprite_normal
    violet "No sé... sigue dándome vergüenza la idea"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_idea with sprite_normal
    mc "Piensa que va a ir mucha gente y mucha va a usar cosplay, no te tiene que dar vergüenza"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica ot_none c_pijama_base with sprite_normal
    else:
        show violet_parada b_hablandochica ot_none c_rbase_pensando with sprite_normal
    violet "¿Y tú vas a usar algo?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "No lo pensé, pero si te hace sentir más cómoda, puedo usar algún cosplay también"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    if vq4e_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_normal
    else:
        show violet_parada b_hablandochica c_rbase_base with sprite_normal
    violet "Está bien, pero que no sea algo tan llamativo y apretado esta vez"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Tengo el contacto del chico de la tienda, le voy a escribir para ver qué opciones hay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "Está bien... pero no te emociones, no es que ya acepté usarlo, depende mucho de lo que sea"
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

    piensa "Bueno tengo que conseguir un cosplay para Violet y uno para mí, espero que esto no me cueste mucho dinero"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_e")

    # Terminal de contenido: jump game_loop (si el camino hasta aca vino con
    # frames, los drena el inicio del game_loop).
    window hide
    $ mostrar_hud()
    jump game_loop
