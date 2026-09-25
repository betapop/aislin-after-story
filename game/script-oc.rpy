default persistent.fhair = "normal_b"
default persistent.bhair = "normal_f"
default persistent.outfit = "uniform"
default persistent.mask = "maskon"
default persistent.hat = "tophat"

layeredimage oc:

    always:
        "oc/hair/normal/normal_b.png"
    
    always:
        "oc/body/body.png"
    
    always:
        "oc/hair/normal/normal_f.png"
    
    if persistent.mask == "maskon":
        "oc/clothing/uniform/mask.png"
    elif persistent.mask == "maskoff":
        "oc/clothing/empty.png"


    group mouth:
        attribute smile default:
            WhileSpeaking("e", "oc_talksmile", "oc/face/mouth/smile.png")
        
        attribute eh:
            "oc/face/mouth/eh.png"

        attribute happy:
            "oc/face/mouth/happy.png"

        attribute wow:
            "oc/face/mouth/wow.png"
        
        attribute frown:
            WhileSpeaking("e", "oc_talkfrown", "oc/face/mouth/frown.png")
        
        attribute oh:
            "oc/face/mouth/oh.png"

    # group mouth:
    #     attribute smile default:
    #         "oc/face/mouth/smile.png"
        
    #     attribute eh:
    #         "oc/face/mouth/eh.png"

    #     attribute happy:
    #         "oc/face/mouth/happy.png"

    #     attribute wow:
    #         "oc/face/mouth/wow.png"
        
    #     attribute frown:
    #         "oc/face/mouth/frown.png"
        
    #     attribute oh:
    #         "oc/face/mouth/oh.png"

    group eyebrows:
        attribute nb default:
            "oc/face/eyebrows/happybrow.png"
        
        attribute hb:
            "oc/face/eyebrows/huhbrow.png"
        
        attribute sb:
            "oc/face/eyebrows/sadbrow.png"
        
        attribute ab:
            "oc/face/eyebrows/angrybrow.png"
        
        attribute nub:
            "oc/face/eyebrows/nullbrow.png"

    group eyes:
        attribute normal default EasyBlink(
            path="eyes_{img}", img="normal",
            ## This will go normal->semi->closed->semi->normal
            ## The mid-eye frames are also substituted in for {img} in the path.
            ## So this finds "eyes_semi" and "eyes_closed"
            ## along with the open eye image, "eyes_normal"
            reverse=True, mid_eye_frames=["closed"],
        )
        attribute bsad EasyBlink(
            path="eyes_{img}{num}", img="sad",
            ## These images use a numbering scheme, from 0-2
            ## eyes_cry0, eyes_cry1, eyes_cry2
            mid_eye_frames=["closed"],
        )
        attribute bshocked EasyBlink(
            path="eyes_{img}", img="shocked",
            ## This attribute lacks the "semi" frame, so it goes from open
            ## to closed with no other in-between frames.
            mid_eye_frames=["closed"],
        )

        attribute bplayful EasyBlink(
            path="eyes_{img}", img="playful",
            ## This attribute lacks the "semi" frame, so it goes from open
            ## to closed with no other in-between frames.
            mid_eye_frames=["closed"],
        )

        attribute lookleft EasyBlink(
            path="eyes_{img}", img="lookleft",
            mid_eye_frames=["closed"],
        )

        attribute lookright EasyBlink(
            path="eyes_{img}", img="lookright",
            mid_eye_frames=["closed"],
        )

        attribute idle1 EasyBlink(
            path="eyes_{img}", reverse=True,

            sequence=[("normal", 0.25, Dissolve(0.1)),
                ("shocked", 0.5, Dissolve(0.3)), ("lookleft", 0.2),
                ("normal", 0.04), ("closed", 0.04)],
                ## You might have noticed "side_eyes" in here twice - this is
                ## so the looped blinking doesn't have a long pause on the first
                ## frame, but we also want to linger on side_eyes for a moment
                ## after the surprised eyes.
                ## There's also a tuple that starts with [0.85] - this is
                ## interpreted as an automatic_blink_frames argument. It will
                ## use the eye image immediately before it (the side_eyes) at
                ## 85% of its usual height.

            ## Lastly, this says that the actual blink looping starts at frame
            ## 3, aka on ("side_eyes", 0.04) - remember that indices start at 0.
            loop_start_frame=3,
        )

        ## This is just a regular, non-blinking attribute
        attribute closed "eyes_closed"

        attribute hapclosed "eyes_happy"


    if persistent.outfit == "uniform":
        "oc/clothing/uniform/uniform.png"
    elif persistent.outfit == "casual":
        "oc/clothing/casual/casual.png"

    if persistent.hat == "tophat":
        "oc/clothing/uniform/tophat.png"
    elif persistent.hat == "none":
        "oc/clothing/empty.png"


image oc_talksmile:
    "oc/face/mouth/happy.png"
    0.2
    "oc/face/mouth/smile.png"
    0.2
    repeat

image oc_talkfrown:
    "oc/face/mouth/oh.png"
    0.2
    "oc/face/mouth/frown.png"
    0.2
    repeat


transform zoo: 
        ease .5 zoom 1.1 yalign 0.1

transform bac: 
        ease .5 zoom 1.0 yalign 1.0 yoffset 0

transform ugo2: 
        yoffset 0 
        linear 0.2 yoffset 10 
        linear 0.2 yoffset 0

transform shake2(rate= 0.090 ): 
        linear rate xoffset 2 yoffset 0 
        linear rate xoffset - 2.8 yoffset 2 
        linear rate xoffset 2.8 yoffset 0 
        linear rate xoffset - 2 yoffset 2 
        linear rate xoffset + 0 yoffset + 0 
        repeat

image oc resized = LayeredImageProxy("oc", Transform(zoom=0.95))

