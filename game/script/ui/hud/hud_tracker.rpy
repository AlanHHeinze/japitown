################################################################################
## App Tracker — ubicación de los NPCs
################################################################################
## App del celular que lista los NPCs disponibles con su icono (el mismo de
## chat/pistas/relaciones), su nombre y debajo "Locación Madre - Sublocación"
## donde se encuentran. Si el NPC no está en ninguna locación (o está oculto
## por una restricción de quest), muestra "Fuera de la casa".

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


screen panel_tracker():
    """App Tracker — lista de NPCs con su ubicación actual"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_tracker") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("panel_tracker")

    # Frame constrainido al area del celular
    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            # Barra de estado
            use _celular_barra_status("panel_tracker")

            # Header de app
            use _celular_app_header(_("Tracker"), "📍", [Hide("panel_tracker"), Show("menu_celular")], "panel_tracker")

            # Lista de NPCs
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (int(15 * _k), int(12 * _k))

                    vbox:
                        spacing int(10 * _k)
                        xfill True

                        for _tr_id in TRACKER_NPCS:
                            $ _tr_npc = obtener_npc(_tr_id)
                            if _tr_npc:
                                frame:
                                    xfill True
                                    background "#1e1e3aCC"
                                    padding (int(12 * _k), int(10 * _k))

                                    hbox:
                                        spacing int(14 * _k)

                                        # Icono del NPC (el mismo de chat/pistas/relaciones)
                                        $ _tr_icono = tracker_icono_npc(_tr_id)
                                        frame:
                                            xysize (int(64 * _k), int(64 * _k))
                                            background "#12122a"
                                            padding (0, 0)
                                            if _tr_icono:
                                                add _tr_icono fit "contain" xysize (int(64 * _k), int(64 * _k))
                                            else:
                                                text "👤" size int(34 * _k) xalign 0.5 yalign 0.5

                                        # Nombre + ubicación
                                        vbox:
                                            spacing int(4 * _k)
                                            yalign 0.5
                                            text _tr_npc.nombre size int(18 * _k) color "#ffffff" bold True
                                            text tracker_ubicacion_npc(_tr_id) size int(13 * _k) color "#8899BB"
