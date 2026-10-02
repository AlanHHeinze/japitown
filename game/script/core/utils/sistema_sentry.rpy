################################################################################
## Integración con Sentry (captura automática de excepciones)
################################################################################
## Envía cada excepción no controlada a Sentry para agregarlas y deduplicarlas
## automáticamente (en vez de recibir cientos de reportes sueltos por Discord).
##
## NO usa el sentry-sdk de Python: en el build web (Emscripten/wasm) no hay
## threads ni sockets, así que el SDK no funciona. En su lugar arma el "envelope"
## a mano y lo manda con renpy.fetch, que anda igual en web y escritorio.
##
## Se engancha en el flujo de error que YA existe (sistema_reporte_errores.rpy):
## el label _jp_error_context llama a jp_sentry_capturar() antes de mostrar la
## pantalla. Reusa el short/full/contexto que ese sistema ya calcula.
##
## Para desactivar: JP_SENTRY_ENABLED = False.
## Para volver a envío manual (solo con botón): JP_SENTRY_AUTO = False.
################################################################################

init python:

    import json as _sentry_json
    import time as _sentry_time
    import uuid as _sentry_uuid
    import re as _sentry_re
    # builtins: para usar el set() nativo de Python en vez del RevertableSet que
    # el store de Ren'Py pone bajo el nombre `set` (ver _jp_sentry_marcar_enviado).
    import builtins as _sentry_builtins

    # DSN del proyecto (Settings → Projects → japitown → Client Keys).
    JP_SENTRY_DSN = "https://2c52aabfb9d63edc6419661323a5d475@o4511656803041280.ingest.us.sentry.io/4511796319551488"

    JP_SENTRY_ENABLED = True    # interruptor maestro
    JP_SENTRY_AUTO = True       # True = envía solo, sin que el jugador toque nada

    # Derivados del DSN (clave pública + endpoint de ingesta "envelope").
    _JP_SENTRY_KEY = "2c52aabfb9d63edc6419661323a5d475"
    _JP_SENTRY_ENVELOPE = "https://o4511656803041280.ingest.us.sentry.io/api/4511796319551488/envelope/"

    # Dedup por sesión: no reenviar el mismo error N veces si el jugador sigue
    # tocando "Continuar" sobre la misma excepción.
    #
    # OJO — POR QUE VA EN renpy.session Y NO EN UN set() DEL STORE:
    # en el store de Ren'Py, `set` ES `RevertableSet` (minstore.py:51), o sea que
    # sus mutaciones las trackea el rollback. El handler de errores corre en un
    # contexto nuevo (`renpy.call_in_new_context`), y al salir de ahi el rollback
    # DESHACIA el .add() — el deduplicador quedaba vacio y cada crash repetido se
    # reenviaba. En Sentry se veia como ~6 eventos por issue.
    #
    # `renpy.session` es un dict plano de Python: no se guarda, no lo toca el
    # rollback, y se limpia solo al reiniciar el juego. Que es exactamente el
    # alcance que queremos para un dedup "por sesion".
    _JP_SENTRY_SESSION_KEY = "jp_sentry_enviados"

    def _jp_sentry_ya_enviado(clave):
        """True si esta clase de error ya se mando en esta sesion."""
        try:
            return clave in renpy.session.get(_JP_SENTRY_SESSION_KEY, ())
        except Exception:
            return False

    def _jp_sentry_marcar_enviado(clave):
        """Registra la clave como ya enviada (fuera del rollback)."""
        try:
            enviados = renpy.session.get(_JP_SENTRY_SESSION_KEY)
            if enviados is None:
                # set() nativo, no el RevertableSet del store.
                enviados = _sentry_builtins.set()
                renpy.session[_JP_SENTRY_SESSION_KEY] = enviados
            enviados.add(clave)
        except Exception:
            pass

    # Largo del id de instalacion, en caracteres hex. 12 = 48 bits: con miles
    # de jugadores la probabilidad de que dos coincidan es despreciable, y
    # entra legible en el reporte de Discord (donde tiene que poder leerse y
    # buscarse a mano).
    _JP_INSTALACION_LARGO = 12

    def jp_instalacion_id():
        """
        Id ANONIMO y estable de esta instalacion del juego.

        PARA QUE: sin un `user.id`, Sentry no puede contar personas — todos los
        issues decian "Users Impacted: 0" y habia que adivinar por pais y
        navegador si 46 eventos eran un jugador insistiendo o cuarenta y seis
        jugadores distintos (revision del 2026-09-23: eran uno). Con esto, el
        dashboard dice cuanta gente toca cada error, que es lo unico que
        permite priorizar de verdad.

        QUE ES Y QUE NO ES: un uuid4 al azar, generado en la maquina del
        jugador la primera vez y guardado en `persistent`. No sale de ningun
        dato de la persona, no viaja con nada mas, y no sirve para reconocerlo
        en ningun otro lado. Borrar los datos del navegador (en web) o el
        persistent (en escritorio) lo cambia por otro — es a proposito: el id
        identifica UNA instalacion, no a alguien.

        VA TAMBIEN EN EL REPORTE DE DISCORD (sistema_reporte_errores.rpy), y
        ese es medio punto del asunto: con el mismo id en los dos lados, un
        feedback que llega por Discord se puede cruzar con los crashes que esa
        misma instalacion mando a Sentry.
        """
        try:
            _id = getattr(persistent, "jp_instalacion_id", None)
            if not _id:
                _id = _sentry_uuid.uuid4().hex[:_JP_INSTALACION_LARGO]
                persistent.jp_instalacion_id = _id
            return str(_id)
        except Exception:
            # Sin persistent (caso raro, y en web puede fallar la primera
            # escritura): uno de sesion, asi el evento igual trae algo con que
            # agrupar. El prefijo avisa que no sobrevive al reinicio.
            try:
                _id = renpy.session.get("jp_instalacion_id")
                if not _id:
                    _id = "sesion_" + _sentry_uuid.uuid4().hex[:8]
                    renpy.session["jp_instalacion_id"] = _id
                return _id
            except Exception:
                return "desconocido"

    def _jp_sentry_entorno():
        """
        Distingue web de escritorio para taggear el evento — y "dev" cuando
        corre desde el SDK (config.developer, que en un build es False): lo que
        revienta en la maquina de desarrollo, incluidos los archivos temporales
        de un lint, llegaba a Sentry mezclado con lo de los jugadores (evento
        1d2daf07, 2026-09-17). Con environment=dev se filtra de un click.
        """
        try:
            if config.developer:
                return "dev"
            return "web" if jp_es_web() else "desktop"
        except Exception:
            return "desconocido"

    def _jp_sentry_tags():
        """Mismos datos de contexto que el reporte de Discord, como tags de Sentry
        (así se puede filtrar por locación / horario / día en el dashboard)."""
        tags = {}
        try:
            loc = store.sistema_locaciones.locacion_actual
            tags["loc"] = loc.id if loc else "?"
        except Exception:
            pass
        for var in ("dias_totales", "dia_semana_actual", "horario_actual"):
            try:
                tags[var] = str(getattr(store, var, "?"))
            except Exception:
                pass
        try:
            tags["renpy"] = getattr(renpy, "version_only", "?")
        except Exception:
            pass

        # --- Contexto de plataforma -------------------------------------------
        # Sin esto no se puede distinguir un crash de GPU movil de uno de
        # escritorio: Sentry solo reporta "Emscripten wasm32" para TODO lo web.
        # Fue el dato que falto para decidir sobre S04/S06 (renderer muerto).
        try:
            if renpy.variant("small") or renpy.variant("phone"):
                tags["dispositivo"] = "movil"
            elif renpy.variant("tablet") or renpy.variant("medium"):
                tags["dispositivo"] = "tablet"
            elif renpy.variant("web"):
                tags["dispositivo"] = "escritorio_web"
            else:
                tags["dispositivo"] = "escritorio"
        except Exception:
            pass

        # Renderer realmente en uso (lo setea set_mode). Clave para los errores
        # de GL: dice si corrio gl2, y en web si hubo fallback.
        try:
            tags["renderer"] = str(renpy.session.get("renderer", "?"))
        except Exception:
            pass

        # Ultimo disparador del game_loop que salto (diagnostico de S11:
        # "Possible infinite loop"). Vacio = la vuelta se completo bien; con
        # valor = ese disparador estaba activo cuando reventó.
        try:
            _glt = getattr(store, "_gl_ultimo_trigger", "")
            if _glt:
                tags["gl_trigger"] = str(_glt)
        except Exception:
            pass

        # Quien juega esta partida (mismo helper que el reporte de Discord).
        # Va como TAG y no dentro del fingerprint: identifica al que reporta
        # sin partir en dos el agrupamiento de un mismo error.
        try:
            tags["jugador"] = jp_jugador_actual()[:60]
        except Exception:
            pass

        # Ultima quest activada (ver activar_quest en questsystem_core).
        try:
            _qa = getattr(store, "_quest_activada_ultima", "")
            if _qa:
                tags["quest_activada"] = str(_qa)
        except Exception:
            pass

        # Navegador (solo web). Recortado: solo interesa identificar el motor.
        try:
            if renpy.emscripten:
                import emscripten
                ua = emscripten.run_script_string("navigator.userAgent") or ""
                tags["navegador"] = ua[:120]
        except Exception:
            pass

        return tags

    # Linea de excepcion de Python: un identificador (posiblemente con puntos)
    # al inicio de linea, con mensaje opcional. Matchea tanto
    # "AttributeError: 'NoneType' object has..." como
    # "renpy.gl2.gl2shader.ShaderError" (sin mensaje).
    _JP_SENTRY_RE_EXC = _sentry_re.compile(
        r'^([A-Za-z_][A-Za-z0-9_.]*)(?::\s*(.*))?$'
    )

    def _jp_sentry_parse(full, short):
        """
        Extrae (tipo, mensaje) de la excepción del traceback.

        OJO — por que NO alcanza con tomar la ultima linea: Ren'Py agrega DESPUES
        del traceback un bloque de plataforma/version/fecha:

            AttributeError: 'NoneType' object has no attribute 'update'

            Emscripten-3.1.67-wasm32-32bit wasm32
            Ren'Py 8.5.2.26010301
            Japitown 0.1.8f
            Thu Jul 30 22:07:51 2026      <- ultima linea no vacia

        La version anterior agarraba esa ultima linea, con lo cual el tipo era
        siempre "Error" y el mensaje era el TIMESTAMP. Como el fingerprint se
        arma con eso, cada evento tenia una huella unica y Sentry abria un issue
        nuevo por cada ocurrencia en vez de agruparlas (bug real, visible en el
        dashboard como `Fingerprint values: Error, Thu Jul 30 22:07:51 #`).

        Ahora se busca hacia atras la ultima linea que REALMENTE parezca una
        excepcion: sin indentar (los frames y el codigo van indentados) y con
        forma de identificador. El bloque de metadata no matchea porque sus
        lineas tienen espacios, guiones o apostrofes antes de cualquier ':'.
        """
        texto = full or short or ""
        tipo, valor = "Error", ""

        for l in reversed(texto.splitlines()):
            linea = l.rstrip()
            if not linea or linea[0].isspace():
                continue                      # frames y codigo van indentados
            if linea.startswith(("File ", "Traceback")):
                continue
            m = _JP_SENTRY_RE_EXC.match(linea)
            if not m:
                continue
            tipo = m.group(1)
            valor = (m.group(2) or "").strip()
            break

        return tipo, valor

    def _jp_sentry_frames(full):
        """Parsea las líneas 'File "...", line N, in ...' del traceback completo a
        frames de Sentry. Incluye tanto los frames de Python como los 'script call'
        de Ren'Py. El orden del traceback (viejo→nuevo) ya es el que espera Sentry."""
        frames = []
        pat = _sentry_re.compile(r'File "(.+?)", line (\d+), in (.+)')
        for m in pat.finditer(full or ""):
            try:
                frames.append({
                    "filename": m.group(1),
                    "lineno": int(m.group(2)),
                    "function": m.group(3).strip(),
                })
            except Exception:
                pass
        return frames

    def _jp_sentry_archivo_juego(full):
        """
        El ultimo archivo del JUEGO (game/...) que aparece en el traceback, sin
        ruta ni extension, o "". Es donde estaba parado el script cuando salto
        el error — para los errores cuyo mensaje no dice nada del lugar.
        """
        try:
            _archivos = _sentry_re.findall(r'File "(?://)?game/([^"]+?)\.rpyc?"', full or "")
            return _archivos[-1].rsplit("/", 1)[-1] if _archivos else ""
        except Exception:
            return ""

    def _jp_sentry_fingerprint(tipo, valor, full=""):
        """Agrupa por tipo + mensaje normalizado. Normaliza direcciones de memoria
        y números largos para que la misma clase de error caiga en un solo issue
        aunque los frames acumulados varíen (los stacks vienen inflados).

        "Possible infinite loop." lleva ademas el archivo del juego donde salto:
        el mensaje es el mismo para cualquier bucle, y con eso la variante de la
        precarga (pantalla_carga) y la del game_loop (intro_main), que son dos
        problemas distintos, caian en el mismo issue (S11)."""
        norm = _sentry_re.sub(r'0x[0-9a-fA-F]+', '0xADDR', valor or "")
        norm = _sentry_re.sub(r'\b\d{4,}\b', '#', norm)
        fp = [tipo, norm]
        if norm.startswith("Possible infinite loop"):
            _arch = _jp_sentry_archivo_juego(full)
            if _arch:
                fp.append(_arch)
        return fp

    def jp_sentry_capturar(short, full):
        """
        Envía una excepción a Sentry. Silenciosa y a prueba de fallos: cualquier
        problema se traga (nunca debe romper el flujo de error ni tapar la
        pantalla de reporte). Deduplica por sesión.
        """
        if not (JP_SENTRY_ENABLED and JP_SENTRY_DSN):
            return
        try:
            tipo, valor = _jp_sentry_parse(full, short)
            fp = _jp_sentry_fingerprint(tipo, valor, full)
            clave = "|".join(fp)
            if _jp_sentry_ya_enviado(clave):
                return

            event_id = _sentry_uuid.uuid4().hex
            evento = {
                "event_id": event_id,
                "timestamp": _sentry_time.time(),
                "platform": "python",
                "level": "error",
                "logger": "renpy",
                "release": str(getattr(config, "version", "?")),
                "environment": _jp_sentry_entorno(),
                # Sin esto Sentry cuenta eventos pero no personas. El id es
                # anonimo y por instalacion — ver jp_instalacion_id().
                "user": {"id": jp_instalacion_id()},
                "tags": _jp_sentry_tags(),
                "fingerprint": fp,
                "exception": {"values": [{
                    "type": tipo,
                    "value": (valor or "")[:500],
                    "stacktrace": {"frames": _jp_sentry_frames(full)},
                }]},
                "extra": {
                    # Traceback completo legible dentro del issue (la cola es
                    # donde está el error real).
                    "traceback_full": (full or "")[-8000:],
                    "traceback_short": (short or "")[:2000],
                    # Que estaba procesando el controlador de quests: la
                    # restriccion puesta, las reservas y el estado de cada
                    # quest viva. Es extra y no tag: es multilinea y no tiene
                    # que influir en el agrupamiento.
                    "controlador": jp_controlador_actual(12)[:4000],
                },
            }

            # Se marca ANTES de enviar: si la red esta lenta o falla, no
            # queremos reintentar en bucle sobre el mismo error — el jugador
            # que sigue tocando "Continuar" generaria una avalancha.
            _jp_sentry_marcar_enviado(clave)

            _args, _kwargs = _jp_sentry_armar(evento, timeout=8)
            renpy.fetch(*_args, **_kwargs)
        except Exception:
            pass

    def _jp_sentry_armar(evento, timeout=8):
        """Arma (url, kwargs) del envelope para pasarle a renpy.fetch."""
        payload = _sentry_json.dumps(evento).encode("utf-8")
        header = _sentry_json.dumps({"event_id": evento["event_id"], "dsn": JP_SENTRY_DSN})
        item = _sentry_json.dumps({
            "type": "event",
            "content_type": "application/json",
            "length": len(payload),
        })
        cuerpo = header.encode("utf-8") + b"\n" + item.encode("utf-8") + b"\n" + payload + b"\n"
        return (_JP_SENTRY_ENVELOPE,), dict(
            data=cuerpo,
            content_type="application/x-sentry-envelope",
            params={"sentry_key": _JP_SENTRY_KEY, "sentry_version": "7"},
            timeout=timeout,
            result="text",
        )

    def jp_forzar_error_prueba():
        """
        Lanza una excepción REAL no controlada (a diferencia de un `raise` en la
        consola, que la consola atrapa por su cuenta). Al llamarse desde una
        acción de screen, la excepción sube al manejador de Ren'Py →
        config.exception_handler → pantalla de error → envío automático a Sentry.
        Sirve para probar el pipeline completo en cualquier build, incluido web.
        """
        raise Exception("Error de prueba forzado desde el panel de cheats (Sentry)")

    def jp_sentry_test():
        """
        Prueba MANUAL del transporte, desde la consola (Shift+O):

            jp_sentry_test()

        A diferencia de jp_sentry_capturar, NO se traga los errores: si algo
        falla (CORS, red, DSN) te muestra el error real. Si funciona, devuelve
        la respuesta de Sentry (un id) y avisa con renpy.notify.
        """
        event_id = _sentry_uuid.uuid4().hex
        evento = {
            "event_id": event_id,
            "timestamp": _sentry_time.time(),
            "platform": "python",
            "level": "error",
            "logger": "renpy",
            "release": str(getattr(config, "version", "?")),
            "environment": _jp_sentry_entorno(),
            "tags": _jp_sentry_tags(),
            "exception": {"values": [{
                "type": "PruebaSentry",
                "value": "prueba manual de transporte",
            }]},
        }
        args, kwargs = _jp_sentry_armar(evento, timeout=15)
        resultado = renpy.fetch(*args, **kwargs)
        try:
            renpy.notify("Sentry OK: " + str(resultado)[:80])
        except Exception:
            pass
        return resultado
