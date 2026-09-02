################################################################################
## App de Desbloqueos — hitos y ventajas de UN NPC
################################################################################
## Sub-pantalla de Relaciones: se entra por el botón 🔓 de la fila del NPC y el
## botón de volver regresa a Relaciones, no al home del celular.
##
## Muestra los HITOS del NPC separados por línea (amor / deseo) y, debajo de
## cada uno e indentadas, las VENTAJAS que otorga. Al pasar el mouse por una
## ventaja (o tocarla, en táctil) su descripción aparece en un cuadro al pie.
##
## NADA HARDCODEADO: todo sale de obtener_desbloqueos_stat(), que lee el
## catálogo de hitos y el de ventajas. Un hito o una ventaja nueva aparecen acá
## sin tocar este archivo. Las dos líneas (amor/deseo) sí están enumeradas, que
## es lo mismo que hace el resto del juego — los NPCs tienen exactamente esos
## dos stats.

# Líneas que muestra el panel: (stat, icono, titulo, color de la cabecera).
# El titulo se traduce al usarse. El color es el MISMO que el contador del stat
# en la app de Relaciones, para que las dos pantallas hablen el mismo idioma.
# Si algún día hay un stat más, se agrega acá y el resto sigue igual.
define _DESB_LINEAS = [
    ("amor",  "❤️", "Amor",  "#FF6B9D"),
    ("deseo", "💋", "Deseo", "#E040FB"),
]

# Fondo del cuadro de descripcion. Azul bastante mas claro que el resto del
# panel a proposito: la fila es #12122a y la cabecera de linea #1e1e40, asi que
# el cuadro tiene que despegarse de los dos para que se lea como algo que flota
# por encima y no como otra franja de la lista.
define DESB_POPUP_FONDO = "#2e4a8cF8"

# Nombre del rectangulo de foco que usa el nearrect del cuadro. Lo capturan los
# botones al hoverearse (CaptureFocus) y lo lee el nearrect (focus).
define DESB_FOCO_POPUP = "desb_pop"

# Viñeta de las ventajas. Es "•" (U+2022) y NO "└" (U+2514): las fuentes del
# juego (Roboto-Bold, neotoxic) no traen los caracteres de dibujo de cajas y
# salia el cuadradito de glifo faltante. Mismo problema que el ▼ que en su
# momento hubo que cambiar por 🔽 en la flecha de Relaciones.
define DESB_VINETA = u"•"

# Textos fijos del cuadro emergente. Explican QUE ES un hito y que es una
# ventaja; la descripcion concreta de cada ventaja se arma con DESB_TXT_VENTAJA.
define DESB_TXT_HITO = "Hito: Conseguir un Hito nos permite avanzar en misiones principales y desbloquear elecciones únicas."
define DESB_TXT_VENTAJAS = "Desbloquear una Ventaja nos da mejoras permanentes en algunas interacciones con el personaje."
define DESB_TXT_VENTAJA = "Esta ventaja otorga - {}"


################################################################################
## Pantalla principal
################################################################################

screen panel_desbloqueos(npc_id="violet"):
    modal True

    # Sin container de ajuste_celular a proposito: panel_relaciones, su pantalla
    # madre, tampoco esta registrada. Registrar solo a la hija dejaria la
    # herramienta editando una y no la otra.
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    $ _npc_d = obtener_npc(npc_id)
    $ _nombre_d = _npc_d.nombre if _npc_d else npc_id

    # Al entrar no hay nada hovereado. Sin esto queda colgada la descripcion de
    # la ultima ventaja que se toco en una visita anterior, y con ella el
    # rectangulo viejo contra el que se posicionaria el cuadro.
    on "show" action [SetVariable("_rel_hover_desc", None), ClearFocus(DESB_FOCO_POPUP)]

    use _celular_fondo()
    use _celular_cerrar_exterior("panel_desbloqueos")

    frame:
        xpos ajuste_cel_area_x
        ypos ajuste_cel_area_y
        xsize ajuste_cel_area_w
        ysize ajuste_cel_area_h
        background None
        padding (0, 0)

        vbox:
            xfill True

            use _celular_barra_status("panel_desbloqueos")
            # El volver va a Relaciones, no al menu del celular: esta pantalla
            # es hija de aquella.
            use _celular_app_header(
                "{} — {}".format(renpy.translate_string("Desbloqueos"), _nombre_d),
                "🔓",
                [Hide("panel_desbloqueos"), Show("panel_relaciones")],
                "panel_desbloqueos")

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

                        for _stat_d, _ico_d, _tit_d, _col_d in _DESB_LINEAS:
                            use _desb_linea(npc_id, _stat_d, _ico_d, renpy.translate_string(_tit_d), _col_d) id _stat_d

                        # NPC sin ningun hito cargado todavia (Jasmine y Monica
                        # hoy). Mejor decirlo que dejar la pantalla en blanco.
                        if not _desb_npc_tiene_hitos(npc_id):
                            frame:
                                xfill True
                                background "#12122aCC"
                                padding (int(10 * _k), int(14 * _k))
                                text renpy.translate_string("Todavía no hay nada que descubrir con esta persona.") size int(16 * _k) color "#7a8aaa" xalign 0.5

    # ── Cuadro flotante con la descripcion ───────────────────────────────────
    #
    # EN PC sale PEGADO AL ITEM: `nearrect` lo ubica contra el rectangulo del
    # displayable que capturamos con CaptureFocus("desb_pop") al hoverear.
    # `preferred_side "right"` lo manda a la derecha y, si no entra, Ren'Py lo
    # pasa solo al otro lado. El `ypos 0.5 / yanchor 0.5` del frame es lo que lo
    # centra verticalmente contra el item: nearrect calcula
    # layout_y = py + ypos*alto_item - yanchor*alto_cuadro.
    #
    # Es un `frame` pelado y NO un button a proposito: un button es focusable, y
    # si llegara a tapar al item que estas hovereando dispararia su unhovered →
    # se esconde el cuadro → volves a estar sobre el item → parpadeo infinito.
    #
    # EN TACTIL no existe "a la derecha": el celular ocupa toda la pantalla y no
    # hay margen adonde salir. Ahi se queda el cuadro centrado, y como tampoco
    # hay "sacar el mouse", es button para poder cerrarlo tocandolo.
    if _rel_hover_desc:
        if renpy.variant("small"):
            button:
                xpos ajuste_cel_area_x + int(ajuste_cel_area_w * 0.5)
                ypos ajuste_cel_area_y + int(ajuste_cel_area_h * 0.5)
                xanchor 0.5
                yanchor 0.5
                xmaximum ajuste_cel_area_w - int(40 * _k)
                background DESB_POPUP_FONDO
                padding (int(18 * _k), int(16 * _k))
                action SetVariable("_rel_hover_desc", None)
                text _rel_hover_desc size int(18 * _k) color "#ffffff"
        else:
            nearrect:
                focus "desb_pop"
                preferred_side "right"

                frame:
                    ypos 0.5
                    yanchor 0.5
                    xmaximum int(360 * _k)
                    background DESB_POPUP_FONDO
                    padding (int(16 * _k), int(14 * _k))
                    text _rel_hover_desc size int(18 * _k) color "#ffffff"


init python:

    def _desb_npc_tiene_hitos(npc_id):
        """True si el NPC tiene al menos un hito registrado en cualquier linea."""
        return len(obtener_hitos_npc(npc_id)) > 0

    def _desb_ancho_util(k):
        """
        Ancho que le queda a una fila de la lista, ya descontados los paddings
        que la envuelven: viewport (8 izq + 20 der), frame de la linea (6 x 2) y
        el propio boton de la fila (4 x 2).

        Una sola cuenta para TODAS las filas — hito, rotulo y ventaja. Si cada
        una la calculara por su lado, la que se pase de ancho estira el vbox y
        el frame de la linea recorta a las demas por la derecha.
        """
        return store.ajuste_cel_area_w - int(48 * k)


################################################################################
## Una línea (amor o deseo)
################################################################################

screen _desb_linea(npc_id, stat, icono, titulo, color_barra):
    $ _desbloq_r, _bloq_r = obtener_desbloqueos_stat(npc_id, stat)
    $ _total_r = len(_desbloq_r) + len(_bloq_r)
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    if _total_r > 0:
        vbox:
            xfill True
            spacing 0

            # Cabecera de la seccion: barra del color del stat, con icono,
            # titulo y contador CENTRADOS como un solo grupo. El hbox va sin
            # xfill (es el frame el que ocupa el ancho) y con xalign 0.5: asi
            # los tres se mantienen juntos en el medio en vez de repartirse
            # contra los bordes.
            frame:
                xfill True
                background color_barra
                padding (int(8 * _k), int(6 * _k))

                hbox:
                    xalign 0.5
                    spacing int(8 * _k)
                    yalign 0.5
                    text icono size int(17 * _k) yalign 0.5
                    text titulo size int(17 * _k) color "#ffffff" bold True yalign 0.5
                    text "[len(_desbloq_r)]/[_total_r]" size int(16 * _k) color "#ffffffCC" bold True yalign 0.5

            frame:
                xfill True
                background "#0d0d22CC"
                padding (int(6 * _k), int(4 * _k))

                vbox:
                    xfill True
                    spacing int(2 * _k)

                    # `id` en cada use: sin el, Ren'Py reusa el estado interno
                    # entre las repeticiones del for y una fila puede quedar
                    # renderizada con pedazos de otra.
                    for _it in _desbloq_r:
                        use _desb_hito(_it, False, npc_id) id _it["id"]

                    # Separador solo si hay algo de los dos lados
                    if _desbloq_r and _bloq_r:
                        null height int(3 * _k)
                        frame:
                            xfill True
                            ysize int(1 * _k)
                            background "#3a3a5a"
                            padding (0, 0)
                        null height int(3 * _k)

                    for _it in _bloq_r:
                        use _desb_hito(_it, True, npc_id) id _it["id"]


################################################################################
## Un hito + sus ventajas
################################################################################
## Conseguido y bloqueado comparten screen; cambian los colores y el candado.

screen _desb_hito(item, bloqueado, npc_id="violet"):
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    vbox:
        xfill True
        spacing 0

        use _desb_fila_hito(item, bloqueado)

        # Las ventajas del hito, bajo un rotulo "Ventajas" e indentadas para que
        # se lean como parte de él. Las de un hito bloqueado se muestran igual
        # (en gris): sirven para que el jugador sepa qué gana si sigue la línea.
        # Sin ventajas no va ni el rotulo — un titulo sobre una lista vacia
        # parece un bug.
        if item["ventajas"]:
            use _desb_rotulo_ventajas(bloqueado)

            for _v in item["ventajas"]:
                use _desb_fila_ventaja(_v, bloqueado, npc_id) id _v["id"]

        null height int(6 * _k)


################################################################################
## Fila del hito
################################################################################

screen _desb_fila_hito(item, bloqueado):
    $ _col_icono  = "#555566" if bloqueado else "#ffffff"
    $ _col_nombre = "#666677" if bloqueado else "#ffffff"
    $ _col_numero = "#666677" if bloqueado else "#ffffff"
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    ## Reparto de columnas. _desb_ancho_util() es la MISMA cuenta que usa la
    ## fila de ventaja: las dos tienen que medir igual o la mas ancha estira el
    ## vbox, el frame de la linea recorta por la derecha y se come la columna
    ## del umbral (por eso a algun hito le desaparecia el numero).
    ##
    ## _seg3 es fijo y generoso: ahi entran el numero y el candado, y si queda
    ## corto el numero (que va primero) es lo primero que se recorta.
    $ _avail = _desb_ancho_util(_k)
    $ _seg3  = int((80 if bloqueado else 50) * _k)
    $ _seg1  = int(32 * _k)
    $ _seg2  = max(int(80 * _k), _avail - _seg1 - _seg3)
    $ _txt_h = renpy.translate_string(DESB_TXT_HITO)

    button:
        xfill True
        background None
        hover_background "#ffffff08"
        padding (int(4 * _k), int(5 * _k))
        # hover para PC + action para tactil: ver la nota en _desb_fila_ventaja.
        # CaptureFocus guarda el rectangulo de ESTE boton para que el cuadro
        # salga pegado a el.
        #
        # El cuadro explica QUE ES un hito, igual para todos, y no la
        # descripcion propia de este hito: lo que el jugador necesita saber acá
        # es para qué sirve conseguirlos.
        action [SetVariable("_rel_hover_desc", _txt_h), CaptureFocus(DESB_FOCO_POPUP)]
        hovered [SetVariable("_rel_hover_desc", _txt_h), CaptureFocus(DESB_FOCO_POPUP)]
        unhovered SetVariable("_rel_hover_desc", None)

        hbox:
            spacing 0

            ## Seg 1: icono
            frame:
                xsize _seg1
                background None
                padding (0, 0)
                text item["icono"] size int(20 * _k) color _col_icono xalign 0.5 yalign 0.5

            ## Seg 2: nombre del hito
            frame:
                xsize _seg2
                background None
                padding (int(2 * _k), 0)
                text item["nombre"] size int(17 * _k) color _col_nombre bold True yalign 0.5

            ## Seg 3: umbral [+ candado]
            ## Numero y candado van en UN SOLO text y no en un hbox de dos: con
            ## dos displayables, el numero (el de la izquierda) era lo primero
            ## que se perdia si el alineado o el ancho no daban. Asi o se ve
            ## todo o no se ve nada, y no hay forma de que quede un candado
            ## suelto sin su numero.
            frame:
                xsize _seg3
                background None
                padding (0, 0)

                if bloqueado:
                    text "{} 🔒".format(item["umbral"]) size int(15 * _k) color _col_numero xalign 1.0 yalign 0.5
                else:
                    text "{}".format(item["umbral"]) size int(15 * _k) color _col_numero xalign 0.5 yalign 0.5


################################################################################
## Rótulo "Ventajas" — encabeza la lista de ventajas de un hito
################################################################################
## Indentado un nivel (cuelga del hito) y hovereable: explica qué es una ventaja
## en general, mientras que cada ventaja de abajo explica lo suyo.

screen _desb_rotulo_ventajas(bloqueado):
    $ _col_r = "#6a6a80" if bloqueado else "#9aa8c0"
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    $ _sangria_r = int(32 * _k)
    $ _avail_r   = max(int(80 * _k), _desb_ancho_util(_k) - _sangria_r)
    $ _txt_r     = renpy.translate_string(DESB_TXT_VENTAJAS)

    button:
        xfill True
        background None
        hover_background "#ffffff08"
        padding (int(4 * _k), int(3 * _k))
        action [SetVariable("_rel_hover_desc", _txt_r), CaptureFocus(DESB_FOCO_POPUP)]
        hovered [SetVariable("_rel_hover_desc", _txt_r), CaptureFocus(DESB_FOCO_POPUP)]
        unhovered SetVariable("_rel_hover_desc", None)

        hbox:
            spacing 0
            null width _sangria_r
            frame:
                xsize _avail_r
                background None
                padding (0, 0)
                text renpy.translate_string("Ventajas") size int(15 * _k) color _col_r bold True yalign 0.5


################################################################################
## Fila de una ventaja (hija de un hito)
################################################################################

screen _desb_fila_ventaja(ventaja, bloqueado, npc_id="violet"):
    $ _col_v = "#5a5a6e" if bloqueado else "#b8c4d8"
    $ _k = CEL_APP_ESCALA_SMALL if renpy.variant("small") else 1.0

    ## El ojo solo existe si esa ventaja tiene contenido registrado para ESTE
    ## NPC (core/hitos/ventajas_contenido.rpy). Asi el panel no conoce ninguna
    ## ventaja por nombre: una que no tenga catalogo simplemente no lo muestra.
    ##
    ## Tambien se esconde con el hito bloqueado: la lista de adentro es un
    ## premio de haber llegado, no un catalogo de lo que te falta.
    $ _ojo_v = (not bloqueado) and ventaja_tiene_contenido(ventaja["id"], npc_id)

    ## Sangria de segundo nivel: las ventajas cuelgan del rotulo "Ventajas",
    ## que a su vez cuelga del hito. El ancho restante sale de la MISMA cuenta
    ## que la fila del hito, menos la sangria y el hueco de la viñeta. Con ojo
    ## se descuenta ademas su columna, o el nombre lo empujaria fuera del ancho.
    $ _sangria_v = int(48 * _k)
    $ _vineta_v  = int(18 * _k)
    $ _ojo_w     = int(34 * _k) if _ojo_v else 0
    $ _avail_v   = max(int(80 * _k), _desb_ancho_util(_k) - _sangria_v - _vineta_v - _ojo_w)

    ## El texto del cuadro se arma ACA y no dentro del button: un `$` en medio
    ## del bloque convierte en no-constantes a los argumentos que vienen
    ## despues, y Ren'Py rechaza la screen al compilarla.
    $ _txt_v = renpy.translate_string(DESB_TXT_VENTAJA).format(ventaja["desc"])

    ## El ojo va HERMANO del boton de la descripcion, no adentro: Ren'Py no
    ## admite botones anidados —el de afuera se come el click del de adentro—,
    ## asi que los dos cuelgan de este hbox y cada uno atiende lo suyo.
    hbox:
        xfill True
        spacing 0

        button:
            xsize (_desb_ancho_util(_k) - _ojo_w)
            background None
            hover_background "#ffffff08"
            padding (int(4 * _k), int(3 * _k))
            # LAS DOS COSAS a proposito:
            #  - hovered/unhovered → en PC la descripcion sigue al mouse.
            #  - action            → en tactil no hay hover; el toque es la unica
            #                        via, y fija la descripcion hasta tocar otra.
            # En PC el action no molesta: el hover ya la habia mostrado.
            #
            # CaptureFocus guarda el rectangulo de ESTE boton bajo el nombre
            # DESB_FOCO_POPUP; el nearrect del cuadro lo lee para salir pegado.
            # No hace falta ClearFocus al salir: el cuadro solo se dibuja con
            # _rel_hover_desc puesto, asi que un rectangulo viejo nunca se ve.
            action [SetVariable("_rel_hover_desc", _txt_v), CaptureFocus(DESB_FOCO_POPUP)]
            hovered [SetVariable("_rel_hover_desc", _txt_v), CaptureFocus(DESB_FOCO_POPUP)]
            unhovered SetVariable("_rel_hover_desc", None)

            hbox:
                spacing 0

                # Sangria con un null y no con padding: en un frame el padding
                # pinta fondo y se veria un escalon de color.
                null width _sangria_v

                frame:
                    xsize _vineta_v
                    background None
                    padding (0, 0)
                    text DESB_VINETA size int(14 * _k) color _col_v yalign 0.5

                frame:
                    xsize _avail_v
                    background None
                    padding (int(4 * _k), 0)
                    text ventaja["nombre"] size int(16 * _k) color _col_v yalign 0.5

        # Abre la subapp con la lista de situaciones de esta ventaja.
        if _ojo_v:
            button:
                xsize _ojo_w
                background None
                hover_background "#ffffff14"
                padding (int(4 * _k), int(3 * _k))
                action [Hide("panel_desbloqueos"),
                        Show("panel_contenido_ventaja",
                             npc_id=npc_id, ventaja_id=ventaja["id"])]
                text u"👁️" size int(15 * _k) xalign 0.5 yalign 0.5
