################################################################################
## App de Relaciones — Desbloqueos por NPC
################################################################################

default _rel_abiertos  = {}
default _rel_hover_desc = None

################################################################################
## Screen principal
################################################################################

screen panel_relaciones():
    modal True

    $ _ajc = sistema_ajuste_cel.obtener_container("panel_relaciones") if modo_ajuste_celular else None

    add "images/hud/interfaz_celular.png" xalign 0.0 yalign 0.0
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

            use _celular_barra_status()
            use _celular_app_header(_("Relaciones"), "💝", [Hide("panel_relaciones"), Show("menu_celular")])

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True

                frame:
                    xfill True
                    background None
                    padding (8, 8, 20, 8)

                    vbox:
                        xfill True
                        spacing 8

                        for _npc_rel_id in ["violet", "jasmine", "monica"]:
                            use _rel_bloque_npc(_npc_rel_id)

    if _rel_hover_desc:
        frame:
            xpos ajuste_cel_area_x + 10
            ypos ajuste_cel_area_y + ajuste_cel_area_h - 76
            xsize ajuste_cel_area_w - 20
            background "#0a0a1eEE"
            padding (10, 8)
            text _rel_hover_desc size 13 color "#cccccc"


################################################################################
## Bloque por NPC
################################################################################

screen _rel_bloque_npc(npc_id):
    $ _npc_r = obtener_npc(npc_id)

    if _npc_r and _npc_r.obtener_estado("conocido", False):
        $ _amor_r  = _npc_r.obtener_estado("amor",  0)
        $ _deseo_r = _npc_r.obtener_estado("deseo", 0)

        frame:
            xfill True
            background "#12122aCC"
            padding (10, 10)

            vbox:
                xfill True
                spacing 6

                # Cabecera
                hbox:
                    spacing 10
                    yalign 0.5
                    $ _foto_r = "images/hud/pista_{}.png".format(npc_id)
                    if renpy.loadable(_foto_r):
                        add _foto_r zoom 0.15 yalign 0.5
                    else:
                        frame:
                            xysize (38, 38)
                            background "#3a3a5a"
                            text "?" size 20 xalign 0.5 yalign 0.5 color "#ffffff"
                    text _npc_r.nombre size 18 color "#ffffff" bold True yalign 0.5

                use _rel_stat("❤", _amor_r,  "#c0392b", npc_id, "amor")
                use _rel_stat("🔥", _deseo_r, "#e67e22", npc_id, "deseo")


################################################################################
## Stat: etiqueta + barra + desplegable
################################################################################

screen _rel_stat(icono, valor, color_barra, npc_id, stat):
    $ _v_r = min(max(valor, 0), 100)

    vbox:
        xfill True
        spacing 4

        # Etiqueta con valor
        hbox:
            spacing 6
            text icono size 14 yalign 0.5
            text "{} / 100".format(_v_r) size 13 color "#cccccc" bold True yalign 0.5

        # Barra
        frame:
            xfill True
            ysize 8
            background "#1a1a35"
            padding (0, 0)
            if _v_r > 0:
                frame:
                    xsize (_v_r / 100.0)
                    yfill True
                    background color_barra
                    padding (0, 0)

        # Botón desplegable
        use _rel_desplegable(npc_id, stat)


################################################################################
## Botón desplegable + lista
################################################################################

screen _rel_desplegable(npc_id, stat):
    $ _clave_r    = "{}_{}".format(npc_id, stat)
    $ _abierto_r  = _rel_abiertos.get(_clave_r, False)
    $ _desbloq_r, _bloq_r = obtener_desbloqueos_stat(npc_id, stat)
    $ _total_r    = len(_desbloq_r) + len(_bloq_r)

    if _total_r > 0:
        vbox:
            xfill True
            spacing 0

            button:
                xfill True
                background "#1e1e40CC"
                hover_background "#2a2a58CC"
                padding (8, 6)
                action SetDict(_rel_abiertos, _clave_r, not _abierto_r)

                hbox:
                    xfill True
                    spacing 6
                    yalign 0.5
                    text ("▲" if _abierto_r else "▼") size 12 color "#7a8aaa" yalign 0.5
                    text _("Desbloqueos") size 13 color "#cccccc" yalign 0.5 xfill True
                    text "[len(_desbloq_r)]/[_total_r]" size 12 color "#7a8aaa" yalign 0.5

            if _abierto_r:
                frame:
                    xfill True
                    background "#0d0d22CC"
                    padding (6, 4)

                    vbox:
                        xfill True
                        spacing 2

                        for _it in _desbloq_r:
                            use _rel_item(_it, False)

                        null height 3
                        frame:
                            xfill True
                            ysize 1
                            background "#3a3a5a"
                            padding (0, 0)
                        null height 3

                        for _it in _bloq_r:
                            use _rel_item(_it, True)


################################################################################
## Ítem (desbloqueado y bloqueado comparten screen, flag bloqueado=True/False)
################################################################################

screen _rel_item(item, bloqueado):
    $ _col_icono  = "#555566" if bloqueado else "#ffffff"
    $ _col_nombre = "#666677" if bloqueado else "#ffffff"
    $ _col_numero = "#666677" if bloqueado else "#ffffff"

    ## Espacio total disponible para el hbox:
    ## ajuste_cel_area_w - padding_exterior(28) - padding_npc(20) - padding_lista(12) - padding_boton(9)
    $ _avail = ajuste_cel_area_w - 69
    $ _seg3  = 56 if bloqueado else 34
    $ _seg1  = 26
    $ _seg2  = max(100, _avail - _seg1 - _seg3)

    button:
        xfill True
        background None
        hover_background ("#ffffff08" if not bloqueado else None)
        padding (4, 5)
        action NullAction()
        if not bloqueado and item["desc"]:
            hovered SetVariable("_rel_hover_desc", item["desc"])
            unhovered SetVariable("_rel_hover_desc", None)

        hbox:
            spacing 0

            ## Seg 1: icono — xsize fijo
            frame:
                xsize _seg1
                background None
                padding (0, 0)
                text item["icono"] size 16 color _col_icono xalign 0.5 yalign 0.5

            ## Seg 2: nombre — xsize calculado (ni xfill ni ambigüedad)
            frame:
                xsize _seg2
                background None
                padding (2, 0)
                text item["nombre"] size 13 color _col_nombre yalign 0.5

            ## Seg 3: requisito [+ candado] — xsize fijo
            frame:
                xsize _seg3
                background None
                padding (0, 0)

                if bloqueado:
                    hbox:
                        xalign 1.0
                        yalign 0.5
                        spacing 4
                        text str(item["umbral"]) size 12 color _col_numero yalign 0.5
                        text "🔒" size 13 yalign 0.5
                else:
                    text str(item["umbral"]) size 12 color _col_numero xalign 0.5 yalign 0.5
