################################################################################
## Catálogo de Acciones de Locación
################################################################################
## Define todas las AccionLocacion del juego y sus labels genéricos.
## Los labels genéricos se ejecutan cuando no hay listeners de quest/evento.

init 5 python:

    # ── Quest 0 del MC — Mudanza ──────────────────────────────────────────────

    def _mc_q0_mudanza_garage_visible():
        return getattr(store, 'mc_q0_mudanza_garage_activa', False)

    def _mc_q0_mudanza_hmc_visible():
        return getattr(store, 'mc_q0_mudanza_hmc_activa', False)

    sistema_acciones.registrar_accion(AccionLocacion(
        id="mudanza_garage",
        nombre="Mudanza",
        icono=u"📦",
        locacion_id="casa_garage",
        label_generico="mudanza_garage_generico",
        reseteo=None,
        condicion=_mc_q0_mudanza_garage_visible,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="mudanza_hmc",
        nombre="Mudanza",
        icono=u"📦",
        locacion_id="casa_hmc",
        label_generico="mudanza_hmc_generico",
        reseteo=None,
        condicion=_mc_q0_mudanza_hmc_visible,
    ))

    def _vq9a_accion_activa():
        q = store.sistema_quests.obtener_quest("violet_questprincipal_09_a")
        return (q is not None and q.activa and not q.completada and
                q.etapa_actual == ETAPA_BOTON_LISTO and
                getattr(store, 'violet_9a_pedido_actual', None) is not None and
                not getattr(store, 'violet_9a_entrega_completada', False))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq9a_heladera",
        nombre="Heladera",
        icono=u"🧊",
        locacion_id="casa_cocina",
        label_generico="accion_violet_heladera",
        reseteo=None,
        condicion=_vq9a_accion_activa,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq9a_agua",
        nombre="Agua",
        icono=u"💧",
        locacion_id="casa_cocina",
        label_generico="accion_violet_agua",
        reseteo=None,
        condicion=_vq9a_accion_activa,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq9a_medicina",
        nombre="Medicina",
        icono=u"💊",
        locacion_id="casa_banioabajo",
        label_generico="accion_violet_medicina",
        reseteo=None,
        condicion=_vq9a_accion_activa,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq9a_toalla",
        nombre="Toalla",
        icono=u"🛁",
        locacion_id="casa_banioarriba",
        label_generico="accion_violet_toalla",
        reseteo=None,
        condicion=_vq9a_accion_activa,
    ))

    # =========================================================================
    # EVENTO 03 — Limpieza del Sábado
    # =========================================================================

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ev03_limpiar_living",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_living",
        label_generico="ev03_accion_limpiar_living",
        reseteo=None,
        condicion=lambda: getattr(store, 'vq2_limpiar_accion_activa', False),
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ev03_buscar_cocina",
        nombre="Buscar",
        icono=u"🔍",
        locacion_id="casa_cocina",
        label_generico="ev03_accion_buscar_cocina",
        reseteo=None,
        condicion=lambda: getattr(store, 'vq2_buscar_accion_activa', False),
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ev03_limpiar_pasillo",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_pasilloarriba",
        label_generico="ev03_accion_limpiar_pasillo",
        reseteo=None,
        condicion=lambda: getattr(store, 'vq2_limpiar_pasillo_accion_activa', False),
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="cocinar",
        nombre="Cocinar",
        icono=u"🍳",
        locacion_id="casa_cocina",
        label_generico="accion_cocinar",
        reseteo="diario",
        mensaje_reintento=u"Estoy cansado hoy, quizás debería intentarlo mañana.",
        color="#E65100",
        color_hover="#FF9800",
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ver_tv",
        nombre="Ver TV",
        icono=u"📺",
        locacion_id="casa_living",
        label_generico="accion_ver_tv",
        reseteo="diario",
        mensaje_reintento=None,
        color="#4527A0",
        color_hover="#7E57C2",
    ))


################################################################################
## Label: Cocinar
################################################################################

label accion_cocinar:

    $ sistema_acciones.marcar_usada("cocinar")
    $ ocultar_hud()

    # Aplicar stats antes del texto — las notificaciones quedan en el overlay
    $ obtener_npc("violet").modificar_stat1(1)
    $ obtener_npc("monica").modificar_stat1(1)
    $ obtener_npc("jasmine").modificar_stat1(1)

    # Efecto especial: si Violet tenia hambre y el jugador aún no habló con ella hoy
    $ _ac_v = obtener_npc("violet")
    if _ac_v and _ac_v.talk_estado_id == "violet_hambre" and _ac_v.estado_posterior_id is None:
        $ activar_estado_especial_npc("violet", "violet_feliz")

    window show

    if horario_actual == 0:
        "Preparas el desayuno para todos, las chicas parecen estar muy contentas."
    elif horario_actual == 1:
        "Preparas la merienda para todos, las chicas parecen estar muy contentas."
    else:
        "Preparas la cena para todos, las chicas parecen estar muy contentas."

    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    return


################################################################################
## Label: Ver TV
################################################################################

label accion_ver_tv:

    # Quest 08_a de Violet: la accion Ver TV es el disparador de la escena de la
    # tormenta. Se chequea antes que cualquier restricción horaria.
    $ _q8a_vertv = sistema_quests.obtener_quest("violet_questprincipal_08_a")
    if _q8a_vertv and _q8a_vertv.activa and not _q8a_vertv.completada and _q8a_vertv.etapa_actual == ETAPA_BOTON_LISTO:
        jump violet_quest08a_ver_tv

    # Restricción: solo de noche
    if horario_actual < 2:
        piensa "La casa está muy activa como para ver una película, podría intentarlo por la noche."
        return

    $ sistema_acciones.marcar_usada("ver_tv")
    $ ocultar_hud()

    # Elegir NPC al azar (o nadie) y aplicar stat antes del texto
    $ _vtv_npc_id = renpy.random.choice(["violet", "monica", "jasmine", None])

    if _vtv_npc_id is not None:
        $ _vtv_npc = obtener_npc(_vtv_npc_id)
        $ _vtv_nombre = _vtv_npc.nombre if _vtv_npc else _vtv_npc_id
        $ _vtv_npc.modificar_stat2(1)

    window show

    if _vtv_npc_id is not None:
        "Te sentaste a ver una película, a los minutos apareció [_vtv_nombre] y se unió. Compartieron un lindo momento juntos."
    else:
        "Aprovechaste la noche para ver una película y relajar un poco."

    window hide
    $ avanzar_horario()
    $ mostrar_hud()
    return
