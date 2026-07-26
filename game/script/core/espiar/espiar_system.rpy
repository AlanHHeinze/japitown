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
##   - "Abrir más": 20% base + 10% por punto de destreza - 20% por apertura ya
##     lograda (mínimo 1%). Fallo → el NPC se da cuenta (label de descubierto).
##   - "Entrar" (destreza 10+): pasa a la instancia "entrar" (fondo propio y
##     botones Unirse/Salir), o al label_entrar propio de la secuencia si tiene.
##   - "Sacar foto" (inteligencia 5+): probabilidad segun apertura (1/33/66/99).
##     Bien o mal, termina el minijuego. Las fotos se otorgan en orden y van a
##     la galería del celular al completar la lista de la secuencia.
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
define ESPIAR_HABILITADO = False

# Sesión activa del minijuego (None = no está corriendo). Dict plano picklable:
# {"npc_id", "secuencia_id", "stage" (0-3 aperturas logradas), "instancia"
#  ("mirilla" | "entrar")}
default espiar_sesion = None

# Fotos otorgadas por secuencia: {secuencia_id: cantidad}
default espiar_fotos_obtenidas = {}

# Secuencias cuya lista de fotos ya se completó y pasó a la galería
default espiar_secuencias_completadas = []

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
    ESPIAR_PUERTAS_DEFAULT = [
        "images/minijuegos/ducha_test/secuencias_placeholder_puerta_estado1.png",
        "images/minijuegos/ducha_test/secuencias_placeholder_puerta_estado2.png",
        "images/minijuegos/ducha_test/secuencias_placeholder_puerta_estado3.png",
        "images/minijuegos/ducha_test/secuencias_placeholder_puerta_estado4.png",
    ]

    # Probabilidad de foto buena segun aperturas logradas (stage 0..3)
    ESPIAR_PROB_FOTO = [1, 33, 66, 99]

    # Cuánto se puede arrastrar el fondo hacia cada lado desde su posición
    # inicial, en px. El fondo se muestra a tamaño nativo (sin zoom): el margen
    # se logra dándole al viewport un contenido más ancho que la pantalla, con
    # la imagen centrada. Solo hay desplazamiento horizontal — el alto del
    # contenido es igual al de la pantalla, asi que no hay scroll vertical.
    ESPIAR_DRAG_MARGEN = 200

    # Requisitos de stats para habilitar botones (si no se cumplen, el botón
    # igual se muestra, en gris)
    ESPIAR_DESTREZA_ENTRAR = 10
    ESPIAR_INTELIGENCIA_FOTO = 5

    class SecuenciaEspiar(object):
        """
        Una escena espiable de un NPC en el baño.

        Args:
            id: identificador unico (ej: "violet_espiar_ducha")
            npc_id: NPC al que pertenece
            nombre: nombre descriptivo (para debug/menus futuros)
            fondo: imagen de fondo de la mirilla (tamaño nativo, drag horizontal)
            fotos: lista de {"ruta": str, "descripcion": str} que se otorgan en
                   orden al sacar fotos buenas; al completarla van a la galería
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
        def __init__(self, id, npc_id, fondo, nombre="", fotos=None,
                     fondo_entrar=None, label_entrar=None,
                     label_descubierto=None, puertas=None, margen_drag=None,
                     peso=1, condicion=None):
            self.id = id
            self.npc_id = npc_id
            self.nombre = nombre
            self.fondo = fondo
            self.fotos = list(fotos) if fotos else []
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
        """20% base + 10% por destreza - 20% por apertura lograda, minimo 1%."""
        aperturas = store.espiar_sesion["stage"] if store.espiar_sesion else 0
        destreza = getattr(store, 'mc_destreza', 0)
        return max(1, 20 + 10 * destreza - 20 * aperturas)

    def espiar_prob_foto():
        stage = store.espiar_sesion["stage"] if store.espiar_sesion else 0
        return ESPIAR_PROB_FOTO[max(0, min(stage, len(ESPIAR_PROB_FOTO) - 1))]

    def _espiar_fotos_restantes(secuencia):
        if not secuencia or not secuencia.fotos:
            return 0
        obtenidas = store.espiar_fotos_obtenidas.get(secuencia.id, 0)
        return max(0, len(secuencia.fotos) - obtenidas)

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
        return bool(s) and s.get("instancia") == "mirilla" and s.get("stage", 0) < 3

    # "Entrar" y "Sacar foto" se muestran SIEMPRE durante la mirilla; si no se
    # cumplen sus requisitos aparecen en gris (condicion_habilitada), para que
    # el jugador vea que la opción existe y qué le falta.

    def _esp_acc_entrar_visible():
        s = getattr(store, 'espiar_sesion', None)
        return bool(s) and s.get("instancia") == "mirilla"

    def _esp_acc_entrar_habilitada():
        return getattr(store, 'mc_destreza', 0) >= ESPIAR_DESTREZA_ENTRAR

    def _esp_acc_foto_visible():
        s = getattr(store, 'espiar_sesion', None)
        return bool(s) and s.get("instancia") == "mirilla"

    def _esp_acc_foto_habilitada():
        if getattr(store, 'mc_inteligencia', 0) < ESPIAR_INTELIGENCIA_FOTO:
            return False
        return _espiar_fotos_restantes(_espiar_secuencia_actual()) > 0

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
        id="espiar_foto", nombre="Sacar foto", icono=u"📷",
        locacion_id=None, label_generico="accion_espiar_foto",
        reseteo=None, condicion=_esp_acc_foto_visible,
        condicion_habilitada=_esp_acc_foto_habilitada,
        color="#1565C0", color_hover="#1E88E5",
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
            # Mirilla: fondo a tamaño nativo, arrastrable SOLO en horizontal y
            # como máximo `margen` px hacia cada lado desde su posición inicial.
            #
            # Se consigue con el clamp propio del viewport en vez de calcular
            # límites a mano: el contenido es `margen` px más ancho que la
            # pantalla de cada lado y la imagen va centrada dentro. Asi el
            # recorrido total es 2*margen y `xinitial 0.5` arranca justo en el
            # medio (imagen en su posición nativa). El alto del contenido es
            # igual al de la pantalla, por lo que no hay recorrido vertical y
            # el arrastre en Y no hace nada. Funciona con mouse y touch.
            $ _esp_scr_margen = _esp_scr_sec.obtener_margen_drag()

            viewport:
                xysize (1920, 1080)
                draggable True
                xinitial 0.5

                fixed:
                    xysize (1920 + 2 * _esp_scr_margen, 1080)
                    add _esp_scr_sec.fondo xpos _esp_scr_margen ypos 0

            # Puerta con rendija transparente (no captura el mouse: el drag
            # pasa a traves hacia el viewport)
            add _esp_scr_sec.puerta_por_stage(espiar_sesion.get("stage", 0))

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
        "stage": 0,
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
        # Éxito: la puerta se abre un paso mas (dict nuevo, rollback-friendly)
        $ espiar_sesion = dict(espiar_sesion, stage=espiar_sesion["stage"] + 1)
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

    # Instancia generica: cambia el fondo y los botones (Unirse / Salir)
    $ espiar_sesion = dict(espiar_sesion, instancia="entrar")
    return


# ── Unirse (instancia entrar) ────────────────────────────────────────────────
label accion_espiar_unirse:

    window show
    piensa "(Contenido en desarrollo)"
    window hide
    return


# ── Sacar foto ───────────────────────────────────────────────────────────────
label accion_espiar_foto:

    if not espiar_sesion:
        return

    $ _esp_foto_sec = _espiar_secuencia_actual()
    $ _esp_foto_npc_id = espiar_sesion["npc_id"]
    $ _esp_foto_exito = renpy.random.randint(1, 100) <= espiar_prob_foto()

    # Bien o mal, sacar la foto termina el minijuego
    $ _espiar_cerrar_ui()

    window show

    if _esp_foto_exito and _esp_foto_sec:
        # Otorgar la siguiente foto de la lista de la secuencia
        $ _esp_foto_idx = espiar_fotos_obtenidas.get(_esp_foto_sec.id, 0)
        if _esp_foto_idx < len(_esp_foto_sec.fotos):
            $ espiar_fotos_obtenidas = dict(espiar_fotos_obtenidas, **{_esp_foto_sec.id: _esp_foto_idx + 1})

            # Al completar la lista, todas las fotos pasan a la galería
            if _esp_foto_idx + 1 >= len(_esp_foto_sec.fotos) and _esp_foto_sec.id not in espiar_secuencias_completadas:
                python:
                    for _esp_f in _esp_foto_sec.fotos:
                        sistema_mensajes.agregar_foto_galeria(
                            _esp_f["ruta"], _esp_foto_npc_id,
                            _esp_f.get("descripcion", ""))
                    espiar_secuencias_completadas = espiar_secuencias_completadas + [_esp_foto_sec.id]

        piensa "Pude conseguir una buena foto."
    else:
        piensa "La foto no salió bien, debería intentarlo en otro momento."

    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    return


# ── Salir ────────────────────────────────────────────────────────────────────
label accion_espiar_salir:

    $ _espiar_cerrar_ui()
    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    return
