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
        return "Esperar {} d{}".format(restantes, "ia" if restantes == 1 else "ias")

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
                sprite="images/characters/casa/idle/idle_violet_casa_hviolet_tarde_rutinabase_grupobase_skinbase.png",
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
        # Requiere que la quest 1 del MC esté completa (reconectar con las 3 chicas).
        requisitos=[
            Requisito("quest_mc", "Tengo que terminar de reconectar con todas primero", quest_id="mc_quest_1"),
        ],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Todo tranquilo por ahora",
                que_hacer=_qc("vq01a_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_01_a", 3)),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Todavía tengo cosas pendientes con las chicas antes de seguir.",
                que_hacer="Completar las quests principales de Mónica, Violet y Jasmine",
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
                    "Podría intentar nuevamente" if getattr(store, 'violet_quest02a_primer_intento_hecho', False) and obtener_stat1("violet") >= 10
                    else "Tengo que mejorar la relación con Violet" if getattr(store, 'violet_quest02a_primer_intento_hecho', False)
                    else "Podría hablar con Violet a ver si me presta algún manga"
                )),
                que_hacer=_qc("vq02a_botonlisto_quehacer", lambda: (
                    "Pedirle los mangas a Violet" if getattr(store, 'violet_quest02a_primer_intento_hecho', False) and obtener_stat1("violet") >= 10
                    else "Requisito ❤️ 10" if getattr(store, 'violet_quest02a_primer_intento_hecho', False)
                    else "Hablar con Violet"
                )),
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
                    "Manga leído {}/4".format(getattr(store, 'mangas_violet_lecturas', 0)) if getattr(store, 'mangas_violet_lecturas', 0) > 0
                    else "Desde el inventario leer Mangas de Violet"
                )),
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
                mensaje_despertar="Podría preguntarle a Violet si se probó el cosplay",
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
                sprite="images/characters/casa/idle/idle_violet_casa_pasillo_fuera_rutinabase_grupobase_skinbase.png",
                posicion=(663, 804),
            )
            for dia in range(7)
        },
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                que_hacer=_qc("vq04b_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_04_b", 2)),
                mensaje_despertar="Debería esperar un poco antes de hablar con Violet.",
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
                pista=_qc("vq04c_botonlisto_pista", lambda: "Violet se lo probo debería ir a hablar con ella" if store.sistema_mensajes.grupo_completado("violet_quest04c_chat") else "Violet me envió un mensaje, debería responderle."),
                que_hacer=_qc("vq04c_botonlisto_quehacer", lambda: "Ir a ver a Violet" if store.sistema_mensajes.grupo_completado("violet_quest04c_chat") else "Responder mensaje de Violet"),
                mensaje_despertar=_qc("vq04c_botonlisto_despertar", lambda: "Viole se probo el cosplay, si hablo con ella quizas logre que lo use en el evento" if store.sistema_mensajes.grupo_completado("violet_quest04c_chat") else "Violet me envió un mensaje, debería responderle."),
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
            Requisito("deseo", "Necesitas 10 💋 con Violet", npc_id="violet", valor=10),
        ],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest04d_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Tengo que mejorar mi relación con Violet para que me muestre más del cosplay",
                que_hacer=_qc("vq04d_condiciones_quehacer", lambda: renpy.translate_string("Subir deseo 💋 con Violet ({}/{})").format(
                    getattr(store, 'violet_deseo', 0), 10
                )),
                mensaje_despertar="Violet dijo que tenía más fotos, quizás pueda lograr que me las envie",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq04d_botonlisto_pista", lambda: "Violet ya me contestó, debería ir a hablar con ella" if store.sistema_mensajes.grupo_completado("violet_quest04d_chat") else "Violet me envió un mensaje, debería responderle"),
                que_hacer=_qc("vq04d_botonlisto_quehacer", lambda: "Ir a ver a Violet" if store.sistema_mensajes.grupo_completado("violet_quest04d_chat") else "Responder mensaje de Violet"),
                mensaje_despertar=_qc("vq04d_botonlisto_despertar", lambda: "Tengo que ir a ver a Violet por lo del cosplay" if store.sistema_mensajes.grupo_completado("violet_quest04d_chat") else "Violet me envió un mensaje, debería responderle"),
                trigger_mensaje=("violet_quest04d_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_04_d)

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
        quest_anterior="violet_questprincipal_04_d",
        requisitos=[
            Requisito("deseo", "Necesitas 15 de deseo con Violet", npc_id="violet", valor=15),
        ],
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
                pista=_qc("vq04e_botonlisto_pista", lambda: "Violet ya me contestó, debería ir a hablar con ella" if store.sistema_mensajes.grupo_completado("violet_quest04e_chat") else "Violet me envió un mensaje, debería responderle"),
                que_hacer=_qc("vq04e_botonlisto_quehacer", lambda: "Ir a ver a Violet" if store.sistema_mensajes.grupo_completado("violet_quest04e_chat") else "Responder mensaje de Violet"),
                mensaje_despertar=_qc("vq04e_botonlisto_despertar", lambda: "Tengo que ir a ver a Violet por lo del cosplay" if store.sistema_mensajes.grupo_completado("violet_quest04e_chat") else "Violet me envió un mensaje, debería responderle"),
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
                pista="Las entradas para la Japicon están disponibles",
                que_hacer="Comprar dos entradas para la Japicon",
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
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Ya te pusiste al día con Violet sobre el cosplay",
                que_hacer="Hablar con Violet",
            ),
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
                pista="Esperar a que Violet me hable sobre el cosplay",
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

    _vq9a_sprites_violet = {
        0: "images/characters/casa/idle/idle_violet_casa_hviolet_mañana_rutinabase_grupobase_skinbase.png",
        1: "images/characters/casa/idle/idle_violet_casa_hviolet_tarde_rutinabase_grupobase_skinbase.png",
        2: "images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.png",
        3: "images/characters/casa/idle/idle_violet_casa_hviolet_trasnoche_rutinabase_grupobase_skinbase.png",
    }
    _vq9a_sprites_monica = {
        0: "images/characters/casa/idle/idle_monica_casa_living_mañana_rutinabase_grupobase_skinbase.png",
        1: "images/characters/casa/idle/idle_monica_casa_living_mañana_rutinabase_grupobase_skinbase.png",
        2: "images/characters/casa/idle/idle_monica_casa_hmonica_noche_rutinabase_grupobase_skinbase.png",
        3: "images/characters/casa/idle/idle_monica_casa_hmonica_trasnoche_rutinabase_grupobase_skinbase.png",
    }
    _vq9a_locs_monica = {0: "casa_living", 1: "casa_living", 2: "casa_hmonica", 3: "casa_hmonica"}

    quest_violet_09_a = Quest(
        id="violet_questprincipal_09_a",
        npc_id="violet",
        nombre="Violet enferma",
        descripcion="Violet se pescó una gripe, tengo que cuidarla.",
        numero_quest=20,
        dias_espera=1,
        # BLOQUEADA temporalmente: contenido en desarrollo. La quest queda
        # registrada pero NO se auto-inicia al completar la 08_a. Para reactivar,
        # volver a poner quest_anterior="violet_questprincipal_08_a".
        quest_anterior=None,
        requisitos=[
            Requisito("mensaje", "Leer el mensaje de Tienda Coxplay", grupo_id="tienda_coxplay_q9a_g1"),
        ],
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
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Hay un mensaje de Tienda Coxplay.",
                que_hacer="Leer el mensaje de Tienda Coxplay",
                trigger_mensaje=("tienda_coxplay_q9a_g1", "tienda_coxplay"),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podría ver si Violet necesita algo mientras está enferma.",
                que_hacer=_qc("vq09a_botonlisto_quehacer", lambda: "Ayudar a Violet ({}/3)".format(getattr(store, 'violet_enferma_atencion', 0))),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_09_a)

    # =========================================================================
    # QUEST 11 - Los ruidos nocturnos
    # =========================================================================

    quest_violet_11 = Quest(
        id="violet_questprincipal_11",
        npc_id="violet",
        nombre="Los ruidos nocturnos",
        descripcion="Violet me dijo que estaba intentando hacer cosplays, debería comprarle algunos.",
        numero_quest=11,
        dias_espera=3,
        quest_anterior="violet_questprincipal_09_a",
        requisitos=[
            Requisito("item", "Me falta el conjunto de cosplays", item_id="conjunto_cosplays", cantidad=1),
        ],
        validacion_especial=[
            Requisito("npc_presente", "Violet debe estar en su habitacion", npc_id="violet", locacion_id="casa_hviolet"),
            Requisito("horario", "Debe ser por la noche", horario_id=2),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Todo tranquilo por ahora, debería esperar unos días.",
                que_hacer=_qc("vq11_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_11", 3)),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Podría conseguir algunos cosplay para que Violet se pruebe",
                que_hacer="Comprar el ítem conjunto de cosplay",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podría ir a la habitación de violet por la noche a ver si le gusta lo que compré",
                que_hacer="Ir a la habitación de violet por la noche",
                mensaje_despertar="Podría mostrarle a violet los cosplays que conseguí.",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_11)

    # =========================================================================
    # QUEST 12 - Visita nocturna
    # =========================================================================

    quest_violet_12 = Quest(
        id="violet_questprincipal_12",
        npc_id="violet",
        nombre="Visita nocturna",
        descripcion="Violet me pidió que pase por su habitación a la noche.",
        numero_quest=12,
        dias_espera=3,
        quest_anterior="violet_questprincipal_11",
        requisitos=[],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest12_chat"),
            Requisito("npc_presente", "Violet debe estar en su habitacion", npc_id="violet", locacion_id="casa_hviolet"),
            Requisito("horario", "Debe ser por la noche", horario_id=2),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Debería esperar unos días.",
                que_hacer=_qc("vq12_espera_quehacer", lambda: vq_esperar_texto("violet_questprincipal_12", 3)),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("vq12_botonlisto_pista", lambda: "Violet me pidió que pase por su habitación, debería ir a la noche." if store.sistema_mensajes.grupo_completado("violet_quest12_chat") else "Violet me envió un mensaje, debería responderle."),
                que_hacer=_qc("vq12_botonlisto_quehacer", lambda: "Ir a la habitacion de Violet por la noche." if store.sistema_mensajes.grupo_completado("violet_quest12_chat") else "Responder mensaje de Violet"),
                mensaje_despertar=_qc("vq12_botonlisto_despertar", lambda: "Violet me pidió que pase por su habitación a la noche." if store.sistema_mensajes.grupo_completado("violet_quest12_chat") else "Violet me envió un mensaje, debería responderle"),
                trigger_mensaje=("violet_quest12_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_12)


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

        # Fase 4: dirección de envío
        g4 = _grupo("coxplay_q5a_g4")
        if g4:
            if _completado("coxplay_q5a_g4"):
                dias_restantes = max(0, getattr(store, 'coxplay_pedido_dia', 0) + 2 - getattr(store, 'dias_totales', 0))
                if dias_restantes > 0:
                    return (
                        "Podría hablar con Violet y contarle lo que compré.",
                        "Hablar con Violet / Esperar {} día{} más".format(dias_restantes, "s" if dias_restantes != 1 else ""),
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

        # Fase 3: pago
        g3 = _grupo("coxplay_q5a_g3")
        if g3 and not _completado("coxplay_q5a_g3"):
            if getattr(store, 'dinero', 0) >= 200:
                return (
                    "Tengo que confirmar el pago del cosplay.",
                    "Confirmar pago ($200) en Tienda CoXplay",
                    "Hoy puedo confirmar el pago del cosplay en el chat.",
                )
            return (
                "Necesito $200 para pagar el cosplay.",
                "Juntar $200 para abonar a CoXplay",
                "Necesito ahorrar $200 para pagar el pedido a CoXplay.",
            )

        # Fase 2: conversacion principal
        g2 = _grupo("coxplay_q5a_g2")
        if g2:
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
        Activa la restricción de auto-trigger para la quest 04_b de Violet.
        Se llama como accion_al_entrar cuando la quest alcanza ETAPA_BOTON_LISTO.
        Registra labels en todas las locaciones posibles de Violet.
        Los NPCs siguen siendo interactuables normalmente.
        """
        r = activar_restriccion(
            npcs_interactuables=["violet", "jasmine", "monica"],
        )
        for loc_id in ["casa_hviolet", "casa_pasilloarriba", "casa_cocina", "casa_living", "casa_gym"]:
            r.registrar_label_locacion(loc_id, "violet_quest04b_check_locacion")