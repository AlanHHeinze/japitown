################################################################################
## Sistema de Hitos de relación — motor
################################################################################
## Un HITO es un nivel de relación con nombre que se alcanza alrededor de un
## umbral de amor o deseo, y que agrupa varias VENTAJAS bajo un solo concepto
## entendible para el jugador ("Buena relación") en vez de números sueltos.
##
## ESTE REGISTRO ES LA FUENTE DE VERDAD. Antes cada capacidad la decidia su
## propio sistema releyendo el stat por su cuenta, asi que cada umbral estaba
## escrito dos veces y ya se habian desfasado (el panel prometia ingreso con
## amor 30 y la tabla de puertas pedia 50). Ahora los sistemas preguntan
## `npc_tiene_ventaja(npc, ventaja_id)` y no leen stats para decidir.
##
## PERMANENCIA: un hito alcanzado NO se pierde aunque el stat baje despues
## (los stats pueden bajar: p.ej. una reaccion negativa resta amor). Se guarda
## en `hitos_alcanzados`, que es estado de la partida.
##
## Para AGREGAR hitos: characters/<npc>/hitos_<npc>.rpy, en init 6.
## Para AGREGAR ventajas: core/hitos/hitos_ventajas.rpy (o el archivo del
## contenido que la use, si es propia de una quest/evento).

# Hitos ya alcanzados por NPC: {npc_id: [hito_id, ...]}
# Solo strings — picklable sin riesgo.
default hitos_alcanzados = {}

# Puntos de quest ganados POR ENCIMA del tope, esperando a que se libere el
# tramo: {npc_id: {"amor": N, "deseo": N}}
#
# Por que una variable aparte y no sumarlos al stat del NPC: el stat lo leen los
# requisitos de quest, las condiciones de talk, el door access y los hitos. Si le
# metieramos puntos "virtuales" que el jugador todavia no tiene habilitados, todo
# eso se dispararia antes de tiempo. Manteniendolo afuera, el sobrante es pura
# contabilidad y no puede contaminar ninguna decision del juego.
#
# Lo unico que los suma es el CONTADOR del panel de Relaciones, que muestra
# stat + sobrante (ej. 7/5) para que el jugador vea lo que tiene ganado.
default sobrante_stat = {}


init python:

    # Catalogo de hitos por NPC: {npc_id: [Hito, ...]}
    # Vive en init y NO se guarda, igual que CATALOGO_ESPIAR y LINEAS_RELACION:
    # la partida solo guarda los IDS alcanzados, asi que agregar o retocar hitos
    # impacta en las partidas viejas sin necesidad de migrar nada.
    HITOS_NPC = {}

    # Stat de relacion → accessor. amor = stat1, deseo = stat2 (regla 2 del skill).
    _HITO_STAT_GETTER = {
        "amor":  lambda npc_id: obtener_stat1(npc_id),
        "deseo": lambda npc_id: obtener_stat2(npc_id),
    }


    class Hito(object):
        """
        Un nivel de relación con nombre.

        Args:
            id: identificador unico en todo el proyecto (ej. "violet_hito_amor_01")
            npc_id: NPC al que pertenece
            stat: "amor" o "deseo" — cual de los dos lo desbloquea
            nombre: nombre visible ("Buena relación"). Se traduce al mostrarlo.
            descripcion: texto opcional para el panel
            ventajas: lista de ids de ventaja (ver hitos_ventajas.rpy)
            icono: emoji para el panel
            umbral: valor del stat asociado. Es dato de PRESENTACION (lo usa el
                panel para ordenar y para mostrar "requiere X") y de coherencia
                (verificar_coherencia_hitos chequea que coincida con el
                Requisito de la quest). NO define el tope del stat: ese sale de
                las quests de la linea, ver tope_stat().
            quest_id: quest de relacion que OTORGA este hito. Llegar al umbral
                no alcanza: habilita la quest, y el hito se gana al completarla.
                None = hito sin quest, se otorga con solo alcanzar el umbral.
            proximamente: marcador de contenido que todavia no existe. NUNCA se
                otorga, asi que el panel lo muestra siempre en gris. Sirve para
                que el jugador vea que la linea sigue. Un hito asi no lleva
                ventajas ni quest_id.
        """
        def __init__(self, id, npc_id, stat, umbral, nombre,
                     descripcion="", ventajas=None, icono="⭐", quest_id=None,
                     proximamente=False):
            self.id          = id
            self.npc_id      = npc_id
            self.stat        = stat
            self.umbral      = umbral
            self.nombre      = nombre
            self.descripcion = descripcion
            self.ventajas    = list(ventajas) if ventajas else []
            self.icono       = icono
            self.quest_id    = quest_id
            self.proximamente = proximamente

        def valor_actual(self):
            """Valor que lleva hoy el stat que desbloquea este hito."""
            getter = _HITO_STAT_GETTER.get(self.stat)
            return getter(self.npc_id) if getter else 0

        def umbral_cumplido(self):
            """True si el stat YA alcanza el umbral (independiente de si se otorgó)."""
            return self.valor_actual() >= self.umbral

        def quest_completada(self):
            """True si la quest que otorga este hito ya esta completada."""
            if not self.quest_id:
                return False
            _q = store.sistema_quests.obtener_quest(self.quest_id)
            return bool(_q and _q.completada)

        def otorgable(self):
            """
            ¿Corresponde otorgar este hito ahora?

            Con quest: manda la quest completada — el umbral solo habilita la
            quest y frena el stat, no otorga nada por si mismo.
            Sin quest: alcanza con llegar al umbral.
            Marcado como proximamente: nunca, es solo un cartel.
            """
            if getattr(self, 'proximamente', False):
                return False
            if self.quest_id:
                return self.quest_completada()
            return self.umbral_cumplido()


    # ── Registro ─────────────────────────────────────────────────────────────

    def registrar_hito(hito):
        """Registra un hito. Lo llama cada NPC desde su hitos_<npc>.rpy en init 6."""
        HITOS_NPC.setdefault(hito.npc_id, [])
        HITOS_NPC[hito.npc_id] = [
            h for h in HITOS_NPC[hito.npc_id] if h.id != hito.id
        ] + [hito]

    def obtener_hitos_npc(npc_id, stat=None):
        """Hitos de un NPC, opcionalmente de un solo stat, ordenados por umbral."""
        rv = list(HITOS_NPC.get(npc_id, []))
        if stat is not None:
            rv = [h for h in rv if h.stat == stat]
        rv.sort(key=lambda h: h.umbral)
        return rv

    def obtener_hito(hito_id):
        """Busca un hito por id en todo el catalogo, o None."""
        for _lista in HITOS_NPC.values():
            for _h in _lista:
                if _h.id == hito_id:
                    return _h
        return None

    def texto_hito_corto(hito_id):
        """
        Etiqueta corta de un hito para pistas y que_hacer: "❤️ Buena relación".

        Se arma desde el catalogo en vez de escribir el nombre a mano, asi los
        textos siguen al hito si se lo renombra (los nombres actuales son
        provisorios). Devuelve "" si el hito no existe, para que un id mal
        escrito no rompa la pista.
        """
        _h = obtener_hito(hito_id)
        if not _h:
            return ""
        return u"{} {}".format(_h.icono, renpy.translate_string(_h.nombre))

    def etiqueta_opcion_hito(texto, hito_id):
        """
        Etiqueta de una opcion de eleccion que pide un hito:

            "Ya esta resuelto (Buena relación ❤️)"

        CONVENCION DEL PROYECTO: toda opcion especial que pida un hito muestra
        entre parentesis el NOMBRE del hito y su emoji (❤️ amor / 💋 deseo). La
        opcion se ve siempre; sin el hito queda en gris. Asi el jugador sabe que
        existe y exactamente que le falta, sin abrir el panel de Relaciones.

        Es la version "hito" de las opciones por stat del MC, que ya usaban el
        mismo criterio con otro formato ("Acercarse  🎯 (3 de destreza)").

        El nombre sale del CATALOGO y no se escribe a mano: los hitos se
        renombran seguido y asi la opcion sigue al nombre nuevo sola. Si el id
        no existe devuelve el texto pelado, para que un id mal escrito no deje
        la opcion sin etiqueta.
        """
        _t = renpy.translate_string(texto)
        _h = obtener_hito(hito_id)
        if not _h:
            return _t
        return u"{} ({} {})".format(_t, renpy.translate_string(_h.nombre),
                                    _h.icono)


    # ── Consulta ─────────────────────────────────────────────────────────────

    def tiene_hito(npc_id, hito_id):
        """True si el jugador ya alcanzó ese hito con ese NPC."""
        return hito_id in store.hitos_alcanzados.get(npc_id, [])

    def hito_alcanzado(hito_id):
        """
        tiene_hito() para quien solo conoce el id del hito.

        El npc ya vive adentro del hito, asi que pedirlo de nuevo es una
        oportunidad de escribirlo mal. Es el predicado que va en el `sensitive`
        de las opciones etiquetadas con etiqueta_opcion_hito().
        """
        _h = obtener_hito(hito_id)
        return bool(_h and tiene_hito(_h.npc_id, hito_id))

    def ventajas_activas(npc_id):
        """Set con los ids de todas las ventajas que el NPC tiene otorgadas."""
        rv = set()
        _alcanzados = store.hitos_alcanzados.get(npc_id, [])
        for _h in HITOS_NPC.get(npc_id, []):
            if _h.id in _alcanzados:
                rv.update(_h.ventajas)
        return rv

    def npc_tiene_ventaja(npc_id, ventaja_id):
        """
        LA API que consultan los sistemas. True si algun hito ya alcanzado con
        ese NPC otorga esa ventaja.

        Ejemplo: if npc_tiene_ventaja("violet", "puerta_dejar_pasar"): ...
        """
        return ventaja_id in ventajas_activas(npc_id)


    # ── Tope de stat ─────────────────────────────────────────────────────────

    def _umbral_quest_relacion(quest):
        """
        Umbral de stat que pide una quest de linea, leido de su propio Requisito.
        None si no es una quest de linea o no declara umbral.

        La quest es la unica fuente del numero: asi el tope y el requisito no
        pueden desfasarse, que es todo el punto de este sistema.
        """
        _linea = getattr(quest, "linea", LINEA_PRINCIPAL)
        if _linea not in _HITO_STAT_GETTER:
            return None
        for _req in quest.requisitos:
            # El tipo de Requisito ("amor"/"deseo") coincide con el nombre de linea
            if _req.tipo == _linea:
                return _req.params.get("valor", 0)
        return None

    # Topes provisorios: hasta donde llega el contenido de una linea mientras la
    # proxima quest todavia no exista. Sin esto, terminada la ultima quest el
    # stat queda libre hasta 100 y el jugador sube sin nada que desbloquear.
    # {(npc_id, stat): valor}
    TOPES_PROVISORIOS = {}

    def registrar_tope_provisorio(npc_id, stat, valor):
        """
        Declara hasta donde puede subir un stat mientras no haya mas quests.

        Lo registra el contenido junto a su linea (ej. quests_amor_violet.rpy).
        Al crear la quest que falta, se sube el valor o se borra la linea.
        """
        TOPES_PROVISORIOS[(npc_id, stat)] = valor

    def tope_stat(npc_id, stat):
        """
        Hasta donde puede subir hoy ese stat.

        Es el umbral de la primera QUEST de esa linea que todavia no este
        completada: cada quest frena su tramo. O sea 0→5 topeado en 5, se juega
        la quest de 5, se libera hasta 10, y asi. Cuando no queda ninguna quest
        de la linea sin completar, no hay tope (100).

        OJO — depende de las QUESTS, no de los hitos. Son dos cosas distintas:
        toda quest de linea frena su tramo, pero solo algunas otorgan un hito
        con nombre y ventajas (en Violet, las de 10 / 20 / 30). Si el tope
        dependiera de los hitos, las quests intermedias no frenarian nada.

        Sin quests de linea para ese npc/stat tampoco hay tope, asi que un NPC
        sin linea de relacion se comporta como antes.

        Lo aplica modificar_stat1/2 (npcsystem_core) y lo muestra el panel de
        Relaciones.
        """
        _pendientes = []
        for _q in store.sistema_quests.quests.values():
            if _q.npc_id != npc_id or _q.completada:
                continue
            if getattr(_q, "linea", LINEA_PRINCIPAL) != stat:
                continue
            _u = _umbral_quest_relacion(_q)
            if _u is not None:
                _pendientes.append(_u)

        # El tope provisorio entra al min como una quest mas: si todavia quedan
        # quests por delante manda la mas cercana, y cuando no queda ninguna
        # queda el provisorio en vez del 100 de "sin tope".
        _prov = TOPES_PROVISORIOS.get((npc_id, stat))
        if _prov is not None:
            _pendientes.append(_prov)

        return min(_pendientes) if _pendientes else 100

    def stat_topeado(npc_id, stat):
        """True si el stat ya llego a su tope y no puede subir mas."""
        _getter = _HITO_STAT_GETTER.get(stat)
        if not _getter:
            return False
        return _getter(npc_id) >= tope_stat(npc_id, stat)


    # ── Sobrante: puntos de quest ganados por encima del tope ────────────────

    def sobrante_de(npc_id, stat):
        """Puntos en reserva para ese npc/stat."""
        return store.sobrante_stat.get(npc_id, {}).get(stat, 0)

    def sumar_sobrante(npc_id, stat, cantidad):
        """
        Guarda en la reserva puntos de quest que no entraron por el tope.
        La llama _aplicar_cambio_stat (npcsystem_core) con reserva=True.
        """
        if cantidad <= 0:
            return
        _res_npc = dict(store.sobrante_stat.get(npc_id, {}))
        _res_npc[stat] = _res_npc.get(stat, 0) + cantidad
        # Se reasigna el dict entero para que el rollback lo trackee.
        store.sobrante_stat = dict(store.sobrante_stat, **{npc_id: _res_npc})

    def stat_mostrado(npc_id, stat):
        """
        Valor para MOSTRAR en la UI: el real mas lo que espera en reserva.

        Solo para el contador del panel. Ninguna decision del juego usa esto —
        requisitos, condiciones de talk, door access e hitos leen el stat real.
        """
        _getter = _HITO_STAT_GETTER.get(stat)
        _actual = _getter(npc_id) if _getter else 0
        return _actual + sobrante_de(npc_id, stat)

    def liberar_sobrantes():
        """
        Vuelca la reserva al stat real cuando se abre espacio bajo el tope, o
        sea cuando el jugador completo la quest que lo estaba frenando.

        La llama el trigger de game_loop, junto con actualizar_hitos().

        Escribe con establecer_stat1/2 y NO con modificar_stat1/2 a proposito:
        modificar aplicaria el tope otra vez y devolveria los puntos a la
        reserva, en un ida y vuelta infinito. El valor se calcula aca contra el
        tope, asi que nunca puede pasarse.

        Si la reserva es mas grande que el tramo que se abrio, queda el resto
        guardado para el tramo siguiente.
        """
        for _npc_id, _stats in list(store.sobrante_stat.items()):
            _npc = obtener_npc(_npc_id)
            if _npc is None:
                continue

            for _stat, _reserva in list(_stats.items()):
                if _reserva <= 0:
                    continue
                _getter = _HITO_STAT_GETTER.get(_stat)
                if not _getter:
                    continue

                _actual = _getter(_npc_id)
                _espacio = min(100, tope_stat(_npc_id, _stat)) - _actual
                if _espacio <= 0:
                    continue

                _aplicar = min(_espacio, _reserva)

                if _stat == _npc.nombre_stat1:
                    _npc.establecer_stat1(_actual + _aplicar)
                elif _stat == _npc.nombre_stat2:
                    _npc.establecer_stat2(_actual + _aplicar)
                else:
                    continue

                _res_npc = dict(store.sobrante_stat.get(_npc_id, {}))
                _res_npc[_stat] = _reserva - _aplicar
                store.sobrante_stat = dict(store.sobrante_stat, **{_npc_id: _res_npc})

                if hasattr(store, 'notificar_cambio_stat'):
                    notificar_cambio_stat(_stat, _aplicar, _npc.nombre)


    # ── Detección y otorgamiento ─────────────────────────────────────────────

    def _aplicar_ventajas_hito(hito):
        """
        Corre los handlers `aplicar` de las ventajas del hito (las que los tienen).
        Las CONSULTABLES no hacen nada acá: se preguntan cuando hacen falta.

        No revienta nunca: una ventaja mal declarada no puede dejar el hito a
        medio otorgar. En modo desarrollador el error igual se ve por consola.
        """
        for _vid in hito.ventajas:
            _cfg = VENTAJAS_HITO.get(_vid)
            if _cfg is None:
                if config.developer:
                    print("[Hitos] {}: ventaja desconocida '{}'".format(hito.id, _vid))
                continue
            _fn = _cfg.get("aplicar")
            if _fn is None:
                continue          # consultable: nada que aplicar
            try:
                _fn(hito.npc_id)
            except Exception as _e:
                if config.developer:
                    print("[Hitos] {}: fallo al aplicar '{}': {}".format(hito.id, _vid, _e))

    def actualizar_hitos():
        """
        Otorga los hitos que corresponden y todavia no estaban dados.

        "Corresponde" lo decide Hito.otorgable(): con quest_id manda la quest
        completada, sin quest_id alcanza con el umbral. Llegar al umbral NO
        otorga el hito cuando hay quest — solo habilita esa quest y frena el
        stat (ver tope_stat).

        La engancha un trigger de game_loop (ver el registro mas abajo) y no
        Quest.completar(), para que valga tambien para los hitos sin quest y
        para que un save viejo se ponga al dia en la primera vuelta.

        Tambien funciona retroactivamente: en un save anterior a este sistema,
        `hitos_alcanzados` arranca vacio y la primera vuelta del loop otorga
        todos los que el jugador ya tenia merecidos.

        Returns:
            list[Hito]: los hitos otorgados en esta pasada (vacia casi siempre).
            Sirve para notificar al jugador desde el caller.
        """
        nuevos = []

        for _npc_id, _lista in HITOS_NPC.items():
            _alcanzados = list(store.hitos_alcanzados.get(_npc_id, []))
            _cambio = False

            for _h in _lista:
                if _h.id in _alcanzados:
                    continue
                if not _h.otorgable():
                    continue
                _alcanzados.append(_h.id)
                _cambio = True
                _aplicar_ventajas_hito(_h)
                nuevos.append(_h)

            if _cambio:
                # Se reasigna el dict entero (no se muta in place) para que el
                # rollback de Ren'Py trackee el cambio de forma confiable.
                store.hitos_alcanzados = dict(
                    store.hitos_alcanzados, **{_npc_id: _alcanzados}
                )

        if nuevos and config.developer:
            print("[Hitos] otorgados: {}".format(", ".join(h.id for h in nuevos)))

        return nuevos


    # ── Verificación de desarrollo ───────────────────────────────────────────

    def verificar_coherencia_hitos():
        """
        Chequeo de desarrollo: que todo lo declarado exista y sea consistente.
        Se corre desde la consola (Shift+O) o desde el harness de tests.

        Returns:
            list[str]: problemas encontrados (vacia = todo bien).
        """
        problemas = []
        vistos = {}

        for _npc_id, _lista in HITOS_NPC.items():
            for _h in _lista:
                # ids unicos en todo el proyecto
                if _h.id in vistos:
                    problemas.append("{}: id repetido (tambien en '{}')".format(
                        _h.id, vistos[_h.id]))
                vistos[_h.id] = _npc_id

                # stat valido
                if _h.stat not in _HITO_STAT_GETTER:
                    problemas.append("{}: stat '{}' no es amor ni deseo".format(
                        _h.id, _h.stat))

                # el npc existe
                if obtener_npc(_h.npc_id) is None:
                    problemas.append("{}: el NPC '{}' no existe".format(
                        _h.id, _h.npc_id))

                # toda ventaja referenciada esta registrada, y tiene texto para
                # el panel de Desbloqueos. Sin descripcion la ventaja igual
                # funciona, pero al jugador le aparece un nombre suelto sin
                # explicacion — por eso se avisa acá y no en runtime.
                for _vid in _h.ventajas:
                    if _vid not in VENTAJAS_HITO:
                        problemas.append("{}: ventaja '{}' sin registrar".format(
                            _h.id, _vid))
                    elif not VENTAJAS_HITO[_vid].get("descripcion"):
                        problemas.append("{}: ventaja '{}' sin descripcion".format(
                            _h.id, _vid))

                # la quest que otorga el hito existe, y su Requisito de stat
                # pide el MISMO umbral que declara el hito. Un typo en quest_id
                # dejaria el hito inotorgabale para siempre y sin sintoma; un
                # umbral desfasado es exactamente la clase de mentira que este
                # sistema vino a eliminar.
                if _h.quest_id:
                    _q_h = store.sistema_quests.obtener_quest(_h.quest_id)
                    if _q_h is None:
                        problemas.append("{}: quest_id '{}' no existe".format(
                            _h.id, _h.quest_id))
                    else:
                        for _req_h in _q_h.requisitos:
                            if _req_h.tipo == _h.stat:
                                _val_h = _req_h.params.get("valor", 0)
                                if _val_h != _h.umbral:
                                    problemas.append(
                                        "{}: umbral {} pero su quest '{}' pide {} de {}".format(
                                            _h.id, _h.umbral, _h.quest_id, _val_h, _h.stat))

        if config.developer:
            if problemas:
                for _p in problemas:
                    print("[Hitos] " + _p)
            else:
                print("[Hitos] OK: {} hitos en {} NPCs".format(
                    len(vistos), len(HITOS_NPC)))
        return problemas


# =============================================================================
# Trigger de detección
# =============================================================================
# Va por el registro de triggers (§4 del skill) y no hardcodeado en el loop.
# Devuelve None SIEMPRE: hace su efecto y el flujo del game_loop sigue.

init python:

    def _trigger_actualizar_hitos():
        # Primero se liberan los sobrantes (el tope pudo subir al completarse
        # una quest) y despues se evaluan los hitos, para que un hito que
        # dependa del stat ya vea el valor actualizado.
        liberar_sobrantes()
        actualizar_hitos()
        return None

init 5 python:

    registrar_trigger_game_loop("hitos_actualizar", _trigger_actualizar_hitos, prioridad=0)
