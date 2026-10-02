################################################################################
## Errores y Feedback — reporte manual (sin necesidad de crash)
################################################################################
## Botón "Errores y Feedback" en el menú de pausa → panel donde el jugador
## escribe un título y la descripción del problema/comentario. El reporte se
## envía al webhook de Discord junto con el estado del juego (día, horario,
## lugar, inventario, quests) y, opcionalmente, UNA captura de pantalla.
##
## El botón del menú de Escape hace [Function(jp_fb_abrir), Return()]: el
## Return() CIERRA el menú de pausa, así el panel queda sobre el JUEGO (no
## sobre el menú) y la captura sale del juego real. Para que el panel sobreviva
## al cierre del menú (que es un CONTEXTO aparte, donde los screens mueren) se
## muestra vía config.always_shown_screens — el mismo mecanismo que usa la
## consola de Ren'Py. Por eso el texto vive en variables del store
## (VariableInputValue), no en variables de screen: así no se pierde al
## ocultar/mostrar el panel durante la captura.
##
## La captura la toma el botón "Tomar captura" (NO el de enviar — encadenar la
## llamada de red al flujo de captura colgaba el juego). El flujo es:
##   1. Ocultar el panel → así la foto sale limpia (el texto ya está en el store).
##   2. Un timer deja que se DIBUJE ese frame limpio y recién ahí captura.
##      Es imprescindible: screenshot_to_bytes devuelve "the last thing drawn",
##      así que sin ese redibujo la foto saldría del frame viejo.
##   3. Reabrir el panel con el texto intacto y avisar que la captura se agregó.

init python:

    # Ruta /feedback del proxy (Cloudflare Worker), que reenvía al canal de
    # feedback; los crashes van a /error (JP_WEBHOOK_URL en sistema_reporte_errores.rpy)
    JP_WEBHOOK_FEEDBACK_URL = "https://japitown-reporter.risita022.workers.dev/feedback"

    # Estado interno. No son `default`: la captura son bytes y no deben ir al save.
    store._jp_fb_captura = None
    # None|"ok"|"ok_sin_captura"|"fail"|"captura_fail" y los tres motivos por
    # los que un reporte no se manda: "vacio"|"corto"|"sin_sentido".
    store._jp_fb_status = None
    store._jp_fb_titulo = u""    # el texto vive acá para sobrevivir al ocultar/mostrar
    store._jp_fb_texto = u""

    def _jp_fb_mostrar_panel(mostrar):
        """Muestra/oculta el panel vía always_shown_screens (sobrevive al cierre
        del menú de Escape, que es un contexto distinto).

        OJO: always_shown_screens SOLO re-muestra (hace show_screen si no está);
        nunca oculta. Así que para ocultarlo hay que sacarlo de la lista Y llamar
        a hide_screen — si no, el panel sigue en pantalla y sale en la captura.
        """
        lista = config.always_shown_screens
        if mostrar:
            if "jp_feedback_screen" not in lista:
                lista.append("jp_feedback_screen")
            renpy.show_screen("jp_feedback_screen")
        else:
            if "jp_feedback_screen" in lista:
                lista.remove("jp_feedback_screen")
            renpy.hide_screen("jp_feedback_screen")

    def jp_fb_abrir():
        """Abre el panel limpio. Se usa junto con Return() para cerrar el menú."""
        store._jp_fb_captura = None
        store._jp_fb_status = None
        store._jp_fb_titulo = u""
        store._jp_fb_texto = u""
        _jp_fb_mostrar_panel(True)
        renpy.restart_interaction()

    def jp_fb_cerrar():
        store._jp_fb_captura = None   # no dejar los bytes vivos
        store._jp_fb_status = None
        store._jp_fb_titulo = u""
        store._jp_fb_texto = u""
        _jp_fb_mostrar_panel(False)
        renpy.restart_interaction()

    def jp_fb_tomar_captura():
        """Botón 'Tomar captura': oculta el panel para que la foto salga limpia.
        El texto ya está a salvo en el store. El helper captura tras el redibujo."""
        _jp_fb_mostrar_panel(False)
        renpy.show_screen("_jp_fb_captura_helper")
        renpy.restart_interaction()

    def jp_fb_finalizar_captura():
        """Corre desde el timer, con el panel oculto y el frame limpio ya dibujado."""
        try:
            store._jp_fb_captura = renpy.screenshot_to_bytes((1280, 720))
            store._jp_fb_status = None      # el indicador de captura ya lo muestra
        except Exception:
            store._jp_fb_captura = None
            store._jp_fb_status = "captura_fail"
        renpy.hide_screen("_jp_fb_captura_helper")
        _jp_fb_mostrar_panel(True)          # el texto sigue en el store
        renpy.restart_interaction()

    def jp_fb_borrar_captura():
        """Elimina la captura actual para poder tomar una nueva."""
        store._jp_fb_captura = None
        store._jp_fb_status = None
        renpy.restart_interaction()

    def jp_fb_estado_juego():
        """Lista prolija con el estado del juego. Cada dato con su guarda."""
        L = []
        # Quién lo manda (mismo helper que usan el reporte de error y Sentry)
        try:
            L.append(u"• Jugador: %s" % jp_jugador_actual())
        except Exception:
            pass
        # El id anónimo de la instalación, el MISMO que Sentry recibe como
        # user.id: con los dos lados etiquetados igual, un feedback se cruza
        # con los crashes que esa instalación mandó (ver jp_instalacion_id).
        try:
            L.append(u"• Instalación: %s" % jp_instalacion_id())
        except Exception:
            pass
        # Día y horario
        try:
            _dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            _hors = ["Mañana", "Tarde", "Noche", "Trasnoche"]
            L.append(u"• Día: %s (día %s total) — %s" % (
                _dias[store.dia_semana_actual], store.dias_totales, _hors[store.horario_actual]))
        except Exception:
            pass
        # Lugar
        try:
            _loc = store.sistema_locaciones.locacion_actual
            if _loc:
                L.append(u"• Lugar: %s (%s)" % (_loc.nombre, _loc.id))
        except Exception:
            pass
        # Dinero
        try:
            L.append(u"• Dinero: $%s" % store.dinero)
        except Exception:
            pass
        # Inventario
        try:
            _inv = store.inventario or {}
            if _inv:
                _its = []
                for _iid, _qty in _inv.items():
                    _nom = CATALOGO_ITEMS.get(_iid, {}).get("nombre", _iid)
                    _its.append(u"%s x%s" % (_nom, _qty))
                L.append(u"• Inventario: " + u", ".join(_its))
            else:
                L.append(u"• Inventario: (vacío)")
        except Exception:
            pass
        # Quests activas (NPCs + MC)
        try:
            _acts = [
                u"%s [etapa %s]" % (q.nombre, q.etapa_actual)
                for q in store.sistema_quests.quests.values()
                if q.activa and not q.completada
            ]
        except Exception:
            _acts = []
        try:
            _acts += [
                u"%s (MC)" % q.nombre
                for q in store.sistema_quests_mc.quests.values()
                if getattr(q, 'activa', False) and not q.completada
            ]
        except Exception:
            pass
        L.append(u"• Quests activas: " + (u", ".join(_acts) if _acts else u"(ninguna)"))
        # Quests completadas
        try:
            _comps = [q.nombre for q in store.sistema_quests.quests.values() if q.completada]
            try:
                _comps += [
                    u"%s (MC)" % q.nombre
                    for q in store.sistema_quests_mc.quests.values() if q.completada
                ]
            except Exception:
                pass
            L.append(u"• Quests completadas (%d): %s" % (
                len(_comps), u", ".join(_comps) if _comps else u"(ninguna)"))
        except Exception:
            pass
        # Controlador de quests: qué estaba procesando en ese momento.
        try:
            _ctrl = jp_controlador_actual(10)
            L.append(u"• Controlador:\n" + u"\n".join(
                u"   - " + _l for _l in _ctrl.splitlines()))
        except Exception:
            pass
        # Plataforma
        try:
            L.append(u"• Plataforma: %s — Japitown %s" % (
                u"Web" if jp_es_web() else u"PC", getattr(config, "version", "?")))
        except Exception:
            pass
        return u"\n".join(L)

    # ── ¿Se puede entender este reporte? ────────────────────────────────────
    # Llegaban reportes vacios, con dos palabras sueltas o con teclazos
    # ("asdasd", "1234", "aaaaa"): imposible saber que le pasaba al jugador, y
    # sin forma de volver a preguntarle. La validacion corre ANTES de enviar y
    # explica que falta, en vez de mandar algo que no sirve.
    #
    # SE VALIDA TITULO + DESCRIPCION JUNTOS, no la descripcion sola: quien
    # escribio todo arriba ya dijo algo entendible y no tiene por que copiarlo
    # abajo. Lo que se mide es si el conjunto alcanza.

    JP_FB_MINIMO_CHARS = 20      # caracteres del conjunto, sin contar espacios
    JP_FB_MINIMO_PALABRAS = 3

    # Teclazos tipicos: filas del teclado y la serie de numeros. Solo se miran
    # en textos CORTOS (ver abajo), asi que no pueden ensuciar un reporte largo
    # que de casualidad contenga una de estas cadenas.
    _JP_FB_SECUENCIAS = ("qwerty", "asdfgh", "zxcvbn", "asdf", "qwer", "zxcv",
                         "1234", "abcd")
    _JP_FB_VOCALES = u"aeiouáéíóúàèìòùâêîôûäëïöüãõy"

    def _jp_fb_normalizar(titulo, texto):
        """El conjunto en minusculas y con los espacios colapsados."""
        _todo = u"%s %s" % (titulo or u"", texto or u"")
        return u" ".join(_todo.lower().split())

    def jp_fb_motivo_invalido(titulo, texto):
        """
        None si el reporte se puede interpretar; si no, el motivo:
        "vacio" | "corto" | "sin_sentido".

        Las reglas van de la mas dura a la mas blanda, y las dos ultimas SOLO
        se aplican a textos cortos (< 60 caracteres). Un reporte largo se acepta
        siempre: mejor tragarse un falso negativo que rechazarle el reporte a
        alguien que se tomo el trabajo de escribirlo.
        """
        _t = _jp_fb_normalizar(titulo, texto)
        if not _t:
            return "vacio"

        _letras = [c for c in _t if c.isalpha()]
        _sin_espacios = _t.replace(u" ", u"")

        # Sin una sola letra: "1234", "!!!!", ":)"
        if not _letras:
            return "sin_sentido"
        # Un unico caracter repetido: "aaaaaaa", "ja ja ja ja" no (tiene dos)
        if len(_sin_espacios) > 3 and len(set(_sin_espacios)) <= 2:
            return "sin_sentido"

        # ── Blandas: solo en textos cortos ──────────────────────────────────
        # VAN ANTES DEL LARGO a proposito: "asdasdasd" tambien es corto, pero
        # decirle "escribi un poco mas" a alguien que tecleo al azar no sirve
        # de nada. El motivo correcto es el que le explica que le falta.
        if len(_sin_espacios) < 60:
            # Casi sin vocales = tecleo al azar. El umbral es bajisimo a
            # proposito (el español y el ingles rondan el 40%), asi que solo
            # cae algo que de verdad no es lenguaje.
            _vocales = sum(1 for c in _letras if c in _JP_FB_VOCALES)
            if _vocales * 100 < len(_letras) * 15:
                return "sin_sentido"
            # Filas del teclado
            for _seq in _JP_FB_SECUENCIAS:
                if _seq in _sin_espacios:
                    return "sin_sentido"
            # Muy pocos caracteres DISTINTOS para lo que dura: es el mismo
            # puñado repetido ("asdasdasdasd", "hola hola hola"). Una frase de
            # verdad de este largo usa el triple de letras distintas — probado
            # contra reportes reales en español y en ingles.
            if len(_sin_espacios) >= 8 and \
                    len(set(_sin_espacios)) * 100 < len(_sin_espacios) * 30:
                return "sin_sentido"

        # ── Largo: lo ultimo, cuando ya se sabe que son palabras de verdad ──
        if len(_sin_espacios) < JP_FB_MINIMO_CHARS:
            return "corto"
        if len(_t.split()) < JP_FB_MINIMO_PALABRAS:
            return "corto"

        return None

    def jp_fb_construir(titulo, texto):
        """Arma el mensaje para Discord (límite 2000 chars)."""
        import time
        titulo = (titulo or u"").strip()
        texto = (texto or u"").strip()
        cabecera = (
            u"**[Japitown %s] 📝 %s**\n" % (
                getattr(config, "version", "?"),
                titulo if titulo else u"Reporte manual") +
            u"Fecha: %s\n\n" % time.strftime("%Y-%m-%d %H:%M:%S")
        )
        estado = u"\n\n**Estado del juego**\n" + jp_fb_estado_juego()
        # Recortar la descripción para que el estado siempre entre
        maximo_texto = 1900 - len(cabecera) - len(estado)
        if maximo_texto < 100:
            maximo_texto = 100
        if len(texto) > maximo_texto:
            texto = texto[:maximo_texto] + u"…"
        return (cabecera + texto + estado)[:1990]

    def _jp_fb_enviar_multipart(contenido, png_bytes):
        """POST multipart al webhook: payload_json + files[0] (la captura)."""
        import json as _json
        boundary = u"----JapitownFeedback8f7a2b"
        pj = _json.dumps({"content": contenido})
        pre = (
            u"--" + boundary + u"\r\n"
            u'Content-Disposition: form-data; name="payload_json"\r\n'
            u"Content-Type: application/json\r\n\r\n" + pj + u"\r\n"
            u"--" + boundary + u"\r\n"
            u'Content-Disposition: form-data; name="files[0]"; filename="captura.png"\r\n'
            u"Content-Type: image/png\r\n\r\n"
        ).encode("utf-8")
        post = (u"\r\n--" + boundary + u"--\r\n").encode("utf-8")
        renpy.fetch(
            JP_WEBHOOK_FEEDBACK_URL,
            method="POST",
            data=pre + png_bytes + post,
            content_type="multipart/form-data; boundary=" + boundary,
            timeout=25,
        )

    def jp_fb_enviar(titulo, texto):
        """Botón Enviar: manda el texto + el estado del juego, y la captura si hay."""
        titulo = (titulo or u"").strip()
        texto = (texto or u"").strip()

        # Nada se manda sin poder entenderse: el aviso dice QUE falta, que es
        # lo unico que puede arreglar el jugador (ver jp_fb_motivo_invalido).
        _motivo = jp_fb_motivo_invalido(titulo, texto)
        if _motivo:
            store._jp_fb_status = _motivo
            renpy.restart_interaction()
            return

        contenido = jp_fb_construir(titulo, texto)
        enviado = False
        captura_ok = True

        if store._jp_fb_captura:
            try:
                _jp_fb_enviar_multipart(contenido, store._jp_fb_captura)
                enviado = True
            except Exception:
                captura_ok = False   # reintentar solo texto

        if not enviado:
            try:
                renpy.fetch(JP_WEBHOOK_FEEDBACK_URL, json={"content": contenido}, timeout=15)
                enviado = True
            except Exception:
                pass

        if enviado:
            store._jp_fb_status = "ok" if captura_ok else "ok_sin_captura"
        else:
            store._jp_fb_status = "fail"
        renpy.restart_interaction()


################################################################################
## Pantalla del formulario
################################################################################

screen jp_feedback_screen():
    modal True
    zorder 200

    # El texto vive en variables del STORE (no del screen): así sobrevive al
    # ocultar/mostrar el panel cuando se toma la captura.
    # Solo UN input puede estar editable a la vez: click en cada campo lo activa.
    default fb_iv_titulo = VariableInputValue("_jp_fb_titulo", default=True, returnable=False)
    default fb_iv_texto = VariableInputValue("_jp_fb_texto", default=False, returnable=False)

    add "#101018EE"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1240
        padding (40, 34)
        background "#222233"

        vbox:
            spacing 14
            xfill True

            text _("Errores y Feedback") size 32 color "#4FC3F7" bold True

            text _("Cuéntanos el problema o deja tu comentario. Se envía junto al estado del juego.") size 19 color "#dddddd"

            # EL AVISO PREVENTIVO, y no solo el error al enviar: la mayoría de
            # los reportes inservibles no eran mala voluntad, era no saber qué
            # hacía falta. Decirlo antes evita el rechazo después.
            text _("Hace falta una descripción concreta: qué estabas haciendo, qué pasó y qué esperabas que pasara. Un reporte vacío, incompleto o con texto sin sentido no se puede interpretar y no sirve para arreglar nada.") size 17 color "#ffcc88"

            null height 4

            # Título del reporte (click para escribir acá)
            text _("Título:") size 17 color "#aaaacc"
            button:
                background ("#141430" if fb_iv_titulo.editable else "#11111a")
                hover_background "#161636"
                padding (14, 10)
                xfill True
                key_events True
                action [fb_iv_texto.Disable(), fb_iv_titulo.Enable()]
                input:
                    value fb_iv_titulo
                    length 80
                    size 22
                    color "#ffffff"

            # Descripción (click para escribir acá)
            text _("Descripción:") size 17 color "#aaaacc"
            button:
                background ("#141430" if fb_iv_texto.editable else "#11111a")
                hover_background "#161636"
                padding (14, 10)
                xfill True
                ysize 220
                key_events True
                action [fb_iv_titulo.Disable(), fb_iv_texto.Enable()]
                input:
                    value fb_iv_texto
                    length 1200
                    multiline True
                    size 20
                    color "#ffffff"
                    yalign 0.0

            # Captura adjunta — indicador + botón para eliminarla (solo una por reporte)
            if _jp_fb_captura:
                hbox:
                    spacing 12
                    text _("📷 Captura agregada") size 19 color "#7CFC8A" bold True yalign 0.5
                    textbutton _("🗑 Eliminar"):
                        action Function(jp_fb_borrar_captura)
                        text_size 17 text_color "#ffffff"
                        background "#5a3a3a" hover_background "#7a4a4a" padding (12, 6)
                        yalign 0.5

            # Estado del envío
            if _jp_fb_status == "ok":
                text _("✅ Reporte enviado. ¡Gracias por ayudar a mejorar el juego!") size 19 color "#7CFC8A" bold True
            elif _jp_fb_status == "ok_sin_captura":
                text _("✅ Enviado (la captura no se pudo adjuntar).") size 19 color "#7CFC8A" bold True
            elif _jp_fb_status == "fail":
                text _("❌ No se pudo enviar. Revisa tu conexión e intenta de nuevo.") size 19 color "#ff6b6b" bold True
            elif _jp_fb_status == "vacio":
                text _("⚠️ El reporte está vacío. Sin una descripción no hay forma de saber qué pasó.") size 19 color "#ffcc88" bold True
            elif _jp_fb_status == "corto":
                text _("⚠️ Con eso no alcanza. Hacen falta al menos unas palabras que expliquen qué estabas haciendo y qué pasó.") size 19 color "#ffcc88" bold True
            elif _jp_fb_status == "sin_sentido":
                text _("⚠️ Así no se entiende nada. El reporte tiene que estar escrito en palabras para poder interpretarlo.") size 19 color "#ffcc88" bold True
            elif _jp_fb_status == "captura_fail":
                text _("❌ No se pudo tomar la captura.") size 19 color "#ff6b6b" bold True

            null height 6

            hbox:
                spacing 16
                xalign 0.5

                textbutton _("📤 Enviar"):
                    action Function(jp_fb_enviar, _jp_fb_titulo, _jp_fb_texto)
                    text_size 21 text_color "#ffffff"
                    background "#3a6ea5" hover_background "#4d8bc9" padding (20, 12)

                # Solo se permite una captura: si ya hay, hay que eliminarla primero
                if not _jp_fb_captura:
                    textbutton _("📷 Tomar captura"):
                        action Function(jp_fb_tomar_captura)
                        text_size 21 text_color "#ffffff"
                        background "#444466" hover_background "#555588" padding (20, 12)

                textbutton _("Volver"):
                    action Function(jp_fb_cerrar)
                    text_size 21 text_color "#ffffff"
                    background "#444466" hover_background "#555588" padding (20, 12)


# Helper invisible: existe solo el instante de la captura. Con el panel ya
# oculto y la escena refrescada, el timer deja que se dibuje ese frame limpio
# (screenshot_to_bytes devuelve "the last thing drawn") y recién ahí captura.
# NO hace ninguna llamada de red: encadenar el envío acá colgaba el juego.
screen _jp_fb_captura_helper():
    zorder 200
    timer 0.15 action Function(jp_fb_finalizar_captura)
