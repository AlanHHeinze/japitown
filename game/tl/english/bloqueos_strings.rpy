# Mensajes del embudo unico de bloqueos (accion_bloqueada, refactor C11).
#
# Antes eran dialogo literal en los labels (piensa "...") y se traducian por
# bloques con hash. Ahora los compone accion_bloqueada() en
# script/core/quests/restriccion_quest_system.rpy y se muestran por
# interpolacion (piensa "[_msg_restriccion]"), que NO traduce: los traduce
# accion_bloqueada() via renpy.translate_string y necesitan un `old` aca.
#
# La plantilla del mensaje prioritario usa {npc}: translate_string traduce la
# PLANTILLA y despues se hace .format(npc=...) — el `new` debe conservar {npc}.

translate english strings:

    # Trasnoche: sale al clickear a un NPC que esta durmiendo
    # (MENSAJE_NPC_DURMIENDO en core/quests/restriccion_quest_system.rpy).
    # El mismo texto existe como `piensa` en door_access_system y en la 09_a,
    # pero por hash: los dos sistemas de traduccion no se pisan.
    old "Debe estar durmiendo, no voy a molestar."
    new "She must be asleep, I'm not going to bother her."

    # Generico de DISPONIBILIDAD (core/npcs/npc_disponibilidad.rpy): sale al
    # insistir con un NPC que el contenido saco de juego sin dar un motivo
    # propio. Si el contenido dio uno, gana el suyo.
    old "No es momento para eso"
    new "This isn't the time for that"

    # Quest 09_b: el motivo con el que Violet queda fuera de juego. Sale como
    # `piensa` en su puerta y tambien como motivo de la disponibilidad.
    old "Mónica pidió que no la molestemos"
    new "Monica asked us not to bother her"

    old "Debo responder el mensaje de {npc} antes de continuar"
    new "I have to reply to {npc}'s message before continuing"

    old "No puedes avanzar el tiempo ahora."
    new "You can't advance time right now."

    old "No puedo hacer eso ahora."
    new "I can't do that right now."

    old "Tengo cosas pendientes por hacer, no puedo dormir ahora"
    new "I have pending things to do, I can't sleep now"

    # =========================================================================
    # Violet — Amor 15 ("Juegos Viejos")
    # =========================================================================
    # mensaje_movimiento / mensaje_accion_default / mensaje_celular de las dos
    # restricciones de la quest (violet_amor_15.rpy).

    old "Le dije que la iba a ayudar, primero subo al altillo"
    new "I told her I'd help, first I'm going up to the attic"

    old "No me puedo ir hasta encontrarla"
    new "I can't leave until I find it"

    # =========================================================================
    # Violet — Deseo 10 ("Encuentro nocturno")
    # =========================================================================

    old "Primero voy a tomar algo, me estoy muriendo de sed"
    new "First I'm getting something to drink, I'm dying of thirst"

    # =========================================================================
    # Violet — Amor 25 ("Solos en casa")
    # =========================================================================
    # Mensajes de las tres restricciones de la quest y de sus dos bloqueos
    # registrados (violet_amor_25.rpy).

    old "Debo ver a Monica"
    new "I have to go see Monica"

    old "Hoy me quedo en casa"
    new "Today I'm staying home"

    old "Ya es de noche, el dia se termina acá"
    new "It's night already, the day ends here"

    old "Todavia no me voy a dormir"
    new "I'm not going to sleep yet"

    old "Sin luz no voy a andar dando vueltas por la casa"
    new "With no power I'm not wandering around the house"

    old "Sin luz no puedo hacer nada de eso"
    new "With no power I can't do any of that"

    # =========================================================================
    # Violet — Deseo 30 ("Sinceridad")
    # =========================================================================
    # Etapa 1: sale de su cuarto a buscarla y hasta llegar no hace otra cosa.
    # Un solo texto para el movimiento y para las acciones.
    #
    # La etapa 2 (ignorarla tres dias) no tiene mensajes: no bloquea nada, solo
    # cuenta.

    old "Tengo que hablar con Violet"
    new "I need to talk to Violet"

    # =========================================================================
    # Ventaja "Mensajear" (hito de deseo 20)
    # =========================================================================
    # Bloqueo GLOBAL: sale en cualquier accion mientras haya una conversacion de
    # Mensajear sin contestar.

    old "Debo responderle primero a Violet"
    new "I should reply to Violet first"

    # =========================================================================
    # Violet — Deseo 20 ("Pensando en Violet")
    # =========================================================================
    # Bloqueo GLOBAL de la fase 1: sale en cualquier accion mientras no le
    # escriba. Tambien es el mensaje de movimiento y el de NPC bloqueado de la
    # restriccion, que lo repiten con el mismo texto a proposito.

    old "Deberia escribirle a Violet"
    new "I should text Violet"

    # =========================================================================
    # Violet — Deseo 25 ("En su habitacion")
    # =========================================================================
    # Fase 1: lo planto en el sotano y sube a buscarla. Un solo texto para las
    # dos mitades del recorte — el movimiento (no puede salir de la casa) y las
    # acciones (no puede adelantar el tiempo ni dormir).

    old "Primero voy a ver que paso con Violet"
    new "First I'm going to see what happened with Violet"

    # Ventajas de amor 20 / deseo 15: la accion se corta si Violet no esta, para
    # que el jugador no gaste el horario al pedo.
    old "Violet no está conectada ahora"
    new "Violet isn't online right now"

    old "Violet no está en casa ahora"
    new "Violet isn't home right now"
