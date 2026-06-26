################################################################################
## Violet Quest 04_C — Cadena de afinidad del cosplay (deseo 20)
################################################################################
## La conversacion principal ocurre en el chat (chat_violet.rpy)
## Este label se ejecuta al completar el chat y hacer click en Violet

# Skin activo al entrar a la quest (persiste en saves)
default vq4c_cuerpo = "c_rbase"

################################################################################
## QUEST 04_C — Deseo 20
################################################################################

# El primer mensaje se lo muestra y despues sigue este texto

label quest_violet_questprincipal_04_c:

    $ vq4c_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4c_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    show mc_parado_base b_hablando
    mc "El cosplay te queda genial, deberías usarlo"
    show mc_parado_base b_none

    if vq4c_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_fast
    violet "Ya te dije que no, solo te lo mostré por cortezia"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "Pero no le veo el problema"
    show mc_parado_base b_abiertachica
    mc "La Japicon sera dentro de poco tiempo"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada o_arribanm
    violet "..."
    show violet_parada b_hablandochica o_base
    violet "No voy a usar eso en un evento, suficiente que te mande una de las fotos"
    show violet_parada b_none

    show mc_parado_base o_arribanm c_rbase_pensando with sprite_fast
    piensa "¿Una de las fotos?"
    piensa "Entonces se saco más"

    show mc_parado_base b_hablando o_base
    mc "¿Te sacaste más fotos?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No hay ninguna foto más y fin del tema"
    if vq4c_cuerpo == "c_pijama":
        show violet_parada b_none c_pijama_base with sprite_fast
    else:
        show violet_parada b_none c_rbase_base with sprite_fast

    hide violet_parada with dissolve

    piensa "Violet se saco más fotos, si logre que me mande una, puedo lograr que me mande las otras también"
    piensa "Sera cosa de seguir mejorarndo la relación"
    
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
