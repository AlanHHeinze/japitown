################################################################################
## NPC: LEAH — amiga de Violet
################################################################################
## Una de las dos amigas de Violet. Aparece por primera vez en la quest de amor
## 35 (la noche de película en el sótano) y va a tener contenido propio en
## actualizaciones futuras, por eso vive en su propia carpeta de personaje y no
## adentro de las quests de Violet.
##
## CARACTER: reservada, pero **completamente sincera**. Es el termometro de la
## escena: dice en voz alta lo que los otros tres estan esquivando. No tiene
## malicia — por eso lo que dice incomoda.
##
## La otra amiga es Zowie (energetica, va al frente, la que se insinua al MC).
##
## LO QUE TODAVIA NO ES: Leah NO esta registrada como NPC del sistema
## (`sistema_npcs`). No tiene rutinas, ni stats, ni menu de interaccion, ni
## talk, ni chat. Existe como PERSONAJE DE DIALOGO y sus sprites, que es lo que
## la quest de amor 35 necesita. Cuando tenga contenido propio, lo que hay que
## sumar es:
##   - registro del NPC + rutinas visuales (ver definition_violet.rpy)
##   - contacto de chat (CONTACTOS_ESPECIALES en messagesystem_core.rpy, si va
##     a escribir sin ser NPC; si es NPC, `inicializar_chat`)
##   - visual/skins_leah.rpy, talk/, quests/ — la misma estructura que Violet
################################################################################


# El color va como constante: lo usan el personaje y cualquier variante suya
# (susurro, pensamiento) que se agregue despues. Asi no se pueden desfasar.
#
# El nombre NO se lee contra el fondo del textbox: `style.say_label.outlines`
# (ui/base/gui.rpy) le pone un borde BLANCO de 2px — 4px en pantalla chica — a
# todos los nombres. O sea que el contraste que importa es contra el blanco, y
# ahi un relleno oscuro es lo que mejor funciona: este da 13.9:1 (Monica 5.58,
# Violet 4.10, MC 2.37, Jasmine 2.23, Zowie 2.14). Un color CLARO seria el
# problema, no uno oscuro.
define LEAH_COLOR = "#302b31"

define leah = Character("Leah", color=LEAH_COLOR)
