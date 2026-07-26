# Traducciones de los chats de Jasmine (chat_jasmine.rpy).
#
# Son strings de Python dentro de `init 6 python`, no diálogo: se traducen con un
# bloque `strings`, no con bloques de diálogo por hash.
#
# Los mensajes que son solo emoji (❤️ 😢 😏) no se traducen: translate_string los
# devuelve tal cual. Por eso los emoji van como mensaje aparte dentro de la lista
# de respuesta_npc y NO pegados al texto: si se pegan, el string cambia y hay que
# traducir la misma frase dos veces.

translate english strings:

    old "Lo voy a estar usando, cuando quieras pasa a verlo"
    new "I'll be wearing it, come see it whenever you want"

    old "Te estás perdiendo tú de verlo"
    new "You're the one missing out on seeing it"
