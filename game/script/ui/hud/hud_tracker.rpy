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

