# Mensajes del minijuego de espiar que se muestran por interpolacion
# (piensa "[_esp_foto_msg]") en vez de como dialogo literal.
#
# La interpolacion NO pasa por la traduccion de bloques con hash: el texto lo
# traduce renpy.translate_string() en el propio label (accion_espiar_foto, en
# script/core/espiar/espiar_system.rpy) y por eso necesita un `old` aca.

translate english strings:

    old "(Contenido en desarrollo)"
    new "(Content in development)"

    old "Espiar (requiere [ESPIAR_DESEO_MINIMO] 💋)"
    new "Peek (requires [ESPIAR_DESEO_MINIMO] 💋)"
