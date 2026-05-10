################################################################################
## Evento 1 de Jasmine: Mostrando Ropa Deportiva
################################################################################
## Narrativa del evento donde Jasmine muestra su nueva ropa deportiva

################################################################################
## Label principal del evento
################################################################################

label event_jasmine_01_mostrando_ropa:
    # Guardar el ID del evento para poder completarlo después
    $ _event_id_temp = "jasmine_event_01"
    
    # Esconder pantallas del juego temporalmente
    hide screen hud_navegacion
    
    # Activar el skin de ropa deportiva automáticamente
    $ activar_skin("jasmine", "jasmine_entrenamiento_deportiva")
    
    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion

    # Mostrar background: Patio/Gym
    scene bg_casa_tarde_gym_zoom with fade

    # Mostrar personajes: MC a la izquierda, Jasmine a la derecha con ropa deportiva
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show jasmine_paradadeportiva c_estirando o_base b_none a_short at right

    #Jasmine habla
    show jasmine_paradadeportiva c_animacion1 b_hablando with sprite_normal
    jasmine "¿Recuerdas la ropa que me regalaste?"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion2 b_hablando with sprite_normal
    jasmine "Mira como me queda."
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando o_felicescerrados with sprite_normal
    mc "Te queda muy bien la verdad"
    show mc_parado_base b_felizcerrada o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva c_animacion3 b_hablando with sprite_normal
    jasmine "Es super elastica"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion4 o_abajonm with sprite_normal
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
    jasmine "Abajo tambien"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion10 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion11 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion12 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion13 o_base with sprite_normal
    "Pafffff"


    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Supongo que eso es bueno"
    show mc_parado_base b_felizcerrada with sprite_normal

    #Jasmine habla

    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Si, te mantiente el cuerpo firme y eso es comodo"
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
    mc "Si..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "¿Te gusta?"
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Si... Estan firmes"
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Hablaba del conjunto idiota jajaja"
    show jasmine_paradadeportiva b_none with sprite_normal

    #MC Habla
    show mc_parado_base b_hablando o_arribanm c_rbase_avergonzado with sprite_normal
    mc "Ehh yo tambien"
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Mira de atras como tambien se ajusta"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3

    
    show jasmine_paradadeportiva e_animacion1 ca_none o_none b_none a_none c_none at right with sprite_normal

    show jasmine_paradadeportiva e_animacion2 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion3 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion4 with sprite_normal
    jasmine "¿Que te parece?"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Tambien te queda muy bien"
    show mc_parado_base b_none with sprite_normal

    
    #Jasmine habla
    show jasmine_paradadeportiva e_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    jasmine "Tambien se ajusta perfecto"
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    jasmine "Muchas gracias de verdad, lo amo"
    hide jasmine_paradadeportiva
    show jasmine_paradadeportiva c_estirando o_base b_hablando a_short at right with sprite_normal
    jasmine "Bueno ahora a entrenar"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Te dejo entrenar tranquila"
    show mc_parado_base b_none with sprite_normal

    # Ocultar personaje
    hide jasmine_paradadeportiva

    
    # Completar el evento
    $ event = obtener_event(_event_id_temp)
    if event:
        $ event.completar()
    
    # Mostrar pantallas del juego
    show screen hud_navegacion
    
    # Volver al loop del juego
    jump game_loop


################################################################################
## Label para repetir la escena (después de completar el evento)
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
    mc "Si, cuando vuela a Capital City puedo comprarte otro similar"
    show mc_parado_base b_felizcerrada o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva c_feliz b_hablando with sprite_normal
    jasmine "Jajajaja digamos que te creo que es por eso"
    show jasmine_paradadeportiva b_feliz with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion1 b_hablando with sprite_normal
    jasmine "Bueno, tiene que ser asi."
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
    jasmine "Abajo tambien"
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
    mc "Si..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "¿Eso querias ver?"
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
    jasmine "Te muestro como debe ser de atras"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3

    
    show jasmine_paradadeportiva e_animacion1 ca_none o_none b_none a_none c_none at right with sprite_normal

    show jasmine_paradadeportiva e_animacion2 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion3 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion4 with sprite_normal
    jasmine "Tambien ajustado"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Si, lo veo"
    show mc_parado_base b_none with sprite_normal

    
    #Jasmine habla
    show jasmine_paradadeportiva e_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    jasmine "Sobre todo aca abajo, que es donde mas se mueve"
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
    mc "Si, perdon por molestarte"
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


################################################################################
## Router para repetir la escena (verifica si ya se vio)
################################################################################

default jasmine_event_01_seen_replay = False

label event_jasmine_01_check_replay:
    if not jasmine_event_01_seen_replay:
        $ jasmine_event_01_seen_replay = True
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
    mc "Si, cuando vuela a Capital City puedo comprarte otro similar"
    show mc_parado_base b_felizcerrada o_base with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva c_feliz b_hablando with sprite_normal
    jasmine "Eso ya me lo dijiste y todavia no me compraste nada jajaja."
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
    jasmine "Abajo tambien"
    show jasmine_paradadeportiva b_none with sprite_normal


    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Es que esta parte no me quedaba clara..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla

    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Si... me imagino no..."
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "Aca tiene que sostener firme"
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
    mc "Si..."
    show mc_parado_base b_none with sprite_normal

    #Jasmine habla
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "¿Tambien te tengo que mostrar otra vez como es la parte de atras no?"
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
    jasmine "Asi tiene que ser de atras"
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
    mc "Ajustado de atras, lo voy a anotar"
    show mc_parado_base b_none with sprite_normal

    
    #Jasmine habla
    show jasmine_paradadeportiva e_animacion5 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    jasmine "Asi"
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion7 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva e_animacion6 with sprite_normal
    pause 0.3
    jasmine "¿Entendiste bien? Aunque supongo que no va a ser la ultima vez que tenga que mostrarte esto"
    hide jasmine_paradadeportiva
    show jasmine_paradadeportiva c_estirando o_base b_hablando a_short at right with sprite_normal
    jasmine "Voy a seguir entrenando, espero que no pienses mucho en esto"

    #MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Perdon por molestarte otra vez"
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
