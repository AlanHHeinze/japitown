image escena_final_quest0_mc = "images/quest/mc/quest0/escena_final_quest0_mc.png"

################################################################################
## Quest 0 del MC — De nuevo en casa
################################################################################
## El MC recorre la casa para familiarizarse con ella recién llegado.
## Fase 1: Explorar el Living (todos sus hotspots MOVE).
## Fase 2: Explorar Pasillo Abajo, Pasillo Arriba y Patio.

# ── Estado de la quest ──────────────────────────────────────────────────────
default mc_q0_interceptar_movimiento = False
default mc_q0_fase = 0
default mc_q0_hotspots_visitados = {}      # {loc_id: set_of_hotspot_ids}
default mc_q0_primer_click = {}            # {loc_id: bool}
default mc_q0_locaciones_exploradas = set()
default mc_q0_entrada_mostrada = set()

# Fase mudanza
default mc_q0_cajas_en_garage = False
default mc_q0_mudanza_garage_activa = False
default mc_q0_mudanza_hmc_activa = False
default mc_q0_entrada_garage_mostrada = False

# Fase espera / stage B / sueño final
default mc_q0_esperar_horario = False
default mc_q0_final_sleep = False


# ── Constantes ───────────────────────────────────────────────────────────────

init 5 python:
    # Idle de cajas en el garage — posicionable con la herramienta (P)
    sistema_pos.registrar(
        "mc_q0_cajas_intro",
        "images/quest/mc/quest0/idle_cajas_intro.png",
        "Cajas intro",
        "quest_elemento",
        960, 900,
        xanchor=0.5, yanchor=1.0,
    )


init python:

    MC_Q0_HOTSPOTS_LIVING = frozenset({
        "casa_living_casa_pasilloabajo",
        "casa_living_casa_frente",
        "casa_living_casa_garage",
        "casa_living_casa_patio",
        "casa_living_casa_pasilloarriba",
    })

    MC_Q0_HOTSPOTS_FASE2 = {
        "casa_pasilloabajo": frozenset({
            "casa_pasilloabajo_casa_banioabajo",
            "casa_pasilloabajo_casa_hmonica",
            "casa_pasilloabajo_casa_cocina",
        }),
        "casa_pasilloarriba": frozenset({
            "casa_pasilloarriba_casa_hmc",
            "casa_pasilloarriba_casa_banioarriba",
            "casa_pasilloarriba_casa_hviolet",
            "casa_pasilloarriba_casa_hjasmine",
            "casa_pasilloarriba_casa_altillo",
        }),
        "casa_patio": frozenset({
            "casa_patio_casa_frente",
            "casa_patio_casa_gym",
            "casa_patio_casa_comedor",
        }),
    }

    MC_Q0_LOCS_FASE2 = frozenset({"casa_pasilloabajo", "casa_pasilloarriba", "casa_patio"})

    MC_Q0_NOMBRES_DESTINO = {
        "casa_living":       "el Living",
        "casa_pasilloabajo": "el Pasillo de Abajo",
        "casa_pasilloarriba":"el Pasillo de Arriba",
        "casa_patio":        "el Patio",
        "casa_frente":       "la Salida",
        "casa_garage":       "el Garage",
        "casa_cocina":       "la Cocina",
        "casa_comedor":      "el Comedor",
        "casa_gym":          "el Gym",
        "casa_hmc":          "mi Habitación",
        "casa_hmonica":      "la Habitación de Mónica",
        "casa_hviolet":      "la Habitación de Violet",
        "casa_hjasmine":     "la Habitación de Jasmine",
        "casa_banioabajo":   "el Baño de Abajo",
        "casa_banioarriba":  "el Baño de Arriba",
        "casa_baniomonica":  "el Baño de Mónica",
        "casa_altillo":      "el Altillo",
        "casa_sotano":       "el Sótano",
    }


# ── Helpers Python ────────────────────────────────────────────────────────────

init python:

    def mc_q0_debe_interceptar():
        """True cuando el clic en el hotspot actual debe ser manejado por la quest."""
        ht = store._hotspot_temp
        if not ht or not ht.destino:
            return False
        dest  = ht.destino
        fase  = getattr(store, 'mc_q0_fase', 0)
        loc   = store.sistema_locaciones.locacion_actual
        loc_id = loc.id if loc else ""

        if fase == 1:
            return True

        if fase == 2:
            if loc_id == "casa_living":
                # Desde living: interceptar solo destinos fuera de la fase 2
                return dest not in MC_Q0_LOCS_FASE2
            if loc_id in MC_Q0_LOCS_FASE2:
                # Si la locacion NO está completa, bloquear TODO movimiento (incluido living)
                if loc_id not in store.mc_q0_locaciones_exploradas:
                    return True
                # Completa: solo permitir ir al living (conector)
                return dest != "casa_living"

        return False

    # ──────────────────────────────────────────────────────────────────────────

    def mc_q0_registrar_visita(loc_id, hotspot_id):
        visitados = dict(store.mc_q0_hotspots_visitados)
        if loc_id in visitados:
            visitados[loc_id] = set(visitados[loc_id])
        else:
            visitados[loc_id] = set()
        visitados[loc_id].add(hotspot_id)
        store.mc_q0_hotspots_visitados = visitados

    def mc_q0_locacion_completa(loc_id):
        if loc_id == "casa_living":
            requeridos = MC_Q0_HOTSPOTS_LIVING
        else:
            requeridos = MC_Q0_HOTSPOTS_FASE2.get(loc_id, frozenset())
        visitados = store.mc_q0_hotspots_visitados.get(loc_id, set())
        return requeridos.issubset(visitados)

    def mc_q0_str_faltantes_hotspots(loc_id):
        """Lista legible de destinos no visitados en loc_id."""
        if loc_id == "casa_living":
            requeridos = MC_Q0_HOTSPOTS_LIVING
        else:
            requeridos = MC_Q0_HOTSPOTS_FASE2.get(loc_id, frozenset())
        visitados = store.mc_q0_hotspots_visitados.get(loc_id, set())
        faltantes  = requeridos - visitados
        if not faltantes:
            return ""
        loc = store.sistema_locaciones.locacion_actual
        nombres = []
        if loc:
            for h in loc.hotspots:
                if h.id in faltantes and h.destino:
                    nombres.append(MC_Q0_NOMBRES_DESTINO.get(h.destino, h.destino))
        if not nombres:
            return ""
        if len(nombres) == 1:
            return nombres[0]
        return ", ".join(nombres[:-1]) + " y " + nombres[-1]

    def mc_q0_str_faltantes_fase2():
        """Lista legible de locaciones fase 2 sin completar."""
        exploradas = store.mc_q0_locaciones_exploradas
        faltantes  = MC_Q0_LOCS_FASE2 - exploradas
        nombres_map = {
            "casa_pasilloabajo":  "el Pasillo de Abajo",
            "casa_pasilloarriba": "el Pasillo de Arriba",
            "casa_patio":         "el Patio",
        }
        nombres = [nombres_map[l] for l in faltantes if l in nombres_map]
        if not nombres:
            return ""
        if len(nombres) == 1:
            return nombres[0]
        return ", ".join(nombres[:-1]) + " y " + nombres[-1]

    def mc_q0_activar_rutinas_npc():
        """Pone a Monica, Jasmine y Violet en sus habitaciones para toda la quest."""
        habitaciones = {
            "monica":  "casa_hmonica",
            "jasmine": "casa_hjasmine",
            "violet":  "casa_hviolet",
        }
        for npc_id, hab in habitaciones.items():
            npc = obtener_npc(npc_id)
            if npc:
                npc.rutinas_quest.clear()
                for dia in range(7):
                    for horario in range(4):
                        npc.rutinas_quest[(dia, horario)] = RutinaQuest(locacion=hab)
        actualizar_rutinas_npcs()

    def mc_q0_limpiar_rutinas_npc():
        """Restaura rutinas normales de los NPCs."""
        for npc_id in ["monica", "jasmine", "violet"]:
            npc = obtener_npc(npc_id)
            if npc:
                npc.rutinas_quest.clear()
        actualizar_rutinas_npcs()


################################################################################
## Label principal — inicio de la quest
################################################################################

label quest_mc_quest_0:

    # Asegurar ubicación correcta
    $ sistema_locaciones.mover_a_locacion("casa_living")

    # Rutinas: las tres chicas en sus habitaciones durante toda la quest
    $ mc_q0_activar_rutinas_npc()

    # Estado
    $ mc_q0_fase = 1
    $ mc_q0_interceptar_movimiento = True
    $ mc_q0_hotspots_visitados = {}
    $ mc_q0_primer_click = {}
    $ mc_q0_locaciones_exploradas = set()
    $ mc_q0_entrada_mostrada = set()

    # Activar la visualización de hotspots (la config tambien)
    $ config_mostrar_accion_movimiento = True
    $ visualizador_hotspot_activo = True

    # Restricción fase 1 — todo bloqueado excepto la accion del visualizador
    $ activar_restriccion(
        locaciones_permitidas=[],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar",
            "trabajar", "comprar", "ver_tv", "usar_item",
        ],
        mensaje_movimiento="Primero vamos a ver las locaciones conectadas con el living",
        celular_bloqueado=True,
        mensaje_celular="No es momento de hacer esto",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Actualizar la quest MC en el panel de pistas
    $ sistema_quests_mc.iniciar("mc_quest_0")

    # Piensa iniciales
    $ ocultar_hud()
    window show

    piensa "Que nostalgia, han pasado años desde la última vez que estuve en esta casa "
    piensa "Podría recorrer un poco la casa antes de guardar las cosas"
    piensa "Me gustaría ver que tanto cambio"

    tutorial "Aprendamos como movernos. Todos los puntos de movimiento están remarcados en la pantalla, al hacer click en uno nos llevara a la locacion conectada"
    tutorial "A medida que durante el juego te muevas por la casa, la iras conociendo mejor y moverte sea algo simple"
    tutorial "Ahora vamos a centrarnos en 4 locaciones que son las que conectan a la mayoría.{w} El [colorear_locacion('Living')], el [colorear_locacion('Patio')], el [colorear_locacion('Pasillo de abajo')] y el [colorear_locacion('Pasillo de arriba')]"


    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## Handler de clics MOVE durante la quest
################################################################################

label mc_q0_handler_move:
    $ _dest_id  = _hotspot_temp.destino
    $ _loc_id   = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else ""
    $ _dest_nom = MC_Q0_NOMBRES_DESTINO.get(_dest_id, _dest_id)

    # ── Desde Living en fase 2: redirigir a locaciones pendientes ───────────
    if mc_q0_fase == 2 and _loc_id == "casa_living":
        $ _faltantes_f2 = mc_q0_str_faltantes_fase2()
        if _faltantes_f2:
            piensa "Ir a: [_faltantes_f2]"
        return

    # ── Desde zona incompleta intentando salir al living ────────────────────
    if (mc_q0_fase == 2 and _loc_id in MC_Q0_LOCS_FASE2
            and _loc_id not in mc_q0_locaciones_exploradas
            and _dest_id == "casa_living"):
        $ _faltantes_hs = mc_q0_str_faltantes_hotspots(_loc_id)
        if _faltantes_hs:
            piensa "Todavía me falta explorar: [_faltantes_hs]"
        else:
            piensa "Tengo que ver todo antes de salir"
        return

    # ── Comprobar si este hotspot ya fue visitado ANTES de registrar ────────
    $ _ya_visitado = _hotspot_temp.id in mc_q0_hotspots_visitados.get(_loc_id, set())

    # ── Registrar visita ────────────────────────────────────────────────────
    $ mc_q0_registrar_visita(_loc_id, _hotspot_temp.id)

    # ── Verificar completitud ANTES del piensa — avance automático sin click extra ──
    if mc_q0_fase == 1:
        if mc_q0_locacion_completa("casa_living"):
            jump mc_q0_living_completado

    elif mc_q0_fase == 2 and _loc_id in MC_Q0_LOCS_FASE2:
        if mc_q0_locacion_completa(_loc_id) and _loc_id not in mc_q0_locaciones_exploradas:
            $ mc_q0_locaciones_exploradas = mc_q0_locaciones_exploradas | {_loc_id}
            if MC_Q0_LOCS_FASE2.issubset(mc_q0_locaciones_exploradas):
                jump mc_q0_exploracion_completada

    # ── Locación completada: redirigir a locaciones fase 2 pendientes ──────
    if mc_q0_fase == 2 and _loc_id in MC_Q0_LOCS_FASE2 and _loc_id in mc_q0_locaciones_exploradas:
        $ _faltantes_f2 = mc_q0_str_faltantes_fase2()
        if _faltantes_f2:
            piensa "Ir a: [_faltantes_f2]"
        return

    # ── Mensaje: mostrar faltantes solo si el hotspot YA fue visitado ──────
    if _ya_visitado:
        $ _faltantes_hs = mc_q0_str_faltantes_hotspots(_loc_id)
        if _faltantes_hs:
            piensa "Esto lleva a [_dest_nom]. Todavía me falta explorar: [_faltantes_hs]"
        else:
            piensa "Esto lleva a [_dest_nom]"
    else:
        piensa "Esto lleva a [_dest_nom]"

    return


################################################################################
## Living completado → inicio fase 2
################################################################################

label mc_q0_living_completado:

    $ ocultar_hud()
    window show

    tutorial "Estas son las locaciones conectadas con el [colorear_locacion('Living')]"
    tutorial "Ahora sigamos con el resto... el [colorear_locacion('Patio')], el [colorear_locacion('Pasillo de abajo')] y el [colorear_locacion('Pasillo de arriba')]"
    tutorial "Vamos a recorrerlos uno por uno"

    window hide
    $ mostrar_hud()

    $ mc_q0_fase = 2

    $ activar_restriccion(
        locaciones_permitidas=[
            "casa_living", "casa_pasilloabajo",
            "casa_pasilloarriba", "casa_patio",
        ],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar",
            "trabajar", "comprar", "ver_tv", "usar_item",
        ],
        mensaje_movimiento="Todavía tengo que ver el resto de la casa",
        celular_bloqueado=True,
        mensaje_celular="Mejor termino de recorrer la casa antes",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_pasilloabajo",  "mc_q0_entrada_pasilloabajo")
    $ restriccion_quest_activa.registrar_label_locacion("casa_pasilloarriba", "mc_q0_entrada_pasilloarriba")
    $ restriccion_quest_activa.registrar_label_locacion("casa_patio",         "mc_q0_entrada_patio")

    jump game_loop


################################################################################
## Entrada a cada locación de exploración (fase 2)
## Se disparan via labels_por_locacion al entrar — terminan en return
################################################################################

label mc_q0_entrada_pasilloabajo:
    if "casa_pasilloabajo" not in mc_q0_entrada_mostrada:
        $ mc_q0_entrada_mostrada = mc_q0_entrada_mostrada | {"casa_pasilloabajo"}
        $ actualizar_bg_master()
        $ ocultar_hud()
        window show
        tutorial "El [colorear_locacion('Pasillo abajo')]. Esto conecta con: el [colorear_locacion('Living')], la [colorear_locacion('Cocina')], el [colorear_locacion('Baño de abajo')] y la [colorear_locacion('Habitación de Monica')]"
        tutorial "Veamos a cual es cada una de ellas"
        window hide
        $ mostrar_hud()
    return


label mc_q0_entrada_pasilloarriba:
    if "casa_pasilloarriba" not in mc_q0_entrada_mostrada:
        $ mc_q0_entrada_mostrada = mc_q0_entrada_mostrada | {"casa_pasilloarriba"}
        $ actualizar_bg_master()
        $ ocultar_hud()
        window show
        tutorial "El [colorear_locacion('Pasillo de arriba')]. Esto conecta con: el [colorear_locacion('Living')], [colorear_locacion('Mi Habitación')], la [colorear_locacion('Habitación de Jasmine')], la [colorear_locacion('Habitación de Violet')], el [colorear_locacion('Baño de arriba')] y el [colorear_locacion('Altillo')]"
        tutorial "Veamos cual es cada una de ellas"
        window hide
        $ mostrar_hud()
    return


label mc_q0_entrada_patio:
    if "casa_patio" not in mc_q0_entrada_mostrada:
        $ mc_q0_entrada_mostrada = mc_q0_entrada_mostrada | {"casa_patio"}
        $ actualizar_bg_master()
        $ ocultar_hud()
        window show
        tutorial "El [colorear_locacion('Patio')]. Esto esta conectado con: el [colorear_locacion('Living')], el [colorear_locacion('Gym')], el [colorear_locacion('Frente')] y el [colorear_locacion('Comedor')]"
        tutorial "Veamos cual es cada una de ellas"
        window hide
        $ mostrar_hud()
    return


################################################################################
## Exploración completada → siguiente etapa de la quest
################################################################################

label mc_q0_exploracion_completada:

    $ ocultar_hud()
    window show

    tutorial "Esas son las [colorear_locacion('habitaciones')] con más conexiones dentro de la casa"
    tutorial "Durante el juego te podras mover libremente y explorar cada lugar, el movimiento no tiene ningún costo así que sientete libre de hacerlo"
    tutorial "Siempre que quieras puedes [colorear_quest('activar')] y [colorear_quest('desactivar')] la ayuda de movimiento con el [colorear_quest('boton del ojo')] que tendras en la [colorear_quest('barra de acciones')] de la locacion"
    tutorial "Una vez que estes familiarizado con el movimiento, dentro del [colorear_quest('celular')] en las [colorear_quest('opciones')] podras directamente [colorear_quest('desactivarla')] si así lo prefieres"

    window hide
    $ mostrar_hud()

    # Fin del interceptor de movimiento — la fase mudanza no lo usa
    $ mc_q0_interceptar_movimiento = False
    $ mc_q0_fase = 0

    jump mc_q0_mudanza


################################################################################
## Fase Mudanza — buscar cajas en garage y llevarlas a la habitacion
################################################################################

label mc_q0_mudanza:

    # Cambiar el bg de la habitacion del MC al especial de intro
    python:
        _loc_hmc = sistema_locaciones.locaciones.get("casa_hmc")
        if _loc_hmc:
            _loc_hmc.background_base = "images/quest/mc/quest0/bg_casa_intro_hmc.png"

    # Activar cajas y accion de mudanza en el garage
    $ mc_q0_cajas_en_garage = True
    $ mc_q0_mudanza_garage_activa = True
    $ mc_q0_mudanza_hmc_activa = True

    # Restricción: solo puede ir a hmc, pasillo arriba, living, garage
    $ activar_restriccion(
        locaciones_permitidas=[
            "casa_hmc", "casa_pasilloarriba",
            "casa_living", "casa_garage",
        ],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Monica dijo que las cosas están en el garage",
        mensaje_accion_default="Debo ocuparme de las cosas de la mudanza",
        celular_bloqueado=True,
        mensaje_celular="Debo ocuparme de las cosas de la mudanza",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_garage", "mc_q0_entrada_garage")

    $ ocultar_hud()
    window show

    piensa "Bueno... Monica dijo que mis cosas están en el [colorear_locacion('Garage')]"
    piensa "Voy a buscarlas y subirlas a [colorear_locacion('Mi Habitación')]"

    window hide
    $ mostrar_hud()
    jump game_loop


label mc_q0_entrada_garage:
    if not mc_q0_entrada_garage_mostrada:
        $ mc_q0_entrada_garage_mostrada = True
        $ actualizar_bg_master()
        # Mostrar cajas junto al bg (el HUD que las renderiza se oculta a continuación)
        $ _cajas_pos = sistema_pos.obtener("mc_q0_cajas_intro")
        $ _cajas_x = _cajas_pos.x if _cajas_pos else 629
        $ _cajas_y = _cajas_pos.y if _cajas_pos else 422
        show expression "images/quest/mc/quest0/idle_cajas_intro.png" as cajas_temp:
            xpos _cajas_x ypos _cajas_y xanchor 0.0 yanchor 0.0
        $ ocultar_hud()
        window show
        piensa "Ahí están mis cosas. Tengo que llevarlo todo a mi habitación"

        tutorial "Al entrar a una locacion tendremos un [colorear_quest('menu flotante')] con las [colorear_quest('acciones')] que podremos hacer en la misma"
        tutorial "Algunas [colorear_quest('acciones')] estaran siempre disponibles al entrar a una locacion"
        tutorial "Mientras que otras solo estaran disponibles durante una parte de una [colorear_quest('quest')] o un [colorear_quest('evento')]"
        tutorial "Ahora vamos a usar la acción de [colorear_quest('acción mudanza')] para recoger las cajas"
        window hide
        hide cajas_temp
        $ mostrar_hud()
    return


################################################################################
## Accion Mudanza — Garage
################################################################################

label mudanza_garage_generico:
    $ ocultar_hud()
    window show

    piensa "Voy a agarrar todo esto y subirlo"

    window hide
    $ mostrar_hud()

    # Quitar el idle de cajas
    $ mc_q0_cajas_en_garage = False
    # Desactivar la accion del garage
    $ mc_q0_mudanza_garage_activa = False
    # Dar el item al inventario
    $ agregar_al_inventario("mis_cosas")

    # Cambiar el mensaje de bloqueo de movimiento
    $ restriccion_quest_activa.mensaje_movimiento = "Debo llevar todas las cajas a mi habitación"

    $ ocultar_hud()
    window show

    piensa "Son bastantes cosas"
    piensa "Es momento de llevar todo a [colorear_locacion('Mi Habitación')]"

    window hide
    $ mostrar_hud()
    return


################################################################################
## Accion Mudanza — Habitacion del MC
################################################################################

label mudanza_hmc_generico:
    if "mis_cosas" not in inventario or inventario.get("mis_cosas", 0) <= 0:
        piensa "Primero tengo que buscar mis cosas en el garage"
        return

    $ ocultar_hud()
    window show

    piensa "Momento de empeza a acomodar todo"

    window hide
    $ mostrar_hud()

    $ quitar_del_inventario("mis_cosas")
    $ mc_q0_mudanza_hmc_activa = False

    jump mc_q0_mudanza_completada


################################################################################
## Mudanza completada — pantalla negra + Stage A (esperar horario)
################################################################################

label mc_q0_mudanza_completada:

    $ ocultar_hud()

    # Restaurar bg normal de la habitacion antes de avanzar horario
    python:
        _loc_hmc = sistema_locaciones.locaciones.get("casa_hmc")
        if _loc_hmc:
            _loc_hmc.background_base = "images/bg/casa/bg_casa_{horario}_hmc.png"

    # Pantalla negra con texto
    scene black with fade
    show text "Algunas horas después..." at truecenter with dissolve
    pause 2.5
    hide text with dissolve

    # Avanzar horario (actualiza el bg de la hmc al nuevo horario con fade)
    $ avanzar_horario()

    window show

    piensa "Listo. Ya esta todo acomodado"
    piensa "Monica dijo que ibamos a salir por la [colorear_quest('noche')], todavía falta algo de tiempo"
    piensa "Podría relajarme un momento"

    tutorial "Hacer algunas acciones o quest avanzaran el tiempo automaticamente"
    tutorial "También puedes avanzarlo de forma manual haciendo [colorear_quest('haciendo click en el indicador de horario')] que se encuentra al centro de la parte superior"
    tutorial "Prueba avanzar el tiempo hasta la noche"

    window hide

    # Restricción Stage A: solo se puede avanzar el tiempo, sin salir de la habitacion
    $ activar_restriccion(
        locaciones_permitidas=["casa_hmc"],
        acciones_bloqueadas=[
            "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Tengo que hacer tiempo hasta la noche",
        mensaje_accion_default="Tengo que hacer tiempo hasta la noche",
        celular_bloqueado=True,
        mensaje_celular="Tengo que hacer tiempo hasta la noche",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    $ mc_q0_esperar_horario = True
    $ mostrar_hud()
    jump game_loop


################################################################################
## Stage B — ir al frente
################################################################################

label mc_q0_stage_b:

    $ ocultar_hud()
    window show

    piensa "Ese descanso me vino bien"
    piensa "Las chicas ya deben estar listas para salir"
    piensa "Voy al [colorear_locacion('Frente')] de la casa para encontrarlas"

    window hide

    # Restricción Stage B: solo puede moverse a pasillo arriba, living y frente
    $ activar_restriccion(
        locaciones_permitidas=[
            "casa_pasilloarriba", "casa_living", "casa_frente",
        ],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Debo ir al frente",
        mensaje_accion_default="No puedo, las chicas me están esperando",
        celular_bloqueado=True,
        mensaje_celular="No puedo, las chicas me están esperando",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_frente", "mc_q0_entrada_frente")

    $ mostrar_hud()
    jump game_loop


label mc_q0_entrada_frente:
    $ desactivar_restriccion()
    $ mc_q0_limpiar_rutinas_npc()
    jump mc_q0_siguiente_etapa


################################################################################
## Inicio directo (Omitir intro) — arranca en martes mañana con quest 0 completa
################################################################################

label mc_q0_inicio_directo:
    # Lunes por la noche en la habitacion del MC
    $ dia_semana_actual = 0   # Lunes
    $ horario_actual = 3      # Trasnoche
    $ dia_actual = 1
    $ dias_totales = 1
    $ actualizar_rutinas_npcs()
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ actualizar_bg_master()

    # Visualizador de hotspots apagado (nunca se activó en este path)
    $ config_mostrar_accion_movimiento = False
    $ visualizador_hotspot_activo = False

    # Activar el hook de cleanup que dispara al dormir
    $ mc_q0_final_sleep = True

    $ ocultar_hud()
    window show
    piensa "Hice muchas cosas el día de hoy y estoy completamente agotado"
    piensa "Mejor duermo, mañana sera un día nuevo para ponerme al día con las chicas"
    window hide
    $ mostrar_hud()

    # Ejecutar dormir automáticamente — avanza al martes mañana
    # El hook mc_q0_final_sleep completa la quest y apaga la config
    call accion_dormir from _call_mc_q0_inicio_directo_dormir

    jump game_loop


################################################################################
## Escena final de la intro — contemplación + primer sueño
################################################################################

label mc_q0_siguiente_etapa:

    $ ocultar_hud()
    window show

    scene escena_final_quest0_mc with fade

    piensa "Estoy agotado, no se si fue por la mudanza, por el viaje, por mi padre..."
    piensa "Quizás sea un poco de todo"
    piensa "Pero este momento me hace sentir que estoy en el lugar correcto y con las personas correctas"
    piensa "Es el momento de disfrutar"

    # Llevar al jugador a su habitacion en la trasnoche
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ horario_actual = 3
    $ actualizar_bg_master()

    piensa "No quería que el día termine, tenía tantas cosas por hablar con ellas"
    piensa "Pero tengo muchos días por delante para hacerlo, estando aquí el tiempo ya no es un problema"
    piensa "Ahora a dormir"
    tutorial "Para pasar al día siguiente haz [colorear_quest('click sobre la cama')]"

    window hide
    $ mostrar_hud()

    # Restricción: solo se puede dormir
    $ activar_restriccion(
        locaciones_permitidas=None,
        acciones_bloqueadas=[
            "avanzar_tiempo", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_accion_default="Es tarde, debo dormir",
        celular_bloqueado=True,
        mensaje_celular="Es tarde, debo dormir",
    )

    $ mc_q0_final_sleep = True
    jump game_loop
