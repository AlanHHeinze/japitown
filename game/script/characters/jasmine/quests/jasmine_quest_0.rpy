# =============================================================================
# IMAGENES - Quest 0 Jasmine
# =============================================================================
image jasmine_quest_0_beso = "images/quest/jasmine/quest_0/jasmine_quest_0_beso.png"

# =============================================================================
# QUEST 0 - Rutina y Recuerdos (Jasmine)
# =============================================================================
label quest_jasmine_questprincipal_0:
    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion
    
    # Mostrar background: Patio/Gym
    scene bg_casa_tarde_gym_zoom with dissolve
    
    # Mostrar personajes: MC a la izquierda, Jasmine a la derecha con ropa deportiva
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show jasmine_parada c_rbase_base o_base b_none at right
    
    # === CONVERSACIÓN ===

    # MC habla
    show mc_parado_base b_hablando
    mc "Hola Jasmine... ¿interrumpo?"
    show mc_parado_base b_none

    # Jasmine habla
    show jasmine_parada c_rbase_saludando b_hablando with sprite_normal
    jasmine "No, justo estoy en un descanso."
    show jasmine_parada b_none c_rbase_base with sprite_normal
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "¿Qué necesitas?"
    show jasmine_parada b_none

    # MC habla
    show mc_parado_base c_rbase_avergonzado b_hablando with sprite_normal
    mc "Bueno... Quería darte las gracias por recibirme tan bien."
    show mc_parado_base b_none

    # Jasmine habla
    show jasmine_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    jasmine "¿A qué te referís con recibirte bien?"
    show jasmine_parada b_enojada
    pause 0.3
    show jasmine_parada b_hablando o_arribanm
    jasmine "¿Esperabas que te trate mal o algo?"
    show jasmine_parada b_enojada o_base

    # MC habla
    show mc_parado_base b_hablando o_arribanm c_rbase_brazoscruzados with sprite_normal
    mc "Bueno... Violet me ignoró por completo desde que llegué, me alegra que no seas igual."
    show mc_parado_base b_none o_base

    # Jasmine habla
    show jasmine_parada b_hablando
    jasmine "Yo también estoy enojada contigo, [mc_name]."
    show jasmine_parada b_enojada
    pause 0.3

    show mc_parado_base o_sorprendidos b_seria

    show jasmine_parada b_hablando
    jasmine "Pero a diferencia de mi Violet yo no soy tan inmadura."
    show jasmine_parada b_enojada

    # MC habla
    show mc_parado_base b_hablando c_rbase_avergonzado o_cerrados with sprite_normal
    mc "Con riesgo a que te puedas enojar más, ¿Puedo saber por qué estás enojada?"
    show mc_parado_base b_seria o_base

    # Jasmine habla
    show jasmine_parada b_hablando c_rbase_señalando with sprite_normal
    jasmine "Te fuiste y no volviste nunca más, con el tiempo inclusive te volviste más distante."
    show jasmine_parada b_triste c_rbase_brazoscruzados with sprite_normal
    pause 0.3
    show jasmine_parada b_hablando o_tristesnm
    jasmine "Nuestra relación pasó a ser un saludo de cumpleaños y nada más."
    show jasmine_parada b_triste

    # MC habla
    show mc_parado_base c_rbase_pensando b_hablando o_tristesnm with sprite_normal
    mc "No sé qué decir... Perdón..."
    show mc_parado_base b_seria c_rbase_brazoscruzados o_serios with sprite_normal

    # Jasmine habla
    show jasmine_parada b_hablando
    jasmine "No hace falta que digas nada."
    show jasmine_parada b_triste
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "Pero vuelves de un momento para otro como si nada, va a llevar un tiempo que las cosas vuelvan a ser como antes."
    show jasmine_parada b_triste

    # MC habla
    show mc_parado_base b_hablando c_rbase_avergonzado o_serios with sprite_normal
    mc "Lo entiendo..."
    show mc_parado_base b_seria
    pause 0.3
    show mc_parado_base b_hablando
    mc "Y lo siento, para mi fue muy duro irme de un momento para el otro."
    show mc_parado_base b_seria

    # Jasmine habla
    show jasmine_parada b_hablando o_enojadosnm
    jasmine "¡Y para nosotras también lo fue! Nos quedamos aquí esperando a que al menos preguntaras cómo estábamos."
    show jasmine_parada b_enojada

    menu:
        "Perdón, voy a trabajar para arreglar las cosas":
            jump quest_jasmine_0_opcion_perdon
            
        "Gracias por ser siempre tan madura y comprensiva":
            jump quest_jasmine_0_opcion_madurez
            
        "Yo también perdí mi vida y ustedes tampoco me buscaron":
            jump quest_jasmine_0_opcion_realidad

# -----------------------------------------------------------------------------
# Opción 1: Perdón (+5 adulación con Jasmine)
# -----------------------------------------------------------------------------
label quest_jasmine_0_opcion_perdon:
    
    # MC habla
    show mc_parado_base b_hablando c_rbase_avergonzado o_base with sprite_normal
    mc "Tienes razón. Fui egoísta..."
    show mc_parado_base b_seria
    pause 0.3
    show mc_parado_base b_hablando
    mc "Me concentré en mi dolor y no pensé que para ustedes también fue duro."
    show mc_parado_base b_seria
    
    # Jasmine habla
    show jasmine_parada b_hablando 
    jasmine "Que lo entiendas ya es un buen primer paso."
    show jasmine_parada b_enojada
    pause 0.3
    show jasmine_parada b_hablando o_base
    jasmine "Ahora nos tenemos que esforzar todos para que las cosas vuelvan a ser como antes."
    show jasmine_parada b_enojada
    
    # MC habla
    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Lo haré, voy a esforzarme mucho."
    show mc_parado_base b_seria
    pause 0.3
    show mc_parado_base b_hablando
    mc "Lo prometo."
    show mc_parado_base b_seria

    $ obtener_npc("jasmine").modificar_stat1(5)
    jump quest_jasmine_0_regalo

# -----------------------------------------------------------------------------
# Opción 2: Madurez (+5 provocación con Jasmine)
# -----------------------------------------------------------------------------
label quest_jasmine_0_opcion_madurez:
    show mc_parado_base o_felicescerrados b_felizcerrada
    pause 1.0

    # Jasmine habla
    show jasmine_parada b_hablando o_base
    jasmine "¿Qué pasa que te quedás sin decir nada? ¿Y sonriendo?"
    show jasmine_parada b_enojada
    
    # MC habla
    show mc_parado_base b_hablando o_base
    mc "Sigues siendo igual, siempre la mas madura y directa."
    show mc_parado_base b_felizcerrada
    pause 0.3
    show mc_parado_base b_hablando
    mc "Me había olvidado lo cómodo que me sentía al hablar con vos."
    show mc_parado_base b_none
    
    # Jasmine habla
    show jasmine_parada b_hablando c_rbase_dedolabio with sprite_normal
    jasmine "Idiota... No me intentes comprar ahora..."
    show jasmine_parada b_cachete

    # MC habla
    show mc_parado_base b_hablando
    mc "Es verdad, no lo dije con otra intencion."
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando c_rbase_pensando o_arribanm with sprite_normal
    mc "Aparte no quiero que me perdones."
    show mc_parado_base b_none o_base c_rbase_base with sprite_normal

    # Jasmine habla
    show jasmine_parada b_hablando 
    jasmine "¿No quieres que te perdone?"
    show jasmine_parada b_sexy

    # MC habla
    show mc_parado_base b_hablando c_rbase_brazoscruzados o_felicescerrados with sprite_normal
    mc "No, si me perdonaras ahora sería fácil"
    show mc_parado_base b_felizabierta o_base
    pause 0.3
    show mc_parado_base b_hablando
    mc "Y no es lo que quiero, quiero esforzarme para que me perdones."
    show mc_parado_base b_felizcerrada

    # Jasmine habla
    show jasmine_parada b_hablando o_base
    jasmine "Mmm... Siempre diciendo lo que tenes que decir"
    show jasmine_parada b_sexy
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "Bueno entonces te la voy a poner dificil jajaja."
    show jasmine_parada b_cachete

    # MC habla
    show mc_parado_base b_hablando
    mc "Me alegra que asi sea."
    show mc_parado_base b_none
    
    $ obtener_npc("jasmine").modificar_stat2(5)
    jump quest_jasmine_0_regalo

# -----------------------------------------------------------------------------
# Opción 3: Realidad
# -----------------------------------------------------------------------------
label quest_jasmine_0_opcion_realidad:
    
    # MC habla
    show mc_parado_base b_hablando o_base c_rbase_brazoscruzados with sprite_normal
    mc "Entiendo tu punto y tienes razon"
    show mc_parado_base b_molesta
    pause 0.3
    show mc_parado_base b_hablando
    mc "Pero para mí no fue solo perdelas a ustedes"
    show mc_parado_base b_molesta
    pause 0.3
    show mc_parado_base b_hablando o_molestos
    mc "Yo perdí mi casa, mis amigos, mi escuela, mi ciudad y mi vida."
    show mc_parado_base b_molesta
    
    # Jasmine habla
    show jasmine_parada b_hablando o_sorprendidosnm
    jasmine "..."
    show jasmine_parada b_enojada
    pause 0.3
    show jasmine_parada b_hablando o_tristesnm
    jasmine "Se que fue asi y se que fue mas duro para vos."
    show jasmine_parada b_enojada
    
    # MC habla
    show mc_parado_base b_hablando o_base
    mc "Ustedes estaban juntas, yo estaba solo y nadie me llamó tampoco..."
    show mc_parado_base b_molesta
    pause 0.3
    show mc_parado_base b_hablando 
    mc "En su momento estuve enojado yo también"
    show mc_parado_base b_molesta

    # Jasmine habla
    show jasmine_parada b_hablando o_base
    jasmine "Lo sé, éramos chicos y fuimos idiotas"
    show jasmine_parada b_enojada
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "Todos nos enojamos sin pensar en el otro y cuando lo pude hacer siendo más grande ya era tarde."
    show jasmine_parada b_enojada

    # MC habla
    show mc_parado_base b_hablando o_base
    mc "Como dijiste, eramos chicos y fuimos idiotas."
    show mc_parado_base b_molesta
    pause 0.3
    show mc_parado_base b_hablando
    mc "Ahora somos grandes y solo un poco idiotas jajaja."
    show mc_parado_base b_none

    # Jasmine habla
    show jasmine_parada b_hablando o_base
    jasmine "Jajaja si."
    show jasmine_parada b_none
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "Perdon por haberte dejado solo."
    show jasmine_parada b_none

    # MC habla
    show mc_parado_base b_hablando
    mc "Perdon por haberte dejado sola."
    show mc_parado_base b_none

    jump quest_jasmine_0_regalo

# -----------------------------------------------------------------------------
# Entrega del Regalo
# -----------------------------------------------------------------------------
label quest_jasmine_0_regalo:
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Ahhh, antes de que me olvide, te traje algo."
    show mc_parado_base b_none

    show jasmine_parada b_hablando o_base
    jasmine "¿Eh? ¿Qué cosa?"
    show jasmine_parada b_none

    # Animación mochila/regalo
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_regalojasmine with sprite_normal
    pause 0.3

    # Jasmine recibe el regalo
    show jasmine_parada c_rbase_base b_hablando o_base with sprite_normal
    jasmine "¿Para mí? A ver..."
    show jasmine_parada b_none

    # Pase de regalo
    show mc_parado_base c_rbase_base with sprite_normal
    show jasmine_parada c_rbase_regalo1 with sprite_normal

    #Jasmine habla
    show jasmine_parada b_hablando
    jasmine "Gracias, no me lo esperaba."
    show jasmine_parada b_none

    #animacion abriendo el regalo
    show jasmine_parada c_rbase_regalo2 o_abajonm with sprite_normal
    pause 0.3
    show jasmine_parada c_rbase_regalo3 with sprite_normal
    pause 0.3
    show jasmine_parada c_rbase_regalo4 with sprite_normal
    pause 0.3
    show jasmine_parada c_rbase_regalo5 with sprite_normal
    pause 0.3
    
    #Jasmine habla
    show jasmine_parada b_hablando
    jasmine "ME ENCANTA"
    show jasmine_parada b_none
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "¡Es el conjunto de 'Lion-Fit'! Me encanta, esa marca es muy complicada de conseguir aquí."
    show jasmine_parada b_none
    
    # MC piensa
    show mc_parado_base o_arribanm c_rbase_victoria with sprite_normal
    piensa "¡Sí! Sabía que le gustaría."
    show mc_parado_base o_base c_rbase_base with sprite_normal
    
    #Jasmine habla
    show jasmine_parada b_hablando o_base
    jasmine "¿Quieres que me lo pruebe ahora?"
    show jasmine_parada b_sexy
    
    # MC habla
    show mc_parado_base b_hablando
    mc "Ehhhh..."
    show mc_parado_base b_none
    
    # Jasmine Habla
    show jasmine_parada b_hablando 
    jasmine "Jajaja, no te pongas nervioso."
    show jasmine_parada b_sexy
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "Era broma, no me lo voy a poner ahora, estando toda transpirada."
    show jasmine_parada b_none

    # Jasmine se acerca (Zoom/Evento)
    show jasmine_parada b_hablando
    jasmine "Yo también tengo algo para vos, [mc_name]."
    show jasmine_parada b_none
    pause 0.3
    show jasmine_parada b_hablando
    jasmine "Cierra los ojos."
    show jasmine_parada b_none
    
    pause 0.5
    
    scene black with fade

    jasmine "Jajaja, no te pongas nervioso."
    jasmine "Ven mas para aca..."
    mc "¿Aqui esta bien?"
    jasmine "Espera un momento que lo agarro..."
    jasmine "Listo"
    pause 0.5
    
    scene bg_casa_tarde_gym_zoom with fade
    show jasmine_quest_0_beso with dissolve
    jasmine "Muaaaa"

    hide jasmine_quest_0_beso
    show mc_parado_base at mc_cerca
    show jasmine_parada at npc_cerca
    
    # MC habla
    show mc_parado_base b_hablando c_rbase_asustado o_sorprendidos with sprite_normal
    mc "Yo... eh... mejor te dejo seguir entrenando. Nos vemos luego."
    show mc_parado_base b_none at flip_y_salir_izquierda
    pause 0.5
    hide mc_parado_base

    # Jasmine habla sola
    show jasmine_parada b_hablando
    jasmine "Nos vemos, [mc_name]..."
    show jasmine_parada b_none
    
    # Avanzar horario
    $ avanzar_horario()
    $ completar_quest_actual("jasmine")
    $ activar_estado_especial_npc("jasmine", "jasmine_feliz")

    # Activar skin de ropa deportiva (solo la primera vez)
    $ activar_skin("jasmine", "jasmine_ropa_deportiva")

    jump game_loop
