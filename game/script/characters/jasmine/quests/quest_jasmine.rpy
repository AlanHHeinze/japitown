################################################################################
## Quests de Jasmine
################################################################################
## Archivo principal con definiciones de quest
## Los labels de cada quest estan en archivos separados (jasmine_quest_X.rpy)

init 5 python:

    # =========================================================================
    # QUEST 0_a - Reencuentro con Jasmine (Jasmine)
    # =========================================================================
    # Sin tiempo de espera, sin requisitos
    # Disponible en: Gym, Tarde
    # Label en: jasmine_quest_0.rpy

    quest_jasmine_0a = Quest(
        id="jasmine_questprincipal_0_a",
        npc_id="jasmine",
        nombre="Reencuentro con Jasmine",
        descripcion="Quiero hablar con Jasmine para ponerme al día luego de tanto tiempo",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        mensaje_pista="Me gustaría ponerme al día con Jasmine, podría hablar con ella cuando está sola en el Gym",
        mensaje_despertar="Jasmine suele entrenar en el Gym por la tarde, podría ir a verla y aprovechar el momento para hablar",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podría ver a Jasmine por la tarde cuando entrena y hablar un poco",
                que_hacer="Hablar con Jasmine en el Gym por la tarde",
                mensaje_despertar="Jasmine suele entrenar en el Gym por la tarde, podría ir a verla y aprovechar el momento para hablar",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_jasmine_0a)

    # =========================================================================
    # QUEST 0_b - Respondiendo a Carl
    # =========================================================================

    quest_jasmine_0b = Quest(
        id="jasmine_questprincipal_0_b",
        npc_id="jasmine",
        nombre="Mensaje de Carl",
        descripcion="Tengo un mensaje de mi amigo Carl",
        numero_quest=0,
        dias_espera=0,
        quest_anterior="jasmine_questprincipal_0_a",
        requisitos=[],
        mensaje_pista="Responder el mensaje de Carl.",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Responder el mensaje de Carl",
                que_hacer="Responder los mensajes de Carl en el chat del celular",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_jasmine_0b)

    # =========================================================================
    # QUEST 0_c - Mostrando Ropa Deportiva (Evento convertido)
    # =========================================================================

    quest_jasmine_0c = Quest(
        id="jasmine_questprincipal_0_c",
        npc_id="jasmine",
        nombre="El regalo de Jasmine",
        descripcion="Jasmine quiere mostrarme cómo le queda el conjunto deportivo que le traje",
        numero_quest=0,
        dias_espera=0,
        quest_anterior="jasmine_questprincipal_0_b",
        requisitos=[],
        mensaje_pista="Jasmine quiere mostrar su nueva ropa deportiva.",
        mensaje_despertar="Jasmine quiere que vea cómo le queda el conjunto deportivo que le regalé, podría pasar a la tarde por el Gym",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Jasmine quiere mostrar su nueva ropa deportiva.",
                que_hacer="Ver lo que Jasmine quiere mostrar.",
                mensaje_despertar="Jasmine quiere que vea cómo le queda el conjunto deportivo que le regalé, podría pasar a la tarde por el Gym",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_jasmine_0c)
