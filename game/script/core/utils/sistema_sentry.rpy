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

    # DSN del proyecto (Settings → Projects → japitown → Client Keys).
    JP_SENTRY_DSN = "https://2c52aabfb9d63edc6419661323a5d475@o4511656803041280.ingest.us.sentry.io/4511796319551488"

    JP_SENTRY_ENABLED = True    # interruptor maestro
    JP_SENTRY_AUTO = True       # True = envía solo, sin que el jugador toque nada

    # Derivados del DSN (clave pública + endpoint de ingesta "envelope").
    _JP_SENTRY_KEY = "2c52aabfb9d63edc6419661323a5d475"
    _JP_SENTRY_ENVELOPE = "https://o4511656803041280.ingest.us.sentry.io/api/4511796319551488/envelope/"

    # Dedup por sesión: no reenviar el mismo error N veces si el jugador sigue
    # tocando "Continuar" sobre la misma excepción. (No se guarda: prefijo "_".)
    _jp_sentry_enviados = set()

    def _jp_sentry_entorno():
        """Distingue web de escritorio para taggear el evento."""
        try:
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
        return tags

    def _jp_sentry_parse(full, short):
        """Extrae tipo y mensaje de la excepción de la última línea del traceback
        (ej: 'renpy.script.LabelNotFound: could not find label ...')."""
        linea = ""
        for l in reversed((full or short or "").splitlines()):
            if l.strip():
                linea = l.strip()
                break
        tipo, valor = "Error", linea
        if ": " in linea:
            tipo, valor = linea.split(": ", 1)
        elif linea:
            valor = linea
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

    def _jp_sentry_fingerprint(tipo, valor):
        """Agrupa por tipo + mensaje normalizado. Normaliza direcciones de memoria
        y números largos para que la misma clase de error caiga en un solo issue
        aunque los frames acumulados varíen (los stacks vienen inflados)."""
        norm = _sentry_re.sub(r'0x[0-9a-fA-F]+', '0xADDR', valor or "")
        norm = _sentry_re.sub(r'\b\d{4,}\b', '#', norm)
        return [tipo, norm]

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
            fp = _jp_sentry_fingerprint(tipo, valor)
            clave = "|".join(fp)
            if clave in _jp_sentry_enviados:
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
                },
            }

            _args, _kwargs = _jp_sentry_armar(evento, timeout=8)
            renpy.fetch(*_args, **_kwargs)
            _jp_sentry_enviados.add(clave)
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
