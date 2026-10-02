################################################################################
## Violet — declaraciones del planificador (las tres lineas)
################################################################################
## Que necesita cada quest para poder jugarse (demandas) y que toma del mundo
## mientras esta viva (consumos), en el vocabulario de core/quests/planificador.rpy.
## Es la tabla de docs/arquitectura/planificador.md pasada a codigo; `de_corrido`
## es lectura NARRATIVA (la quest fija un momento y las demas la respetan), no
## se deriva de nada.
##
## Que va y que no:
##   - TODA quest demanda a su propio NPC (Rec("npc", "<npc>")): es lo minimo
##     que necesita para jugarse, y es lo que hace que una reserva sobre el
##     NPC la frene aunque su disparador no pase por el (una accion, una
##     locacion, un mensaje). El validador y el harness lo exigen.
##   - PERSONAJES PRESTADOS: si en la escena aparece otro NPC (habla o se
##     muestra), la quest lo demanda con Rec("npc", "<otro>", en="casa") como
##     minimo — tiene que estar en la casa y no reservado, o su aparicion no
##     tiene sentido. Si la escena lo necesita en un lugar puntual, `en` es
##     ese lugar. El validador (chequeo 8) cruza los labels con la declaracion.
##   - Las DEMANDAS son LA fuente del "cuando y donde" del disparador (paso A,
##     2026-09-12): el disparador ya no chequea hora ni lugar a mano, solo su
##     estado narrativo (flags, fases, chats). Rec("npc", ..., horario=, en=,
##     libre=) y Rec("locacion", en=|locaciones=, horario=) se evaluan
##     ESTRICTO en la capa 2. Una quest con boton "en cualquier lado" y opcion
##     de puerta no declara `en`: la capa 2 esconderia el boton. Lo que ninguna
##     demanda expresa (Violet en el MISMO lugar que el MC, "a solas") sigue en
##     el disparador.
##   - Las fases DESPUES de la activacion no pasan por la capa 2 (la quest ya
##     esta en narrativa): sus condiciones de hora/lugar siguen en el codigo.
##   - CONSUMOS de vida: las rutinas (npc con en/horario), las exclusividades
##     que duran toda la quest (puerta, interaccion, skin). Lo que impone una
##     restriccion mientras esta activa (reloj, locaciones, celular, acciones)
##     NO se declara: el planificador lo lee de la restriccion en el momento.
##   - `duenio`: el id de activar_restriccion(duenio=...) de la quest, para
##     que no se mida contra su propia restriccion (y para la migracion de
##     saves anteriores al punto de activacion).
##   - `reserva=True` en el Rec npc de una de corrido cuyo momento es "esta
##     noche" / "esta mañana": al activarse, nadie mas toca a ese NPC en ese
##     slot y el reloj no pasa de largo.
##
## Horarios: 0 mañana, 1 tarde, 2 noche, 3 trasnoche. Dias: 0 lunes … 6 domingo.

init 6 python:

    # ── Linea principal ──────────────────────────────────────────────────────

    declarar_planificacion("violet_questprincipal_0_a",
        disparador=Disp("boton", "Saludar"),
        demandas=[Rec("npc", "violet"), Rec("interaccion", "violet", accion="talk")])

    declarar_planificacion("violet_questprincipal_0_b",
        disparador=Disp("boton", "Preguntarle qué le pasa"),
        duenio="violet_0_b",
        demandas=[Rec("puerta", "violet"),
                  Rec("npc", "violet", horario=1, en="casa_hviolet")],
        consumos=[Rec("npc", "violet", horario=1, en="casa_hviolet"),
                  Rec("npc", "violet", horario=2, en="casa_hviolet")])

    # Sin consumo de dormir a proposito: el bloqueo de dormir de la 01_a es un
    # registrar_bloqueo_accion que rige SOLO con el paquete pendiente (un rato
    # de un dia), no toda su vida. Declararlo de vida frenaba tres dias a las
    # quests que demandan dormir (deseo 02) con "Terminar ... primero" sin
    # motivo real; el bloqueo registrado ya cubre el momento que importa.
    declarar_planificacion("violet_questprincipal_01_a",
        disparador=Disp("repartidor"),
        demandas=[Rec("npc", "violet")])

    declarar_planificacion("violet_questprincipal_01_b",
        disparador=Disp("puerta", "Dar paquete"),
        demandas=[Rec("npc", "violet"), Rec("puerta", "violet")])

    declarar_planificacion("violet_questprincipal_02_a",
        disparador=Disp("puerta", "Pedir mangas prestados"),
        demandas=[Rec("npc", "violet"), Rec("puerta", "violet")])

    declarar_planificacion("violet_questprincipal_02_b",
        disparador=Disp("puerta", "Vengo por los mangas"),
        demandas=[Rec("puerta", "violet"),
                  Rec("npc", "violet", horario=2, en="casa_hviolet")])

    declarar_planificacion("violet_questprincipal_02_c",
        disparador=Disp("item", "Mangas de Violet"),
        demandas=[Rec("npc", "violet"), Rec("accion", accion="usar_item")])

    declarar_planificacion("violet_questprincipal_03_a",
        disparador=Disp("puerta", "Devolver mangas"),
        duenio="violet_03_a",
        demandas=[Rec("npc", "violet"), Rec("puerta", "violet")])

    # Jasmine entra a la cocina en la mitad de la escena: personaje PRESTADO,
    # tiene que estar en la casa (y no reservada) para que aparezca.
    declarar_planificacion("violet_questprincipal_04_a",
        disparador=Disp("boton", "Preguntar por el cosplay"),
        demandas=[Rec("npc", "violet"), Rec("interaccion", "violet"),
                  Rec("npc", "jasmine", en="casa"),
                  Rec("locacion", en="casa_cocina", horario=0)])

    declarar_planificacion("violet_questprincipal_04_b",
        disparador=Disp("encuentro"),
        duenio="violet_04_b",
        demandas=[Rec("npc", "violet"),
                  Rec("locacion", locaciones=_VQ04B_LOCACIONES)],
        consumos=[Rec("npc", "violet", horario=0, en="casa_pasilloarriba")])

    declarar_planificacion("violet_questprincipal_04_c",
        disparador=Disp("boton", "Preguntarle por el cosplay", nota="después de responder su mensaje"),
        demandas=[Rec("npc", "violet"), Rec("celular")])

    declarar_planificacion("violet_questprincipal_04_d",
        disparador=Disp("boton", "Preguntarle por las fotos", nota="después de responder su mensaje"),
        demandas=[Rec("npc", "violet"), Rec("celular")])

    declarar_planificacion("violet_questprincipal_04_d2",
        disparador=Disp("boton", "¿Puedo hacer algo por ti?"),
        demandas=[Rec("npc", "violet"), Rec("interaccion", "violet")])

    declarar_planificacion("violet_questprincipal_04_d3",
        disparador=Disp("boton", "Preguntarle si necesita algo"),
        demandas=[Rec("npc", "violet"), Rec("interaccion", "violet"), Rec("accion", accion="comprar")])

    declarar_planificacion("violet_questprincipal_04_d4",
        disparador=Disp("boton", "Preguntarle si necesita algo"),
        duenio="violet_04_d4",
        demandas=[Rec("npc", "violet"), Rec("interaccion", "violet"), Rec("accion", accion="cocinar"),
                  Rec("puerta", "violet")],
        consumos=[Rec("npc", "violet", horario=2, en="casa_hviolet")])

    declarar_planificacion("violet_questprincipal_04_d5",
        disparador=Disp("encuentro"),
        demandas=[Rec("npc", "violet")],
        consumos=[Rec("npc", "violet", horario=1, en="casa_pasilloarriba")])

    declarar_planificacion("violet_questprincipal_04_d6",
        disparador=Disp("boton", "Ya terminé de limpiar"),
        demandas=[Rec("npc", "violet"), Rec("interaccion", "violet")])

    declarar_planificacion("violet_questprincipal_04_e",
        disparador=Disp("boton", "Preguntarle por las fotos", nota="después de responder su mensaje"),
        demandas=[Rec("npc", "violet"), Rec("celular")])

    declarar_planificacion("violet_questprincipal_05_a",
        disparador=Disp("boton", "Ya compré los cosplay", nota="después de comprarlos por el celular"),
        demandas=[Rec("npc", "violet"), Rec("celular"), Rec("accion", accion="comprar")])

    declarar_planificacion("violet_questprincipal_05_b",
        disparador=Disp("puerta", "Llegaron los cosplay"),
        demandas=[Rec("npc", "violet"), Rec("puerta", "violet")])

    declarar_planificacion("violet_questprincipal_05_c",
        disparador=Disp("boton", "Pedirle perdón"),
        demandas=[Rec("npc", "violet"), Rec("celular"), Rec("interaccion", "violet")])

    declarar_planificacion("violet_questprincipal_06_a",
        disparador=Disp("boton", "Tengo las entradas"),
        demandas=[Rec("celular"), Rec("interaccion", "violet"),
                  Rec("npc", "violet", horario=2, en="casa_hviolet")])

    declarar_planificacion("violet_questprincipal_06_b",
        disparador=Disp("puerta", "Me pediste que pasara"),
        demandas=[Rec("celular"), Rec("puerta", "violet"),
                  Rec("npc", "violet", horario=2, en="casa_hviolet")],
        consumos=[Rec("npc", "violet", horario=2, en="casa_hviolet")])

    declarar_planificacion("violet_questprincipal_07_a",
        disparador=Disp("puerta", "Preguntar por el cosplay"),
        demandas=[Rec("npc", "violet"), Rec("puerta", "violet")])

    declarar_planificacion("violet_questprincipal_07_b",
        disparador=Disp("boton", "Ya hablé con la tienda", nota="después de hablar con la tienda por el celular"),
        demandas=[Rec("npc", "violet"), Rec("celular"), Rec("interaccion", "violet")])

    declarar_planificacion("violet_questprincipal_07_c",
        disparador=Disp("chat"),
        demandas=[Rec("npc", "violet"), Rec("celular")])

    # La tormenta: es ESA mañana. Se activa al despertar (trigger de dormir) y
    # reserva a Violet la mañana entera: nada mas se dispara con ella ni corre
    # el reloj hasta que la secuencia termina.
    declarar_planificacion("violet_questprincipal_08_a",
        disparador=Disp("dormir"),
        de_corrido=True, duenio="violet_08_a",
        demandas=[Rec("npc", "violet", horario=0, reserva=True),
                  Rec("accion", accion="dormir"),
                  Rec("accion", accion="ver_tv"), Rec("puerta", "violet")])

    # Violet enferma: tres dias en los que ella es de esta quest, y Monica se
    # queda en casa cuidandola. Las dos quedan RESERVADAS hasta completar
    # (reserva="vida"): sus menus y sus puertas solo ofrecen lo de esta quest,
    # nada de Hablar, eventos ni ventajas — cualquier otra interaccion con
    # ellas en esos dias rompe la narrativa. El reloj corre (no es un slot).
    declarar_planificacion("violet_questprincipal_09_a",
        disparador=Disp("dormir"),
        de_corrido=True,
        # Rec accion dormir: es su disparador. Con una restriccion ajena que
        # bloquee dormir (la 0_b de Monica esa misma mañana) no arranca: si
        # arrancara, su reserva de vida sobre Monica escondia la salida de
        # esa restriccion y el dormir que esta quest necesita quedaba
        # bloqueado para siempre.
        demandas=[Rec("accion", accion="dormir"),
                  Rec("npc", "violet", en="casa_hviolet", reserva="vida"), Rec("puerta", "violet"),
                  Rec("npc", "monica", horario=0, en="casa_living", reserva="vida"),
                  Rec("npc", "monica", horario=1, en="casa_living"),
                  Rec("npc", "monica", horario=2, en="casa_cocina"),
                  Rec("npc", "monica", horario=3, en="casa_hmonica"),
                  Rec("npc", "jasmine", en="casa")],       # prestada: aparece en la escena
        consumos=[Rec("npc", "violet", en="casa_hviolet"),
                  Rec("puerta", "violet"),
                  Rec("interaccion", "violet"),
                  Rec("npc", "monica", horario=0, en="casa_living"),
                  Rec("npc", "monica", horario=1, en="casa_living"),
                  Rec("npc", "monica", horario=2, en="casa_cocina"),
                  Rec("npc", "monica", horario=3, en="casa_hmonica")])

    # ── Linea de deseo ───────────────────────────────────────────────────────

    declarar_planificacion("violet_deseo_01",
        disparador=Disp("locacion"),
        demandas=[Rec("npc", "violet", en="casa"),
                  Rec("locacion", en="casa_pasilloarriba", horario=1)])

    # Encuentro nocturno: ESA madrugada. Se activa al dormir (trigger "antes").
    # Se dispara al ir a dormir (noche o trasnoche); la reserva es la madrugada.
    # Sin demanda de locacion: la cocina la pone la escena, el MC se acuesta
    # en su pieza.
    declarar_planificacion("violet_deseo_02",
        disparador=Disp("dormir"),
        de_corrido=True, duenio="violet_deseo_10",
        demandas=[Rec("accion", accion="dormir"),
                  Rec("npc", "violet", horario=2),
                  Rec("npc", "violet", horario=3, reserva=True)])

    declarar_planificacion("violet_deseo_03",
        disparador=Disp("accion", "Ver TV"),
        demandas=[Rec("npc", "violet"), Rec("accion", accion="ver_tv"), Rec("locacion", en="casa_sotano")])

    # Pensando en Violet: encerrado en el celular esa noche.
    declarar_planificacion("violet_deseo_04",
        disparador=Disp("locacion"),
        de_corrido=True, duenio="violet_deseo_20",
        demandas=[Rec("npc", "violet"), Rec("celular"), Rec("mensajes"),
                  Rec("locacion", en="casa_hmc", horario=2)])

    # En su habitacion: ESA noche, del sotano a su puerta. El override de la
    # puerta es de la fase 1 (secuencia, lo pone su restriccion), no de vida:
    # declararlo como consumo escondia toda opcion de puerta de Violet los
    # dias que la quest espera al jugador.
    declarar_planificacion("violet_deseo_05",
        disparador=Disp("accion", "Ver TV"),
        de_corrido=True, duenio="violet_deseo_25",
        demandas=[Rec("accion", accion="ver_tv"), Rec("locacion", en="casa_sotano"),
                  Rec("puerta", "violet"),
                  Rec("npc", "violet", horario=2, en="casa_hviolet", reserva=True, libre=True)],
        consumos=[Rec("npc", "violet", horario=2, en="casa_hviolet")])

    # Sinceridad: ESA noche, de la pieza del MC a la de Violet.
    declarar_planificacion("violet_deseo_06",
        disparador=Disp("locacion"),
        de_corrido=True, duenio="violet_deseo_30",
        demandas=[Rec("locacion", en="casa_hmc", horario=2), Rec("puerta", "violet"),
                  Rec("npc", "violet", horario=2, en="casa_hviolet", reserva=True, libre=True)],
        consumos=[Rec("npc", "violet", horario=2, en="casa_hviolet")])

    # Distancia: tres dias de juego libre con un contador. No pide nada.
    declarar_planificacion("violet_deseo_07",
        demandas=[Rec("npc", "violet")])

    # ── Linea de amor ────────────────────────────────────────────────────────

    declarar_planificacion("violet_amor_01",
        disparador=Disp("puerta", "Llamarla"),
        demandas=[Rec("puerta", "violet"),
                  Rec("npc", "violet", horario=1, en="casa_hviolet")])

    declarar_planificacion("violet_amor_02",
        disparador=Disp("locacion"),
        demandas=[Rec("npc", "violet", horario=0, en="casa_living"),
                  Rec("npc", "monica", horario=0, en="casa_living"),
                  Rec("locacion", en="casa_living", horario=0)],
        consumos=[Rec("npc", "violet", horario=0, en="casa_living"),
                  Rec("npc", "monica", horario=0, en="casa_living")])

    # La visita: Violet pasa por la habitacion del MC DE NOCHE (era de tarde).
    declarar_planificacion("violet_amor_03",
        disparador=Disp("locacion"),
        demandas=[Rec("npc", "violet", en="casa", libre=True),
                  Rec("locacion", en="casa_hmc", horario=2)])

    declarar_planificacion("violet_amor_04",
        demandas=[Rec("accion", accion="comprar"),
                  Rec("interaccion", "violet", accion="jugar"),
                  Rec("npc", "violet")])

    # Solos en casa: ESE domingo entero. Monica y Jasmine afuera, menu
    # exclusivo, la puerta en la fase 4. Sin reserva: la quest ya gobierna el
    # dia con su restriccion, sus listeners y su menu, y bloquear el reloj
    # todo el domingo le sacaria los pasatiempos.
    declarar_planificacion("violet_amor_05",
        disparador=Disp("dormir"),
        de_corrido=True, duenio="violet_amor_25",
        demandas=[Rec("accion", accion="dormir"),
                  Rec("npc", "violet", dia=6, horario=0, en="casa_hviolet"),
                  Rec("npc", "violet", dia=6, horario=1, en="casa_living"),
                  Rec("npc", "violet", dia=6, horario=2, en="casa_hviolet"),
                  Rec("npc", "monica", dia=6, en="fuera"),
                  Rec("npc", "jasmine", dia=6, en="fuera"),
                  Rec("accion", accion="cocinar"), Rec("puerta", "violet")],
        consumos=[Rec("npc", "violet", dia=6, horario=0, en="casa_hviolet"),
                  Rec("npc", "violet", dia=6, horario=1, en="casa_living"),
                  Rec("npc", "violet", dia=6, horario=2, en="casa_hviolet"),
                  Rec("npc", "monica", dia=6, en="fuera"),
                  Rec("npc", "jasmine", dia=6, en="fuera"),
                  Rec("interaccion", "violet"),
                  Rec("puerta", "violet")])

    declarar_planificacion("violet_amor_06",
        disparador=Disp("locacion"),
        demandas=[Rec("npc", "violet", horario=1, en="casa_hviolet", libre=True),
                  Rec("locacion", en="casa_pasilloarriba", horario=1)])

    # Las amigas: la noche de pelicula en el sotano, viernes O sabado.
    #
    # Los dos dias van como DOS Recs de Violet. Cuando no rige ninguno, la guia
    # dice "No es el momento" (tiempo, verde) en vez de marcarla interrumpida:
    # la quest no esta trabada, esta esperando el fin de semana.
    #
    # LA RESERVA ES DEL MC Y NO DE VIOLET, y va sin `dia`: con dos dias posibles
    # un Rec con dia fijo reservaria el viernes que viene aunque hoy sea sabado
    # (planificador_reservar toma el proximo slot que coincide). Sin dia, reserva
    # la noche de hoy — y como el trigger solo la toma un viernes o un sabado, el
    # dia ya esta garantizado. Alcanza con reservar al MC: una reserva sobre el
    # MC frena a CUALQUIER quest ajena, no solo a las que lo declaren.
    #
    # La reserva la toma el trigger del aviso (violet_amor_35.rpy) y se libera al
    # terminar la escena: si quedara puesta congelaria el reloj justo cuando la
    # salida de la quest es dormir.
    # El domingo solos: la quest se toma el domingo entero (de_corrido). Lo
    # unico jugable es la fase 1 —del cuarto del MC al living, con restriccion
    # propia y el reloj congelado—; desde la despedida hasta la cama es UNA
    # escena que no devuelve el control.
    #
    # Monica y Jasmine son PRESTADAS —aparecen en la despedida— y se demandan
    # "fuera": la escena las muestra como sprites, la casa las tiene afuera.
    declarar_planificacion("violet_amor_10",
        disparador=Disp("dormir"),
        de_corrido=True,
        demandas=[Rec("accion", accion="dormir"),
                  Rec("npc", "violet", dia=6, en="casa_hviolet"),
                  Rec("npc", "monica", dia=6, en="fuera"),
                  Rec("npc", "jasmine", dia=6, en="fuera"),
                  Rec("puerta", "violet")],
        consumos=[Rec("npc", "violet", dia=6, en="casa_hviolet"),
                  Rec("npc", "monica", dia=6, en="fuera"),
                  Rec("npc", "jasmine", dia=6, en="fuera"),
                  Rec("puerta", "violet")])

    # La regla de la casa: una sola escena continua, esa mañana. Las demandas
    # son exactamente lo que las rutinas de la quest arman (Violet en la cocina,
    # Monica fuera, Jasmine en su pieza): la rutina construye el mundo y la
    # demanda es lo que la capa 2 verifica antes de dejar activar. La
    # redundancia es a proposito — si alguna vez se sacara la rutina, la quest
    # se quedaria esperando en vez de dispararse en un mundo incoherente.
    #
    # Monica y Jasmine son PERSONAJES PRESTADOS: aparecen en la escena, asi que
    # van declaradas o el chequeo 8 del validador las reclama.
    declarar_planificacion("violet_amor_09",
        disparador=Disp("dormir"),
        de_corrido=True, duenio="violet_amor_45",
        demandas=[Rec("accion", accion="dormir"),
                  Rec("npc", "violet", horario=0, en="casa_cocina"),
                  Rec("npc", "monica", horario=0, en="fuera"),
                  Rec("npc", "jasmine", horario=0, en="casa_hjasmine")],
        consumos=[Rec("npc", "violet", horario=0, en="casa_cocina"),
                  Rec("npc", "monica", horario=0, en="fuera"),
                  Rec("npc", "jasmine", horario=0, en="casa_hjasmine")])

    # La solicitud: Violet va a la habitacion del MC una noche. El disparo es
    # de LOCACION (estar en casa_hmc de noche), no un boton, y desde ahi la
    # quest sigue sola: la puerta de ella y despues el chat.
    #
    # `duenio` porque en la fase 1 pone su propia restriccion (el camino a la
    # puerta de Violet, con el reloj congelado); sin declararlo, el planificador
    # la mediria contra su propia restriccion.
    #
    # NO es de_corrido: la restriccion ya acota lo que se puede hacer, y el
    # jugador se toma el rato que quiera entre tocar la puerta y escribirle.
    declarar_planificacion("violet_amor_08",
        disparador=Disp("locacion"),
        duenio="violet_amor_40",
        demandas=[Rec("npc", "violet", en="casa"),
                  Rec("locacion", en="casa_hmc", horario=2),
                  Rec("celular"),
                  Rec("puerta", "violet")],
        consumos=[Rec("npc", "violet", horario=2, en="casa_hviolet"),
                  Rec("puerta", "violet")])

    declarar_planificacion("violet_amor_07",
        disparador=Disp("locacion", nota="después de que Violet te escriba"),
        de_corrido=True,
        demandas=[Rec("npc", "violet", dia=4, horario=2, en="casa_sotano"),
                  Rec("npc", "violet", dia=5, horario=2, en="casa_sotano"),
                  Rec("mc", horario=2, reserva=True),
                  Rec("locacion", en="casa_sotano"),
                  Rec("celular")],
        consumos=[Rec("npc", "violet", dia=4, horario=2, en="casa_sotano"),
                  Rec("npc", "violet", dia=4, horario=3, en="casa_sotano"),
                  Rec("npc", "violet", dia=5, horario=2, en="casa_sotano"),
                  Rec("npc", "violet", dia=5, horario=3, en="casa_sotano")])
