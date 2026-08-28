# Textos del sistema de compatibilidad de partidas entre versiones
# (script/core/utils/compatibilidad_saves.rpy).
#
# El aviso de partida incompatible se muestra por interpolacion
# (centered "[_jp_aviso]"), que NO traduce: lo traduce el label via
# renpy.translate_string y necesita un `old` aca.
#
# La plantilla usa {version} — translate_string traduce la PLANTILLA y despues
# se hace .format(version=...), asi que el `new` debe conservar el {version}.

translate english strings:

    # Aviso al intentar cargar una partida de otra generacion de guardado
    old "{size=+8}Partida incompatible{/size}\n\nEsta partida fue creada con una versión anterior de Japitown y no se puede continuar en la versión actual ({version}).\n\nTus partidas anteriores siguen en el disco: si querés retomarlas, podés volver a instalar la versión con la que las creaste."
    new "{size=+8}Incompatible save{/size}\n\nThis save was created with an earlier version of Japitown and can't be continued on the current version ({version}).\n\nYour older saves are still on disk: if you want to go back to them, you can reinstall the version they were made with."

    # Marca del slot en las pantallas de Guardar y Cargar
    old "v[_jp_slot_ver] · incompatible"
    new "v[_jp_slot_ver] · incompatible"
