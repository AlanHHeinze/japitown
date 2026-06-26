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
image vq8a_mc_tv             = "images/quest/violet/quest08/violet_quest08_mcmirantotv.png"
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
default vq8a_bgs_originales = {}

################################################################################
## LABELS
################################################################################

# Parte 1 — Al despertar: el MC piensa en su habitacion. El mensaje se muestra
# en un contexto aislado (HUD oculto + escena propia) para que se lea bien y NO
# dentro del game loop. Al terminar pasa a la parte 2 (loop restringido).
label violet_quest08a_despertar:
    # Mover todos los NPCs fuera
    $ obtener_npc("violet").locacion_actual  = "fuera"
    $ obtener_npc("monica").locacion_actual  = "fuera"
    $ obtener_npc("jasmine").locacion_actual = "fuera"
    $ actualizar_rutinas_npcs()

    $ ocultar_hud()
    window hide

    # MC pensando en su habitacion
    $ _bg_hmc_q8a = sistema_locaciones.obtener_locacion("casa_hmc").background
    scene expression _bg_hmc_q8a with fade
    show mc_parado_base c_rbase_pensando o_arribanm b_none at center with dissolve

    window show
    piensa "Hoy las chicas salen. Voy a estar solo en casa."
    piensa "Podría aprovechar y ver la tele tranquilo."
    window hide

    hide mc_parado_base with dissolve

    jump violet_quest08a_iniciar_loop


# Parte 2 — Activa la restricción del dia y devuelve el control al loop
# restringido. La quest sigue su curso cuando el jugador entra al living.
label violet_quest08a_iniciar_loop:
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
    $ mostrar_hud()
    jump game_loop


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
    piensa "Se esta poniendo feo el día, parece que va a llover"

    # Empieza a llover
    scene vq8a_living_lloviendo with Dissolve(2.0)
    show vq8a_mc_tv
    show vq8a_tv2 as vq_tv

    piensa "¿Está lloviendo? Me pregunto si las chicas se llevaron paraguas... Espero que sí"
    piensa "Están bastante de moda ultimamente los piratas, no me quejo me gustan pero ya cansa un poco"

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
    violet "Y aquí estoy empapada"
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
    violet "Si ¿Me puedes traer el pijama rosa del ropero?"
    show violet_mojada b_none

    show violet_mojada b_sonrisaleve
    violet "Así no mojo toda mi habitación"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "Si, anda a bañarte que ahora te lo llevo"
    show mc_parado_base b_none

    hide violet_mojada with dissolve

    piensa "Pobre Violet llego empapada, voy a buscar su pijama y dejarselo"
    window hide

    # Fase 2 — solo living, pasillo arriba y habitacion de Violet
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
    # Registrar un label de entrada para la habitacion de Violet. Sirve para que
    # el routing OMITA el door access (que si no bloquearía porque Violet está en
    # la ducha / oculta) y permita pasar — la entrada se valida solo contra la
    # whitelist de la restricción, que incluye casa_hviolet.
    $ restriccion_quest_activa.registrar_label_locacion("casa_hviolet", "violet_quest08a_entrar_hviolet")

    # Backgrounds especiales de la tormenta durante la fase 2 (modo libre en el
    # game loop). Se guardan los originales y se restauran en el cierre.
    python:
        vq8a_bgs_originales = {}
        _vq8a_overrides = {
            "casa_living":        "images/quest/violet/quest08/violet_quest08_livingtormentacerrado.png",
            "casa_pasilloarriba": "images/bg/casa/bg_casa_trasnoche_pasilloarriba.png",
            "casa_hviolet":       "images/quest/violet/quest08/violet_quest08_hviolet_tormenta.png",
        }
        for _loc_id, _bg_path in _vq8a_overrides.items():
            _loc_obj = sistema_locaciones.obtener_locacion(_loc_id)
            if _loc_obj:
                vq8a_bgs_originales[_loc_id] = _loc_obj.background_base
                _loc_obj.background_base = _bg_path

    # Acciones de locación: ropero y cajonera. Aparecen al estar en la habitacion;
    # al usar AMBAS se auto-avanza (metodología de la quest 03_a), sin botón de salir.
    $ sistema_acciones.registrar_accion(AccionLocacion(
        id="vq8a_ropero", nombre="Ropero", icono=u"🚪",
        locacion_id="casa_hviolet", label_generico="violet_quest08a_accion_ropero",
        reseteo=None, color="#4527A0", color_hover="#7E57C2"
    ))
    $ sistema_acciones.registrar_accion(AccionLocacion(
        id="vq8a_cajonera", nombre="Cajonera", icono=u"🗂️",
        locacion_id="casa_hviolet", label_generico="violet_quest08a_accion_cajonera",
        reseteo=None, color="#2E7D32", color_hover="#43A047"
    ))

    $ sistema_locaciones.mover_a_locacion("casa_living")
    $ mostrar_hud()
    jump game_loop


# Entrada a la habitacion de Violet durante la fase 2. No hace nada por sí mismo
# (la exploración la manejan las acciones Ropero/Cajonera); existe solo para que
# el routing omita el door access y permita entrar aunque Violet no esté.
label violet_quest08a_entrar_hviolet:
    return


# Accion Ropero — el MC encuentra el pijama. Al usar ambas acciones se avanza.
label violet_quest08a_accion_ropero:
    $ ocultar_hud()
    window show
    piensa "El pijama rosa... aquí está"
    window hide

    $ vq8a_ropero_visto = True
    $ sistema_acciones.acciones.pop("vq8a_ropero", None)

    if vq8a_ropero_visto and vq8a_cajonera_vista:
        jump violet_quest08a_ir_al_baño

    $ mostrar_hud()
    return


# Accion Cajonera — el MC encuentra la ropa interior.
label violet_quest08a_accion_cajonera:
    $ ocultar_hud()
    window show
    piensa "Ropa interior..."
    piensa "No me pidió pero supongo que también la va a necesitar"
    window hide

    $ vq8a_cajonera_vista = True
    $ sistema_acciones.acciones.pop("vq8a_cajonera", None)

    if vq8a_ropero_visto and vq8a_cajonera_vista:
        jump violet_quest08a_ir_al_baño

    $ mostrar_hud()
    return


# Fase 3 — El MC ya tiene la ropa. Queda en el pasillo de arriba con todo
# bloqueado salvo la puerta del baño. Al tocar la puerta se dispara el menú.
label violet_quest08a_ir_al_baño:
    window show
    piensa "Ya tengo todo. Voy a llevárselo al baño."
    window hide

    $ desactivar_restriccion()
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_banioarriba"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento="Debo llevarle la ropa a Violet",
        mensajes_acciones={
            "avanzar_tiempo": "Debo llevarle la ropa a Violet",
            "dormir":         "Debo llevarle la ropa a Violet",
            "entrenar":       "Debo llevarle la ropa a Violet",
            "trabajar":       "Debo llevarle la ropa a Violet",
            "usar_item":      "Debo llevarle la ropa a Violet",
            "comprar":        "Debo llevarle la ropa a Violet",
        },
        mensaje_npc_bloqueado="No es el momento.",
        celular_bloqueado=True,
        mensaje_celular="No es el momento.",
        npcs_ocultos=["violet", "monica", "jasmine"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_banioarriba", "violet_quest08a_puerta_baño")

    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ mostrar_hud()
    jump game_loop


# Door access de la puerta del baño: el menú se decide en la puerta (pasillo),
# todavía no se entra. Por eso volvemos a pasillo arriba antes de mostrarlo.
label violet_quest08a_puerta_baño:
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ ocultar_hud()

    $ _bg_pasillo_baño = sistema_locaciones.obtener_locacion("casa_pasilloarriba").background
    scene expression _bg_pasillo_baño

    window show
    piensa "La ropa de Violet... ¿la dejo afuera o llamo?"

    menu:
        "Dejar la ropa afuera":
            jump violet_quest08a_opcion_a
        "Golpear y entrar":
            jump violet_quest08a_entrar_baño


label violet_quest08a_opcion_a:
    piensa "Mejor la dejo aquí y me voy"
    pause 0.3
    violet "¿Ya está?"
    mc "Sí, está afuera de la puerta"
    violet "Gracias"
    piensa "Bien, a seguir con mis cosas"
    jump violet_quest08a_cierre_desarrollo


# Menú del baño: "Acercarse" es una opción especial que requiere 3 de destreza.
# Se muestra siempre; cuando no se cumple el requisito queda en gris (insensitive).
screen vq8a_menu_bano():
    modal True

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Irse":
            style "choice_button"
            action Return("irse")

        textbutton "Acercarse  🎯 (3 de destreza)":
            style "choice_button"
            action Return("acercarse")
            sensitive (getattr(store, 'mc_destreza', 0) >= 3)


label violet_quest08a_entrar_baño:
    scene vq8a_ducha with fade

    window show
    piensa "No se si fue la mejor opcion entrar así"
    piensa "Esta lleno de vapor y no veo bien"
    window hide

    pause 0.5

    window show
    piensa "¿Podría acercarme mas?"

    call screen vq8a_menu_bano

    if _return == "acercarse":
        jump violet_quest08a_baño_acercarse
    else:
        jump violet_quest08a_baño_irse


label violet_quest08a_baño_irse:
    piensa "Mejor me voy, ya tuve suficientes problemas con Violet para buscarme uno nuevo"
    jump violet_quest08a_cierre_desarrollo


label violet_quest08a_baño_acercarse:
    scene vq8a_duchaescena with dissolve
    window show
    piensa "No puedo creer que este haciendo esto, no se desde cuando pero me esta atrayendo mucho Violet"
    piensa "Hasta aquí fue suficiente, si me ve me mata"
    piensa "Mejor me voy"
    jump violet_quest08a_cierre_desarrollo


################################################################################
## CIERRE — Fin del contenido disponible (la quest 09_a está en desarrollo)
################################################################################
## Completa la quest 08_a. La 09_a NO se auto-inicia (su quest_anterior está
## desvinculada temporalmente en quest_violet.rpy); cuando se retome el
## contenido, basta con volver a encadenarla.

label violet_quest08a_cierre_desarrollo:
    window hide

    # Limpiar restricción y acciones de exploración
    $ desactivar_restriccion()
    $ sistema_acciones.acciones.pop("vq8a_ropero", None)
    $ sistema_acciones.acciones.pop("vq8a_cajonera", None)
    $ completar_quest_actual("violet")

    # 1. Adelantar el tiempo 2 veces (queda de noche)
    $ avanzar_horario_multiple(2)

    # 2. Mover al MC a su habitacion
    $ sistema_locaciones.mover_a_locacion("casa_hmc")

    # 3. Restablecer los backgrounds de las locaciones a su estado normal
    python:
        for _loc_id, _bg_orig in dict(vq8a_bgs_originales).items():
            _loc_obj = sistema_locaciones.obtener_locacion(_loc_id)
            if _loc_obj:
                _loc_obj.background_base = _bg_orig
        vq8a_bgs_originales = {}

    $ mostrar_hud()
    jump game_loop


################################################################################
## TESTEO (solo desarrollo) — salta directo al contenido de la quest 08_a
################################################################################
## Disparado por el botón de test en la app de chats. Prepara el estado mínimo
## (quest activa, NPCs fuera, flags limpios) y entra al label violet_quest08a_ver_tv.

label test_quest08a_violet:
    # Cerrar el celular si quedó abierto
    $ renpy.hide_screen("menu_cheats")
    $ renpy.hide_screen("lista_contactos_mensajes")
    $ renpy.hide_screen("menu_celular")
    $ menu_celular_abierto = False

    # Restaurar backgrounds por si un test anterior quedó a medias
    python:
        for _loc_id, _bg_orig in dict(getattr(store, 'vq8a_bgs_originales', {})).items():
            _loc_obj = sistema_locaciones.obtener_locacion(_loc_id)
            if _loc_obj:
                _loc_obj.background_base = _bg_orig
        store.vq8a_bgs_originales = {}

    # Limpiar restricción, acciones y flags de un test previo
    $ desactivar_restriccion()
    $ sistema_acciones.acciones.pop("vq8a_ropero", None)
    $ sistema_acciones.acciones.pop("vq8a_cajonera", None)
    $ vq8a_ropero_visto = False
    $ vq8a_cajonera_vista = False

    # Forzar la 08_a como la ÚNICA quest activa de Violet, en ETAPA_BOTON_LISTO
    # (asi el cierre la completa correctamente con completar_quest_actual("violet"))
    python:
        for _q in sistema_quests.quests.values():
            if _q.npc_id == "violet" and _q.activa and _q.id != "violet_questprincipal_08_a":
                _q.activa = False
        _q08a = sistema_quests.obtener_quest("violet_questprincipal_08_a")
        if _q08a:
            _q08a.completada = False
            _q08a.activa = True
            _q08a.etapa_actual = ETAPA_BOTON_LISTO
            _q08a.dia_inicio = getattr(store, 'dias_totales', 1)

    # Setup de NPCs (replica el despertar) y salto directo al contenido
    $ obtener_npc("violet").locacion_actual  = "fuera"
    $ obtener_npc("monica").locacion_actual  = "fuera"
    $ obtener_npc("jasmine").locacion_actual = "fuera"
    $ actualizar_rutinas_npcs()

    jump violet_quest08a_ver_tv
