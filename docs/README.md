# Documentación de Japitown

Todo lo que antes andaba suelto en la raíz del proyecto vive acá.

| Carpeta | Qué hay |
|---|---|
| `arquitectura/` | Cómo está armado el motor: el relevamiento de sistemas, la tanda de optimización de 2026-07-31 y la guía de testeo por rutas. Los tres se referencian entre sí y desde el código. También vive acá `tinte_horario_personajes.md`, que es una **propuesta todavía no implementada** (dice el estado en su primera línea). |
| `errores/` | Registro de errores reportados (E01–E09), registro de Sentry (S…) y la investigación del textbox. |
| `plantillas/` | Los formularios para pedir una quest nueva. |
| `infra/` | El proxy de Cloudflare que oculta el webhook de Discord del reportador. |
| `versiones/` | Notas de cada versión publicada. |

Y `tools/` tiene los scripts de mantenimiento más `posiciones_idle.txt`, que es
donde la herramienta de posicionamiento va acumulando lo que exporta.

| Script | Qué hace |
|---|---|
| `validar_sprites.py` | Chequea que cada `show <sprite> <atributos>` use atributos que ese layeredimage realmente tenga. **El lint de Ren'Py no valida esto**: un atributo de otro personaje pasa limpio y revienta en pantalla. Sin argumentos revisa todo `game/script`; sale con código 1 si encuentra algo. |
| `validar_traducciones.py` | Busca entradas `old` de `tl/` cuyo texto ya no coincide con la fuente porque el original se editó (una tilde, una mayúscula). Esas traducciones **dejan de aplicarse en silencio** y el jugador en inglés ve la línea en español. **Ni el lint ni nada avisa**: el síntoma solo aparece jugando. Con `--aplicar` reescribe los `old`. |
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
