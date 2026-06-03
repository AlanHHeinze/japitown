################################################################################
## Quest 06_b — La prueba del cosplay
################################################################################

default violet_06b_eleccion = None

################################################################################
## Screen — Menú del cierre
################################################################################

screen vq6b_menu_cierre():
    modal True

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Bajar el cierre":
            style "choice_button"
            action Return("A")

        if mc_fuerza >= 3:
            textbutton "Forzar el cierre":
                style "choice_button"
                action Return("C")
        else:
            textbutton "Forzar el cierre   💪 Requisito: 3":
                style "choice_button"
                action Return("C")
                sensitive False


################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_06_b:
    jump violet_quest06b_puerta


################################################################################
## PUERTA — Violet pide que espere, varios minutos después la invita a pasar
################################################################################

label violet_quest06b_puerta:

    $ ocultar_hud()
    window show

    mc "Violet, me pediste que pasara."

    violet "Sí, esperá un momento."

    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Varios minutos más tarde...{/color}"
    pause 1.0

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    violet "Pasá."

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "¿Que te parece?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Wooooow"
    show mc_parado_base b_abiertachica
    mc "Me encanta"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Puedo ir al evento con esto?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí... ¿Por que no podrias?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Ya sabes el por que..."
    show violet_parada b_hablando
    violet "Decime la verdad. No lo hagas solo porque a vos te gusta"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Lo podes usar sin problema"
    show mc_parado_base b_abiertachica
    mc "Es un poco llamativo pero es algo de lo que no te tenés que preocupar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Sabes que nunca me gusto llamar la atencion"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Te pongas un cosplay o no, vas a llamar la atencion igual"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Por que?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Porque sos una chica linda"
    show mc_parado_base b_abiertachica
    mc "Y porque vamos a la Japicon jajajaja"
    show mc_parado_base b_none

    pause 0.5

    show violet_parada b_hablando
    violet "¿Te puedo pedir un favor?"
    show violet_parada b_hablandochica
    violet "¿Me podés bajar un poco el cierre? Se traba y es muy molesto de sacar"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Emmm sí, claro"
    show mc_parado_base b_none
    piensa "Si fuece un juego para adultos, este es el momento en donde la cosa se descontrolaria"
    piensa "Pero no suelo tener esa suerte en la vida"

    show mc_parado_base b_hablando
    mc "Si esta un poco trabado, no te preocupes que lo voy a arreglar"
    show mc_parado_base b_none

    call screen vq6b_menu_cierre

    if _return == "A":
        jump violet_quest06b_cierre_a
    else:
        jump violet_quest06b_cierre_c


################################################################################
## Fin compartido — completa la quest y devuelve al pasillo con tiempo +1
################################################################################

label violet_quest06b_fin:

    $ completar_quest_actual("violet")
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade
    $ avanzar_horario()
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCIÓN A — Bajar el cierre (siempre disponible)
################################################################################

label violet_quest06b_cierre_a:

    show mc_parado_base b_hablando
    mc "Realmente estaba trabado, no lo puedo bajar"
    show mc_parado_base b_abiertachica
    mc "Voy a hacer un poco de fuerza"
    show mc_parado_base b_none

    pause 0.5

    show violet_parada b_hablandochica
    violet "Con cuidado..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Creo que lo trabe mas, no lo puedo ni subir ahora"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Es un problema ese cierre, me costo mucho sacarmelo la otra vez"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Y ahora que hacemos?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Le voy a pedir a Monica que me lo quite"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Seguro que ella lo puede arreglar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Si, le voy a decir ahora, antes que se haga mas tarde"
    show violet_parada b_none

    hide violet_parada with dissolve
    
    piensa "Vaya, eso no salió como esperaba..."

    $ violet_06b_eleccion = "A"
    jump violet_quest06b_fin


################################################################################
## OPCIÓN C — Forzar el cierre (requiere mc_fuerza >= 3)
################################################################################

label violet_quest06b_cierre_c:

    show mc_parado_base b_hablando
    mc "Voy a hacer un poco de fuerza"
    show mc_parado_base b_none

    pause 0.5

    vozoff "¡CRACK! ¡CRACK! ¡CRACK!"
    vozoff "Cjjjjjj"

    mc "Creo que hice demasiada fuerza"

    violet "..."

    mc "..."

    violet "[mc_name] Este es el momento en que sin decir nada te vas..."
    
    hide mc_parado_base with dissolve

    $ violet_06b_eleccion = "C"
    jump violet_quest06b_fin
