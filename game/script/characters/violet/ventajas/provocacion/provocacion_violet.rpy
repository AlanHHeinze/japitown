################################################################################
## Violet — VENTAJA "Provocación"
################################################################################
## Ventaja del hito de deseo 30. A partir de acá Violet empieza a provocar al MC
## en distintos momentos del juego. La primera situacion es la puerta del baño:
## cuando se esta bañando puede dejarla entreabierta.
##
## COMO SE AGREGAN MAS: cada situacion nueva va en su propio `pv_<nombre>.rpy`
## en esta carpeta, con su propia condicion. Este archivo tiene lo comun: el
## chequeo de la ventaja y el de "esta en un estado que la envalentona".
##
##     characters/violet/ventajas/provocacion/
##     └── provocacion_violet.rpy   ← esto (+ la puerta del baño)
##
## LA PUERTA DEL BAÑO REEMPLAZA AL VIEJO "ESPIAR". Antes el MC espiaba por su
## cuenta con un requisito de deseo, podia "abrir mas" la puerta tirando dados
## contra su destreza, y podia ser descubierto. Ahora es al reves: la puerta esta
## abierta porque ELLA la dejo asi. Todo el andamiaje de abrir/descubrir se
## elimino del motor (core/espiar).


# Estado de la puerta en el baño actual. {"clave": (dia, horario), "abierta": bool}
# None = todavia no se sorteo ninguno.
default violet_provocacion_ducha = None


init python:

    # Probabilidad base de que deje la puerta entreabierta, y la de los dias en
    # que su animo la envalentona.
    VIOLET_PROV_DUCHA_BASE = 0.5
    VIOLET_PROV_DUCHA_ESTADOS = ("violet_caliente", "violet_insinuante")

    def violet_tiene_provocacion():
        return npc_tiene_ventaja("violet", "provocacion")

    def violet_estado_provocador():
        """
        True si el animo del dia de Violet la tiene provocadora.

        Son los dos estados de la linea de deseo — "Hot" (id violet_caliente) e
        "Insinuante". Se lee el estado ASIGNADO del dia, no el stat: la gracia es
        que el mismo dia que esta de ese humor, la puerta queda abierta seguro.
        """
        _npc = obtener_npc("violet")
        if _npc is None:
            return False
        return getattr(_npc, 'talk_estado_id', None) in VIOLET_PROV_DUCHA_ESTADOS

    def _violet_ducha_clave():
        """Identifica el baño actual: (dia, horario)."""
        return (getattr(store, 'dias_totales', 0),
                getattr(store, 'horario_actual', 0))

    def violet_ducha_puerta_abierta():
        """
        ¿Dejo la puerta entreabierta en ESTE baño?

        Se sortea UNA VEZ por baño y queda fijo: si el jugador se va y vuelve, la
        encuentra como estaba. Sorteando en cada acercamiento el 50% se volveria
        100% con solo insistir.

        La rutina de ducha ocupa un unico horario (definition_violet), asi que
        (dia, horario) alcanza para identificar el baño sin guardar nada mas.
        """
        if not violet_tiene_provocacion():
            return False

        _clave = _violet_ducha_clave()
        _est = store.violet_provocacion_ducha
        if _est is not None and _est.get("clave") == _clave:
            return _est.get("abierta", False)

        _prob = 1.0 if violet_estado_provocador() else VIOLET_PROV_DUCHA_BASE
        _abierta = renpy.random.random() < _prob
        store.violet_provocacion_ducha = {"clave": _clave, "abierta": _abierta}
        return _abierta


init 5 python:

    # El menu del baño le pregunta a este registro si ofrece "Mirar".
    registrar_puerta_banio("violet", violet_ducha_puerta_abierta)
