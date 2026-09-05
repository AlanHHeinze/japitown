################################################################################
## Violet — Deseo 15 · "Anime en estreno"
################################################################################
##     archivo   violet_deseo_15.rpy
##     quest     violet_deseo_03          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_03    (lo fija el motor: "quest_" + id)
##
## DISPARADOR UNICO: la accion "Ver TV" del SOTANO, que existe solo mientras
## esta quest esta lista. Por eso la quest esta excluida del boton generico
## "Buscar un momento a solas" del menu de interaccion.
##
## POR QUE NO HACE FALTA NINGUN FLAG `default`: la quest no tiene fases
## intermedias — se dispara y se cierra en la misma escena. La condicion de la
## accion es directamente `quest_lista_para_boton`, asi que aparece y
## desaparece sola sin que ningun label tenga que prender nada.
##
## DE DIA LA ACCION SE VE PERO AVISA, no se esconde: un boton que no esta (o
## que esta en gris sin explicacion) se lee como un bug. El mismo criterio que
## usan el "Ver TV" del living y las limpiezas de la 04_d5.


################################################################################
## Imagenes
################################################################################
## La pantalla del sotano con el anime en pausa. Es full-frame 1920x1080 CON
## alpha: se apoya sobre el fondo de la locacion, asi que va con un `show`
## pelado (sin `at`) y despues de la `scene`. Lo que se muestre DESPUES queda
## dibujado encima — por eso el MC va a continuacion.

image pantalla_anime_pausa = "images/quest/violet/deseo15/pantalla_anime_pausa.webp"

## Fondo de la imaginacion del MC. Es un fondo completo sin alpha, asi que va en
## JPG (convencion del proyecto) y se usa con `scene`, no con `show`.
image bg_qd15_imaginacion = "images/quest/violet/deseo15/bg_qd15_imaginacion.jpg"


init python:

    def _vd15_ver_tv_quest():
        """La accion del sotano esta puesta por la QUEST."""
        return quest_lista_para_boton("violet_deseo_03")

    def _vd15_ver_tv_ventaja():
        """
        La accion del sotano esta puesta por la VENTAJA del hito de deseo 20.

        Es la vida despues de la quest: la misma accion queda para siempre, pero
        en vez de disparar la escena de cierre tira los dados a ver si Violet se
        engancha (ver violet_ver_anime_suelto).
        """
        return npc_tiene_ventaja("violet", "accion_ver_anime")

    def _vd15_ver_tv_visible():
        """
        Condicion de la AccionLocacion del sotano (actions_catalog).

        Dos dueños posibles, y no se pisan: cuando la quest la tiene puesta
        todavia no existe el hito, y cuando existe el hito la quest ya se
        completo.
        """
        return _vd15_ver_tv_quest() or _vd15_ver_tv_ventaja()


################################################################################
## Router de la accion — decide si se puede ver o todavia no
################################################################################
## Es el `label_generico` de la accion, o sea una SUBRUTINA del executor: si no
## se puede ver, termina en `return` y el executor sigue su curso. Cuando si se
## puede, salta a la escena, que ya es contenido y cierra con jump game_loop.

label violet_deseo_15_ver_tv:

    # La serie se emite de noche. Trasnoche tambien queda afuera: a esa hora ya
    # termino, y ademas la escena necesita a Violet despierta. Vale para los dos
    # dueños de la accion, asi que el chequeo va antes de repartir.
    if horario_actual != 2:
        $ _blk_guardar_toque()
        piensa "Todavía no lo dan, la serie se emite por la noche"
        return

    # Ya no esta la quest: manda la ventaja del hito y se ve igual, con o sin
    # ella. Va antes del jump porque cuando existe el hito la quest ya se cerro.
    if not _vd15_ver_tv_quest():
        jump violet_ver_anime_suelto

    jump quest_violet_deseo_03


################################################################################
## LA VENTAJA "Ver Anime" — vida despues de la quest
################################################################################
## Espejo de violet_jugar_suelto (amor 20): se ve igual siempre, si Violet esta
## disponible tiene la mitad de chances de bajar al sotano, y en los dos casos se
## gasta el horario y la accion queda usada por hoy.
##
## El "una vez por dia" y su mensaje de reintento los resuelve la AccionLocacion
## con reseteo="diario" + mensaje_reintento (ver actions_catalog); acá solo hay
## que marcarla usada.

label violet_ver_anime_suelto:

    # tracker_locacion_npc es la fuente de verdad de "se puede ubicar al NPC":
    # devuelve None si esta fuera de casa o si una restriccion la escondio.
    # Acá alcanza con que este EN LA CASA (baja al sotano), a diferencia de
    # "Jugar", que la necesita en su habitacion con la compu.
    $ _va_disponible = (tracker_locacion_npc("violet") is not None)

    # Si no esta, la accion NO se hace: se avisa y se sale sin gastar el horario
    # ni el uso diario, para que el jugador no pierda la noche.
    #
    # Va ANTES de marcar_usada: el intento fallido no consume nada.
    if not _va_disponible:
        $ _blk_guardar_toque()
        piensa "Violet no está en casa ahora"
        return

    $ sistema_acciones.marcar_usada("vd15_ver_tv_sotano")

    $ _va_se_une = renpy.random.random() < 0.5

    $ ocultar_hud()
    window show

    if _va_se_une:
        $ obtener_npc("violet").modificar_stat2(1)
        piensa "Violet se unió y vimos un par de capítulos juntos"
    else:
        piensa "Ver anime solo no es lo mismo"

    window hide
    $ mostrar_hud()
    $ avanzar_horario()
    jump game_loop


################################################################################
## La escena
################################################################################

label quest_violet_deseo_03:

    $ ocultar_hud()
    window show

    # El sotano de noche: se llega acá desde su propia accion de locacion, asi
    # que la locacion actual ya es la correcta.
    $ _vd15_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd15_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    # =========================================================================
    # CONTENIDO — PARTE A · el MC solo, antes de que ella baje
    # =========================================================================

    piensa "Por qué no se me ocurrió usar el sótano antes para ver anime"
    piensa "Puedo ver en pantalla grande y sin molestar a nadie"

    scene black with fade
    show text Text(renpy.translate_string("Unos minutos mas tarde"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause 2.0
    hide text with dissolve

    scene expression _vd15_bg
    show pantalla_anime_pausa
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with fade

    show violet_parada c_pijama_base ca_pijama o_base b_none at right with sprite_normal

    show violet_parada b_hablando c_pijama_pensando with sprite_normal
    violet "¿Qué estás mirando?"
    show violet_parada b_none c_pijama_base with sprite_normal

    show mc_parado_base b_hablando
    mc "El anime se llama"
    show mc_parado_base b_abiertachica
    mc "Aquella vez que revivi en otro mundo y me di cuenta de que tenía un poder inútil para la vida real pero en este mundo es OP igual a mí no me importa ya que mi sueño es tener una tienda de mascotas llena de waifus"
    show mc_parado_base b_hablando
    mc "Esta es la tercera temporada"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Conozco algo de la serie, no me llama la atención, es bastante rara"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "Yo creo que es de lo más común, un fracasado es atropellado por un camión y tiene que vencer al rey demonio"
    show mc_parado_base b_none o_base c_rbase_base with sprite_normal

    show violet_parada b_hablando c_pijama_brazoscruzados with sprite_normal
    violet "Eso sí es clásico, pero los personajes no tienen sentido"
    show violet_parada b_hablandochica
    violet "Mira el traje que usa ese personaje"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Es Mashika, mi personaje favorito y no voy a mentir, me calienta un poco jajaja"
    show mc_parado_base b_abiertachica c_rbase_brazoscruzados with sprite_normal
    mc "Respecto a su traje, está bien que use algo así, es una maga"
    show mc_parado_base b_none

    show violet_parada b_hablando c_pijama_pensando with sprite_normal
    violet "¿Qué tiene que ver que sea maga con que esté casi desnuda?"
    show violet_parada b_none c_pijama_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_idea with sprite_normal
    mc "La ropa bloquea el flujo de mana del cuerpo"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada c_pijama_rascando1 with sprite_normal
    pause 0.3
    show violet_parada c_pijama_rascando2 with sprite_normal
    pause 0.3

    show violet_parada b_hablando c_pijama_rascando1 with sprite_normal
    violet "¿Qué? ... Es solo una excusa del creador para mostrar su cuerpo"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_señalando with sprite_normal
    mc "Está justificado en el lore en realidad, el primer rey demonio hizo una maldición en la tela para que interrumpa la magia y así evitar ser derrotado"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_pijama_pensando with sprite_normal
    violet "¿No te parece que sigue siendo una excusa?"
    show violet_parada b_none c_pijama_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Mmm... sí puede ser"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada c_pijama_señalando with sprite_normal
    pause 0.5

    show violet_parada b_hablando c_pijama_brazoscruzados with sprite_normal
    violet "Aparte no solo su ropa, su cuerpo también es un poquito exagerado"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Yo creo que se parece bastante a ti físicamente"
    show mc_parado_base b_abiertachica o_base
    mc "Más te miro y más lo creo"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_parada b_hablando
    violet "Ehh no... no soy en nada parecida"
    show violet_parada b_none

    show mc_parado_base b_abiertachica
    mc "Yo creo que sí, hasta podría imaginarlo"
    show mc_parado_base b_none

    scene bg_qd15_imaginacion
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show violet_magica c_base bf_none be_none at right
    with fade

    show violet_magica bf_hablando
    violet "¿Estás listo para ir a enfrentarnos al rey demonio?"
    show violet_magica bf_none

    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "Sí, claramente sería perfecta para el personaje"

    show violet_magica bf_hablando
    violet "Me estás mirando mucho"
    show violet_magica bf_hablandochica
    violet "O estabas pensando en ver mejor mi armadura mágica"
    show violet_magica bf_none

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Sí, mejor quiero ver tu armadura mágica"
    show mc_parado_base b_none

    show violet_magica c_espalda o_espalda bf_none be_sonrisa with sprite_normal
    show violet_magica be_hablando
    violet "¿Se ve bien de atrás?"
    show violet_magica be_sonrisa

    show mc_parado_base b_hablando
    mc "Tu trasero es mucho mejor que el de Mashika, es la versión mejorada"
    show mc_parado_base b_none

    show violet_magica be_hablando
    violet "¿Así que es la versión mejorada? Eso que no lo viste bien todavía"
    show violet_magica be_sonrisa

    show mc_parado_base b_hablando
    mc "Pero me lo puedo imaginar perfectamente"
    show mc_parado_base b_none

    show violet_magica be_hablando
    violet "A ver si es como lo imaginas"

    show violet_magica c_mostrando o_espalda be_sonrisa with sprite_normal
    show violet_magica be_hablando
    violet "¿Algo así?"
    show violet_magica be_sonrisa

    show mc_parado_base b_hablando
    mc "Sí, es exactamente como lo imagino"
    show mc_parado_base b_none

    show violet_magica c_base bf_none be_none o_base at right with sprite_normal

    show violet_magica bf_hablando
    violet "[mc_name], hey, te estoy hablando"
    show violet_magica bf_none

    scene expression _vd15_bg
    show pantalla_anime_pausa
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with fade

    show violet_parada b_hablando c_pijama_brazoscruzados with sprite_normal
    violet "¿Ya volviste a la realidad?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Me tildé pensando en algo, perdón"
    show mc_parado_base b_none

    show violet_parada b_hablando ot_avergonzada
    violet "¿No me digas que estuviste imaginándome con eso puesto?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Emmm no... nunca lo hice y nunca lo volvería a hacer"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "¿Y no es la primera vez?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Prefiero no entrar en detalles"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Supongo que es normal fantasear con personajes de anime, más siendo tan sugerentes"
    show violet_parada b_hablandochica
    violet "¿Pero me tienes que incluir a mí en tus fantasías?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Es que ya te dije que creo que son muy parecidas"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Mejor me voy antes de que me empieces a confundir en la realidad"
    show violet_parada b_hablandochica
    violet "La próxima vez que estés mirando algún anime que no me involucre quizás me sume"
    show violet_parada b_hablando
    violet "Ahora te dejo seguir con tus fantasías"
    show violet_parada b_none

    hide violet_parada with dissolve

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "No es en el único momento que pienso en ella, pero no es necesario que lo sepa"
    piensa "Ahora tengo un nuevo objetivo de vida, que Violet use un cosplay de la armadura mágica"

    hide mc_parado_base
    hide pantalla_anime_pausa
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_deseo_03")

    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop
