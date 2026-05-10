################################################################################
## Quests de Mónica
################################################################################
## Archivo principal con definiciones de quest
## Los labels de cada quest están en archivos separados (monica_quest_X.rpy)

init 5 python:
    
    # =========================================================================
    # QUEST 0 - Bienvenido a casa (Mónica)
    # =========================================================================
    
    quest_monica_0 = Quest(
        id="monica_questprincipal_0",
        npc_id="monica",
        nombre="Bienvenido a casa",
        descripcion="Monica quiere hablar para darme la bienvenida a casa.",
        numero_quest=0,
        dias_espera=0,
        requisitos=[],
        validacion_especial=[
            Requisito("locacion", "Debes estar en el living", locacion_id="casa_living"),
            Requisito("horario", "Debe ser por la tarde", horario_id=1)
        ],
        mensaje_pista="Tendría que encontrarme con Monica para darle las gracias, podría verla por la tarde.",
        mensaje_despertar="Podría aprovechar que Monica está en casa para hablar con ella.",
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista="Tendría que encontrarme con Monica para darle las gracias, podría verla por la tarde.",
                que_hacer="Ir al living por la tarde.",
                mensaje_despertar="Podría aprovechar que Monica está en casa para hablar con ella.",
            ),
        },
    )
    sistema_quests.registrar_quest(quest_monica_0)