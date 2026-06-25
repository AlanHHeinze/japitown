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
        descripcion="Quiero hablar con Jasmine para ponerme al dia luego de tanto tiempo",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        validacion_especial=[
            Requisito("locacion", "Debes estar en el gym", locacion_id="casa_gym"),
            Requisito("horario", "Debe ser por la tarde", horario_id=1)
        ],
        mensaje_pista="Me gustaria ponerme al dia con Jasmine, podria hablar con ella cuando esta sola en el Gym",
        mensaje_despertar="Jasmine suele entrenar en el Gym por la tarde, podria ir a verla y aprovechar el momento para hablar",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podria ver a Jasmine por la tarde cuando entrena y hablar un poco",
                que_hacer="Hablar con Jasmine en el Gym por la tarde",
                mensaje_despertar="Jasmine suele entrenar en el Gym por la tarde, podria ir a verla y aprovechar el momento para hablar",
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
        validacion_especial=[],
        mensaje_pista="Responder el mensaje de Carl.",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Responder el mensaje de Carl",
                que_hacer="Entrar a la App Chat y responde los mensajes de Carl",
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
        descripcion="Jasmine quiere mostrarme como el conjunto deportivo que le traje",
        numero_quest=0,
        dias_espera=0,
        quest_anterior="jasmine_questprincipal_0_b",
        requisitos=[],
        validacion_especial=[],
        mensaje_pista="Jasmine quiere mostrar su nueva ropa deportiva.",
        mensaje_despertar="Jasmine quiere que vea como le queda el conjunto deportivo que le regale, podria pasar a la tarde por el gym",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Jasmine quiere mostrar su nueva ropa deportiva.",
                que_hacer="Ver lo que Jasmine quiere mostrar.",
                mensaje_despertar="Jasmine quiere que vea como le queda el conjunto deportivo que le regale, podria pasar a la tarde por el gym",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_jasmine_0c)
