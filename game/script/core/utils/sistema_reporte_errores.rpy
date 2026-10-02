################################################################################
## Sistema de Reporte de Errores
################################################################################
## Cuando ocurre un error no controlado, muestra una pantalla propia con un
## botón "Reportar" que envía el error a un webhook de Discord.
##
## CONFIGURACIÓN: el reporte va al proxy (Cloudflare Worker japitown-reporter),
## que lo reenvía al webhook de Discord guardado como secreto del Worker.
## El código del Worker está en proxy-reportes/, excluido del build en
## options.rpy (estar fuera de game/ NO alcanza: la raíz también se empaqueta).
##
## Nota: el reporte incluye versión, locación/horario actual y el traceback
## (puede contener texto de diálogo). Lo envía SOLO cuando el jugador toca
## "Reportar" (consentimiento explícito).
################################################################################

init python:

    import sys

    # >>> URL a la que se envía el reporte <<<
    # Proxy (Cloudflare Worker): el webhook de Discord real queda solo en el
    # Worker como secreto, nunca en el juego público.
    JP_WEBHOOK_URL = "https://japitown-reporter.risita022.workers.dev/error"

    def jp_es_web():
        """True si el juego corre en el navegador (Ren'Py Web / emscripten)."""
        try:
            if sys.platform == "emscripten":
                return True
        except Exception:
            pass
        try:
            return bool(renpy.variant("web"))
        except Exception:
            return False

    # Estado interno del handler
    store._jp_handling = False
    store._jp_short = ""
    store._jp_short_disp = ""   # versión segura para mostrar en pantalla
    store._jp_full = ""
    store._jp_status = None   # None | "ok" | "fail" | "sin_config"
    store._jp_es_descarga = False   # True si el error es un fallo de descarga web (E04)

    def jp_jugador_actual():
        """
        Quien manda el reporte: el nombre que eligio el jugador. Lo usan los
        tres canales (error, feedback, Sentry) para no tener que adivinar de
        quien es cada reporte. Marca "(tester)" cuando la partida corre con
        MODO_DEV — normalmente un perfil de PERFILES_DEV.
        """
        try:
            nombre = (getattr(store, "mc_name", u"") or u"").strip()
        except Exception:
            nombre = u""
        if not nombre:
            nombre = u"(sin nombre)"
        try:
            if getattr(store, "MODO_DEV", False):
                nombre += u" (tester)"
        except Exception:
            pass
        return nombre

    def jp_controlador_actual(max_lineas=12):
        """
        Lo que esta procesando el controlador de quests (planificador). Con
        guarda propia: si el controlador no existe todavia (crash muy temprano)
        el reporte sale igual.
        """
        try:
            return store.planificador_reporte(max_lineas)
        except Exception:
            return u"(no disponible)"

    def _jp_contexto_actual():
        """Arma una línea con la ubicación/tiempo del juego al momento del error."""
        partes = []
        try:
            loc = store.sistema_locaciones.locacion_actual
            partes.append("loc=" + (loc.id if loc else "?"))
        except Exception:
            partes.append("loc=?")
        for var in ("dias_totales", "dia_semana_actual", "horario_actual"):
            try:
                partes.append("%s=%s" % (var, getattr(store, var, "?")))
            except Exception:
                pass
        return " | ".join(partes)

    def jp_construir_reporte():
        """Construye el texto del reporte (recortado al límite de Discord)."""
        import time
        ver = getattr(config, "version", "?")
        short = (store._jp_short or "").strip()
        full = (store._jp_full or "").strip()

        # La EXCEPCIÓN real es la última línea no vacía del traceback completo.
        # Mostrarla en el encabezado: si un stack largo corta el mensaje, lo
        # importante queda visible arriba (antes se perdía en la cola).
        excepcion = ""
        for _linea in reversed((full or short).splitlines()):
            if _linea.strip():
                excepcion = _linea.strip()
                break

        cabecera = (
            "**[Japitown %s] Reporte de error**\n" % ver +
            "Fecha: %s\n" % time.strftime("%Y-%m-%d %H:%M:%S") +
            "Jugador: %s\n" % jp_jugador_actual() +
            # El MISMO id que va a Sentry como user.id: con los dos lados
            # etiquetados igual, un feedback que llega por Discord se cruza con
            # los crashes que esa instalacion mando (ver jp_instalacion_id).
            "Instalación: %s\n" % jp_instalacion_id() +
            "Contexto: %s\n" % _jp_contexto_actual() +
            "Excepción: %s\n" % (excepcion or "(desconocida)") +
            "Error: %s\n" % ((short[:300] + u"…" if len(short) > 300 else short) or "(sin resumen)")
        )
        # Que estaba haciendo el controlador: restriccion puesta, reservas y
        # como veia a cada quest viva. Va ANTES del traceback y con tope
        # propio — el traceback se recorta contra lo que quede libre.
        _ctrl = jp_controlador_actual(8)
        if len(_ctrl) > 600:
            _ctrl = _ctrl[:600] + u"…"
        controlador = "Controlador:\n%s\n" % _ctrl
        # Discord: límite de 2000 chars en content. Dejamos margen y mandamos
        # la COLA del traceback (donde está el error real) dentro de un bloque.
        margen = 1900 - len(cabecera) - len(controlador) - 10
        if margen < 200:
            margen = 200
        cola = full[-margen:] if len(full) > margen else full
        cuerpo = ("```\n%s\n```" % cola) if cola else ""
        return (cabecera + controlador + cuerpo)[:1990]

    def jp_enviar_reporte():
        """Envía el reporte al webhook. Devuelve 'ok' | 'fail' | 'sin_config'."""
        url = JP_WEBHOOK_URL
        if (not url) or ("PEGAR_AQUI" in url):
            return "sin_config"
        texto = jp_construir_reporte()
        payload = {"content": texto}
        # 1) Intento con renpy.fetch (maneja certificados correctamente)
        try:
            renpy.fetch(url, json=payload, timeout=15)
            return "ok"
        except Exception:
            pass
        # 2) Fallback con urllib (con y sin verificación SSL) — SOLO desktop.
        #    En web no hay sockets crudos; urllib no funciona (y renpy.fetch ya cubre web).
        if jp_es_web():
            return "fail"
        try:
            import json, ssl, urllib.request
            data = json.dumps(payload).encode("utf-8")
            headers = {"Content-Type": "application/json", "User-Agent": "Japitown"}
            for ctx in (ssl.create_default_context(), ssl._create_unverified_context()):
                try:
                    req = urllib.request.Request(url, data=data, headers=headers)
                    urllib.request.urlopen(req, timeout=15, context=ctx)
                    return "ok"
                except Exception:
                    continue
        except Exception:
            pass
        return "fail"

    def jp_reportar_action():
        """Acción del botón Reportar: envía y refresca el estado en pantalla."""
        store._jp_status = jp_enviar_reporte()
        renpy.restart_interaction()

    def _jp_set_clipboard(texto):
        """Copia texto al portapapeles probando varios métodos. True si logra."""
        texto = texto or ""
        # 0) En web: clipboard del navegador via JS (funciona con el gesto del click en https)
        if jp_es_web():
            try:
                import json as _json, emscripten
                js = "navigator.clipboard.writeText(" + _json.dumps(texto) + ");"
                emscripten.run_script(js)
                return True
            except Exception:
                pass
        # 1) API nativa de Ren'Py (si la versión la tiene)
        fn = getattr(renpy, "copy_to_clipboard", None)
        if callable(fn):
            try:
                fn(texto)
                return True
            except Exception:
                pass
        # 2) pygame_sdl2.scrap (SDL2)
        try:
            import pygame_sdl2 as _pg
            try:
                _pg.scrap.init()
            except Exception:
                pass
            # 2a) put_text si existe
            put_text = getattr(_pg.scrap, "put_text", None)
            if callable(put_text):
                put_text(texto)
                return True
            # 2b) put(SCRAP_TEXT, bytes)
            tipo = getattr(_pg.scrap, "SCRAP_TEXT", None)
            if tipo is not None:
                _pg.scrap.put(tipo, texto.encode("utf-8"))
                return True
        except Exception:
            pass
        return False

    def jp_copiar_error():
        """Copia el reporte completo (con contexto) al portapapeles."""
        try:
            try:
                texto = jp_construir_reporte()
            except Exception:
                texto = store._jp_full or store._jp_short or ""
            if _jp_set_clipboard(texto):
                store._jp_status = "copiado"
            else:
                store._jp_status = "copiar_fail"
        except Exception:
            store._jp_status = "copiar_fail"
        renpy.restart_interaction()

    def jp_exception_handler(te):
        """
        Handler global de excepciones no controladas.
        Muestra la pantalla propia; si algo falla, devuelve False para que
        Ren'Py use su pantalla de error por defecto (nunca peor que el default).

        Desde Ren'Py 8.4 el handler recibe UN objeto (TracebackException) con
        .simple/.full, en vez de los tres strings de antes. Con la firma vieja
        Ren'Py caía a su fallback de compatibilidad, y el TypeError que largaba
        inspect.bind al descartar la firma nueva quedaba encadenado al error
        real: el reporte mostraba ESE TypeError en vez de la excepción de
        verdad, siempre apuntando al `pause` del game_loop.
        """
        if getattr(store, "_jp_handling", False):
            return False
        try:
            store._jp_handling = True
            short = te.simple
            full = te.full
            store._jp_short = short or ""
            # Versión segura para mostrar: forma de variable (no interpola []),
            # y escapamos {{ para que no se interpreten como tags de texto.
            store._jp_short_disp = (short or "")[:400].replace("{", "{{").replace("[", "[[")
            store._jp_full = full or ""
            store._jp_status = None
            # ¿Es un fallo de descarga de asset en el build web? (E04). No es un
            # bug de código: es la red/hosting bajando un recurso on-demand. Se
            # muestra una pantalla de "conexión" con Reintentar, en vez de la de
            # crash, para que el jugador no lo reporte como bug.
            store._jp_es_descarga = ("Download error" in (full or "")) or ("Download error" in (short or ""))
            # Si el error reventó a mitad de construir una screen, la pila de
            # widgets quedó abierta y el `call screen` de abajo moriría con
            # "ui.interact called with non-empty widget/layer stack",
            # tapando el error original. Lo que quedó en la pila es basura de
            # una screen que ya falló, asi que descartarla es seguro (mismo
            # criterio que el drenaje de call frames del game_loop).
            try:
                renpy.ui.reset()
            except Exception:
                pass
            resultado = renpy.call_in_new_context("_jp_error_context")
            if resultado == "ignore":
                return True          # intentar continuar (como "Ignore")
            return True
        except Exception:
            return False             # fallback a la pantalla por defecto de Ren'Py
        finally:
            store._jp_handling = False

    # Activar el handler
    config.exception_handler = jp_exception_handler


################################################################################
## Pantalla del reporte de error
################################################################################

screen jp_error_screen():
    modal True
    zorder 32767

    add "#1a1a1aee"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        padding (40, 36)
        background "#222233"

        vbox:
            spacing 16
            xfill True

            # ── E04: fallo de descarga web → pantalla de conexión ──────────────
            if _jp_es_descarga:

                text "Problema de conexión" size 34 color "#ffb74d" bold True

                text "No se pudo cargar un recurso del juego. Suele ser algo temporal de tu conexión o del servidor." size 20 color "#dddddd"
                text "Reintentá; si sigue fallando, recargá la página." size 20 color "#dddddd"

                null height 14

                hbox:
                    spacing 16
                    xalign 0.5

                    textbutton "🔄 Reintentar":
                        action Function(renpy.utter_restart)
                        text_size 24 text_color "#ffffff"
                        background "#3a6ea5" hover_background "#4d8bc9" padding (26, 16)

                    textbutton "Continuar igual":
                        action Return("ignore")
                        text_size 22 text_color "#ffffff"
                        background "#444466" hover_background "#555588" padding (22, 14)

                    if not jp_es_web():
                        textbutton "Salir":
                            action Quit(confirm=False)
                            text_size 22 text_color "#ffffff"
                            background "#5a3a3a" hover_background "#7a4a4a" padding (22, 14)

            else:

                text "Ocurrió un error" size 34 color "#ff6b6b" bold True

                text "El juego encontró un problema. Puedes reportarlo para que se corrija." size 20 color "#dddddd"

                null height 6

                # Resumen del error
                frame:
                    background "#11111a"
                    padding (16, 12)
                    xfill True
                    text _jp_short_disp size 16 color "#ffcc88" substitute False

                # Estado del envío
                if _jp_status == "ok":
                    text "✅ Reporte enviado. ¡Gracias!" size 20 color "#7CFC8A" bold True
                elif _jp_status == "fail":
                    text "❌ No se pudo enviar. Tocá 📋 Copiar y pegá el reporte en el Discord." size 20 color "#ff6b6b" bold True
                elif _jp_status == "sin_config":
                    text "⚠️ El reporte no está configurado todavía (falta el webhook)." size 20 color "#ffcc88" bold True
                elif _jp_status == "copiado":
                    text "📋 Reporte copiado. Pegalo en el Discord o mandálo por mail. ¡Gracias!" size 20 color "#7CFC8A" bold True
                elif _jp_status == "copiar_fail":
                    text "❌ No se pudo copiar. Sacá una captura de esta pantalla y mandála." size 20 color "#ff6b6b" bold True

                null height 10

                hbox:
                    spacing 16
                    xalign 0.5

                    textbutton "📤 Reportar el error":
                        action Function(jp_reportar_action)
                        text_size 22 text_color "#ffffff"
                        background "#3a6ea5" hover_background "#4d8bc9" padding (22, 14)

                    textbutton "📋 Copiar":
                        action Function(jp_copiar_error)
                        text_size 22 text_color "#ffffff"
                        background "#444466" hover_background "#555588" padding (22, 14)

                    textbutton "🔄 Reintentar":
                        action Function(renpy.utter_restart)
                        text_size 22 text_color "#ffffff"
                        background "#444466" hover_background "#555588" padding (22, 14)

                    textbutton "Continuar":
                        action Return("ignore")
                        text_size 22 text_color "#ffffff"
                        background "#444466" hover_background "#555588" padding (22, 14)

                    # "Salir" no tiene sentido en web (no cierra la pestaña)
                    if not jp_es_web():
                        textbutton "Salir":
                            action Quit(confirm=False)
                            text_size 22 text_color "#ffffff"
                            background "#5a3a3a" hover_background "#7a4a4a" padding (22, 14)


# Contexto aislado que muestra la pantalla y devuelve la elección al handler
label _jp_error_context:
    # Captura automática a Sentry (silenciosa). Corre en este contexto nuevo,
    # donde renpy.fetch funciona igual que el envío a Discord del botón. Puede
    # demorar unos segundos la aparición de la pantalla si la red está lenta;
    # para que envíe sin bloquear, poné JP_SENTRY_AUTO = False y llamalo desde
    # un botón. jp_sentry_capturar está definida en sistema_sentry.rpy.
    if getattr(store, "JP_SENTRY_AUTO", False):
        $ jp_sentry_capturar(store._jp_short, store._jp_full)
    call screen jp_error_screen

    # Endurecimiento (E02): si el jugador elige "Continuar", reconstruir los
    # estilos antes de reanudar. Un crash a mitad de un rebuild de Ren'Py (ej:
    # E01 dentro de change_language) puede dejar el registro de estilos
    # incompleto — sin 'namebox' —, y reanudar sin esto reventaba en el
    # siguiente diálogo con "Style 'namebox' does not exist". renpy.style.rebuild()
    # es la misma API que usa Ren'Py al cambiar idioma; deja los estilos sanos.
    if _return == "ignore":
        python:
            try:
                renpy.style.rebuild()
            except Exception:
                pass

    return _return
