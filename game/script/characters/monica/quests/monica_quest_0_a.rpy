# =============================================================================
# IMAGENES - Quest 0 Mónica
# =============================================================================
# Background
image bg_quest_monica_0_living_zoom = "images/quest/monica/quest 0/bg_quest_monica_0_living_zoom.png"

# Sprites MC
image monica_quest_0_mc_avergonzado = "images/quest/monica/quest 0/monica_quest_0_mc_avergonzado.png"
image monica_quest_0_mc_brazosarriba = "images/quest/monica/quest 0/monica_quest_0_mc_brazosarriba.png"
image monica_quest_0_mc_brazosarriba_bocahablando = "images/quest/monica/quest 0/monica_quest_0_mc_brazosarriba_bocahablando.png"
image monica_quest_0_mc_oliendo = "images/quest/monica/quest 0/monica_quest_0_mc_oliendo.png"
image monica_quest_0_mc_oliendo_2 = "images/quest/monica/quest 0/monica_quest_0_mc_oliendo_2.png"
image monica_quest_0_mc_oliendo_2_cara = "images/quest/monica/quest 0/monica_quest_0_mc_oliendo_2_cara.png"
image monica_quest_0_mc_oliendo_3 = "images/quest/monica/quest 0/monica_quest_0_mc_oliendo_3.png"
image monica_quest_0_mc_oliendo_3_cara = "images/quest/monica/quest 0/monica_quest_0_mc_oliendo_3_cara.png"
image monica_quest_0_mc_perdon = "images/quest/monica/quest 0/monica_quest_0_mc_perdon.png"

# Sprites Monica - Carcajada
image monica_quest_0_monica_carcajada = "images/quest/monica/quest 0/monica_quest_0_monica_carcajada.png"

# Sprites Monica - Mirando (expresiones faciales)
image monica_quest_0_monica_mirando_aguantandorisa = "images/quest/monica/quest 0/monica_quest_0_monica_mirando_aguantandorisa.png"
image monica_quest_0_monica_mirando_empezando_a_reir = "images/quest/monica/quest 0/monica_quest_0_monica_mirando_empezando a reir.png"
image monica_quest_0_monica_mirando_enojada = "images/quest/monica/quest 0/monica_quest_0_monica_mirando_enojada.png"
image monica_quest_0_monica_mirando_hablando = "images/quest/monica/quest 0/monica_quest_0_monica_mirando_hablando.png"
image monica_quest_0_monica_mirando_riendo = "images/quest/monica/quest 0/monica_quest_0_monica_mirando_riendo.png"

# Sprites Monica - Perfume
image monica_quest_0_monica_perfume = "images/quest/monica/quest 0/monica_quest_0_monica_perfume.png"
image monica_quest_0_monica_perfume_bocahablando = "images/quest/monica/quest 0/monica_quest_0_monica_perfume_bocahablando.png"
image monica_quest_0_monica_perfume_brazocostado = "images/quest/monica/quest 0/monica_quest_0_monica_perfume_brazocostado.png"
image monica_quest_0_monica_perfume_carafeliz = "images/quest/monica/quest 0/monica_quest_0_monica_perfume_carafeliz.png"
image monica_quest_0_monica_perfume_mirando = "images/quest/monica/quest 0/monica_quest_0_monica_perfume_mirando.png"

# Ruta elegida en el menu de dialogo (para evitar exploit de rollback)
default _ruta_mq0 = ""

# =============================================================================
# INICIO DE LA QUEST 0 — botón "Agradecerle" del menú de Mónica
# =============================================================================
# Lo invoca la opción "Agradecerle (quest)" del menú de interacción de Mónica
# cuando la quest 0 está lista y el MC está a solas con ella.
label monica_q0_agradecer:
    # El MC le entrega el perfume a Mónica durante la quest: consumirlo del inventario.
    $ inventario["perfume"] = max(0, inventario.get("perfume", 0) - 1)
    $ _q_mon0 = sistema_quests.obtener_quest("monica_questprincipal_0")
    if _q_mon0:
        $ _q_mon0.etapa_actual = ETAPA_DESARROLLO
    jump quest_monica_questprincipal_0


# =============================================================================
# QUEST 0 - Bienvenido a casa (Mónica)
# =============================================================================
label quest_monica_questprincipal_0:
    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Mostrar background
    scene bg_casa_tarde_living_zoom with dissolve
    
    # Mostrar personajes: MC a la izquierda (usando transform con flip), Monica a la derecha
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda
    show monica_parada c_rbase_base o_base b_seria at right
    
    # === CONVERSACIÓN ===

    # MC habla
    show mc_parado_base b_hablando
    mc "Mónica, ¿tienes un momento?"
    show mc_parado_base b_none

    # Monica habla
    show monica_parada b_hablando
    monica "Claro, dime."
    show monica_parada b_none

    # MC habla
    show mc_parado_base c_rbase_avergonzado b_hablando with sprite_normal
    mc "Bueno... es que... quería darte las gracias por dejarme estar aquí."
    show mc_parado_base b_asustada

    # Monica habla
    show monica_parada o_felicesnm b_hablando
    monica "No tienes nada que agradecer, tonto. Sabes que esta siempre ha sido y será tu casa."
    show monica_parada b_none o_base

    # MC habla
    show mc_parado_base b_hablando
    mc "Pero me volviste a recibir y eso es muy importante para mi."
    show mc_parado_base b_none

    # Monica habla
    show monica_parada c_rbase_brazoscruzados b_hablando with sprite_normal
    monica "De nuevo, no tienes nada que agradecer, me hace muy feliz tenerte de vuelta."
    show monica_parada b_none

    show mc_parado_base c_rbase_base b_felizcerrada with sprite_normal
    
    #Monica Piensa
    show monica_parada o_arribanm
    monica_pensando "Violet y Jasmine deben estar mas que felices en este momento..."
    show monica_parada o_base

    # Monica habla
    show monica_parada b_hablando o_felicesnm
    monica "Todas lo estamos, no lo dudes."
    show monica_parada b_none o_base
    
    show mc_parado_base o_cerrados
    pause 0.2
    
    # MC habla
    show mc_parado_base b_hablando o_base
    mc "Eso espero. A Jasmine se la notaba feliz de verme."
    show mc_parado_base b_none

    # MC habla
    show mc_parado_base c_rbase_pensando b_hablando o_arribanm with sprite_normal
    mc "Pero a Violet no tanto."
    show mc_parado_base b_none o_base c_rbase_base with sprite_normal

    #Monica Piensa
    show monica_parada o_arribanm
    monica_pensando "Creo saber el motivo..."
    show monica_parada o_base

    # Monica habla
    show monica_parada b_hablando o_felicesnm
    monica "No te preocupes por eso, es un cambio grande para todas y cada una lo procesa a su manera."
    show monica_parada b_none o_base
    
    show mc_parado_base o_cerrados
    pause 0.2
    show mc_parado_base o_base

    # Monica habla
    show monica_parada b_hablando
    monica "Pero se que es para bien... tengo fe que las cosas volveran a ser como antes."
    show monica_parada b_none

    # MC habla
    show mc_parado_base b_hablando
    mc "Yo deseo lo mismo."
    show mc_parado_base b_none
    
    # Monica habla
    show monica_parada b_hablando
    monica "¿Y por tu parte? ¿Cómo te sientes de estar de vuelta?"
    show monica_parada b_seria

    # MC Habla
    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Bueno... quiero aprovechar el momento, es un nuevo comienzo para mi."
    show mc_parado_base b_none

    # Monica Habla
    show monica_parada b_hablando
    monica "¿Y como quieres que sea ese nuevo comienzo?"
    show monica_parada b_none

    jump tutorial_elecciones_monica

label tutorial_elecciones_monica:

    # Tutorial de elecciones compartido con la quest 0_b de Violet y la 0_a de Jasmine.
    # Como no se sabe qué quest hará primero el jugador, solo se muestra una vez.
    if not tutorial_elecciones_visto:
        tutorial "A lo largo del desarrollo de la historia de un personaje nos iremos encontrando varias veces con distintas opciones para elegir. Estas representan la manera en la que nuestro personaje va a actuar ante la situacion"
        tutorial "Estas elecciones afectan el desarrollo inmediato como tambien a largo plazo. Los personajes recordaran las elecciones elegidas y actuaran en relacion a ello en ciertos momentos"
        tutorial "Aparte de los cambios narrativos algunas elecciones podrian darnos recompensas especiales, como estadisticas, objetos, escenas, etc"
        $ tutorial_elecciones_visto = True

    jump elecciones_monica_continuar

label elecciones_monica_continuar:

    menu:
        "Quiero volver a conectarme con todas":
            jump quest_monica_0_opcion_familia

        "Ahora que soy mayor, quiero ser más cercano a ti":
            jump quest_monica_0_opcion_cercania

        "Es una oportunidad para empezar de cero y hacer mi propia vida":
            jump quest_monica_0_opcion_independencia


# -----------------------------------------------------------------------------
# Opción 1: Familia (+5 amor con Monica)
# -----------------------------------------------------------------------------
label quest_monica_0_opcion_familia:
    # MC habla
    show mc_parado_base b_hablando
    mc "Desde el día que me fui casi que perdí el contacto con todas."
    show mc_parado_base b_none
    pause 0.2
    show mc_parado_base b_hablando
    mc "Quiero revertir eso y volver a tener la relación que teníamos antes."
    show mc_parado_base b_none
    
    # Monica habla
    show monica_parada b_hablando c_rbase_base with sprite_normal
    monica "Eso es muy tierno de tu parte. Me alegra mucho escuchar eso, haré lo posible por ayudarte."
    show monica_parada b_none
    pause 0.2
    show monica_parada b_hablando
    monica "Y se que todas pensamos lo mismo."
    show monica_parada b_none

    # MC habla
    show mc_parado_base b_hablando
    mc "Muchas gracias de verdad Monica."
    show mc_parado_base b_none
    pause 0.2
    show mc_parado_base b_hablando
    mc "Gracias por apoyarme antes ahora y siempre."
    show mc_parado_base b_none

    # Monica habla
    show monica_parada b_hablando
    monica "Sabes que siempre voy a estar para vos."
    show monica_parada b_none
    
    $ _ruta_mq0 = "familia"

    jump quest_monica_0_cierre


# -----------------------------------------------------------------------------
# Opción 2: Cercanía (+5 deseo con Monica)
# -----------------------------------------------------------------------------
label quest_monica_0_opcion_cercania:
    
    # Monica habla
    show monica_parada b_hablando c_rbase_dedolabio o_sexysnm with sprite_normal
    monica "¿A que te refieres con eso?"
    show monica_parada b_none
    
    # MC habla
    show mc_parado_base b_hablando
    mc "La última vez que nos vimos yo era un niño y te veia muy distante."
    show mc_parado_base b_none
    pause 0.2
    show mc_parado_base b_hablando
    mc "Pero creo que ahora es distinto."
    show mc_parado_base b_none
    
    # Monica habla
    show monica_parada b_hablando
    monica "Vaya..."
    show monica_parada b_none
    pause 0.2
    show monica_parada b_hablando
    monica "No sabia que pensabas asi..."
    show monica_parada b_none
    
    # MC habla
    show mc_parado_base b_hablando
    mc "Siempre te admiré mucho y ahora que estoy acá quiero aprovechar para pasar mas tiempo contigo"
    show mc_parado_base b_none
    
    show monica_parada c_rbase_avergonzada with sprite_normal
    pause 0.2

    show mc_parado_base b_hablando
    mc "Y conocernos mejor"
    show mc_parado_base b_none
    
    # Monica habla
    show monica_parada b_hablando
    monica "No sabia que pensabas asi..."
    show monica_parada b_none
    pause 0.2
    show monica_parada b_hablando c_rbase_base with sprite_normal
    monica "Voy a dar todo de mi para que podamos tener esa relacion que esperas."
    show monica_parada b_none
    
    $ _ruta_mq0 = "cercania"

    jump quest_monica_0_cierre


# -----------------------------------------------------------------------------
# Opción 3: Independencia
# -----------------------------------------------------------------------------
label quest_monica_0_opcion_independencia:
    # MC habla
    show mc_parado_base b_hablando
    mc "Vuelvo con nostalgia, pero también con ganas de hacer las cosas por mi mismo."
    show mc_parado_base b_none
    pause 0.2
    show mc_parado_base b_hablando
    mc "Quiero aprovechar el momento para empezar de cero y hacer mi propia vida."
    show mc_parado_base b_none
    
    # Monica habla
    show monica_parada b_hablando
    monica "Es un paso importante"
    show monica_parada b_none
    
    # MC habla
    show mc_parado_base b_hablando
    mc "Ya no quiero seguir dependiendo de nadie"
    show mc_parado_base b_none
    pause 0.2
    show mc_parado_base b_hablando
    mc "Quiero hacer las cosas a mi manera, tener el control de mi vida"
    show mc_parado_base b_none
    
    # Monica habla
    show monica_parada b_hablando
    monica "Me gusta..."
    show monica_parada b_none
    pause 0.2
    show monica_parada b_hablando
    monica "Cuentas con mi apoyo para convertirte en un hombre"
    show monica_parada b_none

    $ _ruta_mq0 = "independencia"
    jump quest_monica_0_cierre


# -----------------------------------------------------------------------------
# Cierre común para todas las opciones
# -----------------------------------------------------------------------------
label quest_monica_0_cierre:
    
    # MC habla
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Gracias Monica, de verdad"
    show mc_parado_base b_none
    pause 0.2
    show mc_parado_base b_hablando
    mc "Ahora que recuerdo, te traje algo. Espero que te guste."
    show mc_parado_base b_none o_base

    # Monica habla
    show monica_parada c_rbase_dedolabio b_hablando with sprite_normal
    monica "¿Un regalo? Vaya, sí que eres un caballero. Déjame ver..."
    show monica_parada b_none

    show mc_parado_base c_rbase_mochila1 o_abajonm with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_perfume o_base with sprite_normal

    # MC habla
    show mc_parado_base b_hablando
    mc "Aqui esta"
    show mc_parado_base b_none

    # MC piensa
    show mc_parado_base o_arribanm
    piensa "Espero que le guste"
    show mc_parado_base b_none c_rbase_base o_base with sprite_normal

    # Monica agarra el perfume
    show monica_parada c_rbase_perfume with sprite_normal
    pause 0.3

    # Monica habla
    show monica_parada b_hablando
    monica "Oh, vaya... Un perfume... Sabes que los amo."
    show monica_parada o_felicesnm b_feliz

    show mc_parado_base c_rbase_victoria o_abajonm with sprite_normal
    piensa "Exitoooo"
    show mc_parado_base c_rbase_base o_base with sprite_normal

    # MC habla
    show mc_parado_base b_hablando 
    mc "Cuando lo probé en la tienda, algo en el aroma me recordó a ti."
    show mc_parado_base b_aburrida

    show monica_parada o_sexysnm b_sexy
    pause 0.5

    # Monica habla
    show monica_parada b_hablando
    monica "Sigues diciendo lo que piensas sin pensarlo [mc_name] jajaja."
    show monica_parada b_none

    # Monica habla
    show monica_parada b_hablando
    monica "Te vas a meter en problemas divertidos si sigues siendo tan directo."
    show monica_parada b_none o_base

    # MC habla
    show mc_parado_base o_arribanm
    piensa "¿Qué me querrá decir con eso?"
    show mc_parado_base b_none

    # Monica habla
    show monica_parada b_hablando
    monica "Lo voy a probar."
    show monica_parada b_none

    # Monica prueba el perfume
    hide monica_parada
    show monica_perfume b_none c_costado at right
    pause 0.5
    show monica_perfume c_hechando with sprite_normal
    pause 0.5
    show monica_perfume c_costado with sprite_normal
    pause 0.5
    show monica_perfume b_hablando
    monica "¡Oh! Me encanta... es elegante y tiene mucha personalidad. Es exactamente mi estilo, ¿cómo lo supiste?"
    show monica_perfume b_none
    hide monica_perfume
    show monica_parada c_rbase_perfume o_base at right
    pause 0.5

    # Monica habla
    show monica_parada b_hablando 
    monica "Vamos [mc_name], ven a olerlo"
    show monica_parada b_none at derecha_a_centro
    pause 0.5

    scene bg_quest_monica_0_living_zoom with fade
    show monica_quest_0_monica_perfume with dissolve
    show monica_quest_0_mc_oliendo with dissolve

    show monica_quest_0_monica_perfume_bocahablando
    monica "No seas tímido, acércate más"
    hide monica_quest_0_monica_perfume_bocahablando

    pause 0.3
    hide monica_quest_0_mc_oliendo
    hide monica_quest_0_monica_perfume
    show monica_quest_0_mc_oliendo_2 
    show monica_quest_0_monica_perfume 
    show monica_quest_0_mc_oliendo_2_cara 
    pause 0.3
    "Sniff sniff..."
    pause 0.3

    show monica_quest_0_monica_perfume_bocahablando
    monica "¿Huele rico verdad?"
    hide monica_quest_0_monica_perfume_bocahablando

    pause 0.3
    hide monica_quest_0_mc_oliendo_2
    hide monica_quest_0_monica_perfume
    hide monica_quest_0_mc_oliendo_2_cara
    
    show monica_quest_0_mc_oliendo_3
    show monica_quest_0_monica_perfume_brazocostado
    show monica_quest_0_mc_oliendo_3_cara
    pause 0.3
    "Sniff sniff..."
    pause 0.3
    
    show monica_quest_0_monica_perfume_bocahablando
    monica "Veo que te gustó... y mucho"
    hide monica_quest_0_monica_perfume_bocahablando
    pause 0.3

    "Sniff sniff..."
    pause 0.3
    show monica_quest_0_monica_perfume_bocahablando
    monica "¿No te parece que así está bien?"
    hide monica_quest_0_monica_perfume_bocahablando
    pause 0.3

    hide monica_quest_0_mc_oliendo_3
    hide monica_quest_0_mc_oliendo_3_cara
    show monica_quest_0_mc_avergonzado
    pause 0.3

    piensa "Me dejé llevar y creo que monica se enojó"

    show monica_quest_0_monica_perfume_bocahablando
    monica "No pas..."
    hide monica_quest_0_monica_perfume_bocahablando
    
    hide monica_quest_0_mc_avergonzado
    show monica_quest_0_mc_brazosarriba 
    show monica_quest_0_mc_brazosarriba_bocahablando
    mc "Perdon, me deje llevar"
    hide monica_quest_0_mc_brazosarriba_bocahablando
    pause 0.3

    show monica_quest_0_monica_perfume_bocahablando
    monica "Mmmm..."

    hide monica_quest_0_monica_perfume_bocahablando
    hide monica_quest_0_monica_perfume_brazocostado
    show monica_quest_0_monica_perfume_mirando
    pause 0.5
    monica_pensando "Tan inocente es... No estaría mal aprovecharme"
    
    show monica_quest_0_monica_mirando_enojada
    show monica_quest_0_monica_mirando_hablando
    monica "Creo que te pasaste un poco, ¿Hasta donde querias llegar?"
    hide monica_quest_0_monica_mirando_hablando
    

    show monica_quest_0_mc_brazosarriba_bocahablando
    mc "No es lo que parece"
    hide monica_quest_0_mc_brazosarriba_bocahablando
    
    show monica_quest_0_monica_mirando_hablando
    monica "¿Acaso querias besarme el cuello?"
    hide monica_quest_0_monica_mirando_hablando

    show monica_quest_0_mc_brazosarriba_bocahablando
    mc "Perdon Monica no era mi intencion de verdad"
    hide monica_quest_0_mc_brazosarriba_bocahablando
    hide monica_quest_0_mc_brazosarriba
    show monica_quest_0_mc_perdon

    hide monica_quest_0_monica_mirando_enojada
    show monica_quest_0_monica_mirando_aguantandorisa
    monica "Pffff..."
    hide monica_quest_0_monica_mirando_aguantandorisa
    show monica_quest_0_monica_mirando_empezando_a_reir
    monica "Jajaja"
    hide monica_quest_0_monica_mirando_empezando_a_reir
    show monica_quest_0_mc_perdon at flip_y_salir_izquierda
    hide monica_quest_0_mc_perdon

    show monica_quest_0_monica_mirando_riendo
    monica "Jajajaja"
    hide monica_quest_0_monica_mirando_riendo
    hide monica_quest_0_monica_perfume_mirando
    pause 0.3 
    monica_pensando "Jajaja... Se veia tan tierno estando nervioso"
    monica_pensando "Hace mucho no me reía así"
    hide monica_quest_0_monica_carcajada with fade
    
    # Evaluar ruta elegida y aplicar stats
    if _ruta_mq0 == "familia":
        $ obtener_npc("monica").modificar_stat1(4)
    elif _ruta_mq0 == "cercania":
        $ obtener_npc("monica").modificar_stat2(2)
    elif _ruta_mq0 == "independencia":
        $ obtener_npc("monica").modificar_stat1(2)
        $ obtener_npc("monica").modificar_stat2(1)

    # Avanzar horario
    $ avanzar_horario()

    # Guardar día de completación para el evento 1
    $ store.monica_quest_0_dia_completada = getattr(store, 'dias_totales', 1)

    # Completar quest
    $ completar_quest_actual("monica")
    $ activar_estado_especial_npc("monica", "monica_feliz")

    jump game_loop
