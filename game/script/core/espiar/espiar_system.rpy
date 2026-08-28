################################################################################
## Sistema de Espiar en el Baño — Motor
################################################################################
## Lo que ve el jugador cuando Violet deja la puerta del baño entreabierta y el
## MC MIRA. Es la primera situacion de la ventaja "Provocación" (hito de deseo
## 30): la puerta esta asi porque ELLA la dejo asi.
##
## QUE HACE:
##   - Muestra la escena de la ducha por la rendija, con la puerta en su
##     posicion mas abierta. No hay nada que abrir ni nada que fallar.
##   - Dos botones, AccionLocacion globales (locacion_id=None) que solo existen
##     mientras hay sesion: "Entrar" (en gris, contenido en desarrollo) y
##     "Salir". Salir avanza 1 horario.
##
## QUIEN DECIDE SI SE PUEDE MIRAR: no este archivo. El estado de la puerta lo
## sortea characters/violet/ventajas/provocacion/provocacion_violet.rpy, y el
## menu del baño (core/locations/door_access_system) muestra "Mirar" solo si dio
## abierta.
##
## SE ELIMINO (era del viejo "espiar", donde el MC forzaba la situacion):
##   - "Abrir mas" con su tirada contra la destreza y sus etapas de apertura
##   - todo el "te descubrieron" (reacciones por deseo, primera vez, stats)
##   - el requisito ESPIAR_DESEO_MINIMO — ahora habilita la ventaja
##   - la instancia "entrar" y su boton "Unirse"
##
## Para AGREGAR una escena: registrar_secuencia_espiar(SecuenciaEspiar(...)) —
## ver espiar_violet.rpy.

################################################################################
## Estado guardable
################################################################################

# Interruptor maestro. Mientras este en False la opcion "Mirar" no aparece
# aunque la puerta este abierta — todo el sistema sigue acá, poner True lo
# re-activa de una.
define ESPIAR_HABILITADO = True

# Sesion activa (None = no esta corriendo). Dict plano picklable:
# {"npc_id", "secuencia_id"}
default espiar_sesion = None

# NPC objetivo al iniciar (lo setea interaccion_banio_ocupado)
default _espiar_npc_temp = None


# =============================================================================
# IMÁGENES DEL MINIJUEGO DE DUCHA
# =============================================================================
# Fondos y estructuras
image ducha_mg_fondo           = "images/minijuegos/ducha/ducha_fondo.jpg"
image ducha_mg_pared           = "images/minijuegos/ducha/ducha_pared.webp"
image ducha_mg_puerta          = "images/minijuegos/ducha/ducha_puerta.webp"
image ducha_mg_vidrio          = "images/minijuegos/ducha/ducha_vidrio.webp"

# Capas de vapor
image ducha_mg_vapor_fondo     = "images/minijuegos/ducha/ducha_vapor_fondo.webp"
image ducha_mg_vapor_medio     = "images/minijuegos/ducha/ducha_vapor_medio.webp"
image ducha_mg_vapor_exterior  = "images/minijuegos/ducha/ducha_vapor_exterior.webp"

# Animación de lluvia (3 frames cada una)
layeredimage ducha_mg_lluvia_fondo:
    group secuencia:
        attribute f1 default:
            "images/minijuegos/ducha/ducha_lluvia_fondo_1.webp"
        attribute f2:
            "images/minijuegos/ducha/ducha_lluvia_fondo_2.webp"
        attribute f3:
            "images/minijuegos/ducha/ducha_lluvia_fondo_3.webp"

layeredimage ducha_mg_lluvia_frente:
    group secuencia:
        attribute f1 default:
            "images/minijuegos/ducha/ducha_lluvia_frente_1.webp"
        attribute f2:
            "images/minijuegos/ducha/ducha_lluvia_frente_2.webp"
        attribute f3:
            "images/minijuegos/ducha/ducha_lluvia_frente_3.webp"

# Animación de lluvia: 75% de transparencia en las tres capas. Cada una va a
# un x distinto y arranca en un frame distinto para que no caigan en bloque.
image ducha_mg_lluvia_fondo_animado = Transform(
    Animation(
        "images/minijuegos/ducha/ducha_lluvia_fondo_1.webp", 0.16,
        "images/minijuegos/ducha/ducha_lluvia_fondo_2.webp", 0.16,
        "images/minijuegos/ducha/ducha_lluvia_fondo_3.webp", 0.16,
        loop=True
    ),
    alpha=0.75, xoffset=-50
)

# Columna mas lejana: copia de la de fondo, 50px a la derecha de esta (o sea
# centrada en 0) y arrancando en el frame 3 para no caer sincronizada con ella.
image ducha_mg_lluvia_fondo_animado_alt = Transform(
    Animation(
        "images/minijuegos/ducha/ducha_lluvia_fondo_3.webp", 0.16,
        "images/minijuegos/ducha/ducha_lluvia_fondo_1.webp", 0.16,
        "images/minijuegos/ducha/ducha_lluvia_fondo_2.webp", 0.16,
        loop=True
    ),
    alpha=0.75, xoffset=0
)

# Lluvia frente comienza en imagen 2 (desincronizada)
image ducha_mg_lluvia_frente_animado = Transform(
    Animation(
        "images/minijuegos/ducha/ducha_lluvia_frente_2.webp", 0.11,
        "images/minijuegos/ducha/ducha_lluvia_frente_3.webp", 0.11,
        "images/minijuegos/ducha/ducha_lluvia_frente_1.webp", 0.11,
        loop=True
    ),
    alpha=0.75
)

# Violet en la ducha: el orden de frames NO es lineal (se eligió a mano) y la
# vuelta es en espejo. Cada cambio pasa por un dissolve, asi que se arma con
# anim.TransitionAnimation — Animation() solo hace cortes secos.
#
# Va en `init 5` y no como `image` suelto porque usa sprite_normal, que define
# options.rpy en init 0: este archivo se carga antes (script/core/ < script/ui/),
# asi que a init 0 esa variable todavia no existe.
init 5 python:

    # Ida, y vuelta en espejo salteando los dos extremos: el pivote (4) y el
    # frame inicial (5) quedarian el doble de tiempo en pantalla si se repitieran.
    _ESP_VIOLET_IDA = [5, 8, 12, 9, 2, 14, 3, 1, 7, 10, 11, 13, 15, 4]
    _ESP_VIOLET_CICLO = _ESP_VIOLET_IDA + _ESP_VIOLET_IDA[::-1][1:-1]

    # TransitionAnimation toma (imagen, tiempo, transicion) repetido. La
    # transicion que sigue a cada imagen es la que lleva A LA SIGUIENTE, y la
    # ultima cierra el loop volviendo al primer frame — por eso van todas.
    # El dissolve corre DENTRO del segundo de cada frame, no se le suma.
    _esp_violet_args = []
    for _esp_frame in _ESP_VIOLET_CICLO:
        _esp_violet_args.append("images/minijuegos/ducha/ducha_violet_jabon_%d.webp" % _esp_frame)
        _esp_violet_args.append(1.0)
        _esp_violet_args.append(sprite_normal)

    renpy.image("ducha_mg_violet_animado", anim.TransitionAnimation(*_esp_violet_args))

# Layeredimage para compatibilidad con atributos (j1-j15)
layeredimage ducha_mg_violet:
    group jabon:
        attribute j1 default:
            "images/minijuegos/ducha/ducha_violet_jabon_1.webp"
        attribute j2:
            "images/minijuegos/ducha/ducha_violet_jabon_2.webp"
        attribute j3:
            "images/minijuegos/ducha/ducha_violet_jabon_3.webp"
        attribute j4:
            "images/minijuegos/ducha/ducha_violet_jabon_4.webp"
        attribute j5:
            "images/minijuegos/ducha/ducha_violet_jabon_5.webp"
        attribute j6:
            "images/minijuegos/ducha/ducha_violet_jabon_6.webp"
        attribute j7:
            "images/minijuegos/ducha/ducha_violet_jabon_7.webp"
        attribute j8:
            "images/minijuegos/ducha/ducha_violet_jabon_8.webp"
        attribute j9:
            "images/minijuegos/ducha/ducha_violet_jabon_9.webp"
        attribute j10:
            "images/minijuegos/ducha/ducha_violet_jabon_10.webp"
        attribute j11:
            "images/minijuegos/ducha/ducha_violet_jabon_11.webp"
        attribute j12:
            "images/minijuegos/ducha/ducha_violet_jabon_12.webp"
        attribute j13:
            "images/minijuegos/ducha/ducha_violet_jabon_13.webp"
        attribute j14:
            "images/minijuegos/ducha/ducha_violet_jabon_14.webp"
        attribute j15:
            "images/minijuegos/ducha/ducha_violet_jabon_15.webp"

init python:
    # Desplazamiento de la puerta, en px. Es la posicion mas abierta — la que
    # antes se alcanzaba tras tres "Abrir mas" exitosos (3 x 100px).
    ESPIAR_PUERTA_ABIERTA_X = 300

    # Cuánto se puede arrastrar el fondo hacia cada lado desde su posición
    # inicial, en px. El fondo se muestra a tamaño nativo (sin zoom): el margen
    # se logra dándole al viewport un contenido más ancho que la pantalla, con
    # la imagen centrada. Solo hay desplazamiento horizontal — el alto del
    # contenido es igual al de la pantalla, asi que no hay scroll vertical.
    ESPIAR_DRAG_MARGEN = 50

    # Requisitos de stats para habilitar botones (si no se cumplen, el botón
    # igual se muestra, en gris)
    ESPIAR_DESTREZA_ENTRAR = 10

    class SecuenciaEspiar(object):
        """
        Una escena espiable de un NPC en el baño.

        Args:
            id: identificador unico (ej: "violet_espiar_ducha")
            npc_id: NPC al que pertenece
            nombre: nombre descriptivo (para debug/menus futuros)
            fondo: imagen de fondo de la mirilla (tamaño nativo, drag horizontal)
            label_entrar: si se define, "Entrar" salta a este label (escena
                          propia de la secuencia). Sin el, "Entrar" queda en gris.
            margen_drag: px arrastrables a cada lado (default ESPIAR_DRAG_MARGEN)
            peso: peso relativo en el sorteo aleatorio (default 1)
            condicion: funcion de modulo → bool; si falla, la secuencia no entra
                       al sorteo (permite secuencias de quest/evento)
        """
        def __init__(self, id, npc_id, fondo, nombre="",
                     label_entrar=None, margen_drag=None,
                     peso=1, condicion=None):
            self.id = id
            self.npc_id = npc_id
            self.nombre = nombre
            self.fondo = fondo
            self.label_entrar = label_entrar
            self.margen_drag = margen_drag
            self.peso = peso
            self._condicion = condicion

        def obtener_margen_drag(self):
            m = getattr(self, 'margen_drag', None)
            return ESPIAR_DRAG_MARGEN if m is None else m

        def es_valida(self):
            if self._condicion is None:
                return True
            return self._condicion()

    # Catálogo de secuencias por NPC. Vive en init (no se guarda): la sesión
    # solo referencia secuencias por id, igual que las quests con su catálogo.
    CATALOGO_ESPIAR = {}

    def registrar_secuencia_espiar(secuencia):
        CATALOGO_ESPIAR.setdefault(secuencia.npc_id, [])
        CATALOGO_ESPIAR[secuencia.npc_id] = [
            s for s in CATALOGO_ESPIAR[secuencia.npc_id] if s.id != secuencia.id
        ] + [secuencia]

    def obtener_secuencias_espiar(npc_id):
        """Secuencias del NPC cuya condicion se cumple ahora."""
        return [s for s in CATALOGO_ESPIAR.get(npc_id, []) if s.es_valida()]

    def npc_tiene_espiar(npc_id):
        """True si el NPC tiene al menos una secuencia espiable (habilita el botón)."""
        return bool(obtener_secuencias_espiar(npc_id))

    # ── Estado de la puerta ──────────────────────────────────────────────────
    # El motor NO decide si la puerta esta abierta: pregunta. Cada NPC registra
    # su funcion desde su contenido (para Violet, la ventaja Provocación en
    # characters/violet/ventajas/provocacion/). Sin funcion registrada, cerrada.
    PUERTA_BANIO_REGISTRO = {}   # {npc_id: fn() -> bool}

    def registrar_puerta_banio(npc_id, funcion):
        """
        Registra quien decide si ESE NPC deja la puerta del baño entreabierta.
        `funcion` es de MODULO, sin argumentos, y devuelve bool.
        """
        PUERTA_BANIO_REGISTRO[npc_id] = funcion

    def npc_puerta_banio_abierta(npc_id):
        """
        ¿Dejo la puerta entreabierta? Lo consulta el menu del baño para decidir
        si ofrece "Mirar".

        Envuelto en try porque lo llama una screen: una excepcion ahi rompe el
        menu entero. Ante la duda, cerrada.
        """
        _fn = PUERTA_BANIO_REGISTRO.get(npc_id)
        if _fn is None:
            return False
        try:
            return bool(_fn())
        except Exception:
            return False

    def elegir_secuencia_espiar(npc_id):
        """Sortea una secuencia del pool válido, respetando pesos."""
        pool = obtener_secuencias_espiar(npc_id)
        if not pool:
            return None
        total = sum(max(1, s.peso) for s in pool)
        r = renpy.random.randint(1, total)
        acumulado = 0
        for s in pool:
            acumulado += max(1, s.peso)
            if r <= acumulado:
                return s
        return pool[-1]

    def _espiar_secuencia_actual():
        if not store.espiar_sesion:
            return None
        for s in CATALOGO_ESPIAR.get(store.espiar_sesion["npc_id"], []):
            if s.id == store.espiar_sesion["secuencia_id"]:
                return s
        return None

    def _espiar_cerrar_ui():
        """
        Cierra el minijuego dejando la pantalla lista para un cutscene limpio:
        limpia la sesión, RETIRA el screen del minijuego y OCULTA el HUD.

        Por qué oculta el HUD: el minijuego vive durante un `pause` del
        game_loop, y game_loop hace mostrar_hud() en cada vuelta — asi que
        mientras se juega el HUD (hotspots de movimiento incluidos) está
        "vivo" por debajo, tapado solo por el fondo del minijuego. Al retirar
        el minijuego para la escena de reacción, esos hotspots quedarian a la
        vista. ocultar_hud() lo apaga (y hace restart_interaction, que ademas
        retira ya el screen del minijuego para que su viewport no se coma los
        clicks del primer diálogo). La escena corre entonces como cualquier
        cutscene de quest; el label que llama restaura con mostrar_hud() al
        terminar.
        """
        store.espiar_sesion = None
        renpy.hide_screen("espiar_minijuego")
        renpy.hide_screen("hud_navegacion")
        ocultar_hud()

    # "Entrar" se muestra siempre pero EN GRIS: la escena de adentro todavia no
    # existe. Se deja a la vista para que el jugador sepa que la opcion va a
    # estar. Una secuencia con label_entrar propio si la habilita.

    def _esp_acc_entrar_visible():
        return bool(getattr(store, 'espiar_sesion', None))

    def _esp_acc_entrar_habilitada():
        _sec = _espiar_secuencia_actual()
        return bool(_sec and _sec.label_entrar)

    def _esp_acc_salir_visible():
        return bool(getattr(store, 'espiar_sesion', None))


################################################################################
## Acciones de locación del minijuego
################################################################################
## Globales (locacion_id=None) + condicion por sesión: solo aparecen durante el
## minijuego. obtener_acciones_locacion filtra para que, con sesión activa, el
## panel muestre EXCLUSIVAMENTE estas (ver actionsystem_core).

# (Las dos acciones del minijuego —Entrar y Salir— se registran en
# core/actions/actions_catalog.rpy, con el resto. Sus condiciones
# (_esp_acc_*) siguen viviendo acá.)


################################################################################
## Screen del minijuego
################################################################################
## El minijuego vive durante un `pause` del game_loop, que reactiva el HUD en
## cada vuelta — por eso el screen es `modal`: bloquea el HUD (hotspots, sprites)
## que queda vivo por debajo. El panel de acciones se fuerza desde aca para que
## los botones del minijuego mantengan la estética del juego.

screen espiar_minijuego():
    modal True

    $ _esp_scr_sec = _espiar_secuencia_actual()

    # Fondo negro (limite visual del arrastre)
    add "#000000"

    if _esp_scr_sec and espiar_sesion:

        if True:
            # Orden de capas (de atrás para adelante). Todas son
            # 1920x1080 a pantalla completa, asi que van sin posicionar.
            # Los nombres van entre comillas: `add` evalua una expresion Python
            # y un nombre de imagen suelto seria una variable inexistente.
            # 1. Fondo base
            add "ducha_mg_fondo"
            # 2. Vapor de fondo
            add "ducha_mg_vapor_fondo"
            # 3. Lluvia de fondo lejana (animada, comienza en frame 3)
            add "ducha_mg_lluvia_fondo_animado_alt"
            # 4. Lluvia de fondo (animada)
            add "ducha_mg_lluvia_fondo_animado"
            # 5. Violet animada en loop
            add "ducha_mg_violet_animado"
            # 6. Vapor intermedio
            add "ducha_mg_vapor_medio"
            # 7. Lluvia frontal (animada, comienza en frame 2)
            add "ducha_mg_lluvia_frente_animado"
            # 8. Vidrio frontal
            add "ducha_mg_vidrio"
            # 9. Vapor exterior
            add "ducha_mg_vapor_exterior"
            # 10. Pared frontal
            add "ducha_mg_pared"
            # 11. Puerta frontal, FIJA en su posicion mas abierta. Antes se
            # corria de a 100px con el boton "Abrir mas"; ahora la puerta esta
            # asi porque Violet la dejo asi, no hay nada que forzar.
            add Transform("ducha_mg_puerta", xoffset=ESPIAR_PUERTA_ABIERTA_X)

    # Botones del minijuego con la estética del panel de acciones del HUD
    use acciones_locacion(forzar=True)


################################################################################
## Labels del minijuego
################################################################################

# Punto de entrada — _espiar_npc_temp debe estar seteado (menu del baño)
label espiar_iniciar:

    $ _esp_sec_ini = elegir_secuencia_espiar(_espiar_npc_temp)

    if not _esp_sec_ini:
        # No deberia pasar (el botón se oculta sin secuencias) — salir limpio
        $ mostrar_hud()
        return

    $ espiar_sesion = {
        "npc_id": _espiar_npc_temp,
        "secuencia_id": _esp_sec_ini.id,
    }
    show screen espiar_minijuego
    return


# ── Entrar ───────────────────────────────────────────────────────────────────
label accion_espiar_entrar:

    if not espiar_sesion:
        return

    $ _esp_ent_sec = _espiar_secuencia_actual()

    if _esp_ent_sec and _esp_ent_sec.label_entrar:
        # Escena propia de la secuencia: el label desarrolla lo suyo y retorna
        $ _espiar_cerrar_ui()
        call expression _esp_ent_sec.label_entrar from _call_espiar_entrar_custom
        window hide
        $ avanzar_horario()
        $ mostrar_hud()
        return

    # Sin escena propia no se entra: se avisa y el jugador sigue mirando — no
    # se consume el horario. La accion ya aparece en gris (condicion_habilitada),
    # asi que llegar acá es raro; queda como red de seguridad.
    #
    # El texto va interpolado, asi que NO lo traduce el bloque de dialogo con
    # hash: lo traduce translate_string y el `old` vive en
    # tl/english/espiar_strings.rpy
    $ _esp_ent_msg = renpy.translate_string("(Contenido en desarrollo)")
    window show
    piensa "[_esp_ent_msg]"
    window hide
    return


# ── Salir ────────────────────────────────────────────────────────────────────
label accion_espiar_salir:

    $ _espiar_cerrar_ui()
    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    return
