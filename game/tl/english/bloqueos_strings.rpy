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
    # Violet — Amor 30 ("Noche de amigas")
    # =========================================================================

    old "Violet me esta esperando, no me voy a ir de casa"
    new "Violet is waiting for me, I'm not leaving the house"

    old "Primero voy a ver que necesita Violet"
    new "First I'm going to see what Violet needs"

    # Encerrado en su pieza tras la escena del sotano: lo unico habilitado es
    # dormir, que es el disparador de la ultima parte.
    old "No tengo ganas de nada, mejor me acuesto"
    new "I don't feel like doing anything, I'd better lie down"

    # =========================================================================
    # Ventaja "Mensajear" (hito de deseo 20)
    # =========================================================================
    # Bloqueo GLOBAL: sale en cualquier accion mientras haya una conversacion de
    # Mensajear sin contestar.

    old "Debo responderle primero a Violet"
    new "I should reply to Violet first"
