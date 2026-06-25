################################################################################
## Violet Quest 11 — Los ruidos nocturnos
################################################################################
## Label narrativo principal y ramificaciones
## Corresponde a: quest_violet_6 (id: violet_questprincipal_11)


# =============================================================================
# VARIABLES
# =============================================================================
# Ya no se necesitan variables de estado temporal para jabon, aceite y silicona.


################################################################################
## LABEL PRINCIPAL — Quest 7 de Violet
################################################################################

label quest_violet_questprincipal_11:

    $ ocultar_hud()
    window show

    # Escena nocturna en la habitacion de Violet
    scene expression "images/bg/casa/bg_casa_noche_hviolet.png" with fade

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    # Dialogo introductorio
    show mc_parado_base b_hablando
    mc "Violet, te traje esto."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Uh, que es? Es una caja bastante grande..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Es un conjunto de cosplays. Vi que te gustaba eso y pense que quizás querías probarlos."
    show mc_parado_base b_none

    # Consumir item
    $ store.inventario["conjunto_cosplays"] -= 1
    if store.inventario["conjunto_cosplays"] <= 0:
        $ del store.inventario["conjunto_cosplays"]
    
    show violet_parada b_hablandochica
    violet "¿E-en serio? ¿Para mí? ¿Y cuántos compraste, esto debe haber salido carísimo!"
    show violet_parada b_none
    
    show mc_parado_base b_hablando
    mc "Lo importante es que te gusten, así tienes más opciones para probarte además del que ya tenías."
    show mc_parado_base b_none
    
    show violet_parada b_hablandochica
    violet "Muchas gracias en serio... no me lo esperaba. Déjame ver qué hay adentro."
    show violet_parada b_none
    
    menu:
        "¿Quieres que te deje sola para probártelos?":
            jump violet_quest11_opcion_a
        "Me gustaría ver como te quedan...":
            jump violet_quest11_opcion_b
        "Apuesto a que te van a quedar increibles":
            jump violet_quest11_opcion_c


################################################################################
## OPCION A
################################################################################

label violet_quest11_opcion_a:

    show mc_parado_base b_hablando
    mc "¿Quieres que te deje sola para probártelos?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Hmm... no, no hace falta. Puedes quedarte, me gustaría saber tu opinión."
    show violet_parada b_none

    jump violet_quest11_cierre


################################################################################
## OPCION B
################################################################################

label violet_quest11_opcion_b:

    show mc_parado_base b_hablando
    mc "Me gustaría ver como te quedan..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Q-quédate entonces. Me sirve tener una segunda opinión."
    show violet_parada b_none

    jump violet_quest11_cierre


################################################################################
## OPCION C
################################################################################

label violet_quest11_opcion_c:

    show mc_parado_base b_hablando
    mc "Apuesto a que te van a quedar increíbles."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "B-bueno, gracias... quédate así me dices cuál me queda mejor."
    show violet_parada b_none

    jump violet_quest11_cierre


################################################################################
## CIERRE — Narrativa final
################################################################################

label violet_quest11_cierre:

    show violet_parada b_hablandochica
    violet "Hay un montón de opciones aquí, me va a llevar un tiempo medirme todo esto."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Tomate tu tiempo, tenemos toda la noche."
    show mc_parado_base b_none
    
    show violet_parada b_hablandochica
    violet "de nuevo, gracias por comprarme todo esto, en serio lo valoro muchísimo."
    show violet_parada b_none

    piensa "(Parece que le gustaron mucho los cosplays)"

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    # Completar quest
    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
