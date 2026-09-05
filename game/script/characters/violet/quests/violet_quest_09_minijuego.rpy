################################################################################
## Quest 09 — Minijuego: secarle el sudor a Violet
################################################################################
##     archivo   violet_quest_09_minijuego.rpy
##     entra por violet_quest09b_secar (violet_quest_09_b.rpy)
##
## Violet esta acostada y transpirada. El jugador tiene DOS MANOS y con cada una
## hace algo distinto:
##
##     mano base    → saca la ropa y toca
##     mano toalla  → seca el sudor
##
## PARA TERMINAR hay que sacarle los ocho sudores. Cada uno aguanta tres toques:
## los dos primeros lo dejan mas transparente y el tercero lo borra. Y no se
## puede secar lo que esta tapado: primero hay que sacarle remera y pantalones.
##
## LO QUE SE DIBUJA, de abajo hacia arriba:
##     cama_fondo → los 8 sudores → tanga/remera/pantalones → colcha → cara
##
## NO ES UN LAYEREDIMAGE (salvo la cara). Los sudores necesitan ALPHA propio por
## pieza —33%, 66%, fuera— y un layeredimage no sabe hacer eso: sus atributos
## solo se prenden y se apagan. Asi que la escena se compone en la screen, con
## un `add` por pieza leyendo el estado.
##
## LAS POSICIONES DE LAS PIEZAS ESTAN EN VQ9_POS, mas abajo. Salen de la
## herramienta (tecla P → Assets), que exporta con el mismo anclaje que usa la
## screen: se pegan tal cual, sin convertir nada.
##
## LAS DOS ZONAS DE INTERACCION (pechos y pelvis) son imagenes que en el juego
## van INVISIBLES: solo aportan su rectangulo clickeable. Es el mismo recurso
## que usan los hotspots de locacion con imagen propia.


################################################################################
## Datos
################################################################################

init -1 python:

    VQ9_RUTA = "images/quest/violet/quest9/"

    # Los ocho sudores, en orden de dibujo. El id es la clave de todo el estado.
    VQ9_SUDORES = [
        "pelo", "cara", "brazoizquierdo", "brazoderecho",
        "piernaizquierda", "piernaderecha", "abdominal", "pechos",
    ]

    # Las tres prendas, de adentro hacia afuera.
    VQ9_ROPA = ["tanga", "remera", "pantalones"]

    # Que prendas tapan el cuerpo para secar. La tanga NO cuenta: se puede
    # secar con la tanga puesta, sacarla es otra cosa.
    VQ9_ROPA_TAPA = ["remera", "pantalones"]

    # Toques antes de que salte la conversacion de una zona.
    VQ9_TOQUES_PARA_CHARLA = 4

    # Sudores COMPLETAMENTE secos a partir de los cuales la cara en reposo pasa
    # de neutra a sonriendo: se va sintiendo mejor a medida que la secan.
    VQ9_SUDORES_PARA_SONRISA = 2

    # Toques en una zona intima a partir de los cuales se pone colorada. Se mide
    # sobre los pechos, o sobre la pelvis PERO solo los toques que ocurrieron
    # con la tanga ya fuera.
    VQ9_TOQUES_PARA_VERGUENZA = 3

    # Cuidado minimo (violet_enferma_atencion) para que la deje sacarle la tanga.
    VQ9_CUIDADO_PARA_TANGA = 3

    # Posiciones de cada pieza — top-left, xanchor 0.0 yanchor 0.0.
    #
    # Salen de la herramienta (tecla P → Assets) y se pegan tal cual: la
    # herramienta exporta con el mismo anclaje que usa la screen.
    #
    # La colcha y las piezas de la cara NO estan acá: son de 1920x1080 y caen
    # solas sobre la cama, no necesitan coordenada.
    VQ9_POS = {
        "sudor_pelo":            (159, 324),
        "sudor_cara":            (234, 425),
        "sudor_brazoizquierdo":  (514, 272),
        "sudor_brazoderecho":    (500, 610),
        "sudor_piernaizquierda": (907, 367),
        "sudor_piernaderecha":   (929, 540),
        "sudor_abdominal":       (686, 401),
        "sudor_pechos":          (447, 380),
        "ropa_tanga":            (833, 369),
        "ropa_remera":           (457, 304),
        "ropa_pantalones":       (798, 337),
        "pechos_interaccion":    (558, 393),
        "pelvis_interaccion":    (898, 440),
    }

    # La mano como cursor. El arte es de 700x1065, o sea un brazo entero: al
    # tamaño original tapa media pantalla.
    VQ9_MANO_ZOOM = 0.17

    # Donde cae el puntero dentro de la imagen del cursor.
    #
    # Centrado en X, y en Y al PRIMER CUARTO — a media altura entre el borde de
    # arriba y el centro. Es donde queda la punta de los dedos: con el anclaje
    # al centro (0.5) el click salia del medio del antebrazo y no de donde el
    # jugador ve que esta tocando.
    VQ9_MANO_ANCLA_X = 0.5
    VQ9_MANO_ANCLA_Y = 0.25

    # Giro de la mano, en grados. Positivo = horario.
    #
    # OJO CON EL ANCLA: al rotar, Ren'Py agranda el lienzo para que la imagen
    # entre entera (rotate_pad), asi que el 0.25 de arriba pasa a medirse sobre
    # ese lienzo mas grande y el punto de click se corre un poco. Si al probarlo
    # quedo desfasado, se compensa con VQ9_MANO_ANCLA_Y.
    VQ9_MANO_ROTACION = 45


################################################################################
## Estado
################################################################################

# "base" (saca ropa y toca) | "toalla" (seca)
default vq9_mano = "base"

# {id_sudor: toques}. Tres toques y la pieza se va.
default vq9_sudor_toques = {}

# Prendas que TODAVIA tiene puestas.
default vq9_ropa_puesta = ["tanga", "remera", "pantalones"]

# Ya vio la secuencia de "tenes la ropa mojada". Sirve para las dos manos: si la
# vio con la toalla, con la mano ya no se repite, y al reves.
default vq9_aviso_ropa = False

# Toques por zona. La tanga y las dos zonas de interaccion llevan su cuenta.
default vq9_toques_tanga = 0
default vq9_toques_pechos = 0
default vq9_toques_pelvis = 0

# Toques en la pelvis que ocurrieron CON LA TANGA YA FUERA. Va aparte de
# vq9_toques_pelvis porque la verguenza cuenta solo estos: tocarla tres veces
# por encima de la ropa no es lo mismo.
default vq9_toques_pelvis_desnuda = 0

# Violet dejo sacarle la tanga (se evalua una vez, al cuarto toque).
default vq9_tanga_permitida = False

# Botones grises que se van sumando arriba.
default vq9_boton_boca = False
default vq9_boton_victoria = False

# Ya seco los ocho sudores: aparece el boton de salir.
default vq9_completo = False

# La colcha esta puesta al entrar y se saca antes de jugar.
default vq9_colcha = True

# True mientras corre un dialogo. La screen sigue en pantalla —por eso no hay
# pestañeo— pero apaga sus botones: sin esto el jugador podria clickear un sudor
# mientras lee.
default vq9_hablando = False

# Atributos del layeredimage vq9_boca que tocan dibujar ahora, uno por grupo.
#
# La cara NO se muestra con `show`: eso la manda a la capa master, que queda
# DEBAJO de las screens — o sea tapada por la escena entera. Va como estado y la
# dibuja la screen, al final de todo para quedar por encima.
#
# Son TRES variables y no una porque los grupos son independientes: se puede
# estar hablando con cara de placer y colorada al mismo tiempo.
default vq9_boca_estado = "b_none"
default vq9_ojos_estado = "o_none"
default vq9_ot_estado = "ot_none"

# Copia de las entradas de config.mouse que pisa el minijuego, para poder
# devolverlas al salir.
default _vq9_cursor_previo = None


init python:

    def _vq9_img(nombre):
        """Path de una pieza del minijuego."""
        return VQ9_RUTA + nombre + (".jpg" if nombre.endswith("_interaccion")
                                    or nombre == "cama_fondo" else ".webp")

    def _vq9_pos(nombre):
        """Posicion top-left de una pieza, o (0, 0) si todavia no se acomodo."""
        return VQ9_POS.get(nombre, (0, 0))

    def _vq9_sudor_vivo(sid):
        """True si ese sudor todavia esta en pantalla."""
        return store.vq9_sudor_toques.get(sid, 0) < 3

    def _vq9_sudor_alpha(sid):
        """1.0 → 0.66 → 0.33 segun los toques que lleva."""
        return 1.0 - (store.vq9_sudor_toques.get(sid, 0) * 0.33)

    def _vq9_tapada():
        """True si todavia tiene encima algo que impide secar."""
        return any(_r in store.vq9_ropa_puesta for _r in VQ9_ROPA_TAPA)

    def _vq9_quedan_sudores():
        return any(_vq9_sudor_vivo(_s) for _s in VQ9_SUDORES)

    def _vq9_mano_actual():
        return _vq9_img("mano_toalla" if store.vq9_mano == "toalla" else "mano_base")

    def _vq9_mano_dyn(st, at):
        """
        Que imagen de mano toca ahora.

        Devuelve 0 y no 0.1: con una decima de retraso el jugador cambiaba de
        mano, hacia click enseguida y todavia veia la mano vieja dibujada.
        """
        return _vq9_mano_actual(), 0

    def _vq9_seguir_mouse(trans, st, at):
        """
        Pone el displayable en la posicion del mouse, cada frame.

        HACE FALTA aunque se use config.mouse_displayable: Ren'Py agrega ese
        displayable al root en (0, 0) y NO lo mueve (display/core.py:2666) —
        esconder el puntero y posicionar la imagen son dos cosas separadas, y
        solo se ocupa de la primera.

        Devuelve 0 para que lo vuelva a llamar en el frame siguiente.
        """
        _p = renpy.get_mouse_pos()
        if _p:
            trans.xpos, trans.ypos = _p
        return 0

    # ── Efectos de los clicks ────────────────────────────────────────────────

    def _vq9_secar(sid):
        """Un toque de toalla sobre un sudor."""
        store.vq9_sudor_toques[sid] = store.vq9_sudor_toques.get(sid, 0) + 1
        if not _vq9_quedan_sudores():
            store.vq9_completo = True

    def _vq9_cheat_cuidado(valor):
        """
        Fija el cuidado de la enfermedad desde el menu de cheats.

        Es lo que decide si Violet lo deja sacarle la tanga, y llegar a el
        jugando lleva tres dias — por eso se puede forzar.
        """
        store.violet_enferma_atencion = valor
        renpy.notify("Cuidado de Violet: {}".format(valor))

    # ── La cara ──────────────────────────────────────────────────────────────
    # Tres grupos que se combinan y NO se manejan igual:
    #
    #   boca   estado momentaneo — vuelve al reposo cuando termina de hablar,
    #          y ese reposo cambia solo (neutra → sonriendo) a medida que la
    #          secan.
    #   ojos   momentaneo, solo para el gemido.
    #   ot     PERMANENTE — una vez que se pone colorada, se queda asi.

    def _vq9_sudores_secos():
        """Cuantos sudores estan completamente borrados."""
        return sum(1 for _s in VQ9_SUDORES if not _vq9_sudor_vivo(_s))

    def _vq9_boca_reposo():
        """Que boca queda cuando no esta hablando."""
        if _vq9_sudores_secos() >= VQ9_SUDORES_PARA_SONRISA:
            return "b_sonrisa"
        return "b_none"

    def _vq9_cara_reposo():
        """
        Devuelve la cara a como esta cuando no pasa nada.

        NO toca el grupo `ot` a proposito: la verguenza es permanente.
        """
        store.vq9_boca_estado = _vq9_boca_reposo()
        store.vq9_ojos_estado = "o_none"

    def _vq9_cara_gemido():
        """La cara del gemido: se muerde el labio y pone los ojos de placer."""
        store.vq9_boca_estado = "b_mordiendo"
        store.vq9_ojos_estado = "o_placer"

    def _vq9_actualizar_verguenza():
        """
        Prende la verguenza si ya se la gano, y no la apaga nunca mas.

        Lo llama vq9_hablar_inicio, o sea que el cambio se ve al ARRANCAR el
        dialogo del toque que cumplio la condicion, no despues.
        """
        if store.vq9_ot_estado == "ot_verguenza":
            return
        _pelvis = getattr(store, 'vq9_toques_pelvis_desnuda', 0)
        _pechos = getattr(store, 'vq9_toques_pechos', 0)
        if (_pelvis >= VQ9_TOQUES_PARA_VERGUENZA
                or _pechos >= VQ9_TOQUES_PARA_VERGUENZA):
            store.vq9_ot_estado = "ot_verguenza"

    def _vq9_cara():
        """
        Nombre de imagen de la cara con los tres grupos combinados, o None si no
        hay nada que dibujar.

        Devolver None cuando los tres estan en `none` es solo prolijidad —
        dibujar tres Null() no rompe nada, pero asi no se arma la imagen al
        pedo en cada refresco de la screen.
        """
        _b = getattr(store, 'vq9_boca_estado', "b_none")
        _o = getattr(store, 'vq9_ojos_estado', "o_none")
        _t = getattr(store, 'vq9_ot_estado', "ot_none")
        if _b == "b_none" and _o == "o_none" and _t == "ot_none":
            return None
        return "vq9_boca " + _b + " " + _o + " " + _t

    def _vq9_sacar_ropa(prenda):
        """Le saca una prenda. La tanga NO pasa por acá: tiene su propio flujo."""
        if prenda in store.vq9_ropa_puesta:
            store.vq9_ropa_puesta.remove(prenda)




################################################################################
## Layeredimage de la cara
################################################################################
## Lo unico que SI es layeredimage: estados excluyentes sin alpha propio, o sea
## justo lo que un layeredimage hace bien. TODAS las imagenes son de 1920x1080,
## asi que caen solas sobre la cama y no llevan coordenada.
##
## TRES GRUPOS INDEPENDIENTES, y cada uno arranca en `none`: la boca puede estar
## hablando con los ojos normales, o puede haber verguenza sin boca. Se combinan
## libremente porque el estado de cada grupo es su propia variable.
##
## Los grupos se dibujan EN ORDEN DE DECLARACION, o sea `ot` arriba de todo.

layeredimage vq9_boca:

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/quest/violet/quest9/boca_hablando.webp"
        attribute b_hablandochica:
            "images/quest/violet/quest9/boca_hablandochica.webp"
        attribute b_mordiendo:
            "images/quest/violet/quest9/boca_mordiendo.webp"
        attribute b_sonrisa:
            "images/quest/violet/quest9/boca_sonrisa.webp"

    group ojos:
        attribute o_none default:
            Null()
        attribute o_placer:
            "images/quest/violet/quest9/ojos_placer.webp"

    group ot:
        attribute ot_none default:
            Null()
        attribute ot_verguenza:
            "images/quest/violet/quest9/ot_verguenza.webp"


################################################################################
## La escena — todo lo que se dibuja, sin botones
################################################################################
## La usan la screen jugable Y los tramos de dialogo, que no son jugables. Por
## eso esta separada: asi la conversacion se ve exactamente igual que el juego,
## sin repetir la lista de piezas en dos lados.

screen vq9_escena():

    # zorder NEGATIVO: durante los dialogos esta screen queda sola en pantalla y
    # el textbox de Ren'Py vive en zorder 0. Sin esto la escena se dibujaba
    # ENCIMA del textbox y el jugador no veia el mensaje ni podia cerrarlo.
    zorder -10

    add _vq9_img("cama_fondo")

    # Sudores. Cada uno con su propio alpha segun los toques que lleva.
    for _s in VQ9_SUDORES:
        if _vq9_sudor_vivo(_s):
            $ _sp = _vq9_pos("sudor_" + _s)
            add _vq9_img("sudor_" + _s):
                xpos _sp[0]
                ypos _sp[1]
                alpha _vq9_sudor_alpha(_s)

    # Ropa, de adentro hacia afuera.
    for _r in VQ9_ROPA:
        if _r in vq9_ropa_puesta:
            $ _rp = _vq9_pos("ropa_" + _r)
            add _vq9_img("ropa_" + _r) xpos _rp[0] ypos _rp[1]

    if vq9_colcha:
        add _vq9_img("colcha_puesta")

    # La cara (boca + ojos + ot), ARRIBA DE TODO: es lo unico que cambia
    # mientras habla y no tiene que taparla ninguna pieza.
    #
    # Se saltea cuando los tres grupos estan en none — dibujar tres Null() no
    # rompe nada, pero asi no se arma la imagen al pedo en cada refresco.
    $ _cara = _vq9_cara()
    if _cara:
        add _cara


################################################################################
## Screen jugable
################################################################################

screen vq9_minijuego():

    # zorder NEGATIVO, igual que vq9_escena: el textbox de Ren'Py vive en 0, asi
    # que desde acá abajo queda siempre por encima y se lee sin tener que bajar
    # nada.
    #
    # ANTES esto era zorder 100 y cada dialogo hacia el baile de
    # `hide screen vq9_minijuego` + `show screen vq9_escena` y vuelta. En el
    # hueco entre las dos se veia por un frame la capa master —el fondo de la
    # habitacion de la escena anterior— y eso era el pestañeo.
    #
    # SIN `modal True`, y no es un olvido: un modal se come el click que hace
    # avanzar el dialogo, asi que con el puesto el texto no pasaba nunca. No
    # hace falta igual — mientras habla, `if not vq9_hablando` deja la screen
    # sin un solo boton, y el HUD ya esta oculto: no hay nada abajo que pueda
    # robar el click.
    zorder -5

    use vq9_escena

    # TODO LO INTERACTIVO queda apagado mientras corre un dialogo: la
    # screen no se baja, asi que sin esto los botones seguirian vivos
    # debajo del textbox.
    if not vq9_hablando:

        # ── Zonas clickeables ────────────────────────────────────────────────────
        # EL ORDEN IMPORTA: en Ren'Py el ultimo hijo queda arriba y se lleva el
        # click. Va en el MISMO orden en que se dibuja la escena — sudores abajo,
        # ropa arriba — porque si no, el boton de un sudor tapado se comia el click
        # de la prenda que lo cubre y contestaba "dejar la toalla" con la mano
        # puesta.

        # Sudores: lo mas al fondo.
        for _s in VQ9_SUDORES:
            if _vq9_sudor_vivo(_s):
                $ _sp = _vq9_pos("sudor_" + _s)
                imagebutton:
                    idle Transform(_vq9_img("sudor_" + _s), alpha=0.0)
                    hover Transform(_vq9_img("sudor_" + _s), alpha=0.0)
                    xpos _sp[0]
                    ypos _sp[1]
                    action Return(("sudor", _s))

        # Zonas de interaccion: cuando la prenda que las tapaba ya no esta Y con la
        # MANO puesta. Con la toalla tienen que dejar pasar el click al sudor de
        # abajo — si no, secarle los pechos le sacaba un gemido en vez de limpiar.
        if vq9_mano == "base" and "remera" not in vq9_ropa_puesta:
            $ _pp = _vq9_pos("pechos_interaccion")
            imagebutton:
                idle Transform(_vq9_img("pechos_interaccion"), alpha=0.0)
                hover Transform(_vq9_img("pechos_interaccion"), alpha=0.0)
                xpos _pp[0]
                ypos _pp[1]
                action Return(("pechos", None))

        if vq9_mano == "base" and "tanga" not in vq9_ropa_puesta:
            $ _vp = _vq9_pos("pelvis_interaccion")
            imagebutton:
                idle Transform(_vq9_img("pelvis_interaccion"), alpha=0.0)
                hover Transform(_vq9_img("pelvis_interaccion"), alpha=0.0)
                xpos _vp[0]
                ypos _vp[1]
                action Return(("pelvis", None))

        # Ropa: ARRIBA de todo. Con la mano se saca; con la toalla avisa que
        # primero hay que sacarsela.
        for _r in VQ9_ROPA:
            if _r in vq9_ropa_puesta:
                $ _rp = _vq9_pos("ropa_" + _r)
                imagebutton:
                    idle Transform(_vq9_img("ropa_" + _r), alpha=0.0)
                    hover Transform(_vq9_img("ropa_" + _r), alpha=0.0)
                    xpos _rp[0]
                    ypos _rp[1]
                    action Return(("ropa", _r))

        # ── Barra de botones ─────────────────────────────────────────────────────

        hbox:
            xalign 0.5
            ypos 20
            spacing 14

            # Mano
            button:
                background ("#c66a00EE" if vq9_mano == "base" else "#1e1e3aCC")
                hover_background "#e08020"
                padding (18, 12)
                action SetVariable("vq9_mano", "base")
                text "✋" size 34 yalign 0.5

            # Toalla
            button:
                background ("#c66a00EE" if vq9_mano == "toalla" else "#1e1e3aCC")
                hover_background "#e08020"
                padding (18, 12)
                action SetVariable("vq9_mano", "toalla")
                text "🧻" size 34 yalign 0.5

            # Botones grises: se ganan pero todavia no llevan a ningun lado.
            if vq9_boton_boca:
                button:
                    background "#2a2a2aCC"
                    hover_background "#3a3a3a"
                    padding (18, 12)
                    action Return(("proximamente", None))
                    text "👄" size 34 yalign 0.5

            if vq9_boton_victoria:
                button:
                    background "#2a2a2aCC"
                    hover_background "#3a3a3a"
                    padding (18, 12)
                    action Return(("proximamente", None))
                    text "✌️" size 34 yalign 0.5

            # Salir: recien cuando termino de secarla.
            if vq9_completo:
                button:
                    background "#2e7d32EE"
                    hover_background "#388e3c"
                    padding (18, 12)
                    action Return(("salir", None))
                    text "➡️" size 34 yalign 0.5


init python:

    # ── La mano ES el cursor ─────────────────────────────────────────────────
    # `config.mouse_displayable` es la via que Ren'Py trae para esto: dibuja el
    # displayable en la posicion del mouse Y ESCONDE el puntero del sistema.
    #
    # Reemplaza a dos intentos anteriores que no servian:
    #   - la propiedad `mouse` de la screen — no existe, es de displayables;
    #   - pisar config.mouse con un PNG transparente — dejaba el puntero real
    #     igual, porque los imagebuttons le cambian el cursor al hoverearlos.
    #
    # Ademas se dibuja por encima de TODO, incluido el textbox, asi que la mano
    # sigue a la vista durante los dialogos sin hacer nada especial.
    #
    # ⚠️ LO QUE NO HACE ES MOVERLO. Ren'Py lo agrega al root en (0, 0) y ahi lo
    # deja; el displayable se tiene que posicionar solo. Por eso el Transform
    # de abajo lleva `function=_vq9_seguir_mouse`: sin eso la mano queda en la
    # esquina y parece que no se dibuja.
    #
    # ⚠️ Y NO CORRE si el jugador tiene activada la preferencia "cursor del
    # sistema" (display/core.py:2657): ahi Ren'Py ignora mouse_displayable y
    # deja la flecha. No hay forma de forzarlo desde el contenido.

    def vq9_cursor_ocultar():
        config.mouse_displayable = Transform(
            DynamicDisplayable(_vq9_mano_dyn),
            rotate=VQ9_MANO_ROTACION,
            zoom=VQ9_MANO_ZOOM,
            anchor=(VQ9_MANO_ANCLA_X, VQ9_MANO_ANCLA_Y),
            function=_vq9_seguir_mouse,
        )

    def vq9_cursor_restaurar():
        config.mouse_displayable = None


################################################################################
## Testeo — se entra desde el menu de cheats
################################################################################
## Salta al minijuego sin jugar la quest: deja a Violet como al empezar la
## escena (vestida, transpirada y tapada) y abre la parte jugable.
##
## NO toca `violet_enferma_atencion`: eso lo ajustan los dos botones de cuidado
## del mismo menu, para poder ver las dos respuestas de la tanga.

label test_vq9_minijuego:

    $ ocultar_hud()
    window hide

    # Estado limpio, por si ya se habia jugado en esta partida.
    python:
        vq9_mano = "base"
        vq9_sudor_toques = {}
        vq9_ropa_puesta = list(VQ9_ROPA)
        vq9_aviso_ropa = False
        vq9_toques_tanga = 0
        vq9_toques_pechos = 0
        vq9_toques_pelvis = 0
        vq9_toques_pelvis_desnuda = 0
        vq9_tanga_permitida = False
        vq9_boton_boca = False
        vq9_boton_victoria = False
        vq9_completo = False
        vq9_colcha = False
        vq9_boca_estado = "b_none"
        vq9_ojos_estado = "o_none"
        vq9_ot_estado = "ot_none"

    $ vq9_cursor_ocultar()
    with fade

    jump vq9_bucle


################################################################################
## El bucle del minijuego
################################################################################
## LA SCREEN SE MUESTRA UNA VEZ Y NO SE BAJA; el label se queda dando vueltas en
## `ui.interact()`, que devuelve lo que puso el `Return` del boton apretado.
##
## POR QUE NO `Call(...)` EN LOS BOTONES, que era como estaba: un `Call` desde
## una screen mostrada con `show screen` + `pause` corta ese pause, y al
## terminar el handler el flujo sigue en la linea de DESPUES — que era
## `jump game_loop`. O sea que tocar los pechos te devolvia al juego libre, con
## el fondo de la habitacion y las acciones de locacion encima.
##
## Con `Return` + `ui.interact()` el control vuelve acá, se despacha el handler
## y el bucle sigue. Es el mismo patron que usa la quest 04 de Violet.
##
## Los botones de mano NO pasan por acá: son `SetVariable`, que no corta la
## interaccion — la screen se redibuja sola y listo.

label vq9_bucle:

    show screen vq9_minijuego

    $ _vq9_jugando = True

    while _vq9_jugando:

        $ _vq9_res = ui.interact()
        $ _vq9_tipo = _vq9_res[0] if _vq9_res else None
        $ _vq9_dato = _vq9_res[1] if _vq9_res else None

        if _vq9_tipo == "sudor":
            call vq9_click_sudor(_vq9_dato) from _call_vq9_b_sudor

        elif _vq9_tipo == "ropa":
            call vq9_click_ropa(_vq9_dato) from _call_vq9_b_ropa

        elif _vq9_tipo == "pechos":
            call vq9_click_pechos from _call_vq9_b_pechos

        elif _vq9_tipo == "pelvis":
            call vq9_click_pelvis from _call_vq9_b_pelvis

        elif _vq9_tipo == "proximamente":
            call vq9_proximamente from _call_vq9_b_prox

        elif _vq9_tipo == "salir":
            call vq9_salir from _call_vq9_b_salir
            $ _vq9_jugando = False

    # La screen NO se baja acá: si se bajara, por un frame se veria la capa
    # master —que todavia tiene el fondo de la habitacion de la escena previa—
    # antes de que el cierre pinte lo suyo. La baja vq9_cierre, junto con el
    # fundido a negro.
    jump vq9_cierre


################################################################################
## Handlers de click
################################################################################
## TODOS se llaman desde el bucle y terminan en `return`.
##
## El patron es siempre el mismo: sacar la screen jugable para que el textbox se
## lea sin la mano encima, hablar, y volver a mostrarla. Los dos ayudantes de
## abajo hacen eso para no repetirlo en cada handler.

label vq9_hablar_inicio:
    $ vq9_hablando = True
    $ _vq9_actualizar_verguenza()
    window show
    return


label vq9_hablar_fin:
    $ vq9_hablando = False
    window hide
    return


# ── La ropa mojada ───────────────────────────────────────────────────────────
# La MISMA secuencia sirve para las dos manos: si la vio secando, con la mano ya
# no se repite, y al reves. Por eso el flag es uno solo.

label vq9_aviso_ropa_mojada:
    call vq9_hablar_inicio from _call_vq9_aviso_ini

    if not vq9_aviso_ropa:
        $ vq9_aviso_ropa = True

        piensa "Tiene la ropa empapada, se la tendría que quitar"

        mc "Violet, tienes toda la ropa mojada"

        $ vq9_boca_estado = "b_hablando"
        violet "¿Me la puedes quitar por favor?"
        $ _vq9_cara_reposo()

        mc "Sí"

    else:
        piensa "Debo quitarle la ropa primero (Dejar la toalla)"

    call vq9_hablar_fin from _call_vq9_aviso_fin
    return


# ── Click sobre un sudor ─────────────────────────────────────────────────────

label vq9_click_sudor(sid):

    if vq9_mano != "toalla":
        # Con la mano no se seca. Si todavia no vio el aviso, se lo da igual:
        # es el mismo momento narrativo.
        call vq9_aviso_ropa_mojada from _call_vq9_sudor_mano
        return

    if _vq9_tapada():
        call vq9_aviso_ropa_mojada from _call_vq9_sudor_tapada
        return

    $ _vq9_secar(sid)

    # Si ese toque fue el que borro el segundo sudor, la sonrisa tiene que
    # aparecer AHORA — no en el proximo dialogo.
    $ _vq9_cara_reposo()

    if vq9_completo:
        call vq9_charla_final from _call_vq9_sudor_final

    return


# ── Click sobre una prenda ───────────────────────────────────────────────────

label vq9_click_ropa(prenda):

    if vq9_mano == "toalla":
        # Secar sobre la ropa: mismo aviso que sobre el cuerpo tapado.
        call vq9_aviso_ropa_mojada from _call_vq9_ropa_toalla
        return

    if prenda == "tanga":
        jump vq9_click_tanga

    # La primera vez el click solo dispara la conversacion: es la que explica
    # por que hay que sacarle la ropa. Recien el click SIGUIENTE se la saca.
    if not vq9_aviso_ropa:
        call vq9_aviso_ropa_mojada from _call_vq9_ropa_aviso
        return

    $ _vq9_sacar_ropa(prenda)
    return


# ── La tanga ─────────────────────────────────────────────────────────────────
# Tres gemidos y al cuarto toque se decide, UNA sola vez, si lo deja. La
# decision mira el cuidado que le dio durante los tres dias de enfermedad.

label vq9_click_tanga:

    $ vq9_toques_tanga += 1

    if vq9_tanga_permitida:
        # Ya dijo que si: el proximo toque se la saca.
        $ _vq9_sacar_ropa("tanga")
        return

    call vq9_hablar_inicio from _call_vq9_tanga_ini

    if vq9_toques_tanga < VQ9_TOQUES_PARA_CHARLA:
        $ _vq9_cara_gemido()
        violet "Mmmh..."
        $ _vq9_cara_reposo()

    elif vq9_toques_tanga == VQ9_TOQUES_PARA_CHARLA:
        # El recuerdo se avisa ANTES de que hable: asi el jugador entiende que
        # lo que va a escuchar depende de algo que hizo.
        $ notificar_recuerdo_activado()

        if getattr(store, 'violet_enferma_atencion', 0) >= VQ9_CUIDADO_PARA_TANGA:
            $ vq9_tanga_permitida = True
            $ vq9_boca_estado = "b_hablando"
            violet "Si quieres, sácala"
            $ _vq9_cara_reposo()
        else:
            $ vq9_boca_estado = "b_hablando"
            violet "No te lo ganaste"
            $ _vq9_cara_reposo()

    else:
        # Sigue tocando sin permiso: vuelve al gemido.
        $ _vq9_cara_gemido()
        violet "Mmmh..."
        $ _vq9_cara_reposo()

    call vq9_hablar_fin from _call_vq9_tanga_fin
    return


# ── Los pechos ───────────────────────────────────────────────────────────────

label vq9_click_pechos:

    $ vq9_toques_pechos += 1

    call vq9_hablar_inicio from _call_vq9_pechos_ini

    if vq9_toques_pechos == VQ9_TOQUES_PARA_CHARLA:

        $ vq9_boca_estado = "b_hablando"
        violet "¿Te gustan?"
        $ _vq9_cara_reposo()

        mc "Todo de ti me gustan"

        $ vq9_boca_estado = "b_hablando"
        violet "Si fueran más grandes sería mejor"
        $ _vq9_cara_reposo()

        mc "Tienen su encanto, para grande ya tenemos la cola"

        $ vq9_boton_boca = True

    else:
        $ _vq9_cara_gemido()
        violet "Mmmh..."
        $ _vq9_cara_reposo()

    call vq9_hablar_fin from _call_vq9_pechos_fin
    return


# ── La pelvis ────────────────────────────────────────────────────────────────

label vq9_click_pelvis:

    $ vq9_toques_pelvis += 1

    # La cuenta que mira la verguenza es solo la de los toques sin la tanga.
    if "tanga" not in vq9_ropa_puesta:
        $ vq9_toques_pelvis_desnuda += 1

    call vq9_hablar_inicio from _call_vq9_pelvis_ini

    if vq9_toques_pelvis == VQ9_TOQUES_PARA_CHARLA:

        $ vq9_boca_estado = "b_hablando"
        violet "Estoy muy caliente y no es por la fiebre"
        $ _vq9_cara_reposo()

        mc "No me puedo resistir cuando se trata de ti"

        $ vq9_boca_estado = "b_hablando"
        violet "Nunca dije que te resistas"
        $ _vq9_cara_reposo()

        $ vq9_boton_victoria = True

    else:
        $ _vq9_cara_gemido()
        violet "Mmmh..."
        $ _vq9_cara_reposo()

    call vq9_hablar_fin from _call_vq9_pelvis_fin
    return


# ── Los botones grises ───────────────────────────────────────────────────────

label vq9_proximamente:
    call vq9_hablar_inicio from _call_vq9_prox_ini
    "Este contenido se incluirá en futuras actualizaciones"
    call vq9_hablar_fin from _call_vq9_prox_fin
    return


################################################################################
## Cierre
################################################################################
## La charla salta apenas termina de secarla y deja el boton de salir a la
## vista. El jugador puede seguir tocando lo que quiera antes de irse.

label vq9_charla_final:
    call vq9_hablar_inicio from _call_vq9_final_ini

    $ vq9_boca_estado = "b_hablando"
    violet "..."
    $ _vq9_cara_reposo()

    mc "..."

    call vq9_hablar_fin from _call_vq9_final_fin
    return


label vq9_salir:

    # ANTES ACA HABIA UN MENU "¿Salgo de la habitacion?" con Si/No. Se saco: el
    # boton ya no lleva a irse sino a quedarse, asi que preguntar si sale y que
    # el "Si" termine en dormir con ella era contradictorio. Igual no hace falta
    # protegerlo de un click accidental: el boton recien aparece con los ocho
    # sudores secos, o sea que es un "ya termine" deliberado.

    call vq9_hablar_inicio from _call_vq9_salir_ini

    $ vq9_boca_estado = "b_hablando"
    violet "¿Te quedas a dormir conmigo?"
    $ _vq9_cara_reposo()

    mc "Sí"

    call vq9_hablar_fin from _call_vq9_salir_fin
    return


################################################################################
## El cierre — se queda a dormir con ella
################################################################################
## HASTA ACA LLEGA EL ARCO POR AHORA. La escena de la mañana siguiente todavia
## no existe, asi que en vez de dejarla con dialogo sin escribir se avisa con un
## cartel y la quest cierra al dormir.
##
## El label `vq9_despertar` que habia despues se elimino junto con el cartel: sus
## dos `piensa` eran marcadores vacios y no habia forma de llegar a el sin pasar
## por acá.

label vq9_cierre:

    $ vq9_cursor_restaurar()
    $ ocultar_hud()
    window show

    # El negro y el bajado de las screens van en UNA sola transicion: asi no
    # llega a verse la capa master con el fondo viejo.
    scene black
    hide screen vq9_minijuego
    hide screen vq9_escena
    with fade

    # El cartel espera el CLICK y no un `pause` con segundos: es un aviso para
    # leer, no un efecto.
    show text Text(renpy.translate_string("Continuará en la siguiente actualización"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause
    hide text with dissolve

    # Se duerme AHI, en la habitacion de Violet. El autoguardado va justo
    # despues, como en accion_dormir — nunca adentro de dormir().
    call screen animacion_dormir with dissolve
    $ dormir()
    $ autoguardar_partida()

    # Amanece en su pieza: no volvio a la suya.
    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    $ vq9b_rama = "cerrado"
    $ marcar_npc_disponible("violet")
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_09_a")

    window hide
    $ mostrar_hud()
    jump game_loop
