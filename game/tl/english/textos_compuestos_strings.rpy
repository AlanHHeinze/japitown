# Textos COMPUESTOS (plantilla + valores del juego).
#
# Estos textos se arman en runtime con .format(), asi que NO se pueden traducir
# como un todo: para cuando Ren'Py busca el `old`, los valores ya están incrustados
# y nunca matchea. Por eso el codigo traduce la PLANTILLA y le mete los valores
# despues (renpy.translate_string("...").format(...)).
#
# REGLAS al tocar esto:
#   - Los placeholders con nombre ({dias}, {npc}, {lugar}...) DEBEN conservarse en
#     el `new`. Se pueden reordenar u omitir, pero no renombrar.
#   - Singular y plural son plantillas separadas ("Esperar 1 día" / "Esperar {dias}
#     días"): concatenar la "s" solo funciona en español.
#   - Si agregas un texto compuesto nuevo, traduce la plantilla, no el resultado.

translate english strings:

    # =========================================================================
    # Pistas genéricas de quest (questsystem_core.rpy)
    # Las genera el motor cuando una quest no define pista/que_hacer propios.
    # =========================================================================

    old "Debo esperar {dias} días más."
    new "I have to wait {dias} more days."

    old "Esperar {dias} días"
    new "Wait {dias} days"

    old "Esperar 1 día"
    new "Wait 1 day"

    old "Habla con {npc}"
    new "Talk to {npc}"

    # El artículo ("al" / "a la") es gramática del español: el inglés lo ignora
    # y usa solo {lugar}. Por eso el placeholder {articulo} no aparece en el `new`.
    old "Ve {articulo} {lugar}"
    new "Go to the {lugar}"

    old "el {lugar}"
    new "the {lugar}"

    old "durante {horario}"
    new "during {horario}"

    old "El día {dia}"
    new "On {dia}"

    old "Tener {valor} de Amor con {npc}"
    new "Have {valor} Love with {npc}"

    old "Tener {valor} de Deseo con {npc}"
    new "Have {valor} Desire with {npc}"

    old "Tener {valor} de {stat}"
    new "Have {valor} {stat}"

    old "Tener {cantidad}x {item}"
    new "Have {cantidad}x {item}"

    old "Tener ${valor}"
    new "Have ${valor}"

    # =========================================================================
    # Horarios (se insertan en "durante {horario}")
    # =========================================================================

    old "la Mañana"
    new "the Morning"

    old "la Tarde"
    new "the Afternoon"

    old "la Noche"
    new "the Evening"

    old "la Trasnoche"
    new "the Late Night"

    # =========================================================================
    # Quests de Violet (quest_violet.rpy)
    # =========================================================================

    old "Hablar con Violet / Esperar 1 día más"
    new "Talk to Violet / Wait 1 more day"

    old "Hablar con Violet / Esperar {dias} días más"
    new "Talk to Violet / Wait {dias} more days"

    old "Manga leído {leidos}/4"
    new "Manga read {leidos}/4"

    old "Subir deseo 💋 con Violet ({}/{})"
    new "Raise Desire 💋 with Violet ({}/{})"

    # =========================================================================
    # Quest 02 de Violet — limpieza del living (violet_quest02_screens.rpy)
    # =========================================================================

    old "Todavía me falta limpiar: {lista}"
    new "I still have to clean: {lista}"

    old "la chimenea"
    new "the fireplace"

    old "las escaleras"
    new "the stairs"

    old "el sillon"
    new "the couch"

    # =========================================================================
    # Movimiento bloqueado por item (movesystem_validation.rpy)
    # =========================================================================

    old "Necesitas: {item}"
    new "You need: {item}"

    # =========================================================================
    # Galería de fotos (messagesystem_core.rpy)
    # =========================================================================

    old "Foto de {npc}"
    new "Photo from {npc}"

    # =========================================================================
    # Resumen de órdenes de compra (shopping_system.rpy)
    # =========================================================================

    old "Orden de compra N°{numero}"
    new "Purchase order #{numero}"

    old "Contenido:"
    new "Contents:"

    # =========================================================================
    # Pantalla de carga inicial (pantalla_carga.rpy)
    # =========================================================================

    old "Cargando"
    new "Loading"

    # =========================================================================
    # Carteles de paso de tiempo (`show text` sobre pantalla negra)
    # OJO: `show text "literal"` NO se traduce solo — no es un say ni texto de
    # screen. Hay que envolverlo en Text(renpy.translate_string(...)).
    # =========================================================================

    old "30 minutos más tarde"
    new "30 minutes later"

    old "Algunas horas después..."
    new "A few hours later..."

    # =========================================================================
    # Etiqueta de los slots de Guardar/Cargar (jp_nombre_guardado en
    # timesystem_core.rpy). Se muestra delante de la fecha: "Día 22, domingo...".
    # Conservar el placeholder {dia}.
    # =========================================================================

    old "Día {dia}"
    new "Day {dia}"
