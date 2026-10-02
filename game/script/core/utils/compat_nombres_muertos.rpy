################################################################################
## Nombres muertos — que un save viejo NUNCA falle al abrirse
################################################################################
## EL PROBLEMA (bug real, Sentry d011e4b3, 2026-09-15, jugador en 0.1.9.1):
##
##     AttributeError: Can't get attribute
##     'condicion_aparicion_evento01_violet' on <StoreModule object>
##     ... renpy/loadsave.py:636 in load → pickle find_class
##
## Un save guarda por REFERENCIA las funciones de modulo que quedan dentro de
## objetos guardados: `Event.condicion_aparicion/activacion`, los textos
## callables de `ConfigEtapa`, `ConfigFallo.condicion`, `EstadoTalk.condicion`,
## `Skin.condicion_desbloqueo`, `GrupoMensajes.condicion/accion_al_completar`.
## El pickle no guarda el codigo: guarda `store` + el NOMBRE. Al cargar, el
## unpickler hace getattr(store, nombre) — y si la funcion se borro o se
## renombro, revienta.
##
## POR QUE NO ALCANZA CON EL CONTROL DE GENERACIONES (compatibilidad_saves.rpy):
## ese control decide si una partida se puede seguir jugando, pero corre DESPUES
## de cargarla. El unpickle pasa antes que cualquier codigo nuestro, asi que un
## nombre faltante se lleva puesto el juego con la pantalla de error, incluso
## cuando la partida iba a rechazarse igual. Con los stubs de aca, el save abre
## siempre y el rechazo (si corresponde) sale prolijo por `after_load`.
##
## COMO SE MANTIENE: al BORRAR o RENOMBRAR una funcion de modulo que pueda
## haber quedado guardada, se agrega su nombre viejo a la lista. Para
## encontrarlas todas de una version publicada a esta:
##
##     git ls-tree -r --name-only <rev> game/script/   → defs de esa rev
##     menos las defs de hoy = las candidatas
##
## El stub devuelve "" a proposito: sirve como condicion (es falsy, asi que un
## evento/skin/estado muerto simplemente no aparece) y como texto (no dibuja
## nada). Los catalogos se refrescan igual al cargar (persistencia_sistemas), asi
## que el stub solo tiene que sobrevivir al unpickle.
################################################################################

init -100 python:

    def _jp_nombre_muerto(*args, **kwargs):
        """Reemplazo inerte de una funcion borrada que quedo en saves viejos."""
        return u""

    # Nombres borrados o renombrados desde la 0.1.8f. Agrupados por tanda.
    JP_NOMBRES_MUERTOS = [
        # Evento 01 de Violet (el casco de realidad virtual) — borrado en
        # 0.1.8.6 (309f03b). Es el que rompio la carga del jugador.
        "condicion_aparicion_evento01_violet",
        "condicion_activacion_evento01_violet",
        "pista_evento01_violet",
        "quehacer_evento01_violet",
        "_evento01_violet_tiene_casco",
        "_evento01_violet_casco_en_camino",

        # Sistema de espiar (borrado con el rediseño de ventajas).
        "_esp_acc_abrir_visible",
        "_esp_acc_foto_habilitada",
        "_esp_acc_foto_visible",
        "_esp_acc_unirse_visible",
        "_esp_nombre_abrir",
        "_espiar_fotos_restantes",
        "_espiar_reaccion_fallo",
        "espiar_prob_abrir",
        "espiar_prob_foto",
        "npc_espiar_disponible",
        "registrar_espiar_npc",

        # Lineas de amor/deseo de Violet, antes del rediseño de sus quests.
        "_pista_va15_condiciones",
        "_quehacer_va15_condiciones",
        "_va15_buscar_visible",
        "_va15_chat_completado",
        "_va15_chat_separados",
        "_va15_paso_un_dia",
        "_va30_boton_violet",
        "_va30_chat_condiciones",
        "_va30_disparar_chat",
        "_va30_puerta_ayuda",
        "_vd20_mc_afuera",
        "_vd25_activa",
        "_vd25_boton_violet",
        "_vd25_puerta_ver_anime",
        "_mv_aburrida_condicion",

        # Quest 0 del MC (tutorial de exploracion, rehecho).
        "_gl_trigger_mc_q0_exploracion",
        "mc_q0_exploracion_terminada",
        "mc_q0_locs_exploracion",
        "mc_q0_mensaje_faltantes",
        "mc_q0_mensaje_ubicacion",
        "mc_q0_registrar_exploracion",

        # Quests de Violet: helpers de escena que ya no existen.
        "_gl_trigger_violet_09a_piensa",
        "_vq3a_muñecos_visible",
        "post_completar_violet_quest0",
        "puerta_por_stage",
        "set_vq7_rama_a",
        "set_vq7_rama_b",
        "set_vq7_rama_c",

        # Motor: piezas retiradas con el controlador de quests (0.1.9.1).
        "intentar_ejecutar",
        "intentar_iniciar_quest_actual",
        "obtener_validacion_faltante",
        "validacion_especial",

        # Varios del motor / herramientas.
        "_resolver_conflictos_banio",
        "_stat_acceso_npc",
        "agregar_desbloqueo",
        "cheat_violet_al_bano",
        "cheat_violet_restaurar",
    ]

    # Solo se define lo que HOY no existe: si un nombre volvio al codigo, manda
    # el de verdad. (`hasattr` sobre el store, no sobre este scope.)
    for _jp_nm in JP_NOMBRES_MUERTOS:
        if not hasattr(store, _jp_nm):
            setattr(store, _jp_nm, _jp_nombre_muerto)
    del _jp_nm
