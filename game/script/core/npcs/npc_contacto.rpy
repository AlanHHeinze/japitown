################################################################################
## Contacto diario con un NPC — "¿hoy hiciste algo con ella?"
################################################################################
## Registro chico y generico: marca a los NPCs con los que el jugador hizo algo
## en el dia en curso. Se resetea al dormir, junto al resto de los limites
## diarios.
##
## PARA QUE SIRVE: contenido que necesita medir lo CONTRARIO, o sea ignorar a
## alguien. Hoy lo usa la quest de deseo 30 de Violet, que pide tres dias
## seguidos sin tocarla.
##
## COMO SE MARCA — no lo llama el contenido, lo llaman los EMBUDOS del motor,
## que es lo que hace que funcione sin tener que acordarse en cada escena:
##
##   1. `NPC._aplicar_cambio_stat`  — todo cambio de amor/deseo pasa por ahi
##      (talk, chat, quests, eventos, espiar, acciones, besos, ropa nueva...).
##   2. `completar_quest_actual`    — cerrar una quest de ese NPC.
##   3. `GrupoMensajes.finalizar`   — terminar una conversacion del chat.
##   4. `sistema_talk` al cerrar    — hablarle, aunque el resultado sea "nada"
##      y no mueva ningun stat.
##
## Los tres primeros cubren casi todo por si solos; el cuarto esta porque es el
## unico caso donde el jugador SI interactuo y el stat pudo no moverse.
##
## LO QUE NO CUENTA COMO CONTACTO, a proposito: una accion compartida en la que
## ella NO aparecio (Ver Anime o Jugar cuando el sorteo dice que no se une). No
## mueve stats y no la vio — que el jugador se quede mirando anime solo no es
## interactuar con ella.
##
## `marcar_contacto_npc()` esta expuesta igual por si algun contenido futuro
## necesita declararlo a mano.


# Ids de los NPCs con los que el jugador hizo algo HOY. Lista y no set porque se
# guarda en el save y una lista se lee mejor en un dump.
default npc_contacto_hoy = []


init python:

    def marcar_contacto_npc(npc_id):
        """Deja constancia de que el jugador hizo algo con este NPC hoy."""
        if not npc_id:
            return
        _lista = getattr(store, 'npc_contacto_hoy', None)
        if _lista is None:
            return
        if npc_id not in _lista:
            _lista.append(npc_id)

    def hubo_contacto_npc(npc_id):
        """True si el jugador ya hizo algo con este NPC en el dia en curso."""
        return npc_id in getattr(store, 'npc_contacto_hoy', [])

    def resetear_contacto_npcs():
        """
        Arranca un dia nuevo. La llama dormir(), con el resto de los reseteos
        diarios, DESPUES de los triggers de dormir en fase "antes" — que es
        donde el contenido lee el contador del dia que termina.
        """
        store.npc_contacto_hoy = []
