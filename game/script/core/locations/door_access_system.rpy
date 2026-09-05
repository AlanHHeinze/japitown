################################################################################
## Sistema de Control de Acceso a Habitaciones NPC
################################################################################
## Controla el acceso a habitaciones de NPCs basado en presencia
## Muestra menu de interaccion en la puerta con opciones especiales

# Mapeo de habitaciones a NPCs
define HABITACION_NPC = {
    "casa_hmonica": "monica",
    "casa_hviolet": "violet",
    "casa_hjasmine": "jasmine"
}

# Mapeo de NPC al pasillo correspondiente
define PASILLO_NPC = {
    "monica": "casa_pasilloabajo",
    "violet": "casa_pasilloarriba",
    "jasmine": "casa_pasilloarriba"
}

# Mensaje cuando NPC no esta
define MENSAJES_AUSENTE = {
    "violet": "Violet no está en su habitación.",
    "jasmine": "Jasmine no está en su habitación.",
    "monica": "Mónica no está en su habitación."
}

init python:

    # ==========================================================================
    # Registro declarativo de contenido de puerta (refactor C8).
    #
    # El contenido (quests/eventos) se registra en init 5 desde los archivos del
    # personaje (ej. characters/violet/interaction/puertas_violet.rpy). El motor
    # solo itera los registros: NO conoce ninguna quest por nombre. Las
    # condiciones son funciones de MODULO (regla anti-pickle del proyecto).
    #
    # Tres registros, segun el momento de la puerta que interceptan:
    # - OPCIONES_PUERTA_REGISTRO: botones del menu de puerta (con condicion).
    # - OVERRIDES_PUERTA_REGISTRO: reemplazan TODO el flujo de puerta con un
    #   label propio (ej. la gestion de enfermedad de la 09_a).
    # - BLOQUEOS_GOLPE_REGISTRO: al elegir "Golpear", muestran un pensamiento y
    #   cortan (ej. "Violet debe estar dormida." los sabados a la mañana).
    #   El mensaje se traduce con renpy.translate_string: el `old` vive en
    #   tl/english/script/core/locations/door_access_system.rpy.
    # ==========================================================================

    OPCIONES_PUERTA_REGISTRO = {}   # {npc_id: [dict opcion]}
    OVERRIDES_PUERTA_REGISTRO = {}  # {npc_id: [(condicion, label)]}
    BLOQUEOS_GOLPE_REGISTRO = {}    # {npc_id: [(condicion, mensaje)]}

    def registrar_opcion_puerta(npc_id, texto, label, condicion,
                                ocultar_golpear=False, tipo=None,
                                quest_id=None):
        """
        Registra un boton del menu de puerta de un NPC. El orden de registro es
        el orden en el menu. `condicion` es una funcion de modulo sin argumentos
        que decide si el boton aparece (None = siempre).

        `quest_id`: a que quest pertenece el boton, para el tag " (⭐ Quest)".
        Solo hace falta cuando el label es PROPIO: si se llama `quest_<id>`,
        tag_opcion_quest lo deduce solo. Sin ninguna de las dos cosas el boton
        sale con un " (Quest)" pelado, sin el icono de la linea.
        """
        OPCIONES_PUERTA_REGISTRO.setdefault(npc_id, []).append({
            "texto": texto,
            "label": label,
            "condicion": condicion,
            "ocultar_golpear": ocultar_golpear,
            "tipo": tipo,
            "quest_id": quest_id,
        })

    # ==========================================================================
    # Menu EXCLUSIVO — "durante esta escena, solo esta opcion"
    # ==========================================================================
    # Hay momentos en que el menu de un NPC tiene que quedar reducido a UNA
    # opcion: la escena en curso es lo unico que corresponde, y ofrecerle al
    # jugador devolverle unos mangas en el medio del corte de luz rompe el tono.
    #
    # Va como REGISTRO y no como un `if`: el motor no conoce ninguna quest por
    # nombre (regla 1). El contenido lo declara en su init 5.
    #
    #     registrar_menu_exclusivo("violet", _va25_boton_matar_tiempo,
    #                              "violet_amor_25_matar_tiempo")
    #     registrar_menu_exclusivo("violet", _va25_puerta_exclusiva,
    #                              "violet_amor_25_puerta_entrar", ambito="puerta")
    #
    # DOS AMBITOS porque son dos menus distintos con labels distintos:
    #
    #     "menu"    el menu del sprite. Ademas de filtrar, esconde "Hablar".
    #     "puerta"  el menu de la puerta. "Golpear" y "Volver" se quedan: sin
    #               ellos el jugador no tendria como salir ni como que le
    #               conteste el bloqueo de golpe que corresponda.
    #
    # VIVE ACA Y NO EN ui/menus/ para que la dependencia vaya en la direccion
    # correcta: lo define el core y lo consultan los dos menus.
    #
    # Si la condicion revienta se ignora: es preferible un menu de mas que un
    # menu que no se puede abrir. Gana el PRIMERO que cumple.

    # [(npc_id, ambito, condicion, label)]
    MENU_EXCLUSIVO_REGISTRO = []

    def registrar_menu_exclusivo(npc_id, condicion, label, ambito="menu"):
        """Declara que, con `condicion`, ese menu de `npc_id` es solo `label`."""
        MENU_EXCLUSIVO_REGISTRO.append((npc_id, ambito, condicion, label))

    def menu_exclusivo_label(npc_id, ambito="menu"):
        """Label al que queda reducido el menu, o None si no aplica."""
        for _nid, _amb, _cond, _label in MENU_EXCLUSIVO_REGISTRO:
            if _nid != npc_id or _amb != ambito:
                continue
            try:
                if _cond():
                    return _label
            except Exception:
                continue
        return None

    def registrar_override_puerta(npc_id, condicion, label):
        """
        Registra un label que reemplaza el flujo completo de la puerta cuando
        su condicion da True (se chequea antes del menu; el primero que matchea
        gana). El label recibe el control con jump.
        """
        OVERRIDES_PUERTA_REGISTRO.setdefault(npc_id, []).append((condicion, label))

    def registrar_bloqueo_golpe(npc_id, condicion, mensaje):
        """
        Registra un bloqueo de la accion "Golpear la puerta": si la condicion da
        True, se muestra `mensaje` como pensamiento y no pasa nada mas.
        """
        BLOQUEOS_GOLPE_REGISTRO.setdefault(npc_id, []).append((condicion, mensaje))

    def obtener_override_puerta(npc_id):
        """Primer override cuya condicion da True, o None."""
        for _condicion, _label in OVERRIDES_PUERTA_REGISTRO.get(npc_id, []):
            if _condicion():
                return _label
        return None

    def obtener_bloqueo_golpe(npc_id):
        """Mensaje (ya traducido) del primer bloqueo de golpe activo, o None."""
        for _condicion, _mensaje in BLOQUEOS_GOLPE_REGISTRO.get(npc_id, []):
            if _condicion():
                return renpy.translate_string(_mensaje)
        return None

    def obtener_npc_habitacion(destino_id):
        """
        Obtiene el ID del NPC dueño de una habitacion.
        """
        return HABITACION_NPC.get(destino_id, None)

    def retornar_npcs_pasillo_al_salir(locacion_salida_id):
        """
        Llamada al salir de un pasillo: si algun NPC está ahi por door access
        (no por rutina), lo devuelve automáticamente a su habitacion.
        """
        if locacion_salida_id not in ("casa_pasilloarriba", "casa_pasilloabajo"):
            return
        for npc_id, pasillo_id in PASILLO_NPC.items():
            if pasillo_id != locacion_salida_id:
                continue
            npc_obj = obtener_npc(npc_id)
            if not npc_obj or npc_obj.locacion_actual != locacion_salida_id:
                continue
            loc_rutina = npc_obj.obtener_locacion_rutina()
            if loc_rutina and loc_rutina != locacion_salida_id:
                npc_obj.locacion_actual = loc_rutina

    def obtener_bg_pasillo_npc(npc_id):
        """
        Obtiene el background del pasillo correspondiente al NPC
        con el horario actual.
        """
        pasillo_id = PASILLO_NPC.get(npc_id)
        if pasillo_id and hasattr(store, 'sistema_locaciones'):
            loc = store.sistema_locaciones.obtener_locacion(pasillo_id)
            if loc:
                return loc.background
        return None

    def obtener_opciones_puerta(npc_id):
        """
        Construye las opciones especiales del menu de puerta para un NPC
        iterando el registro declarativo (el orden de registro es el orden
        del menu). El contenido se registra con registrar_opcion_puerta()
        desde los archivos del personaje.

        ⚠️ ESTA FUNCION REARMA EL DICT, no pasa el del registro. Todo campo que
        la screen necesite tiene que copiarse acá explicitamente: si se agrega
        uno nuevo a registrar_opcion_puerta() y no se lo suma a esta lista, se
        pierde en el camino sin ningun error — la opcion aparece igual, solo que
        sin ese dato. Paso con `quest_id`, que quedaba descartado y dejaba a
        todos los botones de puerta con un " (Quest)" sin el icono de la linea.

        Returns:
            list: Lista de dicts {"texto": str, "label": str, "ocultar_golpear": bool}
            (mas "tipo" y "quest_id" si la opcion los declaro)
        """
        # Menu exclusivo: si hay una escena que se lleva la puerta entera, queda
        # su opcion y nada mas. "Golpear" y "Volver" no salen de acá, asi que
        # siguen estando.
        _excl = menu_exclusivo_label(npc_id, "puerta")

        opciones = []
        for _reg in OPCIONES_PUERTA_REGISTRO.get(npc_id, []):
            if _excl and _reg["label"] != _excl:
                continue
            if _reg["condicion"] is not None and not _reg["condicion"]():
                continue
            _op = {
                "texto": _reg["texto"],
                "label": _reg["label"],
                "ocultar_golpear": _reg["ocultar_golpear"],
            }
            if _reg["tipo"]:
                _op["tipo"] = _reg["tipo"]
            if _reg.get("quest_id"):
                _op["quest_id"] = _reg["quest_id"]
            opciones.append(_op)
        return opciones

    def obtener_trigger_habitacion_directo(npc_id):
        """
        Label de quest a disparar cuando el jugador ENTRA DIRECTO a la habitacion
        (por tener relacion suficiente: ingreso_diurno / ingreso_noche), sin pasar
        por el menu de puerta.

        Antes, esos triggers vivían solo como opciones del menu de puerta; si el
        jugador entraba directo, la quest que pedía "ir a la habitacion" (ej: 06_b
        La prueba del cosplay) no se disparaba nunca. Reusa obtener_opciones_puerta
        para respetar EXACTAMENTE las mismas condiciones (etapa, horario, ítems).

        Devuelve el label de la primera opcion de quest disponible, o None. Se
        ignoran las opciones de tipo "evento" (esas no son triggers de quest a
        habitacion; se manejan por su cuenta).
        """
        for op in obtener_opciones_puerta(npc_id):
            if op.get("tipo") == "evento":
                continue
            lbl = op.get("label")
            if lbl:
                return lbl
        return None

    def obtener_npc_en_banio(banio_id):
        """Retorna el NPC que está actualmente en el baño indicado, o None."""
        if not hasattr(store, 'sistema_npcs'):
            return None
        for npc in store.sistema_npcs.npcs.values():
            if npc.locacion_actual == banio_id:
                return npc
        return None



################################################################################
## Screen del Menu de Puerta
################################################################################

screen menu_puerta_npc(npc_id, opciones_especiales, bg_path=None):
    # bg_path: None = usar pasillo del NPC (por defecto)
    #          False = no mostrar background (usar el que ya está en escena)

    modal True

    # Fondo
    $ _bg_puerta_final = bg_path if bg_path is not None else obtener_bg_pasillo_npc(npc_id)
    if _bg_puerta_final:
        add _bg_puerta_final

    # Overlay semi-transparente
    add Solid("#00000088")

    # ¿Alguna opción especial pide ocultar el botón de golpear?
    # (quests cuya interacción reemplaza al golpe normal de puerta)
    $ _ocultar_golpear = any(o.get("ocultar_golpear", False) for o in opciones_especiales)

    # Menu de opciones - Mismo layout que screen choice
    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        # Golpear la puerta — siempre primero, salvo que una quest lo oculte
        if not _ocultar_golpear:
            textbutton "Golpear la puerta":
                style "choice_button"
                action [Hide("menu_puerta_npc"),
                        Return("golpear")]

        # Opciones especiales de quest/evento
        for opcion in opciones_especiales:
            $ _tag_opcion = tag_opcion_quest(opcion.get("label"), opcion.get("tipo") == "evento", opcion.get("tipo"), opcion.get("quest_id"))
            textbutton (renpy.translate_string(opcion.get("texto", "Opcion")) + _tag_opcion):
                style "choice_button"
                action [Hide("menu_puerta_npc"),
                        Return(("opcion_especial", opcion.get("label", "game_loop")))]

        # Volver — siempre al final
        textbutton "Volver":
            style "choice_button"
            action [Hide("menu_puerta_npc"),
                    Return("volver")]


################################################################################
## Screen del Menu de Baño
################################################################################

screen menu_banio_npc(npc_id, bg_path=None):
    modal True

    if bg_path:
        add bg_path

    add Solid("#00000088")

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Golpear la puerta":
            style "choice_button"
            action [Hide("menu_banio_npc"), Return("golpear")]

        # Mirar y Entrar aparecen JUNTAS y solo si el NPC dejo la puerta
        # entreabierta. Eso lo decide su ventaja de Provocación, no este screen
        # — acá solo se pregunta (npc_puerta_banio_abierta, core/espiar).
        #
        # Con la puerta cerrada NO se muestran en gris: el jugador no tiene que
        # enterarse de que a veces esta abierta (la sorpresa es la gracia de la
        # provocacion), y "Entrar" en gris con la puerta cerrada seria doblemente
        # confuso — no se puede entrar porque esta cerrada, no porque falte
        # contenido.
        #
        # "Entrar" queda en gris igual: la escena de adentro todavia no existe.
        # Se deja a la vista para que se entienda que es el paso que sigue.
        if ESPIAR_HABILITADO and npc_tiene_espiar(npc_id) and npc_puerta_banio_abierta(npc_id):
            textbutton "Mirar":
                style "choice_button"
                action [Hide("menu_banio_npc"), Return("espiar")]

            textbutton "Entrar (Contenido en desarrollo)":
                style "choice_button"
                sensitive False
                action NullAction()

        textbutton "Volver":
            style "choice_button"
            action [Hide("menu_banio_npc"), Return("volver")]


################################################################################
## Labels del Sistema de Acceso
################################################################################

# Label completo de interaccion con puerta (se usa con jump, no call)
# _destino_puerta debe estar seteado antes de saltar aqui
label interaccion_puerta_npc:
    # Obtener NPC de la habitacion destino
    $ _npc_habitacion = obtener_npc_habitacion(_destino_puerta)

    if not _npc_habitacion:
        # No es habitacion de NPC, mover directamente
        $ sistema_locaciones.mover_a_locacion(_destino_puerta)
        return

    $ _npc_obj = obtener_npc(_npc_habitacion)
    $ _habitacion_id = "casa_h" + _npc_habitacion
    $ _npc_presente = _npc_obj and _npc_obj.esta_en_locacion(_habitacion_id)

    # Overrides registrados por contenido: reemplazan TODO el flujo de puerta
    # (ej. la gestion de enfermedad de la quest 09_a de Violet). El primero
    # cuya condicion da True gana.
    $ _override_puerta = obtener_override_puerta(_npc_habitacion)
    if _override_puerta:
        jump expression _override_puerta

    # Trasnoche: ingreso_noche requiere que el NPC esté presente
    if store.horario_actual == 3:
        $ _nivel_trasnoche = verificar_nivel_acceso_habitacion(_npc_habitacion)
        if _nivel_trasnoche == "ingreso_noche" and _npc_presente:
            # Si hay una quest esperando "ir a la habitacion", dispararla también
            # cuando se entra directo (antes solo se disparaba desde el menú de
            # puerta, así que con relación alta quedaba sin trigger).
            $ _trigger_dir = obtener_trigger_habitacion_directo(_npc_habitacion)
            if _trigger_dir:
                jump expression _trigger_dir
            $ sistema_locaciones.mover_a_locacion(_destino_puerta)
            $ mostrar_hud()
            return
        else:
            $ _blk_guardar_toque()
            piensa "Debe estar durmiendo, no voy a molestar."
            return

    # Verificar nivel de acceso diurno
    $ _nivel_acceso = verificar_nivel_acceso_habitacion(_npc_habitacion)

    # Ingreso diurno: acceso libre — entra sin importar si el NPC está presente
    if _nivel_acceso == "ingreso_diurno":
        # Igual que en trasnoche: si hay una quest esperando "ir a la habitacion",
        # dispararla al entrar directo (este era el caso de 06_b La prueba del
        # cosplay — con amor >= 50 entraba directo y no se disparaba nunca).
        # Se exige _npc_presente: el menú de puerta solo ofrece estos triggers
        # cuando el NPC está en la habitación, y las escenas asumen que está.
        # Si no está, se entra normal a la habitación vacía.
        $ _trigger_dir = obtener_trigger_habitacion_directo(_npc_habitacion) if _npc_presente else None
        if _trigger_dir:
            jump expression _trigger_dir
        $ sistema_locaciones.mover_a_locacion(_destino_puerta)
        $ mostrar_hud()
        return

    # Para todos los niveles inferiores el NPC debe estar en su habitacion
    if not _npc_presente:
        $ _loc_npc_actual = _npc_obj.locacion_actual if _npc_obj else None

        if _loc_npc_actual == "fuera":
            # Salió de la casa — mensaje directo
            $ _npc_nombre_door = _npc_obj.nombre if _npc_obj else ""
            $ _blk_guardar_toque()
            piensa "Parece que [_npc_nombre_door] no está en casa, debe haber salido."
            return

        else:
            # Ausente por rutina normal, quest, u otra razon
            $ _msg_ausente = renpy.translate_string(MENSAJES_AUSENTE.get(_npc_habitacion, "No hay nadie."))
            $ _msg_ausente = renpy.translate_string(_msg_ausente)
            $ _blk_guardar_toque()
            piensa "[_msg_ausente]"
            return

    # NPC presente — ocultar HUD y preparar interaccion
    $ ocultar_hud()
    hide screen hud_navegacion
    window hide

    # Mostrar background del pasillo correspondiente
    $ _bg_pasillo = obtener_bg_pasillo_npc(_npc_habitacion)
    scene expression _bg_pasillo with fade

    # Obtener opciones especiales y mostrar menu
    $ _opciones_puerta_list = obtener_opciones_puerta(_npc_habitacion)
    call screen menu_puerta_npc(_npc_habitacion, _opciones_puerta_list)

    # Procesar resultado del menu
    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        # Opcion especial: ejecutar el label correspondiente limpiando el HUD
        $ _label_opcion = _return[1]
        $ mostrar_hud()
        jump expression _label_opcion

    if _return == "golpear":
        # Sonido de tocar puerta
        play sound "audio/sfx/door_knock_3.ogg"
        pause 0.5

        # Bloqueos de golpe registrados por contenido (ej. Violet dormida los
        # sabados a la mañana). El mensaje ya viene traducido.
        $ _msg_bloqueo_golpe = obtener_bloqueo_golpe(_npc_habitacion)
        if _msg_bloqueo_golpe:
            $ _blk_guardar_toque()
            piensa "[_msg_bloqueo_golpe]"
            $ mostrar_hud()
            return

        # Dispatch por nivel de acceso
        if _nivel_acceso == "dejar_pasar":
            jump interaccion_golpear_dejar_pasar
        elif _nivel_acceso == "sale_pasillo":
            jump interaccion_golpear_sale_pasillo
        else:
            # Sin nivel suficiente — NPC dice que está ocupada
            $ _msg_ocupada = mensaje_puerta_npc(_npc_habitacion, "ocupada")
            if _npc_habitacion == "violet":
                violet "[_msg_ocupada]"
            elif _npc_habitacion == "jasmine":
                jasmine "[_msg_ocupada]"
            elif _npc_habitacion == "monica":
                monica "[_msg_ocupada]"
            $ mostrar_hud()
            return

    # "volver"
    $ mostrar_hud()
    return


label interaccion_golpear_dejar_pasar:
    # NPC dice "Adelante" y el jugador entra directamente
    $ _msg_adelante = mensaje_puerta_npc(_npc_habitacion, "adelante")
    if _npc_habitacion == "violet":
        violet "[_msg_adelante]"
    elif _npc_habitacion == "jasmine":
        jasmine "[_msg_adelante]"
    elif _npc_habitacion == "monica":
        monica "[_msg_adelante]"
    $ sistema_locaciones.mover_a_locacion(_destino_puerta)
    $ mostrar_hud()
    return


label interaccion_golpear_sale_pasillo:
    # NPC dice "Ahi salgo" y se mueve al pasillo
    $ _msg_ahi_salgo = mensaje_puerta_npc(_npc_habitacion, "ahi_salgo")
    if _npc_habitacion == "violet":
        violet "[_msg_ahi_salgo]"
    elif _npc_habitacion == "jasmine":
        jasmine "[_msg_ahi_salgo]"
    elif _npc_habitacion == "monica":
        monica "[_msg_ahi_salgo]"
    pause 0.5
    $ _pasillo_destino = PASILLO_NPC.get(_npc_habitacion)
    $ sistema_locaciones.mover_a_locacion(_pasillo_destino)
    if _pasillo_destino and _npc_obj:
        $ _npc_obj.locacion_actual = _pasillo_destino
    $ mostrar_hud()
    return


label interaccion_banio_ocupado:
    # El NPC ya puede haber terminado — re-verificar
    $ _npc_banio_obj = obtener_npc_en_banio(_destino_banio_npc)

    if not _npc_banio_obj:
        # Baño libre — entrar normalmente
        $ sistema_locaciones.mover_a_locacion(_destino_banio_npc)
        return

    $ ocultar_hud()
    hide screen hud_navegacion
    window hide

    # Usar el background de la locación actual del jugador (hallway o habitacion)
    $ _bg_banio_frente = store.sistema_locaciones.locacion_actual.background if store.sistema_locaciones.locacion_actual else None

    call screen menu_banio_npc(_npc_banio_obj.id, bg_path=_bg_banio_frente)

    if _return == "espiar":
        # El HUD queda oculto: el minijuego fuerza su propio panel de acciones.
        # espiar_iniciar termina en return, cerrando este frame correctamente.
        $ _espiar_npc_temp = _npc_banio_obj.id
        jump espiar_iniciar

    if _return == "golpear":
        play sound "audio/sfx/door_knock_3.ogg"
        pause 0.5
        if _npc_banio_obj.id == "violet":
            violet "Me estoy bañando."
        elif _npc_banio_obj.id == "jasmine":
            jasmine "Me estoy bañando."
        elif _npc_banio_obj.id == "monica":
            monica "Me estoy bañando."

    $ mostrar_hud()
    return
