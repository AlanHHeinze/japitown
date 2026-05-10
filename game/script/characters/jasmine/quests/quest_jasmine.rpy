################################################################################
## Quests de Jasmine
################################################################################
## Archivo principal con definiciones de quest
## Los labels de cada quest están en archivos separados (jasmine_quest_X.rpy)

init 5 python:
    
    # =========================================================================
    # QUEST 0 - Reencuentro con Jasmine (Jasmine)
    # =========================================================================
    # Sin tiempo de espera, sin requisitos
    # Disponible en: Gym, Tarde
    # Label en: jasmine_quest_0.rpy
    
    quest_jasmine_0 = Quest(
        id="jasmine_questprincipal_0",
        npc_id="jasmine",
        nombre="Reencuentro con Jasmine",
        descripcion="Ponerme al dia con Jasmine.",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        validacion_especial=[
            Requisito("locacion", "Debes estar en el gym", locacion_id="casa_gym"),
            Requisito("horario", "Debe ser por la tarde", horario_id=1)
        ],
        mensaje_pista="Podria ver a Jasmine por la tarde cuando entrena y hablar un poco.",
        mensaje_despertar="Podria buscar a Jasmine cuando este entrenando para hablar con ella.",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Podria ver a Jasmine por la tarde cuando entrena y hablar un poco.",
                que_hacer="Ir al gym por la tarde.",
                mensaje_despertar="Podria buscar a Jasmine cuando este entrenando para hablar con ella.",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_jasmine_0)
