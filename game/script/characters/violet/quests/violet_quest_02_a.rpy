################################################################################
## Violet Quest 02_A — Un manga prestado
################################################################################
## El jugador le pide a Violet que le preste mangas para leer.
## Si tiene 10+ de amor: Violet acepta de entrada (o tras una primera negativa).
## Si tiene menos de 10: Violet rechaza y el botón desaparece hasta llegar al umbral.

# =============================================================================
# VARIABLES
# =============================================================================

# True despues del primer intento (sea exitoso o no)
default violet_quest02a_primer_intento_hecho = False


################################################################################
## LABEL PRINCIPAL — Router
################################################################################

label quest_violet_questprincipal_02_a:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Fondo de la locacion actual donde se da la interaccion
    $ _bg_v02a = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else None
    if _bg_v02a:
        scene expression _bg_v02a with fade

    if not violet_quest02a_primer_intento_hecho:
        $ violet_quest02a_primer_intento_hecho = True
        if obtener_stat1("violet") >= 10:
            jump violet_quest02a_acepta_directo
        else:
            jump violet_quest02a_rechaza
    else:
        if obtener_stat1("violet") >= 10:
            jump violet_quest02a_acepta_insiste
        else:
            jump violet_quest02a_rechaza_insiste


################################################################################
## Violet rechaza prestar los mangas (amor < 10, primer intento)
################################################################################

label violet_quest02a_rechaza_insiste:
    # Volvió a pedir pero todavía no tiene suficiente amor

    show violet_parada c_rbase_brazoscruzados b_aburrida at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando  
    mc "Hola..."
    show mc_parado_base b_none 

    show violet_parada b_hablandochica
    violet "¿Y ahora?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando  
    mc "¿Ya se te paso el capricho?"
    show mc_parado_base b_none 

    show violet_parada b_hablandochica
    violet "¿Cuál de todos?"
    show violet_parada b_aburrida

    show mc_parado_base c_rbase_cuestionando with sprite_fast
    piensa "El de no querer prestarme ningún manga..."
    show mc_parado_base c_rbase_base with sprite_fast

    show violet_parada b_hablando o_arribanm c_rbase_pensando with sprite_fast
    violet "A ver... mmmm..."
    pause 0.5
    show violet_parada b_hablandochica o_base c_rbase_base with sprite_fast
    violet "No, no se me paso ¿Algo más?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando  
    mc "No era solo eso"
    show mc_parado_base b_none 

    hide violet_parada with dissolve

    piensa "Tengo que mejorar un poco más la relación y quizás logre que me los preste"

    hide mc_parado_base with dissolve

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## Violet rechaza prestar los mangas (amor < 10, primer intento)
################################################################################

label violet_quest02a_rechaza:

    show violet_parada c_rbase_brazoscruzados o_enojados b_aburrida at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando  
    mc "Hola..."
    show mc_parado_base b_none 

    show violet_parada b_hablandochica
    violet "¿Qué quieres?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando
    mc "Violet, ¿me prestarías algún manga para leer?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_base with sprite_fast
    violet "Lee algo por internet..."
    show violet_parada b_aburrida

    show mc_parado_base c_rbase_pensando with sprite_fast
    piensa "Podría... pero no es lo mismo"
    show mc_parado_base b_hablando c_rbase_base with sprite_fast
    mc "Sabes que no es lo mismo... Aparte me gustaría leer algo nuevo y esperaba que me recomiendes algo"
    show mc_parado_base b_none 

    show violet_parada b_hablando c_rbase_pensando with sprite_fast
    violet "¿Tengo cara de pagina de reseñas?"
    show violet_parada b_aburrida c_rbase_base with sprite_fast

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "No seas así... ¿Me prestas o no?"
    show mc_parado_base b_seria c_rbase_base with sprite_fast

    show violet_parada b_hablandochica
    violet "No"
    show violet_parada b_aburrida

    piensa "Cortante como siempre"

    show violet_parada b_hablandochica
    violet "¿Algo más?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando  
    mc "No era solo eso"
    show mc_parado_base b_none

    hide violet_parada with dissolve

    piensa "Tendría que mejorar un poco la relación antes de pedirle cosas"

    hide mc_parado_base with dissolve

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## Violet acepta a la primera (amor >= 10, primer intento)
################################################################################

label violet_quest02a_acepta_directo:

    show violet_parada c_rbase_base o_base b_none at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando  
    mc "Hola..."
    show mc_parado_base b_none 

    show violet_parada b_hablandochica
    violet "¿Qué quieres?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando
    mc "¿Me prestarías algún manga para leer?"
    show mc_parado_base b_none

    pause 0.6

    show violet_parada b_hablando o_arribanm c_rbase_pensando with sprite_fast
    violet "Mmm... pordia ser..."
    show violet_parada b_hablandochica o_base
    violet "¿Qué estas buscando?"
    show violet_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_hablando 
    mc "No se..." 
    show mc_parado_base b_abiertachica c_rbase_idea with sprite_fast
    mc "¿Y si me recomendas algo?"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando 
    violet "Bueno, voy a pensar en cual puede ser"
    show violet_parada b_hablandochica o_arribanm c_rbase_pensando with sprite_fast
    violet "Tengo algunas ideas en mente"
    show violet_parada b_aburrida o_base c_rbase_base with sprite_fast

    show mc_parado_base b_abiertachica c_rbase_victoria with sprite_fast
    mc "Genial!"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica o_arribanm
    violet "Raro..."
    show violet_parada b_hablando o_base
    violet "...Pasa por la noche a buscarlos"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando  
    mc "A la noche paso a buscarlos, gracias!"
    show mc_parado_base b_none

    hide violet_parada with dissolve

    piensa "¡Bien! Conseguí que me preste los mangas sin tener que insistir, eso es un gran paso"
    
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## Violet acepta tras insistencia (amor >= 10, segundo intento)
################################################################################

label violet_quest02a_acepta_insiste:

    show violet_parada c_rbase_brazoscruzados o_base b_none at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando  
    mc "Hola..."
    show mc_parado_base b_none 

    show violet_parada b_hablandochica
    violet "¿Y ahora?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "¿Quería saber si cambiaste de idea sobre prestarme algún manga?"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica o_arribanm c_rbase_pensando with sprite_fast
    violet "No se si tengo menos ganas de prestarte algo o de tenerte insistiendome todo el tiempo..."
    show violet_parada b_hablando o_base c_rbase_base with sprite_fast
    violet "¿Qué estas buscando?"
    show violet_parada b_aburrida

    piensa "La insistencia da sus frutos"

    show mc_parado_base b_abiertachica c_rbase_victoria with sprite_fast
    mc "Genial!"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica o_arribanm
    violet "Raro..."
    show violet_parada b_none o_base

    show mc_parado_base b_hablando 
    mc "No se..." 
    show mc_parado_base b_abiertachica c_rbase_idea with sprite_fast
    mc "¿Y si me recomendas algo?"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando 
    violet "Bueno, voy a pensar en cual puede ser"
    show violet_parada b_hablandochica o_arribanm c_rbase_pensando with sprite_fast
    violet "Tengo algunas ideas en mente"
    show violet_parada b_aburrida o_base c_rbase_base with sprite_fast

    show mc_parado_base b_hablando  
    mc "Lo que te parezca va a estar bien, confio en tu criterio"
    show mc_parado_base b_none

    show violet_parada b_hablando 
    violet "...Pasa por la noche a buscarlos"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando  
    mc "A la noche paso a buscarlos, gracias!"
    show mc_parado_base b_none

    hide violet_parada with dissolve

    piensa "No se si es de la manera que me hubiera gustado pero al menos logré que me preste los mangas, eso es un gran paso"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop
