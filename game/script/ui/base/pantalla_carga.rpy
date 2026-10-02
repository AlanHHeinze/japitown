################################################################################
## Splash + Pantalla de carga
################################################################################
## Al abrir el juego:
##   1. Logo de la empresa durante 2 segundos.
##   2. Pantalla de carga con "Cargando/Loading" + contador % mientras se
##      precargan las imagenes al cache (asi no aparecen pixeladas al mostrarse
##      por primera vez).
##
## OJO — limite real del cache: config.image_cache_size_mb son 400 MB de texturas
## YA DECODIFICADAS (un fondo 1920x1080 ocupa ~8 MB en memoria, no lo que pesa el
## archivo). No entran las 691 imagenes del juego. Y si la precarga desborda el
## cache, Ren'Py descarta la cola entera (im.py: preloads.clear()), con lo que se
## perderia todo lo precargado. Por eso la carga:
##   - va por lotes, esperando a que cada lote termine antes del siguiente, y
##   - corta apenas el cache llega a CARGA_TOPE_CACHE.
## Lo precargado es lo que se ve al principio; el resto lo carga el juego solo,
## que en web ya no descarga nada porque todo viene dentro de game.zip.

image carga_empresa = "images/carga/empresa.jpg"
image carga_loading = "images/carga/loading.jpg"

# Progreso visible del contador (0-100)
default _carga_pct = 0

# Fraccion del cache que se permite llenar antes de cortar la precarga.
# Se deja margen para que el juego siga cacheando durante la partida.
define CARGA_TOPE_CACHE = 0.75

# Imagenes por lote. Lotes chicos = el contador se mueve mas fluido.
define CARGA_LOTE = 6


init python:

    def _carga_cache():
        """El cache de imagenes de Ren'Py."""
        import renpy.display.im as _im
        return _im.cache

    def carga_lista_archivos():
        """
        Imagenes a precargar, en orden de prioridad: primero lo que se ve al
        arrancar (hud, gui, intro), despues fondos y sprites.
        Se excluyen las de la propia pantalla de carga y las de test.
        """
        exts = (".webp", ".jpg", ".jpeg", ".png")
        try:
            todos = [f for f in renpy.list_files() if f.lower().endswith(exts)]
        except Exception:
            return []

        def _vale(f):
            if not f.startswith("images/"):
                return False
            if f.startswith("images/test/") or f.startswith("images/carga/"):
                return False
            return True

        todos = [f for f in todos if _vale(f)]

        # Prioridad: menor numero = se precarga antes
        def _prio(f):
            if f.startswith("images/hud/"):
                return 0
            if f.startswith("images/intro/"):
                return 1
            if f.startswith("images/characters/"):
                return 2
            if f.startswith("images/bg/"):
                return 3
            if f.startswith("images/chat/"):
                return 4
            return 5

        todos.sort(key=_prio)
        return todos

    def carga_cache_lleno():
        """True si el cache ya llego al tope permitido."""
        try:
            c = _carga_cache()
            if not c.cache_limit:
                return False
            return c.get_total_size() >= c.cache_limit * CARGA_TOPE_CACHE
        except Exception:
            return True  # ante la duda, cortar (nunca colgar la carga)

    def carga_encolar_lote(archivos, desde):
        """Encola un lote de imagenes al cache. Devuelve el indice siguiente."""
        import renpy.display.im as _im
        c = _carga_cache()
        hasta = min(desde + CARGA_LOTE, len(archivos))
        for i in range(desde, hasta):
            try:
                c.preload_image(_im.image(archivos[i]))
            except Exception:
                pass  # una imagen rota no debe frenar la carga
        return hasta

    def carga_lote_terminado():
        """True cuando el cache termino de procesar la cola pendiente."""
        try:
            return _carga_cache().done()
        except Exception:
            return True


################################################################################
## Pantalla de carga
################################################################################

screen pantalla_carga():
    zorder 100

    add "carga_loading"

    # Bloque centrado en X que TERMINA 150 px por encima del borde inferior.
    # Se ancla por abajo (yanchor 1.0) a proposito: asi el contador nunca se sale
    # de pantalla si mas adelante se cambia el tamaño del texto — el bloque crece
    # hacia arriba en vez de hacia abajo.
    vbox:
        xalign 0.5
        ypos 930          # 1080 - 150
        yanchor 1.0
        spacing 10

        text _("Cargando"):
            xalign 0.5
            size 92
            color "#FFFFFF"
            outlines [(4, "#000000", 0, 0)]

        text "[_carga_pct]%":
            xalign 0.5
            size 68
            color "#FFFFFF"
            outlines [(4, "#000000", 0, 0)]


################################################################################
## Splashscreen — lo llama Ren'Py automaticamente al iniciar el juego
################################################################################

label splashscreen:

    scene black
    with None

    # 1. Logo de la empresa (2 segundos)
    scene carga_empresa
    with dissolve
    pause 2.0

    # 2. Pantalla de carga con precarga real
    scene carga_loading
    with dissolve

    $ store._carga_pct = 0

    show screen pantalla_carga

    # TODO EL BUCLE EN UN SOLO BLOQUE PYTHON, a proposito.
    #
    # El watchdog de Ren'Py ("Exception: Possible infinite loop",
    # execution.py:check_infinite_loop) cuenta STATEMENTS de Ren'Py: cada 1000
    # revienta si pasaron mas de 50 s (en un build) desde el ultimo frame de
    # interaccion. Un bloque `python:` es UN statement, de vueltas que de
    # adentro — asi que acá adentro el contador no se mueve y el watchdog no
    # tiene donde saltar.
    #
    # La version anterior era un `while` de Ren'Py con `pause 0.01` adentro
    # (~15.000 statements) y un `renpy.not_infinite_loop(30)` por lote. No
    # alcanzaba: cada `pause` vuelve a fijar el plazo en 50 s (es una
    # asignacion, no un maximo), y cuando el navegador CONGELA la pestaña
    # (segundo plano largo, minimizar, la maquina que se duerme) la `pause` en
    # curso vuelve con el plazo vencido; si el contador cruzaba el 1000 en los
    # tres statements que iban hasta la siguiente `pause`, saltaba. Un jugador
    # nuevo, en su primera carga, con la pantalla roja. Sentry S11 (variante
    # precarga): 0.1.8f y 0.1.9.1.
    #
    # `renpy.pause` desde Python es la misma interaccion que el statement,
    # asi que el contador de la screen se sigue redibujando igual.
    python:
        _carga_archivos = carga_lista_archivos()
        _carga_total = len(_carga_archivos)
        _carga_idx = 0

        while _carga_idx < _carga_total:
            # Cortar si el cache llego al tope: seguir solo descartaria la cola
            if carga_cache_lleno():
                _carga_idx = _carga_total
            else:
                _carga_idx = carga_encolar_lote(_carga_archivos, _carga_idx)

                # Esperar a que el lote se decodifique antes de seguir, asi el
                # contador refleja carga real y no solo el encolado.
                _carga_espera = 0
                while not carga_lote_terminado() and _carga_espera < 40:
                    _carga_espera += 1
                    renpy.pause(0.01)

            store._carga_pct = min(100, int(_carga_idx * 100 / _carga_total))
            renpy.pause(0.01)

        store._carga_pct = 100
        renpy.pause(0.3)

    hide screen pantalla_carga
    scene black
    with dissolve

    return
