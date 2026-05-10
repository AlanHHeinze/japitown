################################################################################
## Conversación diaria con Mónica
################################################################################
## Pool de preguntas para la interacción "Hablar" con Mónica.
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

default monica_hablar_indice = 0

init python:

    preguntas_hablar_monica = [

        # P1 — A=mad  B=deb  C=per
        {
            "q": "¿Cómo te está yendo por aquí? ¿Te estás adaptando bien?",
            "ops": [
                {"texto": "Bastante bien, poco a poco.",                    "resp": "Me alegra escuchar eso. Ya verás que esto tiene lo suyo.", "stat": "amor"},
                {"texto": "Cuesta un poco, pero voy manejando.",            "resp": "Es normal. No te exijas demasiado.", "stat": "deseo"},
                {"texto": "Más o menos, sigo aprendiendo.",                 "resp": "Esa actitud es la correcta. Uno nunca termina de aprender.", "stat": "amor"},
            ]
        },

        # P2 — A=deb  B=per  C=mad
        {
            "q": "¿Desayunaste bien? Siempre digo que el desayuno es lo más importante.",
            "ops": [
                {"texto": "Sí, gracias. Comí algo antes.",                  "resp": "Bien. El cuerpo necesita energía para empezar el día.", "stat": "deseo"},
                {"texto": "A veces me lo salto, la verdad.",                "resp": "Eso no está bien. Pero no te voy a regañar.", "stat": "amor"},
                {"texto": "Me acordé de comer por lo que preparaste ayer.", "resp": "¡Qué bueno que ayudó! Me alegra que lo hayas aprovechado.", "stat": "amor"},
            ]
        },

        # P3 — A=per  B=mad  C=deb
        {
            "q": "¿Hay algo en esta casa que te parezca raro o que no entiendas todavía?",
            "ops": [
                {"texto": "Algunas cosas, pero voy preguntando cuando surge.",  "resp": "Bien hecho. Mejor preguntar que quedarse con dudas.", "stat": "amor"},
                {"texto": "Voy aprendiendo cómo funciona todo con tiempo.",     "resp": "Eso me tranquiliza. Sabes que puedes contar conmigo.", "stat": "amor"},
                {"texto": "Me cuesta un poco entender las rutinas de todos.",    "resp": "Es natural. Cada persona tiene sus maneras. Con calma.", "stat": "deseo"},
            ]
        },

        # P4 — A=mad  B=per  C=deb
        {
            "q": "¿Te gusta cocinar? Porque siempre necesito ayuda en la cocina.",
            "ops": [
                {"texto": "Me defiendo, aunque no soy el mejor.",           "resp": "Con eso alcanza. Bienvenido al equipo.", "stat": "amor"},
                {"texto": "No mucho, pero aprendo rápido.",                 "resp": "Eso es todo lo que hace falta.", "stat": "amor"},
                {"texto": "Si me enseñás, con gusto.",                     "resp": "¡Trato! Me gusta enseñar a quien quiere aprender.", "stat": "deseo"},
            ]
        },

        # P5 — A=deb  B=mad  C=per
        {
            "q": "¿Cómo te llevas con Violet y Jasmine hasta ahora?",
            "ops": [
                {"texto": "Bien, aunque aún estamos conociéndonos.",        "resp": "Eso es lo esperable. Denle tiempo.", "stat": "deseo"},
                {"texto": "Violet es más reservada, Jasmine más abierta.",  "resp": "Las conoces bien para el tiempo que llevan. Buen ojo.", "stat": "amor"},
                {"texto": "Trato de no meterme mucho por ahora.",           "resp": "También es una opción válida. Cada uno a su ritmo.", "stat": "amor"},
            ]
        },

        # P6 — A=per  B=deb  C=mad
        {
            "q": "¿Qué es lo que más te cuesta de vivir con otras personas?",
            "ops": [
                {"texto": "Adaptarme a los ritmos de los demás.",           "resp": "Es uno de los desafíos más comunes. Pero se aprende.", "stat": "amor"},
                {"texto": "Dar privacidad sin quedar indiferente.",         "resp": "Eso requiere mucha sensibilidad. Buen punto.", "stat": "deseo"},
                {"texto": "A veces extraño mi propio espacio.",             "resp": "Es completamente normal. Esta casa también es tuya.", "stat": "amor"},
            ]
        },

        # P7 — A=mad  B=deb  C=per
        {
            "q": "¿Te parece que esta casa tiene buen ambiente en general?",
            "ops": [
                {"texto": "Sí, se siente bastante cómoda.",                 "resp": "Me alegra. Puse mucho esfuerzo en que así fuera.", "stat": "amor"},
                {"texto": "Hay momentos buenos y otros más tensos.",        "resp": "Es honesto. Toda convivencia tiene sus momentos.", "stat": "deseo"},
                {"texto": "Depende del día y de cómo esté cada uno.",       "resp": "Cierto. El ambiente lo hacemos todos juntos.", "stat": "amor"},
            ]
        },

        # P8 — A=deb  B=per  C=mad
        {
            "q": "¿Hay algo que pueda hacer para que te sientas más cómodo aquí?",
            "ops": [
                {"texto": "No, ya estoy bien. Gracias por preguntar.",     "resp": "De nada. Si algo cambia, avísame sin problema.", "stat": "deseo"},
                {"texto": "Tal vez saber más sobre cómo funciona todo.",   "resp": "Podemos hablar de eso con calma cuando quieras.", "stat": "amor"},
                {"texto": "Con que sigamos hablando así, ya es suficiente.", "resp": "Eso me alegra mucho escucharlo.", "stat": "amor"},
            ]
        },

        # P9 — A=per  B=mad  C=deb
        {
            "q": "¿Eres de los que piden ayuda cuando la necesitan, o prefieres resolver solo?",
            "ops": [
                {"texto": "Intento resolver solo primero, pero pido si es necesario.", "resp": "Eso está muy bien. Independencia con sentido.", "stat": "amor"},
                {"texto": "Me cuesta pedir, pero estoy trabajando en eso.",            "resp": "El solo reconocerlo ya es un gran paso.", "stat": "amor"},
                {"texto": "Depende de la situación, la verdad.",                       "resp": "Eso es sano. No todas las situaciones son iguales.", "stat": "deseo"},
            ]
        },

        # P10 — A=mad  B=per  C=deb
        {
            "q": "¿Hay algo que quieras saber de mí o de cómo funciona esto aquí?",
            "ops": [
                {"texto": "Sí, me gustaría entender mejor las normas de la casa.", "resp": "Con mucho gusto. Siéntate y te cuento todo.", "stat": "amor"},
                {"texto": "Por ahora estoy bien, pero aviso si surge algo.",       "resp": "Perfecto. La puerta siempre está abierta.", "stat": "amor"},
                {"texto": "¿Qué es lo más importante para ti aquí?",               "resp": "Que todos estén bien y se traten con respeto. Eso es todo.", "stat": "deseo"},
            ]
        },

    ]


################################################################################
## Label de conversación con Mónica
################################################################################

label conversacion_hablar_monica:

    # Restaurar fondo de la locación actual (el HUD fue ocultado antes de entrar)
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show monica_parada c_rbase_base o_base b_hablando at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    $ _npc_m = obtener_npc("monica")
    $ _indice = store.monica_hablar_indice % len(preguntas_hablar_monica)
    $ _preg = preguntas_hablar_monica[_indice]
    $ store.monica_hablar_indice += 1
    $ _op0 = _preg["ops"][0]
    $ _op1 = _preg["ops"][1]
    $ _op2 = _preg["ops"][2]

    $ _txt_op0 = formatear_opcion_recompensa(_op0["texto"], _op0["stat"])
    $ _txt_op1 = formatear_opcion_recompensa(_op1["texto"], _op1["stat"])
    $ _txt_op2 = formatear_opcion_recompensa(_op2["texto"], _op2["stat"])

    monica "[_preg['q']]"

    menu:
        "[_txt_op0]":
            monica "[_op0['resp']]"
            $ _npc_m.modificar_stat(_op0["stat"], 1)
        "[_txt_op1]":
            monica "[_op1['resp']]"
            $ _npc_m.modificar_stat(_op1["stat"], 1)
        "[_txt_op2]":
            monica "[_op2['resp']]"
            $ _npc_m.modificar_stat(_op2["stat"], 1)

    hide monica_parada
    hide mc_parado_base

    scene black with fade
    $ avanzar_horario()

    return
