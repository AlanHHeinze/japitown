################################################################################
## Galería de Fotos
################################################################################
## Pantalla para ver fotos desbloqueadas a través del sistema de mensajes.

# Variable para el filtro de NPC activo
default _galeria_filtro = None

screen panel_galeria():
    """Panel de galería con fotos desbloqueadas — App Galería"""

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_galeria") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    # Fondo del celular
    use _celular_fondo()

    # Click fuera del celular cierra todo
    use _celular_cerrar_exterior("panel_galeria")

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
            use _celular_barra_status("panel_galeria")

            # Header de app
            use _celular_app_header("Galería", "🖼️", [Hide("panel_galeria"), Show("menu_celular")], "panel_galeria")

            # Tabs de filtro
            frame:
                xfill True
                background "#12122aCC"
                padding (int(10 * _k), int(8 * _k))

                hbox:
                    spacing int(8 * _k)
                    xalign 0.5

                    $ _btn_bg_all = "#1565C0" if _galeria_filtro is None else "#1e1e3aCC"
                    textbutton "Todas":
                        action SetVariable("_galeria_filtro", None)
                        text_size int(13 * _k)
                        text_color "#ffffff"
                        background _btn_bg_all
                        hover_background "#1976D2"
                        padding (int(12 * _k), int(6 * _k))

                    $ _btn_bg_j = "#1565C0" if _galeria_filtro == "jasmine" else "#1e1e3aCC"
                    textbutton "Jasmine":
                        action SetVariable("_galeria_filtro", "jasmine")
                        text_size int(13 * _k)
                        text_color "#ffffff"
                        background _btn_bg_j
                        hover_background "#1976D2"
                        padding (int(12 * _k), int(6 * _k))

                    $ _btn_bg_m = "#1565C0" if _galeria_filtro == "monica" else "#1e1e3aCC"
                    textbutton "Monica":
                        action SetVariable("_galeria_filtro", "monica")
                        text_size int(13 * _k)
                        text_color "#ffffff"
                        background _btn_bg_m
                        hover_background "#1976D2"
                        padding (int(12 * _k), int(6 * _k))

                    $ _btn_bg_v = "#1565C0" if _galeria_filtro == "violet" else "#1e1e3aCC"
                    textbutton "Violet":
                        action SetVariable("_galeria_filtro", "violet")
                        text_size int(13 * _k)
                        text_color "#ffffff"
                        background _btn_bg_v
                        hover_background "#1976D2"
                        padding (int(12 * _k), int(6 * _k))

            # Contenido — Grid de fotos
            $ _fotos = sistema_mensajes.obtener_galeria(_galeria_filtro)

            if len(_fotos) > 0:
                # Columnas adaptadas al ancho disponible: con las miniaturas 4x
                # más grandes, 3 columnas fijas no entran en pantalla táctil
                # (mismo problema que tuvo la grilla de apps del home).
                $ _gal_pad = int(15 * _k)
                $ _gal_thumb_w = int(180 * _k)
                $ _gal_spacing = int(10 * _k)
                $ _gal_avail = ajuste_cel_area_w - _gal_pad * 2
                $ _gal_max_cols = max(1, (_gal_avail + _gal_spacing) // (_gal_thumb_w + _gal_spacing))
                $ _gal_cols = min(3, _gal_max_cols)
                $ _gal_filas = (len(_fotos) + _gal_cols - 1) // _gal_cols

                viewport:
                    xfill True
                    yfill True
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    frame:
                        xfill True
                        background None
                        padding (_gal_pad, int(10 * _k))

                        grid _gal_cols _gal_filas:
                            spacing _gal_spacing
                            xalign 0.5

                            for _foto in _fotos:
                                button:
                                    action Show("vista_foto_ampliada", foto=_foto["ruta"])

                                    frame:
                                        xysize (_gal_thumb_w, int(130 * _k))
                                        background "#1e1e3aCC"
                                        hover_background "#2a2a50CC"

                                        vbox:
                                            xalign 0.5
                                            yalign 0.5
                                            spacing int(4 * _k)

                                            add _foto["ruta"] xalign 0.5 yalign 0.5 at transform:
                                                fit "contain"
                                                xysize (int(160 * _k), int(100 * _k))

                                            $ _fn = _foto["npc_id"].capitalize()
                                            text "[_fn]" size int(10 * _k) color "#aaaaaa" xalign 0.5

                            # Rellenar grid con espacios vacíos
                            for _i in range(_gal_cols * _gal_filas - len(_fotos)):
                                null

            else:
                frame:
                    xfill True
                    yfill True
                    background "#1e1e3a44"
                    padding (int(20 * _k), int(40 * _k))

                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing int(10 * _k)
                        text "📷" size int(48 * _k) xalign 0.5
                        text "No hay fotos aún" size int(16 * _k) color "#666666" xalign 0.5
                        text "Las fotos se desbloquean a través de conversaciones" size int(12 * _k) color "#444444" xalign 0.5
