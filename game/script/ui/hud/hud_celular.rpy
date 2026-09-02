################################################################################
## Sistema del Celular - Menú Central del Juego
################################################################################
## Script independiente para el sistema de celular.
## Agrupa funciones de informacion y gestión del personaje.

# Variable para controlar visibilidad del menú del celular
default menu_celular_abierto = False

init python:
    def _ejecutar_accion_celular_validada(accion_id):
        """Muestra el mensaje de por que esa app esta cerrada."""
        _msg = app_celular_bloqueada(accion_id)
        if _msg:
            renpy.call("mostrar_bloqueo_accion", _msg)

screen menu_celular():
    """Menú del celular - Home Screen del smartphone"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("menu_celular") if modo_ajuste_celular else None
    $ _cel_small = renpy.variant("small")

    # Definir botones del celular como lista para grid dinamico (comun a ambas variantes)
    python:
        _botones_cel = [
            ("relaciones", "💝", "Relaciones", Show("panel_relaciones"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
            ("pistas", "📋", "Pistas", Show("panel_pistas"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
            ("stats", "🎮", "Stats", Show("panel_stats_mc"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
            ("comprar", "🛒", "Tienda", Show("panel_tienda"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
            ("mensajes", "💬", "Chat", [Function(sistema_mensajes.verificar_mensajes_en_espera), Show("lista_contactos_mensajes")], "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
            ("galeria", "🖼️", "Galería", Show("panel_galeria"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
            # Sin app Tracker: la ubicacion de cada NPC ya la muestra su fila en
            # Relaciones, asi que era una segunda pantalla para el mismo dato.
            ("hot", "🔥", "Hot", Call("narrar_mensaje", "Contenido en desarrollo"), "#2a1a10CC", "#3d2a1aCC", "#888888"),
            ("banco", "🏦", "Banco", Call("narrar_mensaje", "Contenido en desarrollo"), "#2a1a10CC", "#3d2a1aCC", "#888888"),
            ("configuracion", u"⚙️", "Configuración", Show("panel_configuracion"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"),
        ]
        if store.MODO_DEV:
            _botones_cel.insert(4, ("cheats", "⚙️", "Cheats", Show("menu_cheats"), "#1e1e3aCC", "#2a2a50CC", "#ffffff"))

    # Fondo del celular
    use _celular_fondo()

    # Bloqueador exterior + botón de cerrar (compartido con las apps)
    use _celular_cerrar_exterior("menu_celular")

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
            use _celular_barra_status("menu_celular")

            if _cel_small:
                # Home horizontal: grid centrado, ocupando todo el espacio libre.
                # 2 filas es el ideal, pero si con MODO_DEV entra "cheats" y no
                # entran todas en el ancho disponible, se agregan filas en vez
                # de agrandar las columnas más allá de lo que entra en pantalla
                # (eso es lo que se salía por la derecha).
                $ _cel_btn_size = 300
                $ _cel_grid_spacing = 30
                $ _cel_disp_w = ajuste_cel_area_w - 80  # padding (40, 20) horizontal
                $ _cel_max_cols = max(1, (_cel_disp_w + _cel_grid_spacing) // (_cel_btn_size + _cel_grid_spacing))
                $ _cel_grid_cols = min((len(_botones_cel) + 1) // 2, _cel_max_cols)
                $ _cel_grid_filas = (len(_botones_cel) + _cel_grid_cols - 1) // _cel_grid_cols

                frame:
                    xfill True
                    yfill True
                    background None
                    padding (40, 20)

                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing _cel_grid_spacing

                        for _fila_idx in range(_cel_grid_filas):
                            hbox:
                                spacing _cel_grid_spacing
                                xalign 0.5
                                for _col_idx in range(_cel_grid_cols):
                                    $ _btn_idx = _fila_idx * _cel_grid_cols + _col_idx
                                    if _btn_idx < len(_botones_cel):
                                        $ _btn_id, _btn_emoji, _btn_label, _btn_action, _btn_bg, _btn_hover, _btn_text_color = _botones_cel[_btn_idx]
                                        button:
                                            action If(app_celular_bloqueada(_btn_id), Function(_ejecutar_accion_celular_validada, _btn_id), _btn_action)
                                            frame:
                                                xysize (_cel_btn_size, _cel_btn_size)
                                                background _btn_bg
                                                hover_background _btn_hover
                                                vbox:
                                                    spacing 12
                                                    xalign 0.5
                                                    yalign 0.5
                                                    if _btn_id == "mensajes":
                                                        fixed:
                                                            xysize (100, 90)
                                                            xalign 0.5
                                                            text _btn_emoji size 76 xalign 0.5
                                                            $ _total_sin_leer = sistema_mensajes.obtener_pendientes_total()
                                                            if _total_sin_leer > 0:
                                                                frame:
                                                                    xalign 1.0
                                                                    yalign 0.0
                                                                    background "#FF4444"
                                                                    padding (8, 4)
                                                                    xminimum 36
                                                                    text "[_total_sin_leer]" size 20 color "#ffffff" bold True xalign 0.5
                                                    else:
                                                        text _btn_emoji size 76 xalign 0.5
                                                    text _btn_label size 44 color _btn_text_color xalign 0.5
            else:
                # Contenido principal — home screen (vertical, tamaño de celular clásico)
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

                        python:
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
                                            action If(app_celular_bloqueada(_btn_id), Function(_ejecutar_accion_celular_validada, _btn_id), _btn_action)
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

                        textbutton "×":
                            action [SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
                            text_size 24
                            text_color "#666666"
                            text_hover_color "#ffffff"
                            yalign 0.5

    if _cel_small:
        # El home no tiene _celular_app_header (no hay "volver" ni título), así
        # que pone su propio botón de cerrar arriba a la derecha. Va al final
        # del screen (no antes del grid) para quedar dibujado por encima.
        $ _cel_k = CEL_APP_ESCALA_SMALL
        button:
            xpos (ajuste_cel_area_x + ajuste_cel_area_w - int(10 * _cel_k) - int(44 * _cel_k))
            ypos (ajuste_cel_area_y + int(10 * _cel_k))
            xysize (int(44 * _cel_k), int(44 * _cel_k))
            background "#E53935EE"
            hover_background "#FF5449"
            if modo_ajuste_celular:
                action NullAction()
            else:
                action [SetVariable("menu_celular_abierto", False), Hide("menu_celular"), Call("_validar_estado_tras_celular")]
            text "X" size int(24 * _cel_k) color "#ffffff" bold True xalign 0.5 yalign 0.5


################################################################################
## Label para mostrar mensaje de accion bloqueada
################################################################################

label mostrar_bloqueo_accion(mensaje=""):
    $ ocultar_hud()
    window show
    $ _blk_guardar_toque()
    piensa "[mensaje]"
    window hide
    $ mostrar_hud()
    return


################################################################################
## Validar estado despues de cerrar el celular
################################################################################
## Cuarto punto de enganche del motor, junto a game_loop / dormir / avanzar: el
## contenido que le pide algo al jugador adentro del celular sigue la escena
## cuando sale. Se registra con registrar_trigger_salir_celular desde el archivo
## del contenido (ver triggers_contenido.rpy); acá no hay ninguna quest por
## nombre.

label _validar_estado_tras_celular:

    $ _cel_trigger_label = ejecutar_triggers_salir_celular()
    if _cel_trigger_label:
        jump expression _cel_trigger_label

    return
