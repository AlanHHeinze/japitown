################################################################################
## Evento 1 de Mónica: Masaje
################################################################################
## Narrativa del evento donde Mónica y el MC comparten un momento en el living

################################################################################
## Layered Image del evento
################################################################################

layeredimage monica_evento_01:
    
    group img:
        attribute none default null
        attribute img_base:
            "images/eventos/monica/monica_evento1.png"
        attribute img1:
            "images/eventos/monica/monica_evento1_img1.png"
        attribute img2:
            "images/eventos/monica/monica_evento1_img2.png"
        attribute img3:
            "images/eventos/monica/monica_evento1_img3.png"
        attribute img4:
            "images/eventos/monica/monica_evento1_img4.png"
        attribute img5:
            "images/eventos/monica/monica_evento1_img5.png"
        attribute img6:
            "images/eventos/monica/monica_evento1_img6.png"
        attribute img7:
            "images/eventos/monica/monica_evento1_img7.png"
        attribute img8:
            "images/eventos/monica/monica_evento1_img8.png"
        attribute img9:
            "images/eventos/monica/monica_evento1_img9.png"
        attribute img10:
            "images/eventos/monica/monica_evento1_img10.png"
        attribute img11:
            "images/eventos/monica/monica_evento1_img11.png"
        attribute img12:
            "images/eventos/monica/monica_evento1_img12.png"
    
    group mc:
        attribute mc_none:
            Null()
        attribute mc_abajopervertido:
            "images/eventos/monica/monica_evento1_mc_abajopervertido.png"
        attribute mc_avergonzado:
            "images/eventos/monica/monica_evento1_mc_avergonzado.png"
        attribute mc_compasivo:
            "images/eventos/monica/monica_evento1_mc_compasivo.png"
        attribute mc_concentrado:
            "images/eventos/monica/monica_evento1_mc_concentrado.png"
        attribute mc_haciendofuerza:
            "images/eventos/monica/monica_evento1_mc_haciendofuerza.png"
        attribute mc_mirandoabajo:
            "images/eventos/monica/monica_evento1_mc_mirandoabajo.png"
        attribute mc_mirandofeliz:
            "images/eventos/monica/monica_evento1_mc_mirandofeliz.png"
        attribute mc_pensando:
            "images/eventos/monica/monica_evento1_mc_pensando.png"
        attribute mc_resistiendo:
            "images/eventos/monica/monica_evento1_mc_resistiendo.png"
        attribute mc_sonrojado:
            "images/eventos/monica/monica_evento1_mc_sonrojado.png"
        attribute mc_suspirando:
            "images/eventos/monica/monica_evento1_mc_suspirando.png"
    
    group monica:
        attribute monica_none:
            Null()
        attribute monica_aguantando:
            "images/eventos/monica/monica_evento1_monica_aguantando.png"
        attribute monica_aguantando2:
            "images/eventos/monica/monica_evento1_monica_aguantando2.png"
        attribute monica_avergonzada:
            "images/eventos/monica/monica_evento1_monica_avergonzada.png"
        attribute monica_dolor:
            "images/eventos/monica/monica_evento1_monica_dolor.png"
        attribute monica_feliz:
            "images/eventos/monica/monica_evento1_monica_feliz.png"
        attribute monica_gemido:
            "images/eventos/monica/monica_evento1_monica_gemido.png"
        attribute monica_perdida:
            "images/eventos/monica/monica_evento1_monica_perdida.png"
        attribute monica_relajada:
            "images/eventos/monica/monica_evento1_monica_relajada.png"
        attribute monica_resistiendo:
            "images/eventos/monica/monica_evento1_monica_resistiendo.png"
        attribute monica_resistiendo2:
            "images/eventos/monica/monica_evento1_monica_resistiendo2.png"
        attribute monica_sexy:
            "images/eventos/monica/monica_evento1_monica_sexy.png"
        attribute monica_sonrojada:
            "images/eventos/monica/monica_evento1_monica_sonrojada.png"
        attribute monica_suspiro:
            "images/eventos/monica/monica_evento1_monica_suspiro.png"
    
    group bocamc:
        attribute bmc_none:
            Null()
        attribute bmc_hablando:
            "images/eventos/monica/monica_evento1_bocamc_hablando.png"
    
    group bocamonica:
        attribute bmonica_none:
            Null()
        attribute bmonica_hablando:
            "images/eventos/monica/monica_evento1_bocamonica_hablando.png"
        attribute bmonica_hablandoabajo:
            "images/eventos/monica/monica_evento1_bocamc_hablandoabajo.png"
        attribute bmonica_hablandoabajo2:
            "images/eventos/monica/monica_evento1_bocamc_hablandoabajo2.png"


################################################################################
## Label principal del evento
################################################################################

label event_monica_01_narrativa:
    # Guardar el ID del evento para poder completarlo despues
    $ _event_id_temp = "monica_event_01"
    
    # Esconder pantallas del juego temporalmente
    hide screen hud_navegacion
    $ ocultar_hud()
    
    # Mostrar background: Living por la tarde zoom
    scene bg_casa_tarde_living_zoom with fade
    
    # Mostrar personajes: MC a la izquierda, Monica a la derecha
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show monica_parada c_rbase_base o_base b_none at right

    # === CONVERSACIÓN ===

    # MC habla
    show mc_parado_base b_hablando 
    mc "¿Cómo estas Monica? ¿Sigues con dolor en tus hombros?"
    show mc_parado_base b_none 

    # Monica habla
    show monica_parada b_hablando c_rbase_dolorhombro1 with sprite_normal
    monica "Ya se me está pasando,solo tengo que acostumbrarme a usar la notebook en casa"
    show monica_parada b_none
    pause 0.3
    show monica_parada b_dolor c_rbase_dolorhombro2 with sprite_normal
    pause 0.3
    show monica_parada c_rbase_dolorhombro1 with sprite_normal
    pause 0.3
    show monica_parada o_dolornm c_rbase_dolorhombro2 with sprite_normal

    # MC habla
    show mc_parado_base b_hablando c_rbase_avergonzado o_felicescerrados with sprite_normal
    mc "No parece que se te este quitando"
    show mc_parado_base b_none o_base

    # Monica habla
    show monica_parada b_hablando c_rbase_dolorhombro1 with sprite_normal
    monica "Puede ser que no..."
    show monica_parada b_sonrisacerrada

    # MC habla
    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Te voy a hacer un masaje. Soy bueno en eso"
    show mc_parado_base b_felizcerrada o_base 

    # Monica habla
    show monica_parada o_felicesnm b_hablando 
    monica "No me voy a negar a tal oferta."
    show monica_parada b_none o_base 
    
    pause 0.3

    # Monica habla
    show monica_parada b_hablando
    monica "¿Aquí está bien?"
    show monica_parada b_none 

    # MC habla
    show mc_parado_base b_hablando 
    mc "Sí, está bien."
    show mc_parado_base b_none 

    # Monica se cambia
    show monica_parada c_remera_sacando1 with sprite_normal
    pause 0.3
    show monica_parada c_remera_sacando2 with sprite_normal
    pause 0.3
    show monica_parada c_remera_sacando3 with sprite_normal
    pause 0.3
    show monica_parada c_remera_sacando4 with sprite_normal
    pause 0.3
    show monica_parada c_remera_base with sprite_normal
    pause 0.3
    show monica_parada b_hablando c_remera_base
    monica "Vamos al sillón"
    show monica_parada b_none c_remera_base

    # MC piensa
    piensa "No me había puesto a pensar en el increíble cuerpo que tiene Monica para su edad."

    # MC habla
    show mc_parado_base b_hablando 
    mc "Vamos..."
    show mc_parado_base b_none 

    scene black with fade
    show monica_evento_01 img1
    pause 0.3
    show monica_evento_01 img2 with sprite_normal
    pause 0.3
    show monica_evento_01 img3 with sprite_normal
    show monica_evento_01 bmc_hablando
    mc "¿Estas lista?"
    show monica_evento_01 bmc_none
    show monica_evento_01 bmonica_hablando
    monica "Sí"
    show monica_evento_01 bmonica_none
    show monica_evento_01 img4 with sprite_normal
    pause 0.3
    show monica_evento_01 img5 monica_aguantando with sprite_normal
    pause 0.3
    show monica_evento_01 img4 with sprite_normal
    pause 0.3
    show monica_evento_01 img3 monica_none with sprite_normal 
    show monica_evento_01 bmc_hablando
    mc "¿Está bien así? ¿O más suave?"
    show monica_evento_01 bmc_none
    show monica_evento_01 bmonica_hablando
    monica "Mmm... así está bien"
    show monica_evento_01 bmonica_none
    show monica_evento_01 img6 with sprite_normal
    pause 0.3
    show monica_evento_01 img7 with sprite_normal
    pause 0.3
    show monica_evento_01 img8 with sprite_normal
    pause 0.3
    show monica_evento_01 img7 with sprite_normal
    show monica_evento_01 bmonica_hablandoabajo
    monica "Ahí..."
    show monica_evento_01 bmonica_none
    pause 0.3
    show monica_evento_01 img8 monica_feliz with sprite_normal
    pause 0.3
    show monica_evento_01 img7 with sprite_normal
    show monica_evento_01 bmonica_hablando
    monica "Tenías razón... Eres realmente bueno en esto"
    show monica_evento_01 bmonica_none
    show monica_evento_01 bmc_hablando
    mc "Te dije que lo era"
    show monica_evento_01 bmc_none
    show monica_evento_01 bmonica_hablando
    monica "Voy a tener que pedirte que me lo hagas más seguido"
    show monica_evento_01 bmonica_none
    show monica_evento_01 img4 with sprite_normal
    pause 0.3
    show monica_evento_01 img5 monica_aguantando with sprite_normal
    pause 0.3
    show monica_evento_01 img6 with sprite_normal
    pause 0.3
    show monica_evento_01 img7  with sprite_normal
    pause 0.3
    show monica_evento_01 img8 with sprite_normal
    pause 0.3
    show monica_evento_01 bmonica_hablandoabajo
    monica "Más fuerte..."
    show monica_evento_01 bmonica_none
    show monica_evento_01 img6 with sprite_normal
    pause 0.3
    show monica_evento_01 img5 with sprite_normal
    pause 0.3
    show monica_evento_01 img4 with sprite_normal
    pause 0.3
    show monica_evento_01 img3 with sprite_normal
    show monica_evento_01 bmonica_hablandoabajo
    monica "mmmmm..."
    show monica_evento_01 bmonica_none
    show monica_evento_01 bmc_hablando
    mc "¿Estas bien?"
    show monica_evento_01 bmc_none
    show monica_evento_01 bmonica_hablandoabajo
    monica "Sí..."
    show monica_evento_01 bmonica_none
    show monica_evento_01 monica_sonrojada img4 with sprite_normal
    pause 0.3
    show monica_evento_01 img5 with sprite_normal
    pause 0.3
    show monica_evento_01 img6 with sprite_normal
    pause 0.3
    show monica_evento_01 bmonica_hablandoabajo
    monica "mm mmm..."
    show monica_evento_01 bmonica_none
    show monica_evento_01  img7 with sprite_normal
    pause 0.3
    show monica_evento_01 img8 with sprite_normal
    pause 0.3
    piensa "¿Eso fue un gemido?"
    show monica_evento_01 monica_sexy bmonica_hablandoabajo
    monica "Un poco más abajo..."
    show monica_evento_01 bmonica_none
    show monica_evento_01  img9 with sprite_normal
    pause 0.3
    show monica_evento_01 img10 with sprite_normal
    pause 0.3
    show monica_evento_01 img12 with sprite_normal
    show monica_evento_01 monica_relajada bmonica_hablandoabajo
    monica "Ahí es, más duro..."
    show monica_evento_01 bmonica_none
    show monica_evento_01 img10 with sprite_normal
    pause 0.3
    show monica_evento_01 img12 with sprite_normal
    show monica_evento_01 bmonica_hablandoabajo
    monica "Más..."
    show monica_evento_01 bmonica_none
    show monica_evento_01 img10 with sprite_normal
    pause 0.1
    show monica_evento_01 monica_resistiendo with sprite_normal
    pause 0.1
    show monica_evento_01 img12 with sprite_normal
    show monica_evento_01 bmonica_hablandoabajo
    monica "Ya casi..."
    show monica_evento_01 bmonica_none
    show monica_evento_01 img10 with sprite_normal
    pause 0.1
    show monica_evento_01 monica_resistiendo2 img11 with sprite_normal
    pause 0.1
    show monica_evento_01 img12 with sprite_normal
    show monica_evento_01 bmonica_hablandoabajo2
    monica "mm..."
    show monica_evento_01  bmonica_none
    pause 0.3
    show monica_evento_01 bmonica_hablandoabajo2 with hpunch
    monica "mmmmm..."
    show monica_evento_01  bmonica_none
    pause 0.3
    show monica_evento_01 bmonica_hablandoabajo2 with vpunch
    monica "Ahhh..."
    show monica_evento_01 monica_suspirando bmonica_none with hpunch

    # Corrección narrativa
    "Mónica suelta un suspiro profundo, relajando todo su cuerpo contra el sofá."

    # Pausa de "Cooldown" (Momento post-clímax)
    pause 1.0

    # Transición de salida
    scene black with fade
    hide monica_evento_01
    
    # Restaurar ambiente (Opcional: Si quieres que aparezcan acomodándose)
    scene bg_casa_tarde_living_zoom with dissolve
    show monica_parada c_rbase_base o_felicesnm b_sonrisacerrada at right
    show mc_parado_base c_rbase_base o_base at mc_izquierda

    # MC habla
    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "¿Mejor?"
    show mc_parado_base b_felizcerrada o_base 

    # Monica habla
    show monica_parada o_felicesnm b_hablando 
    monica "Mucho mejor... Gracias."
    show monica_parada b_none o_base 

    # Completar el evento
    $ event = obtener_event(_event_id_temp)
    if event:
        $ event.completar()

    # El masaje consume tiempo: adelantar el horario en 1
    $ avanzar_horario()

    # Mostrar pantallas del juego
    show screen hud_navegacion

    # Volver al loop del juego
    jump game_loop


################################################################################
## Router para repetir la escena (verifica item locion_masajes)
################################################################################

label event_monica_01_check_replay:
    # Verificar si el jugador tiene locion_masajes en el inventario
    $ _tiene_locion = getattr(store, 'inventario', {}).get("locion_masajes", 0) >= 1
    
    if _tiene_locion:
        # Consumir 1 unidad de locion_masajes
        $ store.inventario["locion_masajes"] -= 1
        jump masaje_locion
    else:
        jump masaje_repetir


################################################################################
## Label para masaje CON loción (tiene el item)
################################################################################

label masaje_locion:
    # Esconder pantallas del juego temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Escena en el living
    scene bg_casa_tarde_living_zoom with fade
    
    # Mostrar personajes
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show monica_parada c_rbase_base o_base b_none at right

    # MC habla
    show mc_parado_base b_hablando
    mc "Monica, compré una loción de masajes. ¿Te gustaría probarla?"
    show mc_parado_base b_none

    # Monica habla
    show monica_parada b_hablando o_felicesnm
    monica "¿De verdad? Suena relajante, claro que sí."
    show monica_parada b_none o_base

    # MC habla
    show mc_parado_base b_hablando
    mc "Genial, preparemos todo entonces."
    show mc_parado_base b_none

    # Monica habla
    show monica_parada b_hablando
    monica "Muchas gracias, hacía falta un poco de relax."
    show monica_parada b_none

    # Ocultar personajes
    hide monica_parada
    hide mc_parado_base
    
    # Mostrar pantallas del juego
    show screen hud_navegacion
    
    # Volver al loop del juego
    jump game_loop


################################################################################
## Label para masaje SIN loción (no tiene el item)
################################################################################

label masaje_repetir:
    # Esconder pantallas del juego temporalmente
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Escena en el living
    scene bg_casa_tarde_living_zoom with fade
    
    # Mostrar personajes
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show monica_parada c_rbase_base o_base b_none at right

    # MC habla
    show mc_parado_base b_hablando
    mc "Monica, ¿te gustaría un masaje?"
    show mc_parado_base b_none

    # Monica habla
    show monica_parada b_hablando
    monica "Mmmm... no estaría mal, pero estaría mejor con una loción de masajes."
    show monica_parada b_none

    # MC habla
    show mc_parado_base b_hablando o_arribanm
    mc "Tienes razón, debería conseguir una."
    show mc_parado_base b_none o_base

    # Monica habla
    show monica_parada b_hablando o_felicesnm
    monica "Cuando consigas una, me avisas."
    show monica_parada b_none o_base

    # Ocultar personajes
    hide monica_parada
    hide mc_parado_base
    
    # Mostrar pantallas del juego
    show screen hud_navegacion
    
    # Volver al loop del juego
    jump game_loop
