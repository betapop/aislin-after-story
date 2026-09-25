
# affection
default persistent.affection = 0
define persistent.affplatonic = False


# levels - hate
define persistent.affhate = False
define persistent.affdislike = False
define persistent.affrocky = False

# levels - normal
define persistent.affnormal = False
define persistent.affaquant = False
define persistent.afflike = False
define persistent.afffriends = False
define persistent.affbfriends = False

# levels - alt love
define persistent.affsupercl = False
define persistent.affcompanion = False
define persistent.affconnected = False
define persistent.affpair = False
define persistent.affsoulmate = False

init python:
    def affasign():
        if persistent.affection in range(0, 99):
            persistent.affnormal = True

        elif persistent.affection in range(100, 249):
            persistent.affaquant = True
            persistent.affnormal = False

        elif persistent.affection in range(250, 349):
            persistent.afflike = True
            persistent.affaquant = False

        elif persistent.affection in range(350, 499):
            persistent.afffriends = True
            persistent.afflike = False

        elif persistent.affection in range(500, 999):
            persistent.affbfriends = True
            persistent.afffriends = False
        else:
            pass

