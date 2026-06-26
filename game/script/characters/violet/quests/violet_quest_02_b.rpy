################################################################################
## Violet Quest 02_B — Los mangas de Violet
################################################################################
## El jugador pasa a buscar los mangas que Violet prometió prestarle.
## Se activa mediante la opcion "Vengo por los mangas" en la puerta de noche.

# =============================================================================
# VARIABLES
# =============================================================================

# Guarda la eleccion del jugador al recibir los mangas ("deseo" o "amor")
default violet_recuerdo_mangas = None


################################################################################
## LABEL PRINCIPAL
################################################################################

label quest_violet_questprincipal_02_b:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Violet responde desde adentro — el fondo ya es el pasillo (seteado por door_access)
    violet "Pasa."

    # Transicion a la habitacion de Violet (horario noche)
    $ _loc_hviolet_02b = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet_02b = _loc_hviolet_02b.background if _loc_hviolet_02b else None
    if _bg_hviolet_02b:
        scene expression _bg_hviolet_02b with fade

    show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando
    mc "¿Y ya elegiste cual va a ser?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Sí... tengo elegi algunos separados"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sabes lo que no me gusta, eso es lo importante"
    show mc_parado_base b_none

    show violet_parada c_pijama_pensando b_hablandochica with sprite_fast
    violet "Mmm... nada de protas heroicos que quieren salvar al villano supongo"
    show violet_parada c_pijama_base b_none with sprite_fast

    show mc_parado_base b_felizcerrada o_felicescerrados
    mc "Por favor no jajajaja"
    show mc_parado_base b_none o_base

    show violet_parada b_hablando
    violet "¿Pero buscas algún genero en particular?"
    show violet_parada b_none

    show mc_parado_base b_hablando o_arribanm c_rbase_pensando with sprite_fast
    mc "No, si tienes algo con una historia media intrincada estaria bien"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    show violet_parada b_hablando
    violet "Ya se cuales podrian ser"
    show violet_parada b_aburrida

    hide violet_parada with sprite_fast
    show violet_espalda p_base at right with sprite_fast

    show mc_parado_base o_abajonm b_abierta
    piensa "Ufff... es impresionante el trasero que tiene Violet"
    piensa "Yo pensaba que eran esas calza que usa, pero veo que no"
    show mc_parado_base o_base b_none

    show violet_espalda p_base at salir_poquito with sprite_fast

    violet "Bueno veamos..."

    show violet_espalda p_novela at entrar_poquito with sprite_fast

    violet "Tengo este un colegio donde compiten entre los estudiantes con pruebas para subir de clase..."

    show mc_parado_base b_hablando o_cerrados c_rbase_avergonzado with sprite_fast
    mc "Perdón no te escuche ¿Qué dijiste?"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    piensa "Me tengo que concentrar en lo que me dice y no en su trasero"
    show mc_parado_base c_rbase_confianza with sprite_fast
    piensa "Yo puedo con esto"
    show mc_parado_base c_rbase_base with sprite_fast

    violet "Decía que tengo uno de un colegio donde compiten entre los estudiantes con pruebas para subir de clase, es bastante bueno"

    show mc_parado_base b_hablando o_arribanm c_rbase_pensando with sprite_fast
    mc "Suena como un poco generico la verdad"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    violet "Sí, es algo generico pero está bien llevado"

    show mc_parado_base b_hablando
    mc "¿Algún otro?"
    show mc_parado_base b_none

    show violet_espalda p_rascando1 with sprite_fast
    pause 0.3
    show violet_espalda p_rascando2 with sprite_fast
    pause 0.3
    show violet_espalda p_rascando1 with sprite_fast

    violet "Mmmm..."
    violet "Ya se"

    show violet_espalda p_base at salir_poquito with sprite_fast
    pause 1.0
    show violet_espalda p_fantasia at entrar_poquito with sprite_fast

    violet "A ver... Este es de un joven que reencarna en otro mundo siendo un slime, es muy bueno"

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "¿Es bueno para las personas que no son fanatica de los slime también?"
    show mc_parado_base b_none

    show violet_espalda p_pensando with sprite_fast

    violet "Buen punto, no se si te va a gustar ese"

    show violet_espalda p_base at salir_poquito with sprite_fast
    pause 1.0
    show violet_espalda p_cyberpunk at entrar_poquito with sprite_fast

    violet "Tiene que ser este"
    violet "Es estilo cyberpunk donde el prota quiere convertirse en el lider de la ciudad y es bastante crudo"

    show mc_parado_base b_hablando 
    mc "Ese si suena interesante"
    show mc_parado_base b_none 

    violet "Aparte el cyberpunk y los robots siempre te gustaron"

    show mc_parado_base b_hablando c_rbase_señalando with sprite_fast
    mc "Tienes razón"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_espalda p_base at salir_todo with sprite_fast
    pause 1.0
    hide violet_espalda

    show violet_parada c_pijama_mangas ca_pijama at entrar_derecha_aright with sprite_fast

    show mc_parado_base b_hablando
    mc "Perdi la buena vista"
    show mc_parado_base b_none
    show violet_parada c_pijama_base with sprite_fast
    show mc_parado_base c_rbase_mangas with sprite_fast
    pause 0.5
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Ahora si... ¿Qué dijiste?"
    show violet_parada b_aburrida

    show mc_parado_base c_rbase_facepalm b_seria o_abajonm with sprite_fast
    piensa "Lo dije en voz alta..."
    show mc_parado_base b_hablando o_base c_rbase_brazoscruzados with sprite_fast
    mc "Nada nada"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_juzgandonm c_pijama_brazoscruzados with sprite_fast
    violet "Te esche, solo te estaba dando lugar a que me cuentes cual es la buena vista que tenías"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando o_cerrados c_rbase_avergonzado with sprite_fast
    mc "Prefiero no hacerlo"
    show mc_parado_base b_none o_base

    show violet_parada b_hablando 
    violet "Yo si"
    show violet_parada b_none

    show mc_parado_base b_hablando o_arribanm 
    mc "Me quede impactado cuando te diste vuelta"
    show mc_parado_base b_abiertachica o_base
    mc "Perdón me tomo desprevenido"
    show mc_parado_base b_none 

    show violet_parada b_hablandochica o_enojados 
    violet "¿Qué? ¿Me estabas mirando el trasero?"
    show violet_parada b_hablando
    violet "Es increíble que cada vez que intento no estar molesta contigo, terminas logrando que si lo este"
    show violet_parada b_aburrida

    show mc_parado_base b_abiertachica
    mc "La verdad es que..."
    show mc_parado_base b_none 

    menu:
        "No puedo creer lo mucho que creciste":
            jump violet_quest02b_opcion_deseo
        "Todo esto me trajo recuerdo":
            jump violet_quest02b_opcion_amor


################################################################################
## Opcion A — +2 deseo
################################################################################

label violet_quest02b_opcion_deseo:

    $ violet_recuerdo_mangas = "deseo"

    show mc_parado_base b_hablando
    mc "No puedo creer lo mucho que creciste todo este tiempo"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica o_base c_pijama_pensando with sprite_fast
    violet "¿Qué se supone que significa eso?"
    show violet_parada b_aburrida 

    show mc_parado_base b_abiertachica
    mc "Me cuesta asimilar el paso de una niña a una chica linda"
    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_fast
    mc "Me pones las cosas dificiles"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica with sprite_fast
    violet "¿Dificiles?"
    show violet_parada b_aburrida c_pijama_brazoscruzados ot_avergonzada with sprite_fast

    show mc_parado_base b_abiertachica c_rbase_avergonzado with sprite_fast
    mc "Sí, dificiles... es todo lo que voy a decir"
    show mc_parado_base b_hablando
    mc "Gracias por los mangas"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast


    jump violet_quest02b_fin


################################################################################
## Opcion B — +4 amor
################################################################################

label violet_quest02b_opcion_amor:

    $ violet_recuerdo_mangas = "amor"

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Solo estaba mirando lo mucho que creciste"
    show mc_parado_base b_abiertachica
    mc "Se me vino el pasado, hablando juntos de mangas y luego el presente"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    show violet_parada b_hablandochica o_juzgandonm c_pijama_pensando with sprite_fast
    violet "¿Y cual es el problema?"
    show violet_parada b_aburrida o_base

    show mc_parado_base b_hablando o_cerrados c_rbase_brazoscruzados with sprite_fast
    mc "Todo lo contrario, me alegra que aunque el tiempo haya pasado, pueda estar aquí"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    show violet_parada b_hablando c_pijama_brazoscruzados with sprite_fast
    violet "Te estas poniendo raro"
    show violet_parada b_hablandochica
    violet "Y me preocupan tus intenciones..."
    show violet_parada b_aburrida c_pijama_base with sprite_fast

    show mc_parado_base b_hablando
    mc "Fue un simple comentario"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Que tuviste luego de estar mirandome un rato..."
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "Te vas a acostumbrar, es imposible que no te mire"
    show mc_parado_base b_none

    show violet_parada b_hablandochica ot_avergonzada c_pijama_verguenza with sprite_fast
    violet "No tengo que acostumbrarme a nada"
    show violet_parada b_sonrisaleve c_pijama_brazoscruzados with sprite_fast

    show mc_parado_base b_abiertachica c_rbase_base with sprite_fast
    mc "Te pusiste colorara jajaja"
    show mc_parado_base b_hablando
    mc "Gracias por los mangas Violet"
    show mc_parado_base b_felizcerrada


    jump violet_quest02b_fin


################################################################################
## Fin — entregar mangas y completar quest
################################################################################

label violet_quest02b_fin:

    scene expression "images/bg/casa/bg_casa_trasnoche_pasilloarriba.png" with fade

    show mc_parado_base c_rbase_pensando o_arribanm b_none with sprite_fast
    piensa "La situación se fue para otro lado, espero que no se tome las cosas a mal"
    piensa "De momento a leer los mangas, con estos cuatro tengo para un buen rato"
    show mc_parado_base c_rbase_base o_base with sprite_fast

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    # Agregar mangas al inventario
    $ agregar_al_inventario("mangas_violet_mc")

    # Evaluar ruta elegida y aplicar stats
    if violet_recuerdo_mangas == "deseo":
        $ obtener_npc("violet").modificar_stat2(2)
    elif violet_recuerdo_mangas == "amor":
        $ obtener_npc("violet").modificar_stat1(4)

    # Mover al pasillo, avanzar tiempo y completar quest
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ avanzar_horario()
    $ completar_quest_actual("violet")
    $ desbloquear_skin("violet_pijama_base")

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop
