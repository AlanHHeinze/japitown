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

    def _ps_merge_post_load():
        """after_load: inyecta contenido nuevo del catálogo en el save cargado."""

        # Quests (violet/monica/jasmine)
        try:
            _ps_merge_dict(
                _SISTEMAS_FRESCOS["sistema_quests"].quests,
                store.sistema_quests.quests, "quests")

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

        # Quests del MC
        try:
            _ps_merge_dict(
                _SISTEMAS_FRESCOS["sistema_quests_mc"].quests,
                store.sistema_quests_mc.quests, "quests_mc")
        except Exception:
            pass

        # Grupos de mensajes (via registrar_grupo para armar triggers/pendientes)
        try:
            _fresco_msg = _SISTEMAS_FRESCOS["sistema_mensajes"]
            for _gid, _g in _fresco_msg._todos_grupos.items():
                if _gid not in store.sistema_mensajes._todos_grupos:
                    store.sistema_mensajes.registrar_grupo(_g.npc_id, _copy_ps.deepcopy(_g))
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
