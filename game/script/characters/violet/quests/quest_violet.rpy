################################################################################
## Quests de Violet
################################################################################
## Archivo principal con definiciones de quest
## Los labels de cada quest estan en archivos separados (violet_quest_X.rpy)

init 5 python:

    def vq_esperar_texto(quest_id, total_dias):
        """Texto dinámico de cuenta regresiva para una etapa de espera.
        Calcula los dias restantes según el dia_inicio de la quest, asi el
        contador baja solo (3 → 2 → 1) en lugar de quedar fijo.
        Ej.: el primer dia muestra 'Esperar 3 días'; al siguiente, 'Esperar 2 días'."""
        q = sistema_quests.obtener_quest(quest_id)
        dia_inicio = (q.dia_inicio if q else 0) or 0
        restantes = max(1, total_dias - (getattr(store, 'dias_totales', 1) - dia_inicio))
        # Singular y plural son plantillas separadas: el truco de concatenar la "s"
        # solo funciona en español y ademas deja el texto fuera de la traduccion.
        if restantes == 1:
            return renpy.translate_string("Esperar 1 día")
        return renpy.translate_string("Esperar {dias} días").format(dias=restantes)

    # =========================================================================
    # QUEST 0_a - Violet me ignora (Violet)
    # =========================================================================

    quest_violet_0a = Quest(
        id="violet_questprincipal_0_a",
        npc_id="violet",
        nombre="Violet me ignora",
        descripcion="Parece que Violet no quiere hablarme",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        validacion_especial=[],
        mensaje_pista="Tengo que romper el hielo con Violet",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_pista_quest0a_violet,
                que_hacer=_quehacer_quest0a_violet,
                mensaje_despertar="Violet se veia bastante molesta, podría hablar con ella para saber que le pasa",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_0a)

    # =========================================================================
    # QUEST 0_b - ¿Que le pasa a Violet? (Violet)
    # =========================================================================

    quest_violet_0 = Quest(
        id="violet_questprincipal_0_b",
        npc_id="violet",
        nombre="¿Que le pasa a Violet?",
        descripcion="Violet me ignoró desde que llegué, debería hablar con ella.",
        numero_quest=0,
        dias_espera=0,
        quest_anterior="violet_questprincipal_0_a",
        requisitos=[],
        validacion_especial=[
            Requisito("npc_presente", "Violet debe estar en su habitación", npc_id="violet", locacion_id="casa_hviolet"),
            Requisito("horario", "Debe ser por la tarde", horario_id=1)
        ],
        rutina_quest={
            (dia, 1): RutinaQuest(
                locacion="casa_hviolet",
                sprite="images/characters/casa/idle/idle_violet_casa_hviolet_tarde_rutinabase_grupobase_skinbase.jpg",
            )
            for dia in range(7)
        },
        mensaje_pista="Tengo que hablar con Violet, podría aprovechar cuando está en su habitación por la tarde.",
        mensaje_despertar="Tengo que encontrar algún momento para acercarme a Violet y ver qué le pasa.",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Tengo que hablar con Violet, podría aprovechar cuando está en su habitación por la tarde.",
                que_hacer="Ir a la habitación de Violet por la tarde.",
                mensaje_despertar="Tengo que encontrar algún momento para acercarme a Violet y ver qué le pasa.",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_0)

    # =========================================================================
    # QUEST 1 - Un paquete misterioso (Violet)
    # =========================================================================

    quest_violet_01_a = Quest(
        id="violet_questprincipal_01_a",
        npc_id="violet",
        nombre="Un paquete misterioso",
        descripcion="Parece que llegó algo para mí",
        numero_quest=1,
        dias_espera=3,
        condicion_espera=_qc("vq01a_condicion_espera", lambda: len(sistema_compras.verificar_entregas_hoy()) == 0),
        quest_anterior="violet_questprincipal_0_b",
        # Requiere que la quest 1 del MC esté completa (reconectar con las 3 chicas)
        # y que sea la mañana de un día posterior: el repartidor no puede aparecer
        # en el mismo horario en que se completó la quest del MC (ej. trasnoche).
        requisitos=[
            Requisito("quest_mc", "Tengo que terminar de reconectar con todas primero", quest_id="mc_quest_1"),
            Requisito("condicion", "El paquete debería llegar mañana por la mañana", condicion=_vq01a_entrega_lista),
        ],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Todo tranquilo por ahora",
                que_hacer=_qc("vq01a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_01_a", 3)),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                # Dinámicas: mientras faltan las chicas la pista apunta a eso; una vez
                # completa la quest del MC solo queda esperar al repartidor.
                pista=_qc("vq01a_condiciones_pista", lambda: (
                    "El paquete debería llegar mañana por la mañana" if _vq01a_mc_quest1_completa()
                    else "Todavía tengo cosas pendientes con las chicas antes de seguir."
                )),
                que_hacer=_qc("vq01a_condiciones_quehacer", lambda: (
                    "Esperar al repartidor por la mañana" if _vq01a_mc_quest1_completa()
                    else "Completar las quests principales de Mónica, Violet y Jasmine"
                )),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_pista_quest1_violet,
                que_hacer=_quehacer_quest1_violet,
                mensaje_despertar=_qc("vq01a_botonlisto_despertar", lambda: "Escuche el timbre" if getattr(store, 'violet_quest1_entrega_pendiente', False) else ""),
                accion_al_entrar=setup_entrega_quest1_violet,
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_01_a)

    # =========================================================================
    # QUEST 1_B - El contenido del paquete (Violet)
    # =========================================================================

    quest_violet_01_b = Quest(
        id="violet_questprincipal_01_b",
        npc_id="violet",
        nombre="Los mangas de Violet",
        descripcion="Tengo un paquete que parece ser de Violet, podría dárselo o ver qué tiene",
        numero_quest=2,
        dias_espera=0,
        quest_anterior="violet_questprincipal_01_a",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podría entregarle el paquete a Violet o podría ver bien qué tiene",
                que_hacer="Hablar con Violet y darle su paquete o revisar el contenido del paquete",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_01_b)

    # =========================================================================
    # QUEST 02_A - Un manga prestado (Violet)
    # =========================================================================

    quest_violet_02_a = Quest(
        id="violet_questprincipal_02_a",
        npc_id="violet",
        nombre="¿Mangas prestados?",
        descripcion="Podría pedirle a Violet que me preste algún manga para leer",
        numero_quest=3,
        dias_espera=1,
        quest_anterior="violet_questprincipal_01_b",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Podría hablar con Violet a ver si me presta algún manga",
                que_hacer="Darle un día",
                mensaje_despertar="Podría usar el anime para conectarme más con Violet, le voy a hablar para que me preste algún manga y luego hablar de él",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq02a_botonlisto_pista", lambda: (
                    "Podría intentar nuevamente" if getattr(store, 'violet_quest02a_primer_intento_hecho', False) and violet_presta_mangas()
                    else "Tengo que mejorar la relación con Violet" if getattr(store, 'violet_quest02a_primer_intento_hecho', False)
                    else "Podría hablar con Violet a ver si me presta algún manga"
                )),
                que_hacer=_qc("vq02a_botonlisto_quehacer", lambda: (
                    "Pedirle los mangas a Violet" if getattr(store, 'violet_quest02a_primer_intento_hecho', False) and violet_presta_mangas()
                    else violet_mangas_requisito_texto() if getattr(store, 'violet_quest02a_primer_intento_hecho', False)
                    else "Hablar con Violet"
                )),
                mensaje_despertar="Podría preguntarle a Violet si tiene algún manga para prestarme, quizás eso me ayude a mejorar mi relación con ella",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_02_a)

    # =========================================================================
    # QUEST 02_B - Los mangas de Violet
    # =========================================================================

    quest_violet_02_b = Quest(
        id="violet_questprincipal_02_b",
        npc_id="violet",
        nombre="Buscar los mangas",
        descripcion="Violet me dijo que pasara a buscar los mangas esta noche",
        numero_quest=4,
        dias_espera=0,
        quest_anterior="violet_questprincipal_02_a",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Tengo que buscar los mangas",
                que_hacer="Ir a la habitación de Violet por la noche",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_02_b)

    # =========================================================================
    # QUEST 02_C - Leer los mangas
    # =========================================================================

    quest_violet_02_c = Quest(
        id="violet_questprincipal_02_c",
        npc_id="violet",
        nombre="Leer los mangas",
        descripcion="Violet me prestó sus mangas, tendría que leerlos",
        numero_quest=5,
        dias_espera=0,
        quest_anterior="violet_questprincipal_02_b",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq02c_botonlisto_pista", lambda: (
                    "Terminar de leer los mangas" if getattr(store, 'mangas_violet_lecturas', 0) > 0
                    else "Tengo que leer los mangas"
                )),
                que_hacer=_qc("vq02c_botonlisto_quehacer", lambda: (
                    renpy.translate_string("Manga leído {leidos}/4").format(leidos=getattr(store, 'mangas_violet_lecturas', 0)) if getattr(store, 'mangas_violet_lecturas', 0) > 0
                    else "Desde el inventario leer Mangas de Violet"
                )),
                mensaje_despertar="Violet me prestó varios mangas, tendría que leerlos para poder hablar luego con ella y seguir acercándome",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_02_c)

    # =========================================================================
    # QUEST 03_A - Devolver los mangas
    # =========================================================================

    quest_violet_03_a = Quest(
        id="violet_questprincipal_03_a",
        npc_id="violet",
        nombre="Devolver los mangas",
        descripcion="Tengo que devolverle los mangas a Violet.",
        numero_quest=6,
        dias_espera=0,
        quest_anterior="violet_questprincipal_02_c",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Tengo que devolver los mangas",
                que_hacer="Interactuar habitación Violet",
                mensaje_despertar="Listo, lectura terminada. Cuando Violet esté en su habitación se los debería devolver y aprovechar el momento para hablar",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_03_a)

    # =========================================================================
    # QUEST 04_A - El cosplay de Violet
    # =========================================================================

    quest_violet_04_a = Quest(
        id="violet_questprincipal_04_a",
        npc_id="violet",
        nombre="El cosplay de Violet",
        descripcion="Podría preguntarle a Violet si se probó el cosplay",
        numero_quest=6,
        dias_espera=3,
        quest_anterior="violet_questprincipal_03_a",
        requisitos=[],
        validacion_especial=[
            Requisito("horario", "Debe ser por la mañana", horario_id=0),
            Requisito("locacion", "Deben estar en la cocina", locacion_id="casa_cocina"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Recuerdo lo del cosplay, debería esperar unos días.",
                que_hacer=_qc("vq04a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_04_a", 3)),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Cuando encuentre a Violet podría ver si se probó el cosplay",
                que_hacer="Hablar con Violet por la mañana en la Cocina",
                # Lista = dos piensa seguidos al despertar (_agregar_mensajes_despertar)
                mensaje_despertar=[
                    "Ya pasaron algunos días y Violet debería estar menos enfadada, podría preguntarle por el cosplay que le regalé",
                    "Igual por mi seguridad debería hablarle cuando esté en la cocina, si me mata hay testigos",
                ],
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_a)

    # =========================================================================
    # QUEST 04_B - Hablar con Violet (perdón)
    # =========================================================================

    quest_violet_04_b = Quest(
        id="violet_questprincipal_04_b",
        npc_id="violet",
        nombre="Violet y el Cosplay",
        descripcion="Debería ir a hablar con Violet y pedirle perdón.",
        numero_quest=7,
        dias_espera=2,
        quest_anterior="violet_questprincipal_04_a",
        requisitos=[],
        validacion_especial=[],
        rutina_quest={
            (dia, 0): RutinaQuest(
                locacion="casa_pasilloarriba",
                sprite="images/characters/casa/idle/idle_violet_casa_pasillo_fuera_rutinabase_grupobase_skinbase.webp",
                posicion=(663, 804),
            )
            for dia in range(7)
        },
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                que_hacer=_qc("vq04b_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_04_b", 2)),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podría hablar con Violet y pedirle perdón",
                que_hacer="Hablar con Violet",
                mensaje_despertar="No paro de tener problemas con Violet, debería verda y pedirle perdón",
                accion_al_entrar=setup_restriccion_violet_quest04b,
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_b)

    # =========================================================================
    # QUEST 04_C - El cosplay de Violet II (mensaje al dia siguiente)
    # =========================================================================

    quest_violet_04_c = Quest(
        id="violet_questprincipal_04_c",
        npc_id="violet",
        nombre="Violet y el Cosplay II",
        descripcion="Ahora solo queda esperar",
        numero_quest=8,
        dias_espera=1,
        quest_anterior="violet_questprincipal_04_b",
        requisitos=[],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest04c_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Esperar a que Violet me hable del cosplay",
                que_hacer="Darle un día",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                # Rama "todavía no llegó el mensaje": el chat de Violet llega de
                # NOCHE, así que al despertar decía "responderle el mensaje" sin
                # que hubiera mensaje. Ahora invita a esperar.
                pista=_qc("vq04c_botonlisto_pista", lambda: "Violet se lo probo debería ir a hablar con ella" if store.sistema_mensajes.grupo_completado("violet_quest04c_chat") else "No voy a seguir molestando a Violet, por ahora podría esperar"),
                que_hacer=_qc("vq04c_botonlisto_quehacer", lambda: "Ir a ver a Violet" if store.sistema_mensajes.grupo_completado("violet_quest04c_chat") else "Esperar que Violet nos envíe un mensaje"),
                # Sin mensaje_despertar: el chat llega de noche como prioritario y se
                # resuelve en el momento, no hace falta avisar al despertar.
                trigger_mensaje=("violet_quest04c_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_c)

    # =========================================================================
    # QUEST 04_D - El cosplay de Violet III (deseo 10)
    # =========================================================================

    quest_violet_04_d = Quest(
        id="violet_questprincipal_04_d",
        npc_id="violet",
        nombre="Violet y el Cosplay III",
        descripcion="Quizás si sigo mejorando mi relación con Violet me muestre un poco más",
        numero_quest=9,
        dias_espera=0,
        quest_anterior="violet_questprincipal_04_c",
        requisitos=[
            # Por hito y no por "deseo >= 10": el jugador lee un nombre y sabe
            # que le falta, en vez de perseguir un numero.
            Requisito("hito", "Necesitas avanzar en la línea de deseo con Violet",
                npc_id="violet", hito_id="violet_hito_deseo_01"),
        ],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest04d_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Tengo que mejorar mi relación con Violet para que me muestre más del cosplay",
                que_hacer=_qc("vq04d_condiciones_quehacer", lambda: renpy.translate_string("Alcanzar {}").format(
                    texto_hito_corto("violet_hito_deseo_01")
                )),
                mensaje_despertar="Violet dijo que tenía más fotos, quizás pueda lograr que me las envie",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                # Misma corrección que en la 04_c: el chat llega de NOCHE, así que
                # hasta que llegue la pista invita a esperar en vez de pedir que
                # respondas un mensaje que todavía no existe.
                pista=_qc("vq04d_botonlisto_pista", lambda: "Violet ya me contestó, debería ir a hablar con ella" if store.sistema_mensajes.grupo_completado("violet_quest04d_chat") else "Ahora solo queda esperar el mensaje de Violet"),
                que_hacer=_qc("vq04d_botonlisto_quehacer", lambda: "Ir a ver a Violet" if store.sistema_mensajes.grupo_completado("violet_quest04d_chat") else "Esperar el mensaje de Violet"),
                # Sin mensaje_despertar: el chat llega de noche como prioritario.
                trigger_mensaje=("violet_quest04d_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d)

    # =========================================================================
    # QUEST 04_D2 - Hacer algo por ella (paso intermedio 04_d -> 04_e)
    # =========================================================================
    # Se inserta ENTRE la 04_d y la 04_e sin renumerar la cadena: por eso el id
    # lleva "d2" en vez de un numero nuevo.
    #
    # numero_quest queda en 9, igual que la 04_d. Solo lo lee la herramienta de
    # dev para ordenar la lista, y ese sort es estable, asi que el orden de
    # registro alcanza para que d -> d2 -> d3 se vean en secuencia.
    #
    # Arranca sola al completar la 04_d y queda un dia en ETAPA_ESPERA
    # (dias_espera=1): el jugador la ve recien al despertar del dia siguiente.

    quest_violet_04_d2 = Quest(
        id="violet_questprincipal_04_d2",
        npc_id="violet",
        nombre="Algo por ella",
        descripcion="Violet dijo que tenía más fotos, quizás pueda conseguirlas haciendo algo por ella",
        numero_quest=9,
        dias_espera=1,
        quest_anterior="violet_questprincipal_04_d",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Violet dijo que tenía más fotos, tengo que pensar cómo conseguirlas",
                que_hacer="Darle un día",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Violet dijo que tenía más fotos, debería haber alguna forma para que me las mande",
                que_hacer="Ofrecerle ayuda a Violet",
                # Lista y no string: el sistema de despertar acepta varios
                # pensamientos seguidos y los muestra como piensa encadenados.
                mensaje_despertar=[
                    "Violet dijo que tenía más fotos, debería haber alguna forma para que me las mande",
                    "Quizás si hago cosas por ella lo consiga",
                ],
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d2)

    # =========================================================================
    # ARCO DE LOS FAVORES — quests 04_D3 a 04_D6
    # =========================================================================
    # Violet le pide tres cosas al MC (golosinas, cocinar, limpiar) y despues
    # viene el cierre. Va en CUATRO quests encadenadas y no en una sola por dos
    # razones, las dos sobre los textos del panel de pistas:
    #
    #  1. La espera de un dia solo existe al INICIO de una quest (dias_espera se
    #     evalua en ETAPA_ESPERA y nada mas). En una quest unica habria que
    #     llevar tres relojes a mano contra dias_totales.
    #  2. config_etapas se indexa por ETAPA, no por objetivo: una quest sola
    #     tendria un unico ETAPA_BOTON_LISTO para los cuatro favores, o sea cada
    #     pista/que_hacer/despertar seria un _qc de cuatro ramas.
    #
    # Las cuatro son LINEA_PRINCIPAL y encadenan, asi que nunca hay dos activas
    # a la vez: el panel muestra una sola.
    #
    # Los flags (vq4d3_pedido_hecho, etc.), el helper de quest activa y el
    # despachador del boton viven en violet_quest_04_favores.rpy.

    # --- 04_D3: las golosinas ------------------------------------------------

    quest_violet_04_d3 = Quest(
        id="violet_questprincipal_04_d3",
        npc_id="violet",
        nombre="Las golosinas",
        descripcion="Violet me pidió unas golosinas, es lo menos que puedo hacer",
        numero_quest=9,
        dias_espera=1,
        quest_anterior="violet_questprincipal_04_d2",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Violet no necesita nada por hoy",
                que_hacer="Esperar al día siguiente",
            ),
            # Tres estados: todavia no le pregunte / me pidio golosinas y no las
            # tengo / ya las tengo. El texto sigue al inventario solo.
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq04d3_pista", lambda: (
                    "Ya tengo las golosinas que me pidió" if store.vq4d3_pedido_hecho and store.inventario.get("golosinas", 0) > 0
                    else "Violet me pidió unas golosinas" if store.vq4d3_pedido_hecho
                    else "Podría ver si Violet necesita algo"
                )),
                que_hacer=_qc("vq04d3_quehacer", lambda: (
                    "Darle las golosinas a Violet" if store.vq4d3_pedido_hecho and store.inventario.get("golosinas", 0) > 0
                    else "Conseguir golosinas" if store.vq4d3_pedido_hecho
                    else "Hablar con Violet"
                )),
                mensaje_despertar=_qc("vq04d3_despertar", lambda: (
                    "Tengo las golosinas, hoy se las puedo dar" if store.vq4d3_pedido_hecho and store.inventario.get("golosinas", 0) > 0
                    else "Tengo que conseguirle las golosinas a Violet" if store.vq4d3_pedido_hecho
                    else "Debo estar atento por si Violet necesita algo"
                )),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d3)

    # --- 04_D4: la pizza -----------------------------------------------------

    quest_violet_04_d4 = Quest(
        id="violet_questprincipal_04_d4",
        npc_id="violet",
        nombre="La pizza",
        # Ojo: la descripcion NO puede repetir la pista ("Violet quiere volver a
        # cenar pizza") — dos `old` iguales en tl rompen el lint.
        descripcion="Violet quiere que le cocine una pizza para la cena",
        numero_quest=9,
        dias_espera=1,
        quest_anterior="violet_questprincipal_04_d3",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Violet no necesita nada por hoy",
                que_hacer="Esperar al día siguiente",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq04d4_pista", lambda: (
                    "La pizza ya está lista" if store.vq4d4_pizza_cocinada
                    else "Violet quiere volver a cenar pizza" if store.vq4d4_pedido_hecho
                    else "Podría ver si Violet necesita algo"
                )),
                que_hacer=_qc("vq04d4_quehacer", lambda: (
                    "Avisarle a Violet en su habitación" if store.vq4d4_pizza_cocinada
                    else "Cocinar la pizza de noche" if store.vq4d4_pedido_hecho
                    else "Hablar con Violet"
                )),
                mensaje_despertar=_qc("vq04d4_despertar", lambda: (
                    "La pizza quedó lista, tengo que avisarle a Violet" if store.vq4d4_pizza_cocinada
                    else "Violet quiere pizza, tengo que cocinarla esta noche" if store.vq4d4_pedido_hecho
                    else "Debo estar atento por si Violet necesita algo"
                )),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d4)

    # --- 04_D5: la limpieza --------------------------------------------------

    quest_violet_04_d5 = Quest(
        id="violet_questprincipal_04_d5",
        npc_id="violet",
        nombre="La limpieza",
        descripcion="Violet me pidió que limpie algunas partes de la casa",
        numero_quest=9,
        # DOS dias, no uno: acá el MC se da por vencido con las fotos y es
        # VIOLET la que lo busca. La espera es parte de la narrativa.
        dias_espera=2,
        quest_anterior="violet_questprincipal_04_d4",
        requisitos=[],
        validacion_especial=[],
        # Rutina especial: el dia que se cumple la espera, Violet pasa la TARDE
        # en el pasillo de arriba en vez de su lugar habitual — es su forma de
        # cruzarse con el MC. Va para los 7 dias porque no sabemos en cual cae.
        # La rutina se aplica al pasar a ETAPA_RUTINA (o sea, cuando termina la
        # espera) y la levanta violet_q4d5_pedido apenas hablan.
        rutina_quest={
            (dia, 1): RutinaQuest(locacion="casa_pasilloarriba")
            for dia in range(7)
        },
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="No se como conseguir la foto, me rindo",
                que_hacer="Esperar a que Violet te busque",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq04d5_pista", lambda: (
                    "Violet me pidió que limpie el living, el comedor y la cocina" if store.vq4d5_pedido_hecho
                    else "Podría ver si Violet necesita algo"
                )),
                # Contador: el jugador ve cuanto le falta sin tener que recordar
                # en que locaciones ya estuvo.
                que_hacer=_qc("vq04d5_quehacer", lambda: (
                    renpy.translate_string("Limpiar la casa ({}/3)").format(violet_favores_limpiezas_hechas())
                    if store.vq4d5_pedido_hecho else "Hablar con Violet"
                )),
                mensaje_despertar=_qc("vq04d5_despertar", lambda: (
                    "Tengo que limpiar el living, el comedor y la cocina" if store.vq4d5_pedido_hecho
                    else "Debo estar atento por si Violet necesita algo"
                )),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d5)

    # --- 04_D6: el cierre ----------------------------------------------------

    quest_violet_04_d6 = Quest(
        id="violet_questprincipal_04_d6",
        npc_id="violet",
        nombre="Todo lo que me pidió",
        descripcion="Ya hice los tres favores que Violet me pidió",
        numero_quest=9,
        # Sin espera: apenas termina la tercera limpieza el MC puede ir a
        # cobrarse el favor. Hacerlo esperar un dia contradecia el "avisame
        # cuando esté todo listo" de la propia Violet.
        dias_espera=0,
        quest_anterior="violet_questprincipal_04_d5",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            # Sin ETAPA_ESPERA: con dias_espera=0 la quest la atraviesa sin
            # detenerse y esos textos no se verian nunca.
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Hice todo lo que Violet me pidió",
                que_hacer="Hablar con Violet en su habitación",
                mensaje_despertar="Hice todo lo que Violet me pidió, tengo que ir a hablar con ella",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d6)

    # =========================================================================
    # QUEST 04_E - El cosplay de Violet IV (deseo 15)
    # =========================================================================

    quest_violet_04_e = Quest(
        id="violet_questprincipal_04_e",
        npc_id="violet",
        nombre="El cosplay de Violet IV",
        descripcion="Quizás si sigo mejorando mi relación con Violet me muestre un poco más",
        numero_quest=10,
        dias_espera=0,
        quest_anterior="violet_questprincipal_04_d6",
        # Sin requisito de stat: la llave ahora es haber terminado el arco de los
        # favores (04_d6). El "15 de deseo" era del esquema viejo, cuando la 04_e
        # colgaba directo de la 04_d y no existia la cadena de favores; dejarlo
        # sumaba una segunda condicion que ya no representa nada.
        requisitos=[],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest04e_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Tengo que seguir mejorando mi relación con Violet para que me muestre más.",
                que_hacer=_qc("vq04e_condiciones_quehacer", lambda: renpy.translate_string("Subir deseo 💋 con Violet ({}/{})").format(
                    getattr(store, 'violet_deseo', 0), 15
                )),
                mensaje_despertar="Esto de mejorar mi relación con Violet esta trayendo buenos resultados, me pregunto si podre conseguir algo más",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                # Misma corrección que en la 04_c y la 04_d: el chat llega de
                # NOCHE, así que hasta que llegue la pista invita a esperar en vez
                # de pedir que respondas un mensaje que todavía no existe.
                pista=_qc("vq04e_botonlisto_pista", lambda: "Violet ya me contestó, debería ir a hablar con ella" if store.sistema_mensajes.grupo_completado("violet_quest04e_chat") else "Ahora solo queda esperar el mensaje de Violet"),
                que_hacer=_qc("vq04e_botonlisto_quehacer", lambda: "Ir a ver a Violet" if store.sistema_mensajes.grupo_completado("violet_quest04e_chat") else "Esperar el mensaje de Violet"),
                # Doble piensa al despertar, solo despues de responder el chat nocturno
                # (antes de responderlo lo resuelve el mensaje prioritario en el momento).
                mensaje_despertar=_qc("vq04e_botonlisto_despertar", lambda: [
                    "Violet no quiere usar el cosplay que le regalé, pero no significa que no quiera ir",
                    "Voy a sugerirle ir a la Japicon con otro cosplay",
                ] if store.sistema_mensajes.grupo_completado("violet_quest04e_chat") else ""),
                trigger_mensaje=("violet_quest04e_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_e)

    # =========================================================================
    # QUEST 05_A - Un nuevo cosplay (chat con Tienda CoXplay)
    # =========================================================================

    quest_violet_05_a = Quest(
        id="violet_questprincipal_05_a",
        npc_id="violet",
        nombre="Un nuevo cosplay",
        descripcion="Podría averiguar para comprar un nuevo cosplay para Violet",
        numero_quest=11,
        dias_espera=0,
        quest_anterior="violet_questprincipal_04_e",
        requisitos=[],
        validacion_especial=[
            Requisito("mensaje", "Completar la conversación con la tienda", grupo_id="coxplay_q5a_g4"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_pista_quest05a,
                que_hacer=_quehacer_quest05a,
                mensaje_despertar=_despertar_quest05a,
                trigger_mensaje=("coxplay_q5a_g1", "tienda_coxplay"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_05_a)

    # =========================================================================
    # QUEST 05_B - El paquete llegó
    # =========================================================================

    quest_violet_05_b = Quest(
        id="violet_questprincipal_05_b",
        npc_id="violet",
        nombre="El paquete llegó",
        descripcion="Estoy esperando el paquete de cosplays de CoXplay",
        numero_quest=12,
        dias_espera=0,
        quest_anterior="violet_questprincipal_05_a",
        requisitos=[
            Requisito("item", "Recibir el paquete de CoXplay", item_id="coxplay_box"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Estoy esperando que llegue el paquete de CoXplay",
                que_hacer="Esperar el paquete de CoXplay",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Ya tengo los cosplay, debería dárselos a Violet",
                que_hacer="Hablar con Violet",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_05_b)

    # =========================================================================
    # QUEST 05_C - El malentendido del cosplay
    # =========================================================================

    quest_violet_05_c = Quest(
        id="violet_questprincipal_05_c",
        npc_id="violet",
        nombre="El malentendido del cosplay",
        descripcion="Tengo que esperar que Violet se los pruebe",
        numero_quest=13,
        dias_espera=1,
        quest_anterior="violet_questprincipal_05_b",
        requisitos=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_q5c_g1"),
        ],
        validacion_especial=[
            Requisito("npc_presente", "Violet debe estar en su habitación", npc_id="violet", locacion_id="casa_hviolet"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Tengo que esperar que Violet se los pruebe",
                que_hacer="Esperar mensaje de Violet",
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista=_pista_quest05c_condiciones,
                que_hacer="Esperar",
                trigger_mensaje=("violet_q5c_g1", "violet"),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Debería pedirle perdón a Violet... Otra vez",
                que_hacer="Hablar con Violet en su habitación",
                mensaje_despertar="Debería ir a hablar con Violet a su habitación",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_05_c)

    # =========================================================================
    # QUEST 06_A - Las entradas
    # =========================================================================

    quest_violet_06_a = Quest(
        id="violet_questprincipal_06_a",
        npc_id="violet",
        nombre="Las entradas",
        descripcion="Las entradas para la Japicon están disponibles",
        numero_quest=14,
        dias_espera=1,
        quest_anterior="violet_questprincipal_05_c",
        requisitos=[
            Requisito("item", "Comprar dos entradas para la Japicon", item_id="entrada_japicon", cantidad=2),
        ],
        validacion_especial=[
            Requisito("npc_presente", "Violet debe estar en su habitación", npc_id="violet", locacion_id="casa_hviolet"),
            Requisito("horario", "Debe ser de noche", horario_id=2),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Tengo que esperar a que las entradas estén disponibles",
                que_hacer=_qc("vq06a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_06_a", 1)),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                # Dinámicas: al comprar las 2 entradas la pista pasa a "esperar
                # que lleguen" (el requisito recién se cumple cuando se entregan).
                pista=_pista_quest06a_condiciones,
                que_hacer=_quehacer_quest06a_condiciones,
                # Doble piensa al despertar el día que se habilita la venta (se
                # entra a esta etapa justo cuando las entradas salen a la venta).
                mensaje_despertar=[
                    "Hoy comienza la venta de entradas para la Japicon",
                    "Comprarlas sería una buena disculpa y forma de mostrarle lo que quiero",
                ],
                trigger_mensaje=("japicon_tickets_g1", "libre_mercado"),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Contarle a Violet de las entradas por la noche en su habitación",
                que_hacer="Hablar con Violet de noche en su habitación",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_06_a)

    # =========================================================================
    # QUEST 06_B - La prueba del cosplay
    # =========================================================================

    quest_violet_06_b = Quest(
        id="violet_questprincipal_06_b",
        npc_id="violet",
        nombre="La prueba del cosplay",
        descripcion="Violet me pidió que la visite por la noche",
        numero_quest=15,
        dias_espera=2,
        quest_anterior="violet_questprincipal_06_a",
        requisitos=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_q6b_g1"),
        ],
        validacion_especial=[
            Requisito("npc_presente", "Violet debe estar en su habitación", npc_id="violet", locacion_id="casa_hviolet"),
            Requisito("horario", "Debe ser de noche", horario_id=2),
        ],
        # Rutina de quest: al responder el mensaje (CONDICIONES -> RUTINA) Violet se
        # queda en su habitacion TODAS las noches hasta completar la quest. Sin esto,
        # su rutina base la manda al living el domingo a la noche (definition_violet:159)
        # y esa noche la quest era imposible de completar. Se restaura sola al completar.
        # Sprite y posicion: los mismos de su rutina base de noche (definition_violet).
        rutina_quest={
            (dia, 2): RutinaQuest(
                locacion="casa_hviolet",
                sprite="images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.jpg",
                posicion=(1537, 1020),
            )
            for dia in range(7)
        },
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Supongo que toca esperar",
                que_hacer=_qc("vq06b_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_06_b", 2)),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista=_pista_quest06b_condiciones,
                que_hacer=_quehacer_quest06b_condiciones,
                trigger_mensaje=("violet_q6b_g1", "violet"),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Violet me pidió que la visite por la noche.",
                que_hacer="Ir a la habitación de Violet por la noche",
                mensaje_despertar="Violet me pidió que la visite por la noche",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_06_b)

    # =========================================================================
    # QUEST 07_A - El cierre del cosplay
    # =========================================================================

    quest_violet_07_a = Quest(
        id="violet_questprincipal_07_a",
        npc_id="violet",
        nombre="El cierre del cosplay",
        descripcion="Tengo que ver qué pasó con el cosplay",
        numero_quest=16,
        dias_espera=3,
        quest_anterior="violet_questprincipal_06_b",
        requisitos=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista=_pista_quest07a_espera,
                que_hacer=_qc("vq07a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_07_a", 3)),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Tengo que hablar con Violet sobre el cosplay",
                que_hacer="Hablar con Violet",
                mensaje_despertar="Con ese cosplay no va a poder ir, debería hablar con ella para ver si se le ocurre cómo seguir",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_07_a)

    # =========================================================================
    # QUEST 07_B - El cambio del cosplay
    # =========================================================================

    quest_violet_07_b = Quest(
        id="violet_questprincipal_07_b",
        npc_id="violet",
        nombre="El cambio del cosplay",
        descripcion="Tengo que contactar a la tienda para pedir el cambio del cierre",
        numero_quest=17,
        dias_espera=0,
        quest_anterior="violet_questprincipal_07_a",
        requisitos=[
            Requisito("mensaje", "Enviar mensaje a Tienda Coxplay", grupo_id="tienda_coxplay_q7b_g1"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Hablar con la tienda para pedir el cambio.",
                que_hacer="Enviar mensaje a Tienda Coxplay",
                trigger_mensaje=("tienda_coxplay_q7b_g1", "tienda_coxplay"),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Contarle a Violet sobre el cambio",
                que_hacer="Hablar con Violet",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_07_b)

    # =========================================================================
    # QUEST 07_C - Cosplay de reemplazo
    # =========================================================================

    quest_violet_07_c = Quest(
        id="violet_questprincipal_07_c",
        npc_id="violet",
        nombre="Cosplay de reemplazo",
        descripcion="Violet me avisó que habló con la tienda y va a enviar el cosplay",
        numero_quest=18,
        dias_espera=1,
        quest_anterior="violet_questprincipal_07_b",
        requisitos=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_q7c_g1"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Esperar que Violet hable con la tienda",
                que_hacer=_qc("vq07c_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_07_c", 1)),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Violet te mandó un mensaje",
                que_hacer="Responder mensaje de Violet",
                trigger_mensaje=("violet_q7c_g1", "violet"),
            ),
            # Sin ETAPA_BOTON_LISTO: la quest se cierra con el propio chat
            # (accion_al_completar del grupo violet_q7c_g1). No hay que hablar
            # con Violet; al completarse arranca la 08_a con su espera de 3 días.
        },
    )
    sistema_quests.registrar_quest(quest_violet_07_c)

    # =========================================================================
    # QUEST 08_A - La tormenta
    # =========================================================================

    quest_violet_08_a = Quest(
        id="violet_questprincipal_08_a",
        npc_id="violet",
        nombre="La tormenta",
        descripcion="Hoy iba a estar solo en casa",
        numero_quest=19,
        dias_espera=3,
        quest_anterior="violet_questprincipal_07_c",
        requisitos=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="No hay nada urgente que hacer, dejar pasar unos días",
                que_hacer=_qc("vq08a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_08_a", 3)),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Hoy las chicas salieron. Podría ver la TV en el living",
                que_hacer="Ver TV en el living",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_08_a)

    # =========================================================================
    # QUEST 09_A — Violet enferma
    # =========================================================================

    # Idles de Violet ENFERMA. Solo existen los de tarde y noche, que son los
    # dos momentos en que se la puede ir a ver.
    #
    # Mañana y trasnoche van con sprite None A PROPOSITO: el motor la ubica en
    # su habitacion (que es lo que necesita la logica de la quest) pero no la
    # dibuja, y sin sprite no hay imagebutton — o sea que tampoco se la puede
    # clickear. Es justo lo que se quiere: a esas horas no se la molesta.
    #
    # Los idles normales NO sirven acá: la mostraban sana mientras la quest la
    # tiene en cama.
    _vq9a_sprites_violet = {
        0: None,
        1: "images/characters/casa/idle/idle_violet_casa_hviolet_tarde_enferma.jpg",
        2: "images/characters/casa/idle/idle_violet_casa_hviolet_noche_enferma.jpg",
        3: None,
    }
    _vq9a_sprites_monica = {
        0: "images/characters/casa/idle/idle_monica_casa_living_manana_rutinabase_grupobase_skinbase.webp",
        1: "images/characters/casa/idle/idle_monica_casa_living_manana_rutinabase_grupobase_skinbase.webp",
        2: "images/characters/casa/idle/idle_monica_casa_hmonica_noche_rutinabase_grupobase_skinbase.jpg",
        3: "images/characters/casa/idle/idle_monica_casa_hmonica_trasnoche_rutinabase_grupobase_skinbase.jpg",
    }
    _vq9a_locs_monica = {0: "casa_living", 1: "casa_living", 2: "casa_hmonica", 3: "casa_hmonica"}

    quest_violet_09_a = Quest(
        id="violet_questprincipal_09_a",
        npc_id="violet",
        nombre="Violet enferma",
        descripcion="Violet se pescó una gripe, tengo que cuidarla.",
        numero_quest=20,
        dias_espera=1,
        # Ultima quest de la linea principal de Violet: arranca al completarse la
        # 08_a y no encadena a ninguna (las viejas 11 y 12 se eliminaron).
        quest_anterior="violet_questprincipal_08_a",
        # Sin requisitos ademas de la espera: la respuesta de la tienda ya no
        # es un Requisito. Los mensajes se meten en el historial YA LEIDOS
        # dentro de la escena de arranque (violet_quest09a_inicio), asi que no
        # hay nada que el jugador tenga que ir a responder.
        requisitos=[],
        rutina_quest={
            (dia, horario): RutinaQuest(
                locacion="casa_hviolet",
                sprite=_vq9a_sprites_violet[horario],
            )
            for dia in range(7) for horario in range(4)
        },
        rutinas_adicionales={
            "monica": {
                (dia, horario): RutinaQuest(
                    locacion=_vq9a_locs_monica[horario],
                    sprite=_vq9a_sprites_monica[horario],
                )
                for dia in range(7) for horario in range(4)
            }
        },
        prioridad_rutina=0,
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="A seguir esperando por la Japicon.",
                que_hacer=_qc("vq09a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_09_a", 1)),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podría ver si Violet necesita algo mientras está enferma.",
                que_hacer=_qc("vq09a_botonlisto_quehacer", lambda: renpy.translate_string("Ayudar a Violet ({}/3)").format(getattr(store, 'violet_enferma_atencion', 0))),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_09_a)


################################################################################
## Funciones auxiliares para quests de Violet
################################################################################

init python:

    def _estado_quest05a():
        """
        Retorna (pista, que_hacer, despertar) dinámico según el estado del chat CoXplay.
        """
        msgs = getattr(store, 'sistema_mensajes', None)
        if not msgs:
            return (
                "Podría averiguar para comprar un nuevo cosplay para Violet.",
                "Escribirle un mensaje a Tienda CoXplay",
                "Podría escribirle a la tienda CoXplay sobre un nuevo cosplay.",
            )

        def _grupo(grupo_id):
            return msgs._todos_grupos.get(grupo_id)

        def _completado(grupo_id):
            return msgs.grupo_completado(grupo_id)

        def _disparado(grupo_id):
            """
            True si el grupo YA SE DISPARO (no solo si existe).

            Ojo: `_todos_grupos` se llena al REGISTRAR los grupos, en init, asi
            que preguntar por la mera existencia (`if g4:`) daba siempre True y
            la quest se quedaba clavada reportando la fase 4 (la dirección de
            envio) desde el minuto cero, sin llegar nunca a las fases 3/2/1.

            El estado por si solo no alcanza: "pendiente" es a la vez el estado
            inicial de un grupo sin disparar Y el de uno ya entregado esperando
            que el jugador lo abra. Por eso se desempata mirando si el grupo esta
            en la bandeja del chat o en la cola de espera de entrega.
            """
            g = _grupo(grupo_id)
            if not g:
                return False
            if g.estado in ("espera", "en_curso", "completado"):
                return True
            chat = msgs.chats.get(g.npc_id)
            if chat and g in getattr(chat, 'grupos_pendientes', []):
                return True
            return g in getattr(msgs, '_grupos_en_espera', [])

        # Fase 4: dirección de envío
        g4 = _grupo("coxplay_q5a_g4")
        if _disparado("coxplay_q5a_g4"):
            if _completado("coxplay_q5a_g4"):
                dias_restantes = max(0, getattr(store, 'coxplay_pedido_dia', 0) + 2 - getattr(store, 'dias_totales', 0))
                if dias_restantes > 0:
                    if dias_restantes == 1:
                        _txt_espera = renpy.translate_string("Hablar con Violet / Esperar 1 día más")
                    else:
                        _txt_espera = renpy.translate_string("Hablar con Violet / Esperar {dias} días más").format(dias=dias_restantes)
                    return (
                        "Podría hablar con Violet y contarle lo que compré.",
                        _txt_espera,
                        "Podría contarle a Violet sobre el pedido de cosplays.",
                    )
                return (
                    "Podría hablar con Violet y contarle lo que compré.",
                    "Hablar con Violet",
                    "Podría contarle a Violet sobre los cosplays que compré.",
                )
            if g4.estado in ["pendiente", "en_curso"]:
                return (
                    "La tienda me pidió la dirección de envío.",
                    "Responder a Tienda CoXplay",
                    "Tengo que responderle a CoXplay con la dirección.",
                )
            return (
                "La tienda está procesando la dirección de envío.",
                "Esperar horario de atención de CoXplay",
                "Hoy CoXplay puede confirmar la dirección de envío.",
            )

        # Fase 3: pago — la cadena esta esperando que respondamos con el pago.
        # Pista y que_hacer unicos para toda la fase: el texto ya contempla las
        # dos situaciones (juntar la plata y responder el mensaje), asi que no
        # hace falta partirlo segun cuanto dinero haya. Solo cambia el
        # mensaje_despertar, que si distingue.
        if _disparado("coxplay_q5a_g3") and not _completado("coxplay_q5a_g3"):
            if getattr(store, 'dinero', 0) >= 200:
                return (
                    "Tienda Coxplay está esperando el pago",
                    "Tener $200 en la cuenta y responder el mensaje de Tienda Coxplay",
                    "Hoy puedo confirmar el pago del cosplay en el chat.",
                )
            return (
                "Tienda Coxplay está esperando el pago",
                "Tener $200 en la cuenta y responder el mensaje de Tienda Coxplay",
                "Necesito ahorrar $200 para pagar el pedido a CoXplay.",
            )

        # Fase 2: conversacion principal
        g2 = _grupo("coxplay_q5a_g2")
        if _disparado("coxplay_q5a_g2"):
            if g2.estado in ["pendiente", "en_curso"]:
                return (
                    "La tienda me respondió, tengo que continuar la conversación.",
                    "Responder a Tienda CoXplay",
                    "Tengo un mensaje de Tienda CoXplay esperando.",
                )
            return (
                "Esperando respuesta de la tienda.",
                "Esperar horario de atención de CoXplay",
                "Hoy CoXplay puede responder a mi consulta.",
            )

        # Fase 1: esperando respuesta inicial
        if _completado("coxplay_q5a_g1"):
            return (
                "Mandé el mensaje, esperando respuesta de la tienda.",
                "Esperar horario de atención de CoXplay",
                "Hoy CoXplay puede responder a mi consulta.",
            )

        return (
            "Podría averiguar para comprar un nuevo cosplay para Violet.",
            "Escribirle un mensaje a Tienda CoXplay",
            "Podría escribirle a la tienda CoXplay sobre un nuevo cosplay.",
        )

    def _pista_quest05a():
        return _estado_quest05a()[0]

    def _quehacer_quest05a():
        return _estado_quest05a()[1]

    def _despertar_quest05a():
        return _estado_quest05a()[2]

    def _pista_quest05c_condiciones():
        msgs = getattr(store, 'sistema_mensajes', None)
        if not msgs:
            return "Violet va a mandarme un mensaje de noche sobre los cosplays."
        g1 = msgs._todos_grupos.get("violet_q5c_g1")
        if g1 and g1.estado in ["pendiente", "en_curso"]:
            return "Violet me mandó un mensaje, debería responderle."
        return "Violet va a mandarme un mensaje de noche sobre los cosplays."

    def _quehacer_quest05c_condiciones():
        msgs = getattr(store, 'sistema_mensajes', None)
        if not msgs:
            return "Esperar el mensaje de noche"
        g1 = msgs._todos_grupos.get("violet_q5c_g1")
        if g1 and g1.estado in ["pendiente", "en_curso"]:
            return "Responder a Violet"
        return "Esperar el mensaje de noche"

    def _vq06a_entradas_en_camino():
        """True si las 2 entradas ya se compraron pero todavía no llegaron."""
        try:
            en_inventario = store.inventario.get("entrada_japicon", 0)
        except Exception:
            en_inventario = 0
        return cantidad_comprada("entrada_japicon") >= 2 and en_inventario < 2

    def _pista_quest06a_condiciones():
        if _vq06a_entradas_en_camino():
            return "Ya compré las entradas, ahora hay que esperar que lleguen"
        return "Las entradas para la Japicon están disponibles"

    def _quehacer_quest06a_condiciones():
        if _vq06a_entradas_en_camino():
            return "Esperar que lleguen las entradas"
        return "Comprar dos entradas para la Japicon"

    def _pista_quest06b_condiciones():
        msgs = getattr(store, 'sistema_mensajes', None)
        if not msgs:
            return "Violet me envió un mensaje."
        g1 = msgs._todos_grupos.get("violet_q6b_g1")
        if g1 and g1.estado == "completado":
            return "Violet me pidió que la visite por la noche."
        if g1 and g1.estado in ["pendiente", "en_curso"]:
            return "Violet me envió un mensaje."
        return "Violet va a mandarme un mensaje."

    def _quehacer_quest06b_condiciones():
        msgs = getattr(store, 'sistema_mensajes', None)
        if not msgs:
            return "Responder mensaje Violet"
        g1 = msgs._todos_grupos.get("violet_q6b_g1")
        if g1 and g1.estado == "completado":
            return "Ir a la habitación de Violet por la noche"
        if g1 and g1.estado in ["pendiente", "en_curso"]:
            return "Responder mensaje Violet"
        return "Responder mensaje Violet"

    def _pista_quest07a_espera():
        eleccion = getattr(store, 'violet_06b_eleccion', None)
        if eleccion == "C":
            return "Debería esperar antes de hablar con Violet."
        return "Tengo que esperar a ver si Monica pudo arreglar el cierre."

    def setup_restriccion_violet_quest04b():
        """
        accion_al_entrar de ETAPA_BOTON_LISTO. Los NPCs siguen interactuables.

        OJO: aca NO se registra el disparo de la quest. Antes terminaba con un
        loop de `r.registrar_label_locacion(...)` sobre las 5 locaciones de
        Violet, y eso la rompia igual que a la 0_b de Monica: el registro vivia
        en `restriccion_quest_activa`, que es un slot global unico que cualquier
        `activar_restriccion` reemplaza y cualquier `desactivar_restriccion`
        borra. Como accion_al_entrar corre UNA sola vez, la quest quedaba muerta.
        Era peor que el caso de Monica: esta restriccion no bloquea NADA, asi
        que el jugador podia irse a hacer cualquier contenido sin ningun aviso.

        El disparo ahora es un trigger de game_loop registrado en init, en
        violet_quest_04_b.rpy. La llamada de abajo se mantiene tal cual para no
        cambiar el comportamiento de interaccion con NPCs.
        """
        activar_restriccion(
            npcs_interactuables=["violet", "jasmine", "monica"],
        )