################################################################################
## Jasmine — declaraciones del planificador
################################################################################
## Ver characters/violet/quests/planificacion_violet.rpy para el criterio y
## core/quests/planificador.rpy para el vocabulario.

init 6 python:

    declarar_planificacion("jasmine_questprincipal_0_a",
        disparador=Disp("boton", "Saludar"),
        demandas=[Rec("interaccion", "jasmine"),
                  Rec("npc", "jasmine", horario=1, en="casa_gym")])

    # Mensaje de Carl: el tutorial del celular, encerrado hasta contestar.
    declarar_planificacion("jasmine_questprincipal_0_b",
        disparador=Disp("auto"),
        de_corrido=True, duenio="jasmine_0_b",
        demandas=[Rec("npc", "jasmine"), Rec("celular")])

    declarar_planificacion("jasmine_questprincipal_0_c",
        disparador=Disp("boton", "¿Quería mostrarme algo?"),
        demandas=[Rec("interaccion", "jasmine"),
                  Rec("npc", "jasmine", horario=1, en="casa_gym")])
