################################################################################
## Minijuego "misionero" — la escena de sexo del final de amor 50
################################################################################
##     archivo   minijuego_misionero.rpy
##     entrada   `call minijuego_misionero` (subrutina: termina en negro y
##               devuelve al que llamo, que sigue con la escena siguiente)
##     testeo    menu de cheats, seccion MINIJUEGOS → minijuego_misionero_test
##     assets    game/images/minijuegos/misionero/
##
## Lo llama `violet_amor_50_cama` (violet_amor_50.rpy), que sigue desde negro
## con la escena de despues. Los cheats lo abren suelto para probarlo.
##
## Mismo esquema que el minijuego de la quest 09 (violet_quest_09_minijuego.rpy,
## PATRON E del skill de contenido): la screen se muestra UNA vez y no se baja,
## el label da vueltas en `ui.interact()`, y los dialogos corren por encima con
## los botones apagados (`mis_hablando`).
##
## LAS FASES (mis_fase):
##
##   "ropa"    fondo_inicial con corpiño y tanga. La mano es el cursor: el
##             primer toque en una prenda se la saca (fundido) y cada toque es
##             un gemido. La zona de la prenda sigue clickeable aunque ya no
##             este. Con las dos fuera se habilita el boton ❤️ Sexo.
##   "sexo"    la animacion (pene, piernas, pecho). El jugador sube y baja la
##             velocidad; cada subida es un gemido con los ojos cerrados 1 s. En
##             la velocidad maxima aparece 💧 Acabar (y no hay boton de salir).
##   "fuerte"  estocadas de salida lenta y entrada de golpe, con tres gemidos
##             cada vez mas fuertes y el gemido grande.
##   "final"   el pene se queda adentro con movimientos cortos + sacudidas, y
##             fundido a negro.
##
## LAS CAPAS de la pose de sexo, de abajo hacia arriba (el orden del .psd):
##     fondo_pose2 → piernas → pene → pecho → vagina → cara
##
## piernas_nuevas trae tambien la panza, y se superpone con pecho_nuevo en
## y 639-755: por eso el pecho va arriba de las piernas. Encima del pecho solo
## va la vagina (se tocan en y 729-775, como en el .psd); con el pene no se toca.
##
## LA CARA (boca + ojos) es la misma en las dos poses y se dibuja arriba de
## todo. Son imagenes de 1920x1080 que caen solas en su lugar.


################################################################################
## Los assets
################################################################################
## Por RUTA EXPLICITA y con prefijo `mis_`: Ren'Py define solo las imagenes de
## images/ por NOMBRE DE ARCHIVO, sin mirar la carpeta, y "tanga", "pene" o
## "boca_hablando" son nombres que otra escena puede repetir.

image mis_fondo_inicial = "images/minijuegos/misionero/fondo_inicial.jpg"
image mis_corpino = "images/minijuegos/misionero/corpino.webp"
image mis_tanga = "images/minijuegos/misionero/tanga.webp"

image mis_fondo = "images/minijuegos/misionero/fondo_pose2.jpg"
image mis_pecho = "images/minijuegos/misionero/pecho_nuevo.webp"
image mis_piernas = "images/minijuegos/misionero/piernas_nuevas.webp"
image mis_pene = "images/minijuegos/misionero/pene.webp"
image mis_vagina = "images/minijuegos/misionero/vagina.webp"

image mis_boca_hablando = "images/minijuegos/misionero/boca_hablando.webp"
image mis_boca_gemido = "images/minijuegos/misionero/boca_gemido.webp"
image mis_ojos_cerrados = "images/minijuegos/misionero/ojos_cerrados.webp"


################################################################################
## Tiempos
################################################################################

# ── Fase sexo: las tres capas al MISMO ritmo, tramo a tramo ──────────────────
#
#                 pene                 piernas              pecho
#   1. TRAMO      baja                 base → arriba        base → pecho
#   2. PAUSA      quieto abajo         quietas arriba       quieto
#   3. TRAMO      sube                 arriba → base        pecho → base
#   4. PAUSA      quieto arriba        quietas en la base   quieto en la base
#
# El pene hace el primer ciclo solo; piernas y pecho arrancan cuando lo
# completa. Se sincroniza POR TIEMPOS: las tres arrancan juntas con la screen y
# tienen tramos del mismo largo, asi que no se desfasan.

# Donde arranca el pene (y donde se detiene arriba, lo mas profundo), en pixeles
# respecto de donde lo deja el asset. Negativo = mas arriba.
define MIS_PENE_INICIO = -15

# Cuanto baja desde ahi (y despues vuelve a subir lo mismo).
define MIS_PENE_RECORRIDO = 40

# Lo que dura cada tramo (el pene bajando o subiendo, cada fundido de piernas y
# pecho). UNO solo para las tres capas: si cada una tuviera el suyo, dejarian de
# coincidir.
define MIS_TRAMO = 1.0

# Quieto entre un tramo y el siguiente.
define MIS_PAUSA_CAMBIO = 0.3

# Factor sobre la DURACION: mas chico = mas rapido.
define MIS_VELOCIDADES = {
    -1: (1.6, "Lento"),
    0: (1.0, "Normal"),
    1: (0.7, "Rápido"),
    2: (0.45, "Muy rápido"),
}
define MIS_VEL_MIN = -1
define MIS_VEL_MAX = 2

# Lo que dura el gemido de cada subida de velocidad (ojos cerrados incluidos).
define MIS_GEMIDO_VELOCIDAD = 1.0

# ── Fase fuerte: salida lenta, entrada de golpe, un segundo adentro ──────────
define MIS_FUERTE_SALIDA = 1.2
define MIS_FUERTE_ENTRADA = 0.15
define MIS_FUERTE_ADENTRO = 1.0

# Piernas y pecho, en la fase fuerte: aparecen con el golpe (en lo que dura la
# entrada) y se van con este fundido al final del segundo adentro.
define MIS_FUERTE_FUNDIDO_SALIDA = 0.5

# Una estocada entera. Es lo que dura cada uno de los tres gemidos, para que
# cada uno caiga en su golpe.
define MIS_CICLO_FUERTE = MIS_FUERTE_SALIDA + MIS_FUERTE_ENTRADA + MIS_FUERTE_ADENTRO

# ── Fase final: el pene adentro, con movimientos cortos ──────────────────────
define MIS_FINAL_MOVIMIENTO = 5          # pixeles hacia atras
define MIS_FINAL_TRAMO = 0.12           # segundos de cada ida o vuelta
define MIS_FINAL_ESPERA = 2.0           # lo que se ve antes del fundido a negro

# ── La mano como cursor ──────────────────────────────────────────────────────
# La misma del minijuego de la quest 09 (la que no tiene toalla), DERECHA y al
# DOBLE de tamaño (alla va rotada 45° y a 0.17).
define MIS_MANO = "images/quest/violet/quest9/mano_base.webp"
define MIS_MANO_ZOOM = 0.34

# Donde cae el click dentro de la imagen: la punta del dedo mayor (medido sobre
# el asset de 700x1065: x 355, y 80). Sin rotacion no hace falta compensar el
# lienzo agrandado, como en la quest 09.
define MIS_MANO_ANCLA = (0.5, 0.08)


################################################################################
## Estado
################################################################################
## Todo se reinicia en mis_reiniciar(), al entrar: el minijuego se puede jugar
## mas de una vez (el testeo, o un replay algun dia).

# "ropa" | "sexo" | "fuerte" | "final"
default mis_fase = "ropa"

default mis_corpino_fuera = False
default mis_tanga_fuera = False

# Velocidad de la fase sexo: clave de MIS_VELOCIDADES.
default mis_vel = 0

# La cara: "none" | "hablando" | "gemido", y "none" | "cerrados".
default mis_boca = "none"
default mis_ojos = "none"

# True mientras corre un dialogo: la screen sigue en pantalla pero sin botones.
default mis_hablando = False


init python:

    def mis_reiniciar():
        """Deja el minijuego como al empezar."""
        store.mis_fase = "ropa"
        store.mis_corpino_fuera = False
        store.mis_tanga_fuera = False
        store.mis_vel = 0
        store.mis_boca = "none"
        store.mis_ojos = "none"
        store.mis_hablando = False

    def mis_ropa_fuera():
        return store.mis_corpino_fuera and store.mis_tanga_fuera

    def _mis_seguir_mouse(trans, st, at):
        """
        Pone la mano en la posicion del mouse, cada frame. Hace falta aunque se
        use config.mouse_displayable: Ren'Py lo agrega al root en (0, 0) y NO
        lo mueve (ver _vq9_seguir_mouse, quest 09).
        """
        _p = renpy.get_mouse_pos()
        if _p:
            trans.xpos, trans.ypos = _p
        return 0

    def mis_cursor_mano():
        """
        La mano pasa a ser el cursor. Como en la quest 09: no corre si el
        jugador tiene activada la preferencia "cursor del sistema".
        """
        config.mouse_displayable = Transform(
            MIS_MANO,
            zoom=MIS_MANO_ZOOM,
            anchor=MIS_MANO_ANCLA,
            function=_mis_seguir_mouse,
        )

    def mis_cursor_normal():
        config.mouse_displayable = None


################################################################################
## Las animaciones
################################################################################

# ⚠️ CADA `with Dissolve` VA SEGUIDO DE UN `pause` DEL MISMO LARGO. En el ATL el
# cambio de imagen NO espera a que termine el fundido (renpy/atl.py, clase
# Child: devuelve "next" en el acto) — sin la pausa, el siguiente cambio pisa al
# anterior a mitad de camino.
#
# "Base" es no mostrar nada encima (`Null()`): la pose de base ya viene dibujada
# en el fondo. El primer hijo de un ATL se pone sin transicion.
#
# ⚠️ Todas van con `add ... at transform(...)`. Con `at`, cuando la screen se
# vuelve a evaluar Ren'Py le pasa al transform nuevo el reloj del viejo; un
# `add transform(...)` directo puede arrancar de cero y quedar corrido del pene.
# Lo que SI las reinicia es cambiarles un parametro (la velocidad) o el
# transform (la fase): arrancan de nuevo, con el primer ciclo del pene solo.

# ── Fase sexo ────────────────────────────────────────────────────────────────

# El pene: baja, se detiene abajo, sube, se detiene arriba. `ease` desacelera
# al llegar a cada extremo, asi que la frenada no es de golpe.
transform mis_pene_mov(tramo, pausa):
    yoffset MIS_PENE_INICIO
    block:
        ease tramo yoffset MIS_PENE_INICIO + MIS_PENE_RECORRIDO
        pause pausa
        ease tramo yoffset MIS_PENE_INICIO
        pause pausa
        repeat

# Piernas y pecho son el mismo movimiento con otra imagen. El `pause` de afuera
# es el primer ciclo del pene, que esperan en la base.
transform mis_reaccion_mov(imagen, tramo, pausa):
    Null()
    pause 2 * (tramo + pausa)
    block:
        imagen with Dissolve(tramo)
        pause tramo
        pause pausa
        Null() with Dissolve(tramo)
        pause tramo
        pause pausa
        repeat

# ── Fase fuerte ──────────────────────────────────────────────────────────────

# Sale despacio, entra de golpe (`easein`: arranca rapido y frena al llegar) y
# se queda un segundo adentro.
transform mis_pene_fuerte():
    yoffset MIS_PENE_INICIO
    block:
        ease MIS_FUERTE_SALIDA yoffset MIS_PENE_INICIO + MIS_PENE_RECORRIDO
        easein MIS_FUERTE_ENTRADA yoffset MIS_PENE_INICIO
        pause MIS_FUERTE_ADENTRO
        repeat

# Piernas y pecho con el golpe: aparecen en lo que dura la entrada, se quedan
# y se van al final del segundo adentro. Mismo ciclo que el pene.
transform mis_reaccion_fuerte(imagen):
    Null()
    block:
        pause MIS_FUERTE_SALIDA
        imagen with Dissolve(MIS_FUERTE_ENTRADA)
        pause MIS_FUERTE_ENTRADA
        pause MIS_FUERTE_ADENTRO - MIS_FUERTE_FUNDIDO_SALIDA
        Null() with Dissolve(MIS_FUERTE_FUNDIDO_SALIDA)
        pause MIS_FUERTE_FUNDIDO_SALIDA
        repeat

# ── Fase final ───────────────────────────────────────────────────────────────

# Se queda en lo mas profundo y hace unos movimientos cortos atras y adelante.
transform mis_pene_final():
    yoffset MIS_PENE_INICIO
    block:
        ease MIS_FINAL_TRAMO yoffset MIS_PENE_INICIO + MIS_FINAL_MOVIMIENTO
        ease MIS_FINAL_TRAMO yoffset MIS_PENE_INICIO
        repeat 4

# ── Fase ropa ────────────────────────────────────────────────────────────────

# La prenda que se saca se va con un fundido. Lo dispara el `showif` de la
# screen cuando su condicion pasa a False.
transform mis_prenda():
    on show:
        alpha 1.0
    on hide:
        linear 0.5 alpha 0.0


################################################################################
## La escena — todo lo que se dibuja, sin botones
################################################################################

screen mis_escena():

    # zorder NEGATIVO: el textbox de Ren'Py vive en 0 y tiene que quedar arriba
    # (ver vq9_escena, quest 09).
    zorder -10

    if mis_fase == "ropa":
        add "mis_fondo_inicial"

        showif not mis_corpino_fuera:
            add "mis_corpino" at mis_prenda
        showif not mis_tanga_fuera:
            add "mis_tanga" at mis_prenda

    else:
        $ _mis_factor = MIS_VELOCIDADES[mis_vel][0]
        $ _mis_tramo = MIS_TRAMO * _mis_factor
        $ _mis_pausa = MIS_PAUSA_CAMBIO * _mis_factor

        add "mis_fondo"

        if mis_fase == "sexo":
            add Null() at mis_reaccion_mov("mis_piernas", _mis_tramo, _mis_pausa)
            add "mis_pene" at mis_pene_mov(_mis_tramo, _mis_pausa)
            add Null() at mis_reaccion_mov("mis_pecho", _mis_tramo, _mis_pausa)

        elif mis_fase == "fuerte":
            add Null() at mis_reaccion_fuerte("mis_piernas")
            add "mis_pene" at mis_pene_fuerte
            add Null() at mis_reaccion_fuerte("mis_pecho")

        else:
            # "final": piernas arriba y pecho quietos, el pene adentro.
            add "mis_piernas"
            add "mis_pene" at mis_pene_final
            add "mis_pecho"

        add "mis_vagina"

    # La cara, arriba de todo.
    if mis_boca == "hablando":
        add "mis_boca_hablando"
    elif mis_boca == "gemido":
        add "mis_boca_gemido"
    if mis_ojos == "cerrados":
        add "mis_ojos_cerrados"


################################################################################
## Screen jugable
################################################################################

style mis_boton is button:
    background "#1e1e3aCC"
    hover_background "#e08020"
    insensitive_background "#2a2a2a99"
    padding (18, 10)
    yalign 0.5

style mis_boton_text is button_text:
    size 26
    color "#ffffff"
    insensitive_color "#777777"
    yalign 0.5

screen mis_minijuego():

    # zorder NEGATIVO y SIN `modal True`, como en la quest 09: un modal se come
    # el click que hace avanzar el dialogo.
    zorder -5

    use mis_escena

    if not mis_hablando:

        if mis_fase == "ropa":

            # Las prendas: SIEMPRE clickeables, esten o no. Una vez fuera, el
            # toque sigue sacandole un gemido.
            #
            # `focus_mask` con la imagen de la prenda: son de 1920x1080, y sin
            # la mascara el boton seria la pantalla entera. Lo visible va con
            # alpha 0, pero la mascara mira la imagen real.
            imagebutton:
                idle Transform("mis_corpino", alpha=0.0)
                focus_mask "mis_corpino"
                action Return(("prenda", "corpino"))
            imagebutton:
                idle Transform("mis_tanga", alpha=0.0)
                focus_mask "mis_tanga"
                action Return(("prenda", "tanga"))

        # ── Barra de botones: ARRIBA, para que el textbox no la tape ─────────
        hbox:
            xalign 0.5
            ypos 20
            spacing 14

            if mis_fase == "ropa":

                # La mano es la unica herramienta: el boton queda marcado.
                textbutton "✋":
                    style "mis_boton"
                    background "#c66a00EE"
                    action NullAction()
                    text_size 34

                textbutton "👄":
                    style "mis_boton"
                    action Return(("proximamente", None))
                    text_size 34

                textbutton _("❤️ Sexo"):
                    style "mis_boton"
                    sensitive mis_ropa_fuera()
                    action Return(("sexo", None))

            elif mis_fase == "sexo":

                textbutton _("− Más lento"):
                    style "mis_boton"
                    sensitive mis_vel > MIS_VEL_MIN
                    action SetVariable("mis_vel", mis_vel - 1)

                text renpy.translate_string(MIS_VELOCIDADES[mis_vel][1]):
                    size 26
                    color "#FFD54F"
                    min_width 150
                    text_align 0.5
                    yalign 0.5

                textbutton _("+ Más rápido"):
                    style "mis_boton"
                    sensitive mis_vel < MIS_VEL_MAX
                    action Return(("mas", None))

                # Recien en la velocidad maxima. No hay boton de salir.
                if mis_vel == MIS_VEL_MAX:
                    null width 30
                    textbutton _("💧 Acabar"):
                        style "mis_boton"
                        background "#1565c0EE"
                        action Return(("acabar", None))


################################################################################
## Testeo — se entra desde el menu de cheats
################################################################################
## Es CONTENIDO (termina en game_loop): no devuelve a nadie.

label minijuego_misionero_test:

    # El menu de cheats vive dentro del celular: hay que bajar los dos.
    $ renpy.hide_screen("menu_cheats")
    $ renpy.hide_screen("menu_celular")
    $ menu_celular_abierto = False

    call minijuego_misionero from _call_mis_test

    # El minijuego termina en negro; aca se vuelve al juego.
    $ mostrar_hud()
    jump game_loop


################################################################################
## El minijuego
################################################################################
## SUBRUTINA: termina en negro con `return`, y el que lo llamo sigue con la
## escena siguiente.

label minijuego_misionero:

    $ ocultar_hud()
    $ mis_reiniciar()

    show screen mis_minijuego
    with fade

    # ── La charla de entrada ──────────────────────────────────────────────────
    $ mis_hablando = True
    window show

    mc "Esperé mucho esto"

    $ mis_boca = "hablando"
    violet "Yo también"
    $ mis_boca = "none"

    mc "Me muero de ganas de sacarte la ropa"

    $ mis_boca = "hablando"
    violet "Entonces hazlo"
    $ mis_boca = "none"

    window hide
    $ mis_hablando = False

    $ mis_cursor_mano()

    # ── El bucle ──────────────────────────────────────────────────────────────
    # Ver vq9_bucle (quest 09): la screen no se baja, `ui.interact()` devuelve lo
    # que puso el `Return` del boton apretado. Bajar la velocidad no necesita
    # dialogo: es SetVariable y no pasa por aca.

    $ _mis_jugando = True

    while _mis_jugando:

        $ _mis_res = ui.interact()
        $ _mis_tipo = _mis_res[0] if _mis_res else None
        $ _mis_dato = _mis_res[1] if _mis_res else None

        if _mis_tipo == "prenda":
            call mis_click_prenda(_mis_dato) from _call_mis_prenda

        elif _mis_tipo == "proximamente":
            call mis_proximamente from _call_mis_prox

        elif _mis_tipo == "sexo":
            $ mis_cursor_normal()
            $ mis_fase = "sexo"
            with dissolve

        elif _mis_tipo == "mas":
            call mis_mas_rapido from _call_mis_mas

        elif _mis_tipo == "acabar":
            $ _mis_jugando = False

    jump mis_final


################################################################################
## Handlers
################################################################################
## Todos se llaman desde el bucle y terminan en `return`.

label mis_hablar_inicio:
    $ mis_hablando = True
    window show
    return


label mis_hablar_fin:
    $ mis_hablando = False
    window hide
    return


# ── Una prenda ───────────────────────────────────────────────────────────────
# El primer toque la saca; los siguientes (la zona sigue viva) solo el gemido.

label mis_click_prenda(prenda):

    if prenda == "corpino":
        $ mis_corpino_fuera = True
    else:
        $ mis_tanga_fuera = True

    call mis_hablar_inicio from _call_mis_prenda_ini

    $ mis_boca = "gemido"
    violet "Mmmh..."
    $ mis_boca = "none"

    call mis_hablar_fin from _call_mis_prenda_fin
    return


label mis_proximamente:
    call mis_hablar_inicio from _call_mis_prox_ini
    "Este contenido se agregará en futuras actualizaciones"
    call mis_hablar_fin from _call_mis_prox_fin
    return


# ── Subir la velocidad ───────────────────────────────────────────────────────
# El gemido dura MIS_GEMIDO_VELOCIDAD y pasa solo (`{w}` + `{nw}`): es una
# reaccion, no algo para leer. Los ojos se cierran lo mismo.
#
# Cambiar la velocidad reinicia la animacion (ver la nota de los transforms).

label mis_mas_rapido:

    $ mis_vel = min(mis_vel + 1, MIS_VEL_MAX)

    call mis_hablar_inicio from _call_mis_mas_ini

    $ mis_boca = "gemido"
    $ mis_ojos = "cerrados"
    violet "Ahh...{w=[MIS_GEMIDO_VELOCIDAD]}{nw}"
    $ mis_boca = "none"
    $ mis_ojos = "none"

    call mis_hablar_fin from _call_mis_mas_fin
    return


################################################################################
## El final
################################################################################

label mis_final:

    $ mis_hablando = True
    window show

    # Cierra los ojos y la boca de gemido se queda. Habla con la boca abierta
    # y vuelve al gemido.
    $ mis_ojos = "cerrados"
    $ mis_boca = "gemido"

    mc "Voy a acabar"

    $ mis_boca = "hablando"
    violet "Un poco más y yo también"
    $ mis_boca = "gemido"

    # ── Las estocadas fuertes ─────────────────────────────────────────────────
    # La fase cambia y la animacion arranca con la salida. El primer gemido cae
    # en el primer golpe (salida + entrada) y cada uno dura una estocada entera,
    # asi que los siguientes caen cada uno en el suyo.
    #
    # Son `{w}` y no esperan el click: un click los adelanta y el gemido deja de
    # coincidir con el golpe. En una prueba no importa; si molesta, se pasa a
    # renpy.pause(hard=True).
    $ mis_fase = "fuerte"
    $ renpy.pause(MIS_FUERTE_SALIDA + MIS_FUERTE_ENTRADA, hard=True)

    violet "Ah...{w=[MIS_CICLO_FUERTE]}{nw}"
    violet "{size=+8}¡Ah!{/size}{w=[MIS_CICLO_FUERTE]}{nw}"
    violet "{size=+16}¡Aaah!{/size}{w=[MIS_CICLO_FUERTE]}{nw}"

    mc "Me está apretando un montón"
    mc "No aguanto más Violet"

    violet "{size=+26}¡¡Aaaaaah!!{/size}"

    # ── Adentro ───────────────────────────────────────────────────────────────
    window hide
    $ mis_fase = "final"
    with vpunch
    with hpunch
    $ renpy.pause(MIS_FINAL_ESPERA, hard=True)

    # ── Cierre ────────────────────────────────────────────────────────────────
    # El negro y el bajado de la screen en UNA sola transicion: asi no se ve la
    # capa master de abajo (ver vq9_cierre, quest 09).
    $ mis_cursor_normal()
    $ mis_hablando = False
    scene black
    hide screen mis_minijuego
    with fade

    return
