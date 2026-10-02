# Línea de amor de Violet — de 35 a 50

Plan de la próxima actualización: **4 quests nuevas** (amor 35, 40, 45 y 50),
**2 hitos** y **ventajas presentadas pero sin desarrollar**.

Este archivo es el esquema de trabajo: qué pasa en cada quest, en qué orden y
qué decide cada tramo. **No hay diálogo escrito todavía** — eso viene después,
quest por quest.

Estado: **las cuatro con su esqueleto cerrado.** La 45 y la 50 están casi como
un guion sin diálogo; la 35 y la 40 tienen la estructura firme y algunas
decisiones anotadas.

Referencia de voz y personaje: [`perfil_violet_mc_estilo.md`](perfil_violet_mc_estilo.md).
Banco de ideas del que salió la 40: [`ideas_amor_40.md`](ideas_amor_40.md).

---

## Lo nuevo que trae la tanda

### Personajes: las amigas de Violet

Las dos aparecen por primera vez en la 35 y son el motor de las dos quests.

| | **Zowie** | **Leah** |
|---|---|---|
| Carácter | Energética, va al frente | Reservada |
| Con el MC | **Se insinúa ligeramente** — es lo que dispara los celos | Sincera por completo, sin filtro ni maldad |
| Función narrativa | El problema | El termómetro: dice en voz alta lo que los otros tres esquivan |

Decisión pendiente: si son **NPCs** del sistema (rutinas, stats, menú) o
**personajes de escena** que existen solo dentro de estas quests y como contacto
de chat. Lo barato y lo suficiente para esta tanda es lo segundo — el registro
`CONTACTOS_ESPECIALES` de `messagesystem_core.rpy` ya permite un contacto sin
NPC, que es como funcionan la tienda y Libre Mercado.

### App nueva: XGram ✅ hecha

La red social del juego. **Ya está en el celular** (`hud_celular.rpy`), con la
paleta apagada de "en desarrollo" como Hot y Banco: al tocarla dice *"Contenido
en desarrollo"*.

Existe ahora para que el mundo la tenga antes de que la usemos: la quest de amor
40 arranca con una solicitud de amistad que llega por XGram, y el jugador ya va a
conocer el icono. Queda ahí hasta que la queramos explotar.

Ya está sumada a las listas de apps que cierran las dos quests tutorial
(Jasmine 0_b y MC 0_b), que son exhaustivas a propósito.

---

## Amor 35 — La noche de película

**Punto de partida.** Después de la 30, Violet ya está mucho más suelta con él y
entiende las intenciones. Acá **ella habla un poco de lo que siente**, pero sin
proponérselo: lo que la delata es la reacción, no la confesión.

### Esqueleto

1. **Violet invita a sus dos amigas** a ver una película de noche. Usan el
   **sótano** (la pantalla grande ya está establecida ahí, por el anime).
2. En algún momento **Violet llama al MC por un inconveniente**.
3. **Charla entre los cuatro**, con el MC metido en la reunión de ellas.
4. Durante la charla **Zowie se insinúa ligeramente** al MC; Leah dice alguna
   verdad incómoda; Violet lo registra todo sin decir nada.
5. La quest cierra con **Violet celosa**, sin que nadie lo nombre.

### Lo que hay que decidir antes de escribir

- **Cuál es el inconveniente** por el que lo llama. Tiene que ser algo que lo
  obligue a quedarse un rato, no a resolver y irse: el proyector que no anda, la
  tele que no toma la señal, algo de comer, una cortina.
- **Si el MC se queda a ver la película o se va** después de resolverlo. Que se
  quede da más escena; que se vaya hace más creíble el celo (ella lo sigue
  pensando después).
- **Si el jugador elige** durante la charla de los cuatro, y sobre qué. La
  opción natural es cómo responde a la insinuación de Zowie: seguirle el juego,
  esquivarla o cortarla. Eso ya define el tamaño del celo.
- **Qué ve Violet exactamente.** Conviene que sea un detalle concreto y chico
  —dónde se sienta, a quién le contesta un chiste—, porque en la 40 ella lo va a
  tener cronometrado y eso es lo que la delata.
- **Si Leah dice algo que apunte directo a Violet.** Es su función; hay que
  decidir si ya en la 35 o recién en la 40.

### Ganchos que deja para la 40

- Zowie conoce al MC y tiene motivo para buscarlo.
- Violet quedó con algo sin decir.
- Leah quedó como testigo — sirve si alguna vez hace falta alguien que le diga
  la verdad a cualquiera de los dos.

---

## Amor 40 — La solicitud

**El objetivo de la quest, dicho claro:** que quede establecido **en qué punto
está parado el jugador con respecto a ella**. Arranca del celo que dejó la 35 y
termina con Violet planteando que hay que ir a sus tiempos.

**La decisión de diseño que lo hace funcionar:** Violet no habla de sentimientos
de frente — está escrito en todo su contenido previo. Por eso la charla **se
parte en dos**: la parte cara a cara llega hasta donde ella aguanta (admitir el
celo) y **se corta cuando ella se va**; el resto pasa **por mensaje**, que es el
canal donde ella se maneja mejor y donde ya está establecido que dice cosas que
en persona no diría.

### Esqueleto

**1 · El disparo — la solicitud (automático, de noche)**

Al llegar al umbral de amor, **la noche siguiente**, esté donde esté el jugador,
se dispara una escena: el MC queda en el centro, saca el celular, ve que tiene
una **solicitud de amistad de Zowie** en XGram, la acepta y piensa al respecto.
Vuelve al game loop.

*Por qué una solicitud y no un mensaje: es mucho más común, no obliga a nadie a
hablar, y de paso instala la app.*

**2 · La quest sigue — hablar con Violet**

Aparece un **botón en el menú de Violet**. El jugador va cuando quiere.

**3 · La charla cara a cara**

- Violet hace **comentarios ácidos** sobre la noche y sobre su amiga.
- El MC va preguntando **por qué se pone así**; ella está **evasiva**.
- El MC logra que **admita que está celosa**.
- **Ella se va.** La escena termina ahí: no hay reconciliación en persona.

**4 · La charla por mensaje**

Sigue por chat, donde ella maneja mejor la conversación. Acá pasa lo que
importa:

- Hablan **de los celos** de verdad, ya sin esquivarlos.
- Hablan **de lo que sienten** los dos.
- Violet le plantea **ir a sus tiempos**: si él puede seguir su ritmo, la
  relación se vuelve más profunda.

**5 · Cierre**

El cierre de la quest otorga el **hito** y presenta las ventajas.

### Lo que hay que decidir antes de escribir

- **Si aceptar la solicitud es una elección o es automático.** Como está
  planteado es automático (la acepta y piensa). Si se vuelve elección, hay que
  bancar las dos ramas en toda la quest — probablemente no valga la pena ahora,
  pero sí dejar el flag guardado por si más adelante se usa.
- **Si Zowie escribe algo después de la aceptación**, o si solo queda agregada.
  Que solo quede agregada es más incómodo y más real. Si escribe, necesita
  contacto en el chat.
- **Dónde y cuándo se puede usar el botón de Violet.** Si es en cualquier lado,
  la escena tiene que funcionar en cualquier fondo; si es en su habitación, el
  controlador lo pide como demanda y la guía lo dice sola.
- **Qué la hace admitir el celo.** Del banco de ideas, las que mejor le calzan:
  que se contradiga sola, que tenga el detalle cronometrado, o que él confiese
  primero que le gustó verla así. Puede ser la elección del jugador.
- **Cómo arranca el chat.** Dos opciones: lo escribe ella al rato (más de ella,
  y más fuerte: se fue pero volvió), o el juego deja al jugador con la pelota y
  él tiene que escribirle. La segunda hace que el jugador **elija** seguirla.
- **Qué elecciones tiene el chat y qué marcan.** El eje de esta quest no es amor
  contra deseo: es **aceptar su tiempo contra empujar**. Empujar no debería ser
  un muro — ella se cierra un poco y la quest avanza igual, pero deja una marca
  que 45 y 50 puedan leer.
- **Si la última palabra es de ella o de él.**

### Notas de implementación

- **Disparador**: `Disp("auto")` para la escena de la solicitud (trigger de
  game_loop, de noche, una sola vez), y después el botón en el menú de Violet.
  Son dos momentos, así que probablemente sean **dos quests encadenadas** —
  mismo patrón que 04_b → 04_c: una que se dispara sola y deja el flag, y otra
  con el botón. Decidir al escribir.
- **Demandas**: la escena automática no pide nada más que la noche; la charla
  pide a Violet disponible (y su locación, si se decide que sea en su cuarto).
- La parte de chat va como grupo de mensajes de la quest, con `forzada=True` si
  se quiere que el botón "Hablar" aparezca sí o sí — igual que deseo 20.
- El **chat es prioritario** (bloquea el resto) solo si queremos encerrar al
  jugador ahí. Ojo con la regla A1 del skill de advertencias: si se bloquea, la
  salida tiene que estar siempre disponible.

---

## Amor 45 — La regla de la casa

**La idea.** Los tres están haciendo algo en la casa. Mónica comenta que se
están llevando muy bien últimamente; Violet lo niega un poco; Mónica insiste con
que los ve mucho tiempo juntos. Mónica se va, quedan solos, y Violet plantea que
**no quiere que la relación sea un tema de la casa**: van a tener que hacer todo
cuando estén solos.

**Función.** Presentarle al jugador **la mecánica de las interacciones con
Violet**. Es la quest que convierte el acuerdo de la 40 ("a mis tiempos") en
algo que se juega.

Dos anclas que ya existen y que la quest debería cobrar:

- **La regla ya la dijo ella**, en el chat de la 04_d: *"Si tienes algo que
  decirme lo haces en privado"*. Que él la haya incumplido durante 30 puntos de
  amor es el motivo por el que ahora la formaliza.
- **La mecánica ya está a medias en el código**: las dos ventajas de beso
  chequean que no haya nadie más en la locación y ella contesta *"Acá no, no
  delante de otras personas"*. La quest le pone nombre a algo que al jugador ya
  le pasó.

### Disparo

Al llegar al umbral de amor, la quest espera. Se dispara **por la mañana, la
próxima vez que el MC vaya al frente de la casa**, con:

- **Jasmine en su habitación** (entra al final de la escena).
- **Mónica fuera de la casa** (llega con el paquete: es lo que abre todo).

### Esqueleto

**1 · El paquete, en el frente**

Mónica llega con un paquete. El MC se ofrece a ayudarla. Van los dos a la
**cocina** a dejar las cosas.

**2 · Violet se suma**

Aparece y propone ayudarlos. Los tres acomodan.

**3 · El pedido**

Terminado eso, **Violet le pide al MC que cocine algo**. Él pregunta qué quiere;
ella le pide un plato concreto **y se lo halaga**. Él dice que sí.

*Es el punto exacto en el que se los ve funcionando como algo — ella pide con
confianza, él acepta sin discutir. No hace falta que nadie lo diga: es lo que
Mónica ve.*

**4 · El comentario de Mónica**

Entra **como una pregunta**. Violet se hace la desentendida. Mónica **refuerza**:
le alegra mucho verlos tan cercanos. Violet recurre a la **negación técnica**:
es lo normal, viven juntos.

**5 · Mónica se va**

Dice que aprovecha a hacer unas cosas del trabajo, ya que está el MC. Antes de
salir tira el remate —**"los dejo solos"** o parecido— **con una risa**.

**6 · La regla, a solas**

- Violet: se tienen que **cuidar con las cosas que hacen por la casa**.
- MC: no están haciendo nada raro ni malo.
- Violet: **Mónica es muy receptiva**.
- MC: a él le pareció un comentario más.
- Violet: él es **muy impulsivo**, y si quiere hacer algo, **lo pueden hacer
  cuando están solos, únicamente**.

**6b · Qué significa "cuando estemos solos" — la preparación de lo que viene**

- MC: ¿y qué es lo que pueden hacer cuando están solos?
- Violet: **todo**. Sobre todo las cosas pervertidas.
- MC: entonces, estando solos, ¿puede hacer lo que quiera?
- Violet: **no todo** — ya le dijo que para algunas cosas necesita tiempo.
- MC: está bien. **Ligeramente desanimado.**
- Violet: **"no te estoy diciendo que no"**.

*Este tramo es el que hace que la quest no sea solo una regla. Tres cosas
pasan acá:*

1. *La regla se da vuelta: deja de ser un límite y pasa a ser un **permiso con
   condición**. Sin esto, el jugador siente que le sacaron algo; con esto,
   siente que le abrieron una puerta y le pidieron paciencia.*
2. *Reengancha el acuerdo de la 40 — "te dije que para algunas cosas necesito
   tiempo" es ella cobrándole al jugador lo que ya habían hablado. Las dos
   quests dejan de ser dos escenas sueltas.*
3. ***"No te estoy diciendo que no" es la línea que el jugador se tiene que
   llevar**, y es la que deja servida la 50.*

*Dos cuidados al escribirlo:*

- *El desánimo del MC va **corto y seco**: una línea. Su registro es la ironía,
  no la queja; si se lamenta, deja de ser él.*
- *Que ella lo corrija **es su forma de ser cálida**. No dice algo tierno: le
  arregla un malentendido. Es exactamente cómo funciona el personaje, y por eso
  la última palabra tiene que ser suya.*

**7 · Entra Jasmine**

Pregunta qué está pasando. Violet: no pasaba nada, estaban por ponerse a
cocinar. Jasmine le dice al MC: **"te ayudo"**.

*Este es el mejor hallazgo de la quest y conviene no tocarlo: la regla se
enuncia y **una línea después el mundo la demuestra**. Violet dice "solo cuando
estemos solos", y acto seguido aparece alguien. El jugador aprende la mecánica
viéndola funcionar, no leyéndola.*

**8 · Cierre**

Termina la conversación y **avanza el horario a la tarde, en la cocina**.

### Qué decisiones cerró este esquema

Respecto del banco de ideas: la situación es el paquete + cocinar (A5 + A1); el
comentario de Mónica entra como pregunta y después refuerza (B5 → B1); la
negación es la técnica (C1); Mónica sale con remate y risa (D2); la regla se
formula como condición (E1/E2). El cierre con Jasmine **no estaba en el banco**
y es mejor que todo lo que había ahí.

### Lo que queda abierto

- **¿El jugador elige en algún momento?** Tal como está, la escena corre entera
  sin una sola elección. **El tramo 6b es el lugar**: las dos preguntas del MC
  ("¿qué podemos hacer?" y "¿puedo hacer lo que quiera?") ya son elecciones
  disfrazadas de línea. Convertir la segunda en menú da el punto donde el
  jugador se posiciona, y las reacciones ya están escritas en el esquema:
  empujar → "no todo, necesito tiempo"; aceptar → ella igual aclara que no es
  un no. Otro lugar posible, menor: cuando ella le pide que cocine (aceptar de
  una / chicanearla antes). Ver F1-F6 en
  [`ideas_amor_45.md`](ideas_amor_45.md).
- **Qué plato pide.** La pizza ya se usó dos veces (0_b y 04_d4); conviene otro
  para que el halago no suene repetido.
- **Si Violet acota el alcance de la regla.** Si el jugador pregunta "¿y si
  estamos solos en la cocina?", ella define los límites **y ahí el jugador
  aprende la mecánica desde el diálogo**. Es la forma más barata de enseñarla.
- **Si además va un `tutorial`** después de la escena, como el juego ya hace con
  el talk y las elecciones.
- **Qué pasa con Jasmine después.** ¿Se queda cocinando con ellos (y el horario
  avanza con los tres) o el corte es inmediato? Lo segundo es más limpio.
- **Ojo con el eco involuntario**: Jasmine ofreciéndose a cocinar con él, justo
  después de la quest de los celos, puede leerse como otra chica acercándose.
  Puede ser un gag buenísimo si es a propósito (Violet lo registra sin decir
  nada) o ruido si no lo es. Decidirlo.
- **¿Lleva hito?** Ver la sección de hitos: acá es donde cambia **cómo se
  juega**, así que es candidata fuerte aunque el plan tentativo los ponga en 40
  y 50.

### Notas de implementación

- **Disparador**: `Disp("locacion")` — trigger de game_loop sobre `casa_frente`
  en horario mañana. Demandas: `Rec("locacion", en="casa_frente", horario=0)`,
  `Rec("npc", "violet")`, y los dos prestados: `Rec("npc", "monica",
  en="fuera")` y `Rec("npc", "jasmine", en="casa_hjasmine")`. El controlador se
  encarga de que la quest no se active si el mundo no está así.
- La escena **mueve al MC** (frente → cocina) y termina **avanzando el horario**
  a la tarde con él en la cocina: va por `ConfiguracionRetorno` o a mano al
  final del label, como hace amor 25.
- **Dónde queda cada una después.** Mónica dijo que se iba a trabajar: conviene
  dejarla en su habitación y no que reaparezca en el living dos segundos
  después. Jasmine queda en la cocina o vuelve a su rutina, según lo que se
  decida arriba.
- La escena es **continua**: no hace falta restricción. Si en algún tramo el
  jugador recupera el control, ahí sí, con `duenio`.

### Lo que la 40 le deja servido

- Si en la 40 el jugador empujó, acá se puede leer esa marca.
- Zowie sigue agregada en XGram y nadie resolvió qué pasa con eso.

## Amor 50 — El domingo solos

**Cierre de la rama.** Es donde se cumple lo que la 45 dejó puesto: *"para
algunas cosas necesito tiempo"* / *"no te estoy diciendo que no"*. El jugador
viene esperando esto desde dos quests antes, y **la regla de la 45 es lo que le
da sentido**: "no hay nadie en la casa" solo significa algo porque ella misma
estableció que solo cuando están solos.

### Disparo

Al llegar al umbral, la quest espera y se dispara **el domingo siguiente, por la
mañana, al despertar**.

### Esqueleto

**1 · El despertar y la despedida**

- Al despertar, el MC recuerda que **hoy se queda solo**: todas se van a la casa
  de la hermana de Mónica.
- Mira la hora en el teléfono: quizás todavía no se fueron, podría ir a
  despedirse.
- **Tiene que ir al living.** Ahí están Mónica y Jasmine.
- Mónica le pregunta a Jasmine si agarró el cargador del teléfono; Jasmine dice
  que **esta vez se acordó**.
- El MC saluda; charla casual sobre el viaje.
- El MC **pregunta por Violet**. Mónica: se sentía mal y no va a ir.
- Sigue la charla y **las chicas se van**.
- `piensa` de cierre: Violet **ama** ir a lo de su tía, se debe sentir muy mal,
  podría ir a ver qué necesita.

*El cargador es el detalle que hace que la escena no sea un trámite: dos líneas
de rutina familiar que ubican al jugador en una casa de verdad antes de dejarlo
solo en ella.*

**2 · La ducha de Violet**

Violet se está bañando. Hay **dos caminos** y confluyen:

- **Puerta de su habitación** → mensaje: *"Violet no responde, pero escucho la
  ducha abierta, parece que está tomando un baño"*.
- **Puerta del baño** → entra la escena: el MC en el pasillo, Violet contesta
  desde adentro. Si llegó directo acá sin pasar por la habitación, primero
  piensa *"parece que Violet está tomándose un baño"* y después sigue igual.

La charla:

- MC: ¿estás bien?
- Violet: sí.
- MC: ¿y por qué no fuiste a lo de tu tía entonces?
- Violet: **era la oportunidad perfecta**.
- MC: ¿para qué?
- Violet: **ya salgo**.

Violet aparece **envuelta en una toalla**, le dice **"date una ducha vos
también"** y se va a su habitación. El MC se queda pensando en lo que le dijo.

**3 · La ducha del MC**

Tiene que ir al baño, donde aparece **la opción de bañarse**. Al hacerlo: corte
de *"un tiempo más tarde"* y el MC en el baño, pensando en que tiene que ir a
ver a Violet.

**4 · La habitación**

- Violet está **en tanga**.
- *"Te bañaste muy rápido, ¿estabas apurado para algo?"*
- MC: no sabía qué quería.
- Violet: **ya llegó el tiempo**, no hay nadie en la casa, **tiene vía libre**.
- El MC se acerca → **secuencia de beso**, donde le saca la ropa mientras la
  besa.
- Escena nueva: **en la cama, desnudos**. Animación simulada con **botones para
  controlar algunas cosas**.

### Por qué cierra bien la rama

- **Paga las tres quests anteriores.** "Ya llegó el tiempo" es la frase de la 45;
  "no hay nadie en la casa" es la regla de la 45; que ella decida cuándo es el
  acuerdo de la 40.
- **Ella sigue llevando el ritmo hasta el final.** Se queda en casa a propósito,
  lo manda a bañarse, y es la que dice que llegó el momento. El MC no fuerza
  nada en toda la quest: obedece instrucciones sin entenderlas, que es
  exactamente su lugar en la relación desde la 30.
- **El engaño de la enfermedad es un buen chiste con memoria**: Violet mintió
  para quedarse. Y la 09_a ya usó "Violet enferma" en serio — que acá sea
  mentira es un guiño que el jugador veterano va a leer.

### Lo que queda abierto

- **⚠️ La misma premisa que amor 25.** "Solos en casa" también es un domingo en
  el que Mónica y Jasmine se van y Violet se queda. Conviene decidir si es
  **repetición o callback**. Si es callback, es muy fuerte: el MC puede
  pensarlo en una línea ("la última vez que quedamos solos se cortó la luz y no
  pasó nada"), y la quest gana en vez de perder. Si no se dice, se va a leer
  como que se repitió el recurso.
- **El voseo.** En la nota figura *"date una ducha vos también"*. El juego está
  **todo en tuteo neutro** y hubo una pasada entera sacando el voseo; al
  escribir va *"tú también"*.
- **Si el jugador elige en algún punto.** La escena de la habitación es el lugar
  natural: cómo responde a "¿estabas apurado para algo?". Y la secuencia final
  ya trae botones, que es otra forma de decisión.
- **Qué pasa si el jugador no se baña**, o se va a hacer otra cosa. Hace falta
  que el resto de la casa lo devuelva ahí (restricción acotada o mensaje de
  recordatorio), y que no pueda entrar a la habitación antes de bañarse — o que
  si entra, ella lo mande a bañarse.
- **Cuánto dura el día.** Si la quest ocupa la mañana entera, decidir a qué
  horario queda el mundo al terminar y dónde queda el MC.
- **Qué pasa con Zowie y con XGram**, que quedaron abiertos en la 40. Si no se
  tocan acá, quedan para la tanda siguiente — está bien, pero conviene que sea
  una decisión y no un olvido.

### Notas de implementación

- **Disparo**: `registrar_trigger_dormir("despues")`, como el de amor 25, con la
  condición de domingo. En la declaración va `dia=6` (domingo), igual que amor
  25.
- **Personajes prestados**: `Rec("npc", "monica", dia=6, en="casa_living",
  horario=0)` para la escena de la despedida, y después las dos **fuera** por el
  resto del día — mismo esquema que amor 25, que ya las manda afuera el domingo.
- **La puerta de la habitación** con el mensaje de la ducha: `registrar_bloqueo_golpe`
  para Violet mientras dura esa fase (se apaga por flag).
- **La puerta del baño**: `restriccion_quest_activa.registrar_label_locacion("casa_banioarriba", …)`,
  exactamente como hace la 08_a con `violet_quest08a_puerta_baño`. Es el caso
  previsto para esto: la restricción la pone y la saca el mismo contenido, y la
  ventana es corta.
- **La opción de bañarse**: `AccionLocacion` registrada **en `actions_catalog.rpy`,
  en init**, con `condicion` que lea un flag `default` — nunca en runtime (regla
  del proyecto; ya rompió dos quests).
- **La secuencia final con botones**: seguir el **Patrón E** del skill de
  contenido (el minijuego de la 09), sobre todo el bucle con `ui.interact()` y
  `Return` en vez de `Call` desde la screen.
- **Los dos caminos de la escena 2** confluyen en el mismo label: el que entra
  por el baño sin pasar por la habitación solo suma un `piensa` antes. Un label
  con un flag, no dos labels.

### Costo de producción

Es **la quest más cara de la tanda en arte**: Violet en toalla, Violet en tanga
en su habitación, la secuencia de beso con quitado de ropa, y la escena de cama
con animación simulada. Conviene dimensionarlo antes de arrancar a escribir, no
después.

---

## Hitos y ventajas

**2 hitos** en la tanda. Lo más limpio es ponerlos en 40 y 50, que son los dos
puntos donde algo cambia de verdad (el acuerdo y el cierre de rama), y dejar 35
y 45 como quests de desarrollo sin hito. A confirmar.

Ventajas candidatas, **a presentar en la escena y no a desarrollar**. Las que
nacen de lo que la 40 deja dicho:

- **Hablar en serio** — una opción en su menú para conversaciones privadas, sin
  chiste. Es literalmente lo que la quest habilita.
- **Su ritmo** — el talk cambia: lo que antes la cerraba ahora suma.
- **Puerta abierta** — entrar a su habitación sin golpear. El símbolo físico del
  acuerdo.
- **Salidas** — proponerle ir a algún lado fuera de la casa. Abre una locación
  futura sin comprometerla ahora.
- **XGram** — la app pasa de "en desarrollo" a tener contenido. Es la ventaja más
  obvia para más adelante, y explica por qué la app existe desde ahora.

Recordar la regla del panel de Desbloqueos: una ventaja registrada **sin ninguna
escena** le promete al jugador algo que no existe (hoy pasa con "Nuevos Chats").
Si se presentan sin desarrollar, conviene que el texto de la ventaja lo diga.
