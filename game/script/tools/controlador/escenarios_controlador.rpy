################################################################################
## Dev — Escenarios de prueba del controlador
################################################################################
## Arma el MUNDO un paso antes de un disparador y te devuelve el control en
## game_loop, para ver que hace el controlador con los disparadores reales y
## que muestra la app de Pistas: "Disponible" / "Interrumpida (motivo)", el
## "que hacer" generado, el boton escondido, el reloj frenado.
##
## No toca contenido ni personajes: solo estado, con las mismas funciones que
## usa el motor (etapas de quest, stats, reloj, rutinas, posicion del MC). Las
## quests previas de cada cadena se marcan completadas SIN correr sus labels,
## asi que no dejan recuerdos ni chats; si un escenario necesita un flag de
## una quest anterior, lo pone a mano y lo dice.
##
## USO (consola, Shift+O, con config.developer):
##     jp_escenario()                     -> lista los escenarios
##     jp_escenario("interrumpida_09a")   -> arma el escenario y salta a game_loop
##     jp_escenario("limpiar")            -> restriccion, reservas y flags a cero
## O desde el menu de cheats: "Escenarios del controlador".
##
## Corre los escenarios en una partida DESCARTABLE: reescriben el estado de las
## quests de las lineas que usan. El panel en vivo (jp_panel_controlador) vive
## aparte, en panel_controlador.rpy.

init python:

    import collections as _esc_collections

    # ── Primitivas de setup ──────────────────────────────────────────────────

    def _esc_q(qid):
        q = store.sistema_quests.obtener_quest(qid)
        if q is None:
            raise ValueError("escenario: la quest %r no existe" % (qid,))
        return q

    def _esc_marcar_completada(qid):
        """Completada por atajo: sin labels, sin recuerdos, sin chats."""
        q = _esc_q(qid)
        q.resetear()
        q.activa = False
        q.completada = True
        q.etapa_actual = ETAPA_FINALIZACION

    def _esc_completar_cadena(qid):
        """Marca completadas TODAS las predecesoras de `qid` (no a `qid`)."""
        vistos = set()
        ant = _esc_q(qid).quest_anterior
        while ant and ant not in vistos:
            vistos.add(ant)
            _esc_marcar_completada(ant)
            ant = _esc_q(ant).quest_anterior

    def _esc_resetear_lineas(npc_id, lineas=("principal", "amor", "deseo")):
        """Todas las quests del NPC en esas lineas vuelven a 'no iniciada'."""
        for q in store.sistema_quests.quests.values():
            if q.npc_id == npc_id and getattr(q, "linea", "principal") in lineas:
                q.resetear()

    def _esc_dejar_lista(qid, dias_atras=None):
        """
        Deja `qid` activa y la hace avanzar POR EL MOTOR (espera, requisitos,
        capa 1, rutina). Backdatea dia_inicio para que la espera ya haya
        pasado. Si la capa 1 la frena queda en CONDICIONES: eso tambien es
        un resultado.
        """
        _esc_completar_cadena(qid)
        q = _esc_q(qid)
        q.resetear()
        q.activa = True
        q.etapa_actual = ETAPA_INICIALIZACION
        _atras = q.dias_espera if dias_atras is None else dias_atras
        q.dia_inicio = getattr(store, "dias_totales", 1) - _atras
        q._procesar_avance_etapas()
        return q

    def _esc_reloj(dias_totales, dia_semana, horario):
        store.dias_totales = dias_totales
        store.dia_semana_actual = dia_semana
        store.horario_actual = horario
        try:
            actualizar_rutinas_npcs()
        except Exception as e:
            print("[escenario] actualizar_rutinas_npcs: %r" % (e,))
        try:
            actualizar_bg_master()
        except Exception as e:
            print("[escenario] actualizar_bg_master: %r" % (e,))

    def _esc_stats(npc_id, amor=None, deseo=None):
        n = obtener_npc(npc_id)
        if amor is not None:
            n.establecer_stat1(amor)
        if deseo is not None:
            n.establecer_stat2(deseo)

    def _esc_mc(loc_id):
        store.sistema_locaciones.mover_a_locacion(loc_id)

    def _esc_npc_a(npc_id, loc_id):
        """Mueve un NPC a mano ("fuera" incluido). Dura hasta el proximo cambio de horario."""
        n = obtener_npc(npc_id)
        if n is not None:
            n.locacion_actual = loc_id

    def _esc_limpiar():
        """Sin restriccion, sin reservas, flags de los escenarios a cero."""
        desactivar_restriccion(duenio="*")
        store.planificador_reservas = []
        store.vd25_fase = 0
        store.vd30_fase = 0
        store.vd30_dias_ignorada = 0
        store.va25_fase = 0
        store.violet_9a_piensa_mostrado = False
        store.violet_9a_enfermedad_dia = 0
        store.violet_enferma_atencion = 0
        store.violet_9a_pedido_actual = None
        for _n in ("violet", "monica", "jasmine"):
            try:
                marcar_npc_disponible(_n)
            except Exception:
                pass

    def _esc_09a_en_curso():
        """
        Violet enferma, dia 1, ya arrancada (flags que pondria
        violet_quest09a_inicio). Activarla toma las reservas de vida de
        Violet y Monica.
        """
        q = _esc_dejar_lista("violet_questprincipal_09_a")
        store.violet_9a_piensa_mostrado = True
        store.violet_9a_enfermedad_dia = 1
        activar_quest("violet_questprincipal_09_a", origen="escenario")
        return q

    # ── Los escenarios ───────────────────────────────────────────────────────
    # nombre -> (titulo, que_ver, funcion). `que_ver` se imprime al armarlo.

    def _esc_disponible():
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=5, deseo=5)
        _esc_reloj(20, 1, 0)                       # martes, mañana
        _esc_dejar_lista("violet_amor_01")         # ¿Mejor?: puerta "Llamarla", tarde, Violet adentro
        _esc_dejar_lista("violet_deseo_01")        # Atraccion: pasillo de arriba, tarde
        _esc_mc("casa_hmc")

    def _esc_interrumpida_09a():
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=20, deseo=15)
        _esc_reloj(20, 1, 1)                       # martes, tarde
        _esc_09a_en_curso()
        _esc_dejar_lista("violet_amor_04")         # Jugando juntos
        _esc_dejar_lista("violet_deseo_03")        # Anime en estreno
        _esc_dejar_lista("jasmine_questprincipal_0_c")   # El regalo (Jasmine no esta reservada)
        _esc_mc("casa_pasilloarriba")

    def _esc_interrumpida_fuera():
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=15, deseo=5)
        _esc_reloj(20, 1, 1)                       # martes, tarde
        _esc_dejar_lista("violet_amor_03")         # La visita: pide a Violet EN LA CASA
        _esc_dejar_lista("violet_deseo_01")        # Atraccion: idem
        _esc_npc_a("violet", "fuera")
        _esc_mc("casa_living")

    def _esc_interrumpida_reserva():
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=5, deseo=25)
        _esc_reloj(20, 1, 2)                       # martes, noche
        _esc_dejar_lista("violet_deseo_05")        # En su habitacion: la que va a reservar
        _esc_dejar_lista("violet_amor_01")         # ¿Mejor?: queda interrumpida por la reserva
        _esc_reloj(20, 1, 2)
        _esc_mc("casa_sotano")

    def _esc_interrumpida_secuencia():
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=9, deseo=30)     # amor 9: a la 10 le falta UN punto
        _esc_reloj(20, 1, 2)                       # martes, noche
        _esc_dejar_lista("violet_deseo_06")        # Sinceridad: arranca sola en tu pieza y congela el reloj
        _esc_dejar_lista("violet_amor_02")         # Buena relacion: espera el punto de amor
        _esc_reloj(20, 1, 2)
        _esc_mc("casa_pasilloarriba")

    def _esc_amor25_sabado():
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=25, deseo=10)
        _esc_reloj(19, 5, 2)                       # sabado, noche
        _esc_dejar_lista("violet_amor_05")         # Solos en casa: CONDICIONES hasta el domingo
        _esc_mc("casa_hmc")

    def _esc_fin_expansion_anterior():
        """
        Como termina la partida de alguien que jugo todo lo de la version
        anterior (0.1.9): la historia principal y la rama de deseo completas,
        y la de amor completa hasta 30. Amor 35 queda viva esperando su
        umbral, como la encontraria ese jugador al actualizar.
        """
        _esc_limpiar()
        _esc_resetear_lineas("violet")
        _esc_stats("violet", amor=30, deseo=30)
        _esc_reloj(40, 0, 0)                       # lunes, mañana

        # Principal: hasta la 09 (Violet enferma) inclusive.
        _esc_completar_cadena("violet_questprincipal_09_a")
        _esc_marcar_completada("violet_questprincipal_09_a")

        # Deseo: hasta la 07 ("Distancia", el cierre de deseo 30) inclusive.
        _esc_completar_cadena("violet_deseo_07")
        _esc_marcar_completada("violet_deseo_07")

        # Amor: completa hasta la 06 (amor 30) y deja viva la 07 (amor 35),
        # que con amor 30 se queda en CONDICIONES esperando el punto 35.
        _esc_dejar_lista("violet_amor_07")

        # Las fases de las quests con escena de varias partes, en su ultimo
        # valor (_esc_limpiar las deja en 0). Asi ningun trigger de migracion
        # las confunde con una partida a medias.
        store.va25_fase = 5
        store.vd30_fase = 3
        store.vq9b_rama = "cerrado"

        _esc_mc("casa_hmc")

    ESCENARIOS_CONTROLADOR = _esc_collections.OrderedDict([
        ("disponible", (
            "Disponible: dos quests listas, solo falta ir",
            "Martes a la mañana, MC en su pieza. Amor 5 (puerta, tarde) y Deseo 5 (pasillo, tarde) listas.\n"
            "- Pistas > +: las dos en verde 'Disponible' aunque no sea la hora: solo falta esperar/ir.\n"
            "- El 'que hacer' dice opcion, lugar y hora: 'Usar la opcion Llamarla en la puerta de Violet mientras este adentro por la tarde'.",
            _esc_disponible)),
        ("interrumpida_09a", (
            "Interrumpida por otra quest (Violet enferma reserva a Violet y Monica)",
            "Violet enferma en curso. Amor 20 y Deseo 15 listas; El regalo de Jasmine tambien.\n"
            "- Pistas > +: Amor 20 y Deseo 15 en rojo 'Interrumpida (Terminar Violet enferma primero)'; Jasmine en verde.\n"
            "- Sotano: 'Ver TV' de Deseo 15 NO aparece. Menu de Monica: solo 'Preguntar por Violet'.\n"
            "- Completar la 09_a desde Dev > Completar Quests: vuelven a verde.",
            _esc_interrumpida_09a)),
        ("interrumpida_fuera", (
            "Interrumpida porque Violet no esta en la casa",
            "Tarde, Violet AFUERA (movida a mano). Amor 15 y Deseo 5 piden a Violet en la casa.\n"
            "- Pistas > +: las dos en rojo 'Interrumpida (Violet no esta en la casa)'.\n"
            "- Avanza el horario: la rutina la trae de vuelta y pasan a verde.",
            _esc_interrumpida_fuera)),
        ("interrumpida_reserva", (
            "Interrumpida por una reserva (Deseo 25 toma la noche)",
            "Noche, MC en el sotano, Deseo 25 lista, Amor 5 lista.\n"
            "- Hace 'Ver TV': Deseo 25 reserva a Violet esta noche.\n"
            "- Pistas > +: Amor 5 en rojo 'Interrumpida (Le dije a Violet que iba esta noche)'.\n"
            "- Dormir / avanzar: frenados con el mismo texto. Menu de Violet sin ventajas.",
            _esc_interrumpida_reserva)),
        ("interrumpida_secuencia", (
            "Interrumpida por una secuencia en curso (reloj congelado)",
            "Noche, Deseo 30 (Sinceridad) lista: arranca sola al entrar a tu pieza y congela el reloj.\n"
            "- Entra a tu habitacion. En el pasillo, consola: obtener_npc('violet').modificar_stat1(1)\n"
            "- Amor 10 quiere nacer y no puede: Pistas dice 'Terminar lo que esta pasando primero'.\n"
            "- Entra a la pieza de Violet y termina la charla: Amor 10 nace.",
            _esc_interrumpida_secuencia)),
        ("amor25_sabado", (
            "De corrido: Amor 25 arranca solo el domingo",
            "Sabado a la noche, Amor 25 esperando el domingo. Dormi y arranca sola.",
            _esc_amor25_sabado)),
        ("fin_expansion_anterior", (
            "Fin de la version anterior: principal y deseo completas, amor en 30",
            "Lunes a la mañana, MC en su pieza. Violet con amor 30 y deseo 30.\n"
            "- Principal (hasta Violet enferma) y Deseo (hasta deseo 30) completas: los hitos se otorgan solos en esta vuelta.\n"
            "- Amor completa hasta 30. Amor 35 viva, esperando el punto 35: subilo (talk o cheats de stats) para que arranque.\n"
            "- Al terminar amor 50 (las tres ramas completas) sale la pantalla de fin de contenido.",
            _esc_fin_expansion_anterior)),
        ("limpiar", (
            "Limpiar: sin restriccion, sin reservas, flags a cero",
            "Deja la partida sin restriccion activa ni reservas. No toca las quests.",
            _esc_limpiar)),
    ])

    def jp_escenario(nombre=None):
        """Sin argumento lista; con nombre arma el escenario y salta a game_loop."""
        if not config.developer:
            return
        if nombre is None:
            for k, (titulo, _qv, _fn) in ESCENARIOS_CONTROLADOR.items():
                print("  %-24s %s" % (k, titulo))
            return
        if nombre not in ESCENARIOS_CONTROLADOR:
            print("escenario %r no existe. Disponibles: %s" % (nombre, ", ".join(ESCENARIOS_CONTROLADOR)))
            return
        store._jp_escenario_pendiente = nombre
        renpy.jump("jp_escenario_correr")

    def _jp_escenario_armar(nombre):
        titulo, que_ver, fn = ESCENARIOS_CONTROLADOR[nombre]
        fn()
        try:
            actualizar_quests()
        except Exception as e:
            print("[escenario] actualizar_quests: %r" % (e,))
        print("=" * 70)
        print("ESCENARIO %s — %s" % (nombre, titulo))
        print("dia %s, %s, horario %s | MC en %s" % (
            store.dias_totales, store.dia_semana_actual, store.horario_actual,
            store.sistema_locaciones.locacion_actual.id if store.sistema_locaciones.locacion_actual else "?"))
        print(que_ver)
        print("-" * 70)
        print(planificador_estado())
        print("=" * 70)


label jp_escenario_correr:
    $ renpy.hide_screen("menu_cheats")
    $ renpy.hide_screen("escenarios_controlador")
    $ renpy.hide_screen("lista_contactos_mensajes")
    $ renpy.hide_screen("menu_celular")
    $ menu_celular_abierto = False
    $ desactivar_restriccion(duenio="*")
    $ _jp_escenario_armar(_jp_escenario_pendiente)
    jump game_loop


default _jp_escenario_pendiente = "limpiar"


screen escenarios_controlador():
    zorder 290
    modal True

    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        background "#00000066"
        action Hide("escenarios_controlador")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        background "#0d0d1eFF"
        padding (20, 16)

        vbox:
            xfill True
            spacing 8

            hbox:
                xfill True
                text "Dev — Escenarios del controlador" size 20 color "#4FC3F7" bold True xfill True
                textbutton "Cerrar" action Hide("escenarios_controlador")

            text "Reescriben el estado de las quests de Violet: usar en una partida descartable. Lo que hay que ver sale en consola." size 13 color "#aaaaaa"

            for _nombre in ESCENARIOS_CONTROLADOR:
                $ _titulo = ESCENARIOS_CONTROLADOR[_nombre][0]
                button:
                    xfill True
                    background "#1a1a3aCC"
                    hover_background "#2a2a5aCC"
                    padding (12, 8)
                    action [SetVariable("_jp_escenario_pendiente", _nombre),
                            Hide("escenarios_controlador"),
                            Hide("menu_cheats"),
                            Jump("jp_escenario_correr")]
                    hbox:
                        spacing 12
                        text _nombre size 14 color "#FFD54F" bold True xsize 230
                        text _titulo size 14 color "#ffffff"
