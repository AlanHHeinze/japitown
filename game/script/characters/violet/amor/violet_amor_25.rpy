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


    show monica_parada b_hablando
    monica "Hola [mc_name], con Jasmine vamos a ir al shopping a hacer unas compras y ver una pelicula"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "¿Que van a ver?"
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "La moda viste al diablo"
    show jasmine_parada b_none

    show mc_parado_base b_hablando
    mc "¿Y Violet no va?"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "No es su estilo de salida ni de pelica, dijo que se preferia quedar"
    show monica_parada b_abiertachica
    monica "Te tengo que pedir un favor tambien"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "Si decime"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Puede que hoy me llegue un paquete, podrias estar atento para recibirlo"
    show monica_parada b_abiertachica
    monica "No confio en que Violet este atenta"
    show monica_parada b_none
    
    show mc_parado_base b_hablando
    mc "Si, no hay problema yo voy a quedarme todo el dia en casa"
    show mc_parado_base b_abiertachica
    mc "Despreocupate y pasen un lindo dia"
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "Nos vemos luego"
    show jasmine_parada b_none

    show monica_parada b_hablando
    monica "Adios"
    show monica_parada b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide monica_parada
    hide jasmine_parada
    with dissolve

    piensa "Tengo todo el dia"

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

    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — matan el rato juntos en el living
    # =========================================================================

    show violet_parada b_hablando
    violet "¿Que pasa?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Estoy aburrido ¿Miramos alguna pelicual?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Que sea algo de accion"
    show violet_parada b_none

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

    piensa "Supongo que voy a cocinar algo para los dos, si espero que Violet lo haga voy a morir de hambre antes"
    piensa "Voy a ver que hay en la cocina"

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

    piensa "Podra hacer unas hamburguesas, algo simple y rapido"

    # ── SE CORTA LA LUZ ──────────────────────────────────────────────────────
    #
    # El override pinta la casa ENTERA como trasnoche sin tocar el reloj, asi
    # que se prende acá y no mas abajo: es el instante del corte, y de paso deja
    # el resto de la casa ya a oscuras para cuando salga de la cocina. Lo apaga
    # el cierre de la quest.
    $ horario_visual_override = HORARIO_TRASNOCHE

    # SIN TRANSICION a proposito: la luz se corta de golpe, no se desvanece.
    # `scene` limpia la capa entera, asi que el MC se vuelve a poner con los
    # mismos atributos —tambien sin transicion— y queda como si no se hubiera
    # movido: lo unico que cambia es el fondo.
    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center

    piensa "Uhhhh se corto la luz..."
    piensa "No se ve luz afuera tampoco, se ve que el corte es general, no de la casa"
    piensa "Le voy a preguntar a Violet si quiere esperar, o comer a oscuras"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

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

    
    show violet_parada c_rbase_base ca_base o_base b_none at right
    pause 0.2
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la escena final, solos y a oscuras
    # =========================================================================

    show violet_parada b_hablando
    violet "¿El corte es general no?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Parece que si, vamos a tener que esperar que vuelve"
    show mc_parado_base b_abiertachica
    mc "¿Sigo cocinando? o ¿Esperamos un poco a ver si vuelve la luz?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Mejor esperamos, no me gusta comer a oscuras"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Bueno, me voy a mi habitacion a acostarme un rato hasta que vuelva"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Espera..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Que pasa?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Si queres te podes quedar aca acostado hasta que la luz vuelva"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Mmmm... ¿Le seguis teniendo miendo a la oscuridad?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "No"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Entonces me voy, voy a estar mas comodo en mi cama"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Espera... no es que me muera de miedo cuando se esta todo oscuro pero pero si me da un poco"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "En algunas cosas no cambiaste nada"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Pero ahora la situacion es distinta, despues de tantas peliculas de terror la imaginacion me da a pensar que cosas terribles pueden pasar"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No va a pasar nada, es solo un corte de luz"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "¿Y si el corte lo genero un asesino para venir a matarnos?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No creo que nadie me quiera matar"
    show mc_parado_base b_abiertachica
    mc "¿A ti?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "En internet no soy un gran ejemplo, sobre todo cuando pierdo en un juego"
    show violet_parada b_none

    "¡ÑEEEEEEEEEEEEEEEEEC!"

    show violet_parada b_hablando
    violet "¿Eso fue una puerta abajo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Pudo ser el viento"
    show mc_parado_base b_none

    "¡Plaf!"

    piensa "¿Que fue eso?"

    "¡Plaf! ¡Plaf! ¡Plaf!"

    # ── EL ABRAZO Y EL BESO ──────────────────────────────────────────────────
    #
    # Tres tramos:
    #   1. Violet CAMINA hacia el MC (npc_acercarse, el mismo transform de la
    #      quest de deseo 25). El se queda donde esta.
    #   2. se van los dos sprites y entra el layeredimage, que ya los trae
    #      dibujados juntos y arranca solo en `ab_1` (el default de su grupo)
    #   3. la secuencia: abrazo → beso → vuelve al abrazo
    #
    # El `pause` despues del acercamiento es por el transform: dura 0.8s y sin
    # esperarlo el cambio de sprites lo cortaria a la mitad.

    show violet_parada b_none at npc_acercarse
    pause 0.2

    hide mc_parado_base
    hide violet_parada
    show beso_amor_violet with dissolve
    pause 0.5

    # ÚNICO DIÁLOGO de la secuencia, sobre el primer abrazo. Las bocas son dos
    # grupos aparte del layeredimage: se prenden y se apagan como en cualquier
    # sprite, y son independientes entre si.

    show beso_amor_violet bmc_hablando
    mc "Hey tranquila"
    show beso_amor_violet bmc_none

    show beso_amor_violet bv_hablando
    violet "Te dije que algo malo iba a pasar"
    show beso_amor_violet bv_none

    show beso_amor_violet bmc_hablando
    mc "Yo te digo que nada malo va a pasar, estoy aca con vos y te voy a cuidar"
    show beso_amor_violet bmc_none

    # De acá hasta el final va de corrido, sin dialogo ni clicks: cada cuadro
    # entra con sprite_normal y se sostiene medio segundo. Los `pause` llevan
    # duracion, asi que corren solos.
    #
    # El grupo de la secuencia es UNO, o sea que los atributos son excluyentes:
    # cada `show` reemplaza el cuadro anterior y no hay que apagar nada.
    show beso_amor_violet ab_2 with sprite_normal
    pause 1

    show beso_amor_violet ab_3 with sprite_normal
    pause 0.5

    show beso_amor_violet ab_4 with sprite_normal
    pause 0.5

    show beso_amor_violet ab_5 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_1 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_2 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_3 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_4 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_3 with sprite_normal
    pause 0.5

    show beso_amor_violet bs_4 with sprite_normal
    pause 0.5

    monica "¿Chicos donde estan?"

    piensa "Asi que eso habia sido el rudio"

    hide beso_amor_violet with dissolve

    show violet_parada c_rbase_base ca_base o_base b_none ot_verguenza at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with dissolve
    
    show mc_parado_base b_hablando
    mc "Ehhh ¿Estas mejor?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Gracias"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Llegaron las chicas, vamos"
    show mc_parado_base b_none

    # ── EL LIVING — estan las cuatro ─────────────────────────────────────────
    #
    # Se mueve de verdad y no solo cambia el fondo: la escena sigue en el living
    # y despues en la pieza del MC, asi que el motor tiene que saber donde esta.
    #
    # El fondo va con el horario REAL (la luz volvio) y con fade, que es la
    # transicion de cambio de escena.

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ sistema_locaciones.mover_a_locacion("casa_living")

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg with fade

    # Mismo cuadro de cuatro que la intro y con los mismos transforms
    # (core/utils/transforms_common.rpy): el MC en su mc_izquierda y las tres a
    # la derecha, en el mismo orden. El orden de los `show` es el orden de
    # profundidad: el ultimo queda al frente.
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base ca_base o_base b_none ot_verguenza at grupo3_izq
    # (Jasmine cuerpo base ojos base boca neutral)
    show jasmine_parada c_rbase_base o_base b_none at grupo3_centro
    # (Monica cuerpo base ojos base boca neutral)
    show monica_parada c_rbase_base o_base b_none at grupo3_der
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la charla entre las cuatro
    # =========================================================================

    show mc_parado_base b_hablando
    mc "Volvieron mas temprano de lo esperado"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "El corte de luz es muy grande y afecta a casi toda la ciudad"
    show monica_parada b_abiertachica
    monica "El shopping estaba con luces de emergenica y el cine cerrado"
    show monica_parada b_none

    show jasmine_parada b_hablando
    jasmine "Nos reprogramaron la entrada para el proximo domingo"
    show jasmine_parada b_none

    show mc_parado_base b_hablando
    mc "Uhhhh una lastima"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "No es tan grave, compramos algo de comida en el camino para cenar todos juntos"
    show monica_parada b_abiertachica
    monica "¿Violet estas bien?"
    show monica_parada b_none

    show violet_parada b_hablando
    violet "Si"
    show violet_parada b_none

    show jasmine_parada b_hablando
    jasmine "Estas roja ¿No estaras con fiebre no?"
    show jasmine_parada b_none

    show mc_parado_base b_hablando
    mc "Debe ser que se asusto con los ruidos"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "No tenia miedo..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No dije eso, ahora vamos a comer"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Si comamos antes que se enfrie"
    show monica_parada b_none

    # ── DESPUES DE LA CENA ───────────────────────────────────────────────────
    #
    # El cartel espera el click y no un `pause` con segundos: es un corte de
    # tiempo, no un efecto — el jugador decide cuando sigue.

    scene black with fade
    show text Text(renpy.translate_string("Luego de la cena"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause
    hide text with dissolve

    # ── SU HABITACION — solo, antes de dormir ────────────────────────────────

    $ sistema_locaciones.mover_a_locacion("casa_hmc")

    $ _va25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va25_bg with fade

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    piensa "Todo paso muy rapido y luego llegaron las chicas, no tuve tiempo de hablar con Violet"
    piensa "Me pregunto que pensara de esto que paso"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # La quest se cierra ANTES de dormir: asi el motor restaura la rutina de
    # Violet y aplica el `retorno` con el dia viejo todavia puesto, y recien
    # despues dormir() calcula las rutinas del dia nuevo.
    $ completar_quest_actual("violet", quest_id="violet_amor_05")

    # Y se va a dormir. El autoguardado va justo despues, como en accion_dormir
    # — nunca adentro de dormir(), para que el checkpoint no caiga sobre esa
    # linea (ver la nota de autoguardar_partida en timesystem_core).
    call screen animacion_dormir with dissolve
    $ dormir()
    $ autoguardar_partida()

    window hide
    $ mostrar_hud()
    jump game_loop
