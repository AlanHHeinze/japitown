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

        # Opción especial: siempre visible; en gris cuando no se cumple el requisito.
        textbutton "Confesión  💬 (3 de carisma)":
            style "choice_button"
            action Return("B")
            sensitive (mc_carisma >= 3)


default vq5c_cuerpo = "c_rbase"
# "A" = esperar que me crea | "B" = confesión
default vq5c_eleccion = None

################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_05_c:
    jump violet_quest05c_habitacion


################################################################################
## PEDIRLE PERDÓN fuera de la habitacion — Violet no tiene ganas de hablar
################################################################################

label violet_quest05c_perdon_fuera:

    $ vq5c_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq5c_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, quería hablar contigo sobre lo que pasó..."
    show mc_parado_base b_none

    if vq5c_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_enojados c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica o_enojados c_rbase_brazoscruzados with sprite_fast
    violet "Ahora no, no tengo ganas de hablar de esto"
    show viole_parada b_hablando
    violet "Chau"
    if vq5c_cuerpo == "c_pijama":
        show violet_parada b_none c_pijama_base with sprite_fast
    else:
        show violet_parada b_none c_rbase_base with sprite_fast

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## PUERTA — Violet abre desde dentro y el MC entra a la habitacion
################################################################################

label violet_quest05c_puerta:

    $ ocultar_hud()
    window show

    mc "Violet..."

    violet "¿Qué pasa?"

    mc "Necesito pasar a hablar"

    violet "Pasa"

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet with fade

    jump violet_quest05c_habitacion


################################################################################
## HABITACIÓN — Conversacion de perdón con menú de opciones
################################################################################

label violet_quest05c_habitacion:

    $ vq5c_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet

    if vq5c_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando c_rbase_perdon with sprite_fast
    mc "Violet, quería pedirte perdón por lo de los cosplay"
    show mc_parado_base b_seria c_rbase_base with sprite_fast

    show violet_parada o_arribanm
    violet "..."
    show violet_parada o_base

    show mc_parado_base b_hablando c_base_avergonzado with sprite_fast
    mc "Fue un error, no sabía que era ese tipo de tienda"
    show mc_parado_base b_seria 

    if vq5c_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_base with sprite_fast
    else:
        show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_fast
    violet "No tengo ganas de perdonarte ahora"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Lo entiendo..."
    show mc_parado_base b_seria

    show violet_parada b_hablandochica o_arribanm
    violet "Estoy cansada de todo esto"
    show violet_parada b_none o_base

    call screen vq5c_menu_confesion

    $ vq5c_eleccion = _return
    if _return == "A":
        jump violet_quest05c_opcion_a
    else:
        jump violet_quest05c_opcion_b


################################################################################
## OPCIÓN A — "Espero que en algun momento me creas"
################################################################################

label violet_quest05c_opcion_a:

    show mc_parado_base b_hablando o_abajonm c_rbase_brazoscruzados with sprite_fast
    mc "Espero que en algún momento me creas que no tenía malas intenciones y que todo lo hice por ti"
    show mc_parado_base b_seria

    pause 1.0

    show mc_parado_base b_hablando
    mc "Solo pensé en acompañarte en eso que siempre quisiste hacer"
    show mc_parado_base b_abiertachica
    mc "Nuevamente perdón"
    show mc_parado_base b_seria c_rbase_base with sprite_fast

    # La tienda lee stock_tienda, no CATALOGO_ITEMS[...]["stock"]: actualizar ambos
    # para que las entradas aparezcan disponibles con stock real.
    $ CATALOGO_ITEMS["entrada_japicon"]["stock"] = 2
    $ stock_tienda["entrada_japicon"] = 2
    $ cambiar_stat1("violet", 6)
    $ completar_quest_actual("violet", recuerdos={"eleccion_05c": vq5c_eleccion})
    $ notificar_recordara("violet")

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

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "Nunca tuve malas intenciones, todo salió así sin buscarlo"
    show mc_parado_base b_abiertachica 
    mc "Si bien me encantaría verte con algo así puesto... No lo compre para eso, quería que lo usaras en el evento"
    show mc_parado_base b_seria

    show mc_parado_base b_hablando o_abajonm
    mc "No te compraría algo que te exponga y tampoo para que te mire todo el mundo"
    show mc_parado_base b_seria o_base

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Me pondría un poco celoso..."
    show mc_parado_base b_seria

    show violet_parada o_abiertos b_none ot_sonrojada with sprite_normal

    pause 1.5

    show mc_parado_base b_hablando
    mc "Espero que me creas, nos vemos"
    show mc_parado_base b_seria c_rbase_base with sprite_fast

    # La tienda lee stock_tienda, no CATALOGO_ITEMS[...]["stock"]: actualizar ambos
    # para que las entradas aparezcan disponibles con stock real.
    $ CATALOGO_ITEMS["entrada_japicon"]["stock"] = 2
    $ stock_tienda["entrada_japicon"] = 2
    $ cambiar_stat1("violet", 6)
    $ cambiar_stat2("violet", 3)
    $ completar_quest_actual("violet", recuerdos={"eleccion_05c": vq5c_eleccion})
    $ notificar_recordara("violet")

    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    window hide
    $ mostrar_hud()
    jump game_loop
