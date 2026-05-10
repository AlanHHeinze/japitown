################################################################################
## Violet Quest 06 — El cosplay de Violet
################################################################################
## Label narrativo principal y ramificaciones
## Corresponde a: quest_violet_6 (id: violet_questprincipal_6)
## Se ramifica según violet_quest2_trajesexy (decisión de quest 2)


################################################################################
## LABEL PRINCIPAL — Quest 6 de Violet
################################################################################

label quest_violet_questprincipal_6:

    # Ocultar HUD durante la quest
    $ ocultar_hud()
    window show

    # Restaurar fondo de la locación actual
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    # Mostrar sprites
    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    # Diálogo introductorio
    show mc_parado_base b_hablando
    mc "Oye Violet, ¿cómo te fue con el cosplay?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No me lo probé..."
    show violet_parada b_none
    pause 0.3
    show violet_parada b_hablandochica o_enojados
    violet "¿Por qué tan insistente?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Para saber si lo tengo que cambiar..."
    show mc_parado_base b_none

    # Ramificación según decisión de quest 2
    if violet_quest2_trajesexy:
        jump violet_quest6_rama_sexy
    else:
        jump violet_quest6_rama_normal


################################################################################
## RAMA SEXY — El jugador eligió el traje sexy en quest 2
################################################################################

label violet_quest6_rama_sexy:


    show violet_parada b_hablandochica
    violet "Es porque me queres ver con ese traje ajustado..."
    show violet_parada b_none
    pause 0.3
    show violet_parada b_hablandochica o_enojados
    violet "Dijiste que lo compraste porque me quedaria sexy"
    show violet_parada b_none

    mc "..."
    
    show violet_parada b_hablandochica
    violet "Ves, no decís nada"
    show violet_parada b_none
    
    show mc_parado_base b_hablando
    mc "Bueno un poco si, quizas lo primero que pense fue en eso..."
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Pero sabes que la verdadera intención fue cumplir con tu deseo de hacer un cosplay en una convención..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No importa cual sea la intencion, no hay posibilidades de que vaya a una convención con eso..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Bueno... ¿Y con otra cosa?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Quizas..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Podría mandarlo de vuelta y pedir un cambio..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Por que no?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Porque me gusta y quiero tenerlo"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Entonces... ¿Te lo vas a poner?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No, pero lo voy a guardar"
    show violet_parada b_none

    mc "..."

    show violet_parada b_hablandochica
    violet "¿Y ahora?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Aunque sea me lo podrías mostrar a mí, ya que te lo vas a quedar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Vez, es lo unico que te importa..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Me lo muestras y vemos que tan llamativo es, si es mucho como dices te lo quedas y buscamos otro para la convención"
    show mc_parado_base b_none

    violet "..."

    show violet_parada b_hablandochica
    violet "Me voy"
    show violet_parada b_none

    hide violet_parada

    jump violet_quest6_cierre
    

################################################################################
## RAMA NORMAL — El jugador NO eligió el traje sexy en quest 2
################################################################################

label violet_quest6_rama_normal:

    show violet_parada b_hablandochica
    violet "Igual me lo voy a quedar"
    show violet_parada b_none
    pause 0.3
    show violet_parada b_hablandochica o_enojados
    violet "No te preocupes por eso"
    show violet_parada b_none

    mc "..."
    
    show violet_parada b_hablandochica
    violet "¿Que pasa?"
    show violet_parada b_none
    
    show mc_parado_base b_hablando
    mc "¿Para que te lo vas a quedar?"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Si no lo vas a usar..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Porque me gusta"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Entonces... ¿Te lo vas a poner?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No, pero lo voy a guardar"
    show violet_parada b_none

    mc "..."

    show violet_parada b_hablandochica
    violet "¿Y ahora?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Aunque sea me lo podrías mostrar a mí, ya que te lo vas a quedar"
    show mc_parado_base b_none

    violet "..."

    show mc_parado_base b_hablando
    mc "Me lo muestras y vemos que tan llamativo es, si es mucho como dices te lo quedas y buscamos otro para la convención"
    show mc_parado_base b_none

    violet "..."

    show violet_parada b_hablandochica
    violet "Me voy"
    show violet_parada b_none

    hide violet_parada
    
    jump violet_quest6_cierre


################################################################################
## CIERRE — Label común final
################################################################################

label violet_quest6_cierre:

    piensa "Quizas pueda lograr que lo use..."

    hide mc_parado_base with dissolve

    # Completar quest
    $ completar_quest_actual("violet")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    jump game_loop
