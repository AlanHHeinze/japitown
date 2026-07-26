################################################################################
## Viaje Rápido — menú de sublocaciones desde el HUD
################################################################################
## El botón cama del HUD superior despliega este menú: detecta la locación
## madre actual (por prefijo de id) y lista sus sublocaciones; al tocar una
## se viaja usando el MISMO flujo que un hotspot MOVE (accion_hotspot_move),
## así se respetan door access, baños ocupados, restricciones de quest y los
## hooks (quest 0 del MC, labels de restricción, mensajes en espera).
##
## Extensible: cuando haya más zonas (ciudad, tienda, etc.) basta con agregar
## la locación madre a LOCACIONES_MADRE con su prefijo de ids.

define LOCACIONES_MADRE = {
    "casa": {
        "nombre": "Casa",
        "prefijo": "casa_",
        # Locacion destacada: va primera en el menu y lleva estrella.
        "destacada": "casa_hmc",
    },
}

# Destinos con puerta/baño: antes de disparar la interacción, el viaje rápido
# mueve al jugador al pasillo conectado — la puerta se "toca" desde ahí.
define VIAJE_RAPIDO_PREVIA = {
    "casa_hmonica":     "casa_pasilloabajo",
    "casa_hviolet":     "casa_pasilloarriba",
    "casa_hjasmine":    "casa_pasilloarriba",
    "casa_banioarriba": "casa_pasilloarriba",
}

# Locaciones que no aparecen en el menú (solo accesibles desde adentro de otra)
define VIAJE_RAPIDO_OCULTAS = ("casa_baniomonica",)

init python:

    def locacion_madre_actual():
        """Devuelve el id de la locación madre de la locación actual, o None."""
        loc = sistema_locaciones.locacion_actual
        if not loc:
            return None
        for _mid, _cfg in LOCACIONES_MADRE.items():
            if loc.id.startswith(_cfg["prefijo"]):
                return _mid
        return None

    def sublocaciones_de_madre(madre_id):
        """
        Sublocaciones registradas de una locación madre, en orden de registro
        salvo la destacada, que va primera. El sort es estable, asi que el resto
        conserva su orden original.
        """
        cfg = LOCACIONES_MADRE.get(madre_id)
        if not cfg:
            return []
        pref = cfg["prefijo"]
        locs = [l for l in sistema_locaciones.locaciones.values()
                if l.id.startswith(pref) and l.id not in VIAJE_RAPIDO_OCULTAS]
        destacada = cfg.get("destacada")
        if destacada:
            locs.sort(key=lambda l: 0 if l.id == destacada else 1)
        return locs

    def locacion_destacada(madre_id):
        """Id de la locación destacada de una madre (la que lleva estrella), o None."""
        cfg = LOCACIONES_MADRE.get(madre_id)
        return cfg.get("destacada") if cfg else None


# Viaja reusando el flujo completo de un hotspot MOVE. El hotspot sintético
# solo necesita destino: door access, baños ocupados, restricciones y el
# handler de la quest 0 leen únicamente _hotspot_temp.destino.
label accion_viaje_rapido:
    if _locacion_temp:

        # Destinos con puerta/baño: acercarse primero al pasillo conectado, así
        # la interacción ocurre ahí.
        if _locacion_temp in VIAJE_RAPIDO_PREVIA:

            # Si el destino está bloqueado por restricción, avisar sin moverse
            $ _msg_restriccion_vr = accion_bloqueada_movimiento(_locacion_temp)
            if _msg_restriccion_vr:
                $ _blk_guardar_toque()
                piensa "[_msg_restriccion_vr]"
                return

            $ _vr_previa = VIAJE_RAPIDO_PREVIA[_locacion_temp]
            $ _vr_actual_id = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
            if _vr_actual_id != _vr_previa:
                # El paso previo también respeta la restricción de movimiento
                $ _msg_restriccion_vr = accion_bloqueada_movimiento(_vr_previa)
                if _msg_restriccion_vr:
                    $ _blk_guardar_toque()
                    piensa "[_msg_restriccion_vr]"
                    return
                $ sistema_locaciones.mover_a_locacion(_vr_previa)
                # Refrescar el fondo ya: la interacción de puerta/baño ocurre
                # antes de volver al game_loop (que es quien normalmente lo hace)
                $ actualizar_bg_master()

        $ _hotspot_temp = Hotspot("viaje_rapido_" + _locacion_temp, "MOVE", 0, 0, 1, 1, destino=_locacion_temp, nombre="")
        jump accion_hotspot_move
    return


screen menu_viaje_rapido():
    zorder 210
    modal True

    # Cerrar al tocar afuera (sin oscurecer la pantalla)
    button:
        xfill True
        yfill True
        background None
        action Hide("menu_viaje_rapido")

    $ _vr_madre_id = locacion_madre_actual()
    $ _vr_cfg = LOCACIONES_MADRE.get(_vr_madre_id) if _vr_madre_id else None
    $ _vr_actual = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
    $ _vr_destacada = locacion_destacada(_vr_madre_id) if _vr_madre_id else None
    $ _vr_small = renpy.variant("small")
    $ _vr_k = 2.0 if _vr_small else 1.0

    if _vr_small:
        # Pantalla táctil: centrado, texto y contenedor al doble, con scroll
        # táctil (draggable) porque la lista de filas puede superar el alto
        # de pantalla disponible.
        frame:
            xalign 0.5
            yalign 0.5
            xsize int(400 * _vr_k)
            background "#101024F0"
            padding (int(12 * _vr_k), int(12 * _vr_k))

            vbox:
                spacing int(4 * _vr_k)

                if _vr_cfg:
                    text renpy.translate_string(_vr_cfg["nombre"]) size int(24 * _vr_k) color "#4FC3F7" bold True xalign 0.5
                    null height int(4 * _vr_k)

                    viewport:
                        xfill True
                        ysize 820
                        draggable True
                        mousewheel True
                        scrollbars "vertical"

                        vbox:
                            spacing int(4 * _vr_k)

                            for _vr_loc in sublocaciones_de_madre(_vr_madre_id):
                                if _vr_loc.id == _vr_actual:
                                    # Locación actual: marcada, no clickeable
                                    frame:
                                        xsize int(376 * _vr_k)
                                        ysize int(42 * _vr_k)
                                        background "#1b1b33"
                                        padding (int(12 * _vr_k), 0)
                                        use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#8888AA", True, _vr_k)
                                else:
                                    button:
                                        xsize int(376 * _vr_k)
                                        ysize int(42 * _vr_k)
                                        background "#1e1e3a"
                                        hover_background "#2a3f5f"
                                        padding (int(12 * _vr_k), 0)
                                        action [Hide("menu_viaje_rapido"), SetVariable("_locacion_temp", _vr_loc.id), Call("accion_viaje_rapido")]
                                        use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#FFFFFF", False, _vr_k)
                else:
                    text renpy.translate_string("No hay destinos disponibles") size int(21 * _vr_k) color "#dddddd"

    else:
        frame:
            xanchor 1.0
            xpos 1920 - 290     # borde derecho alineado bajo el botón cama (xoffset -344)
            ypos 112
            xsize 400
            background "#101024F0"
            padding (12, 12)

            vbox:
                spacing 4

                if _vr_cfg:
                    text renpy.translate_string(_vr_cfg["nombre"]) size 24 color "#4FC3F7" bold True xalign 0.5
                    null height 4

                    for _vr_loc in sublocaciones_de_madre(_vr_madre_id):
                        if _vr_loc.id == _vr_actual:
                            # Locación actual: marcada, no clickeable
                            frame:
                                xsize 376
                                ysize 42
                                background "#1b1b33"
                                padding (12, 0)
                                use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#8888AA", True)
                        else:
                            button:
                                xsize 376
                                ysize 42
                                background "#1e1e3a"
                                hover_background "#2a3f5f"
                                padding (12, 0)
                                action [Hide("menu_viaje_rapido"), SetVariable("_locacion_temp", _vr_loc.id), Call("accion_viaje_rapido")]
                                use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#FFFFFF", False)
                else:
                    text renpy.translate_string("No hay destinos disponibles") size 21 color "#dddddd"


# Contenido de una fila del menu. La fila mide 376x42 con padding (12, 0), asi que
# el area util es 352x42: la estrella y los iconos de NPC entran holgados y, al ser
# el alto fijo, no pueden agrandar la fila. En pantalla táctil, k=2.0 escala todo
# el contenido de la fila para ocupar las nuevas dimensiones (752x84).
screen _vr_fila(loc, destacada, color_texto, aqui, k=1.0):
    fixed:
        xfill True
        yfill True

        # Estrella + nombre, pegados a la izquierda
        hbox:
            xalign 0.0
            yalign 0.5
            spacing int(6 * k)

            if destacada:
                text "⭐" size int(19 * k) yalign 0.5

            $ _vr_nombre = renpy.translate_string(loc.nombre)
            text "[_vr_nombre]" size int(21 * k) color color_texto yalign 0.5

        # Iconos de quien esta en la locacion, pegados a la derecha: primero el
        # marcador del jugador (solo donde esta el) y despues los NPCs.
        # Reusa tracker_npcs_en_locacion (hud_tracker), asi respeta las mismas
        # reglas que la app: los NPCs ocultos por quest tampoco aparecen aca.
        hbox:
            xalign 1.0
            yalign 0.5
            spacing int(4 * k)

            if aqui:
                text "📍" size int(20 * k) yalign 0.5

            for _vr_npc in tracker_npcs_en_locacion(loc.id):
                $ _vr_icono = tracker_icono_npc(_vr_npc)
                if _vr_icono:
                    add _vr_icono fit "contain" xysize (int(26 * k), int(26 * k)) yalign 0.5
