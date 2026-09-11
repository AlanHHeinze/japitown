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

    def _vq9b_toalla_activa():
        """
        La Toalla vuelve a aparecer en el desenlace de la 09_b: Violet la manda
        a buscar cuando el MC la visita. Es la MISMA accion del baño de arriba
        —no un boton nuevo— porque para el jugador es lo mismo que ya hizo.
        """
        return (_vq9b_quest_viva()
                and getattr(store, 'vq9b_rama', None) == "positivo"
                and getattr(store, 'vq9b_visito', False)
                and not getattr(store, 'vq9b_toalla', False))

    def _vq9a_toalla_visible():
        """La Toalla sirve para las dos etapas: el pedido diario y el desenlace."""
        return _vq9a_accion_activa() or _vq9b_toalla_activa()

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
        condicion=_vq9a_toalla_visible,
    ))

    # =========================================================================
    # EVENTO 03 — Limpieza del Sábado
    # =========================================================================

    # Condiciones como funciones de módulo (NO lambdas), por convención anti-PicklingError.
    def _ev03_limpiar_living_activa():
        return getattr(store, 'vq2_limpiar_accion_activa', False)

    def _ev03_buscar_cocina_activa():
        return getattr(store, 'vq2_buscar_accion_activa', False)

    def _ev03_limpiar_pasillo_activa():
        return getattr(store, 'vq2_limpiar_pasillo_accion_activa', False)

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ev03_limpiar_living",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_living",
        label_generico="ev03_accion_limpiar_living",
        reseteo=None,
        condicion=_ev03_limpiar_living_activa,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ev03_buscar_cocina",
        nombre="Buscar",
        icono=u"🔍",
        locacion_id="casa_cocina",
        label_generico="ev03_accion_buscar_cocina",
        reseteo=None,
        condicion=_ev03_buscar_cocina_activa,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="ev03_limpiar_pasillo",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_pasilloarriba",
        label_generico="ev03_accion_limpiar_pasillo",
        reseteo=None,
        condicion=_ev03_limpiar_pasillo_activa,
    ))

    # =========================================================================
    # VIOLET — Arco de los favores (quests 04_d4 y 04_d5)
    # =========================================================================
    # La LIMPIEZA usa acciones propias (no existe una accion generica de
    # limpiar), pero la PIZZA usa un LISTENER sobre la accion "cocinar" —
    # mismo patron que la quest 0_b.
    #
    # Por que listener y no una accion propia: con una accion aparte quedaban
    # DOS botones de Cocinar en la cocina, el generico y el de la quest. El
    # listener intercepta el que ya existe y no agrega ninguno.
    #
    # Y no hace falta preocuparse por el "ya cocinaste hoy": el ejecutor
    # (accion_locacion_ejecutar) chequea los listeners ANTES que el bloqueo por
    # accion usada, asi que con listener valido la quest siempre pasa. Ademas el
    # boton nunca queda gris, porque "cocinar" tiene mensaje_reintento.
    #
    # DIFERENCIA CON LA 0_b: alla el listener se registra en runtime, dentro del
    # label. Eso se pierde al cargar la partida (sistema_acciones es `define`).
    # Acá va en init con condicion por flag, que es la regla del proyecto.

    def _vq0b_cocinar_visible():
        # Quest 0_b de Violet: entre aceptar preparar la pizza y cocinarla.
        # Se DERIVA de estado que ya se guarda: `vq0b_ruta` se pone justo antes
        # de la restriccion en las dos ramas, y la quest se completa al final
        # del cierre. Sin flag nuevo, y una partida trabada con el codigo viejo
        # (listener perdido al cargar) queda cubierta sola.
        if getattr(store, 'vq0b_ruta', "") not in ("respeto", "confrontar"):
            return False
        _q = store.sistema_quests.obtener_quest("violet_questprincipal_0_b")
        return bool(_q and _q.activa and not _q.completada)

    def _vq4d4_cocinar_visible():
        # Solo de noche: la pizza es para la cena.
        return (getattr(store, 'vq4d4_pedido_hecho', False)
                and not getattr(store, 'vq4d4_pizza_cocinada', False)
                and store.horario_actual == 2)

    def _vq4d5_limpiar_living_visible():
        return (getattr(store, 'vq4d5_pedido_hecho', False)
                and not getattr(store, 'vq4d5_limpio_living', False))

    def _vq4d5_limpiar_comedor_visible():
        return (getattr(store, 'vq4d5_pedido_hecho', False)
                and not getattr(store, 'vq4d5_limpio_comedor', False))

    def _vq4d5_limpiar_cocina_visible():
        return (getattr(store, 'vq4d5_pedido_hecho', False)
                and not getattr(store, 'vq4d5_limpio_cocina', False))

    # Quest 0_b de Violet: la primera pizza. Mismo esquema que la 04_d4 de
    # abajo — unico=False y apagado por flag, porque una mutacion de la lista
    # no sobrevive al save. Antes se registraba en runtime dentro de la quest y
    # cargar una partida guardada en el medio la dejaba trabada.
    sistema_acciones.registrar_listener(ListenerAccion(
        accion_id="cocinar",
        label="quest_violet_0_cierre",
        nombre_menu="Preparar las pizzas",
        prioridad="quest",
        condicion=_vq0b_cocinar_visible,
        unico=False,
    ))

    # La pizza NO agrega boton: intercepta el de "Cocinar" que ya esta en la
    # cocina. unico=False a proposito — post_ejecutar() borraria el listener de
    # la lista, y esa mutacion se pierde al cargar la partida; el que lo apaga
    # es el flag vq4d4_pizza_cocinada, que si se guarda.
    sistema_acciones.registrar_listener(ListenerAccion(
        accion_id="cocinar",
        label="violet_q4d4_cocinar",
        nombre_menu="Preparar las pizzas",
        prioridad="quest",
        condicion=_vq4d4_cocinar_visible,
        unico=False,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq4d5_limpiar_living",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_living",
        label_generico="violet_q4d5_limpiar_living",
        reseteo=None,
        condicion=_vq4d5_limpiar_living_visible,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq4d5_limpiar_comedor",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_comedor",
        label_generico="violet_q4d5_limpiar_comedor",
        reseteo=None,
        condicion=_vq4d5_limpiar_comedor_visible,
    ))

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq4d5_limpiar_cocina",
        nombre="Limpiar",
        icono=u"🧹",
        locacion_id="casa_cocina",
        label_generico="violet_q4d5_limpiar_cocina",
        reseteo=None,
        condicion=_vq4d5_limpiar_cocina_visible,
    ))

    # ── Violet Amor 25 — el domingo solos en casa ────────────────────────────
    # No agrega botones nuevos: intercepta "cocinar" y "ver_tv", que ya existen.
    # Los tres listeners son excluyentes (los separa la fase), asi que nunca hay
    # dos compitiendo por la misma accion.
    #
    # unico=False a proposito: post_ejecutar() borraria el listener de la lista,
    # y esa mutacion se pierde al cargar la partida. Los apaga la condicion, que
    # lee un flag `default` y si se guarda. (Mismo criterio que la pizza 04_d4.)
    sistema_acciones.registrar_listener(ListenerAccion(
        accion_id="cocinar",
        label="violet_amor_25_pasar_cocina",
        nombre_menu="Comer algo",
        prioridad="quest",
        condicion=_va25_listener_pasatiempo,
        unico=False,
    ))
    sistema_acciones.registrar_listener(ListenerAccion(
        accion_id="ver_tv",
        label="violet_amor_25_pasar_tv",
        nombre_menu="Ver algo",
        prioridad="quest",
        condicion=_va25_listener_pasatiempo,
        unico=False,
    ))
    sistema_acciones.registrar_listener(ListenerAccion(
        accion_id="cocinar",
        label="violet_amor_25_cocinar",
        nombre_menu="Hacer la cena",
        prioridad="quest",
        condicion=_va25_listener_cena,
        unico=False,
    ))

    # ── Violet Amor 20 — comprar el juego y jugarlo ──────────────────────────
    # Las dos son excluyentes (fase 1 y fase 2), asi que nunca conviven en el
    # panel. Las condiciones viven en violet_amor_20.rpy y leen va20_fase.
    sistema_acciones.registrar_accion(AccionLocacion(
        id="va20_comprar_juego",
        nombre="Comprar juego",          # lo pisa nombre_dinamico (lleva el precio)
        nombre_dinamico=_va20_nombre_comprar,
        icono=u"🎮",
        locacion_id="casa_hmc",
        label_generico="violet_amor_20_comprar",
        reseteo=None,
        condicion=_va20_comprar_visible,
    ))

    # La pone primero la quest de amor 20 y despues, para siempre, la ventaja
    # "accion_jugar" de su hito. reseteo diario + mensaje_reintento resuelven el
    # "una vez por dia" de la ventaja sin flag propio; durante la quest no
    # molestan porque usarla con exito la completa.
    sistema_acciones.registrar_accion(AccionLocacion(
        id="va20_jugar",
        nombre="Jugar",
        icono=u"🎮",
        locacion_id="casa_hmc",
        label_generico="violet_amor_20_jugar",
        reseteo="diario",
        mensaje_reintento=u"Ya jugué suficiente por hoy",
        condicion=_va20_jugar_visible,
    ))

    # ── Violet Deseo 15 — el estreno del anime en el sotano ──────────────────
    # Es una accion PROPIA y no un listener sobre el "ver_tv" del living: son
    # dos televisores en dos locaciones distintas. Existe solo mientras la quest
    # esta lista (la condicion vive en violet_deseo_15.rpy).
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vd15_ver_tv_sotano",
        nombre="Ver TV",
        icono=u"📺",
        locacion_id="casa_sotano",
        label_generico="violet_deseo_15_ver_tv",
        reseteo="diario",
        mensaje_reintento=u"Ya vi suficiente por hoy",
        condicion=_vd15_ver_tv_visible,
        color="#4527A0",
        color_hover="#7E57C2",
    ))

    # ── Violet Deseo 25 — el planton en el sotano ────────────────────────────
    # No agrega boton: intercepta el "Ver TV" del sotano de acá arriba, que para
    # cuando esta quest esta lista ya existe como la ventaja "Ver Anime" del
    # hito de deseo 20. Un segundo boton en la misma locacion seria un "Ver TV"
    # al lado del otro.
    #
    # El listener corre ANTES de los bloqueos y del "ya la usaste hoy", asi que
    # la quest arranca aunque el jugador ya haya visto anime esa noche.
    #
    # unico=False a proposito: post_ejecutar() borraria el listener de la lista,
    # y esa mutacion se pierde al cargar la partida. Lo apaga la condicion, que
    # lee vd25_fase — un flag `default`, que si se guarda.
    sistema_acciones.registrar_listener(ListenerAccion(
        accion_id="vd15_ver_tv_sotano",
        label="violet_deseo_25_sotano",
        nombre_menu="Ver TV",
        prioridad="quest",
        condicion=_vd25_listener_sotano,
        unico=False,
    ))

    # ── Juego Nuevo "Pocket Boy" — revolver el altillo (arco PARKEADO) ───────
    # El contenido vive en ventajas/juegosnuevos/jn_pocketboy.rpy, pero la
    # accion se registra acá como todas. Hoy no aparece nunca: su condicion mira
    # jnpb_fase, que ese arco no mueve porque esta apagado.
    sistema_acciones.registrar_accion(AccionLocacion(
        id="jnpb_buscar",
        nombre="Buscar",
        icono=u"🔍",
        locacion_id="casa_altillo",
        label_generico="jn_pocketboy_cierre",
        reseteo=None,
        condicion=_jnpb_buscar_visible,
    ))

    # ── Violet Deseo 10 — el vaso de agua de madrugada ───────────────────────
    # Solo existe entre el despertar con sed y la escena. La condicion vive en
    # violet_deseo_10.rpy y lee el flag vd10_sed_activa.
    #
    # Registrada acá y no en runtime desde el label: sistema_acciones es
    # `define` y no se guarda, asi que un registro hecho en runtime desaparece
    # al cargar la partida y dejaria la quest trabada sin forma de dispararla.
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vd10_tomar_agua",
        nombre="Tomar agua",
        icono=u"🥤",
        locacion_id="casa_cocina",
        label_generico="quest_violet_deseo_02",
        reseteo=None,
        condicion=_vd10_tomar_agua_visible,
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

    # ── Violet Quest 03_a — Exploración de la habitación ─────────────────────
    # Registradas en init (NO en runtime): sistema_acciones es define y no se
    # guarda; un registro en runtime desaparece al cargar la partida y traba la
    # quest. La visibilidad la controlan flags default via condicion.

    def _vq3a_peluches_visible():
        return getattr(store, 'vq3a_fase1_activa', False) and not store.vq3a_peluches_hecho

    def _vq3a_pc_visible():
        return getattr(store, 'vq3a_fase1_activa', False) and not store.vq3a_pc_hecho

    def _vq3a_manga_visible():
        return getattr(store, 'vq3a_fase1_activa', False) and not store.vq3a_manga_hecho

    def _vq3a_muñecos_visible():
        return getattr(store, 'vq3a_fase1_activa', False) and not store.vq3a_muñecos_hecho

    def _vq3a_mochila_visible():
        return getattr(store, 'vq3a_fase1_activa', False) and not store.vq3a_mochila_hecho

    def _vq3a_ropero_visible():
        return getattr(store, 'vq3a_fase2_activa', False) and not store.vq3a_ropero_hecho

    def _vq3a_cajonera_visible():
        return getattr(store, 'vq3a_fase2_activa', False) and not store.vq3a_cajonera_hecho

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_peluches", nombre="Peluches", icono=u"🧸",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_peluches",
        reseteo=None, color="#8E24AA", color_hover="#AB47BC",
        condicion=_vq3a_peluches_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_pc", nombre="PC", icono=u"💻",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_pc",
        reseteo=None, color="#1565C0", color_hover="#1E88E5",
        condicion=_vq3a_pc_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_manga", nombre="Manga", icono=u"📚",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_manga",
        reseteo=None, color="#C62828", color_hover="#EF5350",
        condicion=_vq3a_manga_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_muñecos", nombre="Muñecos", icono=u"🎎",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_muñecos",
        reseteo=None, color="#00695C", color_hover="#00897B",
        condicion=_vq3a_muñecos_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_mochila", nombre="Mochila", icono=u"🎒",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_mochila",
        reseteo=None, color="#E65100", color_hover="#FB8C00",
        condicion=_vq3a_mochila_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_ropero", nombre="Ropero", icono=u"🚪",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_ropero",
        reseteo=None, color="#4527A0", color_hover="#7E57C2",
        condicion=_vq3a_ropero_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq3a_cajonera", nombre="Cajonera", icono=u"🗂️",
        locacion_id="casa_hviolet", label_generico="vq3a_accion_cajonera",
        reseteo=None, color="#2E7D32", color_hover="#43A047",
        condicion=_vq3a_cajonera_visible,
    ))

    # ── Violet Quest 08_a — Ropero y cajonera durante la tormenta ────────────

    def _vq8a_ropero_visible():
        return getattr(store, 'vq8a_acciones_activas', False) and not store.vq8a_ropero_visto

    def _vq8a_cajonera_visible():
        return getattr(store, 'vq8a_acciones_activas', False) and not store.vq8a_cajonera_vista

    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq8a_ropero", nombre="Ropero", icono=u"🚪",
        locacion_id="casa_hviolet", label_generico="violet_quest08a_accion_ropero",
        reseteo=None, color="#4527A0", color_hover="#7E57C2",
        condicion=_vq8a_ropero_visible,
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="vq8a_cajonera", nombre="Cajonera", icono=u"🗂️",
        locacion_id="casa_hviolet", label_generico="violet_quest08a_accion_cajonera",
        reseteo=None, color="#2E7D32", color_hover="#43A047",
        condicion=_vq8a_cajonera_visible,
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
        $ _blk_guardar_toque()
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


################################################################################
## Acciones mudadas desde otros archivos
################################################################################
## Vivian en el archivo de su propio sistema. Se trajeron acá para que TODAS las
## acciones del juego esten en un solo lugar (ver la cabecera). Sus funciones de
## condicion siguen viviendo en el archivo de origen, que corre en `init python`
## (prioridad 0) y por lo tanto antes que este `init 5`.

init 5 python:

    # ── Espiar — botones del minijuego (globales, locacion_id=None) ──
    sistema_acciones.registrar_accion(AccionLocacion(
        id="espiar_entrar", nombre="Entrar", icono=u"🚶",
        locacion_id=None, label_generico="accion_espiar_entrar",
        reseteo=None, condicion=_esp_acc_entrar_visible,
        condicion_habilitada=_esp_acc_entrar_habilitada,
        color="#8E24AA", color_hover="#AB47BC",
    ))
    sistema_acciones.registrar_accion(AccionLocacion(
        id="espiar_salir", nombre="Salir", icono=u"❌",
        locacion_id=None, label_generico="accion_espiar_salir",
        reseteo=None, condicion=_esp_acc_salir_visible,
        color="#37474F", color_hover="#546E7A",
    ))

    # ── Herramienta de dev — ver salidas de la locacion ──
    sistema_acciones.registrar_accion(AccionLocacion(
        id="visualizador_hotspot",
        nombre="Ver salidas",
        icono=u"👁",
        locacion_id=None,
        label_generico="visualizador_hotspot_toggle",
        reseteo=None,
        condicion=_cond_accion_movimiento,
        color="#37474F",
        color_hover="#546E7A",
    ))
