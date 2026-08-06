################################################################################
## Sistema de Espiar en el Baño — Motor
################################################################################
## Minijuego de espiar por la puerta entreabierta cuando un NPC está en el baño.
##
## Cómo funciona:
##   - Al elegir "Espiar" en el menú del baño se sortea una SecuenciaEspiar del
##     catálogo del NPC (peso + condicion) y se muestra el screen del minijuego:
##     fondo arrastrable en horizontal (viewport) + imagen de puerta con rendija.
##   - Los botones son AccionLocacion globales (locacion_id=None) que solo se
##     ven mientras hay sesión activa; el panel de acciones del HUD mantiene
##     la estética del resto del juego.
##   - REQUISITO DE ACCESO: el NPC tiene que tener al menos ESPIAR_DESEO_MINIMO
##     de deseo. El minijuego es parte de la tensión ya establecida entre los
##     dos personajes, no un primer contacto: sin ese nivel la opción ni
##     siquiera aparece en el menú del baño.
##   - "Abrir más": 20% base + 10% por punto de destreza - 20% por apertura ya
##     lograda (mínimo 1%). Fallo → el NPC se da cuenta (label de descubierto).
##   - "Entrar" (destreza 10+): hoy avisa "contenido en desarrollo" y no avanza;
##     si la secuencia define label_entrar, salta a esa escena propia.
##   - "Salir": vuelve al pasillo. Toda salida del minijuego avanza 1 horario.
##
## Para AGREGAR contenido (ver espiar_violet.rpy como ejemplo):
##   - registrar_secuencia_espiar(SecuenciaEspiar(...))   → nueva secuencia
##   - registrar_espiar_npc(npc_id, label_primera_vez, reacciones) → reacciones
##   - SecuenciaEspiar(label_entrar=...) → escena propia al entrar
##   - SecuenciaEspiar(label_descubierto=...) → reacción especial al fallar
##   - SecuenciaEspiar(condicion=funcion_de_modulo) → secuencias de quest/evento

################################################################################
## Estado guardable
################################################################################

# Interruptor maestro del minijuego. Mientras esté en False, el botón "Espiar"
# del baño queda deshabilitado ("Contenido en desarrollo") en la versión jugable
# — todo el sistema sigue acá, poner True lo re-activa de una.
define ESPIAR_HABILITADO = True

# Sesión activa del minijuego (None = no está corriendo). Dict plano picklable:
# {"npc_id", "secuencia_id", "xoffset" (0, 100, 200, 300 px), "instancia"
#  ("mirilla" | "entrar")}
default espiar_sesion = None

# NPCs que ya descubrieron al jugador alguna vez: {npc_id: True}
default espiar_descubierto_npc = {}

# NPC objetivo al iniciar (lo setea interaccion_banio_ocupado)
default _espiar_npc_temp = None


################################################################################
## Clases y catálogo
################################################################################

init python:

    # Imagenes de puerta por defecto (stage 0 → estado1 ... stage 3 → estado4).
    # Una secuencia puede traer las suyas con puertas=[...].
    # Por ahora vacío — cada secuencia define sus propias puertas
    ESPIAR_PUERTAS_DEFAULT = []

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
    # Deseo minimo del NPC para que el minijuego este disponible. Es el
    # requisito de acceso: por debajo de esto la opcion "Espiar" no se ofrece.
    ESPIAR_DESEO_MINIMO = 20

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
            fondo_entrar: imagen de la instancia "entrar" (default: mismo fondo)
            label_entrar: si se define, "Entrar" salta a este label en vez de a
                          la instancia generica (escena propia de la secuencia)
            label_descubierto: si se define, reemplaza la reacción estándar al
                               ser descubierto durante esta secuencia
            puertas: lista de 4 imagenes de puerta propias (default compartidas)
            margen_drag: px arrastrables a cada lado (default ESPIAR_DRAG_MARGEN)
            peso: peso relativo en el sorteo aleatorio (default 1)
            condicion: funcion de modulo → bool; si falla, la secuencia no entra
                       al sorteo (permite secuencias de quest/evento)
        """
        def __init__(self, id, npc_id, fondo, nombre="",
                     fondo_entrar=None, label_entrar=None,
                     label_descubierto=None, puertas=None, margen_drag=None,
                     peso=1, condicion=None):
            self.id = id
            self.npc_id = npc_id
            self.nombre = nombre
            self.fondo = fondo
            self.fondo_entrar = fondo_entrar if fondo_entrar else fondo
            self.label_entrar = label_entrar
            self.label_descubierto = label_descubierto
            self.puertas = list(puertas) if puertas else None
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

        def puerta_por_stage(self, stage):
            puertas = self.puertas or ESPIAR_PUERTAS_DEFAULT
            return puertas[max(0, min(stage, len(puertas) - 1))]

    # Catálogo de secuencias por NPC. Vive en init (no se guarda): la sesión
    # solo referencia secuencias por id, igual que las quests con su catálogo.
    CATALOGO_ESPIAR = {}

    # Configuración de reacción al ser descubierto, por NPC:
    # {npc_id: {"label_primera_vez": str|None, "reacciones": [rango, ...]}}
    # Cada rango: {"min": 0, "max": 100, "amor": delta, "deseo": delta}
    # (claves opcionales; se evalua el deseo actual del NPC contra min/max)
    CONFIG_ESPIAR_NPC = {}

    def registrar_secuencia_espiar(secuencia):
        CATALOGO_ESPIAR.setdefault(secuencia.npc_id, [])
        CATALOGO_ESPIAR[secuencia.npc_id] = [
            s for s in CATALOGO_ESPIAR[secuencia.npc_id] if s.id != secuencia.id
        ] + [secuencia]

    def registrar_espiar_npc(npc_id, label_primera_vez=None, reacciones=None):
        CONFIG_ESPIAR_NPC[npc_id] = {
            "label_primera_vez": label_primera_vez,
            "reacciones": list(reacciones) if reacciones else [],
        }

    def obtener_secuencias_espiar(npc_id):
        """Secuencias del NPC cuya condicion se cumple ahora."""
        return [s for s in CATALOGO_ESPIAR.get(npc_id, []) if s.es_valida()]

    def npc_tiene_espiar(npc_id):
        """True si el NPC tiene al menos una secuencia espiable (habilita el botón)."""
        return bool(obtener_secuencias_espiar(npc_id))

    def npc_espiar_disponible(npc_id):
        """
        Requisito de acceso al minijuego: ademas de tener secuencias, el NPC
        tiene que llegar a ESPIAR_DESEO_MINIMO de deseo. El minijuego es parte
        de una tension ya establecida entre los dos personajes, asi que por
        debajo de ese umbral la opcion directamente no se ofrece.
        """
        if not npc_tiene_espiar(npc_id):
            return False
        return obtener_stat2(npc_id) >= ESPIAR_DESEO_MINIMO

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

    def espiar_prob_abrir():
        """20% base + 10% por destreza - 20% por cada 100px abierto, minimo 1%."""
        xoffset = store.espiar_sesion.get("xoffset", 0) if store.espiar_sesion else 0
        aperturas = xoffset // 100  # convertir px a número de aperturas
        destreza = getattr(store, 'mc_destreza', 0)
        return max(1, 20 + 10 * destreza - 20 * aperturas)

    def _espiar_reaccion_fallo(npc_id):
        """Rango de reacción que aplica segun el deseo actual del NPC."""
        conf = CONFIG_ESPIAR_NPC.get(npc_id, {})
        deseo = obtener_stat2(npc_id)
        for rango in conf.get("reacciones", []):
            if rango.get("min", 0) <= deseo <= rango.get("max", 100):
                return rango
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

    def _esp_nombre_abrir():
        """Etiqueta de "Abrir más" con el % de exito actual (cae 20% por stage)."""
        return u"%s (%d%%)" % (renpy.translate_string("Abrir más"), espiar_prob_abrir())

    # ── Condiciones de visibilidad de las acciones (funciones de modulo) ─────

    def _esp_acc_abrir_visible():
        s = getattr(store, 'espiar_sesion', None)
        return bool(s) and s.get("instancia") == "mirilla" and s.get("xoffset", 0) < 300

    # "Entrar" y "Sacar foto" se muestran SIEMPRE durante la mirilla; si no se
    # cumplen sus requisitos aparecen en gris (condicion_habilitada), para que
    # el jugador vea que la opción existe y qué le falta.

    def _esp_acc_entrar_visible():
        s = getattr(store, 'espiar_sesion', None)
        return bool(s) and s.get("instancia") == "mirilla"

    def _esp_acc_entrar_habilitada():
        return getattr(store, 'mc_destreza', 0) >= ESPIAR_DESTREZA_ENTRAR

    def _esp_acc_unirse_visible():
        s = getattr(store, 'espiar_sesion', None)
        return bool(s) and s.get("instancia") == "entrar"

    def _esp_acc_salir_visible():
        return bool(getattr(store, 'espiar_sesion', None))


################################################################################
## Acciones de locación del minijuego
################################################################################
## Globales (locacion_id=None) + condicion por sesión: solo aparecen durante el
## minijuego. obtener_acciones_locacion filtra para que, con sesión activa, el
## panel muestre EXCLUSIVAMENTE estas (ver actionsystem_core).

init 5 python:

    sistema_acciones.registrar_accion(AccionLocacion(
        id="espiar_abrir", nombre="Abrir más", icono=u"🚪",
        locacion_id=None, label_generico="accion_espiar_abrir",
        reseteo=None, condicion=_esp_acc_abrir_visible,
        color="#E65100", color_hover="#FF9800",
        nombre_dinamico=_esp_nombre_abrir,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="espiar_entrar", nombre="Entrar", icono=u"🚶",
        locacion_id=None, label_generico="accion_espiar_entrar",
        reseteo=None, condicion=_esp_acc_entrar_visible,
        condicion_habilitada=_esp_acc_entrar_habilitada,
        color="#8E24AA", color_hover="#AB47BC",
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="espiar_unirse", nombre="Unirse", icono=u"🤝",
        locacion_id=None, label_generico="accion_espiar_unirse",
        reseteo=None, condicion=_esp_acc_unirse_visible,
        color="#C62828", color_hover="#EF5350",
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="espiar_salir", nombre="Salir", icono=u"❌",
        locacion_id=None, label_generico="accion_espiar_salir",
        reseteo=None, condicion=_esp_acc_salir_visible,
        color="#37474F", color_hover="#546E7A",
    ))


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

        if espiar_sesion.get("instancia") == "entrar":
            # Instancia "entrar": fondo propio a pantalla completa
            add _esp_scr_sec.fondo_entrar

        else:
            # Mirilla: orden de capas (de atrás para adelante). Todas son
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
            # 11. Puerta frontal (desplazada por xoffset)
            $ _esp_scr_xoffset = espiar_sesion.get("xoffset", 0)
            add Transform("ducha_mg_puerta", xoffset=_esp_scr_xoffset)

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
        "xoffset": 0,
        "instancia": "mirilla",
    }
    show screen espiar_minijuego
    return


# ── Abrir más ────────────────────────────────────────────────────────────────
label accion_espiar_abrir:

    if not espiar_sesion:
        return

    $ _esp_pct_abrir = espiar_prob_abrir()

    if renpy.random.randint(1, 100) <= _esp_pct_abrir:
        # Éxito: la puerta se desplaza 100px a la derecha (dict nuevo, rollback-friendly)
        $ espiar_sesion = dict(espiar_sesion, xoffset=espiar_sesion.get("xoffset", 0) + 100)
        return

    # Fallo: el NPC se da cuenta
    jump espiar_descubierto


# ── Descubierto (fallo de Abrir más) ─────────────────────────────────────────
label espiar_descubierto:

    $ _esp_desc_sec = _espiar_secuencia_actual()
    $ _esp_desc_npc_id = espiar_sesion["npc_id"]
    $ _esp_desc_npc = obtener_npc(_esp_desc_npc_id)
    $ _esp_desc_nombre = _esp_desc_npc.nombre if _esp_desc_npc else _esp_desc_npc_id
    $ _esp_desc_conf = CONFIG_ESPIAR_NPC.get(_esp_desc_npc_id, {})

    # Cerrar el minijuego ANTES de la reacción — sin ningún mensaje intermedio,
    # el label de descubierto se dispara directo (ver _espiar_cerrar_ui).
    $ _espiar_cerrar_ui()

    if _esp_desc_sec and _esp_desc_sec.label_descubierto:
        # Reacción especial propia de la secuencia (quest/evento)
        call expression _esp_desc_sec.label_descubierto from _call_espiar_desc_secuencia

    elif not espiar_descubierto_npc.get(_esp_desc_npc_id) and _esp_desc_conf.get("label_primera_vez"):
        # Primera vez: secuencia especial del NPC — reemplaza la reacción por
        # deseo (sin resta ni suma de stats)
        $ espiar_descubierto_npc = dict(espiar_descubierto_npc, **{_esp_desc_npc_id: True})
        call expression _esp_desc_conf["label_primera_vez"] from _call_espiar_desc_primera_vez

    else:
        # Reacción estándar segun el deseo actual del NPC
        $ espiar_descubierto_npc = dict(espiar_descubierto_npc, **{_esp_desc_npc_id: True})
        $ _esp_desc_reaccion = _espiar_reaccion_fallo(_esp_desc_npc_id)
        if _esp_desc_reaccion:
            $ _esp_d_amor = _esp_desc_reaccion.get("amor", 0)
            $ _esp_d_deseo = _esp_desc_reaccion.get("deseo", 0)
            if _esp_d_amor:
                $ cambiar_stat1(_esp_desc_npc_id, _esp_d_amor)
            if _esp_d_deseo:
                $ cambiar_stat2(_esp_desc_npc_id, _esp_d_deseo)
            if _esp_d_amor < 0:
                "[_esp_desc_nombre] se enfadó contigo."
            elif _esp_d_deseo > 0:
                "A [_esp_desc_nombre] no pareció molestarle... al contrario."

    window hide
    $ avanzar_horario()
    $ mostrar_hud()
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

    # Instancia generica: TODAVIA NO IMPLEMENTADA. Avisa y deja al jugador en
    # la mirilla — no se entra ni se consume el horario. Cuando este lista, esto
    # vuelve a ser: espiar_sesion = dict(espiar_sesion, instancia="entrar")
    #
    # El texto va interpolado, asi que NO lo traduce el bloque de dialogo con
    # hash: lo traduce translate_string y el `old` vive en
    # tl/english/espiar_strings.rpy
    $ _esp_ent_msg = renpy.translate_string("(Contenido en desarrollo)")
    window show
    piensa "[_esp_ent_msg]"
    window hide
    return


# ── Unirse (instancia entrar) ────────────────────────────────────────────────
label accion_espiar_unirse:

    window show
    piensa "(Contenido en desarrollo)"
    window hide
    return




# ── Salir ────────────────────────────────────────────────────────────────────
label accion_espiar_salir:

    $ _espiar_cerrar_ui()
    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    return
