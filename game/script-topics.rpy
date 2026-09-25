label random1:
    $ persistent.affection += 1
    if persistent.afflike == True and persistent.whoruseen == False:
        show oc nb smile normal
        e "Hey, [playername]..."
        show oc hb smile lookleft
        e "Who... are you?"
        call moveocmenu
        menu:
            "What do you mean?":
                call movegoback
                show oc hb frown closed
                e "I know you as [playername], sure,"
                show oc hb frown normal
                e "But who are {i}you{/i} in relation to me?"
                call moveocmenu
                menu:
                    "I'm not sure I can answer that yet.":
                        call movegoback
                        show oc nub frown closed
                        e "..."
                        show oc nb smile hapclosed
                        e "It's okay. I understand."
                        e "I'll ask about it some other time, then."
                        $ persistent.whoruseen = True
    elif persistent.whoruseen == True:
        show oc nb oh closed
        e "..."
        e "zzz..."
        menu:
            "[persistent.ocname]?":
                show oc nb wow bshocked at ugo2
                e "Ah~ [playername]!"
                show oc sb smile hapclosed
                e "Guess I got caught napping~"
    else:
        pass

    jump worldidle

label random2:
    $ persistent.affection += 1
    show oc hb smile lookleft
    e "Hmm..."
    show oc nb smile bshocked at ugo2
    e "Oh~ [playername]!"
    show oc sb smile hapclosed
    e "You always catch me off guard."
    show oc nb smile lookright
    $ acrd = renpy.random.choice(["I was just drawing something.", "I started working on a sewing project.", "I was just sorting my pencils~", "I was writing something down.", "I was just about to eat~"])
    e "[acrd]"
    show oc nb smile hapclosed
    e "Care to join me?"
    jump worldidle

label random3:
    $ persistent.affection += 1
    show oc nub frown normal
    e "..."
    show oc ab frown lookleft
    e "... This whole situation is still so... weird."
    show oc ab frown closed
    e "Not {i}you{/i}, specifically. Just..."
    show oc nub smile hapclosed
    e "It's fine! Let's continue, shall we~"
    jump worldidle

default persistent.rpcunlocked = False

label random4:
    $ persistent.affection += 1
    show oc nb smile hapclosed
    e "Hey, [playername]! I had an idea!"
    show oc nb smile lookleft
    e "Soo..."
    show oc nb smile lookright
    extend "You like games, right?"
    call moveocmenu
    menu:
        "Sure?":
            call movegoback
            show oc hapclosed
            e "Great!"
    show oc nb normal
    e "I thought we could play rock, paper, sissors if we're bored."
    show oc hb lookleft
    e "It's a game I played a lot as a kid, so maybe it'll fill the time?"
    show oc nb hapclosed
    e "Regardless, just ask me if you're interested!"
    $ persistent.rpcunlocked = True
    jump worldidle

init python:
    topicpool.append("rando5")

label rando5:
    $ persistent.affection += 1
    hide oc 
    with dissolve
    e "..."
    show oc nb smile hapclosed at center zorder 4
    with dissolve
    e "I'm back! Sorry, I went to grab something."
    jump worldidle