################################################################################
## Violet — Amor 50 · "El domingo solos"
################################################################################
##     archivo   violet_amor_50.rpy
##     quest     violet_amor_10          (quests_amor_violet.rpy)
##     label     quest_violet_amor_10    (lo fija el motor: "quest_" + id)
##     esquema   docs/narrativa/mecanica_amor_50.md
##     minijuego minijuego_misionero.rpy (la escena de la cama)
##
## NARRATIVA COMPLETA de punta a punta. Falta el camino de "ya tuvieron sexo
## antes" (ver "LO QUE FALTA").
##
## ES LA ULTIMA QUEST PUBLICADA DE LA RAMA (registrar_fin_de_rama en
## quests_amor_violet.rpy): cuenta para la pantalla de fin de contenido, que
## sale cuando las tres ramas estan terminadas (ui/menus/fin_contenido.rpy). Al
## publicar amor 55, se mueve.
##
## CIERRE DE LA RAMA DE AMOR. Es el domingo en que todas se van menos Violet,
## que se queda a proposito. Paga las quests anteriores: "te dije que me des
## tiempo y que habia que tener cuidado de quien estaba en la casa" junta la
## regla de la 45 con el acuerdo de la 40 (que ella decida cuando).
##
## LAS FASES (flag `va50_fase`):
##
##   0  esperando el domingo            → trigger de dormir ("despues")
##   1  desperto; acotado hasta el      → trigger de game_loop (entrar al living)
##      living (restriccion)
##   5  terminada
##
## LO UNICO JUGABLE ES LA FASE 1. Desde que entra al living hasta la cama es UNA
## escena que no devuelve el control: la despedida, el pasillo de arriba,
## Violet en toalla, la ducha del MC (en negro), la puerta de su habitacion y lo
## que pasa adentro.
##
## Los numeros 2, 3 y 4 no se usan, a proposito. Eran fases jugables que la
## narrativa final absorbio:
##   2  buscar a Violet (golpear su puerta o entrar al baño)
##   3  bañarse con la accion Bañarse, con su habitacion cerrada hasta hacerlo
##   4  ir a su habitacion
## No se renumeran: un save del medio de esta quest tendria un numero que ya
## significaria otra cosa.
##
## Cada fase tiene UN disparador y ninguno existe fuera de su fase.
##
## LAS DUCHAS SON NARRATIVAS: Violet no se mueve al baño en el modelo del motor
## (su rutina la tiene en su habitacion todo el domingo) y el MC se baña en un
## corte a negro. Nada de eso se juega.
##
################################################################################
## LO QUE FALTA
################################################################################
##
## 1. (hecho: la pantalla de fin de contenido; ver la cabecera)
##
## 2. ⚠️ EL CAMINO DE "YA TUVIERON SEXO ANTES" (`violet_tuvo_sexo`, seccion 2,
##    `## TRAMO 7`): hoy no hay forma de llegar —la cama de esta quest es la
##    primera vez—, pero cuando otra quest la prenda, este camino tiene su
##    pensamiento sin escribir. Y probablemente tambien la habitacion.
##
## 3. LAS TRADUCCIONES de todo el dialogo nuevo (quest y minijuego).
##
## 4. EL CALLBACK A AMOR 25. La premisa es la misma (un domingo, las dos se van,
##    Violet se queda). Si no queda DICHO en alguna linea —"la ultima vez que
##    quedamos solos se corto la luz"— se puede leer como que se repitio el
##    recurso. Ni la despedida ni la charla en toalla lo tienen.
##
## 6. ZOWIE Y XGram quedaron abiertos en la 40 y esta quest NO los toca: van a
##    la tanda siguiente.
##
## 7. EL HITO. `violet_hito_amor_05` sigue siendo el marcador "Proximamente" de
##    umbral 50: convertirlo en hito real con quest_id="violet_amor_10" y mover
##    el marcador a 60. El tope provisorio ya quedo en 60.
##
## 8. NOMBRE Y DESCRIPCION de la quest: provisorios, se ven en Pistas.
##
################################################################################


################################################################################
## Estado
################################################################################

# 0 esperando · 1 hasta el living · 5 fin (2, 3 y 4 no se usan: ver cabecera)
default va50_fase = 0

# Fase 1: del cuarto del MC al living, el camino de todos los dias.
define VA50_CAMINO = ["casa_hmc", "casa_pasilloarriba", "casa_living"]

# La escena de despues de la cama: un CG con una boca por personaje. El fondo
# ya los trae con la boca cerrada; la boca abierta se superpone mientras habla.
# Van en master sin prefijo de personaje: un CG no se tiñe por horario.
image amor50_escena = "images/quest/violet/amor50/escena_fondo.jpg"
image amor50_boca_mc = "images/quest/violet/amor50/boca_mc.webp"
image amor50_boca_violet = "images/quest/violet/amor50/boca_violet.webp"

# Una restriccion tiene UN solo mensaje: van las dos frases juntas. Al
# despertar se piensan por separado.
define VA50_MENSAJE_CAMINO = "Hoy las chicas se van a ir, voy a ver si necesitan algo. Seguro están en el living terminando de organizar las cosas"


init python:

    # ── Estado de la quest ───────────────────────────────────────────────────

    def _va50_lista():
        """
        Viva y en la etapa del disparo. NO es `quest_lista_para_boton` (ver la
        35 y la 40): la capa 2 entera pide el mundo tal como lo declaran las
        demandas, y los disparadores de esta quest tienen que seguir existiendo
        durante todo el domingo, sin depender de nada ajeno.
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_10")
        return (_q is not None and _q.activa and not _q.completada
                and _q.etapa_actual == ETAPA_BOTON_LISTO)

    def _va50_viva():
        _q = store.sistema_quests.obtener_quest("violet_amor_10")
        return _q is not None and _q.activa and not _q.completada

    def _va50_fase(n):
        return _va50_lista() and getattr(store, "va50_fase", 0) == n

    # ── Textos de ETAPA_BOTON_LISTO (los usa quests_amor_violet.rpy) ─────────
    # Funciones de MODULO: quedan guardadas dentro del ConfigEtapa de la quest.

    _VA50_PISTAS = {
        0: "Este domingo se van todas a lo de la tía de Violet.",
        1: "Hoy se van las chicas. Seguro están en el living.",
    }
    _VA50_QUEHACER = {
        0: "Esperar al domingo",
        1: "Ir al living a ver si necesitan algo",
    }

    def _pista_va50_listo():
        return renpy.translate_string(
            _VA50_PISTAS.get(getattr(store, "va50_fase", 0), _VA50_PISTAS[0]))

    def _quehacer_va50_listo():
        return renpy.translate_string(
            _VA50_QUEHACER.get(getattr(store, "va50_fase", 0), _VA50_QUEHACER[0]))

    # ── Disparadores ─────────────────────────────────────────────────────────

    def _va50_trigger_dormir():
        """
        Trigger de dormir, fase "despues": amanece el domingo.

        OJO: un trigger "despues" que devuelve label saltea los siguientes Y
        `mensajes_al_despertar`. Acá se acepta — el domingo de esta quest se
        come el resto del dia igual.
        """
        if not _va50_lista() or getattr(store, "va50_fase", 0) != 0:
            return None
        if getattr(store, "dia_semana_actual", 0) != 6:
            return None
        return "violet_amor_50_despertar"

    def _gl_trigger_va50_living():
        """Fase 1: entra al living y las encuentra por irse."""
        if not _va50_fase(1):
            return None
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_living":
            return None
        return "violet_amor_50_despedida"


init 5 python:

    registrar_trigger_dormir("violet_amor_50_domingo", "despues",
                             _va50_trigger_dormir, quest_id="violet_amor_10")

    # `duenio`: la quest pone su propia restriccion en la fase 1, asi que su
    # trigger tiene que poder saltar adentro de ella.
    registrar_trigger_game_loop("violet_amor_50_living", _gl_trigger_va50_living,
                                duenio="violet_amor_50",
                                quest_id="violet_amor_10")


################################################################################
## 1 · EL DESPERTAR — domingo a la mañana
################################################################################
## La quest arranca sola al despertar y lo deja en su habitacion, acotado
## hasta el living: es donde estan Monica y Jasmine terminando de preparar
## todo, y el unico lugar al que tiene que ir.

label violet_amor_50_despertar:

    $ ocultar_hud()
    window show

    $ _va50_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va50_bg

    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    piensa "Hoy las chicas se van a ir, voy a ver si necesitan algo"
    piensa "Seguro están en el living terminando de organizar las cosas"

    hide mc_parado_base with dissolve

    # El reloj congelado para que la despedida no se pierda por avanzar la
    # mañana, y el camino de siempre como unica salida.
    $ activar_restriccion(
        duenio="violet_amor_50",
        congelar_reloj=True,
        locaciones_permitidas=VA50_CAMINO,
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=VA50_MENSAJE_CAMINO,
        mensaje_accion_default=VA50_MENSAJE_CAMINO,
    )

    $ va50_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA DESPEDIDA, VIOLET EN TOALLA Y LA PUERTA — una sola escena
################################################################################
## Arranca en el living (lo exige el trigger) y NO devuelve el control: al
## irse ellas, el MC sube solo al pasillo de arriba con un fundido, y de ahi en
## mas todo sigue de corrido hasta que Violet dice "Adelante" y salta a la
## habitacion (seccion 3).
##
## Monica y Jasmine son PERSONAJES PRESTADOS y aparecen SOLO como sprites de
## escena: sus rutinas las tienen "fuera" todo el domingo (_VIOLET_AMOR_RUTINAS
## [10]) y la planificacion las consume ese dia, asi que ninguna otra quest las
## puede tomar. Por eso no aparecen paradas en el living despues de irse, ni
## siquiera cargando un save en el medio.

label violet_amor_50_despedida:

    $ ocultar_hud()
    window show

    $ _va50_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va50_bg

    # Dos personajes ademas del MC: center y right (las de grupo son para tres).
    #
    # Ya estaban hablando entre ellas cuando el llega: Jasmine mira a Monica
    # (centro_npc_flip). Monica mira a la izquierda, hacia Jasmine y hacia
    # donde entra el MC, asi que no se gira en toda la escena.
    show monica_parada c_rbase_base o_base b_none at right
    show jasmine_parada c_rbase_base o_base b_none at centro_npc_flip
    with sprite_normal

    # El MC entra caminando.
    show mc_parado_base c_rbase_base o_base b_none at mc_entrar_izquierda
    pause 0.8
    show mc_parado_base at mc_izquierda

    ## TRAMO 1 — el control de lo que llevan
    show monica_parada b_hablando
    monica "¿Tienes todo?"
    show monica_parada b_none

    show jasmine_parada b_hablando
    jasmine "Sí, no me olvidé nada"
    show jasmine_parada b_none

    show monica_parada b_hablando
    monica "¿El cargador? No quiero que pase lo de la última vez"
    show monica_parada b_none

    show jasmine_parada b_hablando
    jasmine "Sí, fue lo primero que agarré"
    # Lo saluda a el: se da vuelta.
    show jasmine_parada at centro_npc
    show jasmine_parada b_feliz
    jasmine "Hola [mc_name]"
    show jasmine_parada b_none

    show monica_parada b_hablando
    monica "Buen día [mc_name]"
    show monica_parada b_none

    ## TRAMO 2 — el saludo
    show mc_parado_base b_hablando
    mc "Buen día"
    show mc_parado_base b_abiertachica
    mc "¿Terminando de preparar las cosas para irse?"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Sí, estamos controlando que nadie se olvide nada"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "¿Las ayudo con algo?"
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "Gracias, pero creo que ya tenemos todo listo"
    show jasmine_parada b_none

    ## TRAMO 3 — Violet no va
    show monica_parada b_hablando
    monica "Si te vas a quedar en la casa, fíjate si Violet necesita algo"
    show monica_parada b_hablandochica
    monica "Ayer por la noche me dijo que estaba bastante descompuesta y que no iba a ir"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "¿No va a ir? Se debe sentir súper mal, ama ir a la casa de su tía"
    show mc_parado_base b_none

    show jasmine_parada b_hablando
    jasmine "Eso le pasa por alimentarse a base de comida chatarra"
    show jasmine_parada b_none

    show mc_parado_base b_hablando
    mc "No tenía planes para hoy, me puedo quedar en casa por si necesita algo"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Muchas gracias, me voy más tranquila si es así"
    show monica_parada b_none

    ## TRAMO 4 — se van. Jasmine se lo dice a Monica: la vuelve a mirar.
    show jasmine_parada at centro_npc_flip
    show jasmine_parada b_hablando
    jasmine "Bueno, ¿salimos?"
    show jasmine_parada b_feliz
    jasmine "Así llegamos temprano"
    show jasmine_parada b_none

    # Se dan vuelta y salen por la derecha desde donde estan.
    show monica_parada at salir_derecha_mirando
    show jasmine_parada at salir_derecha_mirando
    pause 1.5
    hide monica_parada
    hide jasmine_parada

    # Ya se fueron: fuera la restriccion. Lo que sigue lo lleva la escena.
    $ desactivar_restriccion(duenio="violet_amor_50")

    piensa "Podría ver si Violet necesita algo y avisarle que voy a estar en la casa"

    ## TRAMO 5 — sube al pasillo de arriba. El jugador NO camina: fundido y ya
    ## esta ahi.
    hide mc_parado_base
    scene black with fade

    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba", escena=True)
    $ _va50_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va50_bg
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with fade

    piensa "Escucho ruido en la ducha. ¿Estará bien?"

    "Knock! Knock! Knock!"

    show mc_parado_base b_hablando
    mc "Violet, ¿estás bien? ¿Necesitas algo?"
    show mc_parado_base b_none

    # Contesta desde adentro del baño: sin sprite.
    violet "Sí, estoy bien, ya salgo"

    ## Corte de tiempo. El cartel espera el CLICK (como en amor 10): es un corte,
    ## no un efecto.
    window hide
    hide mc_parado_base
    scene black with fade
    show text Text(renpy.translate_string("Unos minutos después"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause
    hide text with dissolve

    scene expression _va50_bg
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with fade

    window show

    ## TRAMO 6 — sale en toalla. `violet_toalla` (visual/sprites_violet.rpy)
    ## tiene sus propios ojos y bocas: no mezclar con los de `violet_parada`.
    show violet_toalla c_toalla o_base b_none at right with sprite_normal

    show mc_parado_base b_hablando
    mc "¿Cómo estás?"
    show mc_parado_base b_none

    show violet_toalla b_hablando
    violet "Estoy bien, lo de sentirme mal fue una mentira para no ir"
    show violet_toalla b_none

    show mc_parado_base b_hablando
    mc "¿Pasó algo?"
    show mc_parado_base b_none

    show violet_toalla b_hablando
    violet "Te dije que me des tiempo y que había que tener cuidado de quién estaba en la casa"
    show violet_toalla b_none

    show mc_parado_base b_hablando
    mc "Estoy ligeramente perdido"
    show mc_parado_base b_none

    show violet_toalla b_hablando
    violet "Me di cuenta"
    show violet_toalla b_hablandochica
    violet "Date un baño y ven a mi habitación"
    show violet_toalla b_none

    show violet_toalla at salir_derecha_mirando
    pause 1.5
    hide violet_toalla

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "¿Estará por pasar lo que pienso que está por pasar?"

    ## TRAMO 7 — ¿es la primera vez? `violet_tuvo_sexo` la prende cada escena de
    ## sexo con Violet (definition_violet.rpy). Hoy la unica es la cama de esta
    ## misma quest, asi que siempre se entra por el `else`.
    if violet_tuvo_sexo:
        ## ⚠️ CAMINO SIN ESCRIBIR (LO QUE FALTA, punto 2).
        piensa "ESQUELETO: ya estuvieron juntos antes."
    else:
        piensa "No puedo creer que vaya a llegar el día"
        piensa "Pensé que lo de sus tiempos era solo una excusa para estirarlo"
        piensa "Estoy algo nervioso igual, espero que el baño me despeje un poco"

    ## TRAMO 8 — se baña: corte a negro. El horario NO avanza, la quest se
    ## juega entera en la mañana del domingo.
    window hide
    hide mc_parado_base
    scene black with fade
    show text Text(renpy.translate_string("Un tiempo más tarde"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause
    hide text with dissolve

    scene expression _va50_bg
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with fade

    window show

    ## TRAMO 9 — la puerta de su habitacion. No pasa por el sistema de puertas:
    ## es escena, y ella ya lo invito.
    piensa "Listo, ahora a verla en su habitación"

    "Tock! Tock! Tock!"

    # Contesta desde adentro: sin sprite.
    violet "Adelante"

    jump quest_violet_amor_10


################################################################################
## 3 · LA HABITACION — el cierre de la rama
################################################################################
## Se entra con `jump` desde el final de la seccion 2 ("Adelante"). El nombre
## sigue siendo el que fija el motor ("quest_" + id), aunque ya no lo llama el
## motor sino la escena.
##
## Violet en ropa interior: `violet_ropainterior` (visual/sprites_violet.rpy).
## Sin grupo de ojos —el cuerpo los trae—; bocas y rubor son los de
## `violet_parada`.

label quest_violet_amor_10:

    $ ocultar_hud()
    window show

    $ sistema_locaciones.mover_a_locacion("casa_hviolet", escena=True)
    $ _va50_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    hide mc_parado_base
    scene expression _va50_bg
    show violet_ropainterior c_ropainterior b_none ot_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with fade

    show mc_parado_base b_hablando
    mc "Guau, estás muy sexy con eso, me encanta"
    show mc_parado_base b_none

    # Se pone colorada con el halago y ya no se le va: esta nerviosa toda la
    # escena.
    show violet_ropainterior b_hablando ot_avergonzada
    violet "Gracias..."
    show violet_ropainterior b_none

    show mc_parado_base b_hablando
    mc "Jajaja, no sé qué decir, la verdad estoy algo nervioso"
    show mc_parado_base b_none

    show violet_ropainterior b_hablando
    violet "Estoy igual, pensé tanto en esto y ahora no sé qué decir"
    show violet_ropainterior b_none

    show mc_parado_base b_hablando
    mc "Siempre tan iguales"
    show mc_parado_base b_none

    show violet_ropainterior b_hablando
    violet "Jajaja, la verdad que sí"
    show violet_ropainterior b_hablandochica
    violet "¿Vamos a la cama?"
    show violet_ropainterior b_none

    jump violet_amor_50_cama


################################################################################
## 4 · LA CAMA — el minijuego y el cierre
################################################################################
## El minijuego es una SUBRUTINA: arranca con fundido, termina en negro y
## devuelve el control. Lo que viene despues arranca desde negro: la charla
## sobre el CG, el corte "Mucho sexo mas tarde" y el MC en su habitacion a la
## noche.

label violet_amor_50_cama:

    hide violet_ropainterior
    hide mc_parado_base
    with dissolve

    window hide
    call minijuego_misionero from _call_va50_minijuego

    # Primera vez (o no) para las escenas que vengan: ver definition_violet.rpy.
    # Va apenas termina el minijuego y ANTES de la escena de despues, asi un
    # save en el medio de esa escena ya la tiene puesta.
    $ violet_tuvo_sexo = True

    ## TRAMO 1 — la charla de despues, sobre el CG. Arranca desde negro (asi
    ## termina el minijuego). Cada uno habla con su boca y la baja al terminar.
    scene amor50_escena with fade
    window show

    show amor50_boca_mc
    mc "Eso fue increíble"
    hide amor50_boca_mc

    show amor50_boca_violet
    violet "A mí también me gustó mucho"
    hide amor50_boca_violet

    show amor50_boca_mc
    mc "Ya estoy pensando en repetirlo"
    hide amor50_boca_mc

    show amor50_boca_violet
    violet "Solo cuando no haya nadie en la casa"
    hide amor50_boca_violet

    show amor50_boca_mc
    mc "Ahora no hay nadie"
    hide amor50_boca_mc

    show amor50_boca_violet
    violet "¿En serio?"
    hide amor50_boca_violet

    show amor50_boca_mc
    mc "Sí, hay que aprovechar el momento, no se suelen ir las dos tan seguido"
    hide amor50_boca_mc

    show amor50_boca_violet
    violet "¿Puedes seguir?"
    hide amor50_boca_violet

    show amor50_boca_mc
    mc "¿Lo quieres averiguar?"
    hide amor50_boca_mc

    ## TRAMO 2 — el corte. Se va solo: es un chiste, no un cartel para leer.
    window hide
    scene black with fade
    show text Text(renpy.translate_string("Mucho sexo más tarde"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    with dissolve
    pause 2.5
    hide text with dissolve

    ## TRAMO 3 — la noche, en su habitacion. Pasaron el dia juntos: el horario
    ## avanza hasta la noche (SIEMPRE arranca a la mañana: el reloj estuvo
    ## congelado en la fase 1 y desde ahi todo fue una sola escena). En
    ## silencio, porque la pantalla esta en negro: no hay fondo que repintar.
    python:
        while horario_actual < 2:
            avanzar_horario(silencioso=True)
    $ sistema_locaciones.mover_a_locacion("casa_hmc", escena=True)
    $ _va50_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va50_bg
    show mc_parado_base c_rbase_pensando o_base b_none at center
    with fade

    window show

    piensa "Eso fue increíble, poder estar todo el día solos sin preocuparnos por otra cosa"
    piensa "La próxima vez que se vayan Mónica y Jasmine tengo que aprovechar"
    piensa "Aunque quizás también encuentre alguna forma de hacer que salgan en el futuro"

    hide mc_parado_base with dissolve

    $ va50_fase = 5

    # Al completar, el motor restaura las rutinas: el domingo a la noche Monica
    # y Jasmine ya estan de vuelta en la suya.
    $ completar_quest_actual("violet", quest_id="violet_amor_10")

    # La pantalla de fin de contenido NO va aca: la muestra el game_loop cuando
    # las tres ramas estan completas (ui/menus/fin_contenido.rpy).

    window hide
    $ mostrar_hud()
    jump game_loop
