init python:
    def checkgift():
        try:
            #Try reading the file to see if it exists (file is given as a path relative to the "game" directory):
            renpy.file("gifts/pudding.gift")
        except:
            try:
                renpy.file("gifts/emberplush.gift")
            except:
                try:
                    renpy.file("gifts/pencil.gift")
                except:
                    pass
                else:
                    os.remove(config.gamedir + '/gifts/pencil.gift')
                    renpy.jump("pencilgift")
                
            else:
                os.remove(config.gamedir + '/gifts/emberplush.gift')
                renpy.jump("emplushgift")

        else:
            #The the file exists, act on it here:
            os.remove(config.gamedir + '/gifts/pudding.gift')
            renpy.jump("puddinggift")
        

label puddinggift:
    hide screen menuButton
    hide screen headpather
    show oc nb smile normal
    e "wowie i love pudding"
    jump worldidle

label pencilgift:
    hide screen menuButton
    hide screen headpather
    show oc nb smile normal
    e "ty for the pencil"
    jump worldidle

label emplushgift:
    hide screen menuButton
    hide screen headpather
    show oc nb smile normal
    e "plush of pookie"
    jump worldidle