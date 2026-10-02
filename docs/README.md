# Documentación de Japitown

Todo lo que antes andaba suelto en la raíz del proyecto vive acá.

| Carpeta | Qué hay |
|---|---|
| `arquitectura/` | Cómo está armado el motor: el relevamiento de sistemas, la tanda de optimización de 2026-07-31 y la guía de testeo por rutas. Los tres se referencian entre sí y desde el código. También viven acá `planificador.md` (el sistema de control de quests: diseño, tabla de las 47 quests y notas de implementación) y `tinte_horario_personajes.md` (el tinte de los sprites por horario: relevamiento y lo construido). |
| `narrativa/` | Perfiles de personaje y de estilo, sacados de leer el contenido ya escrito. `perfil_violet_mc_estilo.md`: quién es Violet (y su progresión en cuatro estados), cómo es la voz del MC, y las reglas de escritura que el juego ya tiene. Es la referencia para que el contenido nuevo suene igual. También `plan_amor_35_50.md` (el esquema de las 4 quests de la próxima tanda, sin diálogo todavía) e `ideas_amor_40.md` (el banco de ideas del que salió). Los esquemas MECÁNICOS —cómo se arma cada quest del lado del motor, antes de escribir diálogo— van uno por quest: `mecanica_amor_35.md`, `mecanica_amor_40.md` `mecanica_amor_45.md` y `mecanica_amor_50.md`. Las cuatro tienen la mecánica armada y el diálogo pendiente; la de 50 además tiene la escena final sin producir (falta el arte). |
| `errores/` | Registro de errores reportados (E01–E09), registro de Sentry (S…) y la investigación del textbox. |
| `plantillas/` | Los formularios para pedir una quest nueva. |
| `infra/` | El proxy de Cloudflare que oculta el webhook de Discord del reportador. |
| `versiones/` | Notas de cada versión publicada. `version_0_1_9_1.md` es el changelog completo de la 0.1.8.5 a la 0.1.9.1 (las tres releases: 0.1.9, 0.1.9a y 0.1.9.1). |
| `propuestas_post_0_1_9_1.md` | Las 18 propuestas relevadas el 2026-09-14 (10 técnicas/de cierre, 8 de jugabilidad con el contenido actual), cada una con alcance, testeo y riesgo, y el orden sugerido. Nada de eso está implementado; al tomar una, marcarla ahí. |

Y `tools/` tiene los scripts de mantenimiento más `posiciones_idle.txt`, que es
donde la herramienta de posicionamiento va acumulando lo que exporta.

| Script | Qué hace |
|---|---|
| `validar_bocas.py` | Busca dos líneas seguidas del mismo personaje **sin cambio de boca** en el medio (regla 7 del skill de contenido): la boca queda congelada mientras el jugador avanza el texto y la escena parece trabada. Descarta sola lo que no se puede arreglar — el personaje hablando fuera de cámara y los sprites de espaldas, que no tienen boca — y para cada caso real sugiere el `show` que va. Sale con código 1 si encuentra alguno. |
| `validar_sprites.py` | Chequea que cada `show <sprite> <atributos>` use atributos que ese layeredimage realmente tenga. **El lint de Ren'Py no valida esto**: un atributo de otro personaje pasa limpio y revienta en pantalla. Sin argumentos revisa todo `game/script`; sale con código 1 si encuentra algo. |
| `validar_traducciones.py` | Busca entradas `old` de `tl/` cuyo texto ya no coincide con la fuente porque el original se editó (una tilde, una mayúscula). Esas traducciones **dejan de aplicarse en silencio** y el jugador en inglés ve la línea en español. **Ni el lint ni nada avisa**: el síntoma solo aparece jugando. Con `--aplicar` reescribe los `old`. También chequea `%` sueltos en diálogo y `translate_string(...).format(...)` sobre texto con tags de Ren'Py — los dos crashean en runtime y el lint no los ve. |
| `escanear_saves.py` | Lee los `.save` de `%APPDATA%\RenPy\Japitown-…` sin ejecutarlos y lista, por slot, la versión, la generación de guardado y **los nombres del store que el save necesita y el código ya no define**. Eso último es un save que NO abre (`AttributeError` dentro de `renpy.load`, ver S12): se arregla agregando el nombre a `JP_NOMBRES_MUERTOS`. Correrlo antes de publicar, contra un save de la versión que está en la calle. |
| `find_typos.py` | Busca `[mc_name]` mal escrito (sin corchetes, con espacios, con otro nombre adentro). |

## Lo que SÍ se queda suelto en la raíz

Son cuatro y no es desprolijidad: cada uno tiene que estar ahí o algo se rompe.

| Archivo | Por qué |
|---|---|
| `project.json` · `android.json` | Los busca Ren'Py en la raíz del proyecto. |
| `progressive_download.txt` | Reglas de empaquetado del build web. Ren'Py lo lee del directorio base. |
| `android.keystore` · `bundle.keystore` | Firmas de Android. Ignorados por git a propósito. |

**`game/` no tiene ningún archivo suelto**: todo cuelga de `script/`, `images/`,
`audio/`, `fonts/`, `gui/`, `tl/`, `libs/` y `android/`.

Aparte pueden reaparecer `log.txt`, `errors.txt` y `traceback.txt` en la raíz:
los escribe Ren'Py en el directorio base cada vez que corre o que algo revienta.
Están en el `.gitignore` y se pueden borrar cuando molesten.

## Lo que se borró (2026-09-02)

Material de una sola vez, ya digerido o ya aplicado. Todo sigue recuperable en
la historia de git, en el commit `a139c9d` o antes.

- `errores.txt`, `errores2.txt` — los pegados crudos de Discord de 0.1.7. Su
  contenido quedó destilado en `errores/errores_registro.md`.
- `standardizer.py` — migración de nombres de atributos de sprites. Se corrió
  una vez, en febrero, y sus renombres ya están en el código.
- `scan.py` — el escaneo puntual de atributos ambiguos que preparó esa migración.
- `revision_testeo_fixes.md` — plan de testeo de los fixes E01–E06, cerrados
  hace tiempo.
- `game/extract.py`, `game/translate_q4.py`, `game/scratch_extract.txt` — los
  tres de abril, del día que se completó la traducción al inglés de la quest 04
  de Violet: uno listaba los bloques vacíos, el otro pegaba las 97 líneas
  traducidas y el `.txt` era el papel intermedio. Ya está todo en `tl/english/`.
  Encima vivían dentro de `game/`, así que se empaquetaban en cada build.
