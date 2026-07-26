################################################################################
## App Configuracion del Celular
################################################################################

screen panel_configuracion():

    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_configuracion") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    use _celular_fondo()

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

            use _celular_barra_status("panel_configuracion")
            use _celular_app_header(_("Configuración"), u"⚙️", [Hide("panel_configuracion"), Show("menu_celular")], "panel_configuracion")

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
                    padding (int(15 * _k), int(10 * _k))

                    vbox:
                        spacing int(2 * _k)
                        xfill True

                        # ── Opción: Mostrar Accion movimiento ──
                        frame:
                            xfill True
                            background "#1e1e3aCC"
                            padding (int(15 * _k), int(14 * _k))

                            hbox:
                                xfill True
                                yalign 0.5
                                spacing int(10 * _k)

                                vbox:
                                    xfill True
                                    yalign 0.5
                                    spacing int(3 * _k)
                                    text _("Mostrar Accion movimiento") size int(15 * _k) color "#ffffff" bold True
                                    text _("Muestra el botón para visualizar las salidas de cada locación.") size int(11 * _k) color "#888888"

                                # Toggle ON / OFF
                                button:
                                    yalign 0.5
                                    xsize int(64 * _k)
                                    ysize int(30 * _k)
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
                                        size int(13 * _k)
                                        bold True
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
