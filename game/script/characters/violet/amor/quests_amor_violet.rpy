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

    def _crear_quest_amor_violet(numero, umbral, nombre, descripcion, anterior,
                                 rutina_quest=None, rutinas_adicionales=None,
                                 requisitos_extra=None,
                                 pista_condiciones=None, que_hacer_condiciones=None,
                                 pista_listo=None, que_hacer_listo=None):
        """
        Arma y registra una quest de la linea de amor.

        El texto dinamico va con _qc(clave, lambda): guarda solo la clave, asi
        que el Quest queda picklable (regla 3 del skill). La clave lleva el
        numero de quest para que sea unica.

        rutina_quest / rutinas_adicionales: solo las usan las quests que
        reubican NPCs mientras estan activas (ver _VIOLET_AMOR_RUTINAS).

        requisitos_extra: requisitos ADEMAS del umbral de amor. Los usa la
        quest que tiene fases propias antes de la escena (ej. la 03, que espera
        un chat y un dia). Van en `requisitos` y no en `validacion_especial`
        porque tienen que frenar el avance de etapa, no el disparo del boton.

        pista_* / que_hacer_*: overrides de los textos genericos, para las
        quests con disparador propio donde "hablar con Violet" no sirve — hay
        que decirle al jugador DONDE y CUANDO (ver _VIOLET_AMOR_TEXTOS).
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
            rutina_quest=rutina_quest,
            rutinas_adicionales=rutinas_adicionales,
            requisitos=[
                Requisito("amor",
                          "Necesitas {} ❤️ con Violet".format(umbral),
                          npc_id="violet", valor=umbral),
            ] + list(requisitos_extra or []),
            validacion_especial=[],
            retorno=ConfiguracionRetorno(avanzar_dia=False),
            config_etapas={
                ETAPA_CONDICIONES: ConfigEtapa(
                    pista=pista_condiciones or "Puedo seguir acercandome a Violet.",
                    que_hacer=que_hacer_condiciones or _qc(
                        "va{:02d}_qh".format(numero),
                        lambda u=umbral: _quehacer_amor_violet(u)),
                ),
                ETAPA_BOTON_LISTO: ConfigEtapa(
                    pista=pista_listo or "Es buen momento para hablar con Violet.",
                    que_hacer=que_hacer_listo or "Hablar con Violet",
                ),
            },
        )
        sistema_quests.registrar_quest(_quest)
        return _quest


init 5 python:

    # (numero, umbral, nombre, descripcion, quest_anterior)
    # Las de umbral 10, 20 y 30 son las que otorgan hito.
    _VIOLET_AMOR_QUESTS = [
        (1,  5,  "¿Mejor?",          "Empiezo a llevarme mejor con Violet.",      None),
        (2,  10, "Buena relación",   "La relacion con Violet se afianza.",        "violet_amor_01"),
        # ⚠️ NOMBRE Y DESCRIPCION PROVISORIOS: el arco viejo ("Juegos Viejos",
        # la Portatil Boy) se mudo a jn_pocketboy.rpy y esta quest se rehizo.
        # Estos textos describen la escena nueva pero conviene reemplazarlos al
        # escribir el dialogo — se ven en el panel de pistas.
        (3,  15, "La visita",        "Violet vino a verme a mi habitacion.",      "violet_amor_02"),
        (4,  20, "Jugando juntos",   "Violet y yo terminamos jugando lo mismo.",  "violet_amor_03"),
        (5,  25, "Solos en casa",    "Un domingo entero con Violet y nadie mas.", "violet_amor_04"),
        (6,  30, "¿Que me pongo?",   "Violet quiere mi opinion sobre como se ve.", "violet_amor_05"),
    ]

    # Quests que ademas REUBICAN NPCs mientras estan activas, por numero de
    # quest. La rutina se aplica al llegar a ETAPA_RUTINA y el motor la restaura
    # sola al completar la quest.
    #
    # amor_02 ("Buena relación"): la escena pasa en el living por la mañana con
    # Violet y Monica. Sin esto las dos seguirian su rutina normal —tipicamente
    # la cocina— y aparecerian en el living de la nada al entrar. Se las mueve
    # aunque casi no se llegue a ver: el jugador que pasa antes por la cocina
    # tiene que encontrarlas donde van a estar.
    _VIOLET_AMOR_RUTINAS = {
        2: {
            "rutina_quest": {
                (dia, 0): RutinaQuest(locacion="casa_living") for dia in range(7)
            },
            "rutinas_adicionales": {
                "monica": {
                    (dia, 0): RutinaQuest(locacion="casa_living") for dia in range(7)
                },
            },
        },
    }

    # (amor_03 no define rutina: la que mandaba a Violet al altillo se fue con
    # el arco viejo a ventajas/juegosnuevos/jn_pocketboy.rpy. La quest 15 nueva
    # declara la suya si la necesita.)

    # amor_05 ("Solos en casa"): el domingo Monica y Jasmine se van de la casa y
    # Violet se queda — su habitacion a la mañana y a la noche, el living por la
    # tarde (que es cuando aparece el boton "Matar el tiempo").
    #
    # Las claves son (dia, horario) y todas llevan dia 6, asi que la rutina solo
    # rige el domingo: si el jugador no cierra la quest ese dia, el lunes los
    # tres vuelven solos a su rutina normal.
    #
    # Los sprites hay que darlos SIEMPRE que se mueve a Violet de donde la pone
    # su rutina base, o se veria el idle del lugar equivocado. Los tres son
    # idles que ya existen; las posiciones estan copiadas de definition_violet.
    _VIOLET_AMOR_RUTINAS[5] = {
        "rutina_quest": {
            (6, 0): RutinaQuest(
                locacion="casa_hviolet",
                sprite="images/characters/casa/idle/idle_violet_casa_hviolet_manana_rutinabase_grupobase_skinbase.jpg",
                posicion=(728, 815),
            ),
            (6, 1): RutinaQuest(
                locacion="casa_living",
                sprite="images/characters/casa/idle/idle_violet_casa_living_tarde_rutinabase_grupobase_skinbase.webp",
                posicion=(549, 991),
            ),
            (6, 2): RutinaQuest(
                locacion="casa_hviolet",
                sprite="images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.jpg",
                posicion=(1537, 1020),
            ),
        },
        "rutinas_adicionales": {
            # "fuera" es el valor que el motor entiende como "no esta en casa":
            # tracker_locacion_npc lo traduce a None y las dos desaparecen del
            # mapa, del tracker y de las locaciones.
            "monica": {(6, h): RutinaQuest(locacion="fuera") for h in range(3)},
            "jasmine": {(6, h): RutinaQuest(locacion="fuera") for h in range(3)},
        },
    }

    # Textos y requisitos propios de las quests que no usan el boton generico.
    _VIOLET_AMOR_TEXTOS = {
        1: {
            # El disparador NO es el boton generico de hablar: es la opcion
            # "Llamarla" del menu de PUERTA, que solo aparece por la tarde y con
            # Violet dentro de su habitacion (_puerta_v_amor_01, en
            # interaction/puertas_violet.rpy). Con el texto generico ("Hablar
            # con Violet") el jugador la buscaba en cualquier lado y a cualquier
            # hora, y la opcion no le aparecia nunca.
            "pista_listo": "Podria pasar por su habitacion a la tarde.",
            "que_hacer_listo": "Llamarla desde la puerta de su habitacion por la tarde",
        },
        3: {
            # La escena salta SOLA con el MC en su propia habitacion por la
            # tarde (violet_amor_15.rpy). Los textos genericos —"Es buen momento
            # para hablar con Violet" / "Hablar con Violet"— mandarian al
            # jugador a buscarla, que es exactamente lo contrario: hay que
            # quedarse quieto en el cuarto propio y esperar.
            #
            # No dicen que viene Violet a proposito: la gracia de la escena es
            # que aparece sin avisar, y la pista no tiene por que spoilearla.
            "pista_listo": "Podria pasar un rato en mi habitacion a la tarde.",
            "que_hacer_listo": "Estar en mi habitacion por la tarde",
        },
        4: {
            # La quest se queda en BOTON_LISTO durante sus tres tramos, asi que
            # los textos son funciones que miran `va20_fase` (violet_amor_20.rpy).
            "pista_listo": _pista_va20_listo,
            "que_hacer_listo": _quehacer_va20_listo,
        },
        5: {
            # El domingo es un Requisito, asi que la quest se queda en
            # CONDICIONES contando los dias que faltan (violet_amor_25.rpy).
            "requisitos_extra": [
                Requisito("dia", "Esperar al domingo", dia_id=6),
            ],
            "pista_condiciones": "Esperar algunos dias",
            "que_hacer_condiciones": _quehacer_va25_condiciones,
            # Sin textos de BOTON_LISTO: la escena arranca sola al despertar el
            # domingo, el jugador no tiene que ir a hacer nada.
        },
        6: {
            # El chat es un Requisito: hasta responderlo la quest se queda en
            # CONDICIONES. Los textos de esa etapa son funciones que miran el
            # stat (violet_amor_30.rpy) — mientras falta amor muestran el
            # contador, y recien despues "esperar que te escriba".
            "requisitos_extra": [
                Requisito("mensaje", "Esperar el mensaje de Violet",
                          grupo_id="violet_amor06_chat"),
            ],
            "pista_condiciones": _pista_va30_condiciones,
            "que_hacer_condiciones": _quehacer_va30_condiciones,
            "pista_listo": "Violet quiere mi opinion sobre algo",
            "que_hacer_listo": "Ir a su habitacion por la noche",
        },
    }

    # Hasta donde llega el contenido de la linea. La proxima quest de la cadena
    # seria la de 35, que todavia no existe; sin este tope el stat quedaria libre
    # hasta 100 al completar la de 30 y el jugador subiria sin nada que
    # desbloquear. Al crear esa quest, subir el valor o borrar esta linea.
    registrar_tope_provisorio("violet", "amor", 35)

    for _n, _u, _nom, _desc, _ant in _VIOLET_AMOR_QUESTS:
        _kwargs_amor = dict(_VIOLET_AMOR_RUTINAS.get(_n, {}))
        _kwargs_amor.update(_VIOLET_AMOR_TEXTOS.get(_n, {}))
        _crear_quest_amor_violet(_n, _u, _nom, _desc, _ant, **_kwargs_amor)
