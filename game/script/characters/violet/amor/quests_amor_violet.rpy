################################################################################
## Violet — LINEA DE AMOR
################################################################################
## Una quest cada 5 puntos de amor: 5, 10, 15, 20, 25, 30.
##
## Como funciona el encadenamiento:
##   - La primera (amor_01) NO declara quest_anterior: la abre sola
##     inicializar_todas_las_quests(), que arranca toda quest sin predecesora.
##   - Las siguientes encadenan DENTRO de la linea (amor_02 <- amor_01, etc).
##   - El umbral es un Requisito de la propia Quest, asi que la quest queda
##     visible en ETAPA_CONDICIONES mostrando el progreso hasta que el jugador
##     llega.
##
## QUE DESBLOQUEA cada quest NO se declara acá. Las de umbral 10, 20 y 30
## otorgan un HITO, y el hito es el que lleva las ventajas: ver
## characters/violet/hitos_violet.rpy, donde el Hito referencia la quest por su
## `quest_id`. Las de 5, 15 y 25 no otorgan hito (son escalones intermedios).
##
## Disparador: UN solo boton por quest en el menu de Violet
## (ver interactions_violet.rpy).

init python:

    def _quehacer_amor_violet(umbral):
        """Texto de progreso 'Subir amor (3/5)'. Funcion de modulo: la usan las
        lambdas de _qc, que son las que quedan guardadas."""
        return renpy.translate_string("Subir amor ❤️ con Violet ({}/{})").format(
            getattr(store, 'violet_amor', 0), umbral)

    def _crear_quest_amor_violet(numero, umbral, nombre, descripcion, anterior):
        """
        Arma y registra una quest de la linea de amor.

        El texto dinamico va con _qc(clave, lambda): guarda solo la clave, asi
        que el Quest queda picklable (regla 3 del skill). La clave lleva el
        numero de quest para que sea unica.
        """
        _quest = Quest(
            id="violet_amor_{:02d}".format(numero),
            npc_id="violet",
            linea=LINEA_AMOR,
            nombre=nombre,
            descripcion=descripcion,
            numero_quest=numero,
            dias_espera=0,
            quest_anterior=anterior,
            requisitos=[
                Requisito("amor",
                          "Necesitas {} ❤️ con Violet".format(umbral),
                          npc_id="violet", valor=umbral),
            ],
            validacion_especial=[],
            retorno=ConfiguracionRetorno(avanzar_dia=False),
            config_etapas={
                ETAPA_CONDICIONES: ConfigEtapa(
                    pista="Puedo seguir acercandome a Violet.",
                    que_hacer=_qc("va{:02d}_qh".format(numero),
                                  lambda u=umbral: _quehacer_amor_violet(u)),
                ),
                ETAPA_BOTON_LISTO: ConfigEtapa(
                    pista="Es buen momento para hablar con Violet.",
                    que_hacer="Hablar con Violet",
                ),
            },
        )
        sistema_quests.registrar_quest(_quest)
        return _quest


init 5 python:

    # (numero, umbral, nombre, descripcion, quest_anterior)
    # Las de umbral 10, 20 y 30 son las que otorgan hito.
    _VIOLET_AMOR_QUESTS = [
        (1,  5,  "Un acercamiento",  "Empiezo a llevarme mejor con Violet.",      None),
        (2,  10, "Buena relación",   "La relacion con Violet se afianza.",        "violet_amor_01"),
        (3,  15, "Mas confianza",    "Violet se abre un poco mas.",               "violet_amor_02"),
        (4,  20, "Como antes",       "Volvemos a estar como estabamos.",          "violet_amor_03"),
        (5,  25, "Mas cerca",        "Cada vez pasamos mas tiempo juntos.",       "violet_amor_04"),
        (6,  30, "Algo nos pasa",    "Hay algo entre nosotros dificil de negar.", "violet_amor_05"),
    ]

    for _n, _u, _nom, _desc, _ant in _VIOLET_AMOR_QUESTS:
        _crear_quest_amor_violet(_n, _u, _nom, _desc, _ant)
