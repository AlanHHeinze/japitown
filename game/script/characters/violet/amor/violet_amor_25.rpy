################################################################################
## Violet — Amor 25 · "Solos en casa"
################################################################################
##     archivo   violet_amor_25.rpy
##     quest     violet_amor_05           (quests_amor_violet.rpy)
##     label     quest_violet_amor_05     (lo fija el motor: "quest_" + id)
##
## Es una quest de UN DIA ENTERO: arranca al despertar el domingo y se cierra
## esa misma noche. El domingo NO es un chequeo suelto — es un Requisito de la
## quest, asi que hasta que llegue el dia la quest se queda en ETAPA_CONDICIONES
## mostrando cuantos dias faltan.
##
## LAS SEIS FASES (flag `va25_fase`), cada una con su disparador:
##
##   0  esperando el domingo          → trigger de dormir
##   1  buscando a Monica             → trigger de game_loop (entrar al living)
##   2  dia libre en casa             → trigger de game_loop (llegar la noche)
##   3  la cena                       → listener de la accion "cocinar"
##   4  corte de luz                  → trigger de game_loop (entrar a hviolet)
##   5  terminada
##
## Los disparadores son excluyentes: cada uno solo existe en su fase, asi que
## nunca hay dos formas de avanzar al mismo tiempo.
##
## EL CORTE DE LUZ usa `horario_visual_override` (locationsystem_core): pinta
## toda la casa como si fuera trasnoche sin tocar el reloj. Se apaga en el
## cierre de la quest — si quedara prendido, la casa se veria de madrugada para
## siempre.


################################################################################
## Estado
################################################################################

# 0 espera · 1 buscar a Monica · 2 dia libre · 3 cena · 4 corte de luz · 5 fin
default va25_fase = 0


init python:

    # ── Locaciones permitidas en cada fase ───────────────────────────────────

    # Fase 2 — toda la casa MENOS la calle y la habitacion de Violet.
    # Se lista lo permitido y no lo prohibido porque `locaciones_permitidas` es
    # una whitelist: asi una locacion nueva del juego no se cuela sola en una
    # quest vieja.
    VA25_CASA_LIBRE = [
        "casa_hmc", "casa_pasilloarriba", "casa_pasilloabajo", "casa_living",
        "casa_comedor", "casa_cocina", "casa_banioarriba", "casa_banioabajo",
        "casa_gym", "casa_patio", "casa_garage", "casa_sotano", "casa_altillo",
    ]

    # Fase 4 — con la luz cortada solo se anda por el camino a su puerta.
    VA25_CORTE_LUZ = [
        "casa_pasilloabajo", "casa_living", "casa_pasilloarriba", "casa_hviolet",
    ]

    # ── Textos de la quest (los usa quests_amor_violet.rpy) ──────────────────

    def _va25_dias_hasta_domingo():
        """Dias que faltan para el domingo. 0 = hoy es domingo."""
        return (6 - getattr(store, 'dia_semana_actual', 0)) % 7

    def _quehacer_va25_condiciones():
        """Que hacer en ETAPA_CONDICIONES: el umbral primero, la espera despues."""
        if obtener_stat1("violet") < 25:
            return _quehacer_amor_violet(25)
        _d = _va25_dias_hasta_domingo()
        if _d == 1:
            return renpy.translate_string("Esperar 1 dia")
        return renpy.translate_string("Esperar {} dias").format(_d)

    # ── Condiciones de los disparadores ──────────────────────────────────────

    def _va25_activa():
        """La quest esta lista y todavia no se cerro."""
        return quest_lista_para_boton("violet_amor_05")

    def _va25_trigger_dormir():
        """
        Trigger de dormir, fase "despues": corre con el dia nuevo ya empezado y
        despues del autosave.

        Chequea el domingo aunque el Requisito ya lo pida: las etapas de una
        quest solo AVANZAN, nunca vuelven atras. Si el jugador llegara a 25 de
        amor un domingo a la tarde, la quest quedaria en BOTON_LISTO y sin este
        chequeo la escena saltaria el lunes al despertar.
        """
        if not _va25_activa() or store.va25_fase != 0:
            return None
        if store.dia_semana_actual != 6:
            return None
        return "violet_amor_25_despertar"

    def _gl_trigger_violet_amor_25():
        """
        Trigger de game_loop. Cubre las tres transiciones que no dependen de un
        boton, cada una en su fase.

        La de la noche va por game_loop y no por registrar_trigger_avanzar a
        proposito: el horario tambien lo mueven cocinar, ver TV, entrenar,
        trabajar y el talk, que llaman a avanzar_horario() directamente y no
        pasan por el label accion_avanzar_tiempo. El game_loop corre despues de
        TODAS, asi que es el unico punto que las ve a todas.
        """
        if not _va25_activa():
            return None

        _loc = store.sistema_locaciones.locacion_actual
        _loc_id = _loc.id if _loc else None

        if store.va25_fase == 1 and _loc_id == "casa_living":
            return "violet_amor_25_living"

        if store.va25_fase == 2 and store.horario_actual == 2:
            return "violet_amor_25_noche"

        if store.va25_fase == 4 and _loc_id == "casa_hviolet":
            return "quest_violet_amor_05"

        return None

    # ── Bloqueos y botones de la fase 2 (dia libre) ──────────────────────────

    def _va25_fase_libre():
        return _va25_activa() and getattr(store, 'va25_fase', 0) == 2

    def _va25_no_avanzar_de_noche():
        """
        De noche ya no se adelanta el tiempo: el dia se termina con la cena.

        Va como bloqueo REGISTRADO y no dentro de `acciones_bloqueadas` de la
        restriccion porque depende del horario, y el set de la restriccion es
        estatico — habria que rearmar la restriccion cada vez que cambia la hora.
        """
        return _va25_activa() and getattr(store, 'va25_fase', 0) >= 2 \
            and store.horario_actual >= 2

    def _va25_bloquear_dormir():
        """
        Durante el domingo no se va a dormir: el dia se cierra con la escena.

        Pide fase >= 1 y NO solo que la quest este lista. Si mirara solo la
        quest habria un deadlock: llegando a 25 de amor un domingo la quest
        pasa a BOTON_LISTO ese mismo dia con la fase todavia en 0, y el
        disparador de la fase 1 es justamente dormir — o sea que se bloquearia
        a si misma y la quest no arrancaria nunca.
        """
        return _va25_activa() and getattr(store, 'va25_fase', 0) >= 1

    def _va25_listener_pasatiempo():
        """Condicion de los listeners de cocinar / ver TV durante el dia libre."""
        return _va25_fase_libre() and store.horario_actual < 2

    def _va25_listener_cena():
        """Condicion del listener de cocinar en la fase de la cena."""
        return _va25_activa() and getattr(store, 'va25_fase', 0) == 3

    def _va25_boton_matar_tiempo():
        """
        Boton "Matar el tiempo" del menu de Violet: solo por la tarde, con ella
        en el living, durante el dia libre.
        """
        return (_va25_fase_libre()
                and store.horario_actual == 1
                and tracker_locacion_npc("violet") == "casa_living")

    # ── Puerta de Violet ─────────────────────────────────────────────────────

    def _va25_puerta_entrar():
        """Opcion "Entrar" de la puerta, solo durante el corte de luz."""
        return _va25_activa() and getattr(store, 'va25_fase', 0) == 4

    def _va25_puerta_durmiendo():
        """
        Durante el dia libre Violet duerme y no se la molesta. Es un bloqueo de
        GOLPE y no un recorte de `locaciones_permitidas` porque asi el mensaje
        es especifico: la whitelist tiene un solo mensaje para todos los
        destinos y ahi "Violet esta durmiendo" saldria tambien al ir a la calle.
        """
        return _va25_fase_libre()


init 5 python:

    registrar_trigger_dormir("violet_amor_25_domingo", "despues",
                             _va25_trigger_dormir)

    registrar_trigger_game_loop("violet_amor_25_fases",
                                _gl_trigger_violet_amor_25)

    registrar_bloqueo_accion("avanzar_tiempo", _va25_no_avanzar_de_noche,
                             "Ya es de noche, el dia se termina acá")
    registrar_bloqueo_accion("dormir", _va25_bloquear_dormir,
                             "Todavia no me voy a dormir")

    # Puerta de Violet. El resto de sus opciones vive en puertas_violet.rpy;
    # estas dos van acá porque son de esta quest y de ningun otro lado.
    registrar_opcion_puerta("violet", "Entrar",
                            "violet_amor_25_puerta_entrar", _va25_puerta_entrar,
                            ocultar_golpear=True)
    registrar_bloqueo_golpe("violet", _va25_puerta_durmiendo,
                            "Violet esta durmiendo")


################################################################################
## 1 · EL DESPERTAR — domingo a la mañana
################################################################################

label violet_amor_25_despertar:

    $ ocultar_hud()
    window show

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    piensa "Hoy tengo el dia libre pero no tengo planes, vere que puedo hacer"
    piensa "Quizas arregle para salir"

    # (Mc cuerpo celular)
    show mc_parado_base c_rbase_celular with sprite_fast
    piensa "Tengo una llamada perdida de Monica, voy a ver que quiere"

    hide mc_parado_base with dissolve

    # Hasta encontrarla no se hace otra cosa: solo el camino a el living.
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_living"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Debo ver a Monica"),
        mensaje_accion_default=_("Debo ver a Monica"),
        npcs_ocultos=["violet", "monica", "jasmine"],
    )

    $ va25_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · EL LIVING — Monica y Jasmine se despiden
################################################################################

label violet_amor_25_living:

    $ ocultar_hud()
    window show

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg

    # Las dos ya estaban en el living; el que llega es el MC.
    # (Monica cuerpo base ojos base boca neutral)
    show monica_parada c_rbase_base o_base b_none at right
    # (Jasmine cuerpo base ojos base boca neutral)
    show jasmine_parada c_rbase_base o_base b_none at center
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    # =========================================================================
    # CONTENIDO — le cuentan que se van y lo dejan solo en casa con Violet
    # =========================================================================

    # (Monica boca hablando)
    show monica_parada b_hablando
    monica "..."
    # (Monica boca neutral)
    show monica_parada b_none

    # (Jasmine boca hablando)
    show jasmine_parada b_hablando
    jasmine "..."
    # (Jasmine boca neutral)
    show jasmine_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide monica_parada
    hide jasmine_parada
    with dissolve

    piensa "..."

    hide mc_parado_base with dissolve

    # Dia libre: toda la casa menos la calle y la habitacion de Violet. Las
    # acciones que gastan el dia (entrenar, trabajar, cocinar, ver TV, avanzar)
    # quedan HABILITADAS a proposito — de eso se trata la fase.
    #
    # casa_hviolet queda afuera de la whitelist Y ademas tiene su bloqueo de
    # golpe registrado ("Violet esta durmiendo"): la whitelist corta el
    # movimiento y el bloqueo de golpe le pone el mensaje que corresponde.
    $ activar_restriccion(
        locaciones_permitidas=VA25_CASA_LIBRE,
        acciones_bloqueadas=[],
        mensaje_movimiento=_("Hoy me quedo en casa"),
        npcs_interactuables=["violet"],
    )

    $ va25_fase = 2

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · PASAR EL RATO — listeners de cocinar y ver TV durante el dia libre
################################################################################
## Son `label` de ListenerAccion, o sea SUBRUTINAS del executor de acciones:
## terminan en `return`.

label violet_amor_25_pasar_cocina:
    $ ocultar_hud()
    window show
    piensa "Podria comer algo para pasar el tiempo"
    window hide
    $ mostrar_hud()
    $ avanzar_horario()
    return


label violet_amor_25_pasar_tv:
    $ ocultar_hud()
    window show
    piensa "Podria ver algo para pasar el tiempo"
    window hide
    $ mostrar_hud()
    $ avanzar_horario()
    return


################################################################################
## 4 · MATAR EL TIEMPO — boton del menu de Violet, por la tarde en el living
################################################################################

label violet_amor_25_matar_tiempo:

    $ ocultar_hud()
    window show

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — matan el rato juntos en el living
    # =========================================================================

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    window hide
    $ mostrar_hud()
    $ avanzar_horario()
    jump game_loop


################################################################################
## 5 · LA NOCHE — se acuerda de la cena
################################################################################
## Salta apenas empieza la noche, este el MC donde este.

label violet_amor_25_noche:

    $ ocultar_hud()
    window show

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    piensa "Me tengo que encargar de la cena"

    hide mc_parado_base with dissolve

    # Solo cambia la fase: la restriccion del dia libre sigue sirviendo (misma
    # whitelist), y el bloqueo de avanzar el tiempo ya se activa solo por
    # horario (_va25_no_avanzar_de_noche).
    $ va25_fase = 3

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 6 · LA CENA Y EL CORTE DE LUZ
################################################################################
## Listener de "cocinar" en fase 3. Termina en `jump game_loop` (y no en
## `return` como los otros listeners) porque no devuelve al jugador donde
## estaba: cambia el estado del mundo entero.

label violet_amor_25_cocinar:

    $ ocultar_hud()
    window show

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — cocina, y en algun momento se corta la luz
    # =========================================================================

    piensa "..."

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # CORTE DE LUZ: la casa entera se pinta como trasnoche sin que el reloj
    # cambie. Lo apaga el cierre de la quest.
    $ horario_visual_override = HORARIO_TRASNOCHE

    # A oscuras solo se anda por el camino hasta la puerta de Violet.
    $ activar_restriccion(
        locaciones_permitidas=VA25_CORTE_LUZ,
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Sin luz no voy a andar dando vueltas por la casa"),
        mensaje_accion_default=_("Sin luz no puedo hacer nada de eso"),
        npcs_interactuables=["violet"],
    )

    # El jugador queda en la cocina, que es donde cocino.
    $ sistema_locaciones.mover_a_locacion("casa_cocina")

    $ va25_fase = 4

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 7 · LA PUERTA — opcion "Entrar" durante el corte de luz
################################################################################
## Opcion de puerta = SUBRUTINA: mueve al jugador adentro y devuelve el control.
## La escena la dispara el trigger de game_loop al ver que ya esta en
## casa_hviolet — asi el mismo camino sirve para el que entra por este boton y
## para el que entra directo porque su relacion se lo permite.

label violet_amor_25_puerta_entrar:
    $ sistema_locaciones.mover_a_locacion("casa_hviolet")
    return


################################################################################
## 8 · EL CIERRE — la escena en la habitacion de Violet
################################################################################

label quest_violet_amor_05:

    # Apagar el corte de luz y la restriccion es lo PRIMERO: si la escena se
    # cortara mas adelante, la casa quedaria a oscuras y el jugador encerrado.
    $ va25_fase = 5
    $ horario_visual_override = None
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    # La habitacion se sigue viendo a oscuras durante la escena: el fondo se
    # pide explicitamente en trasnoche, aunque el override global ya este
    # apagado.
    $ _va25_loc_hv = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _va25_bg = _va25_loc_hv.obtener_background_por_horario(HORARIO_TRASNOCHE) if _va25_loc_hv else "#1a1a1a"
    scene expression _va25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la escena final, solos y a oscuras
    # =========================================================================

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_05")

    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop
