################################################################################
## Herramienta de Ajuste Celular - Panel de UI
################################################################################

screen panel_ajuste_celular():
    zorder 300
    modal True

    $ _c = sistema_ajuste_cel.obtener_container(ajuste_cel_screen_actual)
    $ _elems = sistema_ajuste_cel.obtener_elementos_de(ajuste_cel_screen_actual)
    $ _tiene_cambios = sistema_ajuste_cel.hay_cambios() or _area_fue_modificada()
    $ _tiene_undo = len(ajuste_cel_undo) > 0

    # Fondo que bloquea interacciones (invisible, cubre toda la pantalla)
    button:
        style "empty_button"
        xfill True
        yfill True
        action NullAction()

    frame:
        xalign 1.0
        yalign 0.0
        yoffset 10
        xoffset -10
        background "#1a1a2eF5"
        padding (18, 15)
        xsize 380

        vbox:
            spacing 10
            xalign 0.5

            # Header
            text "AJUSTE CELULAR" size 18 color "#FFD700" bold True xalign 0.5

            # Separador
            frame:
                xsize 340
                ysize 2
                background "#FFD70044"

            # Selector de pantalla
            text "Pantalla:" size 14 color "#888888"
            frame:
                xfill True
                background "#0d0d1fCC"
                padding (8, 5)

                vbox:
                    spacing 4
                    for _sn, _snombre in sistema_ajuste_cel.lista_screens():
                        $ _sel_color = "#FFD700" if _sn == ajuste_cel_screen_actual else "#aaaaaa"
                        $ _sel_bg = "#2a2a4a" if _sn == ajuste_cel_screen_actual else None
                        textbutton _snombre:
                            action Function(ajuste_cel_cambiar_screen, _sn)
                            text_size 13
                            text_color _sel_color
                            background _sel_bg
                            hover_background "#3a3a5a"
                            padding (8, 4)
                            xfill True

            # Separador
            frame:
                xsize 340
                ysize 1
                background "#ffffff22"

            # Pestanas
            hbox:
                spacing 10
                xalign 0.5

                $ _tab_c_bg = "#1565C0" if ajuste_cel_tab == "container" else "#2a2a4aCC"
                textbutton "Container":
                    action SetVariable("ajuste_cel_tab", "container")
                    text_size 15
                    text_color "#ffffff"
                    background _tab_c_bg
                    hover_background "#1976D2"
                    padding (15, 7)

                $ _tab_e_bg = "#1565C0" if ajuste_cel_tab == "elementos" else "#2a2a4aCC"
                textbutton "Elementos":
                    action SetVariable("ajuste_cel_tab", "elementos")
                    text_size 15
                    text_color "#ffffff"
                    background _tab_e_bg
                    hover_background "#1976D2"
                    padding (15, 7)

                $ _tab_a_bg = "#1565C0" if ajuste_cel_tab == "area" else "#2a2a4aCC"
                textbutton "Área":
                    action SetVariable("ajuste_cel_tab", "area")
                    text_size 15
                    text_color "#ffffff"
                    background _tab_a_bg
                    hover_background "#1976D2"
                    padding (15, 7)

            # Contenido segun pestana
            if ajuste_cel_tab == "container" and _c:
                use _panel_ajuste_container(_c)
            elif ajuste_cel_tab == "elementos":
                use _panel_ajuste_elementos(_elems)
            elif ajuste_cel_tab == "area":
                use _panel_ajuste_area()

            # Separador
            frame:
                xsize 340
                ysize 1
                background "#ffffff22"

            # Barra de acciones
            hbox:
                spacing 8
                xalign 0.5

                textbutton "Exportar":
                    action Function(exportar_ajuste_celular)
                    text_size 14
                    text_color "#ffffff"
                    background ("#4CAF50" if _tiene_cambios else "#333333")
                    hover_background "#66BB6A"
                    padding (14, 7)
                    sensitive _tiene_cambios

                textbutton "Deshacer":
                    action Function(deshacer_ajuste_cel)
                    text_size 14
                    text_color "#ffffff"
                    background ("#FF9800" if _tiene_undo else "#333333")
                    hover_background "#FFB74D"
                    padding (14, 7)
                    sensitive _tiene_undo

                textbutton "Limpiar":
                    action Function(limpiar_ajuste_cel)
                    text_size 14
                    text_color "#ffffff"
                    background ("#E91E63" if _tiene_cambios else "#333333")
                    hover_background "#F48FB1"
                    padding (14, 7)
                    sensitive _tiene_cambios

                textbutton "Cerrar":
                    action Function(desactivar_ajuste_celular)
                    text_size 14
                    text_color "#ffffff"
                    background "#607D8B"
                    hover_background "#90A4AE"
                    padding (14, 7)

    # Overlay de input de texto
    if ajuste_cel_input_activo:
        use _panel_ajuste_input_overlay()

    # Overlay visual del area de trabajo
    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        # Borde superior
        frame:
            xfill True
            ysize 2
            yalign 0.0
            background "#00FF0088"
        # Borde inferior
        frame:
            xfill True
            ysize 2
            yalign 1.0
            background "#00FF0088"
        # Borde izquierdo
        frame:
            xsize 2
            yfill True
            xalign 0.0
            background "#00FF0088"
        # Borde derecho
        frame:
            xsize 2
            yfill True
            xalign 1.0
            background "#00FF0088"
        # Etiqueta
        text "AREA DE TRABAJO" size 11 color "#00FF0088" xalign 0.5 yalign 0.0 yoffset 5


################################################################################
## Overlay de Input de Texto
################################################################################

screen _panel_ajuste_input_overlay():
    zorder 350
    modal True

    # Fondo oscuro
    button:
        style "empty_button"
        xfill True
        yfill True
        action Function(ajuste_cel_cancelar_input)
        background "#00000088"

    $ _input_attr, _input_es_elem = ajuste_cel_input_activo
    frame:
        xalign 0.5
        yalign 0.4
        background "#1a1a2eF8"
        padding (25, 20)
        xsize 320

        vbox:
            spacing 12
            xalign 0.5

            text "Ingresar valor" size 18 color "#FFD700" bold True xalign 0.5
            text "[_input_attr]" size 14 color "#4FC3F7" xalign 0.5

            frame:
                xfill True
                background "#0d0d1f"
                padding (12, 8)

                input:
                    value VariableInputValue("ajuste_cel_input_valor", returnable=True)
                    size 18
                    color "#ffffff"
                    allow "0123456789.-"
                    length 8

            hbox:
                spacing 12
                xalign 0.5

                textbutton "Aplicar":
                    action Function(ajuste_cel_aplicar_input)
                    text_size 15
                    text_color "#ffffff"
                    background "#4CAF50"
                    hover_background "#66BB6A"
                    padding (18, 8)

                textbutton "Cancelar":
                    action Function(ajuste_cel_cancelar_input)
                    text_size 15
                    text_color "#ffffff"
                    background "#607D8B"
                    hover_background "#90A4AE"
                    padding (18, 8)


################################################################################
## Pestana Container
################################################################################

screen _panel_ajuste_container(c):
    vbox:
        spacing 6

        # Posicion
        text "Posicion" size 14 color "#4FC3F7" bold True

        # xalign
        hbox:
            spacing 5
            yalign 0.5
            text "xalign:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.xalign:.2f]":
                action Function(ajuste_cel_abrir_input, "xalign")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-":
                action Function(ajuste_cel_modificar, "xalign", -0.05)
                text_size 14 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (8, 4)
            textbutton "+":
                action Function(ajuste_cel_modificar, "xalign", 0.05)
                text_size 14 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (8, 4)

        # yalign
        hbox:
            spacing 5
            yalign 0.5
            text "yalign:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.yalign:.2f]":
                action Function(ajuste_cel_abrir_input, "yalign")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-":
                action Function(ajuste_cel_modificar, "yalign", -0.05)
                text_size 14 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (8, 4)
            textbutton "+":
                action Function(ajuste_cel_modificar, "yalign", 0.05)
                text_size 14 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (8, 4)

        # xoffset
        hbox:
            spacing 5
            yalign 0.5
            text "xoffset:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.xoffset]":
                action Function(ajuste_cel_abrir_input, "xoffset")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-5":
                action Function(ajuste_cel_modificar, "xoffset", -5)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+5":
                action Function(ajuste_cel_modificar, "xoffset", 5)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "-20":
                action Function(ajuste_cel_modificar, "xoffset", -20)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+20":
                action Function(ajuste_cel_modificar, "xoffset", 20)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # yoffset
        hbox:
            spacing 5
            yalign 0.5
            text "yoffset:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.yoffset]":
                action Function(ajuste_cel_abrir_input, "yoffset")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-5":
                action Function(ajuste_cel_modificar, "yoffset", -5)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+5":
                action Function(ajuste_cel_modificar, "yoffset", 5)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "-20":
                action Function(ajuste_cel_modificar, "yoffset", -20)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+20":
                action Function(ajuste_cel_modificar, "yoffset", 20)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        null height 4
        text "Tamanio" size 14 color "#4FC3F7" bold True

        # width
        hbox:
            spacing 5
            yalign 0.5
            text "ancho:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            $ _w_display = str(c.width) if c.width else "-"
            textbutton "[_w_display]":
                action Function(ajuste_cel_abrir_input, "width")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-10":
                action Function(ajuste_cel_modificar, "width", -10)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+10":
                action Function(ajuste_cel_modificar, "width", 10)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # height
        hbox:
            spacing 5
            yalign 0.5
            text "alto:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            $ _h_display = str(c.height) if c.height else "-"
            textbutton "[_h_display]":
                action Function(ajuste_cel_abrir_input, "height")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-10":
                action Function(ajuste_cel_modificar, "height", -10)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+10":
                action Function(ajuste_cel_modificar, "height", 10)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        null height 4
        text "Layout" size 14 color "#4FC3F7" bold True

        # padding_x
        hbox:
            spacing 5
            yalign 0.5
            text "pad_x:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.padding_x]":
                action Function(ajuste_cel_abrir_input, "padding_x")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-5":
                action Function(ajuste_cel_modificar, "padding_x", -5)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+5":
                action Function(ajuste_cel_modificar, "padding_x", 5)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # padding_y
        hbox:
            spacing 5
            yalign 0.5
            text "pad_y:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.padding_y]":
                action Function(ajuste_cel_abrir_input, "padding_y")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-5":
                action Function(ajuste_cel_modificar, "padding_y", -5)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+5":
                action Function(ajuste_cel_modificar, "padding_y", 5)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # spacing
        hbox:
            spacing 5
            yalign 0.5
            text "spacing:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[c.spacing]":
                action Function(ajuste_cel_abrir_input, "spacing")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 50
            textbutton "-5":
                action Function(ajuste_cel_modificar, "spacing", -5)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+5":
                action Function(ajuste_cel_modificar, "spacing", 5)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        null height 4
        text "Grilla" size 14 color "#4FC3F7" bold True

        # grid_cols
        if c.grid_cols is not None:
            hbox:
                spacing 5
                yalign 0.5
                text "columnas:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
                textbutton "[c.grid_cols]":
                    action Function(ajuste_cel_abrir_input, "grid_cols")
                    text_size 14 text_color "#ffffff" text_bold True
                    background "#0d0d1f" hover_background "#1a1a3f"
                    padding (6, 3) xsize 50
                textbutton "-1":
                    action Function(ajuste_cel_modificar, "grid_cols", -1)
                    text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                    sensitive (c.grid_cols > 1)
                textbutton "+1":
                    action Function(ajuste_cel_modificar, "grid_cols", 1)
                    text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # grid_rows
        if c.grid_rows is not None:
            hbox:
                spacing 5
                yalign 0.5
                text "filas:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
                textbutton "[c.grid_rows]":
                    action Function(ajuste_cel_abrir_input, "grid_rows")
                    text_size 14 text_color "#ffffff" text_bold True
                    background "#0d0d1f" hover_background "#1a1a3f"
                    padding (6, 3) xsize 50
                textbutton "-1":
                    action Function(ajuste_cel_modificar, "grid_rows", -1)
                    text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                    sensitive (c.grid_rows > 1)
                textbutton "+1":
                    action Function(ajuste_cel_modificar, "grid_rows", 1)
                    text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # Indicador de cambios
        if c.fue_modificado():
            text "* Modificado" size 12 color "#FFD700" xalign 1.0


################################################################################
## Pestana Elementos
################################################################################

screen _panel_ajuste_elementos(elems):
    vbox:
        spacing 6

        if not elems:
            text "Sin elementos registrados" size 14 color "#666666" xalign 0.5
        else:
            # Lista de elementos
            text "Elementos:" size 14 color "#888888"

            frame:
                xfill True
                background "#0d0d1fCC"
                padding (5, 5)
                ymaximum 170

                viewport:
                    scrollbars "vertical"
                    mousewheel True

                    vbox:
                        spacing 3
                        for _elem in elems:
                            $ _e_sel = (ajuste_cel_elemento_id == _elem.id)
                            $ _e_color = "#FFD700" if _e_sel else "#aaaaaa"
                            $ _e_bg = "#2a2a4a" if _e_sel else None
                            $ _e_mod = " *" if _elem.fue_modificado() else ""
                            textbutton "[_elem.nombre][_e_mod]":
                                action SetVariable("ajuste_cel_elemento_id", _elem.id)
                                text_size 13
                                text_color _e_color
                                background _e_bg
                                hover_background "#3a3a5a"
                                padding (8, 4)
                                xfill True

            # Controles del elemento seleccionado
            if ajuste_cel_elemento_id:
                $ _sel_elem = sistema_ajuste_cel.elementos.get(ajuste_cel_elemento_id)
                if _sel_elem:
                    null height 4
                    text "[_sel_elem.nombre]" size 14 color "#FFD700" bold True

                    # xoffset
                    hbox:
                        spacing 5
                        yalign 0.5
                        text "xoffset:" size 13 color "#aaaaaa" yalign 0.5 xsize 70
                        textbutton "[_sel_elem.xoffset]":
                            action Function(ajuste_cel_abrir_input, "xoffset", True)
                            text_size 14 text_color "#ffffff" text_bold True
                            background "#0d0d1f" hover_background "#1a1a3f"
                            padding (6, 3) xsize 45
                        textbutton "-1":
                            action Function(ajuste_cel_modificar, "xoffset", -1, True)
                            text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "+1":
                            action Function(ajuste_cel_modificar, "xoffset", 1, True)
                            text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "-5":
                            action Function(ajuste_cel_modificar, "xoffset", -5, True)
                            text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "+5":
                            action Function(ajuste_cel_modificar, "xoffset", 5, True)
                            text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

                    # yoffset
                    hbox:
                        spacing 5
                        yalign 0.5
                        text "yoffset:" size 13 color "#aaaaaa" yalign 0.5 xsize 70
                        textbutton "[_sel_elem.yoffset]":
                            action Function(ajuste_cel_abrir_input, "yoffset", True)
                            text_size 14 text_color "#ffffff" text_bold True
                            background "#0d0d1f" hover_background "#1a1a3f"
                            padding (6, 3) xsize 45
                        textbutton "-1":
                            action Function(ajuste_cel_modificar, "yoffset", -1, True)
                            text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "+1":
                            action Function(ajuste_cel_modificar, "yoffset", 1, True)
                            text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "-5":
                            action Function(ajuste_cel_modificar, "yoffset", -5, True)
                            text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "+5":
                            action Function(ajuste_cel_modificar, "yoffset", 5, True)
                            text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

                    # ancho
                    hbox:
                        spacing 5
                        yalign 0.5
                        text "ancho:" size 13 color "#aaaaaa" yalign 0.5 xsize 70
                        $ _sw = str(_sel_elem.size_w) if _sel_elem.size_w else "-"
                        textbutton "[_sw]":
                            action Function(ajuste_cel_abrir_input, "size_w", True)
                            text_size 14 text_color "#ffffff" text_bold True
                            background "#0d0d1f" hover_background "#1a1a3f"
                            padding (6, 3) xsize 45
                        textbutton "-5":
                            action Function(ajuste_cel_modificar, "size_w", -5, True)
                            text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "+5":
                            action Function(ajuste_cel_modificar, "size_w", 5, True)
                            text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

                    # alto
                    hbox:
                        spacing 5
                        yalign 0.5
                        text "alto:" size 13 color "#aaaaaa" yalign 0.5 xsize 70
                        $ _sh = str(_sel_elem.size_h) if _sel_elem.size_h else "-"
                        textbutton "[_sh]":
                            action Function(ajuste_cel_abrir_input, "size_h", True)
                            text_size 14 text_color "#ffffff" text_bold True
                            background "#0d0d1f" hover_background "#1a1a3f"
                            padding (6, 3) xsize 45
                        textbutton "-5":
                            action Function(ajuste_cel_modificar, "size_h", -5, True)
                            text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
                        textbutton "+5":
                            action Function(ajuste_cel_modificar, "size_h", 5, True)
                            text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

                    if _sel_elem.fue_modificado():
                        text "* Modificado" size 12 color "#FFD700" xalign 1.0


################################################################################
## Pestana Area de Trabajo
################################################################################

screen _panel_ajuste_area():
    vbox:
        spacing 6

        text "Area de Trabajo" size 14 color "#4FC3F7" bold True
        text "Define el espacio donde funcionan los menus" size 11 color "#888888"

        null height 4
        text "Posicion" size 14 color "#4FC3F7" bold True

        # xpos
        hbox:
            spacing 5
            yalign 0.5
            text "xpos:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[ajuste_cel_area_x]":
                action Function(ajuste_cel_area_abrir_input, "area_x")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 55
            textbutton "-10":
                action Function(ajuste_cel_area_modificar, "area_x", -10)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+10":
                action Function(ajuste_cel_area_modificar, "area_x", 10)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "-50":
                action Function(ajuste_cel_area_modificar, "area_x", -50)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+50":
                action Function(ajuste_cel_area_modificar, "area_x", 50)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # ypos
        hbox:
            spacing 5
            yalign 0.5
            text "ypos:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[ajuste_cel_area_y]":
                action Function(ajuste_cel_area_abrir_input, "area_y")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 55
            textbutton "-10":
                action Function(ajuste_cel_area_modificar, "area_y", -10)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+10":
                action Function(ajuste_cel_area_modificar, "area_y", 10)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "-50":
                action Function(ajuste_cel_area_modificar, "area_y", -50)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+50":
                action Function(ajuste_cel_area_modificar, "area_y", 50)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        null height 4
        text "Tamanio" size 14 color "#4FC3F7" bold True

        # ancho
        hbox:
            spacing 5
            yalign 0.5
            text "ancho:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[ajuste_cel_area_w]":
                action Function(ajuste_cel_area_abrir_input, "area_w")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 55
            textbutton "-10":
                action Function(ajuste_cel_area_modificar, "area_w", -10)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+10":
                action Function(ajuste_cel_area_modificar, "area_w", 10)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "-50":
                action Function(ajuste_cel_area_modificar, "area_w", -50)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+50":
                action Function(ajuste_cel_area_modificar, "area_w", 50)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # alto
        hbox:
            spacing 5
            yalign 0.5
            text "alto:" size 13 color "#aaaaaa" yalign 0.5 xsize 75
            textbutton "[ajuste_cel_area_h]":
                action Function(ajuste_cel_area_abrir_input, "area_h")
                text_size 14 text_color "#ffffff" text_bold True
                background "#0d0d1f" hover_background "#1a1a3f"
                padding (6, 3) xsize 55
            textbutton "-10":
                action Function(ajuste_cel_area_modificar, "area_h", -10)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+10":
                action Function(ajuste_cel_area_modificar, "area_h", 10)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "-50":
                action Function(ajuste_cel_area_modificar, "area_h", -50)
                text_size 13 text_color "#ff8888" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)
            textbutton "+50":
                action Function(ajuste_cel_area_modificar, "area_h", 50)
                text_size 13 text_color "#88ff88" background "#2a2a2a" hover_background "#3a3a3a" padding (7, 4)

        # Indicador de cambios
        if _area_fue_modificada():
            text "* Modificado" size 12 color "#FFD700" xalign 1.0
