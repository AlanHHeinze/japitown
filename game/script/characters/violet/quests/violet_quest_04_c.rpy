################################################################################
## Violet Quest 04_C — Cadena de afinidad del cosplay (deseo 20)
################################################################################
## La conversacion principal ocurre en el chat (chat_violet.rpy)
## Este label se ejecuta al completar el chat y hacer click en Violet


################################################################################
## QUEST 04_C — Deseo 20
################################################################################

# El primer mensaje se lo muestra y despues sigue este texto

label quest_violet_questprincipal_04_c:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    show mc_parado_base b_hablando
    mc "El cosplay te queda genial, deberías usarlo"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Ya te dije que no, solo te lo mostré porque insististe"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Y te voy a seguir insistiendo, te queda genial y lo tenes que usar"
    show mc_parado_base b_abiertachica
    mc "La Japicon sera dentro de poco tiempo"
    show mc_parado_base b_none

    violet "..."

    show violet_parada b_hablandochica
    violet "No voy a usar eso en un evento, suficiente que te mande una de las fotos"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Te sacaste mas fotos?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No hay ninguna foto mas y se termino el tema aca"
    show violet_parada b_none

    hide violet_parada with dissolve

    piensa "Violet se saco mas fotos, si logre que me mande una, puedo lograr que me mande las otras tambien"
    piensa "Sera cosa de seguir mejorarndo la relacion"
    
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
