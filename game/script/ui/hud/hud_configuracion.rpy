################################################################################
## App Configuracion del Celular
################################################################################

screen panel_configuracion():

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_configuracion") if modo_ajuste_celular else None

    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0

    use _celular_cerrar_exterior("panel_configuracion")

    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            use _celular_barra_status()
            use _celular_app_header(_("Configuración"), u"⚙️", [Hide("panel_configuracion"), Show("menu_celular")])

            # Lista de opciones
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

                    vbox:
                        spacing 2
                        xfill True

                        # ── Opción: Mostrar Accion movimiento ──
                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (15, 14)

                            hbox:
                                xfill True
                                yalign 0.5
                                spacing 10

                                vbox:
                                    xfill True
                                    yalign 0.5
                                    spacing 3
                                    text _("Mostrar Accion movimiento") size 15 color "#ffffff" bold True
                                    text _("Muestra el botón para visualizar las salidas de cada locación.") size 11 color "#888888"

                                # Toggle ON / OFF
                                button:
                                    yalign 0.5
                                    xsize 64
                                    ysize 30
                                    if config_mostrar_accion_movimiento:
                                        background "#4CAF50"
                                        hover_background "#66BB6A"
                                        action [
                                            SetVariable("config_mostrar_accion_movimiento", False),
                                            SetVariable("visualizador_hotspot_activo", False),
                                        ]
                                    else:
                                        background "#555555"
                                        hover_background "#777777"
                                        action SetVariable("config_mostrar_accion_movimiento", True)

                                    text ("ON" if config_mostrar_accion_movimiento else "OFF"):
                                        size 13
                                        bold True
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
