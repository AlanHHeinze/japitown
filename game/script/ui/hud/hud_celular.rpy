################################################################################
## Sistema del Celular - Menú Central del Juego
################################################################################
## Script independiente para el sistema de celular.
## Agrupa funciones de informacion y gestión del personaje.

# Variable para controlar visibilidad del menú del celular
default menu_celular_abierto = False

init python:
    def _ejecutar_accion_celular_validada(accion_id):
        """Muestra mensaje de acción bloqueada."""
        _msg = accion_bloqueada(accion_id)
        if _msg:
            renpy.call("mostrar_bloqueo_accion", _msg)

screen menu_celular():
    """Menú del celular - Home Screen del smartphone"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("menu_celular") if modo_ajuste_celular else None

    # Fondo del celular (imagen completa — NO se constrañe al area)
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

    # Fondo clickeable para cerrar (bloqueado en modo ajuste)
    button:
        style "empty_button"
        xfill True
        yfill True
        if modo_ajuste_celular:
            action NullAction()
        else:
            action [SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]

    # Panel del celular — constrainido al area de trabajo
    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            # Barra de estado del smartphone
            use _celular_barra_status()

            # Contenido principal — home screen
            frame:
                xfill True
                yfill True
                background None
                padding (20, 15)

                vbox:
                    spacing 25
                    xfill True

                    # Espacio superior
                    null height 30

                    # Hora grande estilo smartphone
                    vbox:
                        xalign 0.5
                        spacing 2
                        $ _hora_map = {0: "09:00", 1: "14:00", 2: "20:00", 3: "02:00"}
                        $ _hora_display = _hora_map.get(horario_actual, "12:00")
                        text _hora_display size 52 color "#ffffff" bold True xalign 0.5
                        $ _dia_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
                        $ _dia_nombre = renpy.translate_string(_dia_nombres[dia_semana_actual])
                        text "[_dia_nombre], Día [dia_actual]" size 14 color "#aaaaaa" xalign 0.5

                    null height 20

                    # Definir botones del celular como lista para grid dinamico
                    python:
                        _botones_cel = [
                            ("relaciones", "💝", "Relaciones", Show("panel_relaciones"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                            ("pistas", "📋", "Pistas", Show("panel_pistas"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                            ("stats", "🎮", "Stats", Show("panel_stats_mc"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                            ("comprar", "🛒", "Tienda", Show("panel_tienda"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                            ("mensajes", "💬", "Chat", [Function(sistema_mensajes.verificar_mensajes_en_espera), Show("lista_contactos_mensajes")], "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                            ("galeria", "🖼️", "Galería", Show("panel_galeria"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                            ("hot", "🔥", "Hot", Call("narrar_mensaje", "Contenido en desarrollo"), "#2a1a10CC", "#3d2a1aCC", "#888888"),
                            ("banco", "🏦", "Banco", Call("narrar_mensaje", "Contenido en desarrollo"), "#2a1a10CC", "#3d2a1aCC", "#888888"),
                            ("configuracion", u"⚙️", "Configuración", Show("panel_configuracion"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
                        ]
                        if store.MODO_DEV:
                            _botones_cel.insert(4, ("cheats", "⚙️", "Cheats", Show("menu_cheats"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"))
                        _grid_cols = _ajc.grid_cols if _ajc and _ajc.grid_cols else 3
                        _grid_rows = _ajc.grid_rows if _ajc and _ajc.grid_rows else 5

                    # Grid dinamico de apps
                    for _fila_idx in range(_grid_rows):
                        hbox:
                            spacing 15
                            xalign 0.5
                            for _col_idx in range(_grid_cols):
                                $ _btn_idx = _fila_idx * _grid_cols + _col_idx
                                if _btn_idx < len(_botones_cel):
                                    $ _btn_id, _btn_emoji, _btn_label, _btn_action, _btn_bg, _btn_hover, _btn_text_color = _botones_cel[_btn_idx]
                                    $ _e_btn = sistema_ajuste_cel.elementos.get("menu_celular_btn_{}".format(_btn_id)) if _ajc else None
                                    button:
                                        action If(accion_bloqueada(_btn_id), Function(_ejecutar_accion_celular_validada, _btn_id), _btn_action)
                                        xoffset (_e_btn.xoffset if _e_btn else 0)
                                        yoffset (_e_btn.yoffset if _e_btn else 0)
                                        frame:
                                            xysize ((_e_btn.size_w if _e_btn else 150), (_e_btn.size_h if _e_btn else 150))
                                            background _btn_bg
                                            hover_background _btn_hover
                                            vbox:
                                                spacing 6
                                                xalign 0.5
                                                yalign 0.5
                                                if _btn_id == "mensajes":
                                                    fixed:
                                                        xysize (50, 45)
                                                        xalign 0.5
                                                        text _btn_emoji size 38 xalign 0.5
                                                        $ _total_sin_leer = sistema_mensajes.obtener_pendientes_total()
                                                        if _total_sin_leer > 0:
                                                            frame:
                                                                xalign 1.0
                                                                yalign 0.0
                                                                background "#FF4444"
                                                                padding (4, 2)
                                                                xminimum 18
                                                                text "[_total_sin_leer]" size 10 color "#ffffff" bold True xalign 0.5
                                                else:
                                                    text _btn_emoji size 38 xalign 0.5
                                                text _btn_label size 11 color _btn_text_color xalign 0.5

                    # Espaciador para empujar dock abajo
                    null

            # Dock inferior — cerrar
            frame:
                xfill True
                ysize 50
                background "#0a0a18FF"
                padding (0, 0)

                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 40

                    textbutton "○":
                        action [SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
                        text_size 24
                        text_color "#666666"
                        text_hover_color "#ffffff"
                        yalign 0.5


################################################################################
## Label para mostrar mensaje de accion bloqueada
################################################################################

label mostrar_bloqueo_accion(mensaje=""):
    $ ocultar_hud()
    window show
    piensa "[mensaje]"
    window hide
    $ mostrar_hud()
    return


################################################################################
## Validar estado despues de cerrar el celular
################################################################################
## Se ejecuta al cerrar el celular para verificar si hay eventos pendientes
## (similar a lo que ocurre al cambiar de locación o adelantar tiempo)

label _validar_estado_tras_celular:

    # Quest 0b del MC: completar si el jugador ya visitó la app de pistas
    if getattr(store, "mc_q0b_esperando", False) and getattr(store, "mc_q0b_pistas_visitada", False):
        jump mc_q0b_completar

    # (Aqui pueden agregarse futuras validaciones tras cerrar el celular)

    return
