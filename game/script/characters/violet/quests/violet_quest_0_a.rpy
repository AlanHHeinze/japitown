################################################################################
## Quest 0_a de Violet — Violet me ignora
################################################################################
## Primera quest de Violet: romper el hielo y comprender su hambre
## Simula exactamente el sistema Talk original con estado "hambre"

# ── Estado de la quest ──────────────────────────────────────────────────────
# True cuando ya se completó el intro y la quest espera que el jugador use
# "Hablar" con Violet para disparar el sistema talk especial (violet_q0a_talk_sistema).
default violet_q0a_esperando_talk = False

# True una vez completada la quest 0_a: desbloquea el botón "Hablar" del menú de
# interacción de los NPCs (oculto hasta que el jugador aprende a usar el Talk).
default hablar_desbloqueado = False


init python:

    def _pista_quest0a_violet():
        """Pista dinámica de la quest 0_a según el estado del intro."""
        if getattr(store, "violet_q0a_esperando_talk", False):
            return "Tengo que hablar con Violet para romper el hielo"
        return "Tengo que romper el hielo con Violet"

    def _quehacer_quest0a_violet():
        """Texto 'qué hacer' dinámico de la quest 0_a."""
        if getattr(store, "violet_q0a_esperando_talk", False):
            return "Hablar con Violet"
        return "Interactuar con Violet"


################################################################################
## Label principal de la quest
################################################################################

label quest_violet_questprincipal_0_a:
    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # Fondo de la locación actual (habitacion de Violet)
    $ _bg_v0a = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else None
    if _bg_v0a:
        scene expression _bg_v0a with fade

    # Mostrar sprites
    show violet_parada c_rbase_base b_hablandochica at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    # Conversacion inicial
    mc "Hola, Violet, ¿cómo estás?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Hola..."
    show violet_parada b_none
    pause 0.3

    show violet_parada b_hablandochica
    violet "¿Necesitabas algo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Solo quería hablar un momento contigo"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Yo no"
    show violet_parada b_none

    show violet_parada at personaje_salir_izquierda
    pause 1.0
    hide violet_parada with dissolve

    show mc_parado_base c_rbase_pensando o_arribanm
    piensa "Tengo que buscar la manera de romper el hielo y mejorar la relación con ella"
    show mc_parado_base c_rbase_base o_base b_none

    tutorial "Para mejorar la relación con un personaje podremos hacer uso de varios sistemas, uno de ellos es el de Hablar"
    tutorial "Este es un minijuego de opciones que dependerán del estado del personaje (el mismo es aleatorio al inicio de cada día)"
    tutorial "Puedes tratar de recordar las mejores respuestas o ir obteniendo ventajas para este sistema mediante desbloqueos"

    # Marcar que el intro ya se hizo: a partir de ahora "Hablar" con Violet
    # dispara el sistema talk especial (violet_q0a_talk_sistema) en vez del talk común.
    $ violet_q0a_esperando_talk = True

    # La quest queda en ETAPA_BOTON_LISTO (estado de espera estable) para que
    # reaparezca el botón de quest "Hablar" y se use la pista dinámica. (Antes
    # un intentar_ejecutar() la movia a DESARROLLO; ya no existe — el punto de
    # activacion no toca la etapa.)
    $ _q0a_reset = sistema_quests.obtener_quest("violet_questprincipal_0_a")
    if _q0a_reset:
        $ _q0a_reset.etapa_actual = ETAPA_BOTON_LISTO

    # Devolver el control al jugador; la pista cambia a "hablar con Violet".
    # Terminal de contenido: jump game_loop (si el camino hasta aca vino con
    # frames, los drena el inicio del game_loop).
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## Sistema Talk simulado — Estado Hambre
################################################################################

label violet_q0a_talk_sistema:
    $ ocultar_hud()
    window show

    show violet_parada c_rbase_base b_none  at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    tutorial "Algunos estados reciben opciones especiales según objetos, atributos o ventajas que tengamos, las cuales nos darán mejores recompensas"

    # Introducción del estado
    show mc_parado_base c_rbase_pensando
    "Conozco esa cara, no está de buen humor, parece tener hambre"
    show mc_parado_base c_rbase_base
    pause 0.5

    jump violet_q0a_opciones

label violet_q0a_opciones:

    # Mostrar opciones del Talk
    menu:
        "Complacerla (+1 💋)":
            jump violet_q0a_complacer

        "Provocarla (-2 ❤️)":
            jump violet_q0a_provocar

        "Escucharla (Nada)":
            jump violet_q0a_escuchar

        "Hablarle (+2 ❤️)":
            jump violet_q0a_hablar

        "Adularla (Nada)":
            jump violet_q0a_adulación

        "Darle golosinas (+2 ❤️ +1 💋)" if "golosinas" in inventario and inventario.get("golosinas", 0) > 0:
            jump violet_q0a_golosinas


################################################################################
## Opción 1: Complacerla (+1 Deseo)
################################################################################

label violet_q0a_complacer:

    "Podría aprovechar que tengo unas golosinas. Creo que es mi mejor opción"

    jump violet_q0a_opciones


################################################################################
## Opción 2: Provocarla (-2 Amor)
################################################################################

label violet_q0a_provocar:

    "Podría aprovechar que tengo unas golosinas. Creo que es mi mejor opción"

    jump violet_q0a_opciones


################################################################################
## Opción 3: Escucharla (Nada)
################################################################################

label violet_q0a_escuchar:

    "Podría aprovechar que tengo unas golosinas. Creo que es mi mejor opción"

    jump violet_q0a_opciones


################################################################################
## Opción 4: Hablarle (+2 Amor)
################################################################################

label violet_q0a_hablar:

    "Podría aprovechar que tengo unas golosinas. Creo que es mi mejor opción"

    jump violet_q0a_opciones


################################################################################
## Opción 5: Adularla (Nada)
################################################################################

label violet_q0a_adulación:

    "Podría aprovechar que tengo unas golosinas. Creo que es mi mejor opción"

    jump violet_q0a_opciones


################################################################################
## Opción especial: Golosinas (+2 Amor +1 Deseo, continúa quest)
################################################################################

label violet_q0a_golosinas:

    show mc_parado_base b_hablando
    mc "Tengo golosinas. ¿Quieres?"
    show mc_parado_base b_none

    show violet_parada c_rbase_pensando b_hablandochica with sprite_normal
    violet "¿De verdad?"
    show violet_parada c_rbase_base b_none

    show mc_parado_base b_hablando
    mc "Sí, toma"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Gracias..."
    show violet_parada b_none

    # Quitar golosinas del inventario
    $ inventario["golosinas"] = max(0, inventario.get("golosinas", 0) - 1)

    # Recompensa exacta del sistema Talk: +1 Amor + +1 Deseo
    $ obtener_npc("violet").modificar_stat1(1, reserva=True)
    $ obtener_npc("violet").modificar_stat2(1, reserva=True)

    show violet_parada at personaje_salir_izquierda
    pause 1.0
    hide violet_parada with dissolve

    tutorial "En las futuras interacciones no veremos las recompensas asociadas a cada opción"

    # Avanzar tiempo
    $ avanzar_horario()

    # Limpiar el estado de espera del talk especial
    $ violet_q0a_esperando_talk = False

    # Desbloquear el botón "Hablar" del menú de interacción de los NPCs
    $ hablar_desbloqueado = True

    # Completar la quest (auto-inicia la 0_b)
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_0_a")

    window hide
    $ mostrar_hud()
    jump game_loop
