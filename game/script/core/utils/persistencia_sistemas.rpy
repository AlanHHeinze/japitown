################################################################################
## Persistencia de sistemas — merge post-load
################################################################################
## Los sistemas con estado (quests, mensajes, talk, skins, events) son `default`
## y se guardan enteros en el save. Este módulo resuelve la contracara: cuando
## una ACTUALIZACIÓN agrega contenido nuevo (quests, chats, estados de talk,
## skins, eventos), los saves viejos traen el sistema serializado SIN ese
## contenido. Al cargar, se compara contra el catálogo fresco construido en el
## init de esta sesión y se agrega lo que falte (por id), sin tocar el progreso.

init 999 python:

    import copy as _copy_ps

    # Snapshot profundo de los sistemas recién construidos por el init.
    # Nunca se guarda (es una variable de init, no default).
    _SISTEMAS_FRESCOS = {}

    def _ps_stash():
        for _nombre in ("sistema_quests", "sistema_quests_mc", "sistema_mensajes",
                        "sistema_talk", "sistema_skins", "sistema_events"):
            try:
                _SISTEMAS_FRESCOS[_nombre] = _copy_ps.deepcopy(getattr(store, _nombre))
            except Exception as _e:
                if config.developer:
                    print("[Persistencia] No se pudo copiar {}: {}".format(_nombre, _e))

    _ps_stash()

    # Clase de cada sistema, para el fallback de emergencia de _ps_copia_fresca
    _PS_CLASES = {
        "sistema_quests":    "SistemaQuests",
        "sistema_quests_mc": "SistemaQuestsMC",
        "sistema_mensajes":  "SistemaMensajes",
        "sistema_talk":      "SistemaTalk",
        "sistema_skins":     "SistemaSkins",
        "sistema_events":    "SistemaEvents",
    }

    def _ps_copia_fresca(nombre):
        """
        Expresión de los `default sistema_x = ...`: devuelve una COPIA del
        catálogo fresco construido en init. CLAVE: los default se re-evalúan
        en CADA partida nueva — si devolvieran una instancia vacía (SistemaX())
        pisarían el catálogo poblado del init y no habría ninguna quest.
        """
        try:
            return _copy_ps.deepcopy(_SISTEMAS_FRESCOS[nombre])
        except Exception:
            # Emergencia: instancia vacía (no debería ocurrir; el stash corre en init 999)
            try:
                return getattr(renpy.store, _PS_CLASES[nombre])()
            except Exception:
                return None

    def _ps_merge_dict(fresco_dict, cargado_dict, etiqueta):
        """Agrega al dict cargado las claves del catálogo fresco que falten."""
        agregadas = 0
        for _k, _v in fresco_dict.items():
            if _k not in cargado_dict:
                cargado_dict[_k] = _copy_ps.deepcopy(_v)
                agregadas += 1
        if agregadas and config.developer:
            print("[Persistencia] {}: {} elementos nuevos agregados".format(etiqueta, agregadas))

    def _ps_refrescar_quests(fresco_dict, cargado_dict):
        """
        Pisa el CATALOGO de las quests ya presentes en el save con el fresco:
        los textos de guia y las rutinas.

        POR QUE HACE FALTA: _ps_merge_dict solo agrega las quests que faltan, asi
        que una quest que ya venia en el save se queda para siempre con la
        `config_etapas` y la `rutina_quest` del dia que se guardo. Ahi viven la
        pista, el "que hacer" y donde se para cada NPC — o sea que corregir un
        texto, o la posicion de un sprite, no llegaba nunca a una partida en
        curso. Con esto si.

        SOLO SE TOCA EL CATALOGO, no el progreso. Todos esos campos se arman en
        el __init__ del Quest y nadie los muta en runtime (verificado por grep):
        las rutinas se LEEN en cada frame desde _buscar_rutina_quest_vigente,
        asi que refrescar el dict alcanza para que el cambio se vea. El estado
        real de la quest —etapa_actual, activa, completada, fallo_ocurrido— no
        se toca.

        Los requisitos NO se refrescan a proposito: cambiarlos a mitad de una
        partida podria destrabar o trabar el avance de golpe, que es otra cosa
        muy distinta de corregir un texto.

        SIRVE PARA LAS DOS CLASES DE QUEST, que guardan el texto distinto:
        `Quest` (los NPCs) en config_etapas + mensaje_pista, y `QuestMC` en
        _pista + _que_hacer_fn. Por eso se copia campo por campo con hasattr y
        no atributo por atributo a ciegas — y por eso NO entra
        `locaciones_pendientes` de QuestMC, que parece catalogo pero es
        progreso: se va vaciando a medida que el jugador recorre.
        """
        # nombre / descripcion / requisitos: textos de catalogo. Si no se
        # refrescaran, una correccion de texto (una tilde) dejaria al save con
        # el texto viejo — y como la traduccion se busca por el texto nuevo, en
        # ingles ese texto viejo se veria en castellano. `requisitos` es seguro
        # de pisar: un Requisito no guarda estado (tipo, mensaje, params).
        _CAMPOS = ("nombre", "descripcion", "requisitos",
                   "config_etapas", "mensaje_pista", "_pista", "_que_hacer_fn",
                   "rutina_quest", "rutinas_adicionales", "prioridad_rutina",
                   # planificador: lo declarado (no el estado)
                   "planificada", "de_corrido", "demandas", "consumos", "duenio",
                   "disparador")
        for _k, _fresca in fresco_dict.items():
            _cargada = cargado_dict.get(_k)
            if _cargada is None:
                continue
            for _campo in _CAMPOS:
                if hasattr(_fresca, _campo) and hasattr(_cargada, _campo):
                    setattr(_cargada, _campo,
                            _copy_ps.deepcopy(getattr(_fresca, _campo)))

    def _ps_merge_post_load():
        """after_load: inyecta contenido nuevo del catálogo en el save cargado."""

        # Quests (violet/monica/jasmine)
        try:
            _ps_merge_dict(
                _SISTEMAS_FRESCOS["sistema_quests"].quests,
                store.sistema_quests.quests, "quests")

            # Y a las que ya estaban, se les actualiza el catalogo (textos y rutinas).
            _ps_refrescar_quests(
                _SISTEMAS_FRESCOS["sistema_quests"].quests,
                store.sistema_quests.quests)

            # Reconstruir el indice por NPC desde .quests, que es la fuente real.
            # _ps_merge_dict solo llena .quests; quests_por_npc se arma en
            # registrar_quest() y por eso queda desactualizado al cargar. Sin este
            # rebuild, en un save viejo las quests nuevas (p.ej. las lineas de
            # amor/deseo) existen en .quests pero NO aparecen en
            # obtener_quests_npc() ni en obtener_quests_disponibles().
            # Es idempotente: se rearma entero en cada carga.
            _ps_idx_npc = {}
            for _q_idx in store.sistema_quests.quests.values():
                _ps_idx_npc.setdefault(_q_idx.npc_id, []).append(_q_idx)
            store.sistema_quests.quests_por_npc = _ps_idx_npc
        except Exception:
            pass

        # Rutinas de quest: lo que el catalogo fresco declara se copio arriba
        # (_CAMPOS), pero la copia que vive en npc.rutinas_quest se hizo al
        # entrar a ETAPA_RUTINA y quedo con la version vieja. Se reaplica para
        # toda quest viva: el NPC va a donde la quest dice HOY (Monica a la
        # cocina de noche en la 09_a). Respeta prioridad_rutina como siempre.
        try:
            for _q_rt in store.sistema_quests.quests.values():
                if (_q_rt.activa and not _q_rt.completada
                        and _q_rt.etapa_actual >= ETAPA_RUTINA
                        and (_q_rt.rutina_quest or _q_rt.rutinas_adicionales)):
                    _q_rt._aplicar_rutina_quest()
        except Exception as _e_rt:
            if config.developer:
                print("[Persistencia] reaplicar rutinas de quest: %r" % (_e_rt,))

        # Planificador — migracion de saves anteriores al punto de activacion
        # (0.1.9a y antes): una quest que ya esta jugandose no tiene
        # narrativa_activa, y la capa 2 la mediria como si estuviera por
        # empezar (con su propia restriccion en contra, p.ej. la pizza). La
        # unica señal segura es la restriccion activa con SU dueño: esa quest
        # esta adentro. Idempotente: activar() no repite.
        try:
            _r_pl = getattr(store, "restriccion_quest_activa", None)
            _duenio_pl = getattr(_r_pl, "duenio", None) if _r_pl is not None else None
            if _duenio_pl:
                for _q_pl in store.sistema_quests.quests.values():
                    if (_q_pl.activa and not _q_pl.completada
                            and _q_pl.etapa_actual == ETAPA_BOTON_LISTO
                            and getattr(_q_pl, "duenio", None) == _duenio_pl
                            and not getattr(_q_pl, "narrativa_activa", False)):
                        _q_pl.activar()
                        if config.developer:
                            print("[Planificador] migracion: %s marcada en narrativa (restriccion propia activa)" % _q_pl.id)
            # Reservas de quests que ya no estan: fuera.
            if not hasattr(store, "planificador_reservas"):
                store.planificador_reservas = []
        except Exception:
            pass

        # Quests del MC
        try:
            _ps_merge_dict(
                _SISTEMAS_FRESCOS["sistema_quests_mc"].quests,
                store.sistema_quests_mc.quests, "quests_mc")
            _ps_refrescar_quests(
                _SISTEMAS_FRESCOS["sistema_quests_mc"].quests,
                store.sistema_quests_mc.quests)
        except Exception:
            pass

        # Grupos de mensajes (via registrar_grupo para armar triggers/pendientes)
        try:
            _fresco_msg = _SISTEMAS_FRESCOS["sistema_mensajes"]
            for _gid, _g in _fresco_msg._todos_grupos.items():
                if _gid not in store.sistema_mensajes._todos_grupos:
                    store.sistema_mensajes.registrar_grupo(_g.npc_id, _copy_ps.deepcopy(_g))
                    continue

                # El grupo ya estaba en el save, con la conversacion del dia que
                # se guardo. Si TODAVIA NO EMPEZO se le refresca la definicion,
                # asi una correccion a los pasos llega a las partidas en curso;
                # antes se quedaban con la version vieja para siempre.
                _gc = store.sistema_mensajes._todos_grupos[_gid]
                if _gc is _g or _gc.paso_actual != 0 or _gc.estado == "en_curso":
                    # ⚠️ EMPEZADO: NO SE TOCA. `paso_actual` es un indice dentro
                    # de `pasos`, y cambiar la lista debajo lo deja apuntando a
                    # otra cosa — basta con que se haya insertado un paso para
                    # que la conversacion siga por donde no va. Un chat a medias
                    # se queda con la version con la que arranco.
                    continue
                _gc.pasos = _copy_ps.deepcopy(_g.pasos)
                _gc.mensaje_inicial = _copy_ps.deepcopy(_g.mensaje_inicial)
                _gc.foto_inicial = _g.foto_inicial
        except Exception:
            pass

        # SANEO de partidas que ya venian trabadas. Un grupo ACTIVO sin paso
        # valido es basura por definicion: no se puede contestar y nunca se va
        # a completar (bug de la generica de Mensajear en la 0.1.9 — dos
        # reportes). Con el fix del motor ya no bloquea, pero el chat quedaria
        # muerto para siempre. Se lo devuelve a "pendiente" con resetear(): si
        # es repetible vuelve a salir; si es de quest, al menos no estorba.
        # Los pendientes se ponen en paso 0 por si los entrego el codigo viejo
        # (que no reiniciaba el progreso).
        try:
            for _npc_c, _chat_c in store.sistema_mensajes.chats.items():
                _ga = _chat_c.grupo_activo
                if _ga is not None and _ga.pasos and _ga.obtener_paso_actual() is None:
                    if config.developer:
                        print("[Mensajes] saneo: '%s' de %s estaba activo sin paso; "
                              "se resetea" % (_ga.id, _npc_c))
                    _ga.resetear()
                    _chat_c.grupo_activo = None
                for _gp in list(_chat_c.grupos_pendientes):
                    if _gp.pasos and _gp.obtener_paso_actual() is None:
                        _gp.reiniciar_progreso()
        except Exception:
            pass

        # Talk: configs de NPCs nuevos + estados/opciones nuevos en configs existentes
        try:
            _fresco_talk = _SISTEMAS_FRESCOS["sistema_talk"]
            _ps_merge_dict(_fresco_talk._configs, store.sistema_talk._configs, "talk_configs")
            for _nid, _cfg_f in _fresco_talk._configs.items():
                _cfg_c = store.sistema_talk._configs.get(_nid)
                if _cfg_c is None or _cfg_c is _cfg_f:
                    continue
                _ids_estados = {_e.id for _e in _cfg_c.estados}
                for _e in _cfg_f.estados:
                    if _e.id not in _ids_estados:
                        _cfg_c.estados.append(_copy_ps.deepcopy(_e))
                for _gid in _cfg_f.estados_generales_ids:
                    if _gid not in _cfg_c.estados_generales_ids:
                        _cfg_c.estados_generales_ids.append(_gid)
                _ids_esp = {_o.id for _o in _cfg_c.opciones_especiales}
                for _o in _cfg_f.opciones_especiales:
                    if _o.id not in _ids_esp:
                        _cfg_c.opciones_especiales.append(_copy_ps.deepcopy(_o))
        except Exception:
            pass

        # Skins
        try:
            _ps_merge_dict(
                _SISTEMAS_FRESCOS["sistema_skins"].skins,
                store.sistema_skins.skins, "skins")
        except Exception:
            pass

        # Eventos (via registrar_event)
        try:
            _fresco_ev = _SISTEMAS_FRESCOS["sistema_events"]
            for _eid, _ev in _fresco_ev.events.items():
                if _eid not in store.sistema_events.events:
                    store.sistema_events.registrar_event(_copy_ps.deepcopy(_ev))
        except Exception:
            pass

    if not hasattr(config, "after_load_callbacks"):
        config.after_load_callbacks = []
    if _ps_merge_post_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_ps_merge_post_load)
