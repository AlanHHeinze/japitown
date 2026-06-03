################################################################################
## Violet Quest 04_B — Hablar con Violet (perdón)
################################################################################
## Se dispara automáticamente al entrar en una locación donde esté Violet,
## o al golpear la puerta de su habitación (Violet sale al pasillo).


################################################################################
## QUEST 04_B — Label principal
################################################################################

label quest_violet_questprincipal_04_b:

    $ desactivar_restriccion()
    $ ocultar_hud()
    window show

    # Fondo de la locación actual (funciona tanto en pasillo como en otras locaciones)
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "Hola..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Te queria pedir perdón por"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Espera, te quiero hacer una pregunta primero"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Si, decime"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Por qué me trajiste ese regalo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Porque pensé que te gustaría"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Lo viste antes de comprarlo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Si, osea en un maniqui, se que es uno de tus personajes favoritos y queria que el regalo no fuera algo generico"
    show mc_parado_base b_abiertachica
    mc "Aparte de eso pronto se va a hacer la Japicon y pense que seria un buen cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No hay otro tipo de intenciones detras del regalo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No, que puede haber detras de eso? es solo un cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "El tipo de cosplay que es, es un traje digamos que muy apretado..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Pero es asi el traje, no tiene nada de raro"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No creo que todos sean asi ya te digo que no hay posibilidades que vaya a usarlo en un evento"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Pero si de mostramelo a mi?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Lo voy a pensar"
    show violet_parada b_none

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## CHECK LOCACIÓN — Auto-trigger al entrar en locación donde esté Violet
################################################################################

label violet_quest04b_check_locacion:
    $ _violet_npc_04b = obtener_npc("violet")
    $ _loc_actual_04b = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
    if _violet_npc_04b and _violet_npc_04b.locacion_actual == _loc_actual_04b:
        jump quest_violet_questprincipal_04_b
    return


################################################################################
## PUERTA — Violet sale al pasillo cuando el MC golpea
################################################################################

label violet_quest04b_puerta:

    $ ocultar_hud()
    window show

    play sound "audio/sfx/door_knock_3.ogg"
    pause 0.5

    mc "Soy yo"

    violet "Ahí salgo"

    pause 0.5

    jump quest_violet_questprincipal_04_b
