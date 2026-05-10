import os

chat_reps = [
    ("violet_quest8_chat", "violet_quest12_chat"),
    ("chat_violet_quest8", "chat_violet_quest12"),
    ("QUEST 8 ", "QUEST 12 "),
    
    ("violet_quest6_chat", "violet_quest8_chat"),
    ("chat_violet_quest6", "chat_violet_quest8"),
    ("QUEST 6 ", "QUEST 8 "),
    
    ("violet_quest5_chat", "violet_quest7_chat"),
    ("chat_violet_quest5", "chat_violet_quest7"),
    ("vq5_rama", "vq7_rama"),
    ("QUEST 5 ", "QUEST 7 "),
    ("set_vq5_rama", "set_vq7_rama"),

    ("violet_quest4_chat", "violet_quest6_chat"),
    ("chat_violet_quest4", "chat_violet_quest6"),
    ("vq4_rama", "vq6_rama"),
    ("QUEST 4 ", "QUEST 6 "),
    ("set_vq4_rama", "set_vq6_rama"),
]

def apply_reps(filename, reps):
    if not os.path.exists(filename): return
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    for o, n in reps:
        text = text.replace(o, n)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

apply_reps("c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/quest_violet.rpy", chat_reps)
apply_reps("c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/chat/chat_violet.rpy", chat_reps)

replacements = {
    "c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/violet_quest_12.rpy": [("8", "12")],
    "c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/violet_quest_11.rpy": [("7", "11")],
    "c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/violet_quest_08.rpy": [("6", "8")],
    "c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/violet_quest_07.rpy": [("5", "7")],
    "c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/violet_quest_06.rpy": [("4", "6")],
    "c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/quests/violet_quest_05.rpy": [("3", "5")],
}

for fname, reps in replacements.items():
    if not os.path.exists(fname): print("Missing", fname); continue
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()

    old, new = reps[0]
    new_fmt = new if int(new)>9 else '0'+new
    text = text.replace(f"Violet Quest 0{old}", f"Violet Quest {new_fmt}")
    text = text.replace(f"quest_violet_{old} ", f"quest_violet_{new} ")
    text = text.replace(f"quest_violet_0{old}", f"quest_violet_{new_fmt}")
    text = text.replace(f"violet_questprincipal_{old}", f"violet_questprincipal_{new}")
    text = text.replace(f"quest_violet_questprincipal_{old}", f"quest_violet_questprincipal_{new}")
    text = text.replace(f"violet_quest{old}_", f"violet_quest{new}_")
    
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)

apply_reps("c:/Users/Alan/OneDrive/Desktop/Japitown/game/script/characters/violet/interaction/interactions_violet.rpy", [
    ("violet_questprincipal_3", "violet_questprincipal_5"),
    ("quest_violet_questprincipal_3", "quest_violet_questprincipal_5")
])

apply_reps("c:/Users/Alan/OneDrive/Desktop/Japitown/.agents/workflows/character_violet.md", [
    ("violet_questprincipal_2` | Limpieza", "violet_questprincipal_3` | Limpieza"),
    ("violet_questprincipal_3` | El cosplay", "violet_questprincipal_5` | El cosplay"),
    ("violet_questprincipal_4` | El cosplay", "violet_questprincipal_6` | El cosplay"),
    ("violet_questprincipal_5` | El cosplay", "violet_questprincipal_7` | El cosplay"),
    ("violet_questprincipal_6` | El cosplay", "violet_questprincipal_8` | El cosplay"),
    ("violet_questprincipal_7` | Los ruidos", "violet_questprincipal_11` | Los ruidos"),
    ("violet_questprincipal_8` | Visita", "violet_questprincipal_12` | Visita")
])
