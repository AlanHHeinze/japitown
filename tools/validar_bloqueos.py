# -*- coding: utf-8 -*-
"""
Busca BLOQUEOS SIN SALIDA: formas de dejar al jugador trabado que el lint no ve.

Un bloqueo (restriccion, bloqueo de accion, mensaje prioritario) es sano solo si
su salida existe SIEMPRE. Este script lee el codigo y avisa de las cuatro formas
en que este proyecto ya rompio esa regla, cada una con un jugador detras
(auditoria 2026-09-10, skill japitown-warnings):

  1. RELOJ QUE SE ESCAPA — una restriccion bloquea avanzar_tiempo o dormir pero
     deja libre alguna otra accion que tambien mueve el horario (ver TV,
     entrenar, trabajar, cocinar, el talk...). El jugador cae en otro horario
     y la salida, que asumia el original, ya no existe. Fix: congelar_reloj=True.
     Si el reloj queda libre A PROPOSITO (la salida es dormir, o ver TV), se
     declara en la linea de arriba: `# validar_bloqueos: reloj libre — motivo`.

  2. REGISTRO EN RUNTIME — registrar_listener() o registrar_accion() dentro de
     un label. sistema_acciones es `define`: al cargar la partida el registro
     desaparece y la accion que era la salida no dispara. Fix: al catalogo, en
     init, con condicion por flag.

  3. SALIDA DETRAS DE UN MENU DE PUERTA — registrar_opcion_puerta con
     ocultar_golpear=True ("esta es LA cosa que hay que hacer") sin un
     registrar_override_puerta de la misma quest. El menu se arma despues del
     chequeo de trasnoche y del nivel de acceso: la opcion puede no dibujarse
     nunca. Se lista para revisar, no es error seguro.

  4. TRIGGER QUE PISA A OTRO — un trigger de game_loop cuyo label llama a
     desactivar_restriccion() sin preguntar si su NPC esta oculto. Si otro
     contenido tiene una restriccion activa con el NPC escondido, este se
     dispara igual y se la lleva puesta. Fix: declarar `duenio=` en
     registrar_trigger_game_loop — el motor ignora el label de un trigger
     ajeno mientras hay una restriccion con dueño activa.

  5. RESTRICCION SIN QUIEN LA LEVANTE — un `duenio` que aparece en algun
     activar_restriccion pero en ningun desactivar_restriccion. El slot queda
     ocupado para siempre (npc_disponibilidad tiene el mismo riesgo: quien
     apaga tiene que volver a prender).

  6. SALIDA QUE NECESITA A UN NPC SIN RUTINA QUE LO GARANTICE — una restriccion
     que congela el reloj y cuya salida pasa por la puerta de un NPC (override u
     opcion de puerta en el mismo archivo), en una quest que NO declara
     rutina_quest. De noche Violet puede estar en el living (domingo), en el
     baño (25%) o afuera (20%): con la puerta vacia y el reloj congelado no hay
     salida. REGLA: si la salida necesita al NPC en un lugar a una hora, la
     quest lleva la rutina que lo pone ahi (como deseo 25, deseo 30, amor 25 y
     04_d4).

  7. PLANIFICADOR DESALINEADO — el planificador (core/quests/planificador.rpy)
     decide con lo que cada quest DECLARA en planificacion_<npc>.rpy. Si una
     quest no declara nada, no la ve (nace y se activa como antes); si declara
     una rutina que no tiene, o tiene una rutina que no declara, la capa 1 se
     equivoca en silencio. Se listan: quests del catalogo sin
     declarar_planificacion, quests que no demandan a su propio NPC (toda
     quest lo hace: una reserva sobre el NPC tiene que frenarla), quests con
     rutina_quest sin consumo `npc` declarado, y consumos `npc` con `en` en
     quests sin rutina_quest.

  8. PERSONAJE PRESTADO SIN DEMANDA — en los labels de una quest habla o se
     muestra un NPC que no es el suyo (Jasmine en la 04_a de Violet) y la
     declaracion no lo pide con Rec("npc", "<otro>", ...). Sin la demanda la
     capa 2 no mira si esta en la casa ni si esta reservado por otra quest, y
     aparece en la escena aunque este afuera o enferma. Se cruzan los
     archivos de la quest (los que nombran su id) con planificacion_<npc>.rpy;
     los labels de test (`label test_`) no cuentan.

  9. LOCACION CERRADA SIN QUIEN LA ABRA — registrar_bloqueo_locacion() cierra
     una locacion mientras su condicion sea verdadera. Si ninguna de las flags
     que lee esa condicion se apaga en ningun lado (no hay `flag = False` fuera
     de la propia condicion), la locacion queda cerrada para siempre. Es la
     version por locacion del caso 5, y mas facil de dejar colgada porque no
     hay un desactivar_ explicito: la salida es apagar la flag.

USO
    python tools/validar_bloqueos.py

Hermano de validar_traducciones.py y validar_sprites.py.
"""
import io
import os
import re

# Lo mismo que ACCIONES_RELOJ en restriccion_quest_system.rpy. Se lee de ahi
# para no tener dos listas.
def _acciones_reloj():
    ruta = "game/script/core/quests/restriccion_quest_system.rpy"
    t = io.open(ruta, encoding="utf-8").read()
    m = re.search(r'ACCIONES_RELOJ\s*=\s*\((.*?)\)', t, re.S)
    if not m:
        return set()
    return set(re.findall(r'"(\w+)"', m.group(1)))


ACCIONES_RELOJ = _acciones_reloj()

archivos = []
for base, _, fs in os.walk("game/script"):
    for f in sorted(fs):
        if f.endswith(".rpy"):
            archivos.append(os.path.join(base, f).replace("\\", "/"))


def _corto(r):
    return r.replace("game/script/", "")


def _llamada(lineas, i):
    """Texto de una llamada desde la linea i hasta cerrar el parentesis."""
    buf, depth, started = [], 0, False
    for j in range(i, min(i + 60, len(lineas))):
        l = lineas[j]
        buf.append(l)
        for ch in l:
            if ch == "(":
                depth += 1
                started = True
            elif ch == ")":
                depth -= 1
        if started and depth <= 0:
            break
    return "\n".join(buf)


# ── 1. Reloj que se escapa ──────────────────────────────────────────────────
reloj = []
for r in archivos:
    if r.endswith("restriccion_quest_system.rpy") or "/test_rutas.rpy" in r:
        continue
    lineas = io.open(r, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lineas):
        if l.strip().startswith("#") or "desactivar" in l:
            continue
        if "activar_restriccion(" not in l:
            continue
        t = _llamada(lineas, i)
        if "congelar_reloj=True" in t:
            continue
        # Excepcion declarada: la linea de arriba dice por que el reloj queda
        # libre a proposito (la salida ES una accion de reloj, o es un gate
        # blando). Sin motivo escrito no vale.
        if i > 0 and "validar_bloqueos: reloj libre" in lineas[i - 1]:
            continue
        m = re.search(r'acciones_bloqueadas\s*=\s*\[(.*?)\]', t, re.S)
        if not m:
            continue
        bloq = set(re.findall(r'"(\w+)"', m.group(1)))
        if not bloq & {"avanzar_tiempo", "dormir"}:
            continue                       # no pretende frenar el reloj

        # Solo cuentan las acciones que el jugador PUEDE alcanzar desde esta
        # restriccion. Una accion de locacion fuera de la whitelist, o el talk
        # con todos los NPCs vedados, no son escapes.
        ml = re.search(r'locaciones_permitidas\s*=\s*(\[.*?\]|None|\w+)', t, re.S)
        locs_txt = ml.group(1) if ml else "None"
        if locs_txt.startswith("["):
            locs = set(re.findall(r'"(\w+)"', locs_txt))
        else:
            locs = None                    # None o una variable: se asume todo
        mi = re.search(r'npcs_interactuables\s*=\s*\[(.*?)\]', t, re.S)
        hay_npcs = bool(mi and re.findall(r'"(\w+)"', mi.group(1)))

        def _alcanzable(acc):
            if acc in ("avanzar_tiempo", "dormir"):
                return False               # si esta libre, es la salida
            if acc == "hablar":
                return hay_npcs
            if locs is None:
                return True
            if acc == "cocinar":
                return "casa_cocina" in locs
            if acc == "ver_tv":
                return bool(locs & {"casa_living", "casa_sotano"})
            if acc in ("entrenar", "trabajar"):
                return bool(locs & {"casa_hmc", "casa_gym"})
            return True                    # usar_item y lo que venga

        faltan = sorted(a for a in ACCIONES_RELOJ - bloq if _alcanzable(a))
        if faltan:
            reloj.append((r, i + 1, faltan))

# ── 2. Registro en runtime ──────────────────────────────────────────────────
runtime = []
RE_LABEL = re.compile(r'^label\s+[\w.]+\s*:')
RE_INIT = re.compile(r'^init(\s+-?\d+)?\s+python\s*:')
for r in archivos:
    if r.endswith("actions_catalog.rpy"):
        continue
    lineas = io.open(r, encoding="utf-8").read().split("\n")
    en_label = False
    for i, l in enumerate(lineas):
        if RE_LABEL.match(l):
            en_label = True
        elif RE_INIT.match(l) or re.match(r'^(screen|define|default|image|transform)\s', l):
            en_label = False
        if not en_label or l.strip().startswith("#"):
            continue
        if re.search(r'\b(registrar_listener|registrar_accion)\s*\(', l):
            runtime.append((r, i + 1, l.strip()[:80]))

# ── 3. Salida detras de un menu de puerta ───────────────────────────────────
puerta = []
overrides = set()
for r in archivos:
    t = io.open(r, encoding="utf-8").read()
    for m in re.finditer(r'registrar_override_puerta\(\s*"(\w+)"', t):
        overrides.add(r)
for r in archivos:
    lineas = io.open(r, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lineas):
        if "registrar_opcion_puerta(" not in l or l.strip().startswith("#"):
            continue
        t = _llamada(lineas, i)
        if "ocultar_golpear=True" not in t:
            continue
        mt = re.search(r'registrar_opcion_puerta\(\s*"\w+",\s*"([^"]+)"', t)
        texto = mt.group(1) if mt else "?"
        # Si el mismo archivo registra un override, se asume que el caso
        # delicado ya esta cubierto por ahi.
        if r in overrides:
            continue
        puerta.append((r, i + 1, texto))

# ── 4. Trigger que pisa a otro ──────────────────────────────────────────────
pisa = []
for r in archivos:
    t = io.open(r, encoding="utf-8").read()
    # Triggers de game_loop registrados en este archivo y su funcion.
    for m in re.finditer(r'registrar_trigger_game_loop\(\s*"[^"]+",\s*(\w+)', t):
        fn = m.group(1)
        # Con `duenio` declarado, el motor ya no lo deja saltar adentro de la
        # restriccion de otro (triggers_contenido): no hay nada que revisar.
        fin_llamada = t.find(")", m.end())
        if 'duenio=' in t[m.start():fin_llamada + 1]:
            continue
        mf = re.search(r'def %s\s*\(\):(.*?)(?=\n    def |\ninit |\nlabel |\Z)' % fn, t, re.S)
        if not mf:
            continue
        cuerpo = mf.group(1)
        if "npc_esta_oculto" in cuerpo or "npc_interactuable" in cuerpo \
                or "tracker_locacion_npc" in cuerpo or "hay_restriccion_activa" in cuerpo:
            continue
        # Labels que devuelve.
        labels = re.findall(r'return\s+"([\w.]+)"', cuerpo)
        for lb in labels:
            ml = re.search(r'^label %s\s*:(.*?)(?=^label |\Z)' % re.escape(lb), t, re.S | re.M)
            if ml and "desactivar_restriccion(" in ml.group(1):
                pisa.append((r, fn, lb))

# ── 5. Restriccion sin quien la levante ─────────────────────────────────────
activan, levantan = {}, set()
for r in archivos:
    if r.endswith("restriccion_quest_system.rpy"):
        continue
    t = io.open(r, encoding="utf-8").read()
    for m in re.finditer(r'(?<!des)activar_restriccion\(\s*duenio="([^"]+)"', t):
        activan.setdefault(m.group(1), set()).add(_corto(r))
    for m in re.finditer(r'desactivar_restriccion\(duenio="([^"]+)"\)', t):
        levantan.add(m.group(1))
huerfanas = sorted(d for d in activan if d not in levantan and d not in ("test",))

# ── 6. Salida por puerta de NPC sin rutina que lo garantice ────────────────
# Catalogos donde una quest puede declarar rutina_quest.
CATALOGOS = [r for r in archivos if r.endswith((
    "quests/quest_violet.rpy", "deseo/quests_deseo_violet.rpy",
    "amor/quests_amor_violet.rpy", "quests/quest_monica.rpy",
    "quests/quest_jasmine.rpy", "quests/quest_mc.rpy"))]
cat_txt = "\n".join(io.open(c, encoding="utf-8").read() for c in CATALOGOS)


def _quest_con_rutina(qid):
    """
    True si la quest `qid` declara rutina_quest en algun catalogo.

    Dos formas de declararla: en el Quest(...) directo (id="qid" ... rutina_quest=)
    o en las tablas de las lineas de deseo/amor, donde la entrada es el NUMERO
    (_VIOLET_DESEO_TEXTOS[5] para violet_deseo_05, _VIOLET_AMOR_RUTINAS[5]
    para violet_amor_05).
    """
    m = re.search(r'id="%s"(.*?)sistema_quests\.registrar_quest' % re.escape(qid),
                  cat_txt, re.S)
    if m and "rutina_quest" in m.group(1):
        return True
    mn = re.match(r'violet_(deseo|amor)_0?(\d+)$', qid)
    if mn:
        linea, n = mn.group(1), int(mn.group(2))
        # Solo el catalogo de ESA linea: las dos tablas usan los mismos numeros
        # y buscando en todo junto se cruzan.
        cat_linea = "\n".join(io.open(c, encoding="utf-8").read() for c in CATALOGOS
                              if c.endswith("quests_%s_violet.rpy" % linea))
        # _VIOLET_AMOR_RUTINAS[5] = { ... }
        if re.search(r'_VIOLET_AMOR_RUTINAS\[%d\]\s*=' % n, cat_linea):
            return True
        # _VIOLET_DESEO_TEXTOS = { ..., 5: { ... "rutina_quest": ... }, ... }
        # El bloque de la entrada termina en el `},` con la sangria de la
        # entrada (8 espacios); los `},` mas adentro tienen mas.
        mt = re.search(r'\n {8}%d:\s*\{(.*?)\n {8}\},' % n, cat_linea, re.S)
        if mt and "rutina_quest" in mt.group(1):
            return True
    return False


sin_rutina = []
for r in archivos:
    if r.endswith("restriccion_quest_system.rpy") or "/test_rutas.rpy" in r:
        continue
    t = io.open(r, encoding="utf-8").read()
    # Congela el reloj en algun lado?
    congela = ("congelar_reloj=True" in t) or bool(re.search(
        r'acciones_bloqueadas\s*=\s*\[[^\]]*"avanzar_tiempo"[^\]]*"dormir"', t, re.S))
    if not congela:
        continue
    # La salida pasa por la puerta de un NPC?
    puertas = set(re.findall(r'registrar_(?:override|opcion)_puerta\(\s*"(\w+)"', t))
    if not puertas:
        continue
    # Que quest es?
    qids = set(re.findall(r'quest_lista_para_boton\("(\w+)"\)', t)) | \
           set(re.findall(r'quest_id="(\w+)"', t))
    if not qids:
        sin_rutina.append((r, ", ".join(sorted(puertas)), "?"))
        continue
    for qid in sorted(qids):
        if not _quest_con_rutina(qid):
            sin_rutina.append((r, ", ".join(sorted(puertas)), qid))


# ── 7. Planificador desalineado ─────────────────────────────────────────────
# Quests del catalogo (Quest(id=...) directo y las tablas de deseo/amor).
quests_catalogo = set(re.findall(r'\n\s+id="((?:violet|monica|jasmine)_\w+)",', cat_txt))
for c in CATALOGOS:
    if c.endswith(("quests_deseo_violet.rpy", "quests_amor_violet.rpy")):
        linea = "deseo" if "deseo" in c else "amor"
        tc = io.open(c, encoding="utf-8").read()
        mt = re.search(r'_VIOLET_%s_QUESTS\s*=\s*\[(.*?)\n    \]' % linea.upper(), tc, re.S)
        if mt:
            for n in re.findall(r'\(\s*(\d+),\s*\d+,\s*"', mt.group(1)):
                quests_catalogo.add("violet_%s_%02d" % (linea, int(n)))

# Declaraciones: planificacion_<npc>.rpy
decl = {}
for r in archivos:
    if not r.endswith(("planificacion_violet.rpy", "planificacion_monica.rpy",
                       "planificacion_jasmine.rpy")):
        continue
    t = io.open(r, encoding="utf-8").read()
    for m in re.finditer(r'declarar_planificacion\("(\w+)"(.*?)\n\n', t + "\n\n", re.S):
        decl[m.group(1)] = m.group(2)

planif = []
for qid in sorted(quests_catalogo):
    if qid not in decl:
        planif.append((qid, "sin declarar_planificacion"))
        continue
    cuerpo = decl[qid]
    npc = qid.split("_")[0]
    md = re.search(r'demandas=\[(.*?)\]', cuerpo, re.S)
    if not (md and re.search(r'Rec\("npc",\s*"%s"' % npc, md.group(1))):
        planif.append((qid, "no demanda a su propio NPC (Rec(\"npc\", \"%s\"))" % npc))
    mc = re.search(r'consumos=\[(.*?)\]', cuerpo, re.S)
    consumos = mc.group(1) if mc else ""
    consume_npc = bool(re.search(r'Rec\("npc"', consumos))
    if _quest_con_rutina(qid) and not consume_npc:
        planif.append((qid, "tiene rutina_quest pero no declara consumo npc"))
    if consume_npc and re.search(r'Rec\("npc"[^)]*en=', consumos) and not _quest_con_rutina(qid):
        planif.append((qid, "declara consumo npc con `en` pero no tiene rutina_quest"))


# ── 8. Personaje prestado sin demanda ───────────────────────────────────────
NPCS = ("violet", "monica", "jasmine")
_PAT_APARECE = {n: re.compile(
    r'^\s*(%s|%s_susurro|%s_piensa)\s+"|^\s*show\s+%s\b|^\s*show\s+\w*%s\w*\s' % (n, n, n, n, n), re.M)
    for n in NPCS}


def _sin_labels_de_test(t):
    """Corta lo que cuelga de un `label test_...` hasta el siguiente label."""
    return re.sub(r'^label test_\w+:.*?(?=^label |\Z)', '', t, flags=re.M | re.S)


prestados = []
for qid in sorted(quests_catalogo):
    if qid not in decl:
        continue
    npc = qid.split("_")[0]
    md = re.search(r'demandas=\[(.*?)\]', decl[qid], re.S)
    demandados = set(re.findall(r'Rec\("npc",\s*"(\w+)"', md.group(1))) if md else set()
    # Archivos de la quest: los que la nombran y NO son catalogos ni menus.
    for r in archivos:
        if not r.startswith("game/script/characters/%s/" % npc):
            continue
        if r.endswith(("quest_%s.rpy" % npc, "quests_deseo_violet.rpy", "quests_amor_violet.rpy",
                       "planificacion_%s.rpy" % npc)) or "/interaction/" in r:
            continue
        t = io.open(r, encoding="utf-8").read()
        if ('"%s"' % qid) not in t:
            continue
        t = _sin_labels_de_test(t)
        for otro in NPCS:
            if otro == npc or otro in demandados:
                continue
            if _PAT_APARECE[otro].search(t):
                prestados.append((qid, otro, _corto(r)))


# ── 9. Locacion cerrada sin quien la abra ───────────────────────────────────
_PAT_BLOQ_LOC = re.compile(
    r'registrar_bloqueo_locacion\(\s*"(\w+)"\s*,\s*([\w.]+)\s*,')
# Nombres que no son flags de contenido (builtins, helpers del motor).
_NO_FLAG = {"self", "store", "renpy", "config", "True", "False", "None",
            "return", "and", "or", "not", "if", "in", "is", "def"}

_todo_el_codigo = None
loc_cerradas = []
for r in archivos:
    t = io.open(r, encoding="utf-8").read()
    if "def registrar_bloqueo_locacion(" in t:
        continue  # el motor: lo que hay ahi es el ejemplo del docstring
    for loc, fn in _PAT_BLOQ_LOC.findall(t):
        cuerpo = re.search(
            r'\n(\s*)def %s\(\s*\):\n(.*?)(?=\n\1def |\n\1[^\s#\n]|\n\S|\Z)'
            % re.escape(fn.split(".")[-1]), t, re.S)
        if cuerpo is None:
            loc_cerradas.append((_corto(r), loc, "no encuentro la condicion %s()" % fn))
            continue
        flags = set(re.findall(r'\b([a-z_]\w*)\b', cuerpo.group(2))) - _NO_FLAG
        if _todo_el_codigo is None:
            _todo_el_codigo = "".join(
                io.open(a, encoding="utf-8").read() for a in archivos)
        # ¿Alguna de las flags se apaga en algun lado, fuera de la condicion?
        apagable = any(
            re.search(r'\b%s\s*=\s*(False|0|None)\b' % re.escape(f), _todo_el_codigo)
            for f in flags)
        if not apagable:
            loc_cerradas.append((
                _corto(r), loc,
                "nada apaga la condicion %s() (%s)" % (fn, ", ".join(sorted(flags)) or "sin flags")))


# ── Informe ─────────────────────────────────────────────────────────────────
print("reloj que se escapa (restricciones):     %d" % len(reloj))
print("registros en runtime (listeners/acciones): %d" % len(runtime))
print("salidas por menu de puerta sin override:  %d  (revisar)" % len(puerta))
print("triggers que pisan restricciones ajenas:  %d" % len(pisa))
print("restricciones sin quien las levante:      %d" % len(huerfanas))
print("salidas por puerta de NPC sin rutina:     %d" % len(sin_rutina))
print("planificador desalineado:                 %d" % len(planif))
print("personajes prestados sin demanda:         %d" % len(prestados))
print("locaciones cerradas sin quien las abra:   %d" % len(loc_cerradas))
print("")
for r, n, faltan in reloj:
    print("%s:%d  RELOJ: bloquea avanzar/dormir pero deja %s" % (_corto(r), n, ", ".join(faltan)))
for r, n, l in runtime:
    print("%s:%d  RUNTIME: %s" % (_corto(r), n, l))
for r, n, texto in puerta:
    print("%s:%d  PUERTA: opcion '%s' con ocultar_golpear y sin override" % (_corto(r), n, texto))
for r, fn, lb in pisa:
    print("%s  TRIGGER: %s -> %s llama desactivar_restriccion sin mirar NPC oculto" % (_corto(r), fn, lb))
for d in huerfanas:
    print("%s  SIN DESACTIVAR: la activan %s y nadie la levanta" % (d, ", ".join(sorted(activan[d]))))
for r, npcs, qid in sin_rutina:
    print("%s  SIN RUTINA: congela el reloj y sale por la puerta de %s, pero la quest %s no declara rutina_quest" % (_corto(r), npcs, qid))
for qid, motivo in planif:
    print("%s  PLANIFICADOR: %s" % (qid, motivo))
for qid, otro, r in prestados:
    print("%s  PRESTADO: %s aparece en %s y la quest no lo demanda" % (qid, otro, r))
for r, loc, motivo in loc_cerradas:
    print("%s  LOCACION CERRADA: %s queda bloqueada y %s" % (r, loc, motivo))
if not (reloj or runtime or puerta or pisa or huerfanas or sin_rutina or planif
        or prestados or loc_cerradas):
    print("Sin bloqueos sin salida.")
