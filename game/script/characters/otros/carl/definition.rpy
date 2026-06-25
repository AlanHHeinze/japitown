################################################################################
## Definición de Carl
################################################################################

init 5 python:
    # Crear NPC Carl
    carl = NPC(
        id="carl",
        nombre="Carl",
        nombre_completo="Carl",
    )

    # Registrar NPC
    if hasattr(store, 'sistema_npcs'):
        store.sistema_npcs.registrar_npc(carl)
