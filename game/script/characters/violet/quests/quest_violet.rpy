################################################################################
## Quests de Violet
################################################################################
## Archivo principal con definiciones de quest
## Los labels de cada quest están en archivos separados (violet_quest_X.rpy)

init 5 python:

    # =========================================================================
    # QUEST 0 - ¿Que le pasa a Violet? (Violet)
    # =========================================================================

    quest_violet_0 = Quest(
        id="violet_questprincipal_0",
        npc_id="violet",
        nombre="¿Que le pasa a Violet?",
        descripcion="Violet me ignoró desde que llegué, debería hablar con ella.",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        validacion_especial=[
            Requisito("npc_presente", "Violet debe estar en su habitación", npc_id="violet", locacion_id="casa_hviolet"),
            Requisito("horario", "Debe ser por la tarde", horario_id=1)
        ],
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

    quest_violet_1 = Quest(
        id="violet_questprincipal_1",
        npc_id="violet",
        nombre="Un paquete misterioso",
        descripcion="Parece que llegó algo para mí.",
        numero_quest=1,
        dias_espera=3,
        condicion_espera=lambda: len(sistema_compras.verificar_entregas_hoy()) == 0,
        quest_anterior="violet_questprincipal_0",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Todo tranquilo por ahora",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_1').dia_inicio or 0))),
                    "ia" if max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_1').dia_inicio or 0))) == 1 else "ias"
                ),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=lambda: _pista_quest1_violet(),
                que_hacer=lambda: _quehacer_quest1_violet(),
                mensaje_despertar=lambda: "Escuche el timbre" if getattr(store, 'violet_quest1_entrega_pendiente', False) else "",
                accion_al_entrar=lambda: setup_entrega_quest1_violet(),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_1)

    # =========================================================================
    # QUEST 2 NUEVA - El contenido del paquete (Violet)
    # =========================================================================

    quest_violet_2_nueva = Quest(
        id="violet_questprincipal_2",
        npc_id="violet",
        nombre="El contenido del paquete",
        descripcion="Tengo un paquete que parece ser de Violet, podría dárselo o ver qué tiene.",
        numero_quest=2,
        dias_espera=0,
        quest_anterior="violet_questprincipal_1",
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
    sistema_quests.registrar_quest(quest_violet_2_nueva)

    # =========================================================================
    # QUEST 4 - Limpieza del Sábado (Violet)
    # =========================================================================

    quest_violet_4 = Quest(
        id="violet_questprincipal_4",
        npc_id="violet",
        nombre="Limpieza del Sábado",
        descripcion="Monica me pidió que limpie la casa con Violet el sábado por la mañana.",
        numero_quest=4,
        dias_espera=4,
        quest_anterior="violet_questprincipal_2",
        requisitos=[
            Requisito("mensaje", "Contestar el mensaje de Monica", grupo_id="monica_chat_violet_quest2"),
        ],
        validacion_especial=[
            Requisito("dia", "Debe ser sábado", dia_id=5),
            Requisito("horario", "Debe ser por la mañana", horario_id=0),
            Requisito("npc_presente", "Violet debe estar en su habitación", npc_id="violet", locacion_id="casa_hviolet"),
        ],
        rutina_quest={
            (5, 0): RutinaQuest(
                locacion="casa_hviolet",
                sprite="images/characters/casa/idle/idle_violet_casa_hviolet_mañana_rutinabase_grupobase_skinbase.png",
                posicion=(800, 700)
            ),
        },
        rutinas_adicionales={
            "monica": {
                (5, 0): RutinaQuest(locacion="fuera"),
            },
            "jasmine": {
                (5, 0): RutinaQuest(locacion="fuera"),
            },
        },
        prioridad_rutina=0,
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Monica me dijo algo sobre limpiar la casa, tengo que esperar.",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 4 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_4').dia_inicio or 0))),
                    "ia" if max(1, 4 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_4').dia_inicio or 0))) == 1 else "ias"
                ),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Deberia responderle a Monica.",
                que_hacer="Responder mensaje de Monica.",
                trigger_mensaje=("violet_quest2_chat_monica", "monica"),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=lambda: "Hoy es sábado, tengo que despertar a Violet temprano." if getattr(store, 'dia_semana_actual', 0) == 5 else "Monica me pidió que despierte a Violet temprano el sábado para limpiar la casa.",
                que_hacer=lambda: "Ir a la habitación de Violet por la mañana." if getattr(store, 'dia_semana_actual', 0) == 5 else "Esperar hasta el sabado por la mañana.",
                mensaje_despertar=lambda: "Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa." if getattr(store, 'dia_semana_actual', 0) == 5 else "",
            ),
        },
        config_fallo=ConfigFallo(
            condicion=lambda: getattr(store, 'dia_semana_actual', 0) == 5 and getattr(store, 'horario_actual', 0) == 1,
            trigger_mensaje=("violet_quest2_fallo", "monica"),
            cambio_relacion=("monica", -1),
            pista="El próximo sábado debería ocuparme de la limpieza.",
            que_hacer=lambda: "Esperar hasta el próximo sábado por la mañana.",
        ),
    )

    # =========================================================================
    # QUEST 5 - Solo en casa (Violet)
    # =========================================================================

    quest_violet_5 = Quest(
        id="violet_questprincipal_5",
        npc_id="violet",
        nombre="Solo en casa",
        descripcion="Hoy estoy solo en la casa, podría aprovechar el tiempo.",
        numero_quest=5,
        dias_espera=3,
        quest_anterior="violet_questprincipal_4",
        requisitos=[],
        validacion_especial=[],
        rutinas_adicionales={
            "violet": {
                (0, 0): RutinaQuest(locacion="fuera"),
                (1, 0): RutinaQuest(locacion="fuera"),
                (2, 0): RutinaQuest(locacion="fuera"),
                (3, 0): RutinaQuest(locacion="fuera"),
                (4, 0): RutinaQuest(locacion="fuera"),
                (5, 0): RutinaQuest(locacion="fuera"),
                (6, 0): RutinaQuest(locacion="fuera"),
            },
            "monica": {
                (0, 0): RutinaQuest(locacion="fuera"),
                (1, 0): RutinaQuest(locacion="fuera"),
                (2, 0): RutinaQuest(locacion="fuera"),
                (3, 0): RutinaQuest(locacion="fuera"),
                (4, 0): RutinaQuest(locacion="fuera"),
                (5, 0): RutinaQuest(locacion="fuera"),
                (6, 0): RutinaQuest(locacion="fuera"),
            },
            "jasmine": {
                (0, 0): RutinaQuest(locacion="fuera"),
                (1, 0): RutinaQuest(locacion="fuera"),
                (2, 0): RutinaQuest(locacion="fuera"),
                (3, 0): RutinaQuest(locacion="fuera"),
                (4, 0): RutinaQuest(locacion="fuera"),
                (5, 0): RutinaQuest(locacion="fuera"),
                (6, 0): RutinaQuest(locacion="fuera"),
            },
        },
        prioridad_rutina=0,
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Todo tranquilo por ahora.",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_5').dia_inicio or 0))),
                    "ia" if max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_5').dia_inicio or 0))) == 1 else "ias"
                ),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Hoy estoy solo en la casa.",
                que_hacer="Esperar al día siguiente.",
                accion_al_entrar=lambda: setattr(store, 'violet_quest5_inicio_pendiente', True),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_5)
    sistema_quests.registrar_quest(quest_violet_4)

    # =========================================================================
    # QUEST 6 - El cosplay de Violet
    # =========================================================================

    quest_violet_6 = Quest(
        id="violet_questprincipal_6",
        npc_id="violet",
        nombre="El cosplay de Violet",
        descripcion="Podría preguntarle a Violet si se probó el cosplay.",
        numero_quest=6,
        dias_espera=3,
        quest_anterior="violet_questprincipal_5",
        requisitos=[],
        validacion_especial=[],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Recuerdo lo del cosplay, deberia esperar unos dias.",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_6').dia_inicio or 0))),
                    "ia" if max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_6').dia_inicio or 0))) == 1 else "ias"
                ),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Cuando encuentre a Violet podría ver si se probó el cosplay",
                que_hacer="Hablar con Violet",
                mensaje_despertar="Podría preguntarle a Violet si se probó el cosplay",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_6)

    # =========================================================================
    # QUEST 7 - El cosplay de Violet II (deseo 20)
    # =========================================================================

    quest_violet_7 = Quest(
        id="violet_questprincipal_7",
        npc_id="violet",
        nombre="El cosplay de Violet II",
        descripcion="Violet tiene vergüenza de mostrarme el cosplay, tengo que mejorar mi deseo con ella.",
        numero_quest=7,
        dias_espera=0,
        quest_anterior="violet_questprincipal_6",
        requisitos=[
            Requisito("deseo", "Necesitas mas deseo con Violet", npc_id="violet", valor=20),
        ],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest7_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Deberia esperar unos dias antes de hablar con Violet sobre el cosplay.",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 4 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_7').dia_inicio or 0))),
                    "ia" if max(1, 4 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_7').dia_inicio or 0))) == 1 else "ias"
                ),
            ),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Violet tiene vergüenza de mostrarme el cosplay, tengo que mejorar mi deseo con ella",
                que_hacer=lambda: renpy.translate_string("Subir deseo con Violet ({}/{})").format(
                    getattr(store, 'violet_deseo', 0), 20
                ),
                mensaje_despertar="Violet tiene vergüenza de mostrarme el cosplay, tengo que mejorar mi deseo con ella",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=lambda: "Violet ya me contestó, debería ir a hablar con ella." if store.sistema_mensajes.grupo_completado("violet_quest7_chat") else "Violet me envió un mensaje, debería responderle.",
                que_hacer=lambda: "Ir a ver a Violet a su habitación." if store.sistema_mensajes.grupo_completado("violet_quest7_chat") else "Responder mensaje de Violet",
                mensaje_despertar=lambda: "Tengo que ir a ver a Violet por lo de su cosplay." if store.sistema_mensajes.grupo_completado("violet_quest7_chat") else "Violet me envió un mensaje, debería responderle",
                trigger_mensaje=("violet_quest7_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_7)

    # =========================================================================
    # QUEST 8 - El cosplay de Violet III (deseo 25)
    # =========================================================================

    quest_violet_8 = Quest(
        id="violet_questprincipal_8",
        npc_id="violet",
        nombre="El cosplay de Violet III",
        descripcion="Quizás si sigo mejorando mi deseo con Violet me muestre un poco más.",
        numero_quest=8,
        dias_espera=0,
        quest_anterior="violet_questprincipal_7",
        requisitos=[
            Requisito("deseo", "Necesitas mas deseo con Violet", npc_id="violet", valor=25),
        ],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest8_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Quizás si sigo mejorando mi deseo con Violet me muestre un poco más",
                que_hacer=lambda: renpy.translate_string("Subir deseo con Violet ({}/{})").format(
                    getattr(store, 'violet_deseo', 0), 25
                ),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=lambda: "Violet ya me contestó, debería ir a hablar con ella." if store.sistema_mensajes.grupo_completado("violet_quest8_chat") else "Violet me envió un mensaje, debería responderle.",
                que_hacer=lambda: "Ir a ver a Violet a su habitación." if store.sistema_mensajes.grupo_completado("violet_quest8_chat") else "Responder mensaje de Violet",
                mensaje_despertar=lambda: "Tengo que ir a ver a Violet por lo de su cosplay." if store.sistema_mensajes.grupo_completado("violet_quest8_chat") else "Violet me envió un mensaje, debería responderle",
                trigger_mensaje=("violet_quest8_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_8)

    # =========================================================================
    # QUEST 9 - El cosplay de Violet IV (deseo 30)
    # =========================================================================

    quest_violet_9 = Quest(
        id="violet_questprincipal_9",
        npc_id="violet",
        nombre="El cosplay de Violet IV",
        descripcion="Quizás si sigo mejorando mi deseo con Violet me muestre un poco más.",
        numero_quest=9,
        dias_espera=0,
        quest_anterior="violet_questprincipal_8",
        requisitos=[
            Requisito("deseo", "Necesitas mas deseo con Violet", npc_id="violet", valor=30),
        ],
        validacion_especial=[
            Requisito("mensaje", "Responder el mensaje de Violet", grupo_id="violet_quest9_chat"),
        ],
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Quizás si sigo mejorando mi deseo con Violet me muestre un poco más",
                que_hacer=lambda: renpy.translate_string("Subir deseo con Violet ({}/{})").format(
                    getattr(store, 'violet_deseo', 0), 30
                ),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=lambda: "Violet ya me contestó, debería ir a hablar con ella." if store.sistema_mensajes.grupo_completado("violet_quest9_chat") else "Violet me envió un mensaje, debería responderle.",
                que_hacer=lambda: "Ir a ver a Violet a su habitación." if store.sistema_mensajes.grupo_completado("violet_quest9_chat") else "Responder mensaje de Violet",
                mensaje_despertar=lambda: "Tengo que ir a ver a Violet por lo de su cosplay." if store.sistema_mensajes.grupo_completado("violet_quest9_chat") else "Violet me envió un mensaje, debería responderle",
                trigger_mensaje=("violet_quest9_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_9)

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
        quest_anterior="violet_questprincipal_10",
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
                pista="Todo tranquilo por ahora, deberia esperar unos dias.",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_11').dia_inicio or 0))),
                    "ia" if max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_11').dia_inicio or 0))) == 1 else "ias"
                ),
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
                pista="Deberia esperar unos dias.",
                que_hacer=lambda: "Esperar {} d{}".format(
                    max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_12').dia_inicio or 0))),
                    "ia" if max(1, 3 - (getattr(store, 'dias_totales', 1) - (sistema_quests.obtener_quest('violet_questprincipal_12').dia_inicio or 0))) == 1 else "ias"
                ),
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=lambda: "Violet me pidió que pase por su habitación, debería ir a la noche." if store.sistema_mensajes.grupo_completado("violet_quest12_chat") else "Violet me envió un mensaje, debería responderle.",
                que_hacer=lambda: "Ir a la habitacion de Violet por la noche." if store.sistema_mensajes.grupo_completado("violet_quest12_chat") else "Responder mensaje de Violet",
                mensaje_despertar=lambda: "Violet me pidió que pase por su habitación a la noche." if store.sistema_mensajes.grupo_completado("violet_quest12_chat") else "Violet me envió un mensaje, debería responderle",
                trigger_mensaje=("violet_quest12_chat", "violet"),
            ),
        },
    )
    sistema_quests.registrar_quest(quest_violet_12)