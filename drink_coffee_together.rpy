# Register the submod
init -990 python in mas_submod_utils:
    Submod(
        author="geneTechnician",
        name="Drink coffee with Monika",
        description="A submod that let's you ask Monika if she will drink some coffee with you!",
        version="1.1.2",
        dependencies={},
        settings_pane=None,
        version_updates={
            "geneTechnician_drink_coffee_with_monika_1_1_1": "geneTechnician_drink_coffee_with_monika_1_1_2"
        }
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Drink coffee with Monika",
            user_name="geneTechnician",
            repository_name="drink-coffee-with-monika",
            submod_dir="/Submods/GT's interact with Monika pack",
            extraction_depth=3
        )

init python:

    gt_acs_playermug = MASAccessory(
        "player_mug",
        "player_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(gt_acs_playermug)

default -5 persistent._player_likes_coffee = True
default -5 persistent._coffee_pref = None
default -5 persistent._drink_pref_hot = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_drink_coffee",
            category=["us"],
            prompt="Would you like to drink some coffee with me?",
            conditional="mas_consumable_coffee.enabled()",
            pool=True,
            aff_range=(mas_aff.HAPPY, None),
            rules={"no_unlock": None},
            action=EV_ACT_UNLOCK
        ),
    )

label monika_drink_coffee:

    if not mas_globals.time_of_day_4state == "night":
        if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
            $ persistent._has_coffee = True
            $ persistent._has_prepared = True
            m 1hua "I would love to."
            if monika_chr.is_wearing_acs(mas_acs_mug):
                m 3eub "I already have some prepared, so you can go ahead and make yourself some coffee too if you haven't already."
            else:
                m 3eub "I have some brewing right now, so you can go ahead and make yourself some coffee too if you haven't already."
            if persistent.seen_playermug:
                m 3eua "I'll go get your cup out for you.{w=0.5}{nw}"
                jump drink_with_monika
            else:
                pass

        elif MASConsumable._getCurrentDrink() == mas_consumable_hotchocolate:
            if monika_chr.is_wearing_acs(mas_acs_hotchoc_mug):
                m 1eud "I would say yes, but I'm already drinking this cup of hot chocolate."
            else:
                m 1eud "I would say yes, but I already started heating up some hot chocolate."
            m 3eub "If you want, you can make yourself some hot chocolate too and we can drink that together instead."
            m 1hua "Don't worry, [player], I'll have a cup of coffee with you some other time~"

        else:
            if persistent.amount_of_coffees > 0:
                if datetime.datetime.now() > persistent.amount_of_coffees_time + datetime.timedelta(hours=9):
                    jump drink_coffee_refresh
                    
                else:
                    if persistent.amount_of_coffees >= 5:
                        m 2eksdla "I think we've had enough coffee for today, [mas_get_player_nickname()]."
                        m 7mksdla "Don't get me wrong,{w=0.5} I like coffee a lot,{w=0.5} but too much of it can do more harm than good."
                        m 4hkb "I guess it's true what they say:{w=0.3} there {i}can{/i} always be too much of a good thing, Ahaha!"
                        m 1eka "Don't worry, [player], I'd love to have some coffee with you tomorrow~"

                    else:
                        $ persistent._has_prepared = True
                        $ persistent._has_coffee = False

                        m 1etu "You want to have {i}another{/i} cup of coffee with me?"
                        if mas_globals.time_of_day_4state == "evening":
                            m 7lud "Alright, but keep in mind it's pretty late, so I don't think we should have any more after this."
                            m 7eua "I'll go prepare another pot right now.{w=1}{nw}"
                            $ persistent.amount_of_coffees = 5
                        else:
                            if persistent.amount_of_coffees == 4:
                                m 4mub "Wow,{w=0.5} you might like coffee even more than I do..."
                            m 7hub "Alright, alright, I'll go prepare another pot right now. Ahaha!{w=1}{nw}"

                        jump drink_with_monika

            else:
                jump drink_coffee_refresh

    else:
        if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
            if monika_chr.is_wearing_acs(mas_acs_mug):
                m 1gssdlb "I would say yes, but I'm trying to finish drinking this cup before it gets too late."
            else:
                m 1gssdlb "I would say yes, but I need to finish drinking the coffee that's currently brewing before it gets too late."
            m 1eka "Don't worry, [player], I'd love to have some coffee with you tomorrow~"

        else:
            m 1rksdla "I would say yes, but...{w=0.5}{nw}"
            extend 3ekd " it's pretty late, [player]."
            m 4eud "Drinking coffee before bed disrupts your ability to sleep, and poor sleeping habits can lead to some pretty significant health issues."
            m 7eub "How about you have some tea instead?"
            m 3eua "A cup of tea before bed can be incredibly relaxing,{w=0.3} and can even ease stress and anxiety."
            m 1eksdla "Unfortunately, I don't have anything I can use to prepare tea in here, so you'll have to drink some without me."
return

label drink_coffee_refresh:

    m 1sub "Of course!"
    if mas_globals.time_of_day_4state == "evening":
        m 7lud "Keep in mind it's pretty late though, so I don't think we should have any more after this."
        $ persistent.amount_of_coffees = 4
    else:
        m 3eub "I'll never pass up an opportunity to drink some coffee."
        m 1hublu "Especially if I get to drink it with you, [mas_get_player_nickname()]~"
        $ persistent.amount_of_coffees = 0
    m 7eua "Do you have some prepared already?"

    $ _history_list.pop()
    menu: 
        m "Do you have some prepared already?{fast}"

        "Yes.":
            $ persistent._has_prepared = True
            $ persistent._has_coffee = False
            m 1wuo "I should probably go make some for myself before yours gets cold, then!"
            m 2eub "I'll be back in a moment.{w=1}{nw}"

        "No.":
            $ persistent._has_prepared = False
            $ persistent._has_coffee = False
            m 1eub "Let's both take this opportunity to make some coffee for ourselves, then."
            m 3eua "I'll be back in a couple minutes, so you should go ahead and make yours at the same time."
            if mas_getSessionLength() >= datetime.timedelta(hours=2):
                m 4eub "It will also give you an opportunity to stretch your legs a little."
            m 2euu "Try not to miss me too much, okay?{w=1}{nw}"
            
    jump drink_with_monika
return

label drink_with_monika:

    call mas_transition_to_emptydesk
    if persistent._has_prepared == True:
        pause 5.0
    else:
        pause 120.0
    call mas_transition_from_emptydesk
    if persistent._has_coffee == False:
        $ mas_consumable_coffee.prepare()
    else:
        pass
    $ monika_chr.wear_acs(gt_acs_playermug)

    if persistent._has_coffee == True:
        m 1eua "There we go."
        m 1eub "Let me know when you get done drinking your coffee, okay?"

    elif persistent._has_prepared == True:
        m 3eub "Alright, it's brewing as we speak, so it should be ready in a few minutes."
        if not persistent.seen_playermug:
            m 1rkblsdla ".{w=0.5}.{w=0.5}."
            m 3rkblsdlb "As you can see, I put out an extra cup on the desk."
            m 2ekbfa "I thought it might help it feel more like we are drinking our coffee together."
            m 7hkbfsdlb "I hope that doesn't sound too cheesy."
            m 1mkbfa "Anyway..."
            $ persistent.seen_playermug = True
        else:
            pass
        m 1eub "Let me know when you get done drinking your coffee, okay?"

    else:
        m 1eub "I'm back~{w=1}{nw}"
        m 3eua "You can press the option on screen to let me know when you get back, too.{nw}"

        $ _history_list.pop()
        menu:
            m "You can press the option on screen to let me know when you get back, too.{fast}"

            "I'm back!":
                m 1hub "Welcome back, [mas_get_player_nickname()]!"
                if not persistent.seen_playermug:
                    m 1rkblsdla ".{w=0.5}.{w=0.5}."
                    m 3rkblsdlb "As you can see, I put out an extra cup on the desk."
                    m 2ekbfa "I thought it might help it feel more like we are drinking our coffee together."
                    m 7hkbfsdlb "I hope that doesn't sound too cheesy."
                    m 1mkbfa "Anyway..."
                    $ persistent.seen_playermug = True
                else:
                    pass
                m 3eub "My coffee has been brewing while you were gone, so it should be ready soon."
                m 1eub "Let me know when you get done drinking yours, okay?"

    $ persistent._is_drinking_coffee = True

$ mas_idle_mailbox.send_idle_cb("drink_together_callback")
return "idle"

label drink_together_callback:
    $ mas_gainAffection(3, bypass=False)

    if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_drink_coffee"):
        m 1eub "Done drinking your coffee, [mas_get_player_nickname()]?"
    else:
        m 2wuo "You sure drank that fast!"
        m 1lka "I hope you didn't burn your tongue..."
    m 3eua "I'll go put this cup back in the cupboard."
    if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
        m "I'm not quite done drinking my coffee yet, so I'll put my cup away later."
    $ monika_chr.remove_acs(gt_acs_playermug)
    call mas_transition_to_emptydesk
    pause 5.0
    call mas_transition_from_emptydesk
    m 1hua "I'm back!"
    m 1ekbsu "Thank you for wanting to spend time with me like this."

    $ persistent.amount_of_coffees += 1
    $ persistent.amount_of_coffees_time = datetime.datetime.now()

    $ persistent._is_drinking_coffee = False
return
