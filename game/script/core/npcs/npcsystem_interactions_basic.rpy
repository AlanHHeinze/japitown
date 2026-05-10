################################################################################
## Labels de Interacciones Genéricas
################################################################################
## Label que maneja la interacción "Hablar" con NPCs.
## Delega en un label de conversación específico por NPC que:
##   - Muestra sprites de MC y NPC
##   - Presenta una pregunta aleatoria del pool del NPC
##   - Ofrece 3 opciones (cada una sube un stat distinto)
##   - Solo se puede hacer 1 vez por día por NPC

# Variable temporal para pasar el NPC ID
default _npc_id_temp = None


label interaccion_hablar:
    # Delega en el nuevo sistema de talk.
    # _npc_id_temp ya está seteado por el menu de interacción.
    call talk_iniciar from _call_talk_iniciar
    return
