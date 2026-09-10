################################################################################
## Violet — VENTAJA "Ropa Nueva" · el controlador
################################################################################
## Ventaja del hito de amor 30. El menu de Violet ofrece que se pruebe algo
## nuevo: se elige la prenda de un menu y cada una corre su propia escena.
##
## SE LE PUEDE PEDIR DESDE CUALQUIER LADO. Si ya estan en su habitacion la
## escena arranca de una; si no, ella lo CITA —"vente a mi habitacion"—, se va, y
## la escena queda pendiente hasta que el MC llegue. Ver "La convocatoria".
##
## DIFERENCIA CON JUEGOS NUEVOS: aquel solo ENUMERA lo que falta (cada juego se
## juega por su via). Acá la prenda se juega desde la charla, asi que cada una
## registra ademas su LABEL.
##
## COMO AGREGAR UNA PRENDA: crear su `rn_<nombre>.rpy` en esta carpeta con su
## label y su flag, y llamar a registrar_prenda_nueva() desde su init 5.
## ESTE ARCHIVO NO SE TOCA.
##
##     characters/violet/ventajas/ropanueva/
##     ├── ropanueva_violet.rpy   ← esto
##     ├── rn_vestido.rpy         ← una prenda
##     └── rn_jean.rpy            ← otra, esta se puede repetir


init python:

    # [(orden, reg, prenda_id, nombre, label, fn_vista)]
    ROPA_NUEVA_VIOLET = []

    def registrar_prenda_nueva(prenda_id, nombre, label, vista, orden=0):
        """
        Registra una prenda que Violet se puede probar.

        Args:
            prenda_id: id unico (ej. "vestido")
            nombre: como aparece en el menu. Se traduce al mostrarlo.
            label: label de la escena. Es CONTENIDO, asi que cierra con
                jump game_loop.
            vista: funcion de MODULO sin argumentos → True si ya se la probo.
            orden: menor primero. A igual orden, orden de registro.
        """
        ROPA_NUEVA_VIOLET.append((orden, len(ROPA_NUEVA_VIOLET),
                                  prenda_id, nombre, label, vista))

    def ropa_nueva_pendientes_violet():
        """
        Prendas que todavia no se probo, ya ordenadas → [(nombre, label)].

        Una prenda cuya funcion `vista` reviente se considera NO vista y se
        sigue ofreciendo: es preferible que se repita a que el menu se corte por
        una prenda mal escrita.
        """
        _pendientes = []
        for _orden, _reg, _pid, _nom, _lbl, _fn in sorted(ROPA_NUEVA_VIOLET,
                                                          key=lambda p: (p[0], p[1])):
            try:
                if _fn():
                    continue
            except Exception:
                pass
            _pendientes.append((_nom, _lbl))
        return _pendientes

    def _violet_boton_ropa_nueva():
        """
        Condicion del boton del menu de Violet.

        YA NO PIDE QUE ESTE EN SU HABITACION: desde cualquier lado se le puede
        pedir que se pruebe algo, y si no estan ahi ella lo cita. El menu solo
        se abre clickeando su sprite, asi que su presencia —y que sea
        interactuable— ya esta garantizada por el embudo del menu.
        """
        return npc_tiene_ventaja("violet", "ropa_nueva")

    def _rn_ya_en_habitacion():
        """True si el MC ya esta en la habitacion de Violet."""
        _loc = store.sistema_locaciones.locacion_actual
        return _loc is not None and _loc.id == "casa_hviolet"


################################################################################
## La convocatoria — "vente a mi habitacion"
################################################################################
## Cuando la prenda se pide fuera de su habitacion, la escena no corre ahi
## mismo: ella se va y queda PENDIENTE hasta que el MC suba.
##
## VA COMO TRIGGER DE GAME_LOOP Y NO COMO registrar_label_locacion: entre la
## cita y la llegada el jugador anda suelto y puede hacer cualquier otra cosa.
## Ese registro vive adentro del slot unico `restriccion_quest_activa`, asi que
## el primer contenido que active o desactive una restriccion en el medio se
## lleva el disparo puesto y la escena no ocurre nunca.
##
## LA CITA VENCE AL CAMBIAR EL HORARIO. Se pide "vente a mi habitacion", no
## "esperame toda la semana". En vez de limpiar el flag desde triggers de
## avanzar y de dormir —dos lugares que se pueden desincronizar— la cita guarda
## el dia y el horario en que se hizo y el propio trigger la descarta cuando ya
## no corresponden.

# {"label", "dia", "horario"} mientras hay una cita en pie; None si no.
default rn_convocatoria_violet = None


init python:

    def _rn_cita_vigente():
        """
        El label de la cita en pie, o None. Chequeo PURO, sin efectos.

        Lo consultan las DOS vias de entrada: el trigger de game_loop (entrar a
        su pieza) y la condicion del boton de puerta. Que no toque nada es
        obligatorio por la segunda: esa condicion la evalua el armado del menu,
        y una condicion de UI que muta estado se dispara sola cuando el
        predictor corre el screen sin mostrarlo.

        No mira donde esta el MC: el trigger lo pide adentro y el boton, en el
        pasillo.
        """
        _cita = getattr(store, 'rn_convocatoria_violet', None)
        if not _cita:
            return None

        if (_cita.get("dia") != store.dias_totales
                or _cita.get("horario") != store.horario_actual):
            return None

        # Que ella tambien este: si algo la movio en el medio, la cita se cae.
        if tracker_locacion_npc("violet") != "casa_hviolet":
            return None

        return _cita.get("label")

    def _rn_puerta_ver_ropa():
        """Condicion del boton 'Ver ropa' del menu de la puerta."""
        return _rn_cita_vigente() is not None

    def _rn_trigger_convocatoria():
        """Trigger de game_loop: corre la prenda pendiente al llegar a su pieza."""
        _cita = getattr(store, 'rn_convocatoria_violet', None)
        if not _cita:
            return None

        # La cita vencida se descarta ACA y en ningun otro lado: este trigger es
        # lo unico que corre en cada vuelta del loop.
        if (_cita.get("dia") != store.dias_totales
                or _cita.get("horario") != store.horario_actual):
            store.rn_convocatoria_violet = None
            return None

        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_hviolet":
            return None

        _lbl = _rn_cita_vigente()
        if not _lbl:
            return None

        store.rn_convocatoria_violet = None
        return _lbl


init 5 python:

    registrar_trigger_game_loop("rn_convocatoria_violet",
                                _rn_trigger_convocatoria)


################################################################################
## La segunda via — "Ver ropa" en el menu de la puerta
################################################################################
## El trigger de arriba pide ENTRAR a su habitacion, y entrar puede no estar
## disponible: los niveles de acceso del door_access dependen de los stats y del
## horario, una quest puede tener la puerta tomada, o el jugador puede no llegar
## a pasar. Si eso ocurre la cita se vence sin que la escena ocurra nunca.
##
## Esta opcion es la red: aparece en el menu de la puerta mientras la cita este
## en pie y entra directo a la escena, sin depender del acceso.
##
## ⚠️ NO SE ENTRA A LA HABITACION, y es a proposito. El label salta a la escena
## sin mover al MC, asi que cuando la escena cierra con `jump game_loop` el
## jugador sigue en el pasillo, que es de donde vino. Si alguien "arregla" esto
## agregando un mover_a_locacion("casa_hviolet"), lo deja adentro de un cuarto
## en el que nunca entro y del que la puerta podria no dejarlo salir.
##
## La otra via no cambia: si el jugador SI puede entrar, entra, y el trigger
## dispara la escena adentro. Ahi terminar en la habitacion es lo correcto.

label violet_rn_puerta:

    # Se lee y se consume antes de saltar: la escena termina en `jump
    # game_loop` y no vuelve por aca, asi que no hay despues donde limpiarla.
    $ _rnp_label = _rn_cita_vigente()
    $ rn_convocatoria_violet = None

    # Red de seguridad: la condicion del boton ya garantiza que hay cita, pero
    # entre que se dibujo el menu y el click pudo cambiar el horario.
    if not _rnp_label:
        $ mostrar_hud()
        jump game_loop

    jump expression _rnp_label


################################################################################
## La charla
################################################################################

label violet_ropa_nueva:

    $ ocultar_hud()
    window show

    # El fondo sale de la locacion ACTUAL: la charla ya no pasa siempre en su
    # habitacion, se le puede pedir donde sea que este.
    $ _rn_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _rn_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: de noche esta en pijama.
    $ _rn_cuerpo = cuerpo_activo("violet")
    if _rn_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "¿Te compraste algo nuevo?"
    # (Mc boca neutral)
    show mc_parado_base b_none

    $ _rn_pendientes = ropa_nueva_pendientes_violet()

    if not _rn_pendientes:
        # (Violet boca hablando)
        show violet_parada b_hablando
        violet "Ahora no tengo nada nuevo para probarme (Más contenido en futuras actualizaciones)"
        # (Violet boca neutral)
        show violet_parada b_none

        hide mc_parado_base
        hide violet_parada
        with dissolve

        window hide
        $ mostrar_hud()
        jump game_loop

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Sí, algo tengo. ¿Qué quieres que me pruebe?"
    # (Violet boca neutral)
    show violet_parada b_none

    # display_menu y NO un bloque `menu:`: las opciones salen del registro, y el
    # bloque estatico no se puede armar en runtime. Mismo recurso que usa el
    # sistema de talk (talksystem_labels).
    #
    # Los nombres se traducen ANTES de armar el menu: salen de una variable, y
    # el `menu` no pasa por el sistema de traduccion por id.
    python:
        _rn_items = [(renpy.translate_string(_nom), _lbl)
                     for _nom, _lbl in _rn_pendientes]
        _rn_items.append((renpy.translate_string("Volver"), None))

    $ _rn_elegido = renpy.display_menu(_rn_items)

    if _rn_elegido is None:
        hide mc_parado_base
        hide violet_parada
        with dissolve

        window hide
        $ mostrar_hud()
        jump game_loop

    if _rn_ya_en_habitacion():
        hide mc_parado_base
        hide violet_parada
        with dissolve

        window hide
        jump expression _rn_elegido

    # ── LA CITA — no estan en su habitacion ──────────────────────────────────
    # ⚠️ NARRATIVA PROVISORIA: por ahora se lo pide y el MC acepta y ya. Va a
    # crecer.

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Vente a mi habitación"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Ok"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # Se va: primero desaparece el sprite y despues se la mueve de verdad.
    # Alcanza con `locacion_actual` —es lo que leen `esta_en_locacion` y
    # `tracker_locacion_npc`, o sea el sprite, el tracker y las puertas—; es el
    # mismo recurso que usa el motor en door_access_system.
    hide violet_parada with dissolve
    $ obtener_npc("violet").locacion_actual = "casa_hviolet"

    python:
        rn_convocatoria_violet = {
            "label": _rn_elegido,
            "dia": dias_totales,
            "horario": horario_actual,
        }

    hide mc_parado_base with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop
