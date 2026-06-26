################################################################################
## Quest 0_c de Jasmine — Mostrando Ropa Deportiva
################################################################################
## Conversión del evento 01 a quest
## Jasmine muestra su nueva ropa deportiva

label quest_jasmine_questprincipal_0_c:
    # Guardar el ID para referencia
    $ _quest_id_temp = "jasmine_questprincipal_0_c"

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

    # Jasmine habla
    show jasmine_paradadeportiva c_animacion1 b_hablando with sprite_normal
    jasmine "¿Recuerdas la ropa que me regalaste?"
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion2 b_hablando with sprite_normal
    jasmine "Mira como me queda"
    show jasmine_paradadeportiva b_none with sprite_normal

    # MC Habla
    show mc_parado_base b_hablando o_felicescerrados with sprite_normal
    mc "Te queda muy bien la verdad"
    show mc_parado_base b_felizcerrada o_base with sprite_normal

    # Jasmine habla
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
    jasmine "Abajo también"
    show jasmine_paradadeportiva b_none with sprite_normal
    show jasmine_paradadeportiva c_animacion10 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion11 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion12 with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva c_animacion13 o_base with sprite_normal
    "Pafffff"

    # MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Supongo que eso es bueno"
    show mc_parado_base b_felizcerrada with sprite_normal

    # Jasmine habla
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

    # MC Habla
    show mc_parado_base b_hablando with sprite_normal
    mc "Te creo, te creo jaja"
    show mc_parado_base b_felizcerrada with sprite_normal

    # Jasmine habla
    show jasmine_paradadeportiva c_animacion1 b_hablando with sprite_normal
    jasmine "Es que no te lo podía describir con palabras."
    show jasmine_paradadeportiva b_none with sprite_normal
    pause 0.3
    show jasmine_paradadeportiva b_hablando with sprite_normal
    jasmine "¿Me veo bien así?"
    show jasmine_paradadeportiva b_none with sprite_normal

    # MC responde
    show mc_parado_base b_hablando with sprite_normal
    mc "Perfecto. Te ves muy bien."
    show mc_parado_base b_felizcerrada with sprite_normal

    # Mantener activo el skin deportivo: a partir de ahora Jasmine entrena con él
    # (su rutina de entrenamiento usa el grupo "entrenamiento").
    $ activar_skin("jasmine", "jasmine_entrenamiento_deportiva")

    # Completar quest
    $ completar_quest_actual("jasmine")

    window hide
    $ mostrar_hud()
    jump game_loop
