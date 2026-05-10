# TODO: Translation updated at 2026-04-21 21:46

# game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:153
translate english conversacion_hablar_jasmine_8d9d5a79:

    # jasmine "[_preg['q']]"
    jasmine "[_preg['q']]"

# game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:157
translate english conversacion_hablar_jasmine_2bcd79c5:

    # jasmine "[_op0['resp']]"
    jasmine "[_op0['resp']]"

# game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:160
translate english conversacion_hablar_jasmine_2fb3d2a1:

    # jasmine "[_op1['resp']]"
    jasmine "[_op1['resp']]"

# game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:163
translate english conversacion_hablar_jasmine_31699c91:

    # jasmine "[_op2['resp']]"
    jasmine "[_op2['resp']]"

translate english strings:

    # game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:156
    old "[_txt_op0]"
    new "[_txt_op0]"

    # game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:159
    old "[_txt_op1]"
    new "[_txt_op1]"

    # game/script/characters/jasmine/interaction/conversacion_jasmine.rpy:162
    old "[_txt_op2]"
    new "[_txt_op2]"



translate english python:
    preguntas_hablar_jasmine = [
        {
            "q": "Hey! What are you doing? You're not being boring, are you?",
            "ops": [
                {"texto": "Nothing special, that's why I came to talk.", "resp": "Good choice! I'm the best option to not get bored.", "stat": "amor"},
                {"texto": "I was doing my things, calmly.", "resp": "Calmly... what a foreign concept to me.", "stat": "deseo"},
                {"texto": "Thinking, which is also useful.", "resp": "Oh, that sounded serious! I hope you were thinking about something fun.", "stat": "amor"},
            ]
        },
        {
            "q": "What's your favorite movie or series? I need a new recommendation.",
            "ops": [
                {"texto": "Depends on the genre, what do you like?", "resp": "I like everything! Surprise me.", "stat": "deseo"},
                {"texto": "I watch a bit of everything, I don't have a favorite.", "resp": "That's strategic, you never get disappointed.", "stat": "amor"},
                {"texto": "I can give you some options if you want.", "resp": "Yes! Can we watch them together someday?", "stat": "amor"},
            ]
        },
        {
            "q": "Do you prefer big plans with lots of people or something quieter?",
            "ops": [
                {"texto": "Depends on the moment, but both have their charm.", "resp": "That's ideal! Total flexibility.", "stat": "amor"},
                {"texto": "Something quieter, in small groups.", "resp": "I'm the opposite, but I get it. I can still convince you!", "stat": "amor"},
                {"texto": "As long as there's good energy, I adapt.", "resp": "I love that attitude! Good energy is what we have here.", "stat": "deseo"},
            ]
        },
        {
            "q": "Are you the type who listens to music all the time or do you prefer silence?",
            "ops": [
                {"texto": "Music almost always, yeah.", "resp": "Obviously! Silence is weird. What do you listen to?", "stat": "amor"},
                {"texto": "I like silence to concentrate.", "resp": "Respect, though it would be really hard for me.", "stat": "amor"},
                {"texto": "A bit of both depending on what I'm doing.", "resp": "The perfect balance. Very wise.", "stat": "deseo"},
            ]
        },
        {
            "q": "What would you do if you had a free day with no commitments?",
            "ops": [
                {"texto": "Go out, do something different.", "resp": "Exactly! Life is not enjoyed staying at home.", "stat": "deseo"},
                {"texto": "Rest, no drama.", "resp": "Sometimes resting is the best plan. To each their own.", "stat": "amor"},
                {"texto": "Depends on how I feel that day.", "resp": "That's mysterious! I like it.", "stat": "amor"},
            ]
        },
        {
            "q": "What do you think of people who take everything too seriously?",
            "ops": [
                {"texto": "They're fine, everyone has their way of being.", "resp": "That says a lot about you. You're tolerant!", "stat": "amor"},
                {"texto": "Sometimes it's tiring to be with such serious people.", "resp": "Exactly! Life can also be light.", "stat": "deseo"},
                {"texto": "Depends on the situation, it's not always bad.", "resp": "True, true. Context above all.", "stat": "amor"},
            ]
        },
        {
            "q": "Is there anything in this house that still surprises you or that you didn't expect?",
            "ops": [
                {"texto": "Several things, it's more interesting than it seemed.", "resp": "Haha! There are always hidden things in places. I'm glad!", "stat": "amor"},
                {"texto": "To be honest, I got used to it fast.", "resp": "That's great! Adapting quickly is a virtue.", "stat": "deseo"},
                {"texto": "It surprises me how well everything works.", "resp": "It's because Monica leaves nothing to chance!", "stat": "amor"},
            ]
        },
        {
            "q": "What was the best plan you made recently?",
            "ops": [
                {"texto": "Nothing too epic, but I had a good time.", "resp": "The best plans are usually the simplest ones!", "stat": "deseo"},
                {"texto": "I haven't had many plans lately.", "resp": "That changes now! I can't leave you without plans.", "stat": "amor"},
                {"texto": "Talking to you, I guess.", "resp": "Awww! That was very sweet. Officially recognized.", "stat": "amor"},
            ]
        },
        {
            "q": "Are you one to give advice or do you prefer not to meddle in others' business?",
            "ops": [
                {"texto": "I give advice if asked, I don't just meddle.", "resp": "That's respectful! Though sometimes I struggle with boundaries.", "stat": "amor"},
                {"texto": "I like to help, even if they don't ask.", "resp": "Me too! Sometimes it works, sometimes... not so much.", "stat": "amor"},
                {"texto": "Depends on who and what it's about.", "resp": "Selective criteria. Not bad.", "stat": "deseo"},
            ]
        },
        {
            "q": "What do you like most about talking to me?",
            "ops": [
                {"texto": "That there's always something to tell.", "resp": "Exactly! Life is never boring if you tell it well.", "stat": "amor"},
                {"texto": "That you don't have to think too much, it just flows.", "resp": "Exactly! The best conversations are like that.", "stat": "amor"},
                {"texto": "You make me laugh without much effort.", "resp": "It's my superpower! Glad it works.", "stat": "deseo"},
            ]
        }
    ]

