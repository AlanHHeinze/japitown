################################################################################
## Quest 04_d4 — La pizza (favor 2 de 3)
################################################################################
## Violet quiere volver a cenar pizza. El MC cocina de noche y despues le avisa
## en la puerta de su habitación.
##
## Recorrido:
##   1. "Preguntarle si necesita algo"  → _pedido     (prende vq4d4_pedido_hecho)
##   2. mismo boton, antes de cocinar   → _recordatorio
##   3. accion "Cocinar" en la cocina, SOLO de noche → _cocinar
##      (prende vq4d4_pizza_cocinada y avanza el horario)
##   4. opcion de puerta "Ya está la comida" → _avisar (completa la quest)
##
## La accion de cocinar NO agrega un boton propio: es un ListenerAccion sobre la
## accion generica "cocinar" (registrado en actions_catalog.rpy), igual que en la
## quest 0_b. Con una accion aparte quedaban DOS botones de Cocinar en la cocina.
##
## El "ya cocinaste hoy" no molesta: el ejecutor mira los listeners ANTES que el
## bloqueo por accion usada. A diferencia de la 0_b, el listener se registra en
## init y se apaga por flag, no en runtime — un registro en runtime se pierde al
## cargar la partida.
##
## LOS DIALOGOS ESTAN VACIOS A PROPOSITO: los escribe Alan.


################################################################################
## PEDIDO — Violet dice que quiere pizza
################################################################################

label violet_q4d4_pedido:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica o_arribanm c_rbase_pensando with sprite_normal
    violet "¿Y ahora qué podría querer?"
    show violet_parada b_hablando
    violet "Mmmm..."
    show violet_parada b_none

    piensa "Me preocupa un poco esa actitud"

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Si no quieres nada, no hay problema..."
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica o_base c_rbase_base with sprite_normal
    violet "Quiero cenar pizzas"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Podríamos pedir a la noche entonces"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_idea with sprite_normal
    violet "No, quiero que las hagas tú"
    show violet_parada b_hablando
    violet "La otra vez te salieron muy ricas"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Ok... está bien, hago pizzas para cenar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Avísame cuando estén listas"
    show violet_parada b_none

    # Desde acá aparece la acción Cocinar de la quest en la cocina, de noche.
    $ vq4d4_pedido_hecho = True

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## RECORDATORIO — vuelve a preguntar y Violet le recuerda la pizza
################################################################################

label violet_q4d4_recordatorio:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablando
    violet "Todavía estoy esperando las pizzas"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, ya me acuerdo, no te preocupes"
    show mc_parado_base b_none

    hide violet_parada

    piensa "Voy a tener que ocuparme de eso"

    # =========================================================================
    # CONTENIDO — "te pedí pizza" / "la hago esta noche"
    # =========================================================================

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## COCINAR — secuencia de la pizza, sin textos
################################################################################
## Las imágenes son las mismas de la quest 0_b y están definidas allá
## (violet_quest_0_b.rpy) como `image` globales — no hay que redefinirlas.
## Acá van sin `piensa`, solo la secuencia.

label violet_q4d4_cocinar:

    $ ocultar_hud()
    window hide

    scene bg_casa_noche_cocina with fade

    show quest0_violet_heladera with sprite_normal
    pause 1.0
    show quest0_violet_amasando with sprite_normal
    pause 1.0
    show quest0_violet_poniendopizza with sprite_normal
    pause 1.0
    show quest0_violet_esperando with sprite_normal
    pause 1.0
    show quest0_violet_sacandopizza with sprite_normal
    pause 1.0
    show quest0_violet_pizzalista with sprite_normal
    pause 1.0

    # =========================================================================
    # CONTENIDO OPCIONAL — si querés un pensamiento al final, va acá
    # =========================================================================

    $ vq4d4_pizza_cocinada = True

    piensa "Listo, espero que con esto quede satisfecha"
    piensa "Si la veo de buen humor podría preguntarle por las otras fotos"

    # La pizza esta lista: hasta avisarle a Violet no se hace otra cosa. El
    # tiempo queda frenado y el recorrido acotado al camino cocina → su puerta.
    #
    # casa_cocina NO va en la lista a proposito: el MC arranca ahi (la
    # restriccion solo filtra el DESTINO de un movimiento, no donde estas), y
    # la cocina conecta directo con casa_pasilloabajo, asi que puede salir pero
    # no volver. Es el mismo recorte que usa el cierre de la quest 0_b.
    #
    # Los dos mensajes son los MISMOS que usa la 0_b en esta misma situacion:
    # ya estan registrados en core/quests/quest_strings.rpy y traducidos.
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloabajo", "casa_living", "casa_pasilloarriba", "casa_hviolet"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Debo avisarle a Violet que esta la comida"),
        mensajes_acciones={
            "avanzar_tiempo": _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "dormir":         _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "entrenar":       _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "trabajar":       _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "usar_item":      _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "comprar":        _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "cocinar":        _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
            "ver_tv":         _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
        },
    )

    $ mostrar_hud()
    jump game_loop


################################################################################
## AVISAR — opción de puerta "Ya está la comida", la charla pasa en el pasillo
################################################################################

label violet_q4d4_avisar:

    # Se llega acá por la opcion de puerta "Ya está la comida". Levantar la
    # restriccion es lo PRIMERO: si la escena se cortara mas adelante, el
    # jugador quedaria encerrado en el recorrido de la pizza para siempre.
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    # =========================================================================
    # CONTENIDO — el MC golpea y avisa desde afuera (Violet todavía no salió)
    # =========================================================================

    $ _loc_pasillo = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _bg_pasillo = _loc_pasillo.background if _loc_pasillo else "#1a1a1a"
    scene expression _bg_pasillo with fade


    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablando
    violet "¿Qué pasa?"
    show violet_parada b_hablandochica o_base
    violet "¿Ya están las pizzas?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, ya están listas, me pediste que venga a avisarte"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Bueno ahora bajo"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "¿Nada más?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_pijama_pensando with sprite_normal
    violet "¿Nada más de qué?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "No sé, me hiciste subir a avisarte..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_juzgandonm
    violet "¿Estabas esperando algo más?"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Emmm... no"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_pijama_base with sprite_normal
    violet "Ahhh, bueno, entonces bajo a comer"
    show violet_parada b_hablando
    violet "Nos vemos luego, [mc_name]"
    show violet_parada b_none o_guiñando
    pause 0.3
    show violet_parada o_base


    hide violet_parada

    piensa "Empiezo a tener sospechas de que sabe lo que estoy esperando y se está abusando"
    piensa "No creo que me lo muestre, ya hice suficiente esfuerzo, hay que saber cuándo rendirse"

    # Al completar arranca sola la 04_d5, que espera un día antes de habilitarse.
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_d4")

    window hide
    $ mostrar_hud()
    jump game_loop
