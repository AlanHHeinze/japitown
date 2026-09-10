################################################################################
## Rutas entre locaciones — el grafo del mapa
################################################################################
## Calcula el camino mas corto entre dos locaciones. Lo usa el viaje rapido para
## recorrerlo en vez de teletransportar (viaje_rapido.rpy).
##
## EL GRAFO NO SE ESCRIBE: SE DEDUCE. Las aristas son los hotspots de tipo MOVE
## de cada locacion, o sea exactamente por donde puede caminar el jugador. Una
## tabla de adyacencias a mano seria un segundo mapa que hay que acordarse de
## actualizar, y el dia que se desincroniza el viaje rapido manda al jugador por
## un camino que a pie no existe.
##
## Por lo mismo, agregar una locacion o un hotspot no pide tocar este archivo.
##
## LAS RUTAS SON DETERMINISTICAS. Los vecinos se recorren en el orden en que se
## registraron los hotspots, asi que dos llamadas con los mismos argumentos dan
## siempre lo mismo. Importa por el rollback de Ren'Py: si la ruta cambiara entre
## una pasada y la siguiente, deshacer y rehacer un viaje podria mandar al
## jugador por otro lado.
##
## HOY EL MAPA ES SOLO LA CASA y esta todo conectado en los dos sentidos. Cuando
## llegue el mapa de ciudad, dos locaciones madre sin hotspot que las una van a
## dar `[]` (sin ruta) y el viaje rapido cae solo al salto directo de siempre;
## para que haya recorrido entre madres hay que unirlas con un MOVE, igual que
## adentro de la casa.

init python:

    def vecinos_locacion(loc_id):
        """
        Locaciones a un paso de esta, leidas de sus hotspots MOVE.

        Se filtran los destinos que no estan registrados: un hotspot que apunta
        a una locacion inexistente es un error de contenido, pero acá tiene que
        traducirse en "por ahi no se va", no en una ruta que despues revienta al
        recorrerla.
        """
        _loc = store.sistema_locaciones.obtener_locacion(loc_id)
        if _loc is None:
            return []

        _vec = []
        for _h in getattr(_loc, "hotspots", []):
            if getattr(_h, "tipo", None) != "MOVE":
                continue
            _d = getattr(_h, "destino", None)
            if not _d or _d not in store.sistema_locaciones.locaciones:
                continue
            if _d not in _vec:
                _vec.append(_d)
        return _vec

    def calcular_ruta(origen, destino):
        """
        Camino mas corto de `origen` a `destino`.

        Returns:
            list[str]: los pasos SIN el origen y CON el destino, en orden.
                       Ej.: casa_hmc -> casa_garage da
                       ['casa_pasilloarriba', 'casa_living', 'casa_garage'].
                       Lista vacia si no hay ruta, si falta alguna de las dos
                       locaciones, o si origen y destino son la misma.

        Es un BFS y no un Dijkstra porque todas las aristas valen igual: pasar
        de una habitacion a la de al lado cuesta lo mismo en todo el mapa.
        """
        if not origen or not destino or origen == destino:
            return []
        _locs = store.sistema_locaciones.locaciones
        if origen not in _locs or destino not in _locs:
            return []

        # previo[x] = de donde se llego a x. El origen se marca con None para
        # que tambien cuente como visitado y no se vuelva sobre el.
        _previo = {origen: None}
        _cola = [origen]

        while _cola:
            _actual = _cola.pop(0)
            if _actual == destino:
                _camino = []
                while _actual is not None:
                    _camino.append(_actual)
                    _actual = _previo[_actual]
                _camino.reverse()
                return _camino[1:]          # sin el origen

            for _v in vecinos_locacion(_actual):
                if _v not in _previo:
                    _previo[_v] = _actual
                    _cola.append(_v)

        return []

    def hay_ruta(origen, destino):
        """True si se puede llegar caminando. Atajo legible para condiciones."""
        return bool(calcular_ruta(origen, destino))
