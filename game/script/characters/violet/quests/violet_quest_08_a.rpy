################################################################################
## Quest 08_a — La tormenta
################################################################################

# =============================================================================
# IMAGENES
# =============================================================================
image vq8a_living_nublado    = "images/quest/violet/quest08/violet_quest08_livingnublado.png"
image vq8a_living_lloviendo  = "images/quest/violet/quest08/violet_quest08_livinglloviendo.png"
image vq8a_living_tormenta   = "images/quest/violet/quest08/violet_quest08_livingtormenta.png"
image vq8a_living_tormenta1  = "images/quest/violet/quest08/violet_quest08_livingtormenta1.png"
image vq8a_living_tormenta2  = "images/quest/violet/quest08/violet_quest08_livingtormenta2.png"
image vq8a_living_cerrado    = "images/quest/violet/quest08/violet_quest08_livingtormentacerrado.png"
image vq8a_mc_tv             = "images/quest/violet/quest08/violet_quest08_mcmirandotv.png"
image vq8a_tv1               = "images/quest/violet/quest08/violet_quest08_tv1.png"
image vq8a_tv2               = "images/quest/violet/quest08/violet_quest08_tv2.png"
image vq8a_tv3               = "images/quest/violet/quest08/violet_quest08_tv3.png"
image vq8a_tv4               = "images/quest/violet/quest08/violet_quest08_tv4.png"
image vq8a_tv5               = "images/quest/violet/quest08/violet_quest08_tv5.png"
image vq8a_hviolet_tormenta  = "images/quest/violet/quest08/violet_quest08_hviolet_tormenta.png"
image vq8a_ducha             = "images/quest/violet/quest08/violet_quest08_ducha.png"
image vq8a_duchaescena       = "images/quest/violet/quest08/violet_quest08_duchaescena.png"

# =============================================================================
# VARIABLES
# =============================================================================
default vq8a_ropero_visto   = False
default vq8a_cajonera_vista = False

################################################################################
## SCREENS
################################################################################

# Patron A: overlay sobre el living con boton "Ver TV"
screen vq8a_ver_tv_screen():
    if sistema_locaciones.locacion_actual and sistema_locaciones.locacion_actual.id != "casa_living":
        timer 0.01 action Hide("vq8a_ver_tv_screen")
    else:
        button:
            xpos 960
            ypos 420
            xsize 380
            ysize 240
            xanchor 0.5
            yanchor 0.0
            background Frame(Solid("#FFFFFF00"), 0, 0)
            hover_background Frame(Solid("#FFFFFF22"), 0, 0)
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action [Hide("vq8a_ver_tv_screen"), Jump("violet_quest08a_ver_tv")]
            text "Ver TV" size 22 color "#ffffff" xalign 0.5 yalign 0.5 outlines [(1, "#000000", 0, 0)]


# Patron B: exploracion habitacion de Violet (ropero + cajonera)
screen vq8a_habitacion_violet():
    # Fondo absorbe clicks
    button:
        xpos 0 ypos 0 xsize 1920 ysize 1080
        background None
        action NullAction()

    # Ropero
    if not vq8a_ropero_visto:
        button:
            xpos 380
            ypos 560
            xsize 220
            ysize 320
            xanchor 0.5
            yanchor 0.0
            background Frame(Solid("#FFFFFF00"), 0, 0)
            hover_background Frame(Solid("#FFFFFF22"), 0, 0)
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("ropero")
            text "Ropero" size 20 color "#ffffff" xalign 0.5 yalign 0.5 outlines [(1, "#000000", 0, 0)]

    # Cajonera
    if not vq8a_cajonera_vista:
        button:
            xpos 1520
            ypos 620
            xsize 200
            ysize 200
            xanchor 0.5
            yanchor 0.0
            background Frame(Solid("#FFFFFF00"), 0, 0)
            hover_background Frame(Solid("#FFFFFF22"), 0, 0)
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("cajonera")
            text "Cajonera" size 20 color "#ffffff" xalign 0.5 yalign 0.5 outlines [(1, "#000000", 0, 0)]

    button:
        xalign 0.5
        ypos 20
        background "#0288D1EE"
        hover_background "#4FC3F7"
        padding (30, 10)
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("salir")
        text "Salir" size 22 color "#ffffff" bold True


################################################################################
## LABELS
################################################################################

label violet_quest08a_despertar:
    # Mover todos los NPCs fuera
    $ obtener_npc("violet").locacion_actual  = "fuera"
    $ obtener_npc("monica").locacion_actual  = "fuera"
    $ obtener_npc("jasmine").locacion_actual = "fuera"
    $ actualizar_rutinas_npcs()

    window show
    piensa "Hoy las chicas salen. Voy a estar solo en casa."
    piensa "Podría aprovechar y ver la tele tranquilo."
    window hide

    $ activar_restriccion(
        locaciones_permitidas=None,
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=None,
        mensajes_acciones={
            "avanzar_tiempo": "Podría aprovechar a ver la tv",
            "dormir":         "Podría aprovechar a ver la tv",
            "entrenar":       "Podría aprovechar a ver la tv",
            "trabajar":       "Podría aprovechar a ver la tv",
            "usar_item":      "Podría aprovechar a ver la tv",
            "comprar":        "Podría aprovechar a ver la tv",
        },
        mensaje_npc_bloqueado="Podría aprovechar a ver la tv",
        celular_bloqueado=True,
        mensaje_celular="Podría aprovechar a ver la tv",
        npcs_ocultos=["violet", "monica", "jasmine"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_living", "violet_quest08a_en_living")

    call mensajes_al_despertar from _call_quest08a_despertar_msgs

    $ mostrar_hud()
    jump game_loop


label violet_quest08a_en_living:
    show screen vq8a_ver_tv_screen
    return


label violet_quest08a_ver_tv:
    $ ocultar_hud()
    window hide

    # Escena inicial — cielo nublado, MC en el sillon
    scene vq8a_living_nublado with fade
    show vq8a_mc_tv
    show vq8a_tv1 as vq_tv

    window show
    piensa "Qué tranquilo. Hacía tiempo que no tenía la tele para mí solo"

    show vq8a_tv2 as vq_tv with dissolve
    piensa "Quiero ver algo pero no creo que un documental de elefantes sea la mejor opción"
    piensa "Se esta poniendo feo el dia, parece que va a llover"

    # Empieza a llover
    scene vq8a_living_lloviendo with Dissolve(2.0)
    show vq8a_mc_tv
    show vq8a_tv2 as vq_tv

    piensa "¿Está lloviendo? Me pregunto si las chicas se llevaron paraguas... Espero que sí"
    piensa "Estan bastante de moda ultimamente los piratas, no me quejo me gustan pero ya cansa un poco"

    show vq8a_tv3 as vq_tv with dissolve

    # Tormenta
    scene vq8a_living_tormenta with Dissolve(2.0)
    show vq8a_mc_tv
    show vq8a_tv3 as vq_tv

    piensa "La tormenta se está poniendo bastante fuerte"

    scene vq8a_living_tormenta1 with Dissolve(2.0)
    show vq8a_mc_tv
    show vq8a_tv4 as vq_tv

    piensa "No parece que vaya a parar pronto"

    scene vq8a_living_tormenta2 with Dissolve(2.0)
    show vq8a_mc_tv
    show vq8a_tv5 as vq_tv

    piensa "Mejor voy a cerrar las ventanas antes de que entre agua"
    window hide

    # MC cierra ventanas — transición al living cerrado
    hide vq8a_mc_tv with dissolve
    hide vq_tv with dissolve
    scene vq8a_living_cerrado with Dissolve(1.5)

    pause 0.8
    window show
    piensa "Uf. Qué tormenta, ya estaba entrando agua a la casa"
    piensa "Tendria que revisar que esté todo cerrado, no vaya a ser que entre más agua"
    window hide

    # Golpe en la puerta de entrada
    play sound "audio/sfx/door_knock_3.ogg"
    pause 0.9

    window show
    piensa "¿Llego alguien?"
    window hide

    # Violet entra mojada
    show violet_mojada c_mojada o_base b_none at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    window show

    show violet_mojada b_hablando
    violet "Hola..."
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "¡Violet! ¿Estás bien? ¿Qué pasó?"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Monica me dejo en casa de Nath para ver el cosplay y cuando sali estaba apenas nublado, no pense que iba a llover tan fuerte"
    show violet_mojada b_none

    show violet_mojada b_hablando
    violet "Y aca estoy empapada"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "Subi a darte una ducha caliente antes de que te agarre un resfrio"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Ahora voy"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "¿Necesitas algo?"
    show mc_parado_base b_none

    show violet_mojada b_hablandochica
    violet "Si ¿Me podés traer el pijama rosa del ropero?"
    show violet_mojada b_none

    show violet_mojada b_sonrisaleve
    violet "Asi no mojo toda mi habitacion"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "Si, anda a bañarte que ahora te lo llevo"
    show mc_parado_base b_none

    hide violet_mojada with dissolve

    piensa "Pobre Violet llego empapada, voy a buscar su pijama y dejarselo"
    window hide

    # Fase 2 — solo living, pasillo arriba y habitación de Violet
    $ desactivar_restriccion()
    $ activar_restriccion(
        locaciones_permitidas=["casa_living", "casa_pasilloarriba", "casa_hviolet"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento="Tengo que buscar las cosas de Violet",
        mensajes_acciones={
            "avanzar_tiempo": "Tengo que buscar las cosas de Violet",
            "dormir":         "Tengo que buscar las cosas de Violet",
            "entrenar":       "Tengo que buscar las cosas de Violet",
            "trabajar":       "Tengo que buscar las cosas de Violet",
            "usar_item":      "Tengo que buscar las cosas de Violet",
            "comprar":        "Tengo que buscar las cosas de Violet",
        },
        mensaje_npc_bloqueado="No es el momento.",
        celular_bloqueado=True,
        mensaje_celular="No es el momento.",
        npcs_ocultos=["violet", "monica", "jasmine"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_hviolet", "violet_quest08a_en_hviolet")

    $ sistema_locaciones.mover_a_locacion("casa_living")
    $ mostrar_hud()
    jump game_loop


label violet_quest08a_en_hviolet:
    $ ocultar_hud()
    window hide

    scene vq8a_hviolet_tormenta with fade
    show screen vq8a_habitacion_violet

    $ _en_hviolet_q8a = True
    while _en_hviolet_q8a:
        $ _res_hv = ui.interact()

        if _res_hv == "ropero":
            hide screen vq8a_habitacion_violet
            window show
            piensa "El pijama rosa... acá está"
            $ vq8a_ropero_visto = True
            window hide
            show screen vq8a_habitacion_violet

        elif _res_hv == "cajonera":
            hide screen vq8a_habitacion_violet
            window show
            piensa "Ropa interior..."
            piensa "No me pidio pero supongo que también la va a necesitar"
            $ vq8a_cajonera_vista = True
            window hide
            show screen vq8a_habitacion_violet

        elif _res_hv == "salir":
            if not vq8a_ropero_visto or not vq8a_cajonera_vista:
                hide screen vq8a_habitacion_violet
                window show
                piensa "Todavía me falta algo. Violet pidió el pijama rosa y deberia llevarle ropa interior tambien"
                window hide
                show screen vq8a_habitacion_violet
            else:
                $ _en_hviolet_q8a = False

    hide screen vq8a_habitacion_violet
    jump violet_quest08a_puerta_baño


label violet_quest08a_puerta_baño:
    scene vq8a_ducha with fade

    window show
    piensa "La ropa de Violet... ¿la dejo afuera o llamo?"

    menu:
        "Dejar la ropa afuera":
            jump violet_quest08a_opcion_a
        "Golpear y entrar":
            jump violet_quest08a_entrar_baño


label violet_quest08a_opcion_a:
    piensa "Mejor la dejo acá y me voy"
    pause 0.3
    violet "¿Ya está?"
    mc "Sí, está afuera de la puerta"
    violet "Gracias"
    piensa "Bien, a seguir con mis cosas"
    window hide
    $ desactivar_restriccion()
    $ completar_quest_actual("violet")
    $ avanzar_horario_multiple(2)
    $ mostrar_hud()
    jump game_loop


label violet_quest08a_entrar_baño:
    window show
    piensa "No se si fue la mejor opcion entrar así"
    piensa "Esta lleno de vapor y no veo bien"
    window hide

    pause 0.5

    window show
    piensa "¿Podria acercarme mas?"

    menu:
        "Irse":
            jump violet_quest08a_baño_irse
        "Acercarse" if getattr(store, 'mc_destreza', 0) >= 3:
            jump violet_quest08a_baño_acercarse


label violet_quest08a_baño_irse:
    piensa "Mejor me voy, ya tuve suficientes problemas con Violet para buscarme uno nuevo"
    window hide
    $ desactivar_restriccion()
    $ completar_quest_actual("violet")
    $ avanzar_horario_multiple(2)
    $ mostrar_hud()
    jump game_loop


label violet_quest08a_baño_acercarse:
    scene vq8a_duchaescena with Dissolve
    window show
    piensa "No puedo creer que este haciendo esto, no se desde cuando pero me esta atrayendo mucho Violet"
    piensa "Hasta aca fue suficiente, si me ve me mata"
    piensa "Mejor me voy"
    window hide
    $ desactivar_restriccion()
    $ completar_quest_actual("violet")
    $ avanzar_horario_multiple(2)
    $ mostrar_hud()
    jump game_loop
