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
    old "Hito: Conseguir un Hito nos permite avanzar en misiones principales y desbloquear elecciones únicas."
    new "Milestone: Reaching a Milestone lets you advance in main quests and unlock unique choices."

    old "Desbloquear una Ventaja nos da mejoras permanentes en algunas interacciones con el personaje."
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

    old "Podés entrar a su habitación de madrugada sin golpear. Es el nivel de confianza más alto."
    new "You can walk into her room after midnight without knocking. The highest level of trust."

    old "Entrar a la habitación durante el día"
    new "Enter her room during the day"

    old "Podés entrar a su habitación de día sin golpear ni pedir permiso."
    new "You can walk into her room during the day without knocking or asking."

    old "Te deja pasar al golpear la puerta"
    new "She lets you in when you knock"

    old "Si golpeás, te abre y te deja pasar a su habitación."
    new "If you knock, she opens up and lets you into her room."

    old "Sale al pasillo cuando golpeás la puerta"
    new "She comes out to the hallway when you knock"

    old "Si golpeás, sale a hablar al pasillo, pero todavía no te deja entrar."
    new "If you knock, she comes out to talk in the hallway, but won't let you in yet."

    old "Sale al pasillo si golpeás por la tarde"
    new "She comes out to the hallway if you knock in the afternoon"

    old "Por la tarde sale a hablar al pasillo cuando golpeás. A otras horas no atiende."
    new "In the afternoon she comes out to talk when you knock. At other times she doesn't answer."

    old "Sale al pasillo si golpeás por la noche"
    new "She comes out to the hallway if you knock at night"

    old "Por la noche sale a hablar al pasillo cuando golpeás. A otras horas no atiende."
    new "At night she comes out to talk when you knock. At other times she doesn't answer."

    # Conversación
    old "Puede estar de buen humor"
    new "She can be in a good mood"

    old "Se suma «Buen Humor» a sus estados de ánimo posibles del día. En ese estado las conversaciones dan más puntos."
    new "\"Good Mood\" is added to her possible moods for the day. In that mood conversations give more points."

    old "Puede estar de muy buen humor"
    new "She can be in a great mood"

    old "Se suma «Muy Buen Humor» a sus estados posibles. Es el estado que más recompensa da al conversar."
    new "\"Great Mood\" is added to her possible moods. It's the mood that rewards conversation the most."

    old "Puede estar en un estado de ánimo especial"
    new "She can be in a special mood"

    old "Se suma un estado de ánimo nuevo, con opciones de conversación que antes no aparecían."
    new "A new mood is added, with conversation options that didn't show up before."

    old "Intuís el resultado de una de las opciones"
    new "You sense the outcome of one of the options"

    # Trasnoche
    old "Podés hablarle de madrugada"
    new "You can talk to her in the middle of the night"

    old "Aunque sea de madrugada te atiende en vez de estar durmiendo."
    new "Even in the middle of the night she'll talk to you instead of being asleep."

    old "Antes de elegir, una de las opciones de la conversación te muestra qué resultado va a dar."
    new "Before you choose, one of the conversation options shows you what result it will give."

    # ── Hitos de Violet — nombre y descripcion ───────────────────────────────
    # Los pasa por renpy.translate_string() obtener_desbloqueos_stat()
    # (core/relationships/relationship_unlocks.rpy) al armar la lista del panel.
    # Los nombres de esta tanda son PROVISORIOS: si cambian en hitos_violet.rpy,
    # hay que cambiar el `old` de acá o la entrada queda huérfana.

    # Amor
    old "Buena relación"
    new "Good relationship"

    old "Violet me tiene confianza y se muestra mas abierta."
    new "Violet trusts me and is more open with me."

    old "Como antes"
    new "Like before"

    old "Volvimos a tener la relacion que teniamos."
    new "We're back to how we used to be."

    old "Algo nos pasa"
    new "Something's going on"

    old "Hay algo entre nosotros que ya no podemos ignorar."
    new "There's something between us we can't ignore anymore."

    # Deseo
    old "Me atrae"
    new "I'm drawn to her"

    old "Hay una tension distinta entre los dos."
    new "There's a different kind of tension between us."

    old "Confesión"
    new "Confession"

    old "Ya nos dijimos lo que estaba pasando."
    new "We told each other what was going on."

    old "Un paso más allá"
    new "One step further"

    old "La relacion cambio de forma definitiva."
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

    old "Caliente"
    new "Turned On"

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
