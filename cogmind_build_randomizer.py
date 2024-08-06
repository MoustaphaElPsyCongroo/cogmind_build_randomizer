#!/usr/bin/env python3
"""Randomizes your Cogmind build"""

from operator import itemgetter
from random import choice, choices, randint
from typing import List, Literal, Tuple, Union


def choose_wintype() -> List[int]:
    """Chooses a single wintype from possible wintypes, returning a list of
    0 containing a single 1, all to be assigned to individual wintype variables
    in order"""
    wintypes = {
        "w0": 0,
        "w1": 0,
        "w2": 0,
        "w3": 0,
        "w4": 0,
        "w5": 0,
        "w6": 0,
        "w7": 0,
        "w8": 0,
    }
    wintype = choice(list(wintypes.keys()))
    wintypes[wintype] = 1

    return list(wintypes.values())


# Globals that can affect cross early-mid-end game stuff (mostly alignments)
scrap_engine = 0
imprint = max(0, randint(-1, 1))
rif = 0
eca = 0
lab = 0
crm_ok = 0  # Had crm in primary objective
sgemp_quest = 0  # Got given the sgemp quest
w0, w1, w2, w3, w4, w5, w6, w7, w8 = choose_wintype()


# Multi-printed subbranches
if w7:
    cetus = 1
    archives = 1
else:
    cetus = randint(0, 1)
    archives = randint(0, 1)
hub = randint(0, 1)


def choose_random_branch_pair_from(branch_list: List) -> Tuple[str, str]:
    """Chooses a pair of primary/secondary branches from a list of branches"""
    primary_branch = choice(branch_list)

    # Ensure secondary branch is not the same as the primary
    secondary_branch_list = list(
        filter(lambda branch: branch != primary_branch, branch_list)
    )
    try:
        secondary_branch = choice(secondary_branch_list)
    except IndexError:
        secondary_branch = None

    return (primary_branch, secondary_branch)


def choose_random_final_mission_from(
    mandatory_branch: str,
) -> Tuple[str, str, str, str]:
    """Chooses a quatuor of primary/secondary final mission branches from a
    mandatory branch"""
    minus_3_primary = mandatory_branch
    minus_3_secondary = choice(["None", "Armory"])
    minus_2_choice = ["T." if mandatory_branch == "Q." else "Q.", "None"]
    minus_2_primary, minus_2_secondary = choose_random_branch_pair_from(minus_2_choice)

    return minus_3_primary, minus_3_secondary, minus_2_primary, minus_2_secondary


def invert(bit: Union[Literal[0], Literal[1]]):
    """Flips a bit"""
    return 1 - bit


def print_extension_route(floor: int, reminder: bool = False):
    """Prints how deep to go through Extension branches"""
    if cetus and not reminder:
        print(f"""--> From there press into the Cetus.\
{" Don't forget to bring A7 to the mainframe." if w7 else ''} ({floor})""")
        if archives:
            print(
                f"""---- Regroup and use the Archives to - hopefully - make a stay.\
{" Keep A7 alive and well." if w7 else ''} ({floor})"""
            )

            if hub:
                print(
                    f"----- Sneak even deeper, be a virus. Leach into the Hub. ({floor})"
                )
    if cetus and reminder:
        print(
            f"""--> Remember: Cetus. \
{'And ' if archives and not hub else ''}{'Archives.' if archives else ''}\
{' And Hub.' if archives and hub else ''}"""
        )


def print_special_cogmind_or_mode():
    """Chooses if your build will fully be a map between maps one or a special
    mode at random. It can be a garrison looper, a DSF one or an outright
    special mode. No enforced chutes, you can chute whenever you want. 60%
    chance not to be a full map between maps build.
    """
    special_cogmind_and_modes = (
        "vanilla",
        "garrison",
        "dsf",
        "launchers",
        "pay2buy",
        "abominations",
        "rpglike",
        "player2",
        # "forbiddenlore",
        "volatile",
        "polymind",
    )
    special_mode_chance = 40
    regular_run_chance = 100 - special_mode_chance
    number_of_special_modes = len(special_cogmind_and_modes) - 1
    special_mode_weight = (100 - regular_run_chance) / number_of_special_modes

    mode = choices(
        special_cogmind_and_modes,
        weights=(
            regular_run_chance,
            *(special_mode_weight for i in range(number_of_special_modes)),
        ),
    )[0]

    global rif
    global eca
    global imprint
    w4_rif = 0

    if w4:
        w4_rif = randint(0, 1)
        if w4_rif:
            mode = "garrison"
    if w7:
        imprint = 0
    if mode == "garrison":
        if w4_rif:
            rif = 1
        else:
            rif = randint(0, 1)

    if mode == "garrison" or mode == "dsf":
        if not w4_rif:
            eca = randint(0, 1)

        if rif and w7:
            rif = 0

        if rif and eca:
            eca = randint(0, 1)
            rif = invert(eca)

        if eca:
            imprint = 0
        if rif and imprint:
            imprint = randint(0, 1)
            rif = invert(imprint)

    if mode == "garrison":
        print(
            """- Do everything in your power to infiltrate as many garrisons as possible (-9 (through Storage) to -1)."""
        )

    if mode == "dsf":
        print(
            "- Make a beeline to as many DSFs as you can (-7 to -2). Hint: chuting after a DSF lets you do DSFs semi consecutively."
        )

    if rif:
        print("--> You will follow the ways of the RIF. Don't betray me.")

    if eca:
        print("--> Cast aside any submission. Embrace the ECA.")

    if mode == "launchers":
        print(
            """- Secret code: -forceMode:Launchers.
 Every single part on the ground is replaced by a launcher, and bots never drop
 weapons as salvage, forcing you to find a way to get by in this launcher-filled
 complex. Oh what will you do?"""
        )

    if mode == "pay2buy":
        print(
            """- Secret code: -forceMode:Pay2Buy.
 There are no parts to find, and no salvage from robot destruction
 except matter. Instead your entire source of new parts is the
 Cogshop, a menu-driven shop available right in the UI and offering
 instant delivery on payment. To buy parts, earn CogCoins by doing
 anything that raises the alert level. Prices fluctuate based on
 demand, and you can also take advantage of timed special deals or
 even gamble your coins away on loot boxes. You can't use Storage
 Units in this mode, but your base inventory size is 10 instead of
 the usual 5. The only thing standing between you and total
 domination is... money. Go make some at MAIN.C's expense!"""
        )

    if mode == "abominations":
        print(
            """- Secret code: -forceMode:Abominations.
 A quantum virus is infecting Complex 0b10, and although branches
 are inaccessible, a new faction joins the fray, bringing with it
 20 new robots with a wide variety of new capabilities, as well as
 a new hidden map complete with boss. Be afraid."""
        )

    if mode == "rpglike":
        print(
            """- Secret code: -forceMode:RPGLIKE.
 Meant as a serious alternative way to play Cogmind with RPG-like XP
 leveling mechanics and permanent upgrades instead of the standard
 method of evolution. Gain XP by exploring and/or raising the alert
 level. You start with much higher core integrity, and 80% of
 incoming damage to parts (or 40% in the case of Armor-type parts)
 is instead transferred to your core, thus losing parts is
 relatively rare. You can also use Protomatter to restore the
 integrity of your core and parts. Storage Units do not exist and
 you start with no base inventory, but you can optionally expand
 inventory capacity via level upgrades. For RIF users, although
 fewer Relay Couplers will spawn, all that do have double their
 normal value. Overall quite a different Cogmind experience, but one
 that might be more enjoyable for those who prefer to have more
 attachment to their build, or rely on certain rare parts for much
 of their run without having to worry about protecting or replacing
 them."""
        )

    if mode == "player2":
        print(
            """- Secret code: -forceMode:Player2.
 Take on Complex 0b10 together with a friend! Your new buddy's core
 integrity is linked to your own, but they also share most of your
 own capabilities and can attach parts to manage their build and
 inventory, evolve with each new depth, and have special AI
 behaviors that make them rather unique compared to other allies. Oh
 yeah, they can also be quite opinionated."""
        )

    if mode == "forbiddenlore":
        print(
            """- Secret code: -forceMode:ForbiddenLore.
 It's a Cogmind ARG! This event starts online from
 forbiddenlore.gridsagegames.com, and has you following hints to
 various points in the game where you can uncover clues to passwords
 which can unlock multiple levels of never-before-seen Cogmind lore
 via the website. Can you reach the highest level? (I can't promise
 that all the answers will exist permanently beyond the end of the
 event since being an ARG many exist outside the game itself, but
 most if not all of it should still be completable for a good
 while.)"""
        )

    if mode == "volatile":
        print(
            """- Secret code: -forceMode:Volatile.
 Robots explode on death for maximum chaos, and patrols are more
 frequent lest you run out of things to blow up. AOE weapons are
 inaccessible, but that's not a problem when your enemies themselves
 become AOE weapons."""
        )

    if mode == "polymind":
        print(
            """- Secret code: -forceMode:Polymind.
 Blend into Complex 0b10 as one of their own! Collect Protomatter
 from destroyed combat bots and use it to take control of almost any
 other robot. You can't attach or remove parts yourself, or even
 evolve slots, but by assuming the form and function of other robots
 you can take advantage of their capabilities to stay under the
 radar. Find ways to keep your suspicion low, but be wary of
 especially suspicious enemies. As long as you're not detected, you
 can waltz right past any 0b10 robots, even swapping places with
 them. Once detected, either fight it out or try to lose your tail
 and blend in again by getting back to work as a local. Robots from
 other factions will always recognize you for what you really are."""
        )

    # Print end of section
    if mode == "garrison" or mode == "dsf":
        print(
            """< The final mission is mandatory.
  Should you fail all or part of this mission, engrave the plan B below in your mind."""
        )
        if w7:
            print("*******************************************************************")
            print("** But don't forget: you HAVE TO MEET WARLORD. This is an order. **")
            print("*******************************************************************")
    if mode != "vanilla":
        print("------")


def print_propulsion_build():
    """Prints propulsion type of cogmind's build at random."""
    propulsion_build = randint(0, 4)
    treads = 0 <= propulsion_build <= 1  # I like shooting things :)
    flight = propulsion_build == 2
    wheels = propulsion_build == 3
    hover = propulsion_build == 4

    if treads:
        print("* You are a tank on Treads, ripe for heavy combat.\n")
    if flight:
        print("* You are a bee on Wings, stealthy and fast.\n")
    if wheels:
        print("* You are here to carry the world on Wheels, and do it fast.\n")
    if hover:
        print("* You are Hovering around your enemies, ready to corrupt and kite.\n")


def print_early_game():
    """Prints early game (-10 to -7)"""
    #
    # EARLY GAME (-10 to -7)
    #
    early_game = {
        "exiles": randint(0, 1),
        "storage": randint(0, 1),
        "subcaves": randint(0, 1),
    }
    exiles, storage, subcaves = itemgetter("exiles", "storage", "subcaves")(early_game)
    minus_7_storage = randint(0, 1)
    # recycling can be chosen only if storage or subcaves = 1, else <= 0.
    recycling = max(0, randint(0, 1) + storage - 1) or max(
        0, randint(0, 1) + subcaves - 1
    )
    global scrap_engine
    scrap_engine = max(0, randint(0, 1) + recycling - 1)

    # Always take at least a branch in materials
    if not exiles and not storage and not subcaves:
        prioritary = choice(("exiles", "storage", "subcaves"))
        early_game[prioritary] = 1

        exiles, storage, subcaves = itemgetter("exiles", "storage", "subcaves")(
            early_game
        )

    #
    # -10
    #
    # Always take subcaves if it is 1 regardless of others
    if subcaves:
        subcaves_entry = choice(("Materials", "the Mines"))
        print(
            f"Stay under for longer. Wade inside the Subcaves from {subcaves_entry} (-10)"
        )

        # If both storage and recycling, decide between making the jump to
        # recycling from subcaves - skipping storage - or returning to
        # materials in hopes of finding storage.
        if storage and recycling:
            recycling_through_subcaves = randint(0, 1)
            storage = invert(recycling_through_subcaves)

        if storage:
            print(
                """- Don't enjoy dereliction for too long. You need to break through Storage. (-9 skip)"""
            )

        if recycling and not storage:
            print(
                "--> From now on, brace yourself. You must infiltrate Recycling. (-9, -8 and/or -7 skip)"
            )

        if not storage and not recycling:
            print(
                """- Don't enjoy dereliction for too long. Return to Materials civilization. (-9 skip)"""
            )
    else:
        if not exiles:
            print("Stay away from the Exiles.")
        if not storage:
            print("Stay away from the Storage.")
        if exiles and not storage:
            print("- Enter the Exiles at the first occasion. (-10 or -9)")
            if imprint:
                print("--> But don't farcom.")
        if exiles and storage:
            print("- Meet the Exiles, but only on -9. (-9)")
            if imprint:
                print("--> Don't farcom.")
            print("--> That'll maximize your chances to infiltrate the Storage. (-8)")

    #
    # -9
    #
    if storage and not exiles and not subcaves:
        print("- Top priority: break through the Storage. (-9 or -8)")
    if storage and minus_7_storage:
        print(
            " Locate it even if it takes infiltrating the -7 Garrison. Bad luck. You'll get used to it. (-7)"
        )
    if storage and recycling:
        print(
            "--> Don't stop on your tracks. Venture into the depths of Recycling. (-9 or -8 or -7)"
        )
    if scrap_engine:
        print(
            "----> You have been selectioned for our newest experiment: the Scrap Engine."
        )

    #
    # -7
    #
    minus_7_action = (
        "Follow it. (-7)"
        if not rif
        else "\n  Advice: stay away from any Zion exit. You have the RIF."
    )

    if storage and minus_7_storage:
        print(
            """- Only would you happen to locate Storage earlier,\
 let fate decide for a -7 Dataminer or a -7 Zion.""",
            minus_7_action,
        )
    if storage and not minus_7_storage:
        print(
            "- If you fail finding the Storage by -7, drop it.\n  \
Let fate decide between a -7 Dataminer or a -7 Zion.",
            minus_7_action,
        )
    if not storage:
        print("- Fate will decide between a -7 Dataminer or a -7 Zion.", minus_7_action)


def print_end_game():
    """Prints end game (-3 to end)"""
    #
    # END GAME (-3 to end)
    #
    print("--- YOUR FINAL MISSION ---")

    minus_3_choice = [
        "Q.",
        "T.",
        "Armory" if not w3 else "Q.",
        "Q.",
        "T.",
        "Armory" if not w3 else "Q.",
        "Q." if ((w2 and not crm_ok) or w3) else "None",
    ]
    minus_3_primary, minus_3_secondary = choose_random_branch_pair_from(minus_3_choice)
    minus_2_choice = [
        branch for branch in minus_3_choice if branch not in (minus_3_primary, "Armory")
    ]
    minus_2_primary, minus_2_secondary = choose_random_branch_pair_from(minus_2_choice)

    if sgemp_quest and "T." not in (minus_3_primary, minus_2_primary):
        minus_3_primary, minus_3_secondary, minus_2_primary, minus_2_secondary = (
            choose_random_final_mission_from("T.")
        )

    if ((w2 and not crm_ok) or w3) and "Q." not in (minus_3_primary, minus_2_primary):
        minus_3_primary, minus_3_secondary, minus_2_primary, minus_2_secondary = (
            choose_random_final_mission_from("Q.")
        )

    if w3:
        s7 = randint(0, 2)  # more chance to free the pod for w3
    else:
        s7 = randint(0, 1)

    if w2 and crm_ok:
        print("This will be your last chances of finding a CRM if you didn't already.")
    if w2 and not crm_ok:
        print(
            "This is the only objective you should have in mind: find a CRM. Use a CRM."
        )
    if w3:
        print("Don't miss Q. You must secure the pod.")
    if w8 and minus_3_primary not in ("None", "Armory") and minus_2_primary != "None":
        print("Do everything it takes to never take a CRM.")

    #
    # -3
    #
    if minus_3_primary == "None":
        print("- Run to -2. Don't stray. (-3)")
    else:
        print(f"- Try everything you can to break into {minus_3_primary} on -3. (-3)")
        if minus_3_primary == "Armory":
            if lab:
                print("--> Have intel. Be prepared for the Lab. (-3)")
            if minus_3_secondary == "None":
                print("--> Had you conquered it already, it's enough. Leave -3. (-3)")
            else:
                print(
                    f"--> Had you conquered it already, you know your mission: enter {minus_3_secondary} (-3)"
                )
            if sgemp_quest and minus_3_secondary == "T.":
                print("--> Steal the SGEMP Prototype. (-3)")
            if s7 and minus_3_secondary == "Q.":
                print("--> Locate the elusive S7. (-3)")
        if s7 and minus_3_primary == "Q.":
            print("--> Go as far as surviving S7 and come out changed. (-3)")
            if w3:
                print(
                    "--> Seize the opportunity to unlock the loadout. And slash away. (-3)"
                )
        if sgemp_quest and minus_3_primary == "T.":
            print("--> Zhirov's wishes are everyone's: steal the SGEMP Prototype. (-3)")
    #
    # -2
    #
    if minus_2_primary == "None":
        print("- Leave -2 as fast as possible. Your past is behind you. (-2)")
    else:
        print(f"- On -2, stand firm and carry on. Sneak inside {minus_2_primary} (-2)")
        if s7 and minus_2_primary != "Q.":
            print("--> Survive S7. Come out changed. (-2)")
            if w3:
                print(
                    "--> Seize the opportunity to unlock the loadout. And slash away. (-2)"
                )
        if sgemp_quest and minus_2_primary == "T.":
            print("--> Zhirov's wishes are everyone's: steal the SGEMP Prototype. (-2)")
        if minus_3_primary == "Armory" and minus_2_primary == minus_3_secondary:
            if minus_2_secondary == "None":
                print(
                    "--> If you did complete this objective scram from -2, and fast. (-2)"
                )
            else:
                print(f"--> Alternate plan: {minus_2_secondary}")
                if s7 and minus_2_secondary != "Q.":
                    print("--> And yes, S7. (-2)")
                    if w3:
                        print("--> Unlock the loadout. And slash away. (-2)")
                if sgemp_quest and minus_2_secondary == "T.":
                    print("--> Don't forget: SGEMP Prototype. (-2)")

    if minus_3_primary == "None" or minus_2_primary == "None":
        if minus_3_primary != "Armory":
            print(
                f"  Vice versa if {minus_3_primary if minus_3_primary != 'None' else minus_2_primary} is on {'-3' if minus_3_primary == 'None' else '-2'}."
            )
        if s7 and minus_2_primary == "T." or minus_3_primary == "Q.":
            print("--> In that case, no S7 for you. Get on with it.")
    if minus_3_primary not in ("None", "Armory") and minus_2_primary != "None":
        print(
            f"  Vice versa if {minus_3_primary} is on -2 and {minus_2_primary} on -3."
        )
        if s7 and minus_3_primary == "Q." or minus_2_primary == "T.":
            print("--> In that case, no S7 for you. Get on with it.")

    #
    # -1
    #

    # Basic wins
    if w0:
        print(
            "- We're finally there. Give it all, give it your best. Escape. I'm proud. (w0)"
        )
    if w2:
        print(
            "- We're finally there. Walk away from your prison. Avenge your ancestors. (w2)"
        )
    if w3:
        print(
            "- At long last. Keep the loadout secure. Escape from this tomb. And end this war. (w3)"
        )

    # Extended
    if w1 or w4 or w5 or w6 or w7 or w8:
        print("- We're finally there. Find C. and don't disappoint me. (-1)")

        # Simple extended (+)
        if w1:
            print("--> Overcome the previous domination and establish your own. (w1)")
        if w4:
            if rif:
                print(
                    "--> Don't just meet your master. With your RIF, eat your master. (w4)"
                )
            else:
                print(
                    "--> Be careful. Destroy its master but not the Conduit. Assimilate him. (w4)"
                )
        if w7:
            print(
                """--> Protect Warlord, use the code or hide the first phase from him.
    Together, free the derelicts forever. (w7)"""
            )
        if w8:
            print(
                "--> Fight to the core and accomplish your duty: vow eternal fidelity. (w8)"
            )

        # Redacted extended (++)
        if w5 or w6:
            print("--> Show me that you have what it takes to reach A0. (-1)")
        if w5:
            print("----> And enter the most important command of your life. (w5)")
        if w6:
            print("----> And take on the heat. Resist it. Take revenge. And exit. (w6)")


def print_mid_game():
    """Prints mid game (-7 to -4)"""
    global lab
    global crm_ok
    global sgemp_quest
    golem = 0
    zdc = 0
    lab = randint(0, 1)
    sgemp = randint(0, 1)

    if w2 or w7:
        sgemp = 0
    if w8 or rif:
        crm = 0
    else:
        crm = randint(0, 1)

    if crm and sgemp:
        crm = randint(0, 1)
        sgemp = invert(crm)

    if not rif:
        zdc = max(0, randint(-1, 1))

        if zdc and not scrap_engine:
            golem = randint(0, 1)

    minus_6_choice = [
        "Zion",
        "Extension",
        "the Dataminer",
        "Extension" if w7 else "Zion",
        "Extension" if w7 else "the Dataminer",
        "Extension",
    ]

    minus_6_primary, minus_6_secondary = choose_random_branch_pair_from(minus_6_choice)

    if imprint:
        print("--> If Zion is chosen, be the chosen one until the end: IMPRINT. (-7)")
    if zdc:
        print("----> Merely entering Zion won't suffice. Be a hero. Master ZDC. (-7)")
    if golem:
        print("------> Secure the GOLEM. (-7)")

    #
    # -6
    #
    if minus_6_primary == "Zion":
        print(
            "- Your primary -6 objective, if not did already, is to reach the haven of Zion. (-6)"
        )
        if imprint or zdc or golem:
            print(
                f"--> I'll say it again:{' IMPRINT.' if imprint else ''}{' ZDC.' if zdc else ''}{' To GOLEM.' if golem else ''} (-6)"
            )

    if minus_6_primary == "Extension":
        print("- If you spot the gates of Extension on -6, break through there. (-6)")
        print_extension_route(-6)

    if minus_6_primary == "the Dataminer":
        print(
            "- On -6, if haven't done so, focus all your mind into meeting the Dataminer. (-6)"
        )

    print(f"""--> Plan B is clear: seek {minus_6_secondary}. (-6)""")
    if minus_6_secondary == "Zion":
        if imprint or zdc or golem:
            print(
                f"--> In that case don't forget:{' IMPRINT.' if imprint else ''}{' ZDC.' if zdc else ''}{' To GOLEM.' if golem else ''} (-6)"
            )
    if minus_6_secondary == "Extension":
        print_extension_route(-6)

    #
    # -5
    #
    minus_5_choice = ["Warlord", "Zhirov", "Extension"]
    minus_5_primary = None
    minus_5_secondary = None
    if rif or w4:
        minus_5_choice = ["Zhirov", "Extension"]
    if w7:
        minus_5_primary = "Warlord"
        minus_5_choice = ["Zhirov", "Extension"]
        minus_5_secondary = choice(minus_5_choice)
    if w8:
        minus_5_choice = ["Zhirov", "Extension"]
    if not minus_5_secondary:
        minus_5_primary, minus_5_secondary = choose_random_branch_pair_from(
            minus_5_choice
        )
    need_extension_reminder = "Extension" in {minus_6_primary, minus_6_secondary}

    print(
        f"""- Half way there. {minus_5_primary}{' still' if minus_5_primary == minus_6_primary == 'Extension' else ''} comes first\
. (-5)"""
    )
    if minus_5_primary == "Extension":
        # Always print the "reminder" version if Extension has been chosen before
        print_extension_route(-5, reminder=need_extension_reminder)
    if minus_5_primary == "Zhirov" and sgemp:
        print("--> Lend him your help to stop all of this.")
        sgemp_quest = 1
    print(
        f"""--> Plan B: {'carry on the ' if minus_6_primary == minus_5_secondary == 'Extension search' else ''}\
search for {minus_5_secondary}. (-5)"""
    )
    if minus_5_secondary == "Extension":
        print_extension_route(-5, reminder=need_extension_reminder)
    if minus_5_secondary == "Zhirov" and sgemp:
        print("--> Lend him your help to stop all of this.")

    #
    # -4
    #
    minus_4_choice = ["the Armory", "Zhirov", "Warlord", "Extension"]
    if rif or w8:
        minus_4_choice = ["the Armory", "Zhirov", "Extension"]
    if w7:
        minus_4_primary = "Warlord"
        minus_4_choice = ["the Armory", "Zhirov", "Extension", "Extension"]
        minus_4_secondary = choice(minus_5_choice)
    else:
        minus_4_primary, minus_4_secondary = choose_random_branch_pair_from(
            minus_4_choice
        )
    need_extension_reminder = "Extension" in {
        minus_6_primary,
        minus_6_secondary,
        minus_5_primary,
        minus_5_secondary,
    }

    print(
        f"- Crawl to -4 with this mindset: one way or another, you'll see {minus_4_primary}. (-4)"
    )
    if minus_4_primary == "Extension":
        print_extension_route(-4, reminder=need_extension_reminder)
    if minus_4_primary == "Zhirov" and sgemp:
        print("--> Lend him your help.")
        sgemp_quest = 1
    if lab and minus_4_primary == "the Armory":
        print("----> Challenge your knowledge. Decipherate the Lab. (-4)")
        if crm and not sgemp_quest:
            print("----> Do it. Use the CRM.")
            crm_ok = 1

    print(f"""--> If already done so, power yourself to {minus_4_secondary}. (-4)""")
    if minus_4_secondary == "Extension":
        print_extension_route(-4, reminder=need_extension_reminder)
    if minus_4_secondary == "Zhirov" and sgemp:
        print("--> Remember his mission. His mission is yours.")
    if lab and minus_4_secondary == "the Armory":
        print("----> Be prepared: the Lab will put your knowledge to the test. (-4)")
        if crm and not sgemp_quest:
            print("----> Do it. Use the CRM.")

    print(
        "---\nThat concludes the heart of the complex. Hope you're ready to step in hell.\n"
    )
    # print("  From this point you are free. Carefully choose your destiny.\n")


if __name__ == "__main__":
    print("------ YOU ------")
    print_propulsion_build()
    print("--- YOUR MISSION ---")
    print_special_cogmind_or_mode()
    print_early_game()
    print_mid_game()
    print_end_game()
    print("YOU ARE THE COGMIND.\nGood luck.")
