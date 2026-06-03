################################################################################
## Violet Evento 03 — Limpieza del Sábado
################################################################################
## Narrativa del evento de limpieza sábado de Violet
## Se dispara desde el door access de la habitación de Violet (sábado mañana)
## Disponible luego de completar la quest 03_a

# =============================================================================
# IMAGENES
# =============================================================================
image quest2_violet_puertahabitacion = "images/quest/violet/quest1/quest01_violet_puertahabitacion.png"
image quest2_violet_pasilloarriba_mañana = "images/quest/violet/quest1/quest01_violet_pasilloarriba_mañana.png"
image quest2_violet_living_mañana = "images/bg/casa/bg_casa_mañana_living.png"

image quest2_violet_limpiando_chimenea = "images/quest/violet/quest1/violet_quest01_limpiando_chimenea.png"
image quest2_violet_limpiando_escalera = "images/quest/violet/quest1/violet_quest01_limpiando_escalera.png"
image quest2_violet_limpiando_sillon   = "images/quest/violet/quest1/violet_quest01_limpiando_sillon.png"
image quest2_violet_limpiando_alacena = "images/quest/violet/quest1/violet_quest01_limpiando_alacena.png"

image quest2_violet_violetbarriendo = "images/quest/violet/quest1/violet_quest01_violetbarriendo.png"

image quest2_violet_baño1 = "images/quest/violet/quest1/quest01_violet_baño1.png"
image bg_casa_mañana_banioarriba_zoom = "images/quest/violet/quest1/bg_casa_mañana_banioarribazoom.png"

image quest2_violet_limpiandopasilloarriba = "images/quest/violet/quest1/violet_quest01_limpiandopasilloarriba.png"


# =============================================================================
# SCREEN — Menú de 3 opciones con bloqueo por stats
# =============================================================================

screen menu_quest2_violet_opciones():
    style_prefix "choice"

    vbox:
        # Opción A — siempre disponible
        textbutton "En qué me estoy acostumbrando a volver a vivir acá" action Return("a")

        # Opción B — requiere amor >= 10
        if violet_amor >= 10:
            textbutton "Me acordaba cuando inventábamos excusas para no ordenar y Monica se enojaba" action Return("b")
        else:
            textbutton "Me acordaba cuando inventabamos excusas para no ordenar y Monica se enojaba":
                action None
                sensitive False
                text_color "#666666"
                text_hover_color "#666666"

        # Opción C — requiere deseo >= 10
        if violet_deseo >= 10:
            textbutton "Pensaba en que te queda muy sexy ese pijama" action Return("c")
        else:
            textbutton "Pensaba en que te queda muy sexy ese pijama":
                action None
                sensitive False
                text_color "#666666"
                text_hover_color "#666666"


################################################################################
## LABEL PRINCIPAL — Evento 03 Limpieza del Sábado
################################################################################

label evento03_violet:

    # Ocultar HUD durante el evento
    $ ocultar_hud()
    window show

    # =====================================================================
    # Introduccion: MC toca la puerta de Violet
    # =====================================================================

    scene quest2_violet_puertahabitacion with fade

    # Mostrar MC
    show mc_espalda_base brazoscruzados at mc_cerca:
        xzoom -1.0

    # Mc Piensa
    piensa "Seguro se quedó jugando hasta tarde, va a costar levantarla"

    # Mc Toca la puerta
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    show mc_espalda_base golpeandoruido with sprite_normal
    "Toc Toc Toc"
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    show mc_espalda_base golpeandoruido with sprite_normal
    "Toc Toc Toc"
    pause 0.5

    # Mc piensa
    piensa "Me lo supuse"

    # Mc Toca la puerta
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    show mc_espalda_base golpeandoruido with sprite_normal
    "TOC TOC TOC"
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    show mc_espalda_base golpeandoruido with sprite_normal
    "TOC TOC TOC"
    pause 0.5

    # Violet habla
    violet "¿Mmm?"

    # MC habla
    show mc_espalda_base brazoscruzados
    mc "Violet, Monica pidio que nos ocupemos hoy de la limpieza, mientras ella estaba fuera con Jasmine."

    # MC habla
    piensa "¿Se volvio a dormir?"
    show mc_espalda_base rascarse1
    pause 0.3
    show mc_espalda_base rascarse2
    pause 0.3
    show mc_espalda_base rascarse1
    pause 1.0

    # Mc Toca la puerta
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    show mc_espalda_base golpeandoruido with sprite_normal
    "TOC TOC TOC"
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    show mc_espalda_base golpeandoruido with sprite_normal
    "TOC TOC TOC"
    pause 0.5
    mc "DESPERTATEEEEE"

    # Violet habla
    violet "¿Que pasa?"

    # MC habla
    mc "Vamos... tenemos que limpiar"

    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Varios intentos más tarde{/color}"
    pause 1.0

    # =========================================================================
    # ESCENA 1: Pasillo (Violet recien despierta)
    # =========================================================================

    scene quest2_violet_pasilloarriba_mañana with fade

    # Mostrar personajes
    show violet_parada c_pijama_agotada o_dormidos b_aburrida ca_pijama at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    # Violet habla
    show violet_parada b_hablandochica c_pijama_bostezo1 with sprite_normal
    violet "..."
    show violet_parada b_hablando c_pijama_bostezo2 with sprite_normal
    pause 0.5
    show violet_parada b_none c_pijama_agotada with sprite_normal


    # MC habla
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Planeta tierra a Violet, planeta tierra a Violet."
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica
    violet "¿Que pasa?"
    show violet_parada b_none

    # MC habla
    show mc_parado_base b_hablando
    mc "Hay que ponerse a limpiar un poco la casa"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Encargáte de limpiar el pasillo y el baño, yo voy a hacer el living y la cocina"
    show mc_parado_base b_none
    pause 0.3

    # Violet habla
    show violet_parada b_hablandochica c_pijama_bostezo1 with sprite_normal
    violet "Ahhhh... Esta bien"
    show violet_parada b_hablando
    pause 0.3
    show violet_parada b_none c_pijama_agotada with sprite_normal

    # MC habla
    show mc_parado_base b_hablando
    mc "¿Necesitas algo?"
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica c_pijama_brazoscruzados with sprite_normal
    violet "Dormir..."
    show violet_parada b_none

    # MC habla
    show mc_parado_base b_hablando
    mc "Cuánto antes terminemos, antes te podés dormir"
    show mc_parado_base b_none

    # MC habla
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Comencemos"
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica c_pijama_base with sprite_normal
    violet "Ok..."
    show violet_parada b_none

    # =========================================================================
    # ESCENA 2: Activar restricción — Solo se puede ir al living
    # =========================================================================

    # Resetear estado de elementos de limpieza
    $ vq2_chimenea_pendiente = True
    $ vq2_escalera_pendiente = True
    $ vq2_sillon_pendiente   = True
    $ vq2_texto_inicial_mostrado = False

    # Activar restricción: solo living permitido
    $ activar_restriccion(
        locaciones_permitidas=["casa_living"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Debo encargarme de limpiar la planta baja"),
        mensajes_acciones={
            "avanzar_tiempo": _("No debo perder el tiempo"),
            "dormir":         _("No debo perder el tiempo"),
            "entrenar":       _("No debo perder el tiempo"),
            "trabajar":       _("No debo perder el tiempo"),
            "usar_item":      _("No debo perder el tiempo"),
            "comprar":        _("No debo perder el tiempo"),
        },
        mensaje_npc_bloqueado=_("No tengo tiempo para eso ahora"),
        celular_bloqueado=True,
        mensaje_celular=_("No debo perder el tiempo"),
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para cuando el jugador entre al living
    $ restriccion_quest_activa.registrar_label_locacion("casa_living", "violet_quest2_living_interactivo")

    # Mostrar HUD para que el jugador pueda moverse
    window hide
    $ mostrar_hud()

    # Mover al jugador al pasillo arriba (donde termina la escena narrativa)
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    jump game_loop


################################################################################
## LABEL: Jugador entra al living — Screen de limpieza
################################################################################

label violet_quest2_living_interactivo:

    # Ocultar HUD, mostrar fondo del living
    $ ocultar_hud()
    window show

    scene quest2_violet_living_mañana with fade

    # Texto inicial del MC
    piensa "Bueno, a limpiar"

    # Marcar que se mostró el texto inicial
    $ vq2_texto_inicial_mostrado = True

    # Loop del screen de limpieza
    label .loop_limpieza:

        # Mostrar screen y esperar interacción
        $ _elemento_elegido = renpy.call_screen("limpieza_quest2_violet")

        if _elemento_elegido == "chimenea":
            scene quest2_violet_limpiando_chimenea with fade
            piensa "No se por que me puse a limpiar esto..."
            $ vq2_chimenea_pendiente = False
            scene quest2_violet_living_mañana with fade

        elif _elemento_elegido == "escalera":
            scene quest2_violet_limpiando_escalera with fade
            piensa "Espero que Raquel vuelva pronto"
            $ vq2_escalera_pendiente = False
            scene quest2_violet_living_mañana with fade

        elif _elemento_elegido == "sillon":
            scene quest2_violet_limpiando_sillon with fade
            piensa "Violet debería tener un poco más de cuidado cuando come acá"
            $ vq2_sillon_pendiente = False
            scene quest2_violet_living_mañana with fade

        # Verificar si quedan elementos
        if vq2_chimenea_pendiente or vq2_escalera_pendiente or vq2_sillon_pendiente:
            jump .loop_limpieza

    # =========================================================================
    # Limpieza terminada — Activar restricción 2: solo pasillo arriba
    # =========================================================================

    piensa "Listo el living. Voy a ver como va Violet."

    # Actualizar restricción: ahora solo puede ir al pasillo arriba
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Debo ir a ver como va Violet con la limpieza"),
        mensajes_acciones={
            "avanzar_tiempo": _("No puedo perder tiempo con esto"),
            "dormir":         _("No puedo perder tiempo con esto"),
            "entrenar":       _("No puedo perder tiempo con esto"),
            "trabajar":       _("No puedo perder tiempo con esto"),
            "usar_item":      _("No puedo perder tiempo con esto"),
            "comprar":        _("No puedo perder tiempo con esto"),
        },
        mensaje_npc_bloqueado=_("No tengo tiempo para eso ahora"),
        celular_bloqueado=True,
        mensaje_celular=_("No puedo perder tiempo con esto"),
        npcs_ocultos=["monica", "jasmine", "violet"],
        # Sprite de Violet barriendo como elemento de escena en el pasillo
        elementos_escena=[
            {
                "locacion": "casa_pasilloarriba",
                "tipo": "imagebutton",
                "id": "violet_barriendo",
                "imagen": "images/quest/violet/quest1/violet_quest01_violetbarriendo.png",
                "pos": vq2_pos_violet_barriendo,
                "anchor": (0.5, 1.0),
                "label": "violet_quest2_escena_pasillo",
            }
        ],
    )

    # Registrar label para cuando el jugador entre al pasillo arriba
    $ restriccion_quest_activa.registrar_label_locacion("casa_pasilloarriba", "violet_quest2_pasillo_interactivo")

    # Mover al jugador al living (donde terminó la limpieza)
    $ sistema_locaciones.mover_a_locacion("casa_living")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LABEL: Jugador entra al pasillo arriba — Violet barriendo
################################################################################

label violet_quest2_pasillo_interactivo:
    return


################################################################################
## LABEL: Escena del pasillo — Violet barriendo
################################################################################

label violet_quest2_escena_pasillo:

    $ ocultar_hud()
    window show

    scene quest2_violet_pasilloarriba_mañana with fade

    # Mostrar personajes
    show violet_parada c_pijama_escoba ca_pijama o_dormidos b_aburrida at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    # MC habla
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "¿Todavía estás barriendo?"
    show mc_parado_base b_none
    pause 0.3

    # Violet habla
    show violet_parada b_hablandochica c_pijama_escoba o_base with sprite_normal
    violet "Recién empezamos a limpiar"
    show violet_parada b_none
    pause 0.3

    # MC habla
    show mc_parado_base b_hablando
    mc "No, empezamos hace una hora..."
    show mc_parado_base b_none
    pause 0.3

    # Violet habla
    show violet_parada b_hablandochica
    violet "Fueron 5 minutos"
    show violet_parada b_none
    pause 0.3

    # MC piensa
    piensa "¿Se quedó dormida?"
    piensa "Se quedó dormida"

    # MC habla
    show mc_parado_base b_hablando
    mc "¿Te quedaste dormida barriendo?"
    show mc_parado_base b_none
    pause 0.3

    # Violet habla
    show violet_parada b_hablandochica
    violet "¿Como me voy a quedar dormida barriendo?"
    show violet_parada b_none
    pause 0.3

    # MC habla
    show mc_parado_base b_hablando
    mc "Hay que apurarnos Violet, tenemos que terminar antes que vuelvan las chicas"
    show mc_parado_base b_none
    pause 0.3

    # Violet habla
    show violet_parada b_hablandochica o_tristes
    violet "Perdon"
    show violet_parada b_none
    pause 0.3

    # MC piensa
    piensa "Por lo menos dormida tiene buen carácter"

    # MC habla
    show mc_parado_base b_hablando
    mc "Te voy a ayudar, yo sigo aca arriba, voy a buscar algo para limpiar"
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica
    violet "Si... gracias [mc_name]"
    show violet_parada b_none

    # MC piensa
    piensa "Voy a ir a la cocina a buscar un trapeador"

    # =========================================================================
    # Activar restricción: navegar a la cocina para buscar trapeador
    # =========================================================================

    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_living", "casa_pasilloabajo", "casa_cocina"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Debo buscar algo para limpiar"),
        mensajes_acciones={
            "avanzar_tiempo": _("No puedo perder tiempo con esto"),
            "dormir":         _("No puedo perder tiempo con esto"),
            "entrenar":       _("No puedo perder tiempo con esto"),
            "trabajar":       _("No puedo perder tiempo con esto"),
            "usar_item":      _("No puedo perder tiempo con esto"),
            "comprar":        _("No puedo perder tiempo con esto"),
        },
        mensaje_npc_bloqueado=_("No tengo tiempo para eso ahora"),
        celular_bloqueado=True,
        mensaje_celular=_("No puedo perder tiempo con esto"),
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para cuando el jugador entre a la cocina
    $ restriccion_quest_activa.registrar_label_locacion("casa_cocina", "violet_quest2_cocina_interactivo")

    # Mover al jugador al pasillo arriba (donde está)
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LABEL: Jugador entra a la cocina — Buscar trapeador
################################################################################

label violet_quest2_cocina_interactivo:

    $ ocultar_hud()
    window show

    scene bg_casa_mañana_cocina with fade

    piensa "Alguno de estos muebles debe tener un trapeador"

    # Loop del screen de búsqueda
    label .loop_busqueda:

        # Mostrar screen y esperar interacción
        $ _elemento_cocina = renpy.call_screen("buscar_trapeador_quest2_violet")

        if _elemento_cocina == "alacena":
            piensa "Aca esta"
        else:
            piensa "Alguno de estos muebles debe tener un trapeador"
            jump .loop_busqueda

    # =========================================================================
    # Trapeador encontrado — Restricción: solo pasillo arriba
    # =========================================================================

    $ activar_restriccion(
        locaciones_permitidas=["casa_cocina", "casa_pasilloabajo", "casa_living", "casa_pasilloarriba"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Debo volver arriba a limpiar"),
        mensajes_acciones={
            "avanzar_tiempo": _("No puedo perder tiempo con esto"),
            "dormir":         _("No puedo perder tiempo con esto"),
            "entrenar":       _("No puedo perder tiempo con esto"),
            "trabajar":       _("No puedo perder tiempo con esto"),
            "usar_item":      _("No puedo perder tiempo con esto"),
            "comprar":        _("No puedo perder tiempo con esto"),
        },
        mensaje_npc_bloqueado=_("No tengo tiempo para eso ahora"),
        celular_bloqueado=True,
        mensaje_celular=_("No puedo perder tiempo con esto"),
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para cuando el jugador llegue al pasillo arriba
    $ restriccion_quest_activa.registrar_label_locacion("casa_pasilloarriba", "violet_quest2_limpieza_pasillo")

    # Mover al jugador a la cocina (donde está)
    $ sistema_locaciones.mover_a_locacion("casa_cocina")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LABEL: Jugador llega al pasillo arriba — Transición limpieza
################################################################################

label violet_quest2_limpieza_pasillo:

    $ ocultar_hud()
    window show

    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Una limpieza más tarde{/color}"
    pause 1.0

    scene quest2_violet_limpiandopasilloarriba with fade

    piensa "Estoy agotado ya, Violet debería haber terminado"
    piensa "Voy a ver como esta"


################################################################################
## LABEL: Post-menú — Activar restricción 3: solo baño arriba
################################################################################

label violet_quest2_post_menu:

    # Activar restricción 3: solo baño arriba
    $ activar_restriccion(
        locaciones_permitidas=["casa_banioarriba"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Debo ver como va Violet con el baño"),
        mensajes_acciones={
            "avanzar_tiempo": _("No puedo perder tiempo con esto"),
            "dormir":         _("No puedo perder tiempo con esto"),
            "entrenar":       _("No puedo perder tiempo con esto"),
            "trabajar":       _("No puedo perder tiempo con esto"),
            "usar_item":      _("No puedo perder tiempo con esto"),
            "comprar":        _("No puedo perder tiempo con esto"),
        },
        mensaje_npc_bloqueado=_("No tengo tiempo para eso ahora"),
        celular_bloqueado=True,
        mensaje_celular=_("No puedo perder tiempo con esto"),
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para cuando el jugador entre al baño arriba
    $ restriccion_quest_activa.registrar_label_locacion("casa_banioarriba", "violet_quest2_banio_interactivo")

    # Mover al jugador al pasillo arriba (donde termina la escena del pasillo)
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LABEL: Jugador entra al baño arriba — Escena final
################################################################################

label violet_quest2_banio_interactivo:

    $ ocultar_hud()
    window show

    jump violet_quest2_escena_banio


################################################################################
## LABEL: Escena del baño
################################################################################

label violet_quest2_escena_banio:

    scene quest2_violet_baño1

    mc "¿Violet?"
    violet "¿Si?"
    mc "¿Qué hacés?"
    violet "Estoy limpiando el baño"
    mc "¿Está limpiando la alfombra del baño con un trapo?"
    violet "Estoy secando, se me cayó agua"
    piensa "Tiene medio trasero al aire..."
    violet "¿Necesitas algo?"
    piensa "Tengo que dejar de mirarla o va a ser un problema"
    mc "No, ya terminé y quería ver cómo estaba"
    violet "Yo también, ayudame a pararme"
    mc "Ok"

    scene bg_casa_mañana_banioarriba_zoom

    show violet_parada c_pijama_agotada o_base ca_pijama at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    # Violet habla
    show violet_parada b_hablandochica
    violet "Gracias [mc_name]"
    show violet_parada b_sonrisapequeña

    # Mc piensa
    piensa "Es raro verla con este carácter"
    piensa "Podría aprovechar para mejorar un poco la relación"

    # Violet habla
    show violet_parada b_hablandochica o_arribanm
    violet "¿Pasa algo?"
    show violet_parada b_none o_base

    # Mc habla
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "No, ¿Por qué?"
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica c_pijama_brazoscruzados with sprite_normal
    violet "Me estas mirando sin decir nada"
    show violet_parada b_sonrisapequeña

    # Mc piensa
    piensa "Mierda, ¿Se dio cuenta de que la estaba mirando cuando estaba agachada?"
    piensa "Tengo que decir algo"

    # Mc habla
    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Estaba mirando como limpiabas"
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica o_enojados
    violet "Ahora digo..."
    show violet_parada b_none o_base

    # Mc Habla
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Ahh... Me tildé pensando"
    show mc_parado_base b_none

    # Violet habla
    show violet_parada b_hablandochica o_arribanm
    violet "¿En que?"
    show violet_parada b_sonrisapequeña o_base

    # =====================================================================
    # MENÚ DE 3 OPCIONES (con bloqueo por stats)
    # =====================================================================

    $ _resultado_menu = renpy.call_screen("menu_quest2_violet_opciones")

    if _resultado_menu == "a":
        jump violet_quest2_opcion_a
    elif _resultado_menu == "b":
        jump violet_quest2_opcion_b
    elif _resultado_menu == "c":
        jump violet_quest2_opcion_c

    jump violet_quest2_cierre


################################################################################
## RAMA A
################################################################################

label violet_quest2_opcion_a:

    show violet_parada b_hablandochica
    violet "Yo espero acostumbrarme tambien"
    show violet_parada b_sonrisapequeña

    show mc_parado_base b_hablando
    mc "¿A que yo este aca?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Si..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No seas mala, sabes que nos podemos llevar bien si colaboras"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_enojados
    violet "¿Colaborar yo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí vos, ignorándome cada vez que tenés la oportunidad"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Yo pienso que tendrías que colaborar vos en remediar todo el tiempo que desapareciste"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sabes que no pude decidir"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "Pero si te podías comunicar y no lo hiciste, no respondiste mas mensajes ni nada"
    show violet_parada b_none o_base
    pause 0.3
    show violet_parada b_hablandochica o_arribanm
    violet "Y ahora venís en rol de víctima esperando que todos digamos pobrecito [mc_name]"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando
    mc "No es asi"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "Bueno eso parece..."
    show violet_parada b_none o_base

    show mc_parado_base b_hablando
    mc "Entiendo el punto y voy a tratar de que cambies de parecer"
    show mc_parado_base b_none

    "Ruidos en la puerta"

    show mc_parado_base b_hablando
    mc "Parece que volvieron las chicas con las compras"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Voy a ayudarla a entrar las cosas"
    show mc_parado_base b_none

    hide mc_parado_base with dissolve

    show violet_parada b_hablandochica
    violet "Otra vez escapando"
    show violet_parada b_none

    $ vq4_rama_elegida = "a"

    jump violet_quest2_cierre


################################################################################
## RAMA B
################################################################################

label violet_quest2_opcion_b:

    show violet_parada b_hablandochica
    violet "Siempre nos estaba regañando para que hagamos las cosas"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Si o para que nos fueramos a dormir"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "O para que no gritemos jugando video juegos jajaja"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "O para que te bañes jajaja"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Si o para que te bañes"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_enojados
    violet "Yo no tenia problemas con bañarme"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Yo recuerdo otra cosa"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Tenes los recuerdos un poco alterados"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No, en todos mis recuerdos nos llevabamos muy bien"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "..."
    show violet_parada b_none

    "Ruidos en la puerta"

    show mc_parado_base b_hablando
    mc "Parece que volvieron las chicas con las compras"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Voy a ayudarla a entrar las cosas"
    show mc_parado_base b_none

    hide mc_parado_base with dissolve

    show violet_parada b_hablandochica
    violet "Yo tambien"
    show violet_parada b_none

    $ vq4_rama_elegida = "b"

    jump violet_quest2_cierre


################################################################################
## RAMA C
################################################################################

label violet_quest2_opcion_c:

    $ violet_quest2_trajesexy = True

    show violet_parada b_hablandochica
    violet "¿Que dijiste?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Jajajaja mala mia"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Pero es la verdad"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_enojados
    violet "¿Ahora te volviste una especie de pervertido?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Es tu culpa..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_enojados
    violet "¿Mi culpa?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No te tapa ni la mitad del trasero"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Y sabes que siempre fue mi parte favorita"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_enojados
    violet "No lo hice a propósito, si me queda bien arriba me queda chico abajo"
    show violet_parada b_none
    pause 0.3
    show violet_parada b_hablando
    violet "No tengo la culpa de mi cuerpo desproporcionado"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "A mí me parece perfecto"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Poco arriba y mucho abajo"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Por que terminamos hablando de esto?"
    show violet_parada b_none
    pause 0.3
    show violet_parada b_hablando
    violet "Ahh si por que sos un pervertido"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Tengo mis debilidades"
    show mc_parado_base b_none

    "Ruidos en la puerta"

    show mc_parado_base b_hablando
    mc "Parece que volvieron las chicas con las compras"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Voy a ayudarla a entrar las cosas"
    show mc_parado_base b_none

    hide mc_parado_base with dissolve

    show violet_parada b_hablandochica
    violet "¿Debilidades...?"
    show violet_parada b_none

    $ vq4_rama_elegida = "c"

    jump violet_quest2_cierre


################################################################################
## CIERRE COMÚN — Todas las ramas convergen aquí
################################################################################

label violet_quest2_cierre:

    # Evaluar ruta elegida y aplicar stats
    if vq4_rama_elegida == "a":
        $ obtener_npc("violet").modificar_stat1(5)
    elif vq4_rama_elegida == "b":
        $ obtener_npc("violet").modificar_stat2(5)
    elif vq4_rama_elegida == "c":
        $ obtener_npc("violet").modificar_stat2(5)

    # Desactivar restricción
    $ desactivar_restriccion()

    # Completar el evento
    $ _ev03 = obtener_event("violet_evento_03")
    if _ev03:
        $ _ev03.completar()
    $ store.violet_limpieza_completada = True

    # Restaurar HUD
    window hide
    $ mostrar_hud()

    # Volver al loop principal
    jump game_loop
