################################################################################
## Historia del Repartidor
################################################################################
## Labels de interacción con el repartidor según nivel de confianza

################################################################################
## Label de entrada - Router según confianza
################################################################################

label interaccion_repartidor:
    # Esconder HUD temporalmente
    hide screen hud_navegacion
    $ ocultar_hud()
    
    # Determinar qué label usar según confianza
    $ _label_entrega = obtener_label_entrega()
    
    # Saltar al label correspondiente
    jump expression _label_entrega


################################################################################
## Primera entrega (Confianza = 0)
################################################################################

label entrega_repartidor_0:
    # Primera vez que el jugador recibe un paquete
    
    scene bg_casa_mañana_frente with fade
    
    show repartidor_parado c_base at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    
    show repartidor_parado c_hablando
    repartidor "Hola, ¿Pedido para [mc_name]?"
    show repartidor_parado c_bas

    show mc_parado_base b_hablando
    mc "Si, soy yo"
    show mc_parado_base b_none
    
    show repartidor_parado c_base
    repartidor "¿Eres nuevo? Nunca te había visto por aquí."
    show repartidor_parado c_base

    show mc_parado_base b_hablando
    mc "Si, acabo de mudarme. Esta sera mi casa a partir de ahora"
    show mc_parado_base b_none
    
    show repartidor_parado c_base
    repartidor "Que afortunado..."
    show repartidor_parado c_base

    show mc_parado_base b_hablando
    mc "¿Qué?"
    show mc_parado_base b_none

    show repartidor_parado c_hablando
    repartidor "¿Qué?"
    show repartidor_parado c_base

    show mc_parado_base b_hablando
    mc "Nada... Muchas gracias por la entrega"
    show mc_parado_base b_none

    show repartidor_parado c_hablando
    repartidor "A usted joven"
    show repartidor_parado c_base
    
    # Procesar entrega y obtener items
    $ _items_entregados = procesar_entrega_repartidor()
    
    show repartidor_parado c_hablando
    repartidor "Que tengas un buen día."
    
    hide repartidor_parado with dissolve

    show screen hud_navegacion
    $ mostrar_hud()
    return


################################################################################
## Entregas iniciales (Confianza 1-5)
################################################################################

label entrega_repartidor_1_5:
    # El repartidor ya conoce al jugador
    
    scene bg_casa_mañana_frente with fade
    
    show repartidor_parado c_base at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    
    show mc_parado_base b_hablando
    mc "Hola"
    show mc_parado_base b_none
    
    show repartidor_parado c_hablando
    repartidor "¡Hola de nuevo!"
    show repartidor_parado c_base
    pause 0.3
    show repartidor_parado c_hablando
    repartidor "Otro paquete para ti."
    show repartidor_parado c_base

    show mc_parado_base b_hablando
    mc "Gracias"
    show mc_parado_base b_none
    
    # Procesar entrega y obtener items
    $ _items_entregados = procesar_entrega_repartidor()
    
    show repartidor_parado c_hablando
    repartidor "De nada. ¡Hasta la próxima!"
    show repartidor_parado c_base
    
    hide repartidor_parado with dissolve

    show screen hud_navegacion
    $ mostrar_hud()
    return


################################################################################
## Entregas frecuentes (Confianza > 5)
################################################################################

label entrega_repartidor_5_plus:
    # El repartidor y el jugador ya se conocen bien
    
    scene bg_casa_tarde_frente with fade
    
    show repartidor_parado c_hablando at right
    
    repartidor "¡Hey, mi cliente favorito!"
    
    show repartidor_parado c_base with sprite_normal
    repartidor "Ya sabes cómo es esto..."
    
    # Procesar entrega y obtener items
    $ _items_entregados = procesar_entrega_repartidor()
    
    show repartidor_parado c_hablando with sprite_normal
    repartidor "Otro paquete entregado. ¡Nos vemos pronto!"
    
    hide repartidor_parado with dissolve

    show screen hud_navegacion
    $ mostrar_hud()
    return
