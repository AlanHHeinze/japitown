# TODO: Translation updated at 2026-04-23

translate english strings:

    ############################################################################
    ## Nombres de Quests
    ############################################################################

    old "¿Qué le pasa a Violet?"
    new "What's wrong with Violet?"

    old "Un paquete misterioso"
    new "A mysterious package"

    old "El contenido del paquete"
    new "The contents of the package"

    old "Limpieza del Sábado"
    new "Saturday Cleaning"

    old "Solo en casa"
    new "Home Alone"

    old "El cosplay de Violet"
    new "Violet's Cosplay"

    old "El cosplay de Violet II"
    new "Violet's Cosplay II"

    old "El cosplay de Violet III"
    new "Violet's Cosplay III"

    old "El cosplay de Violet IV"
    new "Violet's Cosplay IV"

    # Pasos intermedios entre la 04_d y la 04_e
    old "Algo por ella"
    new "Something for her"

    old "Violet dijo que tenía más fotos, quizás pueda conseguirlas haciendo algo por ella"
    new "Violet said she had more photos, maybe I can get them by doing something for her"

    # ── Líneas de relación de Violet (amor / deseo) ──────────────────────────
    # Nombres y descripciones de las 12 quests de línea.
    #
    # Los nombres de HITO que no coinciden con el de su quest se traducen en
    # relaciones_strings.rpy: "Buena relación", "Algo nos pasa", "Me calienta"
    # y "Confesión".
    #
    # "Jugando juntos" es la excepción: desde 2026-08-26 la quest de amor 20 y su
    # hito se llaman igual, así que comparten el `old` de más abajo. Un segundo
    # `old` con el mismo texto rompería el lint.

    # Amor
    old "¿Mejor?"
    new "Better?"

    old "Empiezo a llevarme mejor con Violet."
    new "I'm starting to get along better with Violet."

    old "La relación con Violet se afianza."
    new "Things with Violet are settling in."

    # Amor 15. "Portatil Boy" se adapta ("Portable Boy"): es un nombre parodia
    # y "Portatil" es palabra comun en español — sin traducir se pierde el
    # chiste. Mismo criterio en chat_violet_strings.rpy.
    old "Juegos Viejos"
    new "Old Games"

    old "Violet quiere su vieja Portatil Boy."
    new "Violet wants her old Portable Boy."

    # Amor 20. Este `old` cubre DOS usos: el nombre de la quest y el del hito de
    # amor 20, que desde 2026-08-26 se llama igual. Las traducciones se resuelven
    # por contenido del string, no por contexto, asi que alcanza con este — y de
    # hecho un segundo `old` con el mismo texto romperia el lint.
    old "Jugando juntos"
    new "Playing together"

    old "Violet y yo terminamos jugando lo mismo."
    new "Violet and I ended up playing the same game."

    # Amor 25. NO se traduce como "Home Alone": ese nombre ya lo tiene la quest
    # principal "Solo en casa" (arriba). El de acá es plural — son los dos.
    old "Solos en casa"
    new "Alone in the house"

    old "Un domingo entero con Violet y nadie más."
    new "A whole Sunday with Violet and nobody else."

    # Deseo 30 (las de umbral 30 se intercambiaron entre lineas).
    # El hito de amor 30 sigue llamandose "Algo nos pasa" y se traduce en
    # relaciones_strings.rpy. El de deseo 30 NO: desde 2026-08-31 la quest y su
    # hito se llaman los dos "Sinceridad" y comparten este `old`. Un segundo
    # `old` con el mismo texto rompe el lint.
    old "Sinceridad"
    new "Honesty"

    # La descripcion se ve en Pistas MIENTRAS la quest esta activa, asi que
    # cuenta el arranque y no el final: que ella recapacite y lo vaya a buscar
    # es el premio, no el enunciado.
    old "Le dije lo que me pasa y se hizo la desinteresada."
    new "I told her how I feel and she acted like she didn't care."

    # Deseo 30, segunda mitad: los tres dias de ignorarla (la quest esta
    # partida en dos desde el planificador; ver violet_deseo_30.rpy).
    old "Distancia"
    new "Distance"

    old "Decidí ignorarla unos días, a ver qué hace."
    new "I decided to ignore her for a few days, to see what she does."

    # Deseo
    old "Atracción"
    new "Attraction"

    old "Algo cambió en cómo Violet me mira."
    new "Something changed in the way Violet looks at me."

    # Deseo 15
    old "Anime en estreno"
    new "Anime premiere"

    old "Estrenan el anime que los dos queríamos ver."
    new "The anime we both wanted to watch is premiering."

    # Deseo 20. Igual que en amor 20, el nombre ya no coincide con el del hito
    # ("Confesión", en relaciones_strings.rpy, que no se toca).
    old "Pensando en Violet"
    new "Thinking about Violet"

    old "No me la puedo sacar de la cabeza."
    new "I can't get her out of my head."

    # Amor 30.
    old "¿Qué me pongo?"
    new "What should I wear?"

    old "Violet quiere mi opinión sobre cómo se ve."
    new "Violet wants my opinion on how she looks."

    # Deseo 25
    old "En su habitación"
    new "In her room"

    old "Un capítulo de anime en la pieza de Violet."
    new "An anime episode in Violet's room."

    # Arco de los favores — nombres y descripciones de las 4 quests.
    # Las descripciones NO repiten ninguna pista a proposito: dos `old` iguales
    # rompen el lint.
    old "Las golosinas"
    new "The candy"

    old "Violet me pidió unas golosinas, es lo menos que puedo hacer"
    new "Violet asked me for some candy, it's the least I can do"

    old "La pizza"
    new "The pizza"

    old "Violet quiere que le cocine una pizza para la cena"
    new "Violet wants me to cook her a pizza for dinner"

    old "La limpieza"
    new "The cleaning"

    old "Violet me pidió que limpie algunas partes de la casa"
    new "Violet asked me to clean a few parts of the house"

    old "Todo lo que me pidió"
    new "Everything she asked for"

    old "Ya hice los tres favores que Violet me pidió"
    new "I already did the three favors Violet asked me for"

    old "Los ruidos nocturnos"
    new "Night Noises"

    old "Visita nocturna"
    new "Night Visit"

    old "Bienvenido a casa"
    new "Welcome Home"

    old "Reencuentro con Jasmine"
    new "Reunion with Jasmine"

    ############################################################################
    ## Nombres de Eventos
    ############################################################################

    old "Ropa Nueva"
    new "New Outfit"

    old "Mónica adolorida"
    new "Monica in Pain"

    ############################################################################
    ## Mensajes genéricos de Quest
    ############################################################################

    old "Debo esperar [dias_restantes] días más."
    new "I must wait [dias_restantes] more days."

    old "Esperar [dias_restantes] días"
    new "Wait [dias_restantes] days"

    old "Debo esperar hasta mañana."
    new "I must wait until tomorrow."

    old "Esperar hasta mañana"
    new "Wait until tomorrow"

    old "Debo esperar algunos días."
    new "I must wait a few days."

    old "Esperar algunos días"
    new "Wait a few days"

    old "Verificando condiciones..."
    new "Checking conditions..."

    old "Verificando..."
    new "Checking..."

    old " y "
    new " and "

    ############################################################################
    ## Requisitos Genéricos
    ############################################################################

    old "Relación con [npc_id] debe ser de al menos [valor]"
    new "Relationship with [npc_id] must be at least [valor]"

    old "Tener al menos [cantidad] de [item_id]"
    new "Have at least [cantidad] [item_id]"

    old "Tener al menos $[valor]"
    new "Have at least $[valor]"

    ############################################################################
    ## Mensajes de bloqueo de restricciones — movimiento
    ############################################################################

    old "No puedo ir ahí ahora"
    new "I can't go there right now"

    old "Debo ir a mi habitación"
    new "I need to go to my room"

    old "Debería ir a la cocina a preparar la pizza"
    new "I should go to the kitchen to make the pizza"

    old "Deberia ir a la cocina a preparar la pizza"
    new "I should go to the kitchen to make the pizza"

    old "Debo avisarle a Violet que esta la comida"
    new "I should let Violet know the food is ready"

    old "Debo encargarme de limpiar la planta baja"
    new "I need to handle cleaning the ground floor"

    old "Debo ir a ver como va Violet con la limpieza"
    new "I should check how Violet is doing with the cleaning"

    old "Debo buscar algo para limpiar"
    new "I need to find something to clean with"

    old "Debo volver arriba a limpiar"
    new "I need to go back upstairs to clean"

    old "Debo ver como va Violet con el baño"
    new "I should check how Violet is doing with the bathroom"

    old "No puedo salir de la casa ahora"
    new "I can't leave the house right now"

    old "Debería llevarle ropa a Violet"
    new "I should bring Violet some clothes"

    old "Debo llevarle la ropa a Violet"
    new "I need to bring Violet her clothes"

    ############################################################################
    ## Mensajes de bloqueo de restricciones — acciones
    ############################################################################

    old "No puedo hacer eso ahora"
    new "I can't do that right now"

    old "No debo perder el tiempo"
    new "I can't waste time"

    old "No puedo perder tiempo con esto"
    new "I can't waste time on this"

    old "Tengo que encargarme de las pizzas antes de hacer otra cosa"
    new "I need to take care of the pizzas before doing anything else"

    old "Tengo que cocinar primero"
    new "I need to cook first"

    old "No tengo ganas de hacer nada productivo"
    new "I don't feel like doing anything productive"

    old "No tengo sueño"
    new "I'm not tired"

    old "No tengo ganas de entrenar"
    new "I don't feel like working out"

    old "No tengo ganas de trabajar"
    new "I don't feel like working"

    old "No tengo ganas de usar eso ahora"
    new "I don't feel like using that right now"

    old "No tengo ganas de comprar nada"
    new "I don't feel like buying anything"

    ############################################################################
    ## Mensajes de bloqueo de restricciones — NPC y celular
    ############################################################################

    old "No tengo tiempo para eso ahora"
    new "I don't have time for that right now"

    old "No tengo tiempo para hablar"
    new "I don't have time to talk"

    old "No hay nadie en la casa"
    new "There's no one at home"

    old "No hay nadie mas en la casa"
    new "There's no one else at home"

    old "No es momento de usar el celular"
    new "It's not the time to use my phone"

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 0
    ############################################################################

    old "Tengo que hablar con Violet, podría aprovechar cuando está en su habitación por la tarde."
    new "I should talk to Violet. I could catch her in her room in the afternoon."

    old "Ir a la habitación de Violet por la tarde."
    new "Go to Violet's room in the afternoon."

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 1
    ############################################################################

    old "Todo tranquilo por ahora"
    new "All quiet for now"

    old "Parece que hay alguien afuera"
    new "Looks like someone's outside"

    old "Tengo un mensaje por ver"
    new "I have a message to check"

    old "Revisar el paquete"
    new "Check the package"

    old "Esperar"
    new "Wait"

    old "Ir al frente"
    new "Go to the front door"

    old "Ir a la habitación por el paquete"
    new "Go to the room for the package"

    old "Responder el mensaje de Monica"
    new "Reply to Monica's message"

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 2
    ############################################################################

    old "Podría entregarle el paquete a Violet o podría ver bien qué tiene"
    new "I could give the package to Violet or take a closer look at what's inside"

    old "Hablar con Violet y darle su paquete o revisar el contenido del paquete"
    new "Talk to Violet and give her the package, or check what's inside"

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 4 (Limpieza)
    ############################################################################

    old "Monica me dijo algo sobre limpiar la casa, tengo que esperar."
    new "Monica mentioned something about cleaning the house, I need to wait."

    old "Debería responderle a Monica."
    new "I should reply to Monica."

    old "Responder mensaje de Monica."
    new "Reply to Monica's message."

    old "Hoy es sábado, tengo que despertar a Violet temprano."
    new "Today is Saturday, I need to wake Violet up early."

    old "Monica me pidió que despierte a Violet temprano el sábado para limpiar la casa."
    new "Monica asked me to wake Violet up early on Saturday to clean the house."

    old "El próximo sábado debería ocuparme de la limpieza."
    new "I should take care of the cleaning next Saturday."

    old "Esperar hasta el próximo sábado por la mañana."
    new "Wait until next Saturday morning."

    old "Ir a la habitación de Violet por la mañana."
    new "Go to Violet's room in the morning."

    old "Esperar hasta el sabado por la mañana."
    new "Wait until Saturday morning."

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 5 (Solo en casa)
    ############################################################################

    old "Todo tranquilo por ahora."
    new "All quiet for now."

    old "Hoy estoy solo en la casa."
    new "I'm home alone today."

    old "Esperar al día siguiente."
    new "Wait until the next day."

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 6
    ############################################################################

    old "Cuando encuentre a Violet podría ver si se probó el cosplay"
    new "When I find Violet I could check if she tried on the cosplay"

    old "Hablar con Violet"
    new "Talk to Violet"

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 7-9 (Cosplay II-IV)
    ############################################################################

    old "Debería esperar unos días antes de hablar con Violet sobre el cosplay."
    new "I should wait a few days before talking to Violet about the cosplay."

    old "Subir deseo con Violet ({}/{})"
    new "Increase desire with Violet ({}/{})"

    old "Quizás si sigo mejorando mi deseo con Violet me muestre un poco más"
    new "Maybe if I keep improving my desire with Violet she'll show me a little more"

    old "Violet me envió un mensaje, debería responderle."
    new "Violet sent me a message, I should reply."

    old "Violet ya me contestó, debería ir a hablar con ella."
    new "Violet replied, I should go talk to her."

    old "Violet me envió un mensaje, debería responderle"
    new "Violet sent me a message, I should reply"

    old "Ir a ver a Violet a su habitación."
    new "Go see Violet in her room."

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 11 (Los ruidos nocturnos)
    ############################################################################

    old "Podría conseguir algunos cosplay para que Violet se pruebe"
    new "I could get some cosplays for Violet to try on"

    old "Comprar el ítem conjunto de cosplay"
    new "Buy the cosplay set item"

    old "Podría ir a la habitación de violet por la noche a ver si le gusta lo que compré"
    new "I could go to Violet's room at night to see if she likes what I got"

    old "Ir a la habitación de violet por la noche"
    new "Go to Violet's room at night"

    ############################################################################
    ## Pistas y qué hacer — Quest Violet 12 (Visita nocturna)
    ############################################################################

    old "Violet me pidió que pase por su habitación, debería ir a la noche."
    new "Violet asked me to stop by her room, I should go at night."

    old "Ir a la habitación de Violet por la noche."
    new "Go to Violet's room at night."

    ############################################################################
    ## Pistas y qué hacer — Quests Monica
    ############################################################################

    old "Tendría que encontrarme con Monica para darle las gracias, podría verla por la tarde."
    new "I should meet up with Monica to thank her, I could see her in the afternoon."

    old "Ir al living por la tarde."
    new "Go to the living room in the afternoon."

    old "Monica parece más ocupada por las tardes"
    new "Monica seems busier in the afternoons"

    old "Ir a la habitación de Monica por la tarde"
    new "Go to Monica's room in the afternoon"

    old "Podría ver a Mónica en la tarde y ofrecerle un masaje."
    new "I could see Monica in the afternoon and offer her a massage."

    old "Habla con Mónica cuando esté en el Living por la tarde."
    new "Talk to Monica when she's in the living room in the afternoon."

    ############################################################################
    ## Pistas y qué hacer — Quests Jasmine
    ############################################################################

    old "Podría ver a Jasmine por la tarde cuando entrena y hablar un poco."
    new "I could see Jasmine in the afternoon when she's working out and chat a bit."

    old "Ir al gym por la tarde."
    new "Go to the gym in the afternoon."

    ############################################################################
    ## Mensajes de Requisito (panel validación fallida)
    ############################################################################

    old "Violet debe estar en su habitación"
    new "Violet must be in her room"

    old "Debe ser sábado"
    new "It must be Saturday"

    old "Debe ser por la mañana"
    new "It must be morning"

    old "Debe ser por la tarde"
    new "It must be afternoon"

    old "Debe ser por la noche"
    new "It must be nighttime"

    old "Me falta el conjunto de cosplays"
    new "I'm missing the cosplay set"

    old "Contestar el mensaje de Monica"
    new "Reply to Monica's message"

    old "Monica debe estar en su habitación"
    new "Monica must be in her room"

    old "Necesitas mas deseo con Violet"
    new "You need more desire with Violet"

    old "Debes estar en el gym"
    new "You must be at the gym"

    old "Debes estar en el living"
    new "You must be in the living room"

    old "La quest no está lista para iniciarse."
    new "The quest is not ready to start."

    ############################################################################
    ## Mensajes de Despertar
    ############################################################################

    old "Tengo que encontrar algún momento para acercarme a Violet y ver qué le pasa."
    new "I have to find a moment to approach Violet and see what's wrong with her."

    old "Escuché el timbre"
    new "I heard the doorbell"

    old "Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa."
    new "Today is Saturday, I have to wake Violet up so we can clean the house."

    old "Podría preguntarle a Violet si se probó el cosplay"
    new "I could ask Violet if she tried on the cosplay"

    old "Violet tiene vergüenza de mostrarme el cosplay, tengo que mejorar mi deseo con ella"
    new "Violet is too shy to show me the cosplay, I need to improve my desire with her"

    old "Tengo que ir a ver a Violet por lo de su cosplay."
    new "I have to go see Violet about her cosplay."

    old "Podría mostrarle a violet los cosplays que conseguí."
    new "I could show Violet the cosplays I got."

    old "Violet me pidió que pase por su habitación a la noche."
    new "Violet asked me to drop by her room at night."

    old "Podría aprovechar que Monica está en casa para hablar con ella."
    new "I could take advantage of Monica being home to talk to her."

    old "Podría buscar a Jasmine cuando este entrenando para hablar con ella."
    new "I could look for Jasmine while she's working out to talk to her."

    old "Mónica se quejó de dolor en sus hombros, podría hacerle un masaje en la tarde."
    new "Monica complained about shoulder pain, I could give her a massage in the afternoon."

    old "Jasmine me dijo que hoy la vea en el gym por la tarde."
    new "Jasmine told me to meet her at the gym in the afternoon."

    # Amor 35 ("Las amigas"): la noche de pelicula en el sotano con Zowie y
    # Leah. El nombre es como las llama el MC, no un titulo.
    old "Las amigas"
    new "Her friends"

    old "Violet bajó al sótano con sus amigas."
    new "Violet went down to the basement with her friends."

    # Amor 40 ("La solicitud"). PROVISORIOS: se ven en el panel de Pistas y hay
    # que revisarlos al escribir el dialogo.
    old "La solicitud"
    new "The friend request"

    old "Una amiga de Violet me agregó en XGram."
    new "A friend of Violet's added me on XGram."

    # Amor 45 ("La regla de la casa"). PROVISORIOS: se ven en el panel de
    # Pistas y hay que revisarlos al escribir el dialogo.
    old "La regla de la casa"
    new "The house rule"

    old "Lo que hagamos, lo hacemos a solas."
    new "Whatever we do, we do it alone."

    # Amor 50 ("El domingo solos"). PROVISORIOS: se ven en el panel de Pistas.
    old "El domingo solos"
    new "Sunday alone"

    old "Violet se quedó en casa conmigo."
    new "Violet stayed home with me."
