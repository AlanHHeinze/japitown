################################################################################
## Planificador de contenido — control y validacion de quests
################################################################################
## Diseño completo en docs/arquitectura/planificador.md. Resumen operativo:
##
## Cada quest declara (planificacion_<npc>.rpy, via declarar_planificacion):
##   - de_corrido  : su narrativa fija un momento y las demas la respetan
##   - demandas    : lo que necesita LIBRE para poder jugarse   (lista de Rec)
##   - consumos    : lo que TOMA del mundo mientras esta viva   (lista de Rec)
##   - duenio      : el id que usa en activar_restriccion(duenio=...), para que
##                   el planificador no la mida contra su propia restriccion
##
## Y el motor decide en dos momentos:
##
##   CAPA 1 — NACER  (Quest._procesar_avance_etapas, CONDICIONES → RUTINA)
##     puede_nacer(): ¿mis consumos le pisan una demanda a una quest activa
##     DE CORRIDO? Si → espero (FIFO). ¿Hay una secuencia en curso (restriccion
##     ajena con congelar_reloj)? Si → espero. Si no, nazco y aplico mi rutina.
##
##   CAPA 2 — ACTIVAR  (quest_lista_para_boton, el predicado de todo disparador)
##     puede_activarse(): ¿hay una reserva ajena sobre mi NPC ahora? ¿los
##     consumos declarados de otra activa, o los vivos de la restriccion
##     activa, me cubren una demanda? ¿el mundo esta como necesito (NPC donde
##     hace falta, disponible, celular libre)? Cualquier "no" esconde el
##     disparador; los "no" por conflicto ademas escriben el "que hacer".
##     Una quest ya en narrativa (activar_quest) no se vuelve a medir: la
##     protegen los dueños de restriccion.
##
##   RESERVA  (activar_quest de una de corrido con Rec("npc", ..., reserva=))
##     Dos formas:
##       reserva=True    → un SLOT (npc, dia, horario): "vení esta noche".
##                         Vence al pasar el slot. Ademas congela el reloj
##                         (ACCIONES_RELOJ bloqueadas): la salida es la quest.
##       reserva="vida"  → el NPC ES DE ESTA QUEST hasta que se complete:
##                         "esta enferma", "se queda cuidandola". El reloj
##                         corre; vence al completar.
##     Mientras una reserva rige, el NPC solo ofrece las interacciones de la
##     quest que lo reservo: en su menu quedan las opciones cuyo quest_id es
##     esa quest y nada mas (ni Hablar, ni eventos, ni ventajas); en su
##     puerta, idem, y golpear no responde. Ninguna otra quest DEL NPC ni que
##     lo demande se activa (capa 2) — sus disparadores se esconden, aunque
##     no pasen por su menu (una accion, una locacion) — y las que esperan lo
##     dicen en su "que hacer".
##
##   AUTODISPAROS  (triggers registrados con quest_id=)
##     _ejecutar_triggers no evalua un trigger cuya quest no esta viva o esta
##     bloqueada por conflicto (capa 2 sin la parte momentanea). Asi la capa 2
##     alcanza a los disparos automaticos sin depender de cada funcion.
##
## REGLA ANTI-RECURSION: nada de aca llama a accion_bloqueada() ni a
## quest_lista_para_boton(): los bloqueos registrados por contenido las
## llaman a ellas, y el ciclo seria inmediato. La restriccion activa se lee
## directo.

init python:

    import copy as _pl_copy

    # Efecto 3 de la reserva: durante el slot reservado no corre el reloj
    # (ACCIONES_RELOJ bloqueadas). Se puede apagar sin tocar nada mas.
    PLANIFICADOR_RESERVA_CONGELA_RELOJ = True

    # ==========================================================================
    # Rec — un recurso declarado
    # ==========================================================================

    REC_TIPOS = ("npc", "interaccion", "puerta", "locacion", "locaciones",
                 "reloj", "accion", "celular", "mensajes", "mc")

    # Atributos de estado de un Rec "npc". Dos Rec npc se pisan si comparten
    # NPC y slot y ALGUNO de estos lo especifican los dos con valores distintos.
    _REC_ATRIBUTOS_NPC = ("en", "skin", "animo", "disponible")

    class Rec(object):
        """
        Recurso declarado por una quest. Datos puros (picklable): vive dentro
        del Quest, que se guarda.

            Rec("npc", "violet", horario=2, en="casa_hviolet", reserva=True)
            Rec("interaccion", "violet")            # el menu entero
            Rec("interaccion", "violet", accion="jugar")
            Rec("puerta", "violet")
            Rec("locacion", en="casa_cocina")       # demanda: una locacion
            Rec("locaciones", locaciones=[...])     # consumo: la whitelist
            Rec("reloj")
            Rec("accion", accion="cocinar")
            Rec("celular") / Rec("mensajes")
            Rec("mc", dia=4, horario=2, reserva=True)   # la noche es de esta quest

        `mc` NO es `Rec("npc", "mc")`: el MC no esta en `sistema_npcs`, asi que
        no tiene locacion consultable con obtener_npc, ni disponibilidad, ni
        rutina — todo el camino de NPC daria falso. Es un tipo aparte y hoy
        sirve para UNA cosa: reservarlo. Reservado, ninguna otra quest se
        activa en ese slot y ningun mensaje prioritario ajeno se entrega.

        Sin `dia` = todos los dias; sin `horario` = todo el dia. Un atributo en
        None = no lo pido / no lo toco.

        COMO SE LEE AHORA (capa 2, parte momentanea — desde el paso A las
        demandas son LA fuente del "cuando y donde", los disparadores ya no lo
        chequean a mano):
          - npc: de los Recs de ese NPC, los que rigen en este (dia, horario)
            tienen que cumplirse (`en`, `skin`, `animo`, `libre`); si el NPC
            tiene Recs con slot y ninguno rige ahora, "no es el momento". Un
            Rec sin slot rige siempre. Siempre: disponible y no oculto.
          - locacion: el MC esta AHI ahora (`en`, o cualquiera de
            `locaciones`), en su slot si lo tiene, y la restriccion activa lo
            permite.
        """
        def __init__(self, tipo, npc=None, dia=None, horario=None, en=None,
                     skin=None, animo=None, disponible=None, accion=None,
                     reserva=False, locaciones=None, libre=False):
            if tipo not in REC_TIPOS:
                raise ValueError("Rec: tipo desconocido %r" % (tipo,))
            self.tipo = tipo
            self.npc = npc
            self.dia = dia
            self.horario = horario
            # `en`: id de locacion, o una locacion MADRE ("casa": en cualquier
            # sublocacion de la casa — lo que pide un personaje prestado).
            self.en = en
            self.skin = skin
            self.animo = animo
            self.disponible = disponible
            # libre=True (solo npc, momentaneo): sin rutina especial (ducha,
            # salida) e interactuable. Es el "sin nada encima" de los triggers.
            self.libre = bool(libre)
            self.accion = accion
            # False | True (slot) | "vida" (hasta completar la quest)
            if reserva not in (False, True, "vida"):
                raise ValueError("Rec: reserva tiene que ser True, False o 'vida' (%r)" % (reserva,))
            self.reserva = reserva
            self.locaciones = set(locaciones) if locaciones else None

        def slot_incluye(self, dia_semana, horario):
            """True si este Rec rige en (dia_semana, horario)."""
            if self.dia is not None and self.dia != dia_semana:
                return False
            if self.horario is not None and self.horario != horario:
                return False
            return True

        def slots_superpuestos(self, otro):
            """True si hay algun (dia, horario) en el que rigen los dos."""
            if (self.dia is not None and otro.dia is not None
                    and self.dia != otro.dia):
                return False
            if (self.horario is not None and otro.horario is not None
                    and self.horario != otro.horario):
                return False
            return True

        def __repr__(self):
            partes = [self.tipo]
            if self.npc:
                partes.append(self.npc)
            if self.accion:
                partes.append(self.accion)
            extra = []
            if self.dia is not None:
                extra.append("dia=%d" % self.dia)
            if self.horario is not None:
                extra.append("h=%d" % self.horario)
            for a in _REC_ATRIBUTOS_NPC:
                v = getattr(self, a, None)
                if v is not None:
                    extra.append("%s=%r" % (a, v))
            if self.locaciones:
                extra.append("locaciones=%d" % len(self.locaciones))
            if self.reserva:
                extra.append("reserva")
            s = ":".join(partes)
            if extra:
                s += "(" + ", ".join(extra) + ")"
            return "Rec<%s>" % s

    def rec_cubre(consumo, demanda):
        """
        True si el CONSUMO le pisa la DEMANDA. Es la tabla de cobertura del
        diseño, tipo por tipo.
        """
        ct, dt = consumo.tipo, demanda.tipo

        if ct == "npc" and dt == "npc":
            if consumo.npc != demanda.npc:
                return False
            if not consumo.slots_superpuestos(demanda):
                return False
            for a in _REC_ATRIBUTOS_NPC:
                cv, dv = getattr(consumo, a), getattr(demanda, a)
                if cv is not None and dv is not None and cv != dv:
                    return True
            return False

        if ct == "interaccion" and dt == "interaccion":
            if consumo.npc != demanda.npc:
                return False
            return (consumo.accion is None or demanda.accion is None
                    or consumo.accion == demanda.accion)

        if ct == "puerta" and dt == "puerta":
            return consumo.npc == demanda.npc

        if ct == "locaciones" and dt == "locacion":
            _wl = consumo.locaciones or set()
            if demanda.locaciones:
                return not any(l in _wl for l in demanda.locaciones)
            return bool(demanda.en) and demanda.en not in _wl

        if ct == "reloj":
            if dt == "reloj":
                return True
            return dt == "accion" and demanda.accion in ACCIONES_RELOJ

        if ct == "accion" and dt == "accion":
            return consumo.accion == demanda.accion

        if ct == "celular":
            return dt in ("celular", "mensajes")
        if ct == "mensajes":
            return dt == "mensajes"

        if ct == "mc" and dt == "mc":
            return consumo.slots_superpuestos(demanda)

        return False

    # ==========================================================================
    # Declaracion — lo llama el contenido en init 6
    # ==========================================================================

    DISP_TIPOS = ("boton", "puerta", "locacion", "encuentro", "dormir",
                  "accion", "item", "chat", "repartidor", "auto")

    class Disp(object):
        """
        El DISPARADOR de una quest, declarado para que el motor pueda escribir
        el "que hacer" completo a partir de el y de las demandas (ver
        planificador_que_hacer). Datos puros (picklable).

            Disp("boton", "Preguntar por el cosplay")   # opcion del menu del NPC
            Disp("puerta", "Llamarla")                  # opcion de la puerta
            Disp("locacion")                            # entrar a la locacion demandada
            Disp("encuentro")                           # cruzarse con el NPC
            Disp("dormir") / Disp("accion", "Ver TV") / Disp("item", "Mangas")
            Disp("chat") / Disp("repartidor") / Disp("auto")

        `nota`: un detalle narrativo que ninguna demanda expresa ("despues de
        responder su mensaje"), va al final.
        """
        def __init__(self, tipo, texto=None, nota=None):
            if tipo not in DISP_TIPOS:
                raise ValueError("Disp: tipo desconocido %r" % (tipo,))
            self.tipo = tipo
            self.texto = texto
            self.nota = nota

        def __repr__(self):
            return "Disp<%s%s>" % (self.tipo, (":" + self.texto) if self.texto else "")

    def declarar_planificacion(quest_id, de_corrido=False, demandas=None,
                               consumos=None, duenio=None, disparador=None):
        """
        Carga en la quest del catalogo lo que el planificador necesita. Se
        llama en `init 6` (las quests se registran en init 5) desde
        characters/<npc>/quests/planificacion_<npc>.rpy. Los campos entran en
        _CAMPOS de persistencia_sistemas: al cargar un save se copian del
        catalogo fresco, asi que cambiar una declaracion alcanza a las
        partidas viejas.
        """
        q = store.sistema_quests.obtener_quest(quest_id)
        if q is None:
            raise ValueError("declarar_planificacion: la quest %r no existe" % (quest_id,))
        for r in list(demandas or []) + list(consumos or []):
            if not isinstance(r, Rec):
                raise ValueError("declarar_planificacion(%r): %r no es un Rec" % (quest_id, r))
        if disparador is not None and not isinstance(disparador, Disp):
            raise ValueError("declarar_planificacion(%r): disparador tiene que ser un Disp" % (quest_id,))
        q.de_corrido = bool(de_corrido)
        q.demandas = list(demandas or [])
        q.consumos = list(consumos or [])
        q.duenio = duenio
        q.disparador = disparador
        q.planificada = True

    # ==========================================================================
    # Lecturas del mundo (sin pasar por los embudos — ver REGLA ANTI-RECURSION)
    # ==========================================================================

    def _pl_quests_activas(excepto=None):
        """Quests vivas (nacieron y no terminaron), salvo `excepto`."""
        out = []
        for q in store.sistema_quests.quests.values():
            if q is excepto or not q.activa or q.completada:
                continue
            if q.etapa_actual < ETAPA_RUTINA:
                continue
            out.append(q)
        return out

    def _pl_restriccion_ajena(quest):
        """La restriccion activa si NO es de esta quest, o None."""
        r = getattr(store, "restriccion_quest_activa", None)
        if r is None or not getattr(r, "activa", True):
            return None
        _duenio_q = getattr(quest, "duenio", None) if quest is not None else None
        if _duenio_q is not None and getattr(r, "duenio", None) == _duenio_q:
            return None
        return r

    def _pl_consumos_vivos(restriccion):
        """Lo que una restriccion activa consume, como Recs."""
        recs = []
        if restriccion is None:
            return recs
        if getattr(restriccion, "congelar_reloj", False):
            recs.append(Rec("reloj"))
        for a in (getattr(restriccion, "acciones_bloqueadas", None) or ()):
            recs.append(Rec("accion", accion=a))
        if getattr(restriccion, "locaciones_permitidas", None) is not None:
            recs.append(Rec("locaciones", locaciones=restriccion.locaciones_permitidas))
        if getattr(restriccion, "celular_bloqueado", False):
            recs.append(Rec("celular"))
        if getattr(restriccion, "mensajes_bloqueados", False):
            recs.append(Rec("mensajes"))
        # Un NPC oculto por la restriccion no se puede clickear ni golpear su
        # puerta; el Rec npc lo cubre _pl_conflicto_activacion aparte.
        for n in (getattr(restriccion, "npcs_ocultos", None) or ()):
            recs.append(Rec("interaccion", n))
            recs.append(Rec("puerta", n))
        return recs

    def _pl_ubicacion_npc(npc_id):
        """
        Locacion cruda del NPC ("fuera" incluido): las declaraciones usan los
        mismos valores que las rutinas. tracker_locacion_npc no sirve aca
        porque traduce "fuera" a None.
        """
        try:
            n = obtener_npc(npc_id)
        except Exception:
            return None
        return getattr(n, "locacion_actual", None) if n is not None else None

    def _pl_nombre_quest(q):
        try:
            return renpy.translate_string(q.nombre)
        except Exception:
            return q.id

    def _pl_nombre_npc(npc_id):
        try:
            n = obtener_npc(npc_id)
        except Exception:
            return npc_id
        return n.nombre if n is not None else npc_id

    def _pl_texto_terminar_primero(otra):
        return renpy.translate_string("Terminar «{quest}» primero").format(
            quest=_pl_nombre_quest(otra))

    # ==========================================================================
    # CAPA 1 — nacer
    # ==========================================================================

    def _pl_consumos_pisan(consumos, demandas):
        for c in consumos:
            for d in demandas:
                if rec_cubre(c, d):
                    return (c, d)
        return None

    def planificador_puede_nacer(quest):
        """
        (True, None) si la quest puede pasar de CONDICIONES a RUTINA; si no,
        (False, quest_id_que_la_frena o None). No mira a la quest en si: mira
        si su entrada le rompe algo a lo que ya esta corriendo.
        """
        if not getattr(quest, "planificada", False):
            return (True, None)

        # Con una secuencia ajena en curso (reloj congelado) no nace nada: una
        # rutina nueva a mitad de la noche de otra la rompe. Duran horas.
        r = _pl_restriccion_ajena(quest)
        if r is not None and getattr(r, "congelar_reloj", False):
            return (False, None)

        consumos = getattr(quest, "consumos", None) or []
        if not consumos:
            return (True, None)

        # ¿Le piso una demanda a una DE CORRIDO activa?
        for otra in _pl_quests_activas(excepto=quest):
            if not getattr(otra, "de_corrido", False):
                continue
            if _pl_consumos_pisan(consumos, getattr(otra, "demandas", None) or []):
                return (False, otra.id)

        # FIFO: no me adelanto a una de corrido que espera desde antes si al
        # nacer yo se la seguiria frenando.
        _mi_turno = getattr(quest, "esperando_desde", None)
        for w in store.sistema_quests.quests.values():
            if w is quest or not w.activa or w.completada:
                continue
            if w.etapa_actual != ETAPA_CONDICIONES or not getattr(w, "de_corrido", False):
                continue
            _turno_w = getattr(w, "esperando_desde", None)
            if _turno_w is None:
                continue
            if _mi_turno is not None and _turno_w > _mi_turno:
                continue
            if _pl_consumos_pisan(consumos, getattr(w, "demandas", None) or []):
                return (False, w.id)

        return (True, None)

    # ==========================================================================
    # CAPA 2 — activar
    # ==========================================================================

    def _pl_duenia_de_la_restriccion(quest):
        """
        True si la restriccion activa es de ESTA quest (mismo `duenio`): su
        secuencia ya arranco aunque nadie la haya pasado por activar_quest
        (la ponen accion_al_entrar de BOTON_LISTO, como la 0_b de Monica).
        Para la capa de conflicto cuenta como "en narrativa": lo que la
        frenaria (una reserva ajena, los consumos de otra) ya no la puede
        frenar, porque su salida es la unica forma de levantar la
        restriccion. Caso real: la 0_b de Monica (bloquea dormir hasta ir al
        living) y la 09_a naciendo esa misma mañana con Monica reservada de
        vida — la reserva escondia el disparador de la 0_b y la 0_b bloqueaba
        el dormir que la 09_a necesita. Deadlock.
        """
        _d = getattr(quest, "duenio", None)
        if not _d:
            return False
        r = getattr(store, "restriccion_quest_activa", None)
        return bool(r is not None and r.activa and getattr(r, "duenio", None) == _d)

    def _pl_conflicto_activacion(quest):
        """
        La parte de la capa 2 que depende de OTRO contenido: reserva ajena,
        consumos declarados de otras activas y consumos vivos de la
        restriccion ajena. Devuelve el texto del motivo (ya traducido) o None.
        Es lo que se escribe en el "que hacer" y lo que gatea los autodisparos.
        """
        demandas = getattr(quest, "demandas", None) or []

        # 1. Reserva ajena vigente sobre un NPC que es MIO (una quest de la
        #    linea de Violet es, por definicion, una interaccion con Violet:
        #    no hace falta que lo declare) o que necesito por demanda.
        #
        #    Y sobre el MC: si otra quest tiene reservada la noche, NINGUNA
        #    entra — el MC esta en todas las escenas del juego, asi que no hace
        #    falta que lo declaren. Va primero porque no depende de demandas.
        for res in planificador_reservas_vigentes():
            if res["quest_id"] == quest.id:
                continue
            if res["npc"] == "mc":
                return res["texto"]
            if getattr(quest, "npc_id", None) == res["npc"]:
                return res["texto"]
            for d in demandas:
                if d.tipo in ("npc", "interaccion", "puerta") and d.npc == res["npc"]:
                    return res["texto"]

        if not demandas:
            return None

        # 2. Consumos declarados de las otras activas.
        for otra in _pl_quests_activas(excepto=quest):
            if _pl_consumos_pisan(getattr(otra, "consumos", None) or [], demandas):
                return _pl_texto_terminar_primero(otra)

        # 3. Consumos vivos de la restriccion ajena (incluido un NPC que
        #    necesito y ella tiene oculto).
        r = _pl_restriccion_ajena(quest)
        if r is not None:
            if _pl_consumos_pisan(_pl_consumos_vivos(r), demandas):
                return renpy.translate_string("Terminar lo que está pasando primero")
            _ocultos = getattr(r, "npcs_ocultos", None) or ()
            for d in demandas:
                if d.tipo == "npc" and d.npc in _ocultos:
                    return renpy.translate_string("Terminar lo que está pasando primero")

        return None

    def _pl_npc_en(npc_id, en):
        """
        True si el NPC esta en `en`. `en` puede ser una locacion o una
        LOCACION MADRE (`LOCACIONES_MADRE`, hoy "casa", o "fuera", que es su
        propia madre): ahi alcanza con que este en cualquier sublocacion de
        esa madre. Es lo que pide un personaje PRESTADO (Jasmine en una quest
        de Violet): no hace falta que este en un lugar puntual, pero si en la
        casa, o su aparicion no tiene sentido. `en="fuera"` = salio.
        """
        _loc = _pl_ubicacion_npc(npc_id)
        if not _loc:
            return False
        # Una madre ("casa", o "fuera", que es su propia madre y NO parte de
        # la casa): se compara la madre del NPC. Si no, la locacion exacta.
        if en == LOCACION_FUERA or en in LOCACIONES_MADRE:
            return madre_de_locacion(_loc) == en
        return _loc == en

    def _pl_mundo_detalle(quest):
        """
        La parte momentanea de la capa 2, separada en TIEMPO y LUGAR:
        devuelve (motivo_tiempo, motivo_lugar), cada uno un texto ya traducido
        o None si esa parte se cumple. Es lo que muestra el panel en vivo,
        para que se vea cual de las dos falla.

          TIEMPO: algun Rec con slot rige en este (dia, horario) — por NPC y
                  por locacion del MC.
          LUGAR : todo lo demas que se pide AHORA — NPC disponible y no
                  oculto, donde hace falta (`en`), libre, skin, animo; el MC
                  en la locacion demandada; el celular libre.

        Es ESTRICTA desde el paso A: las demandas son la unica fuente del
        "cuando y donde" de un disparador (ver Rec).
        """
        _dia = getattr(store, "dia_semana_actual", 0)
        _h = getattr(store, "horario_actual", 0)
        demandas = getattr(quest, "demandas", None) or []
        _tiempo = None
        _lugar = None
        # EXTERNO: la falla de lugar no depende del jugador (el NPC no esta,
        # se fue, esta oculto/ocupado, el celular bloqueado). Es lo que la
        # guia muestra en rojo. Que el MC no este en el lugar, no.
        _externo = False

        def _t(msg):
            return renpy.translate_string(msg)

        # NPCs: disponible y no oculto, siempre (LUGAR).
        _npcs = []
        for d in demandas:
            if d.tipo in ("npc", "interaccion", "puerta") and d.npc and d.npc not in _npcs:
                _npcs.append(d.npc)
        for n in _npcs:
            if _lugar:
                break
            _pide_disp = all(d.disponible is not False for d in demandas if d.tipo == "npc" and d.npc == n)
            if (_pide_disp and not npc_disponible(n)) or npc_esta_oculto(n):
                _lugar = _t("{npc} no está").format(npc=_pl_nombre_npc(n))
                _externo = True

        # NPCs: el slot (TIEMPO) y el estado que piden los Recs que rigen (LUGAR).
        for n in _npcs:
            _recs = [d for d in demandas if d.tipo == "npc" and d.npc == n]
            if not _recs:
                continue
            _con_slot = [d for d in _recs if d.dia is not None or d.horario is not None]
            _rigen = [d for d in _recs if d.slot_incluye(_dia, _h)]
            if _con_slot and not any(d in _rigen for d in _con_slot):
                _tiempo = _tiempo or _t("No es el momento")
            if _lugar:
                continue
            for d in _rigen:
                if d.en is not None and not _pl_npc_en(n, d.en):
                    if not _pl_npc_en(n, "casa"):
                        _lugar = _t("{npc} no está en la casa").format(npc=_pl_nombre_npc(n))
                    else:
                        _lugar = _t("{npc} no está donde hace falta").format(npc=_pl_nombre_npc(n))
                    _externo = True
                    break
                if d.libre:
                    _obj = obtener_npc(n)
                    if ((_obj is not None and _obj.obtener_rutina_especial_actual() is not None)
                            or not npc_interactuable(n)):
                        _lugar = _t("{npc} está ocupada").format(npc=_pl_nombre_npc(n))
                        _externo = True
                        break
                if d.skin is not None:
                    _sk = obtener_skin_activo(n)
                    if _sk is None or (d.skin != getattr(_sk, "id", None)
                                       and d.skin != getattr(_sk, "grupo", None)):
                        _lugar = _t("{npc} no está como hace falta").format(npc=_pl_nombre_npc(n))
                        _externo = True
                        break
                if d.animo is not None:
                    try:
                        _est = store.sistema_talk.obtener_estado_activo(n)
                    except Exception:
                        _est = None
                    if _est is None or getattr(_est, "id", None) != d.animo:
                        _lugar = _t("{npc} no está como hace falta").format(npc=_pl_nombre_npc(n))
                        _externo = True
                        break

        # El resto: celular (LUGAR), locacion del MC (slot = TIEMPO, donde = LUGAR).
        _loc_mc = store.sistema_locaciones.locacion_actual
        _loc_mc_id = _loc_mc.id if _loc_mc else None
        r = _pl_restriccion_ajena(quest)
        for d in demandas:
            if d.tipo == "celular":
                if not _lugar and celular_esta_bloqueado():
                    _lugar = _t("No puedo usar el celular ahora")
                    _externo = True
            elif d.tipo == "locacion":
                if not d.slot_incluye(_dia, _h):
                    _tiempo = _tiempo or _t("No es el momento")
                if _lugar:
                    continue
                _donde = set(d.locaciones) if d.locaciones else ({d.en} if d.en else set())
                if _donde and _loc_mc_id not in _donde:
                    _lugar = _t("No estoy donde hace falta")
                elif r is not None and _loc_mc_id and not r.es_locacion_permitida(_loc_mc_id):
                    _lugar = _t("No puedo ir ahí ahora")
                    _externo = True
        return (_tiempo, _lugar, _externo)

    def _pl_mundo_cumple(quest):
        """Motivo momentaneo (tiempo primero, despues lugar) o None. Ver _pl_mundo_detalle."""
        _tiempo, _lugar, _ext = _pl_mundo_detalle(quest)
        return _tiempo or _lugar

    # ==========================================================================
    # LA GUIA — "que hacer" generado y estado de la quest
    # ==========================================================================

    _PL_HORARIO_FRASE = {0: "por la mañana", 1: "por la tarde", 2: "por la noche", 3: "de madrugada"}
    _PL_LUGAR_LA = ("cocina", "hviolet", "hmonica", "hjasmine")
    _PL_HABITACION_DE = {"hviolet": "violet", "hmonica": "monica", "hjasmine": "jasmine"}

    def _pl_lugar_frase(loc_id):
        """'en la Cocina' / 'en el Living' / 'en tu habitación' (traducido)."""
        if loc_id == "casa_hmc":
            return renpy.translate_string("en tu habitación")
        _loc = store.sistema_locaciones.obtener_locacion(loc_id) if hasattr(store, "sistema_locaciones") else None
        _nombre = renpy.translate_string(_loc.nombre) if _loc is not None else loc_id
        _art = "la" if any(k in loc_id for k in _PL_LUGAR_LA) else "el"
        return renpy.translate_string("en {articulo} {lugar}").format(articulo=_art, lugar=_nombre)

    def _pl_entrar_frase(loc_id):
        """'Entrar a la Cocina' / 'Entrar al Living' / 'Entrar a tu habitación' (traducido)."""
        if loc_id == "casa_hmc":
            return renpy.translate_string("Entrar a tu habitación")
        _loc = store.sistema_locaciones.obtener_locacion(loc_id) if hasattr(store, "sistema_locaciones") else None
        _nombre = renpy.translate_string(_loc.nombre) if _loc is not None else loc_id
        _art = "a la" if any(k in loc_id for k in _PL_LUGAR_LA) else "al"
        return renpy.translate_string("Entrar {articulo} {lugar}").format(articulo=_art, lugar=_nombre)

    def _pl_es_habitacion_de(loc_id, npc_id):
        return _PL_HABITACION_DE.get(loc_id.replace("casa_", ""), None) == npc_id

    def _pl_juntar_nombres(nombres):
        """'Violet' / 'Violet y Mónica' / 'Violet, Mónica y Jasmine' (traducido)."""
        if len(nombres) == 1:
            return nombres[0]
        return renpy.translate_string("{a} y {b}").format(
            a=", ".join(nombres[:-1]), b=nombres[-1])

    def _pl_condiciones_npcs(npcs_en, destino=None, nombrado=None):
        """
        Las condiciones de presencia de los NPCs, AGRUPADAS: los que piden lo
        mismo van en una sola frase ("mientras Violet y Mónica estén en la
        casa"). `npcs_en` es una lista de (npc_id, en).

        `nombrado`: el NPC que la accion ya nombro ("Usar la opción X con
        Violet"). Si queda SOLO en su frase, va sin nombre — "(mientras esté
        en la casa)" — para no repetirlo.

        Que significa cada `en`:
          None / "casa" / el `destino` del MC -> "en la casa". Si el NPC tiene
              que estar justo donde va el MC, es la quest la que lo pone ahi
              con su rutina: lo unico que el jugador puede ver es si esta en la
              casa o no.
          "fuera"                  -> "afuera"
          su propia habitacion     -> "en su habitación"
          otra locacion            -> "en la Cocina", etc.
        """
        _t = renpy.translate_string
        grupos = []          # [(clave, [nombres])] en orden de aparicion
        for _nid, _en in npcs_en:
            if _en is None or _en == "casa" or (destino is not None and _en == destino):
                _clave = ("casa", None)
            elif _en == "fuera":
                _clave = ("fuera", None)
            elif _pl_es_habitacion_de(_en, _nid):
                _clave = ("suya", None)
            else:
                _clave = ("lugar", _en)
            _nombre = _pl_nombre_npc(_nid)
            for _g in grupos:
                if _g[0] == _clave:
                    if _nombre not in _g[1]:
                        _g[1].append(_nombre)
                    break
            else:
                grupos.append((_clave, [_nombre]))

        frases = []
        _nombre_ya_dicho = _pl_nombre_npc(nombrado) if nombrado else None
        for (_tipo, _loc), _nombres in grupos:
            if _nombre_ya_dicho and _nombres == [_nombre_ya_dicho]:
                if _tipo == "casa":
                    frases.append(_t("mientras esté en la casa"))
                elif _tipo == "fuera":
                    frases.append(_t("mientras esté afuera"))
                elif _tipo == "suya":
                    frases.append(_t("mientras esté en su habitación"))
                else:
                    frases.append(_t("mientras esté {lugar}").format(lugar=_pl_lugar_frase(_loc)))
                continue
            _npcs = _pl_juntar_nombres(_nombres)
            _varios = len(_nombres) > 1
            if _tipo == "casa":
                _f = "mientras {npcs} estén en la casa" if _varios else "mientras {npcs} esté en la casa"
                frases.append(_t(_f).format(npcs=_npcs))
            elif _tipo == "fuera":
                _f = "mientras {npcs} estén afuera" if _varios else "mientras {npcs} esté afuera"
                frases.append(_t(_f).format(npcs=_npcs))
            elif _tipo == "suya":
                _f = "mientras {npcs} estén en sus habitaciones" if _varios else "mientras {npcs} esté en su habitación"
                frases.append(_t(_f).format(npcs=_npcs))
            else:
                _f = "mientras {npcs} estén {lugar}" if _varios else "mientras {npcs} esté {lugar}"
                frases.append(_t(_f).format(npcs=_npcs, lugar=_pl_lugar_frase(_loc)))
        return frases

    def planificador_que_hacer(quest):
        """
        El "que hacer" COMPLETO de una quest a partir de su disparador (Disp)
        y de sus demandas. None si la quest no declara disparador (usa su
        texto propio).

        LA FORMA ES SIEMPRE LA MISMA: primero lo que hay que HACER, donde y
        cuando; despues, entre parentesis, las CONDICIONES que no dependen del
        jugador pero que tiene que saber para entender por que no pasa nada.

            Entrar al Living por la mañana (mientras Violet y Mónica estén en la casa)
            Usar la opción «Llamarla» en la puerta de Violet por la tarde (mientras esté adentro)
            Entrar al Sótano el Viernes o el Sábado por la noche (después de que Violet te escriba)
            Ir a dormir el Sábado
        """
        disp = getattr(quest, "disparador", None)
        if disp is None:
            return None
        demandas = getattr(quest, "demandas", None) or []
        npc_id = getattr(quest, "npc_id", None)
        npc = _pl_nombre_npc(npc_id) if npc_id else ""
        _t = renpy.translate_string

        # Lo que dicen las demandas, ordenado.
        recs_npc = [d for d in demandas if d.tipo == "npc" and d.npc == npc_id]
        ens = sorted(set(d.en for d in recs_npc if d.en))
        en_propio = ens[0] if len(ens) == 1 else None
        recs_loc = [d for d in demandas if d.tipo == "locacion"]
        loc_mc = None
        if recs_loc and recs_loc[0].en:
            loc_mc = recs_loc[0].en
        horarios = sorted(set(d.horario for d in demandas if d.tipo in ("npc", "locacion") and d.horario is not None))
        horario = horarios[0] if len(horarios) == 1 else None
        dias = sorted(set(d.dia for d in demandas if d.tipo in ("npc", "locacion") and d.dia is not None))
        dia = dias[0] if len(dias) == 1 else None
        otros = []
        for d in demandas:
            if d.tipo == "npc" and d.npc != npc_id and d.npc not in [o[0] for o in otros]:
                otros.append((d.npc, d.en))

        accion = []        # que hacer, donde y cuando
        condiciones = []   # entre parentesis
        # El NPC de la quest en las condiciones: (npc_id, en) o None si ya
        # quedo dicho en la accion ("con Violet en la Cocina").
        propio_cond = (npc_id, en_propio) if (npc_id and recs_npc) else None
        destino = None     # adonde va el MC, si la accion es ir a un lugar

        if disp.tipo == "boton":
            accion.append(_t("Usar la opción «{opcion}» con {npc}").format(opcion=_t(disp.texto or ""), npc=npc))
            if en_propio and _pl_es_habitacion_de(en_propio, npc_id):
                accion.append(_t("en su habitación"))
                propio_cond = None
            elif en_propio and en_propio not in ("casa", "fuera"):
                accion.append(_pl_lugar_frase(en_propio))
                propio_cond = None
            if loc_mc and loc_mc != en_propio:
                accion.append(_pl_lugar_frase(loc_mc))
        elif disp.tipo == "puerta":
            accion.append(_t("Usar la opción «{opcion}» en la puerta de {npc}").format(opcion=_t(disp.texto or ""), npc=npc))
            if en_propio and _pl_es_habitacion_de(en_propio, npc_id):
                condiciones.append(_t("mientras esté adentro"))
                propio_cond = None
        elif disp.tipo == "locacion":
            if loc_mc:
                accion.append(_pl_entrar_frase(loc_mc))
                destino = loc_mc
            else:
                accion.append(_t("Ir a la locación"))
        elif disp.tipo == "encuentro":
            accion.append(_t("Cruzarte con {npc}").format(npc=npc))
            if en_propio and en_propio not in ("casa", "fuera") and not _pl_es_habitacion_de(en_propio, npc_id):
                accion.append(_pl_lugar_frase(en_propio))
                propio_cond = None
        elif disp.tipo == "dormir":
            # SOLO "Ir a dormir" (y el dia, si la quest pide uno). Las demandas
            # de una quest de dormir describen el mundo que ella misma arma con
            # sus rutinas al despertar ("Monica afuera, Jasmine en su pieza"):
            # el jugador no puede hacer nada con eso, y listarlo confundia.
            accion.append(_t("Ir a dormir"))
            # Se duerme a la noche; el horario que declara una quest de dormir
            # es el del despertar o el de la reserva, no el de la accion.
            horario = None
            otros = []
            propio_cond = None
            # El dia que declaran las demandas es el de la ESCENA, que pasa al
            # despertar. Lo que el jugador tiene que hacer es dormir la noche
            # ANTERIOR: para una escena del domingo, "Ir a dormir el sábado".
            if dia is not None:
                dia = (dia - 1) % 7
            dias = [(_d - 1) % 7 for _d in dias]
        elif disp.tipo == "accion":
            accion.append(_t("Usar la acción «{opcion}»").format(opcion=_t(disp.texto or "")))
            if loc_mc:
                accion.append(_pl_lugar_frase(loc_mc))
        elif disp.tipo == "item":
            accion.append(_t("Usar {item}").format(item=_t(disp.texto or "")))
        elif disp.tipo == "chat":
            accion.append(_t("Responder el mensaje de {npc}").format(npc=npc))
            propio_cond = None
        elif disp.tipo == "repartidor":
            accion.append(_t("Atender al repartidor"))
        elif disp.tipo == "auto":
            # Una quest que arranca sola sigue teniendo algo que hacer (Carl:
            # contestarle). "Se activa sola" no lo dice: va el texto propio.
            return None

        # Cuando: primero el dia, despues el horario ("el Sábado por la noche").
        if dia is not None:
            accion.append(_t("el {dia}").format(dia=_q_nombre_dia(dia)))
        elif len(dias) > 1:
            # Varios dias posibles (amor 35: viernes o sabado). Sin esto el
            # texto no decia ninguno y el jugador no sabia por que no pasaba
            # nada el resto de la semana.
            _nombres = [_q_nombre_dia(_d) for _d in dias]
            accion.append(_t("el {dias} o el {ultimo}").format(
                dias=", ".join(_nombres[:-1]), ultimo=_nombres[-1]))
        if horario is not None:
            accion.append(_t(_PL_HORARIO_FRASE.get(horario, "")))

        # Las condiciones: quien tiene que estar donde (agrupado) y la nota.
        _npcs_en = ([propio_cond] if propio_cond else []) + list(otros)
        # Las acciones que nombran al NPC de la quest no lo repiten en la condicion.
        _nombrado = npc_id if disp.tipo in ("boton", "puerta", "encuentro") else None
        condiciones = _pl_condiciones_npcs(_npcs_en, destino=destino, nombrado=_nombrado) + condiciones
        if disp.nota:
            condiciones.append(_t(disp.nota))

        texto = " ".join(p for p in accion if p)
        if condiciones:
            texto += " (" + ", ".join(condiciones) + ")"
        return texto

    def planificador_estado_guia(quest):
        """
        Estado de la quest para la guia: ("lista", "Disponible") en verde
        cuando se puede hacer —ahora o en cuanto el jugador vaya al lugar o
        espere el horario—; ("bloqueada", motivo) en rojo, "Interrumpida",
        cuando algo EXTERNO la frena (otra quest la reservo o le pisa una
        demanda, una restriccion ajena, el NPC no esta en la casa / no
        disponible / oculto / ocupado, el celular bloqueado). (None, None)
        solo si la quest no esta en BOTON_LISTO o ya esta en narrativa.
        """
        if (not getattr(quest, "planificada", False) or not quest.activa or quest.completada
                or quest.etapa_actual != ETAPA_BOTON_LISTO or getattr(quest, "narrativa_activa", False)):
            return (None, None)
        if not npc_disponible(quest.npc_id):
            return ("bloqueada", renpy.translate_string("{npc} no está").format(npc=_pl_nombre_npc(quest.npc_id)))
        _c = None if _pl_duenia_de_la_restriccion(quest) else _pl_conflicto_activacion(quest)
        if _c:
            return ("bloqueada", _c)
        _tiempo, _lugar, _externo = _pl_mundo_detalle(quest)
        if _lugar and _externo:
            return ("bloqueada", _lugar)
        return ("lista", renpy.translate_string("Disponible"))

    def planificador_puede_activarse(quest):
        """
        Capa 2 completa. (True, None) o (False, motivo). Deja en
        quest.bloqueo_activacion el motivo SOLO cuando es un conflicto con
        otro contenido — es lo que la guia muestra en el "que hacer".
        """
        if not getattr(quest, "planificada", False):
            return (True, None)
        if getattr(quest, "narrativa_activa", False):
            quest.bloqueo_activacion = None
            return (True, None)
        # La dueña de la restriccion activa ya esta en su secuencia: solo se
        # mide lo momentaneo (lugar/hora), nunca el conflicto con otras.
        motivo = None if _pl_duenia_de_la_restriccion(quest) else _pl_conflicto_activacion(quest)
        if motivo:
            if getattr(quest, "bloqueo_activacion", None) != motivo:
                quest.bloqueo_activacion = motivo
            return (False, motivo)
        if getattr(quest, "bloqueo_activacion", None):
            quest.bloqueo_activacion = None
        motivo = _pl_mundo_cumple(quest)
        if motivo:
            return (False, motivo)
        return (True, None)

    def planificador_trigger_permitido(quest_id):
        """
        Gate de los autodisparos (triggers con quest_id=): la quest esta viva
        y no la frena un conflicto. La parte momentanea no se mira aca — la
        funcion del trigger ya chequea lo suyo, y hay triggers (contadores de
        dias) que tienen que correr aunque el momento no sea el del disparo.
        """
        q = store.sistema_quests.obtener_quest(quest_id)
        if q is None:
            return True
        if not (q.activa and not q.completada and q.etapa_actual == ETAPA_BOTON_LISTO):
            return False
        if getattr(q, "narrativa_activa", False) or not getattr(q, "planificada", False):
            return True
        if _pl_duenia_de_la_restriccion(q):
            return True
        return _pl_conflicto_activacion(q) is None

    # ==========================================================================
    # RESERVA
    # ==========================================================================

    _PL_MOMENTOS = {0: "esta mañana", 1: "esta tarde", 2: "esta noche", 3: "esta madrugada"}
    _PL_MOMENTOS_MANANA = {0: "mañana a la mañana", 1: "mañana a la tarde",
                           2: "mañana a la noche", 3: "mañana a la madrugada"}

    def _pl_proximo_slot(rec):
        """
        (dia_total, horario) del proximo slot que coincide con el Rec: hoy si
        no paso, si no mañana (o el proximo dia de la semana que pida).
        horario None = el dia entero (horario None en la reserva).
        """
        _hoy = getattr(store, "dias_totales", 1)
        _dia_sem = getattr(store, "dia_semana_actual", 0)
        _h = getattr(store, "horario_actual", 0)
        for delta in range(0, 8):
            dia_total = _hoy + delta
            dia_sem = (_dia_sem + delta) % 7
            if rec.dia is not None and rec.dia != dia_sem:
                continue
            if delta == 0 and rec.horario is not None and rec.horario < _h:
                continue
            return (dia_total, rec.horario, delta)
        return (_hoy, rec.horario, 0)

    def planificador_reservar(quest):
        """
        Al activarse una de corrido: reserva los slots que sus demandas marcan
        con reserva=True. Lo llama activar_quest.
        """
        if not getattr(quest, "planificada", False) or not getattr(quest, "de_corrido", False):
            return
        for d in (getattr(quest, "demandas", None) or []):
            if not d.reserva:
                continue
            # Que se reserva: un NPC (Rec npc) o el MC (Rec mc).
            if d.tipo == "mc":
                _a_reservar = "mc"
            elif d.tipo == "npc" and d.npc:
                _a_reservar = d.npc
            else:
                continue
            if any(r["quest_id"] == quest.id and r["npc"] == _a_reservar
                   for r in store.planificador_reservas):
                continue
            if d.reserva == "vida":
                store.planificador_reservas.append({
                    "quest_id": quest.id, "npc": _a_reservar,
                    "dia_total": None, "horario": None,
                    "texto": _pl_texto_terminar_primero(quest),
                })
                if config.developer:
                    print("[Planificador] reserva %s: %s hasta completar" % (quest.id, _a_reservar))
                continue
            dia_total, horario, delta = _pl_proximo_slot(d)
            if horario is None:
                momento = renpy.translate_string("hoy") if delta == 0 else renpy.translate_string("mañana")
            elif delta == 0:
                momento = renpy.translate_string(_PL_MOMENTOS[horario])
            else:
                momento = renpy.translate_string(_PL_MOMENTOS_MANANA[horario])
            if _a_reservar == "mc":
                # "Le dije a Mc que iba esta noche" no se puede leer. El texto
                # del MC habla de su agenda, que es lo que la reserva significa.
                texto = renpy.translate_string("Tengo algo pendiente {momento}").format(
                    momento=momento)
            else:
                texto = renpy.translate_string("Le dije a {npc} que iba {momento}").format(
                    npc=_pl_nombre_npc(d.npc), momento=momento)
            store.planificador_reservas.append({
                "quest_id": quest.id, "npc": _a_reservar,
                "dia_total": dia_total, "horario": horario, "texto": texto,
            })
            if config.developer:
                print("[Planificador] reserva %s: %s dia %d horario %r" % (
                    quest.id, _a_reservar, dia_total, horario))

    def _pl_reserva_es_vida(res):
        return res.get("dia_total") is None

    def _pl_reserva_vigente_ahora(res):
        if _pl_reserva_es_vida(res):
            return True
        _hoy = getattr(store, "dias_totales", 1)
        _h = getattr(store, "horario_actual", 0)
        if res["dia_total"] != _hoy:
            return False
        return res["horario"] is None or res["horario"] == _h

    def _pl_reserva_vencida(res):
        if _pl_reserva_es_vida(res):
            return False
        _hoy = getattr(store, "dias_totales", 1)
        _h = getattr(store, "horario_actual", 0)
        if res["dia_total"] < _hoy:
            return True
        if res["dia_total"] == _hoy and res["horario"] is not None and _h > res["horario"]:
            return True
        return False

    def planificador_reservas_vigentes(npc=None):
        """Reservas que rigen en este (dia, horario), opcionalmente de un NPC."""
        out = []
        for res in getattr(store, "planificador_reservas", None) or []:
            if npc is not None and res["npc"] != npc:
                continue
            if _pl_reserva_vigente_ahora(res):
                out.append(res)
        return out

    def planificador_reserva_vigente(npc=None):
        """La primera reserva vigente ahora (dict) o None."""
        _v = planificador_reservas_vigentes(npc)
        return _v[0] if _v else None

    def planificador_bloqueo_reloj():
        """
        Efecto 3 de la reserva, para el embudo accion_bloqueada: el texto del
        bloqueo si hay una reserva vigente, o None.
        """
        if not PLANIFICADOR_RESERVA_CONGELA_RELOJ:
            return None
        for res in planificador_reservas_vigentes():
            if not _pl_reserva_es_vida(res):
                return res["texto"]
        return None

    def planificador_mc_reservado_por():
        """
        quest_id de la quest que tiene reservado al MC ahora, o None.

        Lo consulta el CONTENIDO antes de arrancar algo que le va a ocupar el
        rato al jugador (una escena larga, un mensaje que lo manda a un lugar):

            if planificador_mc_reservado_por() is None:
                ...

        La capa 2 ya lo usa sola para frenar las quests ajenas; esto es para
        los triggers, que no pasan por la parte momentanea.
        """
        return planificador_npc_reservado_por("mc")

    def planificador_npc_reservado_por(npc_id):
        """
        quest_id de la quest que tiene reservado al NPC ahora, o None. Es lo
        que consultan el menu del NPC y su puerta para dejar solo las opciones
        de esa quest.
        """
        res = planificador_reserva_vigente(npc_id)
        return res["quest_id"] if res else None

    def planificador_opcion_permitida(npc_id, label, quest_id=None):
        """
        True si una opcion del menu/puerta del NPC puede mostrarse: sin
        reserva, todas; con reserva, solo las de la quest que lo reservo.
        """
        _res_q = planificador_npc_reservado_por(npc_id)
        if _res_q is None:
            return True
        return resolver_quest_id_opcion(label, quest_id) == _res_q

    def planificador_texto_reserva(npc_id):
        """
        Texto (ya traducido) para el jugador que golpea la puerta de un NPC
        reservado, o None si el golpe sigue su flujo normal.

        SOLO bloquea la reserva de VIDA (09_a: hasta completar). La reserva de
        slot no: existe mientras corre la secuencia de la quest que la puso, y
        esa secuencia puede necesitar el golpe normal para entrar (Sinceridad
        entra a la pieza de Violet con la ventaja de deseo 20, sin opcion de
        puerta propia). Bloquearlo la dejaba sin salida: el reloj congelado
        por la misma reserva, la restriccion cerrando todo lo demas, y en la
        puerta "Le dije a Violet que iba esta noche" — soft lock real,
        reportado en la 0.1.9.1 (dia 51, noche, deseo 30).

        El menu del NPC sigue filtrando por quest en los dos tipos de reserva
        (planificador_opcion_permitida): lo que se libera es solo el golpe.
        """
        res = planificador_reserva_vigente(npc_id)
        if res is None or not _pl_reserva_es_vida(res):
            return None
        return renpy.translate_string("Mejor no molestar a {npc} ahora").format(npc=_pl_nombre_npc(npc_id))

    def planificador_limpiar_reservas():
        """
        Saca las reservas vencidas (avisando en desarrollo si su quest no se
        completo: es una narrativa rota) y las de quests ya completadas. Corre
        en cada actualizar_quests.
        """
        _lista = getattr(store, "planificador_reservas", None)
        if not _lista:
            return
        _quedan = []
        for res in _lista:
            q = store.sistema_quests.obtener_quest(res["quest_id"])
            if q is None or q.completada or not q.activa:
                continue
            if _pl_reserva_vencida(res):
                # En narrativa no es alarma: la secuencia arranco en el slot y
                # sigue (la tormenta empieza a la mañana y termina mas tarde).
                if config.developer and not getattr(q, "narrativa_activa", False):
                    print("[Planificador] AVISO: la reserva de %s (%s, dia %d h %r) "
                          "vencio sin que la quest arrancara" % (
                              res["quest_id"], res["npc"], res["dia_total"], res["horario"]))
                continue
            _quedan.append(res)
        if len(_quedan) != len(_lista):
            store.planificador_reservas = _quedan

    def planificador_liberar(quest_id):
        """Al completar o resetear una quest: se van sus reservas."""
        _lista = getattr(store, "planificador_reservas", None)
        if not _lista:
            return
        _quedan = [r for r in _lista if r["quest_id"] != quest_id]
        if len(_quedan) != len(_lista):
            store.planificador_reservas = _quedan

    # ==========================================================================
    # Diagnostico
    # ==========================================================================

    def planificador_reporte(max_lineas=12):
        """
        Lo que el controlador esta procesando AHORA, en lineas cortas, para
        los reportes de error y de feedback (y como extra de Sentry).

        Es la version "para afuera" de planificador_estado(): dice ademas que
        restriccion esta puesta y en que estado ve el controlador a cada quest
        viva, que es lo que hace falta para reconstruir una traba sin tener la
        partida. A prueba de fallos y con tope de lineas: corre dentro del
        handler de errores, donde cualquier excepcion taparia el reporte.

        Devuelve un string con saltos de linea, o "(nada pendiente)".
        """
        lineas = []

        # La restriccion activa: es la que explica la mayoria de las trabas.
        try:
            r = getattr(store, "restriccion_quest_activa", None)
            if r is not None and getattr(r, "activa", False):
                _p = ["restriccion de %s" % (getattr(r, "duenio", None) or "(sin dueño)")]
                if getattr(r, "congelar_reloj", False):
                    _p.append("reloj congelado")
                # sorted: `acciones_bloqueadas` es un set (congelar_reloj le
                # suma ACCIONES_RELOJ), y sin ordenar dos reportes del mismo
                # estado se leen distinto.
                _acc = sorted(getattr(r, "acciones_bloqueadas", None) or ())
                if _acc:
                    _p.append("bloquea %s%s" % (",".join(_acc[:6]),
                                                "…" if len(_acc) > 6 else ""))
                _locs = getattr(r, "locaciones_permitidas", None)
                if _locs is not None:
                    _locs = list(_locs)
                    _p.append("solo %s%s" % (",".join(_locs[:4]),
                                             "…" if len(_locs) > 4 else ""))
                _oc = list(getattr(r, "npcs_ocultos", None) or ())
                if _oc:
                    _p.append("ocultos %s" % ",".join(_oc))
                if getattr(r, "celular_bloqueado", False):
                    _p.append("celular bloqueado")
                lineas.append(" · ".join(_p))
        except Exception:
            pass

        # Reservas vigentes y vencidas (las dos importan: una vencida sin
        # completar es narrativa rota).
        try:
            for res in getattr(store, "planificador_reservas", None) or []:
                if _pl_reserva_es_vida(res):
                    lineas.append("reserva %s → %s (hasta completar)" % (
                        res["quest_id"], res["npc"]))
                else:
                    lineas.append("reserva %s → %s (dia %s, horario %s)" % (
                        res["quest_id"], res["npc"], res["dia_total"], res["horario"]))
        except Exception:
            pass

        # Como ve el controlador a cada quest viva.
        try:
            for q in store.sistema_quests.quests.values():
                if len(lineas) >= max_lineas:
                    lineas.append("… (mas quests sin listar)")
                    break
                try:
                    if not q.activa or q.completada or not getattr(q, "planificada", False):
                        continue
                    _b1 = getattr(q, "bloqueada_por", None)
                    if q.etapa_actual == ETAPA_CONDICIONES and _b1:
                        lineas.append("%s: espera para nacer (detras de %s)" % (q.id, _b1))
                        continue
                    if getattr(q, "narrativa_activa", False):
                        lineas.append("%s: en narrativa" % q.id)
                        continue
                    _est, _motivo = planificador_estado_guia(q)
                    if _est == "bloqueada":
                        lineas.append("%s: interrumpida (%s)" % (q.id, _motivo))
                    elif _est == "lista":
                        lineas.append("%s: disponible" % q.id)
                except Exception:
                    pass
        except Exception:
            pass

        return "\n".join(lineas) if lineas else "(nada pendiente)"

    def planificador_estado():
        """Resumen para la consola: que espera, que reserva, que bloquea."""
        lineas = []
        for q in store.sistema_quests.quests.values():
            if not q.activa or q.completada:
                continue
            _b1 = getattr(q, "bloqueada_por", None)
            _b2 = getattr(q, "bloqueo_activacion", None)
            _n = getattr(q, "narrativa_activa", False)
            if q.etapa_actual == ETAPA_CONDICIONES and _b1 is not None:
                lineas.append("%s  espera (capa 1) detras de %s" % (q.id, _b1))
            elif _b2:
                lineas.append("%s  bloqueada (capa 2): %s" % (q.id, _b2))
            elif _n:
                lineas.append("%s  en narrativa" % q.id)
        for res in getattr(store, "planificador_reservas", None) or []:
            if _pl_reserva_es_vida(res):
                lineas.append("reserva %s -> %s hasta completar" % (res["quest_id"], res["npc"]))
            else:
                lineas.append("reserva %s -> %s dia %d h %r" % (
                    res["quest_id"], res["npc"], res["dia_total"], res["horario"]))
        return "\n".join(lineas) if lineas else "(nada pendiente)"


# Reservas vivas: [{quest_id, npc, dia_total, horario, texto}]. Se guardan.
default planificador_reservas = []

# Contador de turnos para la cola FIFO de la capa 1 (esperando_desde).
default _planificador_turno = 0
