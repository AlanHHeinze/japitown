################################################################################
## Violet Quest 04_A — El cosplay de Violet
################################################################################
## Label narrativo principal y ramificaciones
## Corresponde a: quest_violet_04_a (id: violet_questprincipal_04_a)
## Se ramifica según violet_quest2_trajesexy (decisión de quest 2)


################################################################################
## LABEL PRINCIPAL — Quest 04_A de Violet
################################################################################

label quest_violet_questprincipal_04_a:

    # Ocultar HUD durante la quest
    $ ocultar_hud()
    window show

    # Restaurar fondo de la locación actual
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    
    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Violet una pregunta"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_brazoscruzados o_enojados with sprite_fast
    violet "Si te interesa saber si te perdone, no lo hice"
    show violet_parada b_hablandochica 
    violet "Y tampoco quiero que me devuelvas lo que me robaste"
    show violet_parada b_none 

    show mc_parado_base b_hablando
    mc "Perdon por eso, fue todo una gran confusion"
    show mc_parado_base b_abiertachica
    mc "Pero queria hablarte de otra cosa"
    show mc_parado_base b_seria

    show violet_parada b_hablandochica o_arribanm
    violet "¿Que queres?"
    show violet_parada b_none o_enojados

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "Queria saber si te habias probado el regalo que te traje"
    show mc_parado_base b_seria

    show violet_parada b_hablandochica o_base c_rbase_base with sprite_fast
    violet "¿A que viene eso ahora?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "El otro dia vi la caja en tu ropero y me acorde de el"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_enojados
    violet "Entonces, si estabas revisando mis cosas..."
    show violet_parada b_none

    show mc_parado_base b_hablando o_abajonm c_rbase_facepalm with sprite_fast
    mc "Es que... "
    
    show jasmine_parada c_rbase_base o_base b_none at entrar_derecha_centro with sprite_normal
    pause 0.5
    show jasmine_parada c_rbase_saludando at personaje_flip with sprite_fast
    pause 0.5
    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 0.5
    
    show mc_parado_base b_seria o_base c_rbase_base with sprite_fast
    
    show jasmine_parada b_hablando o_arribanm c_rbase_dedolabio with sprite_fast
    jasmine "¿Por que pelean ahora?"
    show jasmine_parada b_none o_base
    

    show jasmine_parada at personaje_flip with sprite_fast
    pause 0.5
    
    show violet_parada b_hablando o_enojados c_rbase_brazoscruzados with sprite_fast
    violet "Porque [mc_name] aprovecho que estaba solo en mi habitacion y me robo ropa interior"
    show violet_parada b_none

    show jasmine_parada b_hablando c_rbase_brazoscruzados with sprite_fast
    jasmine "Es una acusacion fuerte jajaja"
    show jasmine_parada b_sorprendida
    jasmine "Pero no te enojes, es algo normal a esa edad"
    show jasmine_parada b_felizcerrada c_rbase_base with sprite_fast

    show violet_parada b_hablando 
    violet "No me interesa si es normal o no"
    show violet_parada b_none

    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 1.0

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "No fue asi, sabes que fue todo una confusion"
    show mc_parado_base b_seria

    show jasmine_parada b_hablando
    jasmine "No lo hagas mas si le molesta"
    show jasmine_parada b_sorprendida c_rbase_dedolabio with sprite_fast
    jasmine "Si te vuelve a surgir la necesidad, yo te regalo una jajaja"
    show jasmine_parada b_felizcerrada

    show violet_parada b_hablando o_arribanm
    violet "Idiota..."
    show violet_parada b_none o_base

    show mc_parado_base b_abiertachica
    mc "Se esta malinterpretando todo"
    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_fast
    mc "Solo queria preguntarle por el regalo que le traje de Central City"
    show mc_parado_base b_abiertachica
    mc "Queria saber si te habia gustado"
    show mc_parado_base b_seria c_rbase_base o_base

    show jasmine_parada c_rbase_base at personaje_flip with sprite_fast
    pause 1.0

    show violet_parada b_hablando c_rbase_pensando with sprite_fast
    violet "Si me gusto, pero despues de esto tengo mas dudas sobre las intenciones de tu regalo"
    show violet_parada b_none c_rbase_base with sprite_fast

    show jasmine_parada b_hablando
    jasmine "Uhhhhh ahora me pregunto que clase de regalo es"
    show jasmine_parada b_none

    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 1.0

    show mc_parado_base b_hablando c_rbase_facepalm o_abajonm with sprite_fast
    mc "Es solo un cosplay, recorde que es algo que siempre quizo y pense que era un buen regalo"
    show mc_parado_base b_abiertachica 
    mc "Y antes de que digas algo, no es nada raro... es de uno de sus personajes favoritos"
    show mc_parado_base b_seria o_base c_rbase_brazoscruzados with sprite_fast

    show jasmine_parada b_hablando
    jasmine "No veo el problema entonces"
    show jasmine_parada b_none

    show jasmine_parada at personaje_flip with sprite_fast
    pause 1.0

    show violet_parada b_hablando o_arribanm c_rbase_brazoscruzados with sprite_fast
    violet "Gracias por el regalo..."
    show violet_parada b_hablandochica o_base
    violet "¿Feliz?"
    show violet_parada b_none

    show jasmine_parada b_hablando c_rbase_brazoscruzados with sprite_fast
    jasmine "No te portes como una niña Violet, te trajo un regalo tienes que ser agradecida de verdad"
    show jasmine_parada b_sorprendida
    jasmine "Luego te lo pruebas y se lo mostras"
    show jasmine_parada b_aburrida

    show violet_parada b_hablando c_rbase_base with sprite_fast
    violet "Gracias por el regalo"
    show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_fast
    violet "Pero ni loca voy a mostrarselo"
    show violet_parada b_none


    # Evaluación: estado de progresión con Jasmine
    if not (sistema_quests.obtener_quest("jasmine_questprincipal_0") and sistema_quests.obtener_quest("jasmine_questprincipal_0").completada):
        jump violet_quest04a_jasmine_sin_quest0
    elif not jasmine_event_01_completado():
        jump violet_quest04a_jasmine_quest0_ok
    else:
        jump violet_quest04a_jasmine_todo_ok


################################################################################
## RAMAS JASMINE — Según estado de progresión con Jasmine
################################################################################

label violet_quest04a_jasmine_sin_quest0:

    $ notificar_recuerdo_activado()

    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 1.0

    show jasmine_parada b_hablando
    jasmine "Elegiste mal a quien traerle algo, si me hubieras traido algo a mi, yo te lo mostraria"
    show jasmine_parada b_sorprendida c_rbase_dedolabio with sprite_fast
    jasmine "Ahora no se si quiero darte mi ropa interior"
    show jasmine_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Si te traje algo, pero no tuve momento para dartelo"
    show mc_parado_base b_abiertachica
    mc "No te enojes, por favor"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show jasmine_parada b_hablando c_rbase_base with sprite_fast
    jasmine "Te estaba peleando jajaja"
    show jasmine_parada b_none

    jump violet_quest04a_continua


label violet_quest04a_jasmine_quest0_ok:
    
    $ notificar_recuerdo_activado()

    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 1.0

    show jasmine_parada b_hablando
    jasmine "A mi me trajo un conjunto para entrenar y lo primero que pense fue en mostraselo"
    show jasmine_parada b_sorprendida
    jasmine "Le mande una foto y le dije que pase a verlo cuando entreno por la tarde"
    show jasmine_parada b_none

    show mc_parado_base b_hablando 
    mc "Si todavia te debo pasar a verlo"
    show mc_parado_base b_none 

    show jasmine_parada b_sorprendida c_rbase_dedolabio with sprite_fast
    jasmine "Me parece que te voy a tener que ofrecer mi ropa interior como bonus para que vengas"
    show jasmine_parada b_none

    show mc_parado_base b_hablando 
    mc "No es por eso, no tuve tiempo, perdon Jazmine"
    show mc_parado_base b_none 

    show jasmine_parada b_hablando c_rbase_base with sprite_fast
    jasmine "Te estaba peleando jajaja"
    show jasmine_parada b_none

    jump violet_quest04a_continua


label violet_quest04a_jasmine_todo_ok:
    
    $ notificar_recuerdo_activado()

    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 1.0

    show jasmine_parada b_hablando
    jasmine "A mi me trajo un conjunto para entrenar y lo primero que pense fue en mostraselo"
    show jasmine_parada b_sorprendida
    jasmine "Le mande una foto y le dije que pase a verlo cuando entreno por la tarde"
    show jasmine_parada b_hablando
    jasmine "Parece que le gusto mucho"
    show jasmine_parada b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_fast
    mc "Si, te quedaba genial, tengo buen gusto"
    show mc_parado_base b_none with sprite_fast

    show jasmine_parada b_hablando
    jasmine "Es mi conjunto favorito ahora"
    show jasmine_parada b_none

    jump violet_quest04a_continua


################################################################################
## CONTINUACIÓN — Label común post-evaluación Jasmine
################################################################################

label violet_quest04a_continua:

    show jasmine_parada at personaje_flip with sprite_fast
    pause 1.0

    show jasmine_parada b_hablando
    jasmine "Volviendo al tema, Violet si te hizo un regalo lo minimo que podes hacer es mostrarselo"
    show jasmine_parada b_none

    show violet_parada b_hablandochica o_enojados c_rbase_brazoscruzados with sprite_fast
    violet "No se porque te metes Jasmine, no es tu asunto"
    show violet_parada b_none o_base

    show jasmine_parada b_hablando
    jasmine "Seguite portando como una niña pequeña si queres"
    show jasmine_parada b_sorprendida
    jasmine "Mejor para mi"
    show jasmine_parada b_none

    show jasmine_parada at personaje_enderezar with sprite_fast
    pause 1.0

    show mc_parado_base b_hablando
    mc "No se peleen, no es la idea"
    show mc_parado_base b_abiertachica
    mc "Si no quiere ya esta, no hay que insistir"
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "Si, lo mejor es no insistirle"
    show jasmine_parada b_sorprendida c_rbase_saludando with sprite_fast
    jasmine "Nos vemos luego"
    show jasmine_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_abiertachica
    mc "Nos vemos luego"
    show mc_parado_base b_none

    show jasmine_parada at personaje_salir_izquierda

    hide jasmine_parada with dissolve

    show mc_parado_base b_hablando
    mc "No era para molestarte de verdad"
    show mc_parado_base b_abiertachica
    mc "Prometo no molestarte mas con eso"
    show mc_parado_base b_none

    hide mc_parado_base with dissolve
    hide violet_parada with dissolve



    $ completar_quest_actual("violet")

    
    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    jump game_loop
