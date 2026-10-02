################################################################################
## Tracker — dónde está cada NPC
################################################################################
## ACÁ YA NO HAY APP. La pantalla `panel_tracker` del celular se eliminó: la
## ubicación de cada NPC ya la muestra su fila en la app de Relaciones, así que
## eran dos pantallas para el mismo dato.
##
## Lo que queda son los HELPERS de ubicación, que siguen muy vivos:
##   - tracker_ubicacion_npc()    → la fila de Relaciones (hud_relaciones.rpy)
##   - tracker_npcs_en_locacion() → iconos del menú de viaje rápido
##   - tracker_icono_npc()        → idem
##   - tracker_locacion_npc()     → base de los tres, y ÚNICA fuente de verdad
##     de la visibilidad: un NPC oculto por restricción de quest no se filtra
##     por ningún lado.
##
## El archivo sigue en ui/hud/ por historia; siendo ya solo lógica de locación,
## su lugar natural sería core/locations/.

define TRACKER_NPCS = ("violet", "monica", "jasmine")

init python:

    def tracker_locacion_npc(npc_id):
        """
        Id de la locación donde está el NPC, o None si no es "ubicable".
        Unica fuente de verdad de la visibilidad: la usan el panel del tracker y
        los iconos del menu de viaje rapido, asi que un NPC oculto por una
        restriccion de quest no se filtra por ningun lado.
        """
        # NPC fuera de juego: para todo el que pregunte, no esta en ningun
        # lado (core/npcs/npc_disponibilidad.rpy). Con esto se caen solas las
        # puertas, el viaje rapido, las acciones compartidas y las condiciones
        # de contenido que preguntan por su locacion.
        if not npc_disponible(npc_id):
            return None

        npc = obtener_npc(npc_id)
        if not npc or not npc.locacion_actual or npc.locacion_actual == "fuera":
            return None

        # NPCs ocultos por una restricción de quest no se muestran ubicados
        if hay_restriccion_activa():
            _ocultos = getattr(restriccion_quest_activa, 'npcs_ocultos', None)
            if _ocultos and npc_id in _ocultos:
                return None

        loc = sistema_locaciones.obtener_locacion(npc.locacion_actual)
        if not loc:
            return None
        return loc.id

    def npc_a_solas(npc_id):
        """
        True si el MC y ese NPC estan SIN NADIE MAS en la locacion actual.

        Es la condicion de "no delante de otras personas": la usan las dos
        ventajas de beso de Violet y, desde la quest de amor 45, es la regla que
        ella misma enuncia. Estaba escrita dos veces, identica, en
        beso_violet.rpy y beso_deseo_violet.rpy; vive acá para que cuando la
        regla cambie, cambie en un solo lugar.

        Pregunta por tracker_locacion_npc y no por obtener_npcs_en_locacion:
        esa ultima devuelve tambien a los que una restriccion de quest escondio,
        y al jugador no le estan delante. Por eso vive en este archivo, pegada a
        la fuente de verdad de "se puede ubicar al NPC".
        """
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None:
            return False
        for _nid in store.sistema_npcs.npcs:
            if _nid == npc_id:
                continue
            if tracker_locacion_npc(_nid) == _loc.id:
                return False
        return True

    def tracker_npcs_en_locacion(loc_id):
        """NPCs visibles que están en esa locación, en el orden de TRACKER_NPCS."""
        return [n for n in TRACKER_NPCS if tracker_locacion_npc(n) == loc_id]

    def tracker_icono_npc(npc_id):
        """Ruta del icono del NPC (el mismo de chat/pistas/relaciones), o None."""
        ruta = "images/hud/pista_{}.png".format(npc_id)
        return ruta if renpy.loadable(ruta) else None

    def tracker_ubicacion_npc(npc_id):
        """Texto legible de la ubicación de un NPC: 'Casa - Habitación de Violet'."""
        _fuera = renpy.translate_string("Fuera de la casa")

        loc_id = tracker_locacion_npc(npc_id)
        if not loc_id:
            return _fuera

        loc = sistema_locaciones.obtener_locacion(loc_id)
        if not loc:
            return _fuera

        sub = renpy.translate_string(loc.nombre)
        for _mid, _cfg in LOCACIONES_MADRE.items():
            if loc.id.startswith(_cfg["prefijo"]):
                return renpy.translate_string(_cfg["nombre"]) + u" - " + sub
        return sub

