################################################################################
## Viaje Rápido — menú de sublocaciones desde el HUD
################################################################################
## El botón cama del HUD superior despliega este menú: detecta la locación
## madre actual (por prefijo de id) y lista sus sublocaciones; al tocar una
## se viaja usando el MISMO flujo que un hotspot MOVE (accion_hotspot_move),
## así se respetan door access, baños ocupados, restricciones de quest y los
## hooks (quest 0 del MC, labels de restricción, mensajes en espera).
##
## Extensible: cuando haya más zonas (ciudad, tienda, etc.) basta con agregar
## la locación madre a LOCACIONES_MADRE con su prefijo de ids.
##
################################################################################
## EL VIAJE RECORRE LA RUTA, no teletransporta
################################################################################
## Antes el viaje armaba un hotspot con el destino y saltaba: el jugador
## aparecía del otro lado de la casa sin pasar por ningún lado. El problema no
## era estético — los disparadores que dependen de ENTRAR a una locación (los
## TRIGGERS_GAME_LOOP, casi todos con un chequeo de `locacion_actual`) no se
## enteraban, así que una quest que arranca en el living no arrancaba nunca por
## esta vía y el jugador se salteaba contenido sin querer.
##
## Ahora se calcula la ruta (`calcular_ruta`, ruta_locaciones.rpy) y se recorre
## paso a paso. En cada tramo se evalúa lo mismo que evalúa el game_loop, y lo
## primero que devuelva un label CORTA el viaje ahí.
##
## EL ÚLTIMO PASO VA POR EL FLUJO DE SIEMPRE (hotspot sintético →
## accion_hotspot_move). Eso es lo que mantiene funcionando door access, baños
## ocupados y el handler de la quest 0 sin duplicar una sola línea: los tramos
## intermedios son pasillos y cuartos comunes, y todo lo delicado pasa en el
## destino.
##
## AL CORTARSE, EL VIAJE SE CANCELA: el jugador queda donde saltó el trigger. No
## se guarda un destino pendiente a propósito — sería un flag más con reglas de
## vencimiento (cambio de horario, dormir, otra quest) y ninguna forma obvia de
## que el jugador sepa que sigue vigente.

define LOCACIONES_MADRE = {
    "casa": {
        "nombre": "Casa",
        "prefijo": "casa_",
        # Locacion destacada: va primera en el menu y lleva estrella.
        "destacada": "casa_hmc",
    },
}

# Locaciones que no aparecen en el menú (solo accesibles desde adentro de otra)
define VIAJE_RAPIDO_OCULTAS = ("casa_baniomonica",)

# Se ve el recorrido: cada locación del camino se pinta con su fondo y se
# sostiene un momento. Es lo que hace legible el corte — el jugador entiende
# DÓNDE se interrumpió el viaje y no le aparece una escena de la nada.
# En False el viaje sigue recorriendo la ruta (y disparando lo que haya en el
# medio), pero sin dibujar los pasos.
define VIAJE_MOSTRAR_RECORRIDO = True

# Cuánto se sostiene cada tramo. El `pause` es salteable con un click, así que
# quien ya conoce el camino puede apurarlo.
define VIAJE_PAUSA_PASO = 0.4


init python:

    def _vr_interrupcion():
        """
        ¿Algo tiene que cortar el viaje en esta locación? Devuelve un label o None.

        Es LO MISMO que evalúa el game_loop en cada vuelta, en el mismo orden.
        No se inventa un registro nuevo de "disparadores de camino": si una
        quest ya sabe arrancar cuando el jugador entra a una locación, arranca
        igual pasando de largo, sin que su archivo se entere de que existe el
        viaje rápido.

        ⚠️ Esto corre los cuatro embudos una vez por TRAMO y no una por acción.
        No es una clase de comportamiento nueva —el game_loop ya los corre
        después de cada interacción— pero un trigger escrito asumiendo "una vez
        por acción del jugador" ahora puede dispararse a mitad de viaje. Que es,
        justamente, lo que se busca.
        """
        actualizar_quests()
        if hasattr(store, 'sistema_mensajes'):
            store.sistema_mensajes.verificar_mensajes_en_espera()
        validar_eventos()
        return ejecutar_triggers_game_loop()

init python:

    def locacion_madre_actual():
        """Devuelve el id de la locación madre de la locación actual, o None."""
        loc = sistema_locaciones.locacion_actual
        if not loc:
            return None
        for _mid, _cfg in LOCACIONES_MADRE.items():
            if loc.id.startswith(_cfg["prefijo"]):
                return _mid
        return None

    def sublocaciones_de_madre(madre_id):
        """
        Sublocaciones registradas de una locación madre, en orden de registro
        salvo la destacada, que va primera. El sort es estable, asi que el resto
        conserva su orden original.
        """
        cfg = LOCACIONES_MADRE.get(madre_id)
        if not cfg:
            return []
        pref = cfg["prefijo"]
        locs = [l for l in sistema_locaciones.locaciones.values()
                if l.id.startswith(pref) and l.id not in VIAJE_RAPIDO_OCULTAS]
        destacada = cfg.get("destacada")
        if destacada:
            locs.sort(key=lambda l: 0 if l.id == destacada else 1)
        return locs

    def locacion_destacada(madre_id):
        """Id de la locación destacada de una madre (la que lleva estrella), o None."""
        cfg = LOCACIONES_MADRE.get(madre_id)
        return cfg.get("destacada") if cfg else None


label accion_viaje_rapido:

    if not _locacion_temp:
        return

    $ _vr_origen = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
    $ _vr_ruta = calcular_ruta(_vr_origen, _locacion_temp)

    # Sin ruta, o el destino es vecino directo: no hay nada que recorrer y se
    # va derecho por el flujo de siempre. El caso "sin ruta" también cae acá a
    # propósito — antes de este sistema todo viaje era un salto, así que un
    # mapa mal conectado degrada al comportamiento viejo en vez de dejar al
    # jugador sin poder viajar.
    if len(_vr_ruta) <= 1:
        jump viaje_rapido_ultimo_paso

    # EL HUD SE APAGA MIENTRAS SE CAMINA. Los `pause` de cada tramo son
    # interacciones como cualquier otra: con el HUD arriba el jugador puede
    # clickear un hotspot a mitad de viaje y arrancar un segundo movimiento
    # encima del que ya esta corriendo. `ocultar_hud` deja los botones fuera de
    # juego sin destruir el screen.
    $ ocultar_hud()

    # Los tramos del medio; el último se hace aparte, por el flujo completo.
    $ _vr_intermedios = _vr_ruta[:-1]
    $ _vr_i = 0
    jump viaje_rapido_paso


# Un label con índice y no un `for` de Python: adentro hay `pause` y `jump`, que
# son statements de Ren'Py y no se pueden meter en un bloque python.
label viaje_rapido_paso:

    if _vr_i >= len(_vr_intermedios):
        jump viaje_rapido_ultimo_paso

    $ _vr_dest = _vr_intermedios[_vr_i]

    # Restricción de quest: el camino pasa por una locación prohibida. Se corta
    # acá, con el mensaje de la restricción, en vez de dejarlo llegar al destino
    # y fallar recién ahí.
    $ _vr_msg = accion_bloqueada_movimiento(_vr_dest)
    if _vr_msg:
        $ mostrar_hud()
        $ _blk_guardar_toque()
        piensa "[_vr_msg]"
        return

    $ sistema_locaciones.mover_a_locacion(_vr_dest)
    $ actualizar_bg_master()

    if VIAJE_MOSTRAR_RECORRIDO:
        pause VIAJE_PAUSA_PASO

    # Lo que corta el viaje. El label es de CONTENIDO y cierra con
    # `jump game_loop`, así que no vuelve por acá: el viaje muere y el jugador
    # queda en esta locación, que es donde lo interrumpieron.
    $ _vr_label = _vr_interrupcion()
    if _vr_label:
        jump expression _vr_label

    # Un mensaje prioritario recién entregado no devuelve label —bloquea desde
    # el embudo de acciones— pero igual tiene que frenar el viaje: seguir
    # caminando con el celular sonando es justo lo que el mensaje quiere evitar.
    if obtener_bloqueo_mensaje_prioritario():
        $ mostrar_hud()
        return

    $ _vr_i += 1
    jump viaje_rapido_paso


# El tramo final, con el flujo completo de un hotspot MOVE. El hotspot sintético
# solo necesita destino: door access, baños ocupados, restricciones y el handler
# de la quest 0 leen únicamente _hotspot_temp.destino.
#
# Acá ya no hace falta acercar al jugador al pasillo antes de tocar una puerta
# (lo que hacía el viejo VIAJE_RAPIDO_PREVIA): la ruta a una habitación termina
# sola en el pasillo que la conecta, porque es por donde se entra caminando.
label viaje_rapido_ultimo_paso:

    # Se termino de caminar: el HUD vuelve y de aca en mas manda el flujo de
    # siempre, que ya sabe apagarlo si el destino abre una puerta o un baño.
    # En una ruta corta nunca se apago, asi que esto no hace nada.
    $ mostrar_hud()

    $ _hotspot_temp = Hotspot("viaje_rapido_" + _locacion_temp, "MOVE", 0, 0, 1, 1, destino=_locacion_temp, nombre="")
    jump accion_hotspot_move


screen menu_viaje_rapido():
    zorder 210
    modal True

    # Cerrar al tocar afuera (sin oscurecer la pantalla)
    button:
        xfill True
        yfill True
        background None
        action Hide("menu_viaje_rapido")

    $ _vr_madre_id = locacion_madre_actual()
    $ _vr_cfg = LOCACIONES_MADRE.get(_vr_madre_id) if _vr_madre_id else None
    $ _vr_actual = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
    $ _vr_destacada = locacion_destacada(_vr_madre_id) if _vr_madre_id else None
    $ _vr_small = renpy.variant("small")
    $ _vr_k = 2.0 if _vr_small else 1.0

    if _vr_small:
        # Pantalla táctil: centrado, texto y contenedor al doble, con scroll
        # táctil (draggable) porque la lista de filas puede superar el alto
        # de pantalla disponible.
        frame:
            xalign 0.5
            yalign 0.5
            xsize int(400 * _vr_k)
            background "#101024F0"
            padding (int(12 * _vr_k), int(12 * _vr_k))

            vbox:
                spacing int(4 * _vr_k)

                if _vr_cfg:
                    text renpy.translate_string(_vr_cfg["nombre"]) size int(24 * _vr_k) color "#4FC3F7" bold True xalign 0.5
                    null height int(4 * _vr_k)

                    viewport:
                        xfill True
                        ysize 820
                        draggable True
                        mousewheel True
                        scrollbars "vertical"

                        vbox:
                            spacing int(4 * _vr_k)

                            for _vr_loc in sublocaciones_de_madre(_vr_madre_id):
                                if _vr_loc.id == _vr_actual:
                                    # Locación actual: marcada, no clickeable
                                    frame:
                                        xsize int(376 * _vr_k)
                                        ysize int(42 * _vr_k)
                                        background "#1b1b33"
                                        padding (int(12 * _vr_k), 0)
                                        use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#8888AA", True, _vr_k)
                                else:
                                    button:
                                        xsize int(376 * _vr_k)
                                        ysize int(42 * _vr_k)
                                        background "#1e1e3a"
                                        hover_background "#2a3f5f"
                                        padding (int(12 * _vr_k), 0)
                                        action [Hide("menu_viaje_rapido"), SetVariable("_locacion_temp", _vr_loc.id), Call("accion_viaje_rapido")]
                                        use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#FFFFFF", False, _vr_k)
                else:
                    text renpy.translate_string("No hay destinos disponibles") size int(21 * _vr_k) color "#dddddd"

    else:
        frame:
            xanchor 1.0
            xpos 1920 - 290     # borde derecho alineado bajo el botón cama (xoffset -344)
            ypos 112
            xsize 400
            background "#101024F0"
            padding (12, 12)

            vbox:
                spacing 4

                if _vr_cfg:
                    text renpy.translate_string(_vr_cfg["nombre"]) size 24 color "#4FC3F7" bold True xalign 0.5
                    null height 4

                    for _vr_loc in sublocaciones_de_madre(_vr_madre_id):
                        if _vr_loc.id == _vr_actual:
                            # Locación actual: marcada, no clickeable
                            frame:
                                xsize 376
                                ysize 42
                                background "#1b1b33"
                                padding (12, 0)
                                use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#8888AA", True)
                        else:
                            button:
                                xsize 376
                                ysize 42
                                background "#1e1e3a"
                                hover_background "#2a3f5f"
                                padding (12, 0)
                                action [Hide("menu_viaje_rapido"), SetVariable("_locacion_temp", _vr_loc.id), Call("accion_viaje_rapido")]
                                use _vr_fila(_vr_loc, _vr_loc.id == _vr_destacada, "#FFFFFF", False)
                else:
                    text renpy.translate_string("No hay destinos disponibles") size 21 color "#dddddd"


# Contenido de una fila del menu. La fila mide 376x42 con padding (12, 0), asi que
# el area util es 352x42: la estrella y los iconos de NPC entran holgados y, al ser
# el alto fijo, no pueden agrandar la fila. En pantalla táctil, k=2.0 escala todo
# el contenido de la fila para ocupar las nuevas dimensiones (752x84).
screen _vr_fila(loc, destacada, color_texto, aqui, k=1.0):
    fixed:
        xfill True
        yfill True

        # Estrella + nombre, pegados a la izquierda
        hbox:
            xalign 0.0
            yalign 0.5
            spacing int(6 * k)

            if destacada:
                text "⭐" size int(19 * k) yalign 0.5

            $ _vr_nombre = renpy.translate_string(loc.nombre)
            text "[_vr_nombre]" size int(21 * k) color color_texto yalign 0.5

        # Iconos de quien esta en la locacion, pegados a la derecha: primero el
        # marcador del jugador (solo donde esta el) y despues los NPCs.
        # Reusa tracker_npcs_en_locacion (hud_tracker), asi respeta las mismas
        # reglas que la app: los NPCs ocultos por quest tampoco aparecen aca.
        hbox:
            xalign 1.0
            yalign 0.5
            spacing int(4 * k)

            if aqui:
                text "📍" size int(20 * k) yalign 0.5

            for _vr_npc in tracker_npcs_en_locacion(loc.id):
                $ _vr_icono = tracker_icono_npc(_vr_npc)
                if _vr_icono:
                    add _vr_icono fit "contain" xysize (int(26 * k), int(26 * k)) yalign 0.5
