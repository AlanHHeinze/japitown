################################################################################
## Conversación diaria con Violet
################################################################################
## Pool de preguntas para la interacción "Hablar" con Violet.
## Stats: amor / deseo
## Rotación de asignaciones:
##   P1:  A=amo  B=des  C=per
##   P2:  A=des  B=per  C=amo
##   P3:  A=per  B=amo  C=des
##   P4:  A=amo  B=per  C=des
##   P5:  A=des  B=amo  C=per
##   P6:  A=per  B=des  C=amo
##   P7:  A=amo  B=des  C=per
##   P8:  A=des  B=per  C=amo
##   P9:  A=per  B=amo  C=des
##   P10: A=amo  B=per  C=des
################################################################################

default violet_hablar_indice = 0

init python:

    preguntas_hablar_violet = [

        # P1 — A=com  B=sum  C=per
        {
            "q": "¿Se te perdió algo o me estás mirando?",
            "ops": [
                {"texto": "Solo pasaba por acá.",                               "resp": "Ajá. Seguro pasabas 'por acá' justo donde estoy yo.", "stat": "amor"},
                {"texto": "Me quedé mirando sin querer, disculpá.",              "resp": "Está bien. Al menos sos honesto.", "stat": "deseo"},
                {"texto": "Estaba pensando en otra cosa.",                       "resp": "Eso espero.", "stat": "amor"},
            ]
        },

        # P2 — A=sum  B=per  C=com
        {
            "q": "¿Te molesta el ruido cuando estoy con la música?",
            "ops": [
                {"texto": "Para nada, ponela tranquila.",                        "resp": "Es la primera vez que alguien no se queja.", "stat": "deseo"},
                {"texto": "Depende del volumen, la verdad.",                     "resp": "Tiene sentido. Voy a tratar de no pasarme.", "stat": "amor"},
                {"texto": "A veces hasta me gusta, suena bien.",                 "resp": "...Gracias. No me lo esperaba.", "stat": "amor"},
            ]
        },

        # P3 — A=per  B=com  C=sum
        {
            "q": "¿Cómo te llevás con la gente de esta casa?",
            "ops": [
                {"texto": "Más o menos, cada uno tiene su onda.",                "resp": "Eso es bastante acertado.", "stat": "amor"},
                {"texto": "Bien, me llevo bien con todos, incluida vos.",        "resp": "Incluida yo, claro. Qué generoso.", "stat": "amor"},
                {"texto": "Intento no molestar a nadie, nada más.",              "resp": "Eso ya es mucho más de lo que hacen otros.", "stat": "deseo"},
            ]
        },

        # P4 — A=com  B=per  C=sum
        {
            "q": "¿Te aburre mucho estar acá sin hacer nada?",
            "ops": [
                {"texto": "Mientras pase algo interesante, me banco.",           "resp": "Depende de lo que cuente como 'interesante'.", "stat": "amor"},
                {"texto": "A veces sí, pero me entretengo solo.",                "resp": "Autosuficiente. Eso es raro por acá.", "stat": "amor"},
                {"texto": "Un poco, pero no me quejo.",                          "resp": "Hm. Hay gente que se quejaría igual.", "stat": "deseo"},
            ]
        },

        # P5 — A=sum  B=com  C=per
        {
            "q": "¿Por qué viniste a hablarme hoy?",
            "ops": [
                {"texto": "Porque quería ver cómo estabas.",                     "resp": "...Eso es inesperado.", "stat": "deseo"},
                {"texto": "¿Necesito un motivo?",                               "resp": "No. Pero no mucha gente viene sin uno.", "stat": "amor"},
                {"texto": "Estaba desocupado, nada más.",                        "resp": "Al menos sos sincero. Eso se valora.", "stat": "amor"},
            ]
        },

        # P6 — A=per  B=sum  C=com
        {
            "q": "¿Te molesta cuando alguien no habla mucho?",
            "ops": [
                {"texto": "No. A veces el silencio dice más que mil palabras.",  "resp": "Eso suena a frase de póster, pero… sí.", "stat": "amor"},
                {"texto": "Prefiero escuchar antes que hablar de más.",          "resp": "Eso es más raro de lo que crees.", "stat": "deseo"},
                {"texto": "Depende de la persona. Con vos no me jode.",          "resp": "...Bueno. Eso fue inesperado.", "stat": "amor"},
            ]
        },

        # P7 — A=com  B=sum  C=per
        {
            "q": "¿Alguna vez sentiste que nadie te entiende?",
            "ops": [
                {"texto": "A veces, pero creo que a todos nos pasa.",            "resp": "Puede ser. Aunque no todos lo reconocen.", "stat": "amor"},
                {"texto": "Sí. Pero aprendí a no depender de eso.",              "resp": "Eso es… bastante fuerte.", "stat": "deseo"},
                {"texto": "No mucho, la verdad. Pero lo entiendo.",              "resp": "Qué suerte.", "stat": "amor"},
            ]
        },

        # P8 — A=sum  B=per  C=com
        {
            "q": "¿Qué pensarías si te digo que no confío en casi nadie?",
            "ops": [
                {"texto": "Lo entiendo. Confianza se gana, no se pide.",         "resp": "...Exacto.", "stat": "deseo"},
                {"texto": "Cada uno tiene sus motivos. No juzgo.",               "resp": "Eso está bien.", "stat": "amor"},
                {"texto": "Ojalá con el tiempo puedas confiar en mí.",           "resp": "...Vamos a ver.", "stat": "amor"},
            ]
        },

        # P9 — A=per  B=com  C=sum
        {
            "q": "¿Hay algo que te gustaría cambiar de cómo vivís acá?",
            "ops": [
                {"texto": "Todo cambio empieza por uno mismo.",                  "resp": "Eso suena a consejo de coach, pero tiene razón.", "stat": "amor"},
                {"texto": "Tal vez pasar más tiempo con la gente de la casa.",   "resp": "...Interesante.", "stat": "amor"},
                {"texto": "No mucho. Estoy agradecido con lo que hay.",           "resp": "Eso es sano.", "stat": "deseo"},
            ]
        },

        # P10 — A=com  B=per  C=sum
        {
            "q": "¿Te parece que hablamos poco o mucho?",
            "ops": [
                {"texto": "Me gustaría que fuera más.",                          "resp": "...Voy a tenerlo en cuenta.", "stat": "amor"},
                {"texto": "Lo justo y necesario.",                               "resp": "Práctico. Está bien.", "stat": "amor"},
                {"texto": "Lo que vos necesites, me adapto.",                    "resp": "...Eso es raro viniendo de alguien.", "stat": "deseo"},
            ]
        },

    ]


################################################################################
## Label de conversación con Violet
################################################################################

label conversacion_hablar_violet:

    # Restaurar fondo de la locación actual (el HUD fue ocultado antes de entrar)
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_hablando at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    $ _npc_v = obtener_npc("violet")
    $ _indice = store.violet_hablar_indice % len(preguntas_hablar_violet)
    $ _preg = preguntas_hablar_violet[_indice]
    $ store.violet_hablar_indice += 1
    $ _op0 = _preg["ops"][0]
    $ _op1 = _preg["ops"][1]
    $ _op2 = _preg["ops"][2]

    $ _txt_op0 = formatear_opcion_recompensa(_op0["texto"], _op0["stat"])
    $ _txt_op1 = formatear_opcion_recompensa(_op1["texto"], _op1["stat"])
    $ _txt_op2 = formatear_opcion_recompensa(_op2["texto"], _op2["stat"])

    violet "[_preg['q']]"

    menu:
        "[_txt_op0]":
            violet "[_op0['resp']]"
            $ _hablar_stat_elegido = _op0["stat"]
        "[_txt_op1]":
            violet "[_op1['resp']]"
            $ _hablar_stat_elegido = _op1["stat"]
        "[_txt_op2]":
            violet "[_op2['resp']]"
            $ _hablar_stat_elegido = _op2["stat"]

    # Bloquear rollback — la recompensa y la conversación no se pueden deshacer
    $ renpy.block_rollback()
    $ _npc_v.modificar_stat(_hablar_stat_elegido, 1)

    hide violet_parada
    hide mc_parado_base

    scene black with fade
    $ avanzar_horario()

    return
