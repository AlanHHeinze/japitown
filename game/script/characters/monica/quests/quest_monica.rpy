################################################################################
## Quests de Mónica
################################################################################
## Archivo principal con definiciones de quest
## Los labels de cada quest estan en archivos separados (monica_quest_X.rpy)

init 5 python:
    
    # =========================================================================
    # QUEST 0 - Bienvenido a casa (Mónica)
    # =========================================================================
    
    quest_monica_0 = Quest(
        id="monica_questprincipal_0",
        npc_id="monica",
        nombre="Agradecimiento",
        descripcion="Tengo que hablar con Mónica para agradecerle la oportunidad",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        # El disparo lo controla el botón "Agradecerle" del menú de Mónica
        # (visible solo a solas con ella), no la validación especial de la quest.
        validacion_especial=[],
        mensaje_pista="Debería agradecerle cuando esté a solas con ella",
        mensaje_despertar="Podría agradecerle a Mónica si la encuentro a solas",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Debería agradecerle cuando esté a solas con ella.",
                que_hacer="Hablar con Mónica cuando está sola en el Living por la tarde",
                mensaje_despertar="Todavía tengo que darle las gracias a Mónica por darme un lugar. Podría verla cuando está sola y de paso darle el perfume",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_monica_0)

    # =========================================================================
    # QUEST 0_B - La notebook de Monica
    # =========================================================================

    quest_monica_0b = Quest(
        id="monica_questprincipal_0_b",
        npc_id="monica",
        nombre="Mónica enojada",
        descripcion="Parece que Mónica tiene un problema, ¿qué será?",
        numero_quest=1,
        dias_espera=1,
        quest_anterior="monica_questprincipal_0",
        requisitos=[],
        validacion_especial=[],
        mensaje_pista="Ver qué le pasa a Mónica",
        mensaje_despertar="Escucho que Mónica se está peleando con alguien, debería ver si todo está bien",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(
                pista="Todo tranquilo por ahora",
                que_hacer="Esperar al día siguiente",
                mensaje_despertar="Escucho a Mónica quejarse desde aquí",
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Ver qué le pasa a Mónica",
                que_hacer="Ir al Living",
                mensaje_despertar="Escucho que Mónica se está peleando con alguien, debería ver si todo está bien",
                accion_al_entrar=setup_restriccion_monica_quest0b,
            ),
        },
    )
    sistema_quests.registrar_quest(quest_monica_0b)

    # =========================================================================
    # QUEST 0_C - La batería de la notebook
    # =========================================================================

    quest_monica_0c = Quest(
        id="monica_questprincipal_0_c",
        npc_id="monica",
        nombre="Servicio Técnico",
        descripcion="Tengo la notebook de Monica, debería revisarla en mi habitación",
        numero_quest=2,
        dias_espera=0,
        quest_anterior="monica_questprincipal_0_b",
        requisitos=[],
        validacion_especial=[],
        mensaje_pista="Revisar la notebook de Monica en mi habitación",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Revisar la notebook de Monica en mi habitación",
                que_hacer="Usar el objeto Notebook de Monica desde el inventario, en tu habitación",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_monica_0c)