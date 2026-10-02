################################################################################
## Violet — Amor 45 · "La regla de la casa"
################################################################################
##     archivo   violet_amor_45.rpy
##     quest     violet_amor_09          (quests_amor_violet.rpy)
##     label     quest_violet_amor_09    (lo fija el motor: "quest_" + id)
##     esquema   docs/narrativa/mecanica_amor_45.md
##
## DE QUE VA: Monica vuelve de las compras y los tres acomodan en la cocina. El
## comentario de Monica —"se ve que se estan llevando mejor"— es lo que hace que
## Violet formalice la regla: lo suyo no va a ser un asunto de la casa, y lo que
## tengan que hacer lo hacen cuando estan solos. Una linea despues entra Jasmine
## y el mundo se lo demuestra.
##
## LAS FASES (flag `va45_fase`):
##
##   0  esperando el umbral         → trigger de dormir ("despues"): lo despierta
##                                    la bocina del auto
##   1  hay que ir al frente        → trigger de game_loop (llegar a casa_frente)
##   2  terminada
##
## LA FASE 1 CORRE ACOTADA: una restriccion propia (duenio="violet_amor_45") deja
## el camino de su habitacion al frente y congela el reloj. La salida —salir al
## frente— esta siempre disponible: el camino es el de todos los dias.
##
## DOS LOCACIONES, UNA SOLA ESCENA: del frente se pasa a la cocina con un fundido
## a negro (el jugador NO tiene que caminar). `mover_a_locacion` va igual, para
## que el motor sepa donde quedo parado al terminar.
##
################################################################################
## LO QUE FALTA
################################################################################
##
## 1. TRADUCCION AL INGLES de la escena.
##
## 2. NOMBRE Y DESCRIPCION de la quest ("La regla de la casa" / "Lo que hagamos,
##    lo hacemos a solas."), en quests_amor_violet.rpy: se ven en Pistas y son
##    provisorios.
##
## 3. EL HITO quedo POSTERGADO: se decide con la quest de 50 escrita. Hoy la 45
##    no otorga ninguno y el tope del stat queda en 50.
##
## 4. LA ESCENA NO TIENE ELECCION y no deja ningun flag. El esquema preveia una
##    en el tramo de la regla (aceptar su tiempo / empujar) y el `va45_permiso`
##    que la guardaba se saco el 2026-09-28: un flag que nadie elige es deuda
##    invisible. Si vuelve, el lugar natural es "pero yo decia mas cosas".
##
################################################################################


################################################################################
## Estado
################################################################################

# 0 esperando · 1 hay que ir al frente · 2 terminada
default va45_fase = 0

# Del cuarto del MC al frente: el camino de todos los dias, nada mas.
define VA45_CAMINO = ["casa_hmc", "casa_pasilloarriba", "casa_living",
                      "casa_frente"]


init python:

    # ── Estado de la quest ───────────────────────────────────────────────────

    def _va45_lista():
        """
        Viva y en la etapa del disparo.

        NO es `quest_lista_para_boton`, por lo mismo que en la 35 y la 40: ese
        predicado corre la capa 2 entera y acá alcanza con el gate del motor
        (`planificador_trigger_permitido` ya mira los conflictos antes de
        evaluar un trigger con `quest_id=`). El mundo que la escena necesita lo
        arma la propia quest con sus rutinas.
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_09")
        return (_q is not None and _q.activa and not _q.completada
                and _q.etapa_actual == ETAPA_BOTON_LISTO)

    # ── Textos de ETAPA_BOTON_LISTO (los usa quests_amor_violet.rpy) ─────────
    # Funciones de MODULO: quedan guardadas dentro del ConfigEtapa de la quest.

    def _pista_va45_listo():
        if getattr(store, "va45_fase", 0) >= 1:
            return renpy.translate_string("Escuché el auto de Mónica en la entrada.")
        # Antes de dormir no hay nada que hacer: la quest arranca al despertar.
        return renpy.translate_string("Por ahora solo queda descansar")

    def _quehacer_va45_listo():
        if getattr(store, "va45_fase", 0) >= 1:
            return renpy.translate_string("Salir al frente de la casa")
        return _quehacer_amor_violet(45)

    # ── Disparadores ─────────────────────────────────────────────────────────

    def _va45_trigger_dormir():
        """
        Trigger de dormir, fase "despues": la mañana siguiente al umbral.

        OJO: un trigger "despues" que devuelve label saltea los siguientes Y
        `mensajes_al_despertar`. Acá se acepta — la escena arranca apenas abre
        los ojos y el resto del dia sigue normal despues.
        """
        if not _va45_lista() or getattr(store, "va45_fase", 0) != 0:
            return None
        return "violet_amor_45_despertar"

    def _gl_trigger_va45_frente():
        """
        Fase 1: sale al frente y se encuentra a Monica con las compras.

        CEDE ANTE EL REPARTIDOR. El frente por la mañana es exactamente donde y
        cuando entrega (timesystem_core), y dos escenas de paquete encimadas en
        la misma locacion confunden. Si hay repartidor, esta espera a que el
        jugador lo atienda: no se pierde nada, la quest sigue en fase 1.
        """
        if not _va45_lista() or getattr(store, "va45_fase", 0) != 1:
            return None
        if getattr(store, "repartidor_presente", False):
            return None
        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_frente":
            return None
        return "quest_violet_amor_09"


init 5 python:

    registrar_trigger_dormir("violet_amor_45_despertar", "despues",
                             _va45_trigger_dormir, quest_id="violet_amor_09")

    # `duenio`: la quest pone su propia restriccion en la fase 1, asi que su
    # trigger tiene que poder saltar adentro de ella.
    registrar_trigger_game_loop("violet_amor_45_frente", _gl_trigger_va45_frente,
                                duenio="violet_amor_45",
                                quest_id="violet_amor_09")


# Las compras sobre la mesada. Capa full-frame de 1920x1080 con alpha: solo
# pinta las bolsas. Va DEBAJO de los personajes y ENCIMA del fondo sin hacer
# nada — los sprites viven en la capa `personajes` (tinte_horario.rpy) y esta
# imagen, que no lleva prefijo de personaje, se queda en `master` junto al
# fondo. NADA de `zorder`: en master el fondo lo pone `scene` con zorder 0, asi
# que un zorder negativo la mandaria debajo de un fondo opaco.
image amor45_bolsas = "images/quest/violet/amor45/bolsa_cocina.webp"


################################################################################
## 1 · EL DESPERTAR — la bocina del auto
################################################################################

label violet_amor_45_despertar:

    $ ocultar_hud()
    window show

    $ _va45_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va45_bg

    show mc_parado_base c_rbase_base o_arribanm b_none at center with sprite_normal

    piensa "Me pareció escuchar la bocina del auto"
    piensa "Voy a ver qué pasa"

    hide mc_parado_base with dissolve

    # Acotado hasta el frente: el reloj congelado para que la escena no se
    # pierda por avanzar la mañana, y el camino de siempre como unica salida.
    $ activar_restriccion(
        duenio="violet_amor_45",
        congelar_reloj=True,
        locaciones_permitidas=VA45_CAMINO,
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento="Primero voy a ver qué era esa bocina",
        mensaje_accion_default="Primero voy a ver qué era esa bocina",
    )

    $ va45_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · EL FRENTE Y LA COCINA — la escena entera
################################################################################
## Arranca en el frente (lo exige el trigger) y sigue en la cocina tras un
## fundido a negro. Nunca hay mas de tres personajes a la vez: Monica se va
## antes de que entre Jasmine.

label quest_violet_amor_09:

    $ ocultar_hud()
    window show

    $ _va45_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va45_bg

    # Monica ya esta cargada con una bolsa. El cuerpo se declaro para esta
    # escena (visual/sprites_monica.rpy).
    show monica_parada c_rbase_bolsa o_base b_none at right with sprite_normal
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    ## TRAMO 1 — el saludo y la otra bolsa
    show monica_parada b_hablando
    monica "Ah, justo a tiempo"
    show monica_parada b_hablandochica
    monica "En el auto quedó otra bolsa más, ¿me podrías ayudar con eso?"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "Yo me encargo"
    show mc_parado_base b_none

    # Sale por la izquierda y vuelve cargado con la bolsa.
    show mc_parado_base at mc_salir_izquierda
    pause 0.8
    hide mc_parado_base

    show mc_parado_base c_rbase_bolsamadera o_base b_none at mc_entrar_izquierda
    pause 0.8
    show mc_parado_base at mc_izquierda

    show monica_parada b_hablando
    monica "Hay que llevar todo a la cocina"
    show monica_parada b_none

    show mc_parado_base b_hablando
    mc "Está bien, vamos"
    show mc_parado_base b_none

    ## TRAMO 2 — a la cocina. El jugador NO camina: fundido a negro y ya están
    ## adentro, con las compras sobre la mesada.
    scene black with fade
    pause 0.4

    $ sistema_locaciones.mover_a_locacion("casa_cocina", escena=True)

    $ _va45_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va45_bg
    show amor45_bolsas
    with fade

    # Ya dejaron las bolsas: los dos vuelven a su cuerpo base.
    show monica_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with sprite_normal

    show mc_parado_base b_hablando
    mc "¿Quieres que te ayude a guardar las cosas?"
    show mc_parado_base b_none

    show monica_parada b_hablando
    monica "Te lo agradecería"
    show monica_parada b_none

    ## HACIA DONDE MIRA CADA UNO: el MC a la izquierda mirando a la derecha;
    ## Violet en el centro (centro_npc) y la otra (Monica, despues Jasmine) en
    ## `right`, las dos mirando a la izquierda. Violet se gira (centro_npc_flip)
    ## cuando la charla es con la otra, y vuelve a mirar al MC cuando le habla
    ## a el. Son dos personajes ademas del MC: van en center y right, no en las
    ## posiciones de grupo, que son para tres y quedan montadas.

    ## TRAMO 3 — entra Violet y se ofrece ella
    show violet_parada c_rbase_base ca_base o_base b_none at centro_npc with sprite_normal

    show violet_parada b_hablando c_rbase_saludando with sprite_normal
    violet "Buenos días"
    show violet_parada b_hablandochica c_rbase_base with sprite_normal
    violet "¿Qué pasa acá? ¿Hay algo rico?"
    show violet_parada b_none

    # Monica le contesta a Violet: Violet la mira.
    show violet_parada at centro_npc_flip
    show monica_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    monica "Recién llego de hacer las compras"
    show monica_parada b_hablandochica 
    monica "Y ahora nos vamos a poner a ordenar con [mc_name]"
    show monica_parada b_none

    show violet_parada b_hablando c_rbase_idea with sprite_normal
    violet "No te hagas problema, yo lo ayudo con las cosas"
    show violet_parada b_none c_rbase_base with sprite_normal

    ## TRAMO 4 — EL COMENTARIO. Monica no acusa nada: dice lo que ve, se rie, y
    ## se va. Eso solo ya alcanza para que Violet reaccione.
    show monica_parada b_hablando c_rbase_dedolabio with sprite_normal
    monica "Se ve que se están llevando mejor ustedes dos"
    show monica_parada b_hablandochica c_rbase_base with sprite_normal
    monica "Jajaja, bueno, los dejo solos entonces"
    show monica_parada b_none

    hide monica_parada with dissolve

    ## TRAMO 5 — LA REGLA. Se fue Monica: Violet vuelve a mirarlo.
    show violet_parada at centro_npc
    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "Tenemos que tener cuidado con las cosas que hacemos por la casa"
    show violet_parada b_hablandochica
    violet "Y con las que hablamos"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Por qué?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Por el comentario de Mónica"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "No estamos haciendo nada malo"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "De todas maneras, no quiero que lo nuestro sea un asunto de la casa"
    show violet_parada b_hablandochica
    violet "Las cosas las podemos hacer cuando estamos solos"
    show violet_parada b_none c_rbase_base with sprite_normal

    ## TRAMO 5b — LA VUELTA DE TUERCA: la regla deja de ser un limite y pasa a
    ## ser un permiso con condicion. El desanimo del MC va corto y seco: su
    ## registro es la ironia, no la queja.
    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Entonces cuando estamos solos podemos hacer cosas?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "Lo venimos haciendo"
    show violet_parada b_hablandochica o_arribanm 
    violet "¿O te olvidas de los besos?"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Pero yo decía más cosas"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "Te entiendo, pero te pedí que siguieras mis tiempos"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Tengo muchas ganas de dar el siguiente paso"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    ## TRAMO 6 — ENTRA JASMINE. La regla se enuncia y una linea despues el mundo
    ## la demuestra: el jugador la aprende viendola funcionar, no leyendola.
    show jasmine_parada c_rbase_base o_base b_none at right with sprite_normal

    # Jasmine toma la conversacion: Violet se da vuelta a mirarla.
    show violet_parada at centro_npc_flip
    show jasmine_parada b_hablando
    jasmine "Buenas"
    show jasmine_parada b_feliz c_rbase_dedolabio with sprite_normal
    jasmine "¿Qué hacen?"
    show jasmine_parada b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Estábamos por acomodar las compras"
    show violet_parada b_none

    show jasmine_parada b_hablando c_rbase_idea with sprite_normal
    jasmine "¿Ayudo?"
    show jasmine_parada b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "No"
    show violet_parada b_none

    show jasmine_parada b_hablando
    jasmine "Ehhhh bueno... agarro algo y me voy supongo"
    show jasmine_parada b_none

    show jasmine_parada at personaje_salir_izquierda
    pause 1.0
    hide jasmine_parada

    ## TRAMO 7 — el remate: la regla también vale para lo que dicen. Se fue
    ## Jasmine: Violet vuelve a mirarlo.
    show violet_parada at centro_npc
    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "¿Ves? Hasta con lo que decimos en la casa tenemos que tener cuidado"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Está bien, entendí"
    show mc_parado_base b_abiertachica c_rbase_brazoscruzados with sprite_normal
    mc "Mejor nos ponemos a ordenar"
    show mc_parado_base b_none

    hide violet_parada
    hide mc_parado_base
    hide amor45_bolsas
    with dissolve

    ## TRAMO 8 — cierre. ORDEN IMPORTANTE: primero completar y despues avanzar.
    ## completar_quest_actual() RESTAURA LAS RUTINAS, asi que si se avanzara
    ## primero, las tres quedarian un rato con la rutina de la quest puesta en
    ## un horario que la quest no declara.
    $ desactivar_restriccion(duenio="violet_amor_45")
    $ completar_quest_actual("violet", quest_id="violet_amor_09")

    # La mañana se fue en las compras: el MC queda en la cocina, de tarde.
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop
