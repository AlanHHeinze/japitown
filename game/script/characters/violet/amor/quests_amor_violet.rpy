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
        un chat y un dia). Van en `requisitos`: frenan el avance de etapa, no
        el disparo del boton.

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
            retorno=ConfiguracionRetorno(avanzar_dia=False),
            config_etapas={
                ETAPA_CONDICIONES: ConfigEtapa(
                    pista=pista_condiciones or "Puedo seguir acercándome a Violet.",
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
        (2,  10, "Buena relación",   "La relación con Violet se afianza.",        "violet_amor_01"),
        # ⚠️ NOMBRE Y DESCRIPCION PROVISORIOS: el arco viejo ("Juegos Viejos",
        # la Portatil Boy) se mudo a jn_pocketboy.rpy y esta quest se rehizo.
        # Estos textos describen la escena nueva pero conviene reemplazarlos al
        # escribir el dialogo — se ven en el panel de pistas.
        (3,  15, "La visita",        "Violet vino a verme a mi habitación.",      "violet_amor_02"),
        (4,  20, "Jugando juntos",   "Violet y yo terminamos jugando lo mismo.",  "violet_amor_03"),
        (5,  25, "Solos en casa",    "Un domingo entero con Violet y nadie más.", "violet_amor_04"),
        (6,  30, "¿Qué me pongo?",   "Violet quiere mi opinión sobre cómo se ve.", "violet_amor_05"),
        (7,  35, "Las amigas",       "Violet bajó al sótano con sus amigas.",      "violet_amor_06"),
        (8,  40, "La solicitud",     "Una amiga de Violet me agregó en XGram.",     "violet_amor_07"),
        (9,  45, "La regla de la casa", "Lo que hagamos, lo hacemos a solas.",      "violet_amor_08"),
        (10, 50, "El domingo solos",  "Violet se quedó en casa conmigo.",           "violet_amor_09"),
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

    # amor_07 ("Las amigas"): viernes y sabado a la noche —y la trasnoche que
    # sigue— Violet esta en el sotano con Zowie y Leah. La rutina es lo que hace
    # cierta la demanda del controlador (Violet en casa_sotano esa noche) y lo
    # que la sostiene abajo en la fase 2, cuando la escena ya paso pero la quest
    # sigue viva a proposito.
    #
    # SIN SPRITE, y no es un olvido: NO EXISTE un idle de Violet en el sotano, y
    # tampoco hace falta, porque no hay ningun momento en que se la pueda ver
    # ahi. Con la escena pendiente (fases 0 y 1) el trigger salta al entrar,
    # antes de que el HUD dibuje nada; y despues de la escena (fase 2) el sotano
    # esta cerrado con registrar_bloqueo_locacion. Si alguna vez se abre una
    # ventana para bajar y mirar, hay que pedir el asset: sin sprite propio el
    # HUD cae en la rutina visual base y la dibujaria con el idle de su pieza.
    _VIOLET_AMOR_RUTINAS[7] = {
        "rutina_quest": {
            (dia, horario): RutinaQuest(locacion="casa_sotano")
            for dia in (4, 5) for horario in (2, 3)
        },
    }

    # amor_09 ("La regla de la casa"): la escena necesita una mañana que las
    # rutinas base NO producen nunca. Monica esta en la cocina todas las mañanas
    # (el living el sabado) y Jasmine tambien (su habitacion solo el sabado, que
    # es justo el dia en que Monica esta en el living): cero dias posibles. Sin
    # estas rutinas la quest espera para siempre, en verde, sin que nada la
    # desbloquee.
    #
    # Los siete dias, y se acepta el costo: mientras la quest espera el disparo
    # la cocina se queda sin Monica ni Jasmine por la mañana. La quest se juega
    # la primera mañana que el jugador salga al frente; si no sale, es su
    # decision y el panel de Pistas le dice donde y cuando.
    #
    # EL SPRITE DE JASMINE va explicito: su rutina VISUAL base solo tiene la
    # habitacion por la mañana el SABADO, asi que de lunes a viernes y el
    # domingo el HUD la dibujaria con el idle de la cocina. Es el mismo asset,
    # usado los siete dias. Violet en la cocina por la mañana ya es su rutina
    # visual base, asi que no lo necesita.
    _VIOLET_AMOR_RUTINAS[9] = {
        "rutina_quest": {
            (dia, 0): RutinaQuest(locacion="casa_cocina") for dia in range(7)
        },
        "rutinas_adicionales": {
            # "fuera" = no esta en casa: tracker_locacion_npc lo traduce a None
            # y desaparece del mapa. Es lo que hace verdadera su llegada con el
            # paquete.
            "monica": {
                (dia, 0): RutinaQuest(locacion="fuera") for dia in range(7)
            },
            "jasmine": {
                (dia, 0): RutinaQuest(
                    locacion="casa_hjasmine",
                    sprite="images/characters/casa/idle/idle_jasmine_casa_hjasmine_manana_rutinabase_grupobase_skinbase.jpg",
                    posicion=(527, 976),
                ) for dia in range(7)
            },
        },
    }

    # amor_10 ("El domingo solos"): ESE domingo, Monica y Jasmine fuera de la
    # casa los cuatro horarios y Violet adentro.
    #
    # LAS DOS ESTAN "fuera" DESDE EL PRINCIPIO, incluso durante la despedida:
    # en esa escena aparecen como SPRITES, no como idles. Se hace asi por dos
    # motivos — Jasmine no tiene idle del living por la mañana, y sobre todo
    # porque si la rutina las dejara en el living toda la mañana volverian a
    # aparecer paradas ahi despues de haberse despedido (y al cargar un save en
    # el medio de la mañana, peor todavia: _ps_refrescar_quests reaplica las
    # rutinas de las quests vivas).
    #
    # Violet en su habitacion TODO el domingo: la ducha de la fase 2 es
    # narrativa, no se modela (ver la cabecera de violet_amor_50.rpy). Su idle
    # de la habitacion por la mañana ya es su rutina visual base.
    #
    # Las claves llevan dia 6, asi que la rutina solo rige el domingo: si el
    # jugador no cierra la quest ese dia, el lunes las tres vuelven solas.
    _VIOLET_AMOR_RUTINAS[10] = {
        "rutina_quest": {
            (6, h): RutinaQuest(locacion="casa_hviolet") for h in range(4)
        },
        "rutinas_adicionales": {
            "monica": {(6, h): RutinaQuest(locacion="fuera") for h in range(4)},
            "jasmine": {(6, h): RutinaQuest(locacion="fuera") for h in range(4)},
        },
    }

    # amor_08 ("La solicitud"): Violet en su habitacion TODAS LAS NOCHES
    # mientras la quest esta viva.
    #
    # NO es decoracion: en la fase 1 la quest congela el reloj y la unica salida
    # es tocar la puerta de Violet. Su rutina base ya la pone ahi de noche, pero
    # una rutina ESPECIAL (la ducha, o irse de la casa) puede sacarla — y ahi el
    # jugador se queda con el reloj frenado y sin poder cerrar la escena. La
    # rutina de quest le gana a la especial, que es exactamente para lo que
    # existe. Es la regla A9 y la cobra el chequeo 6 de validar_bloqueos.
    #
    # Sin sprite: la habitacion de Violet de noche ya es su rutina visual base,
    # asi que el HUD la dibuja bien sola.
    _VIOLET_AMOR_RUTINAS[8] = {
        "rutina_quest": {
            (dia, 2): RutinaQuest(locacion="casa_hviolet") for dia in range(7)
        },
    }

    # Textos y requisitos propios de las quests que no usan el boton generico.
    _VIOLET_AMOR_TEXTOS = {
        2: {
            # La escena salta sola al entrar al living por la mañana: la pista
            # generica ("Es buen momento para hablar con Violet") mandaba a
            # buscarla en cualquier lado.
            "pista_listo": "Algo está pasando con Violet y Mónica en el living",
        },
        1: {
            # El disparador NO es el boton generico de hablar: es la opcion
            # "Llamarla" del menu de PUERTA, que solo aparece por la tarde y con
            # Violet dentro de su habitacion (_puerta_v_amor_01, en
            # interaction/puertas_violet.rpy). Con el texto generico ("Hablar
            # con Violet") el jugador la buscaba en cualquier lado y a cualquier
            # hora, y la opcion no le aparecia nunca.
            "pista_listo": "Podría pasar por su habitación a la tarde.",
            "que_hacer_listo": "Llamarla desde la puerta de su habitacion por la tarde",
        },
        3: {
            # La escena salta SOLA con el MC en su propia habitacion por la
            # noche (violet_amor_15.rpy). Los textos genericos —"Es buen momento
            # para hablar con Violet" / "Hablar con Violet"— mandarian al
            # jugador a buscarla, que es exactamente lo contrario: hay que
            # quedarse quieto en el cuarto propio y esperar.
            #
            # No dicen que viene Violet a proposito: la gracia de la escena es
            # que aparece sin avisar, y la pista no tiene por que spoilearla.
            "pista_listo": "Podría pasar un rato en mi habitación esta noche.",
            "que_hacer_listo": "Estar en mi habitación por la noche",
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
            # BOTON_LISTO tambien lleva textos propios, y NO son los de "anda a
            # hablar con ella": acá no hay boton. Se llega a esta etapa cuando
            # el jugador alcanza los 25 de amor con el domingo ya empezado, y
            # entonces lo unico que queda es esperar al domingo siguiente. Ver
            # _pista_va25_listo en violet_amor_25.rpy.
            "pista_listo": _pista_va25_listo,
            "que_hacer_listo": _quehacer_va25_listo,
        },
        6: {
            # Sin requisitos ademas del umbral: alcanzado el amor, la quest
            # arranca sola la proxima vez que el MC pase por el pasillo de
            # arriba por la tarde (trigger de game_loop en violet_amor_30.rpy).
            "pista_condiciones": _pista_va30_condiciones,
            "que_hacer_condiciones": _quehacer_va30_condiciones,
            "pista_listo": "Violet quiere mi opinión sobre algo",
            "que_hacer_listo": "Pasar por el pasillo de arriba por la tarde",
        },
        10: {
            # Cinco fases, cinco pedidos distintos: los dos textos salen de un
            # dict por fase (violet_amor_50.rpy).
            "pista_listo": _pista_va50_listo,
            "que_hacer_listo": _quehacer_va50_listo,
        },
        9: {
            # Un solo pedido en toda la quest: salir al frente por la mañana.
            # No tiene fases — la escena corre entera sin devolver el control.
            "pista_listo": _pista_va45_listo,
            "que_hacer_listo": _quehacer_va45_listo,
        },
        8: {
            # Los tres pedidos de la quest (esperar, hablar, escribirle) son
            # fases distintas del mismo BOTON_LISTO, asi que los dos textos son
            # funciones que miran `va40_fase` (violet_amor_40.rpy).
            "pista_listo": _pista_va40_listo,
            "que_hacer_listo": _quehacer_va40_listo,
        },
        7: {
            # El chat avisa una sola vez y no se reenvia si la noche se pierde,
            # asi que LA PISTA ES LA RED: tiene que decir donde y cuando sin
            # depender de que el jugador se acuerde del mensaje. Los dos textos
            # miran `va35_fase` porque en la fase 2 el pedido cambia de "bajar"
            # a "dejarlas tranquilas" (violet_amor_35.rpy).
            "pista_listo": _pista_va35_listo,
            "que_hacer_listo": _quehacer_va35_listo,
        },
    }

    # Hasta donde llega el contenido de la linea. Con la de 50 la rama cierra:
    # el tope queda en 60, que es el umbral del marcador "Proximamente"
    # siguiente. Si la linea no sigue, esta linea se borra y el stat queda
    # libre — pero eso hay que decidirlo, no dejarlo pasar.
    registrar_tope_provisorio("violet", "amor", 60)

    for _n, _u, _nom, _desc, _ant in _VIOLET_AMOR_QUESTS:
        _kwargs_amor = dict(_VIOLET_AMOR_RUTINAS.get(_n, {}))
        _kwargs_amor.update(_VIOLET_AMOR_TEXTOS.get(_n, {}))
        _crear_quest_amor_violet(_n, _u, _nom, _desc, _ant, **_kwargs_amor)


# Ultima quest publicada de la rama. La pantalla de fin de contenido
# (ui/menus/fin_contenido.rpy) sale cuando las tres ramas tienen la suya completa. Al publicar una quest nueva
# despues de esta, se mueve aca.
init 5 python:
    registrar_fin_de_rama("violet_amor_10", _("Rama de amor de Violet"))
