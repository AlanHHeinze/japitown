################################################################################
## Quest 06_a — Las entradas
################################################################################

################################################################################
## Screen — Menú de razón
################################################################################

screen vq6a_menu_razon():
    modal True

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Entendí lo que quiero":
            style "choice_button"
            action Return("A")

        textbutton "A no repetir errores":
            style "choice_button"
            action Return("B")


################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_06_a:
    jump violet_quest06a_hablar


################################################################################
## HABLAR — Conversación genérica (desde interacción directa o botón Listo)
################################################################################

label violet_quest06a_hablar:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, compré las entradas."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Las entradas?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Para la Japicon. No hace falta que uses ningún cosplay, quiero ir con vos."
    show mc_parado_base b_none

    show violet_parada o_abiertos b_none ot_sonrojada with sprite_normal

    pause 0.5

    show violet_parada b_hablandochica
    violet "Últimamente estás actuando un poco impulsivo..."
    show violet_parada b_none

    show violet_parada b_hablandochica
    violet "¿Por qué lo hacés?"
    show violet_parada b_none

    call screen vq6a_menu_razon

    if _return == "A":
        jump violet_quest06a_opcion_a
    else:
        jump violet_quest06a_opcion_b


################################################################################
## PUERTA — Violet sale al pasillo arriba
################################################################################

label violet_quest06a_puerta:

    $ ocultar_hud()
    window show

    mc "Violet, compré las entradas."

    violet "¿Las entradas?"

    mc "Para la Japicon. Salí un momento."

    violet "Ahí salgo."

    pause 0.5

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada o_abiertos b_none ot_sonrojada with sprite_normal

    pause 0.5

    show violet_parada b_hablandochica
    violet "Últimamente estás actuando un poco impulsivo..."
    show violet_parada b_none

    show violet_parada b_hablandochica
    violet "¿Por qué lo hacés?"
    show violet_parada b_none

    call screen vq6a_menu_razon

    if _return == "A":
        jump violet_quest06a_opcion_a
    else:
        jump violet_quest06a_opcion_b


################################################################################
## OPCIÓN A — "Entendí lo que quiero"
################################################################################

label violet_quest06a_opcion_a:

    show mc_parado_base b_hablando
    mc "Quiero compartir momentos con vos, la Japicon es uno de esos momentos y no lo voy a dejar pasar por un error"
    show mc_parado_base b_abiertachica
    mc "Quiero que lo de los cosplay quede atras"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Está bien..."
    show violet_parada b_hablando
    violet "Voy a ir con vos a la Japicon"
    show violet_parada b_none

    $ cambiar_stat2("violet", 2)
    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCIÓN B — "A no repetir errores"
################################################################################

label violet_quest06a_opcion_b:

    show mc_parado_base b_hablando
    mc "Hoy de nuevo en la casa, compartiendo momentos con vos, entendí que me equivoqué al enojarme cuando me fui y arruine la relación"
    show mc_parado_base b_abiertachica
    mc "No voy a dejar que pase eso otra vez"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Está bien..."
    show violet_parada b_hablando
    violet "Voy a ir con vos a la Japicon"
    show violet_parada b_none

    $ cambiar_stat1("violet", 4)
    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop
