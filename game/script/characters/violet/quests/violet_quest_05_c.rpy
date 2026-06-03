################################################################################
## Quest 05_c — El malentendido del cosplay
################################################################################

################################################################################
## Screen — Menú de confesión (opción B requiere mc_carisma >= 3)
################################################################################

screen vq5c_menu_confesion():
    modal True

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Espero que en algún momento me creas":
            style "choice_button"
            action Return("A")

        if mc_carisma >= 3:
            textbutton "Confesión":
                style "choice_button"
                action Return("B")
        else:
            textbutton "Confesión   💬 Requisito: 3":
                style "choice_button"
                action Return("B")
                sensitive False


################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_05_c:
    jump violet_quest05c_habitacion


################################################################################
## PEDIRLE PERDÓN fuera de la habitación — Violet no tiene ganas de hablar
################################################################################

label violet_quest05c_perdon_fuera:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, quería hablar con vos sobre lo que pasó..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Ahora no, no tengo ganas de hablar de esto."
    show violet_parada b_none

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## PUERTA — Violet abre desde dentro y el MC entra a la habitación
################################################################################

label violet_quest05c_puerta:

    $ ocultar_hud()
    window show

    mc "Violet..."

    violet "¿Qué pasa?"

    mc "Necesito pasar a hablar."

    violet "Pasá."

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet with fade

    jump violet_quest05c_habitacion


################################################################################
## HABITACIÓN — Conversación de perdón con menú de opciones
################################################################################

label violet_quest05c_habitacion:

    $ ocultar_hud()
    window show

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, quería pedirte perdón por lo de los cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Fue un error, no sabía que era ese tipo de tienda"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No tengo ganas de perdonarte ahora"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Lo entiendo"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Estoy cansada de todo esto"
    show violet_parada b_none

    call screen vq5c_menu_confesion

    if _return == "A":
        jump violet_quest05c_opcion_a
    else:
        jump violet_quest05c_opcion_b


################################################################################
## OPCIÓN A — "Espero que en algún momento me creas"
################################################################################

label violet_quest05c_opcion_a:

    show mc_parado_base b_hablando
    mc "Espero que en algún momento me creas que no tenía malas intenciones y que todo lo hice por vos"
    show mc_parado_base b_none

    pause 1.0

    show mc_parado_base b_hablando
    mc "Nos vemos"
    show mc_parado_base b_none

    $ CATALOGO_ITEMS["entrada_japicon"]["stock"] = 2
    $ cambiar_stat1("violet", 6)
    $ cambiar_stat2("violet", 3)
    $ completar_quest_actual("violet")

    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## OPCIÓN B — Confesión (requiere mc_carisma >= 3)
################################################################################

label violet_quest05c_opcion_b:

    show mc_parado_base b_hablando
    mc "Nunca tuve malas intenciones, todo salió así sin buscarlo"
    show mc_parado_base b_none

    show mc_parado_base b_hablando
    mc "Si bien me encantaría verte con algo así puesto... No lo compre para eso, queria que lo usaras en el evento"
    show mc_parado_base b_none

    show mc_parado_base b_hablando
    mc "No te compraría algo que te exponga y tampoo para que te mire todo el mundo"
    show mc_parado_base b_none

    show mc_parado_base b_hablando
    mc "Me pondría un poco celoso..."
    show mc_parado_base b_none

    show violet_parada o_abiertos b_none ot_sonrojada with sprite_normal

    pause 1.5

    show mc_parado_base b_hablando
    mc "Nos vemos"
    show mc_parado_base b_none

    $ CATALOGO_ITEMS["entrada_japicon"]["stock"] = 2
    $ cambiar_stat1("violet", 10)
    $ cambiar_stat2("violet", 5)
    $ completar_quest_actual("violet")

    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    window hide
    $ mostrar_hud()
    jump game_loop
