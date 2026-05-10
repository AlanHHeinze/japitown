################################################################################
## Label: Usar Casco de Realidad Virtual
################################################################################
## Se llama cuando el jugador usa el casco VR desde el inventario.
## Cadena de validacion:
##   1. condicion_uso del catalogo ya verifico: habitacion MC + noche
##   2. Si evento 1 completado + invitacion activa → evento1_violet_repetir
##   3. Si evento 1 completado sin invitacion → usar_casco_vr_repetir
##   4. Primera vez → narrativa completa del casco → check Violet → evento1_violet

label usar_casco_vr:

    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion

    # Si el evento 1 ya se completo
    if violet_evento1_completado:
        # Con invitacion activa → directo al evento repetir
        if violet_evento1_repetir:
            $ violet_evento1_repetir = False
            jump evento1_violet_repetir
        # Sin invitacion → narrativa corta de jugar solo
        jump usar_casco_vr_repetir

    # Primera vez: narrativa completa del casco VR
    scene bg_casa_noche_hmc_zoom with fade
    show mc_parado_base c_rbase_base o_base b_seria at center with dissolve
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_vr with sprite_normal
    pause 0.3

    show mc_parado_base b_hablando 
    mc "Al fin lo tengo"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando 
    mc "Voy a probar el X Fighters"
    show mc_parado_base b_none
    
    hide mc_parado_base with dissolve
    show mc_base_parado_vr vr1 at center with dissolve
    piensa "Tendria que ver como configurar esto"
    show mc_base_parado_vr vr2 at center with dissolve
    piensa "Creo que voy entendiendo"
    show mc_base_parado_vr vr3 at center with dissolve
    piensa "Ahi esta"
    show mc_base_parado_vr vr2 at center with dissolve
    pause 0.3
    show mc_base_parado_vr vr1 at center with dissolve
    
    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Un tiempo mas tarde...{/color}"
    scene bg_casa_noche_hmc_zoom with fade

    show violet_evento_01_jugandosolo j1 with dissolve
    piensa "Ya casi lo tengo, un golpe mas y destruyo al terrible Majin Freazing Cell Z"
    show violet_evento_01_jugandosolo j2 with dissolve
    piensa "¡Muereeeeeee!"
    show violet_evento_01_jugandosolo j3 with dissolve
    mc "AHHHHHHHH"
    show violet_evento_01_jugandosolo j4 with dissolve
    pause 0.3
    show violet_evento_01_jugandosolo j5 with dissolve
    pause 0.3
    show violet_evento_01_jugandosolo j6 with dissolve
    pause 0.3
    show violet_evento_01_jugandosolo j7 with dissolve
    pause 0.3
    mc "Estoy bien..."
    mc "Pero ya es suficiente de esto"
    mc "Me duele todo"
    hide violet_evento_01_jugandosolo with dissolve

    # Ocultar MC VR
    hide mc_base_parado_vr with dissolve

    # Post-narrativa primera vez: comprobar si Violet esta en su habitacion
    $ _violet_vr = obtener_npc("violet")
    if _violet_vr and _violet_vr.locacion_actual == "casa_hviolet":
        jump evento1_violet

    # Violet no esta → volver al game loop
    $ mostrar_hud()
    jump game_loop


################################################################################
## Label: Casco VR — Repetir (jugar solo, sin evento)
################################################################################

label usar_casco_vr_repetir:

    scene bg_casa_noche_hmc_zoom with fade

    show mc_base_parado_vr vr1 at center with dissolve
    piensa "Placeholder: Voy a jugar un rato con el casco."

    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Un tiempo mas tarde...{/color}"

    show violet_evento_01_jugandosolo j1 with dissolve
    piensa "Placeholder: Estuvo bien la sesion de hoy."
    hide violet_evento_01_jugandosolo with dissolve

    $ mostrar_hud()
    jump game_loop
