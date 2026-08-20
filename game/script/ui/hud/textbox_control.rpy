################################################################################
## Controlador del cuadro de texto — opacidad y visibilidad
################################################################################
## Tres botones sobre el borde superior derecho del cuadro de texto:
##
##     −   baja la opacidad del FONDO
##     +   la sube
##     👁  oculta / muestra el cuadro
##
## TODO lo configurable vive en los `define` de abajo: rango de opacidad, paso,
## tamaño de los botones, margen y colores. La screen no tiene ni un numero
## suelto, asi que cambiar el comportamiento no obliga a tocar la maquinaria.
##
## ENGANCHE CON EL JUEGO — dos lineas en `screen say` (ui/base/screens.rpy):
##
##     window:
##         id "window"
##         background jp_tb_fondo()          <- opacidad y ocultado
##     ...
##     use jp_textbox_controles()            <- los botones
##
##
## POR QUE LA OPACIDAD VA EN EL `background` Y NO EN UN Transform DEL `window`:
## un Transform con alpha atenua TODO lo que envuelve, texto incluido, y el
## texto atenuado se vuelve ilegible justo cuando lo que se quiere es ver mejor
## la pantalla. Tocando solo el fondo, el dialogo se sigue leyendo igual con el
## cuadro al 30%.
##
## El fondo se toma del propio estilo (style.window.background) en vez de
## repetir el color acá: la variante `small` usa una imagen y no un color, y
## Transform funciona igual con las dos.
##
##
## OCULTAR ES MOMENTANEO: dura hasta la proxima linea de dialogo. Es para
## despejar la pantalla y mirar algo puntual, no un modo. Si quedara pegado, el
## jugador se perderia texto sin darse cuenta. Lo restaura un callback de
## personaje en el evento "begin", que Ren'Py dispara en cada linea.
##
## Por eso la opacidad es `persistent` (preferencia, sobrevive a todo) pero el
## ocultado es una variable comun que se resetea sola.


################################################################################
## Parametros
################################################################################

# Rango de opacidad del fondo y salto de cada click. 1.0 = el fondo tal cual lo
# define el estilo; 0.3 = un 30% de eso.
define JP_TB_ALPHA_MIN = 0.3
define JP_TB_ALPHA_MAX = 1.0
define JP_TB_ALPHA_PASO = 0.1

# Aspecto de los botones.
define JP_TB_BOTON_TAM = 40
define JP_TB_BOTON_SPACING = 8
define JP_TB_MARGEN_DERECHO = 30
define JP_TB_ESCALA_SMALL = 1.7

define JP_TB_COLOR_FONDO = "#1e1e3aEE"
define JP_TB_COLOR_HOVER = "#2a2a60EE"
define JP_TB_COLOR_OCULTO = "#7a3a3aEE"
define JP_TB_COLOR_TEXTO = "#ffffff"
define JP_TB_COLOR_TEXTO_OFF = "#666677"

# Fondo del cuadro, DUPLICADO A PROPOSITO de `style window` (ui/base/screens.rpy).
#
# Antes esto leia style.window.background y le aplicaba un Transform con alpha.
# No funciono: un Transform como `background` de un `window` no se dibuja, y el
# resultado era que al tocar +/− el fondo desaparecia del todo en vez de
# atenuarse. Con el color explicito se arma el string "#rrggbbaa" a mano, que es
# lo que un window espera y renderiza siempre igual.
#
# ⚠️ Si cambia el color del cuadro en `style window`, hay que cambiarlo acá.
define JP_TB_FONDO_COLOR = "#1a1a1a"

# Opacidad del fondo cuando el control esta al 100%. Es el "CC" del estilo
# original (204/255 = 0.8): al maximo el cuadro se ve exactamente como antes de
# que existiera este sistema.
define JP_TB_FONDO_ALPHA_BASE = 0.8

# La variante tactil usa una imagen y no un color, asi que ahi si va por
# Transform — no hay un hex que atenuar.
define JP_TB_FONDO_IMAGEN_SMALL = "gui/phone/textbox.png"


################################################################################
## Estado y logica
################################################################################

# Ocultado momentaneo. NO es persistent: se apaga solo en la proxima linea.
default jp_tb_oculto = False


init 1 python:

    # La opacidad se guarda como NIVEL entero, no como float: sumar 0.1 ocho
    # veces da 0.9999999 y los chequeos de "ya esta al maximo" fallarian.
    # El nivel 0 es el minimo y JP_TB_NIVELES el maximo.
    JP_TB_NIVELES = int(round((JP_TB_ALPHA_MAX - JP_TB_ALPHA_MIN) / JP_TB_ALPHA_PASO))

    if persistent.jp_tb_nivel is None:
        persistent.jp_tb_nivel = JP_TB_NIVELES      # arranca al 100%

    def jp_tb_alpha():
        """Opacidad elegida por el jugador, ignorando si esta oculto."""
        _n = min(JP_TB_NIVELES, max(0, persistent.jp_tb_nivel))
        return JP_TB_ALPHA_MIN + _n * JP_TB_ALPHA_PASO

    def jp_tb_fondo():
        """
        Fondo del cuadro con la opacidad aplicada. SOLO el fondo — el texto no
        pasa por acá y por eso se sigue leyendo igual al 30%.

        En PC devuelve un string "#rrggbbaa": es lo que un `window` espera como
        background y se dibuja siempre. En tactil el fondo es una imagen, asi
        que ahi no queda otra que envolverla en un Transform.
        """
        if renpy.variant("small"):
            return Transform(JP_TB_FONDO_IMAGEN_SMALL, alpha=jp_tb_alpha())

        _a = int(round(255 * JP_TB_FONDO_ALPHA_BASE * jp_tb_alpha()))
        return "{}{:02x}".format(JP_TB_FONDO_COLOR, max(0, min(255, _a)))

    def jp_tb_alpha_general():
        """
        Opacidad de TODO el cuadro (fondo, nombre y texto). Solo tiene dos
        valores: 1.0 normalmente y 0.0 con el cuadro oculto.

        Ocultar y bajar la opacidad son cosas distintas y por eso van por
        propiedades distintas: bajar la opacidad afecta al fondo, ocultar hace
        desaparecer todo. El `window` sigue existiendo en los dos casos — la
        screen `say` necesita SIEMPRE su widget de texto (id "what") para que
        el dialogo avance y se pueda cliquear.
        """
        return 0.0 if store.jp_tb_oculto else 1.0

    def jp_tb_porcentaje():
        """Opacidad del fondo como entero 30..100, para mostrarla."""
        return int(round(jp_tb_alpha() * 100))

    def jp_tb_puede_bajar():
        return not store.jp_tb_oculto and persistent.jp_tb_nivel > 0

    def jp_tb_puede_subir():
        return not store.jp_tb_oculto and persistent.jp_tb_nivel < JP_TB_NIVELES

    def jp_tb_cambiar(delta):
        """Mueve un nivel de opacidad, con tope en los dos extremos."""
        persistent.jp_tb_nivel = min(JP_TB_NIVELES,
                                     max(0, persistent.jp_tb_nivel + delta))
        renpy.restart_interaction()

    def jp_tb_toggle():
        """Oculta o vuelve a mostrar el cuadro (hasta la proxima linea)."""
        store.jp_tb_oculto = not store.jp_tb_oculto
        renpy.restart_interaction()

    def _jp_tb_callback_personaje(event, **kwargs):
        """
        Devuelve el cuadro en cada linea nueva.

        Se engancha en config.all_character_callbacks, que corre para TODOS los
        personajes (mc, violet, piensa, narrator...), asi que no hay que
        acordarse de nada al crear un Character nuevo.
        """
        if event == "begin" and store.jp_tb_oculto:
            store.jp_tb_oculto = False

    config.all_character_callbacks.append(_jp_tb_callback_personaje)


################################################################################
## Los botones
################################################################################
## Se ubican pegados al borde SUPERIOR del cuadro, contra la derecha: con
## yanchor 0.5 sobre ese borde, la mitad del boton queda afuera y la mitad
## adentro. La altura del cuadro se lee de gui.textbox_height en vez de fijarla,
## porque la variante `small` la agranda (278 → 360) y asi los botones la siguen
## sin tener que duplicar nada.

screen jp_textbox_controles():

    $ _tb_k = JP_TB_ESCALA_SMALL if renpy.variant("small") else 1.0
    $ _tb_tam = int(JP_TB_BOTON_TAM * _tb_k)
    $ _tb_borde_y = config.screen_height - gui.textbox_height

    hbox:
        xpos config.screen_width - int(JP_TB_MARGEN_DERECHO * _tb_k)
        xanchor 1.0
        ypos _tb_borde_y
        yanchor 0.5
        spacing int(JP_TB_BOTON_SPACING * _tb_k)

        # Bajar opacidad del fondo
        button:
            xysize (_tb_tam, _tb_tam)
            background JP_TB_COLOR_FONDO
            hover_background JP_TB_COLOR_HOVER
            # NullAction en vez de `sensitive False` al llegar al tope: un boton
            # insensible NO se queda con el click, se lo pasa a la screen `say`
            # de atras y el dialogo AVANZA. Con el nivel al maximo (que es como
            # arranca una partida) tocar "+" hacia desaparecer el mensaje.
            # El estado de tope se sigue viendo: el simbolo se pone gris.
            action (Function(jp_tb_cambiar, -1) if jp_tb_puede_bajar() else NullAction())
            text "−":
                xalign 0.5
                yalign 0.5
                size int(24 * _tb_k)
                color (JP_TB_COLOR_TEXTO if jp_tb_puede_bajar() else JP_TB_COLOR_TEXTO_OFF)

        # Subir opacidad del fondo
        button:
            xysize (_tb_tam, _tb_tam)
            background JP_TB_COLOR_FONDO
            hover_background JP_TB_COLOR_HOVER
            action (Function(jp_tb_cambiar, 1) if jp_tb_puede_subir() else NullAction())
            text "+":
                xalign 0.5
                yalign 0.5
                size int(24 * _tb_k)
                color (JP_TB_COLOR_TEXTO if jp_tb_puede_subir() else JP_TB_COLOR_TEXTO_OFF)

        # Ocultar / mostrar. El fondo del boton cambia cuando esta oculto: el
        # emoji es un bitmap y no respeta `color`, asi que el estado se marca
        # con el boton y no con el icono.
        button:
            xysize (_tb_tam, _tb_tam)
            background (JP_TB_COLOR_OCULTO if jp_tb_oculto else JP_TB_COLOR_FONDO)
            hover_background JP_TB_COLOR_HOVER
            action Function(jp_tb_toggle)
            text "👁️":
                xalign 0.5
                yalign 0.5
                size int(20 * _tb_k)
