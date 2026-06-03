################################################################################
## Conversación diaria con Jasmine
################################################################################
## Pool de preguntas para la interacción "Hablar" con Jasmine.
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

default jasmine_hablar_indice = 0

init python:

    preguntas_hablar_jasmine = [

        # P1 — A=adu  B=pro  C=per
        {
            "q": "¡Ey! ¿Qué estás haciendo? No estás siendo aburrido, ¿no?",
            "ops": [
                {"texto": "Nada en especial, por eso me acerqué a hablar.",   "resp": "¡Buena decisión! Soy la mejor opción para no aburrirse.", "stat": "amor"},
                {"texto": "Estaba haciendo mis cosas, tranquilo.",             "resp": "Tranquilo... qué concepto tan ajeno para mí.", "stat": "deseo"},
                {"texto": "Pensando, que también sirve de algo.",              "resp": "¡Uy, eso sonó serio! Ojalá estuviera pensando en algo divertido.", "stat": "amor"},
            ]
        },

        # P2 — A=pro  B=per  C=adu
        {
            "q": "¿Cuál es tu peli o serie favorita? Necesito nueva recomendación.",
            "ops": [
                {"texto": "Depende del género, ¿qué te gusta a vos?",        "resp": "¡Me gusta todo! Sorpréndeme.", "stat": "deseo"},
                {"texto": "Veo de todo un poco, no tengo una favorita.",      "resp": "Eso es estratégico, nunca te decepcionan.", "stat": "amor"},
                {"texto": "Te paso algunas opciones si querés.",               "resp": "¡Sí! ¿Las vemos juntos algún día?", "stat": "amor"},
            ]
        },

        # P3 — A=per  B=adu  C=pro
        {
            "q": "¿Preferís planes grandes con mucha gente o algo más tranquilo?",
            "ops": [
                {"texto": "Depende del momento, pero los dos tienen lo suyo.", "resp": "¡Eso es lo ideal! Flexibilidad total.", "stat": "amor"},
                {"texto": "Algo más tranquilo, en grupos chicos.",              "resp": "Yo al revés, pero lo entiendo. ¡Igual puedo convencerte!", "stat": "amor"},
                {"texto": "Mientras haya buena energía, me adapto.",           "resp": "¡Me encanta esa actitud! Energía buena es lo que sobra acá.", "stat": "deseo"},
            ]
        },

        # P4 — A=adu  B=per  C=pro
        {
            "q": "¿Sos de los que escucha música todo el tiempo o preferís el silencio?",
            "ops": [
                {"texto": "Música casi siempre, sí.",                         "resp": "¡Obvio! El silencio es raro. ¿Qué escuchás?", "stat": "amor"},
                {"texto": "Me gusta el silencio para concentrarme.",           "resp": "Respeto, aunque a mí me costaría muchísimo.", "stat": "amor"},
                {"texto": "Un poco de los dos según lo que esté haciendo.",    "resp": "El balance perfecto. Muy sabio.", "stat": "deseo"},
            ]
        },

        # P5 — A=pro  B=adu  C=per
        {
            "q": "¿Qué harías si tuvieras un día libre sin ningún compromiso?",
            "ops": [
                {"texto": "Salir, hacer algo diferente.",                     "resp": "¡Eso mismo! La vida no se disfruta en casa.", "stat": "deseo"},
                {"texto": "Descansar, sin dramas.",                           "resp": "A veces el descanso es el mejor plan. Cada uno sabe.", "stat": "amor"},
                {"texto": "Depende de cómo me sienta ese día.",               "resp": "¡Eso es misterioso! Me gusta.", "stat": "amor"},
            ]
        },

        # P6 — A=per  B=pro  C=adu
        {
            "q": "¿Qué opinas de las personas que se toman todo muy en serio?",
            "ops": [
                {"texto": "Están bien, cada uno tiene su manera de ser.",      "resp": "Eso dice mucho de vos. ¡Sos tolerante!", "stat": "amor"},
                {"texto": "A veces es cansador estar con gente tan seria.",    "resp": "¡Exacto! La vida también puede ser liviana.", "stat": "deseo"},
                {"texto": "Depende de la situación, no siempre está mal.",     "resp": "Cierto, cierto. Contexto ante todo.", "stat": "amor"},
            ]
        },

        # P7 — A=adu  B=pro  C=per
        {
            "q": "¿Hay algo de esta casa que todavía te sorprende o que no esperabas?",
            "ops": [
                {"texto": "Varias cosas, es más interesante de lo que parecía.", "resp": "¡Jaja! Siempre hay cosas ocultas en los lugares. ¡Me alegra!", "stat": "amor"},
                {"texto": "La verdad que me fui acostumbrando rápido.",           "resp": "¡Eso es buenísimo! Adaptarse rápido es una virtud.", "stat": "deseo"},
                {"texto": "Me sorprende lo bien que funciona todo.",              "resp": "¡Es que Mónica no deja nada al azar!", "stat": "amor"},
            ]
        },

        # P8 — A=pro  B=per  C=adu
        {
            "q": "¿Cuál fue el mejor plan que hiciste últimamente?",
            "ops": [
                {"texto": "Nada muy épico, pero pasé un buen rato.",           "resp": "¡Los mejores planes suelen ser los más simples!", "stat": "deseo"},
                {"texto": "No tuve muchos planes últimamente.",                 "resp": "¡Eso cambia ya! No te puedo dejar sin planes.", "stat": "amor"},
                {"texto": "Ponerme a hablar con vos, supongo.",                 "resp": "¡Awww! Eso fue muy lindo. Reconocido oficialmente.", "stat": "amor"},
            ]
        },

        # P9 — A=per  B=adu  C=pro
        {
            "q": "¿Sos de dar consejos o preferís no meterte en los asuntos de los demás?",
            "ops": [
                {"texto": "Doy consejos si me los piden, no me meto solo.",    "resp": "¡Eso es respetuoso! Aunque a veces me cuestan las fronteras.", "stat": "amor"},
                {"texto": "Me gusta ayudar, aunque no me lo pidan.",            "resp": "¡Yo igual! A veces funciona, a veces... no tanto.", "stat": "amor"},
                {"texto": "Depende de quién y de qué se trate.",               "resp": "Criterio selectivo. No está mal.", "stat": "deseo"},
            ]
        },

        # P10 — A=adu  B=per  C=pro
        {
            "q": "¿Qué es lo que más te gusta de hablar conmigo?",
            "ops": [
                {"texto": "Que siempre hay algo que contar.",                   "resp": "¡Eso! La vida nunca es aburrida si la contás bien.", "stat": "amor"},
                {"texto": "Que no hay que pensar demasiado, fluye solo.",       "resp": "¡Exacto! Las mejores conversaciones son así.", "stat": "amor"},
                {"texto": "Me hace reír sin mucho esfuerzo.",                   "resp": "¡Es mi superpoder! Que bueno que funciona.", "stat": "deseo"},
            ]
        },

    ]


################################################################################
## Label de conversación con Jasmine
################################################################################

label conversacion_hablar_jasmine:

    # Restaurar fondo de la locación actual (el HUD fue ocultado antes de entrar)
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show jasmine_parada c_rbase_base o_base b_hablando at right
    show mc_parado_base c_rbase_base o_base b_seria at mc_izquierda

    $ _npc_j = obtener_npc("jasmine")
    $ _indice = store.jasmine_hablar_indice % len(preguntas_hablar_jasmine)
    $ _preg = preguntas_hablar_jasmine[_indice]
    $ store.jasmine_hablar_indice += 1
    $ _op0 = _preg["ops"][0]
    $ _op1 = _preg["ops"][1]
    $ _op2 = _preg["ops"][2]

    $ _txt_op0 = formatear_opcion_recompensa(_op0["texto"], _op0["stat"])
    $ _txt_op1 = formatear_opcion_recompensa(_op1["texto"], _op1["stat"])
    $ _txt_op2 = formatear_opcion_recompensa(_op2["texto"], _op2["stat"])

    jasmine "[_preg['q']]"

    menu:
        "[_txt_op0]":
            jasmine "[_op0['resp']]"
            $ _hablar_stat_elegido = _op0["stat"]
        "[_txt_op1]":
            jasmine "[_op1['resp']]"
            $ _hablar_stat_elegido = _op1["stat"]
        "[_txt_op2]":
            jasmine "[_op2['resp']]"
            $ _hablar_stat_elegido = _op2["stat"]

    # Bloquear rollback — la recompensa y la conversación no se pueden deshacer
    $ renpy.block_rollback()
    $ _npc_j.modificar_stat(_hablar_stat_elegido, 1)

    hide jasmine_parada
    hide mc_parado_base

    scene black with fade
    $ avanzar_horario()

    return
