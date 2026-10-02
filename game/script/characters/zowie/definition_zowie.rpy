################################################################################
## NPC: ZOWIE — amiga de Violet
################################################################################
## La otra amiga de Violet (la primera es Leah, en characters/leah/). Aparece
## por primera vez en la quest de amor 35 (la noche de película en el sótano) y
## va a tener contenido propio en actualizaciones futuras, por eso vive en su
## propia carpeta de personaje y no adentro de las quests de Violet.
##
## CARACTER: energetica, va al frente. Es la que **se insinua ligeramente al
## MC**, y eso es lo que dispara los celos de Violet — o sea que es el motor de
## la 35 y el motivo de la 40.
##
## Ademas es la que manda la solicitud de amistad por XGram al principio de la
## quest de amor 40. Si en algun momento se decide que le escriba, va a hacer
## falta darle contacto de chat (ver abajo).
##
## Contraste con Leah: Zowie empuja, Leah observa. En una escena con las dos, si
## alguien incomoda a proposito es Zowie; si alguien incomoda sin querer, Leah.
##
## LO QUE TODAVIA NO ES: Zowie NO esta registrada como NPC del sistema
## (`sistema_npcs`). No tiene rutinas, ni stats, ni menu de interaccion, ni
## talk, ni chat. Existe como PERSONAJE DE DIALOGO y sus sprites, que es lo que
## la quest de amor 35 necesita. Cuando tenga contenido propio, lo que hay que
## sumar es:
##   - registro del NPC + rutinas visuales (ver definition_violet.rpy)
##   - contacto de chat (CONTACTOS_ESPECIALES en messagesystem_core.rpy, si va
##     a escribir sin ser NPC; si es NPC, `inicializar_chat`)
##   - visual/skins_zowie.rpy, talk/, quests/ — la misma estructura que Violet
################################################################################


# El color va como constante: lo usan el personaje y cualquier variante suya
# (susurro, pensamiento) que se agregue despues. Asi no se pueden desfasar.
#
# Sobre el contraste: el nombre lleva borde BLANCO de 2px — 4px en pantalla
# chica — por `style.say_label.outlines` (ui/base/gui.rpy), asi que lo que
# importa es como se ve el relleno contra ese blanco, no contra el fondo del
# textbox. Este rosa da 2.14:1, en linea con Jasmine (2.23) y el MC (2.37).
define ZOWIE_COLOR = "#e99abb"

define zowie = Character("Zowie", color=ZOWIE_COLOR)
