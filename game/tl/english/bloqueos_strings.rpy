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
