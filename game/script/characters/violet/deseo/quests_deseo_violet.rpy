################################################################################
## Violet — LINEA DE DESEO
################################################################################
## Una quest cada 5 puntos de deseo: 5, 10, 15, 20, 25, 30.
## Misma maquinaria que la linea de Amor (ver amor/quests_amor_violet.rpy); lo
## unico que cambia es el stat que mide el Requisito y la linea declarada.
##
## QUE DESBLOQUEA cada quest NO se declara acá. Las de umbral 10, 20 y 30
## otorgan un HITO, y el hito es el que lleva las ventajas: ver
## characters/violet/hitos_violet.rpy, donde el Hito referencia la quest por su
## `quest_id`. Las de 5, 15 y 25 no otorgan hito (son escalones intermedios).
##
## Disparador: UN solo boton por quest en el menu de Violet.

init python:

    def _quehacer_deseo_violet(umbral):
        """Texto de progreso 'Subir deseo (3/5)'. Funcion de modulo: la usan las
        lambdas de _qc, que son las que quedan guardadas."""
        return renpy.translate_string("Subir deseo 💋 con Violet ({}/{})").format(
            getattr(store, 'violet_deseo', 0), umbral)

    def _crear_quest_deseo_violet(numero, umbral, nombre, descripcion, anterior):
        """
        Arma y registra una quest de la linea de deseo.

        El texto dinamico va con _qc(clave, lambda): guarda solo la clave, asi
        que el Quest queda picklable (regla 3 del skill).
        """
        _quest = Quest(
            id="violet_deseo_{:02d}".format(numero),
            npc_id="violet",
            linea=LINEA_DESEO,
            nombre=nombre,
            descripcion=descripcion,
            numero_quest=numero,
            dias_espera=0,
            quest_anterior=anterior,
            requisitos=[
                Requisito("deseo",
                          "Necesitas {} 💋 con Violet".format(umbral),
                          npc_id="violet", valor=umbral),
            ],
            validacion_especial=[],
            retorno=ConfiguracionRetorno(avanzar_dia=False),
            config_etapas={
                ETAPA_CONDICIONES: ConfigEtapa(
                    pista="Todavia hay margen para que esto avance.",
                    que_hacer=_qc("vd{:02d}_qh".format(numero),
                                  lambda u=umbral: _quehacer_deseo_violet(u)),
                ),
                ETAPA_BOTON_LISTO: ConfigEtapa(
                    pista="Es momento de hablar con Violet.",
                    que_hacer="Hablar con Violet",
                ),
            },
        )
        sistema_quests.registrar_quest(_quest)
        return _quest


init 5 python:

    # (numero, umbral, nombre, descripcion, quest_anterior)
    # Las de umbral 10, 20 y 30 son las que otorgan hito.
    _VIOLET_DESEO_QUESTS = [
        (1,  5,  "Otra mirada",        "Algo cambio en como Violet me mira.",      None),
        (2,  10, "Me atrae",           "Hay una tension distinta entre los dos.",  "violet_deseo_01"),
        (3,  15, "Sin disimular",      "Ya casi no lo escondemos.",                "violet_deseo_02"),
        (4,  20, "Confesión",          "Nos dijimos lo que estaba pasando.",       "violet_deseo_03"),
        (5,  25, "Sin rodeos",         "Con Violet ya no hace falta rodear nada.", "violet_deseo_04"),
        (6,  30, "Un paso más allá",   "La relacion cambio de forma definitiva.",  "violet_deseo_05"),
    ]

    for _n, _u, _nom, _desc, _ant in _VIOLET_DESEO_QUESTS:
        _crear_quest_deseo_violet(_n, _u, _nom, _desc, _ant)
