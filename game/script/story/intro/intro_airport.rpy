
label intro_conversacion_padre:

    scene bg_intro_aeropuerto_zoom
    show mc_parado_base ddimensiones ca_cabeza o_base b_aburrida xnone c_rbase_base at mc_izquierda

    show padre_intro ddimensiones cbase omirando bnone pbase at right
    pause 0.5
    show padre_intro bhablando
    padre "Pensé que no ibas a venir"
    show padre_intro bnone
    
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Una parte de mí no quería venir, pero acá estoy."
    show mc_parado_base b_seria
    
    show padre_intro bhablando
    padre "Jajaja vamos, no seas así, vas a extrañar a tu padre."
    show padre_intro bnone
    
    show mc_parado_base o_serios b_hablando
    mc "Sí sí, te voy a extrañar un montón."
    show mc_parado_base b_seria
    
    show padre_intro bhablando 
    padre "Jajaja lo sabía."
    show padre_intro bnone
    
    show mc_parado_base b_hablando
    mc "Te conformas con poco..."
    show mc_parado_base b_seria
    
    show padre_intro bhablando 
    padre "Así somos los padres, jajaja."
    show padre_intro bnone
    
    terminal_micros "Los pasajeros del vuelo 91218 con destino a Argentonia por favor acercarse a la puerta número 4."
    
    show padre_intro bhablando pbrazoscruzados
    padre "Bueno, ese es mi vuelo. ¿Estás seguro que no quieres venir?"
    show padre_intro bnone
    
    show mc_parado_base b_hablando
    mc "Te seguí siempre... pero ir a Argentonia, es una locura."
    show mc_parado_base b_seria
    
    show padre_intro bhablando
    padre "Es un país lleno de gente alegre y mujeres hermosas."
    show padre_intro bnone

    piensa "Se nota que este hombre jamás vio una noticia internacional..."
    
    show mc_parado_base b_hablando
    mc "Gracias, pero realmente prefiero ir a Japitown que a Argentonia."
    show mc_parado_base b_seria

    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Igual deseo que Eva y tú sean muy felices allí."
    show mc_parado_base o_base
    
    show padre_intro bhablando pbase
    padre "Bueno, ya terminé de arreglar todo con Mónica para que te reciba en su casa, no vayas a causarles muchos problemas."
    show padre_intro bnone
    
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Causar problemas es lo tuyo, no lo mío."
    show mc_parado_base b_seria
    
    vozoff "Brrrr Brrrr"
    
    show mc_parado_base o_abajonm c_rbase_celular with sprite_normal
    piensa "El micro sale en 20 minutos."
    show mc_parado_base o_base b_hablando 
    mc "Bueno, yo también debería irme o voy a perder mi viaje."
    show mc_parado_base b_seria
    
    show padre_intro bhablando 
    padre "Espero verte en Argentonia en el verano."
    show padre_intro bnone
    
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Supongo que podría ir en plan turístico..."
    show mc_parado_base c_rbase_base with sprite_normal
    mc "Avísame cuando llegues y mándale saludos a Eva de mi parte."
    
    show padre_intro bhablando 
    padre "Tú también avísame cuando llegues a Japitown."
    show padre_intro bnone

    show mc_parado_base b_hablando
    mc "Nos vemos, papá."  
    show mc_parado_base b_seria

    show mc_parado_base at mc_salir_izquierda
    pause 1.0

    show padre_intro bhablando 
    padre "Adiós..."
    show padre_intro bnone
    
    pause 1.0

    hide padre_intro with dissolve
    hide mc_parado_base with dissolve

    jump intro_llegada_casa


################################################################################
## LLEGADA A LA CASA
################################################################################

label intro_llegada_casa:

    scene black with fade

    show text Text(renpy.translate_string("Más tarde..."), size=50, color="#FFFFFF",
        outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause 2.0
    hide text with dissolve

    # Frente de la casa — horario mañana (inicio del juego)
    scene expression "images/bg/casa/bg_casa_mañana_frente.png" with fade

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    piensa "Qué nostalgia estar aquí de nuevo, pasaron muchos años..."
    piensa "Aquí viví una parte importante de mi infancia. Mi papá conoció a Mónica en uno de sus viajes de trabajo,"
    piensa "y a los pocos meses nos estábamos mudando de la capital a esta casa."
    piensa "En ese momento Japitown era solo una pequeña ciudad, pasar de la metrópoli a aquí fue horrible."
    piensa "Pero me adapté rápido. Mónica me ayudó mucho y sus hijas fueron de gran compañía."
    piensa "Cada vez que lo pienso, fueron los mejores años de mi vida."
    piensa "Momento de dar el paso y entrar."

    scene expression "images/bg/casa/bg_casa_mañana_living.png" with fade

    # Posicionar a las tres a la derecha, ligeramente montadas
    # Orden de show = orden de profundidad (último = al frente)
    show violet_parada c_rbase_base o_base b_none:
        xpos 0.58
        xanchor 0.5
        yanchor 1.0
        ypos 1.0
    show jasmine_parada c_rbase_base o_base b_none:
        xpos 0.70
        xanchor 0.5
        yanchor 1.0
        ypos 1.0
    show monica_parada c_rbase_base o_base b_none:
        xpos 0.82
        xanchor 0.5
        yanchor 1.0
        ypos 1.0

    show mc_parado_base c_rbase_base o_base at mc_izquierda with dissolve  

    # Monica da la bienvenida
    show monica_parada b_hablando
    monica "Bienvenido [mc_name], ¿Cómo estuvo el viaje?"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "Bien pero agotador, fueron muchas horas arriba del micro"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Me alegra mucho que estés de nuevo en casa."
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "Yo también me siento muy feliz de estar de vuelta."
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Bueno, tu habitación está casi lista, solo falta que desempaques lo que enviaste en las cajas."
    show monica_parada b_hablandochica
    monica "No queríamos tocar tus cosas."
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "No te preocupes por eso, hicieron mucho por mí. No sé dónde estaría en este momento si no me hubieras dado un lugar aquí."
    show mc_parado_base b_none
    
    show monica_parada b_hablando
    monica "No tienes que agradecerme por nada, esta fue y será siempre tu casa."
    show monica_parada b_none
    
    show mc_parado_base b_hablando
    mc "De verdad me alegra mucho volver a verlas a todas. Estuve todo el viaje preocupado por este momento,"
    show mc_parado_base b_abiertachica
    mc "pero sigue siendo como lo fue siempre."
    show mc_parado_base b_none

    # Jasmine habla
    show jasmine_parada b_hablando
    jasmine "¿Cómo pensaste que iba a ser?"
    show jasmine_parada b_sorprendida
    jasmine "Esta fue y será siempre tu casa."
    show jasmine_parada b_none

    show mc_parado_base b_hablando
    mc "De nuevo, muchas gracias por recibirme después de tanto tiempo."
    show mc_parado_base b_none

    # Violet solo saluda
    show violet_parada b_hablandochica
    violet "Bueno, esto fue mucho del reencuentro feliz para mí..."
    show violet_parada b_none

    hide violet_parada with dissolve

    show mc_parado_base b_hablando
    mc "¿Qué le pasa a Violet?"
    show mc_parado_base b_none

    # Jasmine habla
    show jasmine_parada b_hablando
    jasmine "Ella es así, le toma más tiempo procesar los cambios."
    show jasmine_parada b_sorprendida
    jasmine "No te preocupes."
    show jasmine_parada b_none

    # Monica propone entrar
    show monica_parada b_hablando
    monica "Voy a hablar con ella luego."
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "No te preocupes Mónica, después yo hablo con ella."
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Bueno dejemos que [mc_name] se acomode tranquilo."
    show monica_parada b_none

    hide monica_parada with dissolve
    hide jasmine_parada with dissolve

    piensa "Bueno, a terminar de acomodar mis cosas y a dormir."
    
    hide mc_parado_base with dissolve

    # Habitación del MC — noche, termino de acomodar
    scene expression "images/bg/casa/bg_casa_noche_hmc.png" with fade

    show mc_parado_base c_rbase_base o_abajonm b_none at center

    pause 0.5

    show mc_parado_base b_hablando
    mc "Por fin terminé de acomodar todas mis cosas."
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Estoy cansado... es hora de dormirme."
    show mc_parado_base b_none

    hide mc_parado_base with dissolve

    jump menu_tutorial
