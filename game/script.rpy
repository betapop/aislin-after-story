# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

init python:
    config.ftfont_scale["OpenDyslexic.otf"] = .7
    config.ftfont_vertical_extent_scale["OpenDyslexic.otf"] = .8

    # This is set to the name of the character that is speaking, or
    # None if no character is currently speaking.
    speaking = None
  
    # This returns speaking if the character is speaking, and done if the
    # character is not.
    def while_speaking(name, speak_d, done_d, st, at):
        if speaking == name:
            return speak_d, .1
        else:
            return done_d, None
  
    # Curried form of the above.
    curried_while_speaking = renpy.curry(while_speaking)
  
    # Displays speaking when the named character is speaking, and done otherwise.
    def WhileSpeaking(name, speaking_d, done_d=Null()):
        return DynamicDisplayable(curried_while_speaking(name, speaking_d, done_d))
  
    # This callback maintains the speaking variable.
    def speaker_callback(name, event, **kwargs):
        global speaking
       
        if event == "show":
            renpy.sound.play("audio/bleep015.ogg", channel="sound", loop=True)
            speaking = name
        elif event == "slow_done" or event == "end":
            speaking = None
            renpy.sound.stop(channel="sound", fadeout=1)
  
    # Curried form of the same.
    speaker = renpy.curry(speaker_callback)

# init python:
#    def bleep015(event, **kwargs):
#        if event == "show":
#            renpy.music.play("audio/bleep015.ogg", channel="sound", loop=True)
#        elif event == "slow_done" or event == "end":
#            renpy.music.stop(channel="sound", fadeout=1)

init:
    transform ocright:
        xpos 1300

    transform furnright:
        xpos 350

label moveocmenu:
    show chair at furnright
    show table at furnright
    show oc at ocright
    with ease

    return

label movegoback:
    show chair at left zorder 2
    show table at left zorder 5
    show oc at center zorder 4
    with ease

    return


screen choice(items):
    style_prefix "choice"
    default time_delay = 0.06

    fixed pos (150,100) xysize (900,800):
        viewport:
            if len(items) >= 8:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xmaximum 700
                ymaximum 700
                side_yfill True

            vbox:
                for i, item in enumerate(items, start=1):
                    textbutton item.caption:
                        action item.action
                        at animated_button_show(i * time_delay)

transform animated_button_show(time_delay):
    alpha 0.0
    yoffset 20
    pause time_delay
    parallel:
        ease 0.3 yoffset 0
    parallel:
        easeout 0.3 alpha 1.0
    on hide:
        ease 0.2 alpha 0.0

    on hover: 
        linear 0.15 zoom 1.05

    on idle: 
        linear 0.15 zoom 1.0

image nightsky = Movie(size=(1920, 1080), play="images/sky/night.webm")
image morningsky = Movie(size=(1920, 1080), play="images/sky/day.webm")
image afternoonsky = Movie(size=(1920, 1080), play="images/sky/afternoon.webm")
image eveningsky = Movie(size=(1920, 1080), play="images/sky/evening.webm")

label start:

    show blackbg 

    $hour = datetime.datetime.now().hour        ######### this will verify what time it currently is
    
    if hour in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:            ######### type here the hour you want the image to be displayed
        scene morningsky
        $startTime= 6
        $endTime= 16

    if hour in [17, 18]:
        scene afternoonsky
        $startTime= 17
        $endTime= 18

    if hour in [18, 19, 20]:
        scene eveningsky
        $startTime= 18
        $endTime= 20
        
    if hour in [21, 22, 23, 00, 1, 2, 3, 4, 5]:   
        scene nightsky
        $startTime= 21
        $endTime= 5
    
    jump loadstart



label main_menu:
    return

define e = Character("[persistent.ocname!cl]", what_slow_cps=50, color="#ffffff", callback=speaker("e"))
default persistent.ocname = "Aislin"
define playername = Character("[persistent.pname!cl]")
default persistent.pname = "Player"

default persistent.whoruseen = False

define gbrd = renpy.random.choice(["Ah, see you later.", "Adieu!~", "Until we meet again~", "Have fun out there~", "Good luck~", "Have a good one."] )
define config.layers = ['bgroom', 'behindbuttons', 'master', 'transient', 'screens', 'overlay']
default persistent.saidgoodbye = True

image mainroom = "background/mainroom.png"
image table = "oc/other/table.png"
image chair = "oc/other/chair.png"
image mainsky = Movie(size=(1920, 1080), play="images/sky/sky.webm")

define _game_menu_screen = "preferences"

default persistent.isnew = True
default persistent.headpatseen = False
default persistent.hasleftbf = False

default persistent.randomchatter = True

$ _skipping = False
define config.allow_skipping = False 
define config.rollback_enabled = False 
$ renpy.block_rollback()
$ yesno = layout.yesno_screen()

init python:
    config.quit_action = ui.gamemenus("quit_prompt")


label quit_prompt:
    if persistent.isnew == True:
        return
    elif persistent.hasleftbf == False:
        $ persistent.saidgoodbye = False
        
        show oc hb smile hapclosed
        e "Leaving now, are we?"
        show oc nb smile normal
        e "Well, I suppose I'll see you later, then."
        e "I hope you have a good one, [playername]."
        call moveocmenu
        menu:
            "Goodbye, [persistent.ocname].":
                call movegoback
                $ persistent.saidgoodbye = True
                show oc nb smile hapclosed
        $ persistent.hasleftbf = True
        $ renpy.pause(0.1, hard=True)
        $ Quit(confirm=False)()
    else:
        $ persistent.saidgoodbye = False
        show oc nb smile normal
        e "[gbrd]"
        call moveocmenu
        menu:
            "Goodbye, [persistent.ocname].":
                call movegoback
                show oc nb smile hapclosed
                $ persistent.saidgoodbye = True
            "...":
                call movegoback
                show oc nub frown lookleft
            "Nevermind!":
                call movegoback
                show oc hb smile hapclosed
                e "Changed your mind, hm?"
                e "Well I don't mind a little extra attention~"
                $ persistent.saidgoodbye = False
                jump worldidle

        $ renpy.pause(0.1, hard=True)
        $ Quit(confirm=False)()

init python:
    import time

    year, month, day, hour, minute, second, dow, doy, dst = time.localtime()


# The game starts here.

screen headpather():
    imagebutton:
        xpos 780 ypos 20
        idle "/gui/headpat.png"
        hover "/gui/headpat.png"
        action Jump("ocheadpat")

label ocheadpat:
    hide screen menuButton
    hide screen headpather
    with dissolve

    if persistent.headpatseen == False:
        $ persistent.headpatseen = True
        show oc nb frown bshocked
        e "..."
        show oc nb smile bplayful
        e "Headpats, hm?"
        show oc nb smile lookright
        e "Well, I won't say i'm adverse to it~"
        jump worldidle
    else:
        $ hedrd = renpy.random.choice(["Headpat...", "A headpat, hm?~", "Pff, haha...", "Another headpat~"])
        show oc sb smile hapclosed
        e "[hedrd]"
    jump worldidle

label loadstart:


    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    if persistent.isnew is True:
        jump newgame
    
    elif persistent.saidgoodbye is False:
        jump nogoodbye

    elif persistent.isnew is False:
        jump continuegame

    else: 
        jump newgame


label nogoodbye:

    show mainroom
    $ persistent.saidgoodbye = True
    $ affloss = renpy.random.randint(5, 20)
    $ persistent.affection -= affloss
    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen smile.png" to the images
    # directory.
    show chair at center zorder 2
    show table at center zorder 5
    show oc ab frown lookright at center zorder 4
    with fade
    $ nogbrd = renpy.random.choice(["Too good for 'goodbyes' now, huh?", "...", "Why didn't you say goodbye back?", "I'm just not in a good mood right now.", "Be a little nicer, alright?"])
    e "[nogbrd]"
    show oc ab frown closed
    $ renpy.pause(1, hard=True)
    show oc nub frown closed
    e "Lets just... move on. Okay?"
    show oc nub frown lookleft
    e "Just say it back next time, thats all."
    jump worldidle
  
label continuegame:    
    show mainroom

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen smile.png" to the images
    # directory.
    show chair at center zorder 2
    show table at center zorder 5
    show oc nb smile normal at center zorder 4
    with fade

    $ hlrd = renpy.random.choice(["Welcome in, ", "Hi there, ", "Oh! Nice to see you, ", "Hi, ", "Hey there, ", "Welcome, ",] )
    e "[hlrd][playername]!"
    $ randomgreet = renpy.random.randint(1, 2)
    if randomgreet == 1:
        jump greetime
    else:
        jump hellod

label greetime:
    $ hlgm = renpy.random.choice(["Good morning.", "Let's start the day off right!", "I'm a little tired this morning~", "Hopefully this day will be better then yesterday."] )
    $ hlga = renpy.random.choice(["Good afternoon.", "I was just sketching something before you came in.", "Great to see you.", "Thanks for stopping by.", "It was getting a little lonely in here~"] )
    $ hlgd = renpy.random.choice(["Good evening.", "It's almost bedtime, hm?", "Was today a good day so far?", "How are you feeling?", "Mm, i'm feeling a bit sleepy~", "Good evening~"] )

    show oc nb smile normal
    if hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        e "[hlgm]"
    elif hour in [12, 13, 14, 15, 16, 17]:
        e "[hlga]"
    elif hour in [18, 19, 20, 21, 22, 23, 24]:
        e "[hlgd]"
    else:
        e "What time is it again..?"
    
    jump worldidle

label hellod:
    $ hlex = renpy.random.choice(["Nice weather we're having, hm?", "How have you been doing?", "Hopefully your day hasn't been stressful.", "It's been a while since you've visited, no?", "How are you?",] )

    e "[hlex]"

    jump worldidle


label newgame:
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    show mainroom

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen smile.png" to the images
    # directory.
    show chair at center zorder 2
    show table at center zorder 5
    show oc nb frown closed at center zorder 4
    with fade
    # These display lines of dialogue.
    e "..."

    e "Huh? Where..."

    show oc nb frown bshocked
    e "Where am i!?"
    e "..."
    e "... You haven't kidnapped me or anything, right?"
    hide chair
    hide table
    hide oc nb frown closed
    
    show chair at furnright zorder 2
    show table at furnright zorder 5
    show oc nb frown bshocked at furnright zorder 4
    with ease
    menu:
        "I haven't.":
            call movegoback
            show oc nub frown lookleft
            e "I see... I don't know if I trust that."
            e "Now, where am I?"
            show chair at furnright
            show table at furnright
            show oc nub frown lookleft at ocright
            with ease

    menu:
        "I don't know.":
            call movegoback
            show oc ab smile closed
            e "Thats just {i}great.{/i}"
            show oc ab frown lookright
            e "And from the look of your face, theres no exit either."
            show oc ab frown closed
            e "..."
            e "It's... fine."
            show oc nub smile normal
            e "I might as well get to know you then, hm?"
            show oc hb smile lookleft
            e "From the looks of it, you already know me. Unsure {i}how{/i}, though."

    show oc nb smile normal
    e "Now, what's your name?"
    $ persistent.pname = renpy.input("What is your name?", "Amari", length=15, exclude=" 0123456789+=,.?!<>").strip() or "Player"
    show oc nb smile lookright
    e "Nice to meet you, [playername]. I'm Aislin, although that's all you'll get out of me~"
    show oc nb frown normal
    e "This is mostly for formality, but what pronouns do you prefer?"
    $ quick_menu = False
    call screen pick_multiple_pronouns()
    $ quick_menu = True
    show oc nb smile normal
    e "So your pronouns are [they]/[them]? Thanks."
    show oc nub frown lookleft
    e "Look. I still don't trust you, or whatever this place is."
    show oc nub frown closed
    e "...But it doesn't look like the situation will change anytime soon."
    show oc nb smile hapclosed
    e "So I suppose I will have to entertain for now~ Hopefully you're okay with that."
    
    $ persistent.isnew = False

    jump worldidle

screen menuButton:
    imagebutton idle "gui/menubutton.png" xalign 1 yalign 1 action ToggleScreen("menuButton"), Jump("ocmenu")

define topicpool = ["random1", "random2", "random3", "random4"]

label talkoc:
    $ _window_show()
    hide screen headpather
    show oc nb smile normal
    python:
        from plyer import notification

        notification.notify(
            title="Hi there!",
            message="I have something to talk about!",
            app_icon="",
            timeout="10"
        )
    $ renpy.jump((renpy.random.choice(topicpool)))

label idleoc:
    $ _window_hide()
    hide screen headpather
    show oc nb smile normal
    $ renpy.jump('idle'+str(renpy.random.randint(1,2)))

label idle1:
    show oc nb smile bshocked at ugo2
    $ renpy.pause(4)
    jump worldidle

label idle2:
    show oc hb frown bshocked
    $ renpy.pause(15)
    jump worldidle


label worldidle:
    $ affasign()
    $ _window_hide() 
    $ persistent.saidgoodbye = False
    show screen headpather
    show screen menuButton
    with dissolve
    show chair at left zorder 2
    show table at left zorder 5
    show oc nb smile normal at center zorder 4
    with ease
    pause 0.5
    $ checkgift()
    $ waittime = renpy.random.randint(10, 30)
    $ randomidle = renpy.random.randint(1, 2)
    $ renpy.pause(waittime, hard=True)
    if randomidle == 1:
        jump idleoc
    else:
        if persistent.randomchatter == True:
            hide screen menuButton
            hide screen headpather
            jump talkoc
        else:
            jump idleoc
    

label ocmenu:
    call moveocmenu
    menu:
        "Discuss...":
            jump discussoc
        "Goodbye...":
            menu:
                "I'm going to restart.":
                    call movegoback
                    show oc nb smile normal
                    e "See you soon, [playername]~"
                    $ persistent.saidgoodbye = True
                    $ renpy.pause(0.1, hard=True)
                    $ Quit(confirm=False)()
                "Goodbye.":
                    call movegoback
                    show oc nb smile normal
                    e "[gbrd]"
                    $ persistent.saidgoodbye = True
                    $ renpy.pause(0.1, hard=True)
                    $ Quit(confirm=False)()
                "Back":
                    jump ocmenu
        "Close":
            jump worldidle

label discussoc:
    menu:
        "Outfit":
            jump dis_outfitoc
        "Us":
            jump dis_usoc
        "Ember":
            call movegoback
            $ persistent.affection += 25
            show oc nb smile bshocked
            e "You know of her?"
            show oc nb smile normal
            e "She's one of my favorite detectives to toy with."
            show oc sb smile lookleft
            e "If only she knew... Ah, nevermind that."
            jump worldidle
        
        "You":
            call movegoback
            $ persistent.affection += 10
            show oc nb smile hapclosed
            e "Ah, me, hm?"
            show oc nb smile normal
            e "Well, as you know..."
            show oc nb smile closed
            e "I try to be as {i}charming{/i} as possible."
            show oc nb eh lookright
            e "..."
            show oc hb eh normal
            e "Is it working?"
            jump worldidle
            
        "Back":
            jump ocmenu

jump ocmenu

label dis_outfitoc:
    call movegoback
    e "Outfit, hm?"
    e "What are we feeling today?"
    jump outfitpicker

label outfitpicker:
    call moveocmenu
    menu:
        "Clothing":
            menu:
                "Uniform":
                    $ SetVariable("persistent.outfit", "uniform")()
                    
                    jump outfitpicker
                "Casual":
                    $ SetVariable("persistent.outfit", "casual")()
                    
                    jump outfitpicker
                "Back":
                    jump outfitpicker

        "Accessories":
            menu:
                "Add Top Hat":
                    $ SetVariable("persistent.hat", "tophat")()
                    
                    jump outfitpicker
                "Remove Top Hat":
                    $ SetVariable("persistent.hat", "none")()
                    
                    jump outfitpicker
                "Add Mask":
                    $ SetVariable("persistent.mask", "maskon")()
                    
                    jump outfitpicker
                "Remove Mask":
                    $ SetVariable("persistent.mask", "maskodd")()
                    
                    jump outfitpicker
                "Back":
                    jump outfitpicker
        
        "Outfit":
            menu:
                "Casual":
                    $ SetVariable("persistent.outfit", "casual")()
                    $ SetVariable("persistent.mask", "maskodd")()
                    $ SetVariable("persistent.hat", "none")()

                    jump outfitpicker
                "Uniform":
                    $ SetVariable("persistent.mask", "maskon")()
                    $ SetVariable("persistent.hat", "tophat")()
                    $ SetVariable("persistent.outfit", "uniform")()

                    jump outfitpicker

                "Back":
                    jump outfitpicker
        "Back":
                    jump worldidle

label dis_usoc:
    
    menu:
        "What do you think of me?":
            call movegoback
            if persistent.affnormal is True:
                show oc nub smile closed
                e "Hmm..."
                show oc nb frown lookright
                e "We don't know each other yet, so i'm unsure if..."
                show oc nb smile hapclosed
                e "Well, lets just say we have room to grow~"
            elif persistent.affaquant is True:
                show oc nb smile normal
                e "I'd say i'm starting to get to know you!"
                show oc nb smile closed
                e "And you me, for that matter."
            elif persistent.afflike is True:
                show oc nb smile hapclosed
                e "I'd say we're well acquainted now."
                show oc nb smile normal
                e "I do look forward to your visits, thats for sure~"
            elif persistent.afffriends is True:
                show oc nb smile hapclosed
                e "I consider you a friend~"
                show oc sb smile lookleft
                e "I wish I could see you more, but..."
                show oc nb smile hapclosed
                e "... You know what I mean."
                show oc nb smile normal
                e "I hope you feel the same, [persistent.pname]."
            elif persistent.affbfriends is True:
                show oc nb smile closed
                e "One of my dearest friends."
                show oc nb smile hapclosed
                e "One day, I would love to meet you face to face~"
            else:
                show oc nb smile normal
                e "I don't know, [persistent.pname]..."
            jump worldidle

        "[persistent.ocname], Can I change your nickname?":
            call movegoback
            if persistent.affnormal is True:
                show oc nub frown lookright
                e "I'm not sure i'd be comfortable with that yet. Sorry."
            elif persistent.affaquant is True:
                show oc nub frown lookright
                e "I'm not sure i'd be comfortable with that yet. Sorry."
            else:
                show oc nb smile normal
                e "I don't see why not."
                show oc nb smile hapclosed
                e "Just don't pick anything weird, alright?"
                $ persistent.ocname = renpy.input("Give them a nickname!", "Aislin", length=15, exclude=" 0123456789+=,.?!<>").strip() or "Aislin"
                show oc nb smile normal
                e "[persistent.ocname]? I think I could get used to that~"
            jump worldidle

        "Can I change my name?":
            call movegoback
            show oc nb smile normal
            e "Of course."
            show oc hb smile normal
            e "What do you want it to be?"
            $ persistent.pname = renpy.input("What is your name?", "Player", length=15, exclude=" 0123456789+=,.?!<>").strip() or "Player"
            show oc hb smile lookleft
            e "[persistent.pname], hm?"
            show oc nb smile hapclosed
            e "What a pretty name~"
            jump worldidle
        
        "Let's play!" if persistent.rpcunlocked is True:
            call movegoback
            show oc nb smile normal
            e "Sound's good to me!"
            call rps_select

        "Back":
            jump discussoc