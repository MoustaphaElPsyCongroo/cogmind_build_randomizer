#!/usr/bin/env python3
"""Randomizes your Cogmind build"""

from operator import itemgetter
from random import choice, choices, randint
from typing import List, Literal, Tuple, Union

# Globals that can affect cross early-mid-end game stuff (mostly alignments)
scrap_engine = 0
imprint = 0
rif = 0
eca = 0

# Multi-printed subbranches
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
    secondary_branch = choice(secondary_branch_list)

    return (primary_branch, secondary_branch)


def invert(bit: Union[Literal[0], Literal[1]]):
    """Flips a bit"""
    return 1 - bit


def print_extension_route(floor: int, reminder: bool = False):
    """Prints how deep to go through Extension branches"""
    if cetus and not reminder:
        print(f"""--> From there press into the Cetus. ({floor})""")
        if archives:
            print(
                f"---- Regroup and use the Archives to - hopefully - make a stay. ({floor})"
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
        # "dsf",
        "launchers",
        "pay2buy",
        "abominations",
        "rpglike",
        "player2",
        "forbiddenlore",
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

    if mode == "garrison":
        rif = randint(0, 1)

    if mode == "garrison" or mode == "dsf":
        eca = randint(0, 1)

        if rif and eca:
            eca = randint(0, 1)
            rif = invert(eca)

    if mode == "garrison":
        print(
            "- Do everything in your power to infiltrate as many garrisons as possible (-9 (through Storage) to -1)."
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
            "< Should you fail all or part of this mission, engrave this plan B in your mind:\n------"
        )
    elif mode != "vanilla":
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
            print(
                "- Take the Exiles wherever you see them. You'll need them. (-10 or -9)"
            )
        if exiles and storage:
            print("- Take the Exiles help, but only on -9. (-9)")
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
    print("  But should you want an outline until the end, listen.\n------")

    minus_3_choice = ["Q.", "T.", "Q.", "T.", "None"]
    minus_3_q_or_t = choice(minus_3_choice)
    minus_2_q_or_t = choice(
        [branch for branch in minus_3_choice if branch != minus_3_q_or_t]
    )
    s7 = randint(0, 1)

    if minus_3_q_or_t == "None":
        print("- Run to -2. Don't stray. (-3)")
    else:
        print(f"- Try everything you can to break into {minus_3_q_or_t} on -3. (-3)")
        if s7 and minus_3_q_or_t == "Q.":
            print("--> Go as far as surviving S7 and come out changed. (-3)")

    if minus_2_q_or_t == "None":
        print("- Leave -2 as fast as possible. Your past is behind you. (-2)")
    else:
        print(f"- On -2, stand firm and carry on. Sneak inside {minus_2_q_or_t} (-2)")
        if s7 and minus_3_q_or_t != "Q.":
            print("--> Go as far as surviving S7 and come out changed. (-2)")

    if minus_3_q_or_t == "None" or minus_2_q_or_t == "None":
        print(
            f"  Vice versa if {minus_3_q_or_t if minus_3_q_or_t != 'None' else minus_2_q_or_t} is on {'-3' if minus_3_q_or_t == 'None' else '-2'}."
        )
    if minus_3_q_or_t != "None" and minus_2_q_or_t != "None":
        print(f"  Vice versa if {minus_3_q_or_t} is on -2 and {minus_2_q_or_t} on -3.")

    extended = randint(0, 1)
    a0 = randint(0, 1)
    extended_win = choice(("w5", "w6"))

    if not extended:
        print("- Leave -1 as soon as possible. Not bad. (-1)")
    if extended:
        print("- C. will await you. Don't disappoint me. (-1)")
        if a0:
            print("--> Show me that you have what it takes to reach A0. (-1)")
            if extended_win == "w5":
                print("----> And enter the most important command of your life. (-1)")
            if extended_win == "w6":
                print(
                    "--> And take on the heat. Resist it. Take revenge. And exit. (-1)"
                )


def print_mid_game():
    """Prints mid game (-7 to -4)"""
    global imprint
    global scrap_engine
    golem = 0
    zdc = 0

    minus_6_choice = ["Zion", "Extension", "the Dataminer"]
    if rif:
        minus_6_choice = ["Extension", "the Dataminer"]
    if not rif:
        if not eca:
            imprint = max(0, randint(-2, 1))
        zdc = max(0, randint(-1, 1))

        if zdc and not scrap_engine:
            golem = randint(0, 1)

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

    print(
        f"""--> You have a plan B should {minus_6_primary} not be on -6:\
 seek {minus_6_secondary}. (-6)"""
    )
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
    if rif:
        minus_5_choice = ["Zhirov", "Extension"]
    minus_5_primary, minus_5_secondary = choose_random_branch_pair_from(minus_5_choice)
    need_extension_reminder = "Extension" in {minus_6_primary, minus_6_secondary}

    print(
        f"""- -5. Half way there. {minus_5_primary}{' still' if minus_5_primary == minus_6_primary == 'Extension' else ''} comes first\
. (-5)"""
    )
    if minus_5_primary == "Extension":
        # Always print the "reminder" version if Extension has been chosen before
        print_extension_route(-5, reminder=need_extension_reminder)
    print(
        f"""--> Plan B: {'carry on to ' if minus_6_primary == minus_5_secondary == 'Extension' else ''}\
search for {minus_5_secondary}. (-5)"""
    )
    if minus_5_secondary == "Extension":
        print_extension_route(-5, reminder=need_extension_reminder)

    #
    # -4
    #
    minus_4_choice = ["the Armory", "Zhirov", "Warlord", "Extension"]
    if rif:
        minus_4_choice = ["the Armory", "Zhirov", "Extension"]
    minus_4_primary, minus_4_secondary = choose_random_branch_pair_from(minus_4_choice)
    need_extension_reminder = "Extension" in {
        minus_6_primary,
        minus_6_secondary,
        minus_5_primary,
        minus_5_secondary,
    }
    lab = randint(0, 1)

    print(
        f"\n- Crawl to -4 with this mindset: one way or another, you'll see {minus_4_primary}. (-4)"
    )
    if minus_4_primary == "Extension":
        print_extension_route(-4, reminder=need_extension_reminder)
    if lab and minus_4_primary == "the Armory":
        print("----> Challenge your knowledge. Decipherate the Lab. (-4)")
    print(f"""--> If already done so, power yourself to {minus_4_secondary}. (-4)""")
    if minus_4_secondary == "Extension":
        print_extension_route(-4, reminder=need_extension_reminder)
    if lab and minus_4_secondary == "the Armory":
        print("----> Be prepared: the Lab will put your knowledge to the test. (-4)")

    print(
        "---\n- That concludes the heart of the complex. Hope you're ready to step in hell."
    )
    print("  From this point you are free. Carefully choose your destiny.\n")


if __name__ == "__main__":
    print("------ YOU ------")
    print_propulsion_build()
    print("--- YOUR MISSION ---")
    print_special_cogmind_or_mode()
    print_early_game()
    print_mid_game()
    print_end_game()
    print("YOU ARE THE COGMIND.\nGood luck.")
