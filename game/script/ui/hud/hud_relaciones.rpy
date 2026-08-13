################################################################################
## App de Relaciones — una fila por NPC
################################################################################
## La lista de desbloqueos ya no vive acá: tiene pantalla propia
## (panel_desbloqueos, en hud_desbloqueos.rpy), a la que se entra por el botón
## 🔓 de la fila. Antes era un desplegable con una flecha al pie de cada fila.

# Descripcion que muestra el cuadro flotante del panel de Desbloqueos. Vive acá
# porque la usan las dos pantallas.
default _rel_hover_desc = None

################################################################################
## Screen principal
################################################################################

screen panel_relaciones():
    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_relaciones") if modo_ajuste_celular else None
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    use _celular_fondo()
    use _celular_cerrar_exterior("panel_relaciones")

    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            use _celular_barra_status("panel_relaciones")
            use _celular_app_header(_("Relaciones"), "💝", [Hide("panel_relaciones"), Show("menu_celular")], "panel_relaciones")

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (int(8 * _k), int(8 * _k), int(20 * _k), int(8 * _k))

                    vbox:
                        xfill True
                        spacing int(8 * _k)

                        for _npc_rel_id in ["violet", "jasmine", "monica"]:
                            use _rel_bloque_npc(_npc_rel_id)


################################################################################
## Bloque por NPC
################################################################################

screen _rel_bloque_npc(npc_id):
    $ _npc_r = obtener_npc(npc_id)
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    if _npc_r and _npc_r.obtener_estado("conocido", False):
        # stat_mostrado = valor real + lo que espera en reserva. Es el UNICO
        # lugar donde los dos se suman: el sobrante son puntos de quest ganados
        # por encima del tope, que se cobran al liberarse el tramo. Se muestran
        # acá para que el jugador vea lo que tiene (ej. 7/5), pero no se tocan
        # el stat real ni nada que dependa de el.
        $ _amor_r  = stat_mostrado(npc_id, "amor")
        $ _deseo_r = stat_mostrado(npc_id, "deseo")

        # Tope de hitos: hasta donde puede subir hoy cada stat. Mientras haya un
        # hito pendiente se muestra "5/5" en vez de "5/100", asi el jugador ve
        # que el numero se freno a proposito y no parece un bug. Sin hitos
        # pendientes el tope es 100 y la fila se ve como siempre.
        $ _tope_amor_r  = tope_stat(npc_id, "amor")
        $ _tope_deseo_r = tope_stat(npc_id, "deseo")

        # Ubicacion: la resuelve el tracker (unica fuente de verdad — respeta
        # los NPCs ocultos por restriccion de quest).
        $ _loc_r = tracker_ubicacion_npc(npc_id)

        # Estado de talk del dia. obtener_estado_activo() ya resuelve la
        # prioridad de los especiales sobre el general y asigna uno si falta.
        $ _estado_r = sistema_talk.obtener_estado_activo(npc_id) if hasattr(store, 'sistema_talk') else None
        $ _estado_txt_r = renpy.translate_string(_estado_r.nombre) if _estado_r else renpy.translate_string("Sin novedades")

        # ── Medidas de la fila ───────────────────────────────────────────────
        # Dentro de un hbox, un hijo con `xfill True` se come TODO el ancho
        # restante y empuja a los que siguen fuera del frame (por eso los stats
        # no se veian). Cada columna va con xsize calculado, igual que _rel_item.
        #
        # Ancho util = area del celular
        #              - padding del viewport exterior (8 izq + 20 der)
        #              - padding de la propia fila (10 x 2)
        # Ancho util = area del celular - padding del viewport (8 izq + 20 der).
        # La fila NO suma padding propio: va en (0,0) para que la foto llegue al
        # ras de los bordes (ver abajo).
        $ _rel_avail   = ajuste_cel_area_w - int(28 * _k)
        $ _rel_gap     = int(10 * _k)

        # Alto de la fila = alto de la FOTO, que es hermana de todo el bloque
        # de texto.
        #
        # OJO: tiene que ser MAYOR que el alto real del contenido de la col 2
        # (nombre + 2 lineas). Si el contenido desborda, la fila crece con el y
        # la foto queda corta — se ve como si la imagen "no agrandara".
        $ _rel_alto    = int(132 * _k)

        # Columna 2 = todo lo que no es la foto
        $ _rel_col2_w  = max(int(120 * _k), _rel_avail - _rel_alto - _rel_gap)
        # Dentro de la col 2: los stats van pegados al texto, no contra el borde
        # derecho — con la columna de texto ocupando todo el sobrante quedaban
        # separados por un hueco enorme.
        $ _rel_stats_w = int(112 * _k)
        $ _rel_texto_w = max(int(80 * _k), _rel_col2_w - _rel_stats_w)

        # Las imagenes son 250x250 exactas: este zoom las lleva justo al alto de
        # la fila sin deformarlas.
        $ _rel_zoom    = _rel_alto / 250.0

        frame:
            xfill True
            background "#12122aCC"
            # padding CERO a proposito: cualquier padding acá pinta una franja
            # del azul de la fila alrededor de la foto y se ve como un borde.
            # El margen que necesita el texto se lo pone la columna 2.
            padding (0, 0)

            hbox:
                spacing _rel_gap
                xfill True

                # ── Col 1: foto, al ras de la fila (sin margen alrededor) ──
                $ _foto_r = "images/hud/personajes_{}.png".format(npc_id)
                if renpy.loadable(_foto_r):
                    add _foto_r zoom _rel_zoom
                else:
                    frame:
                        xysize (_rel_alto, _rel_alto)
                        background "#3a3a5a"
                        padding (0, 0)
                        text "?" size int(30 * _k) xalign 0.5 yalign 0.5 color "#ffffff"

                # ── Col 2: datos, DENTRO del alto de la foto ──
                # Sigue siendo un `fixed` con ysize clavado y no un vbox: asi el
                # bloque de texto no puede estirar la fila por encima del alto
                # de la foto pase lo que pase con su contenido.
                fixed:
                    xsize _rel_col2_w
                    ysize _rel_alto

                    # Nombre + boton, y despues DOS FILAS que llevan el dato a
                    # la izquierda y el stat a la derecha. Van en el mismo hbox
                    # a proposito: alinear dos columnas independientes por
                    # yalign no funciona (el borde inferior del hbox no
                    # coincide con donde termina la linea de Estado).
                    # Compartiendo fila, la alineacion queda garantizada.
                    vbox:
                        yalign 0.0
                        spacing int(3 * _k)

                        # Respiro arriba: baja el titulo y, con el, todo lo que
                        # sigue (va en este mismo vbox). Se agrando al sacar la
                        # flecha del pie: ese espacio quedo libre.
                        null height int(20 * _k)

                        # Fila del nombre: titulo a la izquierda y el boton de
                        # Desbloqueos pegado a la derecha. El hbox va con
                        # xfill True y el boton con xalign 1.0 — NO con xsize:
                        # el reparto por xsize de mas abajo existe porque ahi
                        # conviven texto largo y stats, aca alcanza con empujar.
                        hbox:
                            xfill True
                            yalign 0.5

                            text _npc_r.nombre size int(27 * _k) color "#ffffff" bold True yalign 0.5

                            button:
                                xalign 1.0
                                yalign 0.5
                                background "#1e1e40CC"
                                hover_background "#2a2a60CC"
                                padding (int(12 * _k), int(8 * _k))
                                action [Hide("panel_relaciones"), Show("panel_desbloqueos", npc_id=npc_id)]

                                hbox:
                                    spacing int(6 * _k)
                                    yalign 0.5
                                    text "🔓" size int(17 * _k) yalign 0.5
                                    # translate_string y no _(): con _() el
                                    # extractor genera una entrada aparte en
                                    # tl/english/script/... que choca con la que
                                    # vive a mano en relaciones_strings.rpy.
                                    text renpy.translate_string("Desbloqueos") size int(16 * _k) color "#dddddd" yalign 0.5

                        null height int(8 * _k)

                        # Fila 1: Locacion + amor
                        hbox:
                            xfill True
                            frame:
                                xsize _rel_texto_w
                                background None
                                padding (0, 0)
                                text "{} [_loc_r]".format(renpy.translate_string("Locación:")) size int(16 * _k) color "#9aa8c0" yalign 0.5
                            hbox:
                                spacing int(5 * _k)
                                yalign 0.5
                                text "[_amor_r]/[_tope_amor_r]" size int(17 * _k) color "#FF6B9D" bold True yalign 0.5
                                text "❤️" size int(17 * _k) yalign 0.5

                        # Fila 2: Estado + deseo
                        hbox:
                            xfill True
                            frame:
                                xsize _rel_texto_w
                                background None
                                padding (0, 0)
                                text "{} [_estado_txt_r]".format(renpy.translate_string("Estado de ánimo:")) size int(16 * _k) color "#9aa8c0" yalign 0.5
                            hbox:
                                spacing int(5 * _k)
                                yalign 0.5
                                text "[_deseo_r]/[_tope_deseo_r]" size int(17 * _k) color "#E040FB" bold True yalign 0.5
                                text "💋" size int(17 * _k) yalign 0.5
