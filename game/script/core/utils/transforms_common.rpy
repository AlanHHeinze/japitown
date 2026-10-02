
################################################################################
## Transforms comunes — Movimientos, posiciones y efectos de sprites
################################################################################


# =============================================================================
# POSICIONES ESTÁTICAS
# =============================================================================

# MC en posición izquierda, flipeado hacia la derecha
transform mc_izquierda:
    xpos 0.15
    xanchor 0.5
    xzoom -1.0

# MC cerca del centro, mira a la derecha (borde derecho del sprite en x=960)
transform mc_cerca:
    xpos 960
    xanchor 1.0
    xzoom -1.0

# NPC cerca del centro, mira a la izquierda (borde izquierdo del sprite en x=960)
transform npc_cerca:
    xpos 960
    xanchor 0.0

# TRES NPCs a la derecha, ligeramente montados, con el MC en su mc_izquierda.
# Es la escena de cuatro personajes: la usa la intro (Violet / Jasmine / Monica
# en ese orden) y la escena final de la quest de amor 25.
#
# El ORDEN DE PROFUNDIDAD no lo dan estos numeros sino el orden de los `show`:
# el ultimo queda al frente.
transform grupo3_izq:
    xpos 0.58
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0

transform grupo3_centro:
    xpos 0.70
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0

transform grupo3_der:
    xpos 0.82
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0

# El `xzoom 1.0` de los tres de arriba NO es redundante: al cambiar de transform
# Ren'Py le pasa al nuevo las propiedades que este no define. Sin el, un sprite
# que estaba en la version `_flip` volvia a su lugar SEGUIA espejado.
#
# Los mismos tres lugares ESPEJADOS: el sprite queda en el mismo punto (el
# anclaje es el centro) pero mira a la derecha. Sirven para que una del grupo
# mire a la que tiene al costado derecho. Van como transforms propios y no como
# `at grupo3_izq, personaje_flip` por lo mismo que right_flip (mas abajo).
transform grupo3_izq_flip:
    xpos 0.58
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom -1.0

transform grupo3_centro_flip:
    xpos 0.70
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom -1.0

transform grupo3_der_flip:
    xpos 0.82
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom -1.0

# DOS personajes ademas del MC: uno en `right` y otro aca, en el centro. Las
# posiciones grupo3_* son para TRES y con dos quedan montadas sin necesidad.
#
# Es el `center` de Ren'Py pero con la orientacion EXPLICITA (xzoom), para que
# el que se gira pueda volver: con el `center` pelado el espejado de la version
# _flip se heredaba y el sprite quedaba dado vuelta (ver grupo3_izq).
transform centro_npc:
    xpos 0.5
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0

# El del centro mirando a la derecha (al que esta en `right`).
transform centro_npc_flip:
    xpos 0.5
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom -1.0

# La de la IZQUIERDA del grupo se APARTA: da unos pasos hacia la izquierda y
# recien ahi se da vuelta a mirar a las otras. Separada no se enciman los
# sprites al girar (en grupo3_izq, espejada, se monta sobre la del centro).
#
# 0.47 sale de medir el sprite de Violet: el dibujo ocupa ~455 de los 680 px del
# lienzo, y espejado en 0.47 su borde derecho queda justo antes del de la que
# esta en grupo3_centro. Y a la izquierda le queda lugar al MC en mc_izquierda.
transform grupo3_izq_apartarse:
    xpos 0.58
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0
    ease 0.6 xpos 0.47
    xzoom -1.0

# Ya apartada: mirando a la izquierda (al MC) o espejada (al grupo).
transform grupo3_izq_aparte:
    xpos 0.47
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom 1.0

transform grupo3_izq_aparte_flip:
    xpos 0.47
    xanchor 0.5
    yanchor 1.0
    ypos 1.0
    xzoom -1.0

# Los mismos dos lugares, pero LLEGANDO: parten de mc_izquierda / right y se
# acercan hasta quedar frente a frente. Terminan EXACTAMENTE en mc_cerca y
# npc_cerca, asi que se pueden encadenar con ellos sin que el sprite salte.
#
# El punto de partida va en PIXELES y no en fracciones (0.15, xalign 1.0) a
# proposito: Ren'Py no interpola bien entre un xpos float —que lee como
# fraccion de pantalla— y uno int —que lee como pixeles—, y el sprite pega un
# salto en el primer frame. 288 = 0.15 * 1920 y 1920 = el borde derecho, o sea
# los mismos lugares de los que salen.
transform mc_acercarse:
    xpos 288
    xanchor 0.5
    xzoom -1.0
    linear 0.8 xpos 960 xanchor 1.0

transform npc_acercarse:
    xpos 1920
    xanchor 1.0
    linear 0.8 xpos 960 xanchor 0.0

# MC en posición intro nocturna
transform mc_intro_micro_noche_transform:
    xalign 0.62
    yalign 1.0

# Solo gira en X (espejo horizontal), sin tocar ninguna otra propiedad
transform girar_x:
    xzoom -1.0

# El `right` de Ren'Py pero ESPEJADO. Los valores son los del transform estandar
# (renpy/common/00definitions.rpy:37) mas el xzoom, asi que ocupa exactamente el
# mismo rectangulo de pantalla: el zoom negativo espeja la superficie y el
# anclaje se calcula sobre el mismo ancho.
#
# Va como transform PROPIO y no como `at right, girar_x`: en una lista `at` cada
# transform envuelve al anterior, asi que mezclar posicionamiento con zoom queda
# a merced del orden. Con las cuatro propiedades en el mismo nivel no hay nada
# que interpretar.
transform right_flip:
    xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0
    xzoom -1.0

# Flip horizontal instantáneo (para usar en cadena con at)
transform personaje_flip:
    xzoom -1.0
    yzoom 1.0

# Vuelve a orientación normal instantáneamente
transform personaje_enderezar:
    xzoom 1.0
    yzoom 1.0


# =============================================================================
# ENTRADAS — hacia posición izquierda
# =============================================================================

# Entra desde fuera por la izquierda hacia posición izquierda
transform personaje_entrar_pizquierda:
    xalign -0.5 yalign 1.0
    linear 1.4 xalign 0.0

# Entra desde la derecha hacia posición izquierda
transform personaje_entrar_derecha_pizquierda:
    xalign 1.5 yalign 1.0
    linear 1.4 xalign 0.0

# Entra desde la derecha mirando a la izquierda, gira al llegar
transform personaje_entrar_derecha_y_giro_pizquierda:
    xzoom -1.0
    xalign 1.5 yalign 1.0
    easein 1.8 xalign 0.0
    pause 0.1
    xzoom 1.0


# =============================================================================
# ENTRADAS — hacia el centro
# =============================================================================

# Entra desde fuera por la izquierda hasta el centro (suave)
transform entrar_izquierda_centro:
    xalign -0.5
    yalign 1.0
    ease 1.2 xalign 0.5

# Entra desde fuera por la derecha hasta el centro (suave)
transform entrar_derecha_centro:
    xalign 1.5
    yalign 1.0
    ease 1.2 xalign 0.5

# Mueve desde el borde derecho visible hasta el centro
transform derecha_a_centro:
    xalign 1.0
    easein 0.8 xalign 0.5


# =============================================================================
# ENTRADAS — hacia posición derecha (right)
# =============================================================================

# Entra violet_espalda (680px) desde fuera por la derecha hasta right
transform entrar_derecha_aright:
    xpos 2600
    xanchor 1.0
    ypos 1.0
    yanchor 1.0
    ease 1.2 xpos 1920

# Entra desde fuera por la izquierda hasta la posición right, flipeada (mirando
# a la derecha mientras camina) y al llegar gira en X a su orientación original.
transform reentrar_izquierda_a_right:
    xzoom -1.0
    xalign -0.3 yalign 1.0
    ease 1.5 xalign 1.0
    xzoom 1.0

# El mismo estado FINAL del transform de arriba, pero quieto.
#
# VA DESPUES DEL `pause` QUE ESPERA LA ANIMACION. El `pause` es una interaccion,
# asi que un click lo corta — y con el se corta el `ease`: el sprite se queda
# donde iba, a mitad de camino, y ahi se queda el resto de la escena. Reafirmar
# la posicion final lo deja en su lugar igual, con click o sin click. Sin click
# no se nota nada, porque el sprite ya estaba justo ahi.
#
# Los dos valores tienen que seguir a los del transform animado: si uno cambia,
# el otro tambien.
transform reentrar_izquierda_a_right_final:
    xzoom 1.0
    xalign 1.0 yalign 1.0

# Entra desde la derecha ya flipeado hasta right (par de right_a_salir)
transform entrar_a_right:
    xzoom 1.0
    xpos 2800
    xanchor 1.0
    ypos 1.0
    yanchor 1.0
    ease 1.2 xpos 1920

# Mueve violet_espalda desde fuera hacia right (parcial: 1/3 visible)
transform entrar_poquito:
    xpos 2147
    xanchor 1.0
    ypos 1.0
    yanchor 1.0
    ease 0.6 xpos 1920


# =============================================================================
# SALIDAS
# =============================================================================

# Sale hacia la izquierda (desde posición actual)
transform personaje_salir_izquierda:
    ease 1.5 xalign -0.6

# Sale hacia la derecha
transform personaje_salir_derecha:
    xalign 0.0 yalign 1.0
    linear 1.5 xalign 1.5

# Se da vuelta y sale por la derecha DESDE DONDE ESTA. A diferencia de
# personaje_salir_derecha (que arranca en xalign 0.0, o sea que el sprite salta
# al borde izquierdo y cruza toda la pantalla), este no fija el punto de
# partida: el `ease` parte de la posicion que el sprite ya tenia. El xzoom -1
# lo deja mirando hacia donde camina (los sprites base miran a la izquierda).
transform salir_derecha_mirando:
    xzoom -1.0
    ease 1.5 xalign 1.6

# MC sale hacia la izquierda (más rapido). El xzoom 1.0 lo ENDEREZA primero: en
# mc_izquierda está espejado mirando a la derecha, así que al irse se da vuelta
# y camina mirando hacia donde va.
transform mc_salir_izquierda:
    xzoom 1.0
    yzoom 1.0
    ease 0.8 xpos -0.2

# El PAR de mc_salir_izquierda: vuelve a entrar por el mismo borde y termina
# exactamente en el estado de mc_izquierda (misma xpos, mismo anchor, mismo
# espejo), así que se puede encadenar con él sin que el sprite salte.
#
# xpos en FRACCIÓN en los dos extremos (-0.2 → 0.15) por lo que explica
# mc_acercarse: Ren'Py no interpola entre una fracción y un entero, y el sprite
# pega un salto en el primer frame.
transform mc_entrar_izquierda:
    xpos -0.2
    xanchor 0.5
    xzoom -1.0
    ease 0.8 xpos 0.15

# Flip + salida hacia la izquierda (para sprites de quest)
transform flip_y_salir_izquierda:
    xzoom -1.0
    ease 0.8 xalign -0.3

# Flip + salida hacia la derecha (sprite en right mira afuera y se va)
transform right_a_salir:
    xpos 1920
    xanchor 1.0
    ypos 1.0
    yanchor 1.0
    xzoom -1.0
    ease 1.2 xpos 2800

# Sale violet_espalda (680px) completamente fuera por la derecha
transform salir_todo:
    xpos 1920
    xanchor 1.0
    ypos 1.0
    yanchor 1.0
    ease 1.2 xpos 2600

# Sale violet_espalda (680px) parcialmente (1/3 fuera)
transform salir_poquito:
    xpos 1920
    xanchor 1.0
    ypos 1.0
    yanchor 1.0
    ease 0.6 xpos 2147


# =============================================================================
# MOVIMIENTOS INTERNOS — de una posición visible a otra
# =============================================================================

# Mueve desde posición actual hacia el centro
transform mover_al_centro:
    easein 1.0 xalign 0.5 yalign 0.5

transform mover_al_centro_rapido:
    easein 0.5 xalign 0.5 yalign 0.5

transform mover_al_centro_lento:
    easein 1.5 xalign 0.5 yalign 0.5

# Solo centra horizontalmente (mantiene Y)
transform mover_al_centro_horizontal:
    easein 1.0 xalign 0.5

# Del centro (mirando a la derecha) hasta right, girando al llegar para quedar
# mirando a la izquierda. Para cuando un personaje que hablaba con alguien a su
# derecha se corre y se da vuelta hacia el MC.
transform centro_a_right_y_giro:
    xalign 0.5
    yalign 1.0
    xzoom -1.0
    ease 1.0 xalign 1.0
    xzoom 1.0


# =============================================================================
# EFECTOS VISUALES
# =============================================================================

define fade_white = Fade(1.0, 0.5, 1.0, color="#FFFFFF")

transform remember_text_anim:
    alpha 0.0
    linear 0.3 alpha 1.0
    pause 1.2
    linear 0.5 alpha 0.0
