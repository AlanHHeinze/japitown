# Textos del sistema de notificaciones flotantes (hud_notificaciones.rpy).
#
# Los nombres de item NO van acá: se traducen desde CATALOGO_ITEMS y ya están en
# tl/english/script/core/shopping/shopping_strings.rpy. La notificación arma el
# texto como "{emoji} + {nombre}", asi que traduce el nombre por separado
# (_nombre_item_traducido) — el string ya compuesto nunca matchearia un `old`.
#
# Las notificaciones de stats solo muestran signo + número (y el nombre propio del
# NPC), asi que no necesitan traducción.

translate english strings:

    old "Recuerdo activado"
    new "Memory unlocked"

    # El {} lo reemplaza el nombre del NPC — conservarlo en el `new`.
    old "{} recordará esto"
    new "{} will remember this"
