
################################################################################
## FLAG DE MODO DESARROLLO
## True  = herramientas de dev disponibles (debug panel, tecla P, etc.)
## False = todo el sistema dev desactivado (versión jugable final)
################################################################################
default MODO_DEV = False


################################################################################
## ENLACES EXTERNOS
################################################################################
## Van acá y no inline en la pantalla que los usa porque quedan CONGELADOS en
## cada build: el jugador que descargó una version vieja se queda con la URL de
## esa version para siempre, y no hay parche que lo alcance.
##
## La invitacion de Discord esta creada con caducidad "Nunca" y usos ilimitados
## (por defecto Discord las vence a los 30 dias). Aun asi sigue siendo un punto
## unico de falla: si algun dia se revoca o cambia el servidor, lo ideal es que
## esto apunte a un redirect propio (itch, dominio corto) en vez de a discord.gg
## directo — asi se actualiza el destino sin sacar build nuevo.
define JP_URL_DISCORD = "https://discord.gg/XHeUH3FXqf"

default mc_name = ""

# Color del MC. Va como constante y con prioridad -10 porque lo usan dos
# archivos distintos: el `mc` de acá abajo y el `piensa` de sprites_mc.rpy.
# Asi el nombre del MC y el de su pensamiento no se pueden desfasar.
define -10 MC_COLOR = "#56b6c2"

define mc = Character("[mc_name]", color=MC_COLOR)


################################################################################
## PENSAMIENTOS — estilo compartido
################################################################################
## Todo pensamiento del juego (el del MC y el de cada NPC) sale igual: el TEXTO
## en blanco e italica entre comillas, y el nombre tal cual, con el color propio
## del personaje — el pensamiento no es otro personaje, es el mismo hablando
## para adentro.
##
## El texto va BLANCO, igual que el dialogo normal. Estuvo un tiempo en gris
## (#AAAAAA y despues #B4B4B4) y se descarto: el gris se lee como "esto esta
## apagado / deshabilitado" y no como "esto es un pensamiento". Lo que tiene que
## distinguir al pensamiento son las comillas y la italica, no la intensidad.
##
## OJO CON LOS DOS PARAMETROS DE COLOR: `color` es el del NOMBRE y `what_color`
## el del TEXTO. Acá va solo `what_color`; el `color` lo pasa cada personaje al
## heredar, o le borrariamos el suyo.
##
## Cada personaje hereda de acá con `kind=`, que es el mecanismo de Ren'Py para
## exactamente esto: una sola definicion del estilo y una linea por personaje.
## Cambiar el color o sacar las comillas se hace UNA vez, acá.
##
##     define violet_piensa = Character("Violet", kind=piensa_base,
##                                      color=VIOLET_COLOR)
##
## Va con prioridad -10 para que exista antes que los `define` de los personajes
## (que corren en prioridad 0, y el orden entre archivos no esta garantizado).
##
## SOBRE LA ITALICA: el proyecto trae el par completo de Roboto —
## Roboto-Bold.ttf (familia Roboto, estilo Bold) y Roboto-BoldItalic.ttf
## (familia Roboto, estilo Bold Italic). El mapeo de abajo hace que `what_italic`
## use el archivo italic REAL.
##
## Sin ese mapeo Ren'Py sintetiza la italica inclinando los glifos del Bold, que
## es lo que habia antes: se notaba poco y quedaba sucia, porque una inclinacion
## mecanica no dibuja las formas propias de la cursiva (en Roboto la `a` y la `e`
## cambian de forma, no solo de angulo).

init python:

    # Cuando alguien pide Roboto-Bold en italica, usar el archivo italic real.
    # La clave es (fuente, bold, italic) y el valor tambien.
    #
    # LOS DOS FLAGS DEL DESTINO SON DISTINTOS, Y A PROPOSITO:
    #
    #   bold=False   el archivo YA es bold. En True, Ren'Py le engrosaria los
    #                trazos encima y el pensamiento saldria mas pesado que el
    #                dialogo normal.
    #
    #   italic=True  el archivo YA es italic, pero aca SI queremos el extra:
    #                Ren'Py le suma su inclinacion sintetica ARRIBA de la cursiva
    #                real. Las dos cosas se acumulan y la italica queda mas
    #                marcada, que es el efecto buscado.
    #                Es un valor fijo del motor y no hay forma de graduarlo: si
    #                resulta excesivo se pone en False y queda solo la cursiva
    #                del archivo, que ya de por si es una italica de verdad.
    #
    # No hay recursion: get_font hace UN solo lookup en el mapa
    # (renpy/text/font.py:712), asi que el destino no se vuelve a mapear.
    #
    # Se registran las dos variantes de `bold` en la CLAVE porque el estilo del
    # dialogo no pide bold (la negrita viene del archivo) pero algunos textos de
    # HUD si.
    for _bold in (False, True):
        config.font_replacement_map["fonts/Roboto-Bold.ttf", _bold, True] = (
            "fonts/Roboto-BoldItalic.ttf", False, True)

define -10 piensa_base = Character(
    None,
    # Blanco, el mismo que gui.text_color: el pensamiento se distingue por las
    # comillas y la italica, no por ser mas tenue.
    what_color="#FFFFFF",
    what_italic=True,
    what_prefix="«",
    what_suffix="»",
)


################################################################################
## El character `tutorial` y su plano oscuro
################################################################################
## Antes de cada linea de tutorial entra un plano negro al 75% que baja el fondo
## y los personajes, para que el texto resalte.
##
## VA EN LA CAPA DE SCREENS Y NO EN LA DE IMAGENES: asi tapa de una todo lo que
## haya puesto `scene` y `show` —fondo y sprites— sin tener que enumerar nada ni
## acordarse de apagarlo.
##
## CON zorder -1 QUEDA DEBAJO DEL CUADRO DE TEXTO Y DEL HUD (los dos en 0). Que
## el HUD NO se oscurezca es a proposito: varios tutoriales justamente señalan
## sus botones ("haz click en el botón central de la parte superior"), y
## atenuar lo que se esta señalando seria contraproducente.
##
## SE MUESTRA TRANSIENT, igual que la screen `say`: Ren'Py lo saca solo al
## terminar la interaccion. Por eso el callback solo se ocupa del "begin" — no
## hay que apagarlo a mano, y entre dos lineas seguidas de tutorial no parpadea
## porque no se dibuja ningun frame en el medio.

screen tutorial_oscurecer():
    zorder -1
    add Solid("#000000") alpha 0.75


# El callback va en un init ANTERIOR al `define`: Character() resuelve el nombre
# en el momento de definirse, asi que la funcion ya tiene que existir.
init -20 python:

    def _tutorial_oscurecer(event, **kwargs):
        """Callback del character `tutorial`: planta el plano al empezar la linea."""
        if event == "begin":
            renpy.show_screen("tutorial_oscurecer", _transient=True)


# what_size fijo en 33 ignora el bump de gui.text_size que aplica en pantalla
# chica (ver @gui.variant small() en gui.rpy) — por eso el texto del tutorial
# se veía chico ahi. Se lo hace seguir al mismo tamaño que el diálogo general.
define tutorial = Character("Tutorial", color="#FFB74D", what_size=(gui.text_size if renpy.variant("small") else 33), what_text_align=0.5, callback=_tutorial_oscurecer)


init python:

    # Sacar la rueda del mouse de rollback/rollforward. Ren'Py la asigna por
    # defecto (rueda arriba = atrás, rueda abajo = adelante), lo que hace que
    # el jugador retroceda/avance el diálogo sin querer al scrollear.
    # El scroll de los viewports usa viewport_wheelup/viewport_wheeldown, que
    # son entradas distintas del keymap y NO se tocan: sigue funcionando.
    if "mousedown_4" in config.keymap.get("rollback", []):
        config.keymap["rollback"].remove("mousedown_4")
    if "mousedown_5" in config.keymap.get("rollforward", []):
        config.keymap["rollforward"].remove("mousedown_5")

    # Asignación incondicional (sin el "if ... is None") pisaba el toggle del
    # cheat "Ver resultados Talk" en cada arranque/reload — persistent debe
    # sembrarse una sola vez, no reescribirse siempre.
    if persistent.mostrar_recompensa is None:
        persistent.mostrar_recompensa = False

    import re as _re_nombre

    _LETRAS_PERMITIDAS_NOMBRE = (
        u"abcdefghijklmnopqrstuvwxyz"
        u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        u" "
        u"áéíóúüñÁÉÍÓÚÜÑàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛäëïöÄËÏÖ"
    )

    def _nombre_mc_valido(nombre):
        s = nombre.strip()
        if not s:
            return True
        return bool(_re_nombre.match(r'^[a-zA-ZÀ-ÿ\s]+$', s))


screen name_input_screen(nombre_previo=u"", error_msg=u""):

    default name = nombre_previo
    default name_iv = ScreenVariableInputValue("name", returnable=True)

    modal True

    add "gui/overlay/confirm.png"

    frame:
        style "name_input_frame"

        # El estilo "confirm_frame" centra con yalign 0.5, pero en táctil el
        # teclado (anclado abajo, JP_TECLADO_ALTO + margen) ocupa esa zona.
        # Se reubica el panel por encima del teclado, igual que el screen
        # "input" en teclado_tactil.rpy. Solo aplica a small; en PC no cambia.
        if renpy.variant("small"):
            yanchor 1.0
            ypos (config.screen_height - JP_TECLADO_ALTO - JP_TECLADO_MARGEN)

        vbox:
            xalign 0.5
            spacing 18

            label _("Ingresa el nombre del personaje"):
                style "name_input_title"
                xalign 0.5

            text _("Nombre por defecto: Mc"):
                xalign 0.5
                size 22
                color "#AAAAAA"

            null height 10

            frame:
                xalign 0.5
                xsize 480
                background "#111111CC"
                padding (18, 12, 18, 12)

                input:
                    value name_iv
                    length 20
                    allow _LETRAS_PERMITIDAS_NOMBRE
                    size 28
                    color "#FFFFFF"

            if error_msg:
                text error_msg:
                    xalign 0.5
                    size 20
                    color "#FF5252"
                    xmaximum 520
                    textalign 0.5
                    layout "subtitle"
            else:
                null height 28

            null height 6

            textbutton _("Confirmar"):
                style "name_input_button"
                xalign 0.5
                action Return(name)


style name_input_frame is confirm_frame:
    xminimum 640
    padding (50, 44, 50, 44)

style name_input_title is gui_label

style name_input_title_text is gui_label_text:
    size 30
    color "#4FC3F7"
    outlines [(2, "#0288D180", 0, 0)]
    xalign 0.5

style name_input_button is confirm_button

style name_input_button_text is confirm_button_text:
    color "#FFFFFF"
    hover_color "#FFB74D"


# Variables del ingreso de nombre. Con `default` por la misma razón que
# `_jugar_intro` en intro_main.rpy: si el `renpy.call_screen` que asigna
# `_nc_nombre` crashea y el jugador toca "Continuar", la ejecución sigue sin que
# la variable exista y la línea siguiente (`_nc_nombre.strip()`) revienta con
# NameError. Con "" el flujo termina en `mc_name = "Mc"`, que ya es el fallback
# previsto para cuando no se escribe nada.
default _nc_nombre = u""
default _nc_previo = u""
default _nc_error = u""


label choose_name:

    $ _nc_previo = u""
    $ _nc_error = u""

    label .loop:

        $ _nc_nombre = renpy.call_screen(
            "name_input_screen",
            nombre_previo=_nc_previo,
            error_msg=_nc_error
        )
        $ _nc_nombre = _nc_nombre.strip() if _nc_nombre else u""

        if _nc_nombre and not _nombre_mc_valido(_nc_nombre):
            $ _nc_previo = _nc_nombre
            $ _nc_error = _("El nombre no puede contener números ni caracteres especiales")
            jump .loop

        $ mc_name = _nc_nombre if _nc_nombre else u"Mc"

        if mc_name == "alanhhdev":
            $ MODO_DEV = True
            $ mc_name = "Dev"

    return
