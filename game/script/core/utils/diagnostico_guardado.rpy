################################################################################
## Diagnóstico de guardados que fallan
################################################################################
## Para errores del tipo "TypeError: cannot pickle 'X' instances" al guardar.
##
## POR QUE NO SE USA config.save_dump:
## dump_paths() de Ren'Py asume que si __getstate__ devuelve una tupla es
## (state, slots) y la desempaqueta a ciegas (compat/pickle.py:143). En este
## proyecto algo devuelve una tupla de un solo elemento, asi que save_dump
## revienta en CADA guardado — rompe el juego en vez de diagnosticarlo.
##
## Este modulo hace lo mismo pero a mano y sin romper nada: recorre lo que iria
## al save y reporta que objeto no se puede serializar y por que camino se
## llega a el.

init python:

    def jp_buscar_no_picklables(limite=40):
        """
        Recorre el estado que iria al save y devuelve las rutas de todo lo que
        no se pueda serializar.

        Prueba objeto por objeto en vez de todo junto: asi el primer fallo no
        corta la busqueda y se ven TODOS los culpables de una.

        Returns:
            list[str]: descripciones "ruta = <tipo> (motivo)"
        """
        import pickle as _pk

        fallos = []
        vistos = set()

        def _picklable(obj):
            try:
                _pk.dumps(obj, _pk.HIGHEST_PROTOCOL)
                return True, None
            except Exception as e:
                return False, "{}: {}".format(type(e).__name__, e)

        def _visitar(obj, ruta, profundidad):
            if len(fallos) >= limite or profundidad > 6:
                return

            ido = id(obj)
            if ido in vistos:
                return
            vistos.add(ido)

            ok, motivo = _picklable(obj)
            if ok:
                return

            # El objeto falla. Bajar para ubicar al culpable exacto; si ningun
            # hijo falla, el problema es este objeto.
            hijos = []
            try:
                if isinstance(obj, dict):
                    hijos = [("{}[{!r}]".format(ruta, k), v) for k, v in obj.items()]
                elif isinstance(obj, (list, tuple, set, frozenset)):
                    hijos = [("{}[{}]".format(ruta, i), v) for i, v in enumerate(obj)]
                elif hasattr(obj, "__dict__"):
                    hijos = [("{}.{}".format(ruta, k), v) for k, v in vars(obj).items()]
            except Exception:
                hijos = []

            antes = len(fallos)
            for sub_ruta, sub_obj in hijos:
                _visitar(sub_obj, sub_ruta, profundidad + 1)

            if len(fallos) == antes:
                fallos.append("{} = <{}>  ({})".format(
                    ruta, type(obj).__name__, motivo))

        try:
            raices = renpy.game.log.get_roots()
        except Exception as e:
            return ["No se pudieron obtener las raices del save: {}".format(e)]

        for nombre, valor in raices.items():
            _visitar(valor, "store." + nombre, 0)

        return fallos

    def jp_reportar_no_picklables():
        """
        Corre la busqueda y deja el resultado a la vista: notificacion, consola
        y el archivo diagnostico_guardado.txt en la raiz del proyecto.
        Pensada para engancharla a un boton del panel de cheats.
        """
        import os

        fallos = jp_buscar_no_picklables()

        if not fallos:
            texto = "Todo el estado del juego se puede guardar. No hay objetos problematicos."
        else:
            texto = "OBJETOS QUE ROMPEN EL GUARDADO ({}):\n\n".format(len(fallos))
            texto += "\n".join("  - " + f for f in fallos)

        try:
            ruta = os.path.join(config.basedir, "diagnostico_guardado.txt")
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(texto + "\n")
        except Exception:
            pass

        print(texto)

        try:
            if fallos:
                renpy.notify("{} objeto(s) rompen el guardado - ver diagnostico_guardado.txt".format(len(fallos)))
            else:
                renpy.notify("Guardado OK: no hay objetos problematicos")
        except Exception:
            pass

        return fallos
