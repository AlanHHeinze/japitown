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

    # Fondo del celular
    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

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
            use _celular_barra_status()

            # Header de app
            use _celular_app_header("Galería", "🖼️", [Hide("panel_galeria"), Show("menu_celular")])

            # Tabs de filtro
            frame:
                xfill True
                background "#12122aCC"
                padding (10, 8)

                hbox:
                    spacing 8
                    xalign 0.5

                    $ _btn_bg_all = "#1565C0" if _galeria_filtro is None else "#1e1e3aCC"
                    textbutton "Todas":
                        action SetVariable("_galeria_filtro", None)
                        text_size 13
                        text_color "#ffffff"
                        background _btn_bg_all
                        hover_background "#1976D2"
                        padding (12, 6)

                    $ _btn_bg_j = "#1565C0" if _galeria_filtro == "jasmine" else "#1e1e3aCC"
                    textbutton "Jasmine":
                        action SetVariable("_galeria_filtro", "jasmine")
                        text_size 13
                        text_color "#ffffff"
                        background _btn_bg_j
                        hover_background "#1976D2"
                        padding (12, 6)

                    $ _btn_bg_m = "#1565C0" if _galeria_filtro == "monica" else "#1e1e3aCC"
                    textbutton "Monica":
                        action SetVariable("_galeria_filtro", "monica")
                        text_size 13
                        text_color "#ffffff"
                        background _btn_bg_m
                        hover_background "#1976D2"
                        padding (12, 6)

                    $ _btn_bg_v = "#1565C0" if _galeria_filtro == "violet" else "#1e1e3aCC"
                    textbutton "Violet":
                        action SetVariable("_galeria_filtro", "violet")
                        text_size 13
                        text_color "#ffffff"
                        background _btn_bg_v
                        hover_background "#1976D2"
                        padding (12, 6)

            # Contenido — Grid de fotos
            $ _fotos = sistema_mensajes.obtener_galeria(_galeria_filtro)

            if len(_fotos) > 0:
                viewport:
                    xfill True
                    yfill True
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    frame:
                        xfill True
                        background None
                        padding (15, 10)

                        grid 3 max(1, (len(_fotos) + 2) // 3):
                            spacing 10
                            xalign 0.5

                            for _foto in _fotos:
                                button:
                                    action Show("vista_foto_ampliada", foto=_foto["ruta"])

                                    frame:
                                        xysize (180, 130)
                                        background "#1e1e3aCC"
                                        hover_background "#2a2a50CC"

                                        vbox:
                                            xalign 0.5
                                            yalign 0.5
                                            spacing 4

                                            add _foto["ruta"] xalign 0.5 yalign 0.5 at transform:
                                                fit "contain"
                                                xysize (160, 100)

                                            $ _fn = _foto["npc_id"].capitalize()
                                            text "[_fn]" size 10 color "#aaaaaa" xalign 0.5

                            # Rellenar grid con espacios vacíos
                            for _i in range(((len(_fotos) + 2) // 3) * 3 - len(_fotos)):
                                null

            else:
                frame:
                    xfill True
                    yfill True
                    background "#1e1e3a44"
                    padding (20, 40)

                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 10
                        text "📷" size 48 xalign 0.5
                        text "No hay fotos aún" size 16 color "#666666" xalign 0.5
                        text "Las fotos se desbloquean a través de conversaciones" size 12 color "#444444" xalign 0.5
