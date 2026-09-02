################################################################################
## App de Contenido de una Ventaja — que hay adentro
################################################################################
## Sub-pantalla de Desbloqueos: se entra por el botón 👁️ de una fila de ventaja
## y el botón de volver regresa a Desbloqueos, no al home del celular.
##
## Lista las situaciones concretas que habilita esa ventaja, cada una con su
## estado (bloqueada / sin ver / vista) y una PISTA de cómo llegar. Los tres
## estados, sus iconos y sus colores los define core/hitos/ventajas_contenido.rpy;
## acá solo se pintan.
##
## NADA HARDCODEADO: la lista sale de obtener_contenido_ventaja(). Una situación
## nueva aparece sola con solo registrarla desde el archivo de su contenido.

# Cabecera de la subapp. El {} lo llena el nombre de la ventaja.
define VC_TITULO = "{} — Contenido"

# Texto cuando la ventaja no tiene NINGUNA entrada para este NPC. No deberia
# verse (sin entradas no se dibuja el ojo que trae acá), pero si alguna vez se
# llega por otro camino es mejor un cartel que una pantalla vacia.
define VC_TXT_VACIO = "Todavía no hay contenido cargado para esta ventaja."

# Pie de la lista: aclara que las bloqueadas no son un error.
define VC_TXT_PIE = "Lo que aparece con 🔒 todavía no se puede alcanzar; hace falta avanzar en otra parte primero."


screen panel_contenido_ventaja(npc_id="violet", ventaja_id="mensajear"):
    modal True

    # Sin container de ajuste_celular, igual que panel_desbloqueos: su pantalla
    # madre tampoco esta registrada y registrar solo a la hija dejaria la
    # herramienta editando una y no la otra.
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    $ _npc_vc = obtener_npc(npc_id)
    $ _nombre_vc = _npc_vc.nombre if _npc_vc else npc_id

    # Nombre de la ventaja para el titulo. Sale del catalogo y pasa por el mismo
    # reemplazo de {npc} que usa el panel de Desbloqueos.
    $ _cfg_vc = obtener_ventaja(ventaja_id)
    $ _nom_vc = renpy.translate_string(_cfg_vc["nombre"]).replace("{npc}", _nombre_vc) if _cfg_vc else ventaja_id

    $ _entradas_vc = obtener_contenido_ventaja(ventaja_id, npc_id)
    $ _vistas_vc, _total_vc = contar_contenido_ventaja(ventaja_id, npc_id)

    use _celular_fondo()
    use _celular_cerrar_exterior("panel_contenido_ventaja")

    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            use _celular_barra_status("panel_contenido_ventaja")
            # El volver va a Desbloqueos y le devuelve el npc_id: sin eso la
            # pantalla madre se reabriria con su NPC por defecto.
            use _celular_app_header(
                renpy.translate_string(VC_TITULO).format(_nom_vc),
                u"👁️",
                [Hide("panel_contenido_ventaja"), Show("panel_desbloqueos", npc_id=npc_id)],
                "panel_contenido_ventaja")

            # Contador de progreso. Solo cuenta lo alcanzable (ver
            # contar_contenido_ventaja).
            frame:
                xfill True
                background "#1e1e40FF"
                padding (int(10 * _k), int(6 * _k))
                text "[_vistas_vc]/[_total_vc]":
                    size int(15 * _k)
                    color "#9aa8c0"
                    bold True
                    xalign 1.0

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

                        if _entradas_vc:
                            for _e_vc in _entradas_vc:
                                use _vc_fila(_e_vc) id _e_vc["id"]

                            text renpy.translate_string(VC_TXT_PIE):
                                size int(12 * _k)
                                color "#6a6a80"
                                italic True
                        else:
                            text renpy.translate_string(VC_TXT_VACIO):
                                size int(14 * _k)
                                color "#6a6a80"
                                italic True


################################################################################
## Fila de una situación
################################################################################
## No es un button: acá no hay nada que tocar. La descripción va SIEMPRE
## visible, debajo del nombre, en vez de en el cuadro emergente de Desbloqueos —
## es una pista de cómo llegar, o sea justo lo que el jugador vino a leer, y
## esconderla detrás de un hover la volvería inútil en táctil.

screen _vc_fila(entrada):
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    $ _col_vc = VC_COLOR[entrada["estado"]]
    $ _ico_vc = VC_ICONO[entrada["estado"]]

    frame:
        xfill True
        background "#12122aFF"
        padding (int(10 * _k), int(8 * _k))

        hbox:
            xfill True
            spacing int(10 * _k)

            # Columna del icono: ancho fijo para que los nombres alineen aunque
            # el emoji mida distinto.
            frame:
                xsize int(28 * _k)
                background None
                padding (0, 0)
                text _ico_vc size int(16 * _k) yalign 0.0

            vbox:
                xfill True
                spacing int(3 * _k)

                text entrada["nombre"]:
                    size int(16 * _k)
                    color _col_vc
                    bold True

                # La pista siempre en gris, sin importar el estado: lo que
                # cambia de color es el nombre, que es lo que marca el progreso.
                if entrada["desc"]:
                    text entrada["desc"]:
                        size int(13 * _k)
                        color "#8a8aa0"
