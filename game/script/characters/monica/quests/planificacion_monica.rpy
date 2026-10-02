################################################################################
## Monica — declaraciones del planificador
################################################################################
## Ver characters/violet/quests/planificacion_violet.rpy para el criterio y
## core/quests/planificador.rpy para el vocabulario.

init 6 python:

    declarar_planificacion("monica_questprincipal_0",
        disparador=Disp("boton", "Agradecerle", nota="a solas con ella"),
        demandas=[Rec("npc", "monica"), Rec("interaccion", "monica")])

    # Monica enojada: el gate (no dormir / no avanzar) lo pone su restriccion
    # mientras esta activa; el planificador lo lee de ahi.
    declarar_planificacion("monica_questprincipal_0_b",
        disparador=Disp("locacion"),
        duenio="monica_0_b",
        demandas=[Rec("npc", "monica"), Rec("locacion", en="casa_living")])

    declarar_planificacion("monica_questprincipal_0_c",
        disparador=Disp("item", "la notebook de Mónica"),
        demandas=[Rec("npc", "monica"), Rec("accion", accion="usar_item")])
