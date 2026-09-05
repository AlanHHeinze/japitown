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
    violet "[mc_name], ¿me puedes ayudar en algo?"

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Emmmm sí, ¿qué pasa?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    violet "Entra por favor"

    hide mc_parado_base with dissolve

    # ── SU HABITACION — el pantalon blanco ───────────────────────────────────
    # El movimiento es de verdad y no solo un cambio de fondo: el cierre lo
    # devuelve al pasillo, asi que el motor tiene que saber que estuvo adentro.

    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    $ _va30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va30_bg with fade


    # ENTRAN ESCALONADOS: primero ella, que ya estaba adentro, y despues el MC.
    #
    # Cada uno lleva SU PROPIO `with`. El `pause` de por medio es una
    # interaccion, asi que corta lo pendiente: sin el `with` en la linea de
    # Violet, ella aparecia de golpe y el sprite_normal terminaba siendo solo
    # del MC.
    #
    # El pause es 0.5 porque sprite_normal es un Dissolve(0.5) (options.rpy):
    # asi el fundido de ella alcanza a terminar justo antes de que el entre.

    # (Violet cuerpo jean blanco base boca neutral)
    show violet_q30a c_jeanblanco_base b_none at right with sprite_normal
    pause 0.5
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Qué tengo que hacer?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_q30a bf_hablando
    violet "Necesito que me des una opinión y quiero que seas objetivo"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "¿Sobre qué?"
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "Sobre mi trasero y el pantalón que me voy a poner"
    show violet_q30a bf_hablandochica
    violet "Creo que tu pasatiempo de mirarme el trasero todo el tiempo puede ser útil"
    show violet_q30a b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Veo que es un tema serio que va a requerir toda mi atención"
    show mc_parado_base b_abiertachica c_rbase_brazoscruzados with sprite_normal
    mc "Adelante"
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "Voy a salir por un cumpleaños y estoy entre dos pantalones, no quiero algo muy llamativo"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Va a ser difícil porque caminas con algo llamativo"
    show mc_parado_base b_none

    show violet_q30a bf_hablando
    violet "Dijiste que ibas a ser serio..."
    show violet_q30a bf_hablandochica
    violet "Esta es una de las opciones, lo siento bastante ajustado"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Lo estoy siendo..."
    show mc_parado_base b_abiertachica c_rbase_idea with sprite_normal
    mc "Date vuelta"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    piensa "Siempre quise decir eso"

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
    violet "¿Qué opinas?"
    show violet_q30a b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Es hermoso..."
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_q30a bf_hablando
    violet "De verdad... necesito colaboración y me da vergüenza preguntarle a Jasmine o a Mónica"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Insisto, estoy siendo serio y objetivo"
    show mc_parado_base b_abiertachica c_rbase_pensando with sprite_normal
    mc "Bueno, a ver la otra opción"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    violet "..."

    show violet_q30a bf_hablando
    violet "Por lo menos date la vuelta"
    show violet_q30a b_none

    # ── A OSCURAS — el MC cierra los ojos ────────────────────────────────────
    # La charla sigue sin nadie en pantalla: se van los dos sprites junto con el
    # fondo, y las lineas se leen sobre negro.

    scene black with fade

    mc "Tengo que admitir que la situación es bastante excitante"

    violet "No es el momento para eso"

    mc "Soy una persona muy imaginativa"

    violet "Sí, eso ya lo sé"

    mc "¿De qué color es?"

    violet "¿De verdad...?"

    mc "Bueno, tenía esa duda"

    violet "Listo, ya puedes abrir los ojos"

    # ── SU HABITACION — el jean ──────────────────────────────────────────────
    # Vuelve a abrir los ojos y ella ya se cambio.

    $ _va30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va30_bg with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo jean base boca neutral)
    #
    show violet_q30a c_jean_base b_none at right
    with sprite_normal

    show violet_q30a bf_hablando
    violet "Este es el otro"
    show violet_q30a b_none

    show mc_parado_base b_hablando
    mc "Sexy"
    show mc_parado_base b_abiertachica c_rbase_pensando with sprite_normal
    mc "A ver atrás"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    # Se da vuelta. ACÁ SI HABLA DE ESPALDAS: la boca pasa a `be_*`, que es la
    # que esta dibujada para esa vista.
    #
    # Y ACÁ ENTRA EL ESPEJADO, junto con el giro: el `at right_flip` va en el
    # mismo `show` que la espalda, asi el cambio de vista y el espejo pasan en
    # el mismo frame en vez de verse como dos movimientos.
    #
    # Se queda para el resto de la quest: los `show violet_q30a ...` que siguen
    # no llevan `at` y Ren'Py le conserva el transform al tag. No hay ningun
    # `at` posterior — el siguiente toque a este tag es el `hide` del cierre.
    show violet_q30a c_jean_espalda at right_flip with sprite_normal
    pause 0.5

    show violet_q30a be_hablando
    violet "Creo que es más ajustado"
    show violet_q30a b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Sí, parece un poco más ajustado, te lo hace más redondo que el blanco"
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

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Si bien este te marca más el trasero, es menos llamativo que el otro"
    show mc_parado_base b_abiertachica
    mc "El blanco se ve a kilómetros"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_q30a be_hablando
    violet "Entonces me quedo con este"
    show violet_q30a be_hablandochica
    violet "Gracias por ayudarme"
    show violet_q30a b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "De nada, cuando quieras probarte pantalones puedes contar conmigo"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_q30a be_hablando
    violet "Me imaginé que no ibas a tener problemas en ayudarme con esto"
    show violet_q30a b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Listo?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_q30a be_hablando
    violet "¿Estabas esperando algo más?"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Mmmm... ¿No te tienes que probar otro?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_q30a be_hablando
    violet "No, estaba entre esos dos"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿No tienes dudas con la ropa interior que vas a llevar?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_q30a be_hablando
    violet "Jajajaja no"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Lo intenté"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_q30a be_hablando
    violet "¿Tantas ganas tienes de verla?"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Cerrar los ojos mientras te cambiabas fue una situación letal"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "¿Se mira y no se toca?"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando
    mc "Me pides imposibles"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "Eso o nada"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Acepto el trato, solo miro"
    show mc_parado_base b_none

    # Y se lo empieza a bajar.
    show violet_q30a c_jean_bajando1 with sprite_normal
    pause 0.5
    show violet_q30a c_jean_bajando2 with sprite_normal
    pause 0.5

    show violet_q30a be_hablando
    violet "Listo, ya sabes el color"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_facepalm with sprite_normal
    mc "No me puedes poner el to be continue justo ahora"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_q30a be_hablando
    violet "Jajajajaja, dale las gracias a ese comentario"
    show violet_q30a be_sonrisa

    show mc_parado_base c_rbase_victoria with sprite_normal
    pause 0.5
    show mc_parado_base c_rbase_base with sprite_normal

    show violet_q30a c_jean_bajando3 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando4 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando5 with sprite_normal
    pause 0.5

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "Es todo lo que está bien en este mundo"
    show mc_parado_base b_abiertachica
    mc "Muero de ganas de darle un besito"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_q30a be_hablando
    violet "Aceptaste los términos de no tocar"
    show violet_q30a be_sonrisa

    show violet_q30a c_jean_bajando2 with sprite_normal
    pause 0.5
    show violet_q30a c_jean_bajando1 with sprite_normal
    pause 0.5

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Sí, me voy antes de que me vuelva peligroso jajaja"
    show mc_parado_base b_none

    show violet_q30a be_hablando
    violet "Eres bastante peligroso, mira lo que me hiciste hacer..."
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Sé que te gusta volverme loco, no fue solo algo mío"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_q30a be_hablando
    violet "Bueno, terminó la exhibición que se me hace tarde"
    show violet_q30a be_hablandochica
    violet "Nos vemos después"
    show violet_q30a be_sonrisa

    show mc_parado_base b_hablando
    mc "Nos vemos después"
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

    show mc_parado_base c_rbase_avergonzado with sprite_normal
    piensa "Su trasero hizo olvidarme por completo que quería hablar con ella y ver cómo había repercutido lo del beso"
    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "Aunque creo que no hace falta hablar nada"
    piensa "Espero que me vuelva a pedir ayuda con la ropa en algún momento"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_06")

    # El horario NO avanza: la escena pasa en un rato.

    window hide
    $ mostrar_hud()
    jump game_loop
