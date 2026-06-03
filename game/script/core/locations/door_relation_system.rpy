################################################################################
## Sistema de Relación — Nivel de Acceso a Habitaciones y Baño
################################################################################
## Define los umbrales de stats que determinan cómo responde el NPC
## cuando el jugador intenta entrar a su habitación o al baño.
##
## Jerarquía de niveles para HABITACIÓN (el más alto que se cumpla aplica):
##   "ingreso_noche"   — horario 3, entra directamente sin menú      (stat2)
##   "ingreso_diurno"  — horario 0-2, entra directamente sin menú    (stat1)
##   "dejar_pasar"     — al golpear, NPC dice "Adelante" y el jugador entra (stat1)
##   "sale_pasillo"    — al golpear, NPC dice "Ahí salgo" y va al pasillo   (stat1)
##   None              — respuesta negativa ("Estoy ocupada") — sin requisito
##
## Para el BAÑO las opciones "espiar" y "entrar" están reservadas pero
## desactivadas (verificar_nivel_acceso_banio siempre retorna None).

################################################################################
## TABLA DE ACCESO A HABITACIONES
################################################################################
## Editar los valores de "umbral" para ajustar la progresión por NPC.
##
## stat: "stat1" → Amor (stat principal, todos los NPCs)
##       "stat2" → Deseo (stat secundario, todos los NPCs)

define TABLA_ACCESO_HABITACION = {

    # Violet — requiere Amor mínimo para cada nivel (0-9 = ninguna respuesta)
    "violet": {
        "ingreso_noche":  {"stat": "stat2", "umbral": 50},   # Deseo 50+ → entra de trasnoche
        "ingreso_diurno": {"stat": "stat1", "umbral": 50},   # Amor  50+ → entra de día
        "dejar_pasar":    {"stat": "stat1", "umbral": 30},   # Amor  30+ → "Adelante"
        "sale_pasillo":   {"stat": "stat1", "umbral": 10},   # Amor  10+ → "Ahí salgo"
    },                                                        # Amor  0-9 → sin respuesta ("ocupada")

    # Jasmine — sale al pasillo desde 0; a partir de 15 dice que pase
    "jasmine": {
        "ingreso_noche":  {"stat": "stat2", "umbral": 50},   # Deseo 50+ → entra de trasnoche
        "ingreso_diurno": {"stat": "stat1", "umbral": 40},   # Amor  40+ → entra de día
        "dejar_pasar":    {"stat": "stat1", "umbral": 15},   # Amor  15+ → "Adelante"
        "sale_pasillo":   {"stat": "stat1", "umbral": 0},    # Amor   0+ → "Ahí salgo"
    },

    # Monica — sale al pasillo desde 0; a partir de 15 dice que pase
    "monica": {
        "ingreso_noche":  {"stat": "stat2", "umbral": 50},   # Deseo 50+ → entra de trasnoche
        "ingreso_diurno": {"stat": "stat1", "umbral": 40},   # Amor  40+ → entra de día
        "dejar_pasar":    {"stat": "stat1", "umbral": 15},   # Amor  15+ → "Adelante"
        "sale_pasillo":   {"stat": "stat1", "umbral": 0},    # Amor   0+ → "Ahí salgo"
    },
}


################################################################################
## TABLA DE ACCESO AL BAÑO
################################################################################
## Reservada para cuando se habilite el contenido.
## verificar_nivel_acceso_banio() siempre retorna None hasta entonces.

define TABLA_ACCESO_BANIO = {
    "violet":  {
        "espiar": {"stat": "stat2", "umbral": 40},   # Sumisión 40+ → espiar
        "entrar": {"stat": "stat2", "umbral": 60},   # Sumisión 60+ → entrar
    },
    "jasmine": {
        "espiar": {"stat": "stat2", "umbral": 40},
        "entrar": {"stat": "stat2", "umbral": 60},
    },
    "monica":  {
        "espiar": {"stat": "stat2", "umbral": 40},
        "entrar": {"stat": "stat2", "umbral": 60},
    },
}


################################################################################
## MENSAJES DE RESPUESTA POR NPC
################################################################################
## Textos que dice cada NPC al responder en la puerta.
## Editar aquí para personalizar la voz de cada personaje.

define MENSAJES_NPC_PUERTA = {
    "violet": {
        "ocupada":   "Estoy ocupada.",
        "ahi_salgo": "Ahí salgo.",
        "adelante":  "Adelante.",
    },
    "jasmine": {
        "ocupada":   "Estoy ocupada.",
        "ahi_salgo": "Ahí salgo.",
        "adelante":  "Adelante.",
    },
    "monica": {
        "ocupada":   "Estoy ocupada.",
        "ahi_salgo": "Ahí salgo.",
        "adelante":  "Adelante.",
    },
}


################################################################################
## Funciones de verificación
################################################################################

init python:

    def _stat_acceso_npc(npc_id, conf):
        """
        Helper interno: retorna el valor del stat indicado por conf para el NPC.
        conf["stat"] puede ser "stat1" o "stat2".
        """
        if conf.get("stat") == "stat2":
            return obtener_stat2(npc_id)
        return obtener_stat1(npc_id)

    def verificar_nivel_acceso_habitacion(npc_id):
        """
        Retorna el nivel de acceso más alto que cumple el jugador para
        la habitación del NPC, teniendo en cuenta el horario actual.

        Jerarquía evaluada de mayor a menor:
            "ingreso_noche"   → horario == 3 y stat2 >= umbral
            "ingreso_diurno"  → horario in (0,1,2) y stat1 >= umbral
            "dejar_pasar"     → stat1 >= umbral
            "sale_pasillo"    → stat1 >= umbral
            None              → ningún nivel alcanzado

        Returns:
            str | None
        """
        tabla = TABLA_ACCESO_HABITACION.get(npc_id)
        if not tabla:
            return None

        horario = getattr(store, "horario_actual", 0)

        # ingreso_noche — solo si es trasnoche
        conf = tabla.get("ingreso_noche")
        if conf and horario == 3 and _stat_acceso_npc(npc_id, conf) >= conf["umbral"]:
            return "ingreso_noche"

        # ingreso_diurno — solo si no es trasnoche
        conf = tabla.get("ingreso_diurno")
        if conf and horario != 3 and _stat_acceso_npc(npc_id, conf) >= conf["umbral"]:
            return "ingreso_diurno"

        # dejar_pasar
        conf = tabla.get("dejar_pasar")
        if conf and _stat_acceso_npc(npc_id, conf) >= conf["umbral"]:
            return "dejar_pasar"

        # sale_pasillo
        conf = tabla.get("sale_pasillo")
        if conf and _stat_acceso_npc(npc_id, conf) >= conf["umbral"]:
            return "sale_pasillo"

        return None

    def verificar_nivel_acceso_banio(npc_id):
        """
        Retorna el nivel de acceso al baño cuando el NPC está dentro.
        Actualmente desactivado — siempre retorna None.

        Para habilitar cuando el contenido esté listo, descomentar el bloque
        y usar TABLA_ACCESO_BANIO para calcular el nivel.

        Returns:
            None  (siempre, por ahora)
        """
        # TODO: Habilitar cuando el contenido de baño esté listo.
        # tabla = TABLA_ACCESO_BANIO.get(npc_id)
        # if not tabla:
        #     return None
        # conf = tabla.get("entrar")
        # if conf and _stat_acceso_npc(npc_id, conf) >= conf["umbral"]:
        #     return "entrar"
        # conf = tabla.get("espiar")
        # if conf and _stat_acceso_npc(npc_id, conf) >= conf["umbral"]:
        #     return "espiar"
        return None
