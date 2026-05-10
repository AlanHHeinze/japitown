# TODO: Translation updated at 2026-04-21 21:46

# game/script/characters/violet/interaction/conversacion_violet.rpy:153
translate english conversacion_hablar_violet_0e01f614:

    # violet "[_preg['q']]"
    violet "[_preg['q']]"

# game/script/characters/violet/interaction/conversacion_violet.rpy:157
translate english conversacion_hablar_violet_92f92889:

    # violet "[_op0['resp']]"
    violet "[_op0['resp']]"

# game/script/characters/violet/interaction/conversacion_violet.rpy:160
translate english conversacion_hablar_violet_6d2bbcf6:

    # violet "[_op1['resp']]"
    violet "[_op1['resp']]"

# game/script/characters/violet/interaction/conversacion_violet.rpy:163
translate english conversacion_hablar_violet_bb568820:

    # violet "[_op2['resp']]"
    violet "[_op2['resp']]"



translate english python:
    preguntas_hablar_violet = [
        {
            "q": "Did you lose something, or are you staring at me?",
            "ops": [
                {"texto": "I was just passing by.", "resp": "Uh-huh. Sure you were 'passing by' right where I am.", "stat": "amor"},
                {"texto": "I stared by accident, sorry.", "resp": "It's fine. At least you're honest.", "stat": "deseo"},
                {"texto": "I was thinking about something else.", "resp": "I hope so.", "stat": "amor"},
            ]
        },
        {
            "q": "Does the noise bother you when I'm listening to music?",
            "ops": [
                {"texto": "Not at all, play it as much as you want.", "resp": "It's the first time someone doesn't complain.", "stat": "deseo"},
                {"texto": "Depends on the volume, to be honest.", "resp": "Makes sense. I'll try not to turn it up too much.", "stat": "amor"},
                {"texto": "Sometimes I even like it, sounds good.", "resp": "...Thanks. I wasn't expecting that.", "stat": "amor"},
            ]
        },
        {
            "q": "How do you get along with the people in this house?",
            "ops": [
                {"texto": "More or less, everyone has their own vibe.", "resp": "That's pretty accurate.", "stat": "amor"},
                {"texto": "Good, I get along well with everyone, including you.", "resp": "Including me, of course. How generous.", "stat": "amor"},
                {"texto": "I just try not to bother anyone.", "resp": "That's already a lot more than what others do.", "stat": "deseo"},
            ]
        },
        {
            "q": "Do you get bored being here doing nothing?",
            "ops": [
                {"texto": "As long as something interesting happens, I can handle it.", "resp": "Depends on what counts as 'interesting'.", "stat": "amor"},
                {"texto": "Sometimes yes, but I entertain myself.", "resp": "Self-sufficient. That's rare around here.", "stat": "amor"},
                {"texto": "A bit, but I'm not complaining.", "resp": "Hm. Some people would complain anyway.", "stat": "deseo"},
            ]
        },
        {
            "q": "Why did you come to talk to me today?",
            "ops": [
                {"texto": "Because I wanted to see how you were doing.", "resp": "...That's unexpected.", "stat": "deseo"},
                {"texto": "Do I need a reason?", "resp": "No. But not many people come without one.", "stat": "amor"},
                {"texto": "I was free, that's all.", "resp": "At least you're honest. That's appreciated.", "stat": "amor"},
            ]
        },
        {
            "q": "Does it bother you when someone doesn't talk much?",
            "ops": [
                {"texto": "No. Sometimes silence speaks louder than words.", "resp": "That sounds like a poster quote, but... yes.", "stat": "amor"},
                {"texto": "I prefer listening rather than talking too much.", "resp": "That's rarer than you think.", "stat": "deseo"},
                {"texto": "Depends on the person. With you, it doesn't bother me.", "resp": "...Well. That was unexpected.", "stat": "amor"},
            ]
        },
        {
            "q": "Have you ever felt like no one understands you?",
            "ops": [
                {"texto": "Sometimes, but I think it happens to everyone.", "resp": "Maybe. Though not everyone admits it.", "stat": "amor"},
                {"texto": "Yes. But I learned not to depend on that.", "resp": "That's... pretty strong.", "stat": "deseo"},
                {"texto": "Not really, to be honest. But I understand.", "resp": "Lucky you.", "stat": "amor"},
            ]
        },
        {
            "q": "What would you think if I told you I trust almost no one?",
            "ops": [
                {"texto": "I get it. Trust is earned, not asked for.", "resp": "...Exactly.", "stat": "deseo"},
                {"texto": "Everyone has their reasons. I don't judge.", "resp": "That's good.", "stat": "amor"},
                {"texto": "I hope you can trust me over time.", "resp": "...We'll see.", "stat": "amor"},
            ]
        },
        {
            "q": "Is there anything you would like to change about how you live here?",
            "ops": [
                {"texto": "Every change starts from within.", "resp": "That sounds like coach advice, but it's true.", "stat": "amor"},
                {"texto": "Maybe spend more time with the people in the house.", "resp": "...Interesting.", "stat": "amor"},
                {"texto": "Not much. I'm grateful for what we have.", "resp": "That's healthy.", "stat": "deseo"},
            ]
        },
        {
            "q": "Do you think we talk too little or too much?",
            "ops": [
                {"texto": "I'd like it to be more.", "resp": "...I'll keep that in mind.", "stat": "amor"},
                {"texto": "Just enough.", "resp": "Practical. That's fine.", "stat": "amor"},
                {"texto": "Whatever you need, I adapt.", "resp": "...That's rare coming from someone.", "stat": "deseo"},
            ]
        }
    ]

