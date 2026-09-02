################################################################################
## Sprites de Violet
################################################################################
## Definición de sprites para el personaje Violet

################################################################################
## Layeredimage: violet_parada
################################################################################

layeredimage violet_parada:
    # Area
    group area:
        attribute a_base default:
            "images/characters/casa/violet/violet_parada_area.webp"
        attribute a_none:
            Null()
    
    # Cabeza
    group cabeza:
        attribute ca_base default:
            "images/characters/casa/violet/violet_parada_cabeza_rbase.webp"
        attribute ca_pijama:
            "images/characters/casa/violet/violet_parada_cabeza_pijama.webp"
        attribute ca_none:
            Null()

    # Cuerpo completo — sprites que YA incluyen cabeza/cara (ej: cosplay eva).
    # Va ANTES de boca/ojos para dibujarse DEBAJO de ellos, asi las expresiones
    # faciales (boca/ojos) siguen siendo visibles encima del sprite.
    # Usar con c_none (cuerpo base en Null) y ca_none (cabeza base en Null).
    group cuerpocompleto:
        attribute cc_none default:
            Null()
        attribute cc_eva_base:
            "images/characters/casa/violet/violet_parada_cuerpo_eva_base.webp"

    # Boca
    group boca:
        attribute b_aburrida default:
            "images/characters/casa/violet/violet_parada_boca_aburrida.webp"
        attribute b_bostezogrande:
            "images/characters/casa/violet/violet_parada_boca_bostezogrande.webp"
        attribute b_abiertachica:
            "images/characters/casa/violet/violet_parada_boca_abiertachica.webp"
        attribute b_cerradachica:
            "images/characters/casa/violet/violet_parada_boca_cerradachica.webp"
        attribute b_contenta:
            "images/characters/casa/violet/violet_parada_boca_contenta.webp"
        attribute b_feliz:
            "images/characters/casa/violet/violet_parada_boca_feliz.webp"
        attribute b_gritandomucho:
            "images/characters/casa/violet/violet_parada_boca_gritandomucho.webp"
        attribute b_hablando:
            "images/characters/casa/violet/violet_parada_boca_hablando.webp"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_hablandochica.webp"
        attribute b_mordiendo:
            "images/characters/casa/violet/violet_parada_boca_mordiendo.webp"
        attribute b_sexy:
            "images/characters/casa/violet/violet_parada_boca_sexy.webp"
        attribute b_sonrisacerrada:
            "images/characters/casa/violet/violet_parada_boca_sonrisacerrada.webp"
        attribute b_sonrisacostado:
            "images/characters/casa/violet/violet_parada_boca_sonrisacostado.webp"
        attribute b_sonrisaleve:
            "images/characters/casa/violet/violet_parada_boca_sonrisaleve.webp"
        attribute b_sonrisapequeña:
            "images/characters/casa/violet/violet_parada_boca_sonrisapequena.webp"
        attribute b_triste:
            "images/characters/casa/violet/violet_parada_boca_triste.webp"
        attribute b_none:
            Null()
    
    # Ojos
    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_base.webp"
        attribute o_bostezograndenm:
            "images/characters/casa/violet/violet_parada_ojos_bostezograndenm.webp"
        attribute o_abajonm:
            "images/characters/casa/violet/violet_parada_ojos_abajonm.webp"
        attribute o_abiertos:
            "images/characters/casa/violet/violet_parada_ojos_abiertos.webp"
        attribute o_arribanm:
            "images/characters/casa/violet/violet_parada_ojos_arribanm.webp"
        attribute o_cerrados:
            "images/characters/casa/violet/violet_parada_ojos_cerrados.webp"
        attribute o_felicesnm:
            "images/characters/casa/violet/violet_parada_ojos_felicesnm.webp"
        attribute o_dormidos:
            "images/characters/casa/violet/violet_parada_ojos_dormidos.webp"
        attribute o_enojados:
            "images/characters/casa/violet/violet_parada_ojos_enojados.webp"
        attribute o_felices:
            "images/characters/casa/violet/violet_parada_ojos_felices.webp"
        attribute o_guiñando:
            "images/characters/casa/violet/violet_parada_ojos_guinando.webp"
        attribute o_juzgandonm:
            "images/characters/casa/violet/violet_parada_ojos_juzgandonm.webp"
        attribute o_llorandomuchonm:
            "images/characters/casa/violet/violet_parada_ojos_llorandomuchonm.webp"
        attribute o_sexys:
            "images/characters/casa/violet/violet_parada_ojos_sexys.webp"
        attribute o_tristes:
            "images/characters/casa/violet/violet_parada_ojos_tristes.webp"
        attribute o_pensando:
            "images/characters/casa/violet/violet_parada_ojos_pensando.webp"
        attribute o_costadobase:
            "images/characters/casa/violet/violet_parada_ojos_costadobase.webp"
        attribute o_none:
            Null()
    
    # Cuerpo
    group cuerpo:
        attribute c_rbase_base default:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_base.webp"
        attribute c_rbase_brazoscruzados:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_brazoscruzados.webp"
        attribute c_rbase_celu:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_celu.webp"
        attribute c_rbase_chek:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_chek.webp"
        attribute c_rbase_cola:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cola.webp"
        attribute c_rbase_dedolabio:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_dedolabio.webp"
        attribute c_rbase_enojada:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_enojada.webp"
        attribute c_rbase_fuckyou:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_fuckyou.webp"
        attribute c_rbase_gestito:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_gestito.webp"
        attribute c_rbase_idea:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_idea.webp"
        attribute c_rbase_live:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_live.webp"
        attribute c_rbase_notok:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_notok.webp"
        attribute c_rbase_ok:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_ok.webp"
        attribute c_rbase_paz:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_paz.webp"
        attribute c_rbase_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_pensando.webp"
        attribute c_rbase_señalando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_senalando.webp"
        attribute c_rbase_sorprendido:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_sorprendida.webp"
        attribute c_rbase_tetas:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_tetas.webp"
        attribute c_rbase_verguenza:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_verguenza.webp"
        attribute c_rbase_victoria:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_victoria.webp"
        attribute c_rbase_regalo:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cajaregalo.webp"
        attribute c_rbase_cajacosplay:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cajacoxplay.webp"
        attribute c_rbase_saludando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_saludando.webp"
        attribute c_rbase_mangas:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_mangas.webp"
        attribute c_rbase_bolsamadera:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_bolsamadera.webp"

        # Pijama
        attribute c_pijama_base:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_base.webp"
        attribute c_pijama_agotada:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_agotada.webp"
        attribute c_pijama_bostezo1:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bostezo1.webp"
        attribute c_pijama_bostezo2:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bostezo2.webp"
        attribute c_pijama_brazoscruzados:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_brazoscruzados.webp"
        attribute c_pijama_rascando1:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_rascando1.webp"
        attribute c_pijama_rascando2:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_rascando2.webp"
        attribute c_pijama_escoba:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_escoba.webp"
        attribute c_pijama_celu:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_celu.webp"
        attribute c_pijama_dedolabio:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_dedolabio.webp"
        attribute c_pijama_fuckyou:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_fuckyou.webp"
        attribute c_pijama_idea:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_idea.webp"
        attribute c_pijama_notok:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_notok.webp"
        attribute c_pijama_ok:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_ok.webp"
        attribute c_pijama_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_pensando.webp"
        attribute c_pijama_saludando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_saludando.webp"
        attribute c_pijama_señalando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_senalando.webp"
        attribute c_pijama_tetas:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_tetas.webp"
        attribute c_pijama_verguenza:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_verguenza.webp"
        attribute c_pijama_victoria:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_victoria.webp"
        attribute c_pijama_mangas:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_mangas.webp"
        attribute c_pijama_cajacosplay:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_cajacoxplay.webp"
        attribute c_pijama_bolsamadera:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bolsamadera.webp"

        # (Acá vivía el placeholder `c_tanga_base`, que apuntaba al cuerpo base.
        # La tanga pasó a ser su propio layeredimage `violet_tanga`, al final de
        # este archivo, junto con `violet_mojada`.)

        attribute c_none:
            Null()
    
    # Otros (efectos adicionales)
    group otros:
        attribute ot_none default:
            Null()
        attribute ot_avergonzada:
            "images/characters/casa/violet/violet_parada_otros_avergonzada.webp"

################################################################################
## Layeredimage: violet_espalda
################################################################################

layeredimage violet_espalda:

    # Grupo skin base — Violet de espaldas con su ropa de siempre.
    # Era un placeholder vacio hasta que llegó la primera imagen; NO se creó un
    # grupo aparte para la ropa base porque este ya lo era, y dos grupos para el
    # mismo atuendo se dibujarian como dos capas superpuestas.
    group skinbase:
        attribute sb_none default:
            Null()
        attribute sb_celular:
            "images/characters/casa/violet/violet_parada_espalda_rbase_celular.webp"

    # Grupo pijama — imágenes de espalda con skin pijama
    group pijama:
        attribute p_none default:
            Null()
        attribute p_base:
            "images/characters/casa/violet/violet_parada_espalada_pijama_base.webp"
        attribute p_cyberpunk:
            "images/characters/casa/violet/violet_parada_espalada_pijama_cyberpunk.webp"
        attribute p_fantasia:
            "images/characters/casa/violet/violet_parada_espalada_pijama_fantasia.webp"
        attribute p_novela:
            "images/characters/casa/violet/violet_parada_espalada_pijama_novela.webp"
        attribute p_pensando:
            "images/characters/casa/violet/violet_parada_espalada_pijama_pensando.webp"
        attribute p_rascando1:
            "images/characters/casa/violet/violet_parada_espalada_pijama_rascando1.webp"
        attribute p_rascando2:
            "images/characters/casa/violet/violet_parada_espalada_pijama_rascando2.webp"

    # Grupo eva — imágenes de espalda con skin eva
    group eva:
        attribute e_none default:
            Null()
        attribute e_base:
            "images/characters/casa/violet/violet_parada_espalada_eva_base.webp"
        attribute e_lista:
            "images/characters/casa/violet/violet_parada_espalada_eva_lista.webp"
        attribute e_pelo:
            "images/characters/casa/violet/violet_parada_espalada_eva_pelo.webp"
        attribute e_cola1:
            "images/characters/casa/violet/violet_parada_espalada_eva_cola1.webp"
        attribute e_cola2:
            "images/characters/casa/violet/violet_parada_espalada_eva_cola2.webp"


################################################################################
## Layeredimage: violet_mojada
################################################################################

layeredimage violet_mojada:
    group cuerpo:
        attribute c_mojada default:
            "images/quest/violet/quest08/violet_parada_mojada.webp"

    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_base.webp"

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/characters/casa/violet/violet_parada_boca_hablando.webp"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_hablandochica.webp"
        attribute b_sonrisaleve:
            "images/characters/casa/violet/violet_parada_boca_sonrisaleve.webp"
        attribute b_sorprendida:
            "images/characters/casa/violet/violet_parada_boca_abiertachica.webp"


################################################################################
## Layeredimage: violet_tanga_qd10
################################################################################
## Violet en ropa interior. Antes era `c_tanga_base`, una sección del grupo
## `cuerpo` de `violet_parada`; se separó a layeredimage propio para que su arte
## no tenga que encajar con los atributos de la ropa de siempre.
##
## El sufijo `_qd10` es a propósito: por ahora este arte se usa SOLO en la quest
## de deseo 10. Si más adelante aparece en otras escenas, ahí sí conviene
## renombrarlo a algo genérico y actualizar los `show`.
##
## NO tiene grupo de ojos: el arte del cuerpo ya los trae dibujados. Solo la boca
## va aparte, y su grupo se declara DESPUÉS del cuerpo para que se dibuje encima
## (en un layeredimage el orden de los grupos es el orden de las capas). Por lo
## mismo `otros` va ÚLTIMO: el rubor tiene que quedar sobre todas las demás.
##
## Los seis assets son de 680x1080, el mismo lienzo, así que las capas alinean
## sin offsets.

layeredimage violet_tanga_qd10:

    group cuerpo:
        attribute c_tanga default:
            "images/characters/casa/violet/violet_tanga_qd10_cuerpo.webp"
        attribute c_tomando:
            "images/characters/casa/violet/violet_tanga_qd10_cuerpotomando.webp"

    # Después del cuerpo = encima del cuerpo. El default es Null: boca cerrada.
    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/characters/casa/violet/violet_tanga_qd10_bocahablando.webp"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_tanga_qd10_bocahablandochica.webp"
        attribute b_sonrisa:
            "images/characters/casa/violet/violet_tanga_qd10_bocasonrisa.webp"

    # Otros (efectos adicionales). Último grupo = capa de más arriba.
    group otros:
        attribute ot_none default:
            Null()
        attribute ot_colorada:
            "images/characters/casa/violet/violet_tanga_qd10_rubor.webp"


################################################################################
## (Las imagenes de la quest de amor 15 se mudaron)
################################################################################
## Los fondos y los layeredimage de sus escenas (primer plano, caida, Violet
## sentada) vivian acá. El arco entero paso a
## ventajas/juegosnuevos/jn_pocketboy.rpy y quedo parkeado, asi que sus
## imagenes se declaran ahi junto al contenido que las usa.


################################################################################
## Layeredimage: violet_magica
################################################################################
## Violet disfrazada de maga. Es un layeredimage propio y no un grupo de
## `violet_parada` porque el disfraz trae su propia cabeza dibujada: no combina
## con los grupos `cabeza` ni `ojos` del sprite normal.
##
## DOS GRUPOS DE BOCA, y hay que elegir el que corresponde al cuerpo:
##   - de frente (c_base, c_mostrando, c_1..c_5) -> grupo `boca_frente`
##   - de espaldas (c_espalda)                   -> grupo `boca_espalda`
## Son archivos distintos porque la boca cae en otro lugar segun para donde
## mire. Los dos arrancan en Null: boca cerrada.
##
## Al cambiar de un cuerpo de frente a c_espalda hay que bajar la boca de frente
## a bf_none y subir la de espalda (y al revés), o quedarian las dos puestas.
##
## Los 12 assets son 680x1080, el mismo lienzo que el resto de los sprites de
## Violet, asi que se muestra con las mismas posiciones (`at right`, etc).

layeredimage violet_magica:

    group cuerpo:
        attribute c_base default:
            "images/characters/casa/violet/violet_parada_cuerpo_magica_base.webp"
        attribute c_espalda:
            "images/characters/casa/violet/violet_parada_cuerpo_magica_espalda.webp"
        attribute c_mostrando:
            "images/characters/casa/violet/violet_parada_cuerpo_magica_mostrando.webp"

    # Ojos. UN solo grupo con las dos versiones, no dos grupos: los ojos SIEMPRE
    # se ven (no hay estado "sin ojos"), asi que dos grupos con imagen por
    # defecto dibujarian los dos pares a la vez. Con un grupo unico se ve
    # exactamente uno, y `o_base` —la version de frente— es el default.
    #
    # Al girar hay que cambiarlo a mano, igual que la boca.
    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_magica_base.webp"
        attribute o_espalda:
            "images/characters/casa/violet/violet_parada_ojos_magica_espaldabase.webp"

    # Boca para los cuerpos de FRENTE.
    group boca_frente:
        attribute bf_none default:
            Null()
        attribute bf_hablando:
            "images/characters/casa/violet/violet_parada_boca_magica_hablando_frente.webp"
        attribute bf_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_magica_hablandochica_frente.webp"

    # Boca para el cuerpo de ESPALDAS.
    #
    # `be_sonrisa` es la boca "en reposo" de espaldas: al girar va esa, no
    # be_none. Se vuelve a ella al terminar cada linea, igual que en los cuerpos
    # de frente se vuelve a bf_none.
    group boca_espalda:
        attribute be_none default:
            Null()
        attribute be_sonrisa:
            "images/characters/casa/violet/violet_parada_boca_magica_espaldasonrisa.webp"
        attribute be_hablando:
            "images/characters/casa/violet/violet_parada_boca_magica_hablando_espalda.webp"
        attribute be_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_magica_hablandochica_espalda.webp"


################################################################################
## Layeredimage: beso_deseo_violet
################################################################################
## La secuencia del beso, cuadro por cuadro. UN SOLO GRUPO con diez atributos
## excluyentes: mostrar uno apaga el anterior, asi que la escena avanza con
## `show beso_deseo_violet bs_3` y nada mas — no hay que apagar el cuadro
## previo a mano.
##
## Es un layeredimage y no diez `image` sueltas justamente por eso: con
## imagenes separadas cada paso serian un show + un hide, y un olvido dejaria
## dos cuadros encimados.
##
## `bs_frenteafrente` es el default: el primer `show` sin atributos ya entra por
## ahi, que es como arranca la secuencia.
##
## Los diez assets son de 1920x1080 CON transparencia: son la pareja recortada,
## no un CG completo. Van encima del fondo de la locacion, asi que la escena
## tiene que dejar el `scene` de la habitacion puesto detras.

layeredimage beso_deseo_violet:

    group secuencia:
        attribute bs_frenteafrente default:
            "images/minijuegos/beso/violet/beso_deseo_frenteafrente.webp"
        attribute bs_1:
            "images/minijuegos/beso/violet/beso_deseo_secuencia1.webp"
        attribute bs_2:
            "images/minijuegos/beso/violet/beso_deseo_secuencia2.webp"
        attribute bs_3:
            "images/minijuegos/beso/violet/beso_deseo_secuencia3.webp"
        attribute bs_4:
            "images/minijuegos/beso/violet/beso_deseo_secuencia4.webp"
        attribute bs_5:
            "images/minijuegos/beso/violet/beso_deseo_secuencia5.webp"
        attribute bs_6:
            "images/minijuegos/beso/violet/beso_deseo_secuencia6.webp"
        attribute bs_7:
            "images/minijuegos/beso/violet/beso_deseo_secuencia7.webp"
        attribute bs_8:
            "images/minijuegos/beso/violet/beso_deseo_secuencia8.webp"
        attribute bs_9:
            "images/minijuegos/beso/violet/beso_deseo_secuencia9.webp"


################################################################################
## Layeredimage: beso_amor_violet
################################################################################
## El abrazo y el beso de la quest de amor 25, cuadro por cuadro. Hermano de
## `beso_deseo_violet`: mismo criterio, distinta escena.
##
## TRES GRUPOS. El primero es la SECUENCIA —un solo grupo con los nueve
## cuadros, o sea excluyentes: mostrar uno apaga el anterior—. Los otros dos son
## las BOCAS, una por personaje, y van declaradas DESPUES para dibujarse encima.
##
## Las dos bocas arrancan en Null y son independientes: se puede hablar de a uno
## o encimar los dos. Estan dibujadas para el cuadro del abrazo, que es donde
## pasa el unico dialogo de la secuencia.
##
## `ab_1` es el default: el primer `show` sin atributos ya entra por ahi, que es
## como arranca. Y tambien es donde vuelve al final, despues del beso.
##
## Los once assets son 1920x1080 CON transparencia: la pareja recortada, no un
## CG. Van encima del fondo de la locacion, asi que la escena tiene que dejar
## el `scene` de la habitacion puesto detras.

layeredimage beso_amor_violet:

    group secuencia:
        attribute ab_1 default:
            "images/quest/violet/amor25/abrazo1.webp"
        attribute ab_2:
            "images/quest/violet/amor25/abrazo2.webp"
        attribute ab_3:
            "images/quest/violet/amor25/abrazo3.webp"
        attribute ab_4:
            "images/quest/violet/amor25/abrazo4.webp"
        attribute ab_5:
            "images/quest/violet/amor25/abrazo5.webp"
        attribute bs_1:
            "images/minijuegos/beso/violet/beso_amor1.webp"
        attribute bs_2:
            "images/minijuegos/beso/violet/beso_amor2.webp"
        attribute bs_3:
            "images/minijuegos/beso/violet/beso_amor3.webp"
        attribute bs_4:
            "images/minijuegos/beso/violet/beso_amor4.webp"

    # Bocas. Despues de la secuencia = encima de ella.
    group boca_mc:
        attribute bmc_none default:
            Null()
        attribute bmc_hablando:
            "images/quest/violet/amor25/mc_hablando.webp"

    group boca_violet:
        attribute bv_none default:
            Null()
        attribute bv_hablando:
            "images/quest/violet/amor25/violet_hablando.webp"


################################################################################
## Layeredimage: violet_q30a
################################################################################
## Violet para la quest de amor 30. Es un layeredimage propio y no un grupo de
## `violet_parada` porque el arte trae la cabeza y la cara dibujadas: no combina
## con los grupos `cabeza` ni `ojos` del sprite de siempre.
##
## DOS GRUPOS. El cuerpo y, DESPUES, la boca — despues = encima. La boca arranca
## en Null (`b_none`): boca cerrada.
##
## DOS ROPAS EN EL MISMO GRUPO `cuerpo`: jean y jeanblanco. Son excluyentes, que
## es justo lo que se quiere — mostrar una apaga la otra, y no hay forma de
## dejar las dos puestas.
##
## LAS BOCAS DE FRENTE Y DE ESPALDAS TAMBIEN COMPARTEN GRUPO, aunque sean
## archivos distintos: la boca cae en otro lugar segun para donde mire, pero
## nunca se ven las dos a la vez. Al girar hay que cambiarla a mano — un cuerpo
## `_espalda` con una boca `bf_` deja la boca flotando.
##
##     bf_*  →  para los cuerpos de FRENTE
##     be_*  →  para los cuerpos _espalda
##
## Los 23 assets son 680x1080, el mismo lienzo que el resto de los sprites de
## Violet, asi que se muestra con las mismas posiciones (`at right`, etc).

layeredimage violet_q30a:

    group cuerpo:
        attribute c_jean_base default:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_base.webp"
        attribute c_jean_bajando1:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_bajando1.webp"
        attribute c_jean_bajando2:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_bajando2.webp"
        attribute c_jean_bajando3:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_bajando3.webp"
        attribute c_jean_bajando4:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_bajando4.webp"
        attribute c_jean_bajando5:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_bajando5.webp"
        attribute c_jean_tocando1:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_tocando1.webp"
        attribute c_jean_tocando2:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_tocando2.webp"
        attribute c_jean_tocando3:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_tocando3.webp"
        attribute c_jean_espalda:
            "images/characters/casa/violet/violet_parada_cuerpo_jean_espalda.webp"
        attribute c_jeanblanco_base:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_base.webp"
        attribute c_jeanblanco_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_pensando.webp"
        attribute c_jeanblanco_tocando1:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_tocando1.webp"
        attribute c_jeanblanco_tocando2:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_tocando2.webp"
        attribute c_jeanblanco_tocando3:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_tocando3.webp"
        attribute c_jeanblanco_tocando4:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_tocando4.webp"
        attribute c_jeanblanco_espalda:
            "images/characters/casa/violet/violet_parada_cuerpo_jeanblanco_espalda.webp"

    # Despues del cuerpo = encima del cuerpo. El default es Null: boca cerrada.
    group boca:
        attribute b_none default:
            Null()
        attribute bf_hablando:
            "images/characters/casa/violet/violet_parada_boca_frente_hablando.webp"
        attribute bf_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_frente_hablandochica.webp"
        attribute bf_sonrisa:
            "images/characters/casa/violet/violet_parada_boca_frente_sonrisa.webp"
        attribute be_hablando:
            "images/characters/casa/violet/violet_parada_boca_espalda_hablando.webp"
        attribute be_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_espalda_hablandochica.webp"
        attribute be_sonrisa:
            "images/characters/casa/violet/violet_parada_boca_espalda_sonrisa.webp"
