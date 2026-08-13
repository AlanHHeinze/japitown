################################################################################
## Red de seguridad: builtins pisados en el store
################################################################################
## Si una variable del store tapa un builtin de Python (int, str, len...), TODO
## el código que use ese builtin revienta con "'X' object is not callable" —
## incluidos los screens del HUD, o sea el juego entero.
##
## Y es peor de lo que parece: las variables del store SE GUARDAN. Una vez que
## pasa, la partida queda envenenada de forma permanente y el jugador no tiene
## forma de saber por qué ni de arreglarlo.
##
## Ya nos pasó dos veces:
##   - `_p` (E01/S02): un `for _i, _p in ...` en talksystem pisaba el builtin de
##     Ren'Py y hacía crashear `define gui.about = _p(...)` al cambiar de idioma.
##   - `int` (S05): alguien con la consola de desarrollador abierta escribió
##     `int = <numero>`; a partir de ahí el HUD crasheaba en `int(120 * _pe_k)`.
##
## Este módulo detecta y limpia esos casos al iniciar y al cargar. NO tapa bugs
## nuestros en silencio: en modo desarrollador avisa por consola, así si el
## culpable es el código del juego igual se ve.

init -100 python:

    # Builtins que nunca deberían existir como variable del store. No se
    # incluyen `_`, `__` ni `_p`: esos SÍ son del store en Ren'Py (traducción y
    # formato de párrafos), así que borrarlos rompería el juego.
    #
    # TAMPOCO van `list`, `dict` ni `set` (ni `object`): Ren'Py los reemplaza A
    # PROPOSITO en el store por sus versiones revertibles —RevertableList,
    # RevertableDict, RevertableSet (renpy/minstore.py:41,45,53)— para que el
    # rollback trackee las mutaciones. Son distintos del builtin por diseño, asi
    # que la comparación de abajo los daba por "pisados" y los BORRABA del store.
    # Resultado: al cambiar de idioma, clean_data() hace renpy.store.list() y
    # revienta con "'StoreModule' object has no attribute 'list'". Bug real,
    # 2026-08-06.
    JP_BUILTINS_PROTEGIDOS = (
        "int", "str", "float", "bool", "tuple",
        "len", "min", "max", "abs", "round", "sum", "sorted", "range",
        "type", "id", "print", "open", "getattr", "setattr", "hasattr",
        "isinstance", "enumerate", "zip", "map", "filter", "any", "all",
    )

    def jp_limpiar_builtins_pisados():
        """
        Borra del store las variables que tapan un builtin.

        Compara contra el builtin real: solo borra si el nombre está en el store
        Y su valor es distinto del original. Así no toca nada que Ren'Py haya
        puesto ahí legítimamente.

        Returns:
            list[str]: nombres limpiados (vacío si no había ninguno)
        """
        import builtins as _bi

        try:
            store_dict = renpy.python.store_dicts.get("store")
        except Exception:
            return []

        if not store_dict:
            return []

        limpiados = []

        for nombre in JP_BUILTINS_PROTEGIDOS:
            if nombre not in store_dict:
                continue

            original = getattr(_bi, nombre, None)
            if original is None:
                continue

            # Si es el builtin de siempre, no hay nada que arreglar.
            if store_dict[nombre] is original:
                continue

            try:
                del store_dict[nombre]
                limpiados.append(nombre)
            except Exception:
                pass

        if limpiados and config.developer:
            print(
                "[Builtins] Se limpiaron variables del store que tapaban "
                "builtins: {}. Si no fue la consola, hay codigo del juego "
                "asignando esos nombres.".format(", ".join(limpiados))
            )

        return limpiados


init python:

    def _jp_builtins_after_load():
        """Limpieza al cargar: la partida pudo guardarse ya envenenada."""
        try:
            jp_limpiar_builtins_pisados()
        except Exception:
            pass

    if not hasattr(config, "after_load_callbacks"):
        config.after_load_callbacks = []
    if _jp_builtins_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_jp_builtins_after_load)

    # Tambien al cambiar de idioma: ese momento re-evalua los `define` (es donde
    # nos exploto `_p` en su momento), asi que conviene entrar limpio.
    if _jp_builtins_after_load not in config.change_language_callbacks:
        config.change_language_callbacks.append(_jp_builtins_after_load)
