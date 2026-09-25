################################################################################
##
## Easy Blinking for Ren'Py by Feniks (feniksdev.itch.io / feniksdev.com) v1.1
##
################################################################################
## This file contains code for a special DynamicDisplayable subclass called
## EasyBlink. It makes it simple to declare blinking images for characters.
## You can find detailed write-ups on the properties + examples on my website:
## https://feniksdev.com/docs-category/easy-blinking/
##
## If you'd like to see how to use this tool, check the other file,
## easy_blink_examples.rpy! This is just the backend; you don't need to
## understand everything in this file. However, you can look at the blink_config
## constants declared immediately below; these are the default values for the
## EasyBlink class. You can change these to suit how you typically set up your
## blinking sprites.
##
## If you use this code in your projects, credit me as Feniks @ feniksdev.com
##
## Leave a comment on the tool page on itch.io if you run into any issues.
################################################################################
init -250 python in blink_config:
    _constant = True
    ## DEFAULT KWARGS. You can also supply any of these arguments
    ## to EasyBlink to change them on an individual basis.
    ## Modify the values here to what you will use most often so you don't
    ## have to specify it each time.

    ## The length of time between each blink frame.
    ## You can do 1.0/60.0 if you want this to be 60fps, for example.
    ## This can also be a list of times, which should be the same
    ## length as the number of frames your blink animation has.
    ## e.g. blink_framerate = 0.04
    ## e.g. blink_framerate = [0.04, 0.02, 0.02, 0.04]
    blink_framerate = 0.04
    ## How many seconds to wait before blinking again, in the format:
    ## (min time, max time)
    blink_repeat = (1.8, 4.5)
    ## How often the character should blink twice in quick succession.
    ## 0.1 is 10%. If this is 0.0 then the character will never blink twice
    ## in a row.
    double_blink_pct = 0.1
    ## If True, the sequence of eye images is expected to be numbered.
    ## e.g. "happy_eyes0.webp", "happy_eyes1.webp", "happy_eyes2.webp" etc.
    ## It will keep looking for images until it can't find any more.
    ## Note that the path should have a {num} substitution in it if using
    ## this.
    numbered = False
    ## If True, and numbered=True, then the first image in a numbered
    ## sequence will *not* have any number in it i.e. it will go:
    ## "happy_eyes.webp", "happy_eyes1.webp", "happy_eyes2.webp" etc.
    start_no_num = False
    ## The naming convention of additional eye images. Used only if
    ## numbered=False. So, if this was ["half_closed", "closed"] then a
    ## path of "eileen/{img}_eyes.webp" and an img of "happy" would look for:
    ##      "eileen/happy_eyes.webp", "eileen/half_closed_eyes.webp",
    ##      "eileen/closed_eyes.webp"
    ## If the path doesn't have an {img} substitution, then these should be
    ## direct image paths like ["eileen/half_closed_eyes.webp",
    ##      "eileen/closed_eyes.webp"]
    mid_eye_frames = ["closed"]
    ## If not empty, this is a list of yzoom numbers to use for automatically
    ## generated blink frames. This works by squishing the open eye frame.
    ## For this to work, the image should have all transparency below the eyes
    ## trimmed away, so that the bottom of the eye illustration is at the bottom
    ## of the image. This image will be squished down starting from the top, so
    ## the bottom always stays in the same place. It does not look good for all
    ## eye images. Looks best if the character is facing the viewer or close
    ## to it. e.g. automatic_blink_frames = [0.9, 0.8]
    automatic_blink_frames = []
    ## If True, the animation will play in reverse after it's done e.g.
    ## going from happy_eyes0 -> happy_eyes1 -> happy_eyes2 -> happy_eyes1
    ## -> happy_eyes0
    ## Otherwise it would go happy_eyes0 -> happy_eyes1 -> happy_eyes2 ->
    ## happy_eyes0
    reverse = False
    ## This is the frame the animation should begin on when looping. For most
    ## cases this will be 0, but if you have 3 frames of "startup" before it
    ## starts looping, then you would set this to 3. Note that if reverse=True,
    ## the non-looping frames won't be reversed (so if frames 0, 1, 2 were
    ## "startup", and frames 3, 4, 5 were the loop, then it would go 0, 1, 2,
    ## 3, 4, 5, 4, 3, 4, 5, 4, 3 etc).
    loop_start_frame = 0
    ## This is the transition that should be used when switching between blink
    ## frames, or None if no transition should be used. It can either be a
    ## single transition, like `transition=Dissolve(0.2)`, or a list of
    ## transitions (same as blink_framerate).
    transitions = None
    ## A configuration value which determines whether the game should block
    ## eye blinking while a transition is occurring. If True, eyes will be
    ## shown in their open state only until the transition is completed.
    block_during_transition = True

## This is a persistent variable which determines whether blinking is on or off.
## You can adjust it as part of an animation or accessibility toggle.
default persistent.blinking_on = True

################################################################################
## Below here is the class declaration; none of the code below this point needs
## to be modified or understood unless you want to change how it works. Use
## the blink_config constants above to change the behavior instead!
init -200 python:

    from random import uniform

    class EasyBlink(DynamicDisplayable):
        """
        A dynamic displayable which blinks.

        Attributes:
        -----------
        blink_st : float
            When the image should blink again.
        blink_num : int
            Which frame the blink is currently on.
        double_blink : bool
            Whether the image recently blinked twice in a row.
        blink_framerate : float or list of floats
            The length of time between each blink frame. If a list, it should
            be the same length as the number of frames your blink animation has.
        blink_repeat : tuple of floats
            How many seconds to wait before blinking again, in the format:
            (min time, max time)
        double_blink_pct : float
            How often the character should blink twice in quick succession.
            0.1 is 10%. If this is 0.0 then the character will never blink
            twice in a row.
        last_transition : Transition
            The last transition that was used. Saved so blinks don't happen
            while a transition is ongoing.
        transition_timing : float
            The time when the last transition will be done transitioning.
        blink_images : string[]
            List of the images making up the blink animation.
        open_eyes : string
            The image with the eyes open.
        should_blink : bool
            Whether the character should blink at all. If we only have one
            blink image, there is no blinking.
        """
        def __init__(self, path, img="", *args, **kwargs):
            """
            Create a EasyBlink displayable.

            Arguments:
            ----------
            path : string
                The path where the eye images are found, so the image path can
                be put together with path + image names. It should include the
                substitution {img} which will be replaced with the image name.
                e.g. "characters/eileen/{img}.webp"
                If numbered=True, it should also include a {num} substitution
                which will be replaced with the number of the image.
                e.g. "characters/eileen/{img}{num}.webp"
                If it doesn't include the {img} substitution, it must be a
                direct image path on its own.
            img : string
                The name of the first frame of the animation/the open eye image.
                e.g. "happy_eyes"
            sequence : list
                A list of (image, time) or (image, time, transition) tuples
                which will be used to create the blink animation.
            All other kwargs are as declared in blink_config above.
            """
            ## Basics
            self.blink_st = None
            self.blink_num = -1
            self.double_blink = False
            self.last_transition = None
            self.transition_timing = None
            self.blink_images = [ ]

            ## Properties
            self.blink_framerate = kwargs.pop('blink_framerate',
                                                blink_config.blink_framerate)
            self.blink_repeat = kwargs.pop('blink_repeat',
                                        blink_config.blink_repeat)
            self.double_blink_pct = kwargs.pop('double_blink_pct',
                                            blink_config.double_blink_pct)
            self.block_during_transition = kwargs.pop('block_during_transition',
                                        blink_config.block_during_transition)
            self.loop_start_frame = kwargs.pop('loop_start_frame',
                                        blink_config.loop_start_frame)

            ## Image setup
            mid_eye_frames = kwargs.pop('mid_eye_frames',
                                        blink_config.mid_eye_frames)
            start_no_num = kwargs.pop('start_no_num', blink_config.start_no_num)
            automatic_blink_frames = kwargs.pop('automatic_blink_frames',
                                            blink_config.automatic_blink_frames)
            numbered = kwargs.pop('numbered', blink_config.numbered)
            reverse = kwargs.pop('reverse', blink_config.reverse)
            transitions = kwargs.pop('transitions', blink_config.transitions)
            sequence = kwargs.pop('sequence', None)

            if sequence:
                new_transitions = [ ]
                new_framerate = [ ]
                img = ""
                if not isinstance(transitions, list):
                    transitions = [transitions]*len(sequence)
                if not isinstance(self.blink_framerate, list):
                    self.blink_framerate = [self.blink_framerate]*len(sequence)
                if mid_eye_frames:
                    mid_eye_frames = [ ]
                ## Split it up into its parts
                for i, tup in enumerate(sequence):
                    if len(tup) == 3:
                        frame, t, tr = tup
                    elif len(tup) == 2:
                        frame, t = tup
                        try:
                            tr = transitions[i]
                        except:
                            tr = None
                    else:
                        frame = tup
                        try:
                            t = self.blink_framerate[i]
                        except:
                            t = self.blink_framerate[-1]
                        try:
                            tr = transitions[i]
                        except:
                            tr = None

                    if i == 0 and not img:
                        img = frame
                    else:
                        mid_eye_frames.append(frame)

                    new_transitions.append(tr)
                    new_framerate.append(t)

                if reverse:
                    ## The last transition will already be duplicated below
                    new_transitions.pop(-1)

                transitions = new_transitions
                self.blink_framerate = new_framerate

            if numbered:
                if "{num}" not in path:
                    raise ValueError("Numbered images require a {num} substitution in the path.")
                # The frame with their eyes open
                if start_no_num:
                    self.open_eyes = path.format(img=img, num="")
                else:
                    self.open_eyes = path.format(img=img, num=0)
                self.blink_images.append(self.open_eyes)
                ## Loop through as many images as are available
                i = 0
                while True:
                    i += 1
                    new_img = path.format(img=img, num=i)
                    if (renpy.loadable(new_img)
                            or renpy.loadable("images/" + new_img)
                            or renpy.get_registered_image(new_img)):
                        self.blink_images.append(new_img)
                    else:
                        break
            elif not isinstance(path, str) and path is not None:
                ## It's not a string, so we don't perform any substitutions.
                self.open_eyes = path
                self.blink_images.append(self.open_eyes)
                ## If we're using automatic blink frames, generate them now.
                if automatic_blink_frames:
                    ## Generate the yzoom level
                    for yz in automatic_blink_frames:
                        ## Use a fixed so the bottom can be aligned to the
                        ## same spot.
                        new_img = Fixed(
                            Transform(self.open_eyes, alpha=0.0),
                            Transform(self.open_eyes, yzoom=yz, yalign=1.0),
                        fit_first=True)
                        self.blink_images.append(new_img)
                ## Add the mid-eye frames
                for eye in mid_eye_frames:
                    self.blink_images.append(eye)
            else:
                # The frame with their eyes open
                if path is None and img:
                    self.open_eyes = img
                elif path is None:
                    self.open_eyes = mid_eye_frames[0]
                else:
                    self.open_eyes = path.format(img=img, num="")
                self.blink_images.append(self.open_eyes)
                ## If we're using automatic blink frames, generate them now.
                if automatic_blink_frames:
                    ## Generate the yzoom level
                    self.make_auto_blink(automatic_blink_frames,
                        self.blink_images[-1], img, path)
                ## Add the mid-eye frames
                for eye in mid_eye_frames:
                    if path and "{img}" in path and isinstance(eye, str):
                        self.blink_images.append(path.format(img=eye, num=""))
                    elif isinstance(eye, list):
                        ## A list of auto-blink frames
                        self.make_auto_blink(eye, self.blink_images[-1],
                            self.blink_images[-1], None)
                    else:
                        self.blink_images.append(eye)

            ## Add back the images in reverse order
            if reverse and len(self.blink_images) > 1:
                self.blink_images += self.blink_images[-2:self.loop_start_frame:-1]

            self.open_eyes = self.blink_images[self.loop_start_frame]

            ## Make sure the framerate is a list of the same length as the
            ## number of blink images.
            if not isinstance(self.blink_framerate, list):
                self.blink_framerate = [self.blink_framerate] * len(self.blink_images)
            else:
                if (len(self.blink_framerate) != len(self.blink_images)
                        and reverse):
                    ## Add it back in reverse
                    self.blink_framerate += self.blink_framerate[-2:self.loop_start_frame:-1]
                if len(self.blink_framerate) != len(self.blink_images):
                    raise ValueError("The length of blink_framerate must be the same as the number of blink images.")

            ## Add a bunch of dissolves between the images, if available.
            if transitions:
                new_blinks = [ ]
                new_framerates = [ ]
                new_loop_start = self.loop_start_frame
                if not isinstance(transitions, list):
                    transitions = [transitions]*len(self.blink_images)
                elif len(transitions) != len(self.blink_images) and reverse:
                    ## Add it back in reverse
                    start = None if self.loop_start_frame == 0 else self.loop_start_frame-1
                    transitions += transitions[-1:start:-1]

                if len(transitions) != len(self.blink_images):
                    raise ValueError("The length of transitions must be the same as the number of blink images.")

                for i, tr in enumerate(transitions):
                    if i == len(self.blink_images)-1:
                        j = self.loop_start_frame
                    else:
                        j = i+1

                    if i == self.loop_start_frame:
                        new_loop_start = len(new_blinks)

                    if tr != None:
                        tr = tr(old_widget=renpy.displayable(self.blink_images[i]),
                            new_widget=renpy.displayable(self.blink_images[j]))
                        tr._unique()
                        delay = tr.delay
                        new_blinks.append(self.blink_images[i])
                        new_blinks.append(tr)
                        new_framerates.append(self.blink_framerate[i])
                        new_framerates.append(delay)
                    else:
                        new_blinks.append(self.blink_images[i])
                        new_framerates.append(self.blink_framerate[i])

                self.loop_start_frame = new_loop_start
                self.blink_images = new_blinks
                self.blink_framerate = new_framerates

            self.finish_init(*args, **kwargs)

        def finish_init(self, *args, **kwargs):
            ## If there's only one blink image, there isn't any blinking.
            ## This simplifies a check later on.
            self.should_blink = len(self.blink_images) > 1

            kwargs.update( {
                '_predict_function' : self.predict_images } )

            super(EasyBlink, self).__init__(self.get_blink_image,
                                                *args, **kwargs )

        def make_auto_blink(self, auto_blink_frames, open_eye, img, path):
            for yz in auto_blink_frames:
                ## Use a fixed so the bottom can be aligned to the
                ## same spot.
                if isinstance(img, str) and isinstance(path, str):
                    new_img = Fixed(
                        Transform(open_eye, alpha=0.0),
                        Transform(path.format(img=img, num=""), yzoom=yz, yalign=1.0),
                    fit_first=True)
                else:
                    new_img = Fixed(
                        Transform(open_eye, alpha=0.0),
                        Transform(img, yzoom=yz, yalign=1.0),
                    fit_first=True)
                self.blink_images.append(new_img)

        def reset_eyes(self, reset=0.1):
            """
            Reset the eyes to the open position.
            """
            if self.blink_num is None:
                pass
            elif self.blink_num > 0:
                self.blink_num = None
            else:
                self.blink_num = -1
            self.blink_st = None
            if self.blink_num == -1:
                return self.blink_images[0], reset
            return self.open_eyes, reset

        def per_interact(self):
            """
            Refresh the saved transitions on a new interaction.
            """
            super(EasyBlink, self).per_interact()
            self.kwargs['can_reset_transition'] = True

        def render(self, w, h, st, at):
            self.update(st, at)
            if isinstance(self.child, renpy.display.transition.Transition):
                ## If it's a transition, we need to keep updating until it's
                ## done. Also the timebase has an offset.
                nst = st-self.kwargs.get('blink_offset', 0)
                cr = self.child.render(w, h, nst, nst)
                renpy.redraw(self, 0)
            else:
                cr = renpy.render(self.child, w, h, st, at)
            rv = renpy.Render(cr.width, cr.height)
            rv.blit(cr, (0, 0))
            return rv

        def get_blink_image(self, st, at, *args, **kwargs):
            """
            The DynamicDisplayable callback method. Returns the correct
            blink image and a time when the callback should be called again.

            Notable Kwargs:
            --------------
            can_reset_transition : bool
                Whether a new interaction means a new transition may have
                begun.
            blink_offset : float
                The time when the last transition began. Used to offset the
                timebase to play the transition out.
            """
            if not self.should_blink or not persistent.blinking_on:
                ## No blinking to be done
                return self.open_eyes, None

            if not st:
                ## Start the cycle over
                ret = self.reset_eyes()
                self.blink_num = -1
                if st is None:
                    return ret

            ## Use ongoing_transition to determine when transitions are
            ## happening.
            if self.block_during_transition:
                can_reset_transition = kwargs.get('can_reset_transition', True)
                try:
                    ongoing_transition = renpy.game.interface.ongoing_transition
                    if ongoing_transition.get(None):
                        return self.reset_eyes()
                    elif (ongoing_transition and self.transition_timing
                            and st <= self.transition_timing
                            and not can_reset_transition):
                        return self.reset_eyes()
                    elif ongoing_transition:
                        ## Dict transitions don't end like normal ones do.
                        longest_duration = 0
                        final_trans = None
                        for layer, trans in ongoing_transition.items():
                            if trans().delay > longest_duration:
                                longest_duration = trans().delay
                                final_trans = trans

                        if (final_trans is not None
                                and final_trans is self.last_transition):
                            if can_reset_transition:
                                ## We can reset the transition now.
                                self.kwargs['can_reset_transition'] = False
                                self.last_transition = None
                                self.transition_timing = 0
                            ## We've already perused this list of transitions
                            ## and the longest one is the same; is the timing
                            ## done?
                            elif st <= self.transition_timing:
                                ## No; keep waiting. Otherwise, pass through
                                ## and animate.
                                return self.reset_eyes()
                        if (final_trans is not None
                                and final_trans is not self.last_transition):
                            ## This means we haven't recorded this transition.
                            self.last_transition = final_trans
                            self.transition_timing = st + longest_duration
                            return self.reset_eyes(longest_duration)
                except Exception as e:
                    ## Usually this means the ongoing transitions dictionary
                    ## isn't set up yet during init time.
                    pass

            if self.blink_st is not None and st >= self.blink_st:
                ## We've refreshed and it's time to advance the blink.
                if self.blink_num is None:
                    self.blink_num = self.loop_start_frame-1
                self.blink_num += 1

                if self.blink_num >= len(self.blink_images):
                    ## Start the loop over again
                    self.blink_num = None
                    self.blink_st = None
                else:
                    # In the process of blinking
                    self.kwargs['blink_offset'] = st
                    self.blink_st = st + self.blink_framerate[self.blink_num]-0.01
                    return self.blink_images[self.blink_num], self.blink_framerate[self.blink_num]

            elif (self.blink_st is not None and self.blink_num is not None
                    and self.blink_num >= 0):
                ## Blinking, but refreshed too soon. Keep showing the
                ## current blink frame.
                return self.blink_images[self.blink_num], self.blink_framerate[self.blink_num]

            refresh_time = 0.1
            if (self.blink_st is None and self.blink_num is not None
                    and self.blink_num < self.loop_start_frame-1):
                ## The eyes are open, but we're not in the loop yet. Start
                ## playing the animation as soon as possible.
                self.blink_st = st
                return self.open_eyes, 0.0
            if not self.blink_st or self.blink_st > st + self.blink_repeat[1]:
                ## Blink twice, on occasion - but don't triple-blink.
                if (self.double_blink_pct > 0.0 and not self.double_blink
                        and uniform(0.0, 1.0) <= self.double_blink_pct):
                    self.blink_st = st
                    self.double_blink = True
                    refresh_time = 0.0
                else:
                    self.double_blink = False
                    refresh_time = uniform(self.blink_repeat[0],
                                            self.blink_repeat[1])
                    self.blink_st = st + refresh_time

            return self.open_eyes, refresh_time

        def predict_images(self):
            return self.blink_images
