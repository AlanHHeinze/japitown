################################################################################
## Quest 05_b — El paquete llegó
################################################################################

default vq5b_cuerpo = "c_rbase"

################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_05_b:
    jump violet_quest05b_hablar

################################################################################
## HABLAR — versión genérica (desde interacción directa o botón Listo)
################################################################################

label violet_quest05b_hablar:

    $ vq5b_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq5b_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, llegó el paquete"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿El paquete?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "La Coxplay Box, el pack de cosplay que te dije que iba a comprar"
    show mc_parado_base b_none

    # Animación: MC busca en la mochila y entrega el paquete
    if vq5b_cuerpo == "c_pijama":
        show violet_parada o_abiertos c_pijama_base with sprite_normal
    else:
        show violet_parada o_abiertos c_rbase_base with sprite_normal
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_cajacosplay with sprite_normal
    pause 0.3
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    if vq5b_cuerpo == "c_pijama":
        show violet_parada c_pijama_base with sprite_normal
    else:
        show violet_parada c_rbase_cajacosplay with sprite_normal
    mc "Toma."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Gracias, los voy a ver y te digo cual me gusta"
    show violet_parada b_none

    $ inventario["coxplay_box"] = max(0, inventario.get("coxplay_box", 0) - 1)
    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop

################################################################################
## PUERTA — Violet sale al pasillo arriba
################################################################################

label violet_quest05b_puerta:

    $ vq5b_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    mc "Violet, llegó el paquete"

    violet "Ahí salgo"

    pause 0.5

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade

    if vq5b_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "¿El paquete?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "La Coxplay Box, el pack de cosplay que te dije que iba a comprar"
    show mc_parado_base b_none

    # Animación: MC busca en la mochila y entrega el paquete
    if vq5b_cuerpo == "c_pijama":
        show violet_parada o_abiertos c_pijama_base with sprite_normal
    else:
        show violet_parada o_abiertos c_rbase_base with sprite_normal
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_cajacosplay with sprite_normal
    pause 0.3
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    if vq5b_cuerpo == "c_pijama":
        show violet_parada c_pijama_base with sprite_normal
    else:
        show violet_parada c_rbase_cajacosplay with sprite_normal
    mc "Toma."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Gracias, los voy a ver y te digo cual me gusta"
    show violet_parada b_none

    $ inventario["coxplay_box"] = max(0, inventario.get("coxplay_box", 0) - 1)
    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop
