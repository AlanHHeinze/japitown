# Textos del panel de PISTAS y QUÉ HACER que faltaban o quedaron rotos.
#
# La mayoría se rompió porque se CAMBIÓ el texto en el código y el `old` viejo
# quedó apuntando a una frase que ya no existe: Ren'Py no avisa, simplemente
# devuelve el original en español.
#
# Cómo llegan a la pantalla:
#   - Quests de NPC  → ConfigEtapa._resolver() (questsystem_core) traduce el
#                      resultado, sea string fijo o callable.
#   - Quests del MC  → QuestMC._traducir() (quest_mc.rpy), que se agregó ahora:
#                      antes QuestMC NO traducía nada.
#
# Los textos que se componen ("Visitar: A, B y C") traducen sus piezas por
# separado; conservar los placeholders con nombre en el `new`.

translate english strings:

    # =========================================================================
    # Quests del MC — panel de Pistas
    # =========================================================================

    old "Visitar: {lista}"
    new "Visit: {lista}"

    old "Has recorrido toda la casa."
    new "You've been all over the house."

    old "Completar:"
    new "Complete:"

    old "¡Todas completadas!"
    new "All done!"

    old "La batería de la notebook (Mónica)"
    new "The laptop battery (Monica)"

    old "¿Que le pasa a Violet? (Violet)"
    new "What's up with Violet? (Violet)"

    old "Reencuentro con Jasmine (Jasmine)"
    new "Reunion with Jasmine (Jasmine)"

    # =========================================================================
    # Violet — Quest 01_a (el paquete misterioso)
    # =========================================================================

    old "El paquete debería llegar mañana por la mañana"
    new "The package should arrive tomorrow morning"

    old "Esperar al repartidor por la mañana"
    new "Wait for the delivery guy in the morning"

    # =========================================================================
    # Violet — Quest 0_a (romper el hielo)
    # =========================================================================

    old "Tengo que hablar con Violet para romper el hielo"
    new "I have to talk to Violet to break the ice"

    old "Interactuar con Violet"
    new "Interact with Violet"

    old "Podría intentar nuevamente"
    new "I could try again"

    old "Debería esperar antes de hablar con Violet."
    new "I should wait before talking to Violet."

    old "Tengo que mejorar la relación con Violet"
    new "I have to improve my relationship with Violet"

    old "Requisito ❤️ 10"
    new "Requirement ❤️ 10"

    # =========================================================================
    # Violet — Quest 02 (los mangas)
    # =========================================================================

    old "Pedirle los mangas a Violet"
    new "Ask Violet for the manga"

    old "Tengo que leer los mangas"
    new "I have to read the manga"

    old "Terminar de leer los mangas"
    new "Finish reading the manga"

    old "Desde el inventario leer Mangas de Violet"
    new "Read Violet's Manga from the inventory"

    # =========================================================================
    # Violet — Quest 04 (el cosplay) y los chats
    # =========================================================================

    old "Violet va a mandarme un mensaje."
    new "Violet is going to send me a message."

    old "Violet va a mandarme un mensaje de noche sobre los cosplays."
    new "Violet is going to message me tonight about the cosplays."

    old "Esperar el mensaje de noche"
    new "Wait for the message tonight"

    old "Violet me envió un mensaje."
    new "Violet sent me a message."

    old "Violet me mandó un mensaje, debería responderle."
    new "Violet sent me a message, I should reply."

    old "Responder a Violet"
    new "Reply to Violet"

    old "Responder mensaje Violet"
    new "Reply to Violet's message"

    old "Violet se lo probo debería ir a hablar con ella"
    new "Violet tried it on, I should go talk to her"

    old "Violet ya me contestó, debería ir a hablar con ella"
    new "Violet already replied, I should go talk to her"

    old "Ir a ver a Violet"
    new "Go see Violet"

    # Rama "el mensaje todavía no llegó" de la 04_c (el chat llega de noche).
    old "No voy a seguir molestando a Violet, por ahora podría esperar"
    new "I'm not going to keep bothering Violet, for now I could just wait"

    old "Esperar que Violet nos envíe un mensaje"
    new "Wait for Violet to send a message"

    # Idem en la 04_d (una vez alcanzado el deseo 10).
    old "Ahora solo queda esperar el mensaje de Violet"
    new "Now all that's left is to wait for Violet's message"

    old "Esperar el mensaje de Violet"
    new "Wait for Violet's message"

    # =========================================================================
    # Violet — Quest 07 (el cierre del cosplay)
    # =========================================================================

    old "Tengo que esperar a ver si Monica pudo arreglar el cierre."
    new "I have to wait and see if Monica managed to fix the zipper."
