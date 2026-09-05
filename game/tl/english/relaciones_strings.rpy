# Textos de la app de Relaciones (ui/hud/hud_relaciones.rpy).
#
# Van todos por `translate english strings:` y no por bloques con hash porque la
# screen los muestra INTERPOLADOS ("Locación: [_loc_r]") o los pasa por
# renpy.translate_string() antes de armar la linea. La interpolacion no dispara
# la traduccion de dialogo, asi que cada texto necesita su `old` aca.
#
# Los nombres de estado de animo salen de los EstadoTalk de cada NPC
# (characters/<npc>/talk/<npc>_talk.rpy) y llegan a la app via
# sistema_talk.obtener_estado_activo().nombre.

translate english strings:

    # ── Etiquetas de la screen ───────────────────────────────────────────────
    old "Locación:"
    new "Location:"

    old "Estado de ánimo:"
    new "Mood:"

    old "Sin novedades"
    new "Nothing new"

    old "Amor"
    new "Love"

    old "Deseo"
    new "Desire"

    # ── Tope de stat por hito pendiente ──────────────────────────────────────
    # Lo muestra notificar_stat_bloqueado() (ui/hud/hud_notificaciones.rpy)
    # cuando el stat no puede subir porque falta completar la quest de relación.
    # El {stat} se reemplaza por "Amor"/"Deseo" YA traducidos.
    old "Incremento de {stat} bloqueado"
    new "{stat} increase blocked"

    # ── Pantalla de Desbloqueos ──────────────────────────────────────────────
    old "Desbloqueos"
    new "Unlocks"

    old "Todavía no hay nada que descubrir con esta persona."
    new "There's nothing to discover with this person yet."

    old "Ventajas"
    new "Perks"

    # Textos fijos del cuadro emergente (DESB_TXT_* en hud_desbloqueos.rpy)
    old "Hito: Conseguir un Hito te permite avanzar en misiones principales y desbloquear elecciones únicas."
    new "Milestone: Reaching a Milestone lets you advance in main quests and unlock unique choices."

    old "Desbloquear una Ventaja te da mejoras permanentes en algunas interacciones con el personaje."
    new "Unlocking a Perk gives you permanent improvements in some interactions with the character."

    # El {} lo rellena la descripcion de la ventaja, ya traducida.
    old "Esta ventaja otorga - {}"
    new "This perk grants - {}"

    # ── Ventajas — nombre y descripcion ──────────────────────────────────────
    # Las pasa por renpy.translate_string() obtener_desbloqueos_stat()
    # (core/relationships/relationship_unlocks.rpy) al armar la lista del panel.
    # El nombre es la linea de la lista; la descripcion sale en el cuadro al
    # pasar el mouse (o al tocarla, en tactil). Ventaja nueva => entrada nueva.

    # Acceso a la habitación
    old "Entrar a la habitación de trasnoche"
    new "Enter her room after midnight"

    old "Puedes entrar a su habitación de madrugada sin golpear. Es el nivel de confianza más alto."
    new "You can walk into her room after midnight without knocking. The highest level of trust."

    old "Entrar a la habitación durante el día"
    new "Enter her room during the day"

    old "Puedes entrar a su habitación de día sin golpear ni pedir permiso."
    new "You can walk into her room during the day without knocking or asking."

    old "Te deja pasar al golpear la puerta"
    new "She lets you in when you knock"

    old "Si golpeas, te abre y te deja pasar a su habitación."
    new "If you knock, she opens up and lets you into her room."

    old "Sale al pasillo cuando golpeas la puerta"
    new "She comes out to the hallway when you knock"

    old "Si golpeas, sale a hablar al pasillo, pero todavía no te deja entrar."
    new "If you knock, she comes out to talk in the hallway, but won't let you in yet."

    # El marcador {npc} se conserva en el `new`: no es un placeholder de Ren'Py,
    # lo sustituye obtener_desbloqueos_stat DESPUES de traducir.
    old "{npc} no me ignora (Tarde)"
    new "{npc} doesn't ignore me (Afternoon)"

    old "Al interactuar con su puerta por la tarde, {npc} responde y sale al pasillo a hablar."
    new "If you interact with her door in the afternoon, {npc} answers and comes out to the hallway to talk."

    old "{npc} no me ignora (Noche)"
    new "{npc} doesn't ignore me (Night)"

    old "Al interactuar con su puerta por la noche, {npc} responde y sale al pasillo a hablar."
    new "If you interact with her door at night, {npc} answers and comes out to the hallway to talk."

    # Conversación
    old "Estado Buen Humor"
    new "Good Mood state"

    old "Al hablar con ella puede tener este estado asignado, que garantiza +1 ❤️ en todas las opciones."
    new "When you talk to her she can be in this mood, which guarantees +1 ❤️ on every option."

    old "Estado Muy Buen Humor"
    new "Great Mood state"

    old "Al hablar con ella puede tener este estado asignado, que garantiza ❤️ en todas las opciones: algunas dan +1 y otras +2."
    new "When you talk to her she can be in this mood, which guarantees ❤️ on every option: some give +1 and others +2."

    old "Estado Hot"
    new "Hot state"

    old "Al hablar con ella puede tener este estado asignado, que garantiza 💋 en todas las opciones: algunas dan +1 y otras +2."
    new "When you talk to her she can be in this mood, which guarantees 💋 on every option: some give +1 and others +2."

    old "Conocerla"
    new "Knowing her"

    # Trasnoche
    old "Puedes hablarle de madrugada"
    new "You can talk to her in the middle of the night"

    old "Aunque sea de madrugada te atiende en vez de estar durmiendo."
    new "Even in the middle of the night she'll talk to you instead of being asleep."

    old "Al hablar con ella siempre ves el resultado de una de las respuestas."
    new "When you talk to her you always see the outcome of one of the replies."

    # Memoria sin tope — ventaja del hito de deseo 10
    old "Recordar"
    new "Remembering"

    old "Al hablar con ella siempre ves el resultado de tu elección pasada con ese estado."
    new "When you talk to her you always see the outcome of your past choice in that mood."

    # ── Hitos de Violet — nombre y descripcion ───────────────────────────────
    # Los pasa por renpy.translate_string() obtener_desbloqueos_stat()
    # (core/relationships/relationship_unlocks.rpy) al armar la lista del panel.
    # Los nombres de esta tanda son PROVISORIOS: si cambian en hitos_violet.rpy,
    # hay que cambiar el `old` de acá o la entrada queda huérfana.

    # Amor
    old "Buena relación"
    new "Good relationship"

    old "Violet me tiene confianza y se muestra más abierta."
    new "Violet trusts me and is more open with me."

    old "Volvimos a tener la relación que teníamos."
    new "We're back to how we used to be."

    old "Algo nos pasa"
    new "Something's going on"

    old "Hay algo entre nosotros que ya no podemos ignorar."
    new "There's something between us we can't ignore anymore."

    # Deseo
    old "Me calienta"
    new "She turns me on"

    old "Hay una tensión distinta entre los dos."
    new "There's a different kind of tension between us."

    old "Confesión"
    new "Confession"

    old "Ya nos dijimos lo que estaba pasando."
    new "We told each other what was going on."

    old "La relación cambió de forma definitiva."
    new "The relationship changed for good."

    # ── Estados de animo — Violet ────────────────────────────────────────────
    old "Defensiva"
    new "Defensive"

    old "Molesta"
    new "Annoyed"

    old "Dormida"
    new "Sleepy"

    old "Hambre"
    new "Hungry"

    old "Ansiosa"
    new "Anxious"

    old "Sumisa"
    new "Submissive"

    old "Buen Humor"
    new "Good Mood"

    old "Muy Buen Humor"
    new "Great Mood"

    # El nombre del estado "Hot" NO lleva entrada acá: ya esta traducido en
    # tl/english/script/ui/hud/hud_celular.rpy (la app "Hot" del celular usa el
    # mismo texto) y un `old` repetido rompe el lint.

    # ── Estados de animo — Jasmine ───────────────────────────────────────────
    old "Provocativa"
    new "Teasing"

    old "Celosa"
    new "Jealous"

    old "Tranquila"
    new "Relaxed"

    old "Enérgica"
    new "Energetic"

    old "Agotada"
    new "Exhausted"

    # ── Estados de animo — Monica ────────────────────────────────────────────
    old "Cansada"
    new "Tired"

    old "Ocupada"
    new "Busy"

    old "Picante"
    new "Flirty"

    old "Abierta"
    new "Open"

    # ── Estados de animo compartidos ─────────────────────────────────────────
    old "Alegre"
    new "Cheerful"

    old "Feliz"
    new "Happy"

    # Estado "Insinuante" — escalon previo a "Caliente" (hito de deseo 10).
    # Las comillas angulares del original van como \" en el `new`, igual que en
    # las otras descripciones de estado.
    old "Insinuante"
    new "Flirty"

    old "Estado Insinuante"
    new "Flirty state"

    old "Al hablar con ella puede tener este estado asignado, que garantiza +1 💋 en todas las opciones."
    new "When you talk to her she can be in this mood, which guarantees +1 💋 on every option."

    # =========================================================================
    # Ventajas del hito de amor 20
    # =========================================================================
    # "Jugar" (el nombre de la ventaja) NO lleva entrada acá: ya esta traducido
    # en actionsystem_strings.rpy como nombre de la accion, y comparten texto.

    old "Pasar (Tarde)"
    new "Come in (Afternoon)"

    old "Puedes ingresar a su habitación por la tarde."
    new "We'll be able to go into her room in the afternoon."

    old "Al hacer uso de la acción Jugar, {npc} se puede unir y mejora la relación en +1 ❤️."
    new "When you use the Play action, {npc} may join in and the relationship improves by +1 ❤️."

    old "Juegos Nuevos"
    new "New Games"

    old "Al interactuar con {npc} tienes la opción de jugar un juego nuevo; son escenas especiales con ella."
    new "When you interact with {npc} you'll have the option to play a new game; they're special scenes with her."

    # Lo que Violet dice al enumerar los juegos pendientes. Sale del registro
    # (registrar_juego_nuevo) y se muestra con translate_string, asi que va
    # por `old`/`new` y no por bloque de dialogo.
    old "Siempre quise probar un casco de realidad virtual"
    new "I always wanted to try a virtual reality headset"

    old "Todavía tengo por ahí la Portátil Boy, si la encontramos podríamos jugar"
    new "I still have the Portable Boy around somewhere, if we find it we could play"

    # =========================================================================
    # Ventajas del hito de deseo 20
    # =========================================================================

    old "Pasar (Noche)"
    new "Come in (Night)"

    old "Puedes ingresar a su habitación por la noche."
    new "We'll be able to go into her room at night."

    old "Ver Anime"
    new "Watch Anime"

    old "Al hacer uso de la acción Ver Anime, {npc} se puede unir y mejora la relación en +1 💋."
    new "When you use the Watch Anime action, {npc} may join in and the relationship improves by +1 💋."

    old "Mensajear"
    new "Texting"

    old "Ahora puedes escribirle a {npc} por el chat cuando quieras y tener conversaciones especiales con ella."
    new "Now we can text {npc} whenever we want and have special conversations with her."

    # =========================================================================
    # Ventajas del hito de amor 30
    # =========================================================================
    # El NOMBRE "Ropa Nueva" no lleva entrada acá: ya esta traducido en
    # quest_strings.rpy como nombre de evento y comparten texto. Solo va su
    # descripcion, que si es nueva.

    old "Beso (Amor)"
    new "Kiss (Love)"

    old "Estando en su habitación por la tarde, en el menú de {npc} tienes la opción de besarla, una vez por día."
    new "While in her room in the afternoon, {npc}'s menu will have the option to kiss her, once per day."

    old "En el menú de {npc} le puedes pedir que te muestre cómo le queda algo nuevo."
    new "{npc}'s menu lets you ask her to show us how something new looks on her."

    # =========================================================================
    # Ventajas del hito de deseo 30
    # =========================================================================
    # "Beso (Deseo)" es a la vez el nombre de la ventaja y el texto del boton:
    # una sola entrada sirve para los dos.

    old "Beso (Deseo)"
    new "Kiss (Desire)"

    old "Estando en su habitación por la noche, en el menú de {npc} tienes otra forma de besarla, una vez por día."
    new "While in her room at night, {npc}'s menu will have another way to kiss her, once per day."

    old "Provocación"
    new "Teasing"

    old "En distintos momentos {npc} te va a estar provocando; son escenas especiales que aparecen solas."
    new "At different moments {npc} will be teasing us; they're special scenes that show up on their own."

    old "Nuevos Chats"
    new "New Chats"

    old "Al escribirle a {npc} se abren conversaciones nuevas, mas directas que las de antes."
    new "Texting {npc} unlocks new conversations, more forward than the earlier ones."

    # Hitos marcador de fin de linea (proximamente=True). Su descripcion
    # comparte el `old` que ya vive en el tl de hud_pistas.
    old "Próximamente"
    new "Coming soon"

    # =========================================================================
    # Subapp de contenido de una ventaja (el ojo del panel)
    # =========================================================================
    # El nombre de cada situacion y su PISTA de como llegar. Las pistas son lo
    # que el jugador viene a leer, asi que se traducen como instrucciones y no
    # como descripciones.
    #
    # "Pensando en Violet" no esta acá: es tambien el nombre de la quest de
    # deseo 20 y comparte el `old` de quest_strings.rpy.

    old "{} — Contenido"
    new "{} — Content"

    old "Todavía no hay contenido cargado para esta ventaja."
    new "There's no content loaded for this perk yet."

    old "Lo que aparece con 🔒 todavía no se puede alcanzar; hace falta avanzar en otra parte primero."
    new "Anything marked 🔒 can't be reached yet; you need to make progress elsewhere first."

    old "Es la quest de 20 💋. Entra de noche a tu habitación y escríbele desde el celular."
    new "It's the 20 💋 quest. Go to your room at night and text her from your phone."

    old "La intención"
    new "The Intention"

    old "Escríbele estando ella en su habitación y libre. Según cómo le contestes cuando pregunte qué buscas, la charla sigue o se corta."
    new "Text her while she's in her room and free. Depending on how you answer when she asks what you're after, the chat continues or ends."

    old "La intención · segunda parte"
    new "The Intention · Part Two"

    old "Sale sola la próxima vez que le escribas, pero solo si en la charla anterior te hiciste el disimulado."
    new "It comes up on its own the next time you text her, but only if you played dumb in the previous chat."

    old "Justo antes de la ducha"
    new "Right Before the Shower"

    old "Escríbele de noche, mientras esté en el baño a punto de bañarse."
    new "Text her at night, while she's in the bathroom about to shower."

    old "Casco de realidad virtual"
    new "VR Headset"

    old "Cómpralo en la tienda del celular y después propónselo desde su menú."
    new "Buy it in the phone store, then suggest it from her menu."

    old "Elige Ropa Nueva en su menú y pídele el vestido."
    new "Pick New Clothes from her menu and ask her for the dress."

    old "El jean, otra vez"
    new "The Jeans, Again"

    old "Elige Ropa Nueva en su menú y pídele el jean. Si no están en su habitación, te cita allá."
    new "Pick New Clothes from her menu and ask her for the jeans. If you are not in her room, she will summon you there."

    old "El beso"
    new "The Kiss"

    old "Elige Beso (Amor) en su menú, en su habitación por la tarde y a solas. Una vez por día."
    new "Pick Kiss (Love) from her menu, in her room in the afternoon and with her alone. Once per day."

    old "El otro beso"
    new "The Other Kiss"

    old "Elige Beso (Deseo) en su menú, en su habitación por la noche y a solas. Una vez por día."
    new "Pick Kiss (Desire) from her menu, in her room at night and with her alone. Once per day."

    old "La puerta entreabierta"
    new "The Door Left Ajar"

    old "Ve al pasillo de arriba mientras se esté bañando. No pasa siempre: depende de si ella dejó la puerta así."
    new "Go to the upstairs hallway while she's showering. It doesn't always happen: it depends on whether she left the door that way."

