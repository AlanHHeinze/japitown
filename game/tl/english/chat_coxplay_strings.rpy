# Traducciones del chat de Tienda CoXplay.
#
# Los mensajes son strings de Python dentro de `init 6 python`, no diálogo, asi que
# se traducen con un bloque `strings` y no con bloques de diálogo por hash.
# Ren'Py los pasa por renpy.translate_string() al mostrarlos (hud_mensajes).
#
# La interpolacion [mc_name] la resuelve renpy.substitute() DESPUES de traducir,
# por eso se mantiene tal cual en el `new`.
#
# Cubre los 6 grupos del contacto "tienda_coxplay":
#   - chat_coxplay.rpy        → coxplay_q5a_g1 .. g4  (compra del Coxplay Box)
#   - chat_violet.rpy         → tienda_coxplay_q7b_g1 (reclamo por el cierre)
#                             → tienda_coxplay_q9a_g1 (aviso de paquete recibido)

translate english strings:

    # =========================================================================
    # Saludos segun horario (se insertan con .format en _coxplay_msg_recordar)
    # =========================================================================

    old "buen día"
    new "good morning"

    old "buenas tardes"
    new "good afternoon"

    # =========================================================================
    # Mensaje de bienvenida — presente en el historial desde el inicio del juego
    # (messagesystem_core: inicializar_chats). Se traduce al mostrarse.
    # =========================================================================

    old "Gracias por su compra en Coxplay, para futuras compras y consultas puede usar este canal"
    new "Thank you for your purchase at Coxplay. For future purchases and inquiries, you can use this channel."

    # =========================================================================
    # GRUPO 1 — El MC inicia contacto
    # =========================================================================

    old "Hola ¿Cómo están? Mi nombre es [mc_name], hice hace algunos días una compra con ustedes y estoy buscando un cosplay nuevo."
    new "Hi, how are you? My name is [mc_name]. I made a purchase with you a few days ago and I'm looking for a new cosplay."

    # =========================================================================
    # GRUPO 2 — Respuesta de la tienda y negociacion
    # =========================================================================

    old "Hola gracias por comunicarte con Tienda CoXplay, recuerda que nuestro horario de atención es de Lunes a Sábado por la mañana y tarde"
    new "Hello, thank you for contacting CoXplay Store. Remember that our business hours are Monday to Saturday, mornings and afternoons."

    # El {} lo reemplaza el saludo segun horario — conservarlo en el `new`.
    old "Hola [mc_name] {}, si me acuerdo ¿Qué estabas buscando?"
    new "Hello [mc_name], {}. Yes, I remember. What were you looking for?"

    old "Estoy buscando algo para la misma persona, el cosplay que le llevé no lo quiere usar en el evento"
    new "I'm looking for something for the same person. She doesn't want to wear the cosplay I brought her to the event."

    old "Entiendo, tenemos una box en promoción que incluye tres cosplay, te sale $200"
    new "I see. We have a box on sale that includes three cosplays, it comes to $200."

    old "Vas a tener más alternativas"
    new "That way you'll have more options."

    old "Es una buena idea, presentarle tres y que ella elija el que más le gusta, el precio también es conveniente"
    new "That's a good idea, showing her three and letting her pick the one she likes best. The price works for me too."

    old "Perfecto, puedes abonar a la misma cuenta"
    new "Perfect, you can pay to the same account."

    old "Una vez realizado el pago hacemos el envío"
    new "Once the payment goes through, we'll ship it."

    old "Muchas gracias, les aviso cuando les haga el pago"
    new "Thank you very much, I'll let you know once I've paid."

    old "Gracias a ti"
    new "Thank you."

    # =========================================================================
    # GRUPO 3 — Confirmacion del pago
    # =========================================================================

    old "El pago está realizado"
    new "The payment has been made."

    # =========================================================================
    # GRUPO 4 — Direccion de envio
    # =========================================================================

    old "Sí ya lo recibimos ¿Para dónde sería el envío?"
    new "Yes, we've received it. Where should we ship it?"

    old "Calle 69 casa 22, en Japitown"
    new "69 Street, house 22, in Japitown."

    old "Perfecto, el paquete estará en su domicilio en 2 días"
    new "Perfect, the package will be at your address in 2 days."

    old "Lo estaré esperando"
    new "I'll be waiting for it."

    # =========================================================================
    # QUEST 07_B — Reclamo por el cierre fallado (chat_violet.rpy)
    # =========================================================================

    old "Hola, buen día, me comunico porque tuve un problema con una compra"
    new "Hello, good morning. I'm reaching out because I had a problem with a purchase."

    old "Hola, buenas tardes, me comunico porque tuve un problema con una compra"
    new "Hello, good afternoon. I'm reaching out because I had a problem with a purchase."

    old "Hola [mc_name], buen día"
    new "Hello [mc_name], good morning."

    old "Hola [mc_name], buenas tardes"
    new "Hello [mc_name], good afternoon."

    old "Tengo dos compras con tu usuario: el traje de piloto 77 y el Coxplay Box"
    new "I have two purchases under your account: the Pilot 77 suit and the Coxplay Box."

    old "¿Con cuál tuvo el problema?"
    new "Which one did you have the problem with?"

    old "Con el traje de piloto 77"
    new "With the Pilot 77 suit."

    old "El cierre está fallado y se traba"
    new "The zipper is faulty and gets stuck."

    old "Lo sentimos mucho"
    new "We're very sorry."

    old "Se puede acercar a la tienda o enviarlo y le haremos el cambio del mismo"
    new "You can drop by the store or ship it to us and we'll replace it."

    old "Lo envío entonces"
    new "I'll ship it, then."

    old "Una vez que lo recibamos hacemos las revisiones y le enviamos el cambio"
    new "Once we receive it, we'll inspect it and send you the replacement."

    old "Muchas gracias por todo"
    new "Thank you very much for everything."

    old "Muchas gracias a ti"
    new "Thank you."

    old "y nuevamente perdón por el inconveniente"
    new "And again, sorry for the inconvenience."

    # =========================================================================
    # QUEST 09_A — La tienda avisa que recibio el paquete (chat_violet.rpy)
    # =========================================================================

    old "Buen día [mc_name], recibimos el paquete. Cuando esté la revisión lista le avisamos."
    new "Good morning [mc_name], we've received the package. We'll let you know once the inspection is done."

    old "Gracias"
    new "Thanks."
