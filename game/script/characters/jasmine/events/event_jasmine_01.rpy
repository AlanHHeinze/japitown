################################################################################
## Evento 1 de Jasmine: "Volver a ver el conjunto"
################################################################################
## La primera parte (Jasmine mostrando la ropa nueva) se convirtio en la quest
## 0_c. Aca queda solo la repeticion: con la quest 0_c completada y Jasmine en
## el gym por la tarde, el menu de interaccion muestra "Volver a ver el conjunto".
## La PRIMERA vez ejecuta event_jasmine_01_repetir; las siguientes,
## event_jasmine_01_repetir_alternativo (lo decide event_jasmine_01_check_replay).
################################################################################


label event_jasmine_01_repetir:
    # Esconder pantallas del juego temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Escena en el gym
    scene bg_casa_tarde_gym_zoom with fade
    
    # Mostrar background: Patio/Gym
    scene bg_casa_tarde_gym_zoom with fade
    
    # Mostrar personajes: MC a la izquierda, Jasmine a la derecha con ropa deportiva
    # Mostrar personajes: MC a la izquierda, Jasmine a la derecha con ropa deportiva
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show jasmine_paradadeportiva c_estirando o_base b_none a_short at right

    #Jasmine habla
    show jasmine_paradadeportiva c_base b_hablando with sprite_normal
    jasmine "¿Lo queres volver a ver?"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Mmmm...."
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando o_felicescerrados with sprite_normal
    mc "Sí, cuando vuela a Capital City puedo comprarte otro similar"
    show mc_parado_base b_felizcerrada o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva c_feliz b_hablando with sprite_normal
    jasmine "Jajajaja digamos que te creo que es por eso"
    show jasmine_paradadeportiva b_feliz with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion1 b_hablando with sprite_normal
    jasmine "Bueno, tiene que ser así."
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion6 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion8 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion9 b_hablando o_base with sprite_normal
    jasmine "Elastico, pero ajustado arriba"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion10 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion11 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion12 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion13 o_base with sprite_normal
    "Pafffff"
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Abajo también"
    show jasmine_paradadeportiva b_none with sprite_normal


    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Entiendo..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla

    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Es importante que te mantenga el cuerpo firme"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Mira"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion14 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion15 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion16 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion17 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion16 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion17 with sprite_normal
    show jasmine_paradadeportiva b_hablando o_base with sprite_normal
    jasmine "Vez lo que te digo"
    show jasmine_paradadeportiva b_none with sprite_normal
    
    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Sí..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "¿Eso querías ver?"
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando o_arribanm c_rbase_avergonzado with sprite_normal
    mc "..."
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Volve a la realidad"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Te muestro como debe ser de atrás"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3

    
    show jasmine_paradadeportiva e_animacion1 ca_none o_none b_none a_none c_none at right with sprite_normal

    show jasmine_paradadeportiva e_animacion2 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion3 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion4 with sprite_normal
    jasmine "También ajustado"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Sí, lo veo"
    show mc_parado_base b_none with sprite_normal

    
    #Jasmine habla
    show jasmine_paradadeportiva e_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    jasmine "Sobre todo aquí abajo, que es donde más se mueve"
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    jasmine "¿Entendiste bien?"
    hide jasmine_paradadeportiva
    show jasmine_paradadeportiva c_estirando o_base b_hablando a_short at right with sprite_normal
    jasmine "Bueno, ya se termino el show, tengo que seguir entrenando"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Sí, perdón por molestarte"
    show mc_parado_base b_none with sprite_normal

    # Ocultar personaje
    hide jasmine_paradadeportiva
    
    # Ocultar personaje
    hide jasmine_paradadeportiva
    with dissolve
    
    # Mostrar pantallas del juego
    show screen hud_navegacion
    
    # Completar el evento formal: lo saca del panel de pistas. El botón "Volver a
    # ver el conjunto" sigue visible (su condición es la quest 0_c completada).
    $ _ev_fin_jas01 = obtener_event("jasmine_event_01")
    if _ev_fin_jas01 and _ev_fin_jas01.estado != ESTADO_EVENT_COMPLETADO:
        $ _ev_fin_jas01.completar()

    # Volver al loop del juego
    jump game_loop


################################################################################
## Router para repetir la escena (verifica si ya se vio)
################################################################################

label event_jasmine_01_check_replay:
    # Primera vez = evento todavía no completado → escena principal de repetición
    # (que lo completa y lo saca del panel). Siguientes = ya completado → alternativa.
    $ _ev_jas01 = obtener_event("jasmine_event_01")
    if _ev_jas01 and _ev_jas01.estado != ESTADO_EVENT_COMPLETADO:
        jump event_jasmine_01_repetir
    else:
        jump event_jasmine_01_repetir_alternativo

################################################################################
## Label alternativo para repetir la escena (segunda vez en adelante)
################################################################################

label event_jasmine_01_repetir_alternativo:
    # Esconder pantallas del juego temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Escena en el gym
    scene bg_casa_tarde_gym_zoom with fade
    
    # Mostrar background: Patio/Gym
    scene bg_casa_tarde_gym_zoom with fade
    
    # Mostrar personajes: MC a la izquierda, Jasmine a la derecha con ropa deportiva
    # Mostrar personajes: MC a la izquierda, Jasmine a la derecha con ropa deportiva
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show jasmine_paradadeportiva c_estirando o_base b_none a_short at right

    #Jasmine habla
    show jasmine_paradadeportiva c_base b_hablando with sprite_normal
    jasmine "¿Otra vez?"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Mmmm...."
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando o_felicescerrados with sprite_normal
    mc "Sí, cuando vuela a Capital City puedo comprarte otro similar"
    show mc_parado_base b_felizcerrada o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva c_feliz b_hablando with sprite_normal
    jasmine "Eso ya me lo dijiste y todavía no me compraste nada jajaja."
    show jasmine_paradadeportiva b_feliz with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion1 b_hablando with sprite_normal
    jasmine "Me parece que tus intenciones son otras, pero esta bien..."
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion6 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion8 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion9 b_hablando o_base with sprite_normal
    jasmine "Elastico, pero ajustado arriba"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion10 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion11 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion12 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion13 o_base with sprite_normal
    "Pafffff"
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Abajo también"
    show jasmine_paradadeportiva b_none with sprite_normal


    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Es que esta parte no me quedaba clara..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla

    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Sí... me imagino no..."
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Aquí tiene que sostener firme"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion14 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion15 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion16 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion17 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion16 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion17 with sprite_normal
    show jasmine_paradadeportiva b_hablando o_base with sprite_normal
    jasmine "¿Esta vez si entendiste?"
    show jasmine_paradadeportiva b_none with sprite_normal
    
    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Sí..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "¿También te tengo que mostrar otra vez como es la parte de atrás no?"
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando o_arribanm c_rbase_avergonzado with sprite_normal
    mc "Supongo que si"
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Mmmm..."
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Así tiene que ser de atrás"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3

    
    show jasmine_paradadeportiva e_animacion1 ca_none o_none b_none a_none c_none at right with sprite_normal

    show jasmine_paradadeportiva e_animacion2 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion3 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion4 with sprite_normal
    jasmine "Bien ajustado"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Ajustado de atrás, lo voy a anotar"
    show mc_parado_base b_none with sprite_normal

    
    #Jasmine habla
    show jasmine_paradadeportiva e_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    jasmine "Así"
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    jasmine "¿Entendiste bien? Aunque supongo que no va a ser la última vez que tenga que mostrarte esto"
    hide jasmine_paradadeportiva
    show jasmine_paradadeportiva c_estirando o_base b_hablando a_short at right with sprite_normal
    jasmine "Voy a seguir entrenando, espero que no pienses mucho en esto"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Perdón por molestarte otra vez"
    show mc_parado_base b_none with sprite_normal

    # Ocultar personaje
    hide jasmine_paradadeportiva
    
    # Ocultar personaje
    hide jasmine_paradadeportiva
    with dissolve
    
    # Mostrar pantallas del juego
    show screen hud_navegacion
    
    # Volver al loop del juego
    jump game_loop
