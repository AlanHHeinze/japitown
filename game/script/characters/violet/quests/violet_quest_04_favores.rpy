################################################################################
## Violet — ARCO DE LOS FAVORES (quests 04_d3 → 04_d6)
################################################################################
## Lo compartido por las cuatro quests del arco. El contenido de cada una vive
## en su propio archivo (violet_quest_04_d3/d4/d5/d6.rpy).
##
## EL ARCO:
##   d3  Violet pide golosinas   → el MC las consigue y se las da
##   d4  Violet pide pizza       → el MC cocina de noche y le avisa
##   d5  Violet pide limpieza    → el MC limpia living, comedor y cocina
##   d6  Cierre narrativo
## Entre una y otra pasa un dia (dias_espera=1 en cada quest).
##
## EL BOTON NUNCA SE VA. "Preguntarle si necesita algo" aparece mientras
## cualquiera de las cuatro este activa — incluso en ETAPA_ESPERA, donde Violet
## contesta que no necesita nada por hoy. Por eso el boton del menu usa
## violet_favores_quest_activa() y NO quest_lista_para_boton(): ese ultimo exige
## BOTON_LISTO y haria desaparecer el boton durante las esperas.

# =============================================================================
# FLAGS DEL ARCO
# =============================================================================
# Todos `default`: se guardan en la partida y los leen las condiciones de las
# acciones de locacion, la opcion de puerta y los botones del menu.

# d3 — golosinas
default vq4d3_pedido_hecho = False

# d4 — pizza
default vq4d4_pedido_hecho = False
default vq4d4_pizza_cocinada = False

# d5 — limpieza
default vq4d5_pedido_hecho = False
default vq4d5_limpio_living = False
default vq4d5_limpio_comedor = False
default vq4d5_limpio_cocina = False

# Ropa de Violet al entrar a cada label (pijama o ropa base). Se lee una vez por
# escena para no consultar cuerpo_activo() en cada show.
default vq4dfav_cuerpo = "c_rbase"


init python:

    # Horario en el que Violet ya no acepta pedidos: contesta que no necesita
    # nada ahora, sin importar en que punto del arco este.
    VIOLET_FAVORES_HORARIO_NOCHE = 2

    # Quests que usan el boton GENERICO "Preguntarle si necesita algo". Una sola
    # lista para que el helper, el despachador y cualquier chequeo futuro no se
    # desincronicen.
    #
    # La 04_d6 quedo AFUERA a proposito: ahi el MC ya sabe lo que tiene que
    # decir ("terminé de limpiar"), asi que tiene boton propio y preguntarle que
    # necesita no viene al caso. Sin esto aparecerian dos botones que hacen lo
    # mismo. La 04_d2 tampoco entra: tiene el suyo ("¿Puedo hacer algo por vos?").
    VIOLET_FAVORES_QUESTS = [
        "violet_questprincipal_04_d3",
        "violet_questprincipal_04_d4",
        "violet_questprincipal_04_d5",
    ]

    # La cadena COMPLETA, con las dos de boton propio en las puntas. Se usa para
    # lo que vale para todo el arco sin importar como se dispare: el corte de la
    # noche y la opcion de puerta nocturna.
    VIOLET_FAVORES_CADENA = (
        ["violet_questprincipal_04_d2"]
        + VIOLET_FAVORES_QUESTS
        + ["violet_questprincipal_04_d6"]
    )

    def _violet_primera_quest_activa(ids):
        for _qid in ids:
            _q = store.sistema_quests.obtener_quest(_qid)
            if _q and _q.activa and not _q.completada:
                return _q
        return None

    def violet_favores_quest_activa():
        """
        La quest del ARCO DE LOS TRES FAVORES que esta corriendo ahora, o None.

        Como encadenan por quest_anterior, a lo sumo una esta activa a la vez.
        Devuelve la quest ENTERA (no un bool) para que el despachador pueda
        mirar tambien su etapa.
        """
        return _violet_primera_quest_activa(VIOLET_FAVORES_QUESTS)

    def violet_favores_cadena_activa():
        """Idem pero contando la 04_d2. Lo que vale para toda la cadena."""
        return _violet_primera_quest_activa(VIOLET_FAVORES_CADENA)

    def violet_favores_es_de_noche():
        """True si a esta hora Violet ya no acepta pedidos."""
        return store.horario_actual == VIOLET_FAVORES_HORARIO_NOCHE

    def violet_favores_puerta_de_noche():
        """
        Condicion de la opcion de puerta: preguntarle de noche, sin que abra.

        Alcanza con que la quest este ACTIVA — a diferencia del boton del menu,
        que desde ahora pide BOTON_LISTO. Son preguntas distintas: el del menu
        es "¿necesitas algo?" y en ETAPA_ESPERA no tiene sentido, mientras que
        este es "¿me atendes ahora?", y de noche la respuesta es no en cualquier
        punto del arco.
        """
        return (violet_favores_es_de_noche()
                and violet_favores_cadena_activa() is not None)

    # Textos del boton del arco. El de "necesitabas" se usa cuando Violet YA
    # pidio algo: preguntarle si necesita algo cuando ya te lo dijo suena a que
    # el MC no la escucho.
    VIOLET_FAVORES_TXT_PREGUNTAR = "Preguntarle si necesita algo"
    VIOLET_FAVORES_TXT_RECORDAR = "¿Que necesitabas?"

    def violet_favores_boton_texto():
        """
        Texto del boton del arco en el menu de interaccion, o None si en este
        punto NO corresponde mostrarlo.

        Concentra acá las tres reglas del arco en vez de repartirlas en
        condiciones sueltas en interactions_violet.rpy:

        Durante los dias de ESPERA no hay boton. Antes salia y Violet contestaba
        que hoy no necesitaba nada, pero eso es un callejon sin salida: el
        jugador ya sabe que tiene que esperar porque ella misma se lo dijo, y el
        boton solo servia para que se lo repitiera. Vuelve a aparecer el dia que
        la quest queda lista. Es el mismo criterio que el boton propio de la d2.

        d3: antes del pedido va "Preguntarle si necesita algo"; despues,
            "¿Que necesitabas?".
        d4: igual que la d3, PERO una vez cocinada la pizza el boton
            desaparece: lo unico que queda es avisarle por la puerta, y tener
            tambien el generico seria ofrecer dos caminos para lo mismo.
        d5: antes del pedido NO hay boton — esta quest la arranca ella
            buscandote, no vos preguntandole. Despues, "¿Que necesitabas?".

        La d2 y la d6 no pasan por acá: tienen boton propio.
        """
        _q_txt = violet_favores_quest_activa()
        if _q_txt is None:
            return None

        # Solo con la quest LISTA: en ETAPA_ESPERA no hay nada que preguntarle.
        if _q_txt.etapa_actual != ETAPA_BOTON_LISTO:
            return None

        if _q_txt.id == "violet_questprincipal_04_d3":
            return (VIOLET_FAVORES_TXT_RECORDAR
                    if getattr(store, 'vq4d3_pedido_hecho', False)
                    else VIOLET_FAVORES_TXT_PREGUNTAR)

        if _q_txt.id == "violet_questprincipal_04_d4":
            if getattr(store, 'vq4d4_pizza_cocinada', False):
                return None
            return (VIOLET_FAVORES_TXT_RECORDAR
                    if getattr(store, 'vq4d4_pedido_hecho', False)
                    else VIOLET_FAVORES_TXT_PREGUNTAR)

        if _q_txt.id == "violet_questprincipal_04_d5":
            return (VIOLET_FAVORES_TXT_RECORDAR
                    if getattr(store, 'vq4d5_pedido_hecho', False)
                    else None)

        return None

    def violet_favores_limpiezas_hechas():
        """Cuantos de los 3 lugares de la d5 ya estan limpios (0-3)."""
        return sum([
            1 if getattr(store, 'vq4d5_limpio_living', False) else 0,
            1 if getattr(store, 'vq4d5_limpio_comedor', False) else 0,
            1 if getattr(store, 'vq4d5_limpio_cocina', False) else 0,
        ])


################################################################################
## DESPACHADOR — a donde lleva "Preguntarle si necesita algo"
################################################################################
## Todo el ruteo del arco vive aca. El menu de interaccion apunta siempre a este
## label y este decide; asi interactions_violet.rpy queda con una sola entrada
## en vez de una condicion por etapa.

label violet_favores_boton:

    # De noche no acepta pedidos, sin importar en que punto del arco estemos.
    # Va antes que todo lo demas: ni siquiera se evalua la etapa.
    if violet_favores_es_de_noche():
        jump violet_q4dfav_de_noche

    python:
        _q_fav = violet_favores_quest_activa()
        # Red de seguridad. Con el boton mostrandose solo en ETAPA_BOTON_LISTO
        # (ver violet_favores_boton_texto) no deberia caer nunca acá, pero el
        # despachador necesita SIEMPRE un destino: un jump a None crashea.
        _fav_destino = "violet_q4d_nada_por_hoy"

        if _q_fav is not None and quest_lista_para_boton(_q_fav.id):
            if _q_fav.id == "violet_questprincipal_04_d3":
                _fav_destino = ("violet_q4d3_recordatorio"
                                if store.vq4d3_pedido_hecho
                                else "violet_q4d3_pedido")
            elif _q_fav.id == "violet_questprincipal_04_d4":
                _fav_destino = ("violet_q4d4_recordatorio"
                                if store.vq4d4_pedido_hecho
                                else "violet_q4d4_pedido")
            elif _q_fav.id == "violet_questprincipal_04_d5":
                _fav_destino = ("violet_q4d5_recordatorio"
                                if store.vq4d5_pedido_hecho
                                else "violet_q4d5_pedido")
            # La 04_d6 no se rutea acá: tiene boton propio ("Ya terminé de
            # limpiar") y ni siquiera esta en VIOLET_FAVORES_QUESTS.

    jump expression _fav_destino


################################################################################
## DE NOCHE — desde el MENU, con los dos personajes en escena
################################################################################
## Vale para toda la cadena (04_d2 → 04_d6). Se juega en la locacion y el
## horario actuales.
##
## El layered de Violet sale de cuerpo_activo("violet"), que devuelve "c_pijama"
## o "c_rbase" segun el grupo de rutina activo — o sea segun donde este y a que
## hora. De noche en su habitacion va a estar en pijama, pero si esta abajo
## puede no estarlo, asi que la rama decide sola.

label violet_q4dfav_de_noche:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # =========================================================================
    # CONTENIDO — Violet responde que no necesita nada ahora
    # =========================================================================

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## DE NOCHE — desde la PUERTA, solo la respuesta
################################################################################
## Violet contesta desde adentro: no cambia el fondo ni muestra sprites, se
## queda el pasillo como estaba. Mismo recurso que usa la apertura de
## violet_quest05c_puerta antes de que ella abra.

label violet_q4dfav_de_noche_puerta:

    $ ocultar_hud()
    window show

    # =========================================================================
    # CONTENIDO — solo la voz de Violet: no necesita nada ahora
    # =========================================================================

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## NADA POR HOY — durante las esperas de un dia entre favor y favor
################################################################################

label violet_q4d_nada_por_hoy:

    $ vq4dfav_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    if vq4dfav_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # =========================================================================
    # CONTENIDO — Violet le dice que hoy no necesita nada
    # =========================================================================

    window hide
    $ mostrar_hud()
    jump game_loop
