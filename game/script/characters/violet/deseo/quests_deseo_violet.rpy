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

    def _crear_quest_deseo_violet(numero, umbral, nombre, descripcion, anterior,
                                  pista_listo=None, que_hacer_listo=None,
                                  trigger_mensaje_listo=None,
                                  rutina_quest=None, rutinas_adicionales=None,
                                  requisitos_extra=None,
                                  pista_condiciones=None,
                                  que_hacer_condiciones=None):
        """
        Arma y registra una quest de la linea de deseo.

        El texto dinamico va con _qc(clave, lambda): guarda solo la clave, asi
        que el Quest queda picklable (regla 3 del skill).

        pista_listo / que_hacer_listo: overrides de ETAPA_BOTON_LISTO para las
        quests con disparador propio, donde el texto generico no sirve — hay
        que decirle al jugador DONDE y CUANDO (ver _VIOLET_DESEO_TEXTOS).

        trigger_mensaje_listo: tupla (grupo_id, npc_id) para disparar un chat al
        ENTRAR a ETAPA_BOTON_LISTO, o sea justo al alcanzar el umbral. Lo usa la
        quest que se juega entera por chat.

        rutina_quest / rutinas_adicionales: reubican a Violet y a los demas NPCs
        mientras la quest esta activa. El motor las aplica en ETAPA_RUTINA y las
        restaura solas al completar.

        requisitos_extra: requisitos ADEMAS del umbral de deseo. Van en
        `requisitos` y no en `validacion_especial` porque tienen que frenar el
        avance de etapa, no el disparo del boton.

        pista_condiciones / que_hacer_condiciones: overrides de los textos de
        ETAPA_CONDICIONES, para las quests que esperan algo mas que el umbral.
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
            rutina_quest=rutina_quest,
            rutinas_adicionales=rutinas_adicionales,
            requisitos=[
                Requisito("deseo",
                          "Necesitas {} 💋 con Violet".format(umbral),
                          npc_id="violet", valor=umbral),
            ] + list(requisitos_extra or []),
            validacion_especial=[],
            retorno=ConfiguracionRetorno(avanzar_dia=False),
            config_etapas={
                ETAPA_CONDICIONES: ConfigEtapa(
                    pista=pista_condiciones or "Todavia hay margen para que esto avance.",
                    que_hacer=que_hacer_condiciones or _qc(
                        "vd{:02d}_qh".format(numero),
                        lambda u=umbral: _quehacer_deseo_violet(u)),
                ),
                ETAPA_BOTON_LISTO: ConfigEtapa(
                    pista=pista_listo or "Es momento de hablar con Violet.",
                    que_hacer=que_hacer_listo or "Hablar con Violet",
                    trigger_mensaje=trigger_mensaje_listo,
                ),
            },
        )
        sistema_quests.registrar_quest(_quest)
        return _quest


init 5 python:

    # (numero, umbral, nombre, descripcion, quest_anterior)
    # Las de umbral 10, 20 y 30 son las que otorgan hito.
    _VIOLET_DESEO_QUESTS = [
        (1,  5,  "Atracción",          "Algo cambio en como Violet me mira.",      None),
        (2,  10, "Encuentro nocturno", "Hay una tension distinta entre los dos.",  "violet_deseo_01"),
        (3,  15, "Anime en estreno",   "Estrenan el anime que los dos queriamos ver.", "violet_deseo_02"),
        (4,  20, "Pensando en Violet",  "No me la puedo sacar de la cabeza.",       "violet_deseo_03"),
        (5,  25, "En su habitacion",   "Un capitulo de anime en la pieza de Violet.", "violet_deseo_04"),
        (6,  30, "Sinceridad",         "Le dije lo que me pasa y se hizo la desinteresada.", "violet_deseo_05"),
    ]

    # Textos de ETAPA_BOTON_LISTO para las quests que NO se disparan con el
    # boton generico: ahi la pista tiene que indicar donde y cuando pasa la
    # escena, porque no alcanza con "hablar con Violet".
    _VIOLET_DESEO_TEXTOS = {
        1: {
            "pista_listo": "Un encuentro casual con Violet",
            "que_hacer_listo": "Ingresar en el pasillo arriba por la tarde",
        },
        2: {
            "pista_listo": "Deberia descansar bien",
            "que_hacer_listo": "Dormir",
        },
        3: {
            "pista_listo": "Podria usar el sotano para ver el nuevo anime",
            "que_hacer_listo": "Hacer la accion ver tv en el sotano",
        },
        4: {
            # La escena arranca sola al entrar de noche a la habitacion del MC
            # (trigger de game_loop en violet_deseo_20.rpy) y de ahi en mas la
            # quest pasa adentro del celular. NO lleva trigger_mensaje: el chat
            # no se entrega, lo abre el jugador con el boton "Hablar".
            "pista_listo": "Estoy pensando mucho en Violet ultimamente podria escribirle",
            "que_hacer_listo": "Ir de noche a mi habitacion",
        },
        5: {
            "pista_listo": "Podria ver un capitulo de anime con Violet",
            "que_hacer_listo": "Ver TV en el sotano por la noche",
            # Mientras la quest esta activa Violet pasa la noche en su pieza.
            # De lunes a sabado ya lo hacia por rutina base; el unico dia que
            # cambia algo es el domingo (que normalmente estaria en el living).
            # El porque de que sea incondicional esta en violet_deseo_25.rpy.
            "rutina_quest": {
                (dia, 2): RutinaQuest(
                    locacion="casa_hviolet",
                    sprite="images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.jpg",
                    posicion=(1537, 1020),
                ) for dia in range(7)
            },
        },
        6: {
            # Arranca sola de noche estando el MC en SU habitacion y ella libre
            # en la suya, asi que el "que hacer" solo tiene que decir donde.
            "pista_listo": "Hay algo que quiero hablar con Violet",
            "que_hacer_listo": "Estar de noche en mi habitacion",
            # Mientras la quest esta activa Violet pasa la noche en su pieza,
            # que es lo que exige el arranque. De lunes a sabado ya lo hacia por
            # rutina base; el unico dia que cambia algo es el domingo (que
            # normalmente estaria en el living), y sin esto la quest no podria
            # empezar esa noche. Mismo criterio que la de 25.
            "rutina_quest": {
                (dia, 2): RutinaQuest(
                    locacion="casa_hviolet",
                    sprite="images/characters/casa/idle/idle_violet_casa_hviolet_noche_rutinabase_grupopijama_skinbase.jpg",
                    posicion=(1537, 1020),
                ) for dia in range(7)
            },
        },
    }

    # Hasta donde llega el contenido de la linea. La proxima quest de la cadena
    # seria la de 35, que todavia no existe; sin este tope el stat quedaria libre
    # hasta 100 al completar la de 30 y el jugador subiria sin nada que
    # desbloquear. Al crear esa quest, subir el valor o borrar esta linea.
    registrar_tope_provisorio("violet", "deseo", 35)

    for _n, _u, _nom, _desc, _ant in _VIOLET_DESEO_QUESTS:
        _crear_quest_deseo_violet(_n, _u, _nom, _desc, _ant,
            **_VIOLET_DESEO_TEXTOS.get(_n, {}))
