################################################################################
## Tinte de personajes por horario
################################################################################
## Los personajes toman levemente el tono de la luz del ambiente segun el
## horario, SIN teñir el fondo (que ya viene pintado con esa luz). Diseño y
## relevamiento del motor en docs/arquitectura/tinte_horario_personajes.md.
##
## Como funciona, en tres piezas:
##
##   1. CAPA `personajes`, justo arriba de `master`. Los sprites de personaje
##      van ahi por TAG (config.tag_layer): `show violet_parada` no cambia. Un
##      `scene` limpia las dos capas (config.scene_callbacks), asi que se
##      comporta exactamente como antes.
##   2. TINTE de la capa entera: renpy.show_layer_at con un transform de
##      matrixcolor, uno por horario, aplicado al cambiar el horario y al
##      cargar. Cero por sprite.
##   3. Los IDLES del HUD (los personajes caminando por la casa) NO llevan
##      tinte, por decision: son ilustraciones ya pintadas con la luz de esa
##      hora. El tinte es solo para los sprites de las secuencias de dialogo
##      (layeredimages). `tinte_transform_actual()` queda disponible para
##      cualquier sprite de personaje dibujado en una screen que si lo pida.
##
## El tinte es una capa de color en modo MULTIPLICAR (como en Photoshop) con
## opacidad `fuerza`, aplicada SOLO a los pixeles del sprite: cada canal se
## multiplica por el color, asi que oscurece y colorea segun lo que hay
## debajo en vez de pintar plano. El alfa no se toca. Mañana no lleva.
##
## Sitios con `show expression` (se saltean tag_layer, llevan `onlayer
## personajes` a mano): talksystem_labels, violet_quest_09_b (x2),
## jn_pocketboy (x2). Las cajas de mc_quest_0_a son un objeto: quedan en master.

# Color por horario. None = sin tinte.
define TINTE_HORARIO_COLORES = {
    0: None,          # mañana
    1: "#df7f4e",     # tarde
    2: "#b78a73",     # noche
    3: "#303b4b",     # trasnoche
}

# Opacidad de la capa multiplicar (0 = nada, 1 = multiplicar a full). Es EL
# boton para ajustar a ojo.
define TINTE_HORARIO_FUERZA = 0.25

# "multiplicar": pixel * color (oscurece y colorea segun lo que hay debajo).
# "normal": mezcla hacia el color plano (lo primero que se probo; aplasta).
define TINTE_MODO = "multiplicar"

# Prefijos de tag que se consideran personaje (van a la capa `personajes`).
define TINTE_PREFIJOS_PERSONAJE = ("violet_", "monica_", "jasmine_", "mc_",
                                   "repartidor_", "padre_", "beso_",
                                   "zowie_", "leah_")
# Tags con esos prefijos que NO son personaje (fondos, efectos, o un
# layeredimage que trae su propio fondo adentro y no hay que teñir).
define TINTE_TAGS_EXCLUIDOS = ("violet_evento02_fondo", "monica_evento_01")


init -20 python:

    # 1. La capa, entre master y transient.
    if "personajes" not in config.layers:
        config.layers.insert(config.layers.index("master") + 1, "personajes")

    # Un `scene` (o renpy.scene) sobre master limpia tambien a los personajes:
    # es lo que hacia antes, cuando vivian en master.
    #
    # OJO: limpiar una capa le borra tambien su at-list
    # (config.scene_clears_layer_at_list, scenelists.py:617), o sea el tinte.
    # Por eso se reaplica aca mismo, despues de limpiar: cada `scene` de una
    # escena narrativa pasaba por aca y dejaba la capa sin teñir.
    def _tinte_scene_callback(layer):
        if layer == "master":
            renpy.scene("personajes")
            aplicar_tinte_personajes()

    if _tinte_scene_callback not in config.scene_callbacks:
        config.scene_callbacks.append(_tinte_scene_callback)


init python:

    class TinteAmbiente(ColorMatrix):
        """
        matrixcolor de una capa de color con opacidad `fuerza` sobre el
        sprite, solo sobre los pixeles visibles (el alfa no se toca).

        modo "multiplicar" (Photoshop: Multiply):
            out = pixel * ((1 - f) + f * color)
          — cada canal se escala por el color: lo claro toma el color, lo
          oscuro sigue oscuro. Es una matriz diagonal.

        modo "normal":
            out = (1 - f) * pixel + f * color
          — mezcla hacia el color plano. El corrimiento va en la 4ta columna
          multiplicado por el alfa (como BrightnessMatrix) para no pintar lo
          transparente.
        """
        def __init__(self, color, fuerza, modo="multiplicar"):
            self.color = Color(color)
            self.fuerza = float(fuerza)
            self.modo = modo
            self.value = self.fuerza

        def __call__(self, other, done):
            if type(other) is SplineMatrix:
                other = other.matrix
            r, g, b, _a = self.color.rgba
            f = self.fuerza
            if type(other) is type(self):
                oldr, oldg, oldb, _oa = other.color.rgba
                r = oldr + (r - oldr) * done
                g = oldg + (g - oldg) * done
                b = oldb + (b - oldb) * done
                f = other.fuerza + (f - other.fuerza) * done
            k = 1.0 - f
            if self.modo == "multiplicar":
                return Matrix([k + f * r, 0, 0, 0,
                               0, k + f * g, 0, 0,
                               0, 0, k + f * b, 0,
                               0, 0, 0, 1])
            return Matrix([k, 0, 0, f * r,
                           0, k, 0, f * g,
                           0, 0, k, f * b,
                           0, 0, 0, 1])

    def tinte_matrix_para(horario):
        """El TinteAmbiente del horario, o None si no lleva."""
        color = TINTE_HORARIO_COLORES.get(horario)
        if not color or TINTE_HORARIO_FUERZA <= 0:
            return None
        return TinteAmbiente(color, TINTE_HORARIO_FUERZA, TINTE_MODO)

    _TINTE_TRANSFORMS = {}

    def tinte_transform_actual():
        """
        Transform para el `at` de los sprites que se dibujan en screens (el
        HUD). Uno por horario, cacheado: crear un Transform nuevo en cada
        refresco de la screen reiniciaria el displayable.
        """
        h = getattr(store, "horario_actual", 0)
        clave = (h, TINTE_HORARIO_FUERZA, TINTE_MODO, TINTE_HORARIO_COLORES.get(h))
        t = _TINTE_TRANSFORMS.get(clave)
        if t is None:
            m = tinte_matrix_para(h)
            t = Transform(matrixcolor=m) if m is not None else Transform()
            _TINTE_TRANSFORMS[clave] = t
        return t

    def aplicar_tinte_personajes():
        """
        Tiñe la capa `personajes` segun el horario actual. Idempotente. Se
        llama al cambiar el horario (avanzar, dormir, actualizar_bg_master) y
        al cargar una partida.
        """
        try:
            m = tinte_matrix_para(getattr(store, "horario_actual", 0))
            renpy.show_layer_at([Transform(matrixcolor=m)] if m is not None else [],
                                layer="personajes")
        except Exception as e:
            if config.developer:
                print("[Tinte] no se pudo aplicar: %r" % (e,))

    def _tinte_es_tag_personaje(tag):
        """
        Personaje = prefijo de personaje y, ademas, imagen CON ALFA: un
        layeredimage (los sprites del proyecto son todos webp/png) o una
        `image` cuyo archivo sea webp/png. Un CG/fondo con prefijo de
        personaje (violet_quest08_livingnublado, un jpg) queda en master:
        teñirlo entero es justo lo que no se quiere.
        """
        if tag in TINTE_TAGS_EXCLUIDOS or not tag.startswith(TINTE_PREFIJOS_PERSONAJE):
            return False
        try:
            d = renpy.get_registered_image(tag)
        except Exception:
            return False
        if d is None:
            return False
        if isinstance(d, LayeredImage):
            return True
        fn = getattr(d, "filename", None)
        if isinstance(fn, str):
            return fn.lower().endswith((".webp", ".png"))
        return False


init 999 python:

    # 2. Rutear por tag: toda imagen registrada cuyo tag sea de personaje va a
    #    la capa `personajes`. Se hace al final del init, con todas las
    #    imagenes (layeredimage e image) ya definidas.
    _tinte_tags = set()
    for _tag in renpy.get_available_image_tags():
        if _tinte_es_tag_personaje(_tag):
            config.tag_layer[_tag] = "personajes"
            _tinte_tags.add(_tag)
    TINTE_TAGS_PERSONAJE = frozenset(_tinte_tags)
    del _tinte_tags


# ── Diagnostico (consola: jp_tinte_diagnostico()) ───────────────────────────
init python:

    def jp_tinte_diagnostico():
        """
        Imprime lo que hace falta para saber por que no se ve el tinte y abre
        una screen de prueba: Violet sin tinte, con el tinte del horario y
        con un TintMatrix pelado a full. Si la de la derecha tampoco cambia,
        el renderer no aplica matrixcolor; si cambia y la del medio no, el
        problema es nuestro transform.
        """
        try:
            print("renderer:", renpy.get_renderer_info())
        except Exception as e:
            print("renderer: ?", e)
        h = getattr(store, "horario_actual", None)
        print("horario:", h, "fuerza:", TINTE_HORARIO_FUERZA, "color:", TINTE_HORARIO_COLORES.get(h))
        print("matrix:", tinte_matrix_para(h)(None, 1.0) if tinte_matrix_para(h) else None)
        try:
            sls = renpy.game.context().scene_lists
            print("layers:", config.layers)
            print("layer_at_list[personajes]:", sls.layer_at_list.get("personajes"))
            print("sprites en personajes:", [e.tag for e in sls.layers.get("personajes", [])])
            print("sprites en master:", [e.tag for e in sls.layers.get("master", [])])
        except Exception as e:
            print("scene lists: ?", e)
        renpy.show_screen("jp_tinte_prueba")
        renpy.restart_interaction()


screen jp_tinte_prueba():
    zorder 400
    frame:
        xalign 0.5 yalign 0.5
        background "#000000CC"
        padding (20, 20)
        vbox:
            spacing 8
            text "Prueba de tinte — izquierda sin tinte, medio tinte del horario, derecha TintMatrix a full" size 16 color "#fff"
            hbox:
                spacing 30
                add "violet_parada" zoom 0.35
                add "violet_parada" zoom 0.35 at tinte_transform_actual()
                add "violet_parada" zoom 0.35:
                    matrixcolor TintMatrix("#df7f4e")
            textbutton "Cerrar" action Hide("jp_tinte_prueba")

