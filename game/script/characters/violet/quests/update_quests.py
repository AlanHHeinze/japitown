import re

with open("quest_violet.rpy", "r", encoding="utf-8") as f:
    text = f.read()

# Replace block by block using specific patterns to avoid overlap
# Old 22 -> 3
text = text.replace("QUEST 22 - Limpieza del Sábado", "QUEST 3 - Limpieza del Sábado")
text = text.replace("quest_violet_22 = Quest", "quest_violet_3 = Quest")
text = text.replace('id="violet_questprincipal_22"', 'id="violet_questprincipal_3"')
text = text.replace('sistema_quests.registrar_quest(quest_violet_22)', 'sistema_quests.registrar_quest(quest_violet_3)')
text = text.replace("obtener_quest('violet_questprincipal_22')", "obtener_quest('violet_questprincipal_3')")
# For quest 22 it originally had numero_quest=2
# But it will become numero_quest=3, quest_anterior = 2
text = re.sub(r'id="violet_questprincipal_3",.*?numero_quest=\d+', 'id="violet_questprincipal_3",\n        npc_id="violet",\n        nombre="Limpieza del Sábado",\n        descripcion="Monica me pidio que limpie la casa con Violet el sabado por la mañana.",\n        numero_quest=3', text, flags=re.DOTALL)
text = re.sub(r'id="violet_questprincipal_3".*?quest_anterior=".*?"', 'id="violet_questprincipal_3",\n        npc_id="violet",\n        nombre="Limpieza del Sábado",\n        descripcion="Monica me pidio que limpie la casa con Violet el sabado por la mañana.",\n        numero_quest=3,\n        dias_espera=4,\n        quest_anterior="violet_questprincipal_2"', text, flags=re.DOTALL)


# Let's do the rest recursively, using intermediate tokens
mapping = [
    (8, 12, 11),  # old 8 -> 12, prev 11
    (7, 11, 10),
    (6,  8,  7),
    (5,  7,  6),
    (4,  6,  5),
    (3,  5,  4),
]

for old, new, prev in mapping:
    # Header
    text = text.replace(f"QUEST {old} -", f"QUEST {new}_TEMPO -")
    text = text.replace(f"quest_violet_{old} = Quest", f"quest_violet_{new}_TEMP = Quest")
    text = text.replace(f'id="violet_questprincipal_{old}"', f'id="violet_questprincipal_{new}_TEMP"')
    text = text.replace(f'sistema_quests.registrar_quest(quest_violet_{old})', f'sistema_quests.registrar_quest(quest_violet_{new}_TEMP)')
    text = text.replace(f"obtener_quest('violet_questprincipal_{old}')", f"obtener_quest('violet_questprincipal_{new}_TEMP')")
    # Change numero_quest
    text = re.sub(rf'id="violet_questprincipal_{new}_TEMP".*?numero_quest=\d+', lambda m: m.group(0).replace(f"numero_quest={old}", f"numero_quest={new}"), text, flags=re.DOTALL)
    # Change quest_anterior. Note: we just replace the quest_anterior arg in that block
    text = re.sub(rf'(id="violet_questprincipal_{new}_TEMP".*?)quest_anterior=".*?"', rf'\1quest_anterior="violet_questprincipal_{prev}_TEMP"', text, flags=re.DOTALL)

# Cleanup TEMPO tags
text = text.replace("_TEMPO", "")
text = text.replace("_TEMP", "")

# Special case for quest_violet_5 (old 3) which prev should be completely 4
text = text.replace('quest_anterior="violet_questprincipal_4_TEMP"', 'quest_anterior="violet_questprincipal_4"')

with open("quest_violet.rpy", "w", encoding="utf-8") as f:
    f.write(text)
