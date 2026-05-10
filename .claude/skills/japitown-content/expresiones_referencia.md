# Referencia de Expresiones de Sprites

Mapeo completo de comentarios `# (...)` a codigo Ren'Py.

**Formato:** `# (Personaje elemento...)` → atributo Ren'Py del `show`

Las posiciones `at`, transiciones `with`, y `xzoom` no van en el comentario.

---

## MC — mc_parado_base

### Cuerpo

| Comentario | Atributo |
|------------|----------|
| `(Mc cuerpo base)` | `c_rbase_base` |
| `(Mc cuerpo asustado)` | `c_rbase_asustado` |
| `(Mc cuerpo avergonzado)` | `c_rbase_avergonzado` |
| `(Mc cuerpo brazos cruzados)` | `c_rbase_brazoscruzados` |
| `(Mc cuerpo celular)` | `c_rbase_celular` |
| `(Mc cuerpo confianza)` | `c_rbase_confianza` |
| `(Mc cuerpo enojado)` | `c_rbase_enojado` |
| `(Mc cuerpo idea)` | `c_rbase_idea` |
| `(Mc cuerpo pensando)` | `c_rbase_pensando` |
| `(Mc cuerpo señalando)` | `c_rbase_señalando` |
| `(Mc cuerpo victoria)` | `c_rbase_victoria` |
| `(Mc cuerpo perfume)` | `c_rbase_perfume` |
| `(Mc cuerpo mochila 1)` | `c_rbase_mochila1` |
| `(Mc cuerpo mochila 2)` | `c_rbase_mochila2` |
| `(Mc cuerpo mochila 3)` | `c_rbase_mochila3` |
| `(Mc cuerpo mochila 4)` | `c_rbase_mochila4` |
| `(Mc cuerpo regalo jasmine)` | `c_rbase_regalojasmine` |
| `(Mc cuerpo regalo violet)` | `c_rbase_regaloviolet` |
| `(Mc cuerpo regalo violet abierto)` | `c_rbase_regalovioletabierto` |
| `(Mc cuerpo manga yamete)` | `c_rbase_mangayamete` |
| `(Mc cuerpo manga yamete pp)` | `c_rbase_mangayametepp` |
| `(Mc cuerpo facepalm)` | `c_rbase_facepalm` |
| `(Mc cuerpo vr)` | `c_rbase_vr` |
| `(Mc cuerpo cuestionando)` | `c_rbase_cuestionando` |
| `(Mc cuerpo neutral)` | `c_none` |

### Boca

| Comentario | Atributo |
|------------|----------|
| `(Mc boca abierta)` | `b_abierta` |
| `(Mc boca abierta chica)` | `b_abiertachica` |
| `(Mc boca aburrida)` | `b_aburrida` |
| `(Mc boca asustada)` | `b_asustada` |
| `(Mc boca disgusto)` | `b_disgusto` |
| `(Mc boca enojada cerrada)` | `b_enojadacerrada` |
| `(Mc boca feliz abierta)` | `b_felizabierta` |
| `(Mc boca feliz cerrada)` | `b_felizcerrada` |
| `(Mc boca hablando)` | `b_hablando` |
| `(Mc boca molesta)` | `b_molesta` |
| `(Mc boca seria)` | `b_seria` |
| `(Mc boca triste)` | `b_triste` |
| `(Mc boca neutral)` | `b_none` |

### Ojos

| Comentario | Atributo |
|------------|----------|
| `(Mc ojos base)` | `o_base` |
| `(Mc ojos aburridos)` | `o_aburridos` |
| `(Mc ojos aburridos sin mirar)` | `o_aburridosnm` |
| `(Mc ojos felices)` | `o_felices` |
| `(Mc ojos felices sin mirar)` | `o_felicesnm` |
| `(Mc ojos felices cerrados)` | `o_felicescerrados` |
| `(Mc ojos asustados)` | `o_asustados` |
| `(Mc ojos asustados sin mirar)` | `o_asustadosnm` |
| `(Mc ojos abajo)` | `o_abajonm` |
| `(Mc ojos arriba)` | `o_arribanm` |
| `(Mc ojos cerrados)` | `o_cerrados` |
| `(Mc ojos disgusto sin mirar)` | `o_disgustonm` |
| `(Mc ojos enojados)` | `o_enojados` |
| `(Mc ojos enojados sin mirar)` | `o_enojadosnm` |
| `(Mc ojos molestos)` | `o_molestos` |
| `(Mc ojos molestos sin mirar)` | `o_molestosnm` |
| `(Mc ojos serios)` | `o_serios` |
| `(Mc ojos serios sin mirar)` | `o_seriosnm` |
| `(Mc ojos sorprendidos)` | `o_sorprendidos` |
| `(Mc ojos sorprendidos sin mirar)` | `o_sorprendidosnm` |
| `(Mc ojos tristes sin mirar)` | `o_tristesnm` |
| `(Mc ojos neutral)` | `o_none` |

---

## MC — mc_espalda_base

El show de espalda incluye `(Mc espalda ...)` como prefijo.

```renpy
# (Mc espalda brazos cruzados)
show mc_espalda_base brazoscruzados at mc_cerca:
    xzoom -1.0
```

| Comentario | Atributo |
|------------|----------|
| `(Mc espalda brazos cruzados)` | `brazoscruzados` |
| `(Mc espalda golpeando)` | `golpeando` |
| `(Mc espalda golpeando ruido)` | `golpeandoruido` |
| `(Mc espalda rascarse 1)` | `rascarse1` |
| `(Mc espalda rascarse 2)` | `rascarse2` |

---

## Violet — violet_parada

### Boca

| Comentario | Atributo |
|------------|----------|
| `(Violet boca aburrida)` | `b_aburrida` |
| `(Violet boca bostezo grande)` | `b_bostezogrande` |
| `(Violet boca abierta chica)` | `b_abiertachica` |
| `(Violet boca cerrada chica)` | `b_cerradachica` |
| `(Violet boca contenta)` | `b_contenta` |
| `(Violet boca feliz)` | `b_feliz` |
| `(Violet boca gritando)` | `b_gritandomucho` |
| `(Violet boca hablando)` | `b_hablando` |
| `(Violet boca hablando chica)` | `b_hablandochica` |
| `(Violet boca mordiendo)` | `b_mordiendo` |
| `(Violet boca sexy)` | `b_sexy` |
| `(Violet boca sonrisa cerrada)` | `b_sonrisacerrada` |
| `(Violet boca sonrisa costado)` | `b_sonrisacostado` |
| `(Violet boca sonrisa leve)` | `b_sonrisaleve` |
| `(Violet boca sonrisa pequeña)` | `b_sonrisapequeña` |
| `(Violet boca triste)` | `b_triste` |
| `(Violet boca neutral)` | `b_none` |

### Ojos

| Comentario | Atributo |
|------------|----------|
| `(Violet ojos base)` | `o_base` |
| `(Violet ojos abiertos)` | `o_abiertos` |
| `(Violet ojos abajo)` | `o_abajonm` |
| `(Violet ojos arriba)` | `o_arribanm` |
| `(Violet ojos cerrados)` | `o_cerrados` |
| `(Violet ojos dormidos)` | `o_dormidos` |
| `(Violet ojos enojados)` | `o_enojados` |
| `(Violet ojos felices)` | `o_felices` |
| `(Violet ojos felices sin mirar)` | `o_felicesnm` |
| `(Violet ojos guiñando)` | `o_guiñando` |
| `(Violet ojos juzgando)` | `o_juzgandonm` |
| `(Violet ojos llorando)` | `o_llorandomuchonm` |
| `(Violet ojos bostezo)` | `o_bostezograndenm` |
| `(Violet ojos sexys)` | `o_sexys` |
| `(Violet ojos tristes)` | `o_tristes` |
| `(Violet ojos pensando)` | `o_pensando` |
| `(Violet ojos costado)` | `o_costadobase` |
| `(Violet ojos neutral)` | `o_none` |

### Cuerpo — Ropa Base (rbase)

| Comentario | Atributo |
|------------|----------|
| `(Violet cuerpo base)` | `c_rbase_base` |
| `(Violet cuerpo brazos cruzados)` | `c_rbase_brazoscruzados` |
| `(Violet cuerpo celular)` | `c_rbase_celu` |
| `(Violet cuerpo chek)` | `c_rbase_chek` |
| `(Violet cuerpo cola)` | `c_rbase_cola` |
| `(Violet cuerpo dedo labio)` | `c_rbase_dedolabio` |
| `(Violet cuerpo enojada)` | `c_rbase_enojada` |
| `(Violet cuerpo fuck you)` | `c_rbase_fuckyou` |
| `(Violet cuerpo gestito)` | `c_rbase_gestito` |
| `(Violet cuerpo idea)` | `c_rbase_idea` |
| `(Violet cuerpo not ok)` | `c_rbase_notok` |
| `(Violet cuerpo ok)` | `c_rbase_ok` |
| `(Violet cuerpo paz)` | `c_rbase_paz` |
| `(Violet cuerpo pensando)` | `c_rbase_pensando` |
| `(Violet cuerpo señalando)` | `c_rbase_señalando` |
| `(Violet cuerpo sorprendida)` | `c_rbase_sorprendido` |
| `(Violet cuerpo tetas)` | `c_rbase_tetas` |
| `(Violet cuerpo verguenza)` | `c_rbase_verguenza` |
| `(Violet cuerpo victoria)` | `c_rbase_victoria` |
| `(Violet cuerpo regalo)` | `c_rbase_regalo` |
| `(Violet cuerpo neutral)` | `c_none` |

### Cuerpo — Pijama

| Comentario | Atributo |
|------------|----------|
| `(Violet cuerpo pijama base)` | `c_pijama_base` |
| `(Violet cuerpo pijama agotada)` | `c_pijama_agotada` |
| `(Violet cuerpo pijama bostezo 1)` | `c_pijama_bostezo1` |
| `(Violet cuerpo pijama bostezo 2)` | `c_pijama_bostezo2` |
| `(Violet cuerpo pijama brazos cruzados)` | `c_pijama_brazoscruzados` |
| `(Violet cuerpo pijama rascando 1)` | `c_pijama_rascando1` |
| `(Violet cuerpo pijama rascando 2)` | `c_pijama_rascando2` |
| `(Violet cuerpo pijama escoba)` | `c_pijama_escoba` |

### Cabeza

| Comentario | Atributo |
|------------|----------|
| `(Violet cabeza rbase)` | `ca_base` |
| `(Violet cabeza pijama)` | `ca_pijama` |
| `(Violet cabeza neutral)` | `ca_none` |

### Otros (efectos)

| Comentario | Atributo |
|------------|----------|
| `(Violet sonrojo)` | `ot_avergonzada` |

---

## Ejemplos combinados

```renpy
# (Mc cuerpo base ojos base boca neutral)
show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

# (Violet cuerpo brazos cruzados ojos enojados boca aburrida)
show violet_parada c_rbase_brazoscruzados o_enojados b_aburrida at right

# (Violet boca hablando chica)
show violet_parada b_hablandochica
violet "Texto"
# (Violet boca aburrida)
show violet_parada b_aburrida

# (Mc boca hablando cuerpo pensando)
show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
mc "Texto"
# (Mc boca neutral cuerpo base)
show mc_parado_base b_none c_rbase_base

# (Mc ojos abajo cuerpo celular)
show mc_parado_base o_abajonm c_rbase_celular with sprite_normal

# (Mc espalda brazos cruzados)
show mc_espalda_base brazoscruzados at mc_cerca:
    xzoom -1.0

# (Violet cuerpo pijama bostezo 1 ojos bostezo boca bostezo grande)
show violet_parada c_pijama_bostezo1 o_bostezograndenm b_bostezogrande

# (Violet sonrojo)
show violet_parada ot_avergonzada
```
