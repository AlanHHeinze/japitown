################################################################################
## Quest 09_a — Violet enferma
################################################################################

# =============================================================================
# VARIABLES
# =============================================================================
default mc_sabe_violet_enferma      = False
default violet_9a_pedido_actual     = None
default violet_9a_tiene_entregable  = False
default violet_9a_entrega_completada = False
default violet_9a_piensa_mostrado   = False
default violet_9a_enfermedad_dia    = 0
default violet_enferma_atencion     = 0

################################################################################
## LABELS
################################################################################

# Piensa "Debería avisarle a Violet" — se dispara desde game_loop al llegar a
# ETAPA_BOTON_LISTO la primera vez.
label violet_quest09a_piensa_avisarle:
    $ store.violet_9a_piensa_mostrado = True
    window show
    piensa "Debería avisarle a Violet."
    window hide
    jump game_loop


# Manejo de la puerta de Violet durante la enfermedad.
# Salta desde interaccion_puerta_npc antes del flujo normal.
label violet_quest09a_manejo_puerta:
    if not getattr(store, 'mc_sabe_violet_enferma', False):
        # MC todavía no sabe que Violet está enferma
        if store.horario_actual in (0, 1):
            # Mañana / tarde: nadie responde
            window show
            piensa "Violet no está... debe estar en su habitación."
            window hide
            return

        elif store.horario_actual == 2:
            # Noche: Violet responde y el MC descubre que está enferma
            $ ocultar_hud()
            hide screen hud_navegacion
            window show
            play sound "audio/sfx/door_knock_3.ogg"
            pause 0.5
            violet "Pasá."
            $ store.mc_sabe_violet_enferma = True
            $ sistema_locaciones.mover_a_locacion("casa_hviolet")
            window hide
            $ mostrar_hud()
            return

        else:
            # Trasnoche
            window show
            piensa "Debe estar durmiendo, no voy a molestar."
            window hide
            return

    else:
        # MC ya sabe que Violet está enferma
        if store.horario_actual == 0:
            # Mañana: puede entrar
            $ ocultar_hud()
            hide screen hud_navegacion
            window show
            play sound "audio/sfx/door_knock_3.ogg"
            pause 0.5
            violet "Adelante."
            $ sistema_locaciones.mover_a_locacion("casa_hviolet")
            window hide
            $ mostrar_hud()
            return

        elif store.horario_actual == 1:
            # Tarde: Violet durmiendo
            window show
            piensa "Violet debe estar durmiendo, no voy a molestarla."
            window hide
            return

        elif store.horario_actual == 2:
            # Noche: puede entrar
            $ ocultar_hud()
            hide screen hud_navegacion
            window show
            play sound "audio/sfx/door_knock_3.ogg"
            pause 0.5
            violet "Adelante."
            $ sistema_locaciones.mover_a_locacion("casa_hviolet")
            window hide
            $ mostrar_hud()
            return

        else:
            # Trasnoche
            window show
            piensa "Debe estar durmiendo, no voy a molestar."
            window hide
            return


# Interacción con Violet enferma en su habitación.
# Reemplaza el menú de interacción normal durante la quest.
label violet_quest09a_interaccion:
    # Si tiene algo para entregar y no lo ha entregado aún, ir directo a entrega
    if (getattr(store, 'violet_9a_tiene_entregable', False) and
            not getattr(store, 'violet_9a_entrega_completada', False)):
        jump violet_quest09a_entregar_directo

    $ ocultar_hud()
    window show

    show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve

    menu:
        "¿Necesitás algo?":
            if getattr(store, 'violet_9a_pedido_actual', None) is not None:
                show violet_parada b_hablandochica
                violet "Está bien por ahora."
                show violet_parada b_none
            else:
                $ _pedidos_vq9 = [
                    "Quiero algo de comer",
                    "Necesito tomar el medicamento",
                    "Un poco de agua",
                    "Dile a Monica que venga",
                    "Traeme una toalla",
                ]
                $ store.violet_9a_pedido_actual = renpy.random.choice(_pedidos_vq9)
                show violet_parada b_hablandochica
                violet "[store.violet_9a_pedido_actual]."
                show violet_parada b_none
        "Volver":
            pass

    hide violet_parada with dissolve
    window hide
    $ mostrar_hud()
    return


# Entrega a Violet: se llama automáticamente cuando tiene_entregable=True.
label violet_quest09a_entregar_directo:
    $ _pedido_vq9 = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show

    show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve

    if _pedido_vq9 == "Dile a Monica que venga":
        mc "Ya le avisé a Monica, dijo que en un momento va."
    else:
        mc "Acá tengo lo que querías."

    show violet_parada b_sonrisaleve
    violet "Gracias."
    show violet_parada b_none

    hide violet_parada with dissolve

    if not getattr(store, 'violet_9a_entrega_completada', False):
        $ store.violet_enferma_atencion += 1
    $ store.violet_9a_entrega_completada = True

    window hide
    $ mostrar_hud()
    return


# Monica explica que Violet está enferma (opción "Preguntar por Violet").
label violet_quest09a_monica_preguntar:
    $ ocultar_hud()
    window show
    mc "¿No viste a Violet? Quería hablar con ella."
    show monica_parada c_rbase_base o_base b_hablandochica at right with dissolve
    monica "Está en su cuarto. Creo que se pescó algo, estaba medio mal."
    show monica_parada b_none
    hide monica_parada with dissolve
    $ store.mc_sabe_violet_enferma = True
    window hide
    $ mostrar_hud()
    return


# MC le dice a Monica que Violet la llama (opción "Te llama Violet").
label violet_quest09a_monica_llamar:
    $ ocultar_hud()
    window show
    mc "Monica, Violet te llama."
    show monica_parada c_rbase_base o_base b_hablandochica at right with dissolve
    monica "Decile que en un momento voy."
    show monica_parada b_none
    hide monica_parada with dissolve
    $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


# Jasmine explica que Violet está enferma (opción "Preguntar por Violet").
label violet_quest09a_jasmine_preguntar:
    $ ocultar_hud()
    window show
    mc "¿Viste a Violet? Quería decirle algo."
    show jasmine_parada c_rbase_base o_base b_hablando at right with dissolve
    jasmine "Está en su habitación. Me parece que está enferma, no salió en todo el día."
    show jasmine_parada b_none
    hide jasmine_parada with dissolve
    $ store.mc_sabe_violet_enferma = True
    window hide
    $ mostrar_hud()
    return


################################################################################
## ACCIONES DE LOCACIÓN — Mini-juego de cuidado
################################################################################

label accion_violet_heladera:
    $ _pedido_h = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show
    if _pedido_h != "Quiero algo de comer":
        piensa "Violet me pidió [_pedido_h]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Acá tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


label accion_violet_agua:
    $ _pedido_a = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show
    if _pedido_a != "Un poco de agua":
        piensa "Violet me pidió [_pedido_a]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Acá tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


label accion_violet_medicina:
    $ _pedido_m = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show
    if _pedido_m != "Necesito tomar el medicamento":
        piensa "Violet me pidió [_pedido_m]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Acá tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


label accion_violet_toalla:
    $ _pedido_t = getattr(store, 'violet_9a_pedido_actual', None)
    $ ocultar_hud()
    window show
    if _pedido_t != "Traeme una toalla":
        piensa "Violet me pidió [_pedido_t]."
    elif getattr(store, 'violet_9a_tiene_entregable', False):
        piensa "Ya tengo lo que necesito, hay que llevárselo a Violet."
    else:
        piensa "Acá tengo lo que quería Violet."
        $ store.violet_9a_tiene_entregable = True
    window hide
    $ mostrar_hud()
    return


################################################################################
## LABEL DE QUEST (ETAPA_DESARROLLO) — seguridad
################################################################################

label quest_violet_questprincipal_09_a:
    $ completar_quest_actual("violet")
    window hide
    $ mostrar_hud()
    jump game_loop
