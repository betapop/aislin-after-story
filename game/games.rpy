#########################
## Rock Paper Scissors ##
##         ###         ##
##  A Ren'Py minigame - https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=50068#p486361  ##
#########################

default result = "none"
default selection = "none"
default score = 0
default computer = 0
default ties = 0

default persistent.cheating = 0
default persistent.scissors_only = 0
default persistent.paper_only = 0
default persistent.rock_only = 0
default persistent.unlose = 0

label rps_select:
    
    show screen stats
    
    if not persistent.cheating:
        menu:
            
            "Rock":
                $selection = "rock"
                $result = renpy.random.choice(['rock', 'paper', 'scissors'])
                jump results
            "Paper":
                $selection = "paper"
                $result = renpy.random.choice(['rock', 'paper', 'scissors'])
                jump results
            "Scissors":
                $selection = "scissors"
                $result = renpy.random.choice(['rock', 'paper', 'scissors'])
                jump results
            "End":
                hide screen stats
                jump rpfback
        
    else:
        menu:
            
            "Rock":
                $selection = "rock"
                $result = "scissors"
                jump results
            "Paper":
                $selection = "paper"
                $result = "rock"
                jump results
            "Scissors":
                $selection = "scissors"
                $result = "paper"
                jump results
            "End":
                hide screen stats
                jump rpfback
                
    if not persistent.unlose:
        
        if persistent.rock_only:
            $ result = "rock"
            jump results
        if persistent.paper_only:
            $ result = "paper"
            jump results
        if persistent.scissors_only:
            $ result = "scissors"
            jump results
    
label results:

####rock####

    if result == "rock":
        if selection == "rock":
            jump tie
        elif selection == "paper":
            jump win
        elif selection == "scissors":
            jump lose

####paper####

    elif result == "paper":
        if selection == "rock":
            jump lose
        elif selection == "paper":
            jump tie
        elif selection == "scissors":
            jump win

####scissors####

    elif result == "scissors":
        if selection == "rock":
            jump win
        elif selection == "paper":
            jump lose
        elif selection == "scissors":
            jump tie

label tie:
    
    e "We tied with [result]!"
    $ ties += 1
    jump rps_select
    
label win:
    
    e "[selection] beats [result], you win!"
    $ score += 1
    jump rps_select
    
label lose:
    
    e "[result] beats [selection], you lost!"
    $ computer += 1
    jump rps_select


screen stats():
    
    modal False
    zorder 100
    vbox:
        xalign 0.5
        ypos 0.01
        text "{color=#000}Computer: [computer] You: [score] Ties: [ties]{/color}"


screen cheats():
    default unlock_cheats = False

    tag menu

    use game_menu(_("Cheats"), scroll="viewport"):

        style_prefix "cheats"
        

        vbox:
            textbutton _("Enable cheats") action ToggleScreenVariable("unlock_cheats")
            if unlock_cheats:
                input:
                    value VariableInputValue('nolose', returnable=False)
        
        if nolose == "renpy":
            
            vbox:
                label _("Never Lose")
                hbox:
                    textbutton _("On") action SetField(persistent, "unlose", 1)
                    textbutton _("Off") action SetField(persistent, "unlose", 0)
            
            vbox:
                label _("Rock on!")
                hbox:
                    textbutton _("On") action SetField(persistent, "rock_only", 1)
                    textbutton _("Off") action SetField(persistent, "rock_only", 0)
            
            vbox:
                label _("Papercut!")
                hbox:
                    textbutton _("On") action SetField(persistent, "paper_only", 1)
                    textbutton _("Off") action SetField(persistent, "paper_only", 0)
                        
            vbox:
                label _("Blades!")
                hbox:
                    textbutton _("On") action SetField(persistent, "scissors_only", 1)
                    textbutton _("Off") action SetField(persistent, "scissors_only", 0)


style cheats_label is gui_label
style cheats_label_text is gui_label_text
style cheats_text is gui_text

style cheats_label_text:
    size gui.label_text_size

default nolose = ""

label rpfback:
    e "No? Fine with me~"
    jump worldidle