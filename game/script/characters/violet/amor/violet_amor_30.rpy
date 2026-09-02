################################################################################
## Violet — Amor 30 · "¿Que me pongo?"
################################################################################
##     archivo   violet_amor_30.rpy
##     quest     violet_amor_06          (quests_amor_violet.rpy)
##     label     quest_violet_amor_06    (lo fija el motor: "quest_" + id)
##
## Ultima quest de la linea. DISPARADOR UNICO: un trigger de game_loop — con la
## quest lista, la proxima vez que el MC pase por el pasillo de arriba por la
## TARDE con Violet libre en su habitacion, ella lo llama.
##
## No hay boton ni opcion de puerta: por eso violet_amor_06 esta en la lista
## _VA_SIN_BOTON de interactions_violet.rpy.
##
## LA ESCENA ES UNA SOLA, sin devolver el control en el medio: arranca en el
## pasillo (ella llama de adentro, sin sprite) y sigue adentro de la pieza. El
## jugador no puede irse a hacer otra cosa entre una cosa y la otra, asi que no
## hace falta ninguna restriccion.
##
## USA EL LAYEREDIMAGE `violet_q30a` (visual/sprites_violet.rpy) y no
## `violet_parada`: ese arte trae la cabeza y la cara dibujadas. Dos ropas en el
## mismo grupo `cuerpo` —jeanblanco y jean— y las bocas de frente y de espaldas
## tambien juntas en `boca`.
##
## ⚠️ AL GIRARLA HAY QUE CAMBIAR LA BOCA. Con un cuerpo `_espalda` va `be_*`;
## con los de frente, `bf_*`. Como comparten grupo, dejar una `bf_` sobre un
## cuerpo de espaldas deja la boca flotando en el aire.


init python:

    def _va30_activa():
        return quest_lista_para_boton("violet_amor_06")

    # ── Textos de ETAPA_CONDICIONES ──────────────────────────────────────────

    def _pista_va30_condiciones():
        return renpy.translate_string("Puedo seguir acercandome a Violet.")

    def _quehacer_va30_condiciones():
        return _quehacer_amor_violet(30)

    # ── Disparador ───────────────────────────────────────────────────────────

    def _va30_violet_libre():
        """
        Violet en su habitacion y sin nada encima.

        La locacion ya descarta casi todo (si se baña esta en el baño, si salio
        esta afuera), pero se chequean igual la rutina especial y los bloqueos:
        una rutina de quest puede tenerla en su pieza metida en otra cosa.
        """
        if tracker_locacion_npc("violet") != "casa_hviolet":
            return False

        _v30 = obtener_npc("violet")
        if _v30 is None or _v30.obtener_rutina_especial_actual() is not None:
            return False

        return not npc_esta_oculto("violet") and npc_interactuable("violet")

    def _gl_trigger_violet_amor_30():
        """
        Trigger de game_loop: el MC pasa por el pasillo de arriba y ella lo
        llama desde adentro.

        Las condiciones van de la mas barata a la mas cara: los dos enteros
        primero y las consultas al sistema de NPCs al final.
        """
        if not _va30_activa():
            return None

        if store.horario_actual != 1:          # Tarde
            return None

        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None or _loc.id != "casa_pasilloarriba":
            return None

        if not _va30_violet_libre():
            return None

        return "quest_violet_amor_06"


init 5 python:

    registrar_trigger_game_loop("violet_amor_30_llamado",
                                _gl_trigger_violet_amor_30)


################################################################################
## La escena — cierre de la quest y de la linea
################################################################################

label quest_violet_amor_06:

    $ ocultar_hud()
    window show

    # ── EL PASILLO — lo llama de adentro ─────────────────────────────────────
    # El trigger solo salta estando ahi, asi que la locacion actual ya es la
    # correcta.

    $ _va30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va30_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # Ella habla del otro lado de la puerta: SIN sprite, a proposito.
    violet "[mc_name] ¿Me podes ayudar en algo?"

    show mc_parado_base b_hablando
    mc "Emmmm si ¿Que pasa?"
    show mc_parado_base b_none

    violet "Entra por favor"

    hide mc_parado_base with dissolve

    # ── SU HABITACION — el pantalon blanco ───────────────────────────────────
    # El movimiento es de verdad y no solo un cambio de fondo: el cierre lo
    # devuelve al pasillo, asi que el motor tiene que saber que estuvo adentro.

    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    $ _va30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va30_bg with fade

   
    # (Violet cuerpo jean blanco base boca neutral)
    show violet_q30a c_jeanblanco_base b_none at right
    pause 0.3
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with sprite_normal

    show mc_parado_base b_hablando
    mc "¿Que tengo que hacer?"
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "Necesito que me des una opinion y quiero que seas objetivo"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "¿Sobre que?"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "Sobre mi trasero y el pantalon que me voy a poner"
    show violet_q30a b_hablandochica
    violet "Creo que tu pasatiempo de mirarme el trasero todo el tiempo puede ser util"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Veo que es un tema serio que va a requerir toda mi atencion"
    show mc_parado_base b_abiertachica
    mc "Adelante"
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "Voy a salir por un cumpleaños y estoy entre dos pantalones, no quiero algo muy llamativo"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Va a ser dificil porque caminas con algo llamativo"
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "Dijiste que ibas a ser serio..." 
    show violet_q30a b_hablandochica
    violet "Esta es una de las opciones, lo siento bastante ajustado"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Date vuelta"
    show mc_parado_base b_none

    # Se da vuelta y se toca el pantalon. Va de corrido: cada cuadro entra con
    # sprite_normal y se sostiene medio segundo. Sin boca — no habla mientras.
    show violet_q30a c_jeanblanco_espalda with sprite_normal
    pause 0.5

    show violet_q30a c_jeanblanco_tocando1 with sprite_normal
    pause 0.5

    show violet_q30a c_jeanblanco_tocando2 with sprite_normal
    pause 0.5

    show violet_q30a c_jeanblanco_tocando3 with sprite_normal
    pause 0.5

    show violet_q30a c_jeanblanco_tocando4 with sprite_normal
    pause 0.5

    # Y vuelve a mirarlo.
    show violet_q30a c_jeanblanco_base with sprite_normal
    pause 0.5

    show violet_q30a bf_hablando
    violet "¿Que opinas?"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Es hermoso..."
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "De verdad... necesito colaboracion y me da verguenza preguntarle a Jasmine o a Monica"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Bueno a ver la otra opcion"
    show mc_parado_base b_none

    violet "..."

    show violet_q30a bf_hablando
    violet "Por lo menos date la vuelta"
    show violet_q30a b_none

    # ── A OSCURAS — el MC cierra los ojos ────────────────────────────────────
    # La charla sigue sin nadie en pantalla: se van los dos sprites junto con el
    # fondo, y las lineas se leen sobre negro.

    scene black with fade

    mc "Tengo que admitir que la situacion es bastante exitante"

    violet "No es el momento para eso"

    mc "¿Ya esta?"

    violet "Listo"

    # ── SU HABITACION — el jean ──────────────────────────────────────────────
    # Vuelve a abrir los ojos y ella ya se cambio.

    $ _va30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va30_bg with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo jean base boca neutral)
    show violet_q30a c_jean_base b_none at right
    with sprite_normal

    show violet_q30a bf_hablando
    violet "Este es el otro"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "A ver atras"
    show mc_parado_base b_none

    # Se da vuelta. ACÁ SI HABLA DE ESPALDAS: la boca pasa a `be_*`, que es la
    # que esta dibujada para esa vista.
    show violet_q30a c_jean_espalda with sprite_normal
    pause 0.5

    show violet_q30a be_hablando
    violet "Creo que es mas ajustado"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Si parece un poco mas ajustado"
    show mc_parado_base b_none

    # Se toca el jean.
    show violet_q30a c_jean_tocando1 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_tocando2 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_tocando3 with sprite_normal
    pause 0.5

    show violet_q30a be_hablando
    violet "¿Y?"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Este te marca mas el trasero, pero es menos llamativo que el otro, el blanco se ve a kilometros"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "Entonces me quedo con este"
    show violet_q30a b_hablandochica
    violet "Gracias por ayudarme"
    show violet_q30a b_none

    violet "..."

    show violet_q30a be_hablando
    violet "¿Estas esperando algo?"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Perdon me quede perdido en la imaginacion"
    show mc_parado_base b_none

    show violet_q30a be_sonrisa

    show violet_q30a be_hablando
    violet "¿Tanto te gusta?"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando
    mc "No lo puedo evitar"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "¿Se mira y no se toca?"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando
    mc "Me pedis imposibles"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "¿Eso nada?"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando
    mc "Me voy a controlar"
    show mc_parado_base b_none

    # Y se lo empieza a bajar.
    show violet_q30a c_jean_bajando1 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando2 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando3 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando4 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando5 with sprite_normal
    pause 0.5

    show mc_parado_base b_hablando
    mc "No le puedo creer"
    show mc_parado_base b_hablandochica
    mc "Cuando vuelvas a necesitar ayuda para elegir ropa, llamame"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "Jajajajaja no creo que vuelvas a tener tanta suerte"
    show violet_q30a b_hablandochica
    violet "Bueno se termino la exhibicion, me voy a cambiar y salir"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando
    mc "Pasala bien en el cumpleaños"
    show mc_parado_base b_none

    hide mc_parado_base
    hide violet_q30a
    with dissolve

    # ── EL PASILLO — solo, rumiando ──────────────────────────────────────────

    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    $ _va30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va30_bg with fade

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    piensa "No pude hablar sobre el beso, pero siento que la relacion con Violet esta un poco mas intima, voy por un buen camino"
    piensa "Y lo del cambio de ropa me dejo pensando que podria ser una excusa para otro momento asi, podria pensar en algo que quiera que use o se pruebe"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_06")

    # El horario NO avanza: la escena pasa en un rato.

    window hide
    $ mostrar_hud()
    jump game_loop
